#!/usr/bin/env python3
"""Fail-closed v5 release contract. Import/status never inspect the input directory.

3056 is the compiled planning contract, not a certified input count. Main must
explicitly confirm it against the frozen input and manifest before any input or
source file is read. A mismatch is an obstacle; there is no adaptive relaxation.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import os
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = HERE.parent / "visible_maximum_joint_v5"
PARENT_SOURCE = HERE.parent / "visible_maximum_joint_v4"
OWNER, RUN, AGENT, PROFILE = "Boss1", "six-boss1-20261111", "/root/visible_joint_v5_solve", "full"
N, M, Q, PREFIX_ROWS, APPENDED_ROWS = 513, 3056, 2, 1586, 1470
BIT_ORDER = ["a1", "a2", "a3", "a4", "a5", "a6", "x", "o", "c"]
WAITING = "WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE"
RELEASE_STATUS = "MAIN_EXPLICIT_FULL3056_RAW_V5_SINGLE_LP_RELEASE"
CERT_STATUS = "PASS_EXACT_PRIMAL_DUAL_FULL_RAW_V5"
CHECK_STATUS = "PASS_FULL_RAW_FRACTION_VERIFICATION_V5"
FACE_CHECK_STATUS = "PASS_COMPLETE_OPTIMAL_FACE_FRACTION_VERIFICATION_V5"
PLANNED_DIMENSIONS = {
    "raw_inequalities": M, "literal_parent_rows": PREFIX_ROWS,
    "appended_rows": APPENDED_ROWS, "nonnegative_columns": N,
    "equalities": Q, "affine_rhs_minus_one_rows": 30,
}
PLANNED_ROW_BLOCKS = [
    {"label": "literal_v4_raw", "start": 0, "stop": 1586, "count": 1586},
    {"label": "fixed_cap_ordered_cells", "start": 1586, "stop": 1767, "count": 181},
    {"label": "fixed_basis_CAP_coupled_C_only", "start": 1767, "stop": 1795, "count": 28},
    {"label": "arbitrary_tau_minimal_cap_C_only", "start": 1795, "stop": 1823, "count": 28},
    {"label": "all_five_source_minimal_CAP_pure_8T", "start": 1823, "stop": 2919, "count": 1096},
    {"label": "adaptive_five_query_minimal_cap_ordered", "start": 2919, "stop": 3056, "count": 137},
]
SOURCE_SCOPE_KEYS = [
    "original_six_player_complete_ordered_pure_SPE_model_reviewed",
    "all_new_sources_reviewed",
    "all_raw_coefficients_and_all_513_columns_reviewed",
    "all_off_path_weak_optimality_states_preserved",
    "empty_duplicate_coverage_alias_and_zero_customer_cases_preserved",
    "C_only_rewrites_use_only_the_C_size_equality",
    "general_8T_and_ordered_rows_keep_uneliminated_K",
    "numerical_divisor_is_not_substituted_for_true_IC_weight",
]
CORE_CODE = [
    "contract.py", "preflight.py", "solve_once.py", "recover_exact.py",
    "verify_certificate.py", "analyze_optimal_face.py", "verify_optimal_face.py",
    "diagnose_true_payments.py", "freeze_scaffold.py",
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def exact_json(raw, label="JSON"):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, label + ": duplicate JSON key " + key)
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(label + ": nonstandard JSON constant " + value)

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant)


def read_json(path):
    return exact_json(path.read_text(), str(path))


def canonical_digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def write_new(path, value):
    """Exclusive, durable write. A consumption marker is never replaced/deleted."""
    payload = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with path.open("x") as output:
        output.write(payload)
        output.flush()
        os.fsync(output.fileno())


def exact_fraction(value, label):
    require(isinstance(value, str), label + ": exact rational string required")
    return F(value)


def exact_sparse(value, label):
    require(isinstance(value, dict), label + ": sparse exact JSON required")
    result = {}
    for key, coefficient in value.items():
        require(isinstance(key, str), label + ": string column key required")
        j = int(key)
        require(str(j) == key and 0 <= j < N, label + ": invalid column " + key)
        result[j] = exact_fraction(coefficient, label + " column " + key)
    return result


def json_pointer(value, pointer):
    require(isinstance(pointer, str) and pointer.startswith("/"),
            "Explicit nonempty JSON pointer required")
    for encoded in pointer[1:].split("/"):
        key = encoded.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def status():
    """Only local gate state; never probes SOURCE existence or content."""
    return {
        "status": WAITING, "owner": OWNER, "RUN": RUN, "agent": AGENT, "profile": PROFILE,
        "local_main_release_exists": (HERE / "main_release.json").is_file(),
        "local_consumption_marker_exists": (HERE / "single_lp_consumed.json").exists(),
        "compiled_planning_dimensions_not_input_certification": PLANNED_DIMENSIONS,
        "compiled_planning_blocks_not_input_certification": PLANNED_ROW_BLOCKS,
        "input_directory_probed": False, "input_or_sources_read": False,
        "optimizer_calls_by_status": 0, "authorization_inferred_from_existence": False,
        "note": "Only load_released can validate an actual Main release; status grants no permission.",
    }


def relative(path):
    return str(path.resolve().relative_to(REPO))


class ReleasedFiles:
    """Read each explicit SHA pin once; parsing uses the already verified bytes."""
    def __init__(self):
        self.pins, self.bytes_by_path = {}, {}

    def read(self, name, expected):
        require(isinstance(name, str) and not Path(name).is_absolute(), "Repository-relative pin required")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                "Missing final SHA release for " + name)
        path = (REPO / name).resolve()
        normalized = str(path.relative_to(REPO))
        require(path.is_file(), "Missing explicitly released file: " + name)
        if normalized in self.pins:
            require(self.pins[normalized] == expected, "Conflicting SHA pins: " + name)
            return self.bytes_by_path[normalized]
        raw = path.read_bytes()
        require(sha256(raw).hexdigest() == expected, "SHA mismatch: " + name)
        self.pins[normalized] = expected
        self.bytes_by_path[normalized] = raw
        return raw

    def json(self, name, expected):
        return exact_json(self.read(name, expected), name)


def validate_model(data, scaling, parent, parent_scaling, release):
    """Exact full-domain checks; called only after explicit input/source release."""
    require(type(data.get("variables")) is int and data["variables"] == N
            and data.get("raw_inequality_count") == M and data.get("equality_count") == Q,
            "Released input differs from confirmed 3056/513/2 contract; report, do not relax")
    require(data.get("nonnegative_columns") == list(range(N)), "All 513 nonnegative columns are mandatory")
    require(data.get("K_column") == 512, "Independent nonnegative K column was lost")
    require(data.get("bit_order") == BIT_ORDER, "Nine-bit complete type routing changed")
    require(data.get("inequality_convention") == "a dot z >= rhs", "Raw inequality direction changed")
    rows, equalities = data["raw_rows"], data["equalities"]
    require(isinstance(rows, list) and len(rows) == M
            and isinstance(equalities, list) and len(equalities) == Q, "Complete raw lists required")
    require(parent.get("raw_inequality_count") == PREFIX_ROWS
            and len(parent["raw_rows"]) == PREFIX_ROWS, "Literal frozen parent is not the 1586 system")
    require(rows[:PREFIX_ROWS] == parent["raw_rows"], "An original raw row, zero, duplicate, metadata or order changed")
    for key in ["variables", "equality_count", "nonnegative_columns", "K_column", "bit_order",
                "inequality_convention", "atom_columns", "equalities", "objective"]:
        require(data[key] == parent[key], "The frozen parent full-domain field changed: " + key)
    names = [row["name"] for row in rows]
    require(all(isinstance(name, str) and name for name in names) and len(set(names)) == M,
            "Distinct raw names and all raw positions must survive, even for identical coefficients")
    require(scaling["raw_order"] == names, "Scaling raw order differs from exact input")
    require(set(scaling["raw_scales"]) == set(names), "Scaling names do not cover exactly every raw row")
    divisors = [exact_fraction(scaling["raw_scales"][name], "scale " + name) for name in names]
    require(all(value > 0 for value in divisors), "Every original numerical divisor must stay positive")
    require(parent_scaling["raw_order"] == names[:PREFIX_ROWS], "Frozen parent scale order differs")
    require(set(parent_scaling["raw_scales"]) == set(names[:PREFIX_ROWS]), "Parent scale map incomplete")
    require(all(scaling["raw_scales"][name] == parent_scaling["raw_scales"][name]
                for name in names[:PREFIX_ROWS]), "Original scale strings were changed")
    require(all(value == 25 for value in divisors[PREFIX_ROWS:]),
            "Every appended row must keep numerical divisor 25, independently of its true IC weight")
    for i, row in enumerate(rows):
        require(isinstance(row.get("family"), str), "Raw family metadata missing at " + str(i))
        if "numerical_divisor" in row:
            require(F(str(row["numerical_divisor"])) == divisors[i], "Row/scaling numerical divisor mismatch")
    A = [exact_sparse(row["a"], "raw row " + str(i)) for i, row in enumerate(rows)]
    b = [exact_fraction(row["rhs"], "raw rhs " + str(i)) for i, row in enumerate(rows)]
    E = [exact_sparse(row["a"], "equality " + str(i)) for i, row in enumerate(equalities)]
    h = [exact_fraction(row["rhs"], "equality rhs " + str(i)) for i, row in enumerate(equalities)]
    cost = exact_sparse(data["objective"], "objective")
    require(sum(value == -1 for value in b) == 30, "Exactly all 30 affine rhs=-1 rows must remain")
    require(h == [F(1), F(0)], "O=1 and size(C)-K=0 affine equalities changed")
    atoms = data["atom_columns"]
    require(isinstance(atoms, list) and len(atoms) == 512, "All 512 customer types are mandatory")
    for j, atom in enumerate(atoms):
        bits = [(j >> k) & 1 for k in range(8, -1, -1)]
        require(atom["index"] == j and atom["a"] == bits[:6]
                and [atom["x"], atom["o"], atom["c"]] == bits[6:], "Wrong full atom at " + str(j))
        require(cost.get(j, F(0)) == int(any(bits[:6])), "Objective is not full actual W")
        require(E[0].get(j, F(0)) == bits[7] and E[1].get(j, F(0)) == bits[8],
                "Original free-equality column routing changed")
    require(cost.get(512, F(0)) == E[0].get(512, F(0)) == 0
            and E[1].get(512, F(0)) == -1, "K objective/equality coefficients changed")
    require(canonical_digest(names) == release["raw_row_order_sha256"], "Released raw-order digest mismatch")
    return dict(rows=rows, A=A, b=b, E=E, h=h, cost=cost, divisors=divisors)


def load_released():
    """No source read, directory probe, old-input fallback or optimizer before Main gate."""
    release_path = HERE / "main_release.json"
    require(release_path.is_file(), WAITING + ": no main_release.json")
    release_bytes = release_path.read_bytes()
    release = exact_json(release_bytes, "Main release")
    require(release.get("schema") == "visible_maximum_joint_v5_main_release_v1", "Unknown Main release schema")
    require(release.get("status") == RELEASE_STATUS and release.get("authorized_by") == "/root",
            "No explicit v5 Main release")
    require(release.get("owner") == OWNER and release.get("RUN") == RUN
            and release.get("agent") == AGENT and release.get("profile") == PROFILE, "Main release identity mismatch")
    require(type(release.get("optimizer_calls_authorized")) is int
            and release["optimizer_calls_authorized"] == 1, "Exactly one optimizer call must be explicitly released")
    require(release.get("input_read_authorized") is True
            and release.get("source_closure_read_authorized") is True, "Final input/source read authorization missing")
    require(isinstance(release.get("explicit_main_instruction"), str)
            and release["explicit_main_instruction"].strip(), "Actual Main instruction is required")
    require(release.get("planning_contract_confirmed") is True
            and release.get("expected_dimensions") == PLANNED_DIMENSIONS
            and release.get("expected_row_blocks") == PLANNED_ROW_BLOCKS,
            "Main must confirm the exact planning counts/order; any mismatch is an obstacle")
    require(release.get("appended_numerical_divisor") == "25", "Appended numerical divisor contract changed")
    require(release.get("input_path") == relative(SOURCE / "exact_input.json"), "Only the final v5 input may be read")
    scope = release.get("source_validity_scope")
    require(isinstance(scope, dict) and all(scope.get(key) is True for key in SOURCE_SCOPE_KEYS),
            "Main's original-model/source/full-column review is incomplete")
    required_hashes = ["input_sha256", "preparation_manifest_sha256", "scaling_sha256",
                       "source_review_sha256", "source_pins_sha256", "scaffold_manifest_sha256",
                       "raw_row_order_sha256"]
    require(all(isinstance(release.get(key), str) and re.fullmatch(r"[0-9a-f]{64}", release[key])
                for key in required_hashes), "Every final primary SHA pin must be explicit before any input read")
    parent_release = release.get("literal_parent")
    require(isinstance(parent_release, dict)
            and parent_release.get("input_path") == relative(PARENT_SOURCE / "exact_input.json")
            and parent_release.get("scaling_path") == relative(PARENT_SOURCE / "numerical_scaling.json"),
            "Literal frozen v4 parent routing missing")
    for key in ["input_sha256", "scaling_sha256"]:
        require(isinstance(parent_release.get(key), str) and re.fullmatch(r"[0-9a-f]{64}", parent_release[key]),
                "Literal parent SHA missing: " + key)
    gate = ReleasedFiles()
    scaffold = gate.json(relative(HERE / "scaffold_manifest.json"), release["scaffold_manifest_sha256"])
    code_pins = scaffold["code_artifact_sha256"]
    require(set(code_pins) == set(CORE_CODE), "Scaffold release must bind every core program exactly")
    for filename, expected in code_pins.items():
        gate.read(relative(HERE / filename), expected)
    # The first possible input/source read is below this point.
    asset_keys = {
        "exact_input.json": "input_sha256", "freeze_manifest.json": "preparation_manifest_sha256",
        "numerical_scaling.json": "scaling_sha256", "source_review.md": "source_review_sha256",
        "source_pins.json": "source_pins_sha256",
    }
    assets = {filename: gate.read(relative(SOURCE / filename), release[key])
              for filename, key in asset_keys.items()}
    preparation = exact_json(assets["freeze_manifest.json"], "prepared manifest")
    manifest_pointers = release.get("preparation_manifest_count_pointers")
    require(isinstance(manifest_pointers, dict)
            and set(manifest_pointers) == {"raw_inequalities", "nonnegative_columns", "equalities"},
            "Main must identify the exact prepared-manifest count fields")
    for field, pointer in manifest_pointers.items():
        require(json_pointer(preparation, pointer) == PLANNED_DIMENSIONS[field],
                "Frozen prepared-manifest count mismatch: " + field)
    if "artifacts" in preparation:
        artifacts = {
            relative(SOURCE / filename): entry["sha256"] if isinstance(entry, dict) else entry
            for filename, entry in preparation["artifacts"].items()
        }
    else:
        require(isinstance(preparation.get("artifact_sha256"), dict), "Unknown prepared manifest interface")
        artifacts = preparation["artifact_sha256"]
    artifacts = {str((REPO / filename).resolve().relative_to(REPO)): expected
                 for filename, expected in artifacts.items()}
    for filename, key in [("exact_input.json", "input_sha256"), ("numerical_scaling.json", "scaling_sha256")]:
        require(artifacts.get(relative(SOURCE / filename)) == release[key],
                "Prepared manifest does not bind the released " + filename)
    for filename, expected in artifacts.items():
        gate.read(filename, expected)
    source_pins = exact_json(assets["source_pins.json"], "prepared source pins")
    require(isinstance(source_pins.get("sources"), dict) and source_pins["sources"], "Explicit source closure is required")
    for filename, expected in source_pins["sources"].items():
        gate.read(filename, expected)
    evidence = release.get("required_evidence")
    require(isinstance(evidence, list) and evidence, "Released audit evidence missing")
    seen_roles = set()
    for item in evidence:
        require(isinstance(item, dict) and isinstance(item.get("role"), str), "Evidence role is required")
        checked = gate.json(item["path"], item["sha256"])
        expected = item["expected_status"]
        require(isinstance(expected, str) and expected.startswith("PASS"), "Only explicit PASS evidence can be released")
        require(json_pointer(checked, item.get("status_pointer", "/status")) == expected,
                "Released evidence did not pass: " + item["path"])
        if item["role"] == "main_preflight":
            require(json_pointer(checked, item.get("input_sha256_pointer", "/input_sha256"))
                    == release["input_sha256"], "Main preflight is not bound to this exact input")
        for pointer, expected_value in item.get("expected_json_values", {}).items():
            require(json_pointer(checked, pointer) == expected_value, "Released evidence field changed: " + pointer)
        seen_roles.add(item["role"])
    require({"main_preflight", "source_legality", "all_raw_column_audit"}.issubset(seen_roles),
            "Main preflight, source-legality and full-column evidence roles are all required")
    parent = gate.json(parent_release["input_path"], parent_release["input_sha256"])
    parent_scaling = gate.json(parent_release["scaling_path"], parent_release["scaling_sha256"])
    data = exact_json(assets["exact_input.json"], "v5 exact input")
    scaling = exact_json(assets["numerical_scaling.json"], "v5 scaling")
    model = validate_model(data, scaling, parent, parent_scaling, release)
    gate.pins[relative(release_path)] = sha256(release_bytes).hexdigest()
    return dict(release=release, data=data, scaling=scaling, pins=gate.pins,
                preparation=preparation, M=M, N=N, Q=Q, **model)


def load_discovery():
    bundle = load_released()
    marker = read_json(HERE / "single_lp_consumed.json")
    discovery = read_json(HERE / "discovery_output.json")
    expected = bundle["release"]["input_sha256"]
    require(marker["optimizer_calls_consumed"] == 1 and marker["input_sha256"] == expected,
            "Missing exact one-call consumption record")
    require(marker["release_sha256"] == bundle["pins"][relative(HERE / "main_release.json")],
            "Main release changed after consumption")
    require(discovery["optimizer_calls"] == 1 and discovery["input_sha256"] == expected,
            "Sole discovery binding mismatch")
    require(discovery.get("success") is True, "The sole solve did not return a successful optimum")
    require(discovery["raw_row_order"] == [row["name"] for row in bundle["rows"]], "Raw rows reordered in discovery")
    require(list(map(F, discovery["raw_row_divisors"])) == bundle["divisors"], "Discovery scales changed")
    require(read_json(HERE / "source_pins_at_solve.json") == bundle["pins"], "Source pins changed after solve")
    require(marker["solver_script_sha256"] == digest(HERE / "solve_once.py")
            and marker["contract_script_sha256"] == digest(HERE / "contract.py"), "Core solver code changed after consumption")
    return bundle, discovery


def load_verified_certificate():
    bundle, discovery = load_discovery()
    cert = read_json(HERE / "exact_certificate.json")
    checked = read_json(HERE / "independent_check_result.json")
    require(cert["status"] == CERT_STATUS and checked["status"] == CHECK_STATUS,
            "Independent full Fraction verification is required")
    require(cert["input_sha256"] == checked["input_sha256"] == bundle["release"]["input_sha256"],
            "Exact certificate/verification input binding mismatch")
    require(checked["certificate_sha256"] == digest(HERE / "exact_certificate.json")
            and cert["discovery_sha256"] == digest(HERE / "discovery_output.json"), "Exact artifact binding mismatch")
    return bundle, cert, checked
