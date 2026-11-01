#!/usr/bin/env python3
"""Exact finite audits of the prefix precision extension; no general Gen/verify."""

from fractions import Fraction as F
from itertools import product
from math import prod
from random import Random
from pathlib import Path
import hashlib
import json
import platform

REPO = Path(__file__).resolve().parents[3]
RNG = Random(7711803)


def prefix_mass(law, prefix):
    return sum((w for atom, w in law.items() if atom[: len(prefix)] == prefix), F(0))


def noisy_max(law, degrees, alpha, offsets=None, choices_by_job=None):
    prefix = ()
    q_previous = F(1)
    Q = 1
    trace = []
    for j, d in enumerate(degrees):
        choices = range(d) if choices_by_job is None else choices_by_job[j]
        assert len(choices) == d
        children = [prefix + (choice,) for choice in choices]
        true = [prefix_mass(law, child) for child in children]
        if offsets is None:
            err = [RNG.choice([-1, 0, 1]) * alpha for child in children]
        else:
            err = [offsets(child, alpha) for child in children]
        approx = [x + e for x, e in zip(true, err)]
        selected = max(range(d), key=lambda c: approx[c])
        prefix = children[selected]
        q = true[selected]
        assert sum(true, F(0)) == q_previous
        assert q >= (q_previous - 2 * alpha * (d - 1)) / d
        Q *= d
        assert q >= (1 - 2 * alpha * (Q - 1)) / Q
        trace.append((q, Q))
        q_previous = q
    return prefix, prefix_mass(law, prefix), trace


def random_law(degrees):
    atoms = list(product(*(range(d) for d in degrees)))
    weights = [RNG.randrange(10) for _ in atoms]
    if not any(weights):
        weights[0] = 1
    total = sum(weights)
    return dict(zip(atoms, (F(w, total) for w in weights)))


def max_mass_audit():
    runs = 0
    for _ in range(500):
        n = RNG.randrange(1, 7)
        degrees = [RNG.randrange(1, 4) for _ in range(n)]
        N = prod(degrees)
        law = random_law(degrees)
        alpha = F(1, 4 * N)
        atom, weight, trace = noisy_max(law, degrees, alpha)
        assert weight >= F(1, 2 * N)
        runs += 1
    for k in range(1, 9):
        N = 2**k
        atoms = list(product(range(2), repeat=k))
        law = {atom: F(int(any(atom)), N - 1) for atom in atoms}
        alpha = F(1, 2 * (N - 1))

        def offsets(child, a):
            if not any(child):
                return a
            if not any(child[:-1]) and child[-1] == 1:
                return -a
            return F(0)

        atom, weight, trace = noisy_max(law, [2] * k, alpha, offsets)
        assert atom == (0,) * k
        assert weight == 0
        assert weight == (1 - 2 * alpha * (N - 1)) / N
    sharp_interval_runs = 0
    for degrees in [[2], [2, 2, 2], [3, 2], [1, 3, 1, 2], [2, 3, 2, 1], [3, 3, 3]]:
        N = prod(degrees)
        critical = F(1, 2 * (N - 1))
        atoms = list(product(*(range(d) for d in degrees)))
        target = (0,) * len(degrees)
        for alpha in [F(0), critical / 16, critical / 2, F(1, 4 * N), critical]:
            target_weight = (1 - 2 * alpha * (N - 1)) / N
            other_weight = (1 + 2 * alpha) / N
            law = {atom: target_weight if atom == target else other_weight for atom in atoms}
            assert all(w >= 0 for w in law.values())
            assert sum(law.values(), F(0)) == 1

            def offsets(child, a):
                return a if not any(child) else -a

            atom, weight, trace = noisy_max(law, degrees, alpha, offsets)
            assert atom == target
            assert weight == target_weight
            for q, Q in trace:
                assert q == (1 - 2 * alpha * (Q - 1)) / Q
            sharp_interval_runs += 1
    return {"random_trees": runs, "zero_mass_sharp_depths": list(range(1, 9)), "full_interval_sharp_runs": sharp_interval_runs, "full_interval_degree_lists": [[2], [2, 2, 2], [3, 2], [1, 3, 1, 2], [2, 3, 2, 1], [3, 3, 3]]}


def dilution_audit():
    records = []
    for k in range(13):
        N = 2**k
        w = F(1, N)
        load = F(3, 4) + F(3, 4)
        residual = (1 - load) * w
        tau = F(1, 2 * N)
        assert residual == -tau
        assert load == 1 + N * tau
        records.append({"dummy_jobs": k, "N": N, "tau": str(tau)})
    return records


def loads(atom, processing):
    m = len(processing)
    return [sum((processing[i][j] for j, choice in enumerate(atom) if choice == i), F(0)) for i in range(m)]


def common_denominator(processing, threshold):
    denominators = [threshold.denominator] + [p.denominator for row in processing for p in row if p is not None]
    D = prod(denominators)
    assert D.bit_length() <= sum(d.bit_length() for d in denominators)
    return D


