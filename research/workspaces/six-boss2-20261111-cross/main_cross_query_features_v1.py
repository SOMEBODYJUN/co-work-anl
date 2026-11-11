"""Main's exact feature evaluator; no discovering-agent imports.

Old-query products are formed by enumerating actual allowed index pairs.
An averaged query remains a list of catalog actions, never a new action.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from main_pair_features import pay, terms


def query_samples(actual, words, left, right, state):
    remaining = [i for i in range(6) if i not in {left, right}]
    samples = tuple((x,) for x in actual + words[left] + words[right] + state)
    samples += tuple(tuple(words[i][family] for i in remaining) for family in range(3))
    assert len(samples) == 17 and len(remaining) in (4, 5)
    means = tuple(sum(map(F, xs), F(0)) / len(xs) for xs in samples)
    moments = tuple(F(sum(words[i][f] * words[i][g] for i in remaining), len(remaining))
                    for f, g in ((0, 1), (0, 2), (1, 2)))
    return samples, means, moments


def literal_product(samples, name):
    kind, pair, mode = name.split(':')
    assert kind in ('oldpair1', 'oldpair2')
    a, b = map(int, pair.split(','))
    xs, ys = samples[a], samples[b]
    if mode == 'product':
        assert a < 14 and a < b
        pairs = tuple(product(xs, ys))
    else:
        assert a >= 14 and b >= a and len(xs) == len(ys)
        if mode == 'same':
            assert a < b
            pairs = tuple(zip(xs, ys))
        else:
            assert mode == 'off'
            pairs = tuple((x, y) for i, x in enumerate(xs) for j, y in enumerate(ys) if i != j)
    return F(sum(x * y for x, y in pairs), len(pairs))


def weighted_value(p, ell, t, qs, hidden, weights, products=()):
    b, c, j, v, s, ss = hidden
    variables = dict(t=F(t), b=F(b), c=F(c), j=F(j), v=F(v), s=F(s), ss=F(ss))
    variables.update({f'q{i}': q for i, q in enumerate(qs)})
    bg1, bg2 = p + t + s, p + c + ss
    z1, z2 = bg1 + b + c, bg2 + j + v
    answer = F(0)
    for name, weight in weights:
        if name == 'sourceT':
            value = pay(t, z1)
        elif name == 'sourceC':
            value = pay(c, z2)
        else:
            kind, label = name.split(':', 1)
            if kind == 'price': value = variables[label] / (ell + 1)
            elif kind == 'cap': value = variables[label]
            elif kind == 'last1': value = variables[label] / (bg1 + b + 1) - pay(c, z1)
            elif kind == 'last2': value = variables[label] / (bg2 + j + 1) - pay(v, z2)
            elif kind == 'safeB': value = variables[label] / (bg1 + 2) - pay(b, z1)
            elif kind == 'safeJ': value = variables[label] / (bg2 + 2) - pay(j, z2)
            elif kind.startswith('oldpair'):
                pair, mode = label.split(':')
                a, d = map(int, pair.split(','))
                beta, first, last, z = (bg1, b, c, z1) if kind == 'oldpair1' else (bg2, j, v, z2)
                value = (qs[a] + qs[d]) / (beta + 1) - (dict(products)[name] + first) / ((beta + 1) * (beta + 2)) - pay(first + last, z)
            elif kind in ('pair1', 'pair2'):
                a, d = label.split(',')
                assert a == d or not (a.startswith('q') and d.startswith('q'))
                overlap = variables[a] if a == d else variables[a] * variables[d]
                beta, first, last, z = (bg1, b, c, z1) if kind == 'pair1' else (bg2, j, v, z2)
                value = (variables[a] + variables[d]) / (beta + 1) - (overlap + first) / ((beta + 1) * (beta + 2)) - pay(first + last, z)
            else: raise AssertionError(name)
        answer += weight * value
    return answer


def projection(weights, k):
    weights = tuple(weights.items())
    hidden = tuple((b, c, j, v, s, ss) for b, c, j, v in product((0, 1), repeat=4)
                   for s in range(k - 2) for ss in range(k - 2))
    @lru_cache(None)
    def minimum(p, ell, t, qs, products=()):
        return min(weighted_value(p, ell, t, qs, h, weights, products) for h in hidden)
    return minimum


def all_332(p, ell, t, qs, hidden, k):
    """Construct 60 common rows and 17*16 query rows from independent 76-row formulas."""
    result, budget = {}, {}
    for qi, q in enumerate(qs):
        ev, cost = terms(p, ell, t, q, *hidden, k=k)
        for name, value in ev.items():
            label = name.split(':')[-1]
            if 'q' not in label:
                if qi == 0: result[name], budget[name] = value, cost[name]
                else: assert result[name] == value
                continue
            kind = name.split(':')[0]
            if kind.startswith('pair'):
                labels = label.split(',')
                other = labels[1] if labels[0] == 'q' else labels[0]
                new_name = kind + ':' + f'q{qi},' + (f'q{qi}' if other == 'q' else other)
            else:
                new_name = kind + ':' + f'q{qi}'
            assert new_name not in result
            result[new_name], budget[new_name] = value, cost[name]
    assert len(result) == len(budget) == 332
    return result, budget
