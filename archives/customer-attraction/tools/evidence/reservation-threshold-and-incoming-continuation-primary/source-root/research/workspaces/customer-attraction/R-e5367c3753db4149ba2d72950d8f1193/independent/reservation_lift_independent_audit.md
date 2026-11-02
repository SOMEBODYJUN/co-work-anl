# Independent audit: literal disjoint reservation lift

2026-10-24. Independently reconstructed from the statement supplied by root,
before reading the proposed proof. The conditional menu closure below is
proved. It does not prove the universal old menu inequality, the general
path-menu conjecture, or Q-CAG-HALF.

## 1. Objects and the conditional statement

Let an arbitrary old common-catalogue game have n>=1 providers and a fixed
complete-history pure SPE sigma. Its actual terminal tuple is z, with welfare
W. For each actual old position i and legal old forced action A, let Z_i(A)
be the full old n-provider terminal tuple obtained by fixing the actual
prefix, forcing A, and following the original sigma thereafter. Set

    K_i(T,A) = sum_(x in T) 1/[1+c_x(Z_i(A))],
    psi_i(p) = min_(A in S) sum_(T in S) p_T K_i(T,A),
    M = max_(T in S) sum_(x in T) 1/[1+c_x(z)].

Assume the universal old inequality

    sum_i psi_i(p) <= W                         (U)

for every distribution p on the old catalogue. Introduce a topic B consisting
of J new unit customers, disjoint from all old customers. Let sigma' be any
complete-history pure SPE of the n+1-provider enlarged game such that:

* its actual first action is B;
* at every history (B,h), with h consisting only of old actions, it literally
  prescribes the old action sigma(h).

No restriction is needed on other histories beyond their being part of a
complete SPE. The lifted actual tuple is (B,z), with welfare W'=W+J.

Then the two scalar assumptions

    M <= J,       (n-1)J/2 <= W                 (S)

imply the lifted universal inequality U'. If in addition M<=W/n, then the
actual lifted insertion cap satisfies M'<=W'/(n+1).

The proof uses only the stated literal subdomain. It neither freezes
continuations after a deviation to B at an old position nor assumes that
these other continuations retain the old strategy.

## 2. Independent proof for every query distribution

Write alpha=p'(S), beta=p'(B)=1-alpha. If alpha>0, let p be the old conditional
query distribution p_T=p'_T/alpha.

For the new first position, use its forced action B in the minimum defining
psi'_1. This is the actual full tuple (B,z). An old query has its unchanged
old insertion value, while a B query receives J/2. Consequently

    psi'_1(p') <= alpha M + beta J/2.           (1)

At the position corresponding to old i, restrict its minimization to old
forced actions A. Literal reproduction says that every such full terminal
tuple is exactly (B,Z_i(A)). Hence

    psi'_(i+1)(p')
      <= min_A [alpha sum_T p_T K_i(T,A) + beta J/2]
       = alpha psi_i(p) + beta J/2.            (2)

The equality is valid because alpha>=0 and the B contribution is independent
of A. When alpha=0, (2) is read directly as psi'_(i+1)<=J/2; no conditional
distribution p needs to be defined. The old catalogue is nonempty, so there
is always an old forced-action column available.

Summing (1)-(2) and invoking U gives

    sum_j psi'_j(p')
      <= alpha(W+M) + beta(n+1)J/2
      <= alpha(W+J) + beta(W+J)
       = W+J.                                 (3)

The two endpoint bounds are exactly the uses of S in this affine estimate.
In particular alpha=1 and alpha=0 are both included. Empty old topics cause
no problem: their query row is zero and all displayed denominators include
the extra 1.

The same reconstruction verifies the proposed weighted form. For any old
position distribution lambda define

    E_lambda(p)=n sum_i lambda_i psi_i(p)-W,
    lambda'_1=1/(n+1),
    lambda'_(i+1)=n lambda_i/(n+1),
    L_z(p)=sum_T p_T sum_(x in T)1/[1+c_x(z)].

