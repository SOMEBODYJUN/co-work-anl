"""Main's independent full-menu and full-strategy check of one fixed game.

No solver or producer imports. The terminal sets are recomputed bottom-up from
the unit-customer input. Count-state caching identifies continuation *sets*,
not the actions prescribed at distinct ordered histories.
"""
from collections import deque
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import math
import time

B = Path(__file__).resolve().parent
D = B / 'master_cuts'
stem = 'full_history_probe_12label_v1'
start = time.time()


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def read(suffix):
    p = D / (stem + suffix)
    raw = gzip.decompress(p.read_bytes()) if suffix.endswith('.gz') else p.read_bytes()
    return p, json.loads(raw)


ip, inp = read('.json')
mp, saved = read('_menus.json.gz')
wp, witness = read('_witnesses.json.gz')
rp, result = read('_result.json')
assert digest(ip) == '59e86b2961662aba4c9a9c9128fa03f2ee68b0b7c5bd7577896bc897838508f7'
assert all(d['input_sha256'] == digest(ip) for d in (saved, witness, result))
assert result['menus_sha256'] == digest(mp) and result['witnesses_sha256'] == digest(wp)
k = inp['players']
labels = inp['labels']
m = len(labels)
assert (k, m) == (6, 12)
N = int(inp['unit_customers'])
customers = [(tuple(a for a in range(m) if int(v['mask']) >> a & 1), int(v['integer_clones']))
             for v in inp['nonzero_customer_types']]
assert all(n > 0 for _, n in customers) and sum(n for _, n in customers) == N
assert all(sum(a >= 6 for a in members) == 1 for members, _ in customers)


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for rest in compositions(total - head, length - 1):
            yield (head,) + rest


@lru_cache(maxsize=None)
def children(c):
    return tuple(c[:a] + (c[a] + 1,) + c[a+1:] for a in range(m))


levels = [tuple(compositions(t, m)) for t in range(k + 1)]
terminals = tuple(tuple(f) for f in saved['leaf_terminal_counts'])
assert len(terminals) == len(set(terminals)) == math.comb(m+k-1, k)
assert set(terminals) == set(levels[k])
terminal_id = {f: i for i, f in enumerate(terminals)}

