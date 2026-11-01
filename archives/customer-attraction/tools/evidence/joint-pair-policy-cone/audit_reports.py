#!/usr/bin/env python3
"""Definition-level audit of ONE saved joint incumbent and one empty report.

Standard library only. Does not import/execute the original programs, generate
MILP matrices, optimize, or change the saved coordinates. Decimal JSON tokens
and the binary floats produced by json.loads are two distinct rational inputs.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations_with_replacement, product
import json
from math import comb
from pathlib import Path


def digest(path):
    b = Path(path).read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def rational_load(path, mode):
    if mode == 'decimal_tokens':
        return json.loads(Path(path).read_text(), parse_float=F)
    return json.loads(Path(path).read_text(), parse_float=lambda x: F(float(x)))


def counts(h, k):
    return tuple(h.count(a) for a in range(k))


def analyze(path, mode):
    d = rational_load(path, mode)
    k, n = d['k'], d['n']
    w, p, Q = list(map(F, d['weights'])), list(map(F, d['p'])), list(map(F, d['Q']))
    histories = [h for depth in range(n) for h in product(range(k), repeat=depth)]
    count_nodes = [counts(h, k) for depth in range(n)
                   for h in combinations_with_replacement(range(k), depth)]
    full = {tuple(x['history']): x['action'] for x in d['full_policy']}
    cp = {tuple(x['counts']): x['action'] for x in d['count_policy']}
    assert len(full) == len(d['full_policy']) == len(histories)
    assert len(cp) == len(d['count_policy']) == len(count_nodes)
    assert set(full) == set(histories) and set(cp) == set(count_nodes)
    assert all(full[h] == cp[counts(h, k)] and 0 <= full[h] < k for h in histories)
    assert len(w) == (1 << k)-1 and len(p) == k
    rivals = list(combinations_with_replacement(range(k), n-3))
    assert list(map(tuple, d['tail_rivals'])) == rivals and len(Q) == len(rivals)

    @lru_cache(None)
    def finish(h):
        return h if len(h) == n else finish(h+(full[h],))

    def payoff(a, leaf):
        ans = F(0)
        for mask, weight in enumerate(w, 1):
            if weight and mask & (1 << a):
                load = sum(bool(mask & (1 << b)) for b in leaf)
                assert load > 0  # a is the actual or deviating player in leaf
                ans += weight/load
        return ans

    ledger = []
    for h in histories:
        a = full[h]
        leaf = finish(h)
        actual = payoff(a, leaf)
        for b in range(k):
            other = finish(h+(b,))
            alt = payoff(b, other)
            ledger.append(dict(history=h, prescribed=a, deviation=b,
                               actual_leaf=leaf, deviation_leaf=other,
                               actual_payoff=str(actual), deviation_payoff=str(alt),
                               slack=str(actual-alt)))
    values = [F(x['slack']) for x in ledger]
    minimum = min(values)
    witness = next(x for x in ledger if F(x['slack']) == minimum)
    leaf = finish(())
    assert list(leaf) == d['path'] and list(counts(leaf, k)) == d['actual_root_counts']

    def query(a, background):
        return sum((mass/F(1+sum(bool(mask & (1 << b)) for b in background))
                    for mask, mass in enumerate(w, 1) if mask & (1 << a)), F(0))

    root_rows = []
    for H in combinations_with_replacement(range(k), n-1):
        pure = [query(a, H) for a in range(k)]
        value = sum((pa*x for pa, x in zip(p, pure)), F(0))
        root_rows.append(dict(background=H, pure_payoffs=list(map(str, pure)), mixed=str(value)))
    tail_rows = []
    for a in range(k):
        pure = [query(a, tuple(leaf[:2])+B) for B in rivals]
        value = sum((qb*x for qb, x in zip(Q, pure)), F(0))
        tail_rows.append(dict(action=a, by_rival=list(map(str, pure)), mixed=str(value)))
    ell = min(F(x['mixed']) for x in root_rows)
    cap = max(F(x['mixed']) for x in tail_rows)
    pair = payoff(leaf[0], leaf)+payoff(leaf[1], leaf)
    formal_gap = pair-n*ell+(n-2)*cap
    stats = dict(
        interpretation=mode, fields=list(d), field_count=len(d), count_nodes=len(cp),
        ordered_nodes=len(full), count_by_depth=dict(Counter(map(sum, cp))),
        ordered_by_depth=dict(Counter(map(len, full))), actual_path=leaf,
        actual_root_counts=counts(leaf, k), count_to_ordered_actions_all_equal=True,
        coordinate_count=len(w), nonzero_weights=[dict(mask=i, value=str(x)) for i,x in enumerate(w,1) if x],
        negative_weight_count=sum(x<0 for x in w), mass_sum=str(sum(w)),
        mass_sum_minus_one=str(sum(w)-1), universal_weight=str(w[-1]),
        frozen_source_universal_upper_bound=0,
        frozen_source_universal_bound_violation=str(w[-1]),
        p_sum=str(sum(p)), p_sum_minus_one=str(sum(p)-1),
        Q_sum=str(sum(Q)), Q_sum_minus_one=str(sum(Q)-1),
        comparisons=len(ledger), self_comparisons=sum(x['prescribed']==x['deviation'] for x in ledger),
        negative_IC=sum(x<0 for x in values), zero_IC=sum(x==0 for x in values),
        positive_IC=sum(x>0 for x in values), minimum_IC=str(minimum),
        minimum_witness=witness,
        stored_floating_min_full_Gamma=str(d['floating_min_full_Gamma']),
        exact_min_minus_stored_min=str(minimum-F(d['floating_min_full_Gamma'])),
        root_background_count=len(root_rows), tail_query_count=len(tail_rows),
        root_min_formal=str(ell), tail_max_formal=str(cap), pair_payoff_formal=str(pair),
        reconstructed_tight_formal_surrogate=str(formal_gap),
        formal_surrogate_float=float(formal_gap),
        stored_objective=str(d['objective']),
        note='Signed mass and nonunit distributions: formal diagnostics only, not a legal game/security certificate. The saved t,h,z,U are absent, so this is NOT the original solver objective.')
    return stats, dict(interpretation=mode, full_history_comparisons=ledger,
                       root_query_rows=root_rows, tail_query_rows=tail_rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--normal', type=Path, required=True)
    ap.add_argument('--strip', type=Path, required=True)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a=ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    primary = json.loads(a.normal.read_text())
    strip = json.loads(a.strip.read_text())
    assert all(primary[x] == strip[x] for x in ('k','n','path','p','Q','tail_rivals','variables','binaries','rows'))
    assert 'weights' not in strip and 'full_policy' not in strip and strip['objective'] is None
    assert "upper[s.k-1]=0" in a.source.read_text()
    k,n=primary['k'],primary['n']
    N=comb(k+n-1,n-1)
    expected=dict(count_nodes=N, types=(1<<k)-1,
                  variables=(1<<k)-1+2*k*N+2, binaries=k*N,
                  rows=1+N*(1+k*(2*k+k-1))+comb(k+n-2,n-1)+k)
    assert all(primary[x] == expected[x] for x in ('variables','binaries','rows'))
    cases=[]; details=[]
    for mode in ('decimal_tokens','decoded_binary_floats'):
        stats, ledger=analyze(a.normal, mode)
        cases.append(stats); details.append(ledger)
    raw=(json.dumps(details, ensure_ascii=False, indent=2)+'\n').encode()
    packed=gzip.compress(raw, mtime=0)
    (a.out/'full-history-ledger.json.gz').write_bytes(packed)
    report=dict(status='PASS: source/report structure and independent diagnostics; saved incumbent FAILS exact feasibility',
                scope=dict(original_main=0, original_functions=0, MILP=0, LP=0,
                           independent_audit=1, saved_incumbents=1, input_interpretations=2,
                           full_history_comparisons=2*k*sum(k**d for d in range(n)),
                           related_report_math=0, rounded_or_repaired_inputs=0),
                sources={x:digest(getattr(a,x)) for x in ('normal','strip','source')},
                static_model_dimensions=expected,
                strip=dict(field_count=len(strip), all_fields=strip,
                           conclusion='Timeout with no saved incumbent; no infeasibility or optimality certificate'),
                interpretations=cases,
                details=dict(path='full-history-ledger.json.gz', compressed=digest(a.out/'full-history-ledger.json.gz'),
                             decoded=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))
    (a.out/'exact-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], dimensions=expected,
                          comparisons=report['scope']['full_history_comparisons'],
                          cases=[{k:x[k] for k in ('interpretation','negative_weight_count','negative_IC','zero_IC','positive_IC','minimum_IC','formal_surrogate_float')} for x in cases]),ensure_ascii=False))


if __name__=='__main__':
    main()
