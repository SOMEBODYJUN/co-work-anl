# Shared-saddle bank ledger and credible tail freedom: exact scope

2026-10-25, credible11. Parent requested an original-model proof attack on
`../parent/shared_load_bregman_working.md`, using full-history bank/PUNISH
incentives at a genuine joint saddle. **No new joint payment inequality
was proved.** The following are exact ledgers and a source clarification;
they are not a welfare improvement or another finite pressure project.
Original HALF, the shared-load bridge, and aggregate safety remain OPEN.

## 1. Prices available only at the joint saddle

Use the parent's K, a joint query/background saddle `(p*,L*)`, and

\[
t_x=\frac1{1+L_x^*},\quad
\rho_x=\Pr_{A\sim p^*}(x\in A),\quad
\gamma=\max_{A\in\mathcal S}\sum_{x\in A}t_x.
\]

All legal themes have price at most gamma, and every p*-supported theme
has price exactly gamma. Thus the action discount

\[
k(A)=\gamma-\sum_{x\in A}t_x
\tag{PRICE}
\]

is nonnegative; it is zero on query support. This requires the joint
saddle, not merely minimization of `F_p` for an arbitrary fixed p.

For a provider choosing A in a terminal profile with final loads c,

\[
u(A)-\gamma
=\sum_{x\in A}\left(\frac1{c_x}-t_x\right)-k(A).
\tag{SIGNED}
\]

Subtracting the same constant gamma from every player's original utility
does not change any original best response. Consequently the original
complete-history SPE inequalities are exactly the SPE inequalities for
signed congestion returns `1/c-t_x` and nonnegative action cost k(A).
The signed resource returns may be negative; they are not new customer
values or a different input class.

In particular at every genuine history, if prescribed action B is compared
to an active query A, define G as the sum of signed returns in the
respective **true completed branch**. Original IC says

\[
G(B;\text{prescribed tail})
\ge G(A;\text{its true tail})+k(B).
\tag{DISCIPLINE}
\]

This retains the nonnegative discount required when a future punisher
uses a lower-price bank action. It is an exact rewriting of that local
IC, not additional money and not a quantitative cross-history charge.

## 2. The exact weighted rent that a bank punishment creates

At actual role i force active A and follow the original full strategy.
Write z_x for the other m-1 players' total final load on x, including all
previous players. Set

\[
R_i(A)=\sum_{x\in A}\frac{t_xz_x}{1+z_x},\qquad
H_i(A)=\sum_{x\in A}\frac{1-t_x}{1+z_x}.
\]

R is the t-weighted combined rent of all other providers on A. Pointwise
conservation, with the same completed branch throughout, gives

\[
\gamma-d_i(A)=R_i(A)-H_i(A).
\tag{RENT-t}
\]

For a nonactive A the left side gains k(A):
`gamma-d_i(A)=k(A)+R_i(A)-H_i(A)`.
Empty themes and zero-membership clients contribute zero. The formulas
never assign shares between different leaves.

The parent's Bregman balance therefore has the exactly equivalent form

\[
C-D=\sum_i\mathbb E_{A\sim p^*}[R_i(A)-H_i(A)],
\]

and the outstanding amount inequality is

\[
\sum_i\mathbb E R_i(A)
\le\sum_i IC_i+\sum_i\mathbb E H_i(A).
\tag{UNPAID}
\]

This is a weighted extension of the same-branch RENT identity already
recorded in `../../round10/direct/direct_general_working.md`, not a newly
proved budget. DISCIPLINE is valid at every successor history, but its
prescribed and queried tails are themselves different full branches.
Summing the displayed rents from different first deviations as if one
actual future player's payoff funded all of them would duplicate money.
The price cap alone bounds each branch's theme price; it has not related
these different-branch weighted rents to one actual budget. KKT controls
the decorrelated coefficient `rho_x t_x^2`, not the query-dependent
capturer incidence appearing in R. This is the precise missing cost.

The peer insurance family shows how a *specific* controller can pay its
middle player's loss by a bank that the final player genuinely copies.
Its last best response, fresh-bank transitions, and joint coordinate
deviations are essential. They do not yet give a universal transportation
of R across arbitrary histories. Aggregate11's exact insurance joint
saddle has positive C and positive D+IC paying it; we neither redo its
special calculation nor infer a sign for C.

## 3. Independent first-deviation reselection is old legitimate freedom

The stronger fixed-original-strategy shared bridge is not necessary for
HALF. Fix only the original actual leaf Z, its actual ordered prefixes
h_i, and actual payoffs u_i. For A different from Z_i, one may replace
the entire first-deviation subtree at h_i A by any complete child SPE
whose entering player payoff is at most u_i. Keep the actual branch
leading to Z and complete its own offpath children in the same manner.

First-deviation subtrees for different actual roles/actions are disjoint
as **ordered histories**. Thus these replacements preserve every
actual-prefix IC, preserve the actual leaf and all its profits, and use
genuine full child SPEs at all nonactual histories. Earlier actual
ancestors do not enter a later first-deviation subtree under their own
different earlier deviation. The actual forced column A=Z_i remains the
actual deleted-slot leaf, rather than an arbitrary capped leaf.

This is standard source material, not a new mechanism:
`research/current/customer_attraction/credible_continuations.md` section 1,
especially its capped menu (2), explicitly constructs all compatible
complete strategies by independent choices in disjoint ordered child
subtrees. Root and direct11 independently pointed to the same old
endpoint reduction.

One may consequently enlarge each fixed menu to all such credible capped
deleted-slot leaves before forming a shared-load domain. Every resulting
background remains a legal total-mass m-1 fractional catalog background.
Its minimax cap is no larger than the cap of the original fixed menus.
Hence a payment proof in this enlarged domain would still be sufficient
for the original arbitrary-SPE welfare target. But we have proved no
amount bound there either: maximizing the saddle shadow weight
`rho t^2` over a larger capped menu does not by itself establish UNPAID.
This freedom should be cited as the old legitimate menu scope, not as a
new welfare result or as already funded tail resets.

## 4. Stop and m=5 status

For arbitrary m and for m=5 the same ledgers, nonnegative k, and
first-deviation compatibility hold. At m=5, UNPAID would establish the
shared cap payment and the corresponding conditional HALF implication;
neither the signed rewrite nor enlarged menu availability proves it.
No further finite scans, local coefficient projects, new auxiliary
counterexamples, or additional bridge candidates were pursued here.
