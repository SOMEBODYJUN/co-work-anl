"""独立逐资源核验线性次数构造的全部小相位与类内时钟。

Finite exact checks only: these do not enumerate the enormous theorem games.
The literal resource construction does not call the author's compressed formulas.
Run from the repository root; --output creates a NEW file and refuses overwrite.
"""

from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json
import platform
import shlex
import sys


ROOT = Path(__file__).resolve().parents[4]
PROOF = "research/current/weighted_congestion/linear_degree_allstate_lower_bound.md"
REVIEWED_SHA256 = "04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33"
CANDIDATE_SHA256 = "c1f846520baa918b5506013e7a2704fb059e64f1f03c6699c0183b799ee0029c"


def front_bits(phase, size):
    if phase < size:
        return tuple(int(index < phase) for index in range(size))
    return tuple(int(index >= phase - size) for index in range(size))


def literal_resource_actions(size, window, light_weight, negative_orientation):
    actions = {(kind, index): [set(), set()]
               for index in range(size) for kind in range(2)}
    for index in range(size):
        heavy = (0, index)
        actions[heavy][0].add((index, 0))
        actions[heavy][1].add((index, 1))
        for offset in range(window):
            light = (1, (index + offset) % size)
            side = int((light[1], light[0]) > (heavy[1], heavy[0]))
            side ^= int(negative_orientation)
            actions[light][0].add((index, side))
            actions[light][1].add((index, 1 - side))
    weights = {(0, index): F(1) for index in range(size)}
    weights.update({(1, index): light_weight for index in range(size)})
    assert all(pair[0] and pair[1] and not pair[0] & pair[1]
               for pair in actions.values())
    return actions, weights


def literal_deviation_costs(actions, weights, state, degree, player):
    loads = {}
    for user in actions:
        for resource in actions[user][state[user]]:
            loads[resource] = loads.get(resource, F()) + weights[user]
    before = sum((loads[resource] ** degree
                  for resource in actions[player][state[player]]), F())
    for resource in actions[player][state[player]]:
        loads[resource] -= weights[player]
    for resource in actions[player][1 - state[player]]:
        loads[resource] = loads.get(resource, F()) + weights[player]
    after = sum((loads[resource] ** degree
                 for resource in actions[player][1 - state[player]]), F())
    return before, after


def phase_state(heavy_phase, light_phase, size):
    state = {(0, index): bit
             for index, bit in enumerate(front_bits(heavy_phase, size))}
    state.update({(1, index): bit
                  for index, bit in enumerate(front_bits(light_phase, size))})
    return state


