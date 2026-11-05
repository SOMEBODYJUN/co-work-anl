"""Repository-scoped GitHub resources using the same external PAT as work.py."""
import argparse
import base64
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from curation import _safe_path
from compute import request as compute_request


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
        if workflow != 'research-compute.yml':
            raise ValueError('Only the registered mathematical compute workflow is supported')
        if not isinstance(inputs, dict) or len(inputs) > 10 or any(not isinstance(k, str) or not isinstance(v, (str, bool, int)) for k, v in inputs.items()):
            raise ValueError('Workflow inputs must be a small explicit JSON object')
        readiness=self.workflow_status(workflow,ref)
        if not readiness['manual_dispatch_ready']:
            raise ValueError('Manual dispatch needs this workflow on the default branch and requested ref. Use compute request plus a branch checkpoint for ordinary computation.')
        result = self.request('POST', self.repo_path('/actions/workflows/' + workflow + '/dispatches'), {'ref': ref, 'inputs': inputs})
        return {'status': 'dispatch-request-accepted', 'response': result, 'workflow': workflow, 'ref': ref,
                'limit': 'Dispatch acceptance is not a completed or passed run; check the actual Actions run separately'}

    def workflow_status(self, workflow, ref):
        if workflow not in {'research-checks.yml', 'research-compute.yml'}:
            raise ValueError('Unknown research workflow')
        repo = self.request('GET', self.repo_path())
        result = {'repository': self.repository, 'default_branch': repo['default_branch'], 'workflow': workflow,
                  'ref': ref, 'mutations_performed': 0}
        for label, branch in [('default_branch_file', repo['default_branch']), ('requested_ref_file', ref)]:
            path = '/contents/.github/workflows/'+workflow+'?ref='+urllib.parse.quote(branch, safe='')
            try:
                value = self.request('GET', self.repo_path(path))
                source=base64.b64decode(value.get('content','')).decode('utf-8',errors='replace') if value.get('encoding')=='base64' else ''
                result[label] = {'exists': True, 'sha': value.get('sha'),
                                 'declares_compute_request_path':'research/compute-requests/' in source}
            except APIError as exc:
                if exc.status != 404: raise
                result[label] = {'exists': False}
        result['manual_dispatch_ready'] = result['default_branch_file']['exists'] and result['requested_ref_file']['exists']
        result['branch_push_route'] = {'declared_on_requested_ref':result['requested_ref_file'].get('declares_compute_request_path',False),
            'enablement':'Push the prepared request workflow/tools to rebuild/research-v2 before an actual explicit computation request. Only newly added research/compute-requests/*.json request calculation; no run has been started by this read.'}
        return result

    def jobs(self, run_id):
        if not str(run_id).isdigit(): raise ValueError('Use the actual numeric Actions run ID')
        rows=[];page=1
        while True:
            value=self.request('GET',self.repo_path('/actions/runs/'+str(run_id)+'/jobs?filter=latest&per_page=100&page='+str(page)))
            rows.extend(value.get('jobs',[]))
            if len(value.get('jobs',[]))<100: return rows
            page+=1

    def runs(self, ref=None, request_id=None, head=None, limit=20, workflow='research-compute.yml'):
        if not 1<=limit<=100:raise ValueError('Choose 1..100 recent runs')
        query={'per_page':limit}
        if ref:query['branch']=ref
        if head:query['head_sha']=head
        rows=self.request('GET',self.repo_path('/actions/runs?'+urllib.parse.urlencode(query))).get('workflow_runs',[])
        result=[]
        for row in rows:
            if row.get('path','').split('@')[0]!='.github/workflows/'+workflow:continue
            item={k:row.get(k) for k in ['id','name','event','status','conclusion','head_branch','head_sha','html_url','created_at','updated_at','run_attempt']}
            if request_id:
                jobs=self.jobs(row['id']);matched=[j for j in jobs if j.get('name')=='compute/'+request_id]
                item['request_jobs']=[{k:j.get(k) for k in ['id','name','status','conclusion','html_url']} for j in matched]
                item['request_id']=request_id
                if not matched and not head:continue
                if not matched:item['request_correlation']='Exact push SHA matches; preparation may still be pending or have failed. Inspect this run.'
            result.append(item)
        return {'runs':result,'request_id':request_id,'head_sha':head,'mutations_performed':0,
                'note':'An empty listing is not completion. Pin --head to the checkpoint commit to find queued or failed preparation before a request job appears.'}

    def run_status(self, run_id):
        if not str(run_id).isdigit():raise ValueError('Use the actual numeric Actions run ID')
        row=self.request('GET',self.repo_path('/actions/runs/'+str(run_id)))
        result={k:row.get(k) for k in ['id','name','event','status','conclusion','head_branch','head_sha','html_url','run_attempt']}
        result['jobs']=[{k:j.get(k) for k in ['id','name','status','conclusion','html_url']} for j in self.jobs(run_id)]
        result['artifacts']=self.artifacts(run_id)['artifacts']
        result['limit']='Read the downloaded result.json and output files; Actions success does not establish a mathematical conclusion.'
        return result

    def artifacts(self, run_id):
        if not str(run_id).isdigit():raise ValueError('Use the actual numeric Actions run ID')
        rows=[];page=1
        while True:
            value=self.request('GET',self.repo_path('/actions/runs/'+str(run_id)+'/artifacts?per_page=100&page='+str(page)))
            rows.extend(value.get('artifacts',[]))
            if len(value.get('artifacts',[]))<100:break
            page+=1
        return {'run_id':int(run_id),'artifacts':[{k:r.get(k) for k in ['id','name','size_in_bytes','expired','created_at','expires_at','digest']} for r in rows]}

    def download(self, artifact_id, output):
        if not str(artifact_id).isdigit():raise ValueError('Use the actual numeric artifact ID')
        destination=_safe_path(self.root,output)
        if destination.exists():raise ValueError('Artifact destination already exists; choose a new path')
        info=self.request('GET',self.repo_path('/actions/artifacts/'+str(artifact_id)))
        if info.get('expired'):raise ValueError('Artifact has expired; use retained checkpoint inputs for a deliberate resumed request')
        class HoldRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):return None
        auth_request=urllib.request.Request('https://api.github.com'+self.repo_path('/actions/artifacts/'+str(artifact_id)+'/zip'),
            headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+self._token,'X-GitHub-Api-Version':'2026-03-10','User-Agent':'co-work-research-tools'})
        opener=urllib.request.build_opener(HoldRedirect())
        try:
            response=opener.open(auth_request,timeout=30)
        except urllib.error.HTTPError as exc:
            if exc.code!=302:raise APIError(exc.code,'Artifact download rejected') from None
            location=exc.headers.get('Location','')
            if urllib.parse.urlparse(location).scheme!='https':raise ValueError('Artifact storage URL must use HTTPS')
            # The storage request carries no GitHub authorization header.
            try:response=urllib.request.urlopen(urllib.request.Request(location,headers={'User-Agent':'co-work-research-tools'}),timeout=60)
            except urllib.error.URLError:raise APIError('download','Artifact storage download failed; retry the artifact ID without exposing its temporary storage URL') from None
        destination.parent.mkdir(parents=True,exist_ok=True)
        try:
            with response, destination.open('xb') as stream:shutil.copyfileobj(response,stream,1024*1024)
        except BaseException:
            destination.unlink(missing_ok=True);raise
        return {'status':'artifact-downloaded','artifact_id':int(artifact_id),'path':output,'bytes':destination.stat().st_size,
                'next':'Inspect result.json, stdout, stderr, declared outputs and saved algorithm checkpoints before deciding the next computation.'}

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
    q = sub.add_parser('workflow-status'); q.add_argument('--workflow',default='research-compute.yml');q.add_argument('--ref',required=True)
    q = sub.add_parser('submit-compute');q.add_argument('experiment');q.add_argument('--manifest',default='research/experiments.json');q.add_argument('--request-id');q.add_argument('--runner');q.add_argument('--timeout-minutes',type=int,required=True);q.add_argument('--resume-from')
    q = sub.add_parser('runs');q.add_argument('--ref');q.add_argument('--request-id');q.add_argument('--head');q.add_argument('--limit',type=int,default=20);q.add_argument('--workflow',default='research-compute.yml')
    q = sub.add_parser('run');q.add_argument('run_id')
    q = sub.add_parser('artifacts');q.add_argument('run_id')
    q = sub.add_parser('download');q.add_argument('artifact_id');q.add_argument('--out',required=True)
    q = sub.add_parser('dispatch'); q.add_argument('--workflow', required=True); q.add_argument('--ref', required=True); q.add_argument('--inputs-file')
    q = sub.add_parser('machines'); q.add_argument('--ref', required=True)
    q = sub.add_parser('create-codespace'); q.add_argument('--ref', required=True); q.add_argument('--machine', required=True)
    q = sub.add_parser('stop-codespace'); q.add_argument('name')
    a = p.parse_args(argv); root = a.repo.resolve()
    if a.command=='submit-compute':
        result=compute_request(root,a.experiment,a.request_id,a.manifest,a.runner,a.timeout_minutes,a.resume_from)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    token_file = os.environ.get('WCG_CHECKPOINT_TOKEN_FILE') or subprocess.run(['git', 'config', '--local', '--get', 'wcg.tokenFile'], cwd=root, capture_output=True, text=True).stdout.strip()
    if not token_file: raise ValueError('Use work.py --token-file with an external PAT; no account-link connector is needed')
    client = Client(root, token_file)
    if a.command == 'status': result = client.status()
    elif a.command=='workflow-status':result=client.workflow_status(a.workflow,a.ref)
    elif a.command=='runs':result=client.runs(a.ref,a.request_id,a.head,a.limit,a.workflow)
    elif a.command=='run':result=client.run_status(a.run_id)
    elif a.command=='artifacts':result=client.artifacts(a.run_id)
    elif a.command=='download':result=client.download(a.artifact_id,a.out)
    elif a.command == 'dispatch': result = client.dispatch(a.workflow, a.ref, json.loads(_safe_path(root, a.inputs_file).read_text()) if a.inputs_file else {})
    elif a.command == 'machines': result = client.machines(a.ref)
    elif a.command == 'create-codespace': result = client.create(a.ref, a.machine)
    else: result = client.stop(a.name)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


if __name__ == '__main__':
    try: raise SystemExit(main())
    except (ValueError, OSError, KeyError, APIError) as exc: raise SystemExit(str(exc))
