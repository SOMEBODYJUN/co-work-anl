import json
from pathlib import Path
p=Path('work/notes-fc2ba28a26cd495f/notes/RA07/project'); v=p/'proposals/integration-v2'; r=p/'reviews/visual-second'
# source geometry/status/evidence
su=v/'source-units.json'; sources=json.loads(su.read_text())
for x in sources:
 if x['id']=='RA07-P004-U006': x['bbox_px']=[610,1395,1725,1775]
 if x['id'] in {'RA07-P003-U007','RA07-P001-U013','RA07-P010-U008','RA07-P011-U008'}: x['status']='unresolved'
 if x['id']=='RA07-P004-U006': x['evidence_ids']=sorted(set(x['evidence_ids']+['artifact:visual-second-p0004-bounded-note']))
su.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
# mapping statuses from source status; all targets linked to an unresolved source inherit unresolved
m=v/'mapping.json'; md=json.loads(m.read_text()); statuses={x['id']:x['status'] for x in sources}
for t in md['targets']:
 if any(statuses.get(s)=='unresolved' for s in t.get('source_ids',[])): t['status']='unresolved'
m.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
# normalized second observations/recoveries
obs=json.loads((r/'observations-second.json').read_text()); (r/'observations-second-ledger.json').write_text(json.dumps({'page_checks':obs['page_checks'],'region_checks':obs['region_checks']},ensure_ascii=False,indent=2)+'\n')
rec=json.loads((r/'recovery-proposals.json').read_text()); (r/'recovery-proposals-ledger.json').write_text(json.dumps(rec['recoveries'],ensure_ascii=False,indent=2)+'\n')
# artifacts/evidence in config
cfg=p/'ledger-config-integration-v2.json'; c=json.loads(cfg.read_text());c['observations']=['proposals/integration-v2/observations-author.json','reviews/visual-second/observations-second-ledger.json'];c['recoveries']='reviews/visual-second/recovery-proposals-ledger.json'
for ident,path in [('visual-second-observations','reviews/visual-second/observations-second.json'),('visual-second-recoveries','reviews/visual-second/recovery-proposals.json'),('visual-second-unit-crosswalk','reviews/visual-second/unit-crosswalk.json'),('visual-second-phase2-evidence','reviews/visual-second/phase2-evidence.json'),('visual-second-math-validation','reviews/visual-second/math-validation.txt')]:
 if not any(a.get('id')==ident for a in c['artifacts']): c['artifacts'].append({'id':ident,'path':path,'kind':'evidence','format':'text'})
for crop in json.loads((r/'phase2-crops.json').read_text())['crops']:
 if not any(a.get('id')==crop['id'] for a in c['artifacts']): c['artifacts'].append({'id':crop['id'],'path':crop['path'],'kind':'evidence','format':'image','source_crop':{'page_id':crop['page_id'],'bbox_px':crop['bbox_px']}})
# root actual revisit evidence
if not any(a.get('id')=='root-extra-crop-revisit' for a in c['artifacts']): c['artifacts'].append({'id':'root-extra-crop-revisit','path':'evidence/root-extra-crop-revisit.json','kind':'evidence','format':'text'})
cfg.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('sources',len(sources),'targets',len(md['targets']),'artifacts',len(c['artifacts']),'recoveries',len(rec['recoveries']))
