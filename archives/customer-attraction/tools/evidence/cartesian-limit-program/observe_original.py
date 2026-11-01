"""One untouched analyze(k6, frozen weights), passive linprog observation only."""
import hashlib
import importlib.util
import json
import math
import platform
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy

ROOT = Path("/workspace/scratch/c0ab78c47566")
SOURCE = ROOT / "round20-cartesian_limit.py"
INPUT = ROOT / "round20-cartesian_limit_k6.json"
RUN = ROOT / "round20-cartesian-limit-work" / "observed-k6"


def normal(value):
    if isinstance(value, np.ndarray):
        return normal(value.tolist())
    if isinstance(value, np.generic):
        return normal(value.item())
    if isinstance(value, dict):
        return {str(k): normal(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [normal(x) for x in value]
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def write(name, value):
    (RUN / name).write_text(json.dumps(normal(value), ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def fingerprint(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    RUN.mkdir(parents=True, exist_ok=False)
    original = RUN / "cartesian_limit.py"
    frozen = RUN / "cartesian_limit_k6.json"
    shutil.copyfile(SOURCE, original)
    shutil.copyfile(INPUT, frozen)
    before = [fingerprint(original), fingerprint(frozen)]
    assert before[0]["sha256"] == "15ff0aa02e7507d2f31c05ea2946e4db3ed27b253ea8ef2c272c9342322650ae"
    assert before[1]["sha256"] == "27219c812da529002a735c1bfd4e949b21bc60b3ed6f67a638b4f7641ae81b80"
    historical = json.loads(frozen.read_text())
    point = historical["best"]
    assert point["k"] == 6 and len(point["weights"]) == 63
    spec = importlib.util.spec_from_file_location("observed_cartesian_limit", original)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    lp_code = module.linprog.__code__
    analyze_code = module.analyze.__code__
    main_code = module.main.__code__
    calls = []
    frames = {}
    counts = {"original_analyze": 0, "original_main": 0, "linprog": 0}
    local_capture = {}

    def profile(frame, event, arg):
        code = frame.f_code
        if event == "call" and code is analyze_code:
            counts["original_analyze"] += 1
        if event == "call" and code is main_code:
            counts["original_main"] += 1
        if code is lp_code:
            if event == "call":
                index = len(calls)
                frames[id(frame)] = index
                counts["linprog"] += 1
                names = ("c", "A_ub", "b_ub", "A_eq", "b_eq", "bounds", "method", "callback", "options", "x0", "integrality")
                calls.append({
                    "index": index,
                    "caller_line": frame.f_back.f_lineno,
                    "arguments": {name: normal(frame.f_locals.get(name)) for name in names},
                })
            elif event == "return":
                index = frames.pop(id(frame))
                calls[index]["result"] = normal(dict(arg)) if arg is not None else None
        if event == "return" and code is analyze_code:
            f = frame.f_locals
            local_capture.update({
                "k": f["k"], "weights": normal(f["w"]), "incidence": normal(f["inc"]),
                "triples": normal(f["triples"]),
                "six_scaled_pay_vectors": [
                    {"terminal": normal(z), "vector": normal(values)} for z, values in f["pay"].items()
                ],
                "six_scaled_second_floors": normal(f["phi"]), "menus": normal(f["menus"]),
                "root_values": normal(f["ga"]), "pure_root_values": normal(f["pure_ga"]),
                "root_minimizers": normal(f["ga_mix"]), "root_floor": normal(f["g"]),
                "actual_rows": normal(f["rows"]), "u1": normal(f["u1"]),
                "u2": normal(f["u2"]), "u3": normal(f["u3"]),
                "second_surplus": normal(f["y2"]), "welfare": normal(f["W"]),
                "security_backgrounds": normal(f["B"]), "security_matrix": normal(f["M"]),
            })

    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    result = None
    error = None
    try:
        sys.setprofile(profile)
        result = module.analyze(point["k"], point["weights"])
    except BaseException:
        error = traceback.format_exc()
    finally:
        sys.setprofile(None)
    elapsed = time.perf_counter() - begin
    write("linprog-calls.json", calls)
    write("original-analyze-locals.json", local_capture)
    if result is not None:
        write("new-analysis.json", result)
    if error is not None:
        (RUN / "error.txt").write_text(error)
    write("execution.json", {
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "invocation": "one untouched original analyze(6, frozen integer weights), passive sys.setprofile only",
        "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
        "assertions_enabled": __debug__, "wall_seconds_with_observer": elapsed,
        "inputs_before": before, "inputs_after": [fingerprint(original), fingerprint(frozen)],
        "call_counts": counts, "helper_replacements": 0,
        "additional_original_calls": 0, "sample_main_calls": 0,
        "status": "PASS" if error is None else "ERROR", "error_record": "error.txt" if error else None,
        "linprog_statuses": [row["result"]["status"] if row["result"] else None for row in calls],
        "new_fields_not_in_frozen_best": sorted(set(result or {}) - set(point)),
        "shared_fields_exactly_equal_as_JSON_values": sorted(k for k in point if k in (result or {}) and normal(result[k]) == point[k]),
        "historical_random_scan_replayed": False,
        "limits": [
            "Original main is not called; this is one frozen-point helper event, not a 300/500-sample reproduction.",
            "The output schema has two pure-root fields absent from the frozen report; byte identity is not claimed.",
            "Profile capture only serializes existing LP arguments/results and function locals; it does not generate a second matrix.",
            "No exact arithmetic theorem is inferred merely from solver success or numerical gap zero.",
        ],
    })
    print(json.dumps({"status": "PASS" if error is None else "ERROR", "counts": counts,
                      "linprog_statuses": [x["result"]["status"] if x["result"] else None for x in calls],
                      "run_dir": str(RUN)}))
    if error is not None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
