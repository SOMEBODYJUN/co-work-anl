"""Exact certificate: aggregate decorrelation fails; BR is NOT refuted."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

WEIGHTS = {
    5: 16, 10: 1, 11: 11, 15: 8, 22: 1, 23: 2,
    24: 2, 26: 1, 33: 1, 35: 5, 40: 4, 46: 2,
    52: 1, 53: 4, 54: 14, 56: 2, 61: 10, 62: 4,
}
POLICY = (
    "222500222522222020250000022020220000022020022522222322253323"
    "022222222322222022222322222020230000022020220000022020053323"
    "030000030000020000030000000000022222222020220000022020220000"
    "022020222322220000030000020000020000020000022022222020000000"
    "0220202200000200200"
)
PRIMARY = [
    F(z, 331825)
    for z in (44245, 49133, 120795, 77367, 0, 40285)
]
DUAL = {
    (0, 1, 2): F(1635, 13273),
    (0, 2, 2): F(5550, 13273),
    (0, 2, 3): F(3365, 13273),
    (0, 2, 5): F(1123, 13273),
    (2, 2, 3): F(1600, 13273),
}


def audit(m, n, weights, encoded):
    """Expand unit customers; check every ordered-history deviation."""
    assert m >= 1 and n >= 1
    assert all(
        0 < t < 2**m and isinstance(k, int) and k > 0
        for t, k in weights.items()
    )
    customers = tuple(
        t for t, k in weights.items() for _ in range(k)
    )
    topics = tuple(
        frozenset(
            x for x, t in enumerate(customers) if t >> a & 1
        )
        for a in range(m)
    )
    assert len(set(topics)) == m

    histories = [
        h
        for k in range(n)
        for h in product(range(m), repeat=k)
    ]
    assert len(encoded) == len(histories)
    policy = dict(zip(histories, map(int, encoded)))
    assert all(0 <= a < m for a in policy.values())

    @lru_cache(None)
    def terminal(h):
        if len(h) == n:
            return h
        return terminal(h + (policy[h],))

    @lru_cache(None)
    def utilities(z):
        loads = [
            sum(x in topics[a] for a in z)
            for x in range(len(customers))
        ]
        return tuple(
            sum((F(1, loads[x]) for x in topics[a]), F(0))
            for a in z
        )

    comparisons = 0
    for h in histories:
        i = len(h)
        current = utilities(terminal(h))[i]
        for a in range(m):
            deviated = utilities(terminal(h + (a,)))[i]
            assert current >= deviated, (h, a)
            comparisons += 1

    def f(a, rivals):
        return utilities((a,) + tuple(rivals))[0]

    return (
        customers, topics, policy, terminal,
        utilities, f, comparisons
    )


def main():
    # Boundary cases and a deliberately non-equilibrium policy.
    audit(1, 1, {1: 1}, "0")
    audit(1, 3, {}, "000")
    audit(2, 2, {1: 1, 2: 1}, "110")

    rejected = False
    try:
        audit(2, 2, {1: 1, 2: 1}, "000")
    except AssertionError:
        rejected = True
    assert rejected

    (
        customers, topics, policy, terminal,
        utilities, f, comparisons
    ) = audit(6, 4, WEIGHTS, POLICY)

    z = terminal(())
    u = utilities(z)
    W = len(frozenset().union(*(topics[a] for a in z)))

    assert len(customers) == 89
    assert len(policy) == 259
    assert comparisons == 1554
    assert z == (2, 5, 0, 0)
    assert u == (F(71, 3), F(22), F(59, 3), F(59, 3))
    assert sum(u) == W == 85

    # Independent comparison variables, not hidden randomized play.
    p = {1: F(1, 2), 2: F(1, 2)}
    rows, h = [], ()

    for i in range(4):
        def rivals(a):
            zz = terminal(h + (a,))
            return zz[:i] + zz[i + 1:]

        D = sum(
            (p[a] * f(a, rivals(a)) for a in p), F(0)
        )
        C = sum(
            (
                p[a] * p[b] * f(a, rivals(b))
                for a in p for b in p
            ),
            F(0),
        )
        rows.append((D, C, D - C, u[i] - D))
        h += (policy[h],)

    assert [r[2] for r in rows] == [
        F(-1, 48), F(0), F(0), F(0)
    ]
    assert sum(r[0] for r in rows) == F(977, 12)
    assert sum(r[1] for r in rows) == F(1303, 16)
    assert sum(r[3] for r in rows) == F(43, 12)
    assert W - sum(r[1] for r in rows) == F(57, 16)

    # Exact certificates over all ordered competitor tuples.
    assert sum(PRIMARY) == sum(DUAL.values()) == 1
    assert min(PRIMARY) >= 0
    assert min(DUAL.values()) >= 0

    lower = min(
        sum(
            (PRIMARY[a] * f(a, B) for a in range(6)),
            F(0),
        )
        for B in product(range(6), repeat=3)
    )
    upper = max(
        sum(
            (q * f(a, B) for B, q in DUAL.items()),
            F(0),
        )
        for a in range(6)
    )

    assert lower == upper == F(508643, 26546)
    assert W - 4 * lower == F(110919, 13273) > 0

    return {
        "claim": (
            "sum_i(D_i-C_i) >= 0 is false; "
            "BR is NOT refuted"
        ),
        "unit_customers": len(customers),
        "ordered_decision_histories": len(policy),
        "exact_incentive_comparisons": comparisons,
        "outcome": list(z),
        "utilities": list(map(str, u)),
        "W": W,
        "v_4": str(lower),
        "W_minus_4v_4": str(W - 4 * lower),
        "aggregate_decorrelation": str(
            sum(r[2] for r in rows)
        ),
        "aggregate_on_path_slack": str(
            sum(r[3] for r in rows)
        ),
        "compensated_budget": str(
            W - sum(r[1] for r in rows)
        ),
        "rows_D_C_kappa_slack": [
            list(map(str, r)) for r in rows
        ],
        "boundary_tests": (
            "passed; non-SPE policy rejected"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
