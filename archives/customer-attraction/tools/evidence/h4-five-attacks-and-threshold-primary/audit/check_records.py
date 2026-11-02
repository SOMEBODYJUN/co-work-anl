"""Read-only byte checks and saved-decimal menu residuals; execute no source."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent


def main():
    manifest = json.loads((EVIDENCE / "source-manifest.json").read_text())
    checks = []
    for item in manifest:
        p = EVIDENCE / "original" / item["id"] / Path(item["path"]).name
        data = p.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert (len(data), sha, blob) == (item["size"], item["sha256"], item["blob"])
        checks.append({"id": item["id"], "size": len(data), "sha256": sha, "blob_sha1": blob, "all_exact": True})

    raw = (EVIDENCE / "original/f7092503addae4d4beef/threshold_menu_probe.json").read_text()
    records = json.loads(raw, parse_float=str)
    assert len(records) == 3
    assert [(x["k"], x["r"], x["seed"]) for x in records] == [(4, 3, 41), (5, 3, 51), (6, 3, 61)]
    item = records[2]
    w = {int(k): F(v) for k, v in item["weights"].items()}
    p = list(map(F, item["p"]))
    eps = F(item["epsilon"])
    assert sum(p) == 1 and all(x >= 0 for x in p) and all(x >= 0 for x in w.values())
    columns = []
    all_slacks = []
    for a, tails in enumerate(item["menu"]):
        z = [a] + tails
        root = F()
        tail_values = [F() for _ in tails]
        query = F()
        for mask, weight in w.items():
            load = sum((mask >> topic) & 1 for topic in z)
            if (mask >> a) & 1:
                root += weight / load
            for j, topic in enumerate(tails):
                if (mask >> topic) & 1:
                    tail_values[j] += weight / load
            query += weight * sum(p[topic] for topic in range(item["k"]) if (mask >> topic) & 1) / (1 + load)
        slacks = [F(1) - eps - root] + [x - 1 for x in tail_values] + [query - 1 - eps]
        all_slacks += slacks
        columns.append({
            "root_label": a, "tails": tails,
            "root_profit_decimal_rational": str(root),
            "tail_profits_decimal_rational": list(map(str, tail_values)),
            "query_profit_decimal_rational": str(query),
            "root_profit_approx": float(root),
            "tail_profits_approx": list(map(float, tail_values)),
            "query_profit_approx": float(query),
            "root_constraint_slack_decimal_rational": str(slacks[0]),
            "tail_constraint_slacks_decimal_rational": list(map(str, slacks[1:-1])),
            "query_constraint_slack_decimal_rational": str(slacks[-1]),
        })
    report = {
        "scope": "Current read-only source-byte and stored-decimal static residual audit; no source execution, import, LP, BI, rational recovery, or exact SPE verification",
        "source_byte_checks": checks,
        "threshold_records": len(records),
        "source_and_report_implied_attempts": 5000 + 10000 + item["trial"] + 1,
        "attempt_count_status": "Derived from source first-positive-stop logic and saved fields, not a reconstructed historical process log",
        "fourth_scheduled_group_recorded": False,
        "stored_positive_support_size": len(w),
        "stored_p_exactly_sums_to_one": True,
        "decimal_vector_all_printed_epsilon_constraints_exact": min(all_slacks) >= 0,
        "minimum_decimal_slack": str(min(all_slacks)),
        "minimum_decimal_slack_approx": float(min(all_slacks)),
        "columns": columns,
        "no_modification_or_upgrade": "Weights and epsilon unchanged; saved decimal vector is not certified exact feasible; no integerization or new witness claimed",
    }
    (HERE / "static-source-and-record-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"seven_sources_byte_exact": True, "threshold_records": 3, "minimum_stored_decimal_slack": str(min(all_slacks)), "source_execution_LP_BI_exact_recovery": 0}))


if __name__ == "__main__":
    main()
