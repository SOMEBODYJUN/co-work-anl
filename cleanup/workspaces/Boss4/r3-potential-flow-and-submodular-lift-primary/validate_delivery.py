"""Read-only source/receipt/link checks; no mathematical experiment."""
from pathlib import Path
import hashlib,json,re
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research';W=Path(__file__).resolve().parent
E=S/'archives/customer-attraction/tools/evidence/potential-flow-and-submodular-lift-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];links=[];js_count=py_count=0
for p in S.rglob('*'):
 if not p.is_file() or p==S/'copy-files.json':continue
 if '__pycache__' in p.parts:errors.append('unexpected bytecode '+str(p))
 if p.suffix=='.json':json.loads(p.read_text());js_count+=1
 if p.suffix=='.py':compile(p.read_text(),str(p),'exec');py_count+=1
 if p.suffix=='.md':
  for raw in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   link=raw.split('#',1)[0]
   if not link or '://' in link:continue
   target=(p.parent/link).resolve()
   try:rel=target.relative_to(S)
   except ValueError:errors.append('outside stage '+str(p)+' '+link);continue
   resolved=target if target.is_file() else R/rel;ok=resolved.is_file()
   links.append({'from':str(p.relative_to(S)),'link':link,'resolved':str(resolved),'exists':ok})
   if not ok:errors.append('missing link '+str(p)+' '+link)
pm=json.loads((E/'primary-manifest.json').read_text());ids={x['id'] for x in pm['sources']}
assert len(ids)==5 and sum(x['size'] for x in pm['sources'])==pm['primary_bytes']==20183
for r in pm['sources']:
 p=S/r['saved_path'];b=p.read_bytes();assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 assert b==Path(r['local_path']).read_bytes()
cap=json.loads((W/'claim-receipt.json').read_text());ob=json.loads((W/'claim-observation.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
assert len(cap['ids'])==5 and set(cap['ids'])==ids==set(ob['claimed_primary_ids'])
assert sha(W/'claim-receipt.json')==ob['capture_sha256'] and sha(W/'intake-local-export-manifest.json')==ob['intake_manifest_sha256']
assert all(r['record']['owner']=='Boss4' and r['record']['disposition']=='in-progress' for r in ob['local_working_tree_owners'])
rec=json.loads((W/'semantic-receipts.json').read_text());assert len(rec)==5 and {x['id'] for x in rec}==ids
for x in rec:
 assert x['disposition']=='integrated' and all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(x[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for path in x['targets']:assert (S/path).is_file()
dep=json.loads((E/'dependency-boundary.json').read_text());assert len(dep['provided_comparison_sources'])==1 and len(dep['confirmed_local_missing'])==4
for r in dep['provided_comparison_sources']:
 p=S/r['saved_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
assert {r['id'] for r in dep['confirmed_local_missing']}=={'8d054ff238057dfc954b','69ab469599fba5e67088','207e2c45326d742b7f5b','54e68ef59de51a7b5e1c'}
rt=json.loads((W/'runtime-summary.json').read_text());assert rt['original_program_runs']==rt['new_numerical_experiments']==rt['optimizer_calls']==0
formal=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(formal)==3
for p in formal:
 text=p.read_text();assert text.startswith('---\n')
 for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in text
 assert not any(x in text for x in ['TODO','TBD','346?'])
 # Ensure rendered static tables do not contain unescaped absolute-value pipes.
 block=[]
 for line in text.splitlines()+['']:
  if line.startswith('|') and line.endswith('|'):block.append(line)
  elif block:
   assert len({len(re.findall(r'(?<!\\)\|',row)) for row in block})==1,(p,block)
   block=[]
global_body=next(p for p in formal if '共同删除势' in p.name).read_text()
assert '同一个Φ' in global_body and 'BC' in global_body and 'L→∞' in global_body
assert '裸效率' in global_body
nexts=json.loads((W/'next-candidates.json').read_text());assert len(nexts['sources'])==5 and nexts['all5_local_bytes_verified']
out={'status':'pass' if not errors else 'fail','primary_count':5,'primary_bytes':20183,'semantic_receipts':5,
 'new_formal_pages':3,'comparison_raw_files':1,'confirmed_missing_dependency_files':4,
 'json_files_read':js_count,'python_sources_compiled_not_executed':py_count,
 'mathematical_experiments_or_optimizers_run_by_validation':0,'local_links':links,'errors':errors}
(W/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='local_links'},ensure_ascii=False))
if errors:raise SystemExit(1)
