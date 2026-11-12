#!/usr/bin/env python3
"""Fail-closed v6 solver-v2 release contract. Import/status do not read the input.

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
WAITING = "WAITING_V2_MAIN_REVIEW_AND_NEW_EXPLICIT_RELEASE"
RELEASE_STATUS = "MAIN_EXPLICIT_FULL4177_RAW_V6_SOLVE_V2_SINGLE_LP_RELEASE"
SOLVER_PACKAGE = "visible_maximum_joint_v6_solve_v2"
RELEASE_SCHEMA = "visible_maximum_joint_v6_solve_v2_main_release_v1"
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

# Exact interface of the already frozen v6 source-pin document. These are source
# file pins, never optimizer support or a reduced mathematical model.
SOURCE_PIN_SCHEMA = "v6_exact_read_set_pins_v1"
SOURCE_PIN_DOCUMENT_SHA256 = "d90e383c1824ea5b3eebb8fbe93b9c53c6a071bb72684740f25f28492c6a5fc0"
EXPECTED_FROZEN_INPUT_SHA256 = "8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769"
ORIGINAL_RELEASE_REFERENCE_SHA256 = "eef504e3ad50d3e2f901e12a8689a95415986be2552c73cd885041e4d8dbdbaf"
MODEL_ERRATUM_PIN = {
    "path": "research/workspaces/six-boss1-20261111/visible_maximum_joint_v6_model_erratum.md",
    "sha256": "a2b83e67ce90597faa005cb893da647555bbb58b0d502fd3f03c12db924172b7",
}
SEMANTIC_RELEASE_PIN = {
    "path": "research/workspaces/six-boss1-20261111/main_v6_semantic_release.json",
    "sha256": "36cdf31f302aefc738a300b9b25a5b29ef9a97e85bdf0499c2beba50bc153c85",
}
SOURCE_PIN_READ_SCOPE = 'Only original model, frozen parent input metadata, frozen requested source packages and Main source checks. No recursive traversal of old inherited source/release metadata.'
EXPECTED_SOURCE_PIN_ENTRIES = {
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md": {
        "sha256": "cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88",
        "bytes": 7598
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/coordinate_contract.json": {
        "sha256": "9d5774899ae89c4a59ef7893d3db0549cc3f0c641104b1eddb875587940809c8",
        "bytes": 79583
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/exact_family.json": {
        "sha256": "22fb5d0f5af953ac6a7c74faadca5ab9ba5703e30d83445b27085a26900de0e6",
        "bytes": 7389405
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/freeze_manifest.json": {
        "sha256": "275e95c2a650aa90bbc86b225cc75a125b5184d27d2b5b3b6e667e9de486643c",
        "bytes": 10851
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/geometry.md": {
        "sha256": "0247d4ecfb38c63108d42d8990dcc954d71fafe4986570b28d78e8798b87634d",
        "bytes": 14671
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/literal_checker_output.json": {
        "sha256": "1ac8d3e7cbf7b8f92e080ecaa4104185c51660f578a1581d121dc4318790927c",
        "bytes": 2960
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/parameter_domains.json": {
        "sha256": "f2adc82e736ede5949459bea47204a462fc25f17647b34971dd701672e40751a",
        "bytes": 321222
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/proof.md": {
        "sha256": "5dfb6e1ed29cd2955461bc15f8184246230de302ef43b6755c907c1b4173195a",
        "bytes": 19900
    },
    "research/workspaces/six-boss1-20261111/later_sources_lambda_cells/row_catalog.json": {
        "sha256": "287cd4d140b6392ac649001332985a75a247348563a5fe3606dce20fa4c62500",
        "bytes": 421082
    },
    "research/workspaces/six-boss1-20261111/main_later_lambda_check.json": {
        "sha256": "b74a0ea95d4094e605a8cb8bd351ecb5a9bb6ba35c0c9862c29c6599d119590f",
        "bytes": 3781
    },
    "research/workspaces/six-boss1-20261111/main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json": {
        "sha256": "a803b4704af3c6a1528deca3f67350a4becab6375133f036058cfba867d37eff",
        "bytes": 19980
    },
    "research/workspaces/six-boss1-20261111/main_root270_strict_outside/check_result.json": {
        "sha256": "01cb05b8491090a23362f3daee1c5811500bdd8535f1e61a32154d4807b67c73",
        "bytes": 850
    },
    "research/workspaces/six-boss1-20261111/main_root270_strict_outside/freeze_manifest.json": {
        "sha256": "403776eb344d9c14bd3dfa5e0c779d11eb2dc0c52f7155d05fdb910481c43c52",
        "bytes": 655
    },
    "research/workspaces/six-boss1-20261111/main_root270_strict_outside/proof.md": {
        "sha256": "3671dd202a476f0cbd48fb5e74fd9912c0f12a0dd4edd7be007c32b880b22fdd",
        "bytes": 1631
    },
    "research/workspaces/six-boss1-20261111/main_source2_delta_check.json": {
        "sha256": "e298848962724006d458126e8767e4ad24d6b2462daffa040ff7defe0fc7644e",
        "bytes": 2834
    },
    "research/workspaces/six-boss1-20261111/main_source2_lambda_anchor_complete_check.json": {
        "sha256": "b02a538af1f42d83ae5ba31f141303d3994ea45dc0484524aaffe7c477fa070a",
        "bytes": 1269
    },
    "research/workspaces/six-boss1-20261111/main_source2_lambda_strip_check.json": {
        "sha256": "eaa9a141f035ffa4ce17f6547a318a1f424ddf4760d180f3d0909b2e273beaae",
        "bytes": 1259
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/coordinate_contract.json": {
        "sha256": "619d9dc8f92060b7fac299c86de592e810634e8f4cc6ed90e6731f3d7ea63c06",
        "bytes": 79949
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/exact_envelopes.json": {
        "sha256": "1420c574fe8d7b75ad098d1b2ec339edf1f994a3b4983a7451cfbbd54a6a510f",
        "bytes": 1142597
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/exact_family.json": {
        "sha256": "cbcec20f5897e4b445cb256d55093a1d9db8e2de4a0b00d766a6ab24af2d74be",
        "bytes": 2313805
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/freeze_manifest.json": {
        "sha256": "9cfbe8eb409b6fd505ea1663183a3a3220602222952a5ba0291e13398578285a",
        "bytes": 7369
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/literal_checker_output.json": {
        "sha256": "30abf7896e45b772fb7b5a11d0c8a12519913a8762b9553159e8648ead41ffec",
        "bytes": 1397
    },
    "research/workspaces/six-boss1-20261111/source2_conditional_redistribution/proof.md": {
        "sha256": "9b9128519aa12d2d9c11d197948751a21ed5f1039eb51640a26f1922e818ea1d",
        "bytes": 17740
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/coordinate_contract.json": {
        "sha256": "50e6f6ccd749392099a3c2d58af61b27c74f6ddca5f6fdb2227bc94338106468",
        "bytes": 97916
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/exact_family.json": {
        "sha256": "a2a7bca9b52d37e6c92f3c67daff0a7c0b7fdd4e9caf50d358bae02eeb2eb48c",
        "bytes": 3296432
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/freeze_manifest.json": {
        "sha256": "43e6c3db3e1631932af72f839dd2e46d7454d23d1884cdc9105cd1609d0821fc",
        "bytes": 8955
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/geometry.md": {
        "sha256": "0042bea4ff377e129514b0cac8ee58d03783d91d270a7f1c38c6d6fbb8d51b97",
        "bytes": 3275
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/literal_checker_output.json": {
        "sha256": "573d4d397a187a3396a555297d44397d474dc89f73d2f8caa8e41a971367ef59",
        "bytes": 1270
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/parameter_domains.json": {
        "sha256": "0927324c430b527e40dae0210bd080307274234c24074a70a3472b5563480ba1",
        "bytes": 26316
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/proof.md": {
        "sha256": "20f58742231f5f273806ea6363b5d3c1480852c2ddda319b9551a62b603b5270",
        "bytes": 19476
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_anchor_complete/row_catalog.json": {
        "sha256": "1993be578363345376fa7d5f76cdc0a07b104e76ec59335c050275fde4054735",
        "bytes": 55423
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/coordinate_contract.json": {
        "sha256": "252dc84f4a815da9c7555b38ca9791a76db81c6928674cded13822fbfade7e76",
        "bytes": 97916
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/exact_family.json": {
        "sha256": "cb6f952edef0f8278fd671cc6ef1f38f7fd47a59d094c008dba9d1376ddc5fac",
        "bytes": 4818130
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/freeze_manifest.json": {
        "sha256": "a3f42d72be4ebecd15f8f74315103ae90bb940d4031fa712211219e2c75f96a4",
        "bytes": 7209
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/geometry.md": {
        "sha256": "0b8d606ece93a1bcee9ef8f78206d0eb8095692bd0a9231e9c0f5e3ff6a429b5",
        "bytes": 3147
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/literal_checker_output.json": {
        "sha256": "06ecdbce36563a7a4fe5653a1a09441e9cbd0028ef79cf15b0693b714451f301",
        "bytes": 1275
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/parameter_domains.json": {
        "sha256": "f7ac2a43747a037dc552437345d82ff571c9c5527860ccb5b44cea2596d91ec8",
        "bytes": 33976
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/proof.md": {
        "sha256": "e367fdda0e98c6e716619b78e3597552af2a583a711b9385145ec959445f599d",
        "bytes": 17536
    },
    "research/workspaces/six-boss1-20261111/source2_lambda_strip/row_catalog.json": {
        "sha256": "d744debed0022395e6bef2f5d161b67ff30a646718aae598c6e9f24d436ec400",
        "bytes": 80300
    },
    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/exact_input.json": {
        "sha256": "12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac",
        "bytes": 42821991
    },
    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/freeze_manifest.json": {
        "sha256": "b49d8bba4197fc6d656005770dace9c5a777816b5e3eaa1105565fb23db51a27",
        "bytes": 10354
    },
    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/literal_check_result.json": {
        "sha256": "ebe43e3a43850b67d575fcf626af622e80a302cc5d29a83f3cd99d850c81d462",
        "bytes": 5694
    },
    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/numerical_scaling.json": {
        "sha256": "c0ac529a5436a21bcc83e8227961ec294cd92b829dfd85b331e3cb5ef9fb8e9b",
        "bytes": 284133
    },
    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/row_catalog.json": {
        "sha256": "fd2aa8bb95c6438de7c3263dda917074ba0e526866e1cabf19093d1ad6254b81",
        "bytes": 2094657
    }
}


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
        "solver_package": SOLVER_PACKAGE, "authorized_repair_stage_has_prior_source_reads": True,
        "local_main_release_exists": (HERE / "main_release.json").is_file(),
        "local_consumption_marker_exists": (HERE / "single_lp_consumed.json").exists(),
        "compiled_planning_dimensions_not_input_certification": PLANNED_DIMENSIONS,
        "compiled_planning_blocks_not_input_certification": PLANNED_ROW_BLOCKS,
        "compiled_planning_scaling_not_input_certification": PLANNED_APPENDED_SCALING,
        "input_directory_probed_by_status": False, "input_or_sources_read_by_status": False,
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
        require(normalized == name, "Noncanonical or aliased repository file path: " + name)
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


def validate_source_pin_entries(document):
    """Accept exactly the frozen 44-file schema before reading any listed file."""
    require(isinstance(document, dict) and set(document) == {"schema", "read_scope", "files"},
            "Unknown source-pin document fields")
    require(document["schema"] == SOURCE_PIN_SCHEMA and document["read_scope"] == SOURCE_PIN_READ_SCOPE,
            "Unknown source-pin schema or declared read scope")
    entries = document["files"]
    require(isinstance(entries, list) and len(entries) == len(EXPECTED_SOURCE_PIN_ENTRIES) == 44,
            "The complete exact 44-file source closure is mandatory")
    normalized = {}
    for item in entries:
        require(isinstance(item, dict) and set(item) == {"path", "sha256", "bytes"},
                "Unknown or missing source-pin entry fields")
        name, expected, count = item["path"], item["sha256"], item["bytes"]
        require(isinstance(name, str) and name and not Path(name).is_absolute()
                and str(Path(name)) == name and all(part not in {".", ".."} for part in Path(name).parts),
                "Canonical repository-relative source path required")
        require(name not in normalized, "Duplicate source-pin path: " + name)
        require(name in EXPECTED_SOURCE_PIN_ENTRIES, "Unknown source-pin path: " + name)
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                "Complete lowercase SHA256 required for every source file")
        require(type(count) is int and count >= 0, "Exact nonnegative byte count required")
        require({"sha256": expected, "bytes": count} == EXPECTED_SOURCE_PIN_ENTRIES[name],
                "A declared source SHA or byte count differs from the frozen exact read set")
        normalized[name] = expected
    require(set(normalized) == set(EXPECTED_SOURCE_PIN_ENTRIES), "Missing exact source-pin paths")
    require(list(normalized) == list(EXPECTED_SOURCE_PIN_ENTRIES), "Frozen source-pin order changed")
    return normalized


def read_source_pin_closure(document, gate):
    """Verify every declared file's bytes and SHA; never skip or recurse into metadata."""
    normalized = validate_source_pin_entries(document)
    for name, expected in normalized.items():
        raw = gate.read(name, expected)
        require(len(raw) == EXPECTED_SOURCE_PIN_ENTRIES[name]["bytes"],
                "Frozen source byte count mismatch: " + name)
    return normalized


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
    require(release.get("schema") == RELEASE_SCHEMA
            and release.get("solver_package") == SOLVER_PACKAGE, "A new explicit solver-v2 Main release is required")
    require(release.get("status") == RELEASE_STATUS and release.get("authorized_by") == "/root",
            "No explicit solver-v2 Main release")
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
    # Only the new Main gate can reach the optimizer's normal input loader.
    bundle = _load_pinned_input(release, gate)
    gate.pins[relative(release_path)] = sha256(release_bytes).hexdigest()
    return bundle


