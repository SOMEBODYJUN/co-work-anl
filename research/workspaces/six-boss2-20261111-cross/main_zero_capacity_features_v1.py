"""Main's independent direct alpha/beta evaluator for frozen packs 2 and 13.

Prefix costs are compiled from the original 76-row formulas. Tail values come
from all four rational two-state policies, without the discovering closed forms.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib, json
from main_pair_features import terms, pay

PACKAGE = Path(__file__).resolve().parent / 'coverage_bridge/selected_prefix_tail_5752.json'
assert hashlib.sha256(PACKAGE.read_bytes()).hexdigest() == '595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50'
data = json.loads(PACKAGE.read_text())
SCALES = {2: 999, 13: 10000}
PARAMS = {}
HIDDEN = tuple(product((0, 1), repeat=4))
for number, scale in SCALES.items():
    rec = data['cuts'][number - 1]
    assert rec['source'] == 4 and rec['k'] == 3 and F(rec['delta']) == F(1, 2)
    alpha = {name: scale * F(w) for name, w in rec['alpha'].items()}
    beta = {name: scale * F(w) for name, w in rec['beta'].items()}
    assert all(w.denominator == 1 and w >= 0 for w in list(alpha.values()) + list(beta.values()))
    assert all(not name.startswith('cap:') for name in alpha)
    assert not beta.get('beta_mid', 0) and not beta.get('beta_last', 0) and not beta.get('mu_current', 0)
    PARAMS[number] = (alpha, beta)


@lru_cache(None)
def prefix_affine(number, p, D, t, hidden):
    alpha, beta = PARAMS[number]
    e0, budget = terms(p, D - 1, t, 0, *hidden, k=3)
    e1, _ = terms(p, D - 1, t, 1, *hidden, k=3)
    constant, coefs = F(0), {}
    for name, weight in alpha.items():
        if '@' not in name:
            constant += weight * e0[name]
        else:
            feature, query = name.split('@')
            constant += weight * e0[feature]
            coefs[query] = coefs.get(query, F(0)) + weight * (e1[feature] - e0[feature])
    return constant, tuple(coefs.items())


def policy_minima(edges, theta=F(1, 2)):
    candidates = ([], [])
    for action0, action1 in product((0, 1), repeat=2):
        a, b = 1 - theta * (action0 == 0), -theta * (action0 == 1)
        c, d = -theta * (action1 == 0), 1 - theta * (action1 == 1)
        det = a * d - b * c
        candidates[0].append((d * edges[0, action0] - b * edges[1, action1]) / det)
        candidates[1].append((a * edges[1, action1] - c * edges[0, action0]) / det)
    values = tuple(min(v) for v in candidates)
    assert all(values[t] == min(edges[t, c] + theta * values[c] for c in (0, 1)) for t in (0, 1))
    return tuple((1 - theta) * v for v in values)


@lru_cache(None)
def tail(number, p, D, q):
    alpha, beta = PARAMS[number]
    a = beta['source']
    total_query_weight = sum(w for name, w in beta.items() if name.startswith('mu_'))
    m, last = beta['alpha_mid'], beta['alpha_last']
    edges = {}
    for t, c in product((0, 1), repeat=2):
        edges[t, c] = min(pay(a * t - total_query_weight * c, p + t + s + c)
                          + m * F(s, D) + last * F(c, D) + q / (p + t + s + 1)
                          for s in (0, 1))
    return policy_minima(edges)


@lru_cache(None)
def L(number, p, D, t, x, y, ci, bj, a6, n):
    assert number in (2, 13) and 0 <= p <= 3 and p + 1 <= D <= p + 3
    assert all(v in (0, 1) for v in (t, x, y, ci, bj, a6)) and 0 <= n - x - y <= 4
    queries = {'Ti': F(x), 'Tj': F(y), 'Ci': F(ci), 'Bj': F(bj), 'A6': F(a6), 'other_T': F(n - x - y, 4)}
    alpha, beta = PARAMS[number]
    q = sum(w * queries[name[3:]] for name, w in beta.items() if name.startswith('mu_'))
    psi = tail(number, p, D, q)
    costs = []
    for hidden in HIDDEN:
        constant, coefs = prefix_affine(number, p, D, t, hidden)
        costs.append(constant + sum(coef * queries[name] for name, coef in coefs) + psi[hidden[3]])
    return min(costs)
