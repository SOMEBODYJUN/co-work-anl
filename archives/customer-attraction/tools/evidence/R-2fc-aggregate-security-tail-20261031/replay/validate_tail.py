#!/usr/bin/env python3
"""Validate frozen aggregate-security tail JSONs without upgrading their truth status."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original"
EXPECTED = {
    "6c9d817c586d116a7ef2_dr_groups_repeats.json": {
        "sha256": "7326bbbb32e5c5bf5d8699bd40fdc560a653cc0180b9750bed072af11bfbb344",
        "size": 543, "objective": 0.0, "seed": 22112, "trials": 1,
        "flags": {"harmonic_repeats": True, "harmonic_diagonals": False, "third_positive": False},
    },
    "615b20e056941847ca2d_dr_groups_simple_query.json": {
        "sha256": "437ca2a9912cb89807768e4e47c5a4d4fb8b7825fa75ad8c58b43c229d08d3d5",
        "size": 10684, "objective": -0.0003226252477301038, "seed": 22112, "trials": 1,
        "flags": {"harmonic_repeats": False, "harmonic_diagonals": False, "third_positive": False},
    },
    "29bbc735344948028c8b_dr_groups_simple_query_diag.json": {
        "sha256": "7257dc41b6323375b68e2f13cca58a25e9e2cbdce0f12cc7abdf9a4f0d15d1c8",
        "size": 10680, "objective": -0.00028658162935766944, "seed": 22112, "trials": 1,
        "flags": {"harmonic_repeats": False, "harmonic_diagonals": True, "third_positive": False},
    },
    "e66595d9da26cedb6334_dr_groups_third.json": {
        "sha256": "a8c7bfec15afa8b38f620c307affcb74d50cb1058426c51db6a7937698bd7506",
        "size": 10710, "objective": -0.0002817921983817029, "seed": 22112, "trials": 1,
        "flags": {"harmonic_repeats": False, "harmonic_diagonals": False, "third_positive": True},
    },
    "4b98a2950c56d94cfbf5_dr_n3k3.json": {
        "sha256": "8982c1bc83539d5344584976fa49032098f213d3b8c0da6131c42b7ebe13bb32",
        "size": 324, "objective": 0.0, "seed": 22101, "trials": 100,
        "flags": {},
    },
    "8cda73aa604b09b9b171_dr_n3k4.json": {
        "sha256": "7b833afb8d1da92bc952b7a9914513d4bc17b6b2622c70443ab1552c0f60a396",
        "size": 324, "objective": 0.0, "seed": 22102, "trials": 100,
        "flags": {},
    },
}
STATUS = "floating diagnostic in an enlarged model, not CAG evidence"
QUERY = "4/15,0,4/15,0,3/15,4/15"
P = [4/15, 0.0, 4/15, 0.0, 3/15, 4/15]

errors = []
for name, exp in EXPECTED.items():
    path = ORIGINAL / name
    if not path.is_file():
        errors.append(f"missing {name}"); continue
    data = path.read_bytes()
    got_sha = hashlib.sha256(data).hexdigest()
    if len(data) != exp["size"]: errors.append(f"size {name}: {len(data)} != {exp['size']}")
    if got_sha != exp["sha256"]: errors.append(f"sha {name}: {got_sha} != {exp['sha256']}")
    try: obj = json.loads(data)
    except Exception as exc:
        errors.append(f"json {name}: {exc}"); continue
    if obj.get("status") != STATUS: errors.append(f"status {name}")
    if obj.get("completed") != exp["trials"]: errors.append(f"completed {name}: {obj.get('completed')}")
    if obj.get("best_objective") != exp["objective"]: errors.append(f"objective {name}: {obj.get('best_objective')!r}")
    args = obj.get("args", {})
    if args.get("seed") != exp["seed"] or args.get("trials") != exp["trials"]: errors.append(f"seed/trials {name}")
    for key, val in exp["flags"].items():
        if args.get(key, False) != val: errors.append(f"flag {name}.{key}: {args.get(key)!r}")
    if "groups_" in name:
        for key, val in (("k", 6), ("n", 3), ("query", QUERY), ("policy", "groups"), ("no_dr", False), ("iterations", 1), ("first", 0)):
            if args.get(key) != val: errors.append(f"arg {name}.{key}: {args.get(key)!r}")
        witness = obj.get("witness")
        if name.startswith("6c9d"):
            if witness is not None: errors.append(f"unexpected witness {name}")
        elif not isinstance(witness, dict):
            errors.append(f"missing witness {name}")
        else:
            if witness.get("root") != [0, 3, 4]: errors.append(f"root {name}: {witness.get('root')!r}")
            if witness.get("p") != P: errors.append(f"p {name}: {witness.get('p')!r}")
            if len(witness.get("policy", {})) != 43: errors.append(f"policy count {name}")
            if len(witness.get("states", [])) != 83: errors.append(f"state count {name}")
            if len(witness.get("potential", [])) != 83: errors.append(f"potential count {name}")
            for field in ("value_lower", "welfare"):
                if not isinstance(witness.get(field), (int, float)) or not math.isfinite(witness[field]): errors.append(f"nonfinite {name}.{field}")
    else:
        if "witness" in obj: errors.append(f"unexpected witness {name}")
    print(f"OK {name} bytes={len(data)} sha256={got_sha} objective={obj.get('best_objective')!r}")

if errors:
    for e in errors: print("ERROR", e)
    raise SystemExit(1)
print(f"validated {len(EXPECTED)} JSON sources; no exact CAG claim inferred")