def _load_pinned_input(release, gate):
    """Common exact read/validation only; this function never authorizes optimization."""
    require(release["input_sha256"] == EXPECTED_FROZEN_INPUT_SHA256
            and release["source_pins_sha256"] == SOURCE_PIN_DOCUMENT_SHA256,
            "Interface repair must use the identical frozen v6 input and source-pin bytes")
    require(release["expected_dimensions"] == PLANNED_DIMENSIONS
            and release["expected_row_blocks"] == PLANNED_ROW_BLOCKS
            and release["expected_appended_scaling"] == PLANNED_APPENDED_SCALING,
            "Interface repair may not change dimensions, order or numerical scaling")
    require(all(release["source_validity_scope"].get(key) is True for key in SOURCE_SCOPE_KEYS),
            "Complete original-model source review remains mandatory")
    parent_release = release["literal_parent"]
    require(parent_release["input_path"] == relative(PARENT_SOURCE / "exact_input.json")
            and parent_release["scaling_path"] == relative(PARENT_SOURCE / "numerical_scaling.json"),
            "Literal frozen v5 input/scale routes may not change")
    require(release.get("mandatory_model_erratum") == MODEL_ERRATUM_PIN
            and release.get("semantic_release") == SEMANTIC_RELEASE_PIN,
            "The independently pinned actual-prefix X model correction is mandatory")
    gate.read(MODEL_ERRATUM_PIN["path"], MODEL_ERRATUM_PIN["sha256"])
    semantic = gate.json(SEMANTIC_RELEASE_PIN["path"], SEMANTIC_RELEASE_PIN["sha256"])
    require(semantic.get("status") == "PASS_MAIN_V6_SOURCE_SCOPE_AND_REQUIRED_X_ERRATUM"
            and semantic.get("input_sha256") == EXPECTED_FROZEN_INPUT_SHA256
            and semantic.get("mandatory_erratum") == MODEL_ERRATUM_PIN,
            "Independent X semantic release binding changed")
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
    source_pins_document = exact_json(assets["source_pins.json"], "prepared source pins")
    source_pins = read_source_pin_closure(source_pins_document, gate)
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
            require(source_route in source_pins and source_route in gate.pins,
                    "Actual new source file is not in the released SHA closure: " + source_route)
    return dict(release=release, data=data, scaling=scaling, pins=gate.pins,
                preparation=preparation, catalog=catalog, source_pin_files_checked=len(source_pins),
                source_pin_byte_counts_checked=len(source_pins), semantic_release=semantic,
                mandatory_model_erratum=MODEL_ERRATUM_PIN, M=M, N=N, Q=Q, **model)


