"""Exact finite replay of antichain-core lifting and integer unit expansion.
Fixed literal fixtures only; no random input, solver, floats, or network.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys


def states(game):
    return (dict(zip(game['weights'], choice))
            for choice in product(*(game['strategies'][i] for i in game['weights'])))


def cost(game, state, i):
    result = F(0)
    for e in state[i]:
        load = sum((w for j, w in game['weights'].items() if e in state[j]), F(0))
        result += sum((a * load**k for k, a in enumerate(game['fees'][e])), F(0))
    return result


def deviated(state, i, action):
    return {**state, i: action}


def core(game):
    minimal = {i: [a for a in acts if not any(b < a for b in acts)]
               for i, acts in game['strategies'].items()}
    mandatory = {i: frozenset.intersection(*acts) for i, acts in minimal.items()}
    background = {e: sum((w for i, w in game['weights'].items() if e in mandatory[i]), F(0))
                  for e in game['fees']}
    mobile = [i for i in game['weights'] if len(minimal[i]) > 1]
    shifted = {}
    for e, polynomial in game['fees'].items():
        shifted[e] = tuple(sum((polynomial[k] * comb(k, j) * background[e]**(k-j)
                                for k in range(j, len(polynomial))), F(0))
                           for j in range(len(polynomial)))
    output = {'weights': {i: game['weights'][i] for i in mobile},
              'strategies': {i: [a - mandatory[i] for a in minimal[i]] for i in mobile},
              'fees': shifted}
    def lift(state):
        return {i: state[i] | mandatory[i] if i in mobile else minimal[i][0]
                for i in game['weights']}
    return output, lift, mandatory, background


def unit_expand(game):
    blocks = {}; fees = {}
    for e, polynomial in game['fees'].items():
        blocks[e] = set()
        for k, coefficient in enumerate(polynomial):
            assert coefficient.denominator == 1 and coefficient >= 0
            for z in range(coefficient.numerator):
                name = (e, k, z); blocks[e].add(name)
                fees[name] = (F(0),)*k + (F(1),)
        assert blocks[e]  # integer-shifted unit resource has a nonzero leading term
    def image(a):
        return frozenset(x for e in a for x in blocks[e])
    return {'weights': game['weights'].copy(), 'fees': fees,
            'strategies': {i: [image(a) for a in acts] for i, acts in game['strategies'].items()}}, image


def fixture(name, weights, strategies, fees, integer_unit=False):
    return {'name': name, 'integer_unit': integer_unit,
            'weights': {i: F(w) for i, w in enumerate(weights)},
            'strategies': {i: [frozenset(a) for a in acts] for i, acts in enumerate(strategies)},
            'fees': {e: tuple(F(a) for a in polynomial) for e, polynomial in enumerate(fees)}}


def run():
    fixtures = [
        fixture('overlapping mandatory plus optional users, containment and fixed player', [2,1,3],
                [[[0,1],[0,2],[0,1,3]], [[0,1],[3]], [[0,2],[0,2,3]]],
                [[0,0,0,1],[0,0,1],[1],[0,1]], True),
        fixture('fractional weights and coefficients with zero fee', [F(3,2),F(2,3)],
                [[[0,1],[0,2]],[[0],[1]]], [[F(1,3),F(2,5),1],[0],[1,2]]),
        fixture('all players deleted, empty strategy dominates', [1,2],
                [[[],[0]],[[1],[0,1]]], [[0],[2]]),
        fixture('zero-degree and zero-cost mobile core', [1,3],
                [[[0],[1]],[[0],[1]]], [[0],[0]]),
        fixture('no mandatory sets, nonempty antichains', [1,2],
                [[[0],[1]],[[1],[0,2]]], [[1],[0,1],[0,0,1]], True),
    ]
    reports=[]; lifting_checks=0; cost_identities=0; expansion_checks=0
    for game in fixtures:
        h, lift, mandatory, background = core(game)
        for i, acts in h['strategies'].items():
            assert len(acts)>=2 and all(acts) and not frozenset.intersection(*acts)
            assert not any(a<b for a in acts for b in acts)
            assert len(set(acts))==len(acts)
        for i in game['weights']:
            assert mandatory[i] == frozenset.intersection(*game['strategies'][i])
        hs=list(states(h)); alpha_pne_counts={}
        for alpha in (F(1),F(3,2),F(4)):
            count=0
            for u in hs:
                s=lift(u)
                is_pne=all(cost(h,u,i)<=alpha*cost(h,deviated(u,i,t),i)
                           for i in h['weights'] for t in h['strategies'][i])
                if is_pne:
                    count+=1
                    for i in game['weights']:
                        for t in game['strategies'][i]:
                            assert cost(game,s,i)<=alpha*cost(game,deviated(s,i,t),i)
                            lifting_checks+=1
            alpha_pne_counts[str(alpha)]=count
        varying_baselines=False
        baselines={i:set() for i in h['weights']}
        for u in hs:
            s=lift(u)
            for i in h['weights']:
                base=cost(game,s,i)-cost(h,u,i)
                expected=sum((sum((a*(background[e]+sum((game['weights'][j] for j in h['weights'] if j!=i and e in u[j]),F(0)))**k for k,a in enumerate(game['fees'][e])),F(0)) for e in mandatory[i]),F(0))
                assert base==expected and base>=0
                baselines[i].add(base)
                for t in h['strategies'][i]:
                    assert cost(game,lift(deviated(u,i,t)),i)-cost(h,deviated(u,i,t),i)==base
                    cost_identities+=1
        varying_baselines=any(len(v)>1 for v in baselines.values())
        units=None
        if game['integer_unit']:
            q,image=unit_expand(h);units=len(q['fees'])
            for i,acts in h['strategies'].items():
                images=q['strategies'][i]
                assert all(images) and not frozenset.intersection(*images)
                for a in acts:
                    for b in acts: assert (a<=b)==(image(a)<=image(b))
            for u in hs:
                v={i:image(a) for i,a in u.items()}
                for i in h['weights']:
                    assert cost(h,u,i)==cost(q,v,i)
                    for t in h['strategies'][i]:
                        assert cost(h,deviated(u,i,t),i)==cost(q,deviated(v,i,image(t)),i)
                        expansion_checks+=1
        reports.append({'fixture':game['name'],'original_players':len(game['weights']),
                        'core_players':len(h['weights']),'core_states':len(hs),
                        'alpha_pne_counts':alpha_pne_counts,'varying_own_baseline':varying_baselines,
                        'integer_expanded_resources':units})
    assert reports[0]['varying_own_baseline']
    return {'status':'all exact Fraction checks passed','scope':'Five fixed fixtures only; finite replay does not prove arbitrary real-coefficient lifting or counterexample equivalence.',
            'arithmetic':'fractions.Fraction; no random input or numeric tolerance',
            'command':['python3',sys.argv[0]],'python':platform.python_version(),
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'fixtures':reports,'lifted_original_deviations_checked':lifting_checks,
            'own_action_baseline_identities':cost_identities,
            'unit_expanded_deviations_checked':expansion_checks}


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
