"""Main independently rebuilds actual3 -> A6 AP from raw histogram bits."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

W = Path(__file__).resolve().parent
point_file = W / "maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json"
rows_file = W / "early_x_anchor_queries/rows_51.json"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(point_file) == "5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe"
assert sha(rows_file) == "0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb"
point = json.loads(point_file.read_text())
packet = json.loads(rows_file.read_text())
cols = point["columns"]
row = {}
terms = []
u = s = quote = correction = F(0)
for xcol in range(20585, 20601):
    hcol = cols[xcol]["hist_column"]
    h = cols[hcol]
    bits = [int(z) for z in h["actual_bits"]]
    assert len(bits) == 6 and h["kind"] == "hist"
    b = sum(bits[:2])
    total = sum(bits)
    hc = (F(23 * bits[2], total) if total else F(0)) - F(bits[5], b + 1)
    xc = -F(22, b + 4) + F(3 * bits[5], (b + 1) * (b + 4))
    if hc:
        row[hcol] = hc
    if xc:
        row[xcol] = xc
    H, X = F(h["weight"]), F(cols[xcol]["weight"])
    u += F(bits[2], total) * H if total else F(0)
    s += X / (b + 4)
    quote += F(bits[5], b + 1) * H
    correction += F(3 * bits[5], (b + 1) * (b + 4)) * X
    terms.append({"hist_column": hcol, "X_column": xcol, "actual_bits": h["actual_bits"],
                  "source_background": b, "hist_coefficient": str(hc), "X_coefficient": str(xc)})
entry = packet["rows"][39]
assert {int(j): F(c) for j, c in entry["row"]} == row
assert all(j < 20601 for j in row)
value = sum((c * F(cols[j]["weight"]) for j, c in row.items()), F(0))
assert value == 23 * u - 22 * s - quote + correction
assert value == -F(2387360308883849167939463658247160398139890481107232380975950684899327,
                  167642800338353195761909644781419248132422636155436956133783540969055432)
out = {
    "status": "PASS_RAW_ACTUAL_BITS_TO_25_COEFFICIENT_AP3_ROW",
    "point_sha256": sha(point_file), "row_packet_sha256": sha(rows_file),
    "histograms": 16, "nonzeros": len(row), "unknown_y_coefficients": 0,
    "u3": str(u), "kappa3_X": str(s), "A6_quote": str(quote),
    "overlap_correction": str(correction), "value": str(value), "float": float(value),
    "row": [[j, str(c)] for j, c in sorted(row.items())], "terms": terms,
    "scope": "Excludes this supplied X even if all 420 y are reselected; not a statement about every X on the full optimum face.",
    "optimizer_calls": 0, "script_sha256": sha(Path(__file__)),
}
dest = W / "main_ap3_cut_audit.json"
assert not dest.exists()
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ("status", "nonzeros", "unknown_y_coefficients", "value", "float")}, indent=2))
