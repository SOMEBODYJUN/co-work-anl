"""Exact parametric certificate for omitted-customer deletion.

All sampled points here are representatives of a proved exhaustive affine sign
partition. This proves the stated one-parameter fixed-size family, never the
general Q-CAG-HALF conjecture. Run from repo root with PYTHONPATH=.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'reduced.json').read_text())
base = Instance.from_dict(data['instance'])
target = tuple(data['target'])
kept = tuple(x for x in base.customers if any(target[a] for a in x.topics))
omitted = tuple(x for x in base.customers if not any(target[a] for a in x.topics))
assert len(omitted) == 1 and omitted[0].topics == frozenset({3})
assert omitted[0].multiplicity == 1
plain = Instance(base.topics, kept, base.players)


def all_counts(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in all_counts(total - first, width - 1):
                yield (first,) + tail


def game(t):
    """Integer unit-customer game = denominator(t) times the normalized game."""
    t = F(t)
    rows = [CustomerType(x.topics, x.multiplicity * t.denominator) for x in kept]
    if t:
        rows.append(CustomerType(frozenset({3}), t.numerator))
    return Instance(base.topics, tuple(rows), base.players)


def ordered_tree_outcomes(instance):
    """Second implementation; visits every ordered history without count cache."""
    @lru_cache(None)
    def utility(q):
        # Direct expansion of unit customers, deliberately not model.topic_payoffs.
        values = [F(0)] * instance.topic_count
        for row in instance.customers:
            for _ in range(row.multiplicity):
                load = sum(q[a] for a in row.topics)
                if load:
                    for a in row.topics:
                        if q[a]:
                            values[a] += F(1, load)
        return tuple(values)

    nodes = 0

    def walk(history):
        nonlocal nodes
        if len(history) == instance.players:
            q = tuple(history.count(a) for a in range(instance.topic_count))
            return {q}
        nodes += 1
        children = [walk(history + (a,)) for a in range(instance.topic_count)]
        floor = max(min(utility(q)[a] for q in child)
                    for a, child in enumerate(children))
        return {q for a, child in enumerate(children) for q in child
                if utility(q)[a] >= floor}

    result = walk(())
    return result, nodes


def main():
    # Every terminal utility is affine in t. Any two possible current-player
    # utility values can change order only at a root listed below. This includes
    # more pairs than any actual node needs; omitting none makes the partition safe.
    lines = set()
    for q in all_counts(base.players, base.topic_count):
        intercepts = plain.topic_payoffs(q)
        for a in range(base.topic_count):
            if q[a]:
                lines.add((intercepts[a], F(1, q[3]) if a == 3 else F(0)))
    cuts = {F(0), F(1)}
    for (a, b), (c, d) in combinations(lines, 2):
        if b != d:
            crossing = (c - a) / (b - d)
            if 0 < crossing < 1:
                cuts.add(crossing)
    cuts = sorted(cuts)
    representatives = sorted(set(cuts + [(a + b) / 2 for a, b in zip(cuts, cuts[1:])]))
    records = []
    for t in representatives:
        instance = game(t)
        solver = ExactSPESolver(instance)
        outcomes = solver.outcomes()
        assert (target in outcomes) == (t >= F(3, 4)), t
        floor = solver.threshold((0,) * base.topic_count) / t.denominator
        assert floor == (F(7) if t >= F(3, 4) else F(33, 4)), (t, floor)
        records.append({'t': str(t), 'target_realizable': target in outcomes,
                        'root_floor': str(floor), 'outcomes': sorted(outcomes)})
    # Each open cell has constant utility-order data. Induction from the terminal
    # layer therefore proves R(k) constant throughout that cell, including ties
    # that are identically zero. Cut endpoints are checked separately above.

    audits = []
    for t in [F(0), F(1, 2), F(3, 4), F(1)]:
        instance = game(t)
        solver = ExactSPESolver(instance)
        independent, nodes = ordered_tree_outcomes(instance)
        assert independent == set(solver.outcomes())
        audit = {'t': str(t), 'ordered_nodes': nodes, 'outcomes': sorted(independent)}
        if target in independent:
            cert = solver.certificate(target)
            check = verify_certificate(instance, cert)
            check.assert_valid()
            audit.update(histories=check.checked_histories,
                         deviations=check.checked_deviations,
                         path=list(check.terminal_history))
            if t == F(3, 4):
                (HERE / 'threshold_certificate.json').write_text(
                    json.dumps(cert.to_dict(), indent=2) + '\n')
        audits.append(audit)

    # General integer family: covered rows are 4k times the table, omitted rows
    # have 3k clients, then one is deleted. The two normalized parameters straddle
    # the proved threshold. These cases are regression checks of that formula.
    families = []
    for k in [1, 2, 3, 11, 100]:
        t_before = F(3, 4)
        t_after = F(3 * k - 1, 4 * k)
        assert F(1, 2) <= t_after < F(3, 4)
        q = 4 * k
        before_floor, after_floor = F(7) * q, F(33, 4) * q
        assert after_floor - before_floor == 5 * k
        assert 35 * q + 3 * k == 143 * k
        assert 35 * q == 140 * k
        families.append({'k': k, 'clients_before': 143 * k,
                         'omitted_before': 3 * k,
                         'welfare_target': 140 * k,
                         'root_floor_before': str(before_floor),
                         'root_floor_after': str(after_floor),
                         'deletion_size': 1})

    strict_pivot_families = []
    for k in [1, 2, 3, 11, 100]:
        scale = 4 * k + 1
        omitted_before = 3 * k + 1
        omitted_after = 3 * k
        floors = []
        for omitted_count in [omitted_before, omitted_after]:
            instance = Instance(base.topics, tuple(
                CustomerType(x.topics, x.multiplicity * scale) for x in kept
            ) + (CustomerType(frozenset({3}), omitted_count),), base.players)
            solver = ExactSPESolver(instance)
            before = omitted_count == omitted_before
            assert (target in solver.outcomes()) == before
            floor = solver.threshold((0,) * base.topic_count)
            assert floor == (7 * scale if before else F(33 * scale, 4))
            floors.append(floor)
        assert floors[1] - floors[0] == F(5 * scale, 4)
        assert F(omitted_before) - F(3 * scale, 4) == F(1, 4)
        assert F(omitted_after) - F(3 * scale, 4) == -F(3, 4)
        strict_pivot_families.append({
            'k': k, 'covered_scale': scale, 'omitted_before': omitted_before,
            'omitted_after': omitted_after, 'root_floors': list(map(str, floors)),
            'floor_jump': str(floors[1] - floors[0]),
            'pivotal_margins': ['1/4', '-3/4'],
            'scope': 'strict pivotal comparison, not strictness of every full-tree IC'})

    report = {'status': 'exact_parametric_family_verified',
              'scope': 'fixed five-player five-theme family, not Q-CAG-HALF',
              'affine_lines': len(lines), 'cuts': list(map(str, cuts)),
              'representatives': len(representatives), 'records': records,
              'independent_ordered_tree_audits': audits, 'integer_family': families,
              'strict_pivot_integer_family': strict_pivot_families}
    (HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'scope', 'affine_lines', 'representatives']}))
    print(json.dumps(audits))
    print(json.dumps(families))


if __name__ == '__main__':
    main()
