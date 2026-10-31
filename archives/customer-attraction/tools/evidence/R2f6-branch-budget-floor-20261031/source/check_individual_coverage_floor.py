"""Test the precise all-m candidate (2m-1)u_i >= OPT_m in fixed full SPE cones.

No strategy search: only the listed pre-existing complete strategies are used.
A negative floating point LP value is only a proposal; output also records exact
rational re-verification of every full-history SPE row and the failed claim.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import itertools, json, math, sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
SOURCES = [
    "individual_security_failure", "aggregate_theta_failure", "root_tax_failure",
    "portfolio_matching_failure", "global_decorrelation_failure",
]


def check(name):
    source = ROOT / "evidence/certificates/customer_attraction" / (name + ".json")
    data = json.loads(source.read_text())
    strategy = data.get("strategy", data)
    actions = {tuple(r["history"]): r["action"] for r in strategy["actions"]}
    m = 1 + max(map(len, actions))
    k = 1 + max(actions.values())
    masks = tuple(range(1, 1 << k))
    bit = np.array([[bool(B >> a & 1) for a in range(k)] for B in masks], int)

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))

    @lru_cache(None)
    def utility(z, a):
        c = bit[:, z].sum(axis=1)
        return bit[:, a] / np.maximum(c, 1)

    rows = []
    exact_rows = []
    for h in actions:
        own = utility(terminal(h), actions[h])
        for a in range(k):
            if a != actions[h]:
                rows.append(utility(terminal(h + (a,)), a) - own)
                exact_rows.append((h, a))
    actual = terminal(())
    best = None
    for target in itertools.combinations(range(k), min(k, m)):
        O = bit[:, target].any(axis=1).astype(float)
        for i, a in enumerate(actual):
            obj = (2 * m - 1) * utility(actual, a) - O
            sol = linprog(obj, A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                          A_eq=[np.ones(len(masks))], b_eq=[1],
                          bounds=[(0, None)] * len(masks), method="highs")
            if sol.success and (best is None or sol.fun < best["lp_value"]):
                best = {"source": name, "players": m, "topics": k,
                        "actual": actual, "target": target, "player": i,
                        "lp_value": float(sol.fun)}
                if sol.fun < -1e-8:
                    vals = [F(float(x)).limit_denominator(10**7) for x in sol.x]
                    den = math.lcm(*(x.denominator for x in vals))
                    counts = [int(x * den) for x in vals]
                    gcd = math.gcd(*counts)
                    counts = [x // gcd for x in counts]
                    def eu(z, aa):
                        return sum((F(v, sum(B >> t & 1 for t in z))
                                    for B, v in zip(masks, counts) if v and B >> aa & 1), F(0))
                    slacks = [eu(terminal(h), actions[h]) - eu(terminal(h + (aa,)), aa)
                              for h, aa in exact_rows]
                    welfare = sum(v for B, v in zip(masks, counts)
                                  if any(B >> aa & 1 for aa in actual))
                    coverage = sum(v for B, v in zip(masks, counts)
                                   if any(B >> aa & 1 for aa in target))
                    covers = [frozenset(B for B, v in zip(masks, counts) if v and B >> aa & 1)
                              for aa in range(k)]
                    best.update({"counts": {str(B): v for B, v in zip(masks, counts) if v},
                                 "exact_all_SPE_rows": min(slacks) >= 0,
                                 "min_SPE_slack": str(min(slacks)),
                                 "distinct_topic_covers": len(set(covers)) == k,
                                 "payoffs": list(map(str, (eu(actual, aa) for aa in actual))),
                                 "welfare": welfare, "comparison_coverage": coverage,
                                 "exact_gap": str((2*m-1)*eu(actual,a)-coverage),
                                 "actions": strategy["actions"]})
                    if min(slacks) >= 0 and (2*m-1)*eu(actual,a) < coverage:
                        return best
    return best


if __name__ == "__main__":
    out = []
    for source in SOURCES:
        result = check(source)
        out.append(result)
        print({k: v for k, v in result.items() if k not in {"actions", "counts"}}, flush=True)
        Path(__file__).with_name("individual_coverage_floor_test.json").write_text(
            json.dumps(out, indent=2) + "\n")
        if result.get("exact_all_SPE_rows") and F(result["exact_gap"]) < 0:
            break
