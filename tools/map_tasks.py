"""One phase-bound CAS queue for registration and mathematical hypergraph work."""
from __future__ import annotations
import argparse
import contextlib
import fcntl
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import uuid

import board
import cleanup
import coordination
from curation import _safe_path
import research_runtime as research
import registration
from research_runtime import _write_json

ACTIVE = {'claimed', 'blocked'}
PHASES = {'registration': ('curator', 'p25-register-v2'), 'map': ('mapper', 'map-v2')}


class TaskBusy(ValueError):
    """Ordinary competition; claim-next may choose another available task."""


def binding(root, phase='map', local=False):
    if phase not in PHASES: raise ValueError('Unknown workflow phase')
    run = coordination.config(root, 'wcg.workflowRun')
    if run:
        name = 'research/operations/' + research.identity(run)
        conf = json.loads(_safe_path(root, name + '/run.json').read_text())
        role, _ = PHASES[phase]
        if conf.get('phase') != phase or conf.get('role') != role:
            raise ValueError('This clone belongs to another workflow phase')
        if coordination.config(root, 'wcg.role') != role:
            raise ValueError('Workflow role differs from this clone binding')
        if coordination.config(root, 'wcg.boardBranch') != conf.get('board_branch'):
            raise ValueError('Workflow board differs from this clone binding')
        return {'phase':phase, 'run':run, 'home':name, 'config':conf, 'local':local}
    if not local:
        raise ValueError('Start this phase with --workflow-run before shared queue operations')
    return {'phase':phase, 'run':PHASES[phase][1],
            'home':'research/operations/' + PHASES[phase][1], 'config':{}, 'local':True}


def _ensure(root, name):
    """Materialize only a needed file in our disposable sparse snapshot."""
    path=_safe_path(root,name)
    if not path.is_file() and (Path(root)/'.git/workflow-snapshot').is_file():
        fetched=board.git(root,'show','HEAD:'+name,check=False)
        if not fetched.returncode:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(fetched.stdout)
    return path


def _ref_bytes(root,ref):
    _ensure(root,ref['path'])
    return research.ref_bytes(root,ref)


def _load(root,name,verify=False):
    _ensure(root,name)
    return research.load(root,name,verify=verify)


def _refresh(client):
    key=hashlib.sha256((client.remote+'\0'+client.branch).encode()).hexdigest()[:16]
    cache=client.cache/('workflow-snapshot-'+key+'.git')
    with (client.cache/('workflow-snapshot-'+key+'.lock')).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if not cache.exists():
            board.git(client.repo,'init','--quiet','--bare',str(cache));board.git(cache,'remote','add','origin',client.remote)
            objects=Path(board.git(client.repo,'rev-parse','--git-path','objects').stdout.decode().strip())
            objects=(client.repo/objects).resolve() if not objects.is_absolute() else objects
            info=cache/'objects/info';info.mkdir(exist_ok=True);(info/'alternates').write_text(str(objects)+'\n')
        if board.git(cache,'remote','get-url','origin').stdout.decode().strip()!=client.remote:raise ValueError('Workflow snapshot remote changed')
        board.git(cache,'config','remote.origin.promisor','true');board.git(cache,'config','remote.origin.partialclonefilter','blob:none')
        board.git(cache,'fetch','--quiet','--no-tags','--depth=1','--filter=blob:none','origin','+refs/heads/'+client.branch+':refs/heads/snapshot')
        tip=board.git(cache,'rev-parse','refs/heads/snapshot').stdout.decode().strip()
        shallow=(cache/'shallow').read_bytes() if (cache/'shallow').exists() else None
    return cache,tip,shallow


def _checkout(client,directory,ctx):
    cache,tip,shallow=_refresh(client);client.setup(directory)
    meta=Path(directory)/'.git';info=meta/'objects/info';info.mkdir(exist_ok=True);(info/'alternates').write_text(str(cache/'objects')+'\n')
    if shallow is not None:(meta/'shallow').write_bytes(shallow)
    board.git(directory,'config','remote.origin.promisor','true');board.git(directory,'config','remote.origin.partialclonefilter','blob:none')
    board.git(directory,'config','core.sparseCheckout','true')
    (meta/'info/sparse-checkout').write_text('/'+ctx['home']+'/\n')
    (meta/'workflow-snapshot').write_text('Disposable metadata-first workflow snapshot\n')
    board.git(directory,'checkout','--quiet','--detach',tip)


@contextlib.contextmanager
def latest(root,phase='map',local=False):
    ctx=binding(root,phase,local)
    if local:yield root,ctx;return
    branch=coordination.config(root,'wcg.branch')
    if not branch:raise ValueError('Start this independent phase clone first')
    client=board.Board(root,branch=branch,retries=8)
    with client.scratch() as temporary:
        directory=Path(temporary);_checkout(client,directory,ctx)
        yield directory,ctx


def task_path(root, task_id, phase='map', ctx=None):
    research.identity(task_id)
    if ctx is not None: return _safe_path(root, ctx['home']+'/tasks/'+task_id+'.json')
    run = coordination.config(root, 'wcg.workflowRun')
    return _safe_path(root, ('research/operations/'+research.identity(run)+'/tasks/' if run else 'map/tasks/')+task_id+'.json')


