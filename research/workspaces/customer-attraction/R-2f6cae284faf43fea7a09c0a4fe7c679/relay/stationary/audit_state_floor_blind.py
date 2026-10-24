"""Independent exact audit from the supplied ten-topic interface statement.

No solver imports, no author proof, and no SPE claim.  Tests only whether
prefix-dependent extra-slot floors plus root comparisons force root >= v4.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPICS = tuple(frozenset(((i-1) % 10, i, (i+1) % 10)) for i in range(10))

def load(profile):
    return Counter(x for a in profile for x in TOPICS[a])

def query(a, competitors=(), prefix=()):
    counts = load(tuple(prefix)+tuple(competitors))
    return sum((F(1, 1+counts[x]) for x in TOPICS[a]), F(0))

def utility(profile, position):
    counts = load(profile)
    return sum((F(1, counts[x]) for x in TOPICS[profile[position]]), F(0))

uniform_values = []
for B in product(range(10), repeat=3):
    value = sum((query(a, B) for a in range(10)), F(0))/10
    uniform_values.append((value, B))
minimum, minimizer = min(uniform_values)
assert minimum == F(33,20)

# Explicit dual: uniform rotational images of one minimizing competitor tuple.
dual_values = []
for a in range(10):
    value = sum((query(a, tuple((b+s)%10 for b in minimizer))
                 for s in range(10)), F(0))/10
    dual_values.append(value)
assert set(dual_values) == {minimum}

records=[]
for i in range(10):
    profile=(i,(i-1)%10,(i+2)%10)
    pay=tuple(utility(profile,j) for j in range(3))
    assert pay == (F(3,2), F(2), F(5,2))
    B3=((i+3)%10,(i+6)%10)
    upper3=tuple(query(a,B3,(i,)) for a in range(10))
    assert max(upper3)==F(2)
    B2=((i+4)%10,)
    upper2=tuple(query(a,B2,(i,(i-1)%10)) for a in range(10))
    assert max(upper2)==F(5,2)
    dev=(i+4)%10
    changed=profile[:2]+(dev,)
    devpay=utility(changed,2)
    assert devpay==F(3)>pay[2]
    records.append(dict(root=i,profile=profile,payoffs=list(map(str,pay)),
                        v3_upper_witness=B3,v3_query_values=list(map(str,upper3)),
                        v2_upper_witness=B2,v2_query_values=list(map(str,upper2)),
                        last_profitable_deviation=dev,last_deviation_payoff=str(devpay)))

report=dict(scope="Exact auxiliary-interface counterexample; profiles are not SPE",
            customers=10,topics=[sorted(T) for T in TOPICS],players=3,
            root_payoff="3/2",v4="33/20",root_gap="3/20",
            uniform_query_lower_checked_competitor_tuples=len(uniform_values),
            v4_minimizer=minimizer,dual_rotational_query_values=list(map(str,dual_values)),
            all_rotations=records)
(HERE/'state_floor_blind_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('all_rotations','topics')},indent=2))
