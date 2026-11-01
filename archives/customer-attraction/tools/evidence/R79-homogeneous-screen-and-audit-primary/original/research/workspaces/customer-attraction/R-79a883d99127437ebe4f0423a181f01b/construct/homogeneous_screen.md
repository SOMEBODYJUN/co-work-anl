# Homogeneous terminal best-response screen for the general counterexample attack

2026-10-24. This is a universal necessary condition on a genuine counterexample,
not a proof of Q-CAG-HALF. The main claim remains OPEN. The original observation
was that a used topic whose homogeneous terminal history repeats itself blocks
a bad source cone; root strengthened it to the intrinsic catalogue statement
below. The independent-audit agent independently reconstructed both inequalities.

Use the exact common-catalogue, unit-customer, unit-provider model. Let m>=1,
K=max_{T in S}|T|, and let O be the union of any at most m comparison topics.

## Intrinsic catalogue statement

Suppose some legal topic B is a last-player best response to m-1 preceding
copies of B. No condition is imposed on the strategy's tie selection, or on
whether an equilibrium path uses B. This assumption is exactly

    m|T\B|+|T intersect B| <= |B|     for every legal T.       (1)

If the comparison is empty its union is empty and the conclusion is immediate.
Otherwise, if it uses fewer than m topics, repeat one of its selected topics
until it has m slots, preserving O. Summing (1), using that the sum of incidences dominates
the corresponding union on and off B, yields

    m|O\B|+|O intersect B| <= m|B|.                          (2)

Consequently

    |O| <= |B|+(1-1/m)|O intersect B|
        <= (2-1/m)|B|.                                       (3)

This proof retains any empty topics and zero-customer case. For m=1, (1) simply
says that B is a maximum-size topic and (3) is the exact optimum bound.
In fact (1) implies |T|<=|B| for every T for every m, so K=|B|.

## Every full-history pure SPE

At every actual position, deviating to a topic of size K gives at least K/m:
each of its clients has final congestion at most m, regardless of the complete
history-dependent continuation. Thus every actual payoff is at least K/m,
and W>=K. Combining with (3) gives

    OPT_m <= (2-1/m)|B| <= (2-1/m)K <= (2-1/m)W.             (4)

Hence a genuine half counterexample necessarily satisfies the following strict
condition for **every** catalogue topic B:

    max_{T in S} [m|T\B|+|T intersect B|] > |B|.              (5)

This is intrinsic to the catalogue. It is stronger than saying a given strategy
must switch topics at every homogeneous last-player history.

## Root-only source plans and the constant-3 insurer interface

Let m>=2. A source plan tau is SPE at every positive-depth subgame; its root
may prescribe a suboptimal topic. Let u_1 be its actual root payoff, d_T the
root payoff after forcing T and following tau thereafter, and

    Delta=max_T d_T-u_1 >=0.

The inequality is nonnegative because the prescribed root action is among T.
Every actual player after the root still gets at least K/m by positive-depth
optimality. Also max_T d_T>=K/m. Therefore

    W+Delta >= K.                                          (6)

If the intrinsic best-response hypothesis (1) holds, then

    OPT_m-2W-3Delta
      <= (2-1/m)(W+Delta)-2W-3Delta
       = -W/m-(1+1/m)Delta <=0.                            (7)

Thus this catalogue cannot supply a positive source margin to the existing
constant-3 insurer compiler. Rational source weights can be scaled to different
unit clients before applying the compiler; (1)--(7) are homogeneous and survive
that scaling. No compilation or full SPE counterexample is asserted here.

For a fixed source strategy cone, the syntactic condition

    tau(B,...,B)=B at the history of length m-1

forces (1) throughout that cone because this is a positive-depth genuine IC.
It is therefore an exact symbolic pruning condition before any numerical LP.
The source attack script in this directory implements that condition.

## Scope of the residual attack

Condition (5) does not prove or disprove half when it holds. In particular,
catalogues can fail the homogeneous test at every topic. The attack must then
exploit credible branching away from every homogeneous topic. Finite LP
failures in such cones are only negative discovery outcomes, not a theorem,
not an impossibility result for counterexample construction, and not evidence
that the general claim is proved.

## Independent-audit strengthening: arbitrary static replication count

The independent-audit agent subsequently observed, and root independently
checked, that the intrinsic argument does not require the replication count
to equal the actual player count. Let r>=1 be an integer, and suppose B is a
best response against r-1 copies of itself in the corresponding static query:

    r|T\B|+|T intersect B| <= |B|     for every T.             (8)

Again K=|B|. Sum (8) over the m comparison slots to get

    r|O\B|+|O intersect B| <= mK,
    |O| <= [1+(m-1)/r]K.                                   (9)

The last step uses r>=1 and |O intersect B|<=K. In particular, for actual
m>=2, r=m-1 already proves OPT_m<=2K<=2W for every full SPE, and gives

    OPT_m-2W-3Delta <= -Delta                               (10)

for every positive-depth SPE source plan. Therefore the stronger intrinsic
necessary condition for a genuine half counterexample is

    max_{T in S} [(m-1)|T\B|+|T intersect B|] > |B|
    for every catalogue topic B.                           (11)

This remains a general counterexample screen. For r=m-1 the query is auxiliary,
so its best-response property cannot be inferred merely from a prescribed
last move in the original m-player tree. The script's symbolic strategy-cone
prune still uses the directly justified r=m case; (11) can instead screen an
actual catalogue or an exact proposed witness.
