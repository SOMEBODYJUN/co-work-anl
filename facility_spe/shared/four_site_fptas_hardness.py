"""Four-site PARTITION gap constructor; this is not an equilibrium solver.

The output uses the canonical two-facility instance format. All clients have
positive binary integer weights, and both facilities have the same catalog.
The proof is research/current/shared/four_site_no_fptas.md.
"""
from fractions import Fraction as F


def parameters(values):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("PARTITION needs a nonempty list of positive integers")
    if any(type(x) is not int or x <= 0 for x in values):
        raise ValueError("PARTITION entries must be strictly positive integers")
    n = 2 * max(len(values), 2)
    total = sum(values)
    a = list(values) + [0] * (n - len(values))
    alpha = F(13, 10)
    macro = F(5 * n, 2)
    tau = F(1, 2 * n)
    cross = alpha * tau
    served = F(11 * n, 2)
    reach_a = alpha * (served + tau) / 2
    variables = [1 + F(n * x - total, 16 * n * n * total) for x in a]
    return dict(n=n, total=total, a=a, alpha=alpha, M=macro, tau=tau,
                q=cross, V=served, R=reach_a, d=F(27 * n, 10),
                variables=variables, scale=80 * n * n * total)


def reduction(values):
    """Return the integer instance in time polynomial in the source bit length.

    Location indices 0,1,2,3 mean B,C,A,D; client zero is the macro, clients
    1..n are the variable clients, followed by cross,B-private,C-private,
    A-private,D-private. No subset search is performed.
    """
    p = parameters(values)
    n, total = p["n"], p["total"]
    weights = [200 * n**3 * total]
    weights += [80 * n**2 * total + 5 * n * x - 5 * total for x in p["a"]]
    weights += [52 * n * total, 80 * n**3 * total - 52 * n * total,
                80 * n**3 * total, 86 * n**3 * total - 26 * n * total,
                16 * n**3 * total]
    menus = [[0, 1, 2, 3]] + [[0, 1] for _ in range(n)]
    menus += [[0, 2], [0], [1], [2], [3]]
    locations = [[i for i, menu in enumerate(menus) if s in menu]
                 for s in range(4)]
    return dict(weights=weights, locations=locations,
                U1=list(range(4)), U2=list(range(4)))
