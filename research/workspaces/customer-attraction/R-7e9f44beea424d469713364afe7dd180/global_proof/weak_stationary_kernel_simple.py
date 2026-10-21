"""Explicit compact full SPE for the prescribed stationary-kernel counterexample."""
from itertools import product
import json
from pathlib import Path


PRIORITY = (3, 2, 4, 1)


def unused_special(history):
    return next(a for a in PRIORITY if a not in history)


def action(history):
    if len(history) == 0:
        return 1
    if len(history) == 1:
        return (3, 2, 2, 2, 4)[history[0]]
    if len(history) == 2:
        first, second = history
        if 0 in history:
            return unused_special(history)
        if first == second:
            return 0
        if first == 1:
            return unused_special(history)
        if first in (2, 4):
            return second
        assert first == 3
        return first
    assert len(history) == 3
    if 0 in history or history[2] not in history[:2]:
        return unused_special(history)
    return 0


if __name__ == "__main__":
    record = {
        "identity": "compact explicit full SPE; failure only of prescribed root-stationary weak cap",
        "main_half_coverage_claim": "OPEN",
        "instance": {"topics": ["T0", "T1", "T2", "T3", "T4"],
                     "customers": [{"topics": [0], "multiplicity": 5}]
                     + [{"topics": [a], "multiplicity": 2} for a in range(1, 5)]
                     + [{"topics": [1, 2, 3, 4], "multiplicity": 12}],
                     "players": 4},
        "actions": [{"history": list(h), "action": action(h)}
                    for n in range(4) for h in product(range(5), repeat=n)],
        "root_counts": [0, 1, 1, 1, 1],
        "stationary_distribution": ["1/4", "0", "7/24", "1/3", "1/8"],
        "root_followers": [[0, 0, 1, 1, 1], [0, 0, 1, 1, 1],
                           [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 0, 1, 1]],
        "query": 1, "scaled_cap_to_welfare": "161/160",
    }
    target = Path(__file__).with_name("weak_stationary_kernel_simple.json")
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(str(target))
