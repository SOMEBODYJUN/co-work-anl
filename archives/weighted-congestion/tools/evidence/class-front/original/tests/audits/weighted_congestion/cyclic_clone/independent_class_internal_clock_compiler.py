"""Literal-resource independent audit of one clock compiler obstruction.

Hard-coded actual resource coefficients; no imports from author or repository.
Finite audits supplement, rather than prove, the general local clock lemma.
"""
from fractions import Fraction as F
from itertools import combinations, product
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

M, N, DEGREE = 3, 4, 8
ALPHA = F(21, 20)
W = (16, 4, 1) * N  # Physical weights are these integers divided by 16.
SPECS = (
    (0, 1, 2, 1, F(196608, 2070241)),
    (0, 2, 1, -1, F(12884901888, 6975757441)),
    (1, 0, 1, 1, F(458752, 390625)),
    (1, 0, 4, -1, F(114688, 1958731377)),
    (1, 2, 2, 1, F(4294967296, 2070241)),
    (2, 0, 3, -1, F(4294967296, 34646314945283)),
    (2, 1, 1, 1, F(17179869184, 390625)),
    (2, 1, 4, -1, F(8589934592, 1958731377)),
)

# Materialize complete resource subsets for both actions of every player.
strategies = [[set(), set()] for _ in W]
resource_test = []
for test, (a, b, length, orientation, coefficient) in enumerate(SPECS):
    for index in range(N):
        rid = len(resource_test)
        resource_test.extend((test, test))
        owner = M * index + a
        memberships = {owner: 0}
        for offset in range(length):
            clone = (index + (a > b) + offset) % N
            user = M * clone + b
            memberships[user] = int(user > owner) ^ int(orientation < 0)
        for player, literal in memberships.items():
            strategies[player][0].add(rid + literal)
            strategies[player][1].add(rid + 1 - literal)
strategies = tuple(tuple(frozenset(action) for action in pair) for pair in strategies)
assert all(x and y and x.isdisjoint(y) for x, y in strategies)
assert len(resource_test) == 64
scaled_coefficients = tuple(s[-1] / 16**DEGREE for s in SPECS)


def profile_costs(bits):
    """Compute costs by explicit resource sets and true deviation loads."""
    loads = [0] * len(resource_test)
    for player, bit in enumerate(bits):
        for resource in strategies[player][bit]:
            loads[resource] += W[player]
    result = []
    for player, bit in enumerate(bits):
        old_terms, new_terms = [0] * len(SPECS), [0] * len(SPECS)
        for resource in strategies[player][bit]:
            old_terms[resource_test[resource]] += loads[resource] ** DEGREE
        for resource in strategies[player][1 - bit]:
            new_terms[resource_test[resource]] += (loads[resource] + W[player]) ** DEGREE
        old = sum((c * v for c, v in zip(scaled_coefficients, old_terms)), F())
        new = sum((c * v for c, v in zip(scaled_coefficients, new_terms)), F())
        result.append((old, new))
    return result


def front_bits(size, phase):
    return tuple(int(j < phase) if phase < size else int(j >= phase - size)
                 for j in range(size))


state, sweep = [0] * len(W), []
for half in range(2):
    for mover in range(len(W)):
        old, post = profile_costs(state)[mover]
        margin = old - ALPHA * post
        assert margin > F(3, 4)
        sweep.append((half, mover, old, post, margin))
        state[mover] ^= 1
assert state == [0] * len(W)
expected_class_margins = (
    F(668952404678020797924570238508829288767787464,
      638047468517767349117246305566039154408203125),
    F(101229878362539180212273, 126720187645370531250000),
    F(2651952901577059953262979194770765518068336861,
      1531313924442641637881391133358493970579687500),
)
for _, mover, _, _, margin in sweep:
    assert margin == expected_class_margins[mover % M]
