"""Replay both frozen protected-price audits and reconcile their distinct scopes.

Frozen programs execute unchanged in temporary directories. The older seven-label
legal-background report is retained separately from the six-label zero-root case.
"""
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


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def comparison_counts(table, root_values, reply):
    gaps = []
    for a, row in enumerate(table):
        values = list(map(F, row))
        gaps.extend(values[reply[a]]-x for x in values)
    first = list(map(F, root_values))
    gaps.extend(first[0]-x for x in first)
    assert min(gaps) >= 0
    return {"nodes": len(table)+1, "comparisons_including_self": len(gaps),
            "nonself_comparisons": len(gaps)-len(table)-1,
            "zero_comparisons_including_self": sum(x == 0 for x in gaps),
            "strict_comparisons": sum(x > 0 for x in gaps)}


def omission_pair_table(labels, clients, actual):
    covered = {i for i, c in enumerate(clients) if c.intersection(actual)}
    records = []
    for a, b in combinations_with_replacement(labels, 2):
        union = {i for i, c in enumerate(clients) if a in c or b in c}
        records.append({"pair": [a, b], "union_size": len(union),
                        "omitted_from_actual": len(union-covered)})
    optimum = max(x["union_size"] for x in records)
    return {"actual_coverage": len(covered), "OPT2": optimum, "all_21_pairs": records,
            "optimal_pairs": [x for x in records if x["union_size"] == optimum]}


def verify_later_unique_case():
    # Explicit k=3 table read from the later source, used only to reconcile the
    # earlier existential claim's status. This is not that source's disposition.
    groups = [("A", 10), ("ARS", 6), ("B", 13), ("BRS", 4),
              ("BTRS", 1), ("BQRS", 1), ("T", 8), ("TR", 5),
              ("TS", 5), ("Q", 8), ("QR", 5), ("QS", 5)]
    labels = list("ABTQRS")
    clients = [set(membership) for membership, n in groups for _ in range(n)]
    assert len(clients) == 71
    replies = dict(zip(labels, "BSRSSR"))

    def payoff(action, terminal):
        value = F(0)
        for memberships in clients:
            if action in memberships:
                value += F(1, sum(a in memberships for a in terminal))
        return value

    table = [[payoff(b, (a, b)) for b in labels] for a in labels]
    root = [payoff(a, (a, replies[a])) for a in labels]
    assert root == [F(16)]*6
    counts = comparison_counts(table, root, [labels.index(replies[a]) for a in labels])
    pairs = omission_pair_table(labels, clients, {"A", "B"})
    assert pairs["actual_coverage"] == 35 and pairs["OPT2"] == 38
    assert pairs["optimal_pairs"] == [
        {"pair": ["T", "Q"], "union_size": 38, "omitted_from_actual": 36}]
    return {"status": "PASS", "scope": "Later explicit 71-client k=3 comparison only; no source done implied.",
            "unit_customers": 71, **counts, **pairs,
            "all_six_true_first_payoffs": list(map(str, root)),
            "actual_only_outside_optimal": 33, "net_OPT_minus_W": 3}


def main():
    out = BASE/"replay"
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BASE/"source-manifest.json").read_text())
    for rows in manifest.values():
        for row in rows:
            raw = (BASE/row["preserved_relative_path"]).read_bytes()
            assert len(raw) == row["size"]
            assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    repo = next(p for p in BASE.parents if (p/"work.py").is_file())
    frozen_checks = {}
    for script, outputs, name in [
        ("audit_protected_root.py", ["protected_root_audit.json"], "author"),
        ("verify_protected_counterexample.py",
         ["protected_counterexample_independent_audit.json",
          "protected_zero_root_independent_audit.json"], "independent"),
    ]:
        with tempfile.TemporaryDirectory(prefix="protected-root-replay-",
                                         dir=repo/"cleanup/workspaces/Boss2") as tmp:
            stage = Path(tmp)
            shutil.copy2(BASE/"original"/script, stage/script)
            result = subprocess.run([sys.executable, str(stage/script)],
                                    capture_output=True, text=True, check=True)
            # Human-readable console copy has one EOF newline; frozen JSON
            # files below are compared and saved with their exact bytes.
            (out/(name+"-stdout.txt")).write_text(result.stdout.rstrip("\n")+"\n")
            for filename in outputs:
                frozen = (BASE/"original"/filename).read_bytes()
                replay = (stage/filename).read_bytes()
                assert json.loads(replay) == json.loads(frozen), filename
                assert replay == frozen, filename
                (out/filename).write_bytes(replay)
                frozen_checks[filename] = {
                    "all_fields_equal": True, "byte_identical": True,
                    "sha256": hashlib.sha256(replay).hexdigest()}
    zero = json.loads((out/"protected_root_audit.json").read_text())
    independent = json.loads((out/"protected_zero_root_independent_audit.json").read_text())
    labels = zero["labels"]
    table = [[zero["second_payoff_matrix"][a][b] for b in labels] for a in labels]
    assert table == independent["last_payoff_table"]
    reply = [labels.index(zero["reply"][a]) for a in labels]
    first = [zero["first_deviation_payoffs"][a] for a in labels]
    counts = comparison_counts(table, first, reply)
    clients = [set(membership) for membership, n in zero["groups"] for _ in range(n)]
    pairs = omission_pair_table(labels, clients, {"A", "B"})
    assert pairs["optimal_pairs"] == [
        {"pair": ["B", "T"], "union_size": 14, "omitted_from_actual": 7},
        {"pair": ["B", "Q"], "union_size": 14, "omitted_from_actual": 7},
        {"pair": ["T", "Q"], "union_size": 14, "omitted_from_actual": 14}]
    write(out/"zero-root-complete-pairs.json", pairs)
    old = json.loads((out/"protected_counterexample_independent_audit.json").read_text())
    old_counts = comparison_counts(old["last_player_payoff_table"],
                                   old["first_player_deviation_values"], old["replies"])
    assert sum(x["unit_customers"] for x in old["rows"]) == 31
    assert old["labels"] == list("ABTQRSE") and old["legal_background_topic"] == "E"
    later = verify_later_unique_case()
    write(out/"later-unique-optimum-comparison.json", later)
    summary = {
        "status": "PASS", "frozen_outputs": frozen_checks,
        "zero_root_27_clients": counts,
        "legal_E_background_31_clients": old_counts,
        "zero_root_OPT": 14, "zero_root_W": 13,
        "zero_root_optimal_omissions": [7, 7, 14],
        "protected_price_at_6": 2, "actual_utility_difference": 1,
        "earlier_existential_bound_not_refuted_by_27_case": True,
        "later_71_case_refutes_existential_bound": True,
        "later_71_source_disposition_in_this_batch": False,
        "GLOBAL_status": "The 27-client empty-root case satisfies GLOBAL; the separately completed 52-client actual-prefix family refutes universal GLOBAL.",
        "implementation_distinction": "Author explicitly expands unit clients; independent code sums exact multiplicity times unit share over 10 types.",
        "not_performed": ["No claim of external peer review or minimality.",
                          "No random LP or chain-search rerun.",
                          "No claim that legal E prefix is on a full root equilibrium path."],
    }
    write(out/"semantic-reconciliation.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
