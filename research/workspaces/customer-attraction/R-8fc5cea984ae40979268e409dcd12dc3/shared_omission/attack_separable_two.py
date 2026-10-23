"""Attack a precise shared-omission bridge using complete two-player policies.

Not a general search for HALF. Actual path (A,B); omitted projections of every
topic are empty, Q0, or Q1. Types meeting A or B have arbitrary interests.
Every policy tested specifies the reply after all six legal first actions.
Floating LP output is only discovery; an alleged counterexample must be replayed
with rational weights and all SPE inequalities before use.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

LABELS = ("A", "B", "T0", "T1", "Q0", "Q1")
TYPES = tuple(mask for mask in range(1, 64) if mask & 3) + (12, 48)

def utility(first, second, player):
    act = first if player == 0 else second
    return np.array([int(mask >> act & 1) /
                     (int(mask >> first & 1) + int(mask >> second & 1))
                     if mask >> act & 1 else 0 for mask in TYPES])

def constraints(replies):
    rows = []
    root = utility(0, 1, 0)
    for first, reply in enumerate(replies):
        chosen = utility(first, reply, 1)
        rows.extend(utility(first, other, 1) - chosen for other in range(6))
        rows.append(utility(first, reply, 0) - root)
    return np.array(rows)

def main():
    # m=2: try all four replies on omitted variants, plus all B replies.
    # This is 6^5=7776 complete policies, a finite exact class of templates.
    obj = np.array([-int(mask in (12, 48)) for mask in TYPES], dtype=float)
    welfare = np.array([int(bool(mask & 3)) for mask in TYPES], dtype=float)
    best = None
    policies = 0
    for rest in product(range(6), repeat=5):
        replies = (1,) + rest
        result = linprog(obj, A_ub=constraints(replies),
                         b_ub=np.zeros(42), A_eq=welfare[None,:],
                         b_eq=[1.0], bounds=(0,None), method="highs")
        policies += 1
        if result.success and (best is None or -result.fun > best["ratio"] + 1e-8):
            best = {"ratio": -result.fun, "replies": replies,
                    "types": [[mask, str(Fraction(float(x)).limit_denominator(100000))]
                              for mask, x in zip(TYPES,result.x) if x > 1e-8]}
    assert best is not None
    # Replay the discovered optimal policy in exact arithmetic. Nonpositive
    # objective is only evidence for this finite template class.
    weights = {mask: Fraction(w) for mask,w in best["types"]}
    def u(a,b,p):
        act = a if p == 0 else b
        return sum(w / (int(mask>>a&1)+int(mask>>b&1))
                   for mask,w in weights.items() if mask>>act&1)
    rows = []
    for first, reply in enumerate(best["replies"]):
        rows += [u(first,reply,1)-u(first,other,1) for other in range(6)]
        rows += [u(0,1,0)-u(first,reply,0)]
    w = sum(w for mask,w in weights.items() if mask&3)
    d = sum(w for mask,w in weights.items() if mask in (12,48))
    report = {"identity":"SEPARABLE-OMISSION-TWO-POLICY-ATTACK-v1",
              "scope":"6 labeled topics; full pair-interest omitted blocks; all C types; m=2",
              "policies":policies,"best":best,"exact_W":str(w),
              "exact_D":str(d),"exact_min_SPE_slack":str(min(rows)),
              "exact_SPE_rows":len(rows),"SPE_valid":min(rows)>=0,
              "warning":"No general claim follows from this finite LP attack."}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    Path(__file__).with_name("attack_separable_two_report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n")

if __name__ == "__main__":
    main()
