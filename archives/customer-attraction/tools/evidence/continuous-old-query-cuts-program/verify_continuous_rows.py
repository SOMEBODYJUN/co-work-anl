"""Current exact, local verification; never builds the combined graph."""
import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

PAT = tuple(itertools.product((0, 1), repeat=3))
GS = ((0, 0), (1, 0), (1, 1))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(None)
def literal(i, p, ell, t, q, am, al, mu):
    n = 5-i
    vals = []
    for hidden in itertools.product((0, 1), repeat=n):
        s, g = sum(hidden[:-1]), hidden[-1]
        z = p+t+s+g
        vals.append((F(t, z) if t else F())
                    + (am*s+al*g)/(ell+1)
                    - (mu*g/z if g else F())
                    + mu*F(q, p+t+s+1))
    return min(vals)


def edges(hist, f, diag):
    words = [w for w, count in zip(PAT, hist) for _ in range(count)]
    assert len(words) == 6
    return [(words[a], words[b]) for a in range(6) for b in range(6)
            if (a == b) == bool(diag)]


def independent_row(cols, cut):
    i, member, f, diag, qi, am, al, mu = cut
    am, al, mu = map(F, (am, al, mu))
    count = 6 if diag else 30
    out = [F()] * len(cols)
    h = None
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            h = c
            a = tuple(map(int, c['actual_bits']))
            p, ell, whole = sum(a[:i]), sum(a[:5]), sum(a)
            own = F(a[i], whole) if a[i] else F()
            last = F(a[5], whole) if a[5] else F()
            pairs = edges(c['hist'], f, diag)
            out[j] = count*(own+((4-i)*am+al)*last)
            out[j] -= sum(literal(i, p, ell, 0, (wi+wj)[qi], am, al, mu)
                          for wi, wj in pairs)
        elif c['kind'] == 'joint-reply':
            ff, dd, wi, wj = c['group']
            if (ff, dd) != (f, diag) or not c['state'][member]:
                continue
            multiplicity = sum(x == tuple(wi) and y == tuple(wj) for x, y in pairs)
            q = (wi+wj)[qi]
            out[j] = -multiplicity*(literal(i, p, ell, 1, q, am, al, mu)
                                    - literal(i, p, ell, 0, q, am, al, mu))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--cuts', type=Path, required=True)
    ap.add_argument('--point', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(args.source.parent))
    spec = importlib.util.spec_from_file_location('frozen_cont', args.source)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    cuts = json.loads(args.cuts.read_text())
    point = json.loads(args.point.read_text())
    cols = point['columns']
    weights = [F(c['weight']) for c in cols]
    assert len(cols) == 1905 and min(weights) >= 0
    kinds = Counter(c['kind'] for c in cols)
    hist_indices = [i for i,c in enumerate(cols) if c['kind'] == 'hist']
    assert len(hist_indices) == 16
    structure_checks = 0
    marginal_checks = 0
    current = None
    grouped = defaultdict(list)
    for index, c in enumerate(cols):
        if c['kind'] == 'hist':
            current = index
            assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0','1'}
            assert len(c['hist']) == 8 and sum(c['hist']) == 6
            assert all(type(v) is int and v >= 0 for v in c['hist'])
            assert c['d'] == sum(n*w[0] for n,w in zip(c['hist'],PAT))
            for f,d in GS:
                expected = Counter(edges(c['hist'], f, d))
                actual = {(wi,wj):n for (ff,dd,wi,wj),n in original.oq.groups(c['hist']).items() if (ff,dd)==(f,d)}
                assert expected == actual
                structure_checks += 1
        elif c['kind'] == 'joint-reply':
            assert current is not None
            f,d,wi,wj = c['group']
            assert (f,d) in GS and tuple(wi) in PAT and tuple(wj) in PAT
            assert c['state'] in [[0,1],[1,0],[1,1]]
            key = (current,f,d,tuple(wi),tuple(wj))
            grouped[key].append(index)
    for key, indices in grouped.items():
        assert len(indices) == 3
        assert {tuple(cols[j]['state']) for j in indices} == {(0,1),(1,0),(1,1)}
        assert sum(weights[j] for j in indices) <= weights[key[0]]
        marginal_checks += 1
    hist_mass = sum(weights[i] for i in hist_indices)
    O = sum(weights[i] for i in hist_indices if cols[i]['d'])
    W = sum(weights[i] for i in hist_indices if '1' in cols[i]['actual_bits'])
    assert O == F(point['O']) == 1 and W == F(point['W'])
    assert F(point['strict_half_gap']) == O-2*W
    assert sum(w > 0 for w in weights) == point['positive_columns']
    allrows = []
    comparisons = 0
    for ordinal, saved in enumerate(cuts['selected']):
        cut = saved['cut']
        i,member,f,d,qi,*prices = cut
        assert i in range(5) and member in range(2) and (f,d) in GS and qi in range(6)
        assert all(F(x)>=0 for x in prices)
        row = original.row(cols, cut)
        independent = independent_row(cols, cut)
        assert row == independent
        comparisons += len(cols)
        slack = sum(a*b for a,b in zip(row,weights))
        assert slack == F(saved['slack']) < 0
        allrows.append({'ordinal':ordinal,'cut':cut,'exact_slack':str(slack),
                        'nonzero_coefficients':sum(v != 0 for v in row),
                        'coefficient_sha256':hashlib.sha256(('\n'.join(map(str,row))+'\n').encode()).hexdigest()})
    prices = {tuple(map(F,c['cut'][5:])) for c in cuts['selected']}
    prices |= {(F(0),F(0),F(0)),(F(1),F(2),F(3)),(F(1000),)*3}
    projection_checks = 0
    for i in range(5):
        for p, rest, t, q, triple in itertools.product(range(i+1),range(6-i),range(2),range(2),sorted(prices)):
            ell = p+rest
            assert original.psi(i,p,ell,t,q,*triple) == literal(i,p,ell,t,q,*triple)
            projection_checks += 1
    data, us = original.sufficient_stats(cols, weights)
    duplicate_vectors = defaultdict(list)
    for r in allrows:
        duplicate_vectors[r['coefficient_sha256']].append(r['ordinal'])
    summary = {
        'status':'PASS','scope':'local coefficient and exact saved-cut audit only; not original graph feasibility or SPE',
        'source_sha256':sha(args.source),'cuts_sha256':sha(args.cuts),'point_sha256':sha(args.point),
        'column_kinds':dict(kinds),'column_count':len(cols),'positive_columns':sum(w>0 for w in weights),
        'histogram_count':len(hist_indices),'histogram_mass':str(hist_mass),'O':str(O),'W':str(W),
        'orbit_group_comparisons':structure_checks,'joint_group_mass_checks':marginal_checks,
        'selected_count':len(allrows),'row_coefficient_comparisons':comparisons,
        'unique_saved_parameter_triples':len({tuple(c['cut'][5:]) for c in cuts['selected']}),
        'projection_parameter_triples_with_boundary_samples':len(prices),'literal_binary_projection_checks':projection_checks,
        'finite_structures':5*2*len(GS)*6,'reported_LPs':cuts['LPs'],
        'i_counts':dict(Counter(str(c['cut'][0]) for c in cuts['selected'])),
        'family_diagonal_counts':dict(Counter(str(tuple(c['cut'][2:4])) for c in cuts['selected'])),
        'minimum_saved_slack':str(min(F(r['exact_slack']) for r in allrows)),
        'maximum_saved_slack':str(max(F(r['exact_slack']) for r in allrows)),
        'all_saved_exact_slacks_match':True,'all_saved_rows_equal_literal_index_implementation':True,
        'distinct_saved_coefficient_vectors':len(duplicate_vectors),
        'duplicate_saved_vector_ordinals_zero_based':[v for v in duplicate_vectors.values() if len(v)>1],
        'point_original_4971_rows_replayed':False,'combined_5108_graph_built':False,'original_discovery_cli_called':False,
        'float_sufficient_stats_structures':len(data),'float_actual_utilities':us,
        'row_results':allrows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k != 'row_results'},indent=2))


if __name__ == '__main__':
    main()
