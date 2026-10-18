"""Independent prefix replay and small exact oracles for bundle peeling.

This audit is finite evidence.  The universal statement uses the manuscript's
proof; the exponential oracle below is not part of the path algorithm.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
from random import Random

from bundle_peeling_buffer_path import bundle_peeling_path


def state(edges, fixed, moved):
    result = [F(v) for v in fixed]
    for j, (s, t, a, b) in enumerate(edges):
        result[t if j in moved else s] += F(b if j in moved else a)
    return result


def replay(edges, fixed, C, T):
    result = bundle_peeling_path(edges, fixed, C, T)
    order = result['order']
    assert sorted(order) == list(range(len(edges)))
    moved, peak = set(), max(state(edges, fixed, set()))
    trace = [state(edges, fixed, moved)]
    bound = max(2*F(T), F(C)+F(T)/2)
    for j in order:
        assert j not in moved
        moved.add(j)
        actual = state(edges, fixed, moved)
        assert min(actual) >= 0 and max(actual) <= bound
        peak = max(peak, max(actual))
        trace.append(actual)
    assert peak == F(result['peak'])
    assert max(trace[-1]) <= T
    return result, trace


def exact_minimax(edges, fixed):
    """All subset states and predecessor choices; no constructor calls."""
    n = len(edges)
    best = [None]*(1 << n)
    best[0] = max(state(edges, fixed, set()))
    for mask in range(1, 1 << n):
        moved = {j for j in range(n) if mask >> j & 1}
        load = max(state(edges, fixed, moved))
        best[mask] = min(max(best[mask ^ (1 << j)], load) for j in moved)
    return best[-1]


def audit():
    fixtures = []
    # Both examples violate the older single-eligible-source condition.
    for name, incoming in [('held_core', [F(1, 4)]*4),
                           ('actual_peeling', [F(1, 8)]*2+[F(3, 8)]*2)]:
        edges = [(s, 1-s, F(3, 8), b) for s in range(2) for b in incoming]
        result, trace = replay(edges, [0, 0], F(3, 2), F(1))
        assert all(a < F(1, 2) for s, t, a, b in edges)
        assert result['held_core'] == ([0, 1] if name == 'held_core' else [])
        fixtures.append({'name': name, 'edges': edges, 'fixed': [0, 0],
                         'C': F(3, 2), 'T': F(1), 'result': result,
                         'trace': trace, 'exact_minimax': exact_minimax(edges, [0, 0])})
    # Exhaust all branch patterns of a three-vertex all-small cycle.
    patterns = [[F(1, 4)]*4, [F(1, 8)]*2+[F(3, 8)]*2,
                [F(3, 8)]*2+[F(1, 8)]*2]
    branch_cases = 0
    for choices in product(range(len(patterns)), repeat=3):
        edges = [(s, (s+1) % 3, F(3, 8), b)
                 for s in range(3) for b in patterns[choices[s]]]
        replay(edges, [0]*3, F(3, 2), F(1))
        branch_cases += 1
    # Already-known single-edge cases, shared receivers and exact long scale.
    split = [(s, 1-s, F(1), F(3, 5)) for s in range(2)]
    split += [(s, 1-s, F(1, 4), F(1, 10)) for s in range(2) for _ in range(4)]
    replay(split, [0, 0], F(2), F(1))
    # Selected core exits must be moved in the initial outside-H phase.
    exits = []
    for s in range(2):
        exits.extend([(s, 1-s, F(1, 4), F(3, 5)),
                      (s, 2, F(1, 4), F(2, 5))])
        exits.extend([(s, 1-s, F(1, 4), F(1, 15))]*6)
    result, trace = replay(exits, [0, 0, 0], F(2), F(1))
    assert result['held_core'] == [0, 1] and result['phase_ends'][0] == 2
    fixtures.append({'name': 'held_core_with_selected_exits', 'edges': exits,
                     'fixed': [0, 0, 0], 'C': F(2), 'T': F(1),
                     'result': result, 'trace': trace})
    scale = F(1, 2**263+9)
    scaled = [(s, t, a*scale, b*scale) for s, t, a, b in split]
    replay(scaled, [0, 0], 2*scale, scale)
    # Zero, empty, fixed loads, unused machines, and zero endpoint times.
    degenerate = [([], [0], 0, 0), ([(0, 1, 0, 0)], [0, 0], 0, 0),
                  ([], [F(1)], F(1), F(1)),
                  ([(0, 1, 0, F(1))], [0, 0], F(1), F(1)),
                  ([(0, 1, F(1), 0)], [0, F(1)], F(1), F(1)),
                  (split, [0, 0, F(1)], F(2), F(1))]
    for args in degenerate:
        replay(*args)
    # Every first move attains the lower bound in these two sharp families.
    sharp = []
    for C in [F(1), F(5, 4), F(3, 2), F(7, 4), F(2)]:
        if C <= F(3, 2):
            edges = [(0, 1, F(1), 2-C), (1, 0, F(1), 2-C)]
            fixed = [C-1]*2
        else:
            edges = [(s, 1-s, C/2, F(1, 2)) for s in range(2) for _ in range(2)]
            fixed = [0, 0]
        result, trace = replay(edges, fixed, C, F(1))
        U = max(F(2), C+F(1, 2))
        assert exact_minimax(edges, fixed) == U == F(result['peak'])
        assert all(max(state(edges, fixed, {j})) == U for j in range(len(edges)))
        # Independently check OPT=T for the original two-end matrix.
        actual_opt = min(max(state(edges, fixed,
                                  {j for j in range(len(edges)) if mask >> j & 1}))
                         for mask in range(1 << len(edges)))
        assert actual_opt == 1
        sharp.append({'C': C, 'U': U, 'exact_minimax': U, 'OPT': actual_opt})
    rng, generated = Random(20261018), 0
    for m in (2, 3, 4, 5):
        for _ in range(12):
            source, target, edges = [0]*m, [0]*m, []
            for j in range(8):
                s = rng.randrange(m)
                t = rng.randrange(m-1)
                t += t >= s
                a = rng.randint(0, min(12, 24-source[s]))
                b = rng.randint(0, 12-target[t])
                edges.append((s, t, F(a, 12), F(b, 12)))
                source[s] += a
                target[t] += b
            C = max(F(1), max(F(v, 12) for v in source))
            replay(edges, [0]*m, C, F(1))
            generated += 1
    invalid = [([], [], 1, 1), ([], [0], 3, 1),
               ([(0, 0, 1, 1)], [0], 1, 1),
               ([(0, 1, F(-1), 0)], [0, 0], 1, 1),
               ([(0, 1, 2, 0)], [0, 0], 2, 1),
               ([(0, 1, 0, 2)], [0, 0], 2, 1),
               ([(0, 1, 0.5, 0)], [0, 0], 1, 1),
               ([(True, 1, 0, 0)], [0, 0], 1, 1),
               ([], [True], 0, 0), ([], [F(-1)], 0, 0),
               ([], [2], 1, 1), ([], [0], True, 0)]
    for args in invalid:
        try:
            bundle_peeling_path(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    here = Path(__file__).resolve()
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [here, here.with_name('bundle_peeling_buffer_path.py')]}
    return {'status': 'passed', 'python': platform.python_version(),
            'arithmetic': 'fractions.Fraction', 'seed': 20261018,
            'source_sha256': hashes, 'all_small_fixtures': fixtures,
            'three_vertex_branch_cases': branch_cases, 'generated_cases': generated,
            'degenerate_cases': len(degenerate), 'sharp_cases': sharp,
            'invalid_cases': len(invalid), 'long_scale': scale,
            'scope': 'Finite independent prefix replay and small minimax/OPT oracles; '
                     'not a universal proof, a target solver, or an approximation algorithm.'}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2,
                     default=lambda v: str(v) if isinstance(v, F) else v))