def grid_audit():
    cases = []
    large = 10**83 + 53
    for B, bad_p in [(F(0), F(1, large)), (F(7, 11), F(7, 11) + F(1, large)), (F(1), F(3, 2))]:
        processing = [[B, F(0)], [bad_p, F(0)]]
        degrees = [2, 2]
        N = 4
        D = common_denominator(processing, B)
        tau = F(1, 4 * D * N)
        excess = bad_p - B
        bad_atom_weight = tau / (2 * excess)
        assert 0 < bad_atom_weight < F(1, 4)
        law = {(0, 0): F(1, 2) - bad_atom_weight,
               (0, 1): F(1, 2) - bad_atom_weight,
               (1, 0): bad_atom_weight,
               (1, 1): bad_atom_weight}
        assert sum(law.values(), F(0)) == 1
        for atom, w in law.items():
            for load in loads(atom, processing):
                assert (load - B) * D == int((load - B) * D)
                assert (B - load) * w >= -tau
        for _ in range(40):
            atom, w, trace = noisy_max(law, degrees, F(1, 4 * N))
            assert w >= F(1, 2 * N)
            for load in loads(atom, processing):
                assert load <= B + 2 * N * tau
                assert load <= B
        cases.append({"B": str(B), "D_bits": D.bit_length(), "tau_denominator_bits": tau.denominator.bit_length(), "runs": 40})

    # Explicitly check the polynomial precision bit count without enumerating leaves.
    n = 1000
    N = 2**n
    alpha = F(1, 4 * N)
    D = 3**n
    tau = F(1, 4 * D * N)
    assert alpha.denominator.bit_length() == n + 3
    assert tau.denominator.bit_length() <= D.bit_length() + N.bit_length() + 2
    return {"grid_cases": cases, "large_implicit_tree": {"n": n, "N_bits": N.bit_length(), "alpha_denominator_bits": alpha.denominator.bit_length(), "tau_denominator_bits": tau.denominator.bit_length()}}


def matrix_multiply(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0)) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(row) for row in zip(*A)]


def congruence(A, C):
    return matrix_multiply(transpose(C), matrix_multiply(A, C))


def add_scaled(A, B, scale):
    return [[a + scale * b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]


def psd2(A):
    assert A[0][1] == A[1][0]
    return A[0][0] >= 0 and A[1][1] >= 0 and A[0][0] * A[1][1] >= A[0][1] ** 2


def relative_gram_audit():
    C = [[F(1), F(2)], [F(3), F(7)]]
    for k in [1, 5, 20, 100]:
        r = F(1, 2**k)
        M = [[1 - r, F(0)], [F(0), r]]
        K = [[F(0), F(0)], [F(0), -r]]
        I = [[F(1), F(0)], [F(0), F(1)]]
        assert psd2(add_scaled(K, I, r))
        assert psd2(add_scaled(K, M, F(1)))
        assert not psd2(add_scaled(K, M, F(1, 2)))
        Mc = congruence(M, C)
        Kc = congruence(K, C)
        assert psd2(add_scaled(Kc, Mc, F(1)))
        assert not psd2(add_scaled(Kc, Mc, F(1, 2)))
    return {"rare_weight_exponents": [1, 5, 20, 100], "nonorthogonal_basis": [[1, 2], [3, 7]]}



def boundary_audit():
    # These are promised laws, not a general scheduling feasibility solver.
    fixtures = [
        ([[]], F(0), {(): F(1)}, [], []),
        ([[F(0)]], F(0), {(0,): F(1)}, [1], [[0]]),
        ([[F(1, 17)], [None]], F(1, 17), {(0,): F(1)}, [1], [[0]]),
        ([[None, F(0)], [F(2, 19), None]], F(2, 19), {(1, 0): F(1)}, [1, 1], [[1], [0]]),
    ]
    for processing, T, law, degrees, choices in fixtures:
        N = prod(degrees)
        atom, weight, _ = noisy_max(law, degrees, F(1, 4*N), choices_by_job=choices)
        assert weight > 0 and atom in law
        for j, i in enumerate(atom):
            assert processing[i][j] is not None
        actual = loads(atom, processing)
        assert max(actual, default=F(0)) <= T
        Q = common_denominator(processing, T)
        for load in actual:
            assert ((load-T)*Q).denominator == 1
    return {"fixtures": len(fixtures), "scope": "empty, zero optimum, one available endpoint, unavailable edges; all exact Fraction"}


def main():
    result = {
        "claim": "UM-PREFIX-ATOMIC-FINITE-PRECISION-v1",
        "scope": "Finite exact Fraction audits only; no general certificate generator, no polynomial full-promise verifier, no sound FAIL procedure. Small-law enumeration is an independent audit oracle, not the claimed polynomial decoder.",
        "seed": 7711803,
        "python": platform.python_version(),
        "command": "python3 tests/audits/unrelated_machines/prefix_atomic_finite_precision.py",
        "max_mass": max_mass_audit(),
        "absolute_localizer_dilution": dilution_audit(),
        "grid_exactness": grid_audit(),
        "relative_gram": relative_gram_audit(),
        "boundaries": boundary_audit(),
        "limitations": ["No approximate conservation or approximate root normalization", "No low-degree Gram inference", "No general P,T oracle construction", "No deterministic scheduling conclusion from finite tests alone"]
    }
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["account_sha256"] = hashlib.sha256((REPO / "research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md").read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
