"""Compare the frozen result JSON with source replay outputs.
The frozen file omits the current source's scope/individual metadata fields.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
frozen = json.loads((HERE.parent / "refined_fractional_scan_results.json").read_text())
common = json.loads((HERE / "refined_fractional_scan_results_common_replay.json").read_text())
individual = json.loads((HERE / "refined_fractional_scan_individual_results_replay.json").read_text())
normalized = {k: {kk: vv for kk, vv in v.items() if kk not in {"scope", "individual"}} for k, v in individual.items()}
summary = {
    "frozen_sha256": "0aa1ae244810ecad26a9d1b32f8bfcbc4b86c87a8b0ad9d9964b4d8692ba44cd",
    "frozen_matches_individual_after_metadata_strip": frozen == normalized,
    "frozen_matches_common_replay": frozen == common,
    "frozen_keys": list(frozen),
    "frozen_optima_lengths": {k: len(v["optima"]) for k, v in frozen.items()},
    "common_optima_lengths": {k: len(v["optima"]) for k, v in common.items()},
    "individual_optima_lengths": {k: len(v["optima"]) for k, v in individual.items()},
    "common_metadata": {k: {"scope": v.get("scope"), "individual": v.get("individual")} for k, v in common.items()},
    "individual_metadata": {k: {"scope": v.get("scope"), "individual": v.get("individual")} for k, v in individual.items()},
}
if not summary["frozen_matches_individual_after_metadata_strip"]:
    raise SystemExit("frozen JSON does not match normalized individual replay")
print(json.dumps(summary, indent=2, ensure_ascii=False))
(HERE / "comparison.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
