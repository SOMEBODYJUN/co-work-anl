#!/usr/bin/env python3
"""One seed policy in each original parameter domain, with exact candidate audits.

The original file is imported unchanged. Only its linprog reference is wrapped
to record the result and the caller's policy; the same SciPy solver is called.
This is a new bounded execution, not the original 1,000-policy main sweep.
"""
from contextlib import redirect_stdout, redirect_stderr
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import inspect
import io
import json
import os
import platform
import time

import numpy
import scipy

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/private_block_scan.py"
PARAMETERS = [(6, 3, 0), (6, 4, 0), (6, 4, 1), (7, 5, 0), (7, 5, 1)]
EXPECTED_SHA = "8852a0c6c5acd6a2ab539ad2210ec6ccf372bcf223f8ba18c8f62f6249bffa91"


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, width - 1):
                yield (first,) + rest


def exact_audit(k, r, background, moves, root_action, chosen_tuple, weights, value):
    w = [F(float(x)).limit_denominator(10**6) for x in weights]
    z = F(float(value)).limit_denominator(10**6)
    expected_states = {q for d in range(r) for q in compositions(d, k)}
    assert set(moves) == expected_states
    assert all(0 <= a < k for a in moves.values())
    assert all(x >= 0 for x in w)
    assert moves[(0,) * k] == root_action
    masks = [tuple(a for a in range(k) if mask >> a & 1)
             for mask in range(1, 1 << k)]

    def terminal(q):
        q = list(q)
        while sum(q) < r:
            q[moves[tuple(q)]] += 1
        return tuple(b + c for b, c in zip(background, q))

    def after_action(q, action):
        q = list(q)
        q[action] += 1
        return terminal(q)

    def utility(action, terminal_counts):
        return sum((weight / sum(terminal_counts[a] for a in members)
                    for members, weight in zip(masks, w)
                    if weight and action in members), F(0))

    gaps = []
    minimum_record = None
    for q in sorted(moves, key=lambda q: (sum(q), q)):
        action = moves[q]
        actual = utility(action, after_action(q, action))
        for other in range(k):
            gap = actual - utility(other, after_action(q, other))
            gaps.append(gap)
            if minimum_record is None or gap < F(minimum_record["gap"]):
                minimum_record = {"counts": list(q), "action": action,
                                  "deviation": other, "gap": str(gap)}
    leaf = terminal((0,) * k)
    root_u = utility(root_action, leaf)
    blocks = []
    for j in chosen_tuple:
        blocks.append(sum((weight for members, weight in zip(masks, w)
                           if weight and root_action not in members and j in members
                           and sum(a in chosen_tuple for a in members) == 1
                           and not any(background[a] for a in members)), F(0)))
    passed = root_u == 1 and min(gaps) >= 0 and z >= 0 and min(blocks) >= z
    return {
        "status": "PASS" if passed else "rational-lift-not-certified",
        "reconstruction_max_denominator": 10**6,
        "max_float_weight_change": max(abs(float(a) - float(b)) for a, b in zip(w, weights)),
        "weights": [[mask, str(weight)] for mask, weight in enumerate(w, 1) if weight],
        "packing_floor": str(z), "root_utility": str(root_u),
        "root_terminal": list(leaf), "block_sizes": list(map(str, blocks)),
        "count_states": len(moves), "action_comparisons_including_self": len(gaps),
        "self_comparisons": len(moves), "minimum_ic": minimum_record,
        "negative_comparisons": sum(gap < 0 for gap in gaps),
        "all_ordered_histories_represented_by_the_given_count_policy": True,
        "count_policy": [{"counts": list(q), "action": a}
                         for q, a in sorted(moves.items(), key=lambda item: (sum(item[0]), item[0]))],
    }


def main():
    raw = SOURCE.read_bytes()
    assert len(raw) == 2306 and sha256(raw).hexdigest() == EXPECTED_SHA
    spec = spec_from_file_location("original_private_block_probe", SOURCE)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    original_solver = module.linprog
    records = []

    def record_solver(*args, **kwargs):
        frame = inspect.currentframe().f_back
        local = frame.f_locals
        result = original_solver(*args, **kwargs)
        record = {
            "k": local["k"], "r": local["r"], "t": local["t"],
            "rep": local["rep"], "background": list(local["b"]),
            "root_action": local["a"], "T": list(local["T"]),
            "solver_success": bool(result.success), "solver_status": int(result.status),
            "solver_message": result.message,
            "inequality_count": int(kwargs["A_ub"].shape[0]),
            "variable_count_including_floor": len(args[0]),
        }
        if result.success:
            record["float_objective"] = float(-result.fun)
            record["float_weights"] = list(map(float, result.x[:-1]))
            record["float_min_inequality_slack"] = float(min(result.ineqlin.residual))
            record["float_equality_residual"] = list(map(float, result.eqlin.residual))
            record["exact_candidate_audit"] = exact_audit(
                local["k"], local["r"], local["b"], dict(local["moves"]),
                local["a"], local["T"], result.x[:-1], -result.fun)
        records.append(record)
        return result

    module.linprog = record_solver
    destination = HERE / "run"
    destination.mkdir(exist_ok=True)
    # The source writes only on a >2 candidate. Contain that hardcoded path.
    (destination / "research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction").mkdir(parents=True, exist_ok=True)
    out, err = io.StringIO(), io.StringIO()
    start = time.perf_counter()
    previous_directory = Path.cwd()
    try:
        os.chdir(destination)
        with redirect_stdout(out), redirect_stderr(err):
            returns = [module.scan(k, r, t, 1) for k, r, t in PARAMETERS]
    finally:
        os.chdir(previous_directory)
    elapsed = time.perf_counter() - start
    assert len(records) == 15 and all(returns)
    assert all(row["solver_success"] for row in records)
    result = {
        "status": "bounded-execution-completed", "source_sha256": EXPECTED_SHA,
        "python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
        "execution": "unchanged original scan; recording wrapper calls the same linprog",
        "seed": 72218, "seed_reset_between_scan_calls": False,
        "parameter_calls": [[k, r, t, 1] for k, r, t in PARAMETERS],
        "original_default_1000_policy_main_executed": False,
        "sampled_seed_policies": 5, "packing_lp_calls": len(records),
        "returns": returns, "elapsed_seconds": elapsed,
        "rational_lifts_certified": sum(row["exact_candidate_audit"]["status"] == "PASS" for row in records),
        "rational_lifts_not_certified": sum(row["exact_candidate_audit"]["status"] != "PASS" for row in records),
        "exact_ic_comparisons_including_self": sum(x["exact_candidate_audit"]["action_comparisons_including_self"] for x in records),
        "records": records,
        "general_private_block_bound_or_half_proved": False,
    }
    (destination / "stdout.txt").write_text(out.getvalue())
    (destination / "stderr.txt").write_text(err.getvalue())
    (destination / "bounded-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
