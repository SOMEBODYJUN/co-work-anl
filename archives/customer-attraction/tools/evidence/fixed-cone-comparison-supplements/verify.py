"""Independently check the two fixed policies and their exact row certificates."""

import json
import sys
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path


REPO = Path(sys.argv[1]).resolve()
EVIDENCE = REPO / "archives/customer-attraction/tools/evidence"
TASK = "boss3-wave8-comparison-3b-6fa659bf565f1e86"
LABELS = tuple(range(5))
MASKS = tuple(range(1, 32))
HISTORIES = tuple(h for d in range(4) for h in product(LABELS, repeat=d))
OLD_TREE = "strategy-cones/original/evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json"
AVERAGE = "distinct-prefix-average-sharp-33-over-16"
INDIVIDUAL = "distinct-prefix-individual-optimal-J-13-over-4"


def read_json(path):
    return json.loads(path.read_bytes())


def pin(record):
    canonical = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()


def policy_rows(actions, comparison):
    terminals = {h: h for h in product(LABELS, repeat=4)}
    for h in reversed(HISTORIES):
        terminals[h] = terminals[h + (actions[h],)]

    def share(mask, action, ending):
        if not mask & (1 << action):
            return Fraction(0)
        return Fraction(1, sum(bool(mask & (1 << label)) for label in ending))

    true_rows = {}
    for h in HISTORIES:
        own = tuple(share(mask, actions[h], terminals[h]) for mask in MASKS)
        for action in LABELS:
            changed = terminals[h + (action,)]
            true_rows[h, action] = tuple(
                v - share(mask, action, changed) for mask, v in zip(MASKS, own, strict=True)
            )

    def average(h, alternatives):
        columns = zip(*(true_rows[h, a] for a in alternatives), strict=True)
        return tuple(sum(column) / len(alternatives) for column in columns)

    unused = {
        h: tuple(a for a in comparison if a not in h)
        for h in HISTORIES
        if len(set(h)) == len(h) and set(h) <= set(comparison)
    }
    rows = {
        "A": {h: average(h, alternatives) for h, alternatives in unused.items()},
        "F": {h: average(h, comparison) for h in HISTORIES},
        "I": {(h, a): true_rows[h, a] for h, alternatives in unused.items() for a in alternatives},
        "T": true_rows,
    }
    assert {name: len(family) for name, family in rows.items()} == {
        "A": 41, "F": 156, "I": 64, "T": 780,
    }
    assert sum(any(row) for row in rows["I"].values()) == sum(a != actions[h] for h, a in rows["I"])
    for h, alternatives in unused.items():
        columns = zip(*(rows["I"][h, a] for a in alternatives), strict=True)
        assert rows["A"][h] == tuple(sum(column) / len(alternatives) for column in columns)
    return terminals, rows


def coverage_row(group):
    group_mask = sum(1 << a for a in set(group))
    return tuple(int(bool(mask & group_mask)) for mask in MASKS)


def value(row, customers):
    return sum(row[mask - 1] * count for mask, count in customers.items())


def bounds(rows, w, o, customers, bound, dual):
    assert all(weight > 0 for weight in dual.values())
    assert all(value(rows[key], customers) == 0 for key in dual)
    residual = tuple(
        bound * w[mask - 1] - o[mask - 1] -
        sum(weight * rows[key][mask - 1] for key, weight in dual.items())
        for mask in MASKS
    )
    assert min(residual) == 0
    assert all(residual[mask - 1] == 0 for mask in customers)
    # At W=0, every feasible mass vector also has O=0 by the same identity.
    assert Fraction(value(o, customers), value(w, customers)) == bound
    assert value(w, customers) * bound == value(o, customers)
    return residual


