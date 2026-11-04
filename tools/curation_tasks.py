"""Version-bound object-group editing tasks, separate from frozen source claims."""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path, PurePosixPath
import re
import time
import uuid
import board
import cleanup
import coordination
import curation

ACTIVE={'claimed','submitted','blocked'}

class TaskWriteError(board.BoardError):
    """A push failure that is not a recoverable ref race."""

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

def transition(root,run,old,all_tasks,actor,operation,request_id,*,assets=None,reason=None,draft_note=None,write_paths=None,reuse_paths=None):
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
        reused=set(reuse_paths or [])
        if not reused<={a.get('path') for a in assets if isinstance(a,dict)}:
            raise ValueError('Reused paths must name submitted assets')
        for name in reused:
            curation._safe_path(root,name)
            if not curation.is_formal_path(name):raise ValueError('Reuse names current formal mathematics')
        for asset in assets:
            if not isinstance(asset,dict) or set(asset)!={'path','sha256'}:raise ValueError('Output asset needs path and SHA')
            name=asset['path'];p=curation._safe_path(root,name)
            if name not in reused and not any(overlaps(name,scope) and (name==scope or PurePosixPath(scope) in PurePosixPath(name).parents) for scope in record['write_paths']):
                raise ValueError('Output is outside claimed scope')
            if not p.is_file() or curation.digest(p.read_bytes())!=asset['sha256']:raise ValueError('Output not published at expected bytes: '+name)
        if not any(curation.is_formal_path(asset['path']) for asset in assets):
            raise ValueError('A workspace draft or evidence alone is not a mathematical delivery; reference current formal mathematics')
        new.update(state='submitted',assets=assets,output_commit=board.git(root,'rev-parse','HEAD').stdout.decode().strip())
        if reused:new['reused_paths']=sorted(reused)
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
    new['request_id']=request_id;new['updated_at']=int(time.time());board.guard(new)
    return new


def snapshot_blobs(root,names):
    """Read indexed regular blobs together, without expanding source files."""
    names=list(dict.fromkeys(names))
    for name in names:
        curation._safe_path(root,name)
        if '\n' in name or '\r' in name:raise ValueError('Invalid transaction path')
    if not names:return {}
    entries=board.git(root,'ls-files','--stage','-z','--',*[':(literal)'+n for n in names]).stdout
    files=[]
    for entry in entries.split(b'\0'):
        if not entry:continue
        head,name=entry.split(b'\t',1)
        if head.split()[0] in {b'100644',b'100755'} and name.decode() in names:
            files.append((name.decode(),head.split()[1].decode()))
    if not files:return {}
    raw=board.git(root,'cat-file','--batch',input_data=''.join(oid+'\n' for _,oid in files).encode()).stdout
    offset=0;result={}
    for name,_ in files:
        end=raw.find(b'\n',offset);header=raw[offset:end].split()
        if len(header)!=3 or header[1]!=b'blob':raise ValueError('Missing transaction blob: '+name)
        size=int(header[2]);data=raw[end+1:end+1+size];offset=end+2+size
        result[name]=data
    return result


def materialize(root,tip,names):
    """Expand only the requested regular blobs, preserving exact bytes."""
    for name,data in snapshot_blobs(root,names).items():
        path=curation._safe_path(root,name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)


def select_claims(root,current,limit,prefix=''):
    """Select compatible, current inputs from this transaction's remote tree."""
    candidates=[t for key,t in sorted(current.items()) if key.startswith(prefix)
                and t['state'] in {'available','handoff'} and not t.get('owner')]
    names=[r['path'] for t in candidates for r in t['definition']['inputs']]
    hashes={name:curation.digest(data) for name,data in snapshot_blobs(root,names).items()}
    occupied=[scope for t in current.values() if t['state'] in ACTIVE for scope in t['definition']['write_paths']]
    chosen=[];skipped=[]
    for t in candidates:
        d=t['definition'];stale=[r['path'] for r in d['inputs'] if hashes.get(r['path'])!=r['sha256']]
        if stale:
            skipped.append({'task_id':d['task_id'],'reason':'input-changed','path':stale[0]});continue
        if any(overlaps(a,b) for a in d['write_paths'] for b in occupied):
            skipped.append({'task_id':d['task_id'],'reason':'write-scope-occupied'});continue
        chosen.append({'operation':'claim','task_id':d['task_id']});occupied.extend(d['write_paths'])
        if len(chosen)==limit:break
    return chosen,{'requested':limit,'selected':[op['task_id'] for op in chosen],
                   'skipped_count':len(skipped),'skipped':skipped[:12]}


