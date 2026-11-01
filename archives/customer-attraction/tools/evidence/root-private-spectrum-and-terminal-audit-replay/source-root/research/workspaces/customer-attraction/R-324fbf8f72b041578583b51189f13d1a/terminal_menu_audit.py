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
    # All terminal-row weights may be changed.  Nevertheless every unit of
    # negative singleton coefficient costs at least 1/2 actual row slack.
    topics = ["C", "A"] + list(range(m - 2))
    for X in topics:
        actual_last = F(3, 1 + (X == "A"))
        for query in topics:
            if query == "A":
                queried = actual_last
                negative_singleton = F(0)
            elif query == "C":
                queried = F(m - 2, m - 1 + (X == "C"))
                negative_singleton = F(0)
            else:
                queried = F(1, 1 + (X == query))
                negative_singleton = queried
            slack = actual_last - queried
            assert slack >= negative_singleton / 2
    # Adding every actual-prefix safe bound also has singleton slack cost
    # at least 1/2 per unit of negative coefficient.
    for i in range(1, m + 1):
        remaining = m - i + 1
        actual_payoff = F(1) if i <= m - 2 else F(3, 2)
        negative_singleton = F(1, remaining)
        assert actual_payoff - negative_singleton >= negative_singleton / 2
    return nodes


def audit_q(m, q):
    """Independently parameterized prescribed-strategy and row-cost checks."""
    assert 2 <= q <= m - 2
    Csize, Asize = m - q, q + 1

    def which(c, a):
        if a == 0 and 0 <= c < Csize:
            return "root_C"
        if c == Csize and 0 <= a < q:
            return "tail_A"
        if 0 <= c <= Csize - 1 and 1 <= a <= q + 1 and c + a < m:
            return "punish_C" if c < Csize - 1 else "punish_A"
        return None

    def finish(c, a):
        while c + a < m:
            r = which(c, a)
            assert r is not None
            if r.endswith("C"):
                c += 1
            else:
                a += 1
        return c, a

    nodes = 0
    for c in range(m):
        for a in range(m - c):
            r = which(c, a)
            if r is None:
                continue
            nodes += 1
            C, A = finish(c, a)
            if r.endswith("C"):
                payoff = F(Csize, C)
                if which(c, a + 1) is not None:
                    _, Adev = finish(c, a + 1)
                    alternative = F(Asize, Adev)
                else:
                    alternative = F(Asize, a + 1)
                assert payoff >= alternative
                assert payoff >= 1
            else:
                payoff = F(Asize, A)
                assert payoff >= F(Csize, c + 1)
                assert payoff >= 1
    assert finish(0, 0) == (Csize, q)
    ua = F(Asize, q)
    S = m * ua - ua - (m - 2) - F(Csize, Csize + 1)
    assert S == F(m - 1, q) + F(1, Csize + 1)
    for X_is_A, X_is_singleton in ((True, False), (False, True), (False, False)):
        actual_last = F(Asize, q if X_is_A else q - 1)
        singleton_query = F(1, 2 if X_is_singleton else 1)
        assert actual_last - singleton_query >= singleton_query / q
    for i in range(1, m + 1):
        remaining = m - i + 1
        payoff = F(1) if i <= Csize else ua
        assert remaining * payoff - 1 >= F(1, q)
    # Exact coefficient and slack decomposition from genuine early queries.
    assert F(Csize, Csize) == 1
    A_coefficient = F(q - 2, q)
    A_remainder = F(2, q)
    assert A_coefficient + A_remainder == 1
    assert A_coefficient >= 0 and A_remainder >= 0
    assert F(q - 2, q) + Asize * A_remainder == 3
    return nodes


if __name__ == "__main__":
    total = sum(audit(m) for m in range(4, 201))
    pairs = [(m, q) for m in range(4, 41) for q in range(2, m - 1)]
    parameter_nodes = sum(audit_q(m, q) for m, q in pairs)
    print({"m_range": [4, 200], "prescribed_count_states": total,
           "parameter_q_pairs": len(pairs), "parameter_count_states": parameter_nodes,
           "exact_checks": "passed", "unbounded_proof": "terminal_menu.md"})
