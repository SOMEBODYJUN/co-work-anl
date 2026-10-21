"""Optional finite MILP compression of the fixed-policy local counterexample."""
import importlib.util
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('exact_instance', HERE / 'audit_coverage_step.py')
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
MASKS = list(inst.WEIGHTS)
SCALE = 60


def shares(a, h):
    terminal = inst.PREFIX + tuple(h)
    return [Fraction(int(bool(mask >> a & 1)), sum(bool(mask >> z & 1) for z in terminal))
            if mask >> a & 1 else Fraction() for mask in MASKS]


def fresh(mask):
    return not any(mask >> a & 1 for a in inst.PREFIX)


def main():
    rows = []
    lower = []
    upper = []
    for c, a in inst.POLICY.items():
        h = tuple(z for z, n in enumerate(c) for _ in range(n))
        on = shares(a, inst.complete(h))
        for b in range(inst.Q):
            off = shares(b, inst.complete(h + (b,)))
            row = [int((x - y) * SCALE) for x, y in zip(on, off)] + [0]
            rows.append(row)
            lower.append(0)
            upper.append(np.inf)
    first = inst.POLICY[(0,) * inst.Q]
    for comp in combinations(range(inst.Q), inst.R - 1):
        rows.append([-int(fresh(mask) and not (mask >> first & 1) and any(mask >> a & 1 for a in comp))
                     for mask in MASKS] + [1])
        lower.append(0)
        upper.append(np.inf)
    comp = (0, 3, 4)
    u = shares(first, inst.complete(()))
    rows.append([int(SCALE * (v + int(fresh(mask) and bool(mask >> first & 1))
                            - int(fresh(mask) and any(mask >> a & 1 for a in comp))))
                 for mask, v in zip(MASKS, u)] + [SCALE])
    lower.append(-np.inf)
    upper.append(-1)
    res = milp(c=np.r_[np.ones(len(MASKS)), 0.0], integrality=np.ones(len(MASKS) + 1),
               bounds=Bounds(np.zeros(len(MASKS) + 1), np.full(len(MASKS) + 1, np.inf)),
               constraints=LinearConstraint(np.array(rows), lower, upper),
               options={'time_limit': 50.0})
    if res.x is None:
        print(res.message)
        return
    weights = {mask: int(round(x)) for mask, x in zip(MASKS, res.x) if x > .5}
    inst.WEIGHTS = weights
    actual = inst.complete(())
    opt, topics = inst.new_opt(inst.R)
    remopt, remtopics = inst.new_opt(inst.R - 1, excluded=(first,))
    gap = inst.payoff(first, actual) + inst.new_coverage((first,)) + remopt - opt
    data = dict(weights=weights, count=sum(weights.values()), first=first, actual=actual,
                u=str(inst.payoff(first, actual)), fresh_opt=opt, fresh_opt_topics=topics,
                remopt=remopt, remtopics=remtopics, gap=str(gap),
                optimality_status=res.message, mip_gap=float(res.mip_gap))
    (HERE / 'coverage_step_compressed.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
