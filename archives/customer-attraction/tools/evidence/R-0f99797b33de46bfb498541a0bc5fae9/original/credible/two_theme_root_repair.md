# Two-theme Cartesian insurance repairs a root-only defect, at sharp cost m+1

2026-10-23; personal research draft and author exact audit. No independent review
or novelty certification. General Q-CAG-HALF remains OPEN.

The earlier conversation reportedly described a construction adding customers and
exactly two themes. That exact construction was **not recovered** in this checkout.
The material actually read was `research/current/customer_attraction/mobius_compiler.md`,
its `compiler_security_barrier.md`,
`R-5d61c5324e744dc0a66133207fcbd010/security/safe_catalog_padding.md`, and
that workspace's `counterexample/coupled_cartesian_family.md`, together with
`R-64201cd12083425899e2d643ec9bc087/next_security/cartesian_limit.md`.
None is the claimed general +2-theme compiler. The following is an independent,
explicit replacement. It doubles the old catalog by a Cartesian product; it
must not be reported as adding only two total themes.

## Exact input and output

Use the current CAG-MODEL. Let m>=2. Fix a complete ordered-history policy tau
whose restriction to every positive-depth subgame is a pure SPE. Its root action
is prescribed as A, and need not be optimal. Let u be its actual first-player
payoff and let d_B be that player's payoff when choosing B at the root and then
following tau's original complete suffix. Put

    Delta = max_B d_B - u >= 0.

The inequality includes B=A. For rational s>0 with s>=Delta, take disjoint new
customer sets X,Y of sizes 2s,(m-1)s. The enlarged common catalog is

    { B union X, B union Y : B in the old catalog }.

For rational sizes scale all old/new multiplicities by one common positive
integer. This is still a finite game of distinct unit customers and m unit
providers. For Delta=0 the old policy is already a complete SPE; no repair or
new customers are necessary.

**Repair theorem.** There is a complete pure SPE with old-coordinate actual path
exactly tau's path and insurance-coordinate actual path X,Y,...,Y. Its actual
root payoff is u+2s, and

    W_new = W_old + (m+1)s,
    OPT_new,m = OPT_old,m + (m+1)s.                 (1)

All positive-depth histories, including repeated themes and arbitrary cross-
coordinate deviations, are part of the construction below.

## Three complete insurance continuations

Normalize s=1. Fix the insurance root action.

* H after root X: every subsequent player chooses Y at every history.
* L_X after root X: the second player chooses X. At every history of length at
  least two every remaining player chooses Y, including histories whose second
  player instead chose Y.
* L_Y after root Y: if no X has occurred choose X; otherwise choose Y.

These are specifications on all ordered histories below their indicated root,
not just actual paths.

For H, let a>=1 be the number of earlier X choices at any history. Choosing Y
and following H gives final Y count m-a and payoff (m-1)/(m-a)>=1. Deviating to
X and then following H pays 2/(a+1)<=1. Thus every H node is optimal.

For L_X, every node of depth at least two is an H-type node with at least one
previous X, so the same comparison applies. At the second player, choosing X
pays 1 (two X in total); choosing Y gives the all-Y continuation after the
original root X and also pays 1. This checks the only additional node.

For L_Y, any history already containing X is again an H-type node. Before the
first X, choosing X gives payoff 2, because all subsequent choices are Y. If a
nonfinal player instead chooses Y, the next player chooses the first X and
all others Y, so this deviator pays 1. If the final player chooses Y, there
are m Y choices and the payoff is (m-1)/m<2. This checks every other node.

Consequently the root insurance payoffs are exactly

    H(X)=2s,  L_X(X)=s,  L_Y(Y)=s.                 (2)

## Joint policy and every deviation

At the joint root prescribe (A,X). After this joint root use the product of
old tau restricted to root A and H. After any other joint root (B,X), use old
tau restricted to B and L_X; after any root (B,Y), use old tau restricted to B
and L_Y. Each of these root branches is a separate ordered-history subtree.

