#!/usr/bin/env python3
"""Independent Fraction checks from individual true-budget shares.

This file imports no project program. It reads only the present point-free
package and the explicitly pinned frozen source2 mathematical package.
No optimizer, candidate LP point, old solver or global input is accessed.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
S2 = HERE.parent / "source2_minimal_cap_safe"
ZERO = Q(0)


def load(path):
    return json.loads(path.read_text())


def save(name, value):
    with (HERE / name).open("x") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def weights(i, vector):
    tau = {j: vector[j-i-1] for j in range(i+1, 6)}
    s = vector[-1]
    beta = {j: Q(1, 12) + tau[j] + sum((tau[k]*Q(1, 6*(7-k)*(8-k))
                                      for k in range(j+1, 6)), ZERO) for j in tau}
    return tau, s, beta, Q(25)+sum(tau.values(), ZERO)-s


def literal(i, p, t, d, tail, vector, beta_override=None):
    """Cost reconstructed as source share + caps - paid actual shares + queries."""
    tau, s, caps, alpha = weights(i, vector)
    if beta_override is not None:
        caps = beta_override
    r = {j: tail[j-i-1] for j in range(i+1, 7)}
    total = p+t+sum(tail)
    source_share = Q(t, total) if total else ZERO
    actual_tail_shares = {j: Q(r[j], total) if total else ZERO for j in r}
    source_payment_cost = alpha*source_share
    size_payment_cost = sum((caps[j]*r[j] for j in caps), ZERO)+r[6]
    terminal_actual_payment = actual_tail_shares[6]
    internal_actual_payment = sum((tau[j]*actual_tail_shares[j] for j in tau), ZERO)
    terminal_query_cost = Q(d, 6*(p+t+sum(r[j] for j in range(i+1, 6))+1))
    internal_query_cost = ZERO
    for j in tau:
        actual_prefix_load = p+t+sum(r[k] for k in range(i+1, j))
        maximum_future_load = 6-j
        internal_query_cost += tau[j]*Q(d, 6*(actual_prefix_load+1+maximum_future_load))
    return (source_payment_cost+size_payment_cost-terminal_actual_payment
            -internal_actual_payment+terminal_query_cost+internal_query_cost)


def anchor_formula(i, p, t, o, vector, beta_override=None):
    tau, s, beta, alpha = weights(i, vector)
    if beta_override is not None:
        beta = beta_override
    d = p+7-i
    ans = t*(1+sum(beta.values(), ZERO))+Q(24*t, d)-s*Q(t, min(d, 5))
    ans += Q(o, 6*(p+1+(6-i)*t))
    for j, weight in tau.items():
        ans += weight*Q(o, 6*(p+(j-i)*t+7-j))
    return ans


def affine(function, dimension):
    origin = [ZERO]*dimension
    c = function(origin)
    coefficients = []
    for k in range(dimension):
        unit = list(origin)
        unit[k] = Q(1)
        coefficients.append(function(unit)-c)
    return (c, tuple(coefficients))


def record_form(form):
    return {"constant": str(form[0]), "coefficients": list(map(str, form[1]))}


def eval_row(row, vector):
    return Q(row["constant"])+sum((Q(c)*x for c, x in zip(row["coefficients"], vector)), ZERO)


def solve_intersection(matrix, rhs):
    """Forward elimination and back substitution, distinct from producer routine."""
    n = len(rhs)
    matrix = [list(map(Q, row))+[Q(b)] for row, b in zip(matrix, rhs)]
    for k in range(n):
        chosen = next((j for j in range(k, n) if matrix[j][k]), None)
        if chosen is None:
            return None
        matrix[k], matrix[chosen] = matrix[chosen], matrix[k]
        for j in range(k+1, n):
            if matrix[j][k]:
                q = matrix[j][k]/matrix[k][k]
                for ell in range(k+1, n+1):
                    matrix[j][ell] -= q*matrix[k][ell]
                matrix[j][k] = ZERO
    x = [ZERO]*n
    for j in reversed(range(n)):
        x[j] = (matrix[j][-1]-sum((matrix[j][k]*x[k] for k in range(j+1, n)), ZERO))/matrix[j][j]
    return tuple(x)


def rational_rank(vectors):
    basis = {}
    for vector in vectors:
        row = list(map(Q, vector))
        for pivot, old in sorted(basis.items()):
            q = row[pivot]
            row = [a-q*b for a, b in zip(row, old)]
        pivot = next((j for j, value in enumerate(row) if value), None)
        if pivot is not None:
            q = row[pivot]
            basis[pivot] = [value/q for value in row]
    return len(basis)


def main():
    pins = load(HERE / "family_source_manifest.json")["sources"]
    for relative, expected in pins.items():
        assert sha256((REPO / relative).read_bytes()).hexdigest() == expected, relative
    families = load(HERE / "parameter_families.json")["sources"]
    source_by_i = {entry["source"]: entry for entry in families}
    own_states = load(HERE / "full_vertex_hidden_states.json")
    own_state_map = {(e["vertex"], e["p"], e["t"], e["o"], tuple(e["tail"])): e for e in own_states}
    own_tables = load(HERE / "minimum_tables.json")
    own_table_map = {(e["vertex"], e["p"], e["t"], e["o"]): e for e in own_tables}
    source2_states = {(e["vertex"], e["state"]): e for e in load(S2 / "hidden_state_checks.json")}
    source2_tables = {(e["vertex"], e["p"], e["c"], e["o"]): e for e in load(S2 / "minimum_tables.json")}
    affine_checks, minima, state_checks, minimal_caps = [], [], [], []
    domain_checks, menu_checks, root_identities = [], [], []
    minimum_lookup, vertex_lookup = {}, {}
    t0_count = query_diff_count = affine_count = menu_count = state_count = 0
    intersections_total = 0
    for entry in families:
        i = entry["source"]
        dim = 6-i
        middles = list(range(i+1, 6))
        facets = entry["complete_domain_halfspaces"]
        known = {tuple(map(Q, vertex["parameters"])) for vertex in entry["vertices"]}
        strict = list(map(Q, entry["strict_interior"]))
        assert all(eval_row(row, strict) > 0 for row in facets)
        assert rational_rank([[a-b for a, b in zip(point, next(iter(known)))] for point in known]) == dim
        if i != 2:
            rebuilt = set()
            attempted = 0
            for chosen in combinations(facets, dim):
                attempted += 1
                point = solve_intersection([row["coefficients"] for row in chosen], [-Q(row["constant"]) for row in chosen])
                if point is not None and all(eval_row(row, point) >= 0 for row in facets):
                    rebuilt.add(point)
            assert rebuilt == known
            intersections_total += attempted
            for row in facets:
                origin = row["origin"]
                if origin["kind"] == "literal_t1_o0_state":
                    p, tail = origin["p"], tuple(origin["tail"])
                    form = affine(lambda v: literal(i, p, 1, 0, tail, v)-anchor_formula(i, p, 1, 0, v), dim)
                    multiplier = Q(row["positive_multiplier_from_literal"])
                    assert multiplier > 0
                    assert tuple([Q(row["constant"])] + list(map(Q, row["coefficients"]))) == tuple(multiplier*x for x in [form[0], *form[1]])
        else:
            attempted = 0
            assert len(known) == 28
        facet_ranks = []
        for row in facets:
            on_face = [point for point in known if eval_row(row, point) == 0]
            assert on_face
            value = rational_rank([[a-b for a, b in zip(point, on_face[0])] for point in on_face[1:]])
            assert value == dim-1
            facet_ranks.append({"name": row["name"], "vertices_on_face": len(on_face), "rank": value})
        domain_checks.append({"source": i, "dimension": dim, "facets": len(facets),
                              "vertices": len(known), "all_facets_irredundant": True,
                              "intersections_independently_replayed": attempted,
                              "source2_frozen_complete_domain_reused": i == 2, "facet_ranks": facet_ranks})

        for p, t, o in product(range(i), [0, 1], [0, 1]):
            D = p+7-i
            anchor = tuple([0]*(6-i) if not t else ([1]*(6-i) if D <= 5 else [1]*(5-i)+[0]))
            anchor_form = affine(lambda v: literal(i, p, t, o, anchor, v)-anchor_formula(i, p, t, o, v), dim)
            assert anchor_form == (ZERO, tuple([ZERO]*dim))
            for tail in product([0, 1], repeat=6-i):
                form = affine(lambda v: literal(i, p, t, o, tail, v)-anchor_formula(i, p, t, o, v), dim)
                additional = {}
                if t == 0:
                    assert form[0] >= 0 and all(c >= 0 for c in form[1][:-1]) and form[1][-1] == 0
                    t0_count += 1
                    additional["nonnegative_for_all_tau_ge0_all_s"] = True
                if t == 1 and o == 1:
                    diff = affine(lambda v: literal(i, p, 1, 1, tail, v)-anchor_formula(i, p, 1, 1, v)
                                  -literal(i, p, 1, 0, tail, v)+anchor_formula(i, p, 1, 0, v), dim)
                    assert diff[0] >= 0 and all(c >= 0 for c in diff[1][:-1]) and diff[1][-1] == 0
                    query_diff_count += 1
                    additional["o1_minus_o0"] = record_form(diff)
                if t == 1 and o == 0:
                    missing = [j for j in middles if not tail[j-i-1]]
                    k, z = len(missing), tail[-1]
                    def missing_formula(v):
                        tau, s, beta, a = weights(i, v)
                        return ((25-s-z+sum((tau[j] for j in missing), ZERO))/Q(D-1-k+z)
                                +z-1-sum((beta[j] for j in missing), ZERO)-Q(24, D)+s/Q(min(D, 5)))
                    assert affine(missing_formula, dim) == form
                    additional["general_missing_middle_formula_verified"] = True
                affine_checks.append({"source": i, "p": p, "t": t, "o": o, "tail": list(tail),
                                      **record_form(form), **additional})
                affine_count += 1

        for j in middles:
            tau_dim = len(middles)
            tail = tuple(int(k == j) for k in range(i+1, 7))
            def free_cap_form(v):
                vector = v[:dim]
                cap = dict(zip(middles, v[dim:]))
                return literal(i, 0, 0, 1, tail, vector, cap)-anchor_formula(i, 0, 0, 1, vector, cap)
            form = affine(free_cap_form, dim+tau_dim)
            expected = [ZERO]*(dim+tau_dim)
            expected[j-i-1] = Q(-1)
            for ell in range(j+1, 6):
                expected[ell-i-1] = -Q(1, 6*(7-ell)*(8-ell))
            expected[dim+j-i-1] = Q(1)
            assert form == (Q(-1, 12), tuple(expected))
            minimal_caps.append({"source": i, "middle_source": j,
                                 "parameter_order": entry["parameter_order"]+["free_beta"+str(k) for k in middles],
                                 "p": 0, "t": 0, "o": 1, "tail": list(tail), **record_form(form)})

        for p, t in product(range(i), [0, 1]):
            for tail in product([0, 1], repeat=6-i):
                r = dict(zip(range(i+1, 7), tail))
                terminal_den = p+t+sum(r[j] for j in middles)+1
                inner_dens = {j: p+t+sum(r[k] for k in range(i+1, j))+7-j for j in middles}
                for queries in product([0, 1], repeat=6):
                    multiplicity = sum(queries)
                    union = int(multiplicity > 0)
                    literal_terminal = sum((Q(q, terminal_den) for q in queries), ZERO)/6-Q(union, 6*terminal_den)
                    assert literal_terminal == Q(multiplicity-union, 6*terminal_den) >= 0
                    for j, den in inner_dens.items():
                        literal_internal = sum((Q(q, den) for q in queries), ZERO)/6-Q(union, 6*den)
                        assert literal_internal == Q(multiplicity-union, 6*den) >= 0
                    menu_count += 1
                menu_checks.append({"source": i, "p": p, "t": t, "tail": list(tail),
                                    "terminal_coefficient_per_extra_membership": str(Q(1, 6*terminal_den)),
                                    "tau_coefficients_per_extra_membership": {str(j): str(Q(1, 6*den)) for j, den in inner_dens.items()},
                                    "all64_menu_patterns_checked": True})

        for vertex in entry["vertices"]:
            vector = tuple(map(Q, vertex["parameters"]))
            tau, s, beta, alpha = weights(i, vector)
            assert alpha >= 0 and all(x >= 0 for x in tau.values()) and all(x >= 0 for x in beta.values())
            assert all(eval_row(row, vector) >= 0 for row in facets)
            assert str(alpha) == vertex["source_IC_weight"]
            assert str(1+sum(beta.values(), ZERO)) == vertex["total_K_weight"]
            vertex_lookup[vertex["id"]] = (i, vertex, vector)
            for p, t, o in product(range(i), [0, 1], [0, 1]):
                candidates = [(tail, literal(i, p, t, o, tail, vector)) for tail in product([0, 1], repeat=6-i)]
                minimum = min(value for tail, value in candidates)
                expected = anchor_formula(i, p, t, o, vector)
                assert minimum == expected
                ties = [list(tail) for tail, value in candidates if value == minimum]
                key = (vertex["id"], p, t, o)
                minimum_lookup[key] = minimum
                if i == 2:
                    old = source2_tables[(vertex["frozen_source2_vertex_id"], p, t, o)]
                else:
                    old = own_table_map[key]
                assert Q(old["minimum"]) == minimum and old["all_attaining_tails"] == ties
                minima.append({"source": i, "vertex": vertex["id"], "p": p, "t": t, "o": o,
                               "minimum": str(minimum), "all_attaining_tails": ties,
                               "common_anchor": old["common_anchor"]})
                for tail, cost in candidates:
                    excess = cost-minimum
                    assert excess >= 0
                    if i == 2:
                        state_name = "p"+str(p)+"_c"+str(t)+"_o"+str(o)+"_r"+"".join(map(str, tail))
                        old_state = source2_states[(vertex["frozen_source2_vertex_id"], state_name)]
                        assert cost == Q(old_state["cost"]) and excess == Q(old_state["residual"])
                    else:
                        old_state = own_state_map[(vertex["id"], p, t, o, tail)]
                        assert cost == Q(old_state["cost"]) and excess == Q(old_state["excess"])
                    state_checks.append({"source": i, "vertex": vertex["id"], "p": p, "t": t, "o": o,
                                         "tail": list(tail), "cost": str(cost), "minimum": str(minimum),
                                         "residual": str(excess)})
                    state_count += 1
        print(json.dumps({"literal_source_completed": i, "vertices": len(known),
                          "all_state_checks_so_far": state_count}), flush=True)

    for k in [2, 3, 4]:
        for subset in combinations([2, 3, 4, 5], k):
            for z in ([0, 1] if k >= 3 else [0]):
                tail = tuple(int(j not in subset) for j in [2, 3, 4, 5])+(z,)
                def difference(v):
                    tau, s, beta, a = weights(1, v)
                    residual = literal(1, 0, 1, 0, tail, v)-anchor_formula(1, 0, 1, 0, v)
                    sum_single = sum((Q(5, 4)+tau[j]/4-beta[j]-s/20 for j in subset), ZERO)
                    T = sum((tau[j] for j in subset), ZERO)
                    if z == 0:
                        remainder = Q(k-1, 4*(5-k))*(5*k+T-Q(k, 5)*s)
                    elif k == 3:
                        remainder = Q(1, 4)+T/12+s/60
                    else:
                        remainder = 3+T/4-s/10
                    return residual-sum_single-remainder
                form = affine(difference, 5)
                assert form == (ZERO, (ZERO,)*5)
                root_identities.append({"missing_middle": list(subset), "terminal": z,
                                        "identity_residual": record_form(form)})

    counter = load(HERE / "single_missing_counterexample.json")
    v = list(map(Q, counter["parameters"]))
    assert literal(1, 0, 1, 0, tuple(counter["bad_tail_r2_r3_r4_r5_r6"]), v)-anchor_formula(1, 0, 1, 0, v) == Q(-1, 192)
    assert weights(1, v)[3] == Q(811, 48)
    assert all(eval_row(row, v) >= 0 for row in source_by_i[1]["complete_domain_halfspaces"]
               if row["name"].startswith("single_missing"))

    coordinates = load(HERE / "coordinate_contract.json")
    atoms = coordinates["atom_columns"]
    assert len(atoms) == 512 and coordinates["K_column"] == 512
    for index, bits in enumerate(product([0, 1], repeat=9)):
        atom = atoms[index]
        assert atom["index"] == index and atom["old_index"] == index//2
        assert atom["a"]+[atom["x"], atom["o"], atom["c"]] == list(bits)
    rows = load(HERE / "exact_family.json")["rows"]
    assert len(rows) == 1096
    row_checks, signed_checks = [], []
    seen_vertex_target = set()
    old_source2 = {row["vertex_id"]: row for row in load(S2 / "exact_family.json")["rows"]}
    for row in rows:
        i, vertex, vector = vertex_lookup[row["vertex_id"]]
        tau, s, caps, alpha = weights(i, vector)
        S = 1+sum(caps.values(), ZERO)
        target = row["forced_target"]
        assert (vertex["id"], target) not in seen_vertex_target
        seen_vertex_target.add((vertex["id"], target))
        assert row["source"] == i and row["numerical_divisor"] == "25" and row["rhs"] == "0"
        assert row["C_size_equality_eliminated"] is False
        assert set(row["a"]) == {str(j) for j in range(513)}
        for atom in atoms:
            members = atom["a"]
            share = Q(members[i-1], sum(members)) if sum(members) else ZERO
            p = sum(members[:i-1])
            t = members[int(target[1:])-1] if target.startswith("A") else atom[target.lower()]
            expected = alpha*share-minimum_lookup[(vertex["id"], p, t, atom["o"])]
            assert expected == Q(row["a"][str(atom["index"])]), (row["name"], atom["index"])
        assert Q(row["a"]["512"]) == S
        row_checks.append({"name": row["name"], "source": i, "target": target,
                           "literal_columns_checked": 513, "all_exact_residuals_zero": True})
        if i == 2 and target == "C":
            old = old_source2[vertex["frozen_source2_vertex_id"]]
            mu = S-s/5
            ceq = [atom["c"] for atom in atoms]+[-1]
            residuals = [Q(row["a"][str(j)])-Q(old["a"][str(j)])+mu*ceq[j] for j in range(513)]
            assert not any(residuals)
            signed_checks.append({"new_row": row["name"], "old_row": old["name"], "mu": str(mu),
                                  "all513_identity_residuals": list(map(str, residuals))})
    target_set = set(["A"+str(i) for i in range(1, 7)]+["X", "C"])
    for vertex in vertex_lookup:
        assert {target for v, target in seen_vertex_target if v == vertex} == target_set
    assert len(signed_checks) == 28 and [entry["mu"] for entry in signed_checks if Q(entry["mu"]) < 0] == ["-11/20"]
    assert (affine_count, t0_count, query_diff_count, menu_count, state_count, len(minima)) == (456, 228, 114, 14592, 16656, 848)
    save("literal_domain_checks.json", domain_checks)
    save("literal_affine_checks.json", affine_checks)
    save("minimal_cap_necessary_witnesses.json", minimal_caps)
    save("literal_menu_checks.json", {"patterns_checked": menu_count, "contexts": menu_checks})
    save("root_multimissing_redundancy_identities.json", root_identities)
    save("literal_minimum_tables.json", minima)
    save("literal_hidden_state_checks.json", state_checks)
    save("literal_row_checks.json", row_checks)
    save("literal_source2_C_identities.json", signed_checks)
    for relative, expected in pins.items():
        assert sha256((REPO / relative).read_bytes()).hexdigest() == expected, relative
    result = {
        "status": "PASS_INDEPENDENT_LITERAL_ALL_FIVE_SOURCES_ALL1096_RAW_ROWS",
        "sources": 5, "parameter_vertices": 137, "irredundant_facets": 45,
        "owned_domain_intersections_independently_replayed": intersections_total,
        "source2_domain_reused_without_reenumeration": True,
        "full_affine_hidden_states": affine_count,
        "t0_nonnegative_forms_for_arbitrary_tau": t0_count,
        "t1_o1_minus_o0_nonnegative_forms": query_diff_count,
        "coordinatewise_minimal_cap_witnesses": len(minimal_caps),
        "vertex_hidden_states": state_count, "all_minima_and_all_ties": len(minima),
        "six_query_membership_patterns": menu_count,
        "raw_rows": len(rows), "columns": 513, "literal_coefficients": len(rows)*513,
        "source2_signed_C_identity_columns": len(signed_checks)*513,
        "negative_source2_C_multiplier": "-11/20",
        "root_counterexample_residual": "-1/192",
        "source_files_unchanged": len(pins), "optimizer_calls": 0,
        "numeric_input_or_point_read": False, "project_programs_imported_or_executed": False,
        "exact_family_sha256": sha256((HERE / "exact_family.json").read_bytes()).hexdigest(),
    }
    save("literal_checker_output.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
