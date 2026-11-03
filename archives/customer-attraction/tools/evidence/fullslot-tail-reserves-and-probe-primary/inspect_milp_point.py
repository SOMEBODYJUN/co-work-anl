"""Inspect one frozen MILP policy exactly; no discovery solver is imported or run."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
from itertools import product
import json, hashlib
B=Path(__file__).resolve().parent
p=B/'original/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/menu_budget/three_tail_k4_b01.json'
raw=p.read_bytes();a=json.loads(raw,parse_float=Decimal)
k=a['k'];n=a['remaining'];bg=tuple(a['background']);w=[F(x) for x in a['w']];law=[F(x) for x in a['p']]
policy={tuple(h):act for h,act in a['sigma']};domain={h for d in range(n) for h in product(range(k),repeat=d)}
assert len(policy)==len(a['sigma']) and set(policy)==domain and all(0<=v<k for v in policy.values())
assert len(w)==2**k-1 and all(x>=0 for x in w) and sum(w)==1 and sum(law)==1

def finish(h):
    while len(h)<n:h=h+(policy[h],)
    return h

def pay(act,z):
    return sum((mass/F(sum((mask>>b)&1 for b in bg+z)) for mask,mass in enumerate(w,1) if mass and (mask>>act)&1),F(0))

def query(z):
    return sum((law[t]*mass/F(1+sum((mask>>b)&1 for b in bg+z)) for t in range(k) for mask,mass in enumerate(w,1) if mass and (mask>>t)&1),F(0))
rows=[];violations=[]
for h in sorted(domain,key=lambda h:(len(h),h)):
    chosen=policy[h];z=finish(h);u=pay(chosen,z);forced=[finish(h+(t,)) for t in range(k)];vals=[pay(t,z1) for t,z1 in enumerate(forced)]
    row={'history':list(h),'chosen':chosen,'actual_tail':list(z),'payoffs':list(map(str,vals)),'slacks':[str(u-v) for v in vals]};rows.append(row)
    for t,v in enumerate(vals):
        if v>u:violations.append({'history':list(h),'chosen':chosen,'deviation':t,'chosen_payoff':str(u),'deviation_payoff':str(v),'deviation_tail':list(forced[t]),'gain':str(v-u)})
z=finish(());u=pay(policy[()],z);qs=[query(finish((t,))) for t in range(k)];m=min(qs)
out={'scope':'Exact fixed-data check; not an original MILP run or a proof of the universal floor.','source_sha256':hashlib.sha256(raw).hexdigest(),'weights_as_exact_decimal_tokens':list(map(str,w)),'history_count':len(domain),'comparisons_including_self':len(domain)*k,'nonself_comparisons':len(domain)*(k-1),'all_rows':rows,'violations':violations,'saved_policy_is_SPE':not violations,'actual_tail':list(z),'actual_root_payoff':str(u),'fullslot_query_by_forced_action':list(map(str,qs)),'fullslot_minimum':str(m),'actual_saved_policy_gap':str(m-u),'reported_gap_float':str(a['gap_float']),'original_status':a['status'],'original_message':a['message'],'original_mip_objective_lower_bound':str(a['dual_bound']),'new_original_solver_calls':0}
(B/'milp-point-exact-inspection.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['history_count','nonself_comparisons','violations','saved_policy_is_SPE','actual_tail','actual_root_payoff','fullslot_minimum','actual_saved_policy_gap']},ensure_ascii=False))
