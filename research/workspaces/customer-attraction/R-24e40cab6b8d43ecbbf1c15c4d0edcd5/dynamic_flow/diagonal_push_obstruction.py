"""Exact finite audit for the diagonal p^T K p <= u strengthening.

This is an auxiliary-interface diagnostic only. It uses the canonical exact
pure-SPE solver to obtain one complete worst-welfare certificate, then checks
all 31 ordered histories / 124 one-shot comparisons through verify_certificate.
The displayed p gives an exact positive gap p^T K p-u=13/1722.
"""
from fractions import Fraction as F
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate

INSTANCE = Instance(
    ("T0", "T1", "T2", "T3", "T4"),
    tuple(CustomerType(frozenset(s), 1) for s in (
        {3}, {0, 3, 4}, {0, 1, 3}, {0, 2}, {2, 4}, {0, 3}, {0, 2}, {0, 1, 2, 3}
    )),
    3,
)
P = (F(10, 287), F(157, 287), F(0), F(0), F(120, 287))

def terminal(cert, history):
    if len(history) == INSTANCE.players:
        return INSTANCE.counts(history, terminal=True), history
    return terminal(cert, history + (cert.actions[history],))

def main():
    solver = ExactSPESolver(INSTANCE)
    cert = solver.worst_certificate()
    checked = verify_certificate(INSTANCE, cert)
    assert checked.valid
    branches = [terminal(cert, (a,))[0] for a in range(INSTANCE.topic_count)]
    # K[T,A] is the payoff of a hypothetical extra T after the full branch A.
    K = []
    for T in range(INSTANCE.topic_count):
        row = []
        for counts in branches:
            row.append(sum((F(ct.multiplicity,
                              sum(counts[t] for t in ct.topics) + 1)
                            for ct in INSTANCE.customers if T in ct.topics), F()))
        K.append(tuple(row))
    d = tuple(INSTANCE.topic_payoffs(c)[a] for a, c in enumerate(branches))
    quadratic = sum(P[i] * P[j] * K[i][j]
                    for i in range(5) for j in range(5))
    expected_d = sum(P[i] * d[i] for i in range(5))
    gap = quadratic - expected_d
    assert quadratic == F(1501, 1722)
    assert expected_d == F(248, 287)
    assert gap == F(13, 1722) and gap > 0
    print({
        "status": "EXACT_AUXILIARY_DIAGONAL_PUSH_FAILURE",
        "players": INSTANCE.players,
        "topics": INSTANCE.topic_count,
        "customers": INSTANCE.customer_count,
        "checked_histories": checked.checked_histories,
        "checked_deviations": checked.checked_deviations,
        "root_path": terminal(cert, ())[1],
        "terminal_counts": cert.terminal_counts,
        "welfare": INSTANCE.welfare(cert.terminal_counts),
        "optimum": INSTANCE.optimal_welfare(),
        "p": tuple(map(str, P)),
        "pKp": str(quadratic),
        "pD": str(expected_d),
        "gap": str(gap),
        "scope": "否定 p^T K p<=u for all p; does not refute Mfull, Mpath, aggregate W budget, or Q-CAG-HALF",
    })

if __name__ == "__main__":
    main()
