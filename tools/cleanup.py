"""Frozen-source reading and concurrent per-file semantic-cleaning receipts."""
from __future__ import annotations
import argparse, fcntl, fnmatch, hashlib, json, subprocess, sys, time, uuid
from pathlib import Path
from urllib.parse import quote
import board

COMPLETE={'integrated','retained','duplicate','retired'}


def inventory(root):
    data=(root/'cleanup/inventory.jsonl').read_bytes()
    meta=json.loads((root/'cleanup/sources.json').read_text())
    if hashlib.sha256(data).hexdigest()!=meta['inventory_sha256']:
        raise ValueError('Frozen inventory changed; register a separate source increment')
    rows=[json.loads(line) for line in data.decode().splitlines() if line]
    if 'inventory_count' in meta and len(rows)!=meta['inventory_count']:
        raise ValueError('Frozen inventory count mismatch')
    for increment in meta.get('increments',[]):
        path=(root/increment['path']).resolve()
        if not path.is_relative_to((root/'cleanup/increments').resolve()):
            raise ValueError('Source increments must stay inside cleanup/increments')
        payload=path.read_bytes()
        if hashlib.sha256(payload).hexdigest()!=increment['sha256']:
            raise ValueError('Frozen source increment changed: '+increment['path'])
        added=[json.loads(line) for line in payload.decode().splitlines() if line]
        if len(added)!=increment['count']:
            raise ValueError('Source increment count mismatch')
        rows.extend(added)
    if len({r['id'] for r in rows})!=len(rows):
        raise ValueError('Duplicate source IDs across frozen batches')
    return rows


def local_hold(root, rows):
    path=root/'cleanup/local-unpublished.json'
    local=json.loads(path.read_text()).get('items',[]) if path.exists() else []
    by_id={r['id']:r for r in rows}
    unresolved=0
    for item in local:
        disposition=item.get('disposition')
        if disposition=='admit-source':
            target=by_id.get(item.get('source_id'),{})
            resolved=target.get('sha256')==item.get('sha256') and target.get('path')==item.get('admitted_path')
        elif disposition=='exclude-prefix-copy':
            comparisons=item.get('byte_comparison',[])
            resolved=bool(comparisons) and all(c.get('exact_prefix') is True and
                by_id.get(c.get('canonical_id'),{}).get('sha256')==c.get('canonical_sha256') for c in comparisons)
        else:
            resolved=disposition in {'exclude-nonmathematical','absorbed-defect-note'}
        # A judgment needs an explanation and a concrete published review record.
        if not resolved or not item.get('review_note') or not item.get('review_commit'):
            unresolved+=1
    return unresolved


def progress(root, sid):
    p=root/'cleanup/progress'/f'{sid}.json'
    return json.loads(p.read_text()) if p.exists() else {}


def source_list(root, prefix='', limit=30, owner=None, state=None, available=False, full=False):
    if owner=='self':
        owner=board.git(root,'config','--local','--get','wcg.actor').stdout.decode().strip()
    result=[]
    for row in inventory(root):
        if not row['path'].startswith(prefix):continue
        record=progress(root,row['id']);disposition=record.get('disposition','unread')
        if owner is not None and record.get('owner')!=owner:continue
        if state and not (disposition in COMPLETE if state=='completed' else disposition==state):continue
        if available and (record.get('owner') is not None or disposition in COMPLETE):continue
        result.append(dict(row,progress=record) if full else
                      {'id':row['id'],'path':row['path'],'state':disposition,'owner':record.get('owner')})
        if limit and len(result)>=limit:break
    return result


def refresh_snapshot(client):
    """Reuse fetched objects across transactions; never share a writable checkout."""
    key=hashlib.sha256((client.remote+'\0'+client.branch).encode()).hexdigest()[:16]
    cache=client.cache/('cleanup-snapshot-'+key+'.git')
    with (client.cache/('cleanup-snapshot-'+key+'.lock')).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if not cache.exists():
            board.git(client.repo,'init','--quiet','--bare',str(cache))
            board.git(cache,'remote','add','origin',client.remote)
        if board.git(cache,'remote','get-url','origin').stdout.decode().strip()!=client.remote:
            raise ValueError('Cleanup snapshot remote mismatch')
        board.git(cache,'fetch','--quiet','--no-tags','--depth=1','origin',
                  '+refs/heads/'+client.branch+':refs/heads/snapshot')
        tip=board.git(cache,'rev-parse','refs/heads/snapshot').stdout.decode().strip()
        shallow=(cache/'shallow').read_bytes() if (cache/'shallow').exists() else None
    return cache,tip,shallow


def checkout_snapshot(client, directory):
    cache,tip,shallow=refresh_snapshot(client)
    client.setup(directory)
    objects=Path(directory)/'.git/objects/info';objects.mkdir(exist_ok=True)
    (objects/'alternates').write_text(str(cache/'objects')+'\n')
    if shallow is not None:(Path(directory)/'.git/shallow').write_bytes(shallow)
    board.git(directory,'checkout','--quiet','--detach',tip)


