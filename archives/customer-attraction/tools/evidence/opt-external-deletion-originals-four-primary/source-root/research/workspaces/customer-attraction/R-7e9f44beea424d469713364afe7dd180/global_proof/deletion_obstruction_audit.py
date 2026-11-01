"""Definition-level audit: deleting customers outside a unique optimum can raise min-SPE W.

Only two-player games are considered here. Every customer is expanded as a distinct
unit. All three last-player nodes and every possible best-reply selector are
enumerated, and every root maximizer is retained. No canonical game solver,
strategy-cone code, or external optimization routine is imported.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


LABELS = ("A", "B", "C")


def expand(rows):
    customers = []
    for interested, count in rows:
        for _ in range(count):
            customers.append(frozenset(interested))
    return tuple(customers)


def utility(customers, selected, other):
    result = Fraction(0)
    for interested in customers:
        if selected in interested:
            result += Fraction(1, 1 + (other in interested))
    return result


def welfare(customers, first, second):
    return sum(first in t or second in t for t in customers)


def all_spe(customers):
    values = {a: {b: utility(customers, b, a) for b in LABELS}
              for a in LABELS}
    replies = {a: tuple(b for b in LABELS if values[a][b] == max(values[a].values()))
               for a in LABELS}
    certificates = []
    for selector in product(*(replies[a] for a in LABELS)):
        response = dict(zip(LABELS, selector))
        root_values = {a: utility(customers, a, response[a]) for a in LABELS}
        best = max(root_values.values())
        for a in LABELS:
            if root_values[a] != best:
                continue
            certificates.append({
                "root": a, "replies": response,
                "terminal": [a, response[a]],
                "root_action_payoffs": root_values,
                "welfare": welfare(customers, a, response[a]),
            })
    assert certificates
    return values, replies, certificates


def classify(customers):
    values, replies, certificates = all_spe(customers)
    pairs = {"".join(pair): welfare(customers, *pair)
             for pair in combinations_with_replacement(LABELS, 2)}
    optimum = max(pairs.values())
    portfolios = sorted(k for k, v in pairs.items() if v == optimum)
    outcomes = sorted({tuple(c["terminal"]) for c in certificates})
    worst = min(c["welfare"] for c in certificates)
    return {
        "unit_customers": len(customers),
        "last_player_payoff_table": values,
        "last_player_best_reply_sets": replies,
        "all_spe_ordered_outcomes": outcomes,
        "complete_spe_strategies": len(certificates),
        "minimum_spe_welfare": worst,
        "pair_coverage": pairs,
        "optimum": optimum,
        "optimal_portfolios": portfolios,
        "worst_spe_certificate": next(c for c in certificates if c["welfare"] == worst),
    }


def amplified(parameter):
    q = parameter
    return [("A", q), ("B", 3), ("C", 2), ("BC", 2 * q - 4)]


def boss_family(parameter):
    q = parameter
    return [("A", 2 * q), ("B", 2 * q), ("C", q),
            ("AC", q), ("BC", 3 * q)]


def run_family(generator, parameters, formulas, name):
    checks = []
    first = None
    for q in parameters:
        rows = generator(q)
        original = classify(expand(rows))
        reduced_rows = [(i, n) for i, n in rows if i != "C"]
        reduced = classify(expand(reduced_rows))
        expected_w, expected_opt, expected_deleted = formulas(q)
        assert original["optimal_portfolios"] == ["AB"]
        assert reduced["optimal_portfolios"] == ["AB"]
        assert original["optimum"] == reduced["optimum"] == expected_opt
        assert original["minimum_spe_welfare"] == expected_w
        assert reduced["minimum_spe_welfare"] == expected_opt
        assert len(expand(rows)) - len(expand(reduced_rows)) == expected_deleted
        assert original["all_spe_ordered_outcomes"] == [("B", "A"), ("B", "C")] if name == "amplified" else original["all_spe_ordered_outcomes"] == [("B", "C"), ("C", "B")]
        assert reduced["all_spe_ordered_outcomes"] == [("B", "A")]
        for c in (original["worst_spe_certificate"], reduced["worst_spe_certificate"]):
            assert set(c["replies"]) == set(LABELS)
        checks.append({"parameter": q, "original_minimum_spe_welfare": expected_w,
                       "reduced_minimum_spe_welfare": expected_opt,
                       "optimum_unchanged": expected_opt,
                       "deleted_customers": expected_deleted,
                       "original_ratio": Fraction(expected_opt, expected_w)})
        if first is None:
            first = {"parameter": q, "rows": rows,
                     "original": original, "reduced": reduced}
    return {"family": name, "checked_parameters": checks,
            "first_instance_all_history_tables_and_certificates": first}


def serializable(obj):
    if isinstance(obj, Fraction):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serializable(v) for v in obj]
    return obj


if __name__ == "__main__":
    report = {
        "identity": "counterexample only to deleting-OPT-external-customers min-SPE welfare monotonicity",
        "main_half_coverage_claim": "OPEN; neither proved nor refuted here",
        "method": "distinct unit customers, Fraction payoffs, exhaustive two-player full-SPE selectors",
        "finite_audit_is_not_the_universal_family_proof": True,
        "families": [
            run_family(amplified, range(4, 61), lambda q: (2*q+1, 3*q-1, 2), "amplified"),
            run_family(boss_family, range(1, 21), lambda q: (7*q, 8*q, q), "boss_9q"),
        ],
    }
    target = Path(__file__).with_name("deletion_obstruction_audit.json")
    target.write_text(json.dumps(serializable(report), indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"written": str(target), "amplified_parameters": 57,
                      "boss_family_parameters": 20, "all_checks_passed": True}))
