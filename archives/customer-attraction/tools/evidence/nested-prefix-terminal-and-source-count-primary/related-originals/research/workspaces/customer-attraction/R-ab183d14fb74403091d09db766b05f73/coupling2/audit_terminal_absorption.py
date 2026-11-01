"""Exact independent checks for terminal absorption; Q-CAG-HALF stays OPEN."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver


def main():
    member_checks = 0
    for h, r in product(range(16), repeat=2):
        for a, b in product((0, 1), repeat=2):
            direct = F(b, h + 1) + (F(1, h + 1 + r * b) if a else F(0))
            reverse = F(a, h + 1) + (F(1, h + 1 + r * a) if b else F(0))
            assert direct == reverse == F(int(a or b), h + 1) + F(a * b, h + r + 1)
            member_checks += 1

    # Every binary actual membership path in this finite range, with B hit last.
    binary_checks = 0
    monotonic_checks = 0
    for m in range(1, 14):
        harmonic = sum((F(1, k) for k in range(1, m + 1)), F(0))
        for bits0 in product((0, 1), repeat=m - 1):
            bits = bits0 + (1,)
            c = sum(bits)
            last = F(1, c)
            delta = F(1, c * (c + 1))
            copying = sum((F(1, sum(bits[:i]) + m - i) for i in range(m)), F(0))
            assert copying >= harmonic * last
            assert copying + delta >= (harmonic + F(1, 2)) * last
            extremal = F(c - 1, m) + sum((F(1, k) for k in range(c, m + 1)), F(0))
            assert copying >= extremal
            if m >= 2:
                g = sum(bits[:-2])
                h = g + bits[-2]
                assert F(1, g + 2) >= F(1, h + 2) == last - delta
            binary_checks += 1
        values = []
        for c in range(1, m + 1):
            hc = sum((F(1, k) for k in range(1, c + 1)), F(0))
            values.append(1 + F(c * (c - 1), m) + c * (harmonic - hc) + F(1, c + 1))
        for c in range(1, m):
            assert values[c] > values[c - 1]
            monotonic_checks += 1

    rng = random.Random(22102026)
    true_rows = 0
    absorbed_nodes = 0
    sharp_tail_rows = 0
    actual_copy_bounds = 0
    instances = 0
    for m, p in [(2, 3), (3, 3), (4, 3), (5, 3), (3, 4)]:
        for sample in range(4):
            customers = tuple(
                CustomerType(frozenset(a for a in range(p) if bit >> a & 1), rng.randint(1, 7))
                for bit in range(1, 1 << p)
                if rng.random() < F(3, 5)
            )
            ins = Instance(tuple(f"T{a}" for a in range(p)), customers, m)
            solver = ExactSPESolver(ins)
            cert = solver.certificate(min(solver.worst_outcomes()))
            acts = dict(cert.actions)

            # Direct unit-customer definition, independently of Instance payoff methods.
            def payoff(a, path):
                return sum(
                    (F(t.multiplicity, sum(b in t.topics for b in path)) for t in customers if a in t.topics),
                    F(0),
                )

            def f(h, a):
                return sum(
                    (F(t.multiplicity, 1 + sum(b in t.topics for b in h)) for t in customers if a in t.topics),
                    F(0),
                )

            def kernel(h, a, b):
                return f(h, b) + payoff(a, h + (a,) + (b,) * (m - len(h) - 1))

            def tax(h):
                return sum(
                    (F(t.multiplicity * (q := sum(b in t.topics for b in h)), q + 1) for t in customers),
                    F(0),
                )

            def continuation(h):
                path = h
                while len(path) < m:
                    path += (acts[path],)
                return path

            for k in range(m):
                for h in product(range(p), repeat=k):
                    r = m - k - 1
                    for a, b in product(range(p), repeat=2):
                        reply = acts[h + (b,) * r]
                        slack = payoff(reply, h + (b,) * r + (reply,)) - payoff(a, h + (b,) * r + (a,))
                        assert slack >= 0
                        assert kernel(h, b, reply) - kernel(h, a, b) == slack
                        true_rows += 1

                    if k <= m - 2:
                        path = continuation(h)
                        penult, last = path[-2:]
                        last_two = payoff(penult, path) + payoff(last, path)
                        for a, b in product(range(p), repeat=2):
                            assert kernel(h, a, b) <= last_two + tax(path) - tax(h)
                            assert kernel(h, a, b) <= last_two + tax(path[:-1]) - tax(h)
                            if k == m - 2:
                                reply = acts[h + (b,)]
                                overlap = sum(
                                    (F(t.multiplicity, (q + 1) * (q + 2))
                                     for t in customers
                                     if penult in t.topics and reply in t.topics
                                     for q in [sum(v in t.topics for v in h)]),
                                    F(0),
                                )
                                slack = (last_two + overlap - kernel(h, a, b))
                                direct_rows = (
                                    payoff(penult, path) - payoff(b, h + (b, reply))
                                    + payoff(last, path) - payoff(reply, h + (penult, reply))
                                    + payoff(reply, h + (b, reply)) - payoff(a, h + (b, a))
                                )
                                assert slack == direct_rows >= 0
                                sharp_tail_rows += 1
                        absorbed_nodes += 1

            path = continuation(())
            utilities = tuple(payoff(a, path) for a in path)
            welfare = sum(utilities, F(0))
            last = path[-1]
            delta = tax(path) - tax(path[:-1])
            harmonic = sum((F(1, k) for k in range(1, m + 1)), F(0))
            for i in range(m):
                lower = sum(
                    (F(t.multiplicity, sum(b in t.topics for b in path[:i]) + m - i) for t in customers if last in t.topics),
                    F(0),
                )
                assert utilities[i] >= lower
                actual_copy_bounds += 1
            assert welfare + delta >= (harmonic + F(1, 2)) * utilities[-1]
            instances += 1

    # Recheck the old complete 23-customer SPE, rather than only its payoff vector.
    types = [({0}, 3), ({1}, 4), ({2, 3}, 6), ({2, 4}, 6), ({0, 3, 4}, 2), ({1, 3, 4}, 2)]
    second = (1, 2, 3, 4, 2)
    last_grid = ((2, 2, 2, 2, 2), (2, 2, 3, 2, 2), (2, 3, 3, 2, 3), (2, 2, 2, 2, 2), (2, 2, 3, 2, 2))

    def old_action(h):
        return 0 if not h else second[h[0]] if len(h) == 1 else last_grid[h[0]][h[1]]

    def old_follow(h):
        while len(h) < 3:
            h += (old_action(h),)
        return h

    def old_pay(a, path):
        return sum((F(mult, sum(b in topics for b in path)) for topics, mult in types if a in topics), F(0))

    old_rows = 0
    for k in range(3):
        for h in product(range(5), repeat=k):
            chosen = old_action(h)
            value = old_pay(chosen, old_follow(h))
            for a in range(5):
                assert value >= old_pay(a, old_follow(h + (a,)))
                old_rows += 1
    path = old_follow(())
    utilities = tuple(old_pay(a, path) for a in path)
    welfare = sum(utilities, F(0))
    tax = sum((F(mult * (q := sum(b in topics for b in path)), q + 1) for topics, mult in types), F(0))
    assert path == (0, 1, 2) and utilities == (5, 6, 12)
    assert welfare == 23 and tax == F(23, 2) and 3 * utilities[-1] > welfare + tax

    report = {
        "status": "exact arithmetic and finite full-SPE audit; general Q-CAG-HALF OPEN",
        "membership_checks": member_checks,
        "binary_paths": binary_checks,
        "terminal_ratio_monotonic_checks": monotonic_checks,
        "full_spe_instances": instances,
        "true_last_reply_rows": true_rows,
        "absorbed_ordered_nodes": absorbed_nodes,
        "exact_sharp_tail_three_row_identities": sharp_tail_rows,
        "actual_copy_bounds": actual_copy_bounds,
        "old_23_customer_full_strategy_rows": old_rows,
        "old_linear_terminal_failure": {"payoffs": [str(v) for v in utilities], "W": str(welfare), "tax": str(tax), "m_u_last": str(3 * utilities[-1])},
        "seed": 22102026,
    }
    (BASE / "terminal_absorption_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
