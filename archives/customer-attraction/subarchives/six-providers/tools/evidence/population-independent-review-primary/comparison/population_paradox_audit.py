#!/usr/bin/env python3
"""Definition-level unit-customer audit; no customer_attraction imports.

At every ordered node, enumerate the Cartesian product of all child SPE paths.
Choose every optimal current action. One child strategy per terminal path is
sufficient because the parent sees only terminal payoffs. Retain a complete
ordered-history strategy witness. All comparisons use Fraction.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

# Distinct unit customers. An element is the tuple of topics liked by that unit.
UNITS = ((0,),) * 3 + ((1,),) * 3 + ((2,),) + ((0, 1),) + ((0, 2),) * 2 + ((1, 2),) * 2
LABELS = 'ABC'


def utility(path, player):
    chosen = path[player]
    return sum((Fraction(1, sum(a in likes for a in path))
                for likes in UNITS if chosen in likes), Fraction(0))


def welfare(path):
    return sum(any(a in likes for a in path) for likes in UNITS)


def enumerate_spe(players):
    """Return map: each realizable ordered path -> a full ordered strategy."""
    @lru_cache(None)
    def solve(history):
        if len(history) == players:
            return {history: {}}
        children = [solve(history + (a,)) for a in range(3)]
        realized = {}
        for branch_paths in product(*(tuple(child) for child in children)):
            values = tuple(utility(path, len(history)) for path in branch_paths)
            best = max(values)
            # Strategies below different child histories have disjoint domains.
            strategy = {}
            for child, path in zip(children, branch_paths):
                strategy.update(child[path])
            for action, value in enumerate(values):
                if value == best:
                    path = branch_paths[action]
                    realized.setdefault(path, {**strategy, history: action})
        return realized
    return solve(()) , solve


def replay(strategy, prefix, players):
    path = tuple(prefix)
    while len(path) < players:
        path += (strategy[path],)
    return path


def verify(strategy, players):
    expected = {h for depth in range(players) for h in product(range(3), repeat=depth)}
    assert set(strategy) == expected
    comparisons = 0
    strict = 0
    ties = 0
    for h in sorted(expected, key=lambda x: (len(x), x)):
        actual = replay(strategy, h, players)
        actual_u = utility(actual, len(h))
        for action in range(3):
            if action == strategy[h]:
                continue
            alternative = replay(strategy, h + (action,), players)
            alternative_u = utility(alternative, len(h))
            assert actual_u >= alternative_u, (h, action, actual_u, alternative_u)
            comparisons += 1
            strict += actual_u > alternative_u
            ties += actual_u == alternative_u
    return {'nodes': len(expected), 'nonself_comparisons': comparisons, 'strict': strict, 'ties': ties}


def text_path(path):
    return ''.join(LABELS[a] for a in path)


def main():
    global UNITS
    report = {'unit_customers': [list(likes) for likes in UNITS], 'players': {}}
    for players in (1, 2, 3, 4, 5):
        all_paths, solve = enumerate_spe(players)
        root_paths = sorted(all_paths)
        counts = {tuple(path.count(a) for a in range(3)) for path in root_paths}
        welfares = {welfare(path) for path in root_paths}
        if players == 3:
            assert counts == {(1, 1, 1)} and welfares == {12}
        if players == 4:
            assert counts == {(2, 2, 0)} and welfares == {11}
        witnesses = {text_path(path): verify(strategy, players) for path, strategy in all_paths.items()}
        selected_path = min(all_paths)
        selected_strategy = all_paths[selected_path]
        tables = {}
        for depth in range(min(players, 3)):
            for history in product(range(3), repeat=depth):
                tables[text_path(history)] = sorted({text_path(path[len(history):]) for path in solve(history)})
        report['players'][str(players)] = {
            'all_ordered_spe_paths': [text_path(p) for p in root_paths],
            'terminal_counts': [list(c) for c in sorted(counts)],
            'welfare_set': sorted(welfares),
            'selected_path': text_path(selected_path),
            'selected_payoffs': [str(utility(selected_path, i)) for i in range(players)],
            'selected_strategy': {text_path(h): LABELS[a] for h, a in sorted(selected_strategy.items(), key=lambda v: (len(v[0]), v[0]))},
            'all_witness_audits': witnesses,
            'ordered_child_menu_table': tables,
        }
    # Boundary regression: empty clients and identical themes. Direct definition
    # replay accepts every strategy; all utilities/welfare are zero.
    original = UNITS
    for units in ((), ((0, 1, 2),), ((0, 1, 2),) * 3):
        UNITS = units
        all_paths, _ = enumerate_spe(2)
        assert len(all_paths) == 9
        for strategy in all_paths.values():
            verify(strategy, 2)
    UNITS = original
    report['boundary_regressions'] = ['zero clients', 'one all-theme client', 'three all-theme clients']
    output = Path(__file__).with_name('population_paradox_audit.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({m: {k: v for k, v in r.items() if k in ('all_ordered_spe_paths', 'terminal_counts', 'welfare_set', 'selected_payoffs')} for m, r in report['players'].items()}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
