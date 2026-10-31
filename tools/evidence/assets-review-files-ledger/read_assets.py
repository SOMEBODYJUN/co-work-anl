"""Lossless reading view: exact repeated human strings and already-read catalog paths get references.
Views do not acknowledge their own reading. Ack confirms only the preceding actual output.
"""
from pathlib import Path
import json,sys
E=Path(__file__).resolve().parent;x=json.loads((E/'original/research/assets.json').read_text());catalog=json.loads((E/'related/catalog/original/research/catalog.json').read_text());pi={r['path']:'C'+str(i) for i,r in enumerate(catalog['entries'])};p=json.loads((E/'reading-progress.json').read_text());start,end=int(sys.argv[1]),int(sys.argv[2]);
if len(sys.argv)>3:p['assets_complete_indices']=list(range(int(sys.argv[3])));(E/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
fields={'status','applies_when','produces','limit','source_role','source_scope','implementation_detail','scope_model','source_interpretation'};pathfields={'proof','tests','records','examples','implementation','reviews','candidates','sources'}
def strings(r):
 for k,v in r.items():
  if k in fields:
   if isinstance(v,str):yield v
   elif isinstance(v,list):
    for s in v:
     if isinstance(s,str):yield s
allstrings=list(dict.fromkeys(s for r in x['entries'] for s in strings(r)));sm={s:'S'+str(i) for i,s in enumerate(allstrings)};seen={s for i in p['assets_complete_indices'] for s in strings(x['entries'][i])};out=['ASSETS positions '+str(start)+'..'+str(end-1)+'; Cn=exact path of already fully read catalog.entries[n]. S identifiers=exact human strings, printed once after full first reading.','NEW HUMAN STRINGS:']
for r in x['entries'][start:end]:
 for s in strings(r):
  if s not in seen:out.append(sm[s]+' '+s);seen.add(s)
out.append('FULL FIELD ASSIGNMENTS (all present keys; absent fields remain absent):')
for i,r in list(enumerate(x['entries']))[start:end]:
 z={}
 for k,v in r.items():
  if k in fields:
   z[k]=sm[v] if isinstance(v,str) else [sm[s] if isinstance(s,str) else s for s in v]
  elif k in pathfields:z[k]=[pi.get(q,q) for q in v]
  else:z[k]=v
 out.append(str(i)+' '+json.dumps(z,ensure_ascii=False,separators=(',',':')))
s='\n'.join(out)+'\n';d=E/'reading-views';d.mkdir(exist_ok=True);(d/('assets-'+str(start)+'-'+str(end-1)+'.txt')).write_text(s);print(s,end='')
