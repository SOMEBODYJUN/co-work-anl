"""Independently rebuild all 560 saved records; do not import the generator.

Closed rational/combinatorial formulas check metadata and counts. A fresh
definition-level policy evaluator checks every actual-path action, every
preselected far witness, and all ordered nodes/actions when m <= 4. The five
large tail domains are counted by stars and bars here, not re-enumerated.
"""
from fractions import Fraction
from itertools import product
from math import comb, lcm
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "original/path_tail_obstruction_audit.json"
TAIL_CASES = {(2, 1), (3, 1), (4, 2), (5, 2), (7, 1)}


def evaluate_case(m, k, radius):
    n = m - k
    d = n - radius
    scale = lcm(*range(1, d + 1))
    topic_count = n + m
    sizes = [scale // max(d - j, 1) for j in range(n)] + [scale] * m

    def prescribed(history):
        t = len(history)
        if t < n:
            wrong_positions = [j for j, a in enumerate(history) if a != j]
            if not wrong_positions:
                return t
            if len(wrong_positions) > radius:
                return history[wrong_positions[0]]
        used = set(history)
        return min(set(range(n, topic_count)) - used)

    def terminal_after_action(history, action):
        terminal = list(history)
        terminal.append(action)
        while len(terminal) < m:
            terminal.append(prescribed(terminal))
        return tuple(terminal)

    def payoff(history, action):
        terminal = terminal_after_action(history, action)
        return Fraction(sizes[action], terminal.count(action))

    actual_path_checks = 0
    for t in range(m):
        history = tuple(range(t))
        assert prescribed(history) == t
        actual = payoff(history, t)
        assert actual == sizes[t]
        for a in range(topic_count):
            assert actual >= payoff(history, a), (m, k, radius, history, a)
            actual_path_checks += 1

    full_ordered_checks = 0
    negatives = []
    if m <= 4:
        for t in range(m):
            for history in product(range(topic_count), repeat=t):
                chosen = prescribed(history)
                actual = payoff(history, chosen)
                for a in range(topic_count):
                    alternative = payoff(history, a)
                    full_ordered_checks += 1
                    if alternative > actual:
                        distance = sum(a != j for j, a in enumerate(history))
                        assert t < n and distance > radius
                        negatives.append({
                            "m": m, "k": k, "radius": radius,
                            "history": list(history), "chosen": chosen,
                            "deviation": a, "actual": str(actual),
                            "deviation_utility": str(alternative),
                            "margin": str(actual - alternative),
                        })
        assert full_ordered_checks == sum(topic_count ** (t + 1) for t in range(m))

    far = None
    if d >= 2:
        history = tuple(range(n, n + radius + 1))
        chosen = prescribed(history)
        deviation = n + radius + 1
        actual = payoff(history, chosen)
        alternative = payoff(history, deviation)
        assert chosen == n and actual == Fraction(scale, d)
        assert alternative == scale and actual < alternative
        assert len(history) < n
        assert sum(a != j for j, a in enumerate(history)) == radius + 1
        far = {"history": list(history), "u": str(actual),
               "deviation_u": str(alternative)}

    harmonic = sum((Fraction(1, j) for j in range(1, d + 1)), Fraction(0))
    welfare = scale * (harmonic + radius + k)
    assert welfare.denominator == 1
    welfare = welfare.numerator
    optimum = m * scale
    tail_count = (topic_count * sum(comb(topic_count + t - 1, t) for t in range(n, m))
                  if radius == 0 and (m, k) in TAIL_CASES else 0)
    return {
        "m": m, "k": k, "radius": radius, "n": n, "d": d,
        "scale": scale, "W": welfare, "OPT": optimum,
        "ratio": str(Fraction(optimum, welfare)), "OPT_minus_2W": optimum - 2 * welfare,
        "all_path_comparisons": actual_path_checks,
        "tail_count_comparisons": tail_count,
        "full_ordered_comparisons": full_ordered_checks,
        "negative_offpath_early_comparisons": len(negatives),
        "first_offpath_failure": far,
    }, negatives


def main():
    saved = json.loads(SOURCE.read_text())
    records = []
    negative_rows = []
    first_crossing = {}
    for m in range(2, 16):
        for k in range(1, m):
            for radius in range(m - k):
                record, negatives = evaluate_case(m, k, radius)
                records.append(record)
                negative_rows.extend(negatives)
                if record["OPT_minus_2W"] > 0:
                    first_crossing.setdefault(f"k{k}_r{radius}", m)
    expected = {
        "status": "exact finite implementation audit; not a general proof or SPE counterexample",
        "cases": len(records),
        "first_half_failures_per_k_in_range": first_crossing,
        "records": records,
    }
    assert expected == saved, "complete JSON differs, including an extra/missing field"
    assert len(records) == comb(16, 3) == 560
    (BASE / "independent-full-negative-rows.json").write_text(
        json.dumps(negative_rows, indent=2) + "\n")
    columns = list(records[0])
    with (BASE / "complete-field-ledger.tsv").open("w") as f:
        f.write("\t".join(columns) + "\n")
        for record in records:
            f.write("\t".join(json.dumps(record[c], separators=(",", ":"))
                              for c in columns) + "\n")
    print(json.dumps({
        "status": "PASS",
        "all_original_json_fields_equal": True,
        "original_generator_imported": False,
        "canonical_solver_imported": False,
        "cases": len(records),
        "d1_cases": sum(r["d"] == 1 for r in records),
        "dge2_cases_with_negative_witness": sum(r["first_offpath_failure"] is not None for r in records),
        "formal_path_below_half_cases": sum(r["OPT_minus_2W"] > 0 for r in records),
        "actual_path_action_comparisons_independently_replayed":
            sum(r["all_path_comparisons"] for r in records),
        "tail_count_action_comparisons_independently_counted_not_replayed":
            sum(r["tail_count_comparisons"] for r in records),
        "small_full_ordered_action_comparisons_independently_replayed":
            sum(r["full_ordered_comparisons"] for r in records),
        "negative_small_full_action_comparisons": len(negative_rows),
        "full_ordered_case_rows": [r for r in records if r["m"] <= 4],
        "tail_count_case_rows": [r for r in records if r["tail_count_comparisons"]],
        "first_half_failures_per_k_in_range": first_crossing,
        "all_d1_have_full_welfare": all(r["W"] == r["OPT"] for r in records if r["d"] == 1),
        "all_formal_below_half_have_negative_witness":
            all(r["first_offpath_failure"] is not None for r in records if r["OPT_minus_2W"] > 0),
        "largest_saved_ratio": max((Fraction(r["ratio"]), r["m"], r["k"], r["radius"])
                                   for r in records)[0].__str__(),
        "general_parameter_claim_proved_by_this_run": False,
    }, indent=2))


if __name__ == "__main__":
    main()
