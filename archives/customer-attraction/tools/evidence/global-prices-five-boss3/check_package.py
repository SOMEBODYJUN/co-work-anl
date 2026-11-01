from pathlib import Path
from fractions import Fraction as F
import json,ast,hashlib,re
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'global_prices_deliverables';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ss=json.loads((S/'source-manifest.json').read_text());assert len(ss)==5 and sum(x['size']for x in ss)==915155
for x in ss:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size']and sha(p)==x['sha256']
related=json.loads((S/'related-and-runtime-manifest.json').read_text());assert len(related)==11
for x in related:
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
rows=json.loads((S/'replay/all-reported-column-checks.json').read_text())['reports'];assert len(rows)==2
assert [(x['negative_columns'],x['active_rows'],x['dual_source_columns'])for x in rows]==[(1024,36,64),(23,37,65)]
for x in rows:
 assert len(x['columns'])==x['negative_columns'] and x['all_unique_atom_keys']and x['all_dual_lambda_nonnegative']and x['discarded_nonzero_lambda_count']==0
 assert all(F(v['exact_binary_float_dual_rational_residual'])<0 and v['stored_float_residual']<-1e-8 and v['float_difference']<1e-8 and len(v['all_2196_coefficient_sha256'])==64 for v in x['columns'])
 assert min(F(v['exact_binary_float_dual_rational_residual'])for v in x['columns'])==F(x['minimum_exact_residual'])
report=json.loads((S/'replay/column-replay-execution.json').read_text());assert report['columns_checked']==1047 and report['source_exact_coefficient_evaluations']==2299212 and report['exit_code']==0 and report['assertions_enabled']
assert all(report[k]==0 for k in ('block_price_imports','price_root_hist_imports','original_CLI_calls','search_run_calls','random_formula_check_calls','LP_calls','root_completion_evaluations'))
assert (S/'column-replay-stderr.txt').read_text()==''
relation=json.loads((S/'frozen-support-version-relations.json').read_text());assert relation['original_64_atoms_equal_reopt_added_first64_in_order']and relation['reopt_added_last_atom_equals_aligned_best']and relation['same_positive_descriptor_support']
assert relation['reopt_added_positive_float_point_count']==relation['later2396_exact_atoms']==38
root=json.loads((S/'root-histogram-input-and-domain-index.json').read_text());assert root['stored_columns']==9770 and root['row_count']==1326 and root['fixed_atoms']==38 and root['full_atom_histograms_that_source_run_would_price']==2356608
assert root['source_run_calls']==root['source_imports']==root['source_direct_off_calls']==0 and root['primitive_prefix_exec_calls']==1
interface=json.loads((S/'root-primitive-interface-execution.json').read_text());assert interface['primitive_rows']==1310 and interface['primitive_variables']==1216 and interface['original_per_index_equality_groups']==76 and interface['fixed_histogram_atom_equalities']==38
assert interface['all_1310_row_names_equal_frozen_root_dual_order']and interface['all_1310_row_specs_equal_frozen_root_dual_order']and interface['LP_calls']==0
finals=[(D/'pricing-programs.md',Path('archives/customer-attraction/state/程序/增强五人索引对偶的全型与分块定价合同--程序.md')),(D/'pricing-columns.md',Path('archives/customer-attraction/state/计算/两份索引定价报告的全部负列与冻结对偶核对--计算.md'))]
ep=R/'archives/customer-attraction/tools/evidence/global-prices-five-boss3';brel=Path('archives/customer-attraction/state/计算/增强三十八原子与五十三根直方图的原审查恢复--计算.md');bstage=B/'global_reviews_stage_boss3/delivery'/brel
links=0;staged_links=0
for src,fr in finals:
 body=src.read_text();assert all(l.count('$')%2==0 for l in body.splitlines())and body.count('\\[')==body.count('\\]')
 assert all(v=='68fad804ec5946cb296f77dc5b336308a66abf12'for v in re.findall(r'source:([^:]+):',body))
 for match in re.finditer(r'\]\(([^)]+)\)',body):
  href=match.group(1)
  if '://'in href or href.startswith('#'):continue
  p=(R/fr.parent/href.split('#')[0]).resolve()
  if p.is_relative_to(ep):p=S/p.relative_to(ep)
  for sf,df in finals:
   if p==R/df:p=sf
  if p==R/brel and not p.exists():p=bstage;staged_links+=1
  assert p.exists(),str(p);links+=1
receipt=json.loads((D/'receipts-20261101-global-prices-five.json').read_text());assert {x['id']for x in receipt}=={x['id']for x in ss}and all(x['disposition']=='integrated'for x in receipt)
assert not any(S.rglob('__pycache__'))
result={'status':'all source/related hashes/all1047 residual records/domain census/receipt/link checks passed','primary_sources':5,'primary_bytes':915155,'related_files':11,'reported_columns_checked':1047,'original_exact_coefficient_evaluations':2299212,'stored_dual_rational_residuals_all_strictly_negative':True,'new_full_or_block_pricing_searches':0,'new_original_CLI_calls':0,'new_LP_calls':0,'price_aligned_definition_import_events':1,'root_primitive_order_prefix_events':1,'root_histogram_run_or_import_calls':0,'root_histogram_enumerations':0,'root_primitive_names_and_specs_match':True,'formal_links_checked':links,'parallel_B_links_currently_resolved_to_its_stage':staged_links,'no_parallel_work_claimed_as_own_execution':True,'math_delimiters_balanced':True,'stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
