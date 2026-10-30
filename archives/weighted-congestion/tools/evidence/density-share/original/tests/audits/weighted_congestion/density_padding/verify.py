#!/usr/bin/env python3
"""Exact finite tests of padding projection/lift, not a universal proof."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import json

if not __debug__:
    raise RuntimeError('Run without -O')


def costs(weights, strategies, polynomials, state):
    selected = [strategies[i][a] for i,a in enumerate(state)]
    loads = [sum((weights[i] for i,s in enumerate(selected) if e in s), Q(0))
             for e in range(len(polynomials))]
    fees = [sum((a*loads[e]**k for k,a in enumerate(poly)), Q(0))
            for e,poly in enumerate(polynomials)]
    return tuple(sum((fees[e] for e in s), Q(0)) for s in selected)


def equilibrium(weights, strategies, polys, state, alpha):
    current = costs(weights, strategies, polys, state)
    for i,options in enumerate(strategies):
        for action in range(len(options)):
            deviation = list(state)
            deviation[i] = action
            if current[i] > alpha*costs(weights,strategies,polys,deviation)[i]:
                return False
    return True


def check_game(weights, strategies, polys, dummy_pairs):
    n = len(weights)
    expanded_w = weights+tuple(w for _,w in dummy_pairs)
    expanded_s = strategies+tuple((frozenset(),frozenset([e])) for e,_ in dummy_pairs)
    old_states = tuple(product(*(range(len(x)) for x in strategies)))
    new_states = tuple(product(*(range(len(x)) for x in expanded_s)))
    factors = [Q(1),Q(5,4),Q(9,5),Q(2),Q(100)]
    projected_checks = 0
    for alpha in factors:
        originals = {s for s in old_states if equilibrium(weights,strategies,polys,s,alpha)}
        augmented = {s for s in new_states if equilibrium(expanded_w,expanded_s,polys,s,alpha)}
        assert {s[:n] for s in augmented} == originals
        for state in augmented:
            for i,(e,_) in enumerate(dummy_pairs,start=n):
                if any(polys[e]):
                    assert state[i] == 0
            projection = state[:n]
            assert costs(expanded_w,expanded_s,polys,state)[:n] == costs(weights,strategies,polys,projection)
            for i,options in enumerate(strategies):
                for a in range(len(options)):
                    target = list(state); target[i] = a
                    old_target = list(projection); old_target[i] = a
                    assert costs(expanded_w,expanded_s,polys,target)[i] == costs(weights,strategies,polys,old_target)[i]
                    projected_checks += 1
        for state in originals:
            assert state+(0,)*len(dummy_pairs) in augmented
    return {'original_states':len(old_states),'augmented_states':len(new_states),
            'factors':list(map(str,factors)), 'deviation_cost_projection_checks':projected_checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate',type=Path)
    args = parser.parse_args()
    E = frozenset()
    inputs = [
        ((Q(1),), ((E,frozenset([0]),frozenset([1])),), ((Q(0),),(Q(0),)), ((0,Q(1,2)),(1,Q(3)))),
        ((Q(1),Q(3)), ((frozenset([0]),frozenset([1])),)*2,
         ((Q(0),Q(0),Q(1)),(Q(1),)), ((0,Q(1,3)),(0,Q(3)))),
        ((Q(1),Q(2),Q(1,2)), ((frozenset([0,2]),frozenset([1])),
         (frozenset([0]),frozenset([1,2])),(E,frozenset([0,1]))),
         ((Q(1),Q(2)),(Q(0),Q(0),Q(0),Q(1)),(Q(0),)),
         ((0,Q(1)),(1,Q(1,2)),(2,Q(2)))),
        ((Q(2),), ((E,frozenset([0,1])),), ((Q(3),),(Q(0),)),
         ((0,Q(1)),(1,Q(5)))),
    ]
    records = [check_game(*x) for x in inputs]
    # Boundary to extending the projection to arbitrary nondecreasing costs.
    step = lambda x: Q(0) if x<=1 else Q(1)
    assert step(Q(1)) == 0 and step(Q(2)) == 1
    assert Q(1,2)<=step(Q(2)) and step(Q(1))<=0
    assert Q(1,2)>100*step(Q(1))
    result = {'arithmetic':'Fraction only','games':records,'status':'passed',
              'step_projection_counterexample_checked':True,'scope':'finite checks only'}
    destination = args.generate or Path(__file__).with_name('verification.json')
    if args.generate:
        if destination.exists():parser.error('refusing to overwrite frozen evidence')
        destination.write_text(json.dumps(result,indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == result
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
