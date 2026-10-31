"""One unchanged --prefer-I invocation; observe existing calls/world variables.

No source functions are called after runpy returns. The ordinary mode is not run.
"""
from pathlib import Path
from collections import Counter, defaultdict
import ast
import hashlib
import json
import runpy
import sys

here = Path(__file__).resolve().parent
source = here / "source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/mixed/audit_joint_rank.py"
assert __debug__
assert hashlib.sha256(source.read_bytes()).hexdigest() == "7ea863dbc55d16514ec3d2ac10333a5bb2ebc5ea5283aaf4f5638dd9a115175a"
assert not source.with_name("joint_rank_audit.json").exists()
assert not source.with_name("joint_rank_audit_prefer_I.json").exists()
lines = source.read_text().splitlines()
tree = ast.parse(source.read_text())
token_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "token")
token_loop_line = next(i for i in range(token_node.lineno, token_node.end_lineno + 1) if lines[i - 1].strip() == "while True:")
report_line = next(i for i, line in enumerate(lines, 1) if line.lstrip().startswith("reports.append("))
counts = Counter()
token_prices = Counter()
token_lengths = Counter()
maxflow_returns = []
send_units = defaultdict(int)
seen_worlds = set()
worlds = []
source_argv_seen = []

def trace_module(frame, event, arg):
    if event == "line" and frame.f_lineno == report_line:
        g = frame.f_globals
        rank = tuple(g["U"])
        if rank not in seen_worlds:
            seen_worlds.add(rank)
            ends, prices, owner = g["ends"], g["prices"], g["owner"]
            worlds.append({"rank": list(rank), "sources_by_role": list(g["src"]),
                           "query_I": g["numI"], "query_tokens": len(ends),
                           "endpoint_prices": dict(Counter(map(str, prices.values()))),
                           "tokens_ending_at_owner": sum(ends[x][0] == owner[x] for x in ends),
                           "tokens_ending_after_owner": sum(ends[x][0] > owner[x] for x in ends),
                           "B_canceled_R": sum(g["canceled_B"].get(x, 0) for x in g["R"]),
                           "B_canceled_I": sum(g["canceled_B"].get(x, 0) for x in g["Im"]),
                           "A_seeded_R_cancellation": g["before"],
                           "A_final_R_cancellation": sum(g["canceled_A"].values()),
                           "joint_cost": str(g["joint"]), "R_only_cost": str(g["onlyR"]),
                           "joint_cost_minus_retained_token_mass": str(g["joint"] - (len(g["R"]) + g["numI"] - len(g["G"]))),
                           "R_only_cost_minus_net_R_mass": str(g["onlyR"] - (len(g["R"]) - len(g["G"]))),
                           "projection_margin": str(g["joint"] - g["numI"] - g["onlyR"])})
    return trace_module

def trace_global(frame, event, arg):
    if event != "call" or frame.f_code.co_filename != str(source):
        return None
    name = frame.f_code.co_name
    if name == "<module>":
        counts["source_module_entries"] += 1
        source_argv_seen.extend(sys.argv)
        return trace_module
    if name == "token":
        counts["token_function_calls"] += 1
        visits = 0
        def trace_token(frame, event, arg):
            nonlocal visits
            if event == "line" and frame.f_lineno == token_loop_line:
                visits += 1
            if event == "return":
                token_lengths[str(visits)] += 1
                token_prices[str(arg[1])] += 1
                counts["token_endpoints_after_owner"] += int(arg[0][0] > frame.f_globals["owner"][frame.f_locals["x"]])
            return trace_token
        return trace_token
    if name == "maxflow":
        counts["maxflow_function_calls"] += 1
        def trace_flow(frame, event, arg):
            if event == "return":
                g = frame.f_globals
                network = "B" if frame.f_locals["self"] is g["B"] else "A"
                maxflow_returns.append({"rank": list(g["U"]), "network": network, "added_flow": arg})
            return trace_flow
        return trace_flow
    if name == "send":
        counts["send_function_calls"] += 1
        g = frame.f_globals
        is_B = frame.f_locals["self"] is g.get("B")
        phase = "B_maxflow" if is_B else ("A_seed_R_paths" if frame.f_back.f_code.co_name == "<module>" else "A_residual_maxflow")
        counts["send_calls_" + phase] += 1
        send_units[phase] += frame.f_locals["amount"]
    return None

old_argv = sys.argv[:]
sys.argv = [str(source), "--prefer-I"]
sys.settrace(trace_global)
try:
    ns = runpy.run_path(str(source), run_name="__main__")
finally:
    sys.settrace(None)
    sys.argv = old_argv

snapshot = {"origin": "external observation of exactly one unchanged --prefer-I source invocation",
            "source_argv_seen": source_argv_seen, "function_counts": dict(counts),
            "token_endpoint_price_counts": dict(token_prices),
            "token_query_state_visit_counts": dict(token_lengths),
            "maxflow_returns": maxflow_returns, "send_units": dict(send_units),
            "world_observations": worlds,
            "query_menus": [{"role": i, "action": a, "leaf": list(z), "D": str(ns["D"][i, a]), "actual_u": str(ns["u"][i])} for (i, a), z in ns["menus"].items()],
            "completed_original_report": ns["out"],
            "ordinary_mode_invocations": 0,
            "source_function_calls_after_runpy_return": 0}
(here / "execution-state.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
