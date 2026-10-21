"""Definition-level exact check of a two-player protected-budget obstruction.

No LP, no discovery code, no package solver imports. All groups expand to
distinct unit clients; all first actions and all second actions are checked.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def audit():
    labels = ['A','B','T','Q','R','S']
    groups = [(['A'],4), (['B'],5), (['T'],3), (['Q'],3),
              (['T','R'],2), (['Q','R'],2), (['T','S'],2),
              (['Q','S'],2), (['A','R','S'],2), (['B','R','S'],2)]
    clients=[]
    for memberships,count in groups:
        clients.extend([frozenset(memberships) for _ in range(count)])
    topics={a:frozenset(i for i,v in enumerate(clients) if a in v) for a in labels}
    reply=dict(zip(labels,['B','R','R','R','S','R']))
    def payoff(a,b):
        return sum((F(1,1+int(x in topics[b])) for x in topics[a]),F(0))
    matrix={a:{b:payoff(b,a) for b in labels} for a in labels}
    leaf_slacks={a:{b:matrix[a][reply[a]]-matrix[a][b] for b in labels} for a in labels}
    first={a:payoff(a,reply[a]) for a in labels}
    first_slacks={a:first['A']-first[a] for a in labels}
    assert all(v>=0 for row in leaf_slacks.values() for v in row.values())
    assert all(v>=0 for v in first_slacks.values())
    actual=topics['A']|topics['B'];D=topics['T']|topics['Q']
    optimum=max(len(topics[a]|topics[b]) for a,b in itertools.product(labels,repeat=2))
    opt_pairs=[(a,b) for a,b in itertools.combinations_with_replacement(labels,2)
               if len(topics[a]|topics[b])==optimum]
    assert len(actual)==13 and len(D)==14 and not actual&D and optimum==14
    # Every theme hits at most seven protected clients. Thus coverage of any
    # nonnegative query vector of mass tau is <=min(7*tau,14); minus 6*tau <=2.
    # T,Q each at unit weight attain 2. This is an exact continuous LP proof.
    protected_sizes={a:len(topics[a]&D) for a in labels}
    assert max(protected_sizes.values())==7
    price=F(2);assert len(D)-2*first['A']==price and price>payoff('B','A')-first['A']
    return {'clients':len(clients),'labels':labels,'groups':groups,'reply':reply,
            'second_payoff_matrix':matrix,'first_deviation_payoffs':first,
            'min_second_slack':min(v for row in leaf_slacks.values() for v in row.values()),
            'min_first_slack':min(first_slacks.values()),'checked_nodes':7,
            'checked_including_self_comparisons':42,'actual_payoffs':[first['A'],payoff('B','A')],
            'W':len(actual),'D':len(D),'OPT_2':optimum,'optimal_unordered_pairs':opt_pairs,
            'protected_sizes':protected_sizes,'B_D_6':price,
            'assertions_passed':True}


if __name__=='__main__':
    data=audit();blob=json.dumps(data,ensure_ascii=False,indent=2,default=str)+'\n'
    Path(__file__).with_name('protected_root_audit.json').write_text(blob)
    print(blob)