def listing(root, phase='map', ctx=None):
    if ctx is None:
        run = coordination.config(root, 'wcg.workflowRun')
        directory = _safe_path(root, 'research/operations/'+research.identity(run)+'/tasks' if run else 'map/tasks')
    else: directory = _safe_path(root, ctx['home']+'/tasks')
    return [json.loads(p.read_text()) for p in sorted(directory.glob('*.json'))]


def overlap(a, b):
    x,y=PurePosixPath(a),PurePosixPath(b)
    return x==y or x in y.parents or y in x.parents


def dependencies(definition):
    result=definition.get('depends_on',[])
    research.strings(result,'depends_on')
    for task in result: research.identity(task)
    if definition['task_id'] in result: raise ValueError('A task cannot depend on itself')
    return result


def validate(root, definition, phase='map'):
    research.identity(definition['task_id'])
    research.nonempty(definition,['goal'])
    dependencies(definition)
    superseded_ids(definition)
    research.strings(definition.get('write_paths'),'write_paths',True)
    for path in definition['write_paths']:
        _safe_path(root,path)
        if phase=='registration':
            if not path.startswith(('research/registration/batches/','research/registration/receipts/','research/workspaces/')):
                raise ValueError('Registration tasks write independent batches or workspaces')
        elif not path.startswith(('map/','research/workspaces/')) and not re.fullmatch(r'archives/[^/]+(?:/subarchives/[^/]+)*/map(?:/.*)?',path):
            raise ValueError('Map tasks write map outputs or research workspaces')
    if phase=='registration':
        if definition.get('stage')!='registration': raise ValueError('Registration stage required')
        baseline=json.loads(_ref_bytes(root,definition['baseline']))
        frozen={r['path']:r for r in baseline['materials']}
        refs=definition.get('materials')
        if not isinstance(refs,list) or not refs: raise ValueError('Explicit registration material refs required')
        seen=set()
        for ref in refs:
            _ref_bytes(root,ref)
            if ref['path'] in seen: raise ValueError('Duplicate task material')
            seen.add(ref['path'])
            if ref['path'] not in frozen or ref['sha256']!=frozen[ref['path']]['sha256']:
                raise ValueError('Task material is outside this frozen registration baseline')
    else:
        research.nonempty(definition,['registry'])
        _,objects=_load(root,definition['registry'],verify=False)
        core=definition.get('object_ids');reads=definition.get('read_object_ids',[])
        research.strings(core,'object_ids',True);research.strings(reads,'read_object_ids')
        if set(core)&set(reads): raise ValueError('Read-only objects must not duplicate core coverage')
        ids=set(core+reads)
        if ids-objects.keys(): raise ValueError('Task has unknown objects')
        if definition.get('input_pins')!={oid:research.pin(objects[oid]) for oid in ids}:
            raise ValueError('Task input objects changed; hand off and plan a reframed task')
        for oid in ids:
            _ref_bytes(root,objects[oid]['body'])
            for ref in objects[oid]['evidence']:_ref_bytes(root,ref)
        if definition.get('stage') not in {'3A','3B','3C','3D'}:raise ValueError('Explicit map stage required')
    board.guard(definition)


def lead_path(root,ctx):return _safe_path(root,ctx['home']+'/lead.json')

def lead_record(root,ctx):
    p=lead_path(root,ctx)
    return json.loads(p.read_text()) if p.exists() else {'owner':None,'state':'available'}

def require_lead(root,ctx,actor,instance=None):
    row=lead_record(root,ctx)
    if row.get('owner')!=actor or row.get('state')!='claimed' or (instance and row.get('instance')!=instance):
        raise ValueError('Only this workflow coordinator/integrator may plan, reclaim or assemble')
    return row


def _request(row,request_id,operation):
    row['request_id']=request_id
    row.setdefault('requests',{})[request_id]=operation
    return row


def _task_keys(definition,phase):
    # The same source may contain several Claims. Reading it is shared; only
    # explicit output paths (and map core objects) are exclusive.
    return set() if phase=='registration' else set(definition['object_ids'])


def _asset_refs(root,definition,receipt):
    assets=receipt.get('assets')
    if not isinstance(assets,list) or not assets:raise ValueError('Already-pushed batch assets required')
    canonical=None
    for ref in assets:
        name=ref['path']
        if not any(name==p or PurePosixPath(p) in PurePosixPath(name).parents for p in definition['write_paths']):
            if definition.get('stage') in {'3A','3B','3C','3D'}:
                if canonical is None:canonical=set(_load(root,definition['registry'],verify=False)[0].get('edge_files',[]))
                if name not in canonical:raise ValueError('New assets require reserved write scope; only unchanged published canonical edges may be shared')
            else:raise ValueError('Asset outside reserved write scope')
        _ref_bytes(root,ref)
    return assets


