"""Check every saved epigraph budget against the separate exact query oracle."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from transport_separator import Point, row_specs, budgets, single_row_lower_cost


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("point", type=Path)
    parser.add_argument("epigraph", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    point = Point(args.point)
    raw = args.epigraph.read_bytes()
    epigraph = json.loads(raw)
    assert epigraph["input_sha256"] == hashlib.sha256(point.raw).hexdigest()
    saved = {item["name"]: F(item["value"])
             for item in epigraph["canonical_extension_at_input"]["budget_rows"]}
    checks = []
    for family in ("B2", "B3", "B4", "Mroot"):
        specs = row_specs(point.labels[family])
        for spec, budget in zip(specs, budgets(point, family, specs)):
            if spec[0] == "new-to-R":
                name = f"tail-budget:{family}:{spec[1]}:R"
            elif spec[0] == "new-to-Z":
                name = f"tail-budget:{family}:{spec[1]}:Z"
            else:
                name = f"Z-budget:{family}:{spec[1]}:{spec[3]}"
            value = budget - single_row_lower_cost(point, family, spec)
            assert saved[name] == value, (name, saved[name], value)
            checks.append({"name": name, "exact_slack": str(value)})
    assert len(checks) == len(saved) == 81
    report = {
        "scope": "all 81 epigraph budgets matched to separate greedy/positive-part query minima",
        "epigraph_sha256": hashlib.sha256(raw).hexdigest(),
        "input_sha256": hashlib.sha256(point.raw).hexdigest(),
        "matched_budget_rows": 81,
        "negative_budget_rows": sum(F(item["exact_slack"]) < 0 for item in checks),
        "checks": checks}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "checks"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
