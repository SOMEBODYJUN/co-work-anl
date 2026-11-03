"""Read all five frozen policies and370 log rows; recompute saved-query arithmetic.
No LP, MILP, original entrypoint, or full-policy IC verification is performed.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
from itertools import product
import json,hashlib
B=Path(__file__).resolve().parent
S=B/'original/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/menu_budget'
names=['probe_k5','probe_k6','probe_k7','probe_role3_k6','probe_average_k6']
points=[];logs=[]
for stem in names:
    f=S/(stem+'.json');raw=f.read_bytes();a=json.loads(raw,parse_float=Decimal)
    k=a['k'];n=a['n'];roles=a.get('roles',list(range(n)));w=[F(v) for v in a['w']];p=[F(v) for v in a['p']]
    policy={tuple(h):act for h,act in a['sigma']};domain={h for d in range(n) for h in product(range(k),repeat=d)}
    assert len(policy)==len(a['sigma']) and set(policy)==domain and all(0<=act<k for act in policy.values())
    assert len(w)==2**k-1 and len(p)==k and min(w)>=0 and min(p)>=0
    def finish(h):
        while len(h)<n:h=h+(policy[h],)
        return h
    def payoff(act,z):
        return sum((v/F(sum((mask>>t)&1 for t in z)) for mask,v in enumerate(w,1) if v and (mask>>act)&1),F(0))
    def price(t,z):
        return sum((v/F(1+sum((mask>>a)&1 for a in z)) for mask,v in enumerate(w,1) if v and (mask>>t)&1),F(0))
    actual=finish(());assert list(actual)==a['actual']
    chosen=[payoff(actual[i],actual) for i in roles];menus=[];minimums=[];averages=[];forced_leaves=[]
    for i in roles:
        zz=[finish(actual[:i]+(act,)) for act in range(k)];kk=[[price(t,z) for t in range(k)] for z in zz]
        q=[sum((p[t]*row[t] for t in range(k)),F(0)) for row in kk]
        forced_leaves.append([list(z) for z in zz]);menus.append([[str(v) for v in row] for row in kk]);minimums.append(min(q));averages.append(sum((p[act]*q[act] for act in range(k)),F(0)))
    baseline=sum(chosen,F(0));min_gap=sum(minimums,F(0))-baseline;avg_gap=sum(averages,F(0))-baseline
    expected=avg_gap if stem=='probe_average_k6' else min_gap
    assert abs(float(expected)-float(a['gap']))<1e-12
    encoded={str(d):''.join(str(policy[h]) for h in product(range(k),repeat=d)) for d in range(n)}
    item={'file':f.name,'source_sha256':hashlib.sha256(raw).hexdigest(),'top_level_fields':list(a),'k':k,'n':n,'roles_as_saved':a.get('roles'),'roles_interpretation':roles,'seed':a['seed'],'best_round':a['round'],'saved_gap_token':str(a['gap']),'all_w_tokens':[str(v) for v in a['w']],'all_p_tokens':[str(v) for v in a['p']],'w_token_sum':str(sum(w,F(0))),'p_token_sum':str(sum(p,F(0))),'ordered_history_domain_size':len(domain),'complete_policy_actions_by_depth_lex_order':encoded,'actual':list(actual),'actual_selected_payoffs':list(map(str,chosen)),'baseline_selected_profit':str(baseline),'forced_leaves_by_role_and_action':forced_leaves,'fullslot_price_matrices_forcing_then_query':menus,'row_minima_at_saved_tokens':list(map(str,minimums)),'same_p_averages_at_saved_tokens':list(map(str,averages)),'summin_gap_at_saved_tokens':str(min_gap),'average_gap_at_saved_tokens':str(avg_gap),'summin_gap_approx':float(min_gap),'average_gap_approx':float(avg_gap),'original_mode_interpretation':'same-p average per primary MD and saved gap' if stem=='probe_average_k6' else 'row minimum per primary MD and saved gap','new_IC_checks':0}
    points.append(item)
    lf=S/(stem+'.log.json');lr=lf.read_bytes();ll=json.loads(lr,parse_float=Decimal)
    assert all(set(z)=={'round','gap','best'} and z['round']==j for j,z in enumerate(ll))
    best=-float('inf')
    for z in ll:
        gap=float(z['gap'])
        if gap>best+1e-10:best=gap
        assert abs(best-float(z['best']))<1e-12
    assert abs(float(a['gap'])-best)<1e-12 and a['round']<len(ll)
    logs.append({'file':lf.name,'source_sha256':hashlib.sha256(lr).hexdigest(),'record_count':len(ll),'all_records':[[z['round'],str(z['gap']),str(z['best'])] for z in ll],'any_reported_positive_defect':any(z['gap']>Decimal('1e-7') for z in ll)})
report={'scope':__doc__,'status':'all-fields-and-policy-domains-read;saved-query-arithmetic-consistent','points':points,'logs':logs,'ordered_policy_entries_consumed':sum(x['ordered_history_domain_size'] for x in points),'log_records_consumed':sum(x['record_count'] for x in logs),'new_original_optimizer_or_full_IC_runs':0,'arithmetic_convention':'Exact source decimal tokens, without probability normalization or rational-policy certification.'}
(B/'saved-probe-reading.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'policy_entries':report['ordered_policy_entries_consumed'],'log_records':report['log_records_consumed'],'points':[{'file':x['file'],'min_gap':x['summin_gap_approx'],'average_gap':x['average_gap_approx'],'p_sum':x['p_token_sum'],'w_sum':x['w_token_sum']} for x in points]},ensure_ascii=False))
