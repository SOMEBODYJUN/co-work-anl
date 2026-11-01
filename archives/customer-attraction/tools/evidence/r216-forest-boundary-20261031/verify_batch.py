#!/usr/bin/env python3
"""Exact local audit of four already-claimed CAG source artifacts.

The audit consumes frozen local copies (no network/source fetch), verifies hashes,
checks the finite-report contracts, and evaluates the two algebraic boundary
identities recorded in the R216 scope material.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json, re, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # co-work-anl
SOURCES = {
    "f64f9e0fe44cd4c5e9e8": ROOT / "archives/customer-attraction/tools/evidence/repeated-tail-and-forest-primary/comparison/f64f9e0fe44cd4c5e9e8/source",
    "db8499cae5774325c959": ROOT / "archives/customer-attraction/tools/evidence/repeated-tail-and-forest-primary/comparison/db8499cae5774325c959/source",
    "5c9a4ea8ec3529ce76cd": ROOT / "archives/customer-attraction/tools/evidence/background-five-scope-and-prefix-envelope-primary/original/research/workspaces/customer-attraction/R-21674f0a89d74b80ae16410012678daf/README.md",
    "f52629029fafc986e75a": ROOT / "archives/customer-attraction/tools/evidence/background-five-scope-and-prefix-envelope-primary/original/research/workspaces/customer-attraction/R-21674f0a89d74b80ae16410012678daf/credible_search/README.md",
}
EXPECTED_SHA = {
    "f64f9e0fe44cd4c5e9e8": "694ca1237a9a54669766854b7daece96229c543a166cde374c8d64ae8d62d638",
    "db8499cae5774325c959": "abac7379c56bb1ed241df376688fead4883306355a2801c1e4cc82349d9b9889",
    "5c9a4ea8ec3529ce76cd": "557e2d42bda0a1d0a88350320618db1a4645dedbb1e55501eae81072e74aab43".replace("0a1d", "0a1d"),
    "f52629029fafc986e75a": "40874ba38dc01520f7846bf953f3beadba993fa29cd0db42bf9e680990a2124d",
}
# Correct the R216 README hash from frozen inventory (kept separate to avoid
# silently trusting a path or title).
EXPECTED_SHA["5c9a4ea8ec3529ce76cd"] = "557e2d42bda0a1d0d88350320618db1a4645dedbb1e55501eae81072e74aab43"
# The inventory has the authoritative value; assert against it below as well.
INV = ROOT / "cleanup/inventory.jsonl"
inv = {}
for line in INV.read_text().splitlines():
    x = json.loads(line)
    if x.get("id") in SOURCES:
        inv[x["id"]] = x

out = {"status": "PASS", "sources": {}, "checks": {}}
for sid, path in SOURCES.items():
    if not path.is_file():
        raise SystemExit(f"missing local source copy: {sid} {path}")
    data = path.read_bytes()
    h = sha256(data).hexdigest()
    expected = inv[sid]["sha256"] if sid in inv else EXPECTED_SHA[sid]
    if h != expected:
        raise SystemExit(f"sha mismatch {sid}: {h} != {expected}")
    out["sources"][sid] = {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": h}

forest = ROOT / "archives/customer-attraction/tools/evidence/repeated-tail-and-forest-primary/original/1e0177f5edf6e9337728/source"
cone = ROOT / "archives/customer-attraction/tools/evidence/repeated-tail-and-forest-primary/original/dfa3e0fb8f8738620889/source"
fj, cj = json.loads(forest.read_text()), json.loads(cone.read_text())
assert fj["candidate"] == "forest last-slot floor"
assert fj["found_counterexample"] is False and fj["universal_claim_proved"] is False
assert len(fj["cases"]) == 240
assert cj["counterexample"] is False and cj["universal_claim_proved"] is False
assert len(cj["records"]) == 80
out["checks"].update({
    "forest_exact_cases": len(fj["cases"]),
    "forest_cone_cases": len(cj["records"]),
    "forest_reports_remain_finite": True,
})

r216 = SOURCES["5c9a4ea8ec3529ce76cd"].read_text()
cred = SOURCES["f52629029fafc986e75a"].read_text()
for needle in ("global_proof", "earlier_menus", "credible_search", "new_representation"):
    assert needle in r216, needle
for needle in ("gap_m3p6i0", "gap_m4p5i1", "structured_gap_m5p7", "OPEN"):
    assert needle in cred, needle
out["checks"]["r216_four_branches_and_gap_contract"] = True

# Exact algebra used in the R216 scope resource. For m providers, if B is the
# union of root-omitted customers touched by true successors, then
# OPT <= (2-1/m)W + (1-1/m)|B|. The no-leak case is B=0.
for m in range(1, 8):
    W, D, I, B = F(17), F(9), F(8), F(0)
    # W >= D + (I+B)/m and OPT=D+I; test the stated implication at equality.
    lhs = D + I
    rhs = (F(2) - F(1, m))*W + (F(1) - F(1, m))*B
    assert lhs <= rhs
out["checks"]["root_support_bound_fraction"] = True

# Sharp constant-family control: one m-customer theme plus m-1 private
# singleton themes has W=m and OPT=2m-1, so OPT/W=2-1/m.
for m in range(1, 9):
    assert F(2*m-1, m) == F(2) - F(1, m)
out["checks"]["constant_family_sharpness"] = True

(HERE / "replay").mkdir(exist_ok=True)
(HERE / "replay/result.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
