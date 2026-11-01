"""One bounded floating attack on a general candidate in old strategy scaffolds.

It requires a target optimal multiset to strictly beat every other multiset and
all its frozen assignments to strictly exceed W. No exact cone theorem follows
from a zero floating optimum. In particular repeated targets can make the strict
optimality condition vacuous because another repetition has the same union.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import argparse
import hashlib
import json

from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
TARGETS = {
    "eight_cce_welfare_gap": ((1, 2, 3),),
    "worst_cce_welfare_failure": ((1, 2, 4), (1, 3, 4)),
    "prefix_balance_failure": ((0, 3, 4, 5),),
    "worst_pne_welfare_failure": ((0, 1, 2), (0, 1, 3), (1, 1, 2), (1, 1, 3), (1, 2, 2)),
}


def diagnose(name, targets):
    cp = Path("evidence/certificates/customer_attraction") / (name + ".json")
    ip = Path("examples/customer_attraction") / (name + ".json")
    raw, original = json.loads((ROOT / cp).read_text()), json.loads((ROOT / ip).read_text())
    certificate = raw.get("strategy", raw)
    actions = {tuple(row["history"]): row["action"] for row in certificate["actions"]}
    m, k = original["players"], len(original["topics"])
    masks = tuple(range(1, 1 << k))

    def finish(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def payoff(h, i):
        return [F(1, sum(bool(mask >> a & 1) for a in h))
                if mask >> h[i] & 1 else F(0) for mask in masks]

    def cover(h):
        return [int(any(mask >> a & 1 for a in h)) for mask in masks]

    z = finish(())
    W = cover(z)
    all_tuples = tuple(combinations_with_replacement(range(k), m))
    base = []
    for i in range(m):
        for h in product(range(k), repeat=i):
            v = payoff(finish(h), i)
            for a in range(k):
                deviation = payoff(finish(h + (a,)), i)
                base.append([float(x - y) for x, y in zip(deviation, v)] + [0])
    outputs = []
    for t in targets:
        O = cover(t)
        constraints = [row[:] for row in base]
        for alternative in all_tuples:
            if alternative != t:
                constraints.append([x - y for x, y in zip(cover(alternative), O)] + [1])
        for assignment in sorted(set(permutations(t))):
            D = [sum(payoff(z[:i] + (assignment[i],) + z[i + 1:], i)[j]
                     for i in range(m)) for j in range(len(masks))]
            constraints.append([float(w - d) for w, d in zip(W, D)] + [1])
        result = linprog([0] * len(masks) + [-1], A_ub=constraints,
                         b_ub=[0] * len(constraints), A_eq=[W + [0]], b_eq=[1],
                         bounds=[(0, None)] * (len(masks) + 1), method="highs")
        record = {"target": list(t), "strict_multiset_uniqueness_required": True,
                  "repeated_target": len(set(t)) != len(t),
                  "floating_solver_status": result.status, "message": result.message,
                  "constraint_count": len(constraints)}
        if result.success:
            record["floating_common_strict_margin"] = float(result.x[-1])
            record["positive_candidate"] = bool(result.x[-1] > 1e-8)
            record["nonzero_floating_customer_types"] = [
                {"mask": mask, "weight": float(weight)}
                for mask, weight in zip(masks, result.x[:-1]) if weight > 1e-8]
        outputs.append(record)
    return {"scaffold": name, "players": m, "catalog_size": k,
            "all_nonempty_customer_types": len(masks), "actual": list(z),
            "SPE_constraints_with_self": len(base), "targets": outputs,
            "source_sha256": {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                              for p in (cp, ip)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"status": "bounded floating candidate attack only; no exact or general positive conclusion",
              "rational_dual_extracted": False, "scaffolds": [diagnose(n, t) for n, t in TARGETS.items()]}
    data = json.dumps(result, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(data)
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
