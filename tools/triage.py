"""Material-level phase 2.5.1 inventory. No truth review or graph admission."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import curation

CATEGORIES = {'math-exposition','numeric-witness','math-fragment','algorithm-result',
              'evidence-only','non-math','mixed/needs-context'}
ROUTES = {'retain','distill','restore','extract','attach','delete','clarify'}
FIELDS = {'path','sha256','category','math_subject_or_nonmath_reason','locator','route'}
OPTIONAL = {'tags','related_paths'}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    temp.replace(path)

def run_path(root, run):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,100}',run):
        raise ValueError('unsafe run ID')
    return curation._safe_path(root,'curation/runs/'+run)

def load(root, run):
    home=run_path(root,run)
    return home,json.loads((home/'snapshot.json').read_text())

def init(root, run, lanes=6, actor=None):
    if not isinstance(actor,str) or not re.fullmatch(r'Boss[1-9][0-9]*',actor):
        raise ValueError('explicit Boss actor required')
    if not 1 <= lanes <= 64:raise ValueError('lanes must be between 1 and 64')
    home=run_path(root,run)
    if home.exists():raise ValueError('run already exists; resume it')
    snap=curation.scan(root)
    snap.pop('status')
    snap['commit']=curation._git(root,'rev-parse','HEAD').decode().strip()
    curation._check_snapshot(root,snap)
    for row in snap['files']:
        row['material_id']=hashlib.sha256(row['path'].encode()).hexdigest()[:20]
        row['bytes']=(root/row['path']).stat().st_size
    groups=[[] for _ in range(lanes)];sizes=[0]*lanes
    # Similar paths stay adjacent in each lane; large wrappers are distributed.
    for row in sorted(snap['files'],key=lambda x:-x['bytes']):
        lane=min(range(lanes),key=lambda i:sizes[i])
        groups[lane].append(row['material_id']);sizes[lane]+=row['bytes']
    write(home/'snapshot.json',snap)
    write(home/'run.json',{'version':1,'run_id':run,'actor':actor,
          'step':'2.5.1','snapshot_commit':snap['commit'],'lanes':lanes,
          'status':'classifying','board':'not-created-single-Boss-internal-batches',
          'scope':'current canonical formal Markdown; evidence originals excluded'})
    for i,ids in enumerate(groups,1):write(home/'lanes'/f'{i}.json',ids)
    return {'run':run,'commit':snap['commit'],'materials':len(snap['files']),
            'bytes':sum(sizes),'lane_bytes':sizes}

def next_batch(root, run, lane, limit=15, byte_limit=70000):
    home,snap=load(root,run)
    config=json.loads((home/'run.json').read_text())
    if limit<1 or byte_limit<1:raise ValueError('positive batch limits required')
    if lane<1 or lane>config['lanes']:
        raise ValueError('unknown lane')
    for p in sorted((home/'batches').glob(f'lane{lane}-*.json')) if (home/'batches').exists() else []:
        old=json.loads(p.read_text())
        if old['state']=='assigned':return old
    rows={r['material_id']:r for r in snap['files']}
    ids=json.loads((home/'lanes'/f'{lane}.json').read_text())
    chosen=[];size=0
    for sid in sorted(ids,key=lambda k:rows[k]['path']):
        if (home/'records'/f'{sid}.json').exists():continue
        row=rows[sid]
        if chosen and (len(chosen)>=limit or size+row['bytes']>byte_limit):break
        chosen.append(row);size+=row['bytes']
    if not chosen:return {'state':'lane-complete','lane':lane}
    batch_id=f'lane{lane}-'+chosen[0]['material_id']
    out={'batch_id':batch_id,'lane':lane,'state':'assigned','files':chosen,
         'record_file':f'curation/workspaces/{run}/{config["actor"]}/{batch_id}.json'}
    write(home/'batches'/f'{batch_id}.json',out)
    return out

def validate_record(record):
    if not isinstance(record,dict) or not FIELDS<=record.keys() or record.keys()-FIELDS-OPTIONAL:
        raise ValueError('classification needs exactly six required fields and optional tags/related_paths')
    if any(not isinstance(record[k],str) or not record[k].strip() for k in FIELDS):
        raise ValueError('nonempty classification fields required')
    c=record['category'];route=record['route']
    if c not in CATEGORIES or route not in ROUTES:raise ValueError('unknown content category or route')
    if not re.fullmatch(r'[0-9a-f]{64}',record['sha256']):raise ValueError('invalid SHA')
    allowed=({'delete','clarify'} if c=='non-math' else
             {'attach','delete','clarify'} if c=='evidence-only' else
             {'extract','clarify'} if c=='mixed/needs-context' else
             {'retain','distill','restore','extract','clarify'})
    if route not in allowed:raise ValueError('classification cannot directly discard mathematics')
    for key in OPTIONAL:
        if key in record and (not isinstance(record[key],list) or
            any(not isinstance(x,str) or not x.strip() for x in record[key]) or
            len(record[key])!=len(set(record[key]))):raise ValueError('invalid optional list')

def ingest(root,run,batch_id,record_file):
    home,snap=load(root,run)
    if not re.fullmatch(r'lane[1-9][0-9]*-[0-9a-f]{20}',batch_id):raise ValueError('invalid batch ID')
    batch_path=home/'batches'/f'{batch_id}.json'
    batch=json.loads(batch_path.read_text())
    records=json.loads(curation._safe_path(root,record_file).read_text())
    if not isinstance(records,list):raise ValueError('batch records must be a list')
    expected={r['path']:r for r in batch['files']}
    if len(records)!=len(expected) or {r.get('path') for r in records if isinstance(r,dict)}!=set(expected):
        raise ValueError('batch contains missing or duplicate material records')
    writes=[]
    for record in records:
        validate_record(record);row=expected[record['path']]
        p=curation._safe_path(root,row['path'])
        if record['sha256']!=row['sha256'] or not p.is_file() or curation.digest(p.read_bytes())!=row['sha256']:
            raise ValueError('source changed; classify the changed version: '+row['path'])
        dest=home/'records'/f"{row['material_id']}.json"
        if dest.exists() and json.loads(dest.read_text())!=record:raise ValueError('conflicting existing classification')
        writes.append((dest,record))
    for dest,record in writes:write(dest,record)
    batch['state']='classified-local';write(batch_path,batch)
    return {'state':'classified-local-not-yet-pushed','batch_id':batch_id,'records':len(writes)}

def status(root,run):
    home,snap=load(root,run);counts=collections.Counter();routes=collections.Counter();records={}
    for p in (home/'records').glob('*.json') if (home/'records').exists() else []:
        r=json.loads(p.read_text());validate_record(r);counts[r['category']]+=1;routes[r['route']]+=1
        records[r['path']]=r
    original={r['path']:r for r in snap['files']}
    if records.keys()-original.keys():raise ValueError('classification outside snapshot')
    stale=[p for p,r in records.items() if r['sha256']!=original[p]['sha256']]
    return {'run':run,'snapshot_commit':snap['commit'],'materials':len(original),
            'classified':len(records),'remaining':len(original)-len(records),
            'categories':dict(counts),'routes':dict(routes),'stale_record_bindings':stale}

def export(root,run):
    home,snap=load(root,run);report=status(root,run);rows=[]
    for original in snap['files']:
        p=home/'records'/f"{original['material_id']}.json"
        if p.exists():rows.append(json.loads(p.read_text()))
    write(home/'summary.json',report)
    write(home/'materials.json',rows)
    for category in sorted(CATEGORIES):
        write(home/'catalog'/f"{category.replace('/','-')}.json",[r for r in rows if r['category']==category])
    write(home/'stage2-candidates.json',[r for r in rows if r['route'] in {'distill','restore','extract','clarify'}])
    with (home/'materials.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=sorted(FIELDS));writer.writeheader()
        writer.writerows({k:r[k] for k in sorted(FIELDS)} for r in rows)
    lines=['# 2.5.1 材料定性目录','',f"固定快照 `{report['snapshot_commit']}`；已定性 {report['classified']}/{report['materials']}。分类不是数学真值审查或超边准入。",'',
           '| 材料类别 | 数量 |','| --- | ---: |']
    lines.extend(f'| {c} | {report["categories"].get(c,0)} |' for c in sorted(CATEGORIES))
    lines+=['','完整六字段清单见 [materials.csv](materials.csv) 和 [materials.json](materials.json)，按类别见 catalog/；第二步候选见 [stage2-candidates.json](stage2-candidates.json)。',
            '','分类与清理落实分开；删除和附件去向另见 actions/。本目录是后台材料清单，不是数学正文。']
    (home/'INDEX.md').write_text('\n'.join(lines)+'\n')
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='command',required=True)
    for name in ['init','next','ingest','status','export']:
        q=sub.add_parser(name);q.add_argument('--run',required=True)
        if name=='init':
            q.add_argument('--lanes',type=int,default=6);q.add_argument('--actor',required=True)
        if name=='next':
            q.add_argument('--lane',type=int,required=True);q.add_argument('--limit',type=int,default=15);q.add_argument('--byte-limit',type=int,default=70000)
        if name=='ingest':q.add_argument('--batch',required=True);q.add_argument('--records',required=True)
    a=p.parse_args();root=a.repo.resolve()
    try:
        if a.command=='init':result=init(root,a.run,a.lanes,a.actor)
        elif a.command=='next':result=next_batch(root,a.run,a.lane,a.limit,a.byte_limit)
        elif a.command=='ingest':result=ingest(root,a.run,a.batch,a.records)
        elif a.command=='status':result=status(root,a.run)
        else:result=export(root,a.run)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:raise SystemExit(str(e))

if __name__=='__main__':main()