def stats(root):
    rows=inventory(root);states=[progress(root,r['id']) for r in rows]
    return {'source_versions':len(rows),'distinct_paths':len({r['path'] for r in rows}),
            'completed':sum(s.get('disposition') in COMPLETE for s in states),
            'claimed':sum(s.get('owner') is not None and s.get('disposition') not in COMPLETE for s in states),
            'unresolved':sum(s.get('disposition')=='needs-decision' for s in states),
            'local_source_hold':local_hold(root,rows)}


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
           '原始分母与每批增量分别冻结于 sources.json；进度来源为 progress/ 下逐文件记录。来源补录不等于语义清洗完成。机器生成本页和分册。','']
    lines += [f'- [第{i+1}册](checklists/{p})' for i,p in enumerate(pages)]
    (root/'cleanup/CHECKLIST.md').write_text('\n'.join(lines)+'\n')
    return s


def resolve(rows, text):
    found=[r for r in rows if r['id']==text or r['path']==text or r['id'].startswith(text)]
    if len(found)!=1:
        raise ValueError('Source ID/path must identify exactly one version: '+text)
    return found[0]


def ensure_source(root,commit):
    if board.git(root,'cat-file','-e',commit,check=False).returncode:
        # Git lazily obtains requested blobs from the ordinary authenticated
        # origin. Servers without filtering fall back to a complete snapshot.
        board.git(root,'config','remote.origin.promisor','true')
        board.git(root,'config','remote.origin.partialclonefilter','blob:none')
        board.git(root,'fetch','--quiet','--no-tags','--depth=1','--filter=blob:none','origin',commit)


def prefetch_text(root,commit,rows):
    # Avoid one network round trip for every promised text blob during grep.
    listing=board.git(root,'rev-list','--objects','--missing=print','--no-object-names',commit).stdout
    missing={line[1:].decode() for line in listing.splitlines() if line.startswith(b'?')}
    wanted=sorted(missing.intersection(row['blob'] for row in rows))
    if wanted:
        board.git(root,'fetch','--quiet','--no-tags','--no-write-fetch-head',
                  '--filter=blob:none','--stdin','origin',input_data=('\n'.join(wanted)+'\n').encode())


def show(root,sid,output=None):
    row=resolve(inventory(root),sid);source=row['sources'][0];commit=source['commit']
    ensure_source(root,commit)
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
    searched_blobs=set()
    for snapshot in snapshots:
        commit=snapshot['commit']
        eligible=[row for row in rows if row['blob'] not in searched_blobs
                  and fnmatch.fnmatchcase(row['path'],pattern)
                  and any(s['commit']==commit for s in row['sources'])]
        if not eligible:continue
        ensure_source(root,commit);prefetch_text(root,commit,eligible)
        # Search only registered versions, including small increment snapshots;
        # their inherited old tree is not a fresh set of research sources.
        paths=[':(literal)'+row['path'] for row in eligible]
        r=board.git(root,'-c','core.quotePath=false','grep','-n','-I','-F','-e',query,commit,'--',*paths,check=False)
        if r.returncode not in (0,1):
            raise ValueError('Could not search frozen source')
        searched_blobs.update(row['blob'] for row in eligible)
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
            directory=Path(name);checkout_snapshot(client,directory)
            rows=inventory(directory);by_id={r['id']:r for r in rows}
            chosen=[]
            if operation=='claim' and prefix is not None:
                chosen=[r for r in rows if r['path'].startswith(prefix)
                        and progress(directory,r['id']).get('disposition') not in COMPLETE
                        and progress(directory,r['id']).get('owner') is None]
                if limit:chosen=chosen[:limit]
            elif operation=='done':
                chosen=[resolve(rows,item['id']) for item in records]
            else:chosen=[resolve(rows,sid) for sid in ids]
            if not chosen:
                if operation=='claim' and prefix is not None:
                    return {'status':'empty','operation':operation,'ids':[],
                            'note':'No unclaimed sources in this prefix; use clean list --owner self to resume your current batch.'}
                raise ValueError('No eligible source files')
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
            _,remote,_=refresh_snapshot(client)
            confirmed=True
            for sid in updates:
                blob=board.git(directory,'show',remote+':cleanup/progress/'+sid+'.json',check=False)
                if blob.returncode or json.loads(blob.stdout).get('request_id')!=request_id:
                    confirmed=False;break
            if confirmed:return {'status':'pushed','operation':operation,'actor':actor,'ids':updates,'remote_tip':remote,'note':'Declared semantic work; field checks do not prove mathematical correctness. The root work.py refreshes the local checkout after this receipt.'}
        time.sleep(min(.4,.03*(attempt+1)))
    raise ValueError('Concurrent updates could not be confirmed; no completion reported')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('status');li=sub.add_parser('list');li.add_argument('--prefix',default='');li.add_argument('--limit',type=int,default=30)
    li.add_argument('--owner',help='Actor ID, or self for this clone')
    li.add_argument('--state',choices=('unread','in-progress','needs-decision','completed'))
    li.add_argument('--available',action='store_true',help='Only unclaimed, unfinished sources')
    li.add_argument('--full',action='store_true',help='Include full frozen-source metadata and receipt')
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
        result=source_list(root,a.prefix,a.limit,a.owner,a.state,a.available,a.full)
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
