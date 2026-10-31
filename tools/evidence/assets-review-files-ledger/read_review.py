"""Lossless review ledger reading view. Axes remain separate; exact strings referenced only after actual first read."""
from pathlib import Path
import json,sys
E=Path(__file__).resolve().parent;x=json.loads((E/'original/research/review_status.json').read_text());cat=json.loads((E/'related/catalog/original/research/catalog.json').read_text());pi={r['path']:'C'+str(i) for i,r in enumerate(cat['entries'])};p=json.loads((E/'reading-progress.json').read_text());start,end=int(sys.argv[1]),int(sys.argv[2]);cols=['source_proof','current_proof','internal_review','external_review','implementation','graph_status']
if len(sys.argv)>3:p['review_complete_indices']=sorted(set(p['review_complete_indices'])|set(range(int(sys.argv[3]))));(E/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
def strs(v):
 if isinstance(v,str):
  if v not in pi:yield v
 elif isinstance(v,list):
  for z in v:yield from strs(z)
 elif isinstance(v,dict):
  for k,z in v.items():
   if k!='id':yield from strs(z)
ss=list(dict.fromkeys(z for r in x['entries'] for z in strs(r)));sm={s:'R'+str(i) for i,s in enumerate(ss)};seen={s for i in p['review_complete_indices'] for s in strs(x['entries'][i])}
def ref(v):
 if isinstance(v,str):return pi.get(v,sm.get(v,v))
 if isinstance(v,list):return [ref(z) for z in v]
 if isinstance(v,dict):return {k:ref(z) for k,z in v.items()}
 return v
out=['REVIEW positions '+str(start)+'..'+str(end-1)+'; Cn=exact already-read catalog path; Rn=complete exact human string; all columns keep independent authorship status.','NEW STRINGS:']
for r in x['entries'][start:end]:
 for s in strs(r):
  if s not in seen:out.append(sm[s]+' '+s);seen.add(s)
out.append('COLUMNS index | complete id | '+ ' | '.join(cols)+' | all optional keys object')
for i,r in list(enumerate(x['entries']))[start:end]:out.append(' | '.join([str(i),r['id']]+[str(ref(r[k])) for k in cols]+[json.dumps({k:ref(v) for k,v in r.items() if k not in ['id']+cols},ensure_ascii=False,separators=(',',':'))]))
s='\n'.join(out)+'\n';d=E/'reading-views';d.mkdir(exist_ok=True);(d/('review-'+str(start)+'-'+str(end-1)+'.txt')).write_text(s);print(s,end='')
