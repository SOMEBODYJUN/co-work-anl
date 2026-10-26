"""Test a fixed rational six-player relaxation witness, never a game or SPE.

Read the saved 3889-row witness. Complete all R bits by a common threshold;
generate each Z conditionally on its own R with the saved four-state masses.
Compute the 60 permutation-class sums for Z_e querying Z_f. This is a
particular joint completion, not optimization over all possible completions.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').is_file())
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'
PAT = list(product(range(2), repeat=3))


def partition(xs):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in xs)


def read_histograms():
    data = json.loads(SOURCE.read_text())
    hs = []
    for c in data['columns']:
        if c['kind'] == 'hist':
            hs.append({'a': tuple(map(int, c['actual_bits'])), 'hist': c['hist'],
                       'h': F(c['weight']), 'groups': defaultdict(dict)})
        elif c['kind'] == 'joint-reply':
            f, diag, wi, wj = c['group']
            group = f, diag, tuple(wi), tuple(wj)
            hs[-1]['groups'][group][tuple(c['state'])] = F(c['weight'])
    return data, hs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data, hs = read_histograms()
    rows = {key: F() for key in product(range(2), range(2), sorted({partition(z) for z in product(range(4), repeat=4)}))}
    unrestricted_upper = dict.fromkeys(rows, F())
    details = []
    max_rows = dict.fromkeys(rows, F())
    for H in hs:
        h = H['h']
        if not h:
            assert not any(v for states in H['groups'].values() for v in states.values())
            continue
        pa = sum(H['a'][:4])
        words = [w for w, n in zip(PAT, H['hist']) for _ in range(n)]
        assert len(words) == 6
        edges = [(f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j]

        def group(e):
            f, i, j = e
            return f, int(i == j), words[i], words[j]

        qs, zs, rs_zs = {}, {}, {}
        for g, st in H['groups'].items():
            p01, p10, p11 = (st[s] for s in ((0, 1), (1, 0), (1, 1)))
            assert min(p01, p10, p11) >= 0 and p01 + p10 + p11 <= h
            qs[g], zs[g], rs_zs[g] = p10 + p11, p01 + p11, p11

        def cross_rz(g, gg):
            # mass(R_g * Z_gg) under threshold R and conditional Z.
            qe, qf = qs[g], qs[gg]
            both = min(qe, qf)
            p01 = zs[gg] - rs_zs[gg]
            return ((rs_zs[gg] * both / qf) if qf else F()) + ((p01 * (qe - both) / (h - qf)) if qf != h else F())

        for g in qs:
            assert cross_rz(g, g) == rs_zs[g]
        cuts = sorted(set([F(), h, *qs.values()]))
        pieces = [(lo, hi) for lo, hi in zip(cuts, cuts[1:]) if hi > lo]
        # Coefficients of each row when Z mass may vary arbitrarily on each
        # fixed R-threshold piece. Saved own (R_g,Z_g) four states stay fixed.
        coefficients = {key: {g: [F()] * len(pieces) for g in qs} for key in rows}
        for e in edges:
            f, i, j = e
            ge = group(e)
            for ee in edges:
                ff, k, l = ee
                gf = group(ee)
                # The Z_e terminal prefix is actual-first-four followed by R_e.
                # Its IC against Z_f equals (z_e-z_f)/(pa+r_e+1).
                value = (zs[ge] - zs[gf]) / (pa + 1) - (rs_zs[ge] - cross_rz(ge, gf)) / ((pa + 1) * (pa + 2))
                key = f, ff, partition((i, j, k, l))
                rows[key] += value
                cross_upper = rs_zs[ge] if e == ee else min(qs[ge], zs[gf])
                unrestricted_upper[key] += ((zs[ge] - zs[gf]) / (pa + 1)
                    - (rs_zs[ge] - cross_upper) / ((pa + 1) * (pa + 2)))
                for si, (lo, hi) in enumerate(pieces):
                    re = int(hi <= qs[ge])
                    c = F(1, pa + re + 1)
                    coefficients[key][ge][si] += c
                    coefficients[key][gf][si] -= c
        for key, coefs in coefficients.items():
            for g, cs in coefs.items():
                for rg, mass in ((1, rs_zs[g]), (0, zs[g] - rs_zs[g])):
                    items = [(c, hi - lo) for c, (lo, hi) in zip(cs, pieces) if int(hi <= qs[g]) == rg]
                    remaining = mass
                    for c, capacity in sorted(items, reverse=True):
                        take = min(remaining, capacity)
                        max_rows[key] += c * take
                        remaining -= take
                    assert remaining == 0
        details.append({'h': str(h), 'groups': len(qs), 'threshold_pieces': len(set([F(), h, *qs.values()])) - 1})
    result = {
        'scope': 'One rational common-threshold/conditional-Z completion of a necessary-condition point; not a game, SPE, full closure, or half proof',
        'source': str(SOURCE.relative_to(ROOT)), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'W': data['W'], 'O': data['O'], 'rows': len(rows),
        'negative_rows': [{'key': [k[0], k[1], list(k[2])], 'slack': str(v)} for k, v in rows.items() if v < 0],
        'min_slack': str(min(rows.values())), 'histograms': details,
        'arbitrary_conditional_Z_individual_row_maxima': {
            'scope': 'Each row independently maximized over conditional Z allocations on the fixed common-threshold R pieces, preserving every own four-state mass; no simultaneous feasibility assertion',
            'strictly_negative_maxima': [{'key': [k[0], k[1], list(k[2])], 'maximum': str(v)} for k, v in max_rows.items() if v < 0],
            'minimum_of_individual_maxima': str(min(max_rows.values())),
        },
        'unrestricted_pairwise_upper_bounds': {
            'scope': 'Upper bound for each class sum under any joint coupling preserving each labeled reply local four-state marginal; each cross R_e Z_f <= min(mass R_e,mass Z_f). Joint attainability is not asserted.',
            'strictly_negative_upper_bounds': [{'key': [k[0], k[1], list(k[2])], 'upper_bound': str(v)} for k, v in unrestricted_upper.items() if v < 0],
            'minimum_upper_bound': str(min(unrestricted_upper.values())),
        },
    }
    if args.output:
        with args.output.open('x') as out:
            out.write(json.dumps(result, indent=2) + '\n')
    assert len(result['unrestricted_pairwise_upper_bounds']['strictly_negative_upper_bounds']) == 4
    assert min(unrestricted_upper.values()) == F(-77805114978912902524965135501273065957, 176731722247831414031521292083980140160)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
