from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"

EXPECTED = {
    "audit_tail_pne_bridge.json": "4a208a4cd9aa0856e4c894cab1050aeecd077497b8215d77c56c2907b6da1631",
    "audit_tail_pne_bridge.py": "b1b104006d53ab0a73b05ed52144f52703a663b30fd4b7a5b54118c8a9725f92",
    "probe_direct_floor.py": "d1cce9460be05890190b5d63c99fa7cda3e61f31512b3bb0886bf280ccf78879",
    "probe_observer_pne.py": "63ff62374859673d131ebf488d6d6202959283b9c7d90de468008217d84a1f1f",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for name, expected in EXPECTED.items():
        got = sha(SOURCE / name)
        assert got == expected, (name, got, expected)

    frozen = (SOURCE / "audit_tail_pne_bridge.json").read_bytes()
    replay = (ROOT / "audit_tail_pne_bridge.replay.json").read_bytes()
    assert frozen == replay
    data = json.loads(frozen)
    assert data["unit_customers"] == 54
    assert data["tail_prescription"] == {"first": 0, "last_reply": [1, 5, 5, 5, 5, 2]}
    assert data["first_tail_true_payoffs"] == ["53/3", "14", "15", "10", "25/2", "17"]
    assert data["actual_old_payoff"] == "44/3"
    assert data["static_tail_profiles_checked"] == 36
    assert data["static_individual_comparisons_including_self"] == 432
    assert data["static_tail_pne"] == [
        {"tail_actions": [2, 5], "all_payoffs": ["21", "15", "17"]},
        {"tail_actions": [5, 2], "all_payoffs": ["21", "17", "15"]},
    ]
    assert data["strict_old_payoff_gap"] == "19/3"

    direct_lines = (ROOT / "probe_direct_floor.stdout").read_text().splitlines()
    assert len(direct_lines) == 2
    direct = [ast.literal_eval(line) for line in direct_lines]
    assert direct[0]["m"] == 4 and direct[0]["max_comparison_over_root"] == 7.0 and direct[0]["direct_threshold"] == 8
    assert direct[1]["m"] == 3 and direct[1]["max_comparison_over_root"] == 4.205623901581722 and direct[1]["direct_threshold"] == 6
    assert all(row["max_comparison_over_root"] < row["direct_threshold"] for row in direct)

    observer = json.loads((ROOT / "probe_observer_pne.stdout").read_text())
    assert observer["iteration"] == 125
    assert observer["k"] == 6 and observer["root"] == 1
    assert observer["tail_spe"] == [0, 1]
    assert observer["spe_root_payoff"] == "44/3"
    assert observer["min_pne_root_payoff"] == "21"
    assert observer["tail_pnes"] == [[2, 5], [5, 2]]
    assert observer["first_tail_threshold"] == "53/3"
    print(json.dumps({"status": "PASS", "source_hashes": EXPECTED, "audit_byte_identical": True,
                      "direct_floor_rows": 2, "observer_iteration": 125}, indent=2))


if __name__ == "__main__":
    main()
