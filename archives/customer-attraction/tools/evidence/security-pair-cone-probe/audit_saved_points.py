"""One independent standard-library check of all three saved automata.

No original import, solver, RNG, LP, or new policy search. Decimal literals,
decoded binary floats, and expressly new integer calibration inputs stay separate.
"""
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import time

BASE = Path(__file__).resolve().parent
INPUT = BASE.parent

def digest(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def counts(seq, q):
    return tuple(seq.count(a) for a in range(q))

def rivals(q, slots):
    # Independent direct product, with set deduplication; no imported compositions.
    return sorted({counts(list(h), q) for h in product(range(q), repeat=slots)})

def evaluate(tag):
    src = INPUT / ('round20-pair_cone_best_' + tag + '.json')
    text = src.read_text()
    parsed = json.loads(text)
    dec = json.loads(text, parse_float=F)
    q, r = parsed['q'], parsed['r']
    prefix = tuple(parsed['prefix'])
    witness = parsed['witness']
    table = {}
    per_count = Counter()
    for rec in parsed['automaton']:
        assert set(rec) == {'counts', 'target', 'action', 'children'}
        c, t, a = tuple(rec['counts']), tuple(rec['target']), rec['action']
        children = tuple(tuple(x) for x in rec['children'])
        assert len(c) == len(t) == len(children) == q
        assert all(isinstance(z, int) and z >= 0 for z in c + t)
        assert 0 <= a < q and sum(c) < r and sum(t) == r
        assert all(cj <= tj for cj, tj in zip(c, t))
        assert (c, t) not in table
        assert children[a] == t
        for b, z in enumerate(children):
            cc = tuple(v + int(j == b) for j, v in enumerate(c))
            assert len(z) == q and sum(z) == r and all(cj <= zj for cj, zj in zip(cc, z))
            if sum(cc) == r:
                assert z == cc
        table[c, t] = (a, children)
        per_count[c] += 1
    assert len(table) == parsed['nodes']
    assert len(per_count) == comb(q + r - 1, r - 1) and max(per_count.values()) == 1
    root = ((0,) * q, tuple(witness[2]))
    assert root in table
    seen = set()
    actions = {}
    terminals = {}
    history_records = []

    def expand(h, state):
        c, t = state
        assert c == counts(list(h), q)
        if len(h) == r:
            assert c == t
            terminals[h] = c
            return c
        seen.add(state)
        a, children = table[state]
        actions[h] = a
        leaves = []
        for b, z in enumerate(children):
            cc = tuple(v + int(j == b) for j, v in enumerate(c))
            leaves.append(expand(h + (b,), (cc, z)))
            assert leaves[-1] == z
        assert leaves[a] == t
        history_records.append((h, a, t, leaves))
        return t

    expand((), root)
    assert seen == set(table)
    expected_nodes = sum(q ** d for d in range(r))
    assert len(actions) == expected_nodes and len(terminals) == q ** r
    path = []
    while len(path) < r:
        path.append(actions[tuple(path)])
    assert path[:2] == witness[:2] and counts(path, q) == tuple(witness[2])
    literal = list(dec['weights'])
    binary = [F.from_float(v) for v in parsed['weights']]
    calibration = [F(round(v)) for v in parsed['weights']]
    assert all(v >= 0 for ws in (literal, binary, calibration) for v in ws)
    assert len(literal) == 2 ** q - 1
    assert all(abs(F(float(v)) - z) < F(1, 10 ** 12) for v, z in zip(parsed['weights'], calibration))
    models = {'literal_decimal': literal, 'decoded_binary_float': binary, 'new_integer_calibration': calibration}
    supports = {label: [(i + 1, v) for i, v in enumerate(ws) if v] for label, ws in models.items()}

    def payoff(a, t, support):
        total = F(0)
        for mask, mass in support:
            if mask >> a & 1:
                load = sum(prefix[j] + t[j] for j in range(q) if mask >> j & 1)
                assert load > 0
                total += mass / load
        return total

    values = {}
    statics = {}
    details = {}
    bgs = rivals(q, r - 1)
    assert len(bgs) == comb(q + r - 2, r - 1)
    for label, support in supports.items():
        utility_cache = {}
        def utility(a, t):
            key = (a, t)
            if key not in utility_cache:
                utility_cache[key] = payoff(a, t, support)
            return utility_cache[key]
        comparisons = []
        for h, a, t, leaves in history_records:
            for b, z in enumerate(leaves):
                gap = utility(a, t) - utility(b, z)
                comparisons.append({'history': list(h), 'chosen': a, 'deviation': b, 'gap': str(gap)})
        gaps = [F(x['gap']) for x in comparisons]
        bad = [x for x in comparisons if F(x['gap']) < 0]
        actual = [utility(a, tuple(witness[2])) for a in path]
        query = list(dec['query']) if label != 'decoded_binary_float' else [F.from_float(v) for v in parsed['query']]
        assert len(query) == q and all(v >= 0 for v in query) and sum(query) == 1
        static_matrix = []
        for bg in bgs:
            row = [sum((mass / (1 + sum(prefix[j] + bg[j] for j in range(q) if mask >> j & 1)) for mask, mass in support if mask >> a & 1), F(0)) for a in range(q)]
            static_matrix.append(row)
        guarantees = [sum(p * v for p, v in zip(query, row)) for row in static_matrix]
        lower = min(guarantees)
        cap, bi = min((max(row), i) for i, row in enumerate(static_matrix))
        assert lower <= cap
        if label == 'new_integer_calibration':
            assert not bad and actual[0] + actual[1] == 2 and lower == cap == 1
        values[label] = {'weights_support': [{'mask': mask, 'mass': str(v)} for mask, v in support], 'IC_comparisons': len(gaps), 'IC_negative': len(bad), 'IC_zero': sum(v == 0 for v in gaps), 'IC_positive': sum(v > 0 for v in gaps), 'minimum_IC_gap': str(min(gaps)), 'first_negative_IC': bad[0] if bad else None, 'actual_payoffs': list(map(str, actual)), 'first_pair_payment': str(actual[0] + actual[1]), 'all_remaining_profit': str(sum(actual)), 'exact_SPE_at_this_point': not bad}
        statics[label] = {'query': list(map(str, query)), 'query_guarantee': str(lower), 'worst_background_for_saved_query': list(bgs[guarantees.index(lower)]), 'pure_background_upper_bound': str(cap), 'upper_background': list(bgs[bi]), 'all_query_payoffs_at_upper_background': list(map(str, static_matrix[bi])), 'matching_bounds': lower == cap, 'exact_security_if_matched': str(lower) if lower == cap else None, 'reported_ratio_minus_query_guarantee': str(F(str(parsed['ratio'])) - lower), 'no_LP': True}
        details[label] = {'all_ordered_history_IC': comparisons, 'all_static_backgrounds_and_query_payoffs': [{'background': list(bg), 'payoffs': list(map(str, row))} for bg, row in zip(bgs, static_matrix)]}
    exact_rows, float_rows = set(), set()
    for (c, t), (a, children) in table.items():
        for b, z in enumerate(children):
            row, floating = [], []
            for mask in range(1, 1 << q):
                ma, mb = (mask >> a) & 1, (mask >> b) & 1
                lt = max(sum(prefix[j] + t[j] for j in range(q) if mask >> j & 1), 1)
                lz = max(sum(prefix[j] + z[j] for j in range(q) if mask >> j & 1), 1)
                row.append(F(ma, lt) - F(mb, lz))
                floating.append(ma / lt - mb / lz)
            exact_rows.add(tuple(row)); float_rows.add(tuple(floating))
    assert len(float_rows) == parsed['rows']
    return {'file': src.name, 'source': digest(src), 'all_fields': list(parsed), 'parameters': {k: parsed[k] for k in ('q', 'r', 'seed', 'trial', 'start', 'iteration', 'ratio', 'prefix', 'witness', 'rows', 'nodes', 'status')}, 'weight_coordinates': len(literal), 'signed_zero_coordinates': [i + 1 for i, v in enumerate(parsed['weights']) if v == 0 and str(v).startswith('-')], 'automaton_states': len(table), 'automaton_states_by_depth': dict(sorted(Counter(sum(c) for c, t in table).items())), 'every_count_has_one_stored_target': True, 'ordered_decision_histories': expected_nodes, 'ordered_terminal_histories': len(terminals), 'actual_action_path': path, 'compressed_action_comparisons': q * len(table), 'reconstructed_float_unique_rows': len(float_rows), 'reconstructed_exact_unique_rows': len(exact_rows), 'static_backgrounds': len(bgs), 'interpretations': values, 'static_certificates': statics}, {'ordered_actions': [{'history': list(h), 'action': a} for h, a in sorted(actions.items())], 'interpretations': details}

def main():
    out = BASE / 'point-audit.json'
    assert not out.exists()
    start = time.time()
    reports, details = [], {}
    for tag in ('6_3', '6_4', '7_5'):
        report, detail = evaluate(tag)
        reports.append(report); details[tag] = detail
    raw = (json.dumps(details, ensure_ascii=False, separators=(',', ':')) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    (BASE / 'point-details.json.gz').write_bytes(packed)
    result = {'identity': 'one independent standard-library complete reading/controller/IC/static-bound audit, no source import or original entry', 'script': digest(Path(__file__)), 'reports': reports, 'details': {'uncompressed_bytes': len(raw), 'uncompressed_sha256': hashlib.sha256(raw).hexdigest(), 'gzip': digest(BASE / 'point-details.json.gz')}, 'original_main_calls': 0, 'original_function_calls': 0, 'LP_calls': 0, 'random_games': 0, 'calibration_is_new_input_not_replacement': True, 'seconds': time.time() - start}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{'file': r['file'], 'histories': r['ordered_decision_histories'], 'comparisons': r['interpretations']['literal_decimal']['IC_comparisons'], 'literal_min': r['interpretations']['literal_decimal']['minimum_IC_gap'], 'binary_min': r['interpretations']['decoded_binary_float']['minimum_IC_gap'], 'calibration_SPE': r['interpretations']['new_integer_calibration']['exact_SPE_at_this_point'], 'calibration_security': r['static_certificates']['new_integer_calibration']['exact_security_if_matched']} for r in reports]))

if __name__ == '__main__':
    main()
