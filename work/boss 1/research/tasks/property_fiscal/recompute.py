"""Reproduce national and local fiscal and housing descriptions from transcribed releases.

Run without network: python recompute.py. Currency in 100 million yuan except the
explicit Dingnan example (10,000 yuan). Areas in 10,000 square metres. Inter-vintage
level comparisons are descriptive. Official comparable growth is a separate input.
"""
import csv
import json
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent


def read_table(name):
    with (HERE / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def regular_table(name):
    return {row["period"]: {key: float(value) for key, value in row.items()
                             if key not in {"period", "source_id", "published_at"}}
            for row in read_table(name)}


def percent_change(new, old):
    return round(100 * (new / old - 1), 4)


def summary():
    prop = regular_table("property_releases.csv")
    fiscal = regular_table("fiscal_releases.csv")
    supplement = {(row["indicator"], row["period"]): float(row["value"])
                  for row in read_table("supplemental.csv")}
    cities = read_table("cities_price_202610.csv")
    assert len({(r["market"], r["city"]) for r in cities}) == 140
    result = {}
    price = {}
    for market in ("new", "resale"):
        members = [r for r in cities if r["market"] == market]
        assert len(members) == 70
        for key in ("mom_index", "yoy_index"):
            levels = [float(r[key]) for r in members]
            price[f"{market}_{key}"] = dict(
                equally_weighted_change_pct=round(mean(levels) - 100, 4),
                up=sum(x > 100 for x in levels),
                flat=sum(x == 100 for x in levels),
                down=sum(x < 100 for x in levels),
            )
    result["cities_202610"] = price
    result["2021_to_2025_level_changes_pct"] = {
        k: percent_change(prop["2025"][k], prop["2021"][k]) for k in prop["2021"]
    }
    result["2021_to_2025_fiscal_level_changes_pct"] = {
        k: percent_change(fiscal["2025"][k], fiscal["2021"][k]) for k in fiscal["2021"]
    }
    current, previous = prop["2026M10"], prop["2025M10"]
    v = supplement
    result["new_property_price_composition"] = {
        "current_yuan_per_m2": round(current["sales_value"] / current["sales_area"] * 10000, 2),
        "comparable_sales_amount_over_area_change_pct": percent_change(
            1 + v["sales_value_comparable_yoy", "2026M10"] / 100,
            1 + v["sales_area_comparable_yoy", "2026M10"] / 100),
        "initial_vintage_sales_area_growth_pct": percent_change(
            current["sales_area"], previous["sales_area"]),
    }
    result["land_receipts_less_broad_related_outlay_100m"] = {
        p: row["land_receipts"] - row["land_related_outlay"] for p, row in fiscal.items()
    }
    diff = {k: fiscal["2026M10"][k] - fiscal["2025M10"][k] for k in fiscal["2026M10"]}
    result["2026M10_minus_2025M10_fiscal_delta_100m"] = diff
    result["change_in_land_receipts_minus_related_outlay_100m"] = diff["land_receipts"] - diff["land_related_outlay"]
    result["change_in_two_local_own_receipt_lines_100m"] = diff["local_general_own_income"] + diff["local_funds_own_income"]
    result["land_income_loss_net_of_avoided_direct_cost_scenarios_100m"] = {
        str(r): round(-diff["land_receipts"] * (1 - r), 2) for r in (0, 0.5, 0.8, 1)
    }
    def final(key):
        return v[key, "2025"]
    fund_resources = final("final_fund_own") + final("final_fund_transfer") + final("final_fund_special_debt")
    assert round(fund_resources - final("final_fund_outlay"), 2) == final("final_fund_balance")
    result["2025_final_accounts_100m"] = {
        "general_expenditure_implied": round(sum(final(k) for k in ("final_general_own",
            "final_general_transfer", "final_general_other_and_carry", "final_general_deficit")), 2),
        "fund_resources": round(fund_resources, 2),
        "fund_outlay": final("final_fund_outlay"),
        "fund_carry_and_transfers": final("final_fund_balance"),
        "land_receipts_minus_broad_outlay": round(final("final_land_revenue") - final("final_land_outlay"), 2),
    }
    total = v["statutory_bond_principal_due", "2026M10"]
    rollover = v["refinancing_for_matured_principal", "2026M10"]
    own = v["other_funds_for_principal", "2026M10"]
    assert total == rollover + own
    result["statutory_bonds_2026M10"] = {
        "principal_refinanced_pct": round(100 * rollover / total, 2),
        "interest_plus_other_principal_resources_100m": v["interest_paid", "2026M10"] + own,
        "all_refinancing_issues_minus_issues_used_for_these_maturities_100m":
            v["all_refinancing_issues", "2026M10"] - rollover,
    }
    for name in ("scheduled_principal", "scheduled_principal_plus_interest"):
        result[name + "_2027_vs_2026_pct"] = percent_change(v[name, "2027"], v[name, "2026"])
    county = {}
    for period in ("2024决算", "2025执行"):
        county[period] = round(v["county_land_gross", period] - v["county_acquisition_compensation", period]
                             - v["county_displaced_farmer_aid", period], 2)
    result["dingnan_receipts_less_two_cost_lines_10000"] = county
    return result


if __name__ == "__main__":
    output = json.dumps(summary(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (HERE / "results.json").write_text(output, encoding="utf-8")
    print(output, end="")

