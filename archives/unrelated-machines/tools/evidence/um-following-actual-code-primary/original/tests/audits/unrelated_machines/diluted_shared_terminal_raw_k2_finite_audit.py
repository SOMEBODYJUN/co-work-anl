"""Author finite audit of k=2 local frames; not a full expanded-input K2 audit.

Enumerates the H/Q assignments directly, matches original B-row first/pair
moments against the five-class CONFIG list, and uses exact rational LDL on
all one-component affine endpoint features plus the selector regime.
The theorem's dimension-free proof, not this finite check, covers arbitrary
other-component affine contexts and arbitrary k.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json
from math import factorial
from pathlib import Path


def encode_fraction(value):
    return str(value)


def generate_states(k, ell, count):
    a = F(1, count)
    dimension = 2 + k * ell + ell * k * k

    def f_index(j, b):
        return 2 + j * ell + b

    def e_index(b, j, t):
        return 2 + k * ell + (b * k + j) * k + t

    states = []
    injection_count = factorial(ell) // factorial(ell - k)
    for injection in permutations(range(ell), k):
        support = {0, 1}
        support.update(f_index(j, b) for j, b in enumerate(injection))
        states.append((a / injection_count, support, "H"))
    states.append(((1 - a) / 2, {0}, "Qzero"))
    for j in range(k):
        for b in range(ell):
            for perm in permutations(range(k)):
                support = {0, f_index(j, b)}
                support.update(e_index(b, h, t) for h, t in enumerate(perm))
                weight = (1 - a) / (4 * k * ell * factorial(k))
                states.append((weight, support, "Qunit"))
    for b in range(ell):
        for j in range(k):
            for t in range(k):
                states.append(((1 - a) / (4 * ell * k * k),
                               {0, e_index(b, j, t)}, "Qnoise"))
    assert sum(weight for weight, _, _ in states) == 1
    return states, dimension, f_index, e_index


def outer_add(matrix, vector, weight):
    support = [(index, value) for index, value in enumerate(vector) if value]
    for i, x in support:
        for j, y in support:
            matrix[i][j] += weight * x * y


def exact_ldl(matrix):
    n = len(matrix)
    lower = [[F(0) for _ in range(n)] for _ in range(n)]
    diagonal = []
    for i in range(n):
        lower[i][i] = 1
        pivot = matrix[i][i] - sum(lower[i][h] ** 2 * diagonal[h]
                                   for h in range(i))
        assert pivot > 0, (i, pivot)
        diagonal.append(pivot)
        for j in range(i + 1, n):
            residual = matrix[j][i] - sum(lower[j][h] * lower[i][h] * diagonal[h]
                                          for h in range(i))
            lower[j][i] = residual / pivot
    for i in range(n):
        for j in range(n):
            replay = sum(lower[i][h] * diagonal[h] * lower[j][h]
                         for h in range(min(i, j) + 1))
            assert replay == matrix[i][j]
    return diagonal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    k = 2
    ell = 2 * k * k
    count = 1 + 60 * ell * k ** 4
    a = F(1, count)
    states, dimension, f_index, e_index = generate_states(k, ell, count)
    row = 0
    gram = [[F(0) for _ in range(dimension)] for _ in range(dimension)]
    moments = [[F(0) for _ in range(2 * k)] for _ in range(2 * k)]
    first = [F(0) for _ in range(2 * k)]
    conditional_gap = {"H": F(0), "Q": F(0)}
    conditional_mass = {"H": F(0), "Q": F(0)}
    for weight, support, label in states:
        incoming = [int(f_index(j, row) in support) for j in range(k)]
        homes = [1 - sum(e_index(row, j, t) in support for t in range(k))
                 for j in range(k)]
        assert sum(incoming) <= 1
        load = sum(incoming) + F(sum(homes), k)
        gap = 1 + F(1, k) - load
        feature = [int(index in support) for index in range(dimension)]
        outer_add(gram, feature, weight * gap)
        local = incoming + homes
        for i, value in enumerate(local):
            first[i] += weight * value
        outer_add(moments, local, weight)
        regime = "H" if label == "H" else "Q"
        conditional_gap[regime] += weight * gap
        conditional_mass[regime] += weight
    p = a * k / ell
    b0 = c0 = (1 - a) / (4 * ell)
    configs = []
    for j in range(k):
        for h in range(k):
            vector = [int(t == j) for t in range(k)] + [int(t == h) for t in range(k)]
            configs.append((p / k, vector))
        configs.append(((b0 - (k - 1) * p) / k,
                        [int(t == j) for t in range(k)] + [0] * k))
    configs.append((p, [0] * (2 * k)))
    for h in range(k):
        configs.append(((c0 - k * p) / k,
                        [0] * k + [int(t != h) for t in range(k)]))
    configs.append((1 - b0 - c0 + (k - 2) * p, [0] * k + [1] * k))
    assert sum(weight for weight, _ in configs) == 1
    check_first = [F(0) for _ in first]
    check_pair = [[F(0) for _ in first] for _ in first]
    for weight, vector in configs:
        assert weight >= 0
        assert sum(vector[:k]) + F(sum(vector[k:]), k) <= 1 + F(1, k)
        for j, value in enumerate(vector):
            check_first[j] += weight * value
        outer_add(check_pair, vector, weight)
    assert check_first == first
    assert check_pair == moments
    pivots = exact_ldl(gram)
    matrix_bytes = json.dumps([[str(value) for value in row] for row in gram],
                              separators=(",", ":")).encode()
    payload = {
        "scope": "author k=2 one-component exact affine Gram/CONFIG frame only",
        "not_claimed": "full expanded-input M2/contexts enumeration or general-k software proof",
        "k": k, "L": ell, "M": count, "dimension": dimension,
        "enumerated_weighted_states": len(states),
        "B_config_first_and_pair_match": True,
        "B_config_count": len(configs),
        "B_config_class_masses": [str(k*p), str(b0-(k-1)*p), str(p),
                                   str(c0-k*p), str(1-b0-c0+(k-2)*p)],
        "conditional_mean_gaps": {key: str(conditional_gap[key] / conditional_mass[key])
                                   for key in conditional_gap},
        "exact_LDL_positive_pivots": [str(value) for value in pivots],
        "exact_LDL_replay": True,
        "gram_canonical_json_sha256": sha256(matrix_bytes).hexdigest(),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"k": k, "dimension": dimension, "states": len(states),
                      "config_match": True, "LDL_positive": True,
                      "output_sha256": sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
