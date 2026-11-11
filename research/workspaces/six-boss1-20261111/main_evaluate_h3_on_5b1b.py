"""Evaluate the previously frozen, independently audited H3 rows at the new exact point."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

W = Path(__file__).resolve().parent
point_file = W / "maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json"
rows_file = W / "maxb_h3_bridge/rows_17.json"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(point_file) == "5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe"
assert sha(rows_file) == "3c9d360cbb0313ae84b4be7add4f4b3f6b67ba57f71cb8f366a2341e8f128d8d"
point = json.loads(point_file.read_text())
data = json.loads(rows_file.read_text())
x = [F(col["weight"]) for col in point["columns"]]
assert len(x) == data["full_dimension"] == 21021
values = []
for entry in data["rows"]:
    value = sum((F(c) * x[int(j)] for j, c in entry["row"]), F(0)) - F(entry["rhs"])
    values.append({"name": entry["name"], "query_members": entry["query_members"],
                   "value": str(value), "float": float(value)})
hist = []
for j in range(20585, 20601):
    descriptor = {k: v for k, v in point["columns"][j].items() if k != "weight"}
    hist.append({"column": j, "descriptor": descriptor, "weight": str(x[j])})
out = {
    "status": "EXACT_EVALUATION_OF_FROZEN_H3_NECESSARY_ROWS",
    "scope": "This supplied X and its supplied upper-envelope overlaps only; negative rows need not exclude reselected X/overlaps.",
    "point_sha256": sha(point_file), "rows_sha256": sha(rows_file),
    "point_W": point["W"], "row_count": len(values),
    "positive": sum(F(v["value"]) > 0 for v in values),
    "zero": sum(F(v["value"]) == 0 for v in values),
    "negative": sum(F(v["value"]) < 0 for v in values),
    "minimum": min(values, key=lambda v: F(v["value"])),
    "values": values, "common_X_histograms": hist,
    "optimizer_calls": 0, "script_sha256": sha(Path(__file__)),
}
target = W / "main_h3_on_5b1b.json"
assert not target.exists()
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ("status", "positive", "zero", "negative", "minimum")}, ensure_ascii=False, indent=2))
