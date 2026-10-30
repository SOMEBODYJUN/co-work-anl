"""Definition-level Fraction checks for the minimum potential-user share bound."""
from fractions import Fraction as F
from itertools import product
import json
import argparse
import hashlib
import platform
from pathlib import Path
import random


def verify(weights, actions, coefficients, k):
    n, number_resources = len(weights), len(coefficients)
    users = [set(i for i in range(n) if any(e in action for action in actions[i])) for e in range(number_resources)]
    shares = [weights[i] / sum(weights[j] for j in group) for group in users for i in group]
    q = min(shares) if shares else F(1)
    beta = 1-(1-q)**k
    assert 0 < beta <= 1
    alpha = 1 / beta

    def evaluate(state):
        loads = [sum(weights[i] for i in range(n) if e in actions[i][state[i]]) for e in range(number_resources)]
        counts = [sum(e in actions[i][state[i]] for i in range(n)) for e in range(number_resources)]
        resource_costs = [sum(c * loads[e]**j for j, c in coefficients[e].items()) for e in range(number_resources)]
        costs = [sum(resource_costs[e] for e in actions[i][state[i]]) for i in range(n)]
        potential = sum(coefficients[e].get(0, 0) * counts[e] + sum(c * loads[e]**j for j, c in coefficients[e].items() if j > 0) for e in range(number_resources))
        return costs, potential, resource_costs

    states = list(product(*[range(len(family)) for family in actions]))
    values = {state: evaluate(state) for state in states}
    minimum = min(value[1] for value in values.values())
    moves = strict = minimizers = 0
    for state in states:
        current, potential, resource_costs = values[state]
        is_minimizer = potential == minimum
        minimizers += is_minimizer
        for i in range(n):
            for action_label in range(len(actions[i])):
                after = list(state)
                after[i] = action_label
                after = tuple(after)
                deviated, new_potential, _ = values[after]
                common = sum(resource_costs[e] for e in actions[i][state[i]] & actions[i][action_label])
                assert new_potential-potential <= deviated[i]-beta*current[i]-(1-beta)*common
                if current[i] > alpha*deviated[i]:
                    assert new_potential < potential
                    strict += 1
                if is_minimizer:
                    assert current[i] <= alpha*deviated[i]
                moves += 1
    return len(states), moves, strict, minimizers, str(q), str(alpha)


def main():
    rng = random.Random(20261015)
    games = []
    # Empty strategies, all-empty resource supports, and q=1.
    games.append(((F(7, 3),), [(frozenset(), frozenset({0}))], [{0:F(3), 3:F(5)}], 3))
    games.append(((F(1), F(2)), [(frozenset(),), (frozenset(),)], [{0:F(8), 4:F(2)}], 4))
    # Retained shared resource, asymmetric weights, zero costs.
    games.append(((F(1, 7), F(5, 3), F(2)),
                  [(frozenset({0}), frozenset({0,1})), (frozenset(), frozenset({0,2})), (frozenset({1}), frozenset({0,1,2}))],
                  [{0:F(2),3:F(5),5:F(3)}, {0:F(7),4:F(2)}, {}], 3))
    for _ in range(200):
        n = rng.randint(1,4)
        number_resources = rng.randint(1,4)
        weights = tuple(F(rng.randint(1,9), rng.randint(1,7)) for _ in range(n))
        all_actions = [frozenset(e for e in range(number_resources) if mask >> e & 1) for mask in range(1 << number_resources)]
        actions = [tuple(rng.sample(all_actions, rng.randint(1, min(4,len(all_actions))))) for _ in range(n)]
        k = rng.randint(1,4)
        d = k+rng.randint(0,2)
        coefficients = [{j:F(rng.randint(0,4), rng.randint(1,4)) for j in [0]+list(range(k,d+1))} for _ in range(number_resources)]
        games.append((weights, actions, coefficients, k))
    results = [verify(*game) for game in games]
    return dict(seed=20261015,
                python_version=platform.python_version(),
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                game_count=len(results),
                states=sum(x[0] for x in results),
                deviations=sum(x[1] for x in results),
                strict_factor_improvements=sum(x[2] for x in results),
                potential_minimizers=sum(x[3] for x in results),
                q_one_case=dict(q=results[0][4],alpha=results[0][5]),
                empty_support_case=dict(q=results[1][4],alpha=results[1][5]),
                evidence_scope='Finite exact regression for all moves and all global minima; not the general proof.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', type=Path)
    args = parser.parse_args()
    report = main()
    if args.generate:
        with args.generate.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    else:
        frozen = Path(__file__).resolve().parents[4] / 'evidence/runs/weighted_congestion/high_degree_share/independent_verification.json'
        assert json.loads(frozen.read_text()) == report, 'frozen record mismatch'
    print(json.dumps(report, ensure_ascii=False))