def witness_report(rows, endings, comparison, customers):
    group_coverages = {
        ",".join(map(str, group)): value(coverage_row(group), customers)
        for group in combinations(LABELS, 4)
    }
    slacks = {
        name: {key: value(row, customers) for key, row in family.items()}
        for name, family in rows.items()
    }
    w, o = coverage_row(endings[()]), coverage_row(comparison)
    topic_sets = [tuple(mask for mask in customers if mask & (1 << a)) for a in LABELS]
    return slacks, {
        "root_path": endings[()],
        "nonempty_and_distinct_topic_sets": bool(all(topic_sets) and len(set(topic_sets)) == len(LABELS)),
        "comparison_group": comparison,
        "unit_customers_by_mask": customers,
        "W": value(w, customers),
        "O_J": value(o, customers),
        "OPT4": max(group_coverages.values()),
        "all_comparison_coverages": group_coverages,
        "slack_summary": {
            name: {"minimum": str(min(s.values())), "negative": sum(v < 0 for v in s.values()),
                   "zero": sum(v == 0 for v in s.values())}
            for name, s in slacks.items()
        },
    }


def read_and_verify_inputs():
    task = read_json(REPO / f"research/operations/map-v2/tasks/{TASK}.json")
    assert task["state"] == "claimed" and task["owner"] == "Boss3"
    definition = task["definition"]
    assert definition["stage"] == "3B"
    assert not definition["read_object_ids"] and not definition.get("overlap_comparisons")
    registry = read_json(REPO / definition["registry"])
    objects = {o["object_id"]: o for o in registry["objects"]}
    refs = definition["context_plan"]["reading_refs"]
    assert len(refs) == 13
    for ref in refs:
        content = (REPO / ref["path"]).read_bytes()
        assert sha256(content).hexdigest() == ref["sha256"]
        if ref["path"].endswith(".json"):
            json.loads(content)
        elif ref["path"].endswith(".py"):
            compile(content, ref["path"], "exec")
        else:
            content.decode()
    for object_id in definition["object_ids"]:
        assert pin(objects[object_id]) == definition["input_pins"][object_id]
    return definition