# Exact terminal payoffs are computed directly from the original customers.
# An action's payoff is subsequently used only where that action was chosen.
pay = {}
welfare = {}
for f in levels[k]:
    utility = [0] * m
    covered = 0
    for members, number in customers:
        load = sum(f[a] for a in members)
        if load:
            assert 60 % load == 0
            covered += number
            share = number * (60 // load)
            for a in members:
                utility[a] += share
    pay[f] = tuple(utility)
    welfare[f] = covered
    assert sum(f[a] * utility[a] for a in range(m)) == 60 * covered

stored_states = saved['states']
assert len(stored_states) == sum(map(len, levels)) == math.comb(m+k, k)
by_counts = {tuple(s['past_counts']): s for s in stored_states}
by_id = {s['state_id']: s for s in stored_states}
assert len(by_counts) == len(by_id) == len(stored_states)
assert set(by_counts) == {c for level in levels for c in level}
menus = {f: frozenset([f]) for f in levels[k]}
threshold = {}
child_minima = {}
checked_action_candidates = 0

for depth in range(k, -1, -1):
    for c in levels[depth]:
        record = by_counts[c]
        if depth < k:
            child = children(c)
            low = tuple(min(pay[f][a] for f in menus[child[a]]) for a in range(m))
            tau = max(low)
            out = set()
            for a, d in enumerate(child):
                assert record['child_state_ids'][a] == by_counts[d]['state_id']
                stated_min = terminals[record['child_minimizing_terminal_ids'][a]]
                assert stated_min in menus[d] and pay[stated_min][a] == low[a]
                for f in menus[d]:
                    assert f[a] > 0
                    checked_action_candidates += 1
                    if pay[f][a] >= tau:
                        out.add(f)
            assert out
            menus[c] = frozenset(out)
            threshold[c] = tau
            child_minima[c] = low
            assert int(record['threshold_scaled60']) == tau
            assert tuple(map(int, record['child_minimum_payoffs_scaled60'])) == low
        ids = record['menu_terminal_ids']
        assert len(ids) == len(set(ids))
        assert {terminals[i] for i in ids} == menus[c]
        assert all(all(fa >= ca for fa, ca in zip(f, c)) for f in menus[c])

root = (0,) * m
target = tuple(inp['target_terminal_counts'])
all_t = (0,) * 6 + (1,) * 6
assert menus[root] == frozenset([all_t])
assert target not in menus[root]
assert welfare[all_t] == N == int(result['minimum_root_W']) == int(result['OPT6'])
assert F(result['minimum_root_W_over_OPT6']) == 1
assert result['target_in_root_menu'] is False and result['root_menu_size'] == 1
assert terminal_id[target] == result['target_terminal_id']
assert welfare[target] == int(result['target_W'])
assert F(welfare[target], N) == F(result['target_W_over_OPT6'])
assert result['all_retained_state_terminal_pairs'] == sum(map(len, menus.values()))
assert result['states'] == len(menus) and result['terminals'] == len(terminals)

# Verify the entire target-dependent DAG and every outgoing action. Since every
# child increases depth, its recursive unfolding covers every ordered history.
wr = witness['worst']
nodes = {}
for node in wr['nodes']:
    key = (tuple(by_id[node['state_id']]['past_counts']), terminals[node['target_terminal_id']])
    assert key not in nodes
    nodes[key] = node
assert wr['node_count'] == len(nodes) == result['worst_witness_nodes']
root_key = (tuple(by_id[wr['root_state_id']]['past_counts']), terminals[wr['root_target_terminal_id']])
assert root_key == (root, all_t)
seen = set()
queue = deque([root_key])
ic_count = 0
ic_min = None
while queue:
    key = queue.popleft()
    if key in seen:
        continue
    seen.add(key)
    c, f = key
    assert key in nodes and f in menus[c]
    node = nodes[key]
    if sum(c) == k:
        assert c == f
        continue
    a = node['chosen_action']
    assert 0 <= a < m
    child_targets = [terminals[t] for t in node['child_target_terminal_ids']]
    assert len(child_targets) == m and child_targets[a] == f
    margins = []
    for b, (d, g) in enumerate(zip(children(c), child_targets)):
        assert g in menus[d] and (d, g) in nodes
        margin = pay[f][a] - pay[g][b]
        assert margin >= 0
        margins.append(margin)
        queue.append((d, g))
        ic_count += 1
    assert min(margins) == int(node['minimum_IC_margin_scaled60'])
    ic_min = min(margins) if ic_min is None else min(ic_min, *margins)
assert seen == set(nodes)
assert ic_min == int(wr['minimum_IC_margin_scaled60']) == int(result['minimum_worst_witness_IC_scaled60']) == 0

# Recheck the first obstruction on the explicitly required A1,...,A6 path.
first = None
prefixes = [tuple(int(a < depth) for a in range(m)) for depth in range(6)]
for depth in range(5, -1, -1):
    c = prefixes[depth]
    child = children(c)[depth]
    credible = target in menus[child]
    admissible = credible and pay[target][depth] >= threshold[c]
    if not admissible and first is None:
        first = (depth, c, credible, threshold[c] - pay[target][depth])
    rec = result['specified_order_checks_leaf_to_root'][5-depth]
    assert rec['prefix'] == labels[:depth] and rec['action'] == labels[depth]
    assert rec['target_in_specified_child'] == credible and rec['specified_action_admissible'] == admissible
    assert int(rec['threshold_scaled60']) == threshold[c]
    assert int(rec['target_payoff_scaled60']) == pay[target][depth]
depth, c, credible, gap = first
assert depth == 4 and credible and gap > 0
reject = result['first_target_rejection_leaf_to_root']
deviation = labels.index(reject['deviation_label'])
assert deviation == 6
d = children(c)[deviation]
assert len(menus[d]) == 5
assert menus[d] == frozenset(d[:a] + (d[a]+1,) + d[a+1:] for a in range(7,12))
assert min(pay[f][deviation] for f in menus[d]) == threshold[c]
assert gap == int(reject['strict_gap_scaled60'])
assert F(gap,60) == F(reject['strict_gap_unit_customer'])
assert F(gap,60*N) == F(reject['strict_gap_normalized'])
assert reject['deviation_child_menu_size'] == 5
assert by_counts[d]['state_id'] == reject['deviation_child_state_id']
assert welfare[all_t] * 2 >= N

output = {
    'status': 'PASS',
    'scope': 'This fixed 12-label finite unit-customer game only; all full-history SPE terminal sets independently recomputed, and one complete strategy DAG independently checked. No exclusion of added labels or general LP realizability.',
    'input_sha256': digest(ip), 'menus_sha256': digest(mp),
    'witnesses_sha256': digest(wp), 'result_sha256': digest(rp),
    'verifier_sha256': digest(Path(__file__)),
    'state_count': len(menus), 'terminal_count': len(terminals),
    'all_retained_state_terminal_pairs': sum(map(len,menus.values())),
    'action_candidate_comparisons': checked_action_candidates,
    'witness_nodes': len(nodes), 'all_witness_action_IC_checks': ic_count,
    'minimum_witness_IC_scaled60': str(ic_min),
    'root_menu': [list(f) for f in sorted(menus[root])],
    'OPT6': str(N), 'root_minimum_W_over_OPT6': '1',
    'target_rejected': True, 'first_rejected_prefix': labels[:depth],
    'rejected_action': labels[depth], 'deviation_label': labels[deviation],
    'complete_deviation_child_menu': [list(f) for f in sorted(menus[d])],
    'strict_normalized_payoff_gap': str(F(gap,60*N)),
    'seconds': time.time()-start,
}
out = B / 'main_verify_full_history_probe_v1.json'
assert not out.exists(), 'Do not overwrite a frozen audit'
out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(output,ensure_ascii=False,indent=2))
