"""Independent stdlib audit of a StrongA-only counterexample.

No canonical solver, cone, scipy, or verifier import. Integer multiplicities
encode distinct unit clients. All histories and all ordered optimal comparison
tuples at this ONE input are checked. This proves no universal upper bound.
"""
from pathlib import Path
from itertools import product, combinations
from functools import lru_cache
from fractions import Fraction
from math import lcm
import hashlib, json

HERE = Path(__file__).resolve().parent


def audit():
    raw = (HERE / "strong_adjacent_gap_attack.json").read_bytes()
    r = json.loads(raw)
    ins = r["endpoint"]
    p, m = len(ins["topics"]), ins["players"]
    scale = lcm(*range(1, m + 2))
    types = tuple((frozenset(c["topics"]), c["multiplicity"])
                  for c in ins["customers"])
    assert all(isinstance(w, int) and w > 0 for _, w in types)
    actions = {}
    for item in r["strategy"]["actions"]:
        h = tuple(item["history"])
        assert h not in actions
        actions[h] = item["action"]
    expected = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert set(actions) == expected and all(a in range(p) for a in actions.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))

    @lru_cache(None)
    def counts(z):
        return tuple(z.count(a) for a in range(p))

    @lru_cache(None)
    def utility(q, a):
        v = 0
        for S, w in types:
            if a in S:
                d = sum(q[b] for b in S)
                assert d > 0 and scale % d == 0
                v += w * (scale // d)
        return v

    def welfare(topics):
        support = frozenset(topics)
        return sum(w for S, w in types if not support.isdisjoint(S))

    minimum, checked = None, 0
    for h, a in actions.items():
        baseline = utility(counts(terminal(h)), a)
        for b in range(p):
            if b == a:
                continue
            margin = baseline - utility(counts(terminal(h + (b,))), b)
            assert margin >= 0, (h, a, b, margin)
            minimum = margin if minimum is None else min(minimum, margin)
            checked += 1
    path = terminal(())
    q = counts(path)
    assert path == tuple(r["actual_path"])
    assert q == tuple(r["strategy"]["terminal_counts"])
    frozen = []
    for a in path:
        row = []
        for t in range(p):
            v = 0
            for S, w in types:
                if t in S:
                    d = 1 + sum(q[b] for b in S) - (a in S)
                    assert scale % d == 0
                    v += w * (scale // d)
            row.append(v)
        frozen.append(tuple(row))
    Q = Fraction(sum(max(row) for row in frozen), scale)
    Csum = Fraction(0)
    J = Fraction(0)
    for S, w in types:
        c = sum(q[a] for a in S)
        if c:
            J += Fraction(w, c + 1)
            losses = sum(a in S and b not in S for a, b in zip(path, path[1:]))
            Csum += Fraction(w * losses, c * (c + 1))
    W = welfare(path)
    OPT = max(welfare(JJ) for JJ in combinations(range(p), min(p, m)))
    gap = Q - W - Csum
    assert (W, OPT, Q, Csum, gap) == (
        r["W"], r["OPT"], Fraction(r["true_Q"]), Fraction(r["Csum"]),
        Fraction(r["true_signed_StrongA_gap"]))
    assert gap > 0 and OPT <= 2 * W

    @lru_cache(None)
    def coverage_support(support):
        return welfare(support)

    best = best_tuple = None
    optimal_tuples = 0
    for comparison in product(range(p), repeat=m):
        if coverage_support(tuple(sorted(set(comparison)))) != OPT:
            continue
        optimal_tuples += 1
        value = sum(frozen[i][a] for i, a in enumerate(comparison))
        if best is None or value < best:
            best, best_tuple = value, comparison
    weak_Q = Fraction(best, scale)
    return {"scope": "independent exact StrongA counterexample; one-point weak-candidate test",
            "packet_sha256": hashlib.sha256(raw).hexdigest(), "m": m, "topics": p,
            "client_count": sum(w for _, w in types), "customer_types": len(types),
            "decision_histories": len(actions), "nonself_IC": checked,
            "minimum_IC_margin": str(Fraction(minimum, scale)), "actual_path": path,
            "W": W, "OPT": OPT, "Q": str(Q), "Csum": str(Csum), "J": str(J),
            "Q-W-Csum": str(gap), "refutes_StrongA": True, "refutes_HALF": False,
            "optimal_ordered_tuples_checked": optimal_tuples,
            "minimum_optimal_assignment": best_tuple, "minimum_optimal_Q": str(weak_Q),
            "minimum_optimal_Q-W-Csum": str(weak_Q - W - Csum),
            "refutes_some_optimal_assignment_weakening": weak_Q > W + Csum,
            "universal_bound_proved": False}


if __name__ == "__main__":
    out = HERE / "strong_adjacent_independent_audit.json"
    if out.exists():
        raise FileExistsError(out)
    result = audit()
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
