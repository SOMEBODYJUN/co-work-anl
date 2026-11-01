#!/usr/bin/env python3
"""New, finite Fraction audit; never imports or runs the historical LP code.

The frozen JSON remains a floating record.  This script proposes small rational
coefficients, then certifies them independently on a precisely defined policy.
The observed current replay is used only for the separate policy-identity check.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/structured_packing_6.json"
EXPECTED_SHA = "6ae7857876244ad2286a57ac49c1548748b6287b20995edb3027eb80e6d68719"
OBSERVED = HERE.parent / "structured-packing-scanner/rerun/observed_6.json"
raw = SOURCE.read_bytes()
assert sha256(raw).hexdigest() == EXPECTED_SHA
data = json.loads(raw)
assert data["n"] == 6 and set(data) == {"n", "ratio", "w", "dual"}
N, K = 6, 8
T = tuple(range(2, K))
PRIORITY = (1, 0) + T
MASKS = tuple(range(1, 1 << K))


def rational(x):
    # This is a candidate proposal, not an assertion that rounding proves it.
    p = F(str(x)).limit_denominator(60)
    assert abs(p - F(str(x))) < F(1, 10**12)
    return p


weights = {int(m): rational(v) for m, v in data["w"]}
assert weights == {1: F(1)} | {m: F(5, 6) for j in T for m in (1 << j, (1 << j) | 2)}
integer_weights = {m: 6 * v for m, v in weights.items()}
assert all(v.denominator == 1 for v in integer_weights.values())
assert sum(weights.values()) == 11 and sum(integer_weights.values()) == 66
target = rational(data["ratio"])
assert target == F(5, 3)
seed = {}
for j in T:
    seed[1 << j] = F(4)
    seed[(1 << j) | 2] = F(4)
    seed[(1 << j) | (1 if j < 7 else 3)] = F(1 if j < 7 else 5)


def bump(q, a):
    c = list(q)
    c[a] += 1
    return tuple(c)


def coefficient(c, a, m):
    if not (m >> a) & 1:
        return F(0)
    d = sum(c[b] for b in range(K) if (m >> b) & 1)
    # Called only for an actual action in the corresponding terminal.
    assert d > 0
    return F(1, d)


@lru_cache(None)
def payoff(c, a, which):
    w = seed if which == "seed" else weights
    return sum((v * coefficient(c, a, m) for m, v in w.items()), F(0))


@lru_cache(None)
def action(q):
    assert sum(q) < N
    if sum(q) < N - 1:
        return 0 if q[1] == sum(q) else 1
    # Exact maximization, with the source's first-maximum priority.
    return max(PRIORITY, key=lambda a: payoff(bump(q, a), a, "seed"))


@lru_cache(None)
def terminal(q):
    return q if sum(q) == N else terminal(bump(q, action(q)))


def compositions(total, slots):
    if slots == 1:
        yield (total,)
        return
    for a in range(total + 1):
        for tail in compositions(total - a, slots - 1):
            yield (a,) + tail


states = tuple(q for level in range(N) for q in compositions(level, K))
root = (0,) * K
c0 = terminal(root)
assert c0 == (1, 5, 0, 0, 0, 0, 0, 0)
assert action(root) == 0 and payoff(c0, 0, "candidate") == 1
slack_hist = Counter()
seed_min = None
row_count = 0
for q in states:
    a = action(q)
    c = terminal(q)
    for b in range(K):
        d = terminal(bump(q, b))
        s = payoff(c, a, "candidate") - payoff(d, b, "candidate")
        ss = payoff(c, a, "seed") - payoff(d, b, "seed")
        assert s >= 0 and ss >= 0, (q, a, b, s, ss)
        slack_hist[s] += 1
        seed_min = ss if seed_min is None else min(seed_min, ss)
        row_count += 1
assert len(states) == comb(13, 8) == 1287 and row_count == 10296

# The ordered strategy is sigma(h)=action(count(h)).  Enumerate every ordered
# history to verify coverage of this stated lift; this is not a quotient theorem
# about arbitrary history-dependent strategies.
ordered_counts = Counter()
ordered_comparisons = 0
for level in range(N):
    for h in product(range(K), repeat=level):
        q = tuple(h.count(a) for a in range(K))
        assert action(q) in range(K)
        ordered_counts[q] += 1
        ordered_comparisons += K
assert set(ordered_counts) == set(states)
assert sum(ordered_counts.values()) == 37449
assert ordered_comparisons == 299592


def pack(j, m):
    return int(not (m & 1) and bool(m & (1 << j))
               and sum(bool(m & (1 << b)) for b in T) == 1)


packs = [sum((v * pack(j, m) for m, v in weights.items()), F(0)) for j in T]
assert packs == [target] * N
dual_ic, dual_pack = [], {}
for rowid, marginal in data["dual"]:
    value = -rational(marginal)
    assert value > 0
    if rowid[0] == "pack":
        dual_pack[int(rowid[1])] = value
    else:
        q, b = tuple(rowid[0]), int(rowid[1])
        assert q in states and b in range(K)
        dual_ic.append((q, b, value))
assert len(dual_ic) == 9 and dual_pack == {i: F(1, 6) for i in range(6)}
assert sum(dual_pack.values()) == 1
residual = {}
for m in MASKS:
    r = target * coefficient(c0, 0, m)
    for q, b, v in dual_ic:
        r -= v * (coefficient(terminal(q), action(q), m)
                  - coefficient(terminal(bump(q, b)), b, m))
    r -= sum((v * pack(T[j], m) for j, v in dual_pack.items()), F(0))
    assert r >= 0, (m, r)
    residual[m] = r
assert all(residual[m] == 0 for m in weights)
assert all(payoff(terminal(q), action(q), "candidate") ==
           payoff(terminal(bump(q, b)), b, "candidate") for q, b, _ in dual_ic)


def coverage(labels):
    bits = sum(1 << a for a in set(labels))
    return sum((v for m, v in weights.items() if m & bits), F(0))


choices = tuple(combinations(range(K), N))
opt = max(map(coverage, choices))
optimizers = [list(c) for c in choices if coverage(c) == opt]
path, q = [], root
while sum(q) < N:
    a = action(q)
    path.append(a)
    q = bump(q, a)
welfare = coverage(path)
assert welfare == 6 and opt == 10 and coverage(T) == opt
assert sum(payoff(c0, a, "candidate") for a in path) == welfare
child_opt = max(coverage((0,) + c) for c in combinations(range(K), N - 1))
assert child_opt == F(28, 3) and opt - child_opt == F(2, 3)

# Compare to the current unmodified historical entry-point run, not to an
# unrecorded historical policy: the old sparse JSON has no full moves table.
observed_bytes = OBSERVED.read_bytes()
observed = json.loads(observed_bytes)
observed_policy = {tuple(q): a for q, a in observed["moves"]}
assert observed_policy == {q: action(q) for q in states}
expected_rows = {(q, b) for q in states for b in range(K)}
assert {(tuple(q), b) for q, b in observed["rowids"]} == expected_rows
assert len(observed["rowids"]) == row_count

certificate = {
    "status": "new_exact_finite_certificate_not_original_json",
    "n": N, "label_order": ["A", "B", "T1", "T2", "T3", "T4", "T5", "T6"],
    "target": str(target), "weights": [[m, str(v)] for m, v in weights.items()],
    "dual_ic_positive_multipliers": [[list(q), b, str(v)] for q, b, v in dual_ic],
    "dual_pack_positive_multipliers": [[j, str(v)] for j, v in dual_pack.items()],
    "dual_coefficient_residual_all_255_types": [[m, str(v)] for m, v in residual.items()],
    "exact_policy": [[list(q), action(q)] for q in states],
}
certificate_bytes = (json.dumps(certificate, indent=2, ensure_ascii=False) + "\n").encode()
(HERE / "exact_certificate.json").write_bytes(certificate_bytes)
report = {
    "status": "all_exact_checks_passed",
    "scope": "one six-player eight-label count policy, all 255 nonempty customer types; no universal half-coverage theorem",
    "source_sha256": EXPECTED_SHA, "source_size": len(raw),
    "observed_current_replay_sha256": sha256(observed_bytes).hexdigest(),
    "exact_certificate_sha256": sha256(certificate_bytes).hexdigest(),
    "source_float_proposal_max_error": str(max(abs(F(str(v)) - weights[m]) for m, v in data["w"])),
    "root_terminal": list(c0), "root_path": path, "root_payoff": "1",
    "minimum_block": str(target), "fixed_policy_lp_exact_optimum": str(target),
    "rational_customer_mass": "11", "integer_scale": 6, "integer_customers": 66,
    "integer_customer_types": [[m, int(v)] for m, v in integer_weights.items()],
    "welfare": str(welfare), "opt6": str(opt), "welfare_over_opt6": str(welfare / opt),
    "five_slot_optimum_after_A": str(child_opt), "root_opportunity_loss": str(opt - child_opt),
    "six_distinct_theme_sets_checked": len(choices), "optimal_six_sets": optimizers,
    "count_decision_states": len(states), "ic_rows_including_self": row_count,
    "ordered_histories_explicitly_enumerated": sum(ordered_counts.values()),
    "ordered_comparisons_represented_by_verified_count_rows": ordered_comparisons,
    "seed_minimum_ic_slack": str(seed_min),
    "candidate_minimum_ic_slack": str(min(slack_hist)),
    "candidate_tight_ic_rows_including_self": slack_hist[F(0)],
    "candidate_ic_slack_histogram": [[str(s), count] for s, count in sorted(slack_hist.items())],
    "packing_rows": 6, "packing_slacks": ["0"] * 6,
    "dual_ic_nonzero": len(dual_ic), "dual_pack_nonzero": len(dual_pack),
    "dual_residual_zero_columns": sum(r == 0 for r in residual.values()),
    "dual_residual_positive_columns": sum(r > 0 for r in residual.values()),
    "dual_residual_minimum": str(min(residual.values())),
    "dual_residual_maximum": str(max(residual.values())),
    "dual_residual_histogram": [[str(s), count] for s, count in sorted(Counter(residual.values()).items())],
    "current_replay_policy_matches_exact_policy": True,
    "caveat": "Small-denominator reconstruction was a proposal; exact nonnegativity, normalization, dual identity, and policy checks supply the new proof. The sparse historical JSON alone lacks the policy, equality multiplier, and bound residuals.",
}
(HERE / "exact_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k: v for k, v in report.items() if "histogram" not in k}, ensure_ascii=False))
