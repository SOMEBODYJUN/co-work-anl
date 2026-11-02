"""One fixed-input replay using the preserved original internal audit.

This imports no discovery/optimization implementation and is not a newly
independent audit. It reuses the original independent audit's row functions,
compares its fixed certificate result to the frozen report, and exports the
complete 64-block minimum table used in the self-contained mathematical text.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json

BASE = Path(__file__).resolve().parent
audit_path = BASE / "original/audit_background_maxroot.py"
spec = importlib.util.spec_from_file_location("original_background_audit", audit_path)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
certificate_path = BASE / "original/research_1/background_maxroot_certificate.json"
saved = json.loads(certificate_path.read_text())
weights = {name: F(value) for name, value in saved["multipliers"].items()}
B, C = F(saved["B"]), F(saved["C"])
D = 5317833390130
scale = 60 * D
assert B > 0 and C == -7 and saved["M"] == 6
assert len(weights) == 25 and all(weight > 0 for weight in weights.values())
union_weight = sum(weight for name, weight in weights.items() if name.endswith("O"))
assert union_weight == 1

minimum = None
zeros = 0
count = 0
background_minima = {0: None, 1: None}
blocks = {}
actual_state_counts = {0: 0, 1: 0}
for bits in product((0, 1), repeat=11):
    member = dict(zip(audit.LABELS, bits))
    residuals = []
    for optimum_bit in (0, 1):
        residual = B * audit.payoff(member, "actual", 0) + C * member["T"] - optimum_bit
        residual -= sum(weight * audit.slack(member, optimum_bit, name)
                        for name, weight in weights.items())
        assert residual >= 0, (bits, optimum_bit, residual)
        assert (scale * residual).denominator == 1
        minimum = residual if minimum is None else min(minimum, residual)
        background_minima[member["Z"]] = residual if background_minima[member["Z"]] is None else min(background_minima[member["Z"]], residual)
        zeros += residual == 0
        count += 1
        residuals.append(residual)
    assert residuals[0] == residuals[1]
    actual_state_counts[member["Z"]] += 1
    key = "".join(str(member[x]) for x in "ZTABCD")
    value = int(scale * residuals[0])
    blocks[key] = value if key not in blocks else min(blocks[key], value)

result = {"status": "passed", "states": count,
          "positive_multipliers": len(weights), "B": str(B), "C": str(C),
          "minimum_residual": str(minimum), "zero_residual_states": zeros,
          "minimum_by_background_bit": {str(k): str(v) for k, v in background_minima.items()},
          "comparison_bit_eliminated": True, "imports_discovery_code": False}
frozen = json.loads((BASE / "original/background_maxroot_independent_audit.json").read_text())
assert result == frozen
assert count == 4096 and len(blocks) == 64 and min(blocks.values()) == 0
table = {"scale": scale, "weight_common_denominator": D,
         "block_prefix_order": "ZTABCD", "minimized_bits_order": "QRSXY",
         "minimized_states_per_block": 32,
         "unique_membership_states": 2048, "literal_states_including_union_bit": count,
         "all_block_minima_nonnegative": True, "minima": blocks}
(BASE / "replay-result.json").write_text(json.dumps(result, indent=2) + "\n")
(BASE / "complete-block-minima.json").write_text(json.dumps(table, indent=2) + "\n")
lines = ["| ABCD | ZT=00 | ZT=01 | ZT=10 | ZT=11 |", "|---|---:|---:|---:|---:|"]
for actual in product((0, 1), repeat=4):
    key = "".join(map(str, actual))
    lines.append("| " + key + " | " + " | ".join(str(blocks[zt + key]) for zt in ("00", "01", "10", "11")) + " |")
(BASE / "complete-block-minima-table.md").write_text("\n".join(lines) + "\n")
(BASE / "execution-scope.json").write_text(json.dumps({
    "script": "replay_and_table.py", "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    "reused_original_audit_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
    "original_discovery_executed": False, "author_verifier_executed": False,
    "uses_original_internal_audit_row_functions": True,
    "new_independent_audit_claimed": False,
    "frozen_report_matches_exactly": True,
    "comparison_metadata_checked": ["B", "C", "M", "positive_multipliers", "minimum_residual", "states", "comparison_bit_coefficient"],
    "certificate_metadata_consistent": saved["states"] == count and saved["positive_multipliers"] == len(weights) and saved["minimum_residual"] == str(minimum) and F(saved["comparison_bit_coefficient"]) == union_weight
}, indent=2) + "\n")
print(json.dumps({"status": result["status"], "literal_states": count,
                  "unique_states": 2048, "blocks": len(blocks), "scale": scale,
                  "frozen_report_exact_match": True, "zero_states": zeros}, indent=2))
