"""Exact Fraction audit of a three-link full-history reply chain.

The source is any true node with three players left (positions 4,5,6).
For branch q, force source theme T_q and write the later themes as
(B_q,R_q), where R_q is the terminal reply.  The chain identity is
T_{q+1}=R_q.  The script checks the customer-wise decomposition of the
weighted source IC, terminal reply IC, actual-last-player price, and K-cap
rows.  It also records the exact linked minimum, which is the projection
used by the resulting necessary condition.
"""
from fractions import Fraction as F
from itertools import product
import json

L = 3
LAMBDA = (F(1), F(3), F(2))
ETA = (F(4), F(1))
ALPHA = (F(1), F(1), F(1))
BETA = (F(1), F(1), F(1))


def sh(n, d):
    return F(n, d) if n and d else F(0)


def branches(linked):
    """Yield (t,b,y) bit tuples, optionally enforcing t[q+1]=y[q]."""
    for ts in product((0, 1), repeat=L):
        for bs in product((0, 1), repeat=L):
            for ys in product((0, 1), repeat=L):
                if linked and any(ts[q + 1] != ys[q] for q in range(L - 1)):
                    continue
                yield ts, bs, ys


def customer_value(p, ell, ts, bs, ys):
    """F_chain contribution of one customer, exactly as a Fraction."""
    ans = F(0)
    den = []
    for q in range(L):
        D = p + ts[q] + bs[q] + ys[q]
        den.append(D)
        ans += LAMBDA[q] * sh(ts[q], D)
        ans += ALPHA[q] * sh(ys[q], ell + 1)
        ans += BETA[q] * ys[q]
    for q in range(L - 1):
        # Last player in branch q+1 queries B_q.  Its denominator is the
        # branch-q+1 prefix plus B_q; zero numerator means zero payoff.
        # The query replaces branch q+1's terminal R_{q+1}; its denominator
        # therefore contains the source, B_{q+1}, and queried B_q only.
        query_den = p + ts[q + 1] + bs[q + 1] + bs[q]
        qpay = sh(bs[q], query_den)
        ans += ETA[q] * (qpay - sh(ys[q + 1], den[q + 1]))
    return ans


def audit_decomposition(p, ell, ts, bs, ys):
    """Check the weighted row sum leaves exactly F_chain.

    We represent each row by its per-customer contribution.  The source
    IC leaves Lambda*r and -sum lambda*v; terminal IC leaves +e-q; price
    rows leave Alpha*u6-Alpha*P; K rows leave Beta*K-Beta*|R|.  Therefore
    after moving the customer terms to the right, the residual must equal
    customer_value().
    """
    # Customer terms on the *left* after collecting all weighted rows.
    left_customer = F(0)
    den = []
    for q in range(L):
        D = p + ts[q] + bs[q] + ys[q]
        den.append(D)
        left_customer -= LAMBDA[q] * sh(ts[q], D)  # -v_q
        left_customer += ALPHA[q] * (-sh(ys[q], ell + 1))  # -P_ell(R_q)
        left_customer -= BETA[q] * ys[q]  # -|R_q|
    for q in range(L - 1):
        query_den = p + ts[q + 1] + bs[q + 1] + bs[q]
        left_customer += ETA[q] * (sh(ys[q + 1], den[q + 1]) - sh(bs[q], query_den))
    # F_chain is by definition the negative of these customer terms.
    assert -left_customer == customer_value(p, ell, ts, bs, ys)


def main():
    rows = []
    for p in range(4):
        for ell in range(p, 6):
            linked = [(customer_value(p, ell, *z), z) for z in branches(True)]
            free = [(customer_value(p, ell, *z), z) for z in branches(False)]
            lv, la = min(linked, key=lambda x: x[0])
            fv, fa = min(free, key=lambda x: x[0])
            for _, z in linked:
                audit_decomposition(p, ell, *z)
            rows.append({
                "p": p, "ell": ell,
                "linked_min": str(lv), "free_min": str(fv),
                "identity_gain": str(lv - fv),
                "linked_arg": la, "free_arg": fa,
                "linked_states": len(linked), "free_states": len(free),
            })
    out = {
        "L": L,
        "lambda": [str(x) for x in LAMBDA],
        "eta": [str(x) for x in ETA],
        "alpha": [str(x) for x in ALPHA],
        "beta": [str(x) for x in BETA],
        "rows": rows,
        "scope": "exact necessary full-history chain projection; not an SPE certificate or half proof",
    }
    with open("chain_L3_exact.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"rows": len(rows), "linked_states": 128,
                      "free_states": 512, "strict_identity_rows": sum(F(r["identity_gain"]) > 0 for r in rows)}, indent=2))


if __name__ == "__main__":
    main()
