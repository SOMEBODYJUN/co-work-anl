"""Exact arithmetic regression for the independently reviewed menu factor."""

from fractions import Fraction as Q


def main():
    local_cases = 0
    menu_cases = 0
    for n in range(1, 81):
        for b in (Q(0), Q(1, 2), Q(1), Q(2), Q(7)):
            m = n * n // 4
            beta = n * (b + 1) / (n * (b + 1) + m)
            c = beta / (n * (b + 1))
            for q in range(n + 1):
                for a in (0, 1):
                    den = b + a + q
                    r = Q(a, 1) / den if a else Q(0)
                    f = Q(q, n) / den if q else Q(0)
                    residual = r - beta * f - c * (n * a - q)
                    assert residual >= 0
                    if a:
                        expected = beta * (m - q * (n - q)) / (
                            n * (b + 1) * (b + 1 + q)
                        )
                    elif q:
                        expected = beta * Q(q, n) * (1 / (b + 1) - 1 / (b + q))
                    else:
                        expected = Q(0)
                    assert residual == expected
                    local_cases += 1

                # N[j][i]: column i contains the successors of root i.
                mat = [[0] * 4 for _ in range(4)]
                mat[1][0], mat[2][0] = q, n - q
                mat[0][1], mat[3][1] = q, n - q
                mat[0][2], mat[3][2] = 1, n - 1
                mat[1][3], mat[2][3] = 1, n - 1
                assert all(mat[i][i] == 0 for i in range(4))
                assert all(sum(mat[j][i] for j in range(4)) == n for i in range(4))
                p = Q(1, n - q + 1)
                pi = (p / 2, p / 2, (1 - p) / 2, (1 - p) / 2)
                assert sum(pi) == 1
                for j in range(4):
                    assert sum(pi[i] * mat[j][i] for i in range(4)) == n * pi[j]
                loads = (q, q, 1, 1)
                assert all(loads[i] == sum(mat[j][i] for j in (0, 1)) for i in range(4))
                r = p / (b + 1 + q)
                f = (p * q / (b + 1 + q) + (1 - p) / (b + 1)) / n
                assert f > 0
                assert r / f == n * (b + 1) / (n * (b + 1) + q * (n - q))
                if q == n // 2:
                    assert r == beta * f
                menu_cases += 1
    print({"local_cases": local_cases, "four_root_menus": menu_cases, "status": "passed"})


if __name__ == "__main__":
    main()
