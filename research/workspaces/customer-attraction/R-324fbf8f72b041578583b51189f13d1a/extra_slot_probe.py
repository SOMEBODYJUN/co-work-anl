"""One fixed full SPE cone versus the extra-slot iid first-mover candidate.

The LP only proposes multiplicities; exact rational stationarity and every
ordered-history comparison are required before accepting a separator.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("cone_audit", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def policy(h):
    if len(h) < 3:
        return 0
    if h.count(0) <= 1:
        return 0
    if h.count(0) == 2 and 5 in h:
        return 4
    return 5


def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))


def main():
    cone = mod.StrategyCone(6, 4, {h:policy(h) for d in range(4) for h in product(range(6), repeat=d)})
    first = mod.payoff_row(6, cone.root, 0)
    results = []
    distributions = [tuple(map(F, q)) for q in [
        (F(3,5), F(3,100), F(3,100), F(3,100), F(31,200), F(31,200)),
        (F(49,80), F(23,800), F(17,800), F(23,800), F(247,1600), F(247,1600)),
        (F(3,5), F(1,30), F(1,30), F(1,30), F(3,20), F(3,20)),
        (F(2,3), 0, 0, 0, F(1,6), F(1,6)),
        (F(1,2), F(1,6), F(1,6), F(1,6), 0, 0),
        (F(1,3), F(1,3), F(1,3), 0, 0, 0),
        (F(1,6),)*6,
    ]]
    for q in distributions:
        assert sum(q) == 1
        gx = []
        for mask in range(1,64):
            t = sum((q[a] for a in range(6) if mask>>a&1),F(0))
            gx.append(sum(((1-t)**j for j in range(5)),F(0))/5)
        alpha = [tuple(gx[mask-1] if mask>>a&1 else F(0) for mask in range(1,64)) for a in range(6)]
        lam = tuple(sum((q[a]*alpha[a][j] for a in range(6)),F(0)) for j in range(63))
        e_rows = [tuple(lam[j]-alpha[a][j] for j in range(63)) for a in range(6)]
        eq = [tuple(F(1) for _ in range(63))] + [e_rows[a] for a in range(6) if q[a]]
        ub = list(cone.rows) + [e_rows[a] for a in range(6) if not q[a]]
        objective = tuple(first[j]-lam[j] for j in range(63))
        ans = linprog(np.array(objective,float), A_ub=-np.array(ub,float), b_ub=np.zeros(len(ub)),
                      A_eq=np.array(eq,float), b_eq=[1]+[0]*(len(eq)-1), bounds=(0,None),method="highs")
        record = {"q":list(map(str,q)),"status":ans.message}
        if ans.success:
            v = tuple(F(float(x)).limit_denominator(10**9) for x in ans.x)
            okay = all(x>=0 for x in v) and sum(v)==1 and all(dot(row,v)==0 for row in eq[1:]) and all(dot(row,v)>=0 for row in ub)
            record.update(floating_gap=float(ans.fun), exact_simple_recovery=okay)
            if okay:
                record["exact_gap"] = str(dot(objective,v))
                if dot(objective,v)<0:
                    scale=math.lcm(*(x.denominator for x in v));counts=[int(x*scale) for x in v]
                    div=math.gcd(*counts);counts=[x//div for x in counts]
                    record["integer_types"]={str(mask):counts[mask-1] for mask in range(1,64) if counts[mask-1]}
        results.append(record)
    print(json.dumps({"scope":"single fixed full four-player policy cone, fixed rational iid queries", "results":results},indent=2))


if __name__ == "__main__":
    main()
