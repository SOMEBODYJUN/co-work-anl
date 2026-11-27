#!/usr/bin/env python3
"""Measure this workbench on the machine that actually executes the command.

All training data are generated capacity fixtures. Scores describe only that
fixture and are not estimates of Chinese economic conditions or crisis risk.
"""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def read_limit(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return None


def environment():
    packages = {}
    for name in ["numpy", "pandas", "scipy", "statsmodels", "akshare", "scikit-learn"]:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    meminfo = read_limit("/proc/meminfo") or ""
    memtotal = next((int(line.split()[1]) * 1024 for line in meminfo.splitlines()
                     if line.startswith("MemTotal:")), None)
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpus_visible": os.cpu_count(),
        "cpu_affinity_count": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "cgroup_cpu_max": read_limit("/sys/fs/cgroup/cpu.max"),
        "cgroup_memory_max": read_limit("/sys/fs/cgroup/memory.max"),
        "host_memory_total_bytes": memtotal,
        "codespaces": os.environ.get("CODESPACES") == "true",
        "codespace_name": os.environ.get("CODESPACE_NAME"),
        "packages": packages,
    }


def training_fixture(rows, features, threads):
    import numpy as np
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score, brier_score_loss, log_loss
    from threadpoolctl import threadpool_limits

    rng = np.random.default_rng(20261126)
    X = rng.normal(size=(rows, features))
    linear = -3.0 + 1.0 * X[:, 0] - .7 * X[:, 1] + .9 * (X[:, 2] > .5)
    probabilities = 1 / (1 + np.exp(-linear))
    y = rng.binomial(1, probabilities)
    train_end, calibration_end = int(rows * .6), int(rows * .8)
    models = {
        "regularized_logit": LogisticRegression(max_iter=300),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=100, max_leaf_nodes=15, l2_regularization=1, random_state=20261126),
    }
    results = []
    with threadpool_limits(limits=threads):
        for name, model in models.items():
            started = time.perf_counter()
            model.fit(X[:train_end], y[:train_end])
            # Fit the calibrator only on the separate middle block. The final
            # block is unused by either fitting step. This is a capacity fixture,
            # not an implementation of episode-grouped crisis validation.
            def logits(p):
                p = np.clip(p, 1e-8, 1 - 1e-8)
                return np.log(p / (1 - p)).reshape(-1, 1)
            calibration_p = model.predict_proba(X[train_end:calibration_end])[:, 1]
            calibrator = LogisticRegression(C=1e6, max_iter=200)
            calibrator.fit(logits(calibration_p), y[train_end:calibration_end])
            raw = model.predict_proba(X[calibration_end:])[:, 1]
            calibrated = calibrator.predict_proba(logits(raw))[:, 1]
            truth = y[calibration_end:]
            baseline = np.repeat(y[:train_end].mean(), len(truth))
            results.append({
                "model": name, "elapsed_seconds": time.perf_counter() - started,
                "training_rows": train_end,
                "calibration_rows": calibration_end - train_end,
                "test_rows": rows - calibration_end,
                "test_positive_count": int(truth.sum()),
                "fixture_only_metrics": {
                    "average_precision": float(average_precision_score(truth, calibrated)),
                    "raw_brier": float(brier_score_loss(truth, raw)),
                    "calibrated_brier": float(brier_score_loss(truth, calibrated)),
                    "base_rate_brier": float(brier_score_loss(truth, baseline)),
                    "log_loss": float(log_loss(truth, calibrated)),
                },
                "prediction_range": [float(calibrated.min()), float(calibrated.max())],
            })
    return {
        "input_kind": "synthetic_capacity_fixture", "rows": rows,
        "features": features, "thread_limit": threads, "seed": 20261126,
        "models": results,
        "interpretation": "Capacity and separate-fit-block exercise only. No Chinese data, event labels, country transfer, crisis-episode validation or economic forecast.",
    }


def run(args):
    from cncrisis import methods
    out = {
        "schema": "cncrisis-runtime-benchmark.v1",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "environment": environment(), "adapter_replays": [],
    }
    summaries = {
        "loan": ["input_kind", "reference_error"],
        "stock-flow": ["input_kind", "debt_identity_residual"],
        "bridge": ["input_kind", "n_test"],
        "nowcast": ["input_kind", "converged", "news_reconciliation_error"],
        "akshare": ["input_kind", "mode", "rows"],
    }
    for name, keys in summaries.items():
        started = time.perf_counter()
        result = methods.execute(name)["result"]
        out["adapter_replays"].append({
            "name": name, "elapsed_seconds": time.perf_counter() - started,
            "result": {k: result[k] for k in keys},
        })
    out["training"] = training_fixture(args.rows, args.features, args.threads)
    out["peak_process_rss_mib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    out["scope"] = "Measured execution on the reported host; not a maximum capacity or economic-model validation claim."
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=30000)
    parser.add_argument("--features", type=int, default=24)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.rows < 1000 or args.features < 3 or args.threads < 1:
        parser.error("rows >= 1000, features >= 3 and threads >= 1 are required")
    result = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
