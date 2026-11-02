"""Read frozen snapshots; independently check every real history and static column.

No author module, canonical model, optimization package or solver is imported.
Decimal literals are interpreted by Fraction(str(value)), not silently rounded.
The output is a current internal audit, not a recovered historical run.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name):
    return json.loads((ROOT / 'original' / name).read_text())


def analyze(k, m, types, policy, multipliers):
    histories = [h for d in range(m) for h in product(range(k), repeat=d)]
    require(set(policy) == set(histories), 'complete unique history domain')
    require(all(type(a) is int and 0 <= a < k for a in policy.values()), 'legal actions')
    require(all(t > 0 and t < (1 << k) and r >= 0 for t, r in types.items()), 'legal nonnegative types')
    require(len(multipliers) == k and min(multipliers) >= 0, 'nonnegative CCE multipliers')

    def finish(h):
        while len(h) < m:
            h += (policy[h],)
        return h

    def payoff(z, i):
        return sum((r / sum((t >> a) & 1 for a in z)
                    for t, r in types.items() if (t >> z[i]) & 1), F())

    def welfare(z):
        return sum((r for t, r in types.items() if any((t >> a) & 1 for a in z)), F())

    rows, failures, margins = [], [], []
    for h in histories:
        z = finish(h)
        incumbent = payoff(z, len(h))
        alternatives = [payoff(finish(h + (a,)), len(h)) for a in range(k)]
        row = {'h': list(h), 'action': policy[h], 's': list(z), 'u': str(incumbent),
               'alternatives': list(map(str, alternatives))}
        rows.append(row)
        for a, alt in enumerate(alternatives):
            margin = incumbent - alt
            margins.append(margin)
            if margin < 0:
                failures.append({'h': list(h), 'chosen': policy[h], 'alternative': a,
                                 'margin': str(margin), 'margin_float': float(margin)})

    def column(z):
        w = welfare(z)
        dev = [sum((payoff(z[:i] + (a,) + z[i+1:], i) for i in range(m)), F()) for a in range(k)]
        gains = [w - d for d in dev]
        lower = w - sum((y * g for y, g in zip(multipliers, gains)), F())
        # Independent per-customer inverse-load expression, including load zero.
        inverse = F()
        for t, r in types.items():
            d = sum((t >> a) & 1 for a in z)
            yt = sum((multipliers[a] for a in range(k) if (t >> a) & 1), F())
            inverse += r * ((1 - sum(multipliers)) * (d > 0) + yt * (F(m) if d == 0 else F(m+1, d+1)))
        require(inverse == lower, 'direct deviation / inverse load identity')
        return {'q': list(z), 'w': int(w) if w.denominator == 1 else str(w),
                'D': list(map(str, dev)), 'G': list(map(str, gains)), 'L': str(lower)}

    columns = [column(z) for z in combinations_with_replacement(range(k), m)]
    by_multiset = {tuple(c['q']): c for c in columns}
    ordered_count = 0
    for z in product(range(k), repeat=m):
        c = column(z)
        ref = by_multiset[tuple(sorted(z))]
        require(all(c[key] == ref[key] for key in ('w', 'D', 'G', 'L')), 'all ordered static columns compressed exactly')
        ordered_count += 1
    actual = finish(())
    w = welfare(actual)
    min_column = min(F(c['L']) for c in columns)
    optimum = max(welfare(z) for z in product(range(k), repeat=m))
    pne_slacks = [[payoff(actual, i) - payoff(actual[:i] + (a,) + actual[i+1:], i)
                   for a in range(k)] for i in range(m)]
    return {'types': {str(t): str(r) for t, r in types.items()},
            'mass': str(sum(types.values(), F())), 'histories': len(histories),
            'comparisons': len(margins), 'path': list(actual),
            'payoffs': [str(payoff(actual, i)) for i in range(m)], 'welfare': str(w),
            'optimum': str(optimum), 'min_spe_margin': str(min(margins)),
            'negative_spe_comparisons': failures, 'dual_y': list(map(str, multipliers)),
            'min_dual_expression': str(min_column), 'dual_gap_to_spe_path': str(min_column - w),
            'dual_gap_float': float(min_column - w), 'dual_tight_multisets': [c['q'] for c in columns if F(c['L']) == min_column],
            'static_multisets': len(columns), 'ordered_static_profiles': ordered_count,
            'actual_terminal_is_static_pne': min(x for row in pne_slacks for x in row) >= 0,
            'actual_terminal_individual_static_slacks': [list(map(str, row)) for row in pne_slacks],
            'spe_rows': rows, 'cce_rows': columns}


def decode_policy(snapshot):
    return {tuple(map(int, key.split(','))) if key else (): action
            for key, action in snapshot['sigma'].items()}


def snapshot_audit(name, integer=False):
    s = load(name)
    require(s['masks'] == list(range(1, 1 << s['k'])), name + ': complete type order')
    values = s['r_integer'] if integer else s['r']
    require(len(values) == len(s['masks']), name + ': vector length')
    types = {t: F(str(r)) for t, r in zip(s['masks'], values) if r}
    y = list(map(F, s['y_rational'])) if integer else [F(str(v)) for v in s['dual_y']]
    report = analyze(s['k'], s['m'], types, decode_policy(s), y)
    require(sorted(report['path']) == s['target'], name + ': target is terminal multiset')
    report['stored_target_multiset'] = s['target']
    report['stored_gap_is_legacy_floating_discovery_field'] = s['gap']
    report['interpretation'] = 'integer weights and explicit rational multipliers' if integer else 'exact decimal-literal interpretation, not a rational repair of intended input'
    return report


def main():
    manifest = json.loads((ROOT / 'source-manifest.json').read_text())
    for row in manifest['primary_sources']:
        raw = (ROOT / row['preserved_path']).read_bytes()
        require(len(raw) == row['size'] and sha256(raw).hexdigest() == row['sha256'], row['id'] + ': frozen bytes')
    floats = {name: snapshot_audit(name) for name in ('cce_best.json', 'cce_best_4_4.json', 'cce_best_5_3.json', 'cce_best_6_3.json')}
    large = load('cce_integer_candidate.json')
    small = load('cce_small_candidate.json')
    require({k: v for k, v in large.items() if k != 'r_integer'} == {k: v for k, v in small.items() if k != 'r_integer'}, 'candidate inherited fields identical')
    first = load('cce_best.json')
    require(all(large[k] == v for k, v in first.items()), 'candidate discovery fields copied from first snapshot')
    integer = snapshot_audit('cce_integer_candidate.json', True)
    tiny = snapshot_audit('cce_small_candidate.json', True)
    for report, clients, welfare, lower, optimum in ((integer, 42, 32, F(33), 42), (tiny, 8, 6, F(85,14), 8)):
        require(F(report['mass']) == clients and F(report['welfare']) == welfare, 'integer client / welfare')
        require(F(report['min_spe_margin']) == 0 and not report['negative_spe_comparisons'], 'exact complete SPE')
        require(F(report['min_dual_expression']) == lower and F(report['optimum']) == optimum, 'exact certificate')
    exact = load('cce_exact.json')
    derived = {'status': 'exact-definition-check-passed', 'types': {k: int(F(v)) for k, v in integer['types'].items()},
               'path': integer['path'], 'payoffs': integer['payoffs'], 'welfare': int(F(integer['welfare'])),
               'optimum': int(F(integer['optimum'])), 'spe_comparisons': integer['comparisons'],
               'spe_min_margin': integer['min_spe_margin'], 'dual_y': integer['dual_y'],
               'cce_lower_bound': 33, 'cce_min_dual_expression': integer['min_dual_expression'],
               'spe_rows': integer['spe_rows'], 'cce_rows': integer['cce_rows']}
    require(derived == exact, 'all 13 top-level fields and all 21 / 20 exact rows reconstructed')
    old = ROOT.parent / 'eight-and-forty-two-client-cce-exact-primary/rerun/forty-two-replay.json'
    require(old.read_bytes() == (ROOT / 'original/cce_exact.json').read_bytes() + b'\n', 'existing replay differs only by final newline')
    for name, expected in (('cce_best_4_4.json', F(4,5)), ('cce_best_6_3.json', F(3,4))):
        r = floats[name]
        require(not r['negative_spe_comparisons'] and r['actual_terminal_is_static_pne'], 'finite equality SPE/PNE')
        require(F(r['min_dual_expression']) == expected == F(r['welfare']), 'finite equality lower/upper')
    require(len(floats['cce_best.json']['negative_spe_comparisons']) == 2, 'first decimal residuals')
    require(len(floats['cce_best_5_3.json']['negative_spe_comparisons']) == 7, 'five-topic decimal residuals')
    # The 42-client full exact rows already exist: retain only the comparison result here.
    integer_summary = {k: v for k, v in integer.items() if k not in ('spe_rows', 'cce_rows')}
    result = {'status': 'passed', 'implementation': 'standard-library Fraction; new internal direct full-history and ordered-profile reconstruction',
              'original_discovery_or_verifier_runs': 0, 'floating_snapshots': floats,
              'forty_two_integer_snapshot': integer_summary, 'eight_integer_snapshot': tiny,
              'exact_frozen_report_all_fields_match': True, 'existing_forty_two_replay_is_source_plus_final_newline': True,
              'integer_candidates_only_differ_in_r_integer': True, 'candidate_discovery_fields_equal_cce_best': True,
              'scope': 'finite explicit points only; no CCE optimality claim for fixed old multipliers at 42/8 clients; no general or six-player conclusion'}
    (ROOT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'primary_source_hashes': 7, 'exact_report_fields_reconstructed': len(exact),
                      'forty_two': {'W': 32, 'CCE_lower': 33}, 'eight': {'W': 6, 'CCE_lower': '85/14'},
                      'decimal_negative_spe_comparisons': {'k4m3': 2, 'k5m3': 7},
                      'finite_equalities': {'k4m4': '4/5', 'k6m3': '3/4'}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
