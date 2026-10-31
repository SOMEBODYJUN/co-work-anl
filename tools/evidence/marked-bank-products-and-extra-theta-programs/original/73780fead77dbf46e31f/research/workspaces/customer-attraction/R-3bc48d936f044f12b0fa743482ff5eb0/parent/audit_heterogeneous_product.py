"""Independent complete product audit of unequal credible-deficit repair.

No imports from the author or the repository game implementation.  The old
path is A,A,B with disjoint blocks of sizes 1,4; multiply everything by 6.
Two fixed insurer components mark {1,2} and {2}, respectively.  The second
component has an unmarked role before its marked role.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform

M = 3
SIZES = ((6, 24), (10, 10, 5), (8, 8, 4))
BANKS = (2, 1)
RESERVOIRS = (2, 1)
NORMAL = ((0, 0, 1), (0, 1, 0), (1, 2, 1))
ACTIONS = tuple(product(range(2), range(3), range(3)))


def payoff(h, a, sizes):
    return Q(sizes[a], h.count(a))


@lru_cache(None)
def old_outcomes(h):
    if len(h) == M:
        return frozenset((h,))
    children = [old_outcomes(h+(a,)) for a in range(2)]
    floor = max(min(payoff(z, a, SIZES[0]) for z in children[a])
                for a in range(2))
    return frozenset(z for a in range(2) for z in children[a]
                     if payoff(z, a, SIZES[0]) >= floor)


def old_policy(h, target):
    if len(h) == M:
        return {}
    children = [old_outcomes(h+(a,)) for a in range(2)]
    floor = max(min(payoff(z, a, SIZES[0]) for z in children[a])
                for a in range(2))
    chosen = next(a for a in range(2) if target in children[a]
                  and payoff(target, a, SIZES[0]) >= floor)
    result = {h: chosen}
    for a in range(2):
        child_target = target if a == chosen else min(
            children[a], key=lambda z: (payoff(z, a, SIZES[0]), z))
        result.update(old_policy(h+(a,), child_target))
    return result


OLD_CHILDREN = {}
DELTAS = []
old_normal = tuple(a[0] for a in NORMAL)
for i in range(M-1):
    floors = []
    for a in range(2):
        h = old_normal[:i]+(a,)
        target = min(old_outcomes(h), key=lambda z: (payoff(z, a, SIZES[0]), z))
        floors.append(payoff(target, a, SIZES[0]))
        OLD_CHILDREN[i, a] = old_policy(h, target)
    DELTAS.append(max(Q(0), max(floors)-payoff(old_normal, old_normal[i], SIZES[0])))
assert DELTAS == [Q(5), Q(9)], DELTAS


@lru_cache(None)
def bank_bi_terminal(component, h):
    if len(h) == M:
        return h
    return bank_bi_terminal(component, h+(bank_bi_action(component, h),))


@lru_cache(None)
def bank_bi_action(component, h):
    return max(range(3), key=lambda a: (
        payoff(bank_bi_terminal(component, h+(a,)), a, SIZES[component]), -a))


def bank_after_exit(component, h, exit_position, forced):
    k = BANKS[component-1]
    reservoir = RESERVOIRS[component-1]
    d = M-k
    before = h[:exit_position]
    mode = 'BI' if forced > reservoir or (forced < k and forced in before) else (
        'Y' if forced == reservoir else 'F')
    # First violation is permanent, even if its count later looks clean.
    for length in range(exit_position+2, len(h)+1):
        p = h[:length]
        if (any(p.count(a) > 1 for a in range(k))
                or any(a > reservoir for a in p)
                or p.count(reservoir) > d-(mode == 'F')):
            mode = 'BI'
            break
    if mode == 'BI':
        return bank_bi_action(component, h)
    fresh = [a for a in range(k) if a not in h]
    if fresh:
        return fresh[0]
    if mode == 'Y' or h.count(reservoir) < d-1:
        return reservoir
    return forced


def choose(h):
    # A first product deviation includes changes only to insurer coordinates.
    exit_position = next((i for i in range(min(len(h), M-1))
                          if h[i] != NORMAL[i]), None)
    if exit_position is None:
        return NORMAL[len(h)]
    first = h[exit_position]
    projected = tuple(a[0] for a in h)
    old = OLD_CHILDREN[exit_position, first[0]][projected]
    bank = tuple(bank_after_exit(c, tuple(a[c] for a in h), exit_position, first[c])
                 for c in (1, 2))
    return (old,)+bank


@lru_cache(None)
def terminal(h):
    return h if len(h) == M else terminal(h+(choose(h),))


def player_payoff(z, position):
    return sum((payoff(tuple(a[c] for a in z), z[position][c], SIZES[c])
                for c in range(3)), Q(0))


def welfare(z):
    return sum(sum(SIZES[c][a] for a in {v[c] for v in z}) for c in range(3))


nodes = checks = 0
minimum = None
for length in range(M):
    for h in product(ACTIONS, repeat=length):
        prescribed = player_payoff(terminal(h), length)
        nodes += 1
        for a in ACTIONS:
            margin = prescribed-player_payoff(terminal(h+(a,)), length)
            assert margin >= 0, (h, a, margin)
            minimum = margin if minimum is None else min(minimum, margin)
            checks += 1

z = terminal(())
assert z == NORMAL
W = welfare(z)
O = max(welfare(z) for z in product(ACTIONS, repeat=M))
profits = tuple(player_payoff(z, i) for i in range(M))
assert (W, O, profits) == (71, 75, (Q(17), Q(21), Q(33)))
assert W == 30+M*max(DELTAS)+sum(DELTAS)
assert O == 30+(2*M-1)*max(DELTAS)
report = {
    'identity': 'unequal-deficit marked-position full Cartesian regression',
    'scope': 'this one finite 75-unit-customer, 18-theme, m=3 instance only',
    'python': platform.python_version(),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'old_sizes_scaled_by_6': SIZES[0],
    'old_target': old_normal,
    'credible_deficits_after_scaling': [str(v) for v in DELTAS],
    'insurer_sizes': SIZES[1:],
    'marked_positions_one_based': [[1, 2], [2]],
    'actual_product_path': z,
    'actual_payoffs': [str(v) for v in profits],
    'customer_count': sum(map(sum, SIZES)), 'W': W, 'OPT': O,
    'ordered_decision_histories': nodes,
    'all_joint_action_comparisons_including_self': checks,
    'terminal_profiles_for_OPT': len(ACTIONS)**M,
    'minimum_IC_margin': str(minimum),
    'passed': True,
    'general_proof': '../credible/heterogeneous_prefix_repair.md',
    'target_counterexample': False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
