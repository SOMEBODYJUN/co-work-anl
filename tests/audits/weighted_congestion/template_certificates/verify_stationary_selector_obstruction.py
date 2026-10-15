#!/usr/bin/env python3
"""Exact audit of the unit-speed stationary-selector restriction obstruction.

No randomness, floating arithmetic, solver status, or epsilon tolerance is used.
Default: print JSON to stdout. --output NEW_PATH uses exclusive creation.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import sys


def template(k: int):
    """Return every binary state, full selector, displayed cycle, and weights."""
    assert k >= 1
    n = k + 1
    weights = (Q(1, k*k),)*k + (Q(1),)
    state = [0]*n
    cycle = [tuple(state)]
    for i in range(k):
        state[i] = 1
        cycle.append(tuple(state))
    state[k] = 1
    cycle.append(tuple(state))
    for i in range(k):
        state[i] = 0
        cycle.append(tuple(state))
    assert len(cycle) == len(set(cycle)) == 2*n
    successors = {s: cycle[(j+1) % len(cycle)]
                  for j, s in enumerate(cycle)}
    all_states = tuple(product((0, 1), repeat=n))
    for s in all_states:
        if s not in successors:
            t = list(s)
            t[next(i for i, bit in enumerate(s) if bit)] = 0
            successors[s] = tuple(t)
    movers = {s: next(i for i in range(n) if s[i] != successors[s][i])
              for s in all_states}
    assert all(sum(a != b for a, b in zip(s, successors[s])) == 1
               for s in all_states)
    return all_states, successors, tuple(cycle), weights, movers


def audit(k: int):
    states, successor, cycle, weights, movers = template(k)
    n = len(weights)
    zero = Q(0)
    uniform = {s: Q(s in cycle, len(cycle)) for s in states}
    total_weight = sum(weights, zero)
    weighted = {s: weights[movers[s]]/(2*total_weight) if s in cycle else zero
                for s in states}
    assert sum(uniform.values(), zero) == sum(weighted.values(), zero) == 1

    # Literal whole-state stationarity, and the finite unique-cycle test.
    def push(distribution):
        image = dict.fromkeys(states, zero)
        for s in states:
            image[successor[s]] += distribution[s]
        return image

    assert push(uniform) == uniform
    weighted_residual = max(abs(push(weighted)[s]-weighted[s]) for s in states)
    assert (weighted_residual == 0) == (k == 1)
    transient_steps = []
    for s in states:
        q, visited, steps = s, set(), 0
        while q not in cycle:
            assert q not in visited
            visited.add(q)
            assert sum(successor[q]) == sum(q)-1
            q = successor[q]
            steps += 1
        assert steps <= n
        transient_steps.append(steps)
    visited = []
    q = cycle[0]
    while q not in visited:
        visited.append(q)
        q = successor[q]
    assert q == cycle[0] and tuple(visited) == cycle

    # Independent cost and finite-set potential oracles for ALL signatures.
    identities = columns = zero_columns = 0
    for signature in product((0, 1), repeat=2*n):
        if not any(signature):
            continue

        def users(s):
            return tuple(i for i in range(n) if signature[2*i+s[i]])

        def load(s):
            return sum((weights[i] for i in users(s)), zero)

        for degree in (0, 1):
            def potential(s):
                active = users(s)
                x = sum((weights[i] for i in active), zero)
                if degree == 0:
                    return x
                return (x*x+sum((weights[i]**2 for i in active), zero))/2

            value = zero
            for s in states:
                t = successor[s]
                i = movers[s]
                # Recompute the load at t; do not freeze the old load.
                old = signature[2*i+s[i]]*load(s)**degree
                new = signature[2*i+t[i]]*load(t)**degree
                assert weights[i]*(old-new) == potential(s)-potential(t)
                identities += 1
                value += weighted[s]*(old-new)
            assert value == 0
            columns += 1
            zero_columns += value == 0

    # The witness column uses label 1 for each player and has cost x.
    old = new = zero
    for s in cycle:
        t = successor[s]
        i = movers[s]
        old += s[i]*sum((weights[j]*s[j] for j in range(n)), zero)
        new += t[i]*sum((weights[j]*t[j] for j in range(n)), zero)
    expected_old = Q((2*k+1)*(k+1), 2*k)
    expected_new = Q(3*(k+1), 2*k)
    threshold = Q(2*k+1, 3)
    assert old == expected_old and new == expected_new
    assert threshold*new == old
    assert (old-threshold*new)/len(cycle) == 0  # exact weak boundary
    alpha_below = threshold-Q(1, 3) if k >= 2 else None
    alpha_above = threshold+Q(1, 3)
    assert (old-alpha_above*new)/len(cycle) < 0
    if k >= 2:
        assert alpha_below >= 1
        assert (old-alpha_below*new)/len(cycle) > 0
    return {
        'K': k, 'players': n, 'light_weight': str(weights[0]),
        'states_checked': len(states), 'unique_cycle_length': len(cycle),
        'max_transient_steps': max(transient_steps),
        'nonempty_signatures_checked': 2**(2*n)-1,
        'affine_columns_checked': columns,
        'single_edge_potential_identities_checked': identities,
        'weighted_dual_zero_columns': zero_columns,
        'weighted_stationarity_residual': str(weighted_residual),
        'witness_current_sum': str(old), 'witness_true_next_sum': str(new),
        'unit_speed_stationary_witness_threshold': str(threshold),
        'strict_below_alpha': str(alpha_below) if alpha_below is not None else None,
        'strict_below_margin': (str((old-alpha_below*new)/len(cycle))
                                if alpha_below is not None else None),
        'equality_boundary_checked': True,
    }


def audit_arbitrary_affine_selectors():
    """Exhaust all 256 tagged selectors on a two-player binary template.

    Each state chooses (player, target-label), so current-action choices and
    self-loop cycles are included, with both possible tagged movers retained.
    This only audits the general affine lemma; its proof covers arbitrary size.
    """
    states = tuple(product((0, 1), repeat=2))
    choices = tuple(product(range(2), repeat=2))
    weights_cases = ((Q(1), Q(1)), (Q(1), Q(2)), (Q(1, 7), Q(11, 3)))
    zero = Q(0)
    selectors_checked = self_loop_cycles = columns_checked = 0
    for weights in weights_cases:
        for selected in product(choices, repeat=len(states)):
            selector = dict(zip(states, selected))
            successor = {}
            for s, (i, target) in selector.items():
                t = list(s)
                t[i] = target
                successor[s] = tuple(t)
            path = []
            q = states[0]
            while q not in path:
                path.append(q)
                q = successor[q]
            cycle = tuple(path[path.index(q):])
            assert cycle and successor[cycle[-1]] == cycle[0]
            normalizer = sum((weights[selector[s][0]] for s in cycle), zero)
            lam = {s: (weights[selector[s][0]]/normalizer if s in cycle else zero)
                   for s in states}
            assert sum(lam.values(), zero) == 1
            self_loop_cycles += len(cycle) == 1
            for signature in product((0, 1), repeat=4):
                if not any(signature):
                    continue

                def load(s):
                    return sum((weights[i]*signature[2*i+s[i]] for i in range(2)), zero)

                for degree in (0, 1):
                    alpha_one = alpha_larger = zero
                    for s in states:
                        i = selector[s][0]
                        t = successor[s]
                        old = signature[2*i+s[i]]*load(s)**degree
                        new = signature[2*i+t[i]]*load(t)**degree
                        alpha_one += lam[s]*(old-new)
                        alpha_larger += lam[s]*(old-Q(3, 2)*new)
                    assert alpha_one == 0 and alpha_larger <= 0
                    columns_checked += 1
            selectors_checked += 1
    return {
        'weight_vectors': [[str(w) for w in weights] for weights in weights_cases],
        'selectors_per_weight_vector': len(choices)**len(states),
        'selectors_checked': selectors_checked,
        'selected_self_loop_cycles': self_loop_cycles,
        'affine_columns_checked_at_each_alpha': columns_checked,
        'alpha_values': ['1', '3/2'],
        'limitations': 'Finite two-player audit; the arbitrary-size affine lemma follows from telescoping.'
    }


def audit_empty_action_cycle_separation():
    """Literal quadratic fixture: empty actions give PNE but its old cycle remains.

    This tests the fixed-incidence cone of FOUR resource columns, not all
    possible signatures of a three-action canonical template.
    """
    weights = (Q(1), Q(2))
    resources = (
        ((0, 1, 0, 1), 1, Q(13)),
        ((0, 1, 1, 0), 2, Q(3)),
        ((1, 0, 0, 1), 2, Q(3)),
        ((1, 0, 1, 0), 1, Q(13)),
    )
    states = tuple(product(range(3), repeat=2))
    cycle = ((0, 0), (1, 0), (1, 1), (0, 1))
    successor = {s: cycle[(j+1) % len(cycle)] for j, s in enumerate(cycle)}
    for s in states:
        if s not in successor:
            i = next(i for i, action in enumerate(s) if action == 2)
            t = list(s)
            t[i] = 0
            successor[s] = tuple(t)
    movers = {s: next(i for i in range(2) if s[i] != successor[s][i]) for s in states}

    def uses(resource, i, action):
        return 0 if action == 2 else resource[0][2*i+action]

    def basis_cost(s, i, resource):
        if not uses(resource, i, s[i]):
            return Q(0)
        load = sum((weights[j]*uses(resource, j, s[j]) for j in range(2)), Q(0))
        return load**resource[1]

    def cost(s, i):
        return sum((resource[2]*basis_cost(s, i, resource) for resource in resources), Q(0))

    alpha = Q(52, 51)
    threshold = Q(53, 51)
    rows, records = {}, []
    for s in states:
        i, t = movers[s], successor[s]
        assert sum(a != b for a, b in zip(s, t)) == 1
        row = tuple(basis_cost(s, i, r)-alpha*basis_cost(t, i, r) for r in resources)
        margin = cost(s, i)-alpha*cost(t, i)
        assert margin == sum((r[2]*b for r, b in zip(resources, row)), Q(0))
        rows[s] = row
        q, visited = s, set()
        while q not in cycle:
            assert q not in visited
            visited.add(q)
            assert successor[q].count(2) == q.count(2)-1
            q = successor[q]
        records.append({
            'state': list(s), 'costs': [str(cost(s, j)) for j in range(2)],
            'selected_player_zero_based': i, 'true_next_state': list(t),
            'selected_old_cost': str(cost(s, i)), 'selected_new_cost': str(cost(t, i)),
            'margin': str(margin), 'player_weight_times_margin': str(weights[i]*margin),
            'basis_margin_row': list(map(str, row)),
        })
    assert all(cost((2, 2), i) == 0 for i in range(2))
    # Empty deviations also eliminate every old state as an exact PNE.
    assert all(cost(s, i) >= 0 for s in states for i in range(2))
    assert all(b <= 0 for b in rows[(2, 2)])
    cycle_ratios = tuple(cost(s, movers[s])/cost(successor[s], movers[s]) for s in cycle)
    assert cycle_ratios == (Q(21, 20), threshold, Q(21, 20), threshold)
    margins = tuple(cost(s, movers[s])-alpha*cost(successor[s], movers[s]) for s in cycle)
    assert margins == (Q(62, 51), Q(1), Q(62, 51), Q(1))
    assert min(margins) > 0
    boundary = tuple(cost(s, movers[s])-threshold*cost(successor[s], movers[s]) for s in cycle)
    assert boundary == (Q(22, 51), Q(0), Q(22, 51), Q(0))
    # For ANY normalized nonnegative lambda on Q, the coefficient-weighted
    # dual sum is >= min(margins) = 1 > 0, so such lambda cannot be dual.
    assert min(margins) == 1
    return {
        'weights': list(map(str, weights)),
        'resources': [{'binary_action_signature': list(sig), 'degree': k,
                       'coefficient': str(coef)} for sig, k, coef in resources],
        'empty_action_label': 2, 'states_checked': len(states),
        'unique_recurrent_cycle': [list(s) for s in cycle],
        'alpha_checked': str(alpha), 'strict_cycle_threshold': str(threshold),
        'cycle_cost_ratios': list(map(str, cycle_ratios)),
        'cycle_margins': list(map(str, margins)),
        'boundary_margins': list(map(str, boundary)),
        'any_recurrent_probability_weighted_margin_lower_bound': '1',
        'transient_delta_dual_state': [2, 2],
        'transient_delta_dual_column_values': list(map(str, rows[(2, 2)])),
        'rows': records,
        'limitations': ('All games in this FOUR-column fixed-incidence cone have '
                        'the all-empty exact PNE. This is not a full-signature '
                        'dual certificate or a full-class growth lower bound.'),
    }


def audit_small_recurrent_support_alternatives():
    """Exact primal/dual certificates on tiny row restrictions; no LP status."""
    positive_cycle_rows = ((Q(1), Q(0)), (Q(0), Q(1)))
    coefficients = (Q(1), Q(1))
    margins = tuple(sum((x*y for x, y in zip(row, coefficients)), Q(0))
                    for row in positive_cycle_rows)
    assert margins == (Q(1), Q(1))
    full_rows = positive_cycle_rows+((Q(-1), Q(-1)),)
    transient_delta = (Q(0), Q(0), Q(1))
    values = tuple(sum((transient_delta[i]*full_rows[i][j] for i in range(3)), Q(0))
                   for j in range(2))
    assert values == (Q(-1), Q(-1))
    dual_cycle_rows = ((Q(1), Q(-2)), (Q(-2), Q(1)))
    cyclic_dual = (Q(1, 2), Q(1, 2))
    dual_values = tuple(sum((cyclic_dual[i]*dual_cycle_rows[i][j] for i in range(2)), Q(0))
                        for j in range(2))
    assert dual_values == (Q(-1, 2), Q(-1, 2))
    return {
        'cases_checked': 2,
        'positive_cycle_primal_margins': list(map(str, margins)),
        'full_matrix_transient_dual_values': list(map(str, values)),
        'other_cycle_dual_values': list(map(str, dual_values)),
        'limitations': 'Tiny matrix certificate checks; general equivalence is proved separately.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    records = [audit(k) for k in (1, 2, 3, 4)]
    report = {
        'schema_version': 1, 'status': 'PASS',
        'arithmetic': 'fractions.Fraction; no tolerance',
        'seed': None, 'randomness': 'none',
        'python_version': sys.version.split()[0],
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'K_values': [1, 2, 3, 4], 'records': records,
        'arbitrary_affine_selector_audit': audit_arbitrary_affine_selectors(),
        'empty_action_cycle_separation': audit_empty_action_cycle_separation(),
        'small_recurrent_support_alternatives': audit_small_recurrent_support_alternatives(),
        'limitations': (
            'Finite exact implementation audit. The general K theorem is in the '
            'proof, not inferred from this enumeration. Only unit-speed '
            'stationarity is obstructed. The explicit nonstationary dual is '
            'verified for degrees 0 and 1; no full-class d/log d conclusion.'),
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as output:
            output.write(payload)
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
