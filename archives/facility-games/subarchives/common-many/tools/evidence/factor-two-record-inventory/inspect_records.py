"""Read every frozen record and check data accounting; run no equilibrium solver.

Input generation is reconstructed from the reviewed audit specification.
Stored strategies, counts, and loads are inspected as data. No NE, lexmax,
packing, constructor, or default-continuation algorithm is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def instance(weights, covers, m, k):
    return dict(m=m, k=k, clients=[
        dict(weight=str(F(w)), sites=sorted(c))
        for w, c in zip(weights, covers)
    ])


def expected_exact_inputs():
    result = []
    masks = [set(), {0}, {1}, {0, 1}]
    for k in (2, 3, 4):
        for weights in product((1, 2, 5), repeat=2):
            for covers in product(masks, repeat=2):
                result.append((f"exhaustive-k{k}-{len(result)}",
                               instance(weights, covers, 2, k), True, False))
    specials = [
        ("heavy-three-sites", instance([100, 1, 20], [{0, 1}, {0}, {2}], 3, 5)),
        ("orphan-overlap", instance([5, 7, 11, 1], [{0, 1}, {1, 2}, {0, 2}, {0}], 3, 3)),
        ("rational", instance([F(1, 97), F(3, 7), F(11, 13), F(2, 5)],
                             [{0}, {0, 1}, {1, 2}, {2}], 3, 4)),
        ("single-site", instance([100, 2, 3], [{0}, {0}, set()], 1, 7)),
        ("zero-clients", instance([], [], 3, 3)),
        ("unreachable-only", instance([1, 100], [set(), set()], 3, 3)),
        ("one-facility", instance([3, 7, 11], [{0}, {1}, {0, 2}], 3, 1)),
    ]
    result.extend((name, value, True, True) for name, value in specials)
    rng = random.Random(20261002)
    for j in range(120):
        m, k, n = rng.choice((2, 3)), rng.choice((2, 3, 4, 5, 6)), rng.randrange(1, 7)
        weights = [F(rng.choice((1, 2, 3, 7, 19, 101)), rng.choice((1, 1, 2, 7)))
                   for _ in range(n)]
        covers = [{s for s in range(m) if rng.randrange(3)} for _ in range(n)]
        result.append((f"random-{j}", instance(weights, covers, m, k),
                       j < 15 and n <= 4 and k <= 4,
                       j < 12 and n <= 4 and k <= 4))
    for k in (7, 12, 25, 50):
        result.append((f"growing-k-{k}",
                       instance([k * k, 1, 2 * k], [{0, 1}, {0}, {2}], 3, k),
                       False, False))
    return result


def inspect_exact(data):
    assert set(data) == {
        "claim", "evidence_kind", "seed", "python", "full_proof", "cases",
        "actual_deviations", "unlisted_labeled_layouts_checked",
        "independent_labeled_lexmax_comparisons", "independent_pure_NE_extremum_comparisons",
        "packing_cases", "mutations_rejected", "feature_counts", "results",
    }
    assert data["claim"] == "SC-K-2-E"
    assert data["evidence_kind"] == "finite exact arithmetic attacks only"
    assert data["seed"] == 20261002 and data["python"] == "3.13.5"
    assert data["full_proof"] == "research/current/multi_facility/uniform_two.md"
    expected = expected_exact_inputs()
    rows = data["results"]
    assert len(rows) == len(expected) == data["cases"] == 563
    assert len({row["name"] for row in rows}) == 563
    groups, factors, inputs = defaultdict(Counter), Counter(), set()
    reverse, full_random, zero, zero_deviations = [], [], [], 0
    fields = {"name", "instance", "on_path_layout", "lex_key",
              "actual_certificate_factor", "actual_deviations_checked",
              "unlisted_labeled_layouts_checked"}
    for row, (name, inst, full, rev) in zip(rows, expected):
        assert set(row) == fields
        assert row["name"] == name and row["instance"] == inst
        inputs.add(json.dumps(inst, sort_keys=True))
        k, m, n = inst["k"], inst["m"], len(inst["clients"])
        layout, loads = row["on_path_layout"], list(map(F, row["lex_key"]))
        assert len(layout) == k and layout == sorted(layout)
        assert all(type(s) is int and 0 <= s < m for s in layout)
        assert len(loads) == k and loads == sorted(loads)
        assert sum(loads, F(0)) == sum(
            (F(c["weight"]) for c in inst["clients"] if set(c["sites"]) & set(layout)), F(0))
        no_reach = not any(c["sites"] for c in inst["clients"])
        assert all(a == 0 for a in loads) if no_reach else all(a > 0 for a in loads)
        factor = F(row["actual_certificate_factor"])
        assert 1 <= factor <= 2
        factors[factor] += 1
        actual = k * (m - 1)
        unlisted = m ** k - 1 - actual if full else 0
        assert row["actual_deviations_checked"] == actual
        assert row["unlisted_labeled_layouts_checked"] == unlisted
        group = ("exhaustive" if name.startswith("exhaustive") else
                 "random" if name.startswith("random") else
                 "growing" if name.startswith("growing") else "special")
        groups[group].update(cases=1, clients=n, actual_deviations=actual,
                             unlisted_layout_checks=unlisted, full_flags=int(full),
                             reverse_flags=int(rev), zero_reach_inputs=int(no_reach))
        if rev:
            reverse.append(dict(name=name, pure_extremum_comparisons=actual if k <= 4 and n <= 4 else 0))
        if group == "random" and full:
            full_random.append(name)
        if no_reach:
            zero.append(name)
            zero_deviations += actual
    assert sum(g["actual_deviations"] for g in groups.values()) == data["actual_deviations"] == 2220
    assert sum(g["unlisted_layout_checks"] for g in groups.values()) == data["unlisted_labeled_layouts_checked"] == 2770
    assert len(reverse) == data["independent_labeled_lexmax_comparisons"] == 11
    assert sum(r["pure_extremum_comparisons"] for r in reverse) == data["independent_pure_NE_extremum_comparisons"] == 43
    features = data["feature_counts"]
    assert features == dict(singleton_departures=91, nonsingleton_departures=2026,
                            occupied_targets=338, unoccupied_targets=1779,
                            isolated_giants=1470, strict_customer_moves=885)
    assert features["singleton_departures"] + features["nonsingleton_departures"] == 2220 - zero_deviations
    assert features["occupied_targets"] + features["unoccupied_targets"] == 2220 - zero_deviations
    assert data["packing_cases"] == 267 and data["mutations_rejected"] == 3
    maximum = max(factors)
    return dict(
        groups=dict(groups), total_clients=sum(g["clients"] for g in groups.values()),
        distinct_ordered_instance_jsons=len(inputs), all_generated_inputs_equal=True,
        all_layout_load_mass_sums_equal=True, actual_factor_distribution={str(q): c for q, c in sorted(factors.items())},
        maximum_stored_actual_factor=str(maximum),
        maximum_factor_rows=[row for row in rows if F(row["actual_certificate_factor"]) == maximum],
        full_random_records=full_random, independent_comparison_records=reverse,
        zero_reach_records=zero, zero_reach_deviations=zero_deviations,
        feature_departure_denominator=2220 - zero_deviations,
        source_only_aggregate_fields=dict(packing_cases=data["packing_cases"],
                                          mutations_rejected=data["mutations_rejected"],
                                          isolated_giants=features["isolated_giants"],
                                          strict_customer_moves=features["strict_customer_moves"]),
        limitation="Stored rows omit probabilities, customer site assignments, deviation strategies and movement traces; no NE or optimum is reverified here.",
    )


def inspect_barrier(data):
    assert set(data) == {"claim", "evidence_kind", "python", "cases", "actual_deviations",
                         "independent_labeled_lexmax_enumerations", "results"}
    assert data["claim"] == "SC-K-LEXMAX-BARRIER"
    assert data["evidence_kind"] == "Exact finite attacks, not the all-k/all-h proof"
    assert data["python"] == "3.13.5"
    rows = data["results"]
    assert len(rows) == data["cases"] == 20
    counts, summaries = Counter(), []
    clients = slots = unserved = 0
    fields = {"instance", "k", "h", "lexmax_occupancy", "lexmax_layout_optimum",
              "full_instance_optimum", "exact_SPE_layout", "witnesses"}
    for row, (k, h) in zip(rows, product((2, 3, 4, 7, 12), (2, 7, 31, 1024))):
        assert set(row) == fields and (row["k"], row["h"]) == (k, h)
        anchor = F(3 * (h + 1), 4)
        expected = instance([h, 1] + [anchor] * (k - 2),
                            [{0, 1}, {0}] + [{j} for j in range(2, k)], k, k)
        assert row["instance"] == expected
        bad, good = [0, 0] + list(range(2, k)), [1, 0] + list(range(2, k))
        assert row["lexmax_occupancy"] == bad and row["exact_SPE_layout"] == good
        assert F(row["lexmax_layout_optimum"]) == F(2 * h, h + 1)
        assert row["full_instance_optimum"] == "1"
        witness_rows = row["witnesses"]
        expected_keys = {(tag, f, r) for tag, layout in [("lexmax", bad), ("exact", good)]
                         for f in range(k) for r in range(k) if r != layout[f]}
        actual_keys = set()
        for wit in witness_rows:
            assert set(wit) == {"profile", "facility", "target", "pure_assignment", "deviator_load"}
            tag, f, r = wit["profile"], wit["facility"], wit["target"]
            actual_keys.add((tag, f, r))
            assert (tag, f, r) in expected_keys
            layout = (bad if tag == "lexmax" else good).copy()
            layout[f] = r
            pure = wit["pure_assignment"]
            assert len(pure) == k
            for i, g in enumerate(pure):
                available = [j for j, s in enumerate(layout) if s in expected["clients"][i]["sites"]]
                assert type(g) is int
                assert g in available if available else g == -1
            load = sum((F(c["weight"]) for c, g in zip(expected["clients"], pure) if g == f), F(0))
            assert F(wit["deviator_load"]) == load
            expected_load = h if tag == "lexmax" and f < 2 and r == 1 else 1 if tag == "exact" and f == 0 and r == 0 else 0
            assert load == expected_load
            counts[(tag, str(load))] += 1
            slots += len(pure)
            unserved += pure.count(-1)
        assert actual_keys == expected_keys and len(witness_rows) == len(expected_keys) == 2 * k * (k - 1)
        clients += k
        summaries.append(dict(k=k, h=h, stored_witnesses=len(witness_rows),
                              lexmax_factor=row["lexmax_layout_optimum"],
                              independent_lexmax_flag=k <= 4 and h in (2, 7)))
    assert sum(counts.values()) == data["actual_deviations"] == 1552
    assert sum(r["independent_lexmax_flag"] for r in summaries) == data["independent_labeled_lexmax_enumerations"] == 6
    return dict(cases=summaries, stored_clients=clients, stored_assignment_slots=slots,
                unserved_assignment_slots=unserved,
                witness_load_counts=[dict(profile=tag, load=load, count=count)
                                     for (tag, load), count in sorted(counts.items())],
                all_actual_deviation_keys_present_once=True,
                all_stored_assignments_feasible=True, all_stored_deviator_loads_recomputed=True,
                limitation="Data feasibility and loads are inspected; no best-response, lexmax, or mixed-equilibrium optimization is run. Earlier full barrier replay remains the NE audit.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite an existing inspection report")
    root = Path(__file__).resolve().parent
    values, sources = {}, []
    specifications = [
        ("exact", "frozen_exact.json", "2cdff156aaa9614bb607", "ea1a4c9ee4cd4a73284639a82ad0a6f3877b5e88ebc9f9bf938e1701051bb6de", 372123, inspect_exact),
        ("barrier", "frozen_lexmax_barrier.json", "754b7f16d578df1fd751", "f4d19e9fc3ea7fa21487e55ef9084c6e9e31f76e241d6cc9b3b32e48267bf3e5", 527820, inspect_barrier),
    ]
    for tag, filename, sid, digest, size, inspect in specifications:
        raw = (root / filename).read_bytes()
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == digest
        values[tag] = inspect(json.loads(raw))
        sources.append(dict(id=sid, retained_file=filename, sha256=digest,
                            size_bytes=size, byte_hash_verified=True))
    result = dict(frozen_commit="68fad804ec5946cb296f77dc5b336308a66abf12",
                  sources=sources, **values, equilibrium_audits_executed=False,
                  scope="Complete static record accounting and input generation reconstruction only.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(exact_records=563, barrier_records=20, stored_barrier_witnesses=1552,
                          equilibrium_audits_executed=False)))


if __name__ == "__main__":
    main()
