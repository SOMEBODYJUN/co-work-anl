"""Exact finite sanity checks for the Boss1 source reconstruction, not a new theorem."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def check_client_rows():
    counts = {"penultimate_global": 0, "penultimate_last_credit": 0,
              "penultimate_new_credit": 0, "coverage_slack": 0}
    for b, a, z, o in product(range(9), range(2), range(2), range(2)):
        covered = int(b + a + z > 0)
        omega = F(o, b + 1)
        tail = F(a + z, b + a + z) if a + z else F(0)
        last = F(z, b + a + z) if z else F(0)
        tax_a = F(a, (b + 1) * (b + 2))
        fresh = int(b == 0 and a + z > 0)
        credit = covered - o + omega
        assert credit >= tail / 2
        assert credit >= last + tax_a
        assert credit >= (tail + fresh) / 2
        for key in tuple(counts)[:3]:
            counts[key] += 1
    for c, e in product(range(9), range(11)):
        covered, optimum_member = int(c > 0), int(e > 0)
        v = F(1, c + 1) if c else F(0)
        slack = covered - v + F(e, c + 1) - optimum_member
        assert slack >= 0
        counts["coverage_slack"] += 1
    return counts


def check_jensen():
    checked = 0
    for length in range(1, 5):
        for hs in product(range(4), repeat=length):
            mean = sum(map(F, hs)) / length
            exact = sum(F(1, 1 + h) for h in hs) / length
            remainder = sum((F(h) - mean) ** 2 /
                            ((1 + mean) ** 2 * (1 + h)) for h in hs) / length
            assert exact == F(1, 1 + mean) + remainder
            assert remainder >= 0
            checked += 1
    return checked


def check_two_player_ledgers():
    themes = ({0, 1}, {0, 1, 2}, {2, 3})

    def utility(actions, i):
        return sum((F(1, sum(x in themes[t] for t in actions))
                    for x in themes[actions[i]]), F(0))

    best_replies = []
    for root in range(3):
        values = [utility((root, b), 1) for b in range(3)]
        best_replies.append([b for b, v in enumerate(values) if v == max(values)])
    policies, tuples, positive, negative = 0, 0, 0, 0
    for tail in product(*best_replies):
        root_values = [utility((a, tail[a]), 0) for a in range(3)]
        for root in range(3):
            if root_values[root] != max(root_values):
                continue
            policies += 1
            actual = (root, tail[root])
            counts = [sum(x in themes[t] for t in actual) for x in range(4)]
            welfare = len(themes[actual[0]] | themes[actual[1]])
            us = [utility(actual, i) for i in range(2)]
            assert sum(us) == welfare
            v = sum((F(1, c + 1) for c in counts if c), F(0))
            for comparison in product(range(3), repeat=2):
                fs, deltas, debts, ic = [], [], [], []
                for i, t in enumerate(comparison):
                    f = sum((F(1, counts[x] + 1) for x in themes[t]), F(0))
                    delta = sum((F(1, counts[x] * (counts[x] + 1))
                                 for x in themes[t] & themes[actual[i]]), F(0))
                    frozen = list(actual)
                    frozen[i] = t
                    q = utility(frozen, i)
                    assert q == f + delta
                    changed = (t, tail[t]) if i == 0 else (root, t)
                    d = utility(changed, i)
                    r = q - d
                    positive += r > 0
                    negative += r < 0
                    fs.append(f)
                    deltas.append(delta)
                    debts.append(r)
                    ic.append(us[i] - d)
                    assert ic[-1] >= 0
                optimum = len(themes[comparison[0]] | themes[comparison[1]])
                ecov = welfare - v + sum(fs) - optimum
                assert ecov >= 0
                assert 2 * welfare - optimum == (
                    v + sum(deltas) - sum(debts) + ecov + sum(ic))
                tuples += 1
    # The explicit source policy root=A, tail(A/B/C)=C/B/B.
    tail = (2, 1, 1)
    actual = (0, 2)
    assert utility(actual, 0) == 2
    assert utility((1, 2), 0) - utility((1, tail[1]), 0) == 1
    assert utility((2, 2), 0) - utility((2, tail[2]), 0) == -F(1, 2)
    assert policies and tuples and positive and negative
    return {"complete_SPE_policies": policies, "comparison_tuples": tuples,
            "positive_debt_entries": positive, "negative_debt_entries": negative,
            "source_explicit_debts": ["1", "-1/2"]}


if __name__ == "__main__":
    result = {"scope": "finite exact checks; universal claims use the source proofs",
              "client_rows": check_client_rows(), "jensen_distributions": check_jensen(),
              "two_player_ledgers": check_two_player_ledgers()}
    destination = Path(__file__).with_name("ledger_checks.json")
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
