"""Independent Fraction replay of the reply-cap interface and failed lifts."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import argparse
import json

ROOT=Path(__file__).resolve().parents[6]


def replay(name):
    raw=json.loads((ROOT/'examples'/'customer_attraction'/f'{name}.json').read_text())
    p=len(raw['topics']);m=raw['players']
    customers=[frozenset(c['topics']) for c in raw['customers'] for _ in range(c['multiplicity'])]
    def utility(a,h):return sum((F(1,sum(b in B for b in h)) for B in customers if a in B),F(0))
    def chosen(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        group=range(3) if h[-1]<3 else range(3,6)
        return next(a for a in group if a not in h)
    def terminal(h):
        while len(h)<m:h=h+(chosen(h),)
        return h
    comparisons=0
    for depth in range(m):
        for h in product(range(p),repeat=depth):
            a=chosen(h);actual=terminal(h);u=utility(a,actual)
            for b in range(p):
                assert u>=utility(b,terminal(h+(b,)))
                comparisons+=1
    caprows=0;minimum=None;local=[]
    for h in product(range(p),repeat=m-2):
        f=lambda a:sum((F(1,1+sum(b in B for b in h)) for B in customers if a in B),F(0))
        g=lambda a,b:sum((F(1,(1+sum(c in B for c in h))*(2+sum(c in B for c in h))) for B in customers if a in B and b in B),F(0))
        maximum=max(f(a) for a in range(p));a=chosen(h);u=utility(a,terminal(h))
        for T in range(p):
            for S in range(T,p):
                slack=u+maximum-f(T)-f(S)+g(T,S)
                assert slack>=0
                minimum=slack if minimum is None else min(minimum,slack)
                caprows+=1
        local.append({'prefix':h,'leader':str(u),'max_f':str(maximum)})
    harmonics=[F(0)]
    for k in range(1,m+1):harmonics.append(harmonics[-1]+F(1,k))
    def phi(h):return sum((harmonics[sum(a in B for a in h)] for B in customers),F(0))
    P=[max(phi(h) for h in combinations_with_replacement(range(p),k)) for k in range(m+1)]
    actual=terminal(());profits=[utility(a,actual) for a in actual];W=sum(profits)
    return {'source':name,'unit_clients':len(customers),'histories':sum(p**k for k in range(m)),'SPE_comparisons':comparisons,'root_path':actual,'root_payoffs':list(map(str,profits)),'W':str(W),'P_k':list(map(str,P)),'delta_P':str(P[-1]-P[-2]),'root_minus_delta':str(profits[0]-(P[-1]-P[-2])),'W_minus_m_delta':str(W-m*(P[-1]-P[-2])),'reply_cap_rows':caprows,'minimum_reply_cap_slack':str(minimum),'local_nodes':local}


def family(m):
    X=4*(m-1)**3;Y=2*m*(m-1)*(m-3);Z=m*(m-3)*(m*m-3*m+4);eps=4*(m-3)
    f=[F(X+Y+Z,m-1),F(X+Z,m-1)+Y,F(Y+Z,m-1)+X,F(X+Y+eps)]
    assert f[3]==max(f)
    p=F(X,m-1)+Y+F(Z,m)
    best_response_lower=f[2]-F(X,2)
    gap=best_response_lower-p
    assert gap==F((m-3)*(m*m-m+2),m-1)
    assert gap>0 if m>=4 else gap==0
    return {'m':m,'gap':str(gap)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    report={'scope':'Exact audit of valid two-remaining reply cap and known-counterexample-derived failures of its individual/aggregate harmonic-potential lifts; no new Q-CAG-HALF counterexample.',
            'instances':[replay('individual_security_failure'),replay('aggregate_theta_failure')],
            'sharp_projection_family':[family(m) for m in range(3,101)]}
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
