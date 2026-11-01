"""Independent unit expansion, full-history SPE check, and exact optimizer check.
This is a finite audit of the separately proved analytic family, not its proof.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json

LABELS=('A','B','T','S','E','F')
REPLIES=(1,4,4,4,5,4)

def verify(d,g):
    assert isinstance(d,int) and isinstance(g,int) and d>3*g>0 and (d-g)%2==0
    types={1:2*d,2:(5*d+g)//2,4:(3*d+g)//2,8:(3*d+g)//2,
           20:d,24:d,36:d,40:d,49:d+g,50:d-g,54:g,58:g}
    units=[frozenset(a for a in range(6) if mask>>a&1) for mask,n in types.items() for _ in range(n)]
    def utility(path,i):
        return sum((Fraction(1,sum(a in membership for a in path)) for membership in units if path[i] in membership),Fraction(0))
    def cover(path):
        return frozenset(x for x,membership in enumerate(units) if any(a in membership for a in path))
    checks=[];last_rows=[]
    for a in range(6):
        row=[utility((a,b),1) for b in range(6)]
        checks.extend(row[REPLIES[a]]-v for v in row)
        last_rows.append([str(v) for v in row])
    root=[utility((a,REPLIES[a]),0) for a in range(6)]
    checks.extend(root[0]-v for v in root)
    pairs={LABELS[a]+LABELS[b]:len(cover((a,b))) for a,b in combinations_with_replacement(range(6),2)}
    C=cover((0,1));O=cover((2,3));R=O-C
    best=max(pairs.values());optimizers=[p for p,v in pairs.items() if v==best]
    assert len(checks)==42 and min(checks)>=0
    assert len(units)==(27*d+7*g)//2
    assert root==[Fraction(3*d+g)]*6
    assert [utility((0,1),i) for i in range(2)]==[Fraction(3*d+g),Fraction(7*d+3*g,2)]
    assert len(C)==Fraction(13*d+5*g,2)
    assert optimizers==['TS'] and best==7*d+3*g
    assert len(C&O)==2*g and len(R)==7*d+g and len(R)-len(C)==Fraction(d-3*g,2)>0
    return {'d':d,'g':g,'types':types,'customers':len(units),'labels':LABELS,'root':'A','replies':dict(zip(LABELS,[LABELS[a] for a in REPLIES])),
            'last_rows':last_rows,'root_action_values':[str(v) for v in root],
            'histories':7,'comparisons_including_self':42,'comparisons_excluding_self':35,'minimum_slack':str(min(checks)),
            'actual':['A','B'],'actual_payoffs':[str(utility((0,1),i)) for i in range(2)],'W':len(C),
            'all_unordered_pairs_including_repetitions':pairs,'OPT':best,'optimizing_topic_sets':optimizers,
            'O_intersect_C':len(C&O),'R':len(R),'R_minus_W':len(R)-len(C),'half_slack':2*len(C)-best,
            'B4_slacks':[str(2*utility((0,1),i)-(best-len(C))) for i in range(2)]}

def main():
    report={'status':'Exact full-history finite audit of a proved auxiliary-bridge counterexample family; Q-CAG-HALF and B4 not refuted',
            'cases':[verify(d,g) for d,g in [(5,1),(7,1),(9,1),(13,3),(11,3),(17,5),(101,1)]]}
    path=Path(__file__).with_name('unique_residual_family_audit.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(report['cases']),'first':report['cases'][0]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
