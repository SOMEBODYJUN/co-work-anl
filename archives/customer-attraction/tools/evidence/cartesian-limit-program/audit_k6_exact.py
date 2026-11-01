"""One exact, raw-unit-client audit of the frozen 23-client point. No LP/model imports."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import time

ROOT = Path("/workspace/scratch/c0ab78c47566")
WORK = ROOT / "round20-cartesian-limit-work"
SOURCE = ROOT / "round20-cartesian_limit_k6.json"
CAPTURE = WORK / "observed-k6"
OUTPUT = WORK / "exact-k6-audit.json"


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(x) for x in obj]
    return obj


def fingerprint(p):
    raw = p.read_bytes()
    return {"path": str(p), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    started = time.perf_counter()
    frozen = json.loads(SOURCE.read_text())
    best = frozen["best"]
    assert best["k"] == 6 and len(best["weights"]) == 63
    nonzero = [(i + 1, w) for i, w in enumerate(best["weights"]) if w]
    assert nonzero == [(19, 5), (33, 18)]
    clients = tuple(mask for mask, w in nonzero for _ in range(w))
    topics = [tuple(i for i, mask in enumerate(clients) if mask & (1 << a)) for a in range(6)]
    assert len(clients) == 23 and set(topics[0]) == set(range(23))
    assert all(set(topics[a]) < set(topics[0]) for a in range(1, 6))
    assert topics[1] == topics[4] and topics[2] == topics[3] == ()

    def payoff(z, position):
        topic = z[position]
        return sum((F(1, sum(bool(mask & (1 << a)) for a in z))
                    for mask in clients if mask & (1 << topic)), F())

    def static(a, background):
        return sum((F(1, 1 + sum(bool(mask & (1 << b)) for b in background))
                    for mask in clients if mask & (1 << a)), F())

    def coverage(z):
        return sum(any(mask & (1 << a) for a in z) for mask in clients)

    triples = tuple(product(range(6), repeat=3))
    pay = {z: tuple(payoff(z, i) for i in range(3)) for z in triples}
    covers = {z: coverage(z) for z in triples}
    assert max(covers.values()) == 23
    last = {}
    last_rows = []
    for a, b in product(range(6), repeat=2):
        vals = [pay[a, b, c][2] for c in range(6)]
        maxima = [c for c, x in enumerate(vals) if x == max(vals)]
        assert maxima == [0]
        last[a, b] = maxima
        last_rows.append({"prefix": (a, b), "payoffs": vals, "best_replies": maxima})
    phi, roots, second_rows = [], [], []
    for a in range(6):
        vals = [pay[a, b, 0][1] for b in range(6)]
        assert vals[0] == max(vals) and all(vals[b] < vals[0] for b in range(1, 6))
        phi.append(vals[0])
        roots.append(pay[a, 0, 0][0])
        second_rows.append({"first": a, "second_payoffs_with_unique_last_reply": vals,
                            "surpluses": [x - vals[0] for x in vals],
                            "unique_credible_second": 0})
    assert phi == [F(23, 3), F(32, 3), F(23, 2), F(23, 2), F(32, 3), F(17, 2)]
    assert roots == [F(23, 3), F(5, 3), F(), F(), F(5, 3), F(6)]
    g = max(roots)
    assert all(roots[a] < g for a in range(1, 6))
    menu = tuple((a, b, 0) for a, b in product(range(6), repeat=2))
    assert all(covers[z] == 23 for z in menu)
    assert all(pay[z][1] - phi[z[0]] <= 0 for z in menu)
    zero_surplus_rows = tuple(z for z in menu if pay[z][1] == phi[z[0]])
    assert zero_surplus_rows == tuple((a, 0, 0) for a in range(6))
    feasible_root_rows = tuple(z for z in zero_surplus_rows if pay[z][0] >= g)
    assert feasible_root_rows == ((0, 0, 0),)

    # Every complete ordered history uses action 0; inspect every actual continuation.
    ic = []
    for length in range(3):
        for h in product(range(6), repeat=length):
            actual = h + (0,) * (3 - length)
            u = pay[actual][length]
            for a in range(6):
                deviated = h + (a,) + (0,) * (2 - length)
                v = pay[deviated][length]
                assert u >= v and (a == 0 or u > v)
                ic.append({"history": h, "action": 0, "alternative": a,
                           "actual_terminal": actual, "deviated_terminal": deviated,
                           "actual_payoff": u, "deviated_payoff": v, "slack": u-v})
    assert len(ic) == 258
    backgrounds = tuple(combinations_with_replacement(range(6), 2))
    matrix = [[static(a, b) for a in range(6)] for b in backgrounds]
    assert all(row[0] >= g for row in matrix)
    assert max(matrix[0]) == g
    assert all(row[0] > g for row in matrix[1:])

    observed = json.loads((CAPTURE / "original-analyze-locals.json").read_text())
    assert observed["triples"] == [list(z) for z in triples]
    assert observed["menus"] == [[list((a, b, 0)) for b in range(6)] for a in range(6)]
    count = 0
    def near(actual, exact):
        nonlocal count
        if isinstance(exact, (tuple, list)):
            assert isinstance(actual, list) and len(actual) == len(exact)
            for x, y in zip(actual, exact):
                near(x, y)
        elif exact is None or isinstance(exact, str):
            assert actual == exact
        else:
            assert abs(float(actual) - float(exact)) <= 1e-12, (actual, exact)
            count += 1
    original_pay_entries = 0
    for row in observed["six_scaled_pay_vectors"]:
        z = tuple(row["terminal"])
        for i in range(3):
            assert row["vector"][z[i]] == 6 * pay[z][i]
            original_pay_entries += 1
    assert original_pay_entries == 648
    near(observed["security_matrix"], matrix)
    calls = json.loads((CAPTURE / "linprog-calls.json").read_text())
    assert [x["result"]["status"] for x in calls] == [0]*6 + [2, 0, 0]
    def check_arguments(call, objective, Aub, bub, Aeq, beq, bounds):
        args = call["arguments"]
        for key, expected in [("c", objective), ("A_ub", Aub), ("b_ub", bub),
                              ("A_eq", Aeq), ("b_eq", beq), ("bounds", bounds)]:
            near(args[key], expected)
        assert args["method"] == "highs"
        assert all(args[key] is None for key in ("callback", "options", "x0", "integrality"))
    for a in range(6):
        rows = [(a, b, 0) for b in range(6)]
        check_arguments(calls[a], [pay[z][0] for z in rows], [[-pay[z][1] for z in rows]],
                        [-phi[a]], [[1]*6], [1], [0, None])
        near(calls[a]["result"]["x"], [1, 0, 0, 0, 0, 0])
        near(calls[a]["result"]["fun"], roots[a])
    Aub = [[-pay[z][0] for z in menu], [phi[z[0]] - pay[z][1] for z in menu]]
    for index, epsilon in [(6, F(1, 1000000)), (7, F())]:
        check_arguments(calls[index], [23]*36, Aub, [-g-epsilon, 0], [[1]*36], [1], [0, None])
    assert calls[6]["result"]["x"] is None
    near(calls[7]["result"]["x"], [1]+[0]*35)
    check_arguments(calls[8], [0]*6+[-1], [[-x for x in row]+[1] for row in matrix],
                    [0]*21, [[1]*6+[0]], [1], [[0, None]]*6+[[None, None]])
    near(calls[8]["result"]["x"][:6], [1, 0, 0, 0, 0, 0])
    near(calls[8]["result"]["x"][-1], g)
    near(best["phi"], phi)
    near(best["root_floor_by_action"], roots)
    near(best["root_floor"], g)
    near(best["security"], g)
    near(best["relaxed_W"], 23)
    near(best["gap"], 0)
    near(best["actual_payoffs"], [g]*3)
    near(best["actual_second_surplus"], 0)
    near(best["actual_first_margin"], 0)
    assert best["actual_mix"] == [{"terminal": [0, 0, 0], "probability": 1.0}]
    assert best["query"] == [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert best["opponent"] == [{"background": [0, 0], "probability": 1.0}]
    assert best["root_minimizers"] == [[[[a, 0, 0], 1.0]] for a in range(6)]
    result = {
        "status": "PASS", "source": fingerprint(SOURCE), "raw_unit_clients": len(clients),
        "nonzero_types": nonzero, "topic_customer_ids": topics,
        "all_terminal_payoffs": [{"terminal": z, "payoffs": pay[z], "welfare": covers[z]} for z in triples],
        "all_last_reply_rows": last_rows, "all_second_menu_rows": second_rows,
        "phi": phi, "convexified_root_floors": roots, "pure_root_floors": roots,
        "root_floor": g, "last_BR_triples": menu, "zero_second_surplus_rows": zero_surplus_rows,
        "weak_root_feasible_support": feasible_root_rows,
        "strict_root_positive_margin_infeasible": True,
        "strict_infeasibility_reason": "All second surplus entries are nonpositive, forcing support to (a,0,0); then every root payoff is <=g, so any positive root surplus is impossible.",
        "security_background_rows": [{"background": b, "query_payoffs": row} for b, row in zip(backgrounds, matrix)],
        "security_primal": [1, 0, 0, 0, 0, 0], "security_dual": [{"background": (0, 0), "probability": 1}],
        "exact_security": g, "exact_relaxed_welfare": 23, "exact_relaxed_gap": 0,
        "complete_constant_zero_strategy": {"decision_histories": 43, "comparisons_including_self": 258,
                                            "strict_nonself_comparisons": 215, "minimum_nonself_slack": min(x["slack"] for x in ic if x["alternative"]),
                                            "actual_path": (0, 0, 0), "payoffs": [g]*3, "W": 23, "OPT": 23},
        "all_complete_strategy_comparisons": ic,
        "observed_original_occupied_pay_entries_compared_exactly": original_pay_entries,
        "observed_LP_float_scalars_compared_to_exact_data": count,
        "float_comparison_tolerance": "1e-12",
        "all_nine_original_LP_argument_blocks_checked": True,
        "source_status_retained": frozen["status"], "historical_completed": frozen["completed"],
        "historical_requested": frozen["requested"], "historical_seed": frozen["seed"],
        "original_program_imports": 0, "original_analyze_calls": 0, "LP_calls": 0, "canonical_SPE_solver_calls": 0,
        "independent_exact_point_audit_runs": 1, "elapsed_seconds": time.perf_counter()-started,
        "limits": [
            "Only this frozen 23-unit-client k6 point is independently audited; historical 300 samples are not reproduced.",
            "The constant-zero complete SPE is established by this exact definition audit and universal-theme argument, not by the original floating report.",
            "Generic Cartesian limit and finite rational rounding require the separate analytic theorem; this equality point is not a negative compiler seed.",
            "Observed numerical coefficients are compared within tolerance; exact claims are supported by separately generated Fraction data and finite certificates.",
        ],
    }
    OUTPUT.write_text(json.dumps(encode(result), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "clients": 23, "terminals": 216, "histories": 43,
                      "IC_comparisons": 258, "original_LP_calls_replayed": 0,
                      "nine_argument_blocks_checked": True, "float_scalars_compared": count}))


if __name__ == "__main__":
    main()