def batch_edges(root,definition,receipt,objects):
    files=[]
    for ref in receipt['assets']:
        if not ref['path'].endswith('.json'):continue
        try:row=json.loads(_ref_bytes(root,ref))
        except (ValueError,UnicodeError):continue
        if isinstance(row,dict) and 'edge_id' in row:
            ids=set(row.get('source_ids',[])+row.get('target_ids',[]))
            permitted=set(definition['object_ids']+definition.get('read_object_ids',[]))
            if not ids<=permitted or not ids.intersection(definition['object_ids']):
                raise ValueError('Batch edge endpoints require a core object and declared read dependencies')
            for evidence in row.get('evidence',[]):_ref_bytes(root,evidence)
            files.append(ref['path'])
    return research.edges(root,{'edge_files':files},objects),files


def _registration_done(root,definition,receipt):
    ref=receipt.get('batch_file')
    if ref not in receipt['assets']:raise ValueError('batch_file must be an already-pushed reserved asset')
    record=json.loads(_ref_bytes(root,ref))
    own={obj['object_id']:obj for obj in record.get('objects',[])}
    external={oid for row in record.get('materials',[]) for oid in row.get('object_ids',[])}-own.keys()
    if external:
        path=_ensure(root,research.REGISTRY)
        existing=json.loads(path.read_text()) if path.exists() else {}
        own.update({obj['object_id']:obj for obj in existing.get('objects',[]) if obj['object_id'] in external})
    for obj in own.values():
        _ref_bytes(root,obj['body'])
        for evidence in obj.get('evidence',[]):_ref_bytes(root,evidence)
    registration.validate_batch(root,record,definition['materials'],definition['baseline'])


def superseded_ids(definition):
    ids=definition.get('supersedes',[]);research.strings(ids,'supersedes')
    for task in ids:research.identity(task)
    if definition['task_id'] in ids:raise ValueError('A batch cannot supersede itself')
    return ids


def _replacement_scope(definition,old,phase):
    if phase=='registration':
        if definition['baseline'] != old['definition']['baseline']:
            raise ValueError('New frozen material versions use incremental composition; do not supersede registration tasks across baselines')
        current={r['path'] for r in definition['materials']};previous={r['path'] for r in old['definition']['materials']}
    else:
        current=set(definition['object_ids']);previous=set(old['definition']['object_ids'])
    if not previous<=current:raise ValueError('A replacement must cover every old core object/material; split its explicit disposition first')


def _supersession(root,definition,receipt,rows,phase):
    targets=superseded_ids(definition)
    notes=receipt.get('supersession',{})
    if set(notes)!=set(targets):raise ValueError('One explicit supersession note per replaced batch required')
    known={r['definition']['task_id']:r for r in rows}
    current={r['path']:r for r in receipt['assets']};retired=set()
    for task in targets:
        old=known.get(task)
        if not old or old['state']!='done':raise ValueError('Only a completed batch can be explicitly superseded: '+task)
        _replacement_scope(definition,old,phase)
        note=notes[task];research.nonempty(note,['reason'])
        dispositions=note.get('assets',{});previous={r['path']:r for r in old['receipt']['assets']}
        if set(dispositions)!=set(previous):raise ValueError('Every old batch asset needs a retained/replaced/retired disposition')
        for name,decision in dispositions.items():
            research.nonempty(decision,['reason'])
            kind=decision.get('disposition')
            if kind=='retained':
                if current.get(name)!=previous[name]:raise ValueError('Retained assets must be present byte-for-byte in the replacement receipt')
            elif kind=='replaced':
                replacements=decision.get('replacement_paths',[]);research.strings(replacements,'replacement_paths',True)
                if set(replacements)-current.keys():raise ValueError('Replacement paths must be actual current batch assets')
                if name not in replacements:retired.add(name)
            elif kind=='retired':retired.add(name)
            else:raise ValueError('Unknown old-asset disposition')
    return retired


def transition(root,old,others,actor,operation,request_id,receipt=None,reason=None,phase='map'):
    new=copy.deepcopy(old);definition=old['definition']
    # Release works even after a legitimate proof/version change made old pins stale.
    if operation=='handoff':
        if old.get('owner')!=actor or old['state'] not in ACTIVE:raise ValueError('Only hand off own unfinished task')
        if not reason or not reason.strip():raise ValueError('Concrete handoff reason required')
        new.update(state='handoff',owner=None,previous_owner=actor,reason=reason)
    else:
        validate(root,definition,phase)
        if operation=='claim':
            if old['state'] not in {'available','handoff'} or old.get('owner'):raise TaskBusy('Task unavailable')
            states={r['definition']['task_id']:r['state'] for r in others}
            if any(states.get(t)!='done' for t in dependencies(definition)):raise TaskBusy('Prerequisite tasks are not done')
            for other in others:
                if other['definition']['task_id']==definition['task_id'] or other['state'] not in ACTIVE:continue
                d=other['definition']
                if _task_keys(d,phase)&_task_keys(definition,phase) or any(overlap(a,b) for a in d['write_paths'] for b in definition['write_paths']):
                    raise TaskBusy('Overlapping active task: '+d['task_id'])
            new.update(state='claimed',owner=actor)
        elif operation=='done':
            if old.get('owner')!=actor or old['state'] not in ACTIVE:raise ValueError('Only task owner may finish')
            if not isinstance(receipt,dict):raise ValueError('Explicit batch receipt required')
            _asset_refs(root,definition,receipt)
            for target in superseded_ids(definition):
                if any(r['state']=='done' and r['definition']['task_id']!=definition['task_id'] and target in superseded_ids(r['definition']) for r in others):
                    raise ValueError('An old batch already has a completed successor; supersede that current successor instead: '+target)
            _supersession(root,definition,receipt,others,phase)
            if phase=='registration':_registration_done(root,definition,receipt)
            else:
                if set(receipt.get('coverage',{}))!=set(definition['object_ids']):raise ValueError('Every core object needs coverage')
                _,objects=_load(root,definition['registry'],verify=False)
                relations,_=batch_edges(root,definition,receipt,objects)
                for row in receipt['coverage'].values():
                    if row.get('state') not in {'linked','isolated-after-review','needs-decision'}:raise ValueError('Unknown coverage outcome')
                    research.nonempty(row,['reason','comparison_scope','object_pin'])
                for oid,row in receipt['coverage'].items():
                    if row['object_pin']!=research.pin(objects[oid]):raise ValueError('Stale coverage input: '+oid)
                resolved={oid:r for oid,r in receipt['coverage'].items() if r['state']!='needs-decision'}
                research.validate_coverage(resolved,{oid:objects[oid] for oid in resolved},relations)
            new.update(state='done',receipt=receipt)
        else:raise ValueError('Unknown task operation')
    _request(new,request_id,operation);board.guard(new);return new


