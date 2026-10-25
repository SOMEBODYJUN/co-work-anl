"""Separate implementation of full-type pricing for the shared-K certificate.

Adapted from the earlier 557-row independent audit, with new active definitions
reconstructed here. Imports no discovery Universe, family_score or row evaluator.
This is an arithmetic audit, not external mathematical review or HALF(5).
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import json
import hashlib
import time
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'exact_shared_root.json'
LABELS = 'ABCDEUVWXY'
PATHS = {'actual': 'ABCDE', 'second': 'AEUVW', 'third': 'ABEXY'}


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for v in range(n+1):
            for tail in compositions(n-v, k-1):
                yield (v,)+tail


def scaled(x):
    v = 120*F(x)
    assert v.denominator == 1
    return v.numerator


def share(bits, path, i):
    n = bits[path[i]]
    return F(n, sum(bits[c] for c in path)) if n else F(0)


def old_value(name, bits, d, menus):
    if name == 'F:second':
        return share(bits, PATHS['actual'], 1)-share(bits, PATHS['second'], 1)
    if name == 'F:third':
        return share(bits, PATHS['actual'], 2)-share(bits, PATHS['third'], 2)
    if name.startswith('MAX:fixed:'):
        return -bits[LABELS[int(name.rsplit(':',1)[1])]]
    if name.startswith('KRS:fixed:'):
        _,_,i,j=name.split(':');t=bits[LABELS[int(i)]];q=bits[LABELS[int(j)]]
        u=share(bits,PATHS['actual'],0)
        return 30*(F(44,3)*u-F(16,3)*t-q+F(4,5)*t*q)
    if name=='KCAP:4':
        return 574700*share(bits,PATHS['actual'],0)-12000*int(d>0)

    pn, *tail = name.split(':')
    path = PATHS[pn]
    if tail[0] == 'reply':
        p = sum(bits[c] for c in path[:3])
        den = (p+1)*(p+2)
        ell, h = menus[list(PATHS).index(pn)]
        if tail[1] == 'S':
            return 5*share(bits, path, 3)-F(d, p+1)+F(h, den)
        if tail[1] == 'V':
            return F(d*ell-5*h, den)
        if tail[1] == 'Z':
            return 5*share(bits, path, 4)-F(ell, p+bits[path[3]]+1)
        assert tail[1] == 'topic-D'
        return F(ell-5*bits['D'], p+1)+F(d*bits['D']-h, den)
    i = int(tail[0])-1
    p = sum(bits[c] for c in path[:i])
    if tail[1] == 'K':
        return share(bits, path, i)-F(bits[tail[2]], p+5-i)
    if tail[1]=='O':
        return 5*(5-i)*share(bits,path,i)+F(p,p+5-i)-int(d>0)
    assert tail[1] == 'sum-opt',name
    return 5*share(bits, path, i)-F(d, p+5-i)


def main():
    begin = time.time()
    src = json.loads(SOURCE.read_text())
    weights = {n: int(v) for n, v in src['integer_multipliers'].items()}
    B, D = int(src['beta_numerator']), int(src['common_denominator'])
    assert min(weights.values()) > 0 and len(weights) == 61
    assert F(B, D) == F(src['dual_beta'])
    old, local, cross = {}, defaultdict(dict), defaultdict(dict)
    for n, v in weights.items():
        parts = n.split(':')
        if parts[0] in ('AB', 'AE', 'Sbranch'):
            tag, tail = parts[0], ':'.join(parts[1:])
            (cross if parts[1] in PATHS else local)[tag][tail] = v
        elif ':sum-S' in n:
            cross['Sbranch'][n] = v
        else:
            old[n] = v
    assert len(old) == 29, len(old)
    hist, types, counts, dvec, ids = {}, {}, {}, {}, {}
    data = {}
    for k in (3, 4):
        types[k] = tuple(product((0, 1), repeat=k))
        hist[k] = np.array(list(compositions(5, 2**k)), dtype=np.int64)
        ty = np.array(types[k], dtype=np.int64)
        counts[k] = hist[k] @ ty
        dvec[k] = counts[k][:, 0]
        ids[k] = [np.flatnonzero(dvec[k] == d) for d in range(6)]
        for p in range(3 if k == 3 else 2):
            def agg(fn):
                return hist[k] @ np.array([scaled(fn(t)) for t in types[k]], dtype=np.int64)
            def sh(t, pos):
                return F(t[pos], p+sum(t)) if t[pos] else F(0)
            data[k, p] = {
                'zt': agg(lambda t: sh(t, 0)),
                'last': agg(lambda t: sh(t, k-1)),
                'du': agg(lambda t: F(1, p+t[0]+3)) if k == 4 else None,
                'zu': agg(lambda t: sh(t, 1)) if k == 4 else None,
            }
            m = data[k, p]
            positions = ((k-2, k-1),)
            lastden = agg(lambda t: F(1, p+sum(t[:-1])+1))
            for pos in range(k):
                own = agg(lambda t: F(t[pos], p+sum(t[:-1])+1))
                m['offdiag', pos] = 4*m['last']-counts[k][:, pos]*lastden+own
            for u, v in positions:
                # Reconstruct query_equal directly as the excluded own index
                # in every source branch's query sum.
                prefix = lambda t: p+sum(t[:-2])
                AA = agg(lambda t: F(1, prefix(t)+1))
                GG = agg(lambda t: F(1, (prefix(t)+1)*(prefix(t)+2)))
                HH = agg(lambda t: (F(t[-2]+t[-1], p+sum(t)) if t[-2]+t[-1] else F(0))
                         + F(t[-2], (prefix(t)+1)*(prefix(t)+2)))
                ownsum = agg(lambda t: F(t[u]+t[v], prefix(t)+1))
                ownboth = agg(lambda t: F(t[u]*t[v], (prefix(t)+1)*(prefix(t)+2)))
                overlap = hist[k] @ np.array([t[u]*t[v] for t in types[k]], dtype=np.int64)
                m['pair'] = (4*HH-(counts[k][:, u]+counts[k][:, v])*AA
                             +ownsum+overlap*GG-ownboth)
            if k == 3:
                DY = agg(lambda t: F(1, p+t[0]+t[1]+1))
                m['last:sum-last'] = 5*m['last']-counts[k][:, 2]*DY
            else:
                DW = lastden
                m['last:sum-last'] = 5*m['last']-counts[k][:, 3]*DW
                m['3:sum-W'] = 5*m['zu']-counts[k][:, 3]*m['du']

    cache = {}
    minimum = None
    zero_cases = 0
    witnesses = []
    for mask in product((0, 1), repeat=10):
        bits = dict(zip(LABELS, mask))
        family_maxima = []
        for tag in ('AB', 'AE', 'Sbranch'):
            k = 4 if tag == 'Sbranch' else 3
            p = bits['A']+(bits['B'] if tag == 'AB' else bits['E'] if tag == 'AE' else 0)
            m = data[k, p]
            const = 0
            crosscoef = [0]*k
            for n, weight in cross[tag].items():
                pn, seat, mn = n.split(':')
                i = int(seat)-1
                path = PATHS[pn]
                pos = ('TUVW' if k == 4 else 'TXY').index(mn.removeprefix('sum-').removeprefix('S'))
                crosscoef[pos] -= weight*scaled(F(1, sum(bits[c] for c in path[:i])+5-i))
                const += weight*scaled(5*share(bits, path, i))
            key = tag, p, bits['Y'] if k == 4 else 0, tuple(crosscoef)
            if key not in cache:
                score = np.zeros(len(hist[k]), dtype=object)
                for n, weight in local[tag].items():
                    if n in ('F2', 'F3'):
                        vec = -m['zt']
                    elif n in ('5:sum-Y', '5:sum-W'):
                        vec = m['last:sum-last']
                    elif n == '3:K:Y':
                        vec = m['zu']-bits['Y']*m['du']
                    elif n == '3:sum-W':
                        vec = m[n]
                    elif n.startswith('5:offdiag:'):
                        vec = m['offdiag', int(n.rsplit(':', 1)[1])]
                    elif n.startswith('pair:'):
                        assert n == ('pair:23:query_equal' if k == 4 else 'pair:12:query_equal')
                        vec = m['pair']
                    else:
                        raise AssertionError(n)
                    score += weight*vec.astype(object)
                for pos, weight in enumerate(crosscoef):
                    score += weight*counts[k][:, pos].astype(object)
                cache[key] = [max(score[ix]) for ix in ids[k]]
            const += local[tag]['F2' if k == 4 else 'F3']*scaled(5*share(bits, PATHS['second' if tag == 'AE' else 'actual'], 1 if k == 4 else 2))
            family_maxima.append([v+const for v in cache[key]])
        for d in range(6):
            menus0 = [(0, 0)]*3
            base = sum(weight*scaled(old_value(n, bits, d, menus0)) for n, weight in old.items())
            extra = 0
            corners = ((0, 0), (d, d), (5-d, 0), (5, d))
            for f in range(3):
                vals = []
                for ell, h in corners:
                    menus = menus0.copy()
                    menus[f] = ell, h
                    vals.append(sum(weight*scaled(old_value(n, bits, d, menus)-old_value(n, bits, d, menus0))
                                    for n, weight in old.items()))
                extra += max(vals)
            residual = 120*(B*int(any(mask[:5]))-D*int(d > 0))-base-extra-sum(f[d] for f in family_maxima)
            assert isinstance(residual, int), type(residual)
            if minimum is None or residual < minimum:
                minimum = residual
            if residual == 0:
                zero_cases += 1
            if residual < 0:
                witnesses.append((''.join(map(str, mask)), d, str(residual)))
    kcoef={n:(1 if n.startswith('MAX:fixed:') else 78 if n.startswith('KRS:fixed:') else -88940 if n=='KCAP:4' else 0) for n in weights}
    kres=-sum(weights[n]*kcoef[n] for n in weights)
    assert kres>=0
    report = {
        'scope': 'Separate active61-multiplier exact full-type shared-K dual pricing; adapted old independent audit',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'beta': str(F(B, D)), 'positive_multipliers': len(weights),
        'fixed_masks': 1024, 'shared_optimal_multiplicities': 6,
        'third_histograms': len(hist[3]), 'second_histograms': len(hist[4]),
        'conditional_cases': 6144, 'score_contexts': len(cache),
        'menu_corners_per_family': 4,
        'minimum_scaled_integer_residual': str(minimum), 'zero_conditional_cases': zero_cases,
        'negative_cases': witnesses, 'all_cases_nonnegative': not witnesses,
        'uses_discovery_pricing_implementation': False,
        'K_dual_residual': str(kres),
        'K_dual_nonnegative': kres>=0,
        'seconds': time.time()-begin,
        'not_claimed': ['SPE completion of relaxation optimum', 'general half coverage'],
    }
    HERE.joinpath('separate_shared_root_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    assert not witnesses


if __name__ == '__main__':
    main()
