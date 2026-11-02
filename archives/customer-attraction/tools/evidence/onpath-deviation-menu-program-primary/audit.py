"""Definition-level finite replay for the retained onpath_menu.py program.

This is a new audit, not a frozen historical output or a universal certificate.
All payoff-row comparisons below use Fraction and explicit ordered histories.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original"
SOURCE = ORIGINAL / "research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_security/onpath_menu.py"
spec = importlib.util.spec_from_file_location("retained_onpath_menu", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
import numpy as np
import scipy


def finish(policy, history, n):
    h = tuple(history)
    while len(h) < n:
        h += (int(policy[h]),)
    return h


def rho(mask, action, leaf):
    if not ((mask >> action) & 1):
        return F(0)
    return F(1, sum((mask >> b) & 1 for b in leaf))


def inspect(s, cone):
    policy = {h: int(a) for h, a in zip(s.histories, cone["policy"])}
    exact_rows = set()
    for h in s.histories:
        chosen = policy[h]
        z = finish(policy, h, s.n)
        for a in range(s.m):
            za = finish(policy, h + (a,), s.n)
            row = tuple(int(s.L * (rho(mask, chosen, z) - rho(mask, a, za))) for mask in range(1, 1 << s.m))
            if any(row):
                exact_rows.add(row)
    assert exact_rows == set(map(tuple, cone["gamma"].tolist()))
    # Independently delete the current position from the full ordered leaf.
    h = ()
    expected = set()
    while len(h) < s.n:
        i = len(h)
        for a in range(s.m):
            z = finish(policy, h + (a,), s.n)
            bg = z[:i] + z[i + 1:]
            assert len(bg) == s.n - 1
            expected.add(tuple(bg.count(b) for b in range(s.m)))
        h += (policy[h],)
    rows, path = mod.menu_rows(s, cone)
    observed = {tuple(map(int, s.Bc[r])) for r in rows}
    assert observed == expected
    assert tuple(path) == finish(policy, (), s.n)
    for r in rows:
        bg = tuple(s.B[r])
        for a in range(s.m):
            for mask in range(1, 1 << s.m):
                exact = F((mask >> a) & 1, 1 + sum((mask >> b) & 1 for b in bg))
                assert abs(float(exact) - s.static[r, a, mask - 1]) < 1e-15
    universal = s.k - 1
    assert int(cone["c"][universal]) == 1
    assert all(int(row[universal]) == 0 for row in cone["gamma"])
    assert all(abs(float(s.static[r, a, universal]) - 1 / s.n) < 1e-15 for r in rows for a in range(s.m))
    return dict(n=s.n, topics=s.m, ordered_histories=len(s.histories), all_comparisons=s.m * len(s.histories), unique_nonzero_Gamma_rows=len(exact_rows), actual_path=path, menu_background_counts=sorted(map(list, observed)), all_static_backgrounds=len(s.B))


def run_cli(label, args, expect_ok=True):
    out = HERE / "replay" / f"{label}.json"
    cmd = [sys.executable, str(SOURCE), *args, "--output", str(out)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    start = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=45)
    (HERE / "replay" / f"{label}.stdout.txt").write_text(p.stdout)
    (HERE / "replay" / f"{label}.stderr.txt").write_text(p.stderr)
    assert (p.returncode == 0) == expect_ok, (label, p.stderr)
    return dict(label=label, args=args, exit_code=p.returncode, elapsed_seconds=time.time()-start, output_created=out.exists(), stderr_last_line=p.stderr.splitlines()[-1] if p.stderr else "")


def main():
    (HERE / "replay").mkdir(exist_ok=True)
    cases = []
    for n in (1, 2, 3):
        for m in (2, 3):
            s = mod.old.Space(n, m)
            policies = {
                "constant_zero": {h: 0 for h in s.histories},
                "ordered_history_rule": {h: (len(h) + sum((i + 1) * a for i, a in enumerate(h))) % m for h in s.histories},
            }
            for name, policy in policies.items():
                row = inspect(s, s.full_policy(policy))
                row["policy_kind"] = name
                cases.append(row)
            weights = np.arange(1, s.k + 1, dtype=np.int64)
            weights[-1] = 0
            cone, meta = s.synthesize(weights, 2026102117)
            row = inspect(s, cone)
            row.update(policy_kind="synthesized", metadata=meta)
            assert all(sum(F(int(g)) * F(int(w)) for g, w in zip(gamma, weights)) >= 0 for gamma in cone["gamma"])
            cases.append(row)
    execution = [run_cli("zero_seed_nonarchive", ["--n", "3", "--k", "3", "--samples", "2", "--rounds", "4", "--seed", "2026102117"], expect_ok=False)]
    execution.append(run_cli("small_main", ["--n", "3", "--k", "3", "--samples", "1", "--rounds", "4", "--seed", "1"]))
    point = json.loads((HERE / "replay/small_main.json").read_text())["best"]
    s = mod.old.Space(point["n"], point["k"])
    cone = s.full_policy({tuple(z["history"]): z["action"] for z in point["policy"]})
    inspect(s, cone)
    w = [F(float(x)).limit_denominator(10**6) for x in point["weights"]]
    p = [F(float(x)).limit_denominator(10**6) for x in point["p"]]
    assert sum(w) == 1 and min(w) >= 0 and w[-1] == 0
    assert sum(p) == 1 and min(p) >= 0
    margins = [sum(F(int(g), s.L) * x for g, x in zip(row, w)) for row in cone["gamma"]]
    assert min(margins, default=F(0)) >= 0
    rows, path = mod.menu_rows(s, cone)
    vals = []
    for r in rows:
        bg = tuple(s.B[r])
        vals.append(sum(w[mask-1] * sum(p[a] for a in range(s.m) if (mask >> a) & 1) / (1 + sum((mask >> b) & 1 for b in bg)) for mask in range(1, 1 << s.m)))
    welfare = sum(F(int(c)) * x for c, x in zip(cone["c"], w))
    t = F(float(point["t"])).limit_denominator(10**6)
    assert min(vals) >= t
    exact_point = dict(weights=list(map(str, w)), query=list(map(str, p)), minimum_IC=str(min(margins, default=F(0))), minimum_selected_menu_value=str(min(vals)), saved_t=str(t), welfare=str(welfare), gap_W_minus_n_t=str(welfare-s.n*t), status="new finite exact reconstruction; no global cone bound")
    # Boundary probes preserve original failures; the source is never edited.
    execution.append(run_cli("zero_samples", ["--samples", "0"]))
    execution.append(run_cli("zero_rounds", ["--n", "2", "--k", "2", "--samples", "1", "--rounds", "0"], expect_ok=False))
    execution.append(run_cli("single_topic_nonarchive", ["--n", "2", "--k", "1", "--samples", "1", "--rounds", "1"], expect_ok=False))
    # A clearly labelled synthetic archive checks skip and process branches.
    # It is neither the frozen 21-case archive nor a historical output.
    fixture = ORIGINAL / "evidence/certificates/customer_attraction/new_policy_security_cones.json.gz"
    fixture.parent.mkdir(parents=True, exist_ok=True)
    fixture_cases = [
        dict(name="AUDIT_SYNTHETIC_single_topic_infeasible_after_exclusion", players=2, topics=1, policy=[dict(history=[], action=0), dict(history=[0], action=0)]),
        dict(name="AUDIT_SYNTHETIC_two_topics_constant_zero", players=2, topics=2, policy=[dict(history=[], action=0), dict(history=[0], action=0), dict(history=[1], action=0)]),
    ]
    fixture_payload = json.dumps(dict(scope="new synthetic archive fixture only", cases=fixture_cases), indent=2).encode()
    with gzip.open(fixture, "wb") as f:
        f.write(fixture_payload)
    try:
        execution.append(run_cli("synthetic_archive", ["--archive", "--rounds", "1", "--samples", "0", "--n", "99", "--k", "99"]))
    finally:
        fixture.unlink()
    (HERE / "replay/synthetic-archive-fixture.json").write_bytes(fixture_payload)
    result = dict(scope="finite implementation calibration and boundary behavior only", environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__), exact_ordered_history_cases=cases, original_cli_runs=execution, reconstructed_small_main_point=exact_point, original_21_case_archive_run=False, default_3player_6topic_run=False)
    (HERE / "audit-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(cases=len(cases), cli_runs=len(execution), exact_point=exact_point), ensure_ascii=False))


if __name__ == "__main__":
    main()
