from pathlib import Path
from fractions import Fraction as F
from math import lcm
from itertools import product
import json,hashlib,ast,re
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'menu_partition_deliverables';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ss=json.loads((S/'source-manifest.json').read_text());assert len(ss)==8 and sum(x['size']for x in ss)==16296
for x in ss:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for x in json.loads((S/'related-manifest.json').read_text()):
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
 primal=json.loads(p.read_text())['primal'];assert len(primal['atoms'])==64
 for atom in primal['atoms']:
  assert len(atom['bits'])==10 and set(atom['bits'])<={'0','1'}and atom['mass_numerator']>0
  assert len(atom['AE_hist'])==8 and sum(atom['AE_hist'])==5 and all(type(x)is int and x>=0 for x in atom['AE_hist'])
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
for case,report in [('menu-exclusion','menu_exclusion_audit.json'),('partition-127','exact_witness.json'),('partition-14','small_exact_witness.json')]:
 e=json.loads((S/'replay'/case/'execution-record.json').read_text());raw=(S/'replay'/case/'stdout.txt').read_bytes();orig=(S/'original'/report).read_bytes()
 assert raw==orig and json.loads(raw)==json.loads((S/'replay'/case/'parsed-output.json').read_text())
 assert e['exit_code']==0 and e['stderr_bytes']==0 and e['assertions_enabled']and e['original_entry_calls']==1 and e['LP_calls']==0 and e['discovery_probe_calls']==0
 assert (S/'replay'/case/'stderr.txt').read_text()==''
menu=json.loads((S/'original/menu_exclusion_audit.json').read_text());assert menu['identity_checks']==sum(2**(k*n)*3*(n-1)*n for k in range(1,4)for n in range(2,5))==168264
assert F(menu['frozen_437_point_AE_last_off_R'])<0
bindings=json.loads((S/'all-vector-recovery-bindings.json').read_text())['inputs'];assert len(bindings)==2
for x in bindings:
 assert x['weights_length']==63 and len(x['all63_coordinates'])==63
 report=json.loads((S/'original'/x['exact_output']).read_text());assert len(report)==17
 assert len(report['last_payoff_matrix'])==6 and all(len(row)==6 for row in report['last_payoff_matrix'])and len(report['all_pair_coverages'])==21
 assert report['complete_replies']==[1,4,4,5,5,4]and report['unique_optimal_support']==[2,3]and report['half_coverage_holds']
 assert x['positive_coordinates']==len(report['types'])and sum(t['multiplicity']for t in report['types'])==report['unit_customers']
 assert all(not(2 in t['topics']and 3 in t['topics'])for t in report['types'])
 assert min(map(F,report['partition_minima_for_two_matchings']))-report['W']==F(report['minimum_excess_over_W'])>0
 assert F(x['addition_query_fee_from_types'])-report['W']==F(x['addition_minus_W'])
assert [(x['common_scale'],x['unit_customers'],x['positive_coordinates'])for x in bindings]==[(71,127,15),(1,14,9)]
assert [x['addition_query_fee_from_types']for x in bindings]==['72','8']
probe=json.loads((S/'original/probe.json').read_text());assert probe['checked']==1 and probe['best']['iteration']==0 and len(probe['best']['weights'])==63
simp=json.loads((S/'original/integer_simplification.json').read_text());assert len(simp)==5 and simp['objective']==14 and len(simp['weights'])==63
finals=[(D/'menu-audit.md',Path('archives/customer-attraction/state/计算/去对角菜单原展开审计与冻结报告复现--计算.md')),(D/'partition-audits.md',Path('archives/customer-attraction/state/计算/最优分区冻结查询的发现记录与两规模原精确审计--计算.md'))]
ep=R/'archives/customer-attraction/tools/evidence/menu-partition-eight-boss3';links=0
for src,fr in finals:
 body=src.read_text();assert all(line.count('$')%2==0 for line in body.splitlines())and body.count('\\[')==body.count('\\]')
 assert all(ref=='68fad804ec5946cb296f77dc5b336308a66abf12'for ref in re.findall(r'source:([^:]+):',body))
 for m in re.finditer(r'\]\(([^)]+)\)',body):
  href=m.group(1)
  if '://'in href or href.startswith('#'):continue
  p=(R/fr.parent/href.split('#')[0]).resolve()
  if p.is_relative_to(ep):p=S/p.relative_to(ep)
  for sf,df in finals:
   if p==R/df:p=sf
  assert p.exists(),str(p);links+=1
receipts=json.loads((D/'receipts-20261101-menu-partition-eight.json').read_text());assert {x['id']for x in receipts}=={x['id']for x in ss}and all(x['disposition']=='integrated'for x in receipts)
assert not any(S.rglob('__pycache__'))
result={'status':'all primary/related hashes/full report bytes/63-coordinate bindings/counts/receipt/link checks passed','primary_sources':8,'primary_bytes':16296,'new_original_entry_calls':3,'menu_entry_calls':1,'exact_audit_entry_calls':2,'new_probe_entry_or_import_calls':0,'new_LP_calls':0,'canonical_imports':0,'all_three_frozen_reports_byte_identical':True,'identity_grid_checks':168264,'additional_fixed437_atoms':64,'vector_lengths':[63,63],'recovered_customers':[127,14],'recovery_scales':[71,1],'addition_fees':['72','8'],'integer_global_minimality_not_claimed':True,'old_missing_source_epoch_retained':True,'formal_links_checked':links,'math_delimiters_balanced':True,'stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
