"""Replay and fully reconcile the 40-label legal-background counterexample."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent


def main():
    manifest = json.loads((BASE/"source-manifest.json").read_text())
    for row in manifest:
        raw = (BASE/row["preserved_relative_path"]).read_bytes()
        assert len(raw) == row["size"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    repo = next(p for p in BASE.parents if (p/"work.py").is_file())
    out = BASE/"replay"
    out.mkdir(exist_ok=True)
    filename = "global_credit_counterexample_audit.json"
    with tempfile.TemporaryDirectory(prefix="singleton-background-",
                                     dir=repo/"cleanup/workspaces/Boss2") as tmp:
        script = Path(tmp)/"global_credit_counterexample.py"
        shutil.copy2(BASE/"original"/script.name, script)
        result = subprocess.run([sys.executable, str(script)],
                                capture_output=True, text=True, check=True)
        raw = (Path(tmp)/filename).read_bytes()
        frozen = (BASE/"original"/filename).read_bytes()
        assert json.loads(raw) == json.loads(frozen)
        assert raw == frozen
        (out/filename).write_bytes(raw)
        (out/"stdout-summary.json").write_text(
            json.dumps(json.loads(result.stdout), ensure_ascii=False, indent=2)+"\n")
    data = json.loads(raw)
    table = [[F(x) for x in row] for row in data["last_payoff_table"]]
    clients, singleton_client = [], {}
    next_label = 6
    for mask, background, count in data["rows"]:
        for _ in range(count):
            interests = {a for a in range(6) if mask & (1 << a)}
            if background:
                singleton_client[next_label] = len(clients)
                interests.add(next_label)
                next_label += 1
            clients.append((interests, background))
    assert next_label == 40 and len(clients) == 52
    assert data["legal_prefix"] == list(range(6, 40))
    assert all(sum(a in interests for a in data["legal_prefix"]) == b
               for interests, b in clients)
    base = [F(8), F(9), F(9), F(9), F(10), F(10)]
    assert all(sum((F(1, b+1) for interests, b in clients if a in interests), F(0))
               == base[a] for a in range(6))
    original_six = [
        [F(16,3),9,9,9,9,9], [8,6,9,9,9,9],
        [8,9,F(9,2),9,9,9], [8,9,9,F(9,2),9,9],
        [7,8,8,8,6,8], [7,8,8,8,8,6],
    ]
    assert [row[:6] for row in table[:6]] == original_six
    # These formulas are the compact all-40-action proof printed in the text.
    for a in range(6):
        for e, x in singleton_client.items():
            interests, _ = clients[x]
            assert table[a][e] == F(1, 2+int(a in interests))
            assert table[e][a] == base[a]-F(int(a in interests), 6)
    for e in singleton_client:
        for f in singleton_client:
            assert table[e][f] == F(1, 2+int(e == f))
    replies = data["replies"]
    assert replies == [1,4,4,4,5,4]+[4]*34
    first = [F(x) for x in data["first_payoff_values"]]
    assert first == [table[replies[a]][a] for a in range(40)]
    gaps = [table[a][replies[a]]-table[a][b] for a in range(40) for b in range(40)]
    gaps += [first[0]-x for x in first]
    assert len(gaps) == 1640 and min(gaps) == 0
    best_fresh = best_profit = F(-1)
    fresh_pairs, profit_pairs = [], []
    for a, b in combinations_with_replacement(range(40), 2):
        fresh = sum(bg == 0 and (a in interests or b in interests)
                    for interests, bg in clients)
        profit = table[a][b]+table[b][a]
        if fresh > best_fresh:
            best_fresh, fresh_pairs = fresh, [[a,b]]
        elif fresh == best_fresh:
            fresh_pairs.append([a,b])
        if profit > best_profit:
            best_profit, profit_pairs = profit, [[a,b]]
        elif profit == best_profit:
            profit_pairs.append([a,b])
    assert best_fresh == 18 and fresh_pairs == [[2,3]]
    assert best_profit == 18 and profit_pairs == [[1,2],[1,3],[2,3]]
    summary = {
        "status": "PASS", "frozen_report_all_fields_equal": True,
        "frozen_report_byte_identical": True,
        "frozen_report_sha256": hashlib.sha256(raw).hexdigest(),
        "unit_customers": 52, "catalog_labels": 40, "legal_past_actions": 34,
        "remaining_players": 2, "ordered_decision_nodes": 41,
        "comparisons_including_self": len(gaps), "nonself_comparisons": len(gaps)-41,
        "zero_comparisons_including_self": sum(x == 0 for x in gaps),
        "strict_comparisons": sum(x > 0 for x in gaps),
        "minimum_positive_gap": str(min(x for x in gaps if x > 0)),
        "all_1600_payoff_cells_match_compact_formulas": True,
        "first_strategic_payoffs": list(map(str, first[:6])),
        "singleton_first_payoffs_by_class": {"A_only": "1/2", "B_only": "1/2",
                                             "ARS": "1/3", "BRS": "1/3"},
        "tail_P": 17, "tail_Delta": 0, "freshOPT2": best_fresh,
        "fresh_optimal_unordered_pairs": fresh_pairs,
        "background_total_profit_optimum_F2": str(best_profit),
        "F2_optimal_unordered_pairs": profit_pairs,
        "GLOBAL_gap": -1,
        "scope": "Complete fixed-background two-player SPE only; no 36-player root on-path certificate.",
        "later_status": "The separately preserved six-label full-root instance establishes actual-prefix failure; the frozen not_refuted field describes this earlier instance only.",
    }
    (out/"reconciliation.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
