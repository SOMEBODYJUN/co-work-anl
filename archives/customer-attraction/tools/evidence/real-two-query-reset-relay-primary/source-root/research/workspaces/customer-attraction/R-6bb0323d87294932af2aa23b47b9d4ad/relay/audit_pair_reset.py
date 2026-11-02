"""Definition-level rational check of the two-query extra-slot reset identity.

This tests a precise general candidate on pre-existing full SPE certificates;
passing certificates do not establish that candidate. No policy search occurs.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
NAMES = [
    "residual_counterexample", "aggregate_theta_failure",
    "individual_security_failure", "local_security_increment",
    "global_decorrelation_failure", "root_tax_failure",
    "five_individual_security",
]


def run(name):
    data = json.loads((ROOT / "examples/customer_attraction" / f"{name}.json").read_text())
    cert = json.loads((ROOT / "evidence/certificates/customer_attraction" / f"{name}.json").read_text())
    cert = cert.get("strategy", cert)
    policy = {tuple(r["history"]): r["action"] for r in cert["actions"]}
    k = len(data["topics"])
    m = max(map(len, policy)) + 1
    customers = [(frozenset(r["topics"]), r.get("multiplicity", 1)) for r in data["customers"]]

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (policy[h],)
        return h

    def load(z, B):
        return sum(a in B for a in z)

    def payoff(z, i):
        return sum((F(w, load(z, B)) for B, w in customers if z[i] in B), F())

    comparisons = 0
    for h in policy:
        z = finish(h)
        for a in range(k):
            assert payoff(z, len(h)) >= payoff(finish(h + (a,)), len(h))
            comparisons += 1

    actual = finish(())
    u = [payoff(actual, i) for i in range(m)]
    W = sum(u)
    H = [[F() for a in range(k)] for t in range(k)]
    worst_local_defect = (F(), None)
    max_abs_identity_error = F()
    for i in range(m):
        h = actual[:i]
        leaves = [finish(h + (a,)) for a in range(k)]
        D = [payoff(z, i) for z in leaves]
        K = [[sum((F(w, 1 + load(leaves[a], B)) for B, w in customers if t in B), F())
              for a in range(k)] for t in range(k)]
        for t in range(k):
            for a in range(k):
                H[t][a] += K[t][a]
                direct = K[t][a] + K[a][t] - D[a] - D[t]
                signed_reset = F()
                for B, w in customers:
                    ax, tx = a in B, t in B
                    ca, ct = load(leaves[a], B), load(leaves[t], B)
                    if ax and tx:
                        signed_reset -= F(w, ca * (ca + 1)) + F(w, ct * (ct + 1))
                    elif ax:
                        ba = load(leaves[a][i+1:], B)
                        bt = load(leaves[t][i+1:], B)
                        b = load(h, B)
                        signed_reset += F(w * (ba - bt), (b + 1 + ba) * (b + 1 + bt))
                    elif tx:
                        ba = load(leaves[a][i+1:], B)
                        bt = load(leaves[t][i+1:], B)
                        b = load(h, B)
                        signed_reset += F(w * (bt - ba), (b + 1 + ba) * (b + 1 + bt))
                err = abs(direct - signed_reset)
                max_abs_identity_error = max(max_abs_identity_error, err)
                assert not err
                if direct > worst_local_defect[0]:
                    worst_local_defect = direct, [i, a, t]
    margins = [(2 * W - H[t][a] - H[a][t], a, t) for a in range(k) for t in range(a, k)]
    margin, a, t = min(margins)
    return {
        "input": name, "players": m, "topics": k,
        "full_SPE_comparisons": comparisons, "actual": actual,
        "profits": list(map(str, u)), "welfare": str(W),
        "max_identity_error": str(max_abs_identity_error),
        "min_pair_budget_margin": str(margin), "argmin_pair": [a, t],
        "max_local_pair_defect": str(worst_local_defect[0]),
        "max_local_pair_defect_location": worst_local_defect[1],
        "H": [list(map(str, row)) for row in H],
    }


if __name__ == "__main__":
    results = [run(name) for name in NAMES]
    out = {"status": "finite verification only; general pair budget OPEN", "results": results}
    (HERE / "pair_reset_checks.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps([{key: val for key, val in r.items() if key != "H"} for r in results], indent=2))
