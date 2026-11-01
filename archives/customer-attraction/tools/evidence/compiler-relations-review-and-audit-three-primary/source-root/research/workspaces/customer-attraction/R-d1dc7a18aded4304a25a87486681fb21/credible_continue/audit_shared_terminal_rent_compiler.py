"""Finite exact audit of the all-depth terminal-rent compiler candidate.

Uses explicit unit-customer sets and Fraction, without repository model/solver.
Different first-exit branches retain different preselected tie rules. Full
ordered joint histories and all simultaneous coordinate deviations are checked.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
from math import lcm
import json


def utilities(z, themes):
    load = {}
    for a in z:
        for x in themes[a]:
            load[x] = load.get(x, 0) + 1
    return [sum((F(1, load[x]) for x in themes[a]), F(0)) for a in z], len(load)


def case(m):
    original_themes = [frozenset(range(2)), frozenset(range(2, 4))]
    planned = (0,) * (m - 1) + (1,)

    def old_bi(themes):
        @lru_cache(None)
        def outcome(h, seed):
            if len(h) == m:
                return h
            candidates = [outcome(h + (a,), seed) for a in range(len(themes))]
            vals = [utilities(z, themes)[0][len(h)] for z in candidates]
            best = max(vals)
            tied = [a for a, v in enumerate(vals) if v == best]
            chosen = max(tied) if seed else min(tied)
            return candidates[chosen]
        return outcome

    orig_bi = old_bi(original_themes)
    orig_u, _ = utilities(planned, original_themes)
    defects = []
    for i in range(m - 1):
        for a in range(2):
            seed = (i + a + 1) % 2
            d = utilities(orig_bi(planned[:i] + (a,), seed), original_themes)[0][i]
            defects.append((i, a, d - orig_u[i]))
    required = max([F(0)] + [v for _, _, v in defects])
    g_orig = max(required, F(1, m))
    scale = g_orig.denominator
    g = int(g_orig * scale)
    old = [frozenset(range(2 * scale)), frozenset(range(2 * scale, 4 * scale))]
    bi = old_bi(old)
    next_customer = 4 * scale
    insurance = []
    for size in [m * (m - 1) * g] + [(m - 1) * g] * (m - 1):
        insurance.append(frozenset(range(next_customer, next_customer + size)))
        next_customer += size
    labels = list(product(range(2), range(m)))
    index = {v: j for j, v in enumerate(labels)}
    themes = [old[a] | insurance[b] for a, b in labels]
    planned_joint = tuple(index[(a, 0 if i < m - 1 else 1)] for i, a in enumerate(planned))

    @lru_cache(None)
    def choice(h):
        mismatch = next((i for i, a in enumerate(h) if a != planned_joint[i]), None)
        if mismatch is None:
            return planned_joint[len(h)]
        old_a = labels[h[mismatch]][0]
        seed = (mismatch + old_a + 1) % 2
        old_h = tuple(labels[j][0] for j in h)
        old_chosen = bi(old_h, seed)[len(h)]
        return index[(old_chosen, 0)]

    @lru_cache(None)
    def leaf(h):
        if len(h) == m:
            return h
        return leaf(h + (choice(h),))

    @lru_cache(None)
    def pay(z):
        return utilities(z, themes)[0]

    histories = checks = 0
    min_slack = None
    for depth in range(m):
        for h in product(range(len(labels)), repeat=depth):
            histories += 1
            actual = pay(leaf(h))[depth]
            for alt in range(len(labels)):
                altpay = pay(leaf(h + (alt,)))[depth]
                slack = actual - altpay
                assert slack >= 0, (m, h, alt, slack)
                checks += 1
                min_slack = slack if min_slack is None else min(min_slack, slack)

    actual_leaf = leaf(())
    assert actual_leaf == planned_joint
    new_u, new_w = utilities(actual_leaf, themes)
    old_u, old_w = utilities(planned, old)
    old_opt = max(len(frozenset().union(*(old[a] for a in chosen)))
                  for r in range(1, min(m, len(old)) + 1)
                  for chosen in combinations(range(len(old)), r))
    new_opt = max(len(frozenset().union(*(themes[a] for a in chosen)))
                  for r in range(1, min(m, len(themes)) + 1)
                  for chosen in combinations(range(len(themes)), r))
    assert new_w == old_w + (m * m - 1) * g
    assert new_opt == old_opt + (m - 1) * (2 * m - 1) * g
    assert new_opt - 2 * new_w == old_opt - 2 * old_w - 3 * (m - 1) * g
    # Include insurance-only root exit; it deliberately swaps to a genuine
    # selected child-SPE, potentially raising the root's old-coordinate payoff.
    only_ins_exit = index[(planned[0], 1)]
    insurance_only_leaf = leaf((only_ins_exit,))
    old_exit_z = tuple(labels[j][0] for j in insurance_only_leaf)
    old_exit_u = utilities(old_exit_z, old)[0][0]
    return {
        "m": m, "old_planned_path": planned, "original_required_g": str(required),
        "original_selected_g": str(g_orig), "common_scale": scale, "integer_g": g,
        "old_actual_utilities": list(map(str, old_u)),
        "exit_defects_before_scale": [{"position_zero_based": i, "old_action": a, "difference": str(v)} for i, a, v in defects],
        "insurance_only_root_old_gain": str(old_exit_u - old_u[0]),
        "insurance_only_joint_gain": str(pay(insurance_only_leaf)[0] - new_u[0]),
        "full_ordered_decision_histories": histories, "exact_action_comparisons": checks,
        "minimum_slack": str(min_slack), "W_old": old_w, "OPT_old": old_opt,
        "W_new": new_w, "OPT_new": new_opt,
        "half_dilution": 3 * (m - 1) * g,
        "joint_themes": [sorted(x) for x in themes],
    }


if __name__ == "__main__":
    results = [case(m) for m in (2, 3, 4, 5)]
    report = {"status": "finite_exact_audit_passed_not_general_proof", "cases": results,
              "total_comparisons": sum(r["exact_action_comparisons"] for r in results)}
    Path(__file__).with_name("shared_terminal_rent_compiler_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(results), "comparisons": report["total_comparisons"]}))
