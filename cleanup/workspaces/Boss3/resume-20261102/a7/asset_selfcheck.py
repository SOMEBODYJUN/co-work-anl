from pathlib import Path
import json,hashlib,ast,re,yaml
R=Path.cwd();W=R/'cleanup/workspaces/Boss3/resume-20261102/a7';E=R/'archives/customer-attraction/tools/evidence/trueH-fixed-and-bidirectional-resumed-boss3'
M=json.loads((E/'source-manifest.json').read_text());D=json.loads((W/'delivery.json').read_text());C=json.loads((W/'semantic-receipts.json').read_text());view=json.loads((E/'complete-data-reading-view.json').read_text())
assert len(M)==len(C)==8 and sum(x['size'] for x in M)==1879792
assert {x['id'] for x in M}=={x['id'] for x in C}
raw={};py=js=0
for m in M:
 p=E/'source-root'/m['path'];b=p.read_bytes();assert len(b)==m['size'] and hashlib.sha256(b).hexdigest()==m['sha256']
 if p.suffix=='.py':ast.parse(b);py+=1
 else:raw[p.name]=json.loads(b);js+=1
assert py==js==4
for m in json.loads((E/'comparison-source-manifest.json').read_text()):
 b=(R/m['evidence_path']).read_bytes();assert len(b)==m['size'] and hashlib.sha256(b).hexdigest()==m['sha256']
atoms=[]
for t in view['atoms_as_pool_indices']:
 atoms.append({f:view['pools'][f][i] for f,i in zip(view['fields'],t) if i!=-1})
assert len(atoms)==849
for name,indices in view['original_record_maps'].items():
 other=view['report_other_fields'][name];d={k:v for k,v in other.items() if k!='other_fields'};d.update(other['other_fields']);d['atoms']=[atoms[i] for i in indices];assert d==raw[name]
 assert len(d['primal_float'])==len(d['atoms']) and len(d['row_names'])==len(set(d['row_names']))
assert sum(len(x) for x in view['original_record_maps'].values())==1747
assert raw['trueH_bidirectional_discovery.json']['atoms']==raw['trueH_fixed_closure_discovery.json']['atoms']
f=raw['trueH_fixed_closure_fullpricing.json'];assert len(f['atoms'])==849 and all(v==0 for v in f['primal_float'][749:])
assert len(f['history'])==4 and sum(len(x['state_reports']) for x in f['history'])==128
assert [x['maximum_state'] for x in f['history'][-1]['state_reports'] if x['minimum_scaled_residual']<0]==[0,1,2,4,8,23,27,29,30,31]
assert raw['exact_all_hinge_breakpoints.json']['source_sha256']=='891c3ad5319436859425bfe3cab25eef68cef66177e505b3087d801baafb327e'
assert len(raw['exact_all_hinge_breakpoints.json']['negative_slacks'])==18
for n,code in [('trueH_bidirectional_discovery.json','trueH_bidirectional_pricing.py'),('trueH_fixed_closure_discovery.json','trueH_fixed_closure_pricing.py')]:
 assert raw[n]['code_sha256']==next(m['sha256'] for m in M if Path(m['path']).name==code)
paths=D['formal_objects']+[str((E/'README.md').relative_to(R))];linkcount=0
for name in paths:
 p=R/name;text=p.read_text()
 if name in D['formal_objects']:
  assert text.startswith('---\n');meta=yaml.safe_load(text.split('---',2)[1]);assert all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs'])
 for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)',text):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#')[0]).resolve();assert q.exists(),(name,target);linkcount+=1
for c in C:
 assert all(c[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all((R/t).exists() for t in c['targets'])
assert all((R/p).exists() for p in D['checkpoint_paths'])
report={'asset_selfcheck_runs':3,'prior_attempts':['failed before completion because reconstruction missed nested other_fields; flattening corrected without changing view','failed at missing expected first formal file; first object explicitly written thenchecked'],'passed':True,'primary_size_sha':8,'comparison_size_sha':3,'primary_python_AST_only':py,'primary_JSON_parsed':js,'formal_YAML_checked':3,'local_links_checked':linkcount,'receipts_checked':8,'lossless_atoms_roundtripped':1747,'distinct_complete_atoms':849,'state_logs_preserved':128,'math_programs_imported_or_executed':0,'LP_oracle_BI_random_runs':0,'scope':'Hash/serialization/shape/link/metadata check only; no original or new mathematical audit executed.'}
(W/'asset-selfcheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