def _verify_actor(caller,directory,ctx,actor,instance):
    conf=json.loads(_safe_path(directory,ctx['home']+'/run.json').read_text())
    if conf.get('phase')!=ctx['phase'] or conf.get('role')!=PHASES[ctx['phase']][0] or conf.get('board_branch')!=ctx['config'].get('board_branch'):
        raise ValueError('Remote workflow phase/role/board changed')
    person=_safe_path(directory,ctx['home']+'/people/'+actor+'.json')
    if not person.is_file() or json.loads(person.read_text()).get('instance')!=instance:
        raise ValueError('Boss identity is not registered for this workflow')


def _plan(root,records,ctx,actor,instance,request_id):
    require_lead(root,ctx,actor,instance)
    current=listing(root,ctx=ctx);known={r['definition']['task_id']:r['definition'] for r in current};new={}
    for record in records:
        validate(root,record,ctx['phase']);task=record['task_id']
        if task in known or task in new:raise ValueError('Duplicate/existing task; preserve ownership')
        new[task]=record
    combined={**known,**new}
    for record in new.values():
        if set(dependencies(record))-combined.keys():raise ValueError('Unknown prerequisite task')
        for target in superseded_ids(record):
            old=next((r for r in current if r['definition']['task_id']==target),None)
            if not old or old['state']!='done':raise ValueError('supersedes names an existing done batch: '+target)
            _replacement_scope(record,old,ctx['phase'])
    visiting=set();done=set()
    def visit(task):
        if task in visiting:raise ValueError('Cyclic task prerequisites')
        if task in done:return
        visiting.add(task)
        for parent in dependencies(combined[task]):visit(parent)
        visiting.remove(task);done.add(task)
    for task in combined:visit(task)
    paths=[]
    for task,definition in new.items():
        row=_request({'definition':definition,'state':'available','owner':None},request_id,'plan')
        path=task_path(root,task,ctx=ctx);_write_json(path,row);paths.append(path)
    lead=lead_record(root,ctx);_request(lead,request_id,'plan');_write_json(lead_path(root,ctx),lead);paths.append(lead_path(root,ctx))
    return paths,{'tasks':sorted(new)}


