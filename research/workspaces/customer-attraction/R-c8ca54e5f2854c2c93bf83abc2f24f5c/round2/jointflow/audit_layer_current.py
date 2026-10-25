"""Definition-level checks of LAYER, not an SPE search or a HALF test.

The first fixed policy is the existing 7/6 prescribed-density diagnostic.
The second is one fixed complete policy with two labels covering the same x.
Two minimal policies check noncovering and zero-cover source boundaries.
These are arbitrary policies; the theorem itself needs no SPE.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def old_policy():
    m = 4
    policy = {h: 'b' for r in range(m) for h in product('ab', repeat=r)}
    policy.update({('a',): 'a', ('a', 'a'): 'b', ('b', 'a'): 'a',
                   ('a', 'a', 'b'): 'a', ('b', 'a', 'a'): 'b',
                   ('b', 'b', 'a'): 'a'})
    return m, policy, 'a'


def two_query_policy():
    m = 7
    digits = {'a': 1, 'c': 2, 'b': 0}
    policy = {}
    for r in range(m):
        for h in product('acb', repeat=r):
            if set(h) <= {'b'}:
                policy[h] = 'b'
            else:
                code = sum((j + 1) * digits[a] for j, a in enumerate(h)) + r*r
                policy[h] = 'acb'[code % 3]
    return m, policy, 'a'


def noncover_query_policy():
    # b and d both miss the tracked x, but may differ on other untracked clients.
    # Source query d does not cover x; its unique future action a does.
    m = 2
    policy = {(): 'b', ('b',): 'b', ('d',): 'a', ('a',): 'b'}
    return m, policy, 'd'


def zero_cover_source_policy():
    return 2, {(): 'b', ('b',): 'b', ('d',): 'b', ('a',): 'b'}, 'd'


def audit(name, data, common_fraction):
    m, policy, initial_query = data

    def finish(history):
        while len(history) < m:
            history += (policy[history],)
        return history

    def cover(leaf):
        return {j for j, a in enumerate(leaf) if a in 'ac'}

    actual = finish(())
    assert set(actual) == {'b'}
    query_leaf = finish((initial_query,))
    initial_covers = cover(query_leaf)
    count = len(initial_covers)
    eta = int(0 in initial_covers)
    source_bound = 1 - F(eta, count) if count else F(0)
    incoming = defaultdict(F)
    for j in initial_covers - {0}:
        incoming[query_leaf[:j]] += F(1, count)
    total_current = F(eta, count) if count else F(0)
    rows, layer_rows = [], []
    for role in range(1, m):
        layer_current, normalized, tail_density, prescribed_density = F(), F(), F(), F()
        by_action = defaultdict(F)
        for h in sorted(k for k in incoming if len(k) == role):
            mass = incoming[h]
            if not mass:
                continue
            old = finish(h)
            action = policy[h]
            reset = finish(actual[:role] + (action,))
            old_set, new_set = cover(old), cover(reset)
            assert role in old_set & new_set
            denom = len(new_set)
            keep = mass
            for j in new_set - {role}:
                assert j > role
                fraction = F(1) if j not in old_set else common_fraction
                edge = mass * fraction / denom
                incoming[reset[:j]] += edge
                keep -= edge
            assert keep >= 0
            term_bound = mass * len(old_set & new_set)
            assert denom * keep <= term_bound
            layer_current += keep
            normalized += denom * keep
            tail_density += len({j for j in old_set if j >= role}) * mass
            prescribed_density += len(old_set) * mass
            by_action[action] += denom * keep
            rows.append({'history': ''.join(h), 'role_zero_based': role,
                         'action': action, 'old_leaf': ''.join(old),
                         'reset_leaf': ''.join(reset), 'incoming': str(mass),
                         'current': str(keep), 'normalized_current': str(denom * keep)})
        assert normalized <= tail_density <= source_bound
        assert sum(by_action.values(), F()) == normalized
        total_current += layer_current
        layer_rows.append({'role_zero_based': role,
                           'normalized_current': str(normalized),
                           'tail_density': str(tail_density),
                           'prescribed_density': str(prescribed_density),
                           'normalized_by_query': {a: str(v) for a, v in sorted(by_action.items())}})
    assert total_current == int(count > 0)
    if name == 'existing_reentry' and common_fraction == 0:
        assert layer_rows[-1]['prescribed_density'] == '7/6'
        assert layer_rows[-1]['normalized_current'] == '5/12'
    if name == 'noncover_query':
        assert eta == 0 and count == 1 and source_bound == 1
        assert layer_rows[0]['tail_density'] == '1'
    if name == 'zero_cover_source':
        assert count == 0 and source_bound == 0 and not rows
    return {'policy': name, 'm': m, 'common_fraction': str(common_fraction),
            'actual': ''.join(actual), 'initial_query_leaf': ''.join(query_leaf),
            'source_query_covers_x': bool(eta),
            'source_bound': str(source_bound), 'layers': layer_rows,
            'all_mass_absorbed': str(total_current), 'rows': rows}


report = {
    'scope': 'Exact audits of TAIL-DENSITY/LAYER on two fixed policies and two source boundary policies, not SPE or HALF evidence.',
    'cases': [audit(name, data(), fraction)
              for name, data in [('existing_reentry', old_policy),
                                 ('fixed_two_query', two_query_policy),
                                 ('noncover_query', noncover_query_policy),
                                 ('zero_cover_source', zero_cover_source_policy)]
              for fraction in [F(0), F(1, 2), F(1)]]}
(ROOT / 'layer_current_audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'cases': len(report['cases']),
                  'all_exact_checks': 'pass',
                  'scope': report['scope']}, ensure_ascii=False))
