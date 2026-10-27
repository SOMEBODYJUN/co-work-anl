"""Literal unit-customer audit of the main researcher's middle-SAFE formula.

The canonical solver is used only to generate complete policies. Checking uses
full ordered histories, unit customers and Fraction, with no author row code.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import random
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'work.py').exists())
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def check(coverage, players, seed):
    rng = random.Random(seed)
    instance = Instance.from_topic_sets(coverage, players)
    solver = ExactSPESolver(instance)
    certificate = solver.certificate(
        action_selector=lambda history, options: rng.choice(options),
        continuation_selector=lambda history, options: rng.choice(options))
    policy = certificate.actions
    clients = sorted(set().union(*coverage))
    likes = {x: frozenset(i for i, topic in enumerate(coverage) if x in topic)
             for x in clients}
    alphabet = tuple(range(len(coverage)))

    @lru_cache(None)
    def finish(history):
        if len(history) == players:
            return history
        return finish(history+(policy[history],))

    @lru_cache(None)
    def utilities(terminal):
        load = {x: sum(a in likes[x] for a in terminal) for x in clients}
        return tuple(sum((F(1, load[x]) for x in clients if a in likes[x]), F())
                     for a in terminal)

    ic_checks = safe_checks = 0
    nonanonymous = False
    seen = {}
    for depth in range(players):
        for history in product(alphabet, repeat=depth):
            assert history in policy
            prescribed = finish(history)
            actual_u = utilities(prescribed)[depth]
            key = tuple(history.count(a) for a in alphabet)
            if key in seen and policy[history] != seen[key]:
                nonanonymous = True
            seen[key] = policy[history]
            old = {x: sum(a in likes[x] for a in history) for x in clients}
            k = players-depth
            for topic in alphabet:
                leaf = finish(history+(topic,))
                payoffs = utilities(leaf)
                assert actual_u >= payoffs[depth]
                ic_checks += 1
                prefix = dict(old)
                for x in clients:
                    prefix[x] += topic in likes[x]
                # l starts at 1; k-l includes this tail player.
                for l in range(1, k):
                    actor = depth+l
                    for query in alphabet:
                        safe = sum((F(1, prefix[x]+k-l) for x in clients
                                    if query in likes[x]), F())
                        direct = finish(leaf[:actor]+(query,))
                        deviation_u = utilities(direct)[actor]
                        assert payoffs[actor] >= deviation_u >= safe
                        # Exact literal formula in the submitted statement.
                        formula = F()
                        for x in clients:
                            b = old[x]
                            t = int(topic in likes[x])
                            y = [int(a in likes[x]) for a in leaf[depth+1:]]
                            total = b+t+sum(y)
                            value = F(y[l-1], total) if y[l-1] else F()
                            if query in likes[x]:
                                value -= F(1, b+t+sum(y[:l-1])+k-l)
                            formula += value
                        assert formula == payoffs[actor]-safe >= 0
                        safe_checks += 1
                    for x in clients:
                        prefix[x] += leaf[actor] in likes[x]
    assert len(policy) == sum(len(alphabet)**d for d in range(players))
    return {
        'players': players, 'catalog_size': len(alphabet),
        'unit_customers': len(clients), 'ordered_history_nodes': len(policy),
        'literal_full_strategy_ic_checks': ic_checks,
        'middle_safe_checks': safe_checks,
        'different_actions_at_same_counts': nonanonymous,
    }


def main():
    cases = [([set()], 6, 681061),
             ([{0}, set()], 6, 681062),
             ([{0, 1, 2}, {3}, {4}, {5}], 6, 681063),
             ([{0, 1, 3, 5}, {1, 2, 4}, {0, 2, 5}, {1, 3, 4, 5}], 6, 681064)]
    rows = [check(*case) for case in cases]
    report = {'status': 'PASS',
              'scope': 'formula/implementation checks; general validity is proved analytically; not a welfare proof',
              'cases': rows}
    Path(__file__).with_name('middle_safe_audit.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
