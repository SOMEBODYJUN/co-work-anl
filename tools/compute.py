"""Run useful registered computations locally or from explicit Actions requests."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import uuid

from curation import _safe_path, _write_json

DEFAULT_MANIFEST = 'research/experiments.json'
REQUESTS = 'research/compute-requests'
IDENT = __import__('re').compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}')


def pin(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def spec(root, name, manifest=DEFAULT_MANIFEST):
    data = json.loads(_safe_path(root, manifest).read_text())
    if data.get('schema') != 1 or name not in data.get('experiments', {}):
        raise ValueError('Unknown computation in '+manifest+': '+name)
    item = data['experiments'][name]
    if not isinstance(item.get('command'), list) or not item['command'] or any(not isinstance(x, str) or not x for x in item['command']):
        raise ValueError('Computation command must be a nonempty argument list')
    timeout = item.get('timeout_seconds')
    if timeout is not None and (type(timeout) is not int or timeout <= 0):
        raise ValueError('timeout_seconds must be positive, or null for an explicitly unbounded local run')
    if not isinstance(item.get('scope'), str) or not item['scope'].strip():
        raise ValueError('State the actual mathematical purpose in scope')
    for key in ['inputs', 'checkout_paths', 'outputs', 'python_packages']:
        if key in item and (not isinstance(item[key], list) or any(not isinstance(x, str) or not x for x in item[key])):
            raise ValueError(key+' must be a list of explicit paths or package specifications')
    for name in item.get('outputs', []):
        _safe_path(root, name)
    return item


def input_paths(root, item, resume_from=None):
    paths = list(item.get('inputs', [])) + list(item.get('checkout_paths', []))
    for arg in item['command']:
        if arg.startswith('{') or arg.startswith('-'):
            continue
        p = root/arg
        if p.is_file():
            paths.append(arg)
    if item.get('requirements_file'):
        paths.append(item['requirements_file'])
    if resume_from:
        paths.append(resume_from)
    files = set()
    resume_path = _safe_path(root,resume_from) if resume_from else None
    excluded = [root/n for n in item.get('outputs', [])]
    for name in dict.fromkeys(paths):
        path = _safe_path(root, name)
        if not path.exists():
            raise ValueError('Declared computation input is absent: '+name)
        for p in path.rglob('*') if path.is_dir() else [path]:
            if not p.is_file() or '__pycache__' in p.parts:
                continue
            if any(p == e or e in p.parents for e in excluded) and not (resume_path and (p==resume_path or resume_path in p.parents)):
                continue
            relative = p.relative_to(root).as_posix()
            _safe_path(root, relative)
            files.add(relative)
    return [{'path': n, 'sha256': hashlib.sha256((root/n).read_bytes()).hexdigest()} for n in sorted(files)]


def request(root, name, request_id=None, manifest=DEFAULT_MANIFEST, runner=None, timeout_minutes=None, resume_from=None):
    item = spec(root, name, manifest)
    request_id = request_id or 'C-'+uuid.uuid4().hex
    if not IDENT.fullmatch(request_id):
        raise ValueError('Use a stable computation request ID')
    minutes = timeout_minutes if timeout_minutes is not None else item.get('actions_timeout_minutes')
    if type(minutes) is not int or not 3 <= minutes <= 360:
        raise ValueError('Choose an explicit Actions budget of 3..360 minutes; hosted jobs have a real six-hour limit')
    if item.get('timeout_seconds') is None or item['timeout_seconds'] > (minutes-2)*60:
        raise ValueError('Set the computation timeout within the chosen Actions budget, leaving two minutes to retain outputs')
    chosen_runner = runner or item.get('runner', 'ubuntu-latest')
    if not isinstance(chosen_runner, str) or not chosen_runner.strip():
        raise ValueError('Choose an existing Actions runner label')
    row = {'schema': 1, 'request_id': request_id, 'experiment': name, 'manifest': manifest,
           'experiment_pin': pin(item), 'runner': chosen_runner, 'timeout_minutes': minutes,
           'files': input_paths(root, item, resume_from), 'resume_from': resume_from,
           'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    destination = _safe_path(root, REQUESTS+'/'+request_id+'.json')
    if destination.exists():
        raise ValueError('Request ID already exists; inspect its run instead of dispatching the same work again')
    _write_json(destination, row)
    return {'status': 'request-local-not-pushed', 'request_id': request_id,
            'request_file': destination.relative_to(root).as_posix(), 'input_files': len(row['files']),
            'runner': chosen_runner, 'timeout_minutes': minutes,
            'next': 'Checkpoint this request together with its computation code, manifest and declared inputs. The branch push runs only newly added requests; use github runs --request-id '+request_id+' to observe execution.'}


def load_request(root, name, verify=True):
    row = json.loads(_safe_path(root, name).read_text())
    if row.get('schema') != 1 or not IDENT.fullmatch(row.get('request_id', '')):
        raise ValueError('Invalid computation request')
    if name != REQUESTS+'/'+row['request_id']+'.json':
        raise ValueError('Request filename and request ID must agree')
    item = spec(root, row['experiment'], row['manifest'])
    if row['experiment_pin'] != pin(item):
        raise ValueError('The requested computation changed; retain this request and submit a new explicit version')
    if not isinstance(row.get('runner'), str) or not row['runner'].strip():
        raise ValueError('Requested runner label is absent')
    if not isinstance(row.get('files'), list):
        raise ValueError('Requested input versions are absent')
    if type(row.get('timeout_minutes')) is not int or not 3 <= row['timeout_minutes'] <= 360:
        raise ValueError('Invalid Actions time budget')
    if item.get('timeout_seconds') is None or item['timeout_seconds'] > (row['timeout_minutes']-2)*60:
        raise ValueError('Computation exceeds its Actions execution budget')
    seen=set()
    for ref in row.get('files', []):
        if not isinstance(ref,dict) or not isinstance(ref.get('sha256'),str) or not __import__('re').fullmatch(r'[0-9a-f]{64}',ref['sha256']):
            raise ValueError('Invalid requested input version')
        if ref['path'] in seen:raise ValueError('Duplicate requested input')
        seen.add(ref['path'])
        p = _safe_path(root, ref['path'])
        if verify and (not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != ref['sha256']):
            raise ValueError('Requested input version changed: '+ref['path'])
    return row, item


def run(root, name, output, manifest=DEFAULT_MANIFEST, resume_from=None, request_id=None):
    item = spec(root, name, manifest)
    receipt = _safe_path(root, output)
    work = receipt.parent
    work.mkdir(parents=True, exist_ok=True)
    stdout_path, stderr_path = work/(receipt.stem+'.stdout.txt'), work/(receipt.stem+'.stderr.txt')
    if receipt.exists() or stdout_path.exists() or stderr_path.exists():
        raise ValueError('Choose a new result directory; previous computation outputs are retained')
    resume = str(_safe_path(root, resume_from)) if resume_from else ''
    command = [sys.executable if arg == '{python}' else arg.replace('{resume_from}', resume) for arg in item['command']]
    env = {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in ('TOKEN', 'SECRET', 'PASSWORD', 'ASKPASS'))}
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONHASHSEED'] = str(item.get('seed') or 0)
    env['RESEARCH_CHECKPOINT_DIR'] = str(work/'checkpoints')
    if resume: env['RESEARCH_RESUME_FROM'] = resume
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = {'schema': 2, 'experiment': name, 'request_id': request_id, 'status': 'running',
              'started_at': started, 'commit': head.stdout.strip() if head.returncode == 0 else None,
              'manifest': manifest, 'experiment_pin': pin(item), 'command': command, 'spec': item,
              'input_files': input_paths(root, item, resume_from), 'stdout_file': stdout_path.relative_to(root).as_posix(),
              'stderr_file': stderr_path.relative_to(root).as_posix(), 'resume_from': resume_from,
              'python': platform.python_version(), 'platform': platform.platform(),
              'interpretation': 'Actual computation output in the declared domain; mathematical conclusions come from its content, not the process exit code.'}
    _write_json(receipt, result)
    clock = time.monotonic()
    with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
        try:
            proc = subprocess.Popen(command, cwd=root, env=env, stdout=stdout, stderr=stderr)
            try:
                code = proc.wait(timeout=item.get('timeout_seconds'))
                status = 'completed' if code == 0 else 'failed'
            except subprocess.TimeoutExpired:
                proc.terminate()
                try: proc.wait(timeout=10)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
                code, status = None, 'timeout'
        except OSError as exc:
            stderr.write(str(exc).encode());code, status = None, 'failed-to-start'
    result.update(status=status, exit_code=code, elapsed_seconds=round(time.monotonic()-clock, 3),
                  completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  output_paths=[n for n in item.get('outputs', []) if _safe_path(root, n).exists()])
    _write_json(receipt, result)
    return code == 0


def prepare_actions(root, event_file, github_output):
    event = json.loads(Path(event_file).read_text())
    jobs = []
    if 'inputs' in event and event.get('inputs', {}).get('experiment'):
        values = event['inputs'];name = values['experiment'];manifest = values.get('manifest') or DEFAULT_MANIFEST
        item = spec(root, name, manifest)
        rid = values.get('request_id') or 'A-'+os.environ.get('GITHUB_RUN_ID', uuid.uuid4().hex)
        if not IDENT.fullmatch(rid):raise ValueError('Invalid dispatch request ID')
        minutes = int(values.get('timeout_minutes') or item.get('actions_timeout_minutes') or 60)
        if not 3 <= minutes <= 360 or item.get('timeout_seconds') is None or item['timeout_seconds'] > (minutes-2)*60:
            raise ValueError('Explicit dispatch budget must cover the registered computation and output retention')
        paths = list(item.get('checkout_paths', []))+list(item.get('inputs', []))
        for arg in item['command']:
            if not arg.startswith(('{', '-')) and '/' in arg:
                paths.append(arg)
        if item.get('requirements_file'): paths.append(item['requirements_file'])
        jobs.append({'request_id':rid,'request_file':'','experiment':name,'manifest':manifest,'experiment_pin':pin(item),
                     'runner':values.get('runner') or item.get('runner','ubuntu-latest'),'timeout_minutes':minutes,
                     'paths':paths,'resume_from':''})
    else:
        before, after = event.get('before', ''), event.get('after') or os.environ['GITHUB_SHA']
        current=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
        if current != after:raise ValueError('Actions checkout is not the pushed commit requested by this event')
        if before and set(before) != {'0'}:
            if subprocess.run(['git','cat-file','-e',before+'^{commit}'],cwd=root,capture_output=True).returncode:
                subprocess.run(['git','fetch','--quiet','--no-tags','--depth=1','--filter=blob:none','origin',before],cwd=root,check=True)
            names = subprocess.check_output(['git','diff','--name-only','--diff-filter=A',before,after,'--',REQUESTS+'/'],cwd=root,text=True).splitlines()
        else:
            names = subprocess.check_output(['git','ls-tree','-r','--name-only',after,'--',REQUESTS+'/'],cwd=root,text=True).splitlines()
        for name in names:
            if not name.endswith('.json'):continue
            raw=json.loads(_safe_path(root,name).read_text())
            manifest_path=_safe_path(root,raw['manifest'])
            if not manifest_path.exists():
                manifest_path.parent.mkdir(parents=True,exist_ok=True)
                manifest_path.write_bytes(subprocess.check_output(['git','show',after+':'+raw['manifest']],cwd=root))
            row, item = load_request(root,name,verify=False)
            jobs.append(dict(row,request_file=name,paths=[r['path'] for r in row['files']]))
    for row in jobs:
        paths = ['work.py','tools/*.py','tools/vendor/**',row['manifest'],*row.pop('paths')]
        if row['request_file']:paths.append(row['request_file'])
        for name in paths:
            if '*' not in name:_safe_path(root,name)
        row['checkout_paths'] = '\n'.join('/'+n.rstrip('/') for n in dict.fromkeys(paths))
        row.pop('files',None)
    with Path(github_output).open('a') as stream:
        stream.write('matrix='+json.dumps({'include':jobs},separators=(',',':'))+'\n')
        stream.write('has_requests='+str(bool(jobs)).lower()+'\n')
    return {'requests':len(jobs),'request_ids':[j['request_id'] for j in jobs]}


def execute_request(root, args):
    if args.request_file:
        row,item=load_request(root,args.request_file)
        name,manifest,resume,rid=row['experiment'],row['manifest'],row.get('resume_from'),row['request_id']
    else:
        name,manifest,resume,rid=args.experiment,args.manifest,args.resume_from,args.request_id
        item=spec(root,name,manifest)
        if args.experiment_pin and pin(item)!=args.experiment_pin:raise ValueError('Dispatch computation version changed')
    work = _safe_path(root,args.out).parent
    work.mkdir(parents=True,exist_ok=True)
    if os.environ.get('GITHUB_OUTPUT'):
        marker='paths_'+uuid.uuid4().hex
        paths=[work.relative_to(root).as_posix(),*item.get('outputs',[])]
        with Path(os.environ['GITHUB_OUTPUT']).open('a') as stream:
            stream.write('artifact_paths<<'+marker+'\n'+'\n'.join(paths)+'\n'+marker+'\n')
    # Dependency installation is explicit in the computation specification.
    packages=item.get('python_packages',[])
    command=[sys.executable,'-m','pip','install',*packages]
    if item.get('requirements_file'):command += ['-r',str(_safe_path(root,item['requirements_file']))]
    if len(command)>4:
        with (work/'dependency-install.txt').open('wb') as log:
            try:subprocess.run(command,cwd=root,stdout=log,stderr=subprocess.STDOUT,check=True)
            except subprocess.CalledProcessError:
                _write_json(_safe_path(root,args.out),{'schema':2,'experiment':name,'request_id':rid,
                    'status':'dependency-install-failed','manifest':manifest,'experiment_pin':pin(item)})
                return False
    return run(root,name,args.out,manifest,resume,rid)


def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    known={'run','request','prepare-actions','execute-request'}
    # Existing explicit compute.py EXP --out ... invocations keep working.
    if argv and argv[0] not in known and argv[0] not in {'-h','--help','--repo'}:argv.insert(0,'run')
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ['run','request']:
        p=sub.add_parser(name);p.add_argument('experiment');p.add_argument('--manifest',default=DEFAULT_MANIFEST);p.add_argument('--resume-from')
        if name=='run':p.add_argument('--out',required=True)
        else:p.add_argument('--request-id');p.add_argument('--runner');p.add_argument('--timeout-minutes',type=int,required=True)
    p=sub.add_parser('prepare-actions');p.add_argument('--event-file',required=True);p.add_argument('--github-output',required=True)
    p=sub.add_parser('execute-request');p.add_argument('--request-file');p.add_argument('--experiment');p.add_argument('--manifest',default=DEFAULT_MANIFEST);p.add_argument('--experiment-pin');p.add_argument('--request-id');p.add_argument('--resume-from');p.add_argument('--out',required=True)
    args=parser.parse_args(argv);root=args.repo.resolve()
    if args.command=='request':result=request(root,args.experiment,args.request_id,args.manifest,args.runner,args.timeout_minutes,args.resume_from)
    elif args.command=='prepare-actions':result=prepare_actions(root,args.event_file,args.github_output)
    else:
        success=execute_request(root,args) if args.command=='execute-request' else run(root,args.experiment,args.out,args.manifest,args.resume_from)
        print(json.dumps({'status':'completed' if success else 'inspect-computation-receipt','receipt':args.out},ensure_ascii=False));return 0 if success else 1
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:raise SystemExit(str(exc))
