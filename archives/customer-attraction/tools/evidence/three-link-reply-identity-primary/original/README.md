# Exact three-link full-history reply closure (six providers)

This workspace records one concrete six-provider closure relation that keeps
the identity of a reply when it is reused as the next source action.  It is a
necessary-condition projection for a complete-history pure SPE.  It is not a
game construction, an SPE certificate, or a proof of `2W >= OPT_6`.

## Relation

Take any true history with three providers left (the fourth, fifth and sixth
positions).  For `q=0,1,2`, force the fourth provider to choose `T_q`; write the
next two themes as `(B_q,R_q)`, with `R_q` the terminal sixth-provider reply.
Reuse the reply as the next source action:

```
T_1 = R_0,   T_2 = R_1.
```

For customer `x`, let `p` be its number of covers before the source and `ell`
its load before the global last player.  Put

```
D_q = p + t_q + b_q + y_q,
Q_q = b_q / (p + t_{q+1} + b_{q+1} + b_q),
```

with zero numerator interpreted as zero, and `t_q,b_q,y_q` the membership bits
of `T_q,B_q,R_q`.  With weights

```
lambda = (1,3,2), eta = (4,1), alpha = (1,1,1), beta = (1,1,1),
```

the customer residual is

```
F = Σq lambda[q] t_q/D_q
  + Σq alpha[q] y_q/(ell+1) + Σq beta[q] y_q
  + 4 (Q_0 - y_1/D_1) + (Q_1 - y_2/D_2).
```

Summing the corresponding nonnegative rows gives the exact necessary
inequality

```
6 r + 3 u_6 + 3 K >= Σ_x F(x),
```

where `r` is the source player's actual payoff, `u_6` the actual global-last
player payoff, and `K=max |S|` over the common catalogue.  The terms are,
respectively, three source-node IC rows, two terminal best-response rows at
the next chain nodes, three global-last-player price rows, and three catalogue
capacity rows.  The script verifies the decomposition with exact `Fraction`
arithmetic for every linked binary assignment.

## Exact closure audit

Run:

```bash
python full_history_chain/check_chain_L3.py
```

This enumerates all 128 identity-linked states and all 512 states without the
identities for each feasible `(p,ell)` (`0 <= p <= 3`, `p <= ell <= 5`).  The
result is [chain_L3_exact.json](full_history_chain/chain_L3_exact.json).

The linked minimum at `(p,ell)=(0,0)` is `-1`, while dropping both identities
gives `-2`; the exact gain is `1`.  Fourteen of the 18 `(p,ell)` rows have a
strict positive identity gain.  This demonstrates that preserving the shared
reply identity is a genuine new full-history closure relation; pairwise
minimization would lose that gain.

The negative minima also state the payment limit precisely: this weighted
three-link closure alone has no nonnegative per-customer lower bound.  A
global half proof would still need additional rows and a common nonnegative
budget that absorbs these negative `F` values.  No such budget or half result
is claimed here.
