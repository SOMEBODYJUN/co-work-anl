import json,hashlib,gzip,ast,csv,collections,os,re,zipfile,math,argparse
from pathlib import Path
ap=argparse.ArgumentParser(description='SHA and complete machine-structure audit; no solver or source execution')
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--output-dir',type=Path,required=True)
args=ap.parse_args();root=args.repo.resolve();out=args.output_dir.resolve()
reg=json.loads((root/'research/registry.json').read_text())
o=next(x for x in reg['objects'] if x['object_id']=='customer-attraction/six-providers/cross-branch-necessary-system-20261111')
refs=[o['body']]+o['evidence'];results=[]
fracpat=re.compile(r'^-?[0-9]+/[0-9]+$')
def structure(x):
 c=collections.Counter();invalid=[];stack=[x]
 while stack:
  a=stack.pop();c[type(a).__name__]+=1
  if isinstance(a,dict):stack.extend(a.values());c['dict_entries']+=len(a)
  elif isinstance(a,list):stack.extend(a);c['list_entries']+=len(a)
  elif isinstance(a,str) and fracpat.fullmatch(a):
   c['fraction_strings']+=1
   if int(a.split('/')[1])==0:invalid.append(a)
  elif isinstance(a,float) and not math.isfinite(a):invalid.append(str(a))
 summary={'top_type':type(x).__name__,'node_counts':dict(c),'invalid_numeric_literals':invalid[:8]}
 if isinstance(x,dict):
  summary['top_keys']=list(x)
  summary['top_array_lengths']={k:len(v) for k,v in x.items() if isinstance(v,(list,dict))}
 elif isinstance(x,list):summary['length']=len(x)
 return summary
for idx,ref in enumerate(refs):
 p=root/ref['path']; b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();r={'path':ref['path'],'expected_sha256':ref['sha256'],'actual_sha256':sha,'bytes':len(b),'sha256_matches':sha==ref['sha256']}
 try:
  raw=gzip.decompress(b) if p.suffix=='.gz' else b
  if p.name.endswith('.json.gz') or p.suffix=='.json':
   r['parse_mode']='complete_json_parse_and_full_recursive_structure';r['structure']=structure(json.loads(raw))
  elif p.name.endswith('.jsonl.gz'):
   vals=[json.loads(line) for line in raw.decode().splitlines() if line.strip()];r['parse_mode']='complete_jsonl_parse_and_full_recursive_structure';r['structure']=structure(vals)
  elif p.suffix=='.py':
   s=b.decode();tree=ast.parse(s);r['parse_mode']='full_UTF8_decode_and_AST_parse_without_execution';r['lines']=len(s.splitlines());r['ast_nodes']=sum(1 for _ in ast.walk(tree))
  elif p.suffix=='.npz':
   import numpy as np
   with np.load(p,allow_pickle=False) as z:
    r['parse_mode']='full_NPZ_materialization_no_pickle';r['arrays']={}
    for k in z.files:
     a=z[k];r['arrays'][k]={'shape':list(a.shape),'dtype':str(a.dtype),'size':int(a.size),'all_finite':bool(np.isfinite(a).all()) if a.dtype.kind in 'fci' else None}
  elif p.suffix=='.tsv':
   rows=list(csv.reader(b.decode().splitlines(),delimiter='\t'));r['parse_mode']='complete_TSV_parse';r['rows']=len(rows);r['row_lengths']=dict(collections.Counter(len(v) for v in rows))
  else:
   s=b.decode();r['parse_mode']='full_UTF8_decode_and_header_inventory_only_not_semantic_read';r['chars']=len(s);r['lines']=len(s.splitlines());r['headers']=[line for line in s.splitlines() if line.startswith('#')]
  if p.suffix=='.gz':r['expanded_bytes']=len(raw)
  r['parse_ok']=True
 except Exception as e:r['parse_ok']=False;r['error']=type(e).__name__+': '+str(e)
 results.append(r)
summary={'object_id':o['object_id'],'object_version':o['version'],'scope':'All 531 core registered refs; SHA verification and complete machine-format parse; markdown header inventory does not claim semantic read','ref_count':len(results),'total_bytes':sum(a['bytes'] for a in results),'sha256_mismatch_paths':[a['path'] for a in results if not a['sha256_matches']],'parse_error_paths':[a['path'] for a in results if not a['parse_ok']],'parse_modes':dict(collections.Counter(a.get('parse_mode') for a in results)),'refs':results}
path=out/'core-ref-structure-audit.json';path.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='refs'},ensure_ascii=False,indent=2))
print('report_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
