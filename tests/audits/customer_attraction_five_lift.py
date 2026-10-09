"""Verify the exact five-player two-root lift obstruction using Fraction.

Recreates every row family from the mathematical definitions, and evaluates
all 460 inequalities on the saved 23-mask feasible point. No LP dependency,
game solver, strategy enumeration, or claim about actual SPE welfare is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/five_lift_relaxation.json"
LABELS = ("A1", "A2", "A3", "A4", "A5", "Q2", "Q3", "Q4", "Q5", "R2", "R3", "R4", "R5")
EXPECTED_O = F(5700963986023035330, 2504954701286191687)


def ratio(count: int, background: int) -> F:
    """Total attraction payoff with zero-count terms defined as zero."""
    return F(count, background + count) if count else F(0)


def own_share(own: int, total_load: int) -> F:
    return F(own, total_load) if own else F(0)


def node_rows(bits: tuple[int, ...], node: str, own_pay: F,
              prefix: int, remaining: int) -> Iterator[tuple[str, str, F, int]]:
    for label, bit in zip(LABELS, bits):
        yield f"{node}:guarantee:{label}", "node_topic_guarantees", own_pay - F(bit, prefix + remaining), 0
    yield (f"{node}:optimal_aggregate", "node_optimal_aggregates",
           5 * remaining * own_pay + F(prefix, prefix + remaining), -1)


def tax_rows(bits: tuple[int, ...], node: str, first_pay: F,
             second_pay: F, prefix: int, first_bit: int
             ) -> Iterator[tuple[str, str, F, int]]:
    h = first_pay + second_pay + F(first_bit, (prefix + 1) * (prefix + 2))
    yield f"{node}:optimal_pair_aggregate", "tax_optimal_aggregates", F(5, 2) * h + F(prefix, prefix + 1), -1
    for j, k in combinations_with_replacement(range(len(LABELS)), 2):
        count = bits[j] + bits[k]
        yield (f"{node}:pair:{LABELS[j]}:{LABELS[k]}", "tax_topic_pairs",
               h - ratio(count, prefix), 0)


def rows_for_customer(bits: tuple[int, ...]) -> Iterator[tuple[str, str, F, int]]:
    """Return (row name, family, multiplicity coefficient, O coefficient)."""
    assert len(bits) == 13 and set(bits) <= {0, 1}
    actual_total = sum(bits[:5])
    actual_pay = [own_share(bits[i], actual_total) for i in range(5)]
    for i in range(5):
        yield from node_rows(bits, f"actual:{i + 1}", actual_pay[i], sum(bits[:i]), 5 - i)
    yield from tax_rows(bits, "actual:last_two", actual_pay[3], actual_pay[4], sum(bits[:3]), bits[3])

    for root, path, branch in ((3, (5, 6, 7, 8), "Q"), (4, (9, 10, 11, 12), "R")):
        total = bits[root] + sum(bits[j] for j in path)
        branch_pay = [own_share(bits[j], total) for j in path]
        yield (f"branch:{branch}:root", "root_comparisons",
               actual_pay[0] - own_share(bits[root], total), 0)
        for position in range(4):
            prefix = bits[root] + sum(bits[j] for j in path[:position])
            yield from node_rows(bits, f"branch:{branch}:{position + 2}", branch_pay[position], prefix, 4 - position)
        prefix = bits[root] + sum(bits[j] for j in path[:2])
        yield from tax_rows(bits, f"branch:{branch}:last_two", branch_pay[2], branch_pay[3], prefix, bits[path[2]])


def check(certificate_path: Path = DEFAULT_CERTIFICATE) -> dict[str, object]:
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    assert certificate["claim"] == "CA-FIVE-LIFT-ROWS-NO"
    assert certificate["players"] == 5
    assert tuple(certificate["labels"]) == LABELS
    assert certificate["branches"] == [
        {"root_topic": "A4", "successors": ["Q2", "Q3", "Q4", "Q5"]},
        {"root_topic": "A5", "successors": ["R2", "R3", "R4", "R5"]},
    ]
    auxiliary_o = F(certificate["auxiliary_O"])
    assert auxiliary_o == EXPECTED_O and auxiliary_o > 2

    support = []
    memberships = set()
    for entry in certificate["support"]:
        membership = entry["membership"]
        assert len(membership) == 13 and set(membership) <= {"0", "1"}
        assert "1" in membership and membership not in memberships
        memberships.add(membership)
        mass = F(entry["multiplicity"])
        assert mass > 0
        support.append((tuple(map(int, membership)), mass))
    assert len(support) == 23
    actual_welfare = sum((mass for bits, mass in support if any(bits[:5])), F(0))
    assert actual_welfare == 1

    totals: dict[str, F] = {}
    metadata: dict[str, tuple[str, int]] = {}
    for bits, mass in support:
        seen = set()
        for name, family, coefficient, o_coefficient in rows_for_customer(bits):
            assert name not in seen
            seen.add(name)
            if name not in metadata:
                metadata[name] = (family, o_coefficient)
                totals[name] = F(0)
            assert metadata[name] == (family, o_coefficient)
            totals[name] += mass * coefficient
        assert len(seen) == 460
    slacks = {name: value + metadata[name][1] * auxiliary_o for name, value in totals.items()}
    assert len(slacks) == certificate["constraint_rows"] == 460
    assert all(value >= 0 for value in slacks.values())
    counts = Counter(family for family, _ in metadata.values())
    assert counts == {
        "node_topic_guarantees": 169,
        "node_optimal_aggregates": 13,
        "root_comparisons": 2,
        "tax_optimal_aggregates": 3,
        "tax_topic_pairs": 273,
    }

    # These are boundary formula checks, not equilibrium tests.
    assert ratio(0, 0) == 0
    assert own_share(0, 0) == 0
    assert len(tuple(rows_for_customer((0,) * 13))) == 460
    assert all(coefficient == 0 for _, _, coefficient, _ in rows_for_customer((0,) * 13))

    return {
        "claim": "CA-FIVE-LIFT-ROWS-NO",
        "all_exact_checks_passed": True,
        "auxiliary_O": str(auxiliary_o),
        "normalized_actual_W": str(actual_welfare),
        "auxiliary_O_minus_2W": str(auxiliary_o - 2 * actual_welfare),
        "support_masks": len(support),
        "verified_constraint_rows": len(slacks),
        "row_family_counts": dict(counts),
        "tight_rows": sum(value == 0 for value in slacks.values()),
        "minimum_slack": str(min(slacks.values())),
        "row_slacks": {name: str(value) for name, value in slacks.items()},
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Feasible relaxation certificate; O is auxiliary, not actual optimum. Not a game, SPE, or half-coverage counterexample.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-slacks", action="store_true")
    args = parser.parse_args()
    result = check(args.certificate)
    if not args.include_slacks:
        result.pop("row_slacks")
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
