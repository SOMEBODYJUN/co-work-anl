"""Frozen-source reading and concurrent per-file semantic-cleaning receipts."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time, uuid
from pathlib import Path
from urllib.parse import quote
import board

COMPLETE={'integrated','retained','duplicate','retired'}


def inventory(root):
    data=(root/'cleanup/inventory.jsonl').read_bytes()
    meta=json.loads((root/'cleanup/sources.json').read_text())
    if hashlib.sha256(data).hexdigest()!=meta['inventory_sha256']:
        raise ValueError('Frozen inventory changed; register a separate source increment')
    return [json.loads(line) for line in data.decode().splitlines() if line]


def progress(root, sid):
    p=root/'cleanup/progress'/f'{sid}.json'
    return json.loads(p.read_text()) if p.exists() else {}


def stats(root):
    rows=inventory(root);states=[progress(root,r['id']) for r in rows]
    hold=root/'cleanup/local-unpublished.json'
    local=json.loads(hold.read_text()).get('items',[]) if hold.exists() else []
    return {'source_versions':len(rows),'distinct_paths':len({r['path'] for r in rows}),
            'completed':sum(s.get('disposition') in COMPLETE for s in states),
            'claimed':sum(s.get('owner') is not None and s.get('disposition') not in COMPLETE for s in states),
            'unresolved':sum(s.get('disposition')=='needs-decision' for s in states),
            'local_source_hold':len(local)}


def coverage(root):
    rows=inventory(root);directory=root/'cleanup/checklists';directory.mkdir(exist_ok=True)
    pages=[]
    for start in range(0,len(rows),200):
        part=rows[start:start+200];name=f'{start//200+1:04d}.md'
        lines=['# 来源逐文件勾选（程序从语义处置记录生成）','',
               '勾选只表示该源版本已有完整处置声明；其正确性仍由清洗者负责。搜索到、只读摘要、搬动文件均不够。','']
        for row in part:
            state=progress(root,row['id']);done=state.get('disposition') in COMPLETE
            source=row['sources'][0]
            url='https://github.com/SOMEBODYJUN/co-work-anl/blob/'+source['commit']+'/'+quote(row['path'])
            label=row['path'].replace('[','\\[').replace(']','\\]')
            lines.append(f"- [{'x' if done else ' '}] `{row['id']}` [{label}]({url}) · {row['blob'][:8]} · {state.get('disposition','unread')} · {state.get('owner','未认领')}")
        (directory/name).write_text('\n'.join(lines)+'\n');pages.append(name)
    s=stats(root)
    lines=['# 全量清点与勾选','',f"远端源版本 {s['source_versions']}；不同路径 {s['distinct_paths']}；语义处置完成 {s['completed']}；认领中 {s['claimed']}；待裁决 {s['unresolved']}；另有本地来源待处理 {s['local_source_hold']}。",'',
           '分母固定于 sources.json 的提交和 inventory.jsonl。进度来源为 progress/ 下逐文件记录；机器生成本页和分册。','']
    lines += [f'- [第{i+1}册](checklists/{p})' for i,p in enumerate(pages)]
    (root/'cleanup/CHECKLIST.md').write_text('\n'.join(lines)+'\n')
    return s


def resolve(rows, text):
    found=[r for r in rows if r['id']==text or r['path']==text or r['id'].startswith(text)]
    if len(found)!=1:
        raise ValueError('Source ID/path must identify exactly one version: '+text)
    return found[0]


def show(root,sid,output=None):
    row=resolve(inventory(root),sid);source=row['sources'][0];commit=source['commit']
    probe=board.git(root,'cat-file','-e',commit+':'+row['path'],check=False)
    if probe.returncode:
        board.git(root,'fetch','--quiet','--no-tags','origin',commit)
    data=board.git(root,'show',commit+':'+row['path']).stdout
    if hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise ValueError('Source content hash mismatch')
    if output:
        target=Path(output).resolve();target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        print(json.dumps({'source':row,'output':str(target)},ensure_ascii=False))
    else:
        try:text=data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('Binary source: use show ID --out PATH, then inspect with the appropriate reader')
        print(text,end='')


def search(root, query, pattern='*.md', limit=30):
    rows=inventory(root)
    lookup={(s['commit'],s['path']):r for r in rows for s in r['sources']}
    snapshots=json.loads((root/'cleanup/sources.json').read_text())['snapshots']
    found=[];seen=set()
    for snapshot in snapshots:
        commit=snapshot['commit']
        if board.git(root,'cat-file','-e',commit,check=False).returncode:
            board.git(root,'fetch','--quiet','--no-tags','origin',commit)
        r=board.git(root,'-c','core.quotePath=false','grep','-n','-I','-F','-e',query,commit,'--',pattern,check=False)
        if r.returncode not in (0,1):
            raise ValueError('Could not search frozen source')
        for line in r.stdout.decode(errors='replace').splitlines():
            fields=line.split(':',3)
            if len(fields)!=4:continue
            c,path,number,text=fields;row=lookup.get((c,path))
            if row is None:continue
            key=(row['blob'],number,text)
            if key in seen:continue
            seen.add(key);found.append({'id':row['id'],'commit':c,'path':path,'line':number,'text':text})
            if limit and len(found)>=limit:return found
    return found


def validate_receipt(directory, item):
    for key in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'):
        if item.get(key) is not True:
            raise ValueError('Semantic completion requires an explicit true declaration: '+key)
    for key in ('read_note','comparison_note','decision_note'):
        if not isinstance(item.get(key),str) or not item[key].strip():
            raise ValueError('Explain actual work in '+key)
    if item.get('disposition') not in COMPLETE|{'needs-decision'}:
        raise ValueError('Unknown disposition')
    targets=item.get('targets',[])
    if not isinstance(targets,list) or not all(isinstance(p,str) for p in targets):
        raise ValueError('targets must be a list of repository-relative files')
    if item['disposition'] in {'integrated','retained','duplicate'} and not targets:
        raise ValueError('Useful/absorbed content requires concrete target files')
    for name in targets:
        target=(directory/name.split('#')[0]).resolve()
        if not target.is_relative_to(directory.resolve()) or not target.is_file():
            raise ValueError('Target must already be pushed to the result branch: '+name)
    if item['disposition']=='integrated' and not any(p.endswith('.md') or '.md#' in p for p in targets):
        raise ValueError('Integrated mathematical knowledge needs an explanatory Markdown target')
    board.guard(item)


def mutate(root, operation, ids=(), prefix=None, limit=20, records=()):
    actor=board.git(root,'config','--local','--get','wcg.actor').stdout.decode().strip()
    branch=board.git(root,'config','--local','--get','wcg.branch').stdout.decode().strip()
    client=board.Board(root,branch=branch,retries=20);request_id=uuid.uuid4().hex
    for attempt in range(20):
        with client.scratch() as name:
            directory=Path(name);client.setup(directory);client.checkout(directory)
            rows=inventory(directory);by_id={r['id']:r for r in rows}
            chosen=[]
            if operation=='claim' and prefix is not None:
                chosen=[r for r in rows if r['path'].startswith(prefix)
                        and progress(directory,r['id']).get('disposition') not in COMPLETE
                        and progress(directory,r['id']).get('owner') in (None,actor)]
                if limit:chosen=chosen[:limit]
            elif operation=='done':
                chosen=[resolve(rows,item['id']) for item in records]
            else:chosen=[resolve(rows,sid) for sid in ids]
            if not chosen:raise ValueError('No eligible source files')
            if len({r['id'] for r in chosen})!=len(chosen):raise ValueError('Duplicate source in one operation')
            updates=[]
            for index,row in enumerate(chosen):
                sid=row['id'];old=progress(directory,sid)
                if old.get('owner') not in (None,actor):
                    raise ValueError('Source is claimed by '+old['owner']+': '+sid)
                if operation=='claim':
                    if old.get('disposition') in COMPLETE:raise ValueError('Already completed: '+sid)
                    new=dict(old,owner=actor,disposition='in-progress')
                elif operation=='release':
                    if old.get('disposition') in COMPLETE:raise ValueError('Completed items need explicit editorial correction, not release')
                    new=dict(old,owner=None,disposition='unread')
                else:
                    if old.get('owner')!=actor:raise ValueError('Claim the source before recording its semantic disposition')
                    item=records[index];validate_receipt(directory,item)
                    new=dict(item,id=sid,owner=actor)
                new.update(id=sid,source_sha256=row['sha256'],request_id=request_id,updated=int(time.time()))
                dest=directory/'cleanup/progress'/f'{sid}.json';dest.parent.mkdir(exist_ok=True)
                dest.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n');updates.append(sid)
            coverage(directory)
            board.git(directory,'add','cleanup/progress','cleanup/CHECKLIST.md','cleanup/checklists')
            board.git(directory,'commit','--quiet','-m',f'cleanup {operation}: {actor} ({len(updates)} source versions)')
            pushed=board.git(directory,'push','--quiet','origin','HEAD:refs/heads/'+branch,check=False)
            # Check actual remote state even if the push response was lost.
            board.git(directory,'fetch','--quiet','--no-tags','origin','refs/heads/'+branch)
            remote=board.git(directory,'rev-parse','FETCH_HEAD').stdout.decode().strip()
            confirmed=True
            for sid in updates:
                blob=board.git(directory,'show',remote+':cleanup/progress/'+sid+'.json',check=False)
                if blob.returncode or json.loads(blob.stdout).get('request_id')!=request_id:
                    confirmed=False;break
            if confirmed:return {'status':'pushed','operation':operation,'actor':actor,'ids':updates,'remote_tip':remote,'note':'Declared semantic work; field checks do not prove mathematical correctness. Run sync before further shared-file edits.'}
        time.sleep(min(.4,.03*(attempt+1)))
    raise ValueError('Concurrent updates could not be confirmed; no completion reported')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('status');li=sub.add_parser('list');li.add_argument('--prefix',default='');li.add_argument('--limit',type=int,default=30)
    sh=sub.add_parser('show');sh.add_argument('id');sh.add_argument('--out')
    se=sub.add_parser('search');se.add_argument('query');se.add_argument('--path',default='*.md');se.add_argument('--limit',type=int,default=30)
    cl=sub.add_parser('claim');cl.add_argument('ids',nargs='*');cl.add_argument('--prefix');cl.add_argument('--limit',type=int,default=20)
    re=sub.add_parser('release');re.add_argument('ids',nargs='+')
    dn=sub.add_parser('done');dn.add_argument('--record-file',type=Path,required=True)
    sub.add_parser('coverage');a=p.parse_args();root=a.repo.resolve()
    if a.command=='show':show(root,a.id,a.out);return
    if a.command=='search':
        if a.limit<0:raise ValueError('limit must be nonnegative')
        result=search(root,a.query,a.path,a.limit)
    elif a.command=='status':result=stats(root)
    elif a.command=='coverage':result=coverage(root)
    elif a.command=='list':
        if a.limit<0:raise ValueError('limit must be nonnegative')
        rows=[dict(r,progress=progress(root,r['id'])) for r in inventory(root) if r['path'].startswith(a.prefix)]
        result=rows[:a.limit] if a.limit else rows
    elif a.command=='done':
        records=json.loads(a.record_file.read_text());records=records if isinstance(records,list) else [records]
        result=mutate(root,'done',records=records)
    else:
        if getattr(a,'limit',0)<0:raise ValueError('limit must be nonnegative')
        result=mutate(root,a.command,getattr(a,'ids',()),getattr(a,'prefix',None),getattr(a,'limit',20))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,board.BoardError,KeyError) as exc:raise SystemExit(str(exc))
