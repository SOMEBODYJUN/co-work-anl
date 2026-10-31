# Canonical floor dual: exact one-shot reset and copy cancellation

2026-10-25, matching12. General original input class; HALF OPEN. This is a
signed reset ledger, not a common-money bound. It applies only when both
endpoints are ALLOWED by the chosen ALL-terminal analytical row domain.
In particular a fixed actual-action tag cannot silently admit a changed
endpoint. No multiplier bound is assumed.

Fix entering row i, forced action A and an ORIGINAL true continuation
witness. Let its endpoint be z. For any strict future role k>i, at the real
history h=z_<k force legal T and then execute the SAME witness thereafter,
obtaining z'. Its true whole-IC gap is

    Gamma=u_k(z)-u_k(z')>=0.

Every strict future role j>k of z' is still prescribed by a complete SPE
at its new prefix; its canonical slack is therefore nonnegative. Define
s_j(y)=u_j(y)-M(y_<j) when that role is genuinely prescribed. All s_j(z)
are nonnegative; all s_j(z') for j>k are nonnegative. Earlier prefixes
i<j<=k are unchanged by the reset.

For one fixed set of nonnegative row floor prices lambda_h, write

    Ftail(y;k)=sum_(j>k)lambda_(y_<j)s_j(y).

The floor deficits of the reset endpoint have the exact expansion

    sum_h lambda_h Delta_h(z')
      =sum_(i<j<k)lambda_(z_<j)
          [u_j(z)-u_j(z')-s_j(z)]
        +lambda_h[Gamma-s_k(z)]-Ftail(z';k).       (RESET-FLOOR)

This keeps every affected earlier ancestor, not only the deviating role.
It gives the exact difference from the original negative-floor bank:

    sum_h lambda_h[Delta_h(z')-Delta_h(z)]
      =sum_(i<j<k)lambda_(z_<j)[u_j(z)-u_j(z')]
        +lambda_h Gamma+Ftail(z;k)-Ftail(z';k).    (DIFF)

Let the all-terminal dual reduced cost be

    R(y)=eta+mu d_i(y)+sum_h lambda_h Delta_h(y)-score(y)>=0.

Subtracting the two dual EQUALITIES gives

    score(z')-score(z)
      =mu[d_i(z')-d_i(z)]
        +sum_(i<j<k)lambda_(z_<j)[u_j(z)-u_j(z')]
        +lambda_h Gamma+Ftail(z;k)-Ftail(z';k)
        +R(z)-R(z').                              (ONE-SHOT)

Thus canonical floor surpluses and reduced costs are real terms with
definite signs, but the ancestor profit losses and priced whole-IC gap
remain. Discarding the negative Ftail(z';k) and R(z') gives a valid upper
bound, not a paid common capacity. A history absent from the source has no
source floor-surplus bank even if its price is positive.

For a copy reset T=A, the entering and deviating role choose the same
theme in z', so their same-leaf utilities are equal:
d_i(z')=u_k(z'). Consequently the cap/deviator terms combine exactly as

    mu[d_i(z')-d_i(z)]+lambda_h Gamma
      =lambda_h u_k(z)-mu d_i(z)
           +(mu-lambda_h)d_i(z').                 (COPY-CANCEL)

If lambda_h=mu, that part becomes mu[u_k(z)-d_i(z)] and no longer contains
the reset leaf. This is a conditional cross-role cancellation, not an
available price normalization: no equality lambda_h=mu or global lambda
bound has been established. Off-path u_k(z) is not the actual role-k bank.

Strictly increasing reset sequences can telescope the complete dual
potential, but cannot replace the remaining signed profit-loss ledger by
its positive part for free. Identifying a feasible endpoint or a set of
dual variables does not pay lambda_h Gamma. A general transport with
compatible history reach masses, or a genuine bound on these terms, is
still needed. At m=5 the same identities leave the same unpaid terms;
they do not establish arbitrary-catalog five-player HALF.
