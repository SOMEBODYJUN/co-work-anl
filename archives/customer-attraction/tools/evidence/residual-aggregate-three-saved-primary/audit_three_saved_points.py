"""Definition-level exact audit of only three frozen residual-game inputs.

No imports of legacy code, numerical optimizer, random scanning, or Git writes.
Run from any cwd; outputs stay next to this script. Complete policies produced
here are new reconstructions, never attributed to the original saved JSONs.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
INPUTS = (
    'cdc51dbd8435fa588def--probe_r3b3.json',
    '816d08f10bd9433415e7--probe_r4b2.json',
    'ec4a78b7b0f1e4b3d871--probe_r5b1.json',
)


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def counts(k, size):
    for z in combinations_with_replacement(range(k), size):
        yield tuple(z.count(a) for a in range(k))


def audit(name):
    raw = (HERE / 'original' / name).read_bytes()
    saved = json.loads(raw)
    x = saved['best']
    k, r, prefix = x['k'], x['r'], tuple(x['prefix'])
    w = x['weights']
    assert len(w) == (1 << k) - 1 and all(isinstance(z, int) and z >= 0 for z in w)
    assert r + len(prefix) == 6 and k > 0 and r > 0
    types = tuple((s, z) for s, z in enumerate(w, 1) if z)
    bg = {s: sum((s >> a) & 1 for a in prefix) for s, _ in types}
    scale = lcm(*range(1, len(prefix) + r + 1))
    terminals = tuple(counts(k, r))
    terminal_id = {q: i for i, q in enumerate(terminals)}

    def integer_pay(q):
        result = [0] * k
        for s, z in types:
            den = bg[s] + sum(q[a] for a in range(k) if (s >> a) & 1)
            if den:
                assert scale % den == 0
                for a in range(k):
                    if (s >> a) & 1:
                        result[a] += z * (scale // den)
        return tuple(result)

    pays = tuple(integer_pay(q) for q in terminals)
    totals = tuple(sum(c * v for c, v in zip(q, u)) for q, u in zip(terminals, pays))
    floors = {}
    menus = {}

    @lru_cache(None)
    def outcomes(q):
        if sum(q) == r:
            answer = frozenset((terminal_id[q],))
        else:
            children = [outcomes(q[:a] + (q[a] + 1,) + q[a + 1:]) for a in range(k)]
            floor = max(min(pays[t][a] for t in child) for a, child in enumerate(children))
            floors[q] = floor
            answer = frozenset(t for a, child in enumerate(children) for t in child if pays[t][a] >= floor)
        menus[q] = answer
        return answer

    zero = (0,) * k
    root = outcomes(zero)
    assert len(root) == x['root_outcomes'] == 1
    target = min(root, key=totals.__getitem__)
    assert terminals[target] == tuple(x['terminal'])
    policy = {}

    def expand(h, q, t):
        if len(h) == r:
            assert terminal_id[q] == t
            return
        child_q = [q[:a] + (q[a] + 1,) + q[a + 1:] for a in range(k)]
        a = next(a for a, child in enumerate(child_q) if t in menus[child] and pays[t][a] >= floors[q])
        policy[h] = a
        for b, child in enumerate(child_q):
            other = t if b == a else min(menus[child], key=lambda j: (pays[j][b], j))
            expand(h + (b,), child, other)

    expand((), zero, target)

    @lru_cache(None)
    def finish(h):
        if len(h) == r:
            return terminal_id[tuple(h.count(a) for a in range(k))]
        return finish(h + (policy[h],))

    path = []
    while len(path) < r:
        path.append(policy[tuple(path)])
    assert finish(()) == target
    slacks = []
    for h, a in policy.items():
        followed = finish(h)
        for b in range(k):
            slack = pays[followed][a] - pays[finish(h + (b,))][b]
            assert slack >= 0
            slacks.append(slack)
    assert len(policy) == sum(k ** d for d in range(r))
    a = next(a for a, q in enumerate(terminals[target]) if q)
    assert terminals[target][a] == r and path == [a] * r
    value = F(pays[target][a], scale)
    total = F(totals[target], scale)
    assert total == r * value

    # Exact static primal and dual. All rival count vectors are kept.
    matrix = []
    rivals = tuple(counts(k, r - 1))
    for q in rivals:
        row = []
        for b in range(k):
            row.append(sum((F(z, 1 + bg[s] + sum(q[c] for c in range(k) if (s >> c) & 1)) for s, z in types if (s >> b) & 1), F(0)))
        matrix.append(row)
    lower = min(row[a] for row in matrix)
    pure_rival = tuple(r - 1 if b == a else 0 for b in range(k))
    upper_row = matrix[rivals.index(pure_rival)]
    assert lower == value == max(upper_row)
    # Legacy decimal fields are preserved, then compared for orientation only.
    assert abs(float(total) - x['tail_total']) < 1e-12
    assert abs(float(value) - x['security']) < 1e-12

    aliases = []
    for a1 in range(k):
        for a2 in range(a1 + 1, k):
            if all(((s >> a1) & 1) == ((s >> a2) & 1) for s, _ in types):
                aliases.append([a1, a2])
    policy_packet = {
        'status': 'new exact reconstruction; not original saved strategy',
        'source_json': name,
        'prefix': prefix,
        'remaining_players': r,
        'topics': k,
        'ordered_path': path,
        'policy': [{'history': h, 'action': policy[h]} for h in sorted(policy, key=lambda z: (len(z), z))],
    }
    policy_name = f'new-complete-policy-r{r}.json'
    policy_raw = dumps(policy_packet).encode()
    (HERE / policy_name).write_bytes(policy_raw)
    matrix_name = f'exact-static-matrix-r{r}.json'
    (HERE / matrix_name).write_text(dumps([
        {'rivals_counts': q, 'query_values': [str(z) for z in row]}
        for q, row in zip(rivals, matrix)
    ]))
    return {
        'source_json': name,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'original_top_level_fields': list(saved),
        'original_best_fields': list(x),
        'original_samples_requested': saved['samples_requested'],
        'original_seed': saved['seed'],
        'not_a_replay_of_original_main': True,
        'total_players_including_prefix': 6,
        'topics': k,
        'remaining_players': r,
        'prefix': prefix,
        'customers': sum(w),
        'nonzero_types': [{'mask': s, 'multiplicity': z} for s, z in types],
        'same_coverage_distinct_labels_retained': aliases,
        'integer_scale': scale,
        'terminal_count_vectors': len(terminals),
        'all_count_states': len(menus),
        'root_outcomes': [terminals[t] for t in sorted(root)],
        'new_ordered_path': path,
        'new_path_payoffs': [str(F(pays[target][b], scale)) for b in path],
        'new_complete_policy': policy_name,
        'new_complete_policy_sha256': hashlib.sha256(policy_raw).hexdigest(),
        'decision_histories': len(policy),
        'comparisons_including_self': len(slacks),
        'comparisons_nonself': len(slacks) - len(policy),
        'minimum_exact_IC_slack': str(F(min(slacks), scale)),
        'static_rival_count_vectors': len(rivals),
        'static_primal_pure_query': a,
        'static_primal_minimum_all_rivals': str(lower),
        'static_dual_pure_rival_counts': pure_rival,
        'static_dual_all_query_values': [str(z) for z in upper_row],
        'exact_static_matrix': matrix_name,
        'security': str(value),
        'tail_total': str(total),
        'exact_ratio': '1',
        'strong_aggregate_gap': '0',
        'original_ratio_float': x['ratio'],
    }


def main():
    result = {'status': 'exact finite audit of three saved inputs only', 'original_random_main_runs': 0,
              'numerical_optimizer_calls': 0, 'cases': [audit(name) for name in INPUTS]}
    (HERE / 'exact-three-saved-point-audit.json').write_text(dumps(result))
    for x in result['cases']:
        print(f"r={x['remaining_players']} customers={x['customers']} histories={x['decision_histories']} "
              f"IC={x['comparisons_including_self']} security={x['security']} P={x['tail_total']} gap=0")


if __name__ == '__main__':
    main()
