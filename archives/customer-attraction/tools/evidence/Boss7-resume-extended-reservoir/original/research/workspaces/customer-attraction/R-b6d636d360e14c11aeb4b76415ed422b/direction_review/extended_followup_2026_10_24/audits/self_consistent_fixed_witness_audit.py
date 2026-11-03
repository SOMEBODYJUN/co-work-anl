"""Definition-level Fraction audit of the two named pooled-load witnesses.

No discovery, optimizer, policy scan, parameter scan, or imported author audit.
Only the already specified 16-client pure-SC witness and 635-client all-p
witness are replayed.  The PB block checks are scalar consequences of its
previously proved complete-history strategy, not a re-proof of that strategy.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "AGENTS.md").is_file() and (p / "work.py").is_file())
ROUND = ROOT / ("research/workspaces/customer-attraction/"
                "R-d3981c0168644971803a9c3380ed687c/round4_general")
RAW635 = ROUND / "security/pooled_mean_background_raw.json"
COUNTS16 = {2: 1, 14: 1, 16: 1, 18: 1, 29: 3, 38: 1,
            41: 1, 43: 2, 45: 2, 47: 1, 49: 1, 52: 1}


def action(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    assert len(history) == 2
    group = range(3) if history[1] < 3 else range(3, 6)
    return min(a for a in group if a not in history)


def leaf(history):
    while len(history) < 3:
        history = (*history, action(history))
    return history


def audit_named_witness(counts, raw_policy=None):
    # Every repeated mask represents a distinct unit customer.
    units = [mask for mask, count in counts.items() for _ in range(count)]
    histories = [h for depth in range(3)
                 for h in product(range(6), repeat=depth)]
    assert len(histories) == 43
    if raw_policy is not None:
        policy = {tuple(row["history"]): row["action"] for row in raw_policy}
        assert policy == {h: action(h) for h in histories}

    def utility(terminal, position):
        return sum((F(1, sum(bool(mask & (1 << a)) for a in terminal))
                    for mask in units if mask & (1 << terminal[position])), F())

    ic_gaps = []
    for history in histories:
        position = len(history)
        prescribed = utility(leaf(history), position)
        for a in range(6):
            ic_gaps.append(prescribed - utility(leaf((*history, a)), position))
    assert len(ic_gaps) == 258 and min(ic_gaps) >= 0

    actual = leaf(())
    welfare = sum(any(mask & (1 << a) for a in actual) for mask in units)
    optimum = max(sum(any(mask & (1 << a) for a in terminal) for mask in units)
                  for terminal in product(range(6), repeat=3))
    utilities = [utility(actual, i) for i in range(3)]
    assert sum(utilities) == welfare
    competitors = {}
    table, topic_count_rows = [], []
    for a in range(6):
        branch_leaves = [leaf((*actual[:i], a)) for i in range(3)]
        competitors[a] = [z[:i] + z[i+1:] for i, z in enumerate(branch_leaves)]
        row = [sum(z.count(t) for z in competitors[a]) for t in range(6)]
        assert sum(row) == 6
        topic_count_rows.append(row)
        mu = [sum(F(sum(bool(mask & (1 << b)) for b in z), 3)
                  for z in competitors[a]) for mask in units]
        query_values = [sum((1 / (1 + mu[j]) for j, mask in enumerate(units)
                             if mask & (1 << t)), F()) for t in range(6)]
        table.append(query_values)
        real_payoff_sum = sum(utility(z, i) for i, z in enumerate(branch_leaves))
        assert 3 * query_values[a] <= real_payoff_sum <= welfare

    # The one prescribed mixture from the prior all-p attack, not a p scan.
    p = {2: F(1, 2), 5: F(1, 2)}
    atoms = [(prob / 3, a, z) for a, prob in p.items() for z in competitors[a]]
    mu = [sum(w * sum(bool(mask & (1 << b)) for b in z)
              for w, a, z in atoms) for mask in units]
    g = [sum((1 / (1 + mu[j]) for j, mask in enumerate(units)
              if mask & (1 << a)), F()) for a in range(6)]
    G = sum(prob * g[a] for a, prob in p.items())
    D = sum(w * sum((F(1, 1 + sum(bool(mask & (1 << b)) for b in z))
                    for mask in units if mask & (1 << a)), F())
            for w, a, z in atoms)
    weighted_covariance = F()
    weighted_curvature = F()
    for j, mask in enumerate(units):
        weighted_covariance += sum(
            w * bool(mask & (1 << a)) *
            (sum(bool(mask & (1 << b)) for b in z) - mu[j])
            for w, a, z in atoms) / (1 + mu[j])**2
        weighted_curvature += sum(
            w * bool(mask & (1 << a)) *
            (sum(bool(mask & (1 << b)) for b in z) - mu[j])**2 /
            (1 + sum(bool(mask & (1 << b)) for b in z))
            for w, a, z in atoms) / (1 + mu[j])**2
    assert D <= F(welfare, 3)
    assert D - G == -weighted_covariance + weighted_curvature

    return {
        "unit_clients": len(units), "ordered_histories": 43,
        "all_IC_comparisons": 258, "minimum_IC_gap": str(min(ic_gaps)),
        "actual_path": list(actual), "utilities": list(map(str, utilities)),
        "welfare": welfare, "OPT_3": optimum,
        "pooled_topic_count_numerators_divide_by_6": topic_count_rows,
        "g_at_pure_queries_rows_A_columns_T": [list(map(str, row)) for row in table],
        "best_response_sets_at_pure_queries": [
            [t for t, value in enumerate(row) if value == max(row)] for row in table],
        "maximum_of_all_pure_query_values": str(max(map(max, table))),
        "fixed_p": ["0", "0", "1/2", "0", "0", "1/2"],
        "g_at_fixed_p": list(map(str, g)), "G_at_fixed_p": str(G),
        "three_G_minus_welfare": str(3 * G - welfare),
        "g5_minus_g2_at_fixed_p": str(g[5] - g[2]),
        "D_real_IC_paid_average": str(D),
        "welfare_div_3_minus_D": str(F(welfare, 3) - D),
        "weighted_covariance_minus_weighted_curvature":
            str(weighted_covariance - weighted_curvature),
    }


def audit_pb_scalars():
    r, Q, H, M = 2475, 2063, 100000, 10**9

    def f(c):
        return F(11) / (M + c) + F(1) / (M + c + 1)

    def g(c):
        return F(H * 12) / (H * M + c)

    L = F(3 * (r - 1), Q)
    delta = 20 * (f(1 + L) + 2 * g(1))
    u = 60 * f(3)
    HR = (F(11) / (M + 1 + L)**2 + F(1) / (M + 2 + L)**2) / Q
    HD = F(H * 12) / (H * M + 1)**2
    checks = {
        "one_real_two_dummy_query_best": f(1 + L) < g(1),
        "three_real_gradient_best": HR > HD,
        "query_beats_singletons": delta > F(1, M + 1),
        "gradient_beats_real_singletons": 60 * HR > F(1, Q) / (M + 1 + L)**2,
        "gradient_beats_dummy_singletons": 60 * HR > F(1) / (H * M + 1)**2,
        "delta_exceeds_first_three_profits": delta > u,
    }
    load_rows = []
    for j in (1, 2, 3):
        theta = 3 * (L - j) / (r - j - 1)
        hot = theta / 3
        outside = (3 - theta) / (Q - 3)
        checks[f"theta_{j}_valid"] = 0 < theta < 1
        checks[f"hot_load_{j}_preserved"] = j + (r - j - 1) * hot == L
        checks[f"outside_load_{j}_preserved"] = (r - j - 1) * outside == L
        load_rows.append({"j": j, "theta": str(theta),
                          "hot_total_load": str(j + (r - j - 1) * hot),
                          "outside_total_load": str((r - j - 1) * outside)})
    assert all(checks.values())
    # On its specified actual tail: 3 hot blocks at load 3, 1648 outside
    # blocks at load 1, 412 outside blocks at load 2, 2 dummy blocks at 2472.
    actual_tail_sum = 20 * (9 * f(3) + 1648 * f(1) + 824 * f(2) + 4944 * g(2472))
    assert actual_tail_sum > r * delta
    return {
        "scope": "Scalar/KKT/load corollary; complete SPE inherited from named old PB proof",
        "checks": checks, "L": str(L), "delta_minus_u": str(delta - u),
        "plateau_mixtures": load_rows,
        "actual_continuation_aggregate_minus_r_delta": str(actual_tail_sum - r * delta),
    }


def main():
    raw_bytes = RAW635.read_bytes()
    raw = json.loads(raw_bytes)
    report16 = audit_named_witness(COUNTS16)
    report635 = audit_named_witness(
        {int(k): v for k, v in raw["customer_mask_multiplicities"].items()}, raw["policy"])
    assert report16["best_response_sets_at_pure_queries"] == [[5], [5], [5], [2], [2], [2]]
    assert report16["maximum_of_all_pure_query_values"] == "107/24"
    assert report635["g_at_pure_queries_rows_A_columns_T"][1] == [
        "36111/280", "5291/35", "35067/280", "31263/280", "4554/35", "5403/40"]
    assert report635["best_response_sets_at_pure_queries"][1] == [1]
    assert F(5291, 35) < F(report635["welfare"], 3)
    assert report635["three_G_minus_welfare"] == "40617/340340"
    assert report635["g5_minus_g2_at_fixed_p"] == "421947/170170"
    report = {
        "scope": "Only named fixed witnesses; no search; no general welfare theorem or counterexample",
        "input_sources": {
            "16_client_counts_and_policy": str((ROUND / "direct/self_consistent_pure_shortcut.md").relative_to(ROOT)),
            "635_client_raw_input": str(RAW635.relative_to(ROOT)),
            "635_raw_sha256": sha256(raw_bytes).hexdigest(),
            "PB_parameters_and_strategy": "research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md",
            "PB_fractional_corollary": str((ROUND / "security/pb_fractional_saddle_plateau.md").relative_to(ROOT)),
        },
        "fixed_16": report16, "fixed_635": report635, "PB": audit_pb_scalars(),
        "635_paid_pure_SC": {"label": 1, "g1": "5291/35", "W_over_3": "154",
                              "W_minus_three_g1": "297/35"},
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "output": str(output.relative_to(ROOT)),
                      "635_paid_pure_SC": report["635_paid_pure_SC"]}, indent=2))


if __name__ == "__main__":
    main()
