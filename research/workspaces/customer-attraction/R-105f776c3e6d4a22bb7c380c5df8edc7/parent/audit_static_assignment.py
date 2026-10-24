"""Independent integer-unit replay of the frozen static-assignment witness.

Uses raw input/policy only; does not import the discovery, author audit,
canonical game model, solver, or certificate validator. Payoffs are integers
in units of 1/6, and every compressed customer is expanded before evaluation.
"""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'dynamic_exchange'
game_path = SOURCE / 'assignment_instance.json'
policy_path = SOURCE / 'assignment_full_policy.json'
game = json.loads(game_path.read_text())
raw_policy = json.loads(policy_path.read_text())
labels = tuple(range(len(game['topics'])))
m = game['players']
assert m == 3 and len(labels) == 6
clients = []
for kind in game['customers']:
    mult = kind['multiplicity']
    assert type(mult) is int and mult > 0
    interests = frozenset(kind['topics'])
    assert interests and interests <= set(labels)
    clients.extend([interests] * mult)
topic_sets = [frozenset(j for j, interests in enumerate(clients) if a in interests)
              for a in labels]
assert len(set(topic_sets)) == len(labels)
policy = {tuple(map(int, key.split(','))) if key else (): value
          for key, value in raw_policy['policy'].items()}
histories = tuple(h for depth in range(m) for h in product(labels, repeat=depth))
assert set(policy) == set(histories)
assert all(a in labels for a in policy.values())

scores = {}
welfares = {}
for z in product(labels, repeat=m):
    score6 = [0] * m
    covered = 0
    for interests in clients:
        users = [i for i, a in enumerate(z) if a in interests]
        if users:
            covered += 1
            for i in users:
                score6[i] += 6 // len(users)
    scores[z] = score6
    welfares[z] = covered
    assert sum(score6) == 6 * covered

def rollout(h):
    while len(h) < m:
        h += (policy[h],)
    return h

slacks6 = []
for h in histories:
    current = len(h)
    prescribed = rollout(h)
    for a in labels:
        forced = rollout(h + (a,))
        slack = scores[prescribed][current] - scores[forced][current]
        assert slack >= 0, (h, a, slack)
        slacks6.append(slack)
actual = rollout(())
assert list(actual) == raw_policy['actual']
W = welfares[actual]
opt = max(welfares.values())
optimal = [z for z, welfare in welfares.items() if welfare == opt]
supports = sorted({tuple(sorted(set(z))) for z in optimal})
assignment_costs6 = {}
for z in optimal:
    cost = 0
    for i, t in enumerate(z):
        replaced = actual[:i] + (t,) + actual[i+1:]
        cost += scores[replaced][i]
    assignment_costs6[','.join(map(str, z))] = cost
minimum6 = min(assignment_costs6.values())
assert minimum6 > 6 * W
result = {
    'status': 'PASS; auxiliary static optimal-assignment bridge only',
    'source_sha256': {p.name: sha256(p.read_bytes()).hexdigest()
                      for p in (game_path, policy_path)},
    'unit_customer_count': len(clients),
    'players': m,
    'topics_distinct': len(set(topic_sets)),
    'complete_ordered_histories': len(histories),
    'true_action_comparisons_including_self': len(slacks6),
    'min_SPE_slack6': min(slacks6),
    'terminal_profiles': len(scores),
    'actual': actual,
    'actual_payoffs6': scores[actual],
    'W': W,
    'OPT': opt,
    'optimal_ordered_tuples': len(optimal),
    'optimal_supports': supports,
    'all_optimal_assignment_costs6': assignment_costs6,
    'minimum_assignment_cost6': minimum6,
    'minimum_minus_W6': minimum6 - 6*W,
    'half_margin': 2*W-opt,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == '__main__':
    import sys
    if '--freeze' in sys.argv:
        (HERE / 'static_assignment_unit_audit.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + '\n')
