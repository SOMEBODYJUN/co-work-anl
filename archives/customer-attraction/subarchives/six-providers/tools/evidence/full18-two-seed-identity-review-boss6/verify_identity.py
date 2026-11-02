"""Check frozen bytes, unit-customer input identity, and saved scalar claims.

This program never imports either research program, constructs SPE outcome sets,
executes an LP, or recovers rational weights.  It only reads the six frozen files
listed in source-manifest.json.  Output is deterministic JSON on stdout.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / "original" / name).read_text())


def input_facts(seed):
    assert seed["players"] == 6 and len(seed["topics"]) == 18
    assert len(set(seed["topics"])) == 18
    support = []
    for row in seed["customers"]:
        topics, weight = row["topics"], row["multiplicity"]
        assert type(weight) is int and weight > 0
        assert topics and len(topics) == len(set(topics))
        assert all(type(a) is int and 0 <= a < 18 for a in topics)
        support.append(tuple(sorted(topics)))
    assert len(support) == len(set(support))
    # Python integers, rather than numpy.int64, establish the range first.
    total = sum(row["multiplicity"] for row in seed["customers"])
    facts = {
        "players": 6,
        "topic_labels": 18,
        "positive_distinct_interest_types": len(support),
        "unit_customers": total,
        "maximum_multiplicity_decimal_digits": max(
            len(str(row["multiplicity"])) for row in seed["customers"]
        ),
        "share_scale_60_total": 60 * total,
        "fixed_int64_bound_holds": 60 * total < 2**63,
    }
    return facts, set(support)


def welfare(seed, counts):
    assert len(counts) == 18 and all(type(c) is int and c >= 0 for c in counts)
    assert sum(counts) == 6
    return sum(
        row["multiplicity"]
        for row in seed["customers"]
        if any(counts[a] for a in row["topics"])
    )


def main():
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for entry in manifest:
        data = (HERE / entry["saved_path"]).read_bytes()
        assert len(data) == entry["size"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
    seed114 = load("research_6/seed_full18.json")
    seed88 = load("research_1/full18_vertex_seed.json")
    report = load("research_1/full18_exact_bi.json")
    recovery = load("research_1/full18_vertex_recovery.json")
    facts114, support114 = input_facts(seed114)
    facts88, support88 = input_facts(seed88)
    assert facts114["positive_distinct_interest_types"] == 114
    assert facts88["positive_distinct_interest_types"] == recovery["positive_types"] == 88
    assert facts88["maximum_multiplicity_decimal_digits"] == recovery["largest_multiplicity_digits"] == 60
    assert support88 < support114
    worst_welfare = welfare(seed114, report["worst_terminal_counts"])
    support = report["optimum_support"]
    assert len(support) == len(set(support)) == 6
    optimum_counts = [int(a in support) for a in range(18)]
    optimum_welfare = welfare(seed114, optimum_counts)
    assert worst_welfare == report["minimum_SPE_welfare"]
    assert optimum_welfare == report["OPT6"] == facts114["unit_customers"]
    ratio = Fraction(optimum_welfare, worst_welfare)
    assert str(ratio) == report["ratio"]
    assert report["strict_target_counterexample"] is (ratio > 2)
    print(json.dumps({
        "scope": "frozen-byte, input-identity and saved-scalar checks only; zero SPE, IC, LP or recovery execution",
        "verified_frozen_files": len(manifest),
        "seed114": facts114,
        "seed88": facts88,
        "support_overlap": len(support114 & support88),
        "support_removed_from_114": len(support114 - support88),
        "saved_worst_counts_direct_welfare": worst_welfare,
        "saved_optimum_support_direct_welfare": optimum_welfare,
        "saved_ratio_scalar_consistent": str(ratio),
        "root_outcome_count": {
            "saved_value": report["root_outcome_count"],
            "recomputed_now": False,
        },
        "recovery_four_fields_preserved": recovery,
        "recovery_old_policy_IC_certified_here": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
