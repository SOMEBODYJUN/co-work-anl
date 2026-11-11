#!/usr/bin/env python3
"""Replay the complete frozen records and derive exact 5/4 schedules for both cubes."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "archives/unrelated-machines/tools/evidence/unit-configuration-tree-originals"
SOURCE = EVIDENCE / "original/unit_readout_two_tree_actual_certificates.json"
SOURCE_SHA = "b44ee0f44485f2e1497b87338106d642beaa85b96196a810c569b4d120febefd"
VARIABLES = range(7)
CLAUSES = range(128)
DIGITS = range(4)
INTERNAL = 294
DENOMINATOR = 128 ** 7


def compare_matrices(scaled, unit):
    """Check the same internal machines and one-to-one job and clause wiring."""
    assert scaled["machines"][:INTERNAL] == unit["machines"][:INTERNAL]
    for a, b in zip(scaled["original_jobs"], unit["original_jobs"], strict=True):
        if a["kind"] == "leaf_port":
            assert {k: v for k, v in a.items() if k != "eligible"} == {
                k: v for k, v in b.items() if k != "eligible"
            }
        else:
            assert a == b
    for record, width in ((scaled, 1), (unit, 4)):
        assert [(m["clause"], m["slot"]) for m in record["machines"][INTERNAL:]] == list(
            product(CLAUSES, range(width))
        )

    collapse = [
        i if i < INTERNAL else INTERNAL + (i - INTERNAL) // 4
        for i in unit["sigma"]
    ]
    assert collapse == scaled["sigma"]
    assigned = Counter()
    lifted = []
    for i in scaled["sigma"]:
        if i < INTERNAL:
            lifted.append(i)
        else:
            lifted.append(INTERNAL + 4 * (i - INTERNAL) + assigned[i])
            assigned[i] += 1
    assert lifted == unit["sigma"]


def conditional_choices(by_clause):
    """Minimize the expected number of overfull clauses at each exposed choice."""
    signs = {}
    drops = {}

    def leaf_probability_numerator(variable, sign, word):
        chosen = signs.get(variable)
        if chosen is not None and chosen != sign:
            return 0
        free_nodes = 0
        for depth, digit in enumerate(word):
            dropped = drops.get((variable, sign, word[:depth]))
            if dropped == digit:
                return 0
            free_nodes += dropped is None
        scale = (2 if chosen is None else 1) * 4 ** free_nodes
        return (128 * 3 ** free_nodes) // scale

    def expectation_numerator():
        result = 0
        for clause in by_clause:
            low = [1, 0, 0, 0, 0]
            for leaf in clause:
                yes = leaf_probability_numerator(*leaf)
                no = 128 - yes
                low = [no * low[0]] + [
                    no * low[count] + yes * low[count - 1] for count in range(1, 5)
                ]
            result += DENOMINATOR - sum(low)
        return result

    current = expectation_numerator()
    initial = Fraction(current, DENOMINATOR)
    assert initial == Fraction(3358203845373, 4398046511104) < 1

    def choose(table, key, choices):
        nonlocal current
        possibilities = []
        for choice in choices:
            table[key] = choice
            possibilities.append((expectation_numerator(), choice))
        assert sum(value for value, _ in possibilities) == len(choices) * current
        current, best = min(possibilities)
        table[key] = best

    for variable in VARIABLES:
        choose(signs, variable, range(2))
    for variable, sign in signs.items():
        level = [()]
        for _ in range(3):
            next_level = []
            for word in level:
                key = (variable, sign, word)
                choose(drops, key, DIGITS)
                next_level.extend(word + (digit,) for digit in DIGITS if digit != drops[key])
            level = next_level
    assert current == 0
    assert list(signs.values()) == [0] * 7
    assert len(drops) == 91 and set(drops.values()) == {0}
    return signs, drops, initial


def materialize(record, signs, drops):
    internal = {
        (m["variable"], m["sign"], tuple(m["word"])): i
        for i, m in enumerate(record["machines"]) if m["kind"] == "internal"
    }
    sigma = []
    load = [Fraction(0) for _ in record["machines"]]
    outgoing = [0] * len(CLAUSES)
    for row in record["original_jobs"]:
        variable = row["variable"]
        kind = row["kind"]
        if kind == "selector":
            destination = internal[variable, signs[variable], ()]
        else:
            sign = row["sign"]
            word = tuple(row["word"])
            keep_path = signs[variable] == sign
            for depth, digit in enumerate(word):
                dropped = drops.get((variable, sign, word[:depth]))
                keep_path &= dropped is not None and dropped != digit
            parent = internal[variable, sign, word[:-1]]
            if not keep_path:
                destination = parent
            elif kind == "tree_edge":
                destination = internal[variable, sign, word]
            else:
                assert kind == "leaf_port"
                clause = row["clause"]
                external = sorted(int(i) for i in row["eligible"] if int(i) != parent)
                destination = external[outgoing[clause]] if len(external) == 4 else external[0]
                outgoing[clause] += 1
        sigma.append(destination)
        load[destination] += Fraction(row["eligible"][str(destination)])
    assert len(sigma) == 1183
    assert Counter(load[:INTERNAL]) == {Fraction(1): 203, Fraction(5, 4): 91}
    assert max(load[INTERNAL:]) == 1
    assert Counter(outgoing) == {0: 48, 1: 7, 2: 41, 3: 28, 4: 4}
    assert sum(outgoing) == 189
    return {
        "makespan": str(max(load)),
        "machines": len(load),
        "jobs": len(sigma),
        "load_histogram": {str(value): count for value, count in sorted(Counter(load).items())},
        "sigma_sha256": sha256(json.dumps(sigma, separators=(",", ":")).encode()).hexdigest(),
    }


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == SOURCE_SHA
    document = json.loads(raw)
    source_code = EVIDENCE / "original/unit_readout_two_tree_certificates.py"
    check_certificates = run_path(str(EVIDENCE / "replay.py"))["certificates"]
    counts, _ = check_certificates(document, sha256(source_code.read_bytes()).hexdigest())

    scaled = document["examples"]["single_endpoint_source_NO_escape"]
    unit = document["examples"]["unit_slot_source_NO_escape"]
    compare_matrices(scaled, unit)
    by_clause = [[] for _ in CLAUSES]
    for row in scaled["original_jobs"]:
        if row["kind"] == "leaf_port":
            by_clause[row["clause"]].append((row["variable"], row["sign"], tuple(row["word"])))
    assert all(sorted(leaf[0] for leaf in clause) == list(VARIABLES) for clause in by_clause)
    signs, drops, initial = conditional_choices(by_clause)

    result = {
        "frozen_source_sha256": SOURCE_SHA,
        "frozen_record_checks": counts,
        "initial_expected_overfull_clauses": str(initial),
        "chosen_signs_by_variable": list(signs.values()),
        "discarded_digit_at_all_91_active_nodes": 0,
        "clause_outgoing_histogram": [48, 7, 41, 28, 4],
        "scaled_single": materialize(scaled, signs, drops),
        "unit_slots": materialize(unit, signs, drops),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
