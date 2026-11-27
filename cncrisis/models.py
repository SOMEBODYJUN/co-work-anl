"""Reproducible research estimators and explicit balance-sheet stress accounts."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import math
from pathlib import Path
import time


def _metrics(y, p, threshold, frame):
    import numpy as np
    from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
    two_classes = len(np.unique(y)) == 2
    alarm = p > threshold
    positives, negatives = y == 1, y == 0
    events = sorted(set(frame.loc[positives, "event_id"]))
    detected = [e for e in events if bool(alarm[(frame["event_id"] == e).to_numpy()].any())]
    reliability = []
    for lo, hi in zip(np.linspace(0, 1, 11)[:-1], np.linspace(0, 1, 11)[1:]):
        mask = (p >= lo) & ((p <= hi) if hi == 1 else (p < hi))
        if mask.any():
            reliability.append({"lower": float(lo), "upper": float(hi), "rows": int(mask.sum()),
                "mean_score": float(p[mask].mean()), "observed_frequency": float(y[mask].mean())})
    return {"rows": len(y), "positive_rows": int(positives.sum()), "distinct_country_episodes": len(events),
        "brier": float(brier_score_loss(y, p)), "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "average_precision": float(average_precision_score(y, p)) if two_classes else None,
        "roc_auc": float(roc_auc_score(y, p)) if two_classes else None,
        "false_alarm_fraction_negative_periods": float(alarm[negatives].mean()) if negatives.any() else None,
        "detected_episodes": len(detected), "missed_episodes": len(events) - len(detected),
        "reliability_bins": reliability}


def _split_panel(frame, spec):
    """Purge targets not yet observable at the next fitting boundary."""
    import pandas as pd
    f = frame.copy()
    for col in ("as_of", "horizon_end"):
        f[col] = pd.to_datetime(f[col], errors="raise")
        if f[col].isna().any():
            raise ValueError("Information and target-horizon dates cannot be missing")
    if f.country.isna().any():
        raise ValueError("Every observation needs its country identifier")
    if f[["country", "as_of"]].duplicated().any():
        raise ValueError("Duplicate country/information-date rows")
    if not f["event"].isin([0, 1]).all() or (f.horizon_end <= f.as_of).any():
        raise ValueError("Binary future-event labels and a strictly later horizon_end are required")
    f["event_id"] = f.event_id.fillna("").astype(str)
    if (f.loc[f.event == 1, "event_id"] == "").any():
        raise ValueError("Every positive label needs its actual crisis episode ID")
    if "event_date" in f:
        dates = pd.to_datetime(f.event_date, errors="coerce")
        pos = f.event == 1
        if (dates[pos].isna() | (dates[pos] <= f.loc[pos, "as_of"]) | (dates[pos] > f.loc[pos, "horizon_end"])).any():
            raise ValueError("Positive labels must describe an onset inside the future prediction window")
    if "available_at" in f:
        available = pd.to_datetime(f.available_at, errors="raise")
        if available.isna().any() or (available > f.as_of).any():
            raise ValueError("Feature release after the information date")
    split = spec["split"]
    train_end, cal_start, cal_end, test_start, test_end = [pd.Timestamp(split[k]) for k in (
        "train_end", "calibration_start", "calibration_end", "test_start", "test_end")]
    if not train_end < cal_start <= cal_end < test_start <= test_end:
        raise ValueError("Training, calibration and test dates must be chronological and disjoint")
    heldout = set(spec.get("heldout_countries", []))
    is_heldout = f.country.isin(heldout)
    train = f[(f.as_of <= train_end) & (f.horizon_end < cal_start) & ~is_heldout].copy()
    cal = f[(f.as_of >= cal_start) & (f.as_of <= cal_end) & (f.horizon_end < test_start) & ~is_heldout].copy()
    test = f[(f.as_of >= test_start) & (f.as_of <= test_end) & (f.horizon_end <= pd.Timestamp(spec["label_observed_through"]))].copy()
    if heldout:
        test = test[test.country.isin(heldout)].copy()
    parts = {"train": train, "calibration": cal, "test": test}
    for name, part in parts.items():
        if part.empty or part.event.nunique() < 2:
            raise ValueError(name + " needs both event and non-event observations; revise the declared experiment")
    for a, b in ((train, cal), (train, test), (cal, test)):
        if set(a.loc[a.event == 1, "event_id"]) & set(b.loc[b.event == 1, "event_id"]):
            raise ValueError("One crisis episode appears on both sides of a fitting boundary")
    return parts


def early_warning(spec):
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from threadpoolctl import threadpool_limits

    if not spec:
        raise ValueError("early-warning requires an explicit data/target/split specification")
    source = Path(spec["csv"])
    frame = pd.read_csv(source)
    features = spec["features"]
    if not features or len(features) != len(set(features)):
        raise ValueError("A unique, explicit feature list is required")
    if set(features) & {"country", "as_of", "horizon_end", "event", "event_id", "event_date", "available_at"}:
        raise ValueError("Labels, event identifiers and dates cannot be predictors")
    frame[features] = frame[features].apply(pd.to_numeric, errors="raise")
    if np.isinf(frame[features].to_numpy()).any():
        raise ValueError("Infinite feature values")
    if spec["information_mode"] not in ("verified_release_vintages", "retrospective_revised_lagged"):
        raise ValueError("Declare actual release-vintage validation or retrospective revised-data validation")
    if spec["information_mode"] == "verified_release_vintages" and "available_at" not in frame:
        raise ValueError("Verified-vintage panels need a maximum feature-release date per row")
    parts = _split_panel(frame, spec)
    train, cal, test = (parts[k] for k in ("train", "calibration", "test"))
    if train[features].isna().all().any():
        raise ValueError("A feature is entirely missing in the training sample")
    budget = float(spec["alarm_rule"]["calibration_false_alarm_budget"])
    if not 0 < budget < 1 or not spec["alarm_rule"].get("decision_rationale"):
        raise ValueError("Alarm tolerance is an explicit decision input with a rationale")
    threads = int(spec.get("threads", 2))
    if threads < 1:
        raise ValueError("Positive thread limit required")
    candidates = {
        "logit": make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=1, max_iter=500)),
        "hist_gradient_boosting": make_pipeline(SimpleImputer(strategy="median"), HistGradientBoostingClassifier(
            max_iter=100, max_leaf_nodes=7, min_samples_leaf=20, l2_regularization=1, random_state=20261126)),
    }
    requested = spec.get("models", list(candidates))
    if not requested or set(requested) - candidates.keys():
        raise ValueError("Supported estimators: logit and hist_gradient_boosting")
    rows, models = [], {}
    y_test = test.event.to_numpy(dtype=int)
    baseline = np.repeat(train.event.mean(), len(test))
    def logits(p):
        p = np.clip(p, 1e-8, 1 - 1e-8)
        return np.log(p / (1 - p)).reshape(-1, 1)
    with threadpool_limits(limits=threads):
        for name in requested:
            started = time.perf_counter()
            model = candidates[name]
            model.fit(train[features], train.event)
            cal_raw = model.predict_proba(cal[features])[:, 1]
            calibrator = LogisticRegression(C=1e6, max_iter=500).fit(logits(cal_raw), cal.event)
            cal_p = calibrator.predict_proba(logits(cal_raw))[:, 1]
            threshold = float(np.quantile(cal_p[cal.event.to_numpy() == 0], 1 - budget, method="higher"))
            raw_threshold = float(np.quantile(cal_raw[cal.event.to_numpy() == 0], 1 - budget, method="higher"))
            raw = model.predict_proba(test[features])[:, 1]
            p = calibrator.predict_proba(logits(raw))[:, 1]
            models[name] = {"parameters": {"estimator": str(model), "calibrator": "sigmoid fit only in calibration block"},
                "alarm_threshold": threshold, "raw_alarm_threshold": raw_threshold, "threshold_operator": ">",
                "elapsed_seconds": time.perf_counter() - started,
                "raw_test": _metrics(y_test, raw, raw_threshold, test),
                "calibrated_test": _metrics(y_test, p, threshold, test),
                "by_country": {c: _metrics(y_test[test.country.to_numpy() == c], p[test.country.to_numpy() == c], threshold,
                    test[test.country == c]) for c in sorted(test.country.unique())}}
            for (_, row), value, uncalibrated in zip(test.iterrows(), p, raw):
                rows.append({"model": name, "country": row.country, "as_of": str(row.as_of.date()),
                    "horizon_end": str(row.horizon_end.date()), "event": int(row.event), "event_id": row.event_id,
                    "raw_score": float(uncalibrated), "score": float(value), "alarm": bool(value > threshold)})
    descriptions = {k: {"rows": len(v), "countries": sorted(v.country.unique()),
        "as_of_min": str(v.as_of.min().date()), "as_of_max": str(v.as_of.max().date()),
        "last_label_maturity": str(v.horizon_end.max().date()),
        "distinct_country_episodes": int(v.loc[v.event == 1, "event_id"].nunique())} for k, v in parts.items()}
    return {"input_kind": spec["input_kind"], "target_definition": spec["target_definition"],
        "information_mode": spec["information_mode"], "data_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "features": features, "splits": descriptions, "baseline": _metrics(y_test, baseline, 1, test),
        "models": models, "test_predictions": rows, "alarm_rule": spec["alarm_rule"],
        "probability_admission": "Scores are research outputs. China transfer and probability use require an independent model-card decision; fitting/calibration alone does not grant that use.",
        "versions": {p: importlib.metadata.version(p) for p in ("numpy", "pandas", "scikit-learn")},
        "executed_at": datetime.now(timezone.utc).isoformat()}


def bank_stress(data):
    if not data:
        raise ValueError("bank-stress requires actual balance-sheet inputs and explicit stress assumptions")
    def number(value, nonnegative=True):
        x = float(value)
        if not math.isfinite(x) or (nonnegative and x < 0):
            raise ValueError("Finite, correctly signed balance-sheet amounts required")
        return x
    results = []
    for bank in data["banks"]:
        cash, liquid, other = [number(bank[k]) for k in ("cash", "liquid_assets_book", "other_assets")]
        deposits, debt, rwa = [number(bank[k]) for k in ("deposits", "other_liabilities", "risk_weighted_assets")]
        capital = number(bank["capital"], nonnegative=False)
        portfolios = {k: {"gross": number(v["gross"]), "allowance": number(v["allowance"])} for k, v in bank["credit"].items()}
        if rwa == 0 or any(v["allowance"] > v["gross"] for v in portfolios.values()):
            raise ValueError("Positive RWA and allowances no greater than gross exposure required")
        opening_assets = cash + liquid + other + sum(v["gross"] - v["allowance"] for v in portfolios.values())
        residual = opening_assets - deposits - debt - capital
        if abs(residual) > 1e-7 * max(1, opening_assets):
            raise ValueError("Opening bank balance sheet does not reconcile: " + bank["id"])
        for scenario in data["scenarios"]:
            rates = scenario["loss_rates"]
            if set(rates) != set(portfolios):
                raise ValueError("Loss rates must cover exactly the bank's non-overlapping credit portfolios")
            losses, used = 0., 0.
            for key, port in portfolios.items():
                rate = number(rates[key])
                if rate > 1:
                    raise ValueError("Credit loss rate cannot exceed one")
                loss = port["gross"] * rate
                losses += loss
                used += min(port["allowance"], loss)
            runoff, haircut = [number(scenario[k]) for k in ("deposit_runoff_fraction", "liquid_asset_haircut")]
            if runoff > 1 or haircut >= 1:
                raise ValueError("Runoff must be <= 1 and liquidation haircut < 1")
            due = number(scenario.get("wholesale_due", 0))
            if due > debt:
                raise ValueError("Wholesale maturities exceed opening non-deposit liabilities")
            earnings = number(scenario.get("cash_retained_earnings", 0), nonnegative=False)
            equity = number(scenario.get("equity_injection", 0))
            liquidity_loan = number(scenario.get("liquidity_loan", 0))
            cash_before_sales = cash + earnings + equity + liquidity_loan
            required = deposits * runoff + due
            sold = min(liquid, max(0, required - cash_before_sales) / (1 - haircut))
            fire_sale_loss = sold * haircut
            cash_position = cash_before_sales + sold * (1 - haircut) - required
            ending_capital = capital + earnings + equity - (losses - used) - fire_sale_loss
            scenario_rwa = rwa * number(scenario.get("rwa_multiplier", 1))
            if scenario_rwa <= 0:
                raise ValueError("Scenario RWA must be positive")
            minimum_ratio = number(bank["minimum_capital_ratio"])
            if minimum_ratio > 1:
                raise ValueError("Capital ratio is a fraction, not percent units")
            results.append({"bank": bank["id"], "scenario": scenario["id"], "gross_credit_loss": losses,
                "opening_allowance_used": used, "new_credit_loss_charged_to_capital": losses - used,
                "liquid_assets_sold_book": sold, "fire_sale_loss": fire_sale_loss,
                "ending_capital": ending_capital, "capital_ratio": ending_capital / scenario_rwa,
                "capital_shortfall": max(0, minimum_ratio * scenario_rwa - ending_capital),
                "cash_available_after_requested_outflows": max(0, cash_position),
                "unmet_funding_need": max(0, -cash_position), "opening_balance_residual": residual})
    return {"input_kind": data["input_kind"], "unit": data["unit"], "results": results,
        "scope": "One-horizon conditional stress accounts: cash earnings are realized and retained; credit losses are not deducted from cash twice; liquidity loans add funding, not equity; assumed RWA is explicit. Unmet outflows are funding needs, not free borrowing. No estimated event probabilities or automatic interbank contagion."}