def checkout_task_snapshot(client,directory,run,actor):
    """Keep the complete Git tree in the index, without expanding the repo."""
    cache,tip,shallow=cleanup.refresh_snapshot(client)
    client.setup(directory)
    info=directory/'.git/objects/info';info.mkdir(parents=True,exist_ok=True)
    (info/'alternates').write_text(str(cache/'objects')+'\n')
    if shallow is not None:(directory/'.git/shallow').write_bytes(shallow)
    board.git(directory,'update-ref','--no-deref','HEAD',tip)
    board.git(directory,'read-tree',tip)
    prefix='curation/runs/'+run
    raw=board.git(directory,'ls-tree','-r','--name-only','-z',tip,'--',
                  prefix+'/run.json',prefix+'/people/'+actor+'.json',prefix+'/tasks').stdout
    materialize(directory,tip,[p.decode() for p in raw.split(b'\0') if p])
    return tip


def task_status(root,run,full=False):
    rows=tasks(root,run);owners=collections.defaultdict(collections.Counter)
    for t in rows:owners[t.get('owner') or 'unowned'][t['state']]+=1
    home=run_home(root,run);delta_file=home/'catalogue-routing-delta.json'
    ungrouped=[]
    if delta_file.is_file():
        inputs={r['path'] for t in rows for r in t['definition']['inputs']}
        delta=json.loads(delta_file.read_text())
        ungrouped=[r['path'] for r in delta.get('ungrouped_candidates',[]) if r['path'] not in inputs]
    result={'run':run,'tasks':len(rows),'states':dict(collections.Counter(t['state'] for t in rows)),
            'owners':{k:dict(v) for k,v in sorted(owners.items())},
            'ungrouped_materials':len(ungrouped),'ungrouped_source':str(delta_file.relative_to(root)),
            'active':[{'task_id':t['definition']['task_id'],'owner':t.get('owner'),
                       'state':t['state'],'updated_at':t.get('updated_at')} for t in rows if t['state'] in ACTIVE],
            'meaning':'Current local snapshot; sync before remote ownership decisions'}
    if full:result['ungrouped_paths']=ungrouped
    return result


def task_list(root,run,*,state=None,owner=None,limit=None,full=False):
    if owner=='self':owner=coordination.config(root,'wcg.actor')
    rows=[t for t in tasks(root,run) if (state is None or t['state']==state) and
          (owner is None or t.get('owner')==owner)]
    limit=(0 if full else 20) if limit is None else limit
    if limit<0:raise ValueError('Limit must be nonnegative; 0 means all')
    if limit:rows=rows[:limit]
    if full:return rows
    return [{'task_id':t['definition']['task_id'],'state':t['state'],'owner':t.get('owner'),
             'question':t['definition']['question'],'inputs':len(t['definition']['inputs']),
             'assets':len(t.get('assets',[]))} for t in rows]


def apply_operation(root,run,old,all_tasks,actor,op,request_id):
    operation=op['operation']
    kwargs={k:op[k] for k in ('assets','reason','draft_note','write_paths','reuse_paths') if k in op}
    if operation=='claim':
        scopes=kwargs.pop('write_paths',None);kwargs.pop('reuse_paths',None)
        new=transition(root,run,old,all_tasks,actor,'claim',request_id,**kwargs)
        if scopes:new=transition(root,run,new,all_tasks,actor,'extend',request_id,write_paths=scopes)
        return new
    if operation=='finish':
        reason=kwargs.pop('reason',None)
        if not reason or not reason.strip():raise ValueError('Concrete mathematical completion required')
        submitted=transition(root,run,old,all_tasks,actor,'submit',request_id,**kwargs)
        return transition(root,run,submitted,all_tasks,actor,'complete',request_id,reason=reason)
    return transition(root,run,old,all_tasks,actor,operation,request_id,**kwargs)