def _apply(root,ctx,actor,instance,intent,request_id):
    operation=intent['operation'];task_id=intent.get('task_id');reason=intent.get('reason');rows=listing(root,ctx=ctx)
    lead=lead_record(root,ctx)
    acknowledged=[r for r in [lead,*rows] if request_id in r.get('requests',{})]
    if acknowledged:
        recovered=[r['definition']['task_id'] for r in acknowledged if 'definition' in r]
        return [],dict(recovered_acknowledgement=True,tasks=recovered,**({'task_id':recovered[0]} if len(recovered)==1 else {}))
    if operation=='lead-claim':
        if lead.get('owner') and (lead['owner']!=actor or lead.get('instance')!=instance):raise TaskBusy('Another conversation is the workflow lead')
        lead.update(owner=actor,instance=instance,state='claimed');_request(lead,request_id,operation);_write_json(lead_path(root,ctx),lead)
        return [lead_path(root,ctx)],{'lead':lead}
    if operation=='lead-handoff':
        require_lead(root,ctx,actor,instance)
        if not reason or not reason.strip():raise ValueError('Concrete lead handoff reason required')
        lead.update(owner=None,state='handoff',previous_owner=actor,reason=reason);_request(lead,request_id,operation);_write_json(lead_path(root,ctx),lead)
        return [lead_path(root,ctx)],{'lead':lead}
    if operation=='plan':return _plan(root,intent['records'],ctx,actor,instance,request_id)
    if operation=='handoff-all':
        chosen=[r for r in rows if r.get('owner')==actor and r['state'] in ACTIVE]
        paths=[]
        for old in chosen:
            new=transition(root,old,rows,actor,'handoff',request_id,reason=reason,phase=ctx['phase']);path=task_path(root,old['definition']['task_id'],ctx=ctx);_write_json(path,new);paths.append(path)
        # Persist one acknowledgement even if another Boss later claims every released task.
        if chosen:
            lead.setdefault('requests',{})[request_id]=operation;_write_json(lead_path(root,ctx),lead);paths.append(lead_path(root,ctx))
        return paths,{'tasks':[r['definition']['task_id'] for r in chosen]}
    if operation=='claim-next':
        owned=[r['definition']['task_id'] for r in rows if r.get('owner')==actor and r['state'] in ACTIVE]
        reframing=[]
        # Existing work is visible but does not forbid taking a second batch for a free worker.
        choices=[r for r in rows if r['state'] in {'available','handoff'} and not r.get('owner') and r['definition']['task_id'].startswith(intent.get('prefix',''))]
        for old in choices:
            if old['definition'].get('stage')=='3D' and lead.get('owner')!=actor:continue
            try:new=transition(root,old,rows,actor,'claim',request_id,phase=ctx['phase'])
            except TaskBusy:continue
            except (ValueError,OSError,KeyError,TypeError) as exc:
                # Keep the stale row visible and unchanged; one old version
                # must not prevent useful work on later current batches.
                reframing.append({'task_id':old['definition']['task_id'],'error':str(exc)})
                continue
            path=task_path(root,old['definition']['task_id'],ctx=ctx);_write_json(path,new)
            return [path],{'task_id':old['definition']['task_id'],'task':new,'owned_tasks':owned,'needs_reframing':reframing}
        return [],{'status':'no-available-task','owned_tasks':owned,'needs_reframing':reframing,'instruction':'Resume owned work; the lead must explicitly reframe or withdraw listed stale tasks. An empty queue does not mean the phase is complete.'}
    matches=[r for r in rows if r['definition']['task_id']==task_id]
    if not matches:raise ValueError('Unknown task in this workflow: '+str(task_id))
    old=matches[0]
    if operation=='read-add':
        if ctx['phase']!='map':raise ValueError('Shared object reads apply to registered map objects')
        if old.get('owner')!=actor or old['state'] not in ACTIVE:raise ValueError('Only extend reads on your active task')
        validate(root,old['definition'],'map')
        extra=intent.get('read_ids') or [];research.strings(extra,'read object IDs',True)
        new=copy.deepcopy(old);definition=new['definition'];_,objects=_load(root,definition['registry'],verify=False)
        if set(extra)-objects.keys():raise ValueError('Unknown read object IDs')
        definition['read_object_ids']=list(dict.fromkeys(definition.get('read_object_ids',[])+[oid for oid in extra if oid not in definition['object_ids']]))
        definition['input_pins']={oid:research.pin(objects[oid]) for oid in definition['object_ids']+definition['read_object_ids']}
        validate(root,definition,'map');_request(new,request_id,operation)
    elif operation=='reclaim':
        require_lead(root,ctx,actor,instance)
        if old['state']=='done':raise ValueError('Do not reclaim completed mathematical work')
        if not old.get('owner') or old['state'] not in ACTIVE:raise ValueError('Only an explicitly unfinished owned task can be reclaimed')
        if not reason or not reason.strip():raise ValueError('Concrete coordinator reclaim reason required')
        new=copy.deepcopy(old);new.update(state='handoff',owner=None,previous_owner=old['owner'],reason=reason,reclaimed_by=actor);_request(new,request_id,operation)
    elif operation=='withdraw':
        require_lead(root,ctx,actor,instance)
        if old.get('owner') or old['state'] not in {'available','handoff'}:raise ValueError('Only withdraw an unowned unfinished task; hand off/reclaim active work first')
        if not reason or not reason.strip():raise ValueError('Concrete withdrawal/replanning reason required')
        new=copy.deepcopy(old);new.update(state='withdrawn',reason=reason,withdrawn_by=actor);_request(new,request_id,operation)
    else:
        if operation=='claim' and old['definition'].get('stage')=='3D':require_lead(root,ctx,actor,instance)
        new=transition(root,old,rows,actor,operation,request_id,intent.get('receipt'),reason,ctx['phase'])
    path=task_path(root,task_id,ctx=ctx);_write_json(path,new)
    return [path],{'task_id':task_id,'task':new}


