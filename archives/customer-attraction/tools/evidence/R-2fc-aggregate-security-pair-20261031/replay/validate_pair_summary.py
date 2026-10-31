#!/usr/bin/env python3
"""Validate the recorded pair-source metadata without changing its truth status."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "sources-summary.json").read_text())
assert data["common_status"] == "floating diagnostic in an enlarged model, not CAG evidence"
expected = {
    "ab961a55539ea83079c6": ("pair_groups_dr_n3k6.json", 10615, "9d3fbd61b8d468f5a2c6f8a79189cfcab91679d4ec95a2174527ae2e60f36f91", -0.00028370513150265814, 1),
    "1245e6ccbc103168b87b": ("pair_groups_monotone_n3k6.json", 9986, "ee929e5985bbd984824e8c84d77bebdcf07c26d27cd4802e3ff3be6dde7e7e55", -0.001265207200675137, 1),
    "5683f1468fa9f737c779": ("pair_monotone_policy_n4k4.json", 403, "ad888e0c6748d4ba91f951e71b9659103f677ea9cfd0f9713ed0b7b59c6f1924", 0.0, 500),
    "ec8ea7d2aeb9864b6398": ("pair_plateau_n3k4.json", 396, "5eaffa11863fa9324aed8ac9180f2f41e11b2d3ac7a002253eb8492bd2da7b0b", 0.0, 1000),
    "4efc80407211435b8fa1": ("verify_dr_boundary.py", 3967, "fe073ff8428f8c8a0428b2aa1edf4b7abd2d58a9e1cf64770c24da60041e791e", None, None),
}
got = {x["id"]: x for x in data["sources"]}
assert set(got) == set(expected)
for sid, (name, size, sha, objective, completed) in expected.items():
    row = got[sid]
    assert row["file"] == name and row["size"] == size and row["sha256"] == sha
    assert row["raw_read"] is True and row["disposition"] == "integrated"
    if objective is not None:
        assert row["best_objective"] == objective and row["completed"] == completed
print("validated 4 floating pair JSON records and 1 exact verifier source metadata record")
print("all five dispositions=integrated; common status remains not CAG evidence")
