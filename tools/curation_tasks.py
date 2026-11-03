"""Version-bound object-group editing tasks, separate from frozen source claims."""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import uuid
import board
import cleanup
import coordination
import curation

ACTIVE={'claimed','submitted','blocked'}

def run_home(root,run):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,100}',run):raise ValueError('Invalid run')
    return curation._safe_path(root,'curation/runs/'+run)

def task_path(root,run,task):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,100}',task):raise ValueError('Invalid task ID')
    run_home(root,run)
    return curation._safe_path(root,'curation/runs/'+run+'/tasks/'+task+'.json')

def overlaps(a,b):
    aa=PurePosixPath(a);bb=PurePosixPath(b)
    return aa==bb or aa in bb.parents or bb in aa.parents

def definition(root,record):
    required={'task_id','inputs','write_paths','question','goal','preserve','budget_minutes','acceptance'}
    if not isinstance(record,dict) or not required<=record.keys() or record.keys()-required-{'related_paths'}:
        raise ValueError('Task definition fields missing or unsupported')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,100}',str(record['task_id'])):raise ValueError('Invalid task ID')
    for k in ('question','goal','preserve','acceptance'):
        if not isinstance(record[k],str) or not record[k].strip():raise ValueError('Concrete mathematical task required: '+k)
    if type(record['budget_minutes']) is not int or not 1<=record['budget_minutes']<=480:
        raise ValueError('Explicit bounded exploration budget required')
    if not isinstance(record['inputs'],list) or not record['inputs']:raise ValueError('Task inputs required')
    seen=set()
    for row in record['inputs']:
        if not isinstance(row,dict) or set(row)!={'path','sha256'}:raise ValueError('Input needs path and SHA')
        curation._safe_path(root,row['path'])
        if row['path'] in seen or not re.fullmatch(r'[0-9a-f]{64}',str(row['sha256'])):raise ValueError('Invalid/duplicate input')
        seen.add(row['path'])
    if not isinstance(record['write_paths'],list) or not record['write_paths']:raise ValueError('Explicit write scope required')
    for name in record['write_paths']:curation._safe_path(root,name)
    if len(set(record['write_paths']))!=len(record['write_paths']):raise ValueError('Duplicate write scope')
    board.guard(record)

def plan(root,run,record_file):
    home=run_home(root,run)
    if not (home/'run.json').is_file():raise ValueError('Run does not exist')
    records=json.loads(curation._safe_path(root,record_file).read_text())
    if isinstance(records,dict):records=[records]
    if not isinstance(records,list) or not records:raise ValueError('Nonempty task definitions required')
    writes=[]
    for record in records:
        definition(root,record);p=task_path(root,run,record['task_id'])
        if p.exists():raise ValueError('Task already exists; do not overwrite ownership')
        writes.append((p,dict(definition=record,state='available',owner=None)))
    if len({p for p,_ in writes})!=len(writes):raise ValueError('Duplicate task ID')
    for p,record in writes:curation._write_json(p,record)
    return {'status':'planned-local-not-pushed','tasks':[r['definition']['task_id'] for _,r in writes]}

def tasks(root,run):
    home=run_home(root,run)
    directory=curation._safe_path(root,home.relative_to(root).as_posix()+'/tasks')
    return [json.loads(curation._safe_path(root,p.relative_to(root).as_posix()).read_text()) for p in sorted(directory.glob('*.json'))] if directory.exists() else []

def validate_inputs(root,record):
    for row in record['inputs']:
        p=curation._safe_path(root,row['path'])
        if not p.is_file() or curation.digest(p.read_bytes())!=row['sha256']:
            raise ValueError('Task input changed; reframe this task before claiming: '+row['path'])

def transition(root,run,old,all_tasks,actor,operation,request_id,*,assets=None,reason=None,draft_note=None,write_paths=None):
    config=json.loads((run_home(root,run)/'run.json').read_text())
    record=old['definition'];definition(root,record)
    new=dict(old)
    if operation=='claim':
        if old['state'] not in {'available','handoff'} or old.get('owner'):
            raise ValueError('Task is not available')
        validate_inputs(root,record)
        for other in all_tasks:
            if other['definition']['task_id']==record['task_id'] or other.get('state') not in ACTIVE:continue
            if any(overlaps(a,b) for a in record['write_paths'] for b in other['definition']['write_paths']):
                raise ValueError('Write scope already occupied by '+other['definition']['task_id'])
        new.update(state='claimed',owner=actor)
    elif operation=='extend':
        if old.get('owner')!=actor or old['state'] not in {'claimed','blocked'}:raise ValueError('Only owner may extend an unfinished task scope')
        if not isinstance(write_paths,list) or not write_paths:raise ValueError('Explicit additional output paths required')
        for name in write_paths:curation._safe_path(root,name)
        for other in all_tasks:
            if other['definition']['task_id']==record['task_id'] or other.get('state') not in ACTIVE:continue
            if any(overlaps(a,b) for a in write_paths for b in other['definition']['write_paths']):raise ValueError('Additional output scope is already occupied')
        revised=dict(record,write_paths=list(dict.fromkeys(record['write_paths']+write_paths)))
        definition(root,revised);new['definition']=revised
    elif operation=='submit':
        if old.get('owner')!=actor or old['state'] not in {'claimed','blocked'}:raise ValueError('Claim task before submitting')
        if not isinstance(assets,list) or not assets:raise ValueError('Already-pushed output assets required')
        for source in record['inputs']:
            if any(overlaps(source['path'],scope) for scope in record['write_paths']):continue
            p=curation._safe_path(root,source['path'])
            if not p.is_file() or curation.digest(p.read_bytes())!=source['sha256']:
                raise ValueError('Read dependency changed; review the task before submitting: '+source['path'])
        for asset in assets:
            if not isinstance(asset,dict) or set(asset)!={'path','sha256'}:raise ValueError('Output asset needs path and SHA')
            name=asset['path'];p=curation._safe_path(root,name)
            if not any(overlaps(name,scope) and (name==scope or PurePosixPath(scope) in PurePosixPath(name).parents) for scope in record['write_paths']):
                raise ValueError('Output is outside claimed scope')
            if not p.is_file() or curation.digest(p.read_bytes())!=asset['sha256']:raise ValueError('Output not published at expected bytes: '+name)
        if not any(curation.is_formal_path(asset['path']) for asset in assets):
            raise ValueError('A workspace draft or evidence alone is not a mathematical delivery; reference current formal mathematics')
        new.update(state='submitted',assets=assets,output_commit=board.git(root,'rev-parse','HEAD').stdout.decode().strip())
    elif operation=='complete':
        if old['state']!='submitted' or actor not in {old.get('owner'),config['actor']}:raise ValueError('Only submitted work can be completed by owner/coordinator')
        for asset in old['assets']:
            p=curation._safe_path(root,asset['path'])
            if not p.is_file() or curation.digest(p.read_bytes())!=asset['sha256']:raise ValueError('Submitted content changed; do not complete stale work')
        if not reason or not reason.strip():raise ValueError('Concrete mathematical completion/outcome required')
        new.update(state='completed',completion=reason,completed_by=actor)
    elif operation=='handoff':
        if old.get('owner')!=actor or old['state'] not in ACTIVE:raise ValueError('Only hand off own unfinished task')
        if not reason or not reason.strip():raise ValueError('Real handoff reason required')
        new.update(state='handoff',owner=None,previous_owner=actor,handoff_reason=reason,draft_note=draft_note)
    else:raise ValueError('Unknown task operation')
    new['request_id']=request_id;board.guard(new)
    return new

