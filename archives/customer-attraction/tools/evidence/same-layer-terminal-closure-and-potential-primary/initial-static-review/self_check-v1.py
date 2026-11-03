"""Static packaging check only. Never imports frozen mathematical modules."""
from pathlib import Path
import argparse,json,hashlib,re,sys
E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();stage=next((q for q in E.parents if q.name=='deliverables'),None) or repo
 def resolve(rel):
  q=stage/rel
  return q if q.exists() else repo/rel
 manifest=read(E/'source-manifest.json');assert len(manifest)==29 and sum(z['size'] for z in manifest)==1265536
 data={}
 for z in manifest:
  q=resolve(z['preserved_repo_path']);assert q.stat().st_size==z['size'] and sha(q)==z['sha256']
  data[Path(z['path']).name]=read(q) if q.suffix=='.json' else q.read_text()
 receipts=read(E/'receipts.json');assert {r['id'] for r in receipts}=={z['id'] for z in manifest}
 for r in receipts:
  assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and r['disposition']=='integrated'
  for target in r['targets']:assert resolve(target).exists(),target
 deps=read(E/'runtime-dependencies.json')['prior_25_file_closure'];assert len(deps)==25
 for z in deps:assert sha(repo/z['repo_path'])==z['sha256']
 compare=read(E/'comparison-and-reuse.json')
 for z in compare['full_read_mature_pages']+compare['reused_large_primary_and_projection']:assert sha(repo/z['repo_path'])==z['sha256']
 d=read(E/'review-view/point-dictionaries.json');weights=d['weights'];groups=d['groups'];assert len(weights)==95 and len(groups)==44
 def decode(row):
  i,kind,*v=row
  if kind=='K':z={'kind':'K','weight':weights[v[0]]}
  elif kind=='H':z={'kind':'hist','actual_bits':v[0],'d':v[1],'hist':list(map(int,v[2])),'weight':weights[v[3]]}
  elif kind=='R':z={'kind':'new-reply','hist_column':v[0],'group':groups[v[1]],'weight':weights[v[2]]}
  elif kind=='J':z={'kind':'joint-reply','hist_column_old':v[0],'group':groups[v[1]],'state':list(map(int,v[2])),'weight':weights[v[3]]}
  elif kind=='O':z={'kind':'overlap','hist_column':v[0],'groups':[groups[v[1]],groups[v[2]]],'weight':weights[v[3]]}
  else:raise AssertionError(kind)
  return i,z
 reconstructed={}
 for name,size in [('full_new_reply_closure_exact',211),('actual_fifth_nested_exact',599),('attractive_nested_exact',1905)]:
  cols={}
  for q in sorted((E/'review-view').glob(name+'-*.jsonl')):
   for line in q.read_text().splitlines():
    i,z=decode(json.loads(line));assert i not in cols;cols[i]=z
  assert sorted(cols)==list(range(size))
  reconstructed[name]=[cols[i] for i in range(size)]
  assert {**d['meta'][name],'columns':reconstructed[name]}==data[name+'.json']
 delta=read(E/'review-view/attractive-first599-delta.json');base=reconstructed['actual_fifth_nested_exact'];att=reconstructed['attractive_nested_exact'][:599]
 actualchanges=[]
 for i,(x,y) in enumerate(zip(base,att)):
  assert {k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'}
  if x['weight']!=y['weight']:actualchanges.append([i,weights.index(x['weight']),weights.index(y['weight'])])
 assert actualchanges==delta['changes'] and len(actualchanges)==78
 raw=data['copy_tax_all_spe_probe.json'];records=raw['trials'];compact=[json.loads(line) for line in (E/'review-view/copy-tax-all-SPE-300-records.jsonl').read_text().splitlines()]
 keys=['trial','unit_customers','root_SPE_terminal_counts','largest_auxiliary_gap_scaled60','prefix_count_states']
 assert compact==[[z[k] for k in keys] for z in records] and len(records)==300
 ownpages={target for r in receipts for target in r['targets'] if '/state/' in target};assert len(ownpages)==7
 links=0
 for rel in ownpages:
  q=resolve(rel);s=q.read_text();assert s.startswith('---\n')
  for z in manifest:
   if z['id'] in {r['id'] for r in receipts if rel in r['targets']}:
    for src in z['sources']:assert 'source:'+src['commit']+':'+src['path'] in s
  for target in re.findall(r'\]\(([^)]+)\)',s):
   if '://' in target or target.startswith('#'):continue
   dest=(q.parent/target.split('#')[0]).resolve()
   if not dest.exists():
    relative=dest.relative_to(stage);assert (repo/relative).exists(),(rel,target)
   links+=1
 run=read(E/'replay/execution.json');proc=read(E/'replay/process-event.json');projection=read(E/'later-projection/execution.json')
 assert run['exit_code']==proc['exit_code']==projection['exit_code']==0
 assert run['script_sha256']==sha(E/'audit_original_layers.py') and projection['script_sha256']==sha(E/'apply_later_projection.py')
 assert run['primary_manifest_sha256']==sha(E/'source-manifest.json') and run['dependency_manifest_sha256']==sha(E/'runtime-dependencies.json')
 assert len(run['frozen_file_hashes_before'])==50 and run['frozen_file_hashes_before']==run['frozen_file_hashes_after']
 assert sha(E/'replay/run.stdout.txt')==proc['stdout_sha256'] and sha(E/'replay/run.stderr.txt')==proc['stderr_sha256'] and proc['stderr_bytes']==0
 fixed=read(E/'replay/fixed-layers-and-parent-points.json')
 for name,count in [('closure1033',1033),('nested1097',1097),('attractive3889',3889),('parent704',704)]:assert len(read(E/'replay'/(name+'-all-row-slacks.json')))==count
 for event in fixed['original_finite_auditor_events']:
  tag=event['function'].split('.')[0];assert sha(E/'replay'/(tag+'.stdout.txt'))==event['stdout_sha256'] and sha(E/'replay'/(tag+'.generated.json'))==event['generated_sha256']
 assert all(v==0 for v in fixed['zero_new_operations'].values())
 assert fixed['original_function_calls']['attractive_nested.build']==fixed['original_function_calls']['actual_fifth_nested.build']==fixed['original_function_calls']['full_new_reply_closure.build']==1
 assert fixed['original_function_calls']['mixed_pair.cut']==2
 assert read(E/'later-projection/thirteen-term-result.json')['common_16_hist_identical_across_211_599_1905'] is True
 assert not list(E.rglob('__pycache__'))
 out={'status':'PASS','scope':'static source bytes, lossless views, links, declared dependencies and recorded event consistency; zero mathematical module import/replay','primary_files':29,'primary_bytes':1265536,'primary_new_copies':27,'primary_same_SHA_reused':2,'receipts':29,'self_contained_pages':7,'full_read_mature_pages':14,'prior_declared_closure_files':25,'runtime_unique_frozen_files_recorded':50,'large_JSON_columns_losslessly_reconstructed':2715,'shared_weight_strings':95,'shared_group_descriptors':44,'attractive_prefix_weight_differences':78,'finite_all_SPE_records_losslessly_reconstructed':300,'local_markdown_links_checked':links,'mathematical_runs_in_this_script':0,'math_module_imports':0,'script_sha256':sha(Path(__file__))}
 (E/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
