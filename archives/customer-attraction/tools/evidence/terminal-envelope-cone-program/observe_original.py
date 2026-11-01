"""One authorized small canonical-certificate/unchanged optimize event; no random main."""
from pathlib import Path
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
import numpy as np
import scipy
from scipy.sparse import issparse

ROOT = Path("/workspace/scratch/c0ab78c47566")
REPO = ROOT / "boss7-cleaner"
WORK = ROOT / "round21-terminal-envelope-work"
RUN = WORK / "original-small-event"
SOURCE = ROOT / "round21-envelope_cone_probe.py"
DEPS = REPO / "archives/customer-attraction/tools/evidence/credible-padding-program/dependencies/customer_attraction"
INSTANCE = REPO / "archives/customer-attraction/tools/evidence/incoming-balance-audit-history-primary/dependencies/examples/customer_attraction/portfolio_matching_failure.json"


def norm(x):
    if issparse(x):
        return norm(x.toarray())
    if isinstance(x, np.ndarray):
        return norm(x.tolist())
    if isinstance(x, np.generic):
        return norm(x.item())
    if isinstance(x, dict):
        return {str(k): norm(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [norm(v) for v in x]
    if isinstance(x, float) and not math.isfinite(x):
        return str(x)
    if x is None or isinstance(x, (str, int, float, bool)):
        return x
    return str(x)


def write(name, data):
    (RUN/name).write_text(json.dumps(norm(data), ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def fp(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def main():
    RUN.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(SOURCE, RUN/"envelope_cone_probe.py")
    shutil.copyfile(INSTANCE, RUN/"portfolio_matching_failure.json")
    (RUN/"customer_attraction").mkdir()
    for name in ["__init__.py", "model.py", "exact.py", "certificate.py"]:
        shutil.copyfile(DEPS/name, RUN/"customer_attraction"/name)
    inputs = [RUN/"envelope_cone_probe.py", RUN/"portfolio_matching_failure.json"] + sorted((RUN/"customer_attraction").glob("*.py"))
    before = [fp(p) for p in inputs]
    sys.path.insert(0, str(RUN))
    sp = importlib.util.spec_from_file_location("observed_envelope", RUN/"envelope_cone_probe.py")
    module = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(module)
    instance = module.Instance.from_dict(json.loads((RUN/"portfolio_matching_failure.json").read_text()))
    assert instance.players == 2 and instance.topic_count == 5 and instance.customer_count == 86
    solver = module.ExactSPESolver(instance)
    counts = {"canonical_worst_certificate": 0, "original_optimize": 0, "original_main": 0, "linprog": 0}
    codes = {module.ExactSPESolver.worst_certificate.__code__: "canonical_worst_certificate",
             module.optimize.__code__: "original_optimize", module.main.__code__: "original_main",
             module.linprog.__code__: "linprog"}
    captures = {}
    lp = []
    def observe(frame, event, arg):
        code = frame.f_code
        if event == "call" and code in codes:
            counts[codes[code]] += 1
        if code is module.linprog.__code__:
            if event == "call":
                names = ["c", "A_ub", "b_ub", "A_eq", "b_eq", "bounds", "method", "callback", "options", "x0", "integrality"]
                lp.append({"arguments": {name: norm(frame.f_locals.get(name)) for name in names}})
            elif event == "return":
                lp[-1]["result"] = norm(dict(arg)) if arg is not None else None
        if code is module.optimize.__code__ and event == "return":
            f = frame.f_locals
            for key in ["m", "p", "masks", "incidence", "z", "w", "rows", "matrix"]:
                captures[key] = norm(f[key])
            captures["terminal_cache"] = norm(f["terminal"].cache_info()._asdict())
            captures["coefficient_cache"] = norm(f["coefficients"].cache_info()._asdict())
    error = None
    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    cert = result = None
    try:
        sys.setprofile(observe)
        cert = solver.worst_certificate()
        result = module.optimize(instance, cert)
    except BaseException:
        error = traceback.format_exc()
    finally:
        sys.setprofile(None)
    elapsed = time.perf_counter()-begin
    if cert is not None:
        write("complete-policy.json", cert.to_dict())
    if result is not None:
        write("original-result.json", result)
    write("linprog-capture.json", lp)
    write("original-local-capture.json", captures)
    write("solver-state.json", {"stats": solver.stats.__dict__,
          "outcomes": [{"counts": k, "terminals": sorted(v)} for k,v in sorted(solver._outcomes.items())],
          "thresholds": [{"counts": k, "value": str(v)} for k,v in sorted(solver._thresholds.items())]})
    if error:
        (RUN/"error.txt").write_text(error)
    historical = json.loads((ROOT/"round21-envelope_known_cones.json").read_text())["records"][-1]
    comparable = {k: historical[k] for k in result or {} if k in historical}
    write("execution.json", {"status": "PASS" if error is None else "ERROR",
          "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
          "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
          "assertions_enabled": __debug__, "observed_wall_seconds": elapsed,
          "call_counts": counts, "helper_replacements": 0,
          "inputs_before": before, "inputs_after": [fp(p) for p in inputs],
          "known_record_compared": "portfolio_matching_failure",
          "shared_historical_fields": comparable,
          "shared_historical_fields_match": {k: norm(result[k]) == v for k,v in comparable.items()},
          "random_main_replayed": False, "remaining_known_cases_replayed": False,
          "limits": ["One m2/p5 canonical worst certificate and one original optimize helper.",
                     "The saved fixture strategy with path 4,0 is not used; canonical reconstruction is recorded.",
                     "Passive capture is not an independent matrix implementation.",
                     "No historical 12-random or seven-known batch reconstruction."]})
    print(json.dumps({"status": "PASS" if error is None else "ERROR", "call_counts": counts,
                      "result": norm(result), "stats": solver.stats.__dict__}))
    if error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
