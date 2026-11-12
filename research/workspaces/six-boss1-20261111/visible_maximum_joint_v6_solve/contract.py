#!/usr/bin/env python3
"""Fail-closed v6 release contract. Import/status never inspect the input directory.

4177 is the compiled planning contract, not a certified input count. Main must
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
SOURCE = HERE.parent / "visible_maximum_joint_v6"
PARENT_SOURCE = HERE.parent / "visible_maximum_joint_v5"
OWNER, RUN, AGENT, PROFILE = "Boss1", "six-boss1-20261111", "/root/visible_joint_v6_solve", "full"
N, M, Q, PREFIX_ROWS, APPENDED_ROWS = 513, 4177, 2, 3056, 1121
BIT_ORDER = ["a1", "a2", "a3", "a4", "a5", "a6", "x", "o", "c"]
WAITING = "WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE"
RELEASE_STATUS = "MAIN_EXPLICIT_FULL4177_RAW_V6_SINGLE_LP_RELEASE"
CERT_STATUS = "PASS_EXACT_PRIMAL_DUAL_FULL_RAW_V6"
CHECK_STATUS = "PASS_FULL_RAW_FRACTION_VERIFICATION_V6"
FACE_CHECK_STATUS = "PASS_COMPLETE_OPTIMAL_FACE_FRACTION_VERIFICATION_V6"
PLANNED_DIMENSIONS = {
    "raw_inequalities": M, "literal_parent_rows": PREFIX_ROWS,
    "appended_rows": APPENDED_ROWS, "nonnegative_columns": N,
    "equalities": Q, "affine_rhs_minus_one_rows": 30,
}
PLANNED_ROW_BLOCKS = [
    {"label": "literal_v5_raw", "start": 0, "stop": 3056, "count": 3056},
    {"label": "source2_lambda_strip", "start": 3056, "stop": 3286, "count": 230},
    {"label": "source2_lambda_anchor_complete", "start": 3286, "stop": 3446, "count": 160},
    {"label": "later_sources_lambda_cells", "start": 3446, "stop": 3996, "count": 550},
    {"label": "source2_conditional_redistribution", "start": 3996, "stop": 4176, "count": 180},
    {"label": "ROOT270_STRICT_C_OUTSIDE", "start": 4176, "stop": 4177, "count": 1},
]
PLANNED_APPENDED_SCALING = [
    {"start": 3056, "stop": 4176, "count": 1120, "numerical_divisor": "25"},
    {"start": 4176, "stop": 4177, "count": 1, "numerical_divisor": "1"},
]
SOLVER_OPTIONS = {
    "time_limit": 60.0, "presolve": False,
    "primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9,
}
SOURCE_SCOPE_KEYS = [
    "original_six_player_complete_ordered_pure_SPE_model_reviewed",
    "all_new_sources_reviewed",
    "all_raw_coefficients_and_all_513_columns_reviewed",
    "all_off_path_weak_optimality_states_preserved",
    "empty_duplicate_coverage_alias_and_zero_customer_cases_preserved",
    "C_only_rewrites_use_only_the_C_size_equality",
    "general_8T_and_ordered_rows_keep_uneliminated_K",
    "numerical_divisor_is_not_substituted_for_true_IC_weight",
    "all_five_new_v6_blocks_and_original_source_metadata_reviewed",
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
    directory_fd = os.open(str(path.parent), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


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
        "compiled_planning_scaling_not_input_certification": PLANNED_APPENDED_SCALING,
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
            "Released input differs from confirmed 4177/513/2 contract; report, do not relax")
    require(data.get("nonnegative_columns") == list(range(N)), "All 513 nonnegative columns are mandatory")
    require(data.get("K_column") == 512, "Independent nonnegative K column was lost")
    require(data.get("bit_order") == BIT_ORDER, "Nine-bit complete type routing changed")
    require(data.get("inequality_convention") == "a dot z >= rhs", "Raw inequality direction changed")
    rows, equalities = data["raw_rows"], data["equalities"]
    require(isinstance(rows, list) and len(rows) == M
            and isinstance(equalities, list) and len(equalities) == Q, "Complete raw lists required")
    require(parent.get("raw_inequality_count") == PREFIX_ROWS
            and len(parent["raw_rows"]) == PREFIX_ROWS, "Literal frozen parent is not the 3056 system")
    require(rows[:PREFIX_ROWS] == parent["raw_rows"], "An original raw row, zero, duplicate, metadata or order changed")
    for key in ["variables", "equality_count", "nonnegative_columns", "K_column", "bit_order",
                "inequality_convention", "atom_columns", "equalities", "objective"]:
        require(data[key] == parent[key], "The frozen parent full-domain field changed: " + key)
    names = [row["name"] for row in rows]
    require(all(isinstance(name, str) and name for name in names) and len(set(names)) == M,
            "Distinct raw names and all raw positions must survive, even for identical coefficients")
    require(scaling["raw_order"] == names, "Scaling raw order differs from exact input")
    require(list(scaling["raw_scales"]) == names, "Scaling names or their full raw order changed")
    require(scaling.get("exact_coefficients_numerically_divided") is False,
            "Raw exact coefficients must remain undivided; numerical scaling is external")
    divisors = [exact_fraction(scaling["raw_scales"][name], "scale " + name) for name in names]
    require(all(value > 0 for value in divisors), "Every original numerical divisor must stay positive")
    require(parent_scaling["raw_order"] == names[:PREFIX_ROWS], "Frozen parent scale order differs")
    require(set(parent_scaling["raw_scales"]) == set(names[:PREFIX_ROWS]), "Parent scale map incomplete")
    require(all(scaling["raw_scales"][name] == parent_scaling["raw_scales"][name]
                for name in names[:PREFIX_ROWS]), "Original scale strings were changed")
    for block in PLANNED_APPENDED_SCALING:
        require(all(scaling["raw_scales"][names[i]] == block["numerical_divisor"]
                    for i in range(block["start"], block["stop"])),
                "A frozen appended numerical scale string changed")
    for i, row in enumerate(rows):
        require(isinstance(row.get("family"), str), "Raw family metadata missing at " + str(i))
        if "numerical_divisor" in row:
            require(F(str(row["numerical_divisor"])) == divisors[i], "Row/scaling numerical divisor mismatch")
        if PREFIX_ROWS <= i < M - 1:
            metadata_keys = {"id", "source_row_id", "source_row_index", "source_package",
                             "source_file", "source_row_metadata", "source_row_object_sha256"}
            require(metadata_keys.issubset(row), "New source row lost literal provenance at " + str(i))
            require(isinstance(row["source_row_metadata"], dict)
                    and type(row["source_row_index"]) is int and row["source_row_index"] >= 0,
                    "New source metadata/index shape changed at " + str(i))
            require(isinstance(row["source_package"], str) and row["source_package"]
                    and isinstance(row["source_file"], str) and row["source_file"],
                    "New source package/file route missing at " + str(i))
            require(row["name"] == row["source_package"] + "::" + str(row["source_row_id"]),
                    "Global raw name does not preserve its original source ID at " + str(i))
            require(row["id"] == row["source_row_id"]
                    and isinstance(row["source_row_object_sha256"], str)
                    and re.fullmatch(r"[0-9a-f]{64}", row["source_row_object_sha256"]),
                    "Original source ID/object SHA changed at " + str(i))
    for block in PLANNED_ROW_BLOCKS[1:-1]:
        require(all(rows[i]["source_package"] == block["label"]
                    and rows[i]["source_file"] == "exact_family.json"
                    for i in range(block["start"], block["stop"])),
                "Prepared source routing does not match its released raw block")
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
    require(release.get("schema") == "visible_maximum_joint_v6_main_release_v1", "Unknown Main release schema")
    require(release.get("status") == RELEASE_STATUS and release.get("authorized_by") == "/root",
            "No explicit v6 Main release")
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
            and release.get("expected_row_blocks") == PLANNED_ROW_BLOCKS
            and release.get("expected_appended_scaling") == PLANNED_APPENDED_SCALING,
            "Main must confirm the exact planning counts/order; any mismatch is an obstacle")
    require(release.get("solver") == "scipy.optimize.linprog/highs-ds"
            and release.get("solver_options") == SOLVER_OPTIONS,
            "Main must release the exact one-call solver configuration")
    require(release.get("input_path") == relative(SOURCE / "exact_input.json"), "Only the final v6 input may be read")
    scope = release.get("source_validity_scope")
    require(isinstance(scope, dict) and all(scope.get(key) is True for key in SOURCE_SCOPE_KEYS),
            "Main's original-model/source/full-column review is incomplete")
    required_hashes = ["input_sha256", "preparation_manifest_sha256", "scaling_sha256", "row_catalog_sha256",
                       "source_review_sha256", "source_pins_sha256", "scaffold_manifest_sha256",
                       "raw_row_order_sha256"]
    require(all(isinstance(release.get(key), str) and re.fullmatch(r"[0-9a-f]{64}", release[key])
                for key in required_hashes), "Every final primary SHA pin must be explicit before any input read")
    parent_release = release.get("literal_parent")
    require(isinstance(parent_release, dict)
            and parent_release.get("input_path") == relative(PARENT_SOURCE / "exact_input.json")
            and parent_release.get("scaling_path") == relative(PARENT_SOURCE / "numerical_scaling.json"),
            "Literal frozen v5 parent routing missing")
    for key in ["input_sha256", "scaling_sha256"]:
        require(isinstance(parent_release.get(key), str) and re.fullmatch(r"[0-9a-f]{64}", parent_release[key]),
                "Literal parent SHA missing: " + key)
    gate = ReleasedFiles()
    scaffold = gate.json(relative(HERE / "scaffold_manifest.json"), release["scaffold_manifest_sha256"])
    require(scaffold.get("status") == "HASHED_WAITING_SCAFFOLD_NOT_INPUT_OR_AUTHORIZATION"
            and scaffold.get("owner") == OWNER and scaffold.get("RUN") == RUN
            and scaffold.get("agent") == AGENT and scaffold.get("optimizer_calls") == 0,
            "The released scaffold identity or waiting state changed")
    code_pins = scaffold["code_artifact_sha256"]
    require(set(code_pins) == set(CORE_CODE), "Scaffold release must bind every core program exactly")
    for filename, expected in code_pins.items():
        gate.read(relative(HERE / filename), expected)
    scaffold_artifacts = scaffold["artifact_sha256"]
    require(set(CORE_CODE).issubset(scaffold_artifacts), "Incomplete scaffold artifact closure")
    for filename, expected in scaffold_artifacts.items():
        require(isinstance(filename, str) and Path(filename).name == filename,
                "Scaffold artifact must remain an exact local filename")
        gate.read(relative(HERE / filename), expected)
    # The first possible input/source read is below this point.
    asset_keys = {
        "exact_input.json": "input_sha256", "freeze_manifest.json": "preparation_manifest_sha256",
        "numerical_scaling.json": "scaling_sha256", "source_review.md": "source_review_sha256",
        "source_pins.json": "source_pins_sha256", "row_catalog.json": "row_catalog_sha256",
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
    for filename, key in asset_keys.items():
        if filename == "freeze_manifest.json":
            continue
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
    data = exact_json(assets["exact_input.json"], "v6 exact input")
    scaling = exact_json(assets["numerical_scaling.json"], "v6 scaling")
    model = validate_model(data, scaling, parent, parent_scaling, release)
    catalog = exact_json(assets["row_catalog.json"], "v6 raw row catalog")
    require(isinstance(catalog, list) and len(catalog) == M, "Complete 4177-row metadata catalog required")
    for i in range(PREFIX_ROWS, M):
        row, entry = model["rows"][i], catalog[i]
        require(isinstance(entry, dict) and entry.get("raw_index") == i
                and entry.get("name") == row["name"] and entry.get("family") == row["family"]
                and entry.get("rhs") == row["rhs"]
                and F(str(entry.get("numerical_divisor"))) == model["divisors"][i],
                "New raw metadata catalog does not match its actual row at " + str(i))
        if i < M - 1:
            for key in ["source_package", "source_row_index", "source_row_id",
                        "source_row_metadata", "source_row_object_sha256"]:
                require(entry.get(key) == row[key], "Literal new source metadata differs: " + str(i) + "/" + key)
            source_route = relative(HERE.parent / row["source_package"] / row["source_file"])
            require(source_route in source_pins["sources"] and source_route in gate.pins,
                    "Actual new source file is not in the released SHA closure: " + source_route)
    gate.pins[relative(release_path)] = sha256(release_bytes).hexdigest()
    return dict(release=release, data=data, scaling=scaling, pins=gate.pins,
                preparation=preparation, catalog=catalog, M=M, N=N, Q=Q, **model)


def load_discovery():
    bundle = load_released()
    marker = read_json(HERE / "single_lp_consumed.json")
    discovery = read_json(HERE / "discovery_output.json")
    expected = bundle["release"]["input_sha256"]
    require(marker["optimizer_calls_consumed"] == 1 and marker["input_sha256"] == expected,
            "Missing exact one-call consumption record")
    require(marker.get("status") == "CONSUMED_BEFORE_OPTIMIZER_ENTRY"
            and marker.get("solver") == "scipy.optimize.linprog/highs-ds"
            and marker.get("options") == SOLVER_OPTIONS
            and (marker.get("raw_inequalities"), marker.get("nonnegative_columns"), marker.get("equalities"))
            == (M, N, Q), "Consumed optimizer configuration or full domain differs")
    require(marker["release_sha256"] == bundle["pins"][relative(HERE / "main_release.json")],
            "Main release changed after consumption")
    require(discovery["optimizer_calls"] == 1 and discovery["input_sha256"] == expected,
            "Sole discovery binding mismatch")
    require(discovery.get("success") is True and type(discovery.get("status")) is int
            and discovery["status"] == 0, "The sole solve did not return a successful optimum")
    require(discovery.get("consumption_marker_sha256") == digest(HERE / "single_lp_consumed.json"),
            "The sole output is not bound to the durable one-call consumption marker")
    for field in ["authorized_by", "owner", "RUN", "agent", "profile", "input_sha256",
                  "preparation_manifest_sha256", "scaling_sha256", "row_catalog_sha256", "release_sha256",
                  "solver_script_sha256", "contract_script_sha256", "source_pins_sha256",
                  "optimizer_calls_consumed", "raw_inequalities", "nonnegative_columns", "equalities",
                  "solver", "scipy_version", "numpy_version", "options", "start_utc"]:
        require(discovery.get(field) == marker.get(field), "Discovery consumption lineage changed: " + field)
    require(discovery["raw_row_order"] == [row["name"] for row in bundle["rows"]], "Raw rows reordered in discovery")
    require(discovery["raw_row_blocks"] == PLANNED_ROW_BLOCKS, "Raw block order changed in discovery")
    require(list(map(F, discovery["raw_row_divisors"])) == bundle["divisors"], "Discovery scales changed")
    require(read_json(HERE / "source_pins_at_solve.json") == bundle["pins"], "Source pins changed after solve")
    require(marker["source_pins_sha256"] == digest(HERE / "source_pins_at_solve.json"),
            "Consumed source-pins artifact SHA changed")
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