front_phases = (0, 0, 1)
f = [front_bits(N, x) for x in front_phases]
front = tuple(f[a][j] for j in range(N) for a in range(M))
front_costs = profile_costs(front)
assert all(old - post < -F(1, 2) for old, post in front_costs)
front_upper_bounds = (
    (-F(1, 2), -F(3), -F(3, 4)),
    (-F(6, 5), -F(6, 5), -F(19, 10)),
    (-F(4, 5), -F(8), -F(2)),
    (-F(4), -F(6), -F(7, 5)),
)
for mover, (old, post) in enumerate(front_costs):
    assert old - post < front_upper_bounds[mover // M][mover % M]

all_fronts = {
    tuple(front_bits(N, phase[a])[j] for j in range(N) for a in range(M))
    for phase in product(range(2 * N), repeat=M)
}
exact_pne, strict_pne, alpha_pne, exact_front_pne = [], [], [], []
for state in product((0, 1), repeat=len(W)):
    costs = profile_costs(state)
    if all(old <= post for old, post in costs):
        exact_pne.append(state)
        if state in all_fronts:
            exact_front_pne.append(state)
    if all(old < post for old, post in costs):
        strict_pne.append(state)
    if all(old <= ALPHA * post for old, post in costs):
        alpha_pne.append(state)
assert front in exact_front_pne and front in strict_pne

clock_cases, legal_flip_cases = 0, 0
clock_transitions = {(2, 2): 0, (1, 3): 0}
for size in range(1, 11):
    fronts = {front_bits(size, phase) for phase in range(2 * size)}
    for bits in product((0, 1), repeat=size):
        no_trigger = all(tuple(bits[i] for i in triple) not in ((0, 1, 0), (1, 0, 1))
                         for triple in combinations(range(size), 3))
        assert no_trigger == (bits in fronts)
    for bits in fronts:
        for triple in combinations(range(size), 3):
            literals = (0, 1, 0)
            sides = [bits[u] ^ q for u, q in zip(triple, literals)]
            for k, mover in enumerate(triple):
                old_load = sides.count(sides[k])
                post_load = sides.count(1 - sides[k]) + 1
                pair = (old_load, post_load)
                assert pair in clock_transitions
                clock_transitions[pair] += 1
                clock_cases += 1
                post = list(bits)
                post[mover] ^= 1
                if tuple(post) in fronts:
                    assert pair == (2, 2)
                    legal_flip_cases += 1

# Direct appended-clock audit on the selected strict PNE, for multiple degrees
# and unrelated amplitudes. Each resource pair is fresh and the two fees match.
clock_family_checks = []
for degree in (0, 1, 2, 8, 16):
    costs = [list(pair) for pair in front_costs]
    for a in range(M):
        for clock_index, indices in enumerate(combinations(range(N), 3)):
            triple, literal = tuple(M * i + a for i in indices), (0, 1, 0)
            sides = [front[u] ^ q for u, q in zip(triple, literal)]
            load = [sum((F(W[u], 16) for u, side in zip(triple, sides) if side == r), F())
                    for r in (0, 1)]
            amplitude = F(10 ** (a + clock_index + 2), 7)
            for u, side in zip(triple, sides):
                costs[u][0] += amplitude * load[side]**degree
                costs[u][1] += amplitude * (load[1 - side] + F(W[u], 16))**degree
    assert all(old < post for old, post in costs)
    clock_family_checks.append(degree)

out = {
    'status': 'all exact assertions passed',
    'method': 'independent complete resource-set materialization; integer physical loads over 16; Fraction aggregate fees; no author-core imports',
    'command': [sys.executable, str(Path(__file__).resolve())],
    'frozen_section8_sha256': 'e401464769ee2eae6a0a185e1be43e0e19f3425ef29dc91bb33412731a692512',
    'original_author_fixture_sha256': 'ecef0a5f213f2f87b9731dddd7273ff792dce8fd07679c6590c43e2ceea48951',
    'input_mode': 'eight actual rational resource coefficients hard-coded in this exact source snapshot',
    'degree': DEGREE, 'alpha': str(ALPHA), 'players': len(W), 'resources': len(resource_test),
    'resource_coefficients': [str(s[-1]) for s in SPECS],
    'checked_profiles': 2**len(W), 'checked_product_fronts': len(all_fronts),
    'exact_pne_count': len(exact_pne), 'strict_pne_count': len(strict_pne),
    'alpha_pne_count': len(alpha_pne), 'exact_pne_product_front_count': len(exact_front_pne),
    'strict_cycle_edges': len(sweep), 'minimum_cycle_alpha_margin': str(min(e[-1] for e in sweep)),
    'class_cycle_alpha_margins': list(map(str, expected_class_margins)),
    'front_phases': list(front_phases), 'front_bits': list(front),
    'maximum_front_exact_margin': str(max(old - post for old, post in front_costs)),
    'front_costs': [{'player': u, 'class': u % M, 'clone': u // M, 'old': str(old),
                     'post': str(post), 'exact_margin': str(old - post)}
                    for u, (old, post) in enumerate(front_costs)],
    'clock_geometry_sizes': [1, 10], 'clock_player_flip_cases': clock_cases,
    'legal_front_flip_cases': legal_flip_cases,
    'clock_load_transition_counts': {str(k): v for k, v in clock_transitions.items()},
    'appended_clock_degree_examples': clock_family_checks,
    'limitations': 'Fixed counterexample to universal compilers that only append fresh class-internal same-fee monotone increasing ordered-triple 010/101 pairs. No claim about general compilers, cross-class synchronization, asymmetric fees, or the universal Cd/log(d) target.',
    'python': platform.python_version(),
    'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(out, ensure_ascii=False, indent=2))
