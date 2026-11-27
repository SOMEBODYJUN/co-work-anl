"""One JSON interface for executable methods and explicitly labelled references.

The default example inputs are synthetic engineering fixtures, not forecasts.
All assumptions for real analysis must come from the caller's input JSON.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import warnings

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "methods"
REGISTRY = {
    "early-warning": {"method": "Chronological, label-maturity-purged logit/HGB with separate sigmoid calibration and episode metrics", "state": "research-estimator; explicit panel and target required", "upstream": "scikit-learn; experiment design informed by BoE WP848", "version": "1"},
    "bank-stress": {"method": "Reconciled opening balance sheet, allowance absorption, capital and liquidity/firesale stress", "state": "conditional accounting; explicit measured inputs and assumptions required", "upstream": "balance-sheet stress accounting; local implementation", "version": "1"},
    "loan": {"method": "Contractual amortization; numpy-financial pmt/ipmt/ppmt reference", "state": "runtime-tested", "upstream": "numpy/numpy-financial", "version": "1.0.0"},
    "bridge": {"method": "Expanding-window OLS bridge and lagged-observation baseline", "state": "runtime-tested-synthetic", "upstream": "numpy.linalg.lstsq", "version": "2.3.5"},
    "nowcast": {"method": "DynamicFactorMQ fit/apply/get_forecast/news", "state": "runtime-tested-synthetic", "upstream": "statsmodels/statsmodels", "version": "0.15.0"},
    "stock-flow": {"method": "Debt and cash stock-flow accounting identities", "state": "runtime-tested-synthetic", "upstream": "national-accounts identities; local implementation", "version": "1"},
    "akshare": {"method": "macro_china_gdp real endpoint and cached replay", "state": "live-endpoint-tested", "upstream": "akfamily/akshare", "version": "1.20.70"},
    "gmd-panel": {"method": "Read user-supplied historical panel CSV; preserve countries and missingness", "state": "input-adapter; database-not-bundled", "upstream": "KMueller-Lab/Global-Macro-Database", "version": "license snapshot 2930dade4a9afefee614eb79091b6de3d90933e3"},
    "boe-reference": {"method": "Historical banking-crisis warning variables and validation design", "state": "reference-only; no upstream model executed", "upstream": "bank-of-england/MachineLearningCrisisPrediction", "version": "282fcbf0111af169053118110b4031d16c64bd56"},
    "frbny-reference": {"method": "Mixed-frequency vintage and news-update design", "state": "source-vendored-reference; MATLAB not executed", "upstream": "FRBNY-TimeSeriesAnalysis/Nowcasting", "version": "19f365cab8269e3aac3faa11ad091d6e913c5c43"},
    "research-contract": {"method": "Macro outlook, scenario analysis and thesis revision prompts", "state": "prompt-vendored-reference; LLM execution belongs to Pro/agents", "upstream": "TauricResearch/TradingAgents", "version": "121265d18d467ac717f7af99cb0d669c15d2e73c"},
    "editorial-contract": {"method": "Chinese prose revision instructions", "state": "prompt-vendored-reference; LLM editing belongs to Pro/agents", "upstream": "jiji262/humanizer-chinese", "version": "1d6c08e10fbfe0e1b36ac784834451c6aae0a92c"},
}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _financial():
    path = ROOT / "vendor" / "numpy-financial" / "_financial.py"
    spec = importlib.util.spec_from_file_location("cncrisis_vendored_financial", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def loan(data):
    data = data or {"principal": 1000000, "annual_rate": 0.03, "months": 240, "input_kind": "synthetic_test"}
    principal, annual, months = float(data["principal"]), float(data["annual_rate"]), data["months"]
    if principal < 0 or annual < 0 or not math.isfinite(principal + annual) or not isinstance(months, int) or isinstance(months, bool) or months < 1:
        raise ValueError("principal/rate must be finite and nonnegative; months must be a positive integer")
    rate = annual / 12
    payment = principal / months if rate == 0 else principal * rate / (1 - (1 + rate) ** (-months))
    reference = float(-_financial().pmt(rate, months, principal))
    if abs(reference - payment) > 1e-6:
        raise ArithmeticError("numpy-financial reference differs")
    remaining, rows = principal, []
    for month in range(1, months + 1):
        interest = remaining * rate
        paid_principal = min(remaining, payment - interest)
        remaining = max(0., remaining - paid_principal)
        rows.append({"month": month, "interest": interest, "principal": paid_principal, "payment": interest + paid_principal, "balance": remaining})
    return {"input_kind": data.get("input_kind", "caller_supplied"), "unit": "CNY; monthly; annual rate in decimal", "payment": payment, "reference_payment": reference, "reference_error": abs(payment-reference), "interest_total": sum(r["interest"] for r in rows), "schedule": rows}


def stock_flow(data):
    data = data or {"input_kind": "synthetic_test", "opening_debt": 100, "new_financing": 20, "principal_repaid": 10, "writeoff": 2, "revaluation": 0, "opening_cash": 15, "cash_receipts": 20, "cash_payments": 18}
    fields = ["opening_debt", "new_financing", "principal_repaid", "writeoff", "revaluation", "opening_cash", "cash_receipts", "cash_payments"]
    v = {k: float(data[k]) for k in fields}
    if not all(math.isfinite(x) for x in v.values()):
        raise ValueError("Accounting inputs must be finite")
    if any(v[k] < 0 for k in fields if k != "revaluation"):
        raise ValueError("Debt, financing, repayments, writeoffs and cash inputs must be nonnegative")
    ending_debt = v["opening_debt"] + v["new_financing"] - v["principal_repaid"] - v["writeoff"] + v["revaluation"]
    if ending_debt < 0:
        raise ValueError("Repayments/writeoffs exceed available debt")
    ending_cash = v["opening_cash"] + v["cash_receipts"] - v["cash_payments"]
    return {"input_kind": data.get("input_kind", "caller_supplied"), "unit": data.get("unit", "same unit as input"), "ending_debt": ending_debt, "ending_cash": ending_cash, "cash_shortfall": max(0., -ending_cash), "cash_usable": max(0., ending_cash), "debt_identity_residual": ending_debt - (v["opening_debt"] + v["new_financing"] - v["principal_repaid"] - v["writeoff"] + v["revaluation"]), "note": "Debt swaps remain debt. Cash shortfall is not automatic borrowing. This identity supplies no crisis probability."}


def _panel(data):
    import pandas as pd
    if data is None:
        data = json.loads((FIXTURES / "synthetic_panel.json").read_text())
    monthly = pd.DataFrame(data["monthly"], index=pd.PeriodIndex(data["monthly_periods"], freq="M"), dtype=float)
    quarterly = pd.DataFrame({"gdp": data["quarterly_gdp"]}, index=pd.PeriodIndex(data["quarterly_periods"], freq="Q"), dtype=float)
    if len(monthly) < 48 or len(quarterly) < 16 or not monthly.index.is_monotonic_increasing or not quarterly.index.is_monotonic_increasing:
        raise ValueError("Panel needs ordered >=48 monthly and >=16 quarterly observations")
    if monthly.index.has_duplicates or quarterly.index.has_duplicates:
        raise ValueError("Duplicate observation periods")
    return monthly, quarterly, data.get("input_kind", "caller_supplied"), data


def bridge(data):
    import numpy as np
    monthly, quarterly, kind, _ = _panel(data)
    aggregates = monthly.groupby(monthly.index.asfreq("Q")).mean()
    joint = aggregates.join(quarterly).dropna()
    X = np.column_stack([np.ones(len(joint)), joint[monthly.columns].values])
    y = joint["gdp"].values
    rows = []
    for t in range(12, len(joint)):
        coefficients = np.linalg.lstsq(X[:t], y[:t], rcond=None)[0]
        prediction = float(X[t] @ coefficients)
        baseline = float(y[t-1])
        rows.append({"quarter": str(joint.index[t]), "bridge": prediction, "lag_baseline": baseline, "actual": float(y[t])})
    return {"input_kind": kind, "evaluation": "Expanding-window completed-quarter bridge: each training sample ends before its evaluation quarter. For real-time nowcasts caller must provide publication-vintage panels.", "n_test": len(rows), "bridge_mae": float(np.mean([abs(x["bridge"]-x["actual"]) for x in rows])), "lag_baseline_mae": float(np.mean([abs(x["lag_baseline"]-x["actual"]) for x in rows])), "predictions": rows}


def nowcast(data):
    from statsmodels.tsa.statespace.dynamic_factor_mq import DynamicFactorMQ
    monthly, quarterly, kind, _ = _panel(data)
    # Withhold the last quarter target and the final monthly release in the old vintage.
    # Apply the identical parameter vector to isolate the contribution of new observations.
    old_monthly, old_quarterly = monthly.iloc[:-1], quarterly.iloc[:-1]
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        old = DynamicFactorMQ(old_monthly, endog_quarterly=old_quarterly, factors=1, factor_orders=1, idiosyncratic_ar1=False).fit(maxiter=500, tolerance=1e-4, disp=False)
        updated = old.apply(monthly, endog_quarterly=old_quarterly, retain_standardization=True)
        target = monthly.index[-1]
        news = updated.news(old, impact_date=target, impacted_variable="gdp")
        previous = float(news.prev_impacted_forecasts.loc[target, "gdp"])
        latest = float(news.post_impacted_forecasts.loc[target, "gdp"])
        impact = float(news.total_impacts.loc[target, "gdp"])
    identity_error = abs(latest-previous-impact)
    if identity_error > 1e-7:
        raise ArithmeticError("News impacts do not reconcile to the forecast revision")
    # statsmodels' EM return dictionary has llf/iter, rather than a converged key.
    # Apply the solver's own documented likelihood-change stopping rule.
    likelihood = old.mle_retvals["llf"]
    criterion = float(2 * abs(likelihood[-1]-likelihood[-2]) / (abs(likelihood[-1])+abs(likelihood[-2])))
    converged = criterion <= 1e-4
    return {"input_kind": kind, "model": "statsmodels DynamicFactorMQ(1 factor, AR(1), iid idiosyncratic)", "target_period": str(target), "target": "quarterly gdp latent monthly representation", "previous_estimate": previous, "updated_estimate": latest, "news_impact": impact, "news_reconciliation_error": identity_error, "next_month_forecast": {k: float(v) for k,v in updated.get_forecast(1).predicted_mean.iloc[0].items()}, "n_new_observations": int(len(news.news)), "parameters_held_fixed": True, "converged": converged, "em_iterations": int(old.mle_retvals["iter"]), "em_tolerance": 1e-4, "em_convergence_criterion": criterion, "warnings": sorted(set(str(w.message) for w in captured)), "economic_interpretation": "Activity nowcast only. The synthetic fixture is an API/information-vintage exercise, not Chinese GDP or a crisis probability."}


def akshare(data):
    data = data or {"mode": "replay"}
    mode = data.get("mode", "replay")
    if mode == "replay":
        path = Path(data.get("csv", FIXTURES / "akshare_macro_china_gdp.csv"))
        if not path.exists():
            raise FileNotFoundError("Cached macro fixture missing; run live mode once")
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        return {"mode": "offline-replay", "input_kind": "observed_vendor_series", "rows": len(rows), "columns": list(rows[0]) if rows else [], "sha256": _sha(path), "first_rows": rows[:2], "last_rows": rows[-2:], "definition": "GDP cumulative-quarter vendor table; not standalone-quarter seasonally adjusted real GDP. Release dates not supplied by this endpoint.", "source": "AKShare macro_china_gdp -> Eastmoney data center"}
    if mode != "live":
        raise ValueError("AKShare mode must be live or replay")
    import akshare as ak
    frame = ak.macro_china_gdp()
    destination = Path(data["output_csv"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    return {"mode": "live", "rows": len(frame), "columns": list(frame.columns), "path": str(destination), "sha256": _sha(destination), "source": "AKShare macro_china_gdp -> Eastmoney data center", "retrieved_at": datetime.now(timezone.utc).isoformat()}


def gmd_panel(data):
    if not data or not data.get("csv"):
        raise ValueError("gmd-panel requires caller's licensed CSV path in input.json")
    with Path(data["csv"]).open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    country_col = data.get("country_column", "country")
    requested = data.get("countries", [])
    selected = [r for r in rows if not requested or r.get(country_col) in requested]
    return {"input_kind": "caller_supplied_historical_panel", "rows": len(selected), "columns": list(selected[0]) if selected else [], "countries_requested": requested, "data": selected, "data_sha256": _sha(data["csv"]), "license": "The GMD database license is separate from Python package code; the workbench does not redistribute the database."}


def references(name):
    names = {"boe-reference": "BoE-license", "frbny-reference": "FRBNY-Nowcasting", "research-contract": "TradingAgents", "editorial-contract": "humanizer-chinese"}
    directory = ROOT / "vendor" / names[name]
    return {"kind": "reference_contract", "files": [str(p.relative_to(ROOT)) for p in sorted(directory.rglob("*")) if p.is_file()], "execution": "Read these references while Pro/agents perform their own analysis. This command does not call or impersonate an LLM."}


def doctor():
    packages = {}
    for name in ["numpy", "scipy", "pandas", "statsmodels", "numpy-financial", "akshare"]:
        try:
            packages[name] = {"installed": True, "version": importlib.metadata.version(name)}
        except importlib.metadata.PackageNotFoundError:
            packages[name] = {"installed": False, "install": "python -m pip install -r requirements-methods.txt"}
    manifest = ROOT / "vendor" / "manifest.json"
    failures = []
    if manifest.exists():
        for row in json.loads(manifest.read_text()):
            path = ROOT / row["path"]
            if not path.is_file() or _sha(path) != row["sha256"]:
                failures.append(row["path"])
    else:
        failures.append("vendor/manifest.json missing")
    return {"packages": packages, "vendor_integrity": "pass" if not failures else "fail", "vendor_failures": failures}


def execute(name, data=None):
    from .models import early_warning, bank_stress
    runners = {"early-warning": early_warning, "bank-stress": bank_stress, "loan": loan, "stock-flow": stock_flow, "bridge": bridge, "nowcast": nowcast, "akshare": akshare, "gmd-panel": gmd_panel}
    value = runners[name](data) if name in runners else references(name)
    return {"schema": "cncrisis-method-result.v1", "name": name, "capability": REGISTRY[name], "result": value}


def register_cli(subparsers):
    parser = subparsers.add_parser("methods", help="Executable method adapters and pinned method references")
    children = parser.add_subparsers(dest="method_command", required=True)
    for cmd in ["list", "doctor"]:
        p = children.add_parser(cmd)
        p.set_defaults(func=_cli)
    run = children.add_parser("run")
    run.add_argument("--name", required=True, choices=list(REGISTRY))
    run.add_argument("--input", type=Path)
    run.add_argument("--output", type=Path)
    run.set_defaults(func=_cli)


def _cli(args):
    if args.method_command == "list":
        result = REGISTRY
    elif args.method_command == "doctor":
        result = doctor()
    else:
        data = json.loads(args.input.read_text()) if args.input else None
        result = execute(args.name, data)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return result
