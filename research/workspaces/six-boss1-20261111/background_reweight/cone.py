"""The complete shifted 53-row cone, with five optional genuine Z queries.

One common nonnegative outer vector is used for BOTH customer backgrounds.
The active local contracts are the already audited fixed-source contracts.
Hidden histograms and menu corners are maximized only AFTER combining rows.
No extremizer from the old 53 weights is frozen by this oracle.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import json
import sys
import time

import numpy as np

# Shared bridge and frozen source trees are read-only dependencies here.
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BRIDGE = HERE.parent / 'background_five_bridge'
SOURCE = ROOT / 'archives/customer-attraction/tools/half5-exact'
sys.path.insert(0, str(BRIDGE))
from shift_certificate import build
from verify_literal_and_bridge import literal_row, expand

LABELS = 'ABCDEUVWXY'
FAMILIES = ('AB', 'AE', 'Sbranch')
CERT = json.loads((SOURCE / 'certificate.json').read_text())
OLD_NAMES = list(CERT['integer_multipliers'])
assert len(OLD_NAMES) == 53
QUERY_NAMES = [f'actual:{i}:query-Z' for i in range(1, 6)]
NAMES = OLD_NAMES + QUERY_NAMES


def normalizer(name):
    z = name.split(':')
    return 10**6 if any(t in ('BG', 'PC', 'DEEP', 'MAXROOT-NEW') for t in z) else 1


SCALES = [normalizer(n) for n in NAMES]


def q(n, d):
    return F(n, d) if n else F(0)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def witness_key(w):
    return json.dumps(w, sort_keys=True, separators=(',', ':'))


def clean_witness(w, background):
    return {k: w[k] for k in ('bits', 'd', 'menus', 'histograms')} | {'background': background}


def target(w):
    b = w['background']
    c = sum(map(int, w['bits'][:5]))
    return 2*q(c, b+c) - q(w['d'], b+w['d'])


def exclusive(w):
    return int(w['background'] == 1 and w['bits'][:5] == '00000')


def query_value(name, bits, background):
    """u_i >= sum_{x in Z} 1/(b+p_i+6-i); the last is exact BR."""
    i = int(name.split(':')[1]) - 1
    actual = [bits[s] for s in 'ABCDE']
    return q(actual[i], background + sum(actual)) - q(
        background, background + sum(actual[:i]) + 5-i)


@lru_cache(maxsize=None)
def literal_vector_cached(key):
    w = json.loads(key)
    b = w['background']
    bits = dict(zip(LABELS, map(int, w['bits'])))
    hist = w['histograms']
    assert b in (0, 1) and len(w['bits']) == 10 and 0 <= w['d'] <= 5
    for tag in FAMILIES:
        k = 4 if tag == 'Sbranch' else 3
        assert len(hist[tag]) == 2**k
        assert all(isinstance(v, int) and v >= 0 for v in hist[tag])
        assert sum(hist[tag]) == 5
        assert sum(n*t[0] for t, n in zip(product((0, 1), repeat=k), hist[tag])) == w['d']
    for ell, h in w['menus']:
        assert 0 <= h <= w['d'] and 0 <= ell-h <= 5-w['d']
    branches = {tag: expand(h, 4 if tag == 'Sbranch' else 3) for tag, h in hist.items()}
    rows = [literal_row(n, bits, w['d'], w['menus'], branches, b, 'profit') for n in OLD_NAMES]
    rows += [(query_value(n, bits, b), F(0)) for n in QUERY_NAMES]
    a = tuple(F(v)/s for (v, k), s in zip(rows, SCALES))
    k = tuple(F(v)/s for (a, v), s in zip(rows, SCALES))
    return a, k


def literal_vector(w):
    return literal_vector_cached(witness_key(w))


def seeds():
    out = []
    for b in (0, 1):
        src = json.loads((BRIDGE / f'fixed53_b{b}_profit.json').read_text())
        out += [clean_witness(r['witness'], b) for r in src['min_by_actual_and_d']]
    return list({witness_key(w): w for w in out}.values())


def old_point():
    D = int(CERT['common_denominator'])
    return [F(int(CERT['integer_multipliers'][n]), D)*s for n, s in zip(OLD_NAMES, SCALES)] + [F(0)]*5


def source_pins():
    paths = [SOURCE/'certificate.json', SOURCE/'verify_certificate.py', BRIDGE/'shift_local.py',
             BRIDGE/'shift_certificate.py', BRIDGE/'shifted_local_tables.json',
             BRIDGE/'verify_literal_and_bridge.py', BRIDGE/'fixed53_b0_profit.json',
             BRIDGE/'fixed53_b1_profit.json']
    paths += sorted((SOURCE/'components').glob('*.json'))
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def check_inputs():
    supplied = json.loads((HERE/'inputs.json').read_text())
    assert supplied['row_names'] == NAMES
    assert supplied['row_normalizers'] == SCALES
    for name, expected in supplied['source_sha256'].items():
        assert sha(ROOT/name) == expected, ('changed source', name)
    return supplied


class Oracle:
    """Exact complete separation on 2*1024*6 visible contexts.

    Three independent histogram MAXes have sizes 792, 792, 15504 and the
    SAME d. Three affine menu MAXes use all four corners. Integer source
    features use share scale 120; exact mode never calls floating argmax.
    A mask restriction is solely for explicitly labelled local smoke tests.
    """

    def __init__(self, mask_ids=None, progress=None):
        self.mask_ids = list(range(1024)) if mask_ids is None else sorted(set(mask_ids))
        self.complete = self.mask_ids == list(range(1024))
        self.domains = {b: build(b, 'profit')[:2] for b in (0, 1)}
        self.fixed = []
        self.family = {tag: [] for tag in FAMILIES}
        for j, name in enumerate(NAMES):
            tag = name.split(':')[0]
            if tag in self.family:
                self.family[tag].append(j)
            elif ':sum-S' in name:
                self.family['Sbranch'].append(j)
            else:
                self.fixed.append(j)
        self.menu = [j for j in self.fixed if ':reply:' in NAMES[j] or ':sum-L-' in NAMES[j]]
        self.contexts = [(b, m, d) for b in (0, 1) for m in self.mask_ids for d in range(6)]
        n = len(self.contexts)
        self.fixed0 = np.zeros((n, len(self.fixed)), dtype=np.int64)
        self.menu_l = np.zeros((n, 3, len(self.fixed)), dtype=np.int64)
        self.menu_h = np.zeros_like(self.menu_l)
        self.t_sc = np.zeros(n, dtype=np.int64)
        self.exclusive = np.zeros(n, dtype=np.int64)
        self.masks = {m: tuple(int(x) for x in f'{m:010b}') for m in self.mask_ids}
        zeros = [(0, 0)]*3
        started = time.monotonic()
        for r, (b, m, d) in enumerate(self.contexts):
            ns, dom = self.domains[b]
            bits = dict(zip(LABELS, self.masks[m]))
            c = sum(self.masks[m][:5])
            self.t_sc[r] = ns['sc'](2*q(c, b+c)-q(d, b+d))
            self.exclusive[r] = int(b == 1 and c == 0)
            for col, j in enumerate(self.fixed):
                name = NAMES[j]
                if j >= 53:
                    v0 = query_value(name, bits, b)
                else:
                    v0, _ = dom.fixed_value(name, bits, d, zeros)
                self.fixed0[r, col] = ns['sc'](v0)
                if j in self.menu:
                    for f in range(3):
                        for which, arr in ((0, self.menu_l), (1, self.menu_h)):
                            menu = zeros.copy()
                            menu[f] = (1, 0) if which == 0 else (0, 1)
                            v, _ = dom.fixed_value(name, bits, d, menu)
                            arr[r, f, col] = ns['sc'](v-v0)
            if progress and r % 1024 == 0:
                progress({'phase': 'compile fixed rows', 'contexts': r, 'seconds': time.monotonic()-started})

    def separate(self, x, epsilon=0, exact=False, return_all=False, progress=None):
        """x_j=lambda_j*normalizer_j; returned residual is target+eps*e-sum."""
        assert len(x) == len(NAMES)
        if exact:
            x = list(map(F, x))
            epsilon = F(epsilon)
            lam = [v/s for v, s in zip(x, SCALES)]
            D = lcm(epsilon.denominator, *(v.denominator for v in lam))
            weights = [int(v*D) for v in lam]
            eps = int(epsilon*D)
            dtype = object
        else:
            weights = [float(v)/s for v, s in zip(x, SCALES)]
            eps = float(epsilon)
            D = 1
            dtype = float
        fw = np.asarray([weights[j] for j in self.fixed], dtype=dtype)
        base = self.fixed0.astype(dtype) @ fw
        ml = self.menu_l.astype(dtype) @ fw
        mh = self.menu_h.astype(dtype) @ fw
        caches = {b: {} for b in (0, 1)}
        out = []
        minimum = None
        chosen_min = None
        negative = 0
        histogram_counts = None
        for im, (b, m) in enumerate((b, m) for b in (0, 1) for m in self.mask_ids):
            ns, dom = self.domains[b]
            bits = dict(zip(LABELS, self.masks[m]))
            maxima = []
            choices = []
            histogram_counts = [len(dom.hist[3]), len(dom.hist[3]), len(dom.hist[4])]
            for tag in FAMILIES:
                ww = {NAMES[j]: weights[j] for j in self.family[tag] if weights[j] != 0}
                key, const, kap = dom.family_parts(tag, bits, ww)
                k, p, terms = key
                if key not in caches[b]:
                    scores = np.zeros(len(dom.hist[k]), dtype=dtype)
                    for feat, coeff in terms:
                        scores += coeff * dom.features[k, p][feat].astype(dtype)
                    vals, pick = [], []
                    for ids in dom.ids[k]:
                        ix = int(ids[int(np.argmax(scores[ids]))])
                        vals.append(scores[ix])
                        pick.append(ix)
                    caches[b][key] = (vals, pick)
                vals, pick = caches[b][key]
                maxima.append([v+const for v in vals])
                choices.append((k, pick))
            for d in range(6):
                r = im*6+d
                assert self.contexts[r] == (b, m, d)
                menu_choice, extra = [], 0
                corners = [(0, 0), (d, d), (5-d, 0), (5, d)]
                for f in range(3):
                    candidates = [ell*ml[r, f] + h*mh[r, f] for ell, h in corners]
                    ii = max(range(4), key=candidates.__getitem__)
                    extra += candidates[ii]
                    menu_choice.append(corners[ii])
                residual = int(self.t_sc[r])*D + 120*eps*int(self.exclusive[r]) - base[r] - extra - sum(a[d] for a in maxima)
                if exact:
                    assert F(residual).denominator == 1, ('noninteger exact residual', residual)
                residual = F(int(residual), 120*D) if exact else float(residual)/120
                w = {'background': b, 'bits': f'{m:010b}', 'd': d, 'menus': menu_choice,
                     'histograms': {tag: list(dom.hist[k][ch[d]]) for tag, (k, ch) in zip(FAMILIES, choices)}}
                item = {'residual': str(residual) if exact else residual, 'witness': w}
                if minimum is None or residual < minimum:
                    minimum, chosen_min = residual, item
                if residual < 0:
                    negative += 1
                if return_all or residual < 0:
                    out.append(item)
            if progress and im % 256 == 0:
                progress({'phase': 'exact separation' if exact else 'numeric separation', 'mask_contexts': im,
                          'minimum': str(minimum), 'cache_contexts': sum(map(len, caches.values()))})
        return {'complete_domain': self.complete, 'conditional_cases': len(self.contexts),
                'histograms_per_family': histogram_counts, 'menu_corners_per_family': 4,
                'cache_contexts': sum(map(len, caches.values())), 'minimum': str(minimum) if exact else minimum,
                'negative_conditional_cases': negative, 'worst': chosen_min, 'rows': out,
                'exact_integer_common_denominator': str(D) if exact else None}


def verify_upper(certificate, oracle, progress=None):
    x = [F(certificate['normalized_multipliers'][n]) for n in NAMES]
    eps = F(certificate['epsilon'])
    assert all(v >= 0 for v in x) and eps >= 0
    _, k = literal_vector(seeds()[0])
    ksum = sum(a*b for a, b in zip(x, k))
    assert ksum <= 0, ('positive K coefficient', str(ksum))
    result = oracle.separate(x, eps, exact=True, progress=progress)
    result['K_residual'] = str(-ksum)
    result['epsilon'] = str(eps)
    result['all_outer_multipliers_nonnegative'] = True
    result['status'] = 'UNIVERSAL-CONE-CERTIFICATE' if result['complete_domain'] and F(result['minimum']) >= 0 else 'NOT-VERIFIED'
    return result


def verify_lower(certificate):
    """A finite exact dual suffices for a lower bound on this WHOLE cone.

    The atoms need not be SPE-realizable. They obstruct this deliberately
    enlarged coefficient-domain proof system, not the game conjecture.
    """
    mass = [F(r['mass']) for r in certificate['atoms']]
    K = F(certificate['capacity_mass'])
    assert all(v >= 0 for v in mass) and K >= 0
    rows = [literal_vector(r['witness']) for r in certificate['atoms']]
    k = rows[0][1] if rows else literal_vector(seeds()[0])[1]
    assert all(kk == k for _, kk in rows)
    E = sum(v*exclusive(r['witness']) for v, r in zip(mass, certificate['atoms']))
    assert E <= 1
    slack = [sum(v*a[j] for v, (a, _) in zip(mass, rows)) + K*k[j] for j in range(len(NAMES))]
    assert all(v >= 0 for v in slack), ('negative cone-row value', [(NAMES[j], str(v)) for j, v in enumerate(slack) if v < 0])
    value = -sum(v*target(r['witness']) for v, r in zip(mass, certificate['atoms']))
    assert value == F(certificate['lower_bound'])
    return {'status': 'EXACT-CONE-LOWER-BOUND', 'lower_bound': str(value), 'exclusive_mass': str(E),
            'capacity_mass': str(K), 'positive_atoms': sum(v > 0 for v in mass),
            'row_slacks': {n: str(v) for n, v in zip(NAMES, slack)},
            'not_an_SPE_counterexample': True}
