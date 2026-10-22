"""Definition-level audit of the projected signed-relay debt identity.

This is an eight-customer mechanism witness, not a half-coverage counterexample.
The general identity is proved in projected_relay_debt.md.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
TOPICS = ("T", "M", "R")
CUSTOMERS = (
    frozenset(("T", "M")),
    frozenset(("T", "M")),
    frozenset(("T",)),
    frozenset(("M",)),
    *(frozenset(("R",)) for _ in range(4)),
)
M = 3


def choose(h, branch):
    if not h:
        return "M"
    if len(h) == 1:
        return {"T": branch, "M": "R", "R": "M"}[h[0]]
    return "M" if h == ("R", "R") else "R"


def finish(h, branch):
    while len(h) < M:
        h += (choose(h, branch),)
    return h


def counts(path):
    return [sum(a in x for a in path) for x in CUSTOMERS]


def payoff(topic, path):
    return sum((F(1, c) for x, c in zip(CUSTOMERS, counts(path)) if topic in x), F(0))


def U(d, a, b):
    return sum((F(1, q + 1 + (b in x)) for x, q in zip(CUSTOMERS, d) if a in x), F(0))


def audit(branch):
    comparison_rows = []
    for depth in range(M):
        for h in product(TOPICS, repeat=depth):
            actual = finish(h, branch)
            own = payoff(choose(h, branch), actual)
            margins = {}
            for t in TOPICS:
                margin = own - payoff(t, finish(h + (t,), branch))
                assert margin >= 0
                margins[t] = margin
            comparison_rows.append(dict(history=h, action=choose(h, branch), payoff=own, margins=margins))

    path = finish((), branch)
    c = counts(path)
    utilities = [payoff(t, path) for t in path]
    W, w = sum(utilities), utilities[-1]
    z = {a: F(1) for a in TOPICS}
    tau = sum(z.values())
    mu = {a: z[a] / tau for a in TOPICS}
    query_load = [sum(z[a] for a in TOPICS if a in x) for x in CUSTOMERS]
    coverage = sum(min(F(1), v) for v in query_load)
    rows = []
    for i in range(M - 1):
        A, B = path[i], path[-1]
        d = [q - (A in x) - (B in x) for x, q in zip(CUSTOMERS, c)]
        leaves = {t: finish(path[:i] + (t,), branch) for t in TOPICS}
        replies = {t: leaves[t][-1] for t in TOPICS}
        diagonal = {t: payoff(t, leaves[t]) for t in TOPICS}
        delta = sum((mu[t] * mu[q] * U(d, t, replies[q]) for t, q in product(TOPICS, repeat=2)), F(0)) - sum(mu[t] * diagonal[t] for t in TOPICS)
        s = utilities[i] - sum(mu[t] * diagonal[t] for t in TOPICS)
        zz = w - sum(mu[t] * U(d, replies[t], A) for t in TOPICS)
        E = F(0)
        raw_residual = F(0)
        t_sum = F(0)
        K = F(0)
        for x, q, v in zip(CUSTOMERS, d, query_load):
            a = A in x
            e = sum((mu[t] for t in TOPICS if replies[t] in x), F(0))
            threshold = min(F(1, q + 1), F(1, q + 2) + F(1, 2 * (q + a + 1)))
            E_x = (1 - threshold) * (1 - min(F(1), v)) + max(F(0), v - 1) / (q + 2)
            R_x = min(F(1), v) - v / (q + 1) - e / (2 * (q + a + 1)) + v * e / ((q + 1) * (q + 2))
            K_x = (1 - threshold) - E_x - R_x
            assert K_x >= 0
            E += E_x
            raw_residual += R_x
            t_sum += 1 - threshold
            K += K_x
        FF = W - utilities[i] / 2 - w / 2 - t_sum
        assert FF >= 0
        projected = tau * sum((mu[t] * mu[q] * U(d, t, replies[q]) for t, q in product(TOPICS, repeat=2)), F(0)) - tau * utilities[i]
        assert tau * (delta - s) == projected
        exact = W + (tau - F(1, 2)) * utilities[i] + tau * delta - tau * s - zz / 2 - E - FF - K
        assert exact == coverage
        rows.append(dict(position=i + 1, replies=replies, deviation_payoffs=diagonal, delta=delta, s=s, z_slack=zz, E=E, F_slack=FF, K=K, projected_delta_minus_S=projected))

    p = [q - (path[-1] in x) for x, q in zip(CUSTOMERS, c)]
    expected_last = sum((mu[t] * U(p, t, "") for t in TOPICS), F(0))
    s_last = w - expected_last
    E_last = sum((F(q, q + 1) * (1 - min(F(1), v)) + max(F(0), v - 1) / (q + 1) for q, v in zip(p, query_load)), F(0))
    F_last = W - w - sum((F(q, q + 1) for q in p), F(0))
    assert coverage == W + (tau - 1) * w - tau * s_last - E_last - F_last
    debt = tau * sum((r["delta"] - r["s"] for r in rows), F(0)) - sum((r["z_slack"] / 2 + r["E"] + r["F_slack"] for r in rows), F(0)) - tau * s_last - E_last - F_last
    threshold = (M - tau + F(1, 2)) * W + w / 2
    K_total = sum(r["K"] for r in rows)
    assert debt - threshold == M * (coverage - 2 * W) + K_total
    return dict(branch_after_T=branch, actual_path=path, W=W, optimal_coverage=coverage, utilities=utilities, tau=tau, rows=rows, last=dict(s=s_last, E=E_last, F_slack=F_last), debt=debt, payment_threshold=threshold, K_total=K_total, SPE_comparisons=3 * len(comparison_rows), full_node_rows=comparison_rows)


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


if __name__ == "__main__":
    first, second = audit("M"), audit("R")
    assert first["actual_path"] == second["actual_path"] == ("M", "R", "R")
    assert first["debt"] == second["debt"]
    assert first["rows"][0]["delta"] - second["rows"][0]["delta"] == F(1, 3)
    assert first["rows"][0]["s"] - second["rows"][0]["s"] == F(1, 3)
    report = dict(status="Exact mechanism witness; not a half-coverage counterexample", first=first, second=second)
    (HERE / "projected_debt_audit.json").write_text(json.dumps(encode(report), indent=2) + "\n")
    print(json.dumps({k: encode(v) for k, v in report.items() if k == "status"}))
    for r in (first, second):
        print(json.dumps(encode({k: r[k] for k in ("branch_after_T", "actual_path", "W", "optimal_coverage", "debt", "payment_threshold", "K_total", "SPE_comparisons")})))
