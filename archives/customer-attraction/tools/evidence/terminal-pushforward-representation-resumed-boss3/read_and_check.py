"""Exact 270-customer packet check; other snapshots get field/target arithmetic only.

No project module, LP, SLSQP, floating discovery entry or other old audit is run.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'original/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation'


def check_270():
    obj = json.loads((SRC / 'entry_potential_implication_270_exact.json').read_text())
    ins = obj['instance']
    clients = [set(c['topics']) for c in ins['customers'] for _ in range(c['multiplicity'])]
    n, m = len(ins['topics']), ins['players']
    rows = obj['certificate']['actions']
    acts = {tuple(row['history']): row['action'] for row in rows}
    assert len(acts) == len(rows)
    assert set(acts) == {h for k in range(m) for h in product(range(n), repeat=k)}
    assert all(type(a) is int and 0 <= a < n for a in acts.values())

    def finish(h):
        while len(h) < m:
            h += (acts[h],)
        return h

    def payoff(z, i):
        return sum((F(1, sum(a in c for a in z)) for c in clients if z[i] in c), F())

    comparisons, least, detail = 0, None, []
    for h in sorted(acts, key=lambda h: (len(h), h)):
        z = finish(h)
        current = payoff(z, len(h))
        differences = []
        for a in range(n):
            other = finish(h + (a,))
            slack = current - payoff(other, len(h))
            assert slack >= 0, (h, a, slack)
            if a != acts[h]:
                comparisons += 1
                least = slack if least is None else min(least, slack)
            differences.append(str(slack))
        detail.append({'history': list(h), 'action': acts[h], 'all_action_slacks': differences})
    paths = [finish((a,)) for a in range(n)]
    D = [payoff(z, 0) for z in paths]
    phi = [sum((sum((F(1, j) for j in range(1, sum(a in c for a in z) + 1)), F())
                for c in clients), F()) for z in paths]
    K = [[sum((F(1, 1 + sum(a in c for a in z)) for c in clients if t in c), F())
          for z in paths] for t in range(n)]
    assert [list(z) for z in paths] == obj['forced_paths']
    assert list(map(str, D)) == obj['root_payoffs']
    assert list(map(str, phi)) == obj['potential']
    assert [list(map(str, row)) for row in K] == obj['K']
    assert obj['verification'] == {'valid': True, 'histories': len(acts), 'deviations': comparisons}
    z = finish(())
    assert [z.count(a) for a in range(n)] == obj['certificate']['terminal_counts']
    witness = obj['witness']
    a, t = witness['b'], witness['t']
    assert [str(K[t][a]), str(D[t]), str(phi[a]), str(phi[t])] == [
        witness['query_entry'], witness['root_t_payoff'], witness['Phi_Z_b'], witness['Phi_Z_t']]
    W = sum(any(a in c for a in z) for c in clients)
    opt = max(sum(any(a in c for a in zs) for c in clients) for zs in product(range(n), repeat=m))
    return {'customers': len(clients), 'histories': len(acts), 'nonself_deviations': comparisons,
            'minimum_ic_slack': str(least), 'all_node_slacks': detail,
            'actual_path': list(z), 'actual_payoffs': list(map(str, [payoff(z, i) for i in range(m)])),
            'W': W, 'OPT': opt, 'root_payoffs': list(map(str, D)),
            'forced_paths': [list(z) for z in paths], 'potential': list(map(str, phi)),
            'K': [list(map(str, row)) for row in K],
            'witness_query_advantage': str(K[t][a]-D[t]),
            'witness_potential_change': str(phi[t]-phi[a]),
            'query_below_actual_u': str(max(D)-K[t][a])}


def snapshot_fields(path):
    d = json.loads(path.read_text(), parse_float=F)
    p, m = d['p'], d['m']
    w = d['weights']
    assert len(w) == (1 << p)-1 and all(x >= 0 for x in w)
    acts = {tuple(h): a for h, a in d['actions']}
    assert len(acts) == len(d['actions'])
    for h, a in acts.items():
        assert 0 <= a < p
    is_individual = path.name.startswith('individual')
    if is_individual:
        expected = {h for k in range(m) for h in product(range(p), repeat=k)}
    else:
        def states(s, k):
            if k == 1:
                yield (s,)
            else:
                for x in range(s+1):
                    for tail in states(s-x, k-1):
                        yield (x,) + tail
        expected = {q for k in range(m) for q in states(k, p)}
        assert len(expected) == comb(p+m-1, m-1)
    assert set(acts) == expected
    result = {'top_level_fields': list(d), 'topics': p, 'players': m,
              'policy_domain': 'ordered histories' if is_individual else 'count states',
              'policy_entries': len(acts), 'weight_entries': len(w),
              'nonzero_weights': [[i+1, str(v)] for i, v in enumerate(w) if v],
              'weight_sum_exact_decimal': str(sum(w)),
              'action_histogram': dict(Counter(acts.values())),
              'SPE_or_IC_checked': False}
    if is_individual:
        h = ()
        while len(h) < m:
            h += (acts[h],)
        result.update({'root_action': d['root_action'], 'ratio_decimal': str(d['ratio']),
                       'actual_path_by_action_table': list(h),
                       'policy_stream_depth_lex': ''.join(map(str, [acts[h] for h in sorted(acts, key=lambda h: (len(h), h))]))})
    else:
        def leaf(a):
            q = [0]*p
            q[a] += 1
            while sum(q) < m:
                q[acts[tuple(q)]] += 1
            return tuple(q)
        Z = [leaf(a) for a in range(p)]
        def val(q, a, extra):
            return sum((v/F(d['background'] + extra + sum(q[j] for j in range(p) if (mask >> j) & 1))
                        for mask, v in enumerate(w, 1) if v and (mask >> a) & 1), F())
        L = [val(Z[a], a, 0) for a in range(p)]
        K = [[val(Z[b], a, 1) for b in range(p)] for a in range(p)]
        probability = d['probability']
        C = sum((probability[a]*probability[b]*K[a][b] for a in range(p) for b in range(p)), F())
        D = sum((probability[a]*L[a] for a in range(p)), F())
        result.update({'forced_terminal_counts': [list(z) for z in Z],
                       'probability_entries_exact_decimal': list(map(str, probability)),
                       'probability_sum_exact_decimal': str(sum(probability)),
                       'saved_D_minus_C_token': str(d['D_minus_C']),
                       'raw_token_D_minus_C_approx': float(D-C),
                       'raw_token_maxL_minus_C_approx': float(max(L)-C),
                       'arithmetic_scope': 'raw decimal polynomial; no normalization, IC or exact-candidate certification'})
    return result


def main():
    start = time.perf_counter()
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    assert all(hashlib.sha256((ROOT/'original'/r['path']).read_bytes()).hexdigest() == r['sha256'] for r in manifest)
    report = {'exact_270': check_270(),
              'floating_snapshot_reading': {p.name: snapshot_fields(p) for p in SRC.glob('*.json') if not p.name.startswith('entry_')},
              'execution_scope': 'one new standard-library 270 full-policy check and field/target arithmetic for five float snapshots; zero original search, LP, SLSQP or old audit runs',
              'elapsed_seconds': time.perf_counter()-start}
    (ROOT/'current-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status':'passed','exact_270':{k:v for k,v in report['exact_270'].items() if k not in ['all_node_slacks','K']},
                      'float_snapshots':{k:{kk:vv for kk,vv in v.items() if kk in ['policy_entries','weight_entries','saved_D_minus_C_token','raw_token_D_minus_C_approx','raw_token_maxL_minus_C_approx']} for k,v in report['floating_snapshot_reading'].items()},
                      'elapsed_seconds':report['elapsed_seconds']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
