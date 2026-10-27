"""Exact full-history SPE check for the m=6 all-big topic family.

Catalog: B={0,...,5} and singleton themes {6},...,{10}; six providers.
The strategy chooses B at every ordered history, including off path.
This is an exact certificate of a *nonviolating* lower-bound example:
W=6, OPT_6=11, so 2W=12>=11 and OPT/W=11/6.
"""
from fractions import Fraction
from itertools import product

M = 6
B = frozenset(range(6))
S = (B,) + tuple(frozenset((x,)) for x in range(6, 11))
MPLAY = 6


def payoff(seq, i):
    """Provider i's terminal utility as a Fraction."""
    chosen = S[seq[i]]
    ans = Fraction(0)
    for x in chosen:
        load = sum(x in S[a] for a in seq)
        ans += Fraction(1, load)
    return ans


def welfare(seq):
    return sum((payoff(seq, i) for i in range(MPLAY)), Fraction(0))


def strategy(_history):
    return 0


def verify_spe():
    checks = 0
    worst_margin = None
    for depth in range(MPLAY):
        for h in product(range(len(S)), repeat=depth):
            a_star = strategy(h)
            terminal = h + (a_star,) + (0,) * (MPLAY - depth - 1)
            own = payoff(terminal, depth)
            for a in range(len(S)):
                # Deviate at this node; all later players use the same strategy B.
                dev_terminal = h + (a,) + (0,) * (MPLAY - depth - 1)
                dev = payoff(dev_terminal, depth)
                margin = own - dev
                checks += 1
                if margin < 0:
                    raise AssertionError((h, a, own, dev, terminal, dev_terminal))
                if worst_margin is None or margin < worst_margin:
                    worst_margin = margin
    return checks, worst_margin


def opt_welfare():
    best = Fraction(-1)
    best_seq = None
    for seq in product(range(len(S)), repeat=MPLAY):
        w = welfare(seq)
        if w > best:
            best, best_seq = w, seq
    return best, best_seq


if __name__ == "__main__":
    checks, margin = verify_spe()
    opt, arg = opt_welfare()
    root = (0,) * MPLAY
    W = welfare(root)
    covered = len(set().union(*(S[a] for a in root)))
    print({
        "players": MPLAY,
        "catalog_size": len(S),
        "histories_and_deviations_checked": checks,
        "worst_SPE_margin": str(margin),
        "root_sequence": root,
        "root_welfare_W": str(W),
        "root_covered": covered,
        "OPT_6": str(opt),
        "one_optimal_sequence": arg,
        "two_W_minus_OPT": str(2 * W - opt),
        "ratio_OPT_over_W": str(opt / W),
        "status": "exact full-history pure SPE; nonviolating lower-bound family",
    })
