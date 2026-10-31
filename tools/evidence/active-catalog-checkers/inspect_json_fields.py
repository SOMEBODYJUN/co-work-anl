#!/usr/bin/env python3
"""New complete JSON field census; preserves values by ordered scalar digest."""
from pathlib import Path
import json,hashlib,collections
E=Path(__file__).resolve().parent
S=E.parents[2]
out={}
for r in json.loads((E/'related-manifest.json').read_text())+json.loads((E/'source-manifest.json').read_text()):
 if not r['path'].endswith('.json'):continue
 p=S/r['saved_path'];v=json.loads(p.read_text());fields=collections.defaultdict(collections.Counter);leaf=[]
 def walk(v,q):
  fields[q][type(v).__name__]+=1
  if isinstance(v,dict):
   for k,w in v.items():walk(w,q+'.'+k)
  elif isinstance(v,list):
   for w in v:walk(w,q+'[]')
  else:leaf.append((q,v))
 walk(v,'$');out[r['id']]={'path':r['path'],'size':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fields':{k:dict(v) for k,v in fields.items()},'ordered_scalar_count':len(leaf),'ordered_scalar_digest':hashlib.sha256(json.dumps(leaf,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()}
(E/'json-field-census.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('actual JSON field census',len(out))
