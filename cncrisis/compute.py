"""Sequential, restartable research jobs with a declared core-hour budget."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"early-warning", "bank-stress", "bridge", "nowcast", "loan", "stock-flow"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def _load(args):
    plan = json.loads(Path(args.file).read_text())
    cores, budget = int(plan["allocated_cores"]), float(plan["plan_core_hour_budget"])
    if cores < 1 or not 0 < budget <= 180:
        raise ValueError("Declare actual allocated cores and a plan budget in (0, 180]")
    if os.environ.get("CODESPACES") == "true":
        cores = os.cpu_count() or cores
    jobs = plan["jobs"]
    if len({j["id"] for j in jobs}) != len(jobs):
        raise ValueError("Unique job IDs required")
    for job in jobs:
        if job["method"] not in ALLOWED or not job["id"] or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in job["id"]):
            raise ValueError("Only named research methods and simple job IDs are allowed")
        timeout = float(job.get("timeout_seconds", 1800))
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("Finite positive per-job timeouts required")
    return plan, cores, budget


def execute(args):
    plan, cores, budget = _load(args)
    base = args.workspace / "compute"
    ledger_path = base / "ledger.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"schema": "cncrisis-compute-ledger.v1", "budget_period": plan["budget_period"], "sessions": [], "runs": []}
    if ledger["budget_period"] != plan["budget_period"]:
        raise ValueError("Use a separate workspace for a new declared budget period")
    consumed = sum(s["estimated_core_hours"] for s in ledger["sessions"])
    if args.compute_command == "plan":
        return {"jobs": len(plan["jobs"]), "allocated_cores": cores, "plan_budget": budget,
            "estimated_plan_usage": consumed, "remaining_plan_budget": max(0, budget - consumed),
            "accounting": "Declared-core x runner wall time. Excludes builds, idle time and other sessions; not the GitHub bill or remaining account allowance."}
    if not 0 < args.session_seconds <= 39600:
        raise ValueError("Keep a session at most 11 hours, below the Codespaces 12-hour lifecycle limit")
    if os.name != "posix":
        raise RuntimeError("The compute runner targets Linux/Codespaces; other CLI functions remain available")
    import fcntl
    base.mkdir(parents=True, exist_ok=True)
    with (base / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another compute runner is using this workspace") from exc
        if ledger_path.exists():
            ledger = json.loads(ledger_path.read_text())
            if ledger["budget_period"] != plan["budget_period"]:
                raise ValueError("The workspace budget period changed before acquiring the lock")
        consumed = sum(s["estimated_core_hours"] for s in ledger["sessions"])
        started = time.monotonic()
        for previous in ledger["sessions"]:
            if previous["status"] == "running":
                previous["status"] = "interrupted"
        for previous in ledger["runs"]:
            if previous["status"] == "running":
                previous["status"] = "interrupted"
        session = {"started_at": datetime.now(timezone.utc).isoformat(), "allocated_cores": cores,
            "estimated_core_hours": 0, "status": "running"}
        ledger["sessions"].append(session)
        sources = sorted((ROOT / "cncrisis").glob("*.py")) + [ROOT / "work.py", ROOT / "crisis.py"] + sorted(ROOT.glob("requirements*.txt"))
        code_hash = hashlib.sha256(b"".join(str(p.relative_to(ROOT)).encode() + b"\0" + p.read_bytes() for p in sources)).hexdigest()
        versions = {"python": sys.version}
        for package in ("numpy", "pandas", "scipy", "statsmodels", "scikit-learn", "joblib", "threadpoolctl"):
            try:
                versions[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                versions[package] = "not-installed"
        environment_hash = hashlib.sha256(json.dumps(versions, sort_keys=True).encode()).hexdigest()
        def checkpoint():
            session["estimated_core_hours"] = (time.monotonic() - started) * cores / 3600
            write(ledger_path, ledger)
        checkpoint()
        for job in plan["jobs"]:
            elapsed = time.monotonic() - started
            remaining_seconds = min(args.session_seconds - elapsed, (budget - consumed) * 3600 / cores - elapsed)
            if remaining_seconds < 1:
                session["status"] = "budget_or_session_limit"
                break
            source = (ROOT / job["input"]).resolve()
            spec = json.loads(source.read_text())
            fingerprint_parts = [code_hash, environment_hash, job["method"], digest(source)]
            if spec.get("csv"):
                fingerprint_parts.append(digest(ROOT / spec["csv"]))
            fingerprint = hashlib.sha256("|".join(fingerprint_parts).encode()).hexdigest()
            old = next((x for x in reversed(ledger["runs"]) if x["id"] == job["id"] and x["fingerprint"] == fingerprint and x["status"] == "complete"), None)
            if old and (base / old["output"]).exists() and digest(base / old["output"]) == old["output_sha256"]:
                checkpoint()
                continue
            output = Path("outputs") / (job["id"] + "-" + fingerprint[:12] + ".json")
            row = {"id": job["id"], "method": job["method"], "fingerprint": fingerprint,
                "output": str(output), "status": "running", "input_sha256": digest(source), "code_sha256": code_hash,
                "environment_sha256": environment_hash, "versions": versions}
            ledger["runs"].append(row)
            checkpoint()
            command = [sys.executable, str(ROOT / "work.py"), "methods", "run", "--name", job["method"], "--input", str(source), "--output", str(base / output)]
            env = os.environ.copy()
            for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
                env[key] = str(cores)
            before = time.monotonic()
            timeout = max(.1, min(float(job.get("timeout_seconds", 1800)), remaining_seconds))
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, pass_fds=(lock.fileno(),))
            try:
                while True:
                    left = timeout - (time.monotonic() - before)
                    if left <= 0:
                        raise subprocess.TimeoutExpired(command, timeout)
                    try:
                        _, error = process.communicate(timeout=min(5, left))
                        break
                    except subprocess.TimeoutExpired:
                        checkpoint()
                row["status"] = "complete" if process.returncode == 0 else "failed"
                if process.returncode == 0:
                    row["output_sha256"] = digest(base / output)
                else:
                    row["error"] = error[-4000:]
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                row["status"] = "timeout"
            except BaseException:
                process.kill()
                process.communicate()
                row["status"] = "interrupted"
                row["wall_seconds"] = time.monotonic() - before
                session["status"] = "interrupted"
                checkpoint()
                raise
            row["wall_seconds"] = time.monotonic() - before
            checkpoint()
        else:
            session["status"] = "finished"
        checkpoint()
    return {"workspace": str(args.workspace), "session": session, "runs": [{k: r[k] for k in ("id", "status", "output")} for r in ledger["runs"]],
        "accounting": "Only runner wall time at declared cores. Builds, idle time, stopped-instance storage and other activity are outside this ledger. Outputs and input/code hashes support restart."}


def register_cli(subparsers):
    parser = subparsers.add_parser("compute", help="按计划运行、保存和恢复实际研究计算；记录计划内估计核时")
    children = parser.add_subparsers(dest="compute_command", required=True)
    for name in ("plan", "run"):
        p = children.add_parser(name)
        p.add_argument("--file", type=Path, required=True)
        p.add_argument("--session-seconds", type=float, default=10800)
        p.set_defaults(func=execute)
