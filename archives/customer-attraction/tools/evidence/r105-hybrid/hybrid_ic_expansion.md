# Expanding a full-tail transplant into true one-action ICs

2026-10-24. Exploratory general-input algebra. No novelty claim and no
nonnegative aggregate budget are asserted. Q-CAG-HALF and FTA remain OPEN.

The purpose is to expose the unpaid term after replacing the invalid move
"a follower chooses a whole continuation" by genuine one-action deviations.

## Setup

Fix any original full SPE, any ordered history h with old load b, and the
current position i. There are r players left, n=r-1 followers. For source
A, write `Y_A` for its original sigma tail, and let `Y_B=(B_1,...,B_n)` be
the original sigma tail after another source B. Define the relative
harmonic potential of a suffix profile P by

`Phi_b(P)=sum_x sum_(ell=1)^(c_x(P)) 1/(b_x+ell)`.

The preexisting continuation-potential debt is

`R_AB = Phi_b(A,Y_B)-Phi_b(A,Y_A)`.

It is not the utility difference of any single player when n>1.

## Genuine hybrid histories

For k=0,...,n, fix the legal ordered history

`H_k=(h,A,B_1,...,B_k)`

and let `P^k` be the r-slot suffix obtained by completing H_k with the same
original sigma. Thus

`P^0=(A,Y_A)` and `P^n=(A,Y_B)`.

At the history H_(k-1), player j=i+k is prescribed the completion P^(k-1).
Forcing only its next action B_k and following original sigma gives P^k.
Hence the following are genuine nonnegative full-history IC slacks:

`gamma_k = u_j(h,P^(k-1))-u_j(h,P^k) >= 0`.

For any suffix P, its current player's marginal in Phi_b is exactly its
final original-game utility:

`Phi_b(P)-Phi_b(P without j)=u_j(h,P)`.

Consequently the following identity holds for every k:

```
Phi_b(P^k)-Phi_b(P^(k-1))
 = -gamma_k
   + Phi_b(P^k without j)-Phi_b(P^(k-1) without j).
```

Summing gives the exact all-input expansion

```
R_AB = -sum_(k=1)^n gamma_k + sum_(k=1)^n E_k,
E_k = Phi_b(P^k without (i+k))
      -Phi_b(P^(k-1) without (i+k)).
```

The k=n residual is zero: at the last player the two profiles differ only
in that player's action, so deleting it leaves identical profiles.

## Exact interpretation of the remainder

Let `Q_(k-1)=(A,B_1,...,B_(k-1))`, and let T_0,T_1 be the suffixes after
player j in P^(k-1), P^k. Cancelling the common fixed Q prefix gives

`E_k = Phi_(b+c(Q_(k-1)))(T_1)
       -Phi_(b+c(Q_(k-1)))(T_0)`.

This is a future-tail potential change with the moved player's action
removed only in the potential calculation. It is not a new game's SPE
comparison. The actual strategy histories retain that removed action,
and T_0,T_1 may both change fully.

One therefore cannot recursively call the same IC as though the moved
player had truly disappeared. At any fixed leaf with a removed topic S,
write c_x for its full load including h. The utility of another original
player j in the algebraically deleted profile
exceeds its original utility by

`rebate_S(j)=sum_(x in S intersect S_j) 1/[(c_x-1)c_x]`.

Only shared x occur, so c_x>=2. Summing over all other original players
(including the fixed old players) at that one leaf yields

`sum_(j != owner(S)) rebate_S(j)
 = sum_(x in S, c_x>=2) 1/c_x <= u_owner(S)`.

This is a same-leaf deletion rebate. Different hybrids P^k are mutually
incompatible leaves; their rebates are not automatically one common
wallet, nor are they the original FTA extra-slot credit H.

## What this does and does not settle

Every gamma above is a legal off-history IC, so no full-tail coalition
deviation or order-insensitive continuation has been used. However the
remaining sum E_k has no established sign or common actual-path payment.
The identity gives no new FTA inequality: a useful next proof must bound
the averaged residuals jointly by the already available H/e credits and
the gamma slacks, paying each utility budget once. Simply naming sum E_k
a continuation debt would add no mathematical information.

No test instance or negative scan was performed. No special topic class,
fixed player count, or stronger pairwise path condition is being pursued.
