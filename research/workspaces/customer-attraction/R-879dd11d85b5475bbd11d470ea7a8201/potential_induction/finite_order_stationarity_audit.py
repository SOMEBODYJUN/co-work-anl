"""Exact checks of formulas; does not solve or certify an SPE."""
from fractions import Fraction as F
from math import comb, factorial, prod


def fall(n, k):
    return prod(range(n - k + 1, n + 1)) if k else 1


def distribution(m, d):
    data = []
    for c in range(1, d + 2):
        z = (-1) ** c * comb(d, c - 1)
        i = int(z > 0)
        a = m - c if i else c
        data.append((c, i, z, F(abs(z), a)))
    k = 1 / sum(row[3] for row in data)
    return k, [(c, i, z, k * p) for c, i, z, p in data]


def verify(m, d, b):
    k, rows = distribution(m, d)
    assert sum(p for c, i, z, p in rows) == 1
    for j in range(1, d + 1):
        h = sum(p * i * F(fall(c - i, j - 1), fall(m - 1, j - 1))
                for c, i, z, p in rows)
        g = sum(p * F(fall(c - i, j), fall(m - 1, j))
                for c, i, z, p in rows)
        assert h == g
    root = sum(p * F(i, b + c) for c, i, z, p in rows)
    tail = sum(p * F(c - i, (m - 1) * (b + c)) for c, i, z, p in rows)
    expected = -k * F(factorial(d), (m - 1) * prod(range(b + 1, b + d + 2)))
    assert root - tail == expected < 0
    return root, tail, expected


def concrete_menu():
    # Three (C=1,I=0), three (C=2,I=1), one (C=3,I=0).
    bits = [0, 0, 0, 1, 1, 1, 0]
    q = [1, 1, 1, 1, 1, 1, 3]
    # Each target appears in precisely three slots. Sources have stated Q.
    one_stubs = [3, 3, 3, 4, 4, 4, 5, 5, 5]
    zero_stubs = [0, 0, 0, 1, 1, 1, 2, 2, 2, 6, 6, 6]
    menu = []
    for n in q:
        menu.append(one_stubs[:n] + zero_stubs[:3-n])
        del one_stubs[:n]
        del zero_stubs[:3-n]
    assert not one_stubs and not zero_stubs
    counts = [sum(row.count(v) for row in menu) for v in range(7)]
    assert counts == [3] * 7
    profiles = [[v] + row for v, row in enumerate(menu)]
    assert [sum(bits[v] for v in row) for row in profiles] == [1, 1, 1, 2, 2, 2, 3]
    root = sum(F(bits[v], sum(bits[w] for w in profiles[v])) for v in range(7)) / 7
    tail = sum(F(sum(bits[w] for w in row[1:]), 3 * sum(bits[w] for w in row))
               for row in profiles) / 7
    assert (root, tail, root-tail) == (F(3, 14), F(11, 42), F(-1, 21))
    return menu


if __name__ == "__main__":
    checks = 0
    for d in range(1, 13):
        for m in (d + 2, d + 3, d + 7):
            for b in (0, 1, 3, 17):
                verify(m, d, b)
                checks += 1
    print(f"Exact parameter checks: {checks}")
    print("m=4,d=2,b=0:", verify(4, 2, 0))
    print("Concrete stationary menu:", concrete_menu())
    print("No SPE claim; general proof uses finite differences, not finite checks.")
