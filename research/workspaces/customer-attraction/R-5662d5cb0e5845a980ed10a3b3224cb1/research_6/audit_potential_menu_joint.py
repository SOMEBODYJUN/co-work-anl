"""Independent exact audit of the saved partial-menu obstruction.

Reads only positive type masses. Materializes the symmetric 18-theme instance,
enumerates every six-slot potential tuple, and checks individual late-menu IC.
It does not construct or assert a complete SPE.
"""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import json
import numpy as np


def compositions(n, width):
    if width == 1:
        yield (n,)
        return
    for a in range(n + 1):
        for rest in compositions(n - a, width - 1):
            yield (a,) + rest


def main():
    root = Path(__file__).parent
    data = json.loads((root/'potential_menu_joint.json').read_text())
    types = [(t, F(v)) for t,v in data['positive_types']]
    scale = lcm(*(6*v.denominator for t,v in types))
    bits = []; weights = []; budget = F(0)
    for (mask,d,ell,h), mass in types:
        assert d == 1 and ((ell,h) in ((0,0),(1,1),(5,0),(6,1)))
        p = 0; tax = F(0)
        for i in range(6):
            if mask >> i & 1:
                tax += F(1,p+1)-F(1,p+6-i); p += 1
        budget += mass*(int(mask>0)+tax)
        for owner in range(6):
            reply = 0 if ell==0 else (1<<owner if ell==1 else (63^(1<<owner) if ell==5 else 63))
            bits.append([(mask>>i)&1 for i in range(6)]+[int(i==owner) for i in range(6)]+[(reply>>i)&1 for i in range(6)])
            weights.append(int(mass*scale/6))
    bits=np.array(bits,dtype=np.int16); weights=np.array(weights,dtype=np.int64)
    H=np.array([sum(60//j for j in range(1,k+1)) for k in range(7)],dtype=np.int64)
    maximum=-1; argmax=None; total=0; batch=[]
    def handle(batch):
        q=np.array(batch,dtype=np.int16); value=H[q@bits.T]@weights
        index=int(np.argmax(value))
        return int(value[index]), batch[index]
    for q in compositions(6,18):
        batch.append(q)
        if len(batch)==2048:
            v,a=handle(batch)
            if v>maximum: maximum,argmax=v,a
            total+=len(batch); batch=[]
    if batch:
        v,a=handle(batch)
        if v>maximum: maximum,argmax=v,a
        total+=len(batch)
    assert F(maximum,60*scale)==budget
    def payoff(counts, action):
        loads=bits@np.array(counts,dtype=np.int16)
        return sum((F(int(w),int(load)) for w,load,member in zip(weights,loads,bits[:,action]) if member),F(0))/scale
    actual=[1]*6+[0]*12
    actual_pay=[payoff(actual,i) for i in range(6)]
    actual_prefix=[1]*5+[0]*13
    prices=[]
    for k in range(18):
        q=actual_prefix.copy();q[k]+=1
        prices.append(actual_pay[5]-payoff(q,k))
    assert min(prices)>=0
    source_slacks=[]; reply_slacks=[]
    for i in range(6):
        q=[1]*4+[0]*14;q[6+i]+=1;q[12+i]+=1
        source_slacks.append(actual_pay[4]-payoff(q,6+i))
        for k in range(18):
            d=q.copy();d[12+i]-=1;d[k]+=1
            reply_slacks.append(payoff(q,12+i)-payoff(d,k))
    assert min(source_slacks)>=0 and min(reply_slacks)>=0
    # Exact supportability of every alternative at the actual penultimate node.
    supportability=[]
    for action in range(18):
        prefix=[1]*4+[0]*14;prefix[action]+=1
        candidates=[]
        for reply in range(18):
            q=prefix.copy();q[reply]+=1
            candidates.append((payoff(q,reply),payoff(q,action)))
        best=max(x for x,y in candidates)
        worst=min(y for x,y in candidates if x==best)
        supportability.append(actual_pay[4]-worst)
    report={'scope':'partial late-menu obstruction, not complete SPE','scale':scale,
            'unit_customer_count':int(sum(weights)),'customer_types':len(weights),
            'potential_multisets':total,'maximum_potential':str(F(maximum,60*scale)),
            'budget_W_plus_C':str(budget),'argmax':argmax,
            'actual_payoffs':list(map(str,actual_pay)),
            'actual_last_minimum_slack':str(min(prices)),
            'optimal_source_minimum_slack':str(min(source_slacks)),
            'reply_full_catalog_minimum_slack':str(min(reply_slacks)),
            'penultimate_all_alternatives_support_slack':list(map(str,supportability))}
    (root/'audit_potential_menu_joint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
