"""Run frozen source once; trace only its maxflow calls and existing loop line.

No functions or data are replaced. After runpy returns no source function runs.
"""
from pathlib import Path
import hashlib
import json
import runpy
import sys

here = Path(__file__).resolve().parent
source = here / "source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/shared/audit_owner_transport_independent.py"
assert __debug__
assert hashlib.sha256(source.read_bytes()).hexdigest() == "536f72ffe712eadb0602536f767b1f75d54c5fd81f29b102006c49a75a1fb343"
assert not source.with_suffix(".json").exists()
augment_line = next(i for i, line in enumerate(source.read_text().splitlines(), 1) if line.strip() == "total+=delta")
calls = 0
module_entries = 0
stats = {}
witnesses = {}

def trace_global(frame, event, arg):
    global calls, module_entries
    if event != "call" or frame.f_code.co_filename != str(source):
        return None
    if frame.f_code.co_name == "<module>":
        module_entries += 1
        return None
    if frame.f_code.co_name != "maxflow":
        return None
    network = "A" if calls % 2 == 0 else "B"
    calls += 1
    case = frame.f_globals["name"]
    key = case + ":" + network
    row = stats.setdefault(key, {"case": case, "network": network, "calls": 0,
                               "positive_source_graphs": 0, "zero_source_graphs": 0,
                               "augmentations": 0, "graphs_with_positive_final_net_role_transfer": 0})
    row["calls"] += 1
    def trace_flow(frame, event, arg):
        if event == "line" and frame.f_lineno == augment_line:
            assert frame.f_locals["delta"] > 0
            row["augmentations"] += 1
        if event == "return":
            loc = frame.f_locals
            cap, residual = loc["cap"], loc["residual"]
            s, t = loc["source"], loc["sink"]
            supply = sum(cap[s])
            assert arg == supply
            row["positive_source_graphs" if supply > 0 else "zero_source_graphs"] += 1
            role_edges = [{"from": i, "to": j, "net_flow": str(cap[i][j] - residual[i][j])}
                          for i in range(s) for j in range(s)
                          if cap[i][j] > 0 and cap[i][j] - residual[i][j] > 0]
            if role_edges:
                row["graphs_with_positive_final_net_role_transfer"] += 1
                if network not in witnesses:
                    g = frame.f_globals
                    witnesses[network] = {"case": case, "network": network,
                                          "profile_bitmasks": list(g["B"]),
                                          "optimal_tuple_bitmasks": list(g["T"]),
                                          "owner": {str(x): o for x, o in sorted(g["owner"].items())},
                                          "capacity_matrix": [[str(v) for v in r] for r in cap],
                                          "source_vertex": s, "sink_vertex": t,
                                          "flow_value": str(arg), "positive_final_net_role_edges": role_edges}
        return trace_flow
    return trace_flow

sys.settrace(trace_global)
try:
    ns = runpy.run_path(str(source), run_name="__main__")
finally:
    sys.settrace(None)
rows = list(stats.values())
snapshot = {"origin": "external observation of one unchanged execution, not fields of the original report",
            "source_module_entries": module_entries, "maxflow_function_calls": calls,
            "positive_source_graphs": sum(r["positive_source_graphs"] for r in rows),
            "zero_source_graphs": sum(r["zero_source_graphs"] for r in rows),
            "positive_augmentations": sum(r["augmentations"] for r in rows),
            "graphs_with_positive_final_net_role_transfer": sum(r["graphs_with_positive_final_net_role_transfer"] for r in rows),
            "by_case_and_network": rows, "first_observed_role_transfer_witnesses": witnesses,
            "original_counts_from_completed_namespace": ns["counts"],
            "source_function_calls_after_runpy_return": 0}
(here / "execution-state.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
