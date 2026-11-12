#!/usr/bin/env python3
"""Independent original-budget, weak-state and formal-column verification."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import os

P = Path(__file__).resolve().parent
INPUT = Path(os.environ.get("ROOT270_FROZEN_INPUT_ROOT", "/workspace/scratch/b0fef5ec503f"))
PREV = INPUT / "root270_replycaps_iter2_stage"
TYPES = list(product((0, 1), repeat=7))
TAILS = list(product((0, 1), repeat=3))
PTAILS = list(product((0, 1), repeat=2))


def enc(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): enc(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [enc(v) for v in value]
    return value


def read(name):
    return json.loads((P / name).read_text())


def save(name, value):
    (P / name).write_text(json.dumps(enc(value), ensure_ascii=False, indent=2) + "\n")


def sources():
    pins = read("source_pins.json")
    count = 0
    for item in pins["sources"]:
        path = INPUT / item["stage"] / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    for stage, expected in pins["frozen_manifest_sha256"].items():
        path = INPUT / stage
        assert hashlib.sha256((path / "freeze_manifest.json").read_bytes()).hexdigest() == expected
        for item in json.loads((path / "freeze_manifest.json").read_text())["artifacts"]:
            assert hashlib.sha256((path / item["path"]).read_bytes()).hexdigest() == item["sha256"]
            count += 1
    return count


def cost_from_original_payments(h, q, tail):
    c, b2, b3, b4, b5, b6, o = h
    r, y, z = tail
    prefix2 = c + b2
    old4den = c + b2 + b3 + 3
    old6den = c + b2 + b3 + b4 + b5 + 1
    pairden = c + b2 + q + r + 1
    new6den = pairden + y
    source = 126000 * Q(q, prefix2 + 1 + r + y + z)
    old4 = [weight * Q(bit, old4den) for weight, bit in zip((43, 31218, 34458), tail)]
    old6 = [1654 * Q(bit, old6den) for bit in tail]
    newlast = Q(z, new6den) - Q(o, 6 * new6den)
    newpair = (Q(y, pairden + z) + Q(z, pairden + y)
               + Q(y, pairden * (pairden + 1)) - Q(o, 3 * pairden))
    terms = [source] + old4 + old6 + [-5400 * newlast, -7740 * newpair]
    assert len(terms) == 9
    return sum(terms, Q(0)) + Q(215, 3) * r


def p25_from_payments(h, tail):
    prefix = sum(h[:3])
    forced = h[5]
    middle, last = tail
    denominator = prefix + forced + middle + last
    forced_profit = Q(forced, denominator) if denominator else Q(0)
    last_profit = Q(last, denominator) if denominator else Q(0)
    middle_size = Q(middle, 2)
    last_size = Q(last)
    last_query = Q(h[6], 6 * (prefix + forced + middle + 1))
    return 25 * forced_profit - last_profit + middle_size + last_size + last_query


def literal_rows(h, cost, pcost):
    total = sum(h[:6])
    profit = [Q(bit, total) if total else Q(0) for bit in h[:6]]
    prefix4 = sum(h[:4])
    out = [-profit[0]]
    out.extend(-Q(bit) for bit in h[1:6])
    out.append(profit[5] - Q(h[6], 6 * (sum(h[:5]) + 1)))
    out.append(profit[4] + profit[5] + Q(h[4], (prefix4 + 1) * (prefix4 + 2))
               - Q(h[6], 3 * (prefix4 + 1)))
    out.append(126000 * profit[2] + (43 + 31218 + 34458) * profit[3]
               + (3 * 1654) * profit[5] - cost)
    out.append(25 * profit[3] - pcost)
    return out


def coefficients_for_basis(rows, masses):
    K = sum((Q(mass * TYPES[h][0]) for h, mass in masses.items()), Q(0))
    sizes = [sum((Q(mass * TYPES[h][j]) for h, mass in masses.items()), Q(0)) for j in range(7)]
    profit = [sum((Q(mass * TYPES[h][j], sum(TYPES[h][:6]))
                   for h, mass in masses.items() if sum(TYPES[h][:6])), Q(0)) for j in range(6)]
    cap = [K - sizes[j] for j in range(1, 6)]
    remaining = [sum((mass * rows[h][j] for h, mass in masses.items()), Q(0))
                 + K * (Q(215, 3) if j == 8 else Q(3, 2) if j == 9 else Q(0))
                 for j in range(6, 10)]
    return K, sizes, profit, cap + remaining


def main():
    old_count = sources()
    baseline = json.loads((PREV / "parameter_family.json").read_text())
    b = Q(37482242363557, 1875285984658080)
    eta = Q(1087978231314917, 84387869309613600)
    scale = Q(67510295447690880)
    original = list(map(Q, [67510295447690880, 622403086173831, 3736484626202371,
                           3694404008494650, 3606523426712610, 3551800449688044,
                           1712829042623520, 2292281651099340, 24602518440, 61096128288912]))
    mixing = Q(146931707350, 112593658798021)
    root1 = Q(1767977474054257, 16877573861922720)
    w2 = [Q(1)] + [(1 - mixing) * original[j] / scale + mixing * b for j in range(1, 6)]
    w2 += [(1 - mixing) * original[j] / scale for j in range(6, 10)]
    bc2 = (1 - mixing) * Q(22376932866410102) / scale + mixing * (Q(1, 5) + 3 * b)
    a2 = root1 + mixing * (Q(1, 5) - root1 - 2 * b)
    assert w2 == list(map(Q, baseline["normalized_weights_at_endpoint"]))
    assert a2 == Q(baseline["new_K_coefficient"])
    zmax = Q(64038719369580574756325, 56305416081414054191857509248)
    ymax = Q(214288412699877216115223075, 102518086330234639169824559963296)
    dwz = [Q(0)] * 10
    for j, value in {4: -Q(4, 3), 5: Q(1), 6: Q(2), 7: -Q(1)}.items():
        dwz[j] = value
    dwy = [Q(0)] * 10
    for j, value in {3: Q(299, 12), 4: -Q(17, 12), 5: -Q(169, 18),
                     6: Q(1), 7: -Q(1), 9: Q(1)}.items():
        dwy[j] = value
    kcol = [Q(0)] + [Q(1)] * 5 + [Q(0), Q(0), Q(215, 3), Q(3, 2)]
    gainz = Q(4, 5) - sum(d * k for d, k in zip(dwz, kcol))
    gainy = Q(721, 45) - sum(d * k for d, k in zip(dwy, kcol))
    assert gainz == Q(17, 15) and gainy == Q(37, 90)
    w3 = [w + zmax * d for w, d in zip(w2, dwz)]
    w4 = [w + ymax * d for w, d in zip(w3, dwy)]
    bc3 = bc2 + Q(4, 5) * zmax
    bc4 = bc3 + Q(721, 45) * ymax
    a3 = a2 + gainz * zmax
    a4 = a3 + gainy * ymax
    assert all(w > 0 for w in w2 + w3 + w4)
    stored = read("true_state_tables.json")["all128_types"]
    previous = json.loads((PREV / "true_state_tables.json").read_text())["all128_types"]
    cert = read("all128_direction_certificate.json")["all128"]
    families = read("parameter_families.json")
    allrows = []
    rhos = [[], [], []]
    slopes = [[], []]
    scalar_checks = 0
    menu_checks = 0
    tail_checks = 0
    p25_checks = 0
    minimum_moment_slope = None
    for code, h in enumerate(TYPES):
        qlow = []
        weak = []
        for q in (0, 1):
            costs = [cost_from_original_payments(h, q, tail) for tail in TAILS]
            assert costs == list(map(Q, stored[code]["C30_all_costs_by_q"][q]))
            assert costs == list(map(Q, previous[code]["C30_all_costs_by_q"][q]))
            low = min(costs)
            qlow.append(low)
            weak.append([list(tail) for tail, val in zip(TAILS, costs) if val == low])
            tail_checks += 8
        assert weak == stored[code]["C30_all_attaining_tails"]
        delta = qlow[1] - qlow[0]
        assert delta > 0
        minimum_moment_slope = delta if minimum_moment_slope is None else min(minimum_moment_slope, delta)
        m = qlow[0] + Q(h[6], 6) * delta
        assert m == Q(stored[code]["C30_CAP_m"])
        for menu in product((0, 1), repeat=6):
            d = sum(menu)
            if int(d > 0) != h[6]:
                continue
            literal_average = sum((qlow[q] for q in menu), Q(0)) / 6
            assert literal_average - m == Q(d - h[6], 6) * delta >= 0
            assert (literal_average == m) == (d == h[6])
            menu_checks += 1
        pvalues = [p25_from_payments(h, tail) for tail in PTAILS]
        pm = min(pvalues)
        assert pvalues == list(map(Q, stored[code]["P25_all_costs"]))
        pweak = [list(tail) for tail, val in zip(PTAILS, pvalues) if val == pm]
        assert pweak == stored[code]["P25_all_attaining_tails"]
        assert all(tail[0] == h[5] for tail in pweak)
        p25_checks += 4
        row = literal_rows(h, m, pm)
        assert row == list(map(Q, stored[code]["ten_real_budget_customer_coefficients"]))
        allrows.append(row)
        rho_values = [
            -sum(w * v for w, v in zip(wt, row)) - bc * h[0] - b * h[6] - eta * h[0] * (1 - h[6])
            for wt, bc in ((w2, bc2), (w3, bc3), (w4, bc4))
        ]
        for j, value in enumerate(rho_values):
            assert value >= 0 and value == Q(cert[code]["rho" + str(j + 2)])
            rhos[j].append(value)
        dirz = -sum(d * v for d, v in zip(dwz, row)) - Q(4, 5) * h[0]
        diry = -sum(d * v for d, v in zip(dwy, row)) - Q(721, 45) * h[0]
        assert dirz == row[7] - 2 * row[6] + h[5] - Q(4, 3) * h[4] - Q(4, 5) * h[0]
        assert diry == (row[7] - row[6] - row[9] + Q(299, 12) * h[3]
                        - Q(17, 12) * h[4] - Q(169, 18) * h[5] - Q(721, 45) * h[0])
        assert dirz == Q(cert[code]["D2"]) and diry == Q(cert[code]["D3"])
        assert rho_values[1] == rho_values[0] + zmax * dirz
        assert rho_values[2] == rho_values[1] + ymax * diry
        slopes[0].append(dirz)
        slopes[1].append(diry)
        for j, (weights, dweights, bc, dbc, residue, dr) in enumerate([
            (w2, dwz, bc2, Q(4, 5), rho_values[0], dirz),
            (w3, dwy, bc3, Q(721, 45), rho_values[1], diry),
        ]):
            want = [-eta * h[0] * (1 - h[6]), Q(0)]
            got = [sum(w * v for w, v in zip(weights, row)) + residue + bc * h[0] + b * h[6],
                   sum(w * v for w, v in zip(dweights, row)) + dr + dbc * h[0]]
            assert want == got
            name = ["ROOT2_to_ROOT3", "ROOT3_to_ROOT4"][j]
            saved = read("all131_affine_column_identities.json")["families"][name][code]
            assert list(map(Q, saved["left_constant_and_slope"])) == want
            assert list(map(Q, saved["right_constant_and_slope"])) == got
            scalar_checks += 2
    negative_counts = []
    for j, (base, slope, endpoint, weights, dweights, bc, dbc, a, gain, first) in enumerate([
        (rhos[0], slopes[0], zmax, w2, dwz, bc2, Q(4, 5), a2, gainz, 125),
        (rhos[1], slopes[1], ymax, w3, dwy, bc3, Q(721, 45), a3, gainy, 103),
    ]):
        bounds = {h: base[h] / (-slope[h]) for h in range(128) if slope[h] < 0}
        budget_bounds = {k: weights[k] / (-dweights[k]) for k in range(10) if dweights[k] < 0}
        assert min(bounds.values()) == endpoint
        assert [h for h, lim in bounds.items() if lim == endpoint] == [first]
        assert min(budget_bounds.values()) > endpoint
        assert all(value >= 0 for value in base)
        assert all(value + endpoint * d >= 0 for value, d in zip(base, slope))
        # These endpoint signs and affine identities prove the entire interval.
        # Beyond the endpoint, the displayed limiting customer's residual is negative.
        assert slope[first] < 0 and base[first] == -endpoint * slope[first]
        negative_counts.append(len(bounds))
        name = ["ROOT2_to_ROOT3", "ROOT3_to_ROOT4"][j]
        fam = families[name]
        assert list(map(Q, fam["complete_nonnegative_domain"])) == [0, endpoint]
        assert list(map(Q, fam["weights_constant"])) == weights
        assert list(map(Q, fam["weights_slope"])) == dweights
        assert Q(fam["C_equality_constant"]) == bc and Q(fam["C_equality_slope"]) == dbc
        assert {x["h"]: Q(x["upper_bound"]) for x in fam["all_negative_direction_bounds"]} == bounds
        cols = [
            ([Q(1), Q(0)], [weights[0], dweights[0]]),
            ([-a, -gain], [sum(w * k for w, k in zip(weights, kcol)) - bc,
                          sum(w * k for w, k in zip(dweights, kcol)) - dbc]),
            ([-b, Q(0)], [-b, Q(0)]),
        ]
        for want, got in cols:
            assert want == got
            scalar_checks += 2
    assert negative_counts == [90, 71] and scalar_checks == 524
    zeros = [[h for h in range(128) if rho[h] == 0] for rho in rhos]
    assert zeros == [[0, 1, 3, 5, 9, 17, 123], [0, 1, 3, 5, 9, 17, 123, 125],
                     [0, 1, 3, 5, 9, 17, 103, 123]]
    formal = []
    groups = [
        ("ROOT3", ["E", "F", "X", "N"],
         [{123: 1, 5: 1}, {125: 1, 3: 1}, {1: 1}, {0: 1}],
         [Q(37, 90), Q(25, 8), Q(0), Q(0)]),
        ("ROOT4", ["A", "E", "X", "N"],
         [{103: 1, 17: 1, 9: 1}, {123: 1, 5: 1}, {1: 1}, {0: 1}],
         [Q(1, 18), Q(17, 15), Q(0), Q(0)]),
    ]
    saved_structures = read("equality_structures.json")
    for label, symbols, bases, expected in groups:
        for j, masses in enumerate(bases):
            K, sizes, profits, paid = coefficients_for_basis(allrows, masses)
            assert sizes[:6] == [K] * 6
            assert paid[:5] == [0] * 5
            safe, pair, c30, p25 = paid[5:]
            gap = pair - safe - p25 if label == "ROOT3" else pair - 2 * safe
            assert gap == expected[j]
            saved = saved_structures[label]["formal_basis_coefficients"][j]
            assert list(map(Q, saved["sizes_c_to_o"])) == sizes
            assert list(map(Q, saved["branch_incomes_v1_to_v6"])) == profits
            assert list(map(Q, saved["budgets_CAP2_to_P25"])) == paid
            formal.append({"root": label, "symbol": symbols[j], "K": K,
                           "SAFE6": safe, "PAIR30": pair, "C30_CAP": c30,
                           "P25": p25, "positive_gap": gap})
    # Check the complete CAP parameterizations by solving their seven visible
    # equations symbolically as rational row reductions, without an optimizer.
    for label, zero_codes, symbols, bases, _ in [
        (groups[0][0], zeros[1], groups[0][1], groups[0][2], None),
        (groups[1][0], zeros[2], groups[1][1], groups[1][2], None),
    ]:
        cap_matrix = [[Q(TYPES[h][j] - TYPES[h][0]) for h in zero_codes] for j in range(1, 6)]
        rank = 0
        for col in range(len(zero_codes)):
            pivot = next((r for r in range(rank, 5) if cap_matrix[r][col]), None)
            if pivot is None:
                continue
            cap_matrix[rank], cap_matrix[pivot] = cap_matrix[pivot], cap_matrix[rank]
            divisor = cap_matrix[rank][col]
            cap_matrix[rank] = [x / divisor for x in cap_matrix[rank]]
            for r in range(5):
                if r != rank:
                    factor = cap_matrix[r][col]
                    cap_matrix[r] = [a - factor * b0 for a, b0 in zip(cap_matrix[r], cap_matrix[rank])]
            rank += 1
            if rank == 5:
                break
        assert rank == 4 and len(zero_codes) - rank == len(bases) == 4
        # Each basis has a distinct free core, X or N coordinate.
        free = [123, 125, 1, 0] if label == "ROOT3" else [103, 123, 1, 0]
        assert [[Q(basis.get(h, 0)) for h in free] for basis in bases] == [
            [Q(i == j) for i in range(4)] for j in range(4)]
    # The three literal IC/BR payments in each PAIR, including zero loads.
    pair_local_checks = 0
    for prefix in range(5):
        den = prefix + 1
        for b5, query, other, reply in product((0, 1), repeat=4):
            load = prefix + query + reply
            source_minus_newlast = Q(query - reply, load) if load else Q(0)
            observed = (source_minus_newlast + Q(reply, den + b5) + Q(other, den + query)
                        + Q(b5, den * (den + 1))
                        - Q(query + other, den) + Q(query * other, den * (den + 1)))
            assert observed == Q(b5 * (1 - reply), den * (den + 1)) >= 0
            pair_local_checks += 1
    assert pair_local_checks == 80
    # The ordered six-label PAIR average and its complete weak equality cases.
    pair_checks = 0
    for den in range(1, 6):
        for menu in product((0, 1), repeat=6):
            d = sum(menu)
            o = int(d > 0)
            exact = sum((Q(menu[k] + menu[l], den)
                         - Q(menu[k] * menu[l], den * (den + 1))
                         for k in range(6) for l in range(6) if k != l), Q(0)) / 30
            assert exact == Q(d, 3 * den) - Q(d * (d - 1), 30 * den * (den + 1))
            assert exact >= Q(o, 3 * den)
            assert (exact == Q(o, 3 * den)) == (d in (0, 1))
            pair_checks += 1
    target = read("ROOT270_REPLY_CAP_ITER4.json")
    visible = read("all513_visible_column_checks.json")
    for col, bits in enumerate(list(product((0, 1), repeat=9)) + [None]):
        if bits is None:
            expect = [-a2, -a3, -a4]
        else:
            value = Q(bits[0], sum(bits[:6])) if sum(bits[:6]) else Q(0)
            value -= b * bits[7] + eta * bits[8] * (1 - bits[7])
            expect = [value] * 3
        assert expect == [Q(visible[col][name]) for name in ("ROOT2", "ROOT3", "ROOT4")]
        assert expect[2] == Q(target["a"][str(col)])
    assert a3 == Q(265603424292741718699660497571, 2533743723663632438633587916160)
    assert a4 == Q(644801865488859242734539976772381, 6151085179814078350189473597797760)
    assert gainy * ymax == Q(1585734253979091399252650755, 1845325553944223505056842079339328)
    assert sources() == old_count
    save("literal_equality_coefficients.json", {
        "method": "formal coefficient comparison and exact CAP matrix rank, not feasible-point testing",
        "complete_CAP_nullspace_dimensions": {"ROOT3": 4, "ROOT4": 4},
        "all_formal_basis_coefficients": formal,
        "ROOT3_positive_K_equality_impossible": True, "ROOT4_positive_K_equality_impossible": True,
        "additional_uniform_gain_beyond_ROOT4_claimed": False,
    })
    result = {
        "status": "PASS_INDEPENDENT_LITERAL_ROOT3_AND_ROOT4",
        "actual_agent_id": "/root/high_lambda_closure", "run": "six-boss1-20261111",
        "imports_from_generator_or_project": 0, "optimizer_calls": 0, "global_candidate_inputs": 0,
        "C30_CAP_all_true_costs": tail_checks, "P25_all_true_costs": p25_checks,
        "physical_six_menu_checks": menu_checks, "PAIR30_ordered_index_checks": pair_checks,
        "PAIR_three_true_payment_local_slacks": pair_local_checks,
        "minimum_C30_a1_minus_a0": minimum_moment_slope,
        "complete_D2_domain": [0, zmax], "complete_D3_domain": [0, ymax],
        "D2_unique_first_type": 125, "D3_unique_first_type": 103,
        "negative_direction_counts": negative_counts, "formal_scalar_coefficients": scalar_checks,
        "full_visible_columns_each": 513, "visible_roots_checked": 3,
        "ROOT3_and_ROOT4_CAP_parameterizations_complete": True,
        "ROOT3_and_ROOT4_equality_iff_K_zero": True,
        "ROOT4_uniform_K_gain_over_ROOT3": a4 - a3,
        "all_budget_weights_strictly_positive": True, "old_artifact_hashes_unchanged": old_count,
        "global_welfare_combination_performed": False, "full_SPE_construction_claimed": False,
    }
    save("literal_checker_output.json", result)
    print(json.dumps(enc(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
