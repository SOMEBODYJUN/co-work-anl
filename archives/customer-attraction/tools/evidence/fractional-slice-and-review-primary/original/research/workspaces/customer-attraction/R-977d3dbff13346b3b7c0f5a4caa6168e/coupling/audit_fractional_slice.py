"""Independent Fraction diagnostics, not a proof of the general claims.

Uses literal Boolean inversion and ordered-history terminal payoffs. The
Johnson eigenvalue checks are kept separate from the direct array checks.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def falling(x, k):
    out = F(1)
    for j in range(k):
        out *= x-j
    return out


def gb(x, k):
    out = F(1)
    for j in range(k):
        out *= F(x-j, j+1)
    return out


def direct_array(m):
    n, r = 2*m+2, F(2*m+1, 2)
    moments = [falling(r, k)/falling(n, k) for k in range(n+1)]
    weights_by_size = [sum(((-1)**(j-k)*comb(n-k, j-k)*moments[j]
                            for j in range(k, n+1)), F())
                       for k in range(n+1)]
    weights = [weights_by_size[b.bit_count()] for b in range(1 << n)]
    assert sum(weights) == 1
    for s in range(1 << n):
        assert sum((w for b, w in enumerate(weights) if b & s == s), F()) == moments[s.bit_count()]
    # Exchangeability lets one representative check every disjoint pattern.
    smallest_local = None
    for s in range(m+1):
        for t in range(m-s+1):
            ones, zeros = (1 << s)-1, ((1 << t)-1) << s
            value = sum((w for b, w in enumerate(weights)
                         if b & ones == ones and not b & zeros), F())
            formula = falling(r, s)*falling(n-r, t)/falling(n, s+t)
            assert value == formula and value > 0
            smallest_local = value if smallest_local is None else min(smallest_local, value)
    integer_value = sum((w*(b.bit_count()-m)*(b.bit_count()-m-1)
                         for b, w in enumerate(weights)), F())
    assert integer_value == -F(1, 4)
    assert sum((w for w in weights if w < 0), F()) < 0
    # Literal homogeneous d-subset matrix and an explicit harmonic vector.
    eigen_checks = 0
    for d in range(m//2+1):
        ds = [sum(1 << j for j in s) for s in combinations(range(n), d)]
        for j in range(d+1):
            # Coefficients of product_{k<j}(x_{2k}-x_{2k+1}).
            coeffs = {sum(1 << (2*k+bit) for k, bit in enumerate(bits)):
                      F((-1)**sum(bits))
                      for bits in product(range(2), repeat=j)}
            v = [sum((c for s, c in coeffs.items() if s & mask == s), F()) for mask in ds]
            lam = gb(r-j, d-j)*falling(r, d)*falling(n-r, j)/falling(n, d+j)
            assert lam > 0
            for a, va in zip(ds, v):
                assert sum((moments[(a | b).bit_count()]*vb
                            for b, vb in zip(ds, v)), F()) == lam*va
            eigen_checks += 1
    out = dict(m=m, n_satellites=n, signed_types=len(weights),
               negative_types=sum(w < 0 for w in weights),
               minimum_local_pattern=str(smallest_local),
               literal_integer_row=str(integer_value),
               literal_harmonic_eigen_checks=eigen_checks)
    if m <= 3:
        # Anchor is label n; all satellite bits are stored in b.
        anchor, p = n, n+1
        def utility(terminal, action):
            return sum((w/F(sum(a == anchor or bool(b >> a & 1) for a in terminal))
                        for b, w in enumerate(weights)
                        if action == anchor or b >> action & 1), F())
        comparisons, minimum = 0, None
        for depth in range(m):
            for history in product(range(p), repeat=depth):
                chosen = history+(anchor,)*(m-depth)
                actual = utility(chosen, anchor)
                for action in range(p):
                    dev = history+(action,)+(anchor,)*(m-depth-1)
                    slack = actual-utility(dev, action)
                    assert slack >= 0
                    minimum = slack if minimum is None else min(minimum, slack)
                    comparisons += 1
        out.update(ordered_history_comparisons=comparisons,
                   minimum_comparison_slack=str(minimum))
    return out


def conditional_square_parameters(m):
    n, r = 2*m+2, F(2*m+1, 2)
    checks = 0
    smallest = None
    for s in range(m+1):
        for t in range(m-s+1):
            N, rho = n-s-t, r-s
            pattern = falling(r, s)*falling(n-r, t)/falling(n, s+t)
            assert pattern > 0
            for d in range((m-s-t)//2+1):
                assert N >= 2*d and rho > d-1 and N-rho > d-1
                for j in range(d+1):
                    lam = gb(rho-j, d-j)*falling(rho, d)*falling(N-rho, j)/falling(N, d+j)
                    assert lam > 0
                    smallest = lam if smallest is None else min(smallest, lam)
                    checks += 1
    return dict(m=m, conditional_homogeneous_eigenvalues=checks,
                minimum_eigenvalue=str(smallest))


def main():
    report = {
        'status': 'finite exact diagnostics; general claims rely on accompanying proof',
        'not_a_half_obstruction': True,
        'root_W_and_OPT': '1',
        'literal_signed_arrays': [direct_array(m) for m in range(2, 5)],
        'conditional_square_parameter_checks': [conditional_square_parameters(m) for m in range(2, 13)]
    }
    output = Path(__file__).with_name('fractional_slice_audit.json')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
