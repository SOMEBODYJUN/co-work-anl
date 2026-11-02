"""Fixed payload/schema and label binding, not another SPE or LP solver."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'original/research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/global_proof/residual_counterexample.json'
raw = SOURCE.read_bytes()
doc = json.loads(raw)
assert set(doc) == {'instance', 'outcome', 'certificate', 'residual', 'welfare'}
inst = doc['instance']
assert set(inst) == {'topics', 'customers', 'players'}
assert inst['topics'] == list('abtsqr') and inst['players'] == 2
expected = {1: 4, 2: 5, 4: 3, 8: 3, 20: 2, 24: 2, 36: 2, 40: 2, 49: 2, 50: 2}
actual = {}
for row in inst['customers']:
    assert set(row) == {'topics', 'multiplicity'}
    assert type(row['multiplicity']) is int and row['multiplicity'] > 0
    assert len(row['topics']) == len(set(row['topics']))
    assert all(type(a) is int and 0 <= a < 6 for a in row['topics'])
    mask = sum(1 << a for a in row['topics'])
    assert mask not in actual
    actual[mask] = row['multiplicity']
assert actual == expected and sum(actual.values()) == 27
cert = doc['certificate']
assert set(cert) == {'terminal_counts', 'actions'}
assert doc['outcome'] == cert['terminal_counts'] == [1, 1, 0, 0, 0, 0]
actions = {}
for row in cert['actions']:
    assert set(row) == {'history', 'action'}
    history = tuple(row['history'])
    assert history not in actions
    assert type(row['action']) is int and 0 <= row['action'] < 6
    actions[history] = row['action']
assert set(actions) == {()} | {(a,) for a in range(6)}
assert actions[()] == 0
replies = [actions[a,] for a in range(6)]
assert replies == [1, 5, 5, 5, 5, 4]
assert doc['residual'] == 14 and doc['welfare'] == 13

# Old official order A,B,T,Q,R,S: exchange the last two roles in this source.
permutation = [0, 1, 2, 3, 5, 4]
mapped_types = {sum(1 << permutation[a] for a in range(6) if mask >> a & 1): n
                for mask, n in actual.items()}
assert mapped_types == expected
mapped_actions = {tuple(permutation[a] for a in h): permutation[a]
                  for h, a in actions.items()}
official_actions = {(): 0, **{(a,): b for a, b in enumerate([1, 4, 4, 4, 5, 4])}}
assert mapped_actions == official_actions
same_index_changes = [a for a in range(6) if replies[a] != official_actions[a,]]
assert same_index_changes == [1, 2, 3]
out = {
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'scope': 'all fixed JSON records and complete action-label relabeling only; no SPE/BI/LP execution',
    'payload_schema_and_declared_terminal_counts_match': True,
    'customer_types': actual,
    'customers': sum(actual.values()),
    'raw_replies': replies,
    'same_index_official_reply_changes': same_index_changes,
    'source_to_official_index_permutation': permutation,
    'permutation_preserves_every_type_and_complete_strategy': True,
    'original_audit_runs': 0,
    'LP_calls': 0,
    'random_search_runs': 0,
    'canonical_solver_imports_or_calls': 0,
}
print(json.dumps(out, ensure_ascii=False, indent=2))
