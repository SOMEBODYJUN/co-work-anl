#!/usr/bin/env python3
"""Exact fixed-size parametric K2+full-local-law certificate audit.

Pure Fraction; no SDP/LP solver and no external file dependencies.
The true matrix has OPT=1; only the stated same-point pullback fails.
"""
import argparse
import itertools
import json
from fractions import Fraction as F


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, F()) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(coefficient, polynomial):
    return {m: coefficient*c for m, c in polynomial.items() if coefficient*c}


def multiply(left, right):
    result = {}
    for m, c in left.items():
        for n, d in right.items():
            product = m | n
            result[product] = result.get(product, F()) + c*d
    return {m: c for m, c in result.items() if c}


ONE = {frozenset(): F(1)}
ZERO = {}
BITS = [{frozenset({i}): F(1)} for i in range(3)]
COMP = [add(ONE, scale(-1, b)) for b in BITS]
MOMENT = [F(1), F(3, 10), F(3, 80), F(-1, 160)]


def expectation(polynomial):
    return sum((coefficient*MOMENT[len(monomial)]
                for monomial, coefficient in polynomial.items()), F())


def evaluate(polynomial, bits):
    return sum((c*int(all(bits.get(i, 0) for i in m))
                for m, c in polynomial.items()), F())


def gram(basis, weight=ONE):
    return [[expectation(multiply(weight, multiply(p, q))) for q in basis] for p in basis]


def positive_ldl(matrix):
    current = [row[:] for row in matrix]
    pivots = []
    while current:
        pivot = current[0][0]
        assert pivot > 0, (len(current), pivot)
        pivots.append(pivot)
        current = [[current[i][j] - current[i][0]*current[0][j]/pivot
                    for j in range(1, len(current))]
                   for i in range(1, len(current))]
    return pivots


def row_bit_law(bit_indices):
    if len(bit_indices) == 0:
        return [({}, F(1))]
    if len(bit_indices) == 1:
        i, = bit_indices
        return [({i: 0}, F(7, 10)), ({i: 1}, F(3, 10))]
    assert len(bit_indices) == 2
    i, j = bit_indices
    return [({i: 0, j: 0}, F(35, 80)),
            ({i: 1, j: 0}, F(21, 80)),
            ({i: 0, j: 1}, F(21, 80)),
            ({i: 1, j: 1}, F(3, 80))]


