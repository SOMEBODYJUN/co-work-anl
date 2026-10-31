"""Exact definition-level audit of the general origin-retraction theorem.

Only established complete-SPE fixtures and boundary/tie policies are used.
No randomized non-SPE flow examples and no claim of universal success.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def audit(name, m, k, clients, policy, comparison, max_future=False):
    def finish(history):
        while len(history) < m:
            history += (policy(history),)
        return history

    def load(leaf, x):
        return sum(a in clients[x] for a in leaf)

    def profit(leaf, i):
        return sum((F(1, load(leaf, x)) for x in range(len(clients))
                    if leaf[i] in clients[x]), F())

    checks = 0
    for i in range(m):
        for history in product(range(k), repeat=i):
            prescribed = finish(history)
            for a in range(k):
                assert profit(prescribed, i) >= profit(finish(history + (a,)), i)
                checks += 1
    B = finish(())
    T = tuple(comparison)
    u = [profit(B, i) for i in range(m)]
    cb = [load(B, x) for x in range(len(clients))]
    ct = [load(T, x) for x in range(len(clients))]
    opt = max(sum(any(a in v for a in z) for v in clients)
              for z in combinations_with_replacement(range(k), m))
    assert sum(c > 0 for c in ct) == opt
    Hx = [[F() for _ in clients] for _ in range(m)]
    d = [F() for _ in range(m)]
    initial = defaultdict(F)
    currents = defaultdict(F)
    for i in range(m):
        W = finish(B[:i] + (T[i],))
        rows = []
        for x, v in enumerate(clients):
            if T[i] not in v:
                continue
            p = F(1, ct[x])
            delta = cb[x] + 1 - int(B[i] in v)
            pb = F()
            for l in range(m):
                if l != i and B[l] in v and T[l] not in v:
                    value = p / delta
                    Hx[l][x] += value
                    pb += value
            r = p - pb
            assert r >= 0
            edges = {j: min(p, F(1, delta)) / load(W, x)
                     for j in range(i + 1, m) if W[j] in v and B[j] not in v}
            q = sum(edges.values(), F())
            rows.append((x, r, q, edges))
        total = sum((r for x, r, q, edges in rows), F())
        available = sum((min(r, q) for x, r, q, edges in rows), F())
        sent = max(F(), total - u[i])
        assert sent <= available
        for x, r, q, edges in rows:
            amount = min(r, q) if max_future else (sent * min(r, q) / available if available else F())
            currents[i, x] = r - amount
            d[i] += r - amount
            for j, cap in edges.items():
                value = amount * cap / q
                assert value <= cap
                initial[i, W[:j], x] += value
        assert d[i] <= u[i]
    H = [sum(row, F()) for row in Hx]
    J = [F() for _ in range(m)]
    for x in range(len(clients)):
        if not cb[x]:
            continue
        mass = sum((value for (i, g, xx), value in initial.items() if xx == x), F())
        remain = [F(int(B[l] in clients[x]), cb[x]) - Hx[l][x] for l in range(m)]
        assert all(r >= 0 for r in remain)
        assert mass <= sum(remain, F())
        if mass:
            for l in range(m):
                J[l] += mass * remain[l] / sum(remain, F())
    for l in range(m):
        assert H[l] + J[l] <= u[l]

    def propagate(retained):
        incoming = defaultdict(F)
        b = [F() for _ in range(m)]
        for (i, g, x), value in initial.items():
            if not cb[x]:
                incoming[i, g, x] += value * (1 - retained[i])
                b[i] += value
        K = [[F() for _ in range(m)] for _ in range(m)]
        count_nodes = 0
        for l in range(m):
            keys = [key for key in incoming if len(key[1]) == l and incoming[key]]
            by_client = defaultdict(F)
            for i, g, x in keys:
                by_client[g, x] += incoming[i, g, x]
            for (g, x), mass in by_client.items():
                assert mass * load(finish(g), x) <= 1
            for i, g, x in keys:
                count_nodes += 1
                h = incoming[i, g, x]
                V = finish(g)
                A = finish(B[:l] + (V[l],))
                den = load(A, x)
                new = [j for j in range(l + 1, m)
                       if A[j] in clients[x] and V[j] not in clients[x]]
                K[i][l] += h * (den - len(new)) / den
                for j in new:
                    incoming[i, A[:j], x] += h / den
        for i in range(m):
            assert sum(K[i], F()) == (1 - retained[i]) * b[i]
            assert all(K[i][j] == 0 for j in range(i + 1))
        return b, K, count_nodes

    b, K, nodes = propagate([F() for _ in range(m)])
    base = [d[l] + H[l] + J[l] for l in range(m)]
    cost = [base[l] + sum((K[i][l] for i in range(l)), F()) for l in range(m)]
    assert sum(cost, F()) == opt
    cap = [2 * value for value in u]
    s = [cap[i] - cost[i] for i in range(m)]
    t = [[K[i][l] / b[i] if b[i] else F() for l in range(m)] for i in range(m)]
    y = [F() for _ in range(m)]
    failure = None
    z_at_failure = None
    for l in range(m):
        z = s[l] + sum((t[i][l] * y[i] for i in range(l)), F())
        if z < 0:
            failure = l
            z_at_failure = z
            break
        y[l] = min(b[l], z)
    dual = None
    if failure is not None:
        lam = [F() for _ in range(m)]
        lam[failure] = F(1)
        for i in reversed(range(failure)):
            q = sum((lam[l] * t[i][l] for l in range(i + 1, m)), F())
            lam[i] = q if y[i] < b[i] else F()
        dual_value = sum((lam[l] * s[l] for l in range(m)), F())
        for i in range(m):
            q = sum((lam[l] * t[i][l] for l in range(i + 1, m)), F())
            dual_value += b[i] * max(F(), q - lam[i])
        assert dual_value == z_at_failure < 0
        dual = {"lambda": list(map(str, lam)), "cut": str(dual_value)}
    theta = [y[i] / b[i] if b[i] else F() for i in range(m)]
    _, scaled, _ = propagate(theta)
    for i in range(m):
        for l in range(m):
            assert scaled[i][l] == (1 - theta[i]) * K[i][l]
    changed = [base[l] + y[l] + sum((scaled[i][l] for i in range(l)), F())
               for l in range(m)]
    for l in range(m):
        assert changed[l] == cost[l] + y[l] - sum((t[i][l] * y[i] for i in range(l)), F())
    assert sum(changed, F()) == opt
    if failure is None:
        assert all(changed[l] <= cap[l] for l in range(m))
        assert opt <= 2 * sum(u, F())
    return {"name": name, "m": m, "topics": k, "unit_clients": len(clients),
            "complete_history_IC_checks": checks, "B": B, "T": T, "OPT": opt,
            "u": list(map(str, u)), "base": list(map(str, base)),
            "R_source": list(map(str, b)), "tagged_R_nodes": nodes,
            "K": [list(map(str, row)) for row in K],
            "original_cost": list(map(str, cost)), "retained": list(map(str, y)),
            "new_cost": list(map(str, changed)), "cap": list(map(str, cap)),
            "first_failure": failure, "failure_dual": dual}


def main():
    fixture = ROOT / "research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json"
    raw = json.loads(fixture.read_text())
    instance = raw["instance"]
    clients = [set(z["topics"]) for z in instance["customers"] for _ in range(z["multiplicity"])]
    table = {tuple(row["history"]): row["action"] for row in raw["certificate"]["actions"]}
    rows = [audit("unchanged_348_unit_complete_SPE", instance["players"],
                  len(instance["topics"]), clients, lambda g: table[g], (5, 2, 4))]
    active_fixture = ROOT / "research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json"
    active = json.loads(active_fixture.read_text())
    active_instance = active["instance"]
    active_clients = [set(z["topics"]) for z in active_instance["customers"]
                      for _ in range(z.get("multiplicity", 1))]
    active_table = {tuple(row["history"]): row["action"]
                    for row in active["certificate"]["actions"]}
    rows.append(audit("unchanged_52_unit_complete_SPE_max_future", active_instance["players"],
                      len(active_instance["topics"]), active_clients,
                      lambda g: active_table[g], (0, 1, 4, 5), max_future=True))
    # Established sharp all-big family, plus a legal empty action. This tests
    # the general construction at m=5, not a new five-player result.
    m = 5
    clients = [{0} for _ in range(m)] + [{j} for j in range(1, m)]
    rows.append(audit("m5_existing_all_big_with_empty", m, m + 1, clients,
                      lambda g: 0, tuple(range(m))))
    rows.append(audit("zero_customers_empty_catalogue", 5, 1, [],
                      lambda g: 0, (0,) * 5))
    rows.append(audit("full_theme_and_empty", 5, 2, [{0}, {0}, {0}],
                      lambda g: 0, (0,) * 5))
    # Tiny tie fixture: the tie selector explicitly uses ordered histories,
    # and equal-count permutations need not prescribe the same action.
    tie_m, tie_k = 5, 3
    tie_clients = [{0}, {1}]
    tie_table = {}
    def tie_finish(g):
        while len(g) < tie_m:
            g += (tie_table[g],)
        return g
    for depth in reversed(range(tie_m)):
        for g in product(range(tie_k), repeat=depth):
            values = []
            for a in range(tie_k):
                leaf = tie_finish(g + (a,))
                values.append(sum((F(1, sum(z in v for z in leaf))
                                   for v in tie_clients if a in v), F()))
            best = [a for a in range(tie_k) if values[a] == max(values)]
            index = sum((i + 1) * (a + 1) for i, a in enumerate(g)) % len(best)
            tie_table[g] = best[index]
    assert tie_table[0, 0, 1, 1] != tie_table[0, 1, 0, 1]
    rows.append(audit("complete_order_sensitive_tie_policy", tie_m, tie_k,
                      tie_clients, lambda g: tie_table[g], (0, 1, 0, 1, 0)))
    output = {"scope": "Exact audits of two fixed existing SPEs and boundary/tie policies; no universal success claim.",
              "fixture_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
              "active_fixture_sha256": hashlib.sha256(active_fixture.read_bytes()).hexdigest(),
              "audits": rows, "status": "passed"}
    path = HERE / "origin_retraction_exact_audit.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
