"""Execute the byte-identical frozen source once; export existing globals only.

No source function is called after runpy returns. Profiling counts function entry
without replacing functions, assertions, inputs, or output paths.
"""
from pathlib import Path
import hashlib
import json
import runpy
import sys

here = Path(__file__).resolve().parent
source = here / "source-root/research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/direction_review/continuation_general_scope/incoming_payment_regression.py"
assert __debug__
assert not source.with_suffix(".json").exists(), "Replay must start without a report"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "f23464b03d8893a101b0af965003875f904d5439ff117017a07b09303bfaf17d"
counts = {}
def profile(frame, event, arg):
    if event == "call" and frame.f_code.co_filename == str(source):
        name = frame.f_code.co_name
        counts[name] = counts.get(name, 0) + 1

sys.setprofile(profile)
try:
    ns = runpy.run_path(str(source), run_name="__main__")
finally:
    sys.setprofile(None)

records = [{"client_index": x, "likes": sorted(ns["X"][x]),
            "owner": ns["owner"][x], "unit_price": str(ns["unit_v"][x]),
            "delta": str(ns["delta"][x]), "gamma": str(ns["gamma"][x]),
            "rho": str(ns["rho"][x]), "kappa": str(ns["kappa"][x])}
           for x in sorted(ns["R"])]
menus = [{"role": i, "action": a, "leaf": list(z),
          "D": str(ns["D"][i, a])} for (i, a), z in ns["menu"].items()]
source_caps = [str(ns["caps"][ns["S"], ("r", i)]) for i in range(ns["m"])]
positive_flows = [{"from": repr(a), "to": repr(b),
                   "flow": str(c - ns["res"][a, b])}
                  for (a, b), c in ns["caps"].items()
                  if c - ns["res"][a, b] > 0]
policy_evaluations = sum(sum(len(ns["X"][x]) ** (ns["m"] - start)
                             for start in range(ns["m"])) for x in ns["R"])
snapshot = {"origin": "post-execution globals; no subsequent source-function calls",
            "function_entries": counts, "client_records": records, "query_menus": menus,
            "residual_source_capacities": source_caps,
            "residual_maxflow_value": str(ns["flow_value"]),
            "positive_original_forward_edge_flows": positive_flows,
            "deterministic_policy_evaluations_from_actual_loop_bounds": policy_evaluations,
            "client_start_comparisons": ns["bell_checks"],
            "actual": list(ns["actual"]), "optimum": list(ns["T"]),
            "fullK": list(map(str, ns["fullK"])),
            "cancelledK": list(map(str, ns["K"]))}
(here / "execution-state.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
