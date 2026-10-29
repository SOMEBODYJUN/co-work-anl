"""Exact certificate for a four-player root-tax counterexample."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product

GROUPS = {
    "A": 12, "B": 8, "C": 4, "D": 8,
    "AE": 6, "AF": 6, "CE": 3, "CF": 3,
    "AEF": 6, "BEF": 2, "CEF": 1, "DEF": 2,
}


def expand_groups(groups, labels="ABCDEF"):
    """Each customer is a distinct unit customer."""
    topics = {a: set() for a in labels}
    next_id = 0

    for membership, multiplicity in groups.items():
        if multiplicity < 0 or not set(membership) <= set(labels):
            raise ValueError("Invalid customer group.")

        for x in range(next_id, next_id + multiplicity):
            for a in membership:
                topics[a].add(x)

        next_id += multiplicity

    return topics


def certify(n, topics, early="A"):
    """First n-1 players choose early; last-player ties favor larger labels."""
    if n < 1 or not topics or early not in topics:
        raise ValueError("Invalid game.")

    actions = tuple(sorted(topics))
    universe = set().union(*topics.values())

    @lru_cache(None)
    def payoffs(profile):
        loads = Counter(x for a in profile for x in topics[a])
        return tuple(
            sum(
                (Fraction(1, loads[x]) for x in topics[a]),
                Fraction(0),
            )
            for a in profile
        )

    @lru_cache(None)
    def last_reply(history):
        return max(
            actions,
            key=lambda a: (payoffs(history + (a,))[-1], a),
        )

    def strategy(history):
        if not 0 <= len(history) < n:
            raise ValueError("Expected a nonterminal history.")
        return early if len(history) < n - 1 else last_reply(history)

    def follow(history):
        while len(history) < n:
            history += (strategy(history),)
        return history

    nodes = deviations = 0

    for depth in range(n):
        for history in product(actions, repeat=depth):
            chosen = strategy(history)
            actual = payoffs(follow(history))[depth]
            nodes += 1

            for alternative in actions:
                if alternative == chosen:
                    continue

                # Execute the SAME strategy after the actual deviation.
                changed = follow(history + (alternative,))
                deviation_payoff = payoffs(changed)[depth]

                if deviation_payoff > actual:
                    raise AssertionError(
                        (
                            history, chosen, alternative,
                            actual, deviation_payoff,
                        )
                    )

                deviations += 1

    outcome = follow(())
    W = len(set().union(*(topics[a] for a in outcome)))

    OPT = max(
        len(set().union(*(topics[a] for a in profile)))
        for profile in product(actions, repeat=n)
    )

    prefix_load = Counter(
        x for a in outcome[:-1] for x in topics[a]
    )
    tau = sum(
        (
            Fraction(prefix_load[x], prefix_load[x] + 1)
            for x in universe
        ),
        Fraction(0),
    )

    assert sum(payoffs(outcome)) == W

    return (
        outcome, payoffs(outcome), W, OPT, tau,
        nodes, deviations,
    )


def main():
    # Boundary tests.
    assert certify(
        1, {"A": set(), "B": {0}}
    )[0] == ("B",)

    assert certify(
        4, {"A": set()}
    )[2:5] == (0, 0, Fraction(0))

    assert certify(
        3, {"A": {0}, "B": {0}}
    )[2:5] == (1, 1, Fraction(2, 3))

    assert certify(
        2, {"A": {0}, "B": {1}}
    )[2:5] == (2, 2, Fraction(1, 2))

    topics = expand_groups(GROUPS)
    result = certify(4, topics)

    expected = (
        tuple("AAAF"),
        tuple(map(Fraction, (9, 9, 9, 11))),
        38, 61, Fraction(45, 2),
        259, 1295,
    )
    assert result == expected

    outcome, utilities, W, OPT, tau, nodes, deviations = result

    assert OPT - W - tau == Fraction(1, 2)
    assert W + tau + Fraction(1, 2) == OPT
    assert OPT <= 2 * W

    # A, B, C, D partition all customers.
    assert sum(len(topics[a]) for a in "ABCD") == OPT
    assert len(
        set().union(*(topics[a] for a in "ABCD"))
    ) == OPT

    print("Boundary tests: passed")
    print("Outcome:", "".join(outcome))
    print("Payoffs:", ", ".join(map(str, utilities)))
    print(f"W = {W}; OPT_4 = {OPT}; tau = {tau}")
    print("OPT_4 - W - tau =", OPT - W - tau)
    print(
        f"Verified all {nodes} ordered decision histories "
        f"and {deviations} deviations."
    )


if __name__ == "__main__":
    main()
