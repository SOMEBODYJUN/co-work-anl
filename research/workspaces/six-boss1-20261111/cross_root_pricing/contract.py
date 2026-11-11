"""Exact six-root shared-customer projection; no optimizer is imported here.

Each column contains SIX root records from one customer, not six independent
tail marginals. The d=1 optimization specialization is checked at its entry.
General exact formulas retain every root's actual prefix and all six indices.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations_with_replacement
import hashlib
import json

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
POINT = RUN / 'peer_augmented_lp/augmented_lp_exact.json'
POINT_SHA = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
KAPPA = F(226487, 10**21)
ZERO = F(0)
WORDS = [tuple(map(int, f'{w:05b}')) for w in range(32)]
QUERY_PAIRS = list(combinations_with_replacement(range(6), 2))


def frac(n, d):
    return F(n, d) if n else ZERO


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_inputs():
    assert sha(POINT) == POINT_SHA, 'The exact necessary point changed.'
    raw = json.loads(POINT.read_text())
    hist = [v for v in raw['columns'] if v['kind'] == 'hist']
    masses = defaultdict(F)
    for v in hist:
        masses[(v['actual_bits'], v['d'])] += F(v['weight'])
    masses = {k: v for k, v in sorted(masses.items()) if v}
    cap = next(F(v['weight']) for v in raw['columns'] if v['kind'] == 'K')
    pay = [sum(m * frac(int(a[i]), sum(map(int, a)))
               for (a, d), m in masses.items()) for i in range(6)]
    assert sum(pay) == F(raw['W'])
    remainder = {}
    sources = [{'path': str(POINT.relative_to(RUN)), 'sha256': POINT_SHA}]
    for t in (0, 1):
        p = RUN / f'background_five_bridge/fixed53_b{t}_profit.json'
        z = json.loads(p.read_text())
        sources.append({'path': str(p.relative_to(RUN)), 'sha256': sha(p)})
        for v in z['min_by_actual_and_d']:
            remainder[t, int(v['actual'], 2), v['d']] = F(v['min_rho'])
    return {'raw': raw, 'hist': hist, 'masses': masses, 'K': cap,
            'u': pay, 'O': F(raw['O']), 'remainder': remainder,
            'sources': sources}


def row_names(extended=True):
    out = [('gamma',)]
    out += [('price', k) for k in range(5)]
    out += [('capacity', k) for k in range(5)]
    out += [('floor-actual', k, i) for k in range(5) for i in range(6)]
    out += [('floor-other-opt', k) for k in range(5)]
    out += [('floor-root', k) for k in range(5)]
    out += [('floor-own-tail', k, l) for k in range(5) for l in range(5) if k != l]
    assert len(out) == 71
    out += [('cross-floor', k, l) for k in range(5) for l in range(5)]
    if extended:
        out += [('cross-pair', q, r) for q, r in QUERY_PAIRS]
        out += [('actual-floor', i, k) for i in range(5) for k in range(5)]
        out += [('actual-pair', q, r) for q, r in QUERY_PAIRS]
    assert len(out) == (163 if extended else 96)
    return out


def budgets(data, names):
    out = []
    for p in names:
        if p[0] == 'gamma':
            out.append(-KAPPA * data['K'] - F(5, 6) * data['O'])
        elif p[0] == 'price':
            out.append(data['u'][5])
        elif p[0] == 'capacity':
            out.append(data['K'])
        elif p[0] == 'actual-floor':
            out.append(data['u'][p[1]])
        elif p[0] == 'actual-pair':
            h = data['u'][4] + data['u'][5]
            h += sum(m * frac(int(a[4]), (sum(map(int, a[:4])) + 1)
                             * (sum(map(int, a[:4])) + 2))
                     for (a, d), m in data['masses'].items())
            out.append(h)
        else:
            out.append(ZERO)
    return out


def single_root_local(actual, d, t, word, names, remainder):
    """Local part of each budget cost, already divided by six.

    For cross-floor/cross-pair the full contribution is pairwise and occurs
    below. This gives a quadratic integer-count pricing representation.
    """
    a = tuple(map(int, actual))
    e = WORDS[word]
    z = sum(e)
    v = [frac(b, t + z) for b in e]
    ell = sum(a[:5])
    out = []
    query = (t,) + e
    actual_pair_p = sum(a[:4])
    for name in names:
        typ = name[0]
        if typ == 'gamma':
            val = -2 * frac(z, t + z) + remainder[t, word, d - t]
        elif typ == 'price':
            val = frac(e[name[1]], ell + 1)
        elif typ == 'capacity':
            val = F(e[name[1]])
        elif typ.startswith('floor-'):
            k = name[1]
            den = t + sum(e[:k]) + 5 - k
            if typ == 'floor-actual':
                ic = v[k] - frac(a[name[2]], den)
            elif typ == 'floor-other-opt':
                ic = 5 * v[k] - frac(d - t, den)
            elif typ == 'floor-root':
                ic = v[k] - frac(t, den)
            elif typ == 'floor-own-tail':
                ic = v[k] - frac(e[name[2]], den)
            else:
                raise ValueError(name)
            val = -ic
        elif typ == 'actual-floor':
            i, k = name[1:]
            val = frac(e[k], sum(a[:i]) + 6 - i)
        elif typ == 'actual-pair':
            q, r = name[1:]
            val = frac(query[q] + query[r], actual_pair_p + 1)
            val -= frac(query[q] * query[r], (actual_pair_p + 1) * (actual_pair_p + 2))
        elif typ in ('cross-floor', 'cross-pair'):
            val = ZERO
        else:
            raise ValueError(name)
        out.append(val / 6)
    return frac(t, t + z) / 6, out


def directed_pair_cost(t, word, s, donor_word, names):
    """One ordered distinct-root pair's contribution to budget costs.

    The cross-floor source sums five queries then averages its six recipients
    (1/6). The strong PAIR is averaged over all 30 ordered distinct-root pairs.
    """
    e, f = WORDS[word], WORDS[donor_word]
    z = sum(e)
    p = t + sum(e[:3])
    h = frac(e[3] + e[4], t + z) + frac(e[3], (p + 1) * (p + 2))
    donor = (s,) + f
    out = []
    for name in names:
        typ = name[0]
        if typ == 'cross-floor':
            k, l = name[1:]
            den = t + sum(e[:k]) + 5 - k
            val = (frac(f[l], den) - frac(e[k], t + z)) / 6
        elif typ == 'cross-pair':
            q, r = name[1:]
            val = (-h + frac(donor[q] + donor[r], p + 1)
                   - frac(donor[q] * donor[r], (p + 1) * (p + 2))) / 30
        else:
            val = ZERO
        out.append(val)
    return out


def compressed_column(actual, d, roots, names, remainder):
    """Cost using count compression and total slot/intersection counts."""
    assert len(roots) == 6 and sum(t for t, w in roots) == d
    counts = defaultdict(int)
    for root in roots:
        counts[root] += 1
    root_pay = ZERO
    out = [ZERO] * len(names)
    for (t, w), n in counts.items():
        r, v = single_root_local(actual, d, t, w, names, remainder)
        root_pay += n * r
        out = [x + n * y for x, y in zip(out, v)]
    total = [sum(n * b for (t, w), n in counts.items()
                 for b in [((t,) + WORDS[w])[q]]) for q in range(6)]
    overlap = {(q, r): sum(n * ((t,) + WORDS[w])[q] * ((t,) + WORDS[w])[r]
                          for (t, w), n in counts.items()) for q, r in QUERY_PAIRS}
    for pos, name in enumerate(names):
        typ = name[0]
        if typ not in ('cross-floor', 'cross-pair'):
            continue
        val = ZERO
        for (t, w), n in counts.items():
            e = WORDS[w]
            query = (t,) + e
            z = sum(e)
            if typ == 'cross-floor':
                k, l = name[1:]
                den = t + sum(e[:k]) + 5 - k
                val += n * (frac(total[l + 1] - e[l], den) - 5 * frac(e[k], t + z)) / 6
            else:
                q, r = name[1:]
                p = t + sum(e[:3])
                h = frac(e[3] + e[4], t + z) + frac(e[3], (p + 1) * (p + 2))
                val += n * (-5 * h + frac(total[q] + total[r] - query[q] - query[r], p + 1)
                            - frac(overlap[q, r] - query[q] * query[r], (p + 1) * (p + 2))) / 30
        out[pos] = val
    return root_pay, out


def column_roots(one_word, zero_words):
    assert len(zero_words) == 5
    return [(1, one_word)] + [(0, w) for w in zero_words]


def serialized_column(context, one_word, zero_words):
    return {'actual': context[0], 'd': context[1], 'one_word': one_word,
            'zero_words': list(sorted(zero_words))}


if __name__ == '__main__':
    data = load_inputs()
    print(json.dumps({'point_sha256': POINT_SHA, 'contexts': len(data['masses']),
                      'hist_records': len(data['hist']), 'O': str(data['O']),
                      'K': str(data['K']), 'u': list(map(str, data['u'])),
                      'rows_basic': len(row_names(False)), 'rows_extended': len(row_names(True))}, indent=2))
