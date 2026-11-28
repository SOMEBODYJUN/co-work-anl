"""Reproduce retrospective event comparisons and accounting checks from pinned inputs."""

import hashlib
import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
REPO = HERE.parents[4]
JST = REPO / "research/models/jst_example/JSTdatasetR6.dta"
JST_SHA256 = "b0ebb74a8d1b5b1bc9033fc46a6dcc578736afff8ce1e1086b7840f2649e79b3"
WARNING = WORKSPACE / "compute/outputs/historical-warning-v1-cdc109f9a414.json"


def percent(factor):
    return (float(factor) - 1.0) * 100


def compound(rates):
    if rates.isna().any():
        return float("nan")
    return float((1 + rates).prod())


def path_metrics(rows, start, end):
    first, last = rows.loc[start], rows.loc[end]
    inflator = last.cpi / first.cpi
    stock_total = compound(rows.loc[start + 1 : end, "eq_tr"])
    stock_price = compound(rows.loc[start + 1 : end, "eq_capgain"])
    return {
        "nominal_home_proxy_pct": percent(last.hpnom / first.hpnom),
        "real_home_proxy_pct": percent(last.hpnom / first.hpnom / inflator),
        "nominal_wage_index_pct": percent(last.wage / first.wage),
        "nominal_gdp_per_person_pct": percent((last.gdp / last["pop"]) / (first.gdp / first["pop"])),
        "real_gdp_per_person_pct": percent(last.rgdpmad / first.rgdpmad),
        "real_consumption_per_person_pct": percent(last.rconsbarro / first.rconsbarro),
        "equity_price_local_pct": percent(stock_price),
        "equity_total_local_nominal_pct": percent(stock_total),
        "equity_total_local_real_pct": percent(stock_total / inflator),
        "equity_total_usd_nominal_pct": percent(stock_total * first.xrusd / last.xrusd),
        "cpi_pct": percent(inflator),
    }


def named_windows(data):
    output = []
    for iso, lo, hi in [("JPN", 1988, 1993), ("USA", 2003, 2008)]:
        rows = data.loc[data.iso == iso].set_index("year").sort_index()
        start = int(rows.loc[lo:hi, "hpnom"].idxmax())
        events = rows.loc[start : start + 10, "crisisJST"]
        event = int(events[events == 1].index[0])
        for end in range(start, start + 11):
            output.append({"country": iso, "peak_year": start, "end_year": end, "years_since_peak": end - start,
                           "jst_onset": event, "lag_years": event - start, **path_metrics(rows, start, end)})
    return pd.DataFrame(output)


def event_scan(data, drawdown):
    """Non-overlapping ex-post episodes; filters see subsequent prices, never a forecasting test."""
    output = []
    for iso, group in data.groupby("iso", sort=True):
        rows = group.set_index("year").sort_index()
        previous = 0
        for start in range(1970, 2011):
            if start - previous < 10:
                continue
            prices = rows.loc[start - 3 : start + 10, "hpnom"]
            labels = rows.loc[start : start + 10, "crisisJST"]
            if len(prices) != 14 or prices.isna().any() or labels.isna().any():
                continue
            # Strict seven-year peak avoids plateaus with arbitrarily chosen anchor years.
            if prices[start] <= prices.loc[start-3:start+3].drop(start).max():
                continue
            change = percent(prices.loc[start+1:start+5].min() / prices[start])
            if change > -drawdown:
                continue
            previous = start
            onsets = [int(year - start) for year in labels[labels == 1].index]
            output.append({"drop_filter_pct": drawdown, "country": iso, "peak_year": start,
                           "minimum_first_five_pct": change, "onset_lags_0_to_10": ",".join(map(str, onsets)),
                           "onset_at_six": 6 in onsets, "onset_in_window": bool(onsets),
                           **path_metrics(rows, start, start + 10)})
    return pd.DataFrame(output)


