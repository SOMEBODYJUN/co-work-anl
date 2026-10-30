#!/usr/bin/env python3
"""Exact author audit of odd-ring selector mover support; no frozen files changed."""
from fractions import Fraction
from itertools import product
import hashlib
import json
import platform
from pathlib import Path


def selected(state):
    n = len(state)
    for i in range(n):
        if state[i] == state[(i + 1) % n]:
            target = list(state)
            target[i] ^= 1
            return i, tuple(target)
    raise AssertionError('Odd ring must have a defect')


def resource_cost(state, signature, mover, degree):
    if not signature[2 * mover + state[mover]]:
        return 0
    load = sum(signature[2 * j + state[j]] for j in range(len(state)))
    return load ** degree


def margin(state, signature, degree, alpha, mover=None):
    if mover is None:
        mover, target = selected(state)
    else:
        assert state[mover] == state[(mover + 1) % len(state)]
        target = list(state)
        target[mover] ^= 1
        target = tuple(target)
    return (resource_cost(state, signature, mover, degree)
            - alpha * resource_cost(target, signature, mover, degree))


def is_proper(signature):
    return all(not (signature[2 * i] and signature[2 * i + 1])
               for i in range(len(signature) // 2))


def single_defect_cycle(n, states):
    ground = [s for s in states if sum(s[i] == s[(i + 1) % n]
                                      for i in range(n)) == 1]
    assert len(ground) == 2 * n
    cycle = [ground[0]]
    while selected(cycle[-1])[1] != cycle[0]:
        nxt = selected(cycle[-1])[1]
        assert nxt not in cycle
        cycle.append(nxt)
    assert len(cycle) == 2 * n and set(cycle) == set(ground)
    assert [sum(selected(s)[0] == i for s in cycle)
            for i in range(n)] == [2] * n
    return cycle


def main():
    cases = []
    totals = {'pair_state_checks': 0, 'full_cycle_columns': 0,
              'proper_cycle_columns': 0, 'full_endpoint_columns': 0,
              'proper_endpoint_columns': 0, 'private_direction_rows': 0}
    for n in (3, 5, 7):
        states = list(product((0, 1), repeat=n))
        cycle = single_defect_cycle(n, states)
        endpoint_states = ((0,) * n, (1, 1) + (0,) * (n - 2))
        assert all(selected(s)[0] == 0 for s in endpoint_states)
        signatures = list(product((0, 1), repeat=2 * n)) if n <= 5 else None
        for degree in range(1, 7):
            q = 2 ** degree
            alphas = (Fraction(1), Fraction(7, 5),
                      Fraction(q) - Fraction(1, 10), Fraction(q))
            count_pair = 0
            for alpha in alphas:
                A, B = q - alpha, alpha * q - 1
                assert A >= 0 and B > 0
                if A:
                    r = A / B
                    assert 0 < r <= 1
                    lower = r ** (n - 1) / sum(r ** j for j in range(n))
                    assert 0 < lower <= Fraction(1, n)
                    if alpha == 1:
                        assert lower == Fraction(1, n)
                for i in range(n):
                    pair = []
                    for bit in (0, 1):
                        sig = [0] * (2 * n)
                        for j in (i, (i + 1) % n):
                            sig[2 * j + bit] = 1
                        assert is_proper(sig)
                        pair.append(sig)
                    for state in states:
                        # Exhaust every admissible defect choice, not only min-index.
                        for mover in range(n):
                            if state[mover] != state[(mover + 1) % n]:
                                continue
                            val = sum(margin(state, sig, degree, alpha, mover)
                                      for sig in pair)
                            if mover == i:
                                assert val == A
                            elif mover == (i + 1) % n:
                                assert val in (A, -B)
                            else:
                                assert val == 0
                            count_pair += 1
                # Private degree-zero columns force both action directions.
                for state in states:
                    for mover in range(n):
                        if state[mover] != state[(mover + 1) % n]:
                            continue
                        for owner in range(n):
                            for bit in (0, 1):
                                sig = [0] * (2 * n)
                                sig[2 * owner + bit] = 1
                                expected = 0
                                if mover == owner:
                                    expected = 1 if state[mover] == bit else -alpha
                                assert margin(state, sig, 0, alpha, mover) == expected
                                totals['private_direction_rows'] += 1
            count_full = count_proper = 0
            if signatures is not None:
                for sig in signatures:
                    if not any(sig):
                        continue
                    proper = is_proper(sig)
                    for k in range(degree + 1):
                        # Every tested complete/proper column telescopes at alpha=1.
                        assert sum(margin(s, sig, k, Fraction(1))
                                   for s in cycle) == 0
                        # Endpoint one-mover certificate for the complete cone.
                        assert sum(margin(s, sig, k, Fraction(q))
                                   for s in endpoint_states) <= 0
                        count_full += 1
                        count_proper += proper
            totals['pair_state_checks'] += count_pair
            totals['full_cycle_columns'] += count_full
            totals['proper_cycle_columns'] += count_proper
            totals['full_endpoint_columns'] += count_full
            totals['proper_endpoint_columns'] += count_proper
            cases.append({'players': n, 'degree': degree,
                          'alphas': [str(a) for a in alphas],
                          'cycle_states': len(cycle),
                          'pair_state_checks': count_pair,
                          'full_cycle_and_endpoint_columns_each': count_full,
                          'proper_cycle_and_endpoint_columns_each': count_proper,
                          'all_mover_theorem_applies': ['alpha < 2^d only'],
                          'all_defect_choices_pair_private': True,
                          'endpoint_single_mover': n <= 5})
    result = {'status': 'passed', 'arithmetic': 'exact integers/Fraction',
              'seed': None, 'external_solver': None,
              'python': platform.python_version(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'coverage': totals, 'cases': cases,
              'scope': 'finite implementation audit; arbitrary-parameter statements require proof'}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
