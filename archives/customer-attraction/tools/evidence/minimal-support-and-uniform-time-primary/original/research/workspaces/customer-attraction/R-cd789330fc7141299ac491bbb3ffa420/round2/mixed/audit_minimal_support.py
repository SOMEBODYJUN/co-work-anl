"""Exact kernel for minimal-support weak-push conditions; no search."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[5]
SOURCE=REPO/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json'


def pair_extremum(alpha,beta,s,u):
    denominator=2*s-alpha-beta
    assert denominator>0
    p=(s-beta)/denominator
    assert 0<p<1
    value=(s*s-alpha*beta)/denominator
    direct=alpha*p*p+2*s*p*(1-p)+beta*(1-p)*(1-p)
    determinant=(u-alpha)*(u-beta)-(u-s)**2
    assert direct==value
    assert value-u==-determinant/denominator
    criterion=s>u and (s-u)**2>(u-alpha)*(u-beta)
    assert criterion==(value>u)
    return dict(alpha=alpha,beta=beta,cross_average=s,root_utility=u,
                probability_A=p,maximum=value,maximum_minus_root=value-u,
                gap_matrix_determinant=determinant,unsafe_pair=criterion)


def main():
    packet=json.loads(SOURCE.read_text())
    instance=packet['instance']
    n=len(instance['topics']);m=instance['players']
    assert (n,m)==(6,3)
    clients=[]
    for row in instance['customers']:
        clients.extend([frozenset(row['topics'])]*row['multiplicity'])
    assert len(clients)==348
    rows=packet['certificate']['actions']
    strategy={tuple(row['history']):row['action'] for row in rows}
    histories={h for depth in range(m) for h in product(range(n),repeat=depth)}
    assert len(rows)==len(strategy)==len(histories)==43
    assert set(strategy)==histories

    def follow(h):
        h=tuple(h)
        while len(h)<m:
            h+=(strategy[h],)
        return h

    def utility(z,who):
        return sum((F(1,sum(a in likes for a in z))
                    for likes in clients if z[who] in likes),F())

    comparisons=0
    for h in histories:
        obey=utility(follow(h),len(h))
        for a in range(n):
            assert obey>=utility(follow(h+(a,)),len(h))
            comparisons+=1
    actual=follow(())
    u=utility(actual,0)
    assert u==F(147,2)
    branches=[follow((a,)) for a in range(n)]
    d=[utility(z,0) for z in branches]
    assert d==[u]*n
    K=[[sum((F(1,1+sum(b in likes for b in z))
             for likes in clients if a in likes),F())
        for z in branches] for a in range(n)]
    assert K==[[F(v) for v in row] for row in packet['K']]
    taxes=[]
    for a,z in enumerate(branches):
        tax=sum((F(1,sum(b in likes for b in z)*(1+sum(b in likes for b in z)))
                 for likes in clients if a in likes),F())
        assert K[a][a]==d[a]-tax
        taxes.append(tax)
    a,b=2,5
    s=(K[a][b]+K[b][a])/2
    pair=pair_extremum(K[a][a],K[b][b],s,u)
    assert pair['maximum']==F(737,12)
    assert pair['gap_matrix_determinant']==F(31465,36)
    assert not pair['unsafe_pair']

    abstract=[]
    for k in range(2,9):
        # G=(k-1/2)I-11^T. This is abstract algebra, never a CAG claim.
        coefficient=F(2*k-1,2)
        G=[[coefficient*(i==j)-1 for j in range(k)] for i in range(k)]
        p=[F(1,k)]*k
        delta=F(1,2*k)
        assert all(sum((G[i][j]*p[j] for j in range(k)),F())==-delta for i in range(k))
        assert all(sum((G[i][j]*(-2) for j in range(k)),F())==1 for i in range(k))
        assert delta==-1/F(-2*k)
        assert all(G[i][i]>0 for i in range(k))
        for size in range(1,k):
            # Every proper face has min q^TGq=coefficient/size-1>0.
            assert coefficient/size-1>0
        abstract.append(dict(support=k,gap=delta,inverse_times_one=[-2]*k,
                             proper_face_minimum=coefficient/(k-1)-1))
    extra_pairs=[pair_extremum(F(3,2),F(3,2),F(3),F(2)),
                 pair_extremum(F(7,10),F(1,2),F(7,5),F(1)),
                 pair_extremum(F(1,3),F(1,2),F(3,4),F(1))]
    report=dict(status='Exact identity/complete-strategy audit passed; no general child-IC bridge claimed.',
                source=str(SOURCE.relative_to(REPO)),
                players=m,topics=n,unit_customers=len(clients),
                ordered_histories=len(histories),deviation_comparisons=comparisons,
                query_matrix_entries=n*n,actual=actual,root_utility=u,
                diagonal_insertion_taxes=taxes,existing_high_cycle_pair=pair,
                abstract_matrix_identity_checks=abstract,
                abstract_pair_formula_checks=extra_pairs,
                scope='The abstract matrices are not claimed to be CAG-realizable; the 348-client game is reused, not a new counterexample.')
    text=json.dumps(report,default=str,ensure_ascii=False,indent=2)+'\n'
    (HERE/'minimal_support_audit.json').write_text(text)
    print(json.dumps({k:v for k,v in report.items() if not k.startswith('abstract')},default=str,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