Within a selected branch, the old policy reads only the old-coordinate
history and the insurance policy only the insurance-coordinate history.
Their subsequent gains add across coordinates. Each component is a complete
suffix SPE, so every simultaneous tuple deviation is nonprofitable. This is
the exact place where product factorization is used: only below the root,
where no further switch of the selected component policy is allowed.

At the root the prescribed payoff is u+2s. Every other joint action receives
at most max_B d_B+s=u+Delta+s<=u+2s. Thus the root is optimal as well.
The old root's original best reply is not frozen after a deviation; each
branch uses its actual original suffix, together with its specified complete
insurance suffix.

Both X and Y occur on the actual path, proving W_new in (1). Any enlarged
m-tuple covers at most OPT_old,m old customers and the (m+1)s new customers.
Conversely realize an optimal old m-tuple and assign X to at least one slot
and Y to another (m>=2). This covers both insurance groups and proves OPT_new.

## The exact half-counterexample threshold

The compiler preserves the old welfare gap OPT-W but increases both sides'
absolute coverage. It yields a Q-CAG-HALF counterexample precisely when

    OPT_old,m - 2 W_old > (m+1)s.                  (3)

At its minimum repair size s=Delta>0, the necessary and sufficient threshold
for this particular compiler is the strict inequality with (m+1)Delta.
No old root-only plan satisfying (3) has been found here. In particular this
is a complete compiler, not a half counterexample.

## Sharp cost within all two-theme independent insurers

Here the insurer may use any two coverage themes, arbitrary common overlap,
and any history-dependent selection of their pure suffix SPEs. The old and
insurance coordinates must remain independent below each root branch. We
only count the number C of newly added insurer customers; hidden additional
resources or policies coupling coordinates after depth one are excluded.

For any fixed insurance root action, the range of that root's possible
payoffs over all complete suffix SPEs is at most C/(m+1). Therefore any such
insurer fixing a root defect Delta>0 necessarily has

    C >= (m+1)Delta.                              (4)

Our construction attains equality. In particular this independent two-theme
mechanism cannot achieve completion cost below 2Delta for any m>=2, even
though other completion mechanisms are not ruled out.

Here is a self-contained proof of the range assertion. The common customers
contribute exactly c/m to every payoff because every player chooses one of
the two insurance themes; they do not affect any incentive or payoff range.
Let the two private petals have sizes x,y>0. If a previous prefix has a X and
b Y choices, define

    t=(m+1)x/(x+y), l=ceil(t)-1, h=floor(t),
    clip(z)=max(a,min(m-b,z)).

The **complete set** of possible final X counts in a pure suffix SPE is

    R(a,b)={clip(l),clip(h)}.                       (5)

This follows by backward induction, with the singleton terminal base case.
For a current X choice, the child outcomes are R(a+1,b), and the minimum
credible payoff of a Y deviation is y/(m-min R(a,b+1)). A chosen X-child
count k survives exactly when

    x/k >= y/(m-min R(a,b+1)).

For a current Y choice the surviving condition is

    y/(m-k) >= x/max R(a+1,b).

Substitute the clipped endpoints into these two comparisons. If a>h only
Y survives, with terminal X count a; if m-b<l only X survives, with terminal
X count m-b. In every remaining case the interval [a,m-b] meets [l,h].
The only candidate outside that interval of equilibrium counts is created
by a child endpoint at a+1 or m-b-1; the displayed comparison rejects it
strictly. For each feasible endpoint l or h, its owning child comparison is
exactly l>=t-1 or h<=t. Hence precisely the clipped endpoint(s) survive.
This proves (5), including integral-t ties and all repeated off-path prefixes.

At the fixed root X, a=1,b=0. A positive payoff range occurs only when t=j
is an integer with 2<=j<=m. Its two possible X counts are j-1 and j. Thus

    range = x/(j-1)-x/j
          = (x+y)/[(m+1)(j-1)]
          <= (x+y)/(m+1) <= C/(m+1).

