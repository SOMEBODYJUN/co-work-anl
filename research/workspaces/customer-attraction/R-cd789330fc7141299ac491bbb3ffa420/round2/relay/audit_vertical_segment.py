"""Exact audit of the proposed finite-slope obstruction; not a half counterexample."""
from fractions import Fraction as F
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
out=[]
for m in [1,2,7]:
    customers=[frozenset([0])]*(2*m)+[frozenset([1])]*m
    def payoff(label,profile):
        return sum((F(1,sum(a in likes for a in profile)) for likes in customers if label in likes),F(0))
    # Fixed ancestor A=0, one actual future player.
    future=[payoff(a,[0,a]) for a in range(2)]
    ancestor=[payoff(0,[0,a]) for a in range(2)]
    assert future==[F(m),F(m)] and ancestor==[F(m),F(2*m)]
    assert all(v==max(future) for v in future)
    out.append(dict(M=m,current=list(map(str,future)),ancestor=list(map(str,ancestor)),current_difference='0',ancestor_difference=str(m)))
(HERE/'vertical_segment_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