def mutate_many(root,run,operations,*,request_id=None):
    actor=coordination.config(root,'wcg.actor');instance=coordination.config(root,'wcg.instance')
    if not re.fullmatch(r'Boss[1-9][0-9]*',actor):raise ValueError('Explicit registered Boss required')
    if coordination.config(root,'wcg.curationRun')!=run:raise ValueError('Start an independent curator clone bound to this run')
    branch=coordination.config(root,'wcg.branch');client=board.Board(root,branch=branch,retries=8)
    request_id=request_id or uuid.uuid4().hex
    if not re.fullmatch(r'[0-9a-f]{32}',request_id):raise ValueError('Invalid request ID')
    if not isinstance(operations,list) or not operations:raise ValueError('Nonempty operation list required')
    allowed={'task_id','operation','assets','reason','draft_note','write_paths','reuse_paths','limit','prefix'}
    for op in operations:
        if not isinstance(op,dict) or op.keys()-allowed or op.get('operation') not in {'claim','claim-next','extend','submit','complete','finish','handoff','handoff-all'}:
            raise ValueError('Invalid task operation')
        if op['operation']=='claim-next':
            if len(operations)!=1 or op.keys()-{'operation','limit','prefix'}:
                raise ValueError('claim-next is one selection request, without fixed task IDs')
            if type(op.get('limit',1)) is not int or op.get('limit',1)<1:raise ValueError('Positive selection limit required')
            if not isinstance(op.get('prefix',''),str):raise ValueError('Task prefix must be text')
        else:
            if 'limit' in op or 'prefix' in op:raise ValueError('Selection fields belong to claim-next')
            if op['operation']!='handoff-all':task_path(root,run,op.get('task_id',''))
        if 'assets' in op and (not isinstance(op['assets'],list) or any(not isinstance(a,dict) or set(a)!={'path','sha256'} for a in op['assets'])):
            raise ValueError('Assets must contain path/SHA records')
        for key in ('write_paths','reuse_paths'):
            if key in op and (not isinstance(op[key],list) or any(not isinstance(p,str) for p in op[key])):raise ValueError('Paths must be a list')
    outbox=client.cache/'curation-outbox';outbox.mkdir(exist_ok=True)
    pending=outbox/(request_id+'.json');receipt=outbox/(request_id+'.done.json');targets=outbox/(request_id+'.targets.json')
    intent={'run':run,'actor':actor,'operations':operations,'request_id':request_id}
    if receipt.is_file():
        saved=json.loads(receipt.read_text())
        if saved['intent']!=intent:raise ValueError('Request ID already has a different intent')
        return saved['result']
    if pending.is_file() and json.loads(pending.read_text())!=intent:raise ValueError('Request ID already has a different intent')
    curation._write_json(pending,intent)
    last_error=None;automatic=operations[0]['operation']=='claim-next'
    for attempt in range(8):
        try:
          with client.scratch() as tmp:
            directory=Path(tmp);tip=checkout_task_snapshot(client,directory,run,actor)
            person=run_home(directory,run)/'people'/f'{actor}.json'
            if not person.is_file() or json.loads(person.read_text()).get('instance')!=instance:
                raise ValueError('Boss identity is not registered for this run')
            # Startup verifies the endpoint; this transaction's actual push is
            # the write check. Repeating a receive-pack dry run adds a round trip.
            current={t['definition']['task_id']:t for t in tasks(directory,run)}
            selection=None
            if targets.is_file():
                saved=json.loads(targets.read_text())
                expanded=saved['operations'] if isinstance(saved,dict) else saved
                if isinstance(saved,dict):selection=saved['selection']
            else:
                if automatic:
                    op=operations[0];expanded,selection=select_claims(directory,current,op.get('limit',1),op.get('prefix',''))
                else:
                    expanded=[]
                    for op in operations:
                        if op['operation']=='handoff-all':
                            expanded.extend(dict(op,operation='handoff',task_id=k) for k,t in current.items()
                                            if t.get('owner')==actor and t['state'] in ACTIVE)
                        else:expanded.append(op)
                curation._write_json(targets,{'operations':expanded,'selection':selection} if automatic else expanded)
            ids=[op['task_id'] for op in expanded]
            if len(ids)!=len(set(ids)):raise ValueError('One operation per task in a batch')
            needed=[]
            for op in expanded:
                old=current.get(op['task_id'])
                if old:
                    needed.extend(r['path'] for r in old['definition']['inputs'])
                    needed.extend(a['path'] for a in old.get('assets',[]))
                needed.extend(a['path'] for a in op.get('assets',[]))
            materialize(directory,tip,needed)
            changed=[];results=[]
            for op in expanded:
                task=op['task_id'];old=current.get(task)
                if old is None:
                    results.append({'task_id':task,'operation':op['operation'],'status':'conflict','detail':'Unknown task'});continue
                if old.get('request_id')==request_id:
                    results.append({'task_id':task,'operation':op['operation'],'status':'pushed','state':old['state'],'already_confirmed':True});continue
                try:new=apply_operation(directory,run,old,list(current.values()),actor,op,request_id)
                except ValueError as exc:
                    results.append({'task_id':task,'operation':op['operation'],'status':'conflict','detail':str(exc)});continue
                current[task]=new;p=task_path(directory,run,task);curation._write_json(p,new);changed.append(p.relative_to(directory).as_posix())
                results.append({'task_id':task,'operation':op['operation'],'status':'pushed','state':new['state']})
            if not changed:
                result={'status':'pushed' if any(r['status']=='pushed' for r in results) else 'no-changes',
                        'request_id':request_id,'actor':actor,'remote_tip':tip,'results':results}
                if selection is not None:result['selection']=selection
                curation._write_json(receipt,{'intent':intent,'result':result});pending.unlink(missing_ok=True);targets.unlink(missing_ok=True);return result
            board.git(directory,'add','--',*changed)
            label=f"curation {expanded[0]['operation']}: {actor} {expanded[0]['task_id']}" if len(expanded)==1 else f'curation batch: {actor} ({len(changed)} tasks)'
            board.git(directory,'commit','--quiet','-m',label)
            pushed=board.git(directory,'push','--quiet','origin','HEAD:refs/heads/'+branch,check=False)
            if board.auth_rejected(pushed):raise board.AuthenticationError('Authentication rejected. Stop credential retries and new claims.')
            _,tip,_=cleanup.refresh_snapshot(client)
            confirmed=True;seen_request=False
            for name in changed:
                actual=board.git(directory,'show',tip+':'+name,check=False)
                matched=not actual.returncode and json.loads(actual.stdout).get('request_id')==request_id
                seen_request=seen_request or matched
                if not matched:confirmed=False
            if confirmed:
                result={'status':'pushed','request_id':request_id,'actor':actor,'remote_tip':tip,'results':results}
                if selection is not None:result['selection']=selection
                curation._write_json(receipt,{'intent':intent,'result':result});pending.unlink(missing_ok=True);targets.unlink(missing_ok=True);return result
            if pushed.returncode and not board.push_race(pushed):
                raise TaskWriteError('Task write not confirmed; pending request '+request_id)
            if automatic and pushed.returncode and board.push_race(pushed) and not seen_request:
                # A definite CAS rejection never published our selection. Pick
                # other free tasks on the next snapshot instead of losing a race
                # over the same IDs. Unknown delivery keeps its original targets.
                targets.unlink(missing_ok=True)
        except (board.AuthenticationError,TaskWriteError):raise
        except board.BoardError as exc:last_error=exc
        if attempt+1<8:board.retry_pause(request_id,attempt)
    raise board.BoardError(str(last_error or 'Concurrent task update could not be confirmed')+
                          '; pending request '+request_id+'; retry with curation-task retry --run '+run+' --request-id '+request_id)


