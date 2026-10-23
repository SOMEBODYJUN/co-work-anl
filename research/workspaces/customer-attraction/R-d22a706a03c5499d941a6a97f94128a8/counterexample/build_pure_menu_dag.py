"""Discover a compressed complete SPE for the two-block pure-menu obstruction.

The canonical solver is used only to choose a full finite strategy.  The output
DAG is checked directly by verify_pure_menu_dag.py, without any SPE oracle.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def main():
    local = [({0}, 2), ({1, 3}, 4), ({0, 2}, 6),
             ({2, 3}, 3), ({0, 1, 2, 3}, 1)]
    inst = Instance(tuple(f'{letter}{block}' for block in range(2) for letter in 'ABCD'),
                    tuple(CustomerType(frozenset(a + 4 * block for a in likes), multiplicity)
                          for block in range(2) for likes, multiplicity in local), 8)
    solver = ExactSPESolver(inst)
    base = (2, 1, 1, 0)
    local_columns = ((2, 0, 1, 1), (1, 1, 1, 1),
                     (1, 0, 2, 1), (1, 0, 1, 2))
    root_columns = tuple(local_columns[b] + base for b in range(4)) + tuple(
        base + local_columns[b] for b in range(4))
    root_target = root_columns[3]
    root_floor = solver.threshold((0,) * 8)
    assert root_floor == Fraction(13, 4)
    for action, target in enumerate(root_columns):
        prefix = tuple(int(a == action) for a in range(8))
        assert target in solver.outcomes(prefix)
        assert inst.topic_payoff(action, target) <= root_floor

    nodes = []
    memo = {}

    def expand(counts, target):
        key = counts, target
        if key in memo:
            return memo[key]
        identity = len(nodes)
        memo[key] = identity
        node = {'counts': list(counts), 'target': list(target)}
        nodes.append(node)
        if sum(counts) == 8:
            assert counts == target
            node.update(action=None, children=[])
            return identity
        floor = solver.threshold(counts)
        children_counts = [tuple(c + int(a == action) for a, c in enumerate(counts))
                           for action in range(8)]
        admissible = [action for action in range(8)
                      if target in solver.outcomes(children_counts[action])
                      and inst.topic_payoff(action, target) >= floor]
        chosen = 3 if not any(counts) else admissible[0]
        assert chosen in admissible
        targets = []
        for action, child_counts in enumerate(children_counts):
            if not any(counts):
                child_target = root_columns[action]
            elif action == chosen:
                child_target = target
            else:
                child_target = min(solver.outcomes(child_counts),
                                   key=lambda z: (inst.topic_payoff(action, z), z))
            targets.append(child_target)
        node.update(action=chosen,
                    children=[expand(child_counts, child_target)
                              for child_counts, child_target in zip(children_counts, targets)])
        return identity

    root = expand((0,) * 8, root_target)
    report = {'schema': 'CA_COMPLETE_SPE_DAG_v1',
              'scope': 'pure root-menu blocker obstruction only; not mixed-menu or half counterexample',
              'instance': inst.to_dict(), 'root': root,
              'root_columns': [list(q) for q in root_columns],
              'nodes': nodes,
              'discovery': {'canonical_root_threshold': str(root_floor),
                            'canonical_count_states': solver.stats.count_states}}
    destination = Path(__file__).with_name('pure_menu_two_block_dag.json')
    with destination.open('x') as stream:
        json.dump(report, stream, separators=(',', ':'))
        stream.write('\n')
    print(json.dumps({'path': str(destination), 'nodes': len(nodes),
                      'root_threshold': str(root_floor)}))


if __name__ == '__main__':
    main()
