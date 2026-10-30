#!/usr/bin/env python3
"""Finite, literal, exact-arithmetic audit; not a proof of the universal theorem."""
from fractions import Fraction as Q
from itertools import product
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

EXPECTED_FREEZE = '0b7735af99dbd9657710fa5c5f94ed4af00649833bad3d60d1c1dd32caa4eb29'
ALPHAS = tuple(map(Q, ('1', '4/3', '3/2', '2', '5', '100')))

def s(*resources):
    return frozenset(resources)

def poly(*coefficients):
    return tuple(map(Q, coefficients))

@dataclass
class Game:
    weights: tuple
    coefficients: dict
    strategies: tuple

    def states(self):
        return product(*self.strategies)

# Literal cost evaluator: no theorem cost decomposition is used here.
def cost(game, profile, player):
    answer = Q(0)
    for resource in profile[player]:
        load = sum((game.weights[j] for j in range(len(game.weights))
                    if resource in profile[j]), Q(0))
        answer += sum((a * load ** k for k, a in enumerate(game.coefficients[resource])), Q(0))
    return answer

def deviated(profile, player, action):
    return tuple(action if j == player else old for j, old in enumerate(profile))

def pne(game, profile, alpha):
    return all(cost(game, profile, i) <= alpha * cost(game, deviated(profile, i, action), i)
               for i, actions in enumerate(game.strategies) for action in actions)

# Deliberately elementary expansion, multiplying by x+B once per source degree.
def shifted(coefficients, background):
    out = [Q(0)] * len(coefficients)
    for k, coefficient in enumerate(coefficients):
        power = [Q(1)]
        for _ in range(k):
            next_power = [Q(0)] * (len(power) + 1)
            for exponent, entry in enumerate(power):
                next_power[exponent] += background * entry
                next_power[exponent + 1] += entry
            power = next_power
        for exponent, entry in enumerate(power):
            out[exponent] += coefficient * entry
    return tuple(out)

def core(game):
    minimal = tuple(tuple(a for a in actions if not any(b < a for b in actions))
                    for actions in game.strategies)
    mandatory = tuple(frozenset.intersection(*actions) for actions in minimal)
    players = tuple(i for i, actions in enumerate(minimal) if len(actions) > 1)
    background = {e: sum((game.weights[i] for i, a in enumerate(mandatory) if e in a), Q(0))
                  for e in game.coefficients}
    if not players:
        return None, minimal, mandatory, players, background
    output = Game(tuple(game.weights[i] for i in players),
                  {e: shifted(c, background[e]) for e, c in game.coefficients.items()},
                  tuple(tuple(a - mandatory[i] for a in minimal[i]) for i in players))
    return output, minimal, mandatory, players, background

def lift(profile, minimal, mandatory, players):
    active = dict(zip(players, profile))
    return tuple((mandatory[i] | active[i]) if i in active else minimal[i][0]
                 for i in range(len(minimal)))

def structure(game):
    assert game.weights and game.coefficients
    for actions in game.strategies:
        assert len(actions) >= 2 and len(set(actions)) == len(actions)
        assert all(actions)
        assert not frozenset.intersection(*actions)
        assert all(not (a <= b) for a in actions for b in actions if a != b)

FIXTURES = (
    ('all_deleted_empty_and_inclusions',
     Game((Q(2), Q(3), Q(5)), {'a':poly(0), 'b':poly(1,1), 'c':poly(0,0,2)},
          ((s(),s('a'),s('a','b')), (s('a'),s('a','b'),s('a','c')),
           (s('b'),s('b','c')))),
     (), (s(),s('a'),s('b'))),
    ('overlapping_mandatory_and_zero_resources',
     Game((Q(2),Q(3),Q(1),Q(4)),
          {'a':poly(1,0,1),'b':poly(0),'c':poly(0,2),'d':poly(0,0,0,1),
           'e':poly(0),'z':poly(0)},
          ((s('a','b'),s('a','c'),s('a','b','c'),s('a','b','z')),
           (s('a','b','d'),s('a','c','d'),s('a','b','c','d')),
           (s('d'),s('d','z')),(s(),s('z')))),
     (0,1), (s('a'),s('a','d'),s('d'),s())),
    ('integer_monomial_optional_mandatory_overlap',
     Game((Q(2),Q(1),Q(3)),
          {'a':poly(0,0,1),'b':poly(0,0,0,1),'c':poly(0,1),
           'd':poly(1),'e':poly(0,0,1)},
          ((s('a','b'),s('a','c'),s('a','b','c')),
           (s('d','a'),s('d','c'),s('d','a','c')),
           (s('d'),s('d','e')))),
     (0,1), (s('a'),s('d'),s('d'))),
    ('degree_zero_and_rational_weights',
     Game((Q('1/2'),Q('3/2'),Q(2)),
          {'a':poly(0),'b':poly(2),'c':poly(5)},
          ((s('a','b'),s('a','c')), (s('a','b'),s('a','c')),
           (s(),s('a')))),
     (0,1), (s('a'),s('a'),s())),
    ('mandatory_baseline_masks_reverse_projection',
     Game((Q(1),), {'a':poly(100),'b':poly(10),'c':poly(1)},
          ((s('a','b'),s('a','c')),)),
     (0,), (s('a'),)),
    ('all_zero_active_with_empty_fixed_player',
     Game((Q('2/3'),Q('5/4')), {'a':poly(0),'b':poly(0),'c':poly(0)},
          ((s('a'),s('b')), (s(),s('c')))),
     (0,), (s(),s())),
)

