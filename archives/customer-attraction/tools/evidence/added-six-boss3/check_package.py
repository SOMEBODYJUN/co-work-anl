from pathlib import Path
from fractions import Fraction as F
import json,hashlib,ast,re
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'added_six_deliverables';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((S/'source-manifest.json').read_text());assert len(sources)==6 and sum(x['size']for x in sources)==307076
for x in sources:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size']and sha(p)==x['sha256']
related=json.loads((S/'related-manifest.json').read_text());assert len(related)==8
for x in related:
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
a=json.loads((S/'original/reopt_added.json').read_text());t=json.loads((S/'original/reopt_added_triple.json').read_text());e=json.loads((S/'original/enhanced_2396_exact_obstruction.json').read_text())
assert len(a)==len(t)==8 and len(e)==12
assert len(a['names'])==len(a['dual_lambda'])==2196 and len(t['names'])==len(t['dual_lambda'])==2396 and len(set(t['names']))==2396
assert a['atoms']==t['atoms']and len(a['atoms'])==len(t['point'])==65 and a['point']==t['point']
assert a['names']==t['names'][:2196]and a['dual_lambda']==t['dual_lambda'][:2196]and all(x==0 for x in t['dual_lambda'][2196:])
primal=json.loads((S/'related/evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
prefix='research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_global/'
best=json.loads((S/'related'/prefix/'price_aligned.json').read_text())['best']['atom'];assert a['atoms']==primal['atoms']+[best]
assert e['rows']==2396 and e['atoms']==65 and e['positive_atoms']==38 and len(e['point'])==65 and len(e['atom_masses'])==38
masses=list(map(F,e['point']));assert min(masses)>=0 and sum(x>0 for x in masses)==38 and sum(x==0 for x in masses)==27
assert [{**atom,'mass':v}for atom,v in zip(t['atoms'],e['point'])if F(v)>0]==e['atom_masses']
assert sum(x*int(any(map(int,atom['bits'][:5])))for atom,x in zip(t['atoms'],masses))==1
assert sum(x*int(any(atom['AB_hist'][4:]))for atom,x in zip(t['atoms'],masses))==F(e['objective'])>2
assert F(e['objective'])-2==F(e['gap_above_two'])and e['aligned_tax_violations']=={}and e['all_rows_verified_exactly']
ns=json.loads((S/'replay/recovery-internals.json').read_text());assert ns['input_atoms']==65 and ns['rows']==2396 and ns['row_names']==t['names']and ns['exact_nonnegative_point']==e['point']
assert len(ns['selected_positive_float_indices'])==ns['exact_basis_rank']==38 and ns['near_active_float_rows']==44
slack={n:F(v)for n,v in ns['all_original_computed_slacks'].items()};assert len(slack)==2396 and min(slack.values())==0 and sum(x==0 for x in slack.values())==e['zero_slacks']==44
assert ns['added_triple_rows']==ns['added_triple_positive_rows']==200 and ns['added_triple_zero_rows']==0 and F(ns['minimum_added_triple_slack'])>0
assert all('three-profit'not in n for n,v in slack.items()if v==0)
event=json.loads((S/'replay/execution-record.json').read_text());assert event['exit_code']==0 and event['assertions_enabled']and event['original_recovery_top_level_runs']==1
assert event['original_reopt_import_or_runs']==event['original_review2396_runs']==event['LP_calls']==0
assert event['output_file_bytes_equal']and (S/'replay/enhanced_2396_exact_obstruction.json').read_bytes()==(S/'original/enhanced_2396_exact_obstruction.json').read_bytes()
assert (S/'replay/stderr.txt').read_text()==''and len((S/'replay/stdout.txt').read_bytes())==450
ref=json.loads((S/'reused-review-reference.json').read_text());assert ref['current_review_runs']==0 and ref['input_primary_sha256']==sha(S/'original/enhanced_2396_exact_obstruction.json')
for x in ref['sources']:
 p=R/x['path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
fr=Path('archives/customer-attraction/state/计算/新增负列与三人条件后的六十五列恢复链--计算.md');ep=R/'archives/customer-attraction/tools/evidence/added-six-boss3';body=(D/'formal-object.md').read_text();assert all(line.count('$')%2==0 for line in body.splitlines())and body.count('\\[')==body.count('\\]')
assert all(x=='68fad804ec5946cb296f77dc5b336308a66abf12'for x in re.findall(r'source:([^:]+):',body));links=0
for m in re.finditer(r'\]\(([^)]+)\)',body):
 href=m.group(1)
 if '://'in href or href.startswith('#'):continue
 p=(R/fr.parent/href.split('#')[0]).resolve()
 if p.is_relative_to(ep):p=S/p.relative_to(ep)
 assert p.exists(),str(p);links+=1
receipts=json.loads((D/'receipts-20261101-added-six.json').read_text());assert {x['id']for x in receipts}=={x['id']for x in sources}and all(x['disposition']=='integrated'for x in receipts)
assert not any(S.rglob('__pycache__'))
result={'status':'all hashes/float-chain/all65exact-vector-and38records/source-recovery-internals/receipt/link checks passed','primary_sources':6,'primary_bytes':307076,'related_files':8,'new_original_recovery_top_level_runs':1,'new_reopt_or_LP_runs':0,'reused_B_review_current_runs':0,'recovery_full_file_bytes_identical':34584,'candidate_columns':65,'exact_positive_atoms':38,'exact_zero_coordinates':27,'selected_near_active_rows':44,'exact_basis_rank':38,'exact2396_slacks_reused_from_original_recover_namespace':True,'new_triple_rows':200,'new_triple_lambda_zero':True,'new_triple_rows_strict_at_current_point':200,'legacy_mass_numerator_positive_records':37,'exact_LP_optimality_or_SPE_claimed':False,'formal_links_checked':links,'math_delimiters_balanced':True,'stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
