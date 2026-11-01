#!/usr/bin/env python3
"""Exact Fraction audit for UM-PREFIX-ATOMIC-DECODING-v1."""
from fractions import Fraction
from itertools import product


def all_assignments(edges):
    return list(product(*[range(len(E)) for E in edges]))


def loads(edges, assignment, machine_count):
    out = [Fraction(0) for _ in range(machine_count)]
    for j, k in enumerate(assignment):
        i, p = edges[j][k]
        out[i] += p
    return out


def evaluator(edges, weights):
    def eval_prefix(prefix):
        return sum((w for assignment, w in weights.items()
                    if all(assignment[j] == k for j, k in prefix.items())), Fraction(0))
    return eval_prefix


def greedy(edges, eval_prefix):
    prefix = {}
    for j, endpoints in enumerate(edges):
        positive = []
        for k in range(len(endpoints)):
            value = eval_prefix({**prefix, j: k})
            if value > 0:
                positive.append((k, value))
        if not positive:
            return None
        prefix[j] = min(positive)[0]
    return tuple(prefix[j] for j in range(len(edges)))


def check_dirac_and_uniform():
    edges = [[(0, Fraction(1)), (1, Fraction(1))],
             [(0, Fraction(1)), (1, Fraction(1))]]
    feasible = [(0, 1), (1, 0)]
    uniform = {a: Fraction(1, 2) for a in feasible}
    got = greedy(edges, evaluator(edges, uniform))
    assert got in feasible and max(loads(edges, got, 2)) <= 1

    edges0 = [[(0, Fraction(0))], [(0, Fraction(0))]]
    got0 = greedy(edges0, evaluator(edges0, {(0, 0): Fraction(1)}))
    assert got0 == (0, 0) and max(loads(edges0, got0, 1)) == 0


def check_infeasible_atomic_boundary():
    edges = [[(0, Fraction(1)), (1, Fraction(1))] for _ in range(3)]
    atoms = all_assignments(edges)
    feasible_atoms = [a for a in atoms if max(loads(edges, a, 2)) <= 1]
    assert len(atoms) == 8 and not feasible_atoms
    # A localizer would force every nonnegative atomic weight to zero,
    # contradicting the one-hot normalization sum_sigma pi(sigma)=1.


def check_heterogeneous_dirac():
    edges = [[(0, Fraction(1, 3)), (1, Fraction(2, 3)), (2, Fraction(1, 2))]
             for _ in range(4)]
    feasible = [a for a in all_assignments(edges)
                if max(loads(edges, a, 3)) <= 1]
    assert feasible
    for atom in feasible[:5]:
        got = greedy(edges, evaluator(edges, {atom: Fraction(1)}))
        assert got == atom and max(loads(edges, got, 3)) <= 1


if __name__ == "__main__":
    check_dirac_and_uniform()
    check_infeasible_atomic_boundary()
    check_heterogeneous_dirac()
    print("prefix atomic decoding exact audit: ok")