def verify():
    definition = read_and_verify_inputs()
    old = read_json(EVIDENCE / OLD_TREE)["cone_proofs"]
    assert len(old) == 70
    stored = {
        index: {tuple(r["history"]): r["action"] for r in old[index]["actions"]}
        for index in (9, 16)
    }
    action_strings = (
        "2",
        "00202",
        "0000020022022200002020022",
        "000020002002200220000200002022222000000222202020020200220202022202"
        "22220220222202020020222020200020200022222022000220202222220",
    )
    assert tuple(map(len, action_strings)) == (1, 5, 25, 125)
    actions9 = dict(zip(HISTORIES, map(int, "".join(action_strings)), strict=True))
    actions16 = {h: (2 if any(h) else 0) for h in HISTORIES}
    assert stored == {9: actions9, 16: actions16}
    action_frequencies = {index: dict(Counter(table.values())) for index, table in stored.items()}
    assert action_frequencies == {9: {0: 78, 2: 78}, 16: {0: 4, 2: 152}}
    origin = read_json(EVIDENCE / "average-and-last-payoff-resumed-boss2/original/average_probe.json")
    origin_failure = origin["failures"]["permutation_prefix"]
    assert origin_failure["cone_index"] == 9 and tuple(origin_failure["J"]) == (1, 2, 3, 4)
    assert {tuple(r["history"]): r["action"] for r in origin_failure["actions"]} == actions9
    specifications = [
        (9, "A", Fraction(33, 16), {2: 19, 5: 96, 9: 38, 17: 45},
         {(2,): Fraction(9, 4), (2, 1): Fraction(1), (2, 3): Fraction(1, 2)}),
        (9, "F", Fraction(7, 4), {4: 20, 5: 8, 9: 21}, {(2, 2, 2): Fraction(4)}),
        (9, "I", Fraction(11, 6), {3: 3, 5: 12, 9: 3, 17: 4},
         {((2,), 1): Fraction(1), ((2,), 3): Fraction(1), ((2, 3), 4): Fraction(1)}),
        (16, "I", Fraction(13, 4), {1: 11, 5: 5, 6: 12, 12: 12, 20: 12},
         {((0,), a): Fraction(3) for a in (1, 3, 4)}),
        (16, "A", Fraction(13, 4), {1: 11, 5: 5, 6: 12, 12: 12, 20: 12},
         {(0,): Fraction(9)}),
    ]
    comparison = {9: (1, 2, 3, 4), 16: (0, 1, 3, 4)}
    reconstructed = {index: policy_rows(actions, comparison[index]) for index, actions in stored.items()}
    output = {}
    runs = {}
    for index, name, bound, customers, dual in specifications:
        endings, rows = reconstructed[index]
        assert endings[()] == ((2,) * 4 if index == 9 else (0,) * 4)
        if index == 16:
            assert sum(any(row) for row in rows["I"].values()) == 63
        slacks, report = witness_report(rows, endings, comparison[index], customers)
        assert report["O_J"] == report["OPT4"] == sum(customers.values())
        assert min(slacks[name].values()) == 0
        residual = bounds(
            rows[name], coverage_row(endings[()]), coverage_row(comparison[index]),
            customers, bound, dual,
        )
        report["attained_ratio"] = str(bound)
        report["dual"] = [
            {"row": row, "weight": str(weight), "coefficients": list(map(str, rows[name][row]))}
            for row, weight in dual.items()
        ]
        report["rho_by_mask_1_to_31"] = list(map(str, residual))
        output[f"{index}:{name}"] = report
        runs[index, name] = (slacks, residual)
    s9a, r9a = runs[9, "A"]
    s9f, r9f = runs[9, "F"]
    s9i, r9i = runs[9, "I"]
    s16i, r16i = runs[16, "I"]
    s16a, r16a = runs[16, "A"]

    # Compare the exact reports to the independent calculations.
    ref_a = read_json(EVIDENCE / AVERAGE / "exact-certificate.json")
    ref_f, ref_i = read_json(EVIDENCE / AVERAGE / "exact-strengthened-check.json")
    ref_16 = read_json(EVIDENCE / INDIVIDUAL / "exact-certificate.json")
    assert r9a == tuple(Fraction(c["remainder"]) for c in ref_a["columns"])
    assert r9f == tuple(map(Fraction, ref_f["rho_in_mask_order"]))
    assert r9i == tuple(map(Fraction, ref_i["rho_in_mask_order"]))
    assert r16i == r16a == tuple(Fraction(c["remainder"]) for c in ref_16["columns"])
    assert {tuple(r["history"]): Fraction(r["slack"]) for r in
            ref_a["normalized_retained_average_slacks"]} == {h: v / 96 for h, v in s9a["A"].items()}
    assert {tuple(r["row"]): Fraction(r["slack"]) for r in ref_f["witness_slacks"]} == s9f["F"]
    assert {(tuple(r["row"][0]), r["row"][1]): Fraction(r["slack"]) for r in
            ref_i["witness_slacks"]} == s9i["I"]
    assert {(tuple(h), a): Fraction(v) for h, a, v in ref_16["kept_individual_slacks"]} == s16i["I"]
    assert {tuple(h): Fraction(v) for h, v in ref_16["kept_average_slacks"]} == s16a["A"]

    origin_rows = read_json(EVIDENCE / "average-and-last-payoff-resumed-boss2/new-average-exact-check.json")
    origin_checks = origin_rows["average_fixed_candidate"]["checks"]["all_rows"]
    assert { (tuple(r["history"]), a): Fraction(v) for r in origin_checks
             for a, v in enumerate(r["individual_slacks"])} == {k: v / 96 for k, v in s9a["T"].items()}
    assert {tuple(r["history"]): Fraction(r["full_uniform_slack"]) for r in origin_checks} == {
        h: v / 96 for h, v in s9a["F"].items()
    }
    origin16 = read_json(EVIDENCE / "continuation-dual-resumed-boss2/saved-witness-exact-check.json")
    _, rows16 = reconstructed[16]
    old_customers = {1: 16, 4: 15, 6: 12, 12: 12, 20: 12}
    old_slacks = {key: value(row, old_customers) / 16 for key, row in rows16["T"].items()}
    assert {(tuple(r["history"]), a): Fraction(v) for r in origin16["all_history_slacks"]
            for a, v in enumerate(r["normalized_slacks_by_alternative_0_to_4"])} == old_slacks
    assert (origin16["fixed_comparison_coverage"], origin16["actual_OPT4"]) == (52, 67)

    ends9, _ = reconstructed[9]
    assert {h: ends9[h] for h in ((2,), (2, 1), (2, 3), (2, 2, 2))} == {
        (2,): (2, 2, 2, 2), (2, 1): (2, 1, 2, 2),
        (2, 3): (2, 3, 2, 2), (2, 2, 2): (2, 2, 2, 2),
    }
    terminals9 = {(2, 1): (2, 1, 2, 2), (2, 3): (2, 3, 2, 2), (2, 4): (2, 4, 0, 0),
                  (2, 1, 3): (2, 1, 3, 0), (2, 1, 4): (2, 1, 4, 2),
                  (2, 3, 1): (2, 3, 1, 2), (2, 3, 4): (2, 3, 4, 2)}
    terminals9.update({(2, 2, 2, a): (2, 2, 2, a) for a in comparison[9]})
    assert all(ends9[h] == ending for h, ending in terminals9.items())
    ends16, _ = reconstructed[16]
    assert ends16[(0,)] == (0, 0, 0, 0)
    assert all(ends16[(0, a)] == (0, a, 2, 2) for a in (1, 3, 4))
    for mask, average, coefficient, residual in zip(
        MASKS, rows16["A"][(0,)],
        map(sum, zip(*(rows16["I"][(0,), a] for a in (1, 3, 4)), strict=True)),
        r16a, strict=True,
    ):
        a0 = int(bool(mask & 1))
        c = int(bool(mask & 4))
        q = sum(bool(mask & (1 << a)) for a in (1, 3, 4))
        assert average == Fraction(a0, 4) - Fraction(q, 3 * (a0 + 1 + 2 * c))
        assert 9 * average == 3 * coefficient
        assert residual == a0 + Fraction(3 * q, a0 + 1 + 2 * c) - int(a0 + q > 0)
    assert s16a == s16i
    assert {h: v for h, v in s16a["F"].items() if v < 0} == {
        (0, 0): Fraction(-3, 2), (0, 0, 0): Fraction(-6)
    }
    assert s16a["T"][(), 2] == Fraction(-25, 4)
    assert {h: v / 96 for h, v in s9a["F"].items() if v < 0} == {
        (2, 2): Fraction(-5, 256), (2, 2, 2): Fraction(-5, 64),
    }
    separators = [
        ("9:A", "I", ((2,), 3), s9a["I"][(2,), 3], Fraction(-14)),
        ("9:A", "F", (2, 2, 2), s9a["F"][(2, 2, 2)], Fraction(-15, 2)),
        ("9:F", "A", (1,), s9f["A"][(1,)], Fraction(-25, 18)),
        ("9:I", "F", (2, 2, 2), s9i["F"][(2, 2, 2)], Fraction(-1, 4)),
        ("16:A/I", "F", (0, 0, 0), s16a["F"][(0, 0, 0)], Fraction(-6)),
    ]
    assert all(found == expected < 0 for _, _, _, found, expected in separators)
    assert min(s9i["A"].values()) >= 0 and min(s16a["A"].values()) >= 0
    result = {
        "task_id": TASK,
        "registration_pins": definition["input_pins"],
        "declared_reading_refs_verified": len(definition["context_plan"]["reading_refs"]),
        "archived_action_tables_matched": [9, 16],
        "prescribed_action_frequencies": action_frequencies,
        "case_labels": {"A": "filtered average", "F": "full history all-J average",
                        "I": "filtered individual", "T": "full genuine individual comparisons"},
        "fixed_case_results": output,
        "separators_integer_scale": [
            {"witness": witness, "violated_family": family, "row": row, "slack": str(found)}
            for witness, family, row, found, _ in separators
        ],
        "policy_16_average_witness_slacks": [
            {"history": h, "slack": str(s16a["A"][h])} for h in s16a["A"]
        ],
        "policy_16_average_certificate": {
            "history": [0], "own_terminal": ends16[(0,)],
            "alternative_terminals": {a: ends16[(0, a)] for a in (1, 3, 4)},
            "weight": 9, "same_weighted_columns_as_three_individual_rows": True,
            "one_average_row_already_certifies_the_upper_bound": True,
        },
    }
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
