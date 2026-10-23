"""Exact audit of the terminal-menu slack family; standard library only."""
from fractions import Fraction as F


def region(c, a, m):
    if a == 0 and 0 <= c < m - 2:
        return "root_C"
    if c == m - 2 and a in (0, 1):
        return "tail_A"
    if 0 <= c <= m - 3 and 1 <= a <= 3 and c + a < m:
        return "punish_C" if c < m - 3 else "punish_A"
    return None


def terminal_counts(c, a, m):
    while c + a < m:
        r = region(c, a, m)
        assert r is not None, (m, c, a)
        if r.endswith("C"):
            c += 1
        else:
            a += 1
    return c, a


def audit(m):
    nodes = 0
    for c in range(m):
        for a in range(m - c):
            r = region(c, a, m)
            if r is None:
                continue
            nodes += 1
            C, A = terminal_counts(c, a, m)
            if r.endswith("C"):
                payoff = F(m - 2, C)
                # Deviating to A either remains in the prescribed region,
                # or already gives four A users, an unconditional 3/4 cap.
                if region(c, a + 1, m) is not None:
                    _, Adev = terminal_counts(c, a + 1, m)
                    bound_A = F(3, Adev)
                elif c + a + 1 == m:
                    bound_A = F(3, a + 1)
                else:
                    assert a == 3
                    bound_A = F(3, a + 1)
                assert payoff >= bound_A
                assert payoff >= 1  # Any singleton deviation has payoff <= 1.
            else:
                payoff = F(3, A)
                bound_C = F(m - 2, c + 1)
                assert payoff >= bound_C
                assert payoff >= 1
    assert terminal_counts(0, 0, m) == (m - 2, 2)
    W, O = m + 1, 2 * m - 1
    S = F(3 * m, 2) - F(m - 2, m - 1) - F(3, 2) - (m - 2)
    assert S == F(m - 1, 2) + F(1, m - 1)
    assert 2 * W - O == 3
    assert (S > 3) == (m >= 7)
    assert F(3, S) == F(6 * (m - 1), (m - 1) ** 2 + 2)
    # The last best reply to each menu action is uniquely A.
    assert F(3, 2) > 1
    assert F(3, 2) > F(m - 2, m - 1)
    return nodes


if __name__ == "__main__":
    total = sum(audit(m) for m in range(4, 201))
    print({"m_range": [4, 200], "prescribed_count_states": total,
           "exact_checks": "passed", "unbounded_proof": "terminal_menu.md"})
