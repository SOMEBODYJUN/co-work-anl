"""Repository-scoped GitHub resources using the same external PAT as work.py."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from curation import _safe_path


class APIError(RuntimeError):
    def __init__(self, status, message):
        self.status = status
        super().__init__('GitHub HTTP %s: %s' % (status, message))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise APIError(code, 'Redirect refused; credentials stay on api.github.com')


class Client:
    def __init__(self, root, token_file):
        self.root = root
        remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], cwd=root, text=True).strip()
        match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?', remote)
        if not match: raise ValueError('Use a credential-free GitHub origin; no custom API destinations')
        self.repository = match[1] + '/' + match[2]
        credential = Path(token_file).resolve()
        if credential.is_relative_to(root.resolve()): raise ValueError('Credential file must stay outside the clone')
        tokens = set(re.findall(rb'(?:github_pat_|ghp_)[A-Za-z0-9_]{12,}', credential.read_bytes()))
        if len(tokens) != 1: raise ValueError('Expected one external GitHub PAT')
        self._token = tokens.pop().decode()
        self._opener = urllib.request.build_opener(NoRedirect())

    def request(self, method, path, payload=None):
        if not path.startswith('/') or path.startswith('//') or '\\' in path:
            raise ValueError('Invalid fixed GitHub API path')
        request = urllib.request.Request('https://api.github.com' + path,
            data=json.dumps(payload).encode() if payload is not None else None, method=method,
            headers={'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer ' + self._token,
                     'X-GitHub-Api-Version': '2026-03-10', 'User-Agent': 'co-work-research-tools', 'Content-Type': 'application/json'})
        try:
            with self._opener.open(request, timeout=30) as response:
                body = response.read()
                return json.loads(body) if body else {'http_status': response.status}
        except urllib.error.HTTPError as exc:
            try: message = json.loads(exc.read()).get('message', 'Request rejected')
            except (ValueError, OSError): message = 'Request rejected'
            message = str(message).replace(self._token, '[REDACTED]')
            raise APIError(exc.code, message) from None
        except urllib.error.URLError as exc:
            raise APIError('network', str(exc.reason).replace(self._token, '[REDACTED]')) from None

    def repo_path(self, suffix=''):
        return '/repos/' + self.repository + suffix

    def status(self):
        repo = self.request('GET', self.repo_path())
        result = {'repository': repo['full_name'], 'default_branch': repo['default_branch'],
                  'repository_permissions': repo.get('permissions', {}), 'student_verification': 'not-inferred-from-repository-access',
                  'resource_operations': {}, 'mutations_performed': 0}
        for name, suffix, key in [('workflows', '/actions/workflows?per_page=100', 'workflows'), ('codespaces', '/codespaces?per_page=100', 'codespaces')]:
            try:
                value = self.request('GET', self.repo_path(suffix))
                fields = ('id', 'name', 'path', 'state') if name == 'workflows' else ('name', 'state', 'web_url')
                result['resource_operations'][name] = {'status': 'readable', 'items': [{k: row[k] for k in fields if k in row} for row in value.get(key, [])],
                                                       'total_count': value.get('total_count'), 'write_permission': 'not-tested'}
            except APIError as exc:
                if exc.status == 401: raise
                result['resource_operations'][name] = {'status': 'unavailable', 'http_status': exc.status, 'detail': str(exc)}
        return result

    def dispatch(self, workflow, ref, inputs):
        if workflow not in {'research-checks.yml', 'research-compute.yml'}:
            raise ValueError('Only the two repository research workflows are supported')
        if not isinstance(inputs, dict) or len(inputs) > 10 or any(not isinstance(k, str) or not isinstance(v, (str, bool, int)) for k, v in inputs.items()):
            raise ValueError('Workflow inputs must be a small explicit JSON object')
        result = self.request('POST', self.repo_path('/actions/workflows/' + workflow + '/dispatches'), {'ref': ref, 'inputs': inputs})
        return {'status': 'dispatch-request-accepted', 'response': result, 'workflow': workflow, 'ref': ref,
                'limit': 'Dispatch acceptance is not a completed or passed run; check the actual Actions run separately'}

    def machines(self, ref):
        return self.request('GET', self.repo_path('/codespaces/machines?ref=' + urllib.parse.quote(ref, safe='')))

    def create(self, ref, machine):
        available = self.machines(ref)
        if machine not in {row['name'] for row in available.get('machines', [])}: raise ValueError('Choose an actual available machine from github machines')
        result = self.request('POST', self.repo_path('/codespaces'), {'ref': ref, 'machine': machine, 'devcontainer_path': '.devcontainer/devcontainer.json'})
        return {'status': 'codespace-create-request-accepted', 'name': result.get('name'), 'state': result.get('state'), 'web_url': result.get('web_url'),
                'limit': 'Creating a codespace consumes account resources; this is not a model or student-benefit activation'}

    def stop(self, name):
        if not re.fullmatch(r'[A-Za-z0-9-]+', name): raise ValueError('Invalid codespace name')
        path = '/user/codespaces/' + name
        info = self.request('GET', path)
        if info.get('repository', {}).get('full_name', '').casefold() != self.repository.casefold():
            raise ValueError('This codespace belongs to another repository')
        return {'status': 'codespace-stop-request-accepted', 'name': name, 'response': self.request('POST', path + '/stop', {})}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--repo', type=Path, required=True)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('status')
    q = sub.add_parser('dispatch'); q.add_argument('--workflow', required=True); q.add_argument('--ref', required=True); q.add_argument('--inputs-file')
    q = sub.add_parser('machines'); q.add_argument('--ref', required=True)
    q = sub.add_parser('create-codespace'); q.add_argument('--ref', required=True); q.add_argument('--machine', required=True)
    q = sub.add_parser('stop-codespace'); q.add_argument('name')
    a = p.parse_args(argv); root = a.repo.resolve()
    token_file = os.environ.get('WCG_CHECKPOINT_TOKEN_FILE') or subprocess.run(['git', 'config', '--local', '--get', 'wcg.tokenFile'], cwd=root, capture_output=True, text=True).stdout.strip()
    if not token_file: raise ValueError('Use work.py --token-file with an external PAT; no account-link connector is needed')
    client = Client(root, token_file)
    if a.command == 'status': result = client.status()
    elif a.command == 'dispatch': result = client.dispatch(a.workflow, a.ref, json.loads(_safe_path(root, a.inputs_file).read_text()) if a.inputs_file else {})
    elif a.command == 'machines': result = client.machines(a.ref)
    elif a.command == 'create-codespace': result = client.create(a.ref, a.machine)
    else: result = client.stop(a.name)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


if __name__ == '__main__':
    try: raise SystemExit(main())
    except (ValueError, OSError, KeyError, APIError) as exc: raise SystemExit(str(exc))
