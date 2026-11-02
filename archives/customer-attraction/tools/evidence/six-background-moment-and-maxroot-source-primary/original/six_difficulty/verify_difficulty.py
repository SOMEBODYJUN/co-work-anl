"""Independent exact diagnostics; no old proof code or solver is imported.

The DP is an arithmetic pricing experiment for a specified additive/pair row
architecture, not a six-player certificate or a claim of a new game inequality.
It compares against every weak-composition histogram at (m,k)=(5,4),(6,5).
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, islice, product
from math import comb, lcm
from pathlib import Path
import json
import time

import numpy as np


HERE = Path(__file__).resolve().parent


def q(n, d):
    return F(n, d) if n else F(0)


def hist_counts_by_dp(m, width):
    """Coefficient of (1-x)^(-2**(width-1))(1-y)^(-same).

    This is a separate knapsack recurrence, not a call to the binomial formula.
    """
    a = [[0] * (m + 1) for _ in range(m + 1)]
    a[0][0] = 1
    for t, *_ in product((0, 1), repeat=width):
        for used in range(1, m + 1):
            for ones in range(t, used + 1):
                a[used][ones] += a[used - 1][ones - t]
    return a[m]


def domain_counts(m, fixed, short, long):
    h = {}
    for k in {short, long}:
        g = [comb(d + 2**(k - 1) - 1, 2**(k - 1) - 1)
             * comb(m - d + 2**(k - 1) - 1, 2**(k - 1) - 1)
             for d in range(m + 1)]
        assert g == hist_counts_by_dp(m, k)
        assert sum(g) == comb(m + 2**k - 1, 2**k - 1)
        h[k] = g
    menus = [(d + 1) * (m - d + 1) for d in range(m + 1)]
    # Literal (ell,h) enumeration independently verifies each menu count.
    for d, expected in enumerate(menus):
        literal = [(ell, overlap) for ell in range(m + 1)
                   for overlap in range(m + 1)
                   if 0 <= overlap <= d and 0 <= ell - overlap <= m - d]
        assert len(literal) == expected
    full = 2**fixed * sum(h[short][d]**2 * h[long][d] * menus[d]**3
                         for d in range(m + 1))
    return dict(m=m, fixed_bits=fixed, short_width=short, long_width=long,
                outer_conditions=2**fixed * (m + 1),
                short_histograms=sum(h[short]), long_histograms=sum(h[long]),
                conditional_short=h[short], conditional_long=h[long],
                menu_states=menus, enlarged_full_type_count=full)


def projected(p, ell, t, query, alpha, beta, mu):
    values = []
    for hidden in product((0, 1), repeat=len(alpha)):
        z = p + t + sum(hidden)
        value = (q(t, z) + sum((b + a / (ell + 1)) * f
                               for a, b, f in zip(alpha, beta, hidden))
                 - mu * q(hidden[-1], z)
                 + mu * F(query, p + t + sum(hidden[:-1]) + 1))
        values.append((value, hidden))
    return min(values), values


def interface_example():
    alpha, beta, mu = (F(1, 8), F(1, 5)), (F(0), F(1, 20)), F(1, 4)
    old, values = projected(2, 5, 1, 1, alpha, beta, mu)
    moved, _ = projected(3, 5, 1, 1, alpha, beta, mu)
    repaired, _ = projected(2, 5, 1, 1, (F(0), *alpha), (F(0), *beta), mu)
    lhs = F(1, 6) + F(13, 40) * F(1, 6) + F(1, 20)
    assert (lhs, old[0], lhs - old[0]) == (F(13, 48), F(73, 240), -F(1, 30))
    assert moved[0] == repaired[0] == F(21, 80)
    assert lhs - repaired[0] == F(1, 120)
    B, C = F(94866177440, 2048362573), F(60732827017, 8193450292)
    maxroot = B / 6 - C
    assert maxroot == F(7533873829, 24580350876) < 1
    return dict(unique_strategy_reason="One legal action at every history",
                customers=1, catalogue_topics=1, players=6,
                W=1, OPT=1, each_payoff="1/6",
                old_rhs=str(old[0]), lhs=str(lhs), old_slack=str(lhs - old[0]),
                old_four_values=[dict(hidden=f, value=str(v)) for v, f in values],
                moved_rhs=str(moved[0]), repaired_rhs=str(repaired[0]),
                repaired_slack=str(lhs - repaired[0]),
                unchanged_maxroot_rhs=str(maxroot))


def compositions(n, bins):
    if bins == 1:
        yield (n,)
    else:
        for first in range(n + 1):
            for rest in compositions(n - first, bins - 1):
                yield (first, *rest)


def primitives(m, width):
    """A weighted sum of SOURCE, LAST-all, LAST-offdiag, PAIR and PC rows.

    Constants in fixed actual payoffs/K are omitted, as in any family pricing
    block. All row multipliers 7,11,13,17,19 are positive. PC's generic legal
    local table is generated afresh using literal follower bits.
    """
    p = m - width
    ell = m - 2
    alpha = (F(0),) * (width - 3) + (F(1, 8), F(1, 5))
    beta = (F(0),) * (width - 2) + (F(1, 20),)
    credit = {(t, query): projected(p, ell, t, query, alpha, beta, F(1, 4))[0][0]
              for t, query in product((0, 1), repeat=2)}
    all_bits = list(product((0, 1), repeat=width))
    rational = []
    for z in all_bits:
        t, first, x, y = z[0], z[1], z[-2], z[-1]
        total = p + sum(z)
        b = p + sum(z[:-2])
        last_share = q(y, total)
        D, A, G = F(1, p + sum(z[:-1]) + 1), F(1, b + 1), F(1, (b + 1) * (b + 2))
        H = q(x + y, total) + x * G
        local = (-7 * q(t, total) + (11 * m + 13 * (m - 1)) * last_share
                 + 13 * first * D + 17 * (m - 1) * H
                 + 17 * (x + y) * A - 17 * x * y * G
                 - 19 * credit[first, y])
        rational.append((local, D, A, G))
    scale = lcm(*(v.denominator for row in rational for v in row))
    table = [[int(v * scale) for v in row] for row in rational]
    return all_bits, table, scale


def local_score(row, nfirst, nx, ny, nxy):
    local, D, A, G = row
    return local - (11 * ny + 13 * nfirst) * D - 17 * (nx + ny) * A + 17 * nxy * G


def price_dp(m, width, bits, rows):
    """Condition only on query moments; keep no 2**width-bin histogram.

    Last two response bits define four groups. Their counts determine all
    PAIR moments. Condition on first-response total. Then each summand is
    local; unused middle bits are eliminated independently, and a cardinality
    DP keeps exact totals of t and first-response membership.
    """
    answer = [None] * (m + 1)
    outer_count = 0
    transitions = 0
    maximum_states = 0
    local_types = list(product((0, 1), repeat=2))
    for groupcounts in compositions(m, 4):
        nx = groupcounts[2] + groupcounts[3]
        ny = groupcounts[1] + groupcounts[3]
        nxy = groupcounts[3]
        groups = [g for g, n in enumerate(groupcounts) for _ in range(n)]
        for nfirst in range(m + 1):
            outer_count += 1
            candidates = {}
            for group, (x, y) in enumerate(product((0, 1), repeat=2)):
                for t, first in local_types:
                    candidates[group, t, first] = max(
                        local_score(row, nfirst, nx, ny, nxy)
                        for z, row in zip(bits, rows)
                        if (z[0], z[1], z[-2], z[-1]) == (t, first, x, y))
            dp = {(0, 0): 0}
            for index, group in enumerate(groups):
                nextdp = {}
                remaining = m - index - 1
                for (d, used_first), value in dp.items():
                    for t, first in local_types:
                        newfirst = used_first + first
                        if not newfirst <= nfirst <= newfirst + remaining:
                            continue
                        key = d + t, newfirst
                        candidate = value + candidates[group, t, first]
                        transitions += 1
                        if key not in nextdp or candidate > nextdp[key]:
                            nextdp[key] = candidate
                dp = nextdp
                maximum_states = max(maximum_states, len(dp))
            for (d, used_first), value in dp.items():
                assert used_first == nfirst
                if answer[d] is None or value > answer[d]:
                    answer[d] = value
    return answer, dict(outer_moment_cases=outer_count,
                        exact_integer_transitions=transitions,
                        maximum_live_dp_states=maximum_states)


def literal_objective(branches, p, scale, credit):
    """Independent double-index row reconstruction for a reported maximizer."""
    m = len(branches)
    share = lambda z, j: q(z[j], p + sum(z))
    result = -7 * sum(share(z, 0) for z in branches)
    for i, source in enumerate(branches):
        den = p + sum(source[:-1]) + 1
        b = p + sum(source[:-2])
        A, G = F(1, b + 1), F(1, (b + 1) * (b + 2))
        H = share(source, -2) + share(source, -1) + source[-2] * G
        for j, query in enumerate(branches):
            result += 11 * (share(source, -1) - F(query[-1], den))
            if i != j:
                result += 13 * (share(source, -1) - F(query[1], den))
                result += 17 * (H - (query[-2] + query[-1]) * A + query[-2] * query[-1] * G)
        result -= 19 * credit[source[1], source[-1]]
    assert (result * scale).denominator == 1
    return int(result * scale)


def price_all_histograms(m, width, bits, rows, scale):
    """Separate exhaustive enumeration, one tuple per histogram, in chunks."""
    a = np.asarray(bits, dtype=np.int64)
    c = np.asarray(rows, dtype=np.int64)
    # Explicit safe bound for every intermediate vector arithmetic operation.
    bound = m * max(abs(int(v)) for row in rows for v in row) * (1 + 100 * m)
    assert bound < 2**63
    answer = [None] * (m + 1)
    witnesses = [None] * (m + 1)
    count = 0
    iterator = combinations_with_replacement(range(len(bits)), m)
    while chunk := list(islice(iterator, 40000)):
        e = np.asarray(chunk, dtype=np.int64)
        branchbits = a[e]
        totals = branchbits.sum(axis=1)
        nfirst, nx, ny = totals[:, 1], totals[:, -2], totals[:, -1]
        nxy = (branchbits[:, :, -2] * branchbits[:, :, -1]).sum(axis=1)
        sums = c[e].sum(axis=1)
        values = (sums[:, 0] - (11 * ny + 13 * nfirst) * sums[:, 1]
                  - 17 * (nx + ny) * sums[:, 2] + 17 * nxy * sums[:, 3])
        for d in range(m + 1):
            ids = np.flatnonzero(totals[:, 0] == d)
            if not len(ids):
                continue
            idx = int(ids[np.argmax(values[ids])])
            value = int(values[idx])
            if answer[d] is None or value > answer[d]:
                answer[d], witnesses[d] = value, chunk[idx]
        count += len(chunk)
    assert count == comb(m + 2**width - 1, 2**width - 1)
    p, ell = m - width, m - 2
    alpha = (F(0),) * (width - 3) + (F(1, 8), F(1, 5))
    beta = (F(0),) * (width - 2) + (F(1, 20),)
    credit = {(t, query): projected(p, ell, t, query, alpha, beta, F(1, 4))[0][0]
              for t, query in product((0, 1), repeat=2)}
    for d, witness in enumerate(witnesses):
        branches = [bits[i] for i in witness]
        assert sum(z[0] for z in branches) == d
        assert literal_objective(branches, p, scale, credit) == answer[d]
    return answer, count, bound


def main():
    report = {"status": "INDEPENDENT_EXACT_DIAGNOSTICS", "domains": [
        domain_counts(5, 10, 3, 4), domain_counts(6, 13, 4, 5), domain_counts(6, 11, 3, 4)],
        "interface_counterexample": interface_example(), "moment_pricing": []}
    for m, width in [(5, 4), (6, 5)]:
        bits, rows, scale = primitives(m, width)
        started = time.monotonic()
        expected, stats = price_dp(m, width, bits, rows)
        dp_seconds = time.monotonic() - started
        started = time.monotonic()
        actual, count, bound = price_all_histograms(m, width, bits, rows, scale)
        brute_seconds = time.monotonic() - started
        assert expected == actual
        report["moment_pricing"].append(dict(m=m, width=width, share_scale=scale,
            histogram_count=count, maxima_by_d=actual, **stats,
            dp_seconds=round(dp_seconds, 4), histogram_seconds=round(brute_seconds, 4),
            independent_literal_witness_checks=m + 1,
            numpy_int64_intermediate_absolute_bound=bound,
            scope="Exact family-pricing architecture test, not half certificate"))
    (HERE / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
