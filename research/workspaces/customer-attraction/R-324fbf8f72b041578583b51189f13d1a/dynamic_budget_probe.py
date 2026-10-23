"""One bounded attack on delta <= 2 u for total-coverage opportunity.

No universal conclusion is inferred from a finite LP. The frozen full policy is
always fresh, with two m-label groups; all histories are included in the SPE cone.
"""
from itertools import product, combinations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def run(m, family="fresh"):
    k = 2 * m if family == "fresh" else m + 2
    masks = np.arange(1, 1 << k)
    membership = np.array([[(mask >> a) & 1 for a in range(k)] for mask in masks], dtype=float)

    def fresh_choice(h):
        if not h:
            return 0
        if len(h) == 1:
            group = 1 - (h[0] // m)
        elif len(set(a // m for a in h)) == 1:
            group = h[0] // m
        else:
            group = h[1] // m
        return next(a for a in range(group * m, (group + 1) * m) if a not in h)

    base_weights = np.zeros(len(masks))
    for j in range(m):
        leaf = j + 2
        for mask, weight in [(1 << leaf, m - 2), ((1 << 1) | (1 << leaf), m - 2),
                             (((1 << 0) | (1 << leaf)) if j < m - 1 else ((1 << 0) | (1 << 1) | (1 << leaf)),
                              1 if j < m - 1 else m - 1)]:
            base_weights[mask - 1] += weight

    def prefix_choice(h):
        if len(h) < m - 1:
            return 0 if not h or all(a == 1 for a in h) else 1
        counts = np.bincount(h, minlength=k)
        values = [float((membership[:, a] / (membership @ counts + 1)) @ base_weights)
                  for a in range(k)]
        order = [1, 0] + list(range(2, k))
        return max(order, key=lambda a: values[a])

    choice = fresh_choice if family == "fresh" else prefix_choice

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (choice(h),)
        return h

    def payoff(path, a):
        counts = np.bincount(path, minlength=k)
        denom = membership @ counts
        return np.divide(membership[:, a], denom, out=np.zeros(len(masks)), where=denom > 0)

    rows = []
    for depth in range(m):
        for h in product(range(k), repeat=depth):
            selected = choice(h)
            actual = payoff(finish(h), selected)
            for a in range(k):
                if a != selected:
                    rows.append(payoff(finish(h + (a,)), a) - actual)
    spe_rows = np.array(rows)
    path = finish(())
    own = payoff(path, path[0])
    completions = list(combinations(range(k), m - 1))
    completion_vectors = [((membership[:, 0] + membership[:, subset].sum(axis=1)) > 0).astype(float)
                          for subset in completions]
    # q caps the coverage of every legal completion after actual root action 0.
    aub = np.vstack([np.column_stack([spe_rows, np.zeros(len(rows))]),
                     np.array([np.r_[v, -1.] for v in completion_vectors])])
    bub = np.zeros(len(aub))
    aeq = np.r_[own, 0.][None, :]
    if family == "fresh":
        candidates = [tuple(range(m, 2 * m)), tuple(range(1, m + 1))]
        candidates += [tuple(range(1, j + 1)) + tuple(range(m, 2 * m - j))
                       for j in range(1, m)]
    else:
        candidates = [tuple(range(2, k))]
    reports = []
    for opt in dict.fromkeys(candidates):
        cover = (membership[:, opt].sum(axis=1) > 0).astype(float)
        objective = np.r_[-cover, 1.]
        result = linprog(objective, A_ub=aub, b_ub=bub, A_eq=aeq,
                         b_eq=[1.], bounds=[(0., None)] * (len(masks) + 1), method="highs")
        report = {"players": m, "topics": k, "family": family, "benchmark": opt,
                  "status": int(result.status), "message": result.message,
                  "histories": sum(k ** d for d in range(m)), "spe_rows": len(rows)}
        if result.success:
            report.update(delta_over_u=float(-result.fun),
                          positive_types=[(int(mask), float(weight)) for mask, weight in zip(masks, result.x[:-1]) if weight > 1e-7])
        reports.append(report)
    return reports


if __name__ == "__main__":
    report = {"scope": "bounded floating LP attack, not proof or exact certificate", "runs": run(3) + run(4) + run(4, "prefix") + run(5, "prefix")}
    destination = Path(__file__).with_name("dynamic_budget_probe.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    for row in report["runs"]:
        print(row["players"], row["benchmark"], row.get("delta_over_u", row["status"]))