Multiplying (2) by n lambda_i, adding the sharper root estimate with M
replaced by L_z(p), and subtracting W+J gives

    E'_(lambda')(p')
      <= alpha E_lambda(p)
         - alpha[J-L_z(p)]
         - beta[W-(n-1)J/2].                    (5)

This is the proposed quantitative closure after exchanging the naming of
old and new query mass. At alpha=0 its old-distribution terms disappear,
so the statement has no hidden support restriction.

At the actual lifted tuple, disjointness gives exactly

    M' = max{M,J/2}.                            (4)

For its old-query part, nM<=W and M<=J imply

    (n+1)M <= W+J.

For its B-query part, the second assumption in S is equivalent to

    (n+1)J/2 <= W+J.

Together with (4), this proves the cap assertion. For n=1 the second scalar
assumption is vacuous, and the same argument remains valid.

## 3. A sufficient full-history SPE construction

This subsection independently reconstructs the advertised credible lift.
It is separate from the conditional closure in Sections 1-2.

Suppose every prescribed old current player's final payoff, at every old
ordered history, is at least eta. Define

    delta_T = min_(S in catalogue) |T intersect S|,
    L = max_(T in catalogue) [|T|-delta_T/2].

For n>=2 assume J>=L and J/2<=eta. For n=1 replace J>=L by the stronger
condition J>=K=max_T |T|. Retain J/2<=eta. Construct a complete lifted policy
as follows:

* At every history with no B, prescribe B.
* At every history with exactly one B, erase B from the ordered history and
  prescribe the corresponding old action of sigma.
* At every history with at least two B actions, select a complete SPE by
  backward induction. These subtrees are closed under extension, so their
  choices can be made consistently once and for all.

At a history with exactly one B, prescribed play thereafter has exactly n
old actions in total. Every old-action deviation remains in this same
literal old game, so its comparison is precisely the old SPE comparison.
A deviation to B yields at most J/2, whatever the subsequent valid subtree
does. The prescribed old action gives at least eta>=J/2. Thus every such
history satisfies all SPE comparisons.

At a history with no B, the prescribed B is the sole B forever after and
earns J. If n>=2 and the current player instead selects an old topic T,
then either another player subsequently selects B, leaving exactly n old
actions, or the current player is last and all n+1 actions are old. In
either case at least one other old action S is present. The deviator's
final payoff is at most

    |T\S| + |T intersect S|/2
      = |T|-|T intersect S|/2 <= L <= J.

This bound needs no assumption about which other old actions the actual
continuation chooses. For n=1 at the root, however, an old deviation is
followed by B and faces no other old provider. Its payoff is |T|, so J>=L
alone is insufficient; J>=K supplies the missing root comparison. The
remaining no-B history already contains one old action, and also satisfies
the weaker intersection bound. Histories with at least two B are SPE by
their construction. This verifies the entire ordered tree, not only the
actual lifted path.

The need for a separate n=1 hypothesis is real. Take one old topic A with
three customers, so eta=3, delta_A=3 and L=3/2. Let J=2. Both J>=L and
J/2<=eta hold. After a first-player deviation from B to A, the last player
strictly prefers B (payoff 2) to A (payoff 3/2). The first player's deviation
then earns 3>2. Hence no literal lift with actual root B exists in this
example, even though the two n>=2 inequalities hold.

These conditions also imply S. Indeed, for any old actual action S_1 and
query T,

    sum_(x in T) 1/[1+c_x(z)]
      <= |T|-|T intersect S_1|/2 <= L <= J.

For n=1 the direct bound M<=K<=J applies as well. Finally W=sum_i u_i>=n eta
and J/2<=eta imply W>=nJ/2>=(n-1)J/2.

## 4. Degeneracy and scope

The finite unit-customer model requires integer J>=0. If the construction
treats B as a distinct new set action, take J>0. When J=0 and the old
catalogue contains the empty topic, B and that old topic are the same set;
one cannot silently use two distinguishable labels in a set catalogue.
Under the sufficient credible conditions above, this zero-J situation
forces every old topic to be empty, so its zero-welfare conclusion can be
handled directly without a distinct reservation action. Empty old topics
with nonzero J are fully covered by the proof.

The lift closure is conditional on U for the old game. It offers no
operation reducing an arbitrary game to a game satisfying U, and hence
does not by itself supply a general half-coverage proof. No computational
claim is needed for the algebraic audit.
