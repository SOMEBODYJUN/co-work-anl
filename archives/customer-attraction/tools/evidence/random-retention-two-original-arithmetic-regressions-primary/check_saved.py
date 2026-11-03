"""Saved-byte/AST/report/event/link verification only; never import or run either entry."""
from pathlib import Path
import ast,hashlib,json,re
E=Path(__file__).resolve().parent
S=E.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
 m=read(E/'source-manifest.json');assert m['primary_source_count']==len(m['sources'])==4
 assert sum(s['size'] for s in m['sources'])==m['primary_bytes']==8970
 source=[]
 for s in m['sources']:
  p=S/s['preserved_as'];b=p.read_bytes()
  assert len(b)==s['size'] and sha(p)==s['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['blob']
  if p.suffix=='.py':
   tree=ast.parse(b);mods=[]
   for node in ast.walk(tree):
    if isinstance(node,ast.Import):mods.extend(x.name for x in node.names)
    elif isinstance(node,ast.ImportFrom):mods.append(node.module)
   assert set(mods)=={'fractions','itertools','math','pathlib','json'}
  else:json.loads(b)
  source.append({'id':s['id'],'size':len(b),'sha256':s['sha256'],'git_blob_matches':True})
 comparisons=read(E/'comparison-and-relationships.json')['comparisons'];assert len(comparisons)==10
 for c in comparisons:
  p=S/c['preserved_as'];assert p.stat().st_size==c['size'] and sha(p)==c['sha256'] and c['full_file_read']
 fresh=read(E/'original/fresh/audit_random_retention_blind.json');root=read(E/'original/root/audit_erasure_kernels.json')
 assert fresh['status']=='passed' and root['status']=='PASS'
 assert fresh['coefficient_domain']=={'r':[1,8],'n':'1..r','t':'1..r','b':[0,4]}
 assert [fresh[k] for k in ('coefficient_checks','enumerated_conditional_samples','concavity_operator_checks','semigroup_and_cocycle_checks')]==[1020,8965,288,960]
 assert root['checks']=={'conditional_subsets':16388,'kernel_cases':1140,'nested_cases':660,'concavity_cases':180,'potential_endpoints':180}
 assert fresh['five_player_total_defect_by_n_and_positive_t']==root['m5_empty_background_Q_coefficients_E1_to_E5']
 events=[]
 for label,stem in (('fresh','audit_random_retention_blind'),('root','audit_erasure_kernels')):
  d=E/'runs'/label;event=read(d/'event.json');started=read(d/'started.json');entry=d/(stem+'.py');report=d/(stem+'.json');original=E/'original'/label
  assert (original/(stem+'.py')).read_bytes()==entry.read_bytes()
  assert (original/(stem+'.json')).read_bytes()==(d/'frozen-report.json').read_bytes()==report.read_bytes()
  assert event['all_pass'] and event['exit_code']==0 and event['original_entry_invocations']==1
  assert event['report_byte_identical'] and event['stdout_json_equals_report']
  assert event['entry_sha256']==started['entry_sha256']==sha(entry)
  assert event['expected_report_sha256']==started['expected_report_sha256']==event['generated_report_sha256']==sha(report)
  assert json.loads((d/'stdout.txt').read_bytes())==read(report)
  assert (d/'stderr.txt').read_bytes()==b''
  assert '-B' in started['command'] and '-O' not in started['command']
  events.append({'label':label,'all_pass':True,'original_entry_invocations':1,'report_byte_identical':True})
 boundary=read(E/'execution-boundary.json')
 assert boundary['original_entry_calls']==2 and boundary['fresh_original_entry_calls']==boundary['root_original_entry_calls']==1
 assert boundary['additional_source_imports_or_source_function_calls']==boundary['canonical_model_SPE_BI_LP_random_discovery_calls']==0
 objects=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(objects)==1
 txt=objects[0].read_text();front=txt.split('---',2)[1]
 for field in ('id:','kind:','type_tag:','title:','status:','truth_status:','review_level:','scope:','summary:','source_refs:'):assert field in front
 known={c['path'] for c in comparisons};missing=[];controls=[]
 for p in (objects+[E/'README.md']):
  b=p.read_bytes()
  if any(x<32 and x not in (9,10,13) for x in b):controls.append(str(p.relative_to(S)))
  for link in re.findall(r'\]\(([^)]+)\)',b.decode()):
   if '://' in link or link.startswith('#'):continue
   q=(p.parent/link.split('#')[0]).resolve()
   try:rel=str(q.relative_to(S))
   except ValueError:missing.append([str(p.relative_to(S)),link]);continue
   if not q.exists() and q!=E/'verification.json' and rel not in known:missing.append([str(p.relative_to(S)),link])
 assert not missing and not controls
 for row in m['payload']:
  p=S/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
 return {'all_pass':True,'primary_count':4,'primary_bytes':8970,'source_fingerprints':source,'complete_comparison_snapshots':len(comparisons),'new_objects':1,'events':events,'current_original_entry_calls_total':2,'current_SPE_BI_LP_random_discovery_calls':0,'checker_original_entry_import_or_source_function_calls':0,'payload_files_checked':len(m['payload']),'missing_links':missing,'control_character_files':controls,'method':'AST parsing; source/comparison fingerprints; complete stored JSON and event binding; byte-identical generated/frozen reports; frontmatter and relative links only. No kernel reconstruction, parameter tests or entry replay.'}
if __name__=='__main__':
 result=check();(E/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_fingerprints'},ensure_ascii=False))