If only one endpoint survives the range is zero. Zero-size petals follow
separately: a player with a positive petal strictly avoids the zero petal
whenever it can, and the root payoff has no continuation range. Swapping X
and Y proves the assertion for either root insurance action.

To infer (4), compare the repaired root's chosen joint action (A,Z) against
the original maximizer B* paired with the **same** insurance root action Z.
Their base-coordinate payoff gap is Delta, so their insurance-coordinate
payoff difference must be at least Delta. Both suffixes are genuine pure
insurance SPEs from the identical insurance root, and (4) follows.

## Extra-iid first-player bridge: this repair adds no new counterexample

This paragraph records a separate observation supplied by the security relay,
not a proof of any general extra-iid bridge. Let lambda_old be the payoff
of a symmetric iid Nash benchmark with m+1 static providers. In a Cartesian
product a product of component benchmark distributions has summed payoff.
For the insurance component, symmetry and the m+1-provider welfare identity
give lambda_ins<=C/(m+1)=s. The repaired actual root gets u+2s, so

    lambda_new-u_new
      <= lambda_old-u-s
      <= lambda_old-max_B d_B.

If the right side is positive, choosing a maximizing old root B already
makes the old positive-depth policy a genuine full SPE with first payoff
max_B d_B<lambda_old. Thus the present repair cannot turn an old nonexample
into a new extra-iid first-player counterexample. No inference is made about
other joint symmetric equilibria or insurance mechanisms.

## Reproduction, complete certificates, and limits

Run from the repository root:

    python3 research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/credible/audit_two_theme_repair.py

The standard-library Fraction implementation checks formula (5) against
set-valued backward induction for m=2,...,20, x,y=1,...,20, **every** prefix:
706,800 exact state comparisons, with 7,600 root-range comparisons. It also
checks all ordered histories of H,L_X,L_Y for m=2,...,10.

`two_theme_repair_m{2,3,4,5}_certificate.json` are complete unit-customer
four-topic SPE witnesses, each generated from an old root-only policy with
Delta=1. All actual/alternative actions at every ordered history are checked
with Fraction. The m=5 witness has 341 ordered decision histories, 1,364
comparisons, W=OPT=17, root payoff 3, and minimum incentive slack zero. Its
purpose is exact full-tree regression; its welfare is optimal.

`probe_root_relaxed.py` is a separate finite diagnostic of the stronger
candidate that every positive-depth SPE plan already obeys 2W>=OPT_m.
The completed 320-case seeded batch found no counterexample. The report
`root_relaxed_probe.json` records exact best ratios and inputs; it proves no
general result. The same batch tested the speculative **all-catalog**
root-payoff range bound C/(m+1), finding no violation; only the two-theme
bound above has been proved. Neither negative result licenses more of the
same random scanning as a new mechanism.

The saved witnesses also replay independently via
`verify_saved_certificate.py`, which reads their unit-customer/action data
and imports neither this construction nor the canonical solver. All 1,808
comparisons in the four certificates pass; results are in
`saved_certificate_replay.json`.

A further **finite, deliberately structured** diagnostic is
`root_relaxed_cone_probe.py/json`: start from a zero-root, all-big equal-welfare
instance for each m=3,4,5, generate two complete positive-depth policies, then
optimize all nonnegative customer incidences with only positive-depth SPE
rows. The root row is omitted by rebuilding the row set from positive-depth
histories, not by subtracting a deduplicated root row (which could accidentally
remove a necessary repeated row). Every one of the 30 m-topic comparison LPs
has exact primal/optimal-dual value 2. Saved data contain all six complete
action graphs and each rational primal/dual. This excludes a violation only
in those six cones; it neither requires the root theme to remain empty nor
proves the general positive-depth-only half candidate.
