"""Exact affine two-type verification; no floating LP is used.

Run from the repository root:
  python research/weighted_congestion_frontier/assets/R2/multiscale_bridge/verify_affine_two_type.py

This finite regression checks the analytic construction, not the general theorem.
"""

from fractions import Fraction as Q


def potential(m, n, a, b, ha, hb, k):
    qa, qb = ha / a, hb / b
    assert qa <= qb and k * k == qb / qa
    A, B, D = m * a, n * b, k * k
    if A >= k * B:
        core = A * A / 2 + D * A * B + D * B * B / 2
    else:
        core = k * A * A / 2 + k * A * B + k**3 * B * B / 2
    return qa * core + (m * ha * a + n * hb * b) / 2


def verify_marginals(a, b, ha, hb, k, M, N):
    checked = 0
    ratios = []
    for m in range(M + 1):
        for n in range(N + 1):
            value = potential(m, n, a, b, ha, hb, k)
            load = m * a + n * b
            if m:
                delta = value - potential(m - 1, n, a, b, ha, hb, k)
                target = ha * load
                assert target <= delta <= k * target, (m, n, "a", delta, target)
                ratios.append(delta / target)
                checked += 1
            if n:
                delta = value - potential(m, n - 1, a, b, ha, hb, k)
                target = hb * load
                assert target <= delta <= k * target, (m, n, "b", delta, target)
                ratios.append(delta / target)
                checked += 1
    return checked, min(ratios), max(ratios)


def maximal_subset_path_ratio(a, b, ha, hb, M, N):
    best = (Q(1), (0, 0))
    for m in range(1, M + 1):
        for n in range(1, N + 1):
            base = ha * a * m * (m + 1) / 2 + hb * b * n * (n + 1) / 2
            ratio = (base + hb * a * m * n) / (base + ha * b * m * n)
            if ratio > best[0]:
                best = ratio, (m, n)
    return best


def main():
    cases = [
        (Q(1), Q(1, 16), Q(1), Q(1, 4), Q(2), 8, 128),
        (Q(3), Q(2, 7), Q(6), Q(36, 7), Q(3), 11, 43),
        (Q(2), Q(3), Q(4), Q(6), Q(1), 13, 17),
        (Q(5, 3), Q(2, 5), Q(10, 3), Q(9, 5), Q(3, 2), 19, 31),
    ]
    total = 0
    for args in cases:
        count, lower, upper = verify_marginals(*args)
        total += count
        print(f"marginals k={args[4]} counts={args[5:]} checked={count} ratio_range=[{lower},{upper}]")

    expected = [
        (1, 16, Q(51, 29), (1, 11)),
        (2, 32, Q(521, 281), (2, 20)),
        (4, 64, Q(1805, 941), (4, 36)),
        (8, 128, Q(6677, 3413), (8, 68)),
    ]
    for M, N, ratio, subset in expected:
        actual = maximal_subset_path_ratio(Q(1), Q(1, 16), Q(1), Q(1, 4), M, N)
        assert actual == (ratio, subset), (actual, ratio, subset)
        print(f"subset path M={M},N={N}: ratio={ratio}, terminal={subset}")
    print(f"PASS: {total} exact marginal inequalities; four exact subset-path scans.")


if __name__ == "__main__":
    main()
