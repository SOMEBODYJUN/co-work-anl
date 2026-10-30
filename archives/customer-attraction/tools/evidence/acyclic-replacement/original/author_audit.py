"""Definition-level replay of the acyclic four-query witness; no solver or LP."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'


def main():
    data=json.loads(SOURCE.read_text());p=len(data['instance']['topics']);m=data['instance']['players']
    actions={tuple(v['history']):v['action'] for v in data['certificate']['actions']}
    assert set(actions)=={h for k in range(m) for h in product(range(p),repeat=k)}
    customers=[(frozenset(v['topics']),v['multiplicity']) for v in data['instance']['customers']]
    def terminal(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    def payoff(a,z,interest):
        return F(1,sum(t in interest for t in z)) if a in interest else F(0)
    def utility(a,z):
        return sum((n*payoff(a,z,t) for t,n in customers),F(0))
    comparisons=0
    for h,a in actions.items():
        actual=utility(a,terminal(h))
        for b in range(p):
            assert utility(b,terminal(h+(b,)))<=actual
            comparisons+=1
    z=terminal(());q=tuple(z.count(a) for a in range(p))
    assert z==(3,3,2,2)
    target=(0,1,4,5);assigned=(2,2,3,3);histories=((3,3),(3,3),(),())
    assert tuple(assigned.count(a) for a in range(p))==q
    branches=[];earlier=[0]*p
    for t,a,h in zip(target,assigned,histories):
        assert h==z[:len(h)] and actions[h]==a
        branch=terminal(h+(t,));counts=tuple(branch.count(b) for b in range(p))
        upper=tuple(q[b]-int(b==a)+int(b==t)+earlier[b] for b in range(p))
        assert all(x<=y for x,y in zip(counts,upper))
        branches.append(branch);earlier[t]+=1
    def charges(interest):
        c=sum(a in interest for a in z)
        owners=[j for j,t in enumerate(target) if t in interest]
        if not owners:return F(0),F(0),F(0),F(int(c>0))
        frozen=[F(1,c+1-int(assigned[j] in interest)) for j in owners]
        first=frozen[0];minimum=min(frozen)
        real=sum((payoff(t,b,interest) for t,b in zip(target,branches)),F(0))
        actual=sum((payoff(a,z,interest) for a in assigned),F(0))
        assert minimum<=first<=real
        assert actual==int(c>0)
        return minimum,first,real,actual
    coefficients=[]
    for mask in range(1,1<<p):
        interest=frozenset(a for a in range(p) if mask>>a&1)
        minimum,first,real,actual=charges(interest)
        coefficients.append({'mask':mask,'R_min':str(minimum),'R_first':str(first),
                             'real_queries':str(real),'payment_residual':str(real-first)})
    totals=[sum((n*charges(t)[i] for t,n in customers),F(0)) for i in range(4)]
    assert totals[2]<=totals[3]
    report={'status':'exact_definition_level_replay_passed',
            'all_ordered_histories':len(actions),'all_comparisons_including_self':comparisons,
            'actual':z,'comparison_order':target,'assigned_actual_topics':assigned,
            'histories':histories,'branches':branches,
            'source_R_min':str(totals[0]),'source_R_first':str(totals[1]),
            'source_real_query_sum':str(totals[2]),'source_W':str(totals[3]),
            'all_interest_type_coefficients':coefficients}
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='all_interest_type_coefficients'},indent=2))

if __name__=='__main__':main()
