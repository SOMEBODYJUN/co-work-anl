"""Independent checker: imports no construction or equilibrium-solving module."""
from fractions import Fraction
from itertools import product


def check_ne(instance, layout, probabilities):
    n, k = len(instance['clients']), instance['k']
    assert len(layout) == k and all(0 <= s < instance['m'] for s in layout)
    assert len(probabilities) == n
    w = [Fraction(c['weight']) for c in instance['clients']]
    p = [[Fraction(x) for x in row] for row in probabilities]
    for i, c in enumerate(instance['clients']):
        assert len(p[i]) == k
        accessible = [f for f in range(k) if layout[f] in c['sites']]
        assert all(x >= 0 for x in p[i])
        assert all(p[i][f] == 0 for f in range(k) if f not in accessible)
        assert sum(p[i]) == (1 if accessible else 0)
        if accessible:
            costs = {f: w[i] + sum(w[j] * p[j][f] for j in range(n) if j != i)
                     for f in accessible}
            minimum = min(costs.values())
            assert all(costs[f] == minimum for f in accessible if p[i][f] > 0)
    return [sum(w[i] * p[i][f] for i in range(n)) for f in range(k)]


def from_pure(assignment, k):
    return [[int(g == f) for f in range(k)] for g in assignment]


def brute_pure_equilibria(instance, layout):
    """Independent complete enumeration, only for small regression instances."""
    options = [[f for f, s in enumerate(layout) if s in c['sites']] or [-1]
               for c in instance['clients']]
    result = []
    for assignment in product(*options):
        p = from_pure(assignment, instance['k'])
        try:
            L = check_ne(instance, layout, p)
        except AssertionError:
            continue
        result.append((assignment, L))
    assert result, "Every fixed layout has a pure NE"
    return result


def check_certificate(cert, all_layouts=False):
    instance = cert['instance']
    k, m = instance['k'], instance['m']
    layout = tuple(cert['on_path']['layout'])
    base = check_ne(instance, layout, cert['on_path']['probabilities'])
    expected = {(f, r) for f in range(k) for r in range(m) if r != layout[f]}
    actual = {(d['facility'], d['site']) for d in cert['deviations']}
    assert actual == expected and len(cert['deviations']) == len(expected)
    used_layouts = {layout}
    alpha = Fraction(cert['factor'])
    ratios = [Fraction(1)]
    for d in cert['deviations']:
        f, r = d['facility'], d['site']
        modified = list(layout)
        modified[f] = r
        modified = tuple(modified)
        assert modified not in used_layouts
        used_layouts.add(modified)
        L = check_ne(instance, modified, from_pure(d['pure_assignment'], k))
        assert L[f] <= alpha * base[f]
        if base[f]:
            ratios.append(L[f] / base[f])
    defaults_checked = 0
    if all_layouts:
        # Independently verifies that every unlisted labeled subgame can be
        # completed, by brute force rather than the constructor's dynamics.
        for other in product(range(m), repeat=k):
            if other not in used_layouts:
                brute_pure_equilibria(instance, other)
                defaults_checked += 1
    assert cert['default_rule'] == 'least-index initial pure assignment, then strict pure best responses'
    return dict(actual_certificate_factor=str(max(ratios)),
                actual_deviations_checked=len(expected),
                unlisted_labeled_layouts_checked=defaults_checked)


def independent_lexmax(instance):
    """All labeled layouts, direct materialization of uniform probabilities."""
    k, m = instance['k'], instance['m']
    w = [Fraction(c['weight']) for c in instance['clients']]
    best = None
    for layout in product(range(m), repeat=k):
        available = set(layout)
        options = [sorted(set(c['sites']) & available) or [-1]
                   for c in instance['clients']]
        for assignment in product(*options):
            values = []
            for f, s in enumerate(layout):
                values.append(sum(w[i] for i, t in enumerate(assignment) if t == s)
                              / layout.count(s))
            key = tuple(sorted(values))
            if best is None or key > best:
                best = key
    return best
