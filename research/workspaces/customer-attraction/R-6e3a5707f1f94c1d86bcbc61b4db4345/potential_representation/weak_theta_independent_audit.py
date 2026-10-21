"""Independent good-state audit for the replicated weak-theta obstruction.

Expands all unit customers; does not import the author audit, solver, or model.
Bad-child utility is bounded at entry, so arbitrary SPE subtrees can be grafted.
The universal claim is proved in weak_theta_independent_review.md.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
import json

CLIENTS = []
for x in range(3):
    for y in range(3, 6):
        CLIENTS.append(frozenset((x, y)))
for xs in combinations(range(3), 2):
    for ys in combinations(range(3, 6), 2):
        CLIENTS.extend([frozenset(xs + ys)] * 3)
assert len(CLIENTS) == 36


@lru_cache(None)
def entry(prefix, action):
    return sum((Fraction(1, 1 + sum(t in client for t in prefix))
                for client in CLIENTS if action in client), Fraction())


def terminal_payoff(prefix, action):
    return sum((Fraction(1, sum(t in client for t in prefix))
                for client in CLIENTS if action in client), Fraction())


def append(state, block, topic):
    return state[:block] + (state[block] + (topic,),) + state[block + 1:]


def policy(state):
    for count in (2, 1, 0):
        for block, prefix in enumerate(state):
            if len(prefix) != count:
                continue
            if count == 0:
                return block, 0
            group = prefix[-1] // 3 if count == 2 else 1 - prefix[0] // 3
            topic = next(a for a in range(3 * group, 3 * group + 3)
                         if a not in prefix)
            return block, topic
    raise ValueError('terminal state')


@lru_cache(None)
def finish(state):
    if all(len(h) == 3 for h in state):
        return state
    block, topic = policy(state)
    return finish(append(state, block, topic))


table = {
    (): (21,) * 6,
    (0,): (Fraction(21, 2), Fraction(33, 2), Fraction(33, 2),
           Fraction(29, 2), Fraction(29, 2), Fraction(29, 2)),
    (0, 1): (9, 9, 12, 10, 10, 10),
    (0, 3): (Fraction(25, 3), 12, 12, Fraction(25, 3), 12, 12),
    (0, 1, 2): (Fraction(15, 2),) * 6,
    (0, 3, 4): (Fraction(20, 3), Fraction(35, 4), Fraction(35, 4),
                Fraction(22, 3), Fraction(22, 3), Fraction(19, 2)),
}
for h, values in table.items():
    assert tuple(entry(h, a) for a in range(6)) == values
for h in product(range(6), repeat=2):
    assert max(entry(h, a) for a in range(6)) >= 12
for h in permutations(range(6), 3):
    assert max(entry(h, a) for a in range(6)) <= Fraction(19, 2)

local_prefixes = [()]
for length in (1, 2, 3):
    local_prefixes.extend(permutations(range(6), length))
results = []
for blocks in (1, 2):
    states = deviations = 0
    for state in product(local_prefixes, repeat=blocks):
        if all(len(h) == 3 for h in state):
            continue
        states += 1
        prescribed_block, prescribed_topic = policy(state)
        final = finish(append(state, prescribed_block, prescribed_topic))
        prescribed = terminal_payoff(final[prescribed_block], prescribed_topic)
        expected = 12 if any(len(h) in (1, 2) for h in state) else 10
        assert prescribed == expected
        for block in range(blocks):
            for topic in range(6):
                deviations += 1
                prefix = state[block]
                if len(prefix) == 3 or topic in prefix:
                    alternative_upper = entry(prefix, topic)
                else:
                    alternative_final = finish(append(state, block, topic))
                    alternative_upper = terminal_payoff(alternative_final[block], topic)
                assert alternative_upper <= prescribed, (state, block, topic)
    root = finish(((),) * blocks)
    assert root == ((0, 3, 4),) * blocks
    results.append({'k': blocks, 'good_nonterminal_states': states,
                    'all_action_comparisons': deviations})

print(json.dumps({'status': 'passed', 'unit_customers_per_block': len(CLIENTS),
                  'exact_local_tables': len(table), 'good_state_checks': results,
                  'universal_proof': 'weak_theta_independent_review.md',
                  'main_half_coverage': 'neither proved nor refuted'}))
