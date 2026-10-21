"""Definition-level unit-customer verification of a two-player auxiliary bridge failure.
No canonical solver, optimization result, compressed-payoff helper, or other audit imported.
"""
from fractions import Fraction
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

TOPICS=('A','B','T','S','E','F')
TYPES={1:4,2:5,4:3,8:3,20:2,24:2,36:2,40:2,49:2,50:2}
REPLY=(1,4,4,4,5,4)
ROOT=0
UNITS=[frozenset(a for a in range(6) if mask>>a&1) for mask,n in TYPES.items() for _ in range(n)]

def payoff(path,i):
    return sum((Fraction(1,sum(a in B for a in path)) for B in UNITS if path[i] in B),Fraction(0))
def covered(path):
    return frozenset(x for x,B in enumerate(UNITS) if any(a in B for a in path))

def main():
    rows=[]
    checks=[]
    for a in range(6):
        row=[payoff((a,b),1) for b in range(6)]
        checks.extend(row[REPLY[a]]-v for v in row)
        rows.append({'first':TOPICS[a],'second_payoffs':[str(v) for v in row], 'reply':TOPICS[REPLY[a]],'first_payoff':str(payoff((a,REPLY[a]),0))})
    root=[payoff((a,REPLY[a]),0) for a in range(6)]
    checks.extend(root[ROOT]-v for v in root)
    assert len(checks)==42 and min(checks)>=0
    actual=(ROOT,REPLY[ROOT]);C=covered(actual)
    pairs={TOPICS[a]+TOPICS[b]:len(covered((a,b))) for a,b in combinations_with_replacement(range(6),2)}
    optimum=max(pairs.values())
    comparison=(2,3);O=covered(comparison);R=O-C
    assert len(UNITS)==27
    assert actual==(0,1)
    assert [payoff(actual,i) for i in range(2)]==[Fraction(6),Fraction(7)]
    assert len(C)==13 and optimum==14 and len(O)==14 and len(R)==14 and not C&O
    report={'identity':'Auxiliary universal optimal-union residual budget failure; not Q-CAG-HALF or B4 failure','unit_customers':len(UNITS),'topics':TOPICS,'types':TYPES,'root':TOPICS[ROOT],'reply':dict(zip(TOPICS,(TOPICS[a] for a in REPLY))),'all_last_nodes':rows,'root_action_values':[str(v) for v in root],'checked_histories':7,'checked_deviations_including_self':len(checks),'minimum_slack':str(min(checks)),'actual_path':[TOPICS[a] for a in actual],'actual_payoffs':[str(payoff(actual,i)) for i in range(2)],'W':len(C),'all_pairs_including_repetitions':pairs,'OPT':optimum,'comparison':[TOPICS[a] for a in comparison],'optimal_comparison_union':len(O),'comparison_actual_intersection':len(C&O),'comparison_missed':len(R),'missed_minus_W':len(R)-len(C),'half_slack':2*len(C)-optimum,'B4_slacks':[str(2*payoff(actual,i)-(optimum-len(C))) for i in range(2)],'boundary':'Other optimal unions BT and BS have missed size 7; existential optimizer version is not refuted.'}
    path=Path(__file__).with_name('residual_counterexample_audit.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
