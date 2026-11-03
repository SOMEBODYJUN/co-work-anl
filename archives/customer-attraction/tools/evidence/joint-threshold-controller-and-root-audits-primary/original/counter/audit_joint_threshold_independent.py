#!/usr/bin/env python3
"""Definition-level independent audit of the exact joint-threshold controller.

No repository model, SPE solver, author proof, or discovery program is imported.
Each client is expanded into a distinct integer identifier. Three-player payoffs
are computed in integer units of 1/6. The audit checks all ordered histories and
all legal joint actions in each declared test input; the all-parameter theorem
is proved separately in the accompanying independent review.
"""

from itertools import product
from fractions import Fraction
from pathlib import Path
import json


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


def audit(a, b, q):
    economic = []
    bank = []
    cursor = 0
    for _ in range(q):
        cells = []
        for _ in range(3):
            cells.append(frozenset(range(cursor, cursor + a)))
            cursor += a
        economic.append(cells)
    for _ in range(q):
        cells = []
        for _ in range(2):
            cells.append(frozenset(range(cursor, cursor + b)))
            cursor += b
        bank.append(cells)

    vectors = list(product(product(range(3), repeat=q),
                           product(range(2), repeat=q)))
    index = {v: i for i, v in enumerate(vectors)}
    topics = []
    for ev, bv in vectors:
        clients = set()
        for t in range(q):
            clients.update(economic[t][ev[t]])
            clients.update(bank[t][bv[t]])
        assert len(clients) == q * (a + b)
        topics.append(frozenset(clients))
    size = len(topics)

    def prescribed_second(root):
        er, br = vectors[root]
        if b < a:
            bad = (q * b) // a
            ev = tuple(er[t] if t < bad else
                       min(v for v in range(3) if v != er[t])
                       for t in range(q))
            bv = tuple(1 - br[t] for t in range(q))
        else:
            rewarded = (q * a + b - 1) // b
            ev = er
            bv = tuple(1 - br[t] if t < rewarded else br[t]
                       for t in range(q))
        return index[(ev, bv)]

    def prescribed_last(root, second):
        er, br = vectors[root]
        es, bs = vectors[second]
        reward = second == prescribed_second(root)
        ev = tuple(min(v for v in range(3)
                       if v != er[t] and v != es[t])
                   for t in range(q))
        bv = []
        for t in range(q):
            if bs[t] == br[t]:
                bv.append(1 - br[t])
            else:
                bv.append(br[t] if reward else bs[t])
        return index[(ev, tuple(bv))]

    def payoffs6(root, second, last):
        selected = (topics[root], topics[second], topics[last])
        loads = {}
        for topic in selected:
            for client in topic:
                loads[client] = loads.get(client, 0) + 1
        values = tuple(sum(6 // loads[x] for x in topic)
                       for topic in selected)
        assert sum(values) == 6 * len(loads)
        return values

    m_exact = (Fraction(q * (a + b), 2) if b >= a else
               Fraction(q * a) + Fraction(q * b - a * ((q * b) // a), 2))
    floor_second = Fraction(q * (2 * a + b), 2)
    root_values6 = []
    min_gap6 = None
    strict = 0
    comparisons = {"root": 0, "second": 0, "last": 0}
    last_values = {}

    for root in range(size):
        for second in range(size):
            chosen = prescribed_last(root, second)
            chosen_values = payoffs6(root, second, chosen)
            last_values[(root, second)] = chosen_values
            er, br = vectors[root]
            es, bs = vectors[second]
            ec, bc = vectors[chosen]
            assert all(ec[t] not in (er[t], es[t]) for t in range(q))
            assert all((bc[t] != br[t]) if bs[t] == br[t] else
                       (bc[t] in (br[t], bs[t])) for t in range(q))
            for alternative in range(size):
                alternative_value = payoffs6(root, second, alternative)[2]
                gap = chosen_values[2] - alternative_value
                assert gap >= 0, (a, b, q, root, second, alternative, gap)
                comparisons["last"] += 1
                strict += gap > 0
                min_gap6 = gap if min_gap6 is None else min(min_gap6, gap)

        chosen_second = prescribed_second(root)
        root_values6.append(last_values[(root, chosen_second)][0])
        assert Fraction(root_values6[-1], 6) == m_exact
        value_second6 = last_values[(root, chosen_second)][1]
        assert Fraction(value_second6, 6) >= floor_second
        for alternative in range(size):
            alternative_values = last_values[(root, alternative)]
            gap = value_second6 - alternative_values[1]
            assert gap >= 0, (a, b, q, root, alternative, gap)
            if alternative != chosen_second:
                assert Fraction(alternative_values[1], 6) <= floor_second
            comparisons["second"] += 1
            strict += gap > 0
            min_gap6 = min(min_gap6, gap)

    for alternative in range(size):
        gap = root_values6[0] - root_values6[alternative]
        assert gap >= 0
        comparisons["root"] += 1
        strict += gap > 0
        min_gap6 = min(min_gap6, gap)

    # The target leaf is separate from the attaining exit controller.
    target_root = index[((0,) * q, (0,) * q)]
    target_second = target_root
    target_last = index[((1,) * q, (1,) * q)]
    target_values = tuple(Fraction(v, 6) for v in
                          payoffs6(target_root, target_second, target_last))
    assert target_values == (Fraction(q * (a + b), 2),
                             Fraction(q * (a + b), 2),
                             Fraction(q * (a + b)))
    for alternative in range(size):
        assert payoffs6(target_root, target_second, alternative)[2] <= 6 * target_values[2]

    # M2: independently enumerate all last best replies at the fixed root.
    second_floor_values6 = []
    for second in range(size):
        terminals = [payoffs6(target_root, second, last) for last in range(size)]
        maximum_last6 = max(v[2] for v in terminals)
        second_floor_values6.append(min(v[1] for v in terminals
                                        if v[2] == maximum_last6))
    m2 = Fraction(max(second_floor_values6), 6)
    assert m2 == Fraction(q * (2 * a + b), 2)
    g1 = m_exact - target_values[0]
    g2 = m2 - target_values[1]
    assert g1 == Fraction(a * max(0, q - (q * b) // a), 2)
    assert g2 == Fraction(q * a, 2)
    assert 0 <= g1 <= g2
    fee_new = 2 * (g1 + g2) + max(g1, g2)
    fee_old = Fraction(5 * q * a, 2)
    saving = fee_old - fee_new
    assert saving == a * min(q, (q * b) // a)
    welfare_target = 2 * q * (a + b)
    optimum = q * (3 * a + 2 * b)
    assert 2 * welfare_target - optimum == q * (a + 2 * b) > 0

    return {
        "a": a, "b": b, "q": q,
        "unit_clients": cursor,
        "joint_topics": size,
        "all_ordered_decision_histories": 1 + size + size * size,
        "all_legal_IC_comparisons": comparisons,
        "strict_IC_comparisons": strict,
        "minimum_IC_gap": Fraction(min_gap6, 6),
        "every_forced_root_attaining_value": m_exact,
        "M2_by_all_last_BR_enumeration": m2,
        "target_payoffs": target_values,
        "g": (g1, g2),
        "signed_fee_new": fee_new,
        "signed_fee_old": fee_old,
        "fee_saving": saving,
        "target_W": welfare_target,
        "OPT3": optimum,
        "target_half_margin_B": 2 * welfare_target - optimum,
        "B_plus_new_fee": 2 * welfare_target - optimum + fee_new,
    }


def main():
    # Exact-divisibility, nondivisibility, zero-saving, and b>=a partial-bank
    # cases all test the one declared general controller, not a search class.
    cases = [(1, 1, 1), (2, 1, 2), (3, 2, 2),
             (3, 1, 2), (2, 3, 2), (1, 3, 2)]
    result = {
        "status": "independent_definition_level_controller_audit_passed",
        "scope": "finite audit only; all-parameter proof is in the review",
        "no_repository_model_or_SPE_solver_imported": True,
        "cases": [audit(*case) for case in cases],
    }
    destination = Path(__file__).with_name("joint_threshold_independent_audit.json")
    destination.write_text(json.dumps(result, indent=2, default=encode) + "\n")
    print(json.dumps(result, indent=2, default=encode))


if __name__ == "__main__":
    main()
