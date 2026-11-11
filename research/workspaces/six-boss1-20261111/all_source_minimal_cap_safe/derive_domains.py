#!/usr/bin/env python3
"""Exact small polytope intersections and literal true-budget checks; no optimizer.

Owned sources are1,3,4,5. Source2 is intentionally not enumerated here.
No global LP input, numerical primal, support or optimal-face file is read.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import comb, gcd, lcm
from pathlib import Path
from time import monotonic
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCES = [1, 3, 4, 5]
ZERO = F(0)


def write(name, value):
    with (HERE / name).open("x") as output:
        output.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def parameters(source, vector):
    middle = list(range(source + 1, 6))
    tau = dict(zip(middle, vector[:-1]))
    s = vector[-1]
    beta = {
        j: F(1, 12) + tau[j] + sum(
            (tau[ell] / (6 * (7 - ell) * (8 - ell)) for ell in middle if ell > j), ZERO)
        for j in middle
    }
    return tau, s, beta, F(25) + sum(tau.values(), ZERO) - s


def true_cost(source, p, t, multiplicity, tail, vector):
    tau, s, beta, a = parameters(source, vector)
    middle = list(range(source + 1, 6))
    members = dict(zip(range(source + 1, 7), tail))
    z = members[6]
    k = sum(members[j] for j in middle)
    load = p + t + sum(tail)
    numerator = a * t - z - sum((tau[j] * members[j] for j in middle), ZERO)
    assert load or numerator == 0
    result = numerator / load if load else ZERO
    result += sum((beta[j] * members[j] for j in middle), ZERO) + z
    result += F(multiplicity, 6 * (p + t + k + 1))
    for j in middle:
        prefix = p + t + sum(members[ell] for ell in middle if ell < j)
        result += tau[j] * F(multiplicity, 6 * (prefix + 7 - j))
    return result


def candidate_minimum(source, p, t, o, vector):
    tau, s, beta, a = parameters(source, vector)
    n = 6 - source
    D = p + n + 1
    result = t * (1 + sum(beta.values(), ZERO)) + F(24 * t, D)
    result -= s * F(t, min(D, 5))
    result += F(o, 6 * (p + 1 + n * t))
    result += sum((tau[j] * F(o, 6 * (p + (j - source) * t + 7 - j))
                   for j in tau), ZERO)
    return result


def affine_state(source, p, tail):
    dimension = 6 - source
    origin = [ZERO] * dimension
    constant = true_cost(source, p, 1, 0, tail, origin) - candidate_minimum(source, p, 1, 0, origin)
    coefficients = []
    for j in range(dimension):
        unit = list(origin)
        unit[j] = F(1)
        coefficients.append(true_cost(source, p, 1, 0, tail, unit)
                            - candidate_minimum(source, p, 1, 0, unit) - constant)
    return constant, tuple(coefficients)


def normalized(constant, coefficients):
    values = [constant, *coefficients]
    denominator = lcm(*(value.denominator for value in values))
    integers = [int(value * denominator) for value in values]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    assert common
    multiplier = F(denominator, common)
    return F(integers[0] // common), tuple(F(value // common) for value in integers[1:]), multiplier


def pack_row(name, constant, coefficients, origin):
    c, a, multiplier = normalized(constant, coefficients)
    return {
        "name": name, "constant": str(c), "coefficients": [str(value) for value in a],
        "positive_multiplier_from_literal": str(multiplier), "origin": origin,
    }


def evaluation(row, vector):
    return F(row["constant"]) + sum((F(a) * x for a, x in zip(row["coefficients"], vector)), ZERO)


def solve_unique(coefficients, rhs):
    """Exact Gauss-Jordan on at most5 unknowns; no numerical solver."""
    size = len(rhs)
    augmented = [[F(value) for value in row] + [F(value)] for row, value in zip(coefficients, rhs)]
    for j in range(size):
        pivot = next((k for k in range(j, size) if augmented[k][j]), None)
        if pivot is None:
            return None
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        divisor = augmented[j][j]
        for k in range(j, size + 1):
            augmented[j][k] /= divisor
        for i in range(size):
            if i == j or not augmented[i][j]:
                continue
            weight = augmented[i][j]
            for k in range(j, size + 1):
                augmented[i][k] -= weight * augmented[j][k]
    return tuple(row[-1] for row in augmented)


def rank(matrix):
    if not matrix:
        return 0
    rows = [list(map(F, row)) for row in matrix]
    r = 0
    for j in range(len(rows[0])):
        pivot = next((k for k in range(r, len(rows)) if rows[k][j]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        q = rows[r][j]
        rows[r] = [value / q for value in rows[r]]
        for k in range(len(rows)):
            if k != r and rows[k][j]:
                q = rows[k][j]
                rows[k] = [x - q * y for x, y in zip(rows[k], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def domain_description(source):
    middle = list(range(source + 1, 6))
    dimension = len(middle) + 1
    full_states = []
    state_lookup = {}
    for p in range(source):
        D = p + 7 - source
        for tail in product([0, 1], repeat=6 - source):
            constant, coefficients = affine_state(source, p, tail)
            entry = {
                "source": source, "p": p, "D": D, "t": 1, "o": 0, "tail": list(tail),
                "missing_middle": [j for j in middle if not tail[j - source - 1]],
                "terminal": tail[-1],
                "constant": str(constant), "coefficients": [str(value) for value in coefficients],
                "identically_zero": constant == 0 and not any(coefficients),
            }
            full_states.append(entry)
            state_lookup[(p, tail)] = (constant, coefficients)
    chosen = []
    for j in middle:
        coefficients = [ZERO] * dimension
        coefficients[middle.index(j)] = F(1)
        chosen.append(pack_row("tau" + str(j) + "_nonnegative", ZERO, coefficients, {"kind": "weight_nonnegative", "source": j}))

    def state_facet(name, p, missing, terminal):
        tail = tuple([0 if j in missing else 1 for j in middle] + [terminal])
        constant, coefficients = state_lookup[(p, tail)]
        chosen.append(pack_row(name, constant, coefficients, {
            "kind": "literal_t1_o0_state", "source": source, "p": p,
            "D": p + 7 - source, "missing_middle": list(missing), "tail": list(tail),
        }))

    state_facet("s_nonnegative", source - 1, [], 1)
    if source == 1:
        for j in middle:
            state_facet("single_missing_" + str(j) + "_D6_terminal1", 0, [j], 1)
            state_facet("single_missing_" + str(j) + "_D6_terminal0", 0, [j], 0)
        for j, k in combinations(middle, 2):
            state_facet("double_missing_" + str(j) + "_" + str(k) + "_D6_terminal1", 0, [j, k], 1)
    else:
        state_facet("s_upper9", source - 2, [], 0)
        for j in middle:
            state_facet("single_missing_" + str(j) + "_D6_terminal1", source - 1, [j], 1)
            state_facet("single_missing_" + str(j) + "_D5_terminal1", source - 2, [j], 1)
    expected = {1: 19, 3: 8, 4: 5, 5: 2}[source]
    assert len(chosen) == expected
    interior = [F(1, 10)] * len(middle) + [F(1)]
    assert all(evaluation(row, interior) > 0 for row in chosen)
    return middle, dimension, full_states, chosen, interior


def enumerate_vertices(source, facets, dimension):
    start = monotonic()
    vertices = set()
    singular = infeasible = feasible = 0
    coefficients = [tuple(map(F, row["coefficients"])) for row in facets]
    rhs = [-F(row["constant"]) for row in facets]
    total = comb(len(facets), dimension)
    attempted = 0
    for indices in combinations(range(len(facets)), dimension):
        attempted += 1
        if attempted % 512 == 0:
            elapsed = monotonic() - start
            if elapsed > 60:
                raise RuntimeError("Exact source" + str(source) + " enumeration stopped at "
                                   + str(attempted) + "/" + str(total) + " after60s; no long blind continuation.")
        solution = solve_unique([coefficients[i] for i in indices], [rhs[i] for i in indices])
        if solution is None:
            singular += 1
        elif not all(evaluation(row, solution) >= 0 for row in facets):
            infeasible += 1
        else:
            feasible += 1
            vertices.add(solution)
    assert attempted == total and singular + infeasible + feasible == total
    return sorted(vertices), {
        "candidate_intersections": total, "attempted": attempted, "singular": singular,
        "infeasible_full_rank": infeasible, "feasible_full_rank": feasible,
        "distinct_vertices": len(vertices), "elapsed_seconds": monotonic() - start,
        "optimizer_calls": 0,
    }


def run():
    domain_results = []
    all_raw_states = []
    all_literal_states = []
    all_minimum_tables = []
    all_boundary_checks = []
    literal_counts = {}
    for source in SOURCES:
        middle, dimension, raw_states, facets, interior = domain_description(source)
        vertices, enumeration = enumerate_vertices(source, facets, dimension)
        assert vertices
        assert rank([[value - vertices[0][j] for j, value in enumerate(vertex)]
                     for vertex in vertices[1:]]) == dimension
        all_raw_states += raw_states
        detailed_vertices = []
        for position, vector in enumerate(vertices):
            tau, s, beta, a = parameters(source, vector)
            assert all(value >= 0 for value in tau.values()) and a >= 0
            assert all(F(row["constant"]) + sum((F(c) * x for c, x in zip(row["coefficients"], vector)), ZERO) >= 0
                       for row in raw_states), (source, vector, "candidate domain misses a true state")
            identifier = "MINCAP_I" + str(source) + "_V" + format(position, "03d")
            detailed_vertices.append({
                "id": identifier, "parameters": [str(value) for value in vector],
                "tau_by_true_source": {str(j): str(tau[j]) for j in middle},
                "s": str(s), "source_IC_weight": str(a),
                "middle_CAP_weights": {str(j): str(beta[j]) for j in middle},
                "terminal_CAP_weight": "1", "terminal_BR_average_weight": "1",
                "total_K_weight": str(1 + sum(beta.values(), ZERO)),
                "active_halfspaces": [row["name"] for row in facets if evaluation(row, vector) == 0],
            })
            for p, t, o in product(range(source), [0, 1], [0, 1]):
                D = p + 7 - source
                target = candidate_minimum(source, p, t, o, vector)
                attaining = []
                for tail in product([0, 1], repeat=6 - source):
                    value = true_cost(source, p, t, o, tail, vector)
                    excess = value - target
                    assert excess >= 0, (identifier, p, t, o, tail, excess)
                    members = dict(zip(range(source + 1, 7), tail))
                    p_extra = None
                    if t == 0:
                        k = sum(members[j] for j in middle)
                        load = p + sum(tail)
                        query_payment = F(k, 12) - F(o * k, 6 * (p + 1) * (p + k + 1))
                        crossed = ZERO
                        for j in middle:
                            prefix_count = sum(members[ell] for ell in middle if ell < j)
                            term = (F(prefix_count, 6 * (7 - j) * (8 - j))
                                    - F(o * prefix_count, 6 * (p + 7 - j) * (p + 7 - j + prefix_count)))
                            assert term >= 0
                            crossed += tau[j] * term
                        shares = ((sum((tau[j] * members[j] for j in middle), ZERO) + members[6])
                                  * (1 - F(1, load))) if load else ZERO
                        assert query_payment >= 0 and crossed >= 0 and shares >= 0
                        assert query_payment + crossed + shares == excess
                        p_extra = {"terminal_query_paid_by_k_over12": str(query_payment),
                                   "internal_query_losses_paid_by_cross_caps": str(crossed),
                                   "nonnegative_share_remainder": str(shares)}
                    if t == 1 and o == 1:
                        base_excess = (true_cost(source, p, 1, 0, tail, vector)
                                       - candidate_minimum(source, p, 1, 0, vector))
                        assert excess >= base_excess
                    all_literal_states.append({
                        "vertex": identifier, "source": source, "p": p, "D": D,
                        "t": t, "o": o, "tail": list(tail), "cost": str(value),
                        "minimum": str(target), "excess": str(excess),
                        "t0_direct_payment": p_extra,
                    })
                    if excess == 0:
                        attaining.append(list(tail))
                if t == 0:
                    anchor = [0] * (6 - source)
                elif D <= 5:
                    anchor = [1] * (6 - source)
                else:
                    anchor = [1] * (5 - source) + [0]
                assert anchor in attaining
                all_minimum_tables.append({
                    "vertex": identifier, "source": source, "p": p, "D": D, "t": t, "o": o,
                    "minimum": str(target), "common_anchor": anchor,
                    "all_attaining_tails": attaining,
                })
        facet_checks = []
        for row in facets:
            boundary = [vertex for vertex in vertices if evaluation(row, vertex) == 0]
            affine_rank = -1 if not boundary else rank([
                [value - boundary[0][j] for j, value in enumerate(vertex)] for vertex in boundary[1:]
            ])
            facet_checks.append({
                "halfspace": row["name"], "boundary_vertex_count": len(boundary),
                "boundary_affine_rank": affine_rank, "is_facet": affine_rank == dimension - 1,
            })
        # Every listed candidate is also certified as a genuine facet.
        assert all(entry["is_facet"] for entry in facet_checks), (source, facet_checks)
        all_boundary_checks += [{"source": source, **entry} for entry in facet_checks]
        minimum_a = min(F(vertex["source_IC_weight"]) for vertex in detailed_vertices)
        maximum_s = max(F(vertex["s"]) for vertex in detailed_vertices)
        assert minimum_a == (F(5, 3) if source == 1 else F(16))
        assert maximum_s == (F(70, 3) if source == 1 else F(9))
        result = {
            "source": source, "middle_sources": middle,
            "parameter_order": ["tau" + str(j) for j in middle] + ["s"],
            "dimension": dimension, "D_values": list(range(7 - source, 7)),
            "complete_domain_halfspaces": facets, "all_listed_halfspaces_are_facets": True,
            "strict_interior": [str(value) for value in interior],
            "explicit_source_IC_nonnegative_condition": {
                "formula": "25+sum(tau)-s>=0",
                "included_in_original_contract": True,
                "redundant_on_complete_domain": True,
                "exact_minimum": str(minimum_a),
            },
            "bounded_box": {
                "tau_each_lower": "0", "tau_each_upper": "43/48",
                "s_lower": "0", "s_upper": str(maximum_s),
            },
            "enumeration": enumeration, "vertices": detailed_vertices,
            "minimum_source_IC_weight": str(minimum_a), "maximum_s": str(maximum_s),
            "minimum_a_vertex_ids": [v["id"] for v in detailed_vertices if F(v["source_IC_weight"]) == minimum_a],
            "maximum_s_vertex_ids": [v["id"] for v in detailed_vertices if F(v["s"]) == maximum_s],
            "original_t1_o0_state_count": len(raw_states),
        }
        domain_results.append(result)
        literal_counts[str(source)] = {
            "vertices": len(vertices), "facets": len(facets),
            "vertex_full_states": len(vertices) * source * 4 * (2 ** (6 - source)),
            "minimum_tables": len(vertices) * source * 4,
        }
        print(json.dumps({"source_completed": source, **literal_counts[str(source)],
                          "enumeration_seconds": enumeration["elapsed_seconds"]}), flush=True)
    # Explicit root counterexample to a single-missing-only domain.
    counter = [F(0), F(0), F(5977, 6912), F(43, 48), F(68185, 6912)]
    tau, s, beta, a = parameters(1, counter)
    single_slacks = {}
    for j in range(2, 6):
        missing = [1 if ell != j else 0 for ell in range(2, 6)]
        for terminal in [0, 1]:
            tail = missing + [terminal]
            excess = true_cost(1, 0, 1, 0, tail, counter) - candidate_minimum(1, 0, 1, 0, counter)
            assert excess >= 0
            single_slacks[str(j) + "_" + str(terminal)] = str(excess)
    bad_tail = [1, 1, 0, 0, 1]
    excess = true_cost(1, 0, 1, 0, bad_tail, counter) - candidate_minimum(1, 0, 1, 0, counter)
    assert excess == F(-1, 192) and a == F(811, 48)
    write("single_missing_counterexample.json", {
        "status": "EXACT_ROOT_PARAMETER_COUNTEREXAMPLE_NOT_AN_SPE_COUNTEREXAMPLE",
        "source": 1, "parameters": [str(value) for value in counter],
        "tau_by_true_source": {str(j): str(value) for j, value in tau.items()},
        "s": str(s), "source_IC_weight": str(a),
        "all_single_missing_slacks": single_slacks,
        "p": 0, "t": 1, "o": 0, "bad_tail_r2_r3_r4_r5_r6": bad_tail,
        "missing_middle": [4, 5], "terminal": 1,
        "literal_cost": str(true_cost(1, 0, 1, 0, bad_tail, counter)),
        "candidate_minimum": str(candidate_minimum(1, 0, 1, 0, counter)),
        "residual": str(excess), "optimizer_calls": 0,
    })
    write("parameter_domains.json", {
        "schema": "minimal_cap_safe_sources1_3_4_5_complete_domains_v1",
        "status": "EXACT_COMPLETE_DOMAINS_AND_ALL_VERTICES",
        "halfspace_convention": "constant+coefficients dot(tau...,s)>=0",
        "sources": domain_results,
        "source2_intentionally_not_enumerated": True,
        "optimizer_calls": 0, "global_numerical_point_read": False,
        "scope": "Complete parameter domains for the specified literal affine envelope with nonnegative true budget weights; not all possible SPE proofs.",
    })
    write("all_t1_o0_affine_states.json", all_raw_states)
    write("full_vertex_hidden_states.json", all_literal_states)
    write("minimum_tables.json", all_minimum_tables)
    write("facet_rank_checks.json", all_boundary_checks)
    source_paths = [
        HERE.parent / "all_source_joint_reweighted_safe/proof.md",
        REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    ]
    write("source_manifest.json", {
        "status": "POINT_FREE_DIRECT_TRUE_BUDGET_SOURCE_BINDING",
        "sources": {str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest() for path in source_paths},
        "proposal_attribution": "Main supplied minimal-cap beta and source-IC reweighting formula; this package derives complete domains for sources1,3,4,5 directly.",
        "source2_domain_or_numeric_points_read": False, "optimizer_calls": 0,
    })
    result = {
        "status": "PASS_COMPLETE_POINT_FREE_MINIMAL_CAP_DOMAINS",
        "sources": SOURCES, "per_source": literal_counts,
        "total_vertices": sum(item["vertices"] for item in literal_counts.values()),
        "total_facets": len(all_boundary_checks),
        "total_t1_o0_affine_states": len(all_raw_states),
        "all_vertex_hidden_states": len(all_literal_states),
        "all_minimum_tables": len(all_minimum_tables),
        "all_weak_attaining_tails_preserved": True,
        "root_multi_missing_counterexample_residual": "-1/192",
        "all_source_IC_weights_nonnegative": True,
        "optimizer_calls": 0, "source2_enumerated": False,
        "global_input_or_point_read": False, "target_coordinate_rows_generated": 0,
    }
    write("domain_result.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        if not (HERE / "domain_obstacle.json").exists():
            write("domain_obstacle.json", {
                "status": "INCOMPLETE_EXACT_DOMAIN_WORK_NO_OPTIMIZER",
                "error_type": type(error).__name__, "error": str(error),
                "optimizer_calls": 0,
            })
        raise
