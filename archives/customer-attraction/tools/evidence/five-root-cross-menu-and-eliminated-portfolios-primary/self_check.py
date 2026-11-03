"""Static preservation/view/receipt/link/event check; no mathematical replay."""
from pathlib import Path
import argparse,json,gzip,hashlib,re
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();stage=next((p for p in E.parents if p.name=='deliverables'),None) or repo
 def resolve(rel):
  p=stage/rel
  return p if p.exists() else repo/rel
 def raw(z):
  p=resolve(z['preserved_repo_path']);b=p.read_bytes()
  if z.get('compression')=='gzip-lossless':assert sha(b)==z['preserved_sha256'];b=gzip.decompress(b)
  assert len(b)==z['size'] and sha(b)==z['sha256'];return b
 M=read(E/'source-manifest.json');assert len(M)==19 and sum(z['size'] for z in M)==4565460
 data={z['id']:json.loads(raw(z)) if z['path'].endswith('.json') else raw(z).decode() for z in M}
 related=read(E/'related-manifest.json');assert len(related)==2
 related_data={z['id']:json.loads(raw(z)) if z['path'].endswith('.json') else raw(z).decode() for z in related}
 receipts=read(E/'receipts.json');assert {z['id'] for z in M}=={r['id'] for r in receipts}
 targets=set()
 for r in receipts:
  assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  for target in r['targets']:assert resolve(target).exists()
  targets.update(q for q in r['targets'] if '/state/' in q)
 assert len(targets)==5
 V=E/'review-view';di=read(V/'eliminated-dictionaries.json');keys=di['columns'];dic=di['dictionaries'];seed=read(V/'eliminated-47seed-times32maxbits.json')['seeds'];atoms=[]
 for index,*ids in seed:
  assert index*32==len(atoms)
  base={k:dic[k][i] for k,i in zip(keys[:-1],ids)}
  atoms.extend({**base,'max_bits':b} for b in dic['max_bits'])
 a=data['f6270d5fff574cfc19a4'];assert len(atoms)==1504 and atoms==a['atoms']
 weights=read(V/'eliminated-sparse-float-weights.json')
 for tag,key in [('primal','primal_float'),('dual','dual_lambda_float')]:
  z=weights[tag];vals=[0.]*z['length']
  for row in z['nonzero']:
   vals[row[0]]=row[-1]
   if tag=='dual':assert a['row_names'][row[0]]==row[1]
  assert vals==a[key]
 suffixes=read(V/'eliminated-row-names-suffix-dictionary.json');names=[]
 for line in (V/'eliminated-row-name-segments.jsonl').read_text().splitlines():
  start,prefix,sid=json.loads(line);assert start==len(names);names.extend(prefix+':'+s if prefix else s for s in suffixes[sid])
 assert names==a['row_names'] and len(names)==4008
 assert {**read(V/'eliminated-metadata.json'),'atoms':atoms,'row_names':names,'primal_float':a['primal_float'],'dual_lambda_float':a['dual_lambda_float']}==a
 cd=read(V/'cross-dictionaries.json');cols=cd['columns'];cd=cd['dictionaries'];cross=[]
 for path in sorted(V.glob('cross-atoms-*.jsonl')):
  for line in path.read_text().splitlines():
   i,*ids=json.loads(line);assert i==len(cross);cross.append({k:cd[k][j] for k,j in zip(cols,ids)})
 c=data['7f1799e3315b81486453'];assert len(cross)==2206 and cross==c['atoms'] and {**read(V/'cross-metadata.json'),'atoms':cross}==c
 vec=read(V/'root-envelope-unique-vectors.json');table={}
 for line in (V/'root-envelope-mapping.jsonl').read_text().splitlines():
  tau,bits,i=json.loads(line);table.setdefault(tau,{})[bits]=vec[i]
 assert table==data['12b09c19f01590fc211e']['coefficients'] and len(vec)==260 and sum(len(s)*6 for s in table.values())==3840
 rpoint=related_data['5db6a037342bdee0f107'];point=[]
 for line in (V/'related-exact61.jsonl').read_text().splitlines():
  i,*rest=json.loads(line);assert i==len(point);ids=rest[:-1];point.append({**{k:dic[k][j] for k,j in zip(keys,ids)},'exact_mass':rest[-1]})
 assert point==rpoint['atoms'] and len(point)==61
 for z in read(E/'comparison-manifest.json')['full_read_mature_pages']:assert sha((repo/z['repo_path']).read_bytes())==z['sha256']
 countlinks=0
 for rel in targets:
  q=resolve(rel);s=q.read_text();assert s.startswith('---\n')
  for z in M:
   if rel in next(r['targets'] for r in receipts if r['id']==z['id']):
    for src in z['sources']:assert 'source:'+src['commit']+':'+src['path'] in s
  for link in re.findall(r'\]\(([^)]+)\)',s):
   if '://' in link or link.startswith('#'):continue
   target=(q.parent/link.split('#')[0]).resolve()
   if not target.exists():assert (repo/target.relative_to(stage)).exists(),(rel,link)
   countlinks+=1
 event=read(E/'fixed-menu-binding/execution.json');process=read(E/'fixed-menu-binding/process-event.json');result=read(E/'fixed-menu-binding/result.json')
 assert event['exit_code']==process['exit_code']==0 and event['script_sha256']==sha((E/'audit_fixed_menu_binding.py').read_bytes())
 assert process['stderr_bytes']==0 and sha((E/'fixed-menu-binding/stdout.txt').read_bytes())==process['stdout_sha256'] and sha((E/'fixed-menu-binding/stderr.txt').read_bytes())==process['stderr_sha256']
 assert event['original_function_calls']==result['original_newrow_calls']==61 and event['independent_state_expansions']==result['independent_S_Z_V_state_expansions']==610
 assert len(read(E/'fixed-menu-binding/atom-values.json'))==61 and len(read(E/'fixed-menu-binding/all610-independent-states.json'))==610
 assert result['E_half_total']==data['5c203feeb991f0926efe']['row_sum']
 assert result['normalized_combination_total']==data['3852a437d1d287e73e2b']['results'][0]['exact_separator']['weighted_maximum']
 assert all(v==0 for v in result['zero_operations'].values())
 assert result['original_function_source_sha256']==sha((E/'fixed-menu-binding/original-newrow-source.txt').read_bytes()) and result['original_AST_sha256']==sha((E/'fixed-menu-binding/original-newrow-AST.txt').read_bytes())
 assert not list(E.rglob('__pycache__'))
 report={'status':'PASS','scope':'static original byte preservation/lossless view reconstruction/receipts/links/dependency fingerprints/execution binding; zero original mathematical module import or replay','primary_sources':19,'primary_bytes':4565460,'losslessly_compressed_primary_JSONs':2,'related_only_sources':2,'self_contained_pages':5,'receipts':19,'full_read_mature_pages':9,'eliminated_atoms_reconstructed':1504,'eliminated_row_names_reconstructed':4008,'eliminated_sparse_primal_nonzeros':len(weights['primal']['nonzero']),'eliminated_sparse_dual_nonzeros':len(weights['dual']['nonzero']),'cross_atoms_reconstructed':2206,'root_exact_coefficients_reconstructed':3840,'related_fixed_atoms_reconstructed':61,'local_links_checked':countlinks,'math_replays_in_this_check':0,'script_sha256':sha(Path(__file__).read_bytes())}
 (E/'self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
