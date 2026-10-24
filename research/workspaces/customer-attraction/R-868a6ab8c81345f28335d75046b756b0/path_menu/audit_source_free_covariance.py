"""Exact independent audit of one old strict-response SPE and the FQ identity.

This fixed example attacks automatic per-customer residual monotonicity only.
No general menu or welfare conclusion is inferred from finite checks.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

TOPICS = [frozenset(s) for s in [
    ('x', 'z1', 'z2'), ('y1', 'y2', 'y3'),
    ('x', 'y1', 'y2', 'y3'), ('z1', 'z2', 'w1', 'w2')]]
CUSTOMERS = sorted(set().union(*TOPICS))
REPLY = (2, 3, 3, 2)
ACTUAL = (2, 3)


def load(z, x):
    return sum(x in TOPICS[a] for a in z)


def utility(z, i):
    return sum((F(1, load(z, x)) for x in TOPICS[z[i]]), F())


def insertion(z, t):
    return sum((F(1, 1 + load(z, x)) for x in TOPICS[t]), F())


def main():
    comparisons = 0
    strict_reply_margins = []
    for a in range(4):
        own = utility((a, REPLY[a]), 1)
        alternatives = [utility((a, b), 1) for b in range(4) if b != REPLY[a]]
        assert own > max(alternatives)
        strict_reply_margins.append(own - max(alternatives))
        comparisons += 4
    root_payoffs = [utility((a, REPLY[a]), 0) for a in range(4)]
    assert root_payoffs == [F(5, 2), F(3), F(4), F(4)]
    assert root_payoffs[ACTUAL[0]] >= max(root_payoffs)
    comparisons += 4
    W = len(set().union(*(TOPICS[a] for a in ACTUAL)))
    OPT = max(len(TOPICS[a] | TOPICS[b]) for a, b in product(range(4), repeat=2))
    assert W == OPT == 8

    p = [F(1, 4), F(3, 4), F(), F()]
    cols = [(a, REPLY[a]) for a in range(4)]
    K = [[insertion(z, t) for z in cols] for t in range(4)]
    C = sum((p[a] * p[t] * K[t][a] for a, t in product(range(4), repeat=2)), F())
    D = sum((p[a] * root_payoffs[a] for a in range(4)), F())
    psi = min(sum((p[t] * K[t][a] for t in range(4)), F()) for a in range(4))
    assert (D, C, psi, C - psi) == (F(23, 8), F(19, 12), F(35, 24), F(1, 8))

    # Audit all rational source/query laws on one fixed denominator-four grid, including
    # pure source distributions. The algebraic proof is separate from this check.
    laws = [[F(a, 4), F(b, 4), F(c, 4), F(4-a-b-c, 4)]
            for a in range(5) for b in range(5-a) for c in range(5-a-b)]
    identities = 0
    for query, source in product(laws, repeat=2):
        lhs = sum((source[a] * query[t] * K[t][a]
                   for a, t in product(range(4), repeat=2)), F())
        lhs -= sum((source[a] * root_payoffs[a] for a in range(4)), F())
        rhs = F()
        for x in CUSTOMERS:
            q = sum((query[t] for t in range(4) if x in TOPICS[t]), F())
            r = sum((source[a] for a in range(4) if x in TOPICS[a]), F())
            reciprocal = [F(1, 1 + load(cols[a], x) - int(x in TOPICS[a])) for a in range(4)]
            tax = [v / (1 + 1/v) for v in reciprocal]
            er = sum((source[a] * reciprocal[a] for a in range(4)), F())
            eir = sum((source[a] * reciprocal[a] for a in range(4) if x in TOPICS[a]), F())
            eij = sum((source[a] * tax[a] for a in range(4) if x in TOPICS[a]), F())
            rhs += (q-r)*er - (eir-r*er) - q*eij
        assert lhs == rhs
        identities += 1

    x = 'x'
    h = [load(cols[a], x) - int(x in TOPICS[a]) for a in range(4)]
    assert (h[0], h[1]) == (1, 0)
    Dx = p[0] * F(1, load(cols[0], x))
    Cx = sum((p[a] * F(1, 4) / (1 + load(cols[a], x)) for a in range(4)), F())
    assert (Dx, Cx, Cx-Dx) == (F(1, 8), F(5, 24), F(1, 12))
    cap_actual = max(insertion(ACTUAL, t) for t in range(4))
    assert cap_actual == 2
    report = dict(
        status='EXACT_OLD_SPE_REUSE; AUTOMATIC_RESIDUAL_MONOTONICITY_FALSE',
        scope='Only automatic all-p per-customer residual monotonicity is rejected; '
              'free Mfull/Mpath and Q-CAG-HALF remain OPEN.',
        source='R-5c4f6385eec046eb9a20052facacba11/global/response_debt_independent_review.md section 6',
        customers=len(CUSTOMERS), complete_decision_histories=5,
        full_SPE_comparisons=comparisons,
        strict_successor_margins=list(map(str, strict_reply_margins)),
        actual=list(ACTUAL), root_payoffs=list(map(str, root_payoffs)), W=W, OPT=OPT,
        query=list(map(str, p)), D=str(D), C=str(C), psi=str(psi), column_gain=str(C-psi),
        x_residual_cover=h[0], x_residual_noncover=h[1], x_D=str(Dx), x_C=str(Cx),
        x_debt=str(Cx-Dx), actual_column_cap=str(cap_actual),
        independent_source_query_identity_checks=identities,
    )
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
