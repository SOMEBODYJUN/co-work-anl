from fractions import Fraction as Q


def path_budget(k, heavy_first):
    small = (Q(1, k**4), Q(1, k**2))
    items = [small] * k**3
    items = ([(Q(1), Q(1))] + items
             if heavy_first else items + [(Q(1), Q(1))])
    load, budget = Q(0), Q(0)
    for weight, multiplier in items:
        load += weight
        budget += multiplier * load
    return budget


def two_type_potential(m, n, eps, q, s):
    d, y = q / eps, eps * n
    if m >= s * y:
        continuous = (m*m + 2*d*m*y + d*y*y) / 2
    else:
        continuous = (s*m*m + 2*s*m*y + s*d*y*y) / 2
    return continuous + (m + q*eps*n) / 2


for k in (2, 3, 4, 8, 16):
    diagonal = Q(3, 2) + Q(1, 2*k**3)
    low, high = diagonal + Q(1, k), diagonal + k
    assert path_budget(k, False) == low
    assert path_budget(k, True) == high
    assert high / low >= Q(k, 3)
    print(k, k**3, low, high, high / low)

edges = 0
for k in (2, 3, 4, 8):
    eps, q, s = Q(1, k**4), Q(1, k**2), Q(k)
    for m in range(9):
        for n in range(2*k**3 + 4):
            phi = two_type_potential(m, n, eps, q, s)
            heavy_delta = two_type_potential(m+1, n, eps, q, s) - phi
            small_delta = two_type_potential(m, n+1, eps, q, s) - phi
            heavy_cost = m + 1 + eps*n
            small_cost = q * (m + eps*(n+1))
            assert heavy_cost <= heavy_delta <= s*heavy_cost
            assert small_cost <= small_delta <= s*small_cost
            edges += 2
    for M in (1, 10, 100, 1000):
        N = M * k**3
        diagonal = Q(M*(M+1), 2) + q*eps*Q(N*(N+1), 2)
        low = diagonal + M*N*eps
        high = diagonal + M*N*q
        assert high / low < s
    print("fixed pair", k, "last dense ratio", high / low)
assert edges == 22284
print("piecewise potential edges:", edges)

weights = (Q(1, 9), Q(2, 3), Q(5, 2), Q(7, 4))
slope, intercept = Q(3, 7), Q(5, 11)


def exact_affine_potential(users):
    load = sum((weights[i] for i in users), Q(0))
    squares = sum((weights[i]**2 for i in users), Q(0))
    return slope * (load*load + squares) / 2 + intercept*load


edges = 0
for mask in range(1 << len(weights)):
    users = {i for i in range(len(weights)) if mask >> i & 1}
    for i, weight in enumerate(weights):
        if i in users:
            continue
        final_load = sum((weights[j] for j in users), Q(0)) + weight
        delta = exact_affine_potential(users | {i}) - exact_affine_potential(users)
        assert delta == weight * (slope*final_load + intercept)
        edges += 1
assert edges == 32
print("exact affine edges:", edges)
