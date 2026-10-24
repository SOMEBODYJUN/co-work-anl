# Independent review: intrinsic homogeneous best-response screen

2026-10-24. Contract reviewed: `../construct/homogeneous_screen.md`. The
reviewer derived the central inequalities independently from the stated
hypothesis before reading the constructor's note. Verdict: valid screening
lemma; no fatal objection. It is not a general half-coverage proof.

## Exact hypothesis and catalogue consequence

Fix m>=1 in the original common finite nonempty catalogue, with unit clients
and unit providers. Let B be a legal topic that is a last-player best
response against m-1 preceding copies of itself. This is an intrinsic
catalogue condition for the specified m; no selected strategy or tie rule is
part of the hypothesis.

Against B^(m-1), choosing B gives |B|/m. Choosing T gives

    |T\B| + |T intersect B|/m.

Thus the hypothesis is exactly

    m|T\B|+|T intersect B| <= |B|    for every legal T.   (H)

As m>=1, (H) also gives |T|<=|B| for every T. Therefore

    K=max_T |T| = |B|.

This slightly sharpens the wording of the constructor's chain, which only
uses |B|<=K. It makes no difference to the validity of that chain.

For a nonempty comparison tuple of at most m topics, repeat one of its own
topics to produce m slots without changing the union O. Summing (H) and
using the fact that incidence multiplicity dominates union membership gives

    m|O\B|+|O intersect B| <= m|B|.

If the comparison tuple is empty, O is empty and the same inequality is
immediate. Consequently

    |O| <= |B|+(1-1/m)|O intersect B|
         <= (2-1/m)|B| = (2-1/m)K.

Maximizing over comparisons proves OPT_m<=(2-1/m)K. The constructor's
instruction to pad with an arbitrary legal topic can enlarge O. The summed
incidence inequality still dominates the original O, so its conclusion is
valid; repeating a comparison topic as above avoids that needless ambiguity.

## Every actual full-history pure SPE

At any actual decision position, deviation to a size-K topic gives at least
K/m regardless of all later prescribed action changes: each of its K unit
clients has terminal congestion at most m. Genuine SPE optimality therefore
gives u_i>=K/m at every actual position. Summation gives W>=K.

Under (H), every complete pure SPE of this catalogue satisfies

    OPT_m <= (2-1/m)K <= (2-1/m)W.

Thus a genuine half counterexample must violate (H) at every legal B:

    max_T [m|T\B|+|T intersect B|] > |B|.

No claim follows about catalogues satisfying this strict failure condition;
it is only a necessary screen for a possible counterexample.

## Root-only source plans and exact margin

Consider a complete plan that is SPE at every positive-depth subgame, with
actual root payoff u_1, terminal welfare W, true root deviation payoffs d_T,
and Delta=max_T d_T-u_1. Its prescribed action is among the legal choices,
so Delta>=0.

For every actual position i>=2 the genuine local IC gives u_i>=K/m. At the
root, forcing a size-K topic gives d_T>=K/m without any rationality
assumption on its continuation. Hence

    W+Delta = (u_1+Delta)+sum_(i>=2)u_i >= K.

Under (H), therefore

    OPT_m-2W-3Delta
      <= (2-1/m)(W+Delta)-2W-3Delta
       = -W/m-(1+1/m)Delta <= 0.

Every inequality here is within the original unit-provider model. Scaling
rational type multiplicities to integers produces distinct unit clients and
preserves these homogeneous inequalities; it does not scale provider weights.

When m>=2, a fixed source strategy prescribing B after the length-(m-1)
homogeneous history B^(m-1) satisfies (H) throughout its genuine source IC
cone: that last decision is at positive depth. This justifies syntactic
pruning of such cones before numerical optimization. At m=1 the history is
the root and is not assumed optimal in a root-only source, so this syntactic
pruning inference must not be applied there.

## All boundary cases

* m=1: (H) says B is a maximum-size topic. The catalogue bound is exactly
  OPT_1=K=|B|, and every full SPE has W=K. For an arbitrary root-only source
  Delta=K-W, so W+Delta=K and the displayed source-margin bound is exact.
  The existing constant-3 compiler remains an m>=2 construction; this
  m=1 algebra does not invoke it.
* B empty: choosing T against copies of B gives |T|. Condition (H) forces
  every legal topic empty. Then K=OPT=W=Delta=0 for every source plan and
  all inequalities read 0<=0.
* Zero clients: every legal topic is empty, covered by the preceding case.
  No ratio or division by K,W,Delta is used.
* Empty topics in a nonzero catalogue remain legal deviations. They
  contribute zero, and do not affect maxima, padding, or any argument.
* Repeated topics and all history-dependent ties are retained. Only one
  final best-response property is hypothesized, and no selected continuation
  or homogeneous tie choice is assumed for the every-SPE conclusion.

The screen gives a correct symbolic exclusion and a corrected source-margin
upper bound. It does not settle the general claim, and finite failures to
find an unscreened source do not strengthen it.

## General comparison population r and the stronger half screen

The catalogue calculation admits an independent generalization, without any
new special-case game project. Fix the actual provider count m>=1, and an
auxiliary integer r>=1. Suppose some topic B is a best response against r-1
copies of itself. This auxiliary homogeneous profile belongs to the same
catalogue but need not have the actual population m. The exact hypothesis is

    r|T\B|+|T intersect B| <= |B|    for every legal T.

It still gives K=|B|. Summing over m comparison slots now gives

    r|O\B|+|O intersect B| <= m|B|,

and therefore

    OPT_m <= [m/r+(1-1/r)]|B|
          = [1+(m-1)/r]K.                                 (R)

The coefficient 1-1/r is nonnegative, which justifies replacing
|O intersect B| by |B|. Empty comparisons, empty B, and zero clients are
handled exactly as above; no positive welfare assumption is needed.
At m=1, (R) is OPT_1<=K, independent of r.

For every actual full pure SPE, (R) and W>=K give

    OPT_m <= [1+(m-1)/r]W.

In particular, for m>=2 the weaker auxiliary population r=m-1 already
screens half coverage, since its coefficient is exactly 2. Every genuine
half counterexample must therefore satisfy the stronger strict catalogue
condition

    max_T [(m-1)|T\B|+|T intersect B|] > |B|
    for every legal B.

For a root-only source plan, let alpha=1+(m-1)/r. The same source floor gives

    OPT_m-2W-3Delta <= (alpha-2)W+(alpha-3)Delta.

At r=m-1 this is at most -Delta, so such catalogues cannot supply a positive
constant-3 source margin either. At r=m it recovers the sharper original
bound -W/m-(1+1/m)Delta.

This is an intrinsic catalogue screen. The original source-cone syntactic
pruning rule still uses the genuine last decision at depth m-1 and certifies
the r=m hypothesis. Prescribing B at an earlier history of m-2 copies does
not automatically certify the auxiliary r=m-1 static best-response condition:
there is still a strategic follower whose genuine continuation can change.
No extra pruning rule is asserted without separately checking that condition.
