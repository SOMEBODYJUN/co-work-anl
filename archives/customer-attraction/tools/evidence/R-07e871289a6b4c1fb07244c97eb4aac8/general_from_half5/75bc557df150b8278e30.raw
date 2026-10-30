#!/usr/bin/env python3
"""Exact parameter tests for scalable CAG certificate infrastructure.

This checks compression identities and a legal local projection compiler. It
does NOT claim a factor-two certificate for six or arbitrary providers.
Writes only the explicitly requested team report, never the five-player data.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, lcm
from pathlib import Path
import argparse
import json
import time


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for x in range(n + 1):
        for tail in compositions(n - x, k - 1):
            yield (x,) + tail


def sh(n, d):
    return F(n, d) if n else F(0)


def share_scale(m):
    # Includes the m/2 coefficient of a pair-to-coverage row if such a row is
    # added. Consecutive pair denominators divide lcm(1,...,m).
    return 2 * lcm(*range(1, m + 1))


def histogram_test(m, k):
    """All histograms, every possible background load, literal index sums."""
    types = tuple(product((0, 1), repeat=k))
    count_by_d = Counter()
    scale = share_scale(m)
    identities = 0
    for hist in compositions(m, len(types)):
        branches = [z for z, n in zip(types, hist) for _ in range(n)]
        d = sum(z[0] for z in branches)
        count_by_d[d] += 1
        for p in range(m - k + 1):
            floor = [scale // (p + sum(z[:-1]) + 1) for z in branches]
            own = [int(scale * sh(z[-1], p + sum(z))) for z in branches]
            # All and off-diagonal terminal ICs, literal source/query indices.
            literal_all = sum(own[i] - branches[j][0] * floor[i]
                              for i in range(m) for j in range(m))
            literal_off = sum(own[i] - branches[j][0] * floor[i]
                              for i in range(m) for j in range(m) if i != j)
            hist_all = m * sum(own) - d * sum(floor)
            hist_diagonal = sum(own[i] - branches[i][0] * floor[i]
                                for i in range(m))
            assert literal_all == hist_all
            assert literal_off == hist_all - hist_diagonal
            identities += 2
            if k < 2:
                continue
            a, g, h = [], [], []
            for z in branches:
                pref = p + sum(z[:-2])
                den = (pref + 1) * (pref + 2)
                assert scale % den == 0
                a.append(scale // (pref + 1))
                g.append(scale // den)
                h.append(int(scale * (sh(z[-2], p + sum(z))
                                       + sh(z[-1], p + sum(z))))
                         + z[-2] * g[-1])
            # Two legal query topics from the same target index j, i != j.
            literal_pair = sum(h[i] - (branches[j][-2] + branches[j][-1]) * a[i]
                               + branches[j][-2] * branches[j][-1] * g[i]
                               for i in range(m) for j in range(m) if i != j)
            n_u = sum(z[-2] for z in branches)
            n_v = sum(z[-1] for z in branches)
            n_uv = sum(z[-2] * z[-1] for z in branches)
            hist_pair = ((m - 1) * sum(h) - (n_u + n_v) * sum(a)
                         + sum((z[-2] + z[-1]) * aa for z, aa in zip(branches, a))
                         + n_uv * sum(g)
                         - sum(z[-2] * z[-1] * gg for z, gg in zip(branches, g)))
            assert literal_pair == hist_pair
            identities += 1
    q = 2 ** (k - 1)
    expected_by_d = {d: comb(d + q - 1, q - 1) * comb(m - d + q - 1, q - 1)
                     for d in range(m + 1)}
    assert dict(count_by_d) == expected_by_d
    expected = comb(m + 2 ** k - 1, 2 ** k - 1)
    assert sum(count_by_d.values()) == expected
    return dict(m=m, tail_width=k, all_histograms=expected,
                histograms_by_d=expected_by_d, integer_identities=identities,
                scale=scale, every_background_load=True)


def menu_test(m):
    scale = share_scale(m)
    identities = 0
    if m >= 2:
        # Every labelled T/L membership array, no quotient in this check.
        for branches in product(tuple(product((0, 1), repeat=2)), repeat=m):
            d = sum(t for t, _ in branches)
            ell = sum(l for _, l in branches)
            h = sum(t * l for t, l in branches)
            for p in range(m - 1):
                literal = sum(int(scale * (sh(li, p + ti + li)
                                           - sh(lj, p + ti + 1)))
                              for ti, li in branches for _, lj in branches)
                assert literal == scale * F(d * ell - m * h, (p + 1) * (p + 2))
                identities += 1
    corner_objectives = 0
    for d in range(m + 1):
        full = [(h + z, h) for h in range(d + 1) for z in range(m - d + 1)]
        corners = [(0, 0), (d, d), (m - d, 0), (m, d)]
        for aa, bb in product(range(-3, 4), repeat=2):
            assert max(aa * ell + bb * h for ell, h in full) == max(
                aa * ell + bb * h for ell, h in corners)
            corner_objectives += 1
    return dict(literal_menu_V_identities=identities,
                full_integer_menu_affine_objectives=corner_objectives,
                penultimate_menu_skipped_because_m1=(m == 1))


def projection_weights(r, variant=1):
    """Any nonnegative weights are legal; these are deterministic test choices."""
    if r == 0:
        return (), (), F(0)
    if r == 2:
        if variant == 0:
            return (F(1, 7), F(5, 21)), (F(0), F(1, 21)), F(2, 7)
        return (F(1, 8), F(1, 5)), (F(0), F(1, 20)), F(1, 4)
    return tuple(F(1, 5 + i) for i in range(r)), (F(0),) * (r - 1) + (F(1, 20),), F(1, 4)


def projected_expression(p, ell, t, q, hidden, alpha, beta, theta):
    z = p + t + sum(hidden)
    value = sh(t, z)
    value += sum(bb * f + aa * F(f, ell + 1)
                 for f, aa, bb in zip(hidden, alpha, beta))
    if hidden:
        value -= theta * (sh(hidden[-1], z)
                          - F(q, p + t + sum(hidden[:-1]) + 1))
    return value


def gamma(p, ell, t, q, r, variant=1):
    alpha, beta, theta = projection_weights(r, variant)
    return min(projected_expression(p, ell, t, q, hidden, alpha, beta, theta)
               for hidden in product((0, 1), repeat=r))


def projection_test(m):
    visible_states = hidden_states = 0
    minimum_credit = None
    for j in range(1, m + 1):
        r = m - j
        alpha, beta, theta = projection_weights(r)
        for p, ell, t, q in product(range(j), range(m), (0, 1), (0, 1)):
            credit = gamma(p, ell, t, q, r)
            minimum_credit = credit if minimum_credit is None else min(minimum_credit, credit)
            visible_states += 1
            for hidden in product((0, 1), repeat=r):
                z = p + t + sum(hidden)
                expression = projected_expression(p, ell, t, q, hidden, alpha, beta, theta)
                # Independent slack assembly. Formal visible R/U/K values are
                # arbitrary: this checks an algebraic identity, not positivity
                # of a single customer's IC contribution.
                rr, uu, kk = F(7, 3), F(11, 5), F(17)
                slack_sum = rr - sh(t, z)
                slack_sum += sum(bb * (kk - f) + aa * (uu - F(f, ell + 1))
                                 for f, aa, bb in zip(hidden, alpha, beta))
                if hidden:
                    slack_sum += theta * (sh(hidden[-1], z)
                                          - F(q, p + t + sum(hidden[:-1]) + 1))
                lhs = rr + sum(alpha) * uu + sum(beta) * kk
                assert lhs - expression == slack_sum
                assert expression >= credit
                hidden_states += 1
    return dict(all_player_positions=True, visible_projection_states=visible_states,
                literal_hidden_states=hidden_states,
                minimum_credit=str(minimum_credit),
                claimed_scope="local row identity and exhaustive hidden-bit elimination only")


def five_source_match(source):
    data = json.loads(source.read_text())
    comparisons = 0
    for variant in (0, 1):
        expected = data[variant]['gamma_ABCDTQ']
        for ix, bits in enumerate(product((0, 1), repeat=6)):
            a, b, c, d, t, q = bits
            computed = gamma(a + b, a + b + c + d, t, q, 2, variant)
            assert computed == F(expected[ix]), (variant, bits, computed, expected[ix])
            comparisons += 1
    # Retaining the same early player position at m=6 leaves THREE replies.
    # Add a first reply at zero price/cap weight and retain the priced last two.
    alpha, beta, theta = projection_weights(2)
    p = ell = q = 0
    t = 1
    old_credit = gamma(p, ell, t, q, 2)
    new_literal = projected_expression(p, ell, t, q, (1, 1, 1),
                                       (F(0),) + alpha, (F(0),) + beta, theta)
    assert old_credit == F(5, 8) and new_literal == F(9, 16) < old_credit
    return dict(exact_source_entries_reconstructed=comparisons,
                source=str(source),
                fixed_early_position_six_player_table_drift={
                    "p": 0, "ell": 0, "t": 1, "q": 0, "hidden": [1, 1, 1],
                    "five_player_credit": str(old_credit),
                    "six_player_literal_expression": str(new_literal),
                    "meaning": "old projected table cannot be copied to a longer tail; not an SPE counterexample"})


def frontier_counts(m):
    early = {"fixed_bits": 3 * m - 5,
             "external_cases": 2 ** (3 * m - 5) * (m + 1),
             "third_position_tail_histograms": comb(m + 2 ** (m - 2) - 1, 2 ** (m - 2) - 1),
             "second_position_tail_histograms": comb(m + 2 ** (m - 1) - 1, 2 ** (m - 1) - 1)}
    anchored = {"fixed_bits": m + 5, "external_cases": 2 ** (m + 5) * (m + 1),
                "three_bit_tail_histograms": comb(m + 7, 7),
                "four_bit_tail_histograms": comb(m + 15, 15)}
    return {"same_early_positions": early, "last_four_positions_anchored": anchored}


def cross_family_warning():
    # Equal histograms separately in two families do not determine a
    # same-index cross-family product, even with a common T marginal d.
    t, f = (0, 0), (1, 0)
    g_same, g_other = (1, 0), (0, 1)
    hf = sorted(zip(t, f))
    assert sorted(zip(t, g_same)) == sorted(zip(t, g_other)) == hf
    assert sum(a * b for a, b in zip(f, g_same)) == 1
    assert sum(a * b for a, b in zip(f, g_other)) == 0
    return {"m": 2, "d": 0, "F": f, "G_aligned": g_same,
            "G_crossed": g_other, "same_index_products": [1, 0],
            "meaning": "new cross-family same-index rows require joint moments or a joint histogram"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--m', nargs='+', type=int, default=[1, 2, 5, 6],
                        help='provider/comparison-index counts to test')
    parser.add_argument('--max-histogram-width', type=int, default=4,
                        help='enumerate all tail widths up to min(this,m)')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('six_certificate_parametric_report.json'))
    parser.add_argument('--five-source', type=Path,
                        default=Path(__file__).resolve().parents[5] / 'customer_attraction/proofs/half5_exact_v1/components/priced_player3.json')
    args = parser.parse_args()
    if not args.m or min(args.m) < 1 or args.max_histogram_width < 1:
        parser.error('m and max-histogram-width must be positive')
    start = time.perf_counter()
    tests = []
    for m in args.m:
        histograms = [histogram_test(m, k) for k in range(1, min(args.max_histogram_width, m) + 1)]
        tests.append(dict(m=m, histograms=histograms, menus=menu_test(m),
                          projection=projection_test(m)))
        print(json.dumps({"m": m, "passed": True, "seconds": round(time.perf_counter() - start, 3)}), flush=True)
    report = dict(status="PASSED_EXACT_INFRASTRUCTURE_TESTS", arithmetic="Python integers and Fraction",
                  factor_two_for_six_or_general_m_proved=False, tests=tests,
                  max_histogram_width=args.max_histogram_width,
                  five_source=five_source_match(args.five_source),
                  cross_family_moment_warning=cross_family_warning(),
                  search_frontier_counts={str(m): frontier_counts(m) for m in (5, 6)},
                  seconds=round(time.perf_counter() - start, 3))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({"status": report['status'], "seconds": report['seconds'], "output": str(args.output)}))


if __name__ == '__main__':
    main()
