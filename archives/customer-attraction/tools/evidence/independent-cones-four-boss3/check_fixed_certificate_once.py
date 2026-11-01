from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import importlib.util,json,sys,time,hashlib,platform
from datetime import datetime,timezone
S=Path(__file__).resolve().parent;R=S.parent/'independent_cones_runtime'
sys.path.insert(0,str(R));sys.path.insert(0,str(R/'tests/audits'))
from customer_attraction import Instance,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,dot
p=R/'research/workspaces/customer-attraction/R-5bb00b5c3cf740f099eae62130632b56/independent/cone_attack.py'
started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
spec=importlib.util.spec_from_file_location('r5bb_independent_cone_source',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
ins=Instance.from_dict(json.loads((R/'examples/customer_attraction/coverage_opportunity_failure.json').read_text()))
cert=StrategyCertificate.from_dict(json.loads((R/'evidence/certificates/customer_attraction/coverage_opportunity_failure.json').read_text()))
verification=verify_certificate(ins,cert);verification.assert_valid()
k=ins.topic_count;m=ins.players;types=module.all_types(k)
rows=module.cone(ins,cert,types)
reference=StrategyCone(k,m,dict(cert.actions))
assert set(rows)=={tuple(-x for x in row) for row in reference.rows}
assert reference.root==cert.terminal_counts==(2,1,0,0,0)
weights=tuple(F(sum(c.multiplicity for c in ins.customers if c.topics==t)) for t in types)
assert all(dot(row,weights)<=0 for row in rows)
A=verification.terminal_history
payoff_columns={a:module.payoff_row(cert.terminal_counts,a,types) for a in set(A)}
assert all(dot(row,weights)==ins.topic_payoff(a,cert.terminal_counts) for a,row in payoff_columns.items())
w=tuple(F(any(cert.terminal_counts[a] for a in t)) for t in types)
assert dot(w,weights)==8
objectives=[]
for portfolio in combinations(range(k),min(k,m)):
 o=tuple(F(bool(t.intersection(portfolio))) for t in types)
 for a,payoff in payoff_columns.items():
  for coef in (m,m-1):
   v=tuple(x+coef*y-z for x,y,z in zip(w,payoff,o))
   slack=dot(v,weights)
   assert slack==ins.welfare(cert.terminal_counts)+coef*ins.topic_payoff(a,cert.terminal_counts)-sum(c.multiplicity for c in ins.customers if c.topics.intersection(portfolio))
   objectives.append({'portfolio':list(portfolio),'topic':a,'coefficient':coef,'exact_slack_at_fixed_input':str(slack),'coefficients':list(map(str,v))})
D=S/'replay';D.mkdir(exist_ok=True)
serialized=[{'comparison_index':i,'deviation_minus_chosen_coefficients':list(map(str,row)),'exact_slack_le_zero_at_fixed_input':str(dot(row,weights))} for i,row in enumerate(sorted(rows))]
(D/'full-cone-row-comparison.json').write_text(json.dumps({'scope':'source cone called once; sorted view only for comparison, not original LP row order','type_masks':[sum(1<<a for a in t)for t in types],'all_rows':serialized,'matches_negative_canonical_G_rows':True},indent=2)+'\n')
(D/'all-fixed-input-objective-comparisons.json').write_text(json.dumps(objectives,indent=2)+'\n')
summary={'event':'one deterministic original cone-function check on existing11-unit-customer complete certificate; not random attack or historical report replay','start_utc':started,'elapsed_seconds':time.monotonic()-tick,'exit_code':0,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'Python':platform.python_version(),'assertions_enabled':__debug__,'k':k,'m':m,'unit_customers':ins.customer_count,'histories':verification.checked_histories,'nonself_deviations':verification.checked_deviations,'distinct_nonzero_cone_rows':len(rows),'all31_type_coefficients_bound':True,'source_cone_calls':1,'reference_cone_calls':1,'ExactSPESolver_calls':0,'attack_calls':0,'original_CLI_calls':0,'random_draws':0,'LP_calls':0,'all_cone_rows_equal_negative_reference':True,'terminal':list(cert.terminal_counts),'actual_path':list(A),'actual_payoffs':list(map(str,ins.player_payoffs(A))),'W':8,'OPT':ins.optimal_welfare(),'exact_objective_comparisons':len(objectives),'minimum_original_m_coefficient_slack':str(min(F(x['exact_slack_at_fixed_input'])for x in objectives if x['coefficient']==m)),'minimum_strong_m_minus1_slack':str(min(F(x['exact_slack_at_fixed_input'])for x in objectives if x['coefficient']==m-1)),'scope_limit':'single supplied strategy and input; no optimized cone upper/lower value or any of280 historical rounds reconstructed'}
(D/'fixed-certificate-check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
