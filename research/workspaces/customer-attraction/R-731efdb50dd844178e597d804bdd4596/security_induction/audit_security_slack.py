"""Definition-level Fraction audit; no solver, LP, or scientific dependencies.

Finite checks supplement, and do not replace, the all-n proofs in the note.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def histories(q,r):
    return list(combinations_with_replacement(range(q),r))


def audit(n,topics,weights,optimal,Q,primal,v,sharp=False):
    q=len(topics)
    clients=list(weights)
    assert sum(Q.values())==1 and len(primal)==q and sum(primal)==1
    assert all(len(B)==n-1 and probability>0 for B,probability in Q.items())
    backgrounds=histories(q,n-1)
    def load(B,x):return sum(x in topics[a] for a in B)
    def f(B,a):return sum((weights[x]/(1+load(B,x)) for x in topics[a]),F(0))
    def welfare(T):return sum((weights[x] for x in set().union(*(topics[a] for a in T))),F(0))
    O=max(map(welfare,histories(q,n)))
    assert welfare(optimal)==O
    values={B:tuple(f(B,a) for a in range(q)) for B in backgrounds}
    assert min(sum(primal[a]*values[B][a] for a in range(q)) for B in backgrounds)==v
    query=[sum(probability*values[B][a] for B,probability in Q.items()) for a in range(q)]
    assert max(query)==v
    C=set().union(*(topics[a] for a in optimal))
    d={x:sum(x in topics[a] for a in optimal) for x in clients}
    L={x:sum(probability*load(B,x) for B,probability in Q.items()) for x in clients}
    marginal=[sum(probability*B.count(a) for B,probability in Q.items())/F(n-1) if n>1 else F(a==0)
              for a in range(q)]
    g=[sum((weights[x]/(1+L[x]) for x in topics[a]),F(0)) for a in range(q)]
    j={x:sum(probability*(load(B,x)-L[x])**2/((1+L[x])**2*(1+load(B,x)))
             for B,probability in Q.items()) for x in clients}
    J=[sum((weights[x]*j[x] for x in topics[a]),F(0)) for a in range(q)]
    delta=[v-query[a] for a in range(q)]
    assert all(value>=0 for value in delta+J)
    assert all(query[a]-g[a]==J[a] for a in range(q))
    Rov=sum((weights[x]*(d[x]-1)/(1+L[x]) for x in C),F(0))
    Rout=sum((weights[x]*L[x]/(1+L[x]) for x in clients if x not in C),F(0))
    Delta=(2*n-1)*v-O
    rhs=Rov+Rout+sum(delta[a]+J[a] for a in optimal)+(n-1)*sum(marginal[a]*(delta[a]+J[a]) for a in range(q))
    assert Delta==rhs
    JC=sum((weights[x]*j[x] for x in C),F(0))
    FC=sum((probability*sum((weights[x]/(1+load(B,x)) for x in C),F(0))
            for B,probability in Q.items()),F(0))
    assert JC+Rout<=Delta and FC<=n*v
    caps={B:max(values[B]) for B in backgrounds}
    # Squared rational check of E cap <= v+Rout+(JC+sqrt(JC FC))/2.
    excess=sum(probability*caps[B] for B,probability in Q.items())-v-Rout-JC/2
    assert excess<=0 or 4*excess**2<=JC*FC
    theta=min(caps.values())
    excess=theta-v-Delta
    assert excess<=0 or 4*excess**2<=n*v*Delta
    sharp_comparisons=0
    if sharp:
        assert Delta==0
        assert all(d[x]==1 for x in C)
        assert all(load(B,x)==L[x] for B in Q for x in clients)
        canonical=[(optimal.count(a)+(n-1)*marginal[a])/F(2*n-1) for a in range(q)]
        for B in backgrounds:
            pay=sum(canonical[a]*values[B][a] for a in range(q))
            exact=sum(v-g[a] for a in B)
            exact+=sum((weights[x]*load(B,x) for x in clients if x not in C),F(0))
            exact+=sum((weights[x]*(load(B,x)-L[x])**2/((1+L[x])*(1+load(B,x)))
                        for x in C),F(0))
            assert pay-v==exact/F(2*n-1)
            assert (pay==v)==all(load(B,x)==L[x] for x in clients)
            # Every pure optimal dual background has the same load.
            if caps[B]==v:
                assert all(load(B,x)==L[x] for x in clients)
            sharp_comparisons+=1
    return dict(n=n,q=q,O=str(O),v=str(v),Delta=str(Delta),theta=str(theta),
                backgrounds=len(backgrounds),sharp_identity_checks=sharp_comparisons)


def main():
    reports=[]
    # All-n sharp family: one n-client theme and n-1 disjoint singleton themes.
    for n in range(1,8):
        topics=[set(range(n))]+[{n+a} for a in range(n-1)]
        weights={x:F(1) for T in topics for x in T}
        Q={(0,)*(n-1):F(1)}
        primal=[F(n,2*n-1)]+[F(1,2*n-1)]*(n-1)
        reports.append(audit(n,topics,weights,tuple(range(n)),Q,primal,F(1),True))
    # Sharp, crossing catalog; two different background topic counts, identical loads.
    # The sixth client lies outside the selected optimal union.
    topics=[{0,2},{1,3},{4},{0,1},{2,3},{5}]
    weights={x:F(1) for x in range(6)}
    Q={(0,1):F(1,2),(3,4):F(1,2)}
    reports.append(audit(3,topics,weights,(0,1,2),Q,[F(1,5)]*5+[F(0)],F(1),True))
    # Genuine mixed minimax Q with customer-load variation; includes nonzero Rout.
    for q in [2,3,4]:
        topics=[{a} for a in range(q)]
        weights={x:F(1) for x in range(q)}
        Q={(a,):F(1,q) for a in range(q)}
        reports.append(audit(2,topics,weights,(0,1),Q,[F(1,q)]*q,F(2*q-1,2*q)))
    # Zero value / empty optimal comparison set, with multiple labels.
    reports.append(audit(3,[set(),set()],{},(0,0,0),{(0,1):F(1)},[F(1),F(0)],F(0),True))
    # Pure scalar tangent identity at every small finite load distribution.
    scalar_checks=0
    for n in range(1,8):
        for h1,h2 in product(range(n),repeat=2):
            for probability in [F(0),F(1,5),F(1,2),F(4,5),F(1)]:
                L=probability*h1+(1-probability)*h2
                J=probability/F(1+h1)+(1-probability)/F(1+h2)-1/(1+L)
                exact=probability*(h1-L)**2/((1+L)**2*(1+h1))
                exact+=(1-probability)*(h2-L)**2/((1+L)**2*(1+h2))
                assert J==exact and J>=0
                scalar_checks+=1
    report=dict(status='all finite exact checks passed; universal claims use the analytic proof',
                cases=reports,scalar_tangent_checks=scalar_checks,
                full_background_checks=sum(r['backgrounds'] for r in reports),
                sharp_identity_checks=sum(r['sharp_identity_checks'] for r in reports))
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':
    report=main()
    import sys
    if '--output' in sys.argv:
        output=Path(sys.argv[sys.argv.index('--output')+1])
        with output.open('x') as stream:json.dump(report,stream,indent=2);stream.write('\n')
