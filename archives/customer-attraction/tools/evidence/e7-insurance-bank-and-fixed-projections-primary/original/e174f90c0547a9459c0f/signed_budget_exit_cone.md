# Signed repair budget: exact exit-cone formulation and current gap

2026-10-25. Task scope: arbitrary player count and arbitrary common finite
catalog in the unit-customer model. Q-CAG-HALF remains OPEN. No general
nonnegativity proof and no strict negative seed were obtained in this note.
This is a scratch handoff, not a canonical theorem promotion.

## Definitions checked against the existing construction

The source is
`R-ab4b3c24c8f949198e194dd45bb66105/mixed/signed_credible_repair.md`.
For a target `z=(A_1,...,A_m)` whose final action is a best response,

`ell_i(T)=min_{real complete tail SPE after (h_i,T)} u_i`,

`M_i=max_T ell_i(T)`, `g_i=M_i-u_i(z)`, `B=2W(z)-OPT_m`.

Every legal `T`, including `T=A_i`, belongs to this maximum. Unchanged
coordinates cannot retain an unverified target tail. Put `M_m=u_m(z)`.
The existing repair cost is

`C(g)=2P-N+p+n`,

where `P=sum g_+`, `N=sum (-g)_+`, `p=max(g,0)`, `n=max(-g,0)`.

Two exact rewritings locate the remaining payment:

`2W+C(g)=2 sum_{i=1}^m M_i+N+p+n`,

`2W+C(g)=W+sum_{i=1}^m M_i+P+p+n`.

The first is the unresolved exact-M path budget with explicit target
defect/selection-surplus corrections. Neither identity realizes the
different M-minimizing children as one common terminal path.

## A single exact LP for one fixed genuine exit table

This is an implementation-ready reduction of a fixed-table seed search,
not an assertion that some fixed table suffices for the general theorem.
It also avoids having to optimize or enumerate the true `OPT_m`.

Fix:

* finitely many catalog labels and customer incidence types;
* the target action tuple `z` and any comparison tuple `O` of at most m labels;
* for every normal target position i<m and every legal forced action T,
  one complete, ordered-history tail strategy map `rho_(i,T)`.

The unknown type masses x are nonnegative rational numbers. Require the
full SPE inequalities for every specified `rho_(i,T)` at every one of its
histories. For fixed strategies every terminal payoff and every such IC
inequality is linear in x. Require the target final action to be a BR.

Let `v_(i,T)(x)` be the forced current player's payoff under that exit map.
Introduce U_i and require

`U_i >= v_(i,T)(x)` for all T.

Then the genuine threshold satisfies `M_i<=U_i`; no claim of equality is
needed. Set `d_i=U_i-u_i(z;x)`. Introduce `r_i,a,b>=0` with

`r_i>=d_i`, `a>=d_i`, `b>=-d_i` for all i<m.

For fixed d, minimizing these auxiliary terms gives

`sum_i d_i + sum_i r_i + a+b = C(d)`.

Indeed `2P-N=P+(P-N)=sum d_i+sum(d_i)_+`, while `a=p,b=n` at the minimum.
Consequently the linear objective

`L(x,U,r,a,b)=2W(z;x)-cover(O;x)+sum d_i+sum r_i+a+b`

has a strictly negative feasible value exactly when this fixed exit table
has a strictly negative certified budget against O. For any feasible point,

`2W-OPT_m+C(M-u) <= L`,

because `OPT_m>=cover(O)`, because `M<=U`, and because C is coordinatewise
nondecreasing. Thus an exact rational feasible point with L<0 is already
a valid signed-repair seed. No exact-M enumeration or proof that O is an
optimal comparison tuple is necessary for that certificate.

All strictness can be made reviewable in one rational LP: normalize
`W(z;x)=1`, introduce `epsilon>0`, and require `L<=-epsilon`. Any strict
seed has W>0: W=0 plus the final BR condition forces every topic empty.

## Duplicate labels can be quotiented without changing the seed data

The mathematical catalog is a set of subsets of customers. Optimizing
type masses can make two initially distinct labels cover exactly the same
positive-mass customers. This does not invalidate a seed, but one must
reconstruct a quotient strategy rather than literally project a strategy
map that might distinguish the duplicate labels.

Let q map each label to its coverage set. For every labeled prefix h,
the set of physical terminal tuples realizable by a complete pure SPE
equals the set for the quotient prefix q(h). Also the current genuine
thresholds M are equal.

Proof is induction on the number of remaining players. The terminal case
is immediate. For a labeled current action a with q(a)=A, the induction
hypothesis identifies the physical SPE continuation set after (h,a) with
that after (q(h),A). The current player's payoff depends only on A and
the physical terminal tuple, hence the current minimum ell is the same.
Taking the maximum over all labeled actions merely repeats identical
ell values and so gives the quotient M. The exact SPE recursion retains
precisely each child outcome whose current payoff is at least M. Taking
the union over labeled actions again only duplicates the same union.
This proves equality at the current prefix, including arbitrary ties.

Consequently W, OPT, all target u_i, all genuine M_i, and B+C(g) survive
quotienting duplicate coverage labels. The finite exit table used for a
certified bound U also survives in the required existence sense: each
forced labeled tail has a quotient tail realizing the same physical
terminal outcome and current payoff. Independent choices of these tail
SPEs are allowed. No unavailable history signal or perturbation of ties
is required.

Thus pairwise positive separation constraints are optional in the LP.
If one nevertheless wants an LP answer with distinct labels already in
place, use

`sum_{types containing exactly one of a,b} x_type >= epsilon`

for every distinct pair a,b. They can exclude degenerate fixed supports,
so the quotient argument is the more general implementation route.

## Independent check of the directed indexed-primal projection

Read `construction/indexed_projection_seed.py` from the current actor.
Its ten labels are ABCDE plus five comparison labels T1,...,T5; it drops
the old fixed reply labels UVWXY. It does not confuse UVWXY with T1,...,T5
or claim that this reduced catalog retains all 437 old rows.

The program's reconstruction uses j from AB_hist[4:], independently
checks AE_hist[4:] and second_hist[8:], and distributes each atom over
all size-j subsets of the five comparison labels. Every binomial(5,j)
divides 10, so its factor 10 and final scale 10D are exact. It checks the
last BR, every forced action including the normal action, and uses the
full true continuation outcome sets. No code-level issue was found in
these definition-critical steps. The reported positive B+C is not a
general nonnegativity result and not evidence that strict seeds do not
exist.

## Remaining mathematical issue and five-player pressure

No new all-input inequality has been proved that pays
`OPT_m <= 2 sum M_i+N+p+n`. The exit-cone LP makes one fixed genuine table
and one rational negative certificate concrete; it does not remove the
need for every tail strategy to be a genuine full SPE.

For m=5 the same formula has four d coordinates and four r variables,
plus the two shared endpoint variables a,b. The exact LP certificate
would still imply a genuine five-player counterexample after signed
repair. No such certificate was found here. No unconditional five-player
half bound follows from this note.
