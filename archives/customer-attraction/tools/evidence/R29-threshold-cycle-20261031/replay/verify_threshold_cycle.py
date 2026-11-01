from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'source'
frozen_path = source / 'opt_threshold_cycle_audit.json'
result = json.loads(frozen_path.read_text())
assert result['claim'] == 'abstract root-tail threshold bridge fails; not an SPE counterexample'
assert result['method'] == 'Fraction and direct set unions; no SPE oracle'
assert [case['k'] for case in result['cases']] == [9, 10, 11, 12]

def topics_for(k):
    return [frozenset(((i - 1) % k, i, (i + 1) % k)) for i in range(k)]

def payoff(topics, action, profile):
    return sum((Fraction(1, sum(customer in topics[v] for v in profile)) for customer in topics[action]), Fraction(0))

menu_count = 0
for case in result['cases']:
    k = case['k']; topics = topics_for(k)
    optimum = max(len(set().union(*(topics[a] for a in profile))) for profile in combinations_with_replacement(range(k), 3))
    assert optimum == 9 and case['optimum'] == 9 and case['threshold'] == '3/2'
    assert case['players'] == 3 and len(case['menus']) == k
    for menu in case['menus']:
        root = menu['root']; profile = tuple(menu['profile'])
        assert profile == (root, (root - 1) % k, (root + 1) % k)
        values = tuple(payoff(topics, a, profile) for a in profile)
        assert tuple(map(Fraction, menu['utilities'])) == values == (Fraction(4,3), Fraction(11,6), Fraction(11,6))
        final_values = tuple(payoff(topics, a, profile[:2] + (a,)) for a in range(k))
        far = (root + 3) % k
        assert topics[far].isdisjoint(topics[profile[0]] | topics[profile[1]])
        assert menu['profitable_last_action'] == far
        assert menu['profitable_last_utility'] == '3'
        assert final_values[far] == max(final_values) == 3
        assert menu['all_last_actions_checked'] == k
        menu_count += 1

out = {
    'status': 'PASS',
    'cases': len(result['cases']),
    'menus': menu_count,
    'exact_values': {'optimum': '9', 'threshold': '3/2', 'root': '4/3', 'tails': '11/6', 'far_last': '3', 'gain': '7/6'},
    'full_spe_claim': False,
    'source_sha256': hashlib.sha256((source/'audit_opt_threshold_cycle.py').read_bytes()).hexdigest(),
    'frozen_json_sha256': hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
}
(Path(__file__).with_name('verification.json')).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, sort_keys=True))
