"""Current reconstruction, not the missing original discovery CLI.

Keeps literal decimal data distinct from the existing 36-unit instance/10.
Uses only the standard library, the saved inputs and complete action tables.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def read(name, exact=False):
    text = (HERE / name).read_text()
    return json.loads(text, parse_float=F) if exact else json.loads(text)


def run():
    source = 'original/pushforward_fractional_candidate_individual_security_failure_0.json'
    raw = read(source)
    literal = read(source, exact=True)
    assert hashlib.sha256((HERE / source).read_bytes()).hexdigest() == '05bc79520b37efa566dc34d332de481cc194d038e8f2ac2d1cf41cb761d40e0e'
    assert set(raw) == {'p', 'weights', 'extra', 'name', 'masklist', 'gap'}
    assert raw['masklist'] == list(range(1, 64))
    assert len(raw['p']) == 6 and len(raw['weights']) == 63
    assert raw['extra'] == 0 and raw['name'] == 'individual_security_failure'
    inp = read('related/aggregate_theta_failure-input.json')
    other = read('related/individual_security_failure-input.json')
    cert = read('related/aggregate_theta_failure-certificate.json')
    other_cert = read('related/individual_security_failure-certificate.json')
    assert inp['players'] == other['players'] == 3
    assert cert['strategy']['actions'] == other_cert['strategy']['actions']
    acts = {tuple(x['history']): x['action'] for x in cert['strategy']['actions']}
    histories = [h for d in range(3) for h in product(range(6), repeat=d)]
    assert set(acts) == set(histories)
    for h, a in acts.items():
        expected = 0 if not h else (3 if h[0] < 3 else 0) if len(h) == 1 else min(t for t in (range(3) if h[1] < 3 else range(3, 6)) if t not in h)
        assert a == expected

    def compressed(data):
        return {sum(1 << t for t in x['topics']): x['multiplicity'] for x in data['customers']}

    units = compressed(inp)
    assert sum(units.values()) == 36
    assert sum(compressed(other).values()) == 34 and units != compressed(other)
    weights = [F(units.get(m, 0), 10) for m in raw['masklist']]
    assert all(w == z.limit_denominator(10) for w, z in zip(weights, literal['weights']))
    max_error = max(abs(w - z) for w, z in zip(weights, literal['weights']))
    assert max_error == F(21, 25000000000000000)

    def terminal(h):
        while len(h) < 3:
            h += (acts[h],)
        return h

    def pay(a, h, ww):
        return sum((w / sum(bool(m & (1 << t)) for t in h) for m, w in zip(raw['masklist'], ww) if m & (1 << a)), F(0))

    exact_rows = []
    literal_rows = []
    for h in histories:
        leaf = terminal(h)
        for a in range(6):
            dev = terminal(h + (a,))
            gap = pay(acts[h], leaf, weights) - pay(a, dev, weights)
            lgap = pay(acts[h], leaf, literal['weights']) - pay(a, dev, literal['weights'])
            exact_rows.append({'history': list(h), 'chosen': acts[h], 'alternative': a, 'chosen_leaf': list(leaf), 'alternative_leaf': list(dev), 'gap': str(gap)})
            literal_rows.append((lgap, h, a))
    assert len(exact_rows) == 258 and all(F(x['gap']) >= 0 for x in exact_rows)
    assert sum(F(x['gap']) > 0 for x in exact_rows) == 126
    assert min(x[0] for x in literal_rows) == F(-161, 10**17)
    assert sum(x[0] < 0 for x in literal_rows) == 61
    path = terminal(())
    assert path == (0, 3, 4)
    assert [pay(a, path, weights) for a in path] == [F(1), F(6, 5), F(6, 5)]
    for h in product(range(6), repeat=3):
        total = sum(pay(a, h, weights) for a in h)
        coverage = sum(w for m, w in zip(raw['masklist'], weights) if any(m & (1 << a) for a in h))
        assert total == coverage
    tails = [terminal((a,))[1:] for a in range(6)]
    assert tails == [(3, 4)] * 3 + [(0, 1)] * 3

    def load(p, full=False):
        return [sum(p[a] * (terminal((a,)) if full else tails[a]).count(t) for a in range(6)) for t in range(6)]

    def queries(L, ww):
        return [sum((w / (1 + sum(L[t] for t in range(6) if m & (1 << t))) for m, w in zip(raw['masklist'], ww) if m & (1 << a)), F(0)) for a in range(6)]

    float_L = load(raw['p'])
    float_g = queries(float_L, raw['weights'])
    float_root = float(pay(0, path, raw['weights']))
    floating_gap = sum(p * g for p, g in zip(raw['p'], float_g)) - float_root
    assert abs(floating_gap - raw['gap']) < 1e-14
    p_sum = sum(literal['p'])
    assert p_sum == F(199999999999999967, 200000000000000000)
    p = [x / p_sum for x in literal['p']]
    L = load(p)
    assert sum(L) == 2
    g = queries(L, weights)
    gap = sum(x * y for x, y in zip(p, g)) - 1
    assert gap > 0
    full_g = queries(load(p, full=True), weights)
    full_gap = sum(x * y for x, y in zip(p, full_g)) - 1
    assert full_gap < 0
    midpoint = queries([F(1, 2), F(1, 2), F(0), F(1, 2), F(1, 2), F(0)], weights)
    free = queries([F(1, 3)] * 6, weights)
    assert midpoint == [F(139, 150), F(139, 150), F(161, 150), F(139, 150), F(139, 150), F(161, 150)]
    assert free == [F(333, 350)] * 6
    # Exact integer-static safety matching pair: uniform query and six
    # same-group distinct two-slot backgrounds, each with probability 1/6.
    all_integer = [queries([F(h.count(t)) for t in range(6)], weights) for h in product(range(6), repeat=2)]
    assert min(sum(row) / 6 for row in all_integer) == 1
    dual = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)]
    dual_g = [queries([F(h.count(t)) for t in range(6)], weights) for h in dual]
    assert all(sum(row[a] for row in dual_g) / 6 == 1 for a in range(6))
    result = {
        'status': 'PASS-current-reconstruction-not-original-CLI',
        'primary_sha256': hashlib.sha256((HERE / source).read_bytes()).hexdigest(),
        'primary_bytes': (HERE / source).stat().st_size,
        'fields_checked': sorted(raw),
        'source_name_is_not_final_customer_input': True,
        'named_input_unit_customers': 34,
        'reconstructed_unit_customers': 36,
        'normalization': 'exact unit customer weights divided by 10; root equals 1',
        'max_literal_weight_reconstruction_error': str(max_error),
        'literal_p_sum': str(p_sum),
        'literal_weights_sum': str(sum(literal['weights'])),
        'literal_root_payoff': str(pay(0, path, literal['weights'])),
        'literal_negative_ic_count': sum(x[0] < 0 for x in literal_rows),
        'literal_minimum_ic': str(min(x[0] for x in literal_rows)),
        'literal_minimum_ic_witness': {'history': [3, 3], 'alternative': 5},
        'rationalized_complete_histories': len(histories),
        'rationalized_ic_comparisons_including_self': len(exact_rows),
        'rationalized_positive_ic': 126,
        'rationalized_zero_ic': 132,
        'ordered_terminals_checked': 216,
        'actual_path': list(path),
        'unit_customer_payoffs': ['10', '12', '12'],
        'unit_customer_welfare': 34,
        'unit_customer_optimum': 36,
        'root_action_to_tail': [list(t) for t in tails],
        'saved_gap': raw['gap'],
        'floating_reconstructed_gap': floating_gap,
        'floating_gap_absolute_error': abs(floating_gap - raw['gap']),
        'normalized_p': list(map(str, p)),
        'normalized_p_tail_load': list(map(str, L)),
        'normalized_p_tail_queries': list(map(str, g)),
        'normalized_p_tail_gap_exact': str(gap),
        'normalized_p_tail_gap_decimal': float(gap),
        'normalized_p_full_terminal_gap_exact': str(full_gap),
        'normalized_p_full_terminal_gap_decimal': float(full_gap),
        'midpoint_queries_normalized': list(map(str, midpoint)),
        'free_uniform_queries_normalized': list(map(str, free)),
        'integer_static_security_normalized': '1',
        'scope': 'Only this saved query and reconstructed 36-unit policy are checked; continuous restricted/free optima rely on the existing convex-symmetry lemma; no original generator, optimizer run, new general counterexample or half claim.'
    }
    output = HERE / 'replay'
    output.mkdir(exist_ok=True)
    (output / 'reconstruction.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    (output / 'rationalized-ic-table.json').write_text(json.dumps(exact_rows, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'literal_negative_ic_count', 'rationalized_ic_comparisons_including_self', 'saved_gap', 'floating_reconstructed_gap', 'normalized_p_tail_gap_decimal', 'normalized_p_full_terminal_gap_decimal']}, indent=2))


if __name__ == '__main__':
    run()
