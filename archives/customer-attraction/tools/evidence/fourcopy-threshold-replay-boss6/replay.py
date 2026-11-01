"""Recheck the frozen four-copy certificate, with the forced-player guard."""
from pathlib import Path
from fractions import Fraction
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("frozen_verifier", HERE / "original/fourcopy_verify.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
certs = json.loads((HERE / "original/fourcopy_threshold_exact.json").read_text())
reports = []
for cert in certs:
    assert cert["n"] == 6 and cert["copies"] == 4
    for key, value in cert["multipliers"].items():
        if not Fraction(value):
            continue
        if key.startswith("PAIR:"):
            # Branch 4 forces the penultimate player; only its last player optimizes.
            assert int(key.split(":")[1]) < 4, key
        if key.startswith("FLOOR:"):
            _, branch, player, _ = key.split(":")
            branch, player = int(branch), int(player)
            assert player >= (1 if branch == 0 else branch + 1), key
    reports.append(module.verify(cert))
expected = json.loads((HERE / "original/fourcopy_threshold_check.json").read_text())
parent = json.loads((HERE / "original/fourcopy_threshold_replay.json").read_text())
# Normalize integer dictionary keys before comparing the entire report.
normalized = json.loads(json.dumps(reports))
assert normalized == expected == parent
(HERE / "replay.json").write_text(json.dumps(reports, indent=2) + "\n")
print(json.dumps({"certificates": len(reports), "types_per_certificate": 65536,
                  "all_original_report_fields_equal": True,
                  "forced_player_guard": "passed",
                  "independent_implementation": False}))