def mutate(root,run,task,operation,*,assets=None,reason=None,draft_note=None,write_paths=None):
    actor=coordination.config(root,'wcg.actor');instance=coordination.config(root,'wcg.instance')
    if not re.fullmatch(r'Boss[1-9][0-9]*',actor):raise ValueError('Explicit registered Boss required')
    if coordination.config(root,'wcg.curationRun')!=run:raise ValueError('Start an independent curator clone bound to this run')
    branch=coordination.config(root,'wcg.branch');client=board.Board(root,branch=branch,retries=8)
    request_id=uuid.uuid4().hex;checked=False
    for _ in range(8):
        with client.scratch() as tmp:
            directory=Path(tmp);cleanup.checkout_snapshot(client,directory)
            person=run_home(directory,run)/'people'/f'{actor}.json'
            if not person.is_file() or json.loads(person.read_text()).get('instance')!=instance:
                raise ValueError('Boss identity is not registered for this run')
            if not checked:
                coordination.verify_write(directory,branch,board.git(directory,'rev-parse','HEAD').stdout.decode().strip());checked=True
            p=task_path(directory,run,task)
            old=json.loads(p.read_text())
            if old.get('request_id')==request_id:return {'status':'pushed','operation':operation,'task_id':task}
            new=transition(directory,run,old,tasks(directory,run),actor,operation,request_id,assets=assets,reason=reason,draft_note=draft_note,write_paths=write_paths)
            curation._write_json(p,new)
            board.git(directory,'add','--',p.relative_to(directory).as_posix())
            board.git(directory,'commit','--quiet','-m',f'curation {operation}: {actor} {task}')
            pushed=board.git(directory,'push','--quiet','origin','HEAD:refs/heads/'+branch,check=False)
            if board.auth_rejected(pushed):raise board.AuthenticationError('Authentication rejected. Stop credential retries and new claims.')
            _,tip,_=cleanup.refresh_snapshot(client)
            actual=board.git(directory,'show',tip+':'+p.relative_to(directory).as_posix(),check=False)
            if not actual.returncode and json.loads(actual.stdout).get('request_id')==request_id:
                return {'status':'pushed','operation':operation,'actor':actor,'task_id':task,'remote_tip':tip,
                        'note':'Task editing outcome, not mathematical truth or graph admission'}
            if pushed.returncode and not re.search(rb'non-fast-forward|fetch first',pushed.stderr+pushed.stdout,re.I):
                raise board.BoardError('Task write not confirmed; local drafts retained')
    raise board.BoardError('Concurrent task update could not be confirmed')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    for command in ['plan','list','show','claim','extend','submit','complete','handoff']:
        q=sub.add_parser(command);q.add_argument('--run',required=True)
        if command=='plan':q.add_argument('--record-file',required=True)
        elif command!='list':q.add_argument('task')
        if command=='submit':q.add_argument('--assets-file',required=True)
        if command=='extend':q.add_argument('--paths-file',required=True)
        if command in {'complete','handoff'}:q.add_argument('--reason',required=True)
        if command=='handoff':q.add_argument('--draft-note')
    a=p.parse_args();root=a.repo.resolve()
    try:
        if a.command=='plan':result=plan(root,a.run,a.record_file)
        elif a.command=='list':result=tasks(root,a.run)
        elif a.command=='show':result=json.loads(task_path(root,a.run,a.task).read_text())
        else:
            assets=json.loads(curation._safe_path(root,a.assets_file).read_text()) if a.command=='submit' else None
            write_paths=json.loads(curation._safe_path(root,a.paths_file).read_text()) if a.command=='extend' else None
            result=mutate(root,a.run,a.task,a.command,assets=assets,reason=getattr(a,'reason',None),draft_note=getattr(a,'draft_note',None),write_paths=write_paths)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,board.BoardError) as e:raise SystemExit(str(e))

if __name__=='__main__':main()
