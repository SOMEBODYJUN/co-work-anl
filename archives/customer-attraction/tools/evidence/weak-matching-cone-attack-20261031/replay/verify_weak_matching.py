from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'

def digest(path: Path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()

def check_source(name, nbytes, sha):
    got = digest(SRC / name)
    assert got == (nbytes, sha), (name, got)

def check_report(name, expect):
    d = json.loads((SRC / name).read_text())
    assert d['status'] == 'no_floating_separator_in_finite_policy_sample'
    p = d['parameters']
    for k, v in expect['parameters'].items():
        assert p[k] == v, (name, k, p[k], v)
    assert d['policy_cones'] == expect['policy_cones']
    assert len(d['records']) == expect['records']
    success = [r for r in d['records'] if r['success']]
    failed = [r for r in d['records'] if not r['success']]
    assert (len(success), len(failed)) == expect['success_failed']
    b = d['best']
    for k, v in expect['best'].items():
        assert b[k] == v, (name, k, b[k], v)
    assert len(b['weights']) == expect['weight_len']
    assert len(b['certificate']['actions']) == expect['action_count']
    return d

check_source('probe.py', 7852, '4bbd3280c6a2eda7ca461fa2cc713b1183b5c0fecae2c0295c5488dccd997f15')
check_source('p6m4_seed104211.json', 52831, '3897844396918eb9bdc4253fe17579def2a4138da70ec569c23ed7bf5ea1ae5d')
check_source('p7m5_seed104212.json', 475501, '7926d9e3a6dd7c4fd87754767f9f2d45b036fc631c38546d612ace289ed1b8dd')
p6 = check_report('p6m4_seed104211.json', {
    'parameters': {'topics': 6, 'players': 4, 'games': 20, 'seed': 104211, 'active_types': 10, 'unique_margin': 1e-6, 'targets': 3},
    'policy_cones': 19, 'records': 57, 'success_failed': (57, 0),
    'best': {'game': 0, 'mode': 'source_complete_policy', 'target': [0, 1, 4, 5], 'rows': 372, 'actual': [3, 3, 2, 2], 'min_matching_ratio': 1.0469067998756625},
    'weight_len': 63, 'action_count': 259,
})
p7 = check_report('p7m5_seed104212.json', {
    'parameters': {'topics': 7, 'players': 5, 'games': 100, 'seed': 104212, 'active_types': 10, 'unique_margin': 1e-6, 'targets': 3},
    'policy_cones': 98, 'records': 294, 'success_failed': (258, 36),
    'best': {'game': 40, 'mode': 'max_credible_payoff', 'target': [2, 3, 4, 5, 6], 'rows': 1260, 'actual': [0, 0, 0, 0, 0], 'min_matching_ratio': 1.0000000000000002},
    'weight_len': 127, 'action_count': 2801,
})
for name, expected in [
    ('p6_one_game.json', {'best_ratio': 1.0469067998756625, 'policy_cones': 1}),
    ('p7_one_game.json', {'best_ratio': 0.999997210139839, 'policy_cones': 1}),
]:
    d = json.loads((ROOT / 'replay' / name).read_text())
    assert d['status'] == 'no_floating_separator_in_finite_policy_sample'
    assert d['policy_cones'] == expected['policy_cones']
    assert d['best']['min_matching_ratio'] == expected['best_ratio']
print(json.dumps({
    'status': 'PASS',
    'sources': {
      'p6m4': {'policy_cones': p6['policy_cones'], 'records': len(p6['records']), 'best_ratio': p6['best']['min_matching_ratio']},
      'p7m5': {'policy_cones': p7['policy_cones'], 'records': len(p7['records']), 'best_ratio': p7['best']['min_matching_ratio']},
    },
    'one_game_replays': {'p6': 'PASS', 'p7': 'PASS'},
    'scope': 'byte/hash/structure checks and one-game floating replay; no universal SPE or integer-client claim',
}, ensure_ascii=False, indent=2))
