"""Unit-set/Fraction replay of a symbolic multisource-pivot obstruction."""
from fractions import Fraction as F
from pathlib import Path
import json


def audit(m):
    sets = [{("x", i), ("y", i)} for i in range(m)]
    sets += [{("x", i) for i in range(m)}]
    universe = set().union(*sets)
    assert len(universe) == 2*m
    assert len(set(map(frozenset, sets))) == m+1

    def utility(path, selected):
        return sum((F(1, sum(x in sets[a] for a in path)) for x in sets[selected]), F(0))

    def kernel(sources):
        total = F(0)
        for x in universe:
            d = sum(x in sets[a] for a in sources)
            total += int(d > 0) + F(max(0, d-1), m)
        return total

    original = tuple(range(m))
    initial = kernel(original)
    assert initial == 2*m
    for b in range(m):
        values = [utility((b,)*(m-1)+(a,), a) for a in range(m+1)]
        assert values[b] == F(2, m)
        assert all(values[a] == 2 for a in range(m) if a != b)
        assert values[m] == m-1+F(1,m)
        assert all(values[m] > values[a] for a in range(m))
        for a in range(m):
            updated = original[:a] + (m,) + original[a+1:]
            assert kernel(updated) == initial-F(1,m)
    return {"m": m, "customers": 2*m, "OPT": 2*m,
            "all_clone_unique_BR": "R", "clone_nodes": m,
            "checked_updates": m*m, "K_initial": str(initial),
            "K_after_every_update": str(initial-F(1,m)), "loss": str(F(1,m))}


if __name__ == "__main__":
    records = [audit(m) for m in range(3, 21)]
    result = {"scope": "Single-source clone-reply nondecreasing-kernel obstruction only",
              "Q_CAG_HALF": "OPEN", "budget_version": "not settled", "records": records}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"checked_m": [3,20], "clone_nodes": sum(r["clone_nodes"] for r in records),
                      "single_source_updates": sum(r["checked_updates"] for r in records),
                      "all_checks_passed": True}))
