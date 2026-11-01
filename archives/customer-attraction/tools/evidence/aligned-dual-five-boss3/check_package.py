from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib,re
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'aligned_dual_deliverables';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((S/'source-manifest.json').read_text());assert len(sources)==5 and sum(x['size']for x in sources)==94304
for x in sources:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for x in json.loads((S/'related-manifest.json').read_text()):
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
e=json.loads((S/'replay/execution-record.json').read_text());assert e['exit_code']==0 and e['assertions_enabled']and e['original_recovery_top_level_runs']==1 and e['original_reopt_import_or_runs']==e['LP_calls']==0
assert e['recovered_file_bytes_equal']and (S/'replay/aligned_support_exact_dual.json').read_bytes()==(S/'original/aligned_support_exact_dual.json').read_bytes()
assert (S/'replay/stderr.txt').read_text()=='' and len((S/'replay/stdout.txt').read_bytes())==396
exact=json.loads((S/'original/aligned_support_exact_dual.json').read_text());assert len(exact)==7 and F(exact['beta'])<2 and 2-F(exact['beta'])==F(exact['gap_below_two'])>0
assert len(exact['multipliers'])==36 and all(F(x)>0 for x in exact['multipliers'].values())
res=list(map(F,exact['support_column_residuals']));assert len(res)==64 and min(res)>=0 and sum(x==0 for x in res)==37 and sum(x>0 for x in res)==27
assert exact['verified_nonnegative_on_64_columns']and not exact['full_type_certificate']
c=json.loads((S/'parameter-and-one-column-comparison.json').read_text());assert c['parameter_count']==37 and c['parameters_identically_equal']==0 and c['parameters_different']==37 and c['same_active_set_despite_thresholds']
assert all(F(x['recovered_exact'])!=F(x['previous_binary_float_as_rational'])and F(x['exact_difference'])==F(x['recovered_exact'])-F(x['previous_binary_float_as_rational'])for x in c['parameters'])
neg=json.loads((S/'original/aligned_dual_exact_negative.json').read_text());assert len(neg)==4 and F(neg['residual'])==F(c['outside_column']['new_rational_residual'])<0 and float(F(neg['residual']))==neg['float']
assert c['outside_column']['outside_original64']and c['outside_column']['valid_domain']and c['outside_column']['same_coefficient_vector_as_previous_aligned_best']and not c['outside_column']['same_residual_exactly']
assert c['execution']['new_negative_columns_checked']==1 and not c['execution']['whole1047_rescan']and c['execution']['new_LP_calls']==0
formal=D/'formal-object.md';body=formal.read_text();assert all(l.count('$')%2==0 for l in body.splitlines())and body.count('\\[')==body.count('\\]')
assert all(x=='68fad804ec5946cb296f77dc5b336308a66abf12'for x in re.findall(r'source:([^:]+):',body))
frel=Path('archives/customer-attraction/state/计算/六十四列增强索引有理对偶的恢复与域外精确分离--计算.md');ep=R/'archives/customer-attraction/tools/evidence/aligned-dual-five-boss3';links=0
for m in re.finditer(r'\]\(([^)]+)\)',body):
 href=m.group(1)
 if '://'in href or href.startswith('#'):continue
 p=(R/frel.parent/href.split('#')[0]).resolve()
 if p.is_relative_to(ep):p=S/p.relative_to(ep)
 assert p.exists(),str(p);links+=1
receipts=json.loads((D/'receipts-20261101-aligned-dual-five.json').read_text());assert {x['id']for x in receipts}=={x['id']for x in sources}and all(x['disposition']=='integrated'for x in receipts)
assert not any(S.rglob('__pycache__'))
result={'status':'all hashes/whole certificate/37 parameters/one column/receipt/link checks passed','primary_sources':5,'primary_bytes':94304,'new_original_recovery_top_level_runs':1,'new_reopt_import_or_runs':0,'new_LP_calls':0,'recovered_certificate_bytes_identical':7348,'support_columns_certified':64,'support_residual_zeros':37,'support_residual_positive':27,'exact_unknowns_and_tight_columns':37,'active_lambda':36,'different_exact_parameters_from_previous_binary_float':37,'new_outside_columns':1,'whole1047_rescan':False,'exact_negative_original_producer_not_in_five_sources':True,'new_exact_primal_optimum_claimed':False,'full_type_certificate':False,'formal_links_checked':links,'math_delimiters_balanced':True,'all_stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
