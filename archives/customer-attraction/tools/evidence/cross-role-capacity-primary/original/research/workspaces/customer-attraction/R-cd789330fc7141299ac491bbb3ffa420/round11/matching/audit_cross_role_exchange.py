"""Exact implementation audit of COPY/GATE on two existing certificates.

General validity is proved in cross_role_optimal_exchange.md. This script
checks the formulas and joint optimal selection, not a new welfare bound.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations
import importlib.util, json

HERE = Path(__file__).resolve().parent
source = HERE.parents[1] / 'round8/matching/audit_terminal_wallet.py'
spec = importlib.util.spec_from_file_location('existing_certificate_loaders', source)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def audit(loader):
    instance, policy, sources = loader()
    m, p = instance['players'], len(instance['topics'])
    clients = [(frozenset(row['topics']), row['multiplicity'])
               for row in instance['customers']]
    B=()
    while len(B)<m:
        B+=(policy[B],)
    c=[sum(a in interest for a in B) for interest,_ in clients]
    def union_profile(profile):
        return frozenset(x for x,(interest,_) in enumerate(clients)
                         if any(a in interest for a in profile))
    def mass(group):
        return sum(clients[x][1] for x in group)
    def f(i,a):
        return sum((F(n,load+1-(B[i] in interest))
                    for (interest,n),load in zip(clients,c) if a in interest), F(0))
    u=[f(i,B[i]) for i in range(m)]
    R=[[sum((F(n,load*(load+1))
             for (interest,n),load in zip(clients,c)
             if B[j] in interest and B[i] not in interest),F(0))
        for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            assert f(i,B[j])==u[j]-R[i][j]
    tuples=list(combinations_with_replacement(range(p),m))
    OPT=max(mass(union_profile(t)) for t in tuples)
    optimal=[t for t in tuples if mass(union_profile(t))==OPT]
    Q,T=min((sum((f(i,t[i]) for i in range(m)),F(0)),t)
            for multiset in optimal for t in set(permutations(multiset)))
    O=union_profile(T)
    zero=0
    checked=0
    minimum_delta=None
    max_zero_excess=None
    positive_excess=[]
    for size in range(m+1):
        for I in combinations(range(m),size):
            noI=union_profile([T[i] for i in range(m) if i not in I])
            for J in combinations(range(m),size):
                A=union_profile([B[j] for j in J])
                delta=mass((O-noI)-A)-mass(A-O)
                assert delta>=0
                refund=max((sum((R[i][j] for i,j in zip(I,rho)),F(0))
                            for rho in permutations(J)),default=F(0))
                excess=sum((f(i,T[i]) for i in I),F(0))-sum((u[j] for j in J),F(0))+refund
                if delta==0:
                    assert excess<=0
                    zero+=1
                    max_zero_excess=excess if max_zero_excess is None else max(max_zero_excess,excess)
                if excess>0:
                    assert delta>0
                    positive_excess.append((I,J,str(excess),delta))
                checked+=1
                minimum_delta=delta if minimum_delta is None else min(minimum_delta,delta)
    return dict(sources=sources,m=m,p=p,actual=list(B),actual_u=list(map(str,u)),
                W=str(sum(u,F(0))),OPT=OPT,optimal_multisets=len(optimal),
                joint_min_assignment=list(T),Q=str(Q),copy_identities=m*m,
                cross_role_block_pairs=checked,zero_net_loss_gates=zero,
                maximal_zero_loss_excess=str(max_zero_excess),
                positive_excess_blocks=len(positive_excess),
                examples_positive_loss=positive_excess[:6],all_checks=True)


if __name__=='__main__':
    report=dict(status='exact existing-certificate formula QA only',
                general_half='OPEN',weak_assignment='OPEN',
                cases=dict(old52=audit(old.load_old52),old1953=audit(old.load_new1953)))
    (HERE/'cross_role_exchange_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
