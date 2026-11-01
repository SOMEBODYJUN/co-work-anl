#!/usr/bin/env python3
"""Exact, independent audits for intersection_moments.md; standard library only."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path


def masks(p: int, maximum: int | None = None):
    return [a for a in range(1, 1 << p)
            if maximum is None or a.bit_count() <= maximum]


def subsets(a: int):
    b = a
    while True:
        yield b
        if not b:
            break
        b = (b - 1) & a


def moments(r: dict[int, F], p: int, d: int):
    return {a: sum((w for b, w in r.items() if a & b == a), F(0))
            for a in masks(p, d)}


def payoff(r: dict[int, F], q: tuple[int, ...], a: int):
    assert q[a] > 0
    return sum((w / sum(q[b] for b in range(len(q)) if mask >> b & 1)
                for mask, w in r.items() if mask >> a & 1), F(0))


def welfare(r: dict[int, F], support: int):
    return sum((w for b, w in r.items() if b & support), F(0))


def coefficient(q: tuple[int, ...], a: int, c: int):
    return sum((F((-1) ** (c.bit_count() - e.bit_count()),
                  q[a] + sum(q[b] for b in range(len(q)) if e >> b & 1))
                for e in subsets(c)), F(0))


def moment_payoff(t: dict[int, F], q: tuple[int, ...], a: int):
    k = sum(1 << b for b, v in enumerate(q) if v)
    return sum((coefficient(q, a, c) * t[c | (1 << a)]
                for c in subsets(k ^ (1 << a))), F(0))


def moment_welfare(t: dict[int, F], support: int):
    return sum(((-1) ** (a.bit_count() + 1) * t[a]
                for a in subsets(support) if a), F(0))


def counts(p: int, m: int):
    if p == 1:
        yield (m,)
    else:
        for a in range(m + 1):
            for rest in counts(p - 1, m - a):
                yield (a,) + rest


def history_counts(history: tuple[int, ...], p: int):
    return tuple(history.count(a) for a in range(p))


def player_subset_payoff(t: dict[int, F], history: tuple[int, ...], i: int):
    others = [j for j in range(len(history)) if j != i]
    result = F(0)
    for selection in range(1 << len(others)):
        selected = [others[j] for j in range(len(others)) if selection >> j & 1]
        labels = (1 << history[i])
        for j in selected:
            labels |= 1 << history[j]
        result += F((-1) ** len(selected), len(selected) + 1) * t[labels]
    return result


def pad_support(a: int, p: int, m: int):
    q = [int(a >> b & 1) for b in range(p)]
    first = next(b for b in range(p) if q[b])
    q[first] += m - a.bit_count()
    return tuple(q)


def parity_trade(p: int, a: int):
    even, odd = {}, {}
    for b in subsets(a):
        (odd if b.bit_count() % 2 else even)[b] = F(1)
    for b in range(p):
        singleton = 1 << b
        even[singleton] = even.get(singleton, F(0)) + 1
        odd[singleton] = odd.get(singleton, F(0)) + 1
    return even, odd


def null_vector(columns: list[list[F]]):
    """Return an exact nonzero vector in the right kernel, or None."""
    if not columns:
        return None
    rows = [list(row) for row in zip(*columns)]
    n = len(columns)
    pivots = []
    row_index = 0
    for col in range(n):
        pivot = next((j for j in range(row_index, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[row_index], rows[pivot] = rows[pivot], rows[row_index]
        factor = rows[row_index][col]
        rows[row_index] = [v / factor for v in rows[row_index]]
        for j in range(len(rows)):
            if j != row_index and rows[j][col]:
                factor = rows[j][col]
                rows[j] = [x - factor * y for x, y in zip(rows[j], rows[row_index])]
        pivots.append(col)
        row_index += 1
        if row_index == len(rows):
            break
    free = next((j for j in range(n) if j not in pivots), None)
    if free is None:
        return None
    out = [F(0)] * n
    out[free] = F(1)
    for j, pivot in enumerate(pivots):
        out[pivot] = -rows[j][free]
    return out


def sparsify(r: dict[int, F], p: int, d: int):
    out = {b: w for b, w in r.items() if b and w}
    indices = masks(p, d)
    steps = 0
    while True:
        support = list(out)
        relation = null_vector([[F(a & b == a) for a in indices] for b in support])
        if relation is None:
            return out, steps
        if not any(v > 0 for v in relation):
            relation = [-v for v in relation]
        distance = min(out[b] / v for b, v in zip(support, relation) if v > 0)
        out = {b: out[b] - distance * v for b, v in zip(support, relation)
               if out[b] - distance * v}
        assert all(v > 0 for v in out.values())
        steps += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "status": "all exact assertions passed",
        "method": "independent standard-library Fraction calculation from customer types",
        "claim_scope": "representation only; Q-CAG-HALF remains OPEN",
        "formula_range": {"topics": [1, 5], "players": [1, 6]},
        "terminal_payoff_checks": 0,
        "welfare_checks": 0,
        "inverse_checks": 0,
        "triangular_rank_checks": 0,
        "true_history_row_checks": 0,
        "coordinate_trade_checks": 0,
        "highest_order_incentive_checks": 0,
        "player_subset_formula_checks": 0,
        "invisible_high_order_trade_checks": 0,
        "sparsification": [],
    }

    for p in range(1, 6):
        r = {b: F(1 + ((b * 37 + p) % 7)) for b in range(1 << p)}
        for m in range(1, 7):
            d = min(m, p)
            t = moments(r, p, d)
            for q in counts(p, m):
                support = sum(1 << a for a, v in enumerate(q) if v)
                w = welfare(r, support)
                assert moment_welfare(t, support) == w
                assert sum((q[a] * payoff(r, q, a) for a in range(p) if q[a]), F(0)) == w
                report["welfare_checks"] += 2
                for a in range(p):
                    if q[a]:
                        assert payoff(r, q, a) == moment_payoff(t, q, a)
                        for c in subsets(support ^ (1 << a)):
                            assert (-1) ** c.bit_count() * coefficient(q, a, c) > 0
                        report["terminal_payoff_checks"] += 1
            unions = {a: sum((q[b] * payoff(r, q, b)
                              for b in range(p) if q[b]), F(0))
                      for a in t for q in [pad_support(a, p, m)]}
            for a in t:
                inverse = sum(((-1) ** (c.bit_count() + 1) * unions[c]
                               for c in subsets(a) if c), F(0))
                assert inverse == t[a]
                report["inverse_checks"] += 1

            # Matrix restricted to subset columns of size <=d is triangular.
            ordered = sorted(t, key=lambda a: (a.bit_count(), a))
            assert len(ordered) == sum(comb(p, j) for j in range(1, d + 1))
            for i, a in enumerate(ordered):
                assert a & ordered[i] == a
                assert all(not (a & b == a) for b in ordered[:i])
            report["triangular_rank_checks"] += 1

            for a in t:
                even, odd = parity_trade(p, a)
                assert sum(even.values()) == sum(odd.values())
                assert all(even.get(1 << b, 0) >= 1 and odd.get(1 << b, 0) >= 1
                           for b in range(p))
                e, o = moments(even, p, p), moments(odd, p, p)
                assert all(e[c] - o[c] == ((-1) ** a.bit_count() if c == a else 0)
                           for c in e)
                q = pad_support(a, p, m)
                assert welfare(even, a) - welfare(odd, a) == -1
                assert sum(q) == m
                report["coordinate_trade_checks"] += 1

            # High-order parity trades are exactly invisible to this whole game.
            for a in masks(p):
                if a.bit_count() <= d:
                    continue
                even, odd = parity_trade(p, a)
                assert moments(even, p, d) == moments(odd, p, d)
                for q in counts(p, m):
                    for b, value in enumerate(q):
                        if value:
                            assert payoff(even, q, b) == payoff(odd, q, b)
                # The union of all labels is nevertheless different by exactly one.
                assert welfare(even, (1 << p) - 1) - welfare(odd, (1 << p) - 1) == -1
                report["invisible_high_order_trade_checks"] += 1

            # Exhibit one true last-node comparison requiring highest order.
            if p >= 2:
                a = (1 << d) - 1
                even, odd = parity_trade(p, a)
                if d == 1:
                    assert m == 1
                    prescribed, deviation = 0, 1
                    q_true, q_dev = (1,) + (0,) * (p - 1), (0, 1) + (0,) * (p - 2)
                else:
                    prescribed, deviation = d - 1, 0
                    prefix = list(range(d - 1)) + [0] * (m - d)
                    assert len(prefix) == m - 1
                    q_true = history_counts(tuple(prefix + [prescribed]), p)
                    q_dev = history_counts(tuple(prefix + [deviation]), p)
                row_even = payoff(even, q_true, prescribed) - payoff(even, q_dev, deviation)
                row_odd = payoff(odd, q_true, prescribed) - payoff(odd, q_dev, deviation)
                assert row_even != row_odd
                report["highest_order_incentive_checks"] += 1

    # Arbitrary history-dependent formal strategies: no SPE assumption needed.
    for p in range(1, 4):
        for m in range(1, 5):
            r = {b: F(1 + (b * 11 + m) % 5) for b in range(1 << p)}
            t = moments(r, p, min(m, p))
            for history in product(range(p), repeat=m):
                q = history_counts(history, p)
                for i, a in enumerate(history):
                    assert player_subset_payoff(t, history, i) == payoff(r, q, a)
                    report["player_subset_formula_checks"] += 1
            sigma = {}
            for depth in range(m):
                for history in product(range(p), repeat=depth):
                    sigma[history] = (depth + sum((j + 3) * (a + 1)
                                                for j, a in enumerate(history))) % p

            def outcome(history):
                while len(history) < m:
                    history += (sigma[history],)
                return history_counts(history, p)

            for history, prescribed in sigma.items():
                q_true = outcome(history)
                for deviation in range(p):
                    q_dev = outcome(history + (deviation,))
                    direct = payoff(r, q_true, prescribed) - payoff(r, q_dev, deviation)
                    via_moments = (moment_payoff(t, q_true, prescribed)
                                   - moment_payoff(t, q_dev, deviation))
                    assert direct == via_moments
                    if p == 1:
                        assert direct == 0
                    report["true_history_row_checks"] += 1

    # Elementary degree-2 positivity misses a valid nonlocal degree-2 condition.
    t = {1: F(1), 2: F(1), 4: F(1), 3: F(1), 5: F(1), 6: F(0)}
    elementary_count = 0
    for a in t:
        for c in range(1 << 3):
            if not a & c and (a | c).bit_count() <= 2:
                value = sum(((-1) ** e.bit_count() * t[a | e]
                             for e in subsets(c)), F(0))
                assert value >= 0
                elementary_count += 1
    values = [(int(bool(b & 1)) - int(b & 3 == 3)
               - int(b & 5 == 5) + int(b & 6 == 6)) for b in range(8)]
    assert min(values) == 0 and t[1] - t[3] - t[5] + t[6] == -1
    report["moment_positivity_obstruction"] = {
        "topics": 3, "degree": 2, "all_elementary_conditions_passed": elementary_count,
        "boolean_polynomial_values": values, "moment_evaluation": -1,
        "is_half_counterexample": False,
    }

    for p, m in [(4, 1), (5, 2), (5, 3)]:
        d = min(p, m)
        original = {b: F(1 + (17 * b % 11)) for b in range(1, 1 << p)}
        sparse, steps = sparsify(original, p, d)
        assert moments(original, p, d) == moments(sparse, p, d)
        bound = sum(comb(p, j) for j in range(1, d + 1))
        assert len(sparse) <= bound
        denominator = lcm(*(v.denominator for v in sparse.values()))
        integer = {b: denominator * v for b, v in sparse.items()}
        assert all(v.denominator == 1 for v in integer.values())
        for q in counts(p, m):
            for a, v in enumerate(q):
                if v:
                    assert payoff(integer, q, a) == denominator * payoff(original, q, a)
        # Different topic coverages are preserved automatically for m>=2.
        if m >= 2:
            assert all(any(w > 0 and bool(b >> a & 1) != bool(b >> c & 1)
                           for b, w in sparse.items()) for a, c in combinations(range(p), 2))
        report["sparsification"].append({
            "topics": p, "players": m, "original_types": len(original),
            "sparse_types": len(sparse), "dimension_bound": bound,
            "elimination_steps": steps, "integer_scale": denominator,
            "all_terminal_payoffs_scale_exactly": True,
        })

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
