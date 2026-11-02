"""Bind alpha=1 target to the same old13 packet, without another SPE audit."""
from argparse import ArgumentParser
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json

ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
a = ap.parse_args()
base = a.repo / 'archives/customer-attraction/tools/evidence/fractional-load-boundaries'
packet = base / 'original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
raw = packet.read_bytes()
packet_sha = hashlib.sha256(raw).hexdigest()
assert len(raw) == 372216
assert packet_sha == 'bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce'
doc = json.loads(gzip.decompress(raw))
inst = doc['instance']
assert inst['players'] == 13 and inst['topics'] == ['A', 'B', 'T', 'D', 'E', 'P']
expected_types = {(0,): 2, (1,): 2, (2,): 1, (2, 3): 1, (2, 4): 1,
                  (0, 3, 4): 3, (1, 3, 4): 1, (5,): 25}
types = {tuple(c['topics']): c['multiplicity'] for c in inst['customers']}
assert len(inst['customers']) == 8 and types == expected_types
nodes = doc['nodes']
node = doc['root']
actual = []
visited = []
while not nodes[node].get('terminal'):
    assert node not in visited
    visited.append(node)
    action = nodes[node]['action']
    actual.append(action)
    node = nodes[node]['children'][action]
visited.append(node)
assert actual == [5] * 10 + [0, 0, 1]
counts = tuple(actual.count(i) for i in range(6))
assert counts == tuple(nodes[node]['counts']) == (2, 1, 0, 0, 0, 10)
loads = {s: sum(counts[i] for i in s) for s in types}
W = sum(n for s, n in types.items() if loads[s])
G = sum((F(n, 1 + loads[s]) for s, n in types.items() if loads[s]), F())
g = [sum((F(n, 1 + loads[s]) for s, n in types.items() if i in s), F())
     for i in range(6)]
M = max(g)
gap = 13 * M - W - G
assert (W, G, M, gap) == (33, F(359, 66), F(3), F(37, 66))
assert g == [F(5, 3), F(3, 2), F(3), F(5, 2), F(5, 2), F(25, 11)]
mass = sum(types.values())
assert mass == 36
normalized = sum((F(n, mass) * (13 * F(int(2 in s), 1 + loads[s])
                              - int(loads[s] > 0)
                              - (F(1, 1 + loads[s]) if loads[s] else 0))
                  for s, n in types.items()), F())
assert normalized == gap / mass == F(37, 2376)
complete_path = base / 'replay-refined-tax.json'
alpha_path = base / 'replay-alpha-one.json'
complete = json.loads(complete_path.read_text())
alpha = json.loads(alpha_path.read_text())
assert complete['status'] == 'PASS'
assert (complete['automaton_nodes'], complete['decision_comparisons']) == (27243, 112050)
assert complete['actual_path'] == actual and complete['W'] == W
assert alpha['source_sha256'] == packet_sha
assert alpha['counts'] == list(counts) and alpha['actual'] == actual
assert F(alpha['J_base']) == G and list(map(F, alpha['g'])) == g
assert F(alpha['m_max_g_minus_W_minus_J']) == gap
report = {
    'scope': 'one fixed packet/source/actual-leaf/alpha-one-goal binding; no whole-automaton SPE audit',
    'packet_repository_path': str(packet.relative_to(a.repo)),
    'packet_sha256': packet_sha,
    'packet_bytes': len(raw),
    'all_eight_instance_customer_records_checked': True,
    'actual_leaf_nodes_followed': len(visited),
    'actual_path': actual,
    'counts': counts,
    'players': 13,
    'unit_customers': mass,
    'W': W,
    'G1': str(G),
    'entrant_values': list(map(str, g)),
    'M1': str(M),
    'unscaled_gap': str(gap),
    'sum_customer_mass_one_cone_goal': str(normalized),
    'existing_complete_audit_reused_comparisons': complete['decision_comparisons'],
    'existing_complete_report_sha256': hashlib.sha256(complete_path.read_bytes()).hexdigest(),
    'existing_alpha_report_sha256': hashlib.sha256(alpha_path.read_bytes()).hexdigest(),
    'all_packet_nodes_or_SPE_comparisons_reread_or_rechecked': False,
    'new_LP_MIP_BI_random_or_original_audit_calls': 0,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
