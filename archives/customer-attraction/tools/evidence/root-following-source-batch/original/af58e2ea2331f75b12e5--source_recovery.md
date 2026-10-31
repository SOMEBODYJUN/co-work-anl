# Full-terminal aggregate: recovered source and exact scope

2026-10-24. Personal exploratory checkpoint. General Q-CAG-HALF and FTA both
remain OPEN. The facts in this note are recoveries, not newly claimed results.

## Fixed definitions

Fix one arbitrary full ordered-history pure SPE `sigma`, with actual leaf
`z=(S_1,...,S_m)`, payoffs `u_i`, and `W=sum_i u_i`. At its actual prefix
`h_i=(S_1,...,S_(i-1))`, force source topic `B` and then follow the same
original sigma. The complete m-slot leaf is `Z_i(B)`. Deleting only the forced
position from that leaf gives `Y_i(B)`, with m-1 slots.

For every topic multiset Q, write

`f_Q(A)=sum_(x in A) 1/(1+c_x(Q))`.

For independent A,B drawn from one arbitrary topic distribution p, set

```
D_i = E_B f_(Y_i(B))(B),
C_i = E_(A,B) f_(Y_i(B))(A),
C_i^+ = E_(A,B) f_(Z_i(B))(A),
e_i = u_i-D_i >= 0,
kappa_i = D_i-C_i,
H_i = C_i-C_i^+
    = E_(A,B) sum_(x in A intersect B)
      1/[c_x(Z_i(B))(c_x(Z_i(B))+1)] >= 0.
```

The denominator in H is used only when x belongs to B, so its load is at
least one. The exact already-known identity is

`W-sum_i C_i^+ = sum_i (e_i+kappa_i+H_i)`.

FTA is the unproved all-input, all-sigma, all-p inequality

`sum_i C_i^+(p) <= W`.

The original source is
`../../R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/full_terminal_debt.md`.
Its static comparison `OPT_m <= 2m v_(m+1)(0)` makes FTA sufficient for half.
The latest actor's
`../../R-cef41b80a6e048b5a395b738d3b0b6e7/menu/README.md` and
`../../R-cef41b80a6e048b5a395b738d3b0b6e7/GENERAL_WORKING.md`
correctly identify AP-extra as exactly this old FTA.

## Already-known barriers retained exactly

The stronger pairwise path inequality has a complete four-player,
six-topic, 245-unit-client counterexample. Actual W is 180 and the relevant
cross sum is 365 > 360. The same pair's genuine two-source FTA quadratic
slack is `143 t^2-101 t+48`, strictly positive on [0,1]. Thus the pairwise
failure does not refute FTA; diagonal credit must not be discarded.
The independent replay is
`../../R-cef41b80a6e048b5a395b738d3b0b6e7/independent/old_crosscap_replay_review.md`.

The old m-1-slot all-p aggregate decorrelation inequality is false. Adding
back the source gives precisely H, not an independently repeatable wallet.
Full-terminal menus, ordinary static security, and iid static benchmarks
have different quantifiers. None is silently substituted for another.

## Explicit paid last-two portion (reconstruction only)

At the last actual position m, the competitor prefix is independent of B,
so `kappa_m=0`. If `b_x` is the actual first m-1 players' load and
`q_x=P_(A~p)(x in A)`, then

`H_m = sum_x q_x^2/[(b_x+1)(b_x+2)]`.

For m>=2, at position m-1 the already-known one-follower identity gives
`kappa_(m-1)=E_(A,B) L(A,B)>=0`, where, against the fixed actual prefix,
`L(A,B)` is the last player's true IC slack between its prescribed reply
after source A and the prescribed reply after source B. Therefore

```
W-sum_i C_i^+
 = sum_(i<=m-2) (e_i+kappa_i+H_i)
   + e_(m-1)+E L+H_(m-1)+e_m+H_m.
```

All the displayed final-five summands are nonnegative, but no payment of
the early kappa terms follows. This is a useful exact accounting boundary,
not new general progress; it follows from the existing last-two identity.