def exact_power_sums(count, degree):
    sums = []
    for power in range(degree + 1):
        numerator = ((count + 1) ** (power + 1) - 1
                     - sum(comb(power + 1, lower) * sums[lower]
                           for lower in range(power)))
        assert numerator % (power + 1) == 0
        sums.append(numerator // (power + 1))
    return sums


def audit():
    counts = {"neighbor_phase_pairs": 0, "return_phase_pairs": 0,
              "clock_states": 0, "power_sum_crosschecks": 0}
    for size in range(2, 9):
        for window in range(1, size + 1):
            actions, weights = literal_resource_actions(
                size, window, F(1, window), True)
            for degree in (1, 2, 4):
                cap = sum(((1 + F(rank, window)) ** degree
                           for rank in range(1, window + 1)), F())
                for heavy_phase, light_phase in product(range(2 * size), repeat=2):
                    state = phase_state(heavy_phase, light_phase, size)
                    relative = (light_phase - heavy_phase) % (2 * size)
                    zeros = (window - min(relative, window) if relative <= size
                             else min(relative - size, window))
                    expected = ((1 + F(zeros, window)) ** degree,
                                (2 - F(zeros, window)) ** degree)
                    assert literal_deviation_costs(
                        actions, weights, state, degree,
                        (0, heavy_phase % size)) == expected
                    reverse_relative = (relative + 1) % (2 * size)
                    reverse_zeros = (
                        window - min(reverse_relative, window)
                        if reverse_relative <= size
                        else min(reverse_relative - size, window))
                    backward = ((2 - F(reverse_zeros, window)) ** degree,
                                (1 + F(reverse_zeros, window)) ** degree)
                    assert literal_deviation_costs(
                        actions, weights, state, degree,
                        (0, (heavy_phase - 1) % size)) == backward
                    for endpoint in (light_phase % size, (light_phase - 1) % size):
                        assert max(literal_deviation_costs(
                            actions, weights, state, degree, (1, endpoint))) <= cap
                    counts["neighbor_phase_pairs"] += 1

    for size in range(2, 12):
        for degree in (2, 3, 5):
            epsilon = F(1, degree * size)
            actions, weights = literal_resource_actions(size, size, epsilon, False)
            for heavy_phase, light_phase in product(range(2 * size), repeat=2):
                state = phase_state(heavy_phase, light_phase, size)
                relative = (heavy_phase - light_phase) % (2 * size)
                shares = [int(front_bits(relative, size)[(-rank) % size]
                              == int(rank == 0)) for rank in range(size)]
                before = sum((((size - rank) * epsilon + shares[rank]) ** degree
                              for rank in range(size)), F())
                after = sum((((rank + 1) * epsilon + 1 - shares[rank]) ** degree
                             for rank in range(size)), F())
                assert literal_deviation_costs(
                    actions, weights, state, degree,
                    (1, light_phase % size)) == (before, after)
                relative = (relative + 1) % (2 * size)
                shares = [int(front_bits(relative, size)[(-rank) % size]
                              == int(rank == 0)) for rank in range(size)]
                before = sum((((size - rank) * epsilon + shares[rank]) ** degree
                              for rank in range(size)), F())
                after = sum((((rank + 1) * epsilon + 1 - shares[rank]) ** degree
                             for rank in range(size)), F())
                assert literal_deviation_costs(
                    actions, weights, state, degree,
                    (1, (light_phase - 1) % size)) == (after, before)
                counts["return_phase_pairs"] += 1

    def clock_fires(triple, state):
        return state[triple[0]] == state[triple[2]] != state[triple[1]]

    for size in range(3, 13):
        triples = [(0, middle, last) for middle in range(1, size)
                   for last in range(middle + 1, size)]
        for state in product((0, 1), repeat=size):
            is_front = sum(state[index] != state[index - 1]
                           for index in range(1, size)) <= 1
            assert any(clock_fires(triple, state) for triple in triples) == (not is_front)
            if not is_front:
                mover = next(index for index in range(1, size)
                             if state[index] != state[0])
                changed = list(state)
                changed[mover] = state[0]
                assert not any(clock_fires(triple, changed)
                               for triple in triples if mover in triple)
            counts["clock_states"] += 1

    for count in range(1, 10):
        for degree in range(8):
            assert exact_power_sums(count, degree)[degree] == sum(
                rank ** degree for rank in range(1, count + 1))
            counts["power_sum_crosschecks"] += 1
    parameter_cases = []
    for degree in (20, 21, 32, 64):
        alpha = F(degree, 10)
        window = degree ** 4
        classes = (degree * degree - 1).bit_length() + 1
        size = window ** (classes - 1) // degree
        epsilon = F(1, window ** (classes - 1))
        h = 2 ** degree - alpha
        sums = exact_power_sums(window, degree)
        x = sum((comb(degree, power) * F(sums[power], window ** power)
                 for power in range(degree + 1)), F())
        y = F(sums[degree], window ** degree)
        loss = alpha * x - y
        sums = exact_power_sums(size, degree)
        u = sum((comb(degree, power) * epsilon ** power * sums[power]
                 for power in range(degree + 1)), F())
        v = epsilon ** degree * sums[degree]
        j = alpha * (1 + F(1, degree)) ** degree - 1
        z = u - alpha * v
        assert F(4, window) <= h / loss <= F(40, window)
        assert z / j > F(3, degree * degree) / epsilon
        amplitude = (2 * loss / h) ** (classes - 2)
        return_amplitude = h / (2 * j)
        assert return_amplitude * z > 3 * amplitude * loss
        parameter_cases.append({"p": degree, "classes": classes, "status": "passed"})
    degree = 2 ** 20
    classes = (degree * degree - 1).bit_length() + 1
    assert 3 ** degree >= (1 << degree) * classes * degree ** (12 * classes - 12)
    return {"status": "all literal exact assertions passed", "counts": counts,
            "parameter_cases": parameter_cases,
            "p0_conservative_clock_budget": {
                "p": degree, "classes": classes,
                "checked_integer_inequality": "3^p >= 2^p m p^(12m-12)",
                "status": "passed"}}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="NEW JSON file; existing paths are refused")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error("--output already exists; frozen evidence must not be overwritten")
    result = audit()
    code = Path(__file__).resolve()
    proof = ROOT / PROOF
    result["metadata"] = {
        "command": shlex.join(["python3", str(code.relative_to(ROOT)), *sys.argv[1:]]),
        "python_version": platform.python_version(),
        "python_build": sys.version,
        "code_path": code.relative_to(ROOT).as_posix(),
        "code_sha256": sha256(code.read_bytes()).hexdigest(),
        "reviewed_proof_path": PROOF,
        "reviewed_proof_sha256": REVIEWED_SHA256,
        "current_proof_sha256": sha256(proof.read_bytes()).hexdigest(),
        "initial_candidate_sha256": CANDIDATE_SHA256,
        "precision": {"arithmetic": "integer and fractions.Fraction", "tolerance": 0},
        "randomness": "none", "seed": None,
        "inputs": {
            "neighbor": {"N_inclusive": [2, 8], "K": "all integers 1..N",
                         "degree": [1, 2, 4], "weight_heavy": "1",
                         "weight_light": "1/K", "phases": "all (2N)^2 pairs"},
            "return": {"N_inclusive": [2, 11], "degree": [2, 3, 5],
                       "K": "N", "epsilon": "1/(degree*N)",
                       "phases": "all (2N)^2 pairs"},
            "clock": {"N_inclusive": [3, 12], "states": "all 2^N bitstrings"},
            "power_sum_crosscheck": {"N_inclusive": [1, 9], "degree_inclusive": [0, 7]},
            "full_parameter_bounds_p": [20, 21, 32, 64],
            "conservative_clock_budget_p": 2 ** 20},
        "scope": "Finite formula/index/repair checks; not an enumeration of the theorem games or a replacement for the general proof."}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(rendered)
        print(json.dumps({"status": result["status"], "output": str(args.output),
                          "counts": result["counts"],
                          "code_sha256": result["metadata"]["code_sha256"]},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
