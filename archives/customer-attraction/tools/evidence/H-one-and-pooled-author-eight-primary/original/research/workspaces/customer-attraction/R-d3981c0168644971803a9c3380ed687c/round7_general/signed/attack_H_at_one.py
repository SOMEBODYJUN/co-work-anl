"""Designated exact attack on H_h(1)>=0, with complete ordered-history BI.

Inputs are the named old34, old23 core, already reviewed old31, and one explicitly
designated multilevel reuse of the read 3-resource x 2-bank construction.
No random scan and no inference of a general positive result.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[6]


def examine(obj):
    p=len(obj['topics']);m=obj['players']
    clients=tuple(frozenset(row['topics']) for row in obj['customers']
                  for _ in range(row['multiplicity']))
    actions=tuple(range(p))
    @lru_cache(None)
    def payoff(t):
        values=[F(0)]*m
        for client in clients:
            owners=[i for i,a in enumerate(t) if a in client]
            for i in owners: values[i]+=F(1,len(owners))
        return tuple(values)
    floors={};outcomes={}
    def BI(h):
        if len(h)==m:
            r=frozenset({h})
        else:
            i=len(h)
            children={a:BI(h+(a,)) for a in actions}
            floor=max(min(payoff(t)[i] for t in children[a]) for a in actions)
            floors[h]=floor
            r=frozenset(t for a in actions for t in children[a] if payoff(t)[i]>=floor)
        outcomes[h]=r
        return r
    BI(())
    records=[]
    for depth in range(m-1):
        for h in product(actions,repeat=depth):
            i=len(h);rows=[]
            for a in actions:
                theta=floors[h+(a,)]
                candidates=[(payoff(t)[i]-payoff(t)[i+1]+theta,b,t)
                            for b in actions for t in outcomes[h+(a,b)]]
                value,b,t=min(candidates)
                rows.append({'A':a,'theta':str(theta),'minimum':str(value),
                             'argmin_B':b,'witness_terminal':t,
                             'd':str(payoff(t)[i]),'v':str(payoff(t)[i+1]),
                             'complete_grandchild_outcomes':len(outcomes[h+(a,b)])})
            H=max(F(row['minimum']) for row in rows)
            records.append({'prefix':h,'remaining':m-len(h),'H_at_1':str(H),
                            'all_current_action_rows':rows})
    minimum=min(records,key=lambda row:F(row['H_at_1']))
    return {'unit_clients':len(clients),'players':m,'topics':obj['topics'],
            'ordered_tree_states':len(outcomes),'examined_prefixes':len(records),
            'minimum_H_at_1':minimum,'negative_prefixes':[r for r in records if F(r['H_at_1'])<0],
            'all_prefixes':records,
            'scope':'Designated exact attack on H(1)>=0 only; no all-input inference.'}


def main():
    old34=json.loads((ROOT/'examples/customer_attraction/individual_security_failure.json').read_text())
    types=[({0},3),({1},4),({2,3},6),({2,4},6),({0,3,4},2),({1,3,4},2)]
    old23={'topics':list(map(str,range(5))),'players':3,
           'customers':[{'topics':sorted(s),'multiplicity':n} for s,n in types]}
    old31=json.loads((Path(__file__).parent.parent.parent/'round6_general/credible/true_reset_floor_counterexample.json').read_text())['instance']
    themes=[(i,j) for i in range(3) for j in range(2)]
    multitypes=[{'topics':[k for k,(x,y) in enumerate(themes) if x==i],
                 'multiplicity':3} for i in range(3)]
    multitypes += [{'topics':[k for k,(x,y) in enumerate(themes) if y==j],
                    'multiplicity':1} for j in range(2)]
    multilevel={'topics':list(map(str,themes)),'players':4,'customers':multitypes}
    report={name:examine(obj) for name,obj in [('old34',old34),('old23',old23),
                                             ('old31',old31),('read_product_a3_b1_m4',multilevel)]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({name:{'min_H':r['minimum_H_at_1']['H_at_1'],
                            'prefix':r['minimum_H_at_1']['prefix'],
                            'negative_count':len(r['negative_prefixes']),
                            'root_H':r['all_prefixes'][0]['H_at_1']}
                      for name,r in report.items()},indent=2))


if __name__=='__main__':main()
