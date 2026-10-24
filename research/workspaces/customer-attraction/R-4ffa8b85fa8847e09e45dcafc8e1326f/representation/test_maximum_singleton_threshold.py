"""Countertest one general conjecture, not Q-CAG-HALF.

Candidate: if B maximizes sum_{x in B} 1/(b_x+1), then the exact
credibility threshold cannot increase after inserting B. Uses the canonical
all-SPE count correspondence, not a fixed anonymous strategy.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import CustomerType, Instance


def compositions(total, size):
    for sequence in combinations_with_replacement(range(size), total):
        yield tuple(sequence.count(i) for i in range(size))


def check(instance):
    solver = ExactSPESolver(instance)
    k = instance.topic_count
    for length in range(instance.players - 1):
        for b in compositions(length, k):
            values = tuple(sum((Fraction(c.multiplicity,
                                             1 + sum(b[j] for j in c.topics))
                                for c in instance.customers if a in c.topics),
                               Fraction(0)) for a in range(k))
            maximum = max(values)
            floor = solver.threshold(b)
            for a, value in enumerate(values):
                if value != maximum:
                    continue
                child = list(b)
                child[a] += 1
                after = solver.threshold(child)
                if after > floor:
                    return {"instance": instance.to_dict(), "background": b,
                            "maximum_singleton_topic": a,
                            "singleton_values": list(map(str, values)),
                            "before_threshold": str(floor),
                            "after_threshold": str(after),
                            "before_outcomes": sorted(solver.outcomes(b)),
                            "after_outcomes": sorted(solver.outcomes(child))}
    return None


def main():
    source = ROOT / "examples/customer_attraction/aggregate_theta_failure.json"
    instance = Instance.from_dict(json.loads(source.read_text()))
    result = check(instance)
    if result is None:
        raise AssertionError("expected the existing 36-customer certificate to separate")
    result["source"] = str(source.relative_to(ROOT))
    result["candidate_status"] = "FALSE"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
