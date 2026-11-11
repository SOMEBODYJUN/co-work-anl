#!/usr/bin/env python3
"""Read-only release gate and exact model contract. No optimizer imports."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = HERE.parent / "visible_maximum_joint_v4"
N, M, Q = 513, 1586, 2
PREFIX_ROWS, NEW_ROWS = 1050, 536
BIT_ORDER = ["a1", "a2", "a3", "a4", "a5", "a6", "x", "o", "c"]
WAITING = "WAITING_INPUT_AND_MAIN_RELEASE"
RELEASE_STATUS = "MAIN_EXPLICIT_FULL1586_RAW_RELEASE"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def exact_sparse(value, label):
    require(isinstance(value, dict), label + " must be sparse exact JSON")
    result = {}
    for key, coefficient in value.items():
        j = int(key)
        require(str(j) == key and 0 <= j < N, label + ": invalid column")
        require(isinstance(coefficient, str), label + ": nonexact coefficient")
        result[j] = F(coefficient)
    return result


def write_new(path, value):
    with path.open("x") as output:
        output.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def status():
    return {
        "status": WAITING,
        "input_exists": (SOURCE / "exact_input.json").is_file(),
        "main_release_exists": (HERE / "main_release.json").is_file(),
        "consumption_marker_exists": (HERE / "single_lp_consumed.json").exists(),
        "expected_raw_rows": M, "expected_columns": N, "expected_equalities": Q,
        "optimizer_called_by_status": 0,
        "note": "Existence alone is not authorization; load_released verifies the complete gate.",
    }


def pinned_repo_file(relative, expected):
    require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
            "Missing exact SHA release for " + str(relative))
    path = (REPO / relative).resolve()
    path.relative_to(REPO)
    require(path.is_file(), "Missing released source: " + str(relative))
    require(digest(path) == expected, "SHA mismatch: " + str(relative))
    return path


def load_released():
    """No default input SHA and no fallback to any predecessor input or solver."""
    release_path = HERE / "main_release.json"
    require(release_path.is_file(), WAITING + ": no main_release.json")
    release = read_json(release_path)
    require(release.get("status") == RELEASE_STATUS, "Not an explicit v4 LP release")
    require(release.get("authorized_by") == "/root", "Release owner must be Main")
    require(release.get("optimizer_calls_authorized") == 1, "Exactly one call required")
    require(release.get("owner") == "Boss1" and release.get("RUN") == "six-boss1-20261111",
            "Release scope mismatch")
    require(isinstance(release.get("explicit_main_instruction"), str)
            and bool(release["explicit_main_instruction"].strip()), "Missing Main instruction")
    expected_path = str((SOURCE / "exact_input.json").relative_to(REPO))
    require(release.get("input_path") == expected_path, "Only the v4 input can be consumed")
    required_assets = {
        "exact_input.json": "input_sha256",
        "freeze_manifest.json": "preparation_manifest_sha256",
        "numerical_scaling.json": "scaling_sha256",
        "source_review.md": "source_review_sha256",
        "source_pins.json": "source_pins_sha256",
    }
    pins = {}
    for filename, key in required_assets.items():
        relative = str((SOURCE / filename).relative_to(REPO))
        pinned_repo_file(relative, release.get(key))
        pins[relative] = release[key]
    sources = read_json(SOURCE / "source_pins.json")["sources"]
    for relative, expected in sources.items():
        pinned_repo_file(relative, expected)
        pins[relative] = expected
    preparation = read_json(SOURCE / "freeze_manifest.json")
    if "artifacts" in preparation:
        artifacts = {
            str((SOURCE / relative).resolve().relative_to(REPO)):
            entry["sha256"] if isinstance(entry, dict) else entry
            for relative, entry in preparation["artifacts"].items()
        }
    else:
        require("artifact_sha256" in preparation, "Unknown prepared manifest interface")
        artifacts = preparation["artifact_sha256"]
    for relative, expected in artifacts.items():
        pinned_repo_file(relative, expected)
        pins[relative] = expected
    evidence = release.get("required_evidence")
    require(isinstance(evidence, list) and evidence, "Missing released preflight/audit evidence")
    main_preflight_seen = False
    for item in evidence:
        path = pinned_repo_file(item["path"], item["sha256"])
        evidence_data = read_json(path)
        require(evidence_data.get("status") == item["expected_status"],
                "Released evidence is not the expected result: " + item["path"])
        require(str(item["expected_status"]).startswith("PASS"), "Non-PASS evidence")
        if item["role"] == "main_preflight":
            key = item.get("input_sha256_key", "input_sha256")
            require(evidence_data.get(key) == release["input_sha256"],
                    "Main preflight is not bound to this input")
            main_preflight_seen = True
        pins[item["path"]] = item["sha256"]
    require(main_preflight_seen, "Main's exact v4 preflight is required")
    data = read_json(SOURCE / "exact_input.json")
    scaling = read_json(SOURCE / "numerical_scaling.json")
    require(data["variables"] == N and data["raw_inequality_count"] == M
            and data["equality_count"] == Q, "1586/513/2 contract changed")
    require(data["nonnegative_columns"] == list(range(N)), "A nonnegative column was removed")
    require(data["K_column"] == 512, "K must remain its own nonnegative column")
    require(data["bit_order"] == BIT_ORDER, "Complete visible type routing changed")
    require(data["inequality_convention"] == "a dot z >= rhs", "Raw inequality direction changed")
    rows, equalities = data["raw_rows"], data["equalities"]
    require(len(rows) == M and len(equalities) == Q, "Full raw lists are required")
    names = [row["name"] for row in rows]
    require(len(set(names)) == M, "Raw names must retain their distinct input positions")
    require(scaling["raw_order"] == names, "Prepared scaling order changed")
    require(len(scaling["raw_scales"]) == M, "Incomplete scaling map")
    divisors = [F(scaling["raw_scales"][name]) for name in names]
    require(all(d > 0 for d in divisors), "All divisors must be positive")
    require(len(divisors[PREFIX_ROWS:]) == NEW_ROWS
            and all(d == 25 for d in divisors[PREFIX_ROWS:]),
            "All536 appended rows keep numerical divisor25, regardless of source weights")
    A = [exact_sparse(row["a"], "raw row " + str(i)) for i, row in enumerate(rows)]
    b = [F(row["rhs"]) for row in rows]
    E = [exact_sparse(row["a"], "equality " + str(i)) for i, row in enumerate(equalities)]
    h = [F(row["rhs"]) for row in equalities]
    cost = exact_sparse(data["objective"], "objective")
    require(h == [F(1), F(0)], "O=1 and C-size=0 affine RHS must be retained")
    require(any(rhs == -1 for rhs in b), "Affine OPT6 upper rows were lost")
    atoms = data["atom_columns"]
    require(len(atoms) == 512, "All512 full client types must be retained")
    for j, atom in enumerate(atoms):
        bits = [(j >> k) & 1 for k in range(8, -1, -1)]
        require(atom["index"] == j and atom["a"] == bits[:6]
                and [atom["x"], atom["o"], atom["c"]] == bits[6:],
                "Incorrect complete type at column " + str(j))
        require(cost.get(j, F(0)) == int(any(bits[:6])), "Objective is not full actual W")
        require(E[0].get(j, F(0)) == bits[7]
                and E[1].get(j, F(0)) == bits[8], "Equality column mapping changed")
    require(cost.get(512, F(0)) == 0 and E[0].get(512, F(0)) == 0
            and E[1].get(512, F(0)) == -1, "K/objective/equality contract changed")
    pins[str(release_path.relative_to(REPO))] = digest(release_path)
    return {
        "release": release, "data": data, "scaling": scaling, "pins": pins,
        "rows": rows, "A": A, "b": b, "E": E, "h": h, "cost": cost, "divisors": divisors,
    }


def load_discovery():
    bundle = load_released()
    marker = read_json(HERE / "single_lp_consumed.json")
    discovery = read_json(HERE / "discovery_output.json")
    expected = bundle["release"]["input_sha256"]
    require(marker["optimizer_calls_consumed"] == 1 and marker["input_sha256"] == expected,
            "Missing exact one-call consumption record")
    require(discovery["optimizer_calls"] == 1 and discovery["input_sha256"] == expected,
            "Discovery binding mismatch")
    require(discovery["success"] is True, "The sole returned solve was not successful")
    require(discovery["raw_row_order"] == [row["name"] for row in bundle["rows"]],
            "Discovery reordered raw rows")
    require(list(map(F, discovery["raw_row_divisors"])) == bundle["divisors"],
            "Discovery scales differ from prepared divisors")
    return bundle, discovery