def audit(c=F(3, 4)):
    assert 0 < c < 1
    target, epsilon = 1+c, 1-c
    menu = {
        "M": [[("u", c), ("v", 1-c)], [("r", 1-c), ("s", c)]],
        "Hu": [[("u", F(1))], [("wu", F(1))]],
        "Hv": [[("v", F(1))], [("wv", F(1))]],
        "Hr": [[("r", F(1))], [("wr", F(1))]],
        "Hs": [[("s", F(1))], [("ws", F(1))]],
    }
    selectors = {"M": [BITS[0], COMP[0]],
                 "Hu": [COMP[1], BITS[1]],
                 "Hv": [ZERO, ONE], "Hr": [ZERO, ONE],
                 "Hs": [BITS[2], COMP[2]]}
    exports = {("M", 0, "u"): BITS[1], ("M", 0, "v"): ONE,
               ("M", 1, "r"): ONE, ("M", 1, "s"): COMP[2],
               ("Hu", 0, "u"): COMP[1], ("Hu", 1, "wu"): BITS[1],
               ("Hv", 0, "v"): ZERO, ("Hv", 1, "wv"): ONE,
               ("Hr", 0, "r"): ZERO, ("Hr", 1, "wr"): ONE,
               ("Hs", 0, "s"): BITS[2], ("Hs", 1, "ws"): COMP[2]}
    images, times, machine_endpoints, jobs = {}, {}, {}, {}

    def endpoint(job, machine, time, polynomial):
        name = (job, machine)
        images[name], times[name] = polynomial, time
        machine_endpoints.setdefault(machine, []).append(name)
        jobs.setdefault(job, []).append(name)

    for group, states in menu.items():
        for state, incidences in enumerate(states):
            private = f"private:{group}:{state}"
            endpoint(f"selector:{group}", private, F(1), selectors[group][state])
            assert sum((p for _, p in incidences), F()) == 1
            for resource, coefficient in incidences:
                job = f"inc:{group}:{state}:{resource}"
                export = exports[group, state, resource]
                endpoint(job, private, coefficient, add(ONE, scale(-1, export)))
                endpoint(job, f"resource:{resource}", F(1), export)
    assert (len(machine_endpoints), len(jobs), len(images)) == (18, 17, 34)
    for endpoints in jobs.values():
        assert add(*(images[e] for e in endpoints)) == ONE
        assert all(not multiply(images[e], images[f])
                   for e, f in itertools.combinations(endpoints, 2))
    for polynomial in images.values():
        assert multiply(polynomial, polynomial) == polynomial
    bit_basis = [ONE] + BITS + [multiply(BITS[i], BITS[j])
                                for i, j in itertools.combinations(range(3), 2)]
    pivots = positive_ldl(gram(bit_basis))
    assert pivots == [F(1), F(21, 100), F(63, 320), F(7, 40),
                      F(7, 256), F(7, 288), F(7, 384)]
    affine_basis = [ONE] + BITS
    cfgs, row_dependencies, localizer_pivots = {}, {}, {}
    moments_checked = 0
    patterns_checked = 0
    for machine, endpoints in machine_endpoints.items():
        dependencies = sorted({i for e in endpoints for m in images[e] for i in m})
        assert len(dependencies) <= 2
        row_dependencies[machine] = dependencies
        load = add(*(scale(times[e], images[e]) for e in endpoints))
        slack = add(scale(target, ONE), scale(-1, load))
        localizer_pivots[machine] = positive_ldl(gram(affine_basis, slack))
        # Establish the nonnegative literal identity used for all rational c.
        if machine == "private:M:0":
            assert slack == add(COMP[0], scale(c, BITS[1]))
        elif machine == "private:M:1":
            assert slack == add(BITS[0], scale(c, COMP[2]))
        else:
            # Every other load is constant one or one literal.
            assert load == ONE or load in BITS or load in COMP
        records = {}
        for bits, probability in row_bit_law(dependencies):
            config = tuple(e for e in endpoints if evaluate(images[e], bits) == 1)
            assert all(evaluate(images[e], bits) in [0, 1] for e in endpoints)
            records[config] = records.get(config, F()) + probability
        assert sum(records.values(), F()) == 1
        assert all(p >= 0 for p in records.values())
        assert all(sum((times[e] for e in config), F()) <= target for config in records)
        # All square-free monomials, with no local-degree truncation.
        for subset_size in range(len(endpoints)+1):
            for subset in itertools.combinations(endpoints, subset_size):
                polynomial = ONE
                for e in subset:
                    polynomial = multiply(polynomial, images[e])
                literal_probability = sum((p for config, p in records.items()
                                           if set(subset).issubset(config)), F())
                assert expectation(polynomial) == literal_probability
                moments_checked += 1
        # Exact full membership patterns; these also cover row complements.
        for assignment in itertools.product(range(2), repeat=len(endpoints)):
            polynomial = ONE
            intended_config = set()
            for e, indicator in zip(endpoints, assignment):
                polynomial = multiply(polynomial, images[e] if indicator
                                      else add(ONE, scale(-1, images[e])))
                if indicator:
                    intended_config.add(e)
            probability = sum((p for config, p in records.items()
                               if set(config) == intended_config), F())
            assert expectation(polynomial) == probability >= 0
            patterns_checked += 1
        cfgs[machine] = [{"members": list(config), "probability": str(p),
                          "load": str(sum((times[e] for e in config), F()))}
                         for config, p in records.items()]
    claim_u = multiply(BITS[0], BITS[1])
    claim_v = BITS[0]
    quality = add(scale(c, claim_u), scale(1-c, claim_v), scale(-epsilon, BITS[0]))
    assert quality == scale(c, multiply(BITS[0], BITS[1]))
    negative_entry = expectation(multiply(claim_u, BITS[2]))
    negative_quality = expectation(multiply(quality, BITS[2]))
    assert negative_entry == F(-1, 160) and negative_quality == -c/160
    # All original jobs are checked in a true makespan-one assignment.
    selected = {"M": 0, "Hu": 1, "Hv": 1, "Hr": 0, "Hs": 0}
    actual, actual_load = {}, {m: F() for m in machine_endpoints}
    for job, endpoints in jobs.items():
        if job.startswith("selector:"):
            group = job.split(":")[1]
            machine = f"private:{group}:{selected[group]}"
        else:
            _, group, state, resource = job.split(":")
            machine = (f"resource:{resource}" if int(state) == selected[group]
                       else f"private:{group}:{state}")
        assert (job, machine) in endpoints
        actual[job] = machine
        actual_load[machine] += times[job, machine]
    assert len(actual) == 17 and max(actual_load.values()) == 1
    return {"scope": "full-local-row-law K2 certificate, direct canonical pullback fails; actual OPT=1",
            "c": str(c), "T": str(target), "epsilon": str(epsilon),
            "machines": len(machine_endpoints), "jobs": len(jobs),
            "finite_endpoints": len(images),
            "global_M2_pullback_basis_size": len(bit_basis),
            "global_original_degree_two_squarefree_monomials": 1+34+34*33//2,
            "global_M2_positive_pivots": list(map(str, pivots)),
            "all_18_raw_affine_localizers_exact_PD_at_this_c": True,
            "outer_private_localizer_pivots": {
                key: list(map(str, localizer_pivots[key]))
                for key in ["private:M:0", "private:M:1"]},
            "maximum_row_bit_dependencies": max(map(len, row_dependencies.values())),
            "all_local_squarefree_moments_checked": moments_checked,
            "all_local_full_membership_patterns_checked": patterns_checked,
            "row_CONFIG_full_laws": cfgs,
            "negative_canonical_claim_state_entry": str(negative_entry),
            "negative_canonical_quality_state_lift": str(negative_quality),
            "actual_complete_assignment": actual,
            "actual_schedule_peak": str(max(actual_load.values())),
            "full_matrix_all_assignments_enumerated": False,
            "global_M3_or_global_literal_nonnegativity_claimed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", default="3/4")
    args = parser.parse_args()
    print(json.dumps(audit(F(args.c)), indent=2))
