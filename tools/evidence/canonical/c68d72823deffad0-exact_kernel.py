#!/usr/bin/env python3
"""Exact check of one six-machine fixed-pair witness; no search beyond 64 tuples.

The instance and pair laws are explicitly prescribed. Fraction arithmetic checks
them; the non-extension proof is also supplied analytically in candidate-body.md.
Only this staging directory is written, and no repository code is imported.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
MACHINES = tuple((i, s) for i in (1, 2, 3) for s in (0, 1))
JOBS = (1, 2, 3)
HALF = Fraction(1, 2)
R = {(1, 2): 0, (2, 3): 0, (1, 3): 1}


def name(machine):
    i, s = machine
    return ("a" if s == 0 else "b") + str(i)


def processing(machine, job):
    return 1 if machine[0] == job else 2


def config(machine, occupancy):
    return frozenset((machine[0],)) if occupancy else frozenset()


def pair_law(u, v):
    i, s = u
    j, t = v
    if i == j:
        assert s != t
        parity = 1
    else:
        assert i < j
        parity = R[(i, j)] ^ s ^ t
    return {(0, parity): HALF, (1, 1 ^ parity): HALF}


def marginal(law, positions):
    result = {}
    for state, mass in law.items():
        key = tuple(state[k] for k in positions)
        result[key] = result.get(key, Fraction()) + mass
    return {key: mass for key, mass in result.items() if mass}


def encode_law(law):
    return [{"state": list(state), "mass": str(mass)}
            for state, mass in sorted(law.items())]


def load_vector(state, machines=MACHINES):
    return [sum(processing(machine, job)
                for job in config(machine, occupancy))
            for machine, occupancy in zip(machines, state)]


def exact_cover(state, machines=MACHINES, jobs=JOBS):
    return all(sum(job in config(machine, z)
                   for machine, z in zip(machines, state)) == 1
               for job in jobs)


def is_forest():
    vertices = [("machine", name(u)) for u in MACHINES]
    vertices += [("job", i) for i in JOBS]
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    edges = []
    for u in MACHINES:
        # The only fractional incidence of this row is its own task.
        a, b = ("machine", name(u)), ("job", u[0])
        ra, rb = find(a), find(b)
        assert ra != rb
        parent[ra] = rb
        edges.append([list(a), list(b)])
    return {"vertices": len(vertices), "edges": len(edges),
            "components": len({find(v) for v in vertices}),
            "is_forest": True, "edge_list": edges}


def main():
    # All threshold-1 configurations are exactly empty or the row's own task:
    # every other job alone exceeds T. No local power-set enumeration needed.
    local_counts = []
    for u in MACHINES:
        assert processing(u, u[0]) == 1
        assert all(processing(u, j) > 1 for j in JOBS if j != u[0])
        local_counts.append(2)

    pairs = {}
    pair_report = []
    for u_idx, v_idx in combinations(range(6), 2):
        u, v = MACHINES[u_idx], MACHINES[v_idx]
        law = pair_law(u, v)
        assert sum(law.values()) == 1
        assert marginal(law, (0,)) == {(0,): HALF, (1,): HALF}
        assert marginal(law, (1,)) == {(0,): HALF, (1,): HALF}
        assert all(config(u, a).isdisjoint(config(v, b))
                   for (a, b), mass in law.items() if mass)
        pairs[(u_idx, v_idx)] = law
        pair_report.append({"machines": [name(u), name(v)],
                            "law": encode_law(law),
                            "row_marginals_correct": True,
                            "disjoint_support": True})
    assert len(pairs) == 15

    # Exactly 2^6=64 row-configuration tuples. Matching zero entries of all
    # prescribed pair laws would require every positive global atom to lie in
    # their support intersection. This intersection is empty.
    states = list(product((0, 1), repeat=6))
    assert len(states) == 64
    cover_states = [state for state in states if exact_cover(state)]
    compatible_states = [state for state in states
                         if all((state[a], state[b]) in law
                                for (a, b), law in pairs.items())]
    assert len(cover_states) == 8
    assert compatible_states == []

    # Existing row laws do have a complete threshold-1 scheduling realization.
    independent = {state: Fraction(1, 8) for state in cover_states}
    assert sum(independent.values()) == 1
    for k in range(6):
        assert marginal(independent, (k,)) == {(0,): HALF, (1,): HALF}
    assert all(max(load_vector(state)) == 1 for state in independent)
    assert all(exact_cover(state) for state in independent)

    # Strong local check: every TWO original components, including all their
    # six machine-pair laws, have one joint distribution on two actual states.
    two_component_report = []
    for i, j in combinations(JOBS, 2):
        indices = [k for k, u in enumerate(MACHINES) if u[0] in (i, j)]
        machines = tuple(MACHINES[k] for k in indices)
        law = {}
        for coin in (0, 1):
            x = {i: coin, j: coin ^ R[(i, j)]}
            state = tuple(x[g] ^ s for g, s in machines)
            law[state] = HALF
        assert all(exact_cover(state, machines, (i, j)) for state in law)
        assert all(max(load_vector(state, machines)) == 1 for state in law)
        for a, b in combinations(range(4), 2):
            assert marginal(law, (a, b)) == pairs[(indices[a], indices[b])]
        two_component_report.append({"components": [i, j],
                                     "all_six_pairs_match": True,
                                     "joint_law": encode_law(law)})

    # The a-machine triple itself gives a short exact support/dual certificate.
    aa_support = [x for x in product((0, 1), repeat=3)
                  if x[0] == x[1] and x[1] == x[2] and x[0] != x[2]]
    assert aa_support == []
    for x in product((0, 1), repeat=3):
        assert int(x[0] != x[2]) <= int(x[0] != x[1]) + int(x[1] != x[2])

    # Separate existing 2x2 single-cycle object, at most four local tuples.
    single_a = [frozenset(), frozenset((1, 2))]
    single_b = [frozenset((1,)), frozenset((2,))]
    assert all(len(a) <= 2 for a in single_a)
    assert all(2 * len(b) <= 2 for b in single_b)
    for job in (1, 2):
        assert sum(HALF * (job in a) for a in single_a) + sum(
            HALF * (job in b) for b in single_b) == 1
    single_tuples = list(product(single_a, single_b))
    single_exact = [(a, b) for a, b in single_tuples
                    if a.isdisjoint(b) and a | b == frozenset((1, 2))]
    assert single_exact == []
    assert all(not single_a[1].isdisjoint(b) for b in single_b)
    single_schedule_loads = (len(frozenset((1, 2))), 0)
    assert max(single_schedule_loads) == 2  # both tasks on A meet T=2

    report = {
        "status": "PASS",
        "method": "exact Fraction arithmetic; one prescribed instance, no parameter sweep",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "machines": [name(u) for u in MACHINES],
        "jobs": list(JOBS), "threshold": 1,
        "processing_matrix": [[processing(u, j) for j in JOBS] for u in MACHINES],
        "local_legal_configuration_counts": local_counts,
        "row_masses": {"empty": "1/2", "own_singleton": "1/2"},
        "job_expected_multiplicity": {str(j): "1" for j in JOBS},
        "fractional_incidence": is_forest(),
        "machine_pair_count": len(pairs),
        "pair_laws": pair_report,
        "global_row_configuration_tuples_enumerated": len(states),
        "threshold_1_exact_cover_tuples": len(cover_states),
        "all_prescribed_pair_supports_compatible_tuples": len(compatible_states),
        "independent_row_preserving_schedule_law": encode_law(independent),
        "independent_law_correct_rows_and_threshold": True,
        "every_two_components_jointly_realize_all_six_pairs": two_component_report,
        "aa_triangle_feasible_supports": len(aa_support),
        "pointwise_dual_inequality": "1[X1!=X3] <= 1[X1!=X2] + 1[X2!=X3]",
        "prescribed_dual_values": {"left": "1", "right": "0"},
        "opt": {"value": "1", "proof": "each task has minimum processing time 1; eight exact-cover threshold-1 tuples exist"},
        "single_cycle_check": {
            "row_configuration_tuples_enumerated": len(single_tuples),
            "row_preserving_exact_cover_tuples": len(single_exact),
            "no_disjoint_pair_partner_for_A_full_state": True,
            "original_threshold_2_schedule_exists": True},
        "limits": [
            "Only the specified six-machine and existing two-machine instances were checked.",
            "The proof of the general forest theorem is analytic, not inferred from this run.",
            "No hardness, approximation lower bound, or minimality is claimed."]}
    output = HERE / "exact_kernel_output.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "output": str(output),
                      "pair_laws": 15, "global_tuples": 64,
                      "row_preserving_schedule_states": 8,
                      "pair_support_compatible_states": 0,
                      "two_component_joint_checks": 3,
                      "single_cycle_local_tuples": 4}, ensure_ascii=False))


if __name__ == "__main__":
    main()
