#!/usr/bin/env python3
"""Reproduce the finite Fraction checks cited in compiler_review.md.

Scope is deliberately fixed: m=5 prefix policies for j=1,...,4; the existing
shared-terminal-rent m=5 case; one Beta customer with b=2 and multiplicities
(1,2,4). This is implementation replay and algebra checking, not a general
proof or an instance search. Existing audit scripts are loaded with runpy's
non-main entry point so their output-writing main blocks do not execute.
"""

from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path
import runpy
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").is_file()
            and (p / "customer_attraction").is_dir())
PREFIX_DIR = REPO / "research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack"
SHARED_DIR = REPO / "research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible_continue"
PREFIX_SCRIPT = PREFIX_DIR / "audit_prefix_bank.py"
SHARED_SCRIPT = SHARED_DIR / "audit_shared_terminal_rent_compiler.py"
RECEIPT = HERE / "compiler_relations_receipt.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    guarded = (
        PREFIX_SCRIPT,
        PREFIX_DIR / "audit_prefix_bank.json",
        SHARED_SCRIPT,
        SHARED_DIR / "shared_terminal_rent_compiler_audit.json",
    )
    before = {str(p.relative_to(REPO)): digest(p) for p in guarded}
    # Default run_name is '<run_path>', so neither source __main__ writes files.
    prefix = runpy.run_path(str(PREFIX_SCRIPT))
    shared = runpy.run_path(str(SHARED_SCRIPT))
    m = 5

    prefix_rows = []
    for j in range(1, 5):
        d = m - j
        w = 2 * j + d
        opt = 2 * j + d + d - 1
        assert w == m + j
        assert opt == 2 * m - 1
        assert 2 * w - opt == 2 * j + 1
        row = prefix["audit"](m, j)
        prefix_rows.append({
            "m": m, "j": j, "d": d,
            "insurance_W_per_s": w,
            "insurance_OPT_per_s": opt,
            "half_dilution_per_s": 2 * w - opt,
            "nodes_checked": row["nodes_checked"],
            "all_action_comparisons": row["all_action_comparisons"],
        })
    assert sum(r["all_action_comparisons"] for r in prefix_rows) == 1020

    shared_w = m * m - 1
    shared_opt = (m - 1) * (2 * m - 1)
    shared_cost = 2 * shared_w - shared_opt
    assert (shared_w, shared_opt, shared_cost) == (24, 36, 12)
    shared_case = shared["case"](m)
    selected = [
        "original_required_g", "original_selected_g", "common_scale",
        "integer_g", "full_ordered_decision_histories",
        "exact_action_comparisons", "minimum_slack", "W_old", "OPT_old",
        "W_new", "OPT_new", "half_dilution",
    ]
    shared_replay = {key: shared_case[key] for key in selected}
    assert shared_replay["full_ordered_decision_histories"] == 11111
    assert shared_replay["exact_action_comparisons"] == 111110
    assert shared_replay["minimum_slack"] == "0"
    assert (shared_replay["W_old"], shared_replay["OPT_old"],
            shared_replay["W_new"], shared_replay["OPT_new"]) == (8, 8, 32, 44)

    floor = Q(4 * (m - 1), m * (2 * m - 1))
    assert floor == Q(16, 45)
    exact_m = {
        "m": m,
        "existing_general_floor_OPT_coefficient": str(floor),
        "OPT_over_W_plus_R_from_this_floor": str(1 / floor),
        "candidate_MP_gap_coefficient_for_j4_if_proved": 8,
        "prefix_compiler_gap_cost_coefficient_for_j4": 9,
        "MP_status": "unproved; conditional coefficient is not an established bound",
    }

    # Direct marginal Beta interest-pattern enumeration, without a SPE solver.
    b = 2
    multiplicities = (1, 2, 4)
    d = len(multiplicities)
    u = [Q(0)] * d
    total_weight = Q(0)
    for bits in product((0, 1), repeat=d):
        k = sum(bits)
        weight = Q(b * factorial(k) * factorial(b + d - k - 1),
                   factorial(b + d))
        total_weight += weight
        load = sum(n * bit for n, bit in zip(multiplicities, bits))
        if load:
            for i, bit in enumerate(bits):
                u[i] += weight * Q(bit, load)
    assert total_weight == 1
    u_background = Q(1, b + sum(multiplicities))
    clone_w = sum(n * val for n, val in zip(multiplicities, u))
    projected_profit = Q(sum(multiplicities), b + sum(multiplicities))
    debt = projected_profit - clone_w
    singleton_gain = u[0] - u_background
    repeat_debt = sum(multiplicities[i] * (u_background - u[i])
                      for i in (1, 2))
    assert u == [Q(236, 1575), Q(41, 420), Q(803, 12600)]
    assert debt == Q(8, 45)
    assert singleton_gain == Q(61, 1575)
    assert repeat_debt == debt + singleton_gain == Q(341, 1575)
    tails = []
    for t in range(1, 5):
        clone_sum = sum(n * val for n, val in zip(multiplicities, u) if n >= t)
        background_sum = sum(n * u_background for n in multiplicities if n >= t)
        assert clone_sum <= background_sum
        tails.append({"threshold": t, "clone_sum": str(clone_sum),
                      "background_sum": str(background_sum), "passed": True})
    beta = {
        "background_load": b, "multiplicities": list(multiplicities),
        "interest_patterns_enumerated": 8, "total_weight": str(total_weight),
        "clone_per_user_payoffs": list(map(str, u)),
        "background_per_user_payoff": str(u_background),
        "D": str(debt), "G": str(singleton_gain),
        "repeat_debt": str(repeat_debt), "upper_tails": tails,
    }

    delta = Q(1, 6)
    scale = delta.denominator
    prefix_blocks = [2 * delta * scale] * (m - 1) + [delta * scale]
    shared_blocks = [m * (m - 1) * delta * scale] + [(m - 1) * delta * scale] * (m - 1)
    assert prefix_blocks == [Q(2)] * 4 + [Q(1)]
    assert shared_blocks == [Q(20)] + [Q(4)] * 4
    scaling = {
        "m": m, "Delta": str(delta), "common_scale_L": scale,
        "old_customer_replication_factor": scale,
        "prefix_integer_blocks": [int(v) for v in prefix_blocks],
        "shared_integer_blocks": [int(v) for v in shared_blocks],
        "prefix_half_dilution_raw": str((2 * m - 1) * delta * scale),
        "shared_half_dilution_raw": str(3 * (m - 1) * delta * scale),
    }

    after = {str(p.relative_to(REPO)): digest(p) for p in guarded}
    assert before == after, "Existing source scripts or their receipts changed"
    result = {
        "status": "finite_exact_replay_passed_not_general_proof",
        "scope": "m5 prefix j1..4; existing shared m5 case; Beta b2 multiplicities(1,2,4); no search or scope expansion",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": digest(Path(__file__).resolve()),
        "source_and_existing_receipt_sha256_before": before,
        "source_and_existing_receipt_sha256_after": after,
        "existing_source_outputs_unchanged": True,
        "prefix_m5": prefix_rows,
        "prefix_total_comparisons": 1020,
        "shared_m5_insurance_coefficients": {
            "W_per_g": shared_w, "OPT_per_g": shared_opt,
            "half_dilution_per_g": shared_cost,
        },
        "shared_m5_replay": shared_replay,
        "exact_M_substitution": exact_m,
        "Beta_direct_subset_check": beta,
        "rational_scaling_example": scaling,
    }
    RECEIPT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "prefix_comparisons": 1020,
        "shared_ordered_histories": shared_replay["full_ordered_decision_histories"],
        "shared_comparisons": shared_replay["exact_action_comparisons"],
        "beta_interest_patterns": 8,
        "existing_source_outputs_unchanged": True,
        "receipt": str(RECEIPT),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
