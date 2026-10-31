"""Definition-level identity audit on one existing complete SPE certificate.

No query optimization, strategy-cone scan, or general candidate verification.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

REPO=Path(__file__).resolve().parents[6]
SOURCE=REPO/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/phi_rise_exact.json'


def main():
    data=json.loads(SOURCE.read_text())
    n=len(data['topics'])
    clients=[]
    for mask,number in data['integer_types'].items():
        likes=frozenset(a for a in range(n) if int(mask)&(1<<a))
        clients.extend([likes]*number)
    strategy={tuple(row['history']):row['action'] for row in data['actions']}
    m=3

    def path(history):
        h=tuple(history)
        while len(h)<m:
            h+=(strategy[h],)
        return h

    def payoff(z,who):
        return sum((F(1,sum(a in likes for a in z))
                    for likes in clients if z[who] in likes),F())

    actual=path(())
    u=[payoff(actual,i) for i in range(m)]
    W=sum(u,F())
    comparisons=0
    for i in range(m):
        for h in product(range(n),repeat=i):
            obey=payoff(path(h),i)
            for a in range(n):
                assert obey>=payoff(path(h+(a,)),i)
                comparisons+=1

    weights=(1,2,3,5,7,11,13)
    p=tuple(F(w,sum(weights)) for w in weights)
    assert n==len(p)
    positions=[]
    for i in range(m):
        branches=[path(actual[:i]+(a,)) for a in range(n)]
        d=[payoff(z,i) for z in branches]
        assert max(d)==u[i]
        K=[[sum((F(1,1+sum(a in likes for a in z))
                 for likes in clients if t in likes),F())
            for z in branches] for t in range(n)]
        costs=[sum((p[t]*K[t][a] for t in range(n)),F()) for a in range(n)]
        psi=min(costs)
        C=sum((p[a]*costs[a] for a in range(n)),F())
        D=sum((p[a]*d[a] for a in range(n)),F())
        e=u[i]-D
        L=C-psi
        assert e>=0 and L>=0
        covariance=F()
        tax=F()
        for likes in clients:
            t=sum((p[a] for a in likes),F())
            ev=eiv=etax=F()
            for a,z in enumerate(branches):
                count=sum(b in likes for b in z)
                v=F(1,count+1)
                ev+=p[a]*v
                if a in likes:
                    assert count>=1
                    eiv+=p[a]*v
                    etax+=p[a]*F(1,count*(count+1))
            covariance+=eiv-t*ev
            tax+=etax
        assert D-C==covariance+tax
        assert psi-u[i]==C-D-e-L
        if i>=m-2:
            assert psi<=u[i]
        positions.append(dict(index=i+1,psi=psi,C=C,D=D,
                              actual_utility=u[i],root_slack=e,
                              free_column_gain=L,covariance=covariance,
                              insertion_tax=tax,identity_residual=D-C-covariance-tax))
    assert sum((r['psi'] for r in positions),F())-W==sum((r['C']-r['D']-r['root_slack']-r['free_column_gain'] for r in positions),F())
    report=dict(status='Definition-level identity audit passed on one existing full SPE. No general menu inference.',
                source=str(SOURCE.relative_to(REPO)),players=m,topics=n,
                unit_customers=len(clients),decision_histories=len(strategy),
                deviation_comparisons=comparisons,actual=actual,welfare=W,
                query=p,positions=positions,
                aggregate_identity_residual=F(),
                scope='Verifies the exact debt decomposition and complete SPE only; no query search, no fixed-cone scan, no evidence for universal uniform time.')
    text=json.dumps(report,default=str,ensure_ascii=False,indent=2)+'\n'
    Path(__file__).with_name('uniform_debt_audit.json').write_text(text)
    print(text)


if __name__=='__main__':
    main()