def mutate(root,task_id,operation,receipt=None,reason=None,phase='map',records=None,prefix='',local=False,read_ids=None):
    ctx=binding(root,phase,local);actor=coordination.config(root,'wcg.actor') or ('Boss1' if local else '')
    instance=coordination.config(root,'wcg.instance') or ('local-offline' if local else '')
    if not re.fullmatch(r'Boss[1-9][0-9]*',actor):raise ValueError('Explicit Boss identity required')
    intent={'operation':operation,'task_id':task_id,'receipt':receipt,'reason':reason,'records':records,'prefix':prefix,'read_ids':read_ids}
    board.guard(intent)
    if local:
        paths,result=_apply(root,ctx,actor,instance,intent,uuid.uuid4().hex)
        return dict(result,status=result.get('status','local-only'),paths=[p.relative_to(root).as_posix() for p in paths])
    branch=coordination.config(root,'wcg.branch')
    if not branch:raise ValueError('Start this independent clone on the shared branch first')
    client=board.Board(root,branch=branch,retries=8)
    pending_dir=client.cache/'workflow-pending'/ctx['run'];pending_dir.mkdir(parents=True,exist_ok=True)
    key=hashlib.sha256((operation+'\0'+str(task_id or prefix)).encode()).hexdigest()[:24]
    pending_path=pending_dir/(key+'.json');intent_pin=research.pin(intent)
    if pending_path.exists():
        pending=json.loads(pending_path.read_text())
        if pending['intent_pin']!=intent_pin:raise ValueError('Unconfirmed operation exists; retry its original receipt/reason before replacing it')
        request_id=pending['request_id']
    else:
        request_id=uuid.uuid4().hex;_write_json(pending_path,{'request_id':request_id,'intent_pin':intent_pin,'intent':intent})
    for _ in range(8):
        with client.scratch() as temporary:
            directory=Path(temporary);_checkout(client,directory,ctx);_verify_actor(root,directory,ctx,actor,instance)
            paths,result=_apply(directory,ctx,actor,instance,intent,request_id)
            if not paths:
                pending_path.unlink(missing_ok=True)
                return dict(result,status=result.get('status','pushed'),request_id=request_id,remote_tip=board.git(directory,'rev-parse','HEAD').stdout.decode().strip())
            names=[p.relative_to(directory).as_posix() for p in paths]
            board.git(directory,'add','--',*names);board.git(directory,'commit','--quiet','-m',f'{phase} {operation}: {actor} {task_id or prefix}')
            pushed=board.git(directory,'push','--quiet','origin','HEAD:refs/heads/'+branch,check=False)
            if board.auth_rejected(pushed):raise board.AuthenticationError('Authentication rejected; retain work and stop new claims')
            _,tip,_=_refresh(client)
            for name in names:
                actual=board.git(directory,'show',tip+':'+name,check=False)
                if actual.returncode:continue
                row=json.loads(actual.stdout)
                if request_id in row.get('requests',{}) or row.get('request_id')==request_id:
                    pending_path.unlink(missing_ok=True)
                    return dict(result,status='pushed',request_id=request_id,remote_tip=tip)
            if pushed.returncode and not board.push_race(pushed):
                raise board.BoardError('Workflow write not confirmed; rerun the same operation with its saved request_id')
    raise board.BoardError('Concurrent workflow write not confirmed; preserve local work and rerun the same operation')


def plan(root,record_file,phase='map',local=False):
    records=json.loads(_safe_path(root,record_file).read_text())
    if isinstance(records,dict):records=[records]
    if not isinstance(records,list) or not records:raise ValueError('Explicit task definitions required')
    return mutate(root,None,'plan',phase=phase,records=records,local=local)


def collect(root,phase='map',local=False,ctx=None,baseline_ref=None):
    ctx=ctx or binding(root,phase,local);rows=[r for r in listing(root,ctx=ctx) if r['state']=='done']
    if not rows:raise ValueError('No completed published batches to collect')
    # Supersession becomes effective only after the replacement itself is done.
    # Old pins/assets may be stale, so validate the replacement closure rather
    # than re-admitting historical bytes which it explicitly disposed.
    retired=set();replaced=set()
    for row in rows:
        retired.update(_supersession(root,row['definition'],row['receipt'],rows,phase))
        replaced.update(superseded_ids(row['definition']))
    rows=[r for r in rows if r['definition']['task_id'] not in replaced]
    if not rows:raise ValueError('Cyclic batch supersession')
    if baseline_ref is not None:
        if phase!='registration':raise ValueError('Baseline filtering applies to registration batches')
        rows=[r for r in rows if r['definition']['baseline']==baseline_ref]
        if not rows:raise ValueError('No current completed registration batch for this baseline')
    for row in rows:
        validate(root,row['definition'],phase);_asset_refs(root,row['definition'],row['receipt'])
    if phase=='registration':
        baseline=rows[0]['definition']['baseline']
        if any(r['definition']['baseline']!=baseline for r in rows):raise ValueError('Completed batches refer to different baselines')
        for row in rows:_registration_done(root,row['definition'],row['receipt'])
        return {'baseline':baseline,'batches':[{'batch_id':r['definition']['task_id'],'record':r['receipt']['batch_file']} for r in rows], 'tasks':[r['definition']['task_id'] for r in rows], 'superseded_tasks':sorted(replaced)}
    registry=rows[0]['definition']['registry']
    if any(r['definition']['registry']!=registry for r in rows):raise ValueError('Map batches use different registries')
    _,objects=_load(root,registry,verify=False);files=[];coverage={};edge_paths={}
    for row in rows:
        relations,names=batch_edges(root,row['definition'],row['receipt'],objects)
        for name in names:
            edge=json.loads(_safe_path(root,name).read_text());eid=edge['edge_id']
            if eid in edge_paths and edge_paths[eid]!=name:raise ValueError('Duplicate edge identity across batch files: '+eid)
            edge_paths[eid]=name
            if name not in files:files.append(name)
        for oid,result in row['receipt']['coverage'].items():
            coverage.setdefault(oid,[]).append({'task_id':row['definition']['task_id'],'stage':row['definition']['stage'],'coverage':result})
    # A later replacement may retain an earlier file. Never remove a current
    # asset just because it was retired in an older step of the replacement chain.
    retired.difference_update(ref['path'] for row in rows for ref in row['receipt']['assets'])
    return {'registry':registry,'edge_files':sorted(files),'retired_edge_files':sorted(retired),'coverage_candidates':coverage,'tasks':[r['definition']['task_id'] for r in rows], 'superseded_tasks':sorted(replaced)}


