"""Exact common-catalog terminal closure of the frozen indexed LP point.

This constructs one honest exchangeable lift of the frozen marginals, with
families conditionally independent given the common optimal-topic memberships.
It does NOT establish that all other lifts fail, or claim a complete strategy.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
LABELS = 'ABCDEUVWXY'
FIXED_PATHS = {'actual': 'ABCDE', 'second': 'AEUVW', 'third': 'ABEXY'}


def families(atom):
    j = sum(n * ty[0] for n, ty in
            zip(atom['AB_hist'], product((0, 1), repeat=3)))
    out = {'AB': (tuple(product((0, 1), repeat=3)), atom['AB_hist']),
           'AE': (tuple(product((0, 1), repeat=3)), atom['AE_hist']),
           'S': (tuple(product((0, 1), repeat=4)), atom['second_hist'])}
    for name, (ell, h) in zip(FIXED_PATHS, atom['menus_lh']):
        out['L_' + name] = (tuple(product((0, 1), repeat=2)),
                            [5 - j - ell + h, ell - h, j - h, h])
    assert all(sum(hist) == 5 for _, hist in out.values())
    assert all(sum(n * ty[0] for n, ty in zip(hist, types)) == j
               for types, hist in out.values())
    return j, out


def query_groups(fams):
    yield ('T', None, 0)
    for family, (types, _) in fams.items():
        for pos in range(1, len(types[0])):
            yield (family + ':' + str(pos), family, pos)


def conditional_bit(fams, family, pos, t):
    types, hist = fams[family]
    den = sum(n for n, ty in zip(hist, types) if ty[0] == t)
    return (F(sum(n * ty[pos] for n, ty in zip(hist, types) if ty[0] == t), den)
            if den else F(0))


def indexed_query(j, fams, branch_family, state, family, pos, same):
    if family is None:
        total = j
        own = state[0]
    else:
        types, hist = fams[family]
        total = sum(n * ty[pos] for n, ty in zip(hist, types))
        own = (F(state[pos]) if family == branch_family else
               conditional_bit(fams, family, pos, state[0]))
    return own if same else (F(total) - own) / 4


def audit():
    cert = json.loads(SOURCE.read_text())['primal']
    slacks = defaultdict(F)
    payoffs = defaultdict(F)
    query_payoffs = defaultdict(F)
    # A terminal-node family is (fixed prefix, indexed family, indexed prefix
    # positions, chosen indexed position). All branches use index i=1.
    nodes = {**{'fixed_' + name: (path[:4], None, (), path[4])
                for name, path in FIXED_PATHS.items()},
             **{'old_' + name: (path[:3], 'L_' + name, (0,), 1)
                for name, path in FIXED_PATHS.items()},
             'branch_AB': ('AB', 'AB', (0, 1), 2),
             'branch_AE': ('AE', 'AE', (0, 1), 2),
             'branch_S': ('A', 'S', (0, 1, 2), 3)}
    for atom in cert['atoms']:
        mass = F(atom['mass_numerator'], cert['denominator'])
        bits = dict(zip(LABELS, map(int, atom['bits'])))
        j, fams = families(atom)
        for node, (fixed, family, prefix_positions, action) in nodes.items():
            if family is None:
                states = [(None, F(1))]
            else:
                types, hist = fams[family]
                states = [(ty, F(n, 5)) for n, ty in zip(hist, types) if n]
            for state, probability in states:
                load = sum(bits[label] for label in fixed)
                if state is not None:
                    load += sum(state[pos] for pos in prefix_positions)
                chosen = bits[action] if family is None else state[action]
                chosen_payoff = F(chosen, load + 1)
                weight = mass * probability
                payoffs[node] += weight * chosen_payoff
                for label in LABELS:
                    key = node + ' -> ' + label
                    alt = F(bits[label], load + 1)
                    slacks[key] += weight * (chosen_payoff - alt)
                    query_payoffs[key] += weight * alt
                for name, query_family, pos in query_groups(fams):
                    positions = [False] if family is None else [True, False]
                    for same in positions:
                        if family is None:
                            count = (j if query_family is None else sum(
                                n * ty[pos] for n, ty in zip(
                                    fams[query_family][1], fams[query_family][0])))
                            bit = F(count, 5)
                        else:
                            bit = indexed_query(j, fams, family, state,
                                                query_family, pos, same)
                        suffix = 'i' if same else ('any' if family is None else 'j!=i')
                        key = node + ' -> ' + name + '[' + suffix + ']'
                        alt = bit / (load + 1)
                        slacks[key] += weight * (chosen_payoff - alt)
                        query_payoffs[key] += weight * alt
    failures = []
    for key, slack in sorted(slacks.items(), key=lambda kv: kv[1]):
        if slack < 0:
            node = key.split(' -> ')[0]
            failures.append({'row': key, 'slack': str(slack),
                             'slack_float': float(slack),
                             'chosen_payoff': str(payoffs[node]),
                             'deviation_payoff': str(query_payoffs[key])})
    return {'scope': 'one exact exchangeable conditional-independent honest membership lift; no SPE',
            'catalog_size': 65, 'terminal_node_families': len(nodes),
            'checked_deviation_categories': len(slacks),
            'negative_categories': len(failures),
            'failures': failures,
            'node_chosen_payoffs': {k: str(v) for k, v in payoffs.items()},
            'all_slacks': {k: str(v) for k, v in sorted(slacks.items())}}


if __name__ == '__main__':
    report = audit()
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'all_slacks'}, indent=2))
