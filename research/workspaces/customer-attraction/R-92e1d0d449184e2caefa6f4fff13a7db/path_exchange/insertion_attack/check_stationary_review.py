"""Independent exact scalar audit; does not import either author's check code."""
from fractions import Fraction as F


def delta(i, k, n, b):
    if i == k == 0:
        return F(0)
    return F(n * i - k, n * (b + i + k))


def run():
    cases = 0
    for r in range(2, 31):
        n = r - 1
        c = n * n // 4
        for b in range(13):
            pairs = []
            ratio_pairs = []
            for a in range(1, n + 1):
                for t in range(1, n + 1):
                    wi, wo = F(t, a + t), F(a, a + t)
                    d = wi * F(1, b + r - a)
                    tail = (wi * F(n - a, b + r - a)
                            + wo * F(t, b + t))
                    value = wi * delta(1, n - a, n, b) + wo * delta(0, t, n, b)
                    explicit = F(a * t * (a + t - r),
                                 n * (a + t) * (b + r - a) * (b + t))
                    assert value == explicit
                    assert tail / d == n + F(a * (r - a - t), b + t)
                    pairs.append(value)
                    ratio_pairs.append(tail / d)
            loss = max([F(0)] + [F(a * t * (r - a - t),
                                           n * (a + t) * (b + r - a) * (b + t))
                                     for a in range(1, n + 1)
                                     for t in range(1, n + 1) if a + t <= n])
            assert min([F(0)] + pairs) == -loss
            assert max([F(n)] + ratio_pairs) == n + F(c, b + 1)
            if b == 0:
                dmax = (r + 1) ** 2 // 4
                assert loss == F(1, n) * (1 - F(r, dmax))
            # Check each finite difference in K, including the 0/0 convention.
            for i in (0, 1):
                for k in range(n):
                    assert delta(i, k, n, b) >= delta(i, k + 1, n, b)
            # Independently build the four columns and test stationarity.
            for a in range(1, n + 1):
                t = 1
                pi = [F(t, 2 * (a + t))] * 2 + [F(a, 2 * (a + t))] * 2
                columns = [
                    [0, n - a, a, 0], [n - a, 0, 0, a],
                    [t, 0, 0, n - t], [0, t, n - t, 0],
                ]
                for j in range(4):
                    assert columns[j][j] == 0
                    assert sum(columns[j]) == n
                    assert sum(pi[i] * columns[i][j] for i in range(4)) == n * pi[j]
            cases += 1
    return {"cases": cases, "r_range": [2, 30], "b_range": [0, 12],
            "pair_formula": True, "additive_sharp": True, "multiplicative_sharp": True,
            "zero_conventions": True, "four_label_stationarity": True}


if __name__ == "__main__":
    print(run())