def mutate(root,run,task,operation,*,assets=None,reason=None,draft_note=None,write_paths=None,reuse_paths=None):
    op={'task_id':task,'operation':operation}
    op.update({k:v for k,v in dict(assets=assets,reason=reason,draft_note=draft_note,write_paths=write_paths,reuse_paths=reuse_paths).items() if v is not None})
    result=mutate_many(root,run,[op]);row=result['results'][0]
    if row['status']!='pushed':raise ValueError(row.get('detail','Task was not changed'))
    return dict(result,task_id=task,operation=operation)


def claim_next(root,run,limit=1,prefix=''):
    return mutate_many(root,run,[{'operation':'claim-next','limit':limit,'prefix':prefix}])


def retry_request(root,run,request_id):
    board.valid_id(request_id)
    client=board.Board(root,branch=coordination.config(root,'wcg.branch'))
    folder=client.cache/'curation-outbox';done=folder/(request_id+'.done.json')
    if done.is_file():
        saved=json.loads(done.read_text())
        if saved['intent']['actor']!=coordination.config(root,'wcg.actor') or saved['intent']['run']!=run:raise ValueError('Request belongs to another actor/run')
        return saved['result']
    record=json.loads((folder/(request_id+'.json')).read_text())
    if record['run']!=run or record['actor']!=coordination.config(root,'wcg.actor'):raise ValueError('Request belongs to another run/actor')
    return mutate_many(root,run,record['operations'],request_id=request_id)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    for command in ['plan','status','list','show','claim','claim-next','extend','submit','complete','finish','handoff','batch','handoff-all','retry']:
        q=sub.add_parser(command);q.add_argument('--run',required=True)
        if command in {'plan','batch'}:q.add_argument('--record-file',required=True)
        elif command=='retry':q.add_argument('--request-id',required=True)
        elif command not in {'list','status','handoff-all','claim-next'}:q.add_argument('task')
        if command=='claim-next':q.add_argument('--limit',type=int,default=1);q.add_argument('--prefix',default='')
        if command in {'submit','finish'}:
            q.add_argument('--assets-file',required=True);q.add_argument('--reuse-paths-file')
        if command in {'extend','claim'}:q.add_argument('--paths-file',required=command=='extend')
        if command in {'complete','finish','handoff','handoff-all'}:q.add_argument('--reason',required=True)
        if command in {'handoff','handoff-all'}:q.add_argument('--draft-note')
        if command=='list':
            q.add_argument('--state');q.add_argument('--owner');q.add_argument('--available',action='store_true');q.add_argument('--limit',type=int)
            mode=q.add_mutually_exclusive_group();mode.add_argument('--full',action='store_true');mode.add_argument('--compact',action='store_true')
        if command=='status':q.add_argument('--full',action='store_true')
    a=p.parse_args();root=a.repo.resolve()
    try:
        if a.command=='plan':result=plan(root,a.run,a.record_file)
        elif a.command=='status':result=task_status(root,a.run,full=a.full)
        elif a.command=='list':result=task_list(root,a.run,state='available' if a.available else a.state,owner=a.owner,limit=a.limit,full=a.full)
        elif a.command=='show':result=json.loads(task_path(root,a.run,a.task).read_text())
        elif a.command=='batch':result=mutate_many(root,a.run,json.loads(curation._safe_path(root,a.record_file).read_text()))
        elif a.command=='claim-next':result=claim_next(root,a.run,a.limit,a.prefix)
        elif a.command=='retry':result=retry_request(root,a.run,a.request_id)
        elif a.command=='handoff-all':result=mutate_many(root,a.run,[{'operation':'handoff-all','reason':a.reason,'draft_note':a.draft_note}])
        else:
            assets=json.loads(curation._safe_path(root,a.assets_file).read_text()) if a.command in {'submit','finish'} else None
            write_paths=json.loads(curation._safe_path(root,a.paths_file).read_text()) if getattr(a,'paths_file',None) else None
            reuse_paths=json.loads(curation._safe_path(root,a.reuse_paths_file).read_text()) if getattr(a,'reuse_paths_file',None) else None
            result=mutate(root,a.run,a.task,a.command,assets=assets,reason=getattr(a,'reason',None),draft_note=getattr(a,'draft_note',None),write_paths=write_paths,reuse_paths=reuse_paths)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,board.BoardError) as e:raise SystemExit(str(e))

if __name__=='__main__':main()
