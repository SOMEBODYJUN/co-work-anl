import json
from pathlib import Path
p=Path('work/notes-fc2ba28a26cd495f/notes/RA07/project');v=p/'proposals/integration-v2';r=p/'reviews/visual-second'
# exact source status/geometry
su=v/'source-units.json'; sources=json.loads(su.read_text())
for x in sources:
 if x['id']=='RA07-P004-U006': x['bbox_px']=[610,1395,1725,1775]; x['evidence_ids']=[e for e in x['evidence_ids'] if e!='artifact:visual-second-p0004-bounded-note']
 if x['id']=='RA07-P006-U014': x['bbox_px']=[0,2410,120,2630]; x['evidence_ids']=['image:p0006','image:p0006-r3c1']
 if x['id'] in {'RA07-P001-U013','RA07-P003-U007','RA07-P003-U009','RA07-P005-U007','RA07-P006-U009','RA07-P010-U008','RA07-P011-U008','RA07-P011-U010','RA07-P006-U014'}: x['status']='unresolved'
su.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
# all target statuses inherit unresolved sources
m=v/'mapping.json';md=json.loads(m.read_text());st={x['id']:x['status'] for x in sources}
for t in md['targets']:
 if any(st.get(s)=='unresolved' for s in t.get('source_ids',[])):t['status']='unresolved'
m.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
# Add new source to both pass page/region inventories as a later geometry mapping, without claiming first visual read in notes.
for fn in ['observations-author.json']:
 f=v/fn;d=json.loads(f.read_text())
 for page in d['page_checks']:
  if page['page_id']=='p0006' and 'RA07-P006-U014' not in page['source_unit_ids']:
   page['source_unit_ids'].append('RA07-P006-U014'); page['observation']+=' Integration mapping later added the second-reader page-edge source; this is not a claim that the author first pass identified it.'
 for reg in d['region_checks']:
  if reg['region_id']=='p0006-r3c1' and 'RA07-P006-U014' not in reg['source_unit_ids']:
   reg['source_unit_ids'].append('RA07-P006-U014'); reg['observation']+=' Later mapping adds the page-edge source; no first-pass semantic claim.'
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# normalized pass2 source lists too
f=r/'observations-second.json';d=json.loads(f.read_text())
for page in d['page_checks']:
 if page['page_id']=='p0006' and 'RA07-P006-U014' not in page['source_unit_ids']:page['source_unit_ids'].append('RA07-P006-U014')
for reg in d['region_checks']:
 if reg['region_id']=='p0006-r3c1' and 'RA07-P006-U014' not in reg['source_unit_ids']:reg['source_unit_ids'].append('RA07-P006-U014')
(r/'observations-second.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(r/'observations-second-ledger.json').write_text(json.dumps({'page_checks':d['page_checks'],'region_checks':d['region_checks']},ensure_ascii=False,indent=2)+'\n')
# normalize recovery return-to-image associations from current source geometry; this adds only already-observed current regions.
rec=json.loads((r/'recovery-proposals.json').read_text())
source_index={x['id']:x for x in sources}
for x in rec['recoveries']:
 regs=set(); pages=set(); ev=set(x.get('evidence_ids',[]))
 for sid in x['source_ids']:
  src=source_index.get(sid)
  if not src:continue
  pages.add(src['page_id']);ev.update(src.get('evidence_ids',[]))
  # actual manifest region intersections from source unit's inherited evidence IDs
  regs.update(e[6:] for e in src.get('evidence_ids',[]) if e.startswith('image:p') and '-r' in e)
 ret=x.setdefault('return_to_image',{});ret['region_ids']=sorted(set(ret.get('region_ids',[]))|regs);ret['page_ids']=sorted(set(ret.get('page_ids',[]))|pages);ret['evidence_ids']=sorted(set(ret.get('evidence_ids',[]))|ev)
(r/'recovery-proposals.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
(r/'recovery-proposals-ledger.json').write_text(json.dumps(rec['recoveries'],ensure_ascii=False,indent=2)+'\n')
print('fixed source geometry/status, pass inventories, and recovery return regions')
