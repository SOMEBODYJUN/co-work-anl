"""Blind independent PI-counterexample review from input + strategy only.

No author solver, payoff, audit, or cached numeric field is used.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'global/pi_fixed_cone_counterexample.json'


def main():
    packet=json.loads(SOURCE.read_text())
    instance=packet['instance']
    certificate=packet['strategy']
    # Deliberately do not read any other author numeric fields.
    n=len(instance['topics']);m=instance['players']
    assert (m,n)==(3,6)
    clients=[]
    for row in instance['customers']:
        assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
        likes=frozenset(row['topics'])
        assert likes and all(a in range(n) for a in likes)
        clients.extend([likes]*row['multiplicity'])
    covers=[frozenset(x for x,t in enumerate(clients) if a in t) for a in range(n)]
    assert len(set(covers))==n
    rows=certificate['actions']
    strategy={tuple(row['history']):row['action'] for row in rows}
    histories={h for depth in range(m) for h in product(range(n),repeat=depth)}
    assert len(rows)==len(strategy)==len(histories)==43
    assert set(strategy)==histories and all(a in range(n) for a in strategy.values())
    for h,a in strategy.items():
        if not h:
            expected=0
        elif len(h)==1:
            expected=3 if h[0]<3 else 0
        else:
            group=range(3) if h[-1]<3 else range(3,6)
            expected=min(a for a in group if a not in h)
        assert a==expected

    def follow(prefix):
        z=tuple(prefix)
        while len(z)<m:
            z+=(strategy[z],)
        return z

    def utility(z,who):
        return sum((F(1,sum(a in likes for a in z))
                    for likes in clients if z[who] in likes),F())

    gaps=[]
    for h in histories:
        obey=utility(follow(h),len(h))
        for a in range(n):
            gap=obey-utility(follow(h+(a,)),len(h))
            assert gap>=0
            gaps.append(gap)
    actual=follow(())
    utilities=[utility(actual,i) for i in range(m)]
    assert certificate['terminal_counts']==[actual.count(a) for a in range(n)]
    harmonic=[F()]
    for count in range(1,5):
        harmonic.append(harmonic[-1]+F(1,count))

    def potential(z):
        return sum((harmonic[sum(a in likes for a in z)] for likes in clients),F())

    def coverage(z):
        return sum(any(a in likes for a in z) for likes in clients)

    tables={}
    maxima={}
    maximizers={}
    for slots in (3,4):
        table=[]
        for z in combinations_with_replacement(range(n),slots):
            counts=tuple(z.count(a) for a in range(n))
            table.append(dict(counts=counts,potential=potential(z),coverage=coverage(z)))
        assert len(table)==(56 if slots==3 else 126)
        assert len({r['counts'] for r in table})==len(table)
        maximum=max(r['potential'] for r in table)
        tables[str(slots)]=table
        maxima[slots]=maximum
        maximizers[slots]=[r['counts'] for r in table if r['potential']==maximum]
    P3,P4=maxima[3],maxima[4]
    delta=P4-P3
    root=utilities[0]
    W=coverage(actual)
    optimum=max(r['coverage'] for r in tables['3'])
    assert sum(utilities,F())==W
    assert len(clients)==430
    assert actual==(0,3,4) and utilities==[F(91),F(91),F(83)]
    assert (P3,P4,delta,delta-root)==(F(329),F(873,2),F(215,2),F(33,2))
    assert W==265 and optimum==324
    assert potential(actual)==P3
    assert len(maximizers[3])==20 and all(max(q)<=1 for q in maximizers[3])
    assert maximizers[4]==[(0,1,1,0,1,1)]
    root_branches=[]
    for a in range(n):
        z=follow((a,))
        root_branches.append(dict(action=a,path=z,root_payoff=utility(z,0),potential=potential(z)))
    assert all(row['root_payoff']==root for row in root_branches)
    caps=[sum((F(1,1+sum(b in likes for b in actual))
               for likes in clients if a in likes),F()) for a in range(n)]
    assert max(caps)==80<root
    root_K=[[sum((F(1,1+sum(c in likes for c in follow((b,))))
                  for likes in clients if a in likes),F())
             for b in range(n)] for a in range(n)]
    assert max(map(max,root_K))==90<root
    report=dict(reviewer='mixed_menus, R-cd789330fc7141299ac491bbb3ffa420; parent-assigned independent review',
                status='PASS: PI auxiliary benchmark counterexample independently verified.',
                input_scope='Only instance and strategy fields read; author cached metrics/solver/payoff/audit unused.',
                source=str(SOURCE.relative_to(HERE.parents[5])),
                unit_customers=len(clients),players=m,topics=n,
                distinct_topic_sizes=[len(s) for s in covers],
                ordered_decision_histories=len(histories),deviation_comparisons=len(gaps),
                minimum_spe_slack=min(gaps),actual_path=actual,actual_payoffs=utilities,
                actual_welfare=W,optimum_3=optimum,half_slack=2*W-optimum,
                actual_potential=potential(actual),P3=P3,P4=P4,
                potential_increment=delta,potential_increment_minus_root=delta-root,
                P3_maximizers=maximizers[3],P4_maximizers=maximizers[4],
                root_branches=root_branches,actual_terminal_extra_query_caps=caps,
                complete_root_insertion_matrix=root_K,maximum_root_insertion_entry=max(map(max,root_K)),
                potential_tables=tables,
                mathematical_scope='Refutes PI root >= P_(r+1)-P_r only. Does not refute WP, EI, Mfull, aggregate security, or Q-CAG-HALF.')
    text=json.dumps(report,default=str,ensure_ascii=False,indent=2)+'\n'
    (HERE/'pi_review_audit.json').write_text(text)
    print(json.dumps({k:v for k,v in report.items() if k!='potential_tables'},default=str,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