def clone_integer_polynomials(game):
    blocks = {}
    coefficients = {}
    for resource, entries in game.coefficients.items():
        block = []
        for exponent, entry in enumerate(entries):
            assert entry.denominator == 1 and entry >= 0
            for copy in range(int(entry)):
                label = (resource, exponent, copy)
                block.append(label)
                coefficients[label] = (Q(0),) * exponent + (Q(1),)
        assert block  # All shifted source unit monomials retain their leading coefficient.
        blocks[resource] = frozenset(block)
    def expand(action):
        return frozenset().union(*(blocks[e] for e in action))
    return Game(game.weights, coefficients,
                tuple(tuple(expand(a) for a in actions) for actions in game.strategies)), expand


def audit_fixture(name, game, expected_players, expected_mandatory):
    output, minimal, mandatory, players, background = core(game)
    assert players == expected_players and mandatory == expected_mandatory
    # Independent set identity on all original actions.
    assert mandatory == tuple(frozenset.intersection(*actions) for actions in game.strategies)
    for i, actions in enumerate(game.strategies):
        assert all(any(a <= t for a in minimal[i]) for t in actions)
    record = {'fixture':name, 'original_states':sum(1 for _ in game.states()),
              'retained_players':list(players), 'alpha_values':[str(a) for a in ALPHAS]}
    if output is None:
        exact = tuple(actions[0] for actions in minimal)
        assert pne(game, exact, Q(1))
        record.update(branch='explicit_exact_PNE', core_states=0, lift_checks=0)
        return record
    structure(output)
    assert len(output.coefficients) == len(game.coefficients)
    assert all(all(a >= 0 for a in entries) for entries in output.coefficients.values())
    state_count = lift_checks = decomposition_checks = superset_checks = 0
    equilibrium_counts = {str(a):0 for a in ALPHAS}
    for profile in output.states():
        state_count += 1
        original = lift(profile,minimal,mandatory,players)
        for resource in game.coefficients:
            actual_load = sum((game.weights[i] for i in range(len(game.weights))
                               if resource in original[i]), Q(0))
            optional_load = sum((output.weights[j] for j in range(len(players))
                                 if resource in profile[j]), Q(0))
            assert actual_load == background[resource] + optional_load
        for local, original_player in enumerate(players):
            baseline = sum((sum((a * sum((game.weights[j] for j in range(len(game.weights))
                                  if e in original[j]),Q(0)) ** k
                                  for k,a in enumerate(game.coefficients[e])),Q(0))
                            for e in mandatory[original_player]),Q(0))
            assert cost(game,original,original_player) == cost(output,profile,local) + baseline
            for a in minimal[original_player]:
                original_dev = deviated(original,original_player,a)
                core_dev = deviated(profile,local,a-mandatory[original_player])
                assert cost(game,original_dev,original_player) == cost(output,core_dev,local) + baseline
                decomposition_checks += 1
            for t in game.strategies[original_player]:
                for a in minimal[original_player]:
                    if a <= t:
                        assert cost(game,deviated(original,original_player,a),original_player) <= cost(game,deviated(original,original_player,t),original_player)
                        superset_checks += 1
        for alpha in ALPHAS:
            if pne(output,profile,alpha):
                equilibrium_counts[str(alpha)] += 1
                assert pne(game,original,alpha)
                lift_checks += 1
    if name == 'mandatory_baseline_masks_reverse_projection':
        original = (s('a','b'),)
        profile = (s('b'),)
        assert pne(game,original,Q(2)) and not pne(output,profile,Q(2))
        record['reverse_projection_counterexample_verified'] = True
    if name == 'integer_monomial_optional_mandatory_overlap':
        # Hard-coded expansion catches an implementation mistake in the shift itself.
        assert output.coefficients['a'] == poly(4,4,1)
        assert background['a'] == Q(2) and background['d'] == Q(4)
        cloned,expand = clone_integer_polynomials(output)
        structure(cloned)
        clone_checks = 0
        for profile in output.states():
            clone_profile = tuple(expand(a) for a in profile)
            for i,actions in enumerate(output.strategies):
                assert cost(output,profile,i) == cost(cloned,clone_profile,i)
                clone_checks += 1
                for action in actions:
                    assert cost(output,deviated(profile,i,action),i) == cost(cloned,deviated(clone_profile,i,expand(action)),i)
                    clone_checks += 1
            for alpha in ALPHAS:
                assert pne(output,profile,alpha) == pne(cloned,clone_profile,alpha)
        for actions in output.strategies:
            for a in actions:
                for b in actions:
                    assert (a <= b) == (expand(a) <= expand(b))
        record['unit_monomial_clone_resources'] = len(cloned.coefficients)
        record['exact_clone_cost_checks'] = clone_checks
    record.update(branch='core',core_states=state_count,lift_checks=lift_checks,
                  decomposition_checks=decomposition_checks,superset_checks=superset_checks,
                  core_equilibrium_counts=equilibrium_counts)
    return record

result = {'scope':'Six literal finite fixtures, exact Fraction costs; not a universal proof.',
          'frozen_proof_sha256':EXPECTED_FREEZE,
          'fixture_count':len(FIXTURES),
          'fixtures':[audit_fixture(*fixture) for fixture in FIXTURES]}
print(json.dumps(result,indent=2))
