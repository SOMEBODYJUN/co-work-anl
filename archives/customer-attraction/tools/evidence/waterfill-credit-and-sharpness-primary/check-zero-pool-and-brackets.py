#!/usr/bin/env python3
"""New data-only arithmetic supplement: six34 leaves/21static columns and saved brackets.
Does not import/execute either original audit, solve VAR, or rescan full SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import Counter
import json,hashlib
E=Path(__file__).resolve().parent
out=E/'zero-pool-and-brackets-exact.json'
assert not out.exists(),'data supplement is single-call; do not repeat'
base=E/'context/archives/customer-attraction/tools/evidence/continuation-security'
ip=base/'examples/customer_attraction/individual_security_failure.json';cp=base/'evidence/certificates/customer_attraction/individual_security_failure.json'
rp=E/'original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/waterfill_exact.json'
ins=json.loads(ip.read_text());cert=json.loads(cp.read_text());report=json.loads(rp.read_text())
customers=[frozenset(r['topics']) for r in ins['customers'] for _ in range(r['multiplicity'])]
actions={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
assert len(customers)==34 and len(actions)==43
# Only six forced-root continuations, not all43 SPE nodes or258 comparisons.
def finish(h):
 while len(h)<3:h=h+(actions[h],)
 return h
def pay(z,a):return sum((F(1,sum(b in c for b in z)) for c in customers if a in c),F())
t=F(cert['security']['value']);assert t==F(2411,246)
roots=[]
for a in range(6):
 z=finish((a,));u=[pay(z,b) for b in z]
 assert u[0]==F(29,3) and min(u[1:])>t
 roots.append({'root':a,'terminal':z,'payoffs':list(map(str,u)),'all_real_tail_strictly_high':True})
z=finish(());assert z==(0,3,4)
spectrum=Counter(sum(b in c for b in z) for c in customers if 0 in c)
assert spectrum=={2:12,3:11}
p=[F(a) for a in cert['security']['primary']];Q={tuple(r['rivals']):F(r['probability']) for r in cert['security']['dual']}
assert sum(p)==sum(Q.values())==1
bs=list(combinations_with_replacement(range(6),2))
def kernel(a,b):return sum((F(1,1+sum(x in c for x in b)) for c in customers if a in c),F())
mat=[[kernel(a,b) for b in bs] for a in range(6)]
cols=[sum(p[a]*mat[a][i] for a in range(6)) for i in range(len(bs))]
assert min(cols)==t
caps=[sum(w*kernel(a,b) for b,w in Q.items()) for a in range(6)]
assert caps==[t]*6
rho=F(99,100);g=12/(1+rho)+11/(2+rho);gap=t-g;lb=(1-rho)*gap
assert gap==F(1342711,14637246) and lb==F(1342711,1463724600)>0
W=sum(pay(z,a) for a in z);assert W==32
sharp=[];D=F(647,8772)
for row in report['cases']:
 assert len(row)==10
 c=row['common_core'];threshold=F(row['threshold']);before=F(row['low_original']);lo,hi=map(F,row['water_weight_interval'])
 assert 0<lo<hi<1 and hi-lo==F(1,2**80)
 def low(w):return 12/(1+w)+11/(2+w)+c/(3+w)
 def gamma(w):return c/(3+w)-F(c,4)
 assert threshold==F(28481,2924)+F(c,4) and before==F(29,3)+F(c,4)
 assert threshold-before==D==F(row['deficit'])
 assert low(lo)>=threshold>=low(hi)
 a,b=gamma(hi),gamma(lo)
 assert [a,b]==list(map(F,row['root_gain_interval']))
 assert [a/D,b/D]==list(map(F,row['root_gain_over_deficit_interval']))
 linear=before/threshold
 assert linear==F(row['linear_retention']) and low(linear)==F(row['linear_final_unit'])
 assert threshold-low(linear)==F(row['linear_shortfall'])>0
 entry={'common_core':c,'bracket_width':str(hi-lo),'F_lower_endpoint':str(low(lo)-threshold),'F_upper_endpoint':str(low(hi)-threshold),'gamma_interval':list(map(str,[a,b])),'ratio_interval':list(map(str,[a/D,b/D])),'linear_shortfall':row['linear_shortfall']}
 if c:
  lower=F(c,c+94);upper=F(9*c,9*c+608)
  assert lower<a/D<=b/D<upper
  entry['strict_rational_ratio_bounds']=[str(lower),str(upper)]
 sharp.append(entry)
result={'status':'pass','entry_calls':1,'original_source_calls':0,'new_full_SPE_scans':0,'VAR_optimization_calls':0,'LP_or_solver_calls':0,'inputs':[{'path':str(p.relative_to(E)),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (ip,cp,rp)],'zero_pool':{'customers':34,'stored_actions':43,'forced_root_leaves':roots,'root_decision_histories_reconstructed':6,'full43_IC_nodes_checked':0,'full258_IC_comparisons_checked':0,'static_backgrounds':list(bs),'static_payoff_matrix':[[str(v) for v in row] for row in mat],'all21_primal_values':list(map(str,cols)),'dual6_caps':list(map(str,caps)),'true_v3':str(t),'X0_original_load_spectrum':dict(spectrum),'rho':str(rho),'endpoint_density':str(g),'threshold_minus_endpoint_density':str(gap),'integral_lower_bound':str(lb),'W':str(W),'W_minus3v3':str(W-3*t),'OPT3':34,'half_slack':30,'VAR_state_zero':'analytic KKT at all-high unit weights, no numerical maximization','not_claimed':'new original34 SPE verification or exact virtual VAR maximum'},'all_five_saved80_step_cases':sharp,'ratio_H_endpoints':['608/9','94'],'not_executed':['original5640 again','mixed7105 peer script','old34 audit','constructor','full2800 SPE scan']}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','new_data_entry_calls':1,'six_root_leaves':6,'static_profiles':21,'saved_bracket_cases':5,'positive_debt_lower_bound':str(lb),'original_calls':0},ensure_ascii=False))
