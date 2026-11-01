"""Run the byte-preserved entry point in an isolated cwd; observe, do not patch it."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import contextlib
import hashlib
import io
import json
import os
import platform
import runpy
import sys
import time
import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/structured_packing_scan.py"
EXPECTED = "635b06a919eaeb2b7a237a80b734cc87ddba1620aa0a1732ce351d5106414f8a"
OUT = HERE / "rerun"
HARD_CODED = Path("research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction")


def observe(frame, event, arg):
    if event != "return" or frame.f_code.co_name != "scan" or Path(frame.f_code.co_filename).resolve() != SOURCE:
        return
    d = frame.f_locals
    n, k, lp = d["n"], d["k"], d["lp"]
    seed = [int(x) for x in d["w"]]
    priority = [1, 0] + list(range(2, k))
    last_differences = []
    exact_seed_min = None
    @lru_cache(None)
    def value(c, a):
        return sum((F(w, sum(c[j] for j in range(k) if mask >> j & 1))
                    for mask, w in enumerate(seed, 1) if w and mask >> a & 1), F(0))
    @lru_cache(None)
    def terminal(q):
        if sum(q) == n:
            return q
        a = d["moves"][q]
        child = list(q)
        child[a] += 1
        return terminal(tuple(child))
    for q, a in d["moves"].items():
        children = []
        for b in range(k):
            child = list(q)
            child[b] += 1
            children.append(terminal(tuple(child)))
        chosen = value(children[a], a)
        for b in range(k):
            slack = chosen - value(children[b], b)
            exact_seed_min = slack if exact_seed_min is None else min(exact_seed_min, slack)
        if sum(q) == n - 1:
            exact_action = max(priority, key=lambda b: value(children[b], b))
            if exact_action != a:
                last_differences.append({"q": q, "float_action": a, "rational_priority_action": exact_action,
                                         "float_action_exact_value": str(chosen),
                                         "priority_action_exact_value": str(value(children[exact_action], exact_action))})
    result = {
        "n": n, "labels": ["A", "B"] + ["L" + str(j + 1) for j in range(n)],
        "customer_type_count": d["K"], "nonterminal_count_states": len(d["moves"]),
        "ic_rows_including_self": len(d["rows"]), "packing_rows": n,
        "ordered_nonterminal_histories_covered_by_count_policy": sum(k ** t for t in range(n)),
        "seed": [(i + 1, w) for i, w in enumerate(seed) if w],
        "root_terminal_count": d["c"], "exact_seed_minimum_ic_slack_for_observed_policy": str(exact_seed_min),
        "last_move_difference_from_exact_priority": last_differences,
        "success": bool(lp.success), "message": lp.message,
        "ratio": float(-lp.fun) if lp.success else None,
        "floating_primal_minimum_ic_slack": float(np.min(np.array(d["rows"]) @ lp.x[:d["K"]])) if lp.success else None,
        "floating_primal_minimum_packing_slack": float(np.min(d["es"] @ lp.x[:d["K"]] - lp.x[-1])) if lp.success else None,
        "floating_primal_root_normalization": float(d["u"] @ lp.x[:d["K"]]) if lp.success else None,
        "equality_marginals": lp.eqlin.marginals.tolist() if lp.success else None,
        "moves": [(q, a) for q, a in d["moves"].items()],
        "rowids": d["rowids"],
    }
    (OUT / ("observed_" + str(n) + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
    (OUT / HARD_CODED).mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    previous = Path.cwd()
    log = io.StringIO()
    try:
        os.chdir(OUT)
        sys.setprofile(observe)
        with contextlib.redirect_stdout(log):
            runpy.run_path(str(SOURCE), run_name="__main__")
    finally:
        sys.setprofile(None)
        os.chdir(previous)
    (OUT / "stdout.txt").write_text(log.getvalue())
    meta = {"status": "local-prepared", "source_sha256": EXPECTED,
            "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "elapsed_seconds": time.perf_counter() - start,
            "method": "unmodified original entry point via runpy; return-frame observer only; isolated cwd",
            "source_bytes_unchanged": hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED,
            "scope": "All original entry point calls n=4,5,6; no other scans or n values executed"}
    (OUT / "run-metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(log.getvalue(), end="")
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
