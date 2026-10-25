"""One exact b<a audit of the all-input pooled-successor theorem.

Checks a=2,b=1,q=2 (36 joint themes, 16 distinct unit clients).
No canonical model or solver imports. No random search or positive-range claim.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def main():
    a,b,q = 2,1,2
    dimensions = (3,3,2,2)
    sizes = (a,a,b,b)
    themes = tuple(product(*(range(n) for n in dimensions)))
    index = {theme:i for i,theme in enumerate(themes)}
    # Each tuple is one distinct unit client; no indivisible weighted customer.
    clients = tuple((dim,res,copy) for dim,n in enumerate(dimensions)
                    for res in range(n) for copy in range(sizes[dim]))
    p = len(themes)

    @lru_cache(None)
    def utility(terminal):
        values = [F(0),F(0),F(0)]
        for dim,res,_ in clients:
            owners = [i for i,act in enumerate(terminal) if themes[act][dim]==res]
            for i in owners:
                values[i] += F(1,len(owners))
        return tuple(values)

    def welfare(terminal):
        return sum(any(themes[act][dim]==res for act in terminal) for dim,res,_ in clients)

    def second_choice(first):
        x=themes[first]
        return index[(x[0],(x[1]+1)%3,1-x[2],1-x[3])]

    def last_choice(first,second):
        x,y=themes[first],themes[second]
        if second==second_choice(first):
            # One economic bad leaf, one economic good leaf; both insurers favorable.
            z=((x[0]+1)%3,(x[1]+2)%3,x[2],x[3])
        else:
            # Every coordinate resets, including coordinates whose action did not change.
            e=[]
            for dim in range(2):
                e.append(min(set(range(3))-{x[dim],y[dim]}))
            z=tuple(e)+(1-x[2] if y[2]==x[2] else y[2],
                        1-x[3] if y[3]==x[3] else y[3])
        return index[z]

    policy={():0}
    for first in range(p):
        policy[(first,)]=second_choice(first)
        for second in range(p):
            policy[(first,second)]=last_choice(first,second)

    def replay(h):
        while len(h)<3:
            h+=(policy[h],)
        return h

    comparisons=0
    minimum=None
    for depth in range(3):
        for h in product(range(p),repeat=depth):
            obey=replay(h)
            for forced in range(p):
                dev=replay(h+(forced,))
                gap=utility(obey)[depth]-utility(dev)[depth]
                assert gap>=0,(h,forced,gap)
                minimum=gap if minimum is None else min(minimum,gap)
                comparisons+=1

    # Independently rebuild the last-BR and second-role SPE outcome sets at every
    # ordered prefix, then min over every true child SPE for the first role.
    current_caps=[]
    ordered_prefixes=0
    leaf_checks=0
    for first in range(p):
        rows=[]
        for second in range(p):
            values=[utility((first,second,last))[2] for last in range(p)]
            best=max(values)
            br=tuple(last for last,v in enumerate(values) if v==best)
            floor=min(utility((first,second,last))[1] for last in br)
            rows.append((second,br,floor))
            ordered_prefixes+=1
            leaf_checks+=p
        theta=max(row[2] for row in rows)
        assert theta==5
        possible=[(first,second,last) for second,br,_ in rows for last in br
                  if utility((first,second,last))[1]>=theta]
        ell=min(utility(t)[0] for t in possible)
        assert ell==4
        actual=replay((first,))
        assert utility(actual)[0]==4 and utility(actual)[1]==5
        current_caps.append({"forced_first":first,"forced_theme":themes[first],
                             "ell":str(ell),"next_threshold":str(theta),
                             "constructed_terminal":actual,
                             "constructed_profits":list(map(str,utility(actual)))})

    target=(index[(0,0,0,0)],index[(0,0,0,0)],index[(1,1,1,1)])
    target_u=utility(target)
    optimum_witness=(index[(0,0,0,0)],index[(1,1,1,1)],index[(2,2,0,0)])
    optimum=welfare(optimum_witness)
    assert optimum==len(clients)==16
    assert utility(target)[2]==max(utility(target[:2]+(z,))[2] for z in range(p))
    target_w=welfare(target)
    g=(F(4)-target_u[0],F(5)-target_u[1])
    assert g==(1,2)
    repair=2*sum(g)+max(g)
    old_repair=F(5*q*a,2)
    assert old_repair-repair==q*min(a,b)==2
    report={
        "status":"PASS",
        "purpose":"Exact designated stress check of pooled all-forced M reduction, not a half witness",
        "parameters":{"a":a,"b":b,"q":q},"unit_clients":len(clients),"themes":p,
        "all_ordered_decision_histories":len(policy),
        "all_forced_IC_comparisons_including_own":comparisons,
        "own_comparisons":len(policy),"minimum_IC_gap":str(minimum),
        "ordered_two_action_prefixes_in_exact_BI":ordered_prefixes,
        "terminal_last_BR_evaluations":leaf_checks,
        "all_forced_first_caps":current_caps,
        "M_root_exact":"4","separate_barM_cap":"5","strict_M_saving":"1",
        "policy":[{"history":h,"action":v} for h,v in sorted(policy.items())],
        "target":{"ordered_topics":target,"profits":list(map(str,target_u)),
                  "W":target_w,"OPT":optimum,"B":2*target_w-optimum,
                  "true_g":list(map(str,g)),"old_repair_cost":str(old_repair),
                  "new_repair_cost":str(repair),"strict_repair_saving":str(old_repair-repair),
                  "B_plus_new_C":str(2*target_w-optimum+repair)},
        "scope":"m=3 numerical check only; all-m theorem is the analytic pooled construction, no universal position price or strict half seed."
    }
    destination=Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','unit_clients','themes','all_ordered_decision_histories',
          'all_forced_IC_comparisons_including_own','M_root_exact','separate_barM_cap','target')},indent=2))


if __name__=='__main__':
    main()
