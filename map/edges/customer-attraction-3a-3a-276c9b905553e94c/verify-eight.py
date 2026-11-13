"""Exact traversal of the eight published policies; never replays random trials.

Run from the repository root. Only this task's verification-result.json is written.
The independent direct-IC pass does not call the outcome recursion. A separate
pass recomputes the seven count-set recursions and the deterministic constructors.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = ROOT / 'archives/customer-attraction/tools/evidence/rd28-exact-outcomes-and-static-backgrounds-primary'
SOURCE = PACKAGE / 'original/experiments/cex_last_half_probe.json'
DATA = PACKAGE / 'new-fixed-audit-001/data'
old = json.loads(SOURCE.read_text())
summary = json.loads((DATA / 'summary.json').read_text())
assert (old['players'], old['topics'], old['seed'], old['trials_run']) == (5, 7, 20261022, 1000)
assert len(old['records']) == 8
p, m, scale = 7, 5, 60
histories = [h for d in range(m) for h in product(range(p), repeat=d)]
terminals = [tuple(z.count(a) for a in range(p))
             for z in combinations_with_replacement(range(p), m)]


class Game:
    def __init__(self, weights):
        assert len(weights) == 127 and all(type(w) is int and w >= 0 for w in weights)
        self.weights = tuple(weights)
        self.types = [(t, w) for t, w in enumerate(weights, 1) if w]
        self.U = {}
        self.W = {}
        for q in terminals:
            self.U[q] = tuple(sum(w * (scale // sum(q[b] for b in range(p) if t >> b & 1))
                                 for t, w in self.types
                                 if t >> a & 1 and sum(q[b] for b in range(p) if t >> b & 1))
                              for a in range(p))
            self.W[q] = sum(w for t, w in self.types
                            if sum(q[b] for b in range(p) if t >> b & 1))
        self.states = 0

    @staticmethod
    def child(k, a):
        return k[:a] + (k[a] + 1,) + k[a + 1:]

    @lru_cache(None)
    def outcomes(self, k):
        self.states += 1
        if sum(k) == m:
            return frozenset([k])
        children = [self.outcomes(self.child(k, a)) for a in range(p)]
        threshold = max(min(self.U[q][a] for q in children[a]) for a in range(p))
        kept = frozenset(q for a in range(p) for q in children[a]
                         if self.U[q][a] >= threshold)
        assert kept
        return kept

    def constructor(self, path):
        target = tuple(path.count(a) for a in range(p))
        assert target in self.outcomes((0,) * p)
        policy = {}

        def visit(h, k, q):
            if len(h) == m:
                assert k == q
                return
            children = [self.outcomes(self.child(k, a)) for a in range(p)]
            threshold = max(min(self.U[r][a] for r in children[a]) for a in range(p))
            legal = [a for a in range(p) if q in children[a] and self.U[q][a] >= threshold]
            assert legal
            a = path[len(h)] if h == path[:len(h)] else legal[0]
            assert a in legal
            policy[h] = a
            for b in range(p):
                goal = q if b == a else min(children[b], key=lambda r: (self.U[r][b], r))
                visit(h + (b,), self.child(k, b), goal)

        visit((), (0,) * p, target)
        return policy


games = {}
reports = []
source_refs = [{'path': str(SOURCE.relative_to(ROOT)), 'sha256': sha256(SOURCE.read_bytes()).hexdigest()},
               {'path': str((DATA / 'summary.json').relative_to(ROOT)),
                'sha256': sha256((DATA / 'summary.json').read_bytes()).hexdigest()}]
expected_keys = {'action_layers_depth_lex', 'actual_path', 'terminal_counts', 'scale', 'utilities', 'W',
                 'by_depth', 'payloads_scaled', 'node_payload_ids_depth_lex', 'histories',
                 'comparisons_including_self', 'nonself_comparisons', 'strict', 'ties', 'record_index',
                 'trial', 'weights', 'source_literal_policy', 'policy_origin', 'individual', 'aggregate',
                 'OPT', 'clients'}
for index, row in enumerate(old['records']):
    file = DATA / f'last-record-{index:02d}-new-policy.json'
    saved = json.loads(file.read_text())
    assert set(saved) == expected_keys
    assert saved['record_index'] == index and saved['trial'] == row['trial']
    assert saved['weights'] == row['weights'] and saved['scale'] == row['scale'] == scale
    assert saved['source_literal_policy'] is False
    assert saved['policy_origin'] == 'new deterministic full-history construction for the preserved ordered path; not restoration of an unsaved author policy'
    weights = tuple(saved['weights'])
    if weights not in games:
        games[weights] = Game(weights)
    game = games[weights]
    layers = saved['action_layers_depth_lex']
    assert len(layers) == m
    policy = {}
    for d, layer in enumerate(layers):
        assert len(layer) == p ** d and all(c in '0123456' for c in layer)
        policy.update({h: int(a) for h, a in zip(product(range(p), repeat=d), layer)})
    assert set(policy) == set(histories)

    # This literal-strategy evaluation is logically independent of outcomes().
    @lru_cache(None)
    def end(h):
        return h if len(h) == m else end(h + (policy[h],))

    payloads, ids, node_ids, depth_reports = [], {}, [], []
    for d in range(m):
        counter = Counter()
        smallest = None
        for h in product(range(p), repeat=d):
            vals = tuple(game.U[tuple(end(h + (a,)).count(b) for b in range(p))][a]
                         for a in range(p))
            prescribed = policy[h]
            assert vals[prescribed] == max(vals)
            if vals not in ids:
                ids[vals] = len(payloads)
                payloads.append(list(vals))
            node_ids.append(ids[vals])
            for a in range(p):
                if a == prescribed:
                    counter['self'] += 1
                    continue
                gap = vals[prescribed] - vals[a]
                assert gap >= 0
                counter['strict' if gap else 'ties'] += 1
                smallest = gap if smallest is None else min(smallest, gap)
        depth_reports.append({'depth': d, 'histories': p ** d, **dict(counter),
                              'minimum_nonself_slack_scaled': smallest})
    assert payloads == saved['payloads_scaled']
    assert node_ids == saved['node_payload_ids_depth_lex']
    assert depth_reports == saved['by_depth']
    path = end(())
    q = tuple(path.count(a) for a in range(p))
    vals = [game.U[q][a] for a in path]
    individual = str(Fraction(vals[-1], min(vals[:-1])))
    aggregate = str(Fraction((m - 1) * vals[-1], 2 * sum(vals[:-1])))
    assert list(path) == saved['actual_path'] == row['path']
    assert list(q) == saved['terminal_counts']
    assert vals == row['payoffs_scaled']
    assert saved['utilities'] == [str(Fraction(v, scale)) for v in vals]
    assert individual == saved['individual'] == row['individual']
    assert aggregate == saved['aggregate'] == row['aggregate']
    assert saved['W'] == game.W[q]
    assert saved['OPT'] == max(game.W.values()) == saved['W'] == sum(weights) == saved['clients']
    assert saved['histories'] == len(histories) == 2801
    assert saved['comparisons_including_self'] == len(histories) * p == 19607
    assert saved['nonself_comparisons'] == len(histories) * (p - 1) == 16806
    assert saved['strict'] == sum(x.get('strict', 0) for x in depth_reports)
    assert saved['ties'] == sum(x.get('ties', 0) for x in depth_reports)
    assert saved['strict'] + saved['ties'] == saved['nonself_comparisons']

    # A separate exact construction pass pays all specified-path prefix tests.
    assert policy == game.constructor(path)
    assert game.states == 792
    report = {k: saved[k] for k in summary['last_payoff_records'][index]}
    assert report == summary['last_payoff_records'][index]
    reports.append({**report, 'distinct_payloads': len(payloads),
                    'all_saved_fields_checked': True, 'constructor_matches_every_action': True,
                    'source': {'path': str(file.relative_to(ROOT)),
                               'sha256': sha256(file.read_bytes()).hexdigest()}})
    source_refs.append(reports[-1]['source'])
assert len(games) == summary['distinct_last_record_inputs'] == 7
assert [g.states for g in games.values()] == summary['last_record_DP_states'] == [792] * 7
assert max(Fraction(x['individual']) for x in reports) == Fraction(old['best_individual']) == Fraction(23, 14)
assert max(Fraction(x['aggregate']) for x in reports) == Fraction(old['best_aggregate']) == Fraction(44, 57)
assert reports[6]['source']['sha256'] != reports[7]['source']['sha256']
result = {
    'verification': 'Boss6 direct exact all-node policy traversal plus separate seven-input outcome recursion',
    'scope': 'All scalar and array entries in all eight saved policy JSONs are parsed and checked; original eight records and last-payoff fields in summary are checked. The unrelated global-boundary witness and historical 1000 trials are not rerun.',
    'raw_json_reading': 'Complete machine parsing and exhaustive traversal, not a claim of line-by-line human reading of the raw policy dumps.',
    'records': reports,
    'distinct_inputs': len(games), 'count_states_per_input': [g.states for g in games.values()],
    'total_policy_nodes': sum(x['histories'] for x in reports),
    'total_nonself_comparisons': sum(x['nonself_comparisons'] for x in reports),
    'total_strict': sum(x['strict'] for x in reports), 'total_ties': sum(x['ties'] for x in reports),
    'original_random_search_replays': 0, 'project_solver_or_verifier_calls': 0,
    'sources': source_refs, 'all_checks_passed': True,
}
assert (result['total_policy_nodes'], result['total_nonself_comparisons'],
        result['total_strict'], result['total_ties']) == (22408, 134448, 133989, 459)
(HERE / 'verification-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in {'records', 'sources'}}, ensure_ascii=False, indent=2))