def score_audit():
    saved = json.loads(WARNING.read_text())["result"]
    predictions = pd.DataFrame(saved["test_predictions"])
    summary = []
    for model, group in predictions.groupby("model"):
        negative = group.loc[group.event == 0]
        episodes = group.loc[group.event == 1].groupby("event_id").alarm.any()
        metrics = saved["models"][model]["calibrated_test"]
        brier = float((group.score - group.event).pow(2).mean())
        assert abs(metrics["brier"] - brier) < 1e-12
        assert int(episodes.sum()) == metrics["detected_episodes"]
        summary.append({"model": model, "test_rows": len(group), "positive_rows": int(group.event.sum()),
                        "negative_alarm_rows": int(negative.alarm.sum()), "negative_rows": len(negative),
                        "episode_hits": int(episodes.sum()), "episode_misses": int((~episodes).sum()),
                        "usa_2007_detected": bool(episodes["USA-2007"]), "brier": brier})
    return summary


def main():
    assert hashlib.sha256(JST.read_bytes()).hexdigest() == JST_SHA256
    data = pd.read_stata(JST)
    assert len(data) == 2718 and len(data.iso.unique()) == 18
    cases = named_windows(data)
    cases.to_csv(HERE / "named_paths.csv", index=False, float_format="%.8f")
    scans, scan_results = [], []
    for threshold in [5, 10, 15]:
        scan = event_scan(data, threshold)
        scans.append(scan)
        valid_equity = scan.equity_total_local_real_pct.dropna()
        scan_results.append({"drawdown_cutoff_pct": threshold, "episodes": len(scan),
                             "countries": scan.country.nunique(),
                             "nominal_home_below_peak_at_ten": int((scan.nominal_home_proxy_pct < 0).sum()),
                             "real_home_below_peak_at_ten": int((scan.real_home_proxy_pct < 0).sum()),
                             "real_equity_below_purchase_at_ten": int((valid_equity < 0).sum()),
                             "real_equity_observed_at_ten": len(valid_equity),
                             "jst_onset_year_zero_to_ten": int(scan.onset_in_window.sum()),
                             "jst_onset_exactly_year_six": int(scan.onset_at_six.sum()),
                             "near_gfc_peaks_2006_to_2009": int(scan.peak_year.between(2006, 2009).sum())})
    pd.concat(scans, ignore_index=True).to_csv(HERE / "event_scan.csv", index=False, float_format="%.8f")
    obs = json.loads((HERE / "official_inputs.json").read_text())
    old, new = obs["china_2015"], obs["china_2016"]
    sg = obs["setser_2024_example"]
    b, deficit = sg["opening_debt_over_gdp"], sg["deficit_over_current_gdp"]
    interest = sg["interest_rate_for_primary_deficit_alternative"]
    kr = obs["korea_1998_1999"]
    jp = obs["japan_world_gdp_current_usd"]
    share_1990 = jp["japan_1990"] / jp["world_1990"]
    share_2010 = jp["japan_2010"] / jp["world_2010"]
    result = {"data_sha256": JST_SHA256, "sample_sensitivity": scan_results,
              "published_forecast_replay": score_audit(),
              "china_2015_2016": {
                  "static_interest_saving_100m_cny": old["swap_issued_100m_cny"] * (old["old_average_rate"] - old["new_average_rate"]),
                  "sales_area_change_pct": percent(new["new_housing_sales_10000_sqm"] / old["new_housing_sales_10000_sqm"]),
                  "finished_unsold_area_change_10000_sqm": new["finished_unsold_10000_sqm"] - old["finished_unsold_10000_sqm"],
                  "finished_unsold_area_change_pct": percent(new["finished_unsold_10000_sqm"] / old["finished_unsold_10000_sqm"])},
              "korea_real_gdp_1999_vs_1997_pct": percent((1 + kr["real_gdp_growth_1998"]) * (1 + kr["real_gdp_growth_1999"])),
              "japan_world_gdp_current_usd": {"share_1990_pct": 100*share_1990,
                                               "share_2010_pct": 100*share_2010,
                                               "difference_pp": 100*(share_2010 - share_1990),
                                               "relative_change_pct": percent(share_2010/share_1990)},
              "setser_debt_dynamics": [{"nominal_growth_pct": 100*g, "general_deficit_end_ratio_pct": 100*(b/(1+g)+deficit),
                                         "general_deficit_stabilizing_ratio_pct": 100*b*g/(1+g),
                                         "primary_deficit_end_ratio_pct": 100*((1+interest)*b/(1+g)+deficit)}
                                        for g in sg["nominal_growth"]]}
    (HERE / "results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
