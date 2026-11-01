"""One saved-input definition check, never import/replay the producer or solver."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib
import json
import sys

source, output = map(Path, sys.argv[1:])
if output.exists():
    raise SystemExit('refuse to overwrite an existing check result')
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '35a0e98bea6da2cb5c3cbc14d84e1cf9613e26bb5ba472723f7c475d5d44d4ae'
packet = json.loads(raw)
inst, cert = packet['instance'], packet['certificate']
p, m = len(inst['topics']), inst['players']
assert (p, m) == (6, 4)
types = [(frozenset(x['topics']), x['multiplicity']) for x in inst['customers']]
assert all(type(w) is int and w > 0 and all(type(a) is int and 0 <= a < p for a in likes) for likes, w in types)
rows = cert['actions']
policy = {tuple(x['history']): x['action'] for x in rows}
expected = [h for d in range(m) for h in product(range(p), repeat=d)]
assert len(rows) == len(policy) == len(expected) == 259
assert set(policy) == set(expected)
assert all(type(a) is int and 0 <= a < p for a in policy.values())

def finish(prefix):
    while len(prefix) < m:
        prefix += (policy[prefix],)
    return prefix

def income(action, final):
    return sum((Fraction(w, sum(a in likes for a in final)) for likes, w in types if action in likes), Fraction())

checks = []
nodes = []
for h in expected:
    a = policy[h]
    chosen = finish(h)
    value = income(a, chosen)
    nodes.append({'history': list(h), 'action': a, 'terminal': list(chosen), 'payoff': str(value)})
    for b in range(p):
        if b == a:
            continue
        alternative = finish(h + (b,))
        other = income(b, alternative)
        slack = value - other
        assert slack >= 0, (h, a, b, value, other)
        checks.append({'history': list(h), 'action': a, 'deviation': b,
                       'chosen_terminal': list(chosen), 'deviating_terminal': list(alternative),
                       'chosen_payoff': str(value), 'deviating_payoff': str(other), 'slack': str(slack)})
assert len(checks) == 1295
actual = finish(())
counts = [actual.count(a) for a in range(p)]
assert list(actual) == packet['actual'] and counts == packet['counts'] == cert['terminal_counts']
assert policy[()] == packet['root_action'] == actual[0]
loads = [sum(a in likes for a in actual) for likes, _ in types]
queries = [sum((Fraction(w, load + 1) for (likes, w), load in zip(types, loads) if a in likes), Fraction()) for a in range(p)]
credit = sum((Fraction(w, 2) for (likes, w), load in zip(types, loads) if actual[0] in likes and load == 1), Fraction())
payoffs = [income(a, actual) for a in actual]
assert payoffs[0] == Fraction(packet['root_payoff'])
assert credit == Fraction(packet['exclusive_credit'])
assert queries == list(map(Fraction, packet['entrant_values']))
gap = payoffs[0] + credit - max(queries)
assert gap == Fraction(packet['gap']) < 0
total = sum(w for _, w in types)
welfare = sum(w for (_, w), load in zip(types, loads) if load > 0)
assert welfare == total == 37 and sum(payoffs) == welfare
G = sum((Fraction(w, load + 1) for (_, w), load in zip(types, loads) if load > 0), Fraction())
global_gap = welfare + G - m * max(queries)
classes = []
signatures = []
for a in range(p):
    signature = tuple(i for i, (likes, w) in enumerate(types) if w > 0 and a in likes)
    if signature in signatures:
        classes[signatures.index(signature)].append(a)
    else:
        signatures.append(signature)
        classes.append([a])
projection = [next(i for i, members in enumerate(classes) if a in members) for a in range(p)]
assert classes == [[0], [1, 3], [2], [4], [5]]
result = {
    'scope': 'one independent fixed saved259-node/1295-deviation definition check and saved metadata; no source probe/core import, RNG replay, outcome solver, LP or quotient-policy audit',
    'source_sha256': hashlib.sha256(raw).hexdigest(), 'all_original_packet_fields': list(packet),
    'p': p, 'm': m, 'unit_customers': total, 'all259_nodes': nodes,
    'all1295_proper_deviation_results': checks, 'all_proper_slacks_nonnegative': True,
    'minimum_proper_slack': str(min(Fraction(x['slack']) for x in checks)),
    'actual': list(actual), 'counts': counts, 'payoffs': list(map(str, payoffs)),
    'type_loads_in_original_order': loads, 'entrant_values': list(map(str, queries)),
    'exclusive_credit': str(credit), 'local_gap': str(gap), 'W': welfare,
    'OPT': total, 'OPT_proof': 'actual already covers all37 unit customers; no optimum enumeration',
    'G1': str(G), 'global_gap': str(global_gap),
    'cover_classes_original_label_indices': classes, 'projection': projection,
    'projected_actual': [projection[a] for a in actual],
    'quotient_complete_policy_not_computed_or_audited': True,
    'quotient_SPE_and_root_observables_transfer_by_recursive_history_lift_proof': True,
}
output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
print(json.dumps({k: result[k] for k in ['p','m','unit_customers','all_proper_slacks_nonnegative','minimum_proper_slack','actual','payoffs','local_gap','W','OPT','G1','global_gap','cover_classes_original_label_indices','projection']}, ensure_ascii=False))