def assemble(root,local=False):
    ctx=binding(root,'map',local);actor=coordination.config(root,'wcg.actor') or ('Boss1' if local else '')
    if local:require_lead(root,ctx,actor)
    if not local:
        # Queue CAS writes intentionally leave the worker clone untouched.
        # Never assemble that old view and silently omit other Bosses' work.
        with latest(root,'map') as (snapshot,remote_ctx):
            require_lead(snapshot,remote_ctx,actor,coordination.config(root,'wcg.instance'))
            remote_rows=listing(snapshot,ctx=remote_ctx)
            if listing(root,ctx=ctx)!=remote_rows or lead_record(root,ctx)!=lead_record(snapshot,remote_ctx):
                raise ValueError('Local workflow state is behind or differs from published batches; run work.py sync before assemble')
            remote_gathered=collect(snapshot,'map',ctx=remote_ctx)
            remote_registry=_ensure(snapshot,remote_gathered['registry']).read_bytes()
            if _safe_path(root,remote_gathered['registry']).read_bytes()!=remote_registry:
                raise ValueError('Local registry differs from the published input; checkpoint intended edits and run work.py sync before assemble')
        try:gathered=collect(root,'map',local)
        except (ValueError,OSError) as exc:
            raise ValueError('Local batch inputs/assets do not match the published snapshot; preserve edits and run work.py sync before assemble: '+str(exc)) from exc
        if gathered!=remote_gathered:raise ValueError('Local batch collection differs from remote; run work.py sync before assemble')
    else:gathered=collect(root,'map',local)
    data,objects=research.load(root,gathered['registry'])
    data['edge_files']=sorted((set(data.get('edge_files',[]))-set(gathered['retired_edge_files']))|set(gathered['edge_files']))
    relations=research.edges(root,data,objects);coverage={}
    for oid,obj in objects.items():
        rows=gathered['coverage_candidates'].get(oid,[]);incident=sorted(eid for eid,e in relations.items() if e['status']=='accepted' and oid in e['source_ids']+e['target_ids'])
        pending=not rows or any(r['coverage']['state']=='needs-decision' for r in rows)
        row={'state':'needs-decision' if pending else 'linked' if incident else 'isolated-after-review','object_pin':research.pin(obj),
             'comparison_scope':'\n'.join(r['stage']+' '+r['task_id']+': '+r['coverage']['comparison_scope'] for r in rows) or 'No completed comparison batch yet',
             'reason':'\n'.join(r['coverage']['reason'] for r in rows) or 'Assign a concrete comparison task'}
        if incident:row['edge_ids']=incident
        coverage[oid]=row
    coverage_path=_safe_path(root,'map/coverage.json');integration_path=_safe_path(root,'map/integration.json')
    # Never overwrite an existing integrator's actual comparison prose.
    draft={'reviewed_by':'','review_note':'','registry_pin':research.pin(data),
           'edge_pins':{eid:research.pin(e) for eid,e in relations.items() if e['status']=='accepted'},
           'object_pins':{oid:research.pin(obj) for oid,obj in objects.items()},
           'object_scopes':{oid:sorted(research.object_scopes({oid:obj})) for oid,obj in objects.items()},
           'edge_endpoints':{eid:sorted(set(e['source_ids']+e['target_ids'])) for eid,e in relations.items() if e['status']=='accepted'},
           'archive_reviews':{scope:{'comparison_scope':'','outcome':'Await actual cross-batch integration review','unresolved':['cross-batch review pending']} for scope in sorted(research.object_scopes(objects))},
           'cross_archive_review':{'comparison_scope':'','outcome':'Await actual cross-archive review','unresolved':['cross-archive review pending']}}
    affected=[]
    if integration_path.exists():
        previous=json.loads(integration_path.read_text())
        if previous.get('registry_pin')==draft['registry_pin'] and previous.get('edge_pins')==draft['edge_pins']:
            draft={**draft,**previous}
        else:
            changed_objects={oid for oid in set(previous.get('object_pins',{}))|objects.keys() if previous.get('object_pins',{}).get(oid)!=draft['object_pins'].get(oid)}
            changed_edges={eid for eid in set(previous.get('edge_pins',{}))|draft['edge_pins'].keys() if previous.get('edge_pins',{}).get(eid)!=draft['edge_pins'].get(eid)}
            for eid in changed_edges:
                changed_objects.update(previous.get('edge_endpoints',{}).get(eid,[]));changed_objects.update(draft['edge_endpoints'].get(eid,[]))
            scopes={scope for oid in changed_objects for scope in previous.get('object_scopes',{}).get(oid,[])+draft['object_scopes'].get(oid,[])}
            if not previous.get('object_pins'):scopes=set(draft['archive_reviews'])
            affected=sorted(scopes)
            draft['reviewed_by']=previous.get('reviewed_by','');draft['review_note']=previous.get('review_note','')
            for scope,row in draft['archive_reviews'].items():
                if scope in previous.get('archive_reviews',{}):row.update(copy.deepcopy(previous['archive_reviews'][scope]))
                if scope in scopes:
                    row['unresolved']=list(dict.fromkeys(row.get('unresolved',[])+['Updated inputs/relations require this preserved comparison to be reviewed again']))
            old_cross=copy.deepcopy(previous.get('cross_archive_review',draft['cross_archive_review']))
            old_cross['unresolved']=list(dict.fromkeys(old_cross.get('unresolved',[])+['Updated inputs/relations require cross-archive integration review']))
            draft['cross_archive_review']=old_cross
            draft['pending_changes']={'object_ids':sorted(changed_objects),'edge_ids':sorted(changed_edges),'archive_scopes':affected}
            removed={k:v for k,v in previous.get('archive_reviews',{}).items() if k not in draft['archive_reviews']}
            if removed:draft['retired_archive_reviews']={**previous.get('retired_archive_reviews',{}),**removed}
    _write_json(_safe_path(root,gathered['registry']),data);_write_json(coverage_path,coverage);_write_json(integration_path,draft)
    return {'status':'assembled-local-draft-not-final','registry':gathered['registry'],'edge_files':len(data['edge_files']),
            'coverage':'map/coverage.json','integration':'map/integration.json','unresolved_objects':[oid for oid,r in coverage.items() if r['state']=='needs-decision'],
            'affected_integration_scopes':affected,
            'instruction':'Read actual cross-batch/cross-archive links, finish integration prose, then research check/build --final; checkpoint exact files.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--phase',choices=sorted(PHASES),default='map');p.add_argument('--local-only',action='store_true',help='Explicit private offline rehearsal; never writes a remote')
    sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('inventory');q.add_argument('--registry',default=research.REGISTRY)
    q=sub.add_parser('plan');q.add_argument('--record-file',required=True)
    q=sub.add_parser('list');q.add_argument('--owner');q.add_argument('--available',action='store_true')
    sub.add_parser('status');sub.add_parser('collect');sub.add_parser('assemble')
    q=sub.add_parser('lead');q.add_argument('action',choices=['claim','handoff','show']);q.add_argument('--reason')
    q=sub.add_parser('claim-next');q.add_argument('--prefix',default='')
    q=sub.add_parser('read-add');q.add_argument('task_id');q.add_argument('--object-ids',nargs='+',required=True)
    for command in ['claim','done','handoff','reclaim','withdraw']:
        q=sub.add_parser(command);q.add_argument('task_id',nargs='?' if command=='handoff' else None)
        if command=='done':q.add_argument('--receipt-file',required=True)
        if command in {'handoff','reclaim','withdraw'}:q.add_argument('--reason',required=True)
        if command=='handoff':q.add_argument('--all',action='store_true')
    a=p.parse_args(argv);root=a.repo.resolve()
    if a.command=='inventory':result=research.inventory(root,a.registry)
    elif a.command=='plan':result=plan(root,a.record_file,a.phase,a.local_only)
    elif a.command=='assemble':
        if a.phase!='map':raise ValueError('Registration collects batches for research compose')
        result=assemble(root,a.local_only)
    elif a.command=='collect':
        with latest(root,a.phase,a.local_only) as (directory,ctx):result=collect(directory,a.phase,a.local_only,ctx)
    elif a.command in {'list','status'}:
        owner=coordination.config(root,'wcg.actor') if getattr(a,'owner',None)=='self' else getattr(a,'owner',None)
        if not coordination.config(root,'wcg.workflowRun') and not a.local_only:
            rows=listing(root,a.phase)
        else:
            with latest(root,a.phase,a.local_only) as (directory,ctx):rows=listing(directory,a.phase,ctx)
        if a.command=='status':result={'tasks':len(rows),'states':{state:sum(row['state']==state for row in rows) for state in ['available','claimed','blocked','done','handoff','withdrawn']}}
        else:result=[row for row in rows if (not owner or row.get('owner')==owner) and (not a.available or row['state'] in {'available','handoff'} and not row.get('owner'))]
    elif a.command=='lead' and a.action=='show':
        with latest(root,a.phase,a.local_only) as (directory,ctx):result=lead_record(directory,ctx)
    else:
        operation='lead-'+a.action if a.command=='lead' else 'handoff-all' if a.command=='handoff' and a.all else a.command
        if a.command=='handoff' and ((a.all and a.task_id) or (not a.all and not a.task_id)):raise ValueError('Use one task ID or --all')
        receipt=json.loads(_safe_path(root,a.receipt_file).read_text()) if a.command=='done' else None
        result=mutate(root,getattr(a,'task_id',None),operation,receipt,getattr(a,'reason',None),a.phase,prefix=getattr(a,'prefix',''),local=a.local_only,read_ids=getattr(a,'object_ids',None))
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError,board.BoardError) as exc:raise SystemExit(str(exc))