def load_repair_read_only():
    """Main-authorized pre-release repair check, with zero optimization authority.

    The withdrawn old release is read only as an exact SHA-bound source of input
    fields. Its former optimizer permission is neither copied nor propagated.
    solve_once.py cannot call this function and still requires a new v2 release.
    """
    for name in ["main_release.json", "single_lp_consumed.json", "source_pins_at_solve.json", "discovery_output.json"]:
        require(not (HERE / name).exists(), "Repair-only check must remain pre-release and unconsumed")
    original = HERE.parent / "visible_maximum_joint_v6_solve"
    require(not (original / "single_lp_consumed.json").exists()
            and not (original / "discovery_output.json").exists(), "Original attempt was unexpectedly consumed")
    plan_path = HERE / "repair_read_plan.json"
    plan = read_json(plan_path)
    require(plan.get("schema") == "visible_maximum_joint_v6_solve_v2_zero_optimizer_repair_read_plan_v1"
            and plan.get("recorded_by") == AGENT and plan.get("optimizer_calls_authorized") == 0
            and plan.get("main_explicit_read_only_repair_instruction_received") is True
            and plan.get("original_release_withdrawn_by_main") is True,
            "Explicitly recorded zero-optimizer repair scope required")
    reference_path = relative(original / "main_release.json")
    require(plan.get("withdrawn_release_reference_path") == reference_path
            and plan.get("withdrawn_release_reference_sha256") == ORIGINAL_RELEASE_REFERENCE_SHA256,
            "Repair may only use the exact withdrawn release as a read-only pin reference")
    gate = ReleasedFiles()
    reference = gate.json(reference_path, ORIGINAL_RELEASE_REFERENCE_SHA256)
    fields = ["input_path", "input_sha256", "preparation_manifest_sha256", "scaling_sha256",
              "row_catalog_sha256", "source_review_sha256", "source_pins_sha256", "raw_row_order_sha256",
              "expected_dimensions", "expected_row_blocks", "expected_appended_scaling", "source_validity_scope",
              "literal_parent", "preparation_manifest_count_pointers", "required_evidence",
              "mandatory_model_erratum", "semantic_release"]
    read_reference = {key: reference[key] for key in fields}
    read_reference.update(status="READ_ONLY_REPAIR_NOT_MAIN_OPTIMIZER_RELEASE",
                          optimizer_calls_authorized=0, authorization_mode="INPUT_READ_AND_VALIDATION_ONLY")
    require(read_reference["input_path"] == relative(SOURCE / "exact_input.json"), "Unexpected repair input route")
    bundle = _load_pinned_input(read_reference, gate)
    gate.pins[relative(plan_path)] = digest(plan_path)
    bundle["repair_read_only"] = True
    bundle["optimizer_calls_authorized"] = 0
    bundle["original_release_reference_is_not_active_authority"] = True
    return bundle


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
