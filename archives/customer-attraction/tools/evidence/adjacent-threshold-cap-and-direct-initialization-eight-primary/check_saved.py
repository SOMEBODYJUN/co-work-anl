"""Source/data/structure selfcheck only; no source imports, BI, SPE or LP runs."""
from pathlib import Path
from itertools import product
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def check():
 manifest=read(HERE/'source-manifest.json');source_checks=[]
 for s in manifest['sources']:
  p=ROOT/s['preserved_as'];b=p.read_bytes()
  assert len(b)==s['size'] and hashlib.sha256(b).hexdigest()==s['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['blob']
  source_checks.append(dict(id=s['id'],size=len(b),sha256=s['sha256'],git_blob_matches=True))
 assert len(source_checks)==manifest['primary_source_count']==8
 assert sum(x['size'] for x in source_checks)==manifest['primary_bytes']==19965
 codes={p.name:ast.parse(p.read_text()) for p in (HERE/'original').glob('*.py')}
 assert set(codes)=={'audit_old_foma_counterexample.py','check_adjacent_threshold_cap.py'}
 for tree in codes.values():
  assert not any(isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.left,ast.Name) and n.test.left.id=='__name__' for n in tree.body)
 names=next(ast.literal_eval(n.value) for n in codes['check_adjacent_threshold_cap.py'].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NAMES' for t in n.targets))
 report=read(HERE/'original/adjacent_threshold_cap_diagnostic.json')
 assert [r['name'] for r in report]==names
 assert [r['ascents_checked'] for r in report]==[105,36,1,0,18]
 assert sum(r['ascents_checked'] for r in report)==160
 assert all(set(r)=={'name','ascents_checked','violations','scope'} and r['violations']==[] and r['scope']=='named fixed input only; not a general theorem' for r in report)
 foma=read(HERE/'original/old_foma_counterexample_independent.json')
 assert len(foma)==16
 assert foma['unit_customers']==52 and foma['histories']==259 and foma['IC_checks_including_self']==1554
 assert foma['actual']==[3,3,2,2] and foma['payoffs']==['47/4']*4
 assert foma['W']==47 and foma['OPT']==52 and foma['optimal_supports']==[[0,1,4,5]] and foma['optimal_ordered_tuples']==24
 assert foma['query_columns']==[0,1,4,5]
 assert foma['query_matrix']==[['51/4','38/3','51/4','71/6']]*2+[['47/4','35/3','47/4','35/3']]*2
 assert foma['min_K']=='48' and foma['max_K']=='293/6' and foma['FOMA_EXISTS_false'] is True
 deps=read(HERE/'dependency-manifest.json')['dependencies'];assert len(deps)==10
 dependency_checks=[];input_dims={}
 for d in deps:
  p=ROOT/d['preserved_as'];assert p.stat().st_size==d['size'] and sha(p)==d['sha256']
  if p.suffix=='.py':ast.parse(p.read_text())
  if '/examples/' in d['logical_original_path'] or d['logical_original_path'].startswith('examples/'):
   data=read(p);name=p.stem
   assert data['players']>0 and len(data['topics'])>0
   assert all(type(c['multiplicity']) is int and c['multiplicity']>0 and all(type(t) is int and 0<=t<len(data['topics']) for t in c['topics']) for c in data['customers'])
   input_dims[name]=[data['players'],len(data['topics']),sum(c['multiplicity'] for c in data['customers'])]
  if d['logical_original_path'].endswith('static_matching_counterexample.json'):
   data=read(p);I=data['instance'];rows=data['certificate']['actions'];A={tuple(r['history']):r['action'] for r in rows}
   assert I['players']==4 and len(I['topics'])==6 and sum(c['multiplicity'] for c in I['customers'])==52
   assert len(rows)==len(A)==259
   assert set(A)=={h for k in range(4) for h in product(range(6),repeat=k)}
   assert all(type(a) is int and 0<=a<6 for a in A.values())
   assert d['sha256']=='9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245'
  dependency_checks.append(dict(path=d['logical_original_path'],sha256=d['sha256'],structure_or_syntax_checked=True))
 assert input_dims==dict(root_tax_failure=[4,6,61],aggregate_theta_failure=[3,6,36],portfolio_matching_failure=[2,5,86],worst_pne_welfare_failure=[3,4,16],coverage_opportunity_failure=[3,5,11])
 comparisons=read(HERE/'comparison-and-relationships.json')['comparisons']
 for c in comparisons:
  if 'preserved_as' in c:
   p=ROOT/c['preserved_as'];assert p.stat().st_size==c['size'] and sha(p)==c['sha256']
 for row in manifest['payload']:
  p=ROOT/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
 decision=read(HERE/'execution-decision.json')
 assert all(decision[k]==0 for k in ('original_entry_calls','original_import_calls','source_function_calls','canonical_solver_calls','new_BI_calls','new_payoff_replay_calls','LP_or_discovery_calls'))
 known={c['path'] for c in comparisons};missing=[];controls=[]
 for p in ROOT.rglob('*.md'):
  if 'original' in p.relative_to(ROOT).parts or 'comparison' in p.relative_to(ROOT).parts:continue
  b=p.read_bytes()
  if any(c<32 and c not in (9,10,13) for c in b):controls.append(str(p.relative_to(ROOT)))
  for link in re.findall(r'\]\(([^)]+)\)',b.decode()):
   if '://' in link or link.startswith('#'):continue
   q=(p.parent/link.split('#')[0]).resolve()
   try:r=str(q.relative_to(ROOT))
   except ValueError:missing.append([str(p.relative_to(ROOT)),link]);continue
   if not q.exists() and q!=HERE/'verification.json' and r not in known:missing.append([str(p.relative_to(ROOT)),link])
 assert not missing and not controls
 return dict(all_pass=True,source_fingerprints=source_checks,source_python_AST_only=2,cap_saved_records=5,cap_saved_ascent_total=160,old_foma_saved_top_level_fields=16,old_foma_matrix_rows_read=4,dependencies=dependency_checks,named_input_dimensions=input_dims,full_comparison_snapshots=sum('preserved_as' in c for c in comparisons),existing_status_link_only=sum(c.get('known_existing_link_only',False) for c in comparisons),payload_files_checked=len(manifest['payload']),missing_links=missing,control_character_files=controls,new_original_entry_import_function_BI_SPE_matching_LP_calls=0,method='file fingerprints, syntax, saved field equality, input schema and complete history key set only; no source code execution or mathematical re-audit')
if __name__=='__main__':
 d=check();(HERE/'verification.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k not in ('source_fingerprints','dependencies')},ensure_ascii=False))
