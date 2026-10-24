"""One targeted floating attack on WEAK-Q, in two existing full policies only.

The precise all-input conjecture attacked is: some optimal m-multiset has a
frozen assignment cost <= (1+1/m)W.  We demand unique optimal support and strict
violation of every permutation, to avoid silently changing the existential
quantifier.  Zero/failed optimization proves nothing generally or exactly.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
import importlib.util
import json
from pathlib import Path
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
source = HERE.parents[1] / "round8" / "matching" / "audit_terminal_wallet.py"
spec = importlib.util.spec_from_file_location("previous_wallet_loaders", source)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def attack(loader, target):
    instance, policy, sources = loader()
    m, k = instance["players"], len(instance["topics"])
    masks = tuple(range(1, 1 << k))

    def finish(h):
        while len(h) < m:
            h += (policy[h],)
        return h

    def payoff(leaf, i):
        return [F(1, sum(bool(mask >> a & 1) for a in leaf))
                if mask >> leaf[i] & 1 else F(0) for mask in masks]

    def cover(leaf):
        return [int(any(mask >> a & 1 for a in leaf)) for mask in masks]

    z = finish(())
    W, O = cover(z), cover(target)
    rows = []
    for i in range(m):
        for h in product(range(k), repeat=i):
            selected = payoff(finish(h), i)
            for a in range(k):
                deviated = payoff(finish(h + (a,)), i)
                rows.append([float(x-y) for x, y in zip(deviated, selected)] + [0.0])
    ic_count = len(rows)
    for alternative in combinations_with_replacement(range(k), m):
        if alternative != target:
            rows.append([float(x-y) for x, y in zip(cover(alternative), O)] + [1.0])
    for permutation in sorted(set(permutations(target))):
        cost_rows = [payoff(z[:i] + (permutation[i],) + z[i+1:], i) for i in range(m)]
        D = [sum((row[j] for row in cost_rows), F(0)) for j in range(len(masks))]
        rows.append([float(F(m+1, m)*w-d) for w, d in zip(W, D)] + [1.0])
    result = linprog([0.0]*len(masks)+[-1.0], A_ub=rows,
                     b_ub=[0.0]*len(rows), A_eq=[W+[0.0]], b_eq=[1.0],
                     bounds=[(0.0, None)]*(len(masks)+1), method="highs")
    record = {"sources": sources, "players": m, "catalog_size": k,
              "policy_fixed": True, "actual": list(z), "target": list(target),
              "uniqueness_over_all_m_multisets_required": True,
              "all_permutations_strictly_violate_weak_bound_required": True,
              "original_IC_rows_including_self": ic_count,
              "total_rows": len(rows), "floating_solver_status": result.status,
              "message": result.message}
    if result.success:
        record["floating_common_strict_margin"] = float(result.x[-1])
        record["positive_candidate"] = bool(result.x[-1] > 1e-8)
        if record["positive_candidate"]:
            record["floating_customer_weights"] = [
                {"mask": mask, "weight": float(x)}
                for mask, x in zip(masks, result.x[:-1]) if x>1e-8]
    return record


def main():
    result = {"status": "bounded floating attack only; no exact or general conclusion",
              "rational_dual_extracted": False,
              "general_half": "OPEN", "weak_optimal_assignment": "OPEN",
              "cases": {
                  "old52_policy": attack(old.load_old52, (0, 1, 4, 5)),
                  "old1953_policy": attack(old.load_new1953, (1, 2, 5)),
              }}
    path = HERE / "weak_assignment_existing_cones_floating.json"
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
