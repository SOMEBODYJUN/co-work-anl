#!/usr/bin/env python3
"""Independent rational audit of the two-parameter cyclic credibility test.

No research solver, strategy cone, discovering script, or numerical LP is used.
The exhaustive affine arrangement checks this parameter family only. The
human-readable general-in-parameters argument is in the relay branch note.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
TYPES = [(frozenset((i, (i+1)%8, (i+2)%8)), (1, 0)) for i in range(8)]
TYPES += [(frozenset((i, i+4)), (0, 1)) for i in range(4)]

def coefficients(z, topic, insertion=False):
    return tuple(sum((F(w[d], int(insertion)+sum(t in b for t in z))
                      for b, w in TYPES if topic in b), F()) for d in range(2))

def at(coeff, q):
    return coeff[0] + q*coeff[1]

PAY = {(b,c): tuple(coefficients((0,b,c), t) for t in (0,b,c))
       for b,c in product(range(8), repeat=2)}
V = (F(23,16), F(5,8))

def continuations(q):
    br = {b: [c for c in range(8)
              if at(PAY[b,c][2],q) == max(at(PAY[b,d][2],q) for d in range(8))]
          for b in range(8)}
    floors = {b:min(at(PAY[b,c][1],q) for c in br[b]) for b in range(8)}
    floor = max(floors.values())
    feasible = [(b,c) for b in range(8) for c in br[b]
                if at(PAY[b,c][1],q) >= floor]
    return br, floors, feasible

def audit_query(q):
    br, floors, feasible = continuations(q)
    root = min(at(PAY[b,c][0],q) for b,c in feasible)
    predicted = F(2)+q/2 if q <= 1 else F(5,2)+q
    assert root == predicted and root > at(V,q)
    # Explicit full ordered-history strategy, including every off-path history.
    chosen = min((b,c) for b,c in feasible if at(PAY[b,c][0],q) == root)
    strategy = {():0}
    for a in range(8):
        strategy[(a,)] = (a+chosen[0])%8
        for b in range(8):
            offset = (b-a)%8
            c = chosen[1] if offset == chosen[0] else min(
                br[offset], key=lambda c:at(PAY[offset,c][1],q))
            strategy[(a,b)] = (a+c)%8
    def terminal(h):
        h = tuple(h)
        while len(h) < 3:
            h += (strategy[h],)
        return h
    checks = 0
    for depth in range(3):
        for h in product(range(8), repeat=depth):
            z = terminal(h)
            actual = at(coefficients(z,z[depth]),q)
            for t in range(8):
                assert actual >= at(coefficients(terminal(h+(t,)),t),q)
                checks += 1
    return root, checks

def main():
    # Complete rational partition for all possible ordering/tie changes.
    vectors = [p[j] for p in PAY.values() for j in range(3)] + [V]
    breaks = {F(0)}
    for x,y in combinations(vectors,2):
        if x[1] != y[1]:
            q = (y[0]-x[0])/(x[1]-y[1])
            if q > 0:
                breaks.add(q)
    bounds = sorted(breaks)
    probes = sorted(set(bounds[1:] + [(x+y)/2 for x,y in zip(bounds,bounds[1:])]
                        + [bounds[-1]+1]))
    checks = 0
    for q in probes:
        _, count = audit_query(q)
        checks += count
    # Static primal and dual independently checked for all 120 count profiles.
    static_checks = 0
    for q in (F(1,3), F(1), F(5), F(25,2), F(100)):
        target = at(V,q)
        for z in combinations_with_replacement(range(8),3):
            uniform = sum((at(coefficients(z,t,True),q) for t in range(8)),F())/8
            assert uniform >= target
            static_checks += 1
        rotations = [tuple((t+j)%8 for t in (0,2,5)) for j in range(8)]
        for t in range(8):
            assert sum((at(coefficients(z,t,True),q) for z in rotations),F())/8 == target
    # The low-root menu is terminal-optimal but violates the earlier player's
    # incentive, rather than being a genuine SPE counterexample.
    assert PAY[4,1] == ((F(2),F(1,2)), (F(3),F(1,2)), (F(2),F(1)))
    assert continuations(F(5))[0][2] == [5]
    assert at(PAY[2,5][1],F(5)) == F(15,2)
    report = {
        "scope":"two-parameter 8-theme cyclic family; no general HALF/EI claim",
        "method":"direct customer membership, exact affine arrangement, full strategy reconstruction",
        "positive_breakpoints":len(bounds)-1,
        "parameter_probes_including_all_breakpoints":len(probes),
        "ordered_history_deviation_comparisons":checks,
        "static_count_profiles_checked":static_checks,
        "root_minimum":"b<=a: 2a+b/2; b>a: 5a/2+b",
        "static_v4":"(23a+10b)/16",
        "status":"passed; finite symbolic reduction is supported by the analytic table in relay note"}
    (HERE/"cyclic_credibility_independent.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main()
