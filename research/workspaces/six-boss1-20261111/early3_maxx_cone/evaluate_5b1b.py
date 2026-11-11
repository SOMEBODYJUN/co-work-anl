#!/usr/bin/env python3
"""Post-freeze exact diagnosis at the specifically authorized 5b1b point."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
POINT = WORK / "maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json"
POINT_SHA = "5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe"
MATH_SHA = "66818ae8e04527b2ea0f91d9bea0ff5573e440e6c328586d640757783c4f8ab1"
INTERFACE_SHA = "96105c90656481740967e9df5d280f59e8c315464efb08b28cb287da68a6fc31"
ROWS_SHA = "ea55c096ced52605b8e03d951f0f4ea1c84130f3d05b351258b42a3be32bf5a0"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def recursive_tuple(value):
    return tuple(map(recursive_tuple, value)) if isinstance(value, list) else value


def sign(value):
    return "positive" if value > 0 else "negative" if value < 0 else "zero"


def save(name, value):
    path = HERE / name
    assert not path.exists(), ("refuse overwrite", str(path))
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


frozen_assets = []
for name, expected in [("math_freeze_manifest.json", MATH_SHA), ("interface_freeze_manifest.json", INTERFACE_SHA)]:
    path = HERE / name
    assert digest(path) == expected
    manifest = json.loads(path.read_text())
    for entry in manifest["files"]:
        assert digest(REPO / entry["path"]) == entry["sha256"]
        frozen_assets.append(entry)
assert digest(HERE / "rows_17.json") == ROWS_SHA and digest(POINT) == POINT_SHA
packet = json.loads((HERE / "rows_17.json").read_text())
old = json.loads((WORK / "early_x_anchor_queries/rows_51.json").read_text())
columns = json.loads(gzip.decompress((WORK / "early_x_anchor_queries/columns_21021.json.gz").read_bytes()))
point = json.loads(POINT.read_text())
assert [{key: value for key, value in column.items() if key != "weight"} for column in point["columns"]] == columns
values = [F(column["weight"]) for column in point["columns"]]
assert len(values) == 21021 and min(values) >= 0 and F(point["O"]) == 1
hist = {j: descriptor for j, descriptor in enumerate(columns) if descriptor["kind"] == "hist"}
xcols = {descriptor["hist_column"]: j for j, descriptor in enumerate(columns) if descriptor["kind"] == "common-X-mass"}
upper = {(descriptor["hist_column"], recursive_tuple(descriptor["query_token"])): j
         for j, descriptor in enumerate(columns) if descriptor["kind"] == "X-query-overlap-upper"}
assert len(hist) == len(xcols) == 16 and len(upper) == 420
for (h, token), j in upper.items():
    marginal = sum((F(coefficient) * values[index] for index, coefficient in columns[j]["query_marginal"]), F(0))
    assert values[j] == min(values[xcols[h]], marginal)
income = [sum((values[h] / sum(map(int, descriptor["actual_bits"]))
               for h, descriptor in hist.items() if descriptor["actual_bits"][i] == "1"), F(0)) for i in range(6)]
assert sum(income, F(0)) == F(point["W"])
kappa = sum((values[xcols[h]] / (sum(map(int, descriptor["actual_bits"][:2])) + 4)
             for h, descriptor in hist.items()), F(0))
safe = income[2] - kappa
assert safe >= 0
shift = F(8, 3) * safe
records = []
for index, row in enumerate(packet["rows"]):
    product = sum((F(coefficient) * values[j] for j, coefficient in row["row"]), F(0))
    old_row = old["rows"][row["old_row_index"]]
    old_product = sum((F(coefficient) * values[j] for j, coefficient in old_row["row"]), F(0))
    quote, correction = F(0), F(0)
    for entry in row["histogram_frequencies"]:
        h = entry["hist_column"]
        b = sum(map(int, hist[h]["actual_bits"][:2]))
        for raw_token, multiplicity in entry["frequencies"]:
            token = recursive_tuple(raw_token)
            probability = F(multiplicity, row["orbit_size"])
            if token[0] == "bit":
                marginal = values[h] * token[1]
                overlap = values[xcols[h]] * token[1]
            else:
                upper_index = upper[h, token]
                marginal = sum((F(a) * values[j] for j, a in columns[upper_index]["query_marginal"]), F(0))
                overlap = values[upper_index]
            quote += probability * marginal / (b + 1)
            correction += probability * F(3, (b + 1) * (b + 4)) * overlap
    assert product == F(61, 3) * income[2] - F(58, 3) * kappa - quote + correction
    assert old_product == product + shift
    records.append({"index": index, "name": row["name"], "orbit_id": row["orbit_id"],
                    "orbit_size": row["orbit_size"], "exact_slack": str(product), "slack_float": float(product),
                    "sign": sign(product), "old_23_slack": str(old_product), "exact_decrease": str(shift),
                    "query_quote": str(quote), "positive_overlap_correction": str(correction)})
minimum = min(F(record["exact_slack"]) for record in records)
counts = Counter(record["sign"] for record in records)
result = {"status": "EXACT_POST_FREEZE_DIAGNOSIS_COMPLETE", "point_path": str(POINT.relative_to(REPO)),
    "point_sha256": POINT_SHA, "mathematical_freeze_sha256": MATH_SHA, "interface_freeze_sha256": INTERFACE_SHA,
    "rows_sha256": ROWS_SHA, "point_W": point["W"], "point_W_float": float(F(point["W"])),
    "all_21021_descriptors_match": True, "all_coordinates_nonnegative": True, "O": "1",
    "point_reported_verified_rows": point["verified_rows"], "full_point_feasibility_reverified_here": False,
    "all_420_upper_coordinates_equal_canonical_min": True, "actual_incomes_sum_to_W": True,
    "u3": str(income[2]), "u3_float": float(income[2]), "kappa_X": str(kappa), "kappa_X_float": float(kappa),
    "SAFE3_slack": str(safe), "SAFE3_slack_float": float(safe),
    "common_17_row_slack_decrease": str(shift), "common_17_row_slack_decrease_float": float(shift),
    "row_count": len(records), "positive": counts["positive"], "zero": counts["zero"], "negative": counts["negative"],
    "minimum_exact_slack": str(minimum), "minimum_slack_float": float(minimum),
    "minimum_names": [record["name"] for record in records if F(record["exact_slack"]) == minimum],
    "all_sparse_products_equal_direct_formula": True, "all_old_to_new_decreases_equal_8_over_3_SAFE3": True,
    "point_excluded": counts["negative"] > 0, "LP_optimum_improvement_proved": False, "six_player_half_proved": False,
    "optimizer_called": False, "cb45_point_read": False, "frozen_assets_unchanged": True,
    "created_utc": datetime.now(timezone.utc).isoformat(), "rows": records}
for entry in frozen_assets:
    assert digest(REPO / entry["path"]) == entry["sha256"]
assert digest(POINT) == POINT_SHA
save("evaluation_5b1b.json", result)
assets = [Path(__file__), HERE / "evaluation_5b1b.json"]
save("evaluation_freeze_manifest.json", {"status": "POST_FREEZE_DIAGNOSIS_FROZEN", "point_sha256": POINT_SHA,
    "mathematical_freeze_sha256": MATH_SHA, "interface_freeze_sha256": INTERFACE_SHA,
    "rows": len(records), "positive": counts["positive"], "zero": counts["zero"], "negative": counts["negative"],
    "optimizer_called": False, "frozen_assets_unchanged": True,
    "files": [{"path": str(path.relative_to(REPO)), "sha256": digest(path), "bytes": path.stat().st_size} for path in assets]})
print(json.dumps({key: result[key] for key in ("status", "row_count", "positive", "zero", "negative",
    "u3_float", "kappa_X_float", "SAFE3_slack_float", "common_17_row_slack_decrease_float",
    "minimum_exact_slack", "minimum_slack_float", "minimum_names", "point_excluded")}, indent=2))
