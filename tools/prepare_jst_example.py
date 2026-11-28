#!/usr/bin/env python3
"""Build a declared retrospective banking-onset experiment from JST R6."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def prepare(source, output):
    import pandas as pd
    data = pd.read_stata(source, convert_categoricals=False).sort_values(["iso", "year"])
    output.mkdir(parents=True, exist_ok=True)
    local_source = output / "JSTdatasetR6.dta"
    if source.resolve() != local_source.resolve():
        shutil.copyfile(source, local_source)
    records = []
    excluded = []
    features = ["credit_gdp", "credit_gdp_change_5y", "yield_curve", "short_rate", "real_house_price_growth_5y", "public_debt_gdp"]
    all_events = []
    for country, group in data.groupby("iso", sort=True):
        g = group.set_index("year").sort_index()
        events = sorted(int(y) for y in g.index[g.crisisJST == 1])
        all_events += [{"country": country, "year": y, "event_id": f"{country}-{y}"} for y in events]
        ratios = g.tloans / g.gdp
        real_house = g.hpnom / g.cpi
        for year in g.index:
            year = int(year)
            if year > 2016 or year + 3 > int(g.index.max()) or year - 6 not in g.index:
                continue
            if any(start <= y <= end for start, end in [(1914, 1919), (1939, 1949)] for y in range(year, year + 4)):
                continue
            if any(e <= year <= e + 4 for e in events):
                continue
            # An unobserved crisis indicator is not evidence of no crisis.  Require
            # the information year and every year of the complete label window.
            label_years = list(range(year, year + 4))
            labels = g.crisisJST.reindex(label_years)
            if labels.isna().any() or not labels.isin([0, 1]).all():
                excluded.append({"country": country, "year": year,
                    "reason": "unobserved_or_invalid_crisis_label",
                    "label_years": label_years})
                continue
            prev, old = g.loc[year - 1], g.loc[year - 6]
            future = [e for e in events if year < e <= year + 3]
            event_year = future[0] if future else None
            record = {"country": country, "as_of": f"{year}-12-31", "horizon_end": f"{year + 3}-12-31",
                "event": int(event_year is not None), "event_id": f"{country}-{event_year}" if event_year else "",
                "event_date": f"{event_year}-12-31" if event_year else "",
                "credit_gdp": float(ratios.loc[year - 1]),
                "credit_gdp_change_5y": float(ratios.loc[year - 1] - ratios.loc[year - 6]),
                "yield_curve": float(prev.ltrate - prev.stir), "short_rate": float(prev.stir),
                "real_house_price_growth_5y": float(real_house.loc[year - 1] / real_house.loc[year - 6] - 1),
                "public_debt_gdp": float(prev.debtgdp)}
            # Partial predictor gaps remain eligible for train-only imputation.
            # A row with no observed predictor contains no country-year signal.
            for feature in features:
                if not math.isfinite(record[feature]):
                    record[feature] = float("nan")
            if all(pd.isna(record[feature]) for feature in features):
                excluded.append({"country": country, "year": year,
                    "reason": "all_predictors_unobserved"})
                continue
            records.append(record)
    panel = pd.DataFrame(records)
    csv = output / "panel.csv"
    panel.to_csv(csv, index=False)
    try:
        csv_ref = str(csv.relative_to(ROOT))
    except ValueError:
        csv_ref = str(csv.resolve())
    spec = {"input_kind": "observed_historical_panel", "csv": csv_ref,
        "target_definition": "JST systemic banking crisis onset during the next three calendar years; yearly end-date convention; current onset and four subsequent information-years excluded",
        "information_mode": "retrospective_revised_lagged", "label_observed_through": "2020-12-31",
        "features": features, "threads": 2, "models": ["logit", "hist_gradient_boosting"],
        "split": {"train_end": "1984-12-31", "calibration_start": "1985-01-01", "calibration_end": "1999-12-31", "test_start": "2003-01-01", "test_end": "2016-12-31"},
        "alarm_rule": {"calibration_false_alarm_budget": .1, "decision_rationale": "Predeclared research comparison at a 10% negative-period alarm budget; not a China or household action threshold"}}
    (output / "experiment.json").write_text(json.dumps(spec, indent=2) + "\n")
    manifest = {"dataset": "Jorda-Schularick-Taylor Macrohistory Database, release 6",
        "source_page": "https://www.macrohistory.net/database/",
        "downloaded_version_url": "https://sfff5b3ac9317c4be.jimcontent.com/download/version/1720600177/module/9834512469/name/JSTdatasetR6.dta",
        "raw_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "panel_sha256": hashlib.sha256(csv.read_bytes()).hexdigest(),
        "raw_rows": len(data), "raw_columns": len(data.columns), "years": [int(data.year.min()), int(data.year.max())],
        "countries": sorted(data.iso.unique()), "source_onsets": all_events,
        "prepared_rows": len(panel), "positive_rows": int(panel.event.sum()),
        "distinct_targeted_episodes": int(panel.loc[panel.event == 1, "event_id"].nunique()),
        "feature_timing": "All predictors use year t-1 or earlier at information year t. These are revised historical data: no claim of verified first-release vintages.",
        "filters": "No information/prediction years overlapping 1914-1919 or 1939-1949; onset year through onset+4 excluded; first onset in next 3 years is the target. Information-year and all three future crisis indicators must be observed as 0/1; wholly unobserved predictor rows excluded. Partial predictor gaps are retained for train-only imputation.",
        "preparation_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_exclusions": excluded,
        "audit_exclusion_counts": {reason: sum(x["reason"] == reason for x in excluded) for reason in sorted({x["reason"] for x in excluded})},
        "coverage_limit": "Episode metrics cover eligible forecast rows. War, post-onset and missing-history exclusions can omit source episodes. Countries share global shocks; episode counts are not claims of statistical independence.",
        "license": "CC BY-NC-SA 4.0; this data/example folder only. See NOTICE.md.",
        "china": "China is not included. This experiment tests an actual historical research pipeline, not China probability calibration or an exact reproduction of BoE WP848."}
    (output / "data_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return {k: manifest[k] for k in ("raw_rows", "prepared_rows", "positive_rows", "distinct_targeted_episodes", "raw_sha256")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "research/models/jst_example")
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output), indent=2))
