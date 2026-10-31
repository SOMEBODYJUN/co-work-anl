"""New definition-level finite check of an analytic cap counterfamily.
This is not a recovered source program or an all-instance solver.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json

def one(m):
    assert m>=2
    labels=range(m) # 0 has two clients; each1..m-1 one distinct client
    def action(h):
        fresh=next((b for b in range(1,m)if b not in h),None)
        if len(h)<m-1:
            assert fresh is not None
            return fresh
        if h.count(0)<=1:return 0
        assert fresh is not None
        return fresh
    @lru_cache(None)
    def finish(h):return h if len(h)==m else finish(h+(action(h),))
    def payoff(a,z):
        assert z.count(a)>0
        return F(2 if a==0 else 1,z.count(a))
    count=checks=0;minimum=None
    for depth in range(m):
        for h in product(labels,repeat=depth):
            own=payoff(action(h),finish(h));count+=1
            for a in labels:
                gap=own-payoff(a,finish(h+(a,)));assert gap>=0,(m,h,a,gap)
                minimum=gap if minimum is None else min(minimum,gap);checks+=1
    z=finish(());u=[payoff(a,z)for a in z];W=sum(2 if a==0 else 1 for a in set(z));OPT=m+1
    assert z==tuple(range(1,m))+(0,)and u==[F(1)]*(m-1)+[F(2)]and W==OPT
    gap=(m-1)*u[-1]-W;assert gap==m-3
    return {'players':m,'topics':m,'unit_customers':m+1,'complete_ordered_decision_histories':count,'IC_including_self':checks,'minimum_IC':str(minimum),'actual_path':z,'actual_payoffs':list(map(str,u)),'W':W,'OPT':OPT,'cap_lhs_minus_W':str(gap),'auxiliary_cap_refuted':gap>0,'half_margin':2*W-OPT}
rows=[one(m)for m in range(2,7)]
result={'scope':'new finite independent expansion of explicit analytic full-history strategy; no old source rerun or general half counterexample','cases':rows,'total_histories':sum(x['complete_ordered_decision_histories']for x in rows),'total_IC_including_self':sum(x['IC_including_self']for x in rows)}
Path(__file__).with_name('last_profit_cap_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
