"""New, standard-library exact audit of the frozen n=5 packing proposal.

No optimization or original research module is imported.  The specified seed
policy is rebuilt with Fraction; an optional captured floating policy can be
compared separately.  All reporting distinguishes exact reconstructions from
the old JSON decimal and binary-float inputs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb, factorial, prod
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
N, K = 5, 7
MASKS = tuple(range(1, 1 << K))


def compositions(total, k):
    if k == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, k - 1):
            yield (first,) + rest


STATES = tuple(q for d in range(N) for q in compositions(d, K))


def add(q, a):
    return tuple(v + (i == a) for i, v in enumerate(q))


def share(mask, a, c):
    if not mask & (1 << a):
        return F(0)
    den = sum(v for i, v in enumerate(c) if mask & (1 << i))
    assert den > 0
    return F(1, den)


def payoff(w, a, c):
    return sum((value * share(mask, a, c) for mask, value in w.items()), F(0))


SEED = {}
for j in range(N):
    leaf = 1 << (j + 2)
    SEED[leaf] = SEED[leaf | 2] = F(N - 2)
    SEED[leaf | (1 if j < N - 1 else 3)] = F(1 if j < N - 1 else N - 1)


def exact_action(q):
    if sum(q) < N - 1:
        return 0 if q[1] == sum(q) else 1
    # Python max keeps the first maximizer in the explicit priority sequence.
    return max([1, 0, *range(2, K)], key=lambda a: payoff(SEED, a, add(q, a)))


POLICY = {q: exact_action(q) for q in STATES}


@lru_cache(None)
def terminal(q):
    if sum(q) == N:
        return q
    return terminal(add(q, POLICY[q]))


def row(q, b):
    a = POLICY[q]
    actual, dev = terminal(q), terminal(add(q, b))
    return tuple(share(mask, a, actual) - share(mask, b, dev) for mask in MASKS)


ROWS = {(q, b): row(q, b) for q in STATES for b in range(K)}
ZERO = (0,) * K
ROOT = terminal(ZERO)
U = tuple(share(mask, 0, ROOT) for mask in MASKS)
E = tuple(tuple(F(not (mask & 1) and bool(mask & (1 << j))
                         and sum(bool(mask & (1 << a)) for a in range(2, K)) == 1)
                for mask in MASKS) for j in range(2, K))


def dot(row_, w):
    return sum((row_[mask - 1] * value for mask, value in w.items()), F(0))


def weights(raw, convert):
    return {int(mask): convert(value) for mask, value in raw["w"]}


def audit_point(w, t):
    slack = [(dot(r, w), q, b) for (q, b), r in ROWS.items()]
    bad = [(s, q, b) for s, q, b in slack if s < 0]
    minimum, mq, mb = min(slack)
    blocks = [dot(e, w) for e in E]
    root_u = dot(U, w)
    cov = lambda support: sum((v for mask, v in w.items()
                              if any(mask & (1 << a) for a in support)), F(0))
    coverage = [(cov(support), support) for support in combinations(range(K), N)]
    opt = max(v for v, _ in coverage)
    actual_w = cov([a for a in range(K) if ROOT[a]])
    completion = max(cov((0,) + support) for support in combinations(range(K), N - 1))
    return {
        "all_nonnegative": all(v >= 0 for v in w.values()),
        "root_u": str(root_u), "root_normalization_error": str(root_u - 1),
        "claimed_t": str(t), "relative_blocks": list(map(str, blocks)),
        "pack_slacks": [str(v - t) for v in blocks],
        "actual_block_over_root": str(min(blocks) / root_u),
        "minimum_ic": str(minimum), "minimum_ic_at": [list(mq), mb],
        "negative_ic_count": len(bad),
        "negative_ic": [[list(q), b, str(s)] for s, q, b in bad],
        "root_terminal": list(ROOT), "root_W": str(actual_w),
        "OPT_5": str(opt), "OPT_over_W": str(opt / actual_w),
        "optimal_supports": [list(s) for v, s in coverage if v == opt],
        "root_topic_sizes": [str(cov([a])) for a in range(K)],
        "actual_player_utilities": [str(payoff(w, a, ROOT))
                                    for a in range(K) for _ in range(ROOT[a])],
        "best_four_topic_completion_after_A": str(completion),
        "first_coverage_loss": str(opt - completion),
        "first_loss_minus_root_utility": str(opt - completion - root_u),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--captured-policy", type=Path)
    args = parser.parse_args()
    source_path = HERE / "original.json"
    source = source_path.read_bytes()
    assert len(source) == 955
    assert hashlib.sha256(source).hexdigest() == "fba7d40d0654ca25257cd54f414954c62f2be0817462d06964127a5a2762d299"
    raw_decimal = json.loads(source, parse_float=F)
    raw_float = json.loads(source)
    assert set(raw_float) == {"n", "ratio", "w", "dual"}
    assert raw_float["n"] == N
    assert len(raw_float["w"]) == 11 and len(raw_float["dual"]) == 14
    exact_w = weights(raw_decimal, lambda x: F(x).limit_denominator(1000))
    assert exact_w == {1: F(1), **{mask: F(4, 5) for j in range(2, K)
                                             for mask in (1 << j, (1 << j) | 2)}}
    beta = F(8, 5)
    exact = audit_point(exact_w, beta)
    assert exact["minimum_ic"] == "0" and exact["negative_ic_count"] == 0
    assert exact["root_u"] == "1" and set(exact["pack_slacks"]) == {"0"}

    # Recover only the displayed support, then prove the certificate afresh.
    ic_multipliers, pack = {}, {}
    for key, value in raw_decimal["dual"]:
        multiplier = -F(value).limit_denominator(1000)
        assert multiplier >= 0
        if key[0] == "pack":
            pack[key[1]] = multiplier
        else:
            q, b = tuple(key[0]), key[1]
            assert (q, b) in ROWS
            ic_multipliers[q, b] = multiplier
    assert sum(pack.values()) == 1
    residual = [beta * U[i]
                - sum(v * ROWS[key][i] for key, v in ic_multipliers.items())
                - sum(v * E[j][i] for j, v in pack.items())
                for i in range(len(MASKS))]
    assert min(residual) >= 0
    assert dot(residual, exact_w) == 0
    assert all(dot(ROWS[key], exact_w) == 0 for key in ic_multipliers)

    # Explicitly traverse the ordered tree in addition to count-state checking.
    ordered_nodes = ordered_checks = 0
    for depth in range(N):
        for history in product(range(K), repeat=depth):
            ordered_nodes += 1
            q = tuple(history.count(a) for a in range(K))
            assert q in POLICY
            actual = list(history)
            while len(actual) < N:
                cq = tuple(actual.count(a) for a in range(K))
                actual.append(POLICY[cq])
            ac = tuple(actual.count(a) for a in range(K))
            for b in range(K):
                deviating = list(history) + [b]
                while len(deviating) < N:
                    cq = tuple(deviating.count(a) for a in range(K))
                    deviating.append(POLICY[cq])
                dc = tuple(deviating.count(a) for a in range(K))
                gap = payoff(exact_w, actual[depth], ac) - payoff(exact_w, b, dc)
                assert gap >= 0 and gap == dot(ROWS[q, b], exact_w)
                ordered_checks += 1
    assert ordered_nodes == 2801 and ordered_checks == 19607
    assert sum(factorial(sum(q)) // prod(factorial(v) for v in q)
               for q in STATES) == ordered_nodes

    report = {
        "status": "new exact reconstruction; old floats separately audited",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "n": N, "k": K, "types": len(MASKS),
        "count_nodes_by_depth": [comb(d + K - 1, K - 1) for d in range(N)],
        "count_nodes": len(STATES), "ic_rows_including_self": len(ROWS),
        "ordered_nodes_explicitly_checked": ordered_nodes,
        "ordered_comparisons_explicitly_checked": ordered_checks,
        "policy_action_frequencies": {str(a): list(POLICY.values()).count(a) for a in range(K)},
        "seed_minimum_ic": str(min(dot(r, SEED) for r in ROWS.values())),
        "decimal": audit_point(weights(raw_decimal, F), F(raw_decimal["ratio"])),
        "binary_float": audit_point(weights(raw_float, F), F(raw_float["ratio"])),
        "reconstructed": exact,
        "integer_scale": 5, "integer_customer_count": 45,
        "integer_types": [[mask, int(v * 5)] for mask, v in exact_w.items()],
        "dual": {
            "beta": str(beta), "sum_pack": str(sum(pack.values())),
            "IC_multipliers": [[list(q), b, str(v)] for (q, b), v in ic_multipliers.items()],
            "pack_multipliers": [[j, str(v)] for j, v in pack.items()],
            "residual_min": str(min(residual)),
            "residual_zero_count": residual.count(F(0)),
            "residual_positive_count": sum(v > 0 for v in residual),
            "all_127_residuals": [[mask, str(v)] for mask, v in zip(MASKS, residual)],
        },
    }
    if args.captured_policy:
        captured = json.loads(args.captured_policy.read_text())
        if isinstance(captured, dict):
            captured = captured["moves"]
        observed = {tuple(q): a for q, a in captured}
        assert observed == POLICY
        report["captured_original_float_policy"] = {
            "path": str(args.captured_policy),
            "sha256": hashlib.sha256(args.captured_policy.read_bytes()).hexdigest(),
            "all_330_actions_equal": True,
        }
    (HERE / "policy-exact.json").write_text(json.dumps([[list(q), a] for q, a in POLICY.items()], indent=2) + "\n")
    (HERE / "exact-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "count_nodes", "ic_rows_including_self", "ordered_nodes_explicitly_checked", "reconstructed")}, indent=2))


if __name__ == "__main__":
    main()
