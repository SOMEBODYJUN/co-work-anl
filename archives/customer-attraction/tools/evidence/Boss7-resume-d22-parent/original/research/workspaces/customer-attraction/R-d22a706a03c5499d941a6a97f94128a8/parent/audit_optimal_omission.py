"""Independent unit-customer audit, based only on the announced statement.
No imports from the discovery code or the repository's game solver.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json

LABELS = ('A', 'B', 'T', 'Q', 'R', 'S')
ROWS = [('A',9),('B',9),('T',13),('Q',8),('AR',1),('BR',4),
        ('QR',5),('AS',1),('BS',4),('QS',5),('ARS',5),('TRS',5),
        ('BTRS',1),('BQRS',1)]
UNITS = [frozenset(s) for s,n in ROWS for _ in range(n)]
TOPICS = {a:frozenset(i for i,interest in enumerate(UNITS) if a in interest)
          for a in LABELS}
REPLY = dict(zip(LABELS, ('B','R','R','R','S','R')))

def payoff(path, player):
    return sum((F(1,sum(x in TOPICS[a] for a in path))
                for x in TOPICS[path[player]]), F(0))

def union(path):
    return frozenset().union(*(TOPICS[a] for a in path))

def main():
    path=('A', REPLY['A'])
    nodes=[()]+[(a,) for a in LABELS]
    rows=[]
    for h in nodes:
        chosen='A' if not h else REPLY[h[0]]
        i=len(h)
        p=(chosen,REPLY[chosen]) if not h else h+(chosen,)
        original=payoff(p,i)
        for a in LABELS:
            dev=(a,REPLY[a]) if not h else h+(a,)
            gap=original-payoff(dev,i)
            assert gap>=0,(h,a,gap)
            rows.append((h,a,gap))
    C=union(path)
    covers=[(a,b,len(union((a,b))))
            for a,b in combinations_with_replacement(LABELS,2)]
    opt=max(n for a,b,n in covers)
    best=[(a,b) for a,b,n in covers if n==opt]
    assert len(UNITS)==71 and len(set(TOPICS.values()))==6
    assert best==[('T','Q')],best
    D=union(best[0])-C
    assert len(C)==35 and opt==38 and len(D)==36
    assert [payoff(path,i) for i in range(2)]==[F(16),F(19)]
    assert set(payoff((a,REPLY[a]),0) for a in LABELS)=={F(16)}
    result={
      'status':'PASS','scope':'announced 71-unit-customer complete two-player SPE only',
      'unit_customers':len(UNITS),'distinct_topics':len(set(TOPICS.values())),
      'decision_nodes':len(nodes),'comparisons_including_self':len(rows),
      'minimum_gap':str(min(g for h,a,g in rows)),
      'path':path,'payoffs':[str(payoff(path,i)) for i in range(2)],
      'W':len(C),'OPT':opt,'unique_optimal_pair':best[0],
      'optimal_omission':len(D),'optimal_intersection':len(union(best[0])&C),
      'half_margin':2*len(C)-opt,
      'last_payoff_table':{a:[str(payoff((a,b),1)) for b in LABELS] for a in LABELS},
      'all_unordered_pair_covers':covers,
      'all_nonnegative_gaps':[{'history':h,'alternative':a,'gap':str(g)} for h,a,g in rows]
    }
    out=Path(__file__).with_name('optimal_omission_independent_audit.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','unit_customers','decision_nodes','comparisons_including_self','W','OPT','unique_optimal_pair','optimal_omission','half_margin')},ensure_ascii=False))

if __name__=='__main__': main()
