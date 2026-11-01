# Arbitrarily many topics can be necessary to preserve one ordered SPE outcome

Status: symbolic all-length bridge obstruction with a definition-level exact
Python audit. This is not a half-coverage counterexample. It strengthens the
existing literal-policy reply-closure obstruction by allowing the entire
continuation policy to change, removing all ties, and retaining the original
optimal pair. It remains an **ordered-outcome** preservation obstruction; a
weaker welfare-only or unordered-multiset compression is not disproved.

## Exact bridge under attack

There is no function f(m) with the following property: for every common-catalog
instance and every complete pure SPE sigma, one can retain at most f(m) topics,
including its actual path topics and some original optimal m-tuple, such that
the same **ordered** actual outcome is realized by a complete pure SPE in the
retained common-catalog game. This holds already for m=2 and games with a
unique complete pure SPE and no ties at any decision history.

Indeed, the construction below has arbitrarily many topics and its original
ordered SPE outcome cannot be preserved in **any proper subcatalog** containing
the actual topics. Those two actual topics are also its unique optimal pair.

## Explicit unit-customer family

Fix an integer L>=3. Set

    C = 20(L+1)^2,        p = C-1,        x_i = C+3i  (0<=i<=L).

There are L+1 topics T_0,...,T_L. For each unordered pair i<j, create a_ij
distinct unit customers interested in exactly these two topics, where

    a_01 = 2;
    a_(i,i+1) = 6i+6                 (1<=i<=L-2);
    a_(L-1,L) = 6L+4;
    a_ij = 6(i+j)+6                  (j>=i+2).

For each i also create q_i=x_i-sum_(j!=i) a_ij private unit customers interested
in T_i alone. Every a_ij<=12L, so sum_(j!=i) a_ij<=12L^2<C. Thus q_i>0 is an
integer. This realizes |T_i|=x_i and |T_i intersect T_j|=a_ij exactly. Every
topic has private customers, so all topics are distinct and inclusion-maximal.

There are exactly two unit players. Define the symmetric pair potential

    P_ij = x_i+x_j-a_ij/2          (i!=j),
    P_ii = 3x_i/2.

After first topic T_i, the last player's payoff from T_j is P_ij-x_i. Thus
maximizing the row P_ij gives precisely its best response. The first player's
payoff on that pair is P_ij-x_j. This identity is only a two-player calculation;
it does not substitute frozen replies into an earlier SPE deviation.

## Unique full-game replies and root action

Every nonadjacent pair has P_ij=2C-3. The adjacent edge values are

    P_01 = 2C+2;
    P_(i,i+1) = 2C+3i              (1<=i<=L-2);
    P_(L-1,L) = 2C+3L-5.

They strictly increase along the chain. Also

    P_ii <= 3C/2+9L/2 < 2C+2,

by the chosen C. Therefore the unique last-player best reply is

    R(i)=i+1   (i<L),             R(L)=L-1.

The corresponding first-player payoffs are

    u_0 = p;
    u_i = p-2                     (1<=i<=L-2);
    u_(L-1) = p-4;
    u_L = p-1.

Consequently T_0 is the root's unique optimal action. The game has a unique
complete pure SPE, namely root T_0 followed by R at each ordered last-player
history, and its unique ordered actual path is (T_0,T_1). No tie selection is
used anywhere in this construction.

## Every proper subcatalog destroys that ordered outcome

Let A be any proper retained subcatalog containing T_0,T_1. Let ell>=2 be the
smallest omitted index, and write j=ell-1. Then T_(j-1),T_j are retained but
T_(j+1) is omitted. At the last-player history (T_j), the unique best retained
reply is T_(j-1): its adjacent potential exceeds every nonadjacent or diagonal
entry, and the only higher adjacent edge has been removed.

If j=1, the root deviation to T_j followed by this forced reply gives

    x_1-a_01/2 = C+2 = p+3.

If 2<=j<=L-1, it gives

    x_j-a_(j-1,j)/2 = C = p+1.

Either is strictly more than the root payoff p on (T_0,T_1). The full-game
reply T_1 remains uniquely best after T_0 in any retained catalog containing
T_0,T_1, so the payoff of that proposed path is still p. It follows directly
from the root SPE inequality that (T_0,T_1) is not an SPE path in A. Replacing
all continuation choices cannot repair it; the relevant reply is forced.

This argument works for every proper retained subcatalog, including one that
retains arbitrary additional topics beyond the first missing index. It is not
just a failure of deleting one topic at a time or retaining a prescribed policy.

## The actual pair is uniquely optimal

The union coverages of distinct pairs are

    |T_0 union T_1| = 2C+1;
    |T_i union T_(i+1)| = 2C-3     (1<=i<=L-2);
    |T_(L-1) union T_L| = 2C-7;
    |T_i union T_j| = 2C-3(i+j)-6 (j>=i+2).

A repeated topic covers at most C+3L<2C+1. Hence the actual unordered pair
{T_0,T_1} is the unique optimum, and W=OPT_2=2C+1. Keeping an optimal tuple
therefore supplies no new topics beyond the actual path in this example.

There is an important limit: the reduced two-topic game can realize the
**reverse** ordered outcome (T_1,T_0), which has the same unordered multiset and
welfare. Thus this construction does not rule out compression that only
preserves the terminal multiset or gives a welfare comparison. It specifically
rules out a uniform catalog-size reduction preserving the original ordered SPE
path, even when completely new continuations are allowed and all original
optimal actions are retained.

## Connection to earlier boundaries

The previous `R-a0bb57fa24044a8794bc7991918a19c6/tree_transport/reply_closed_catalog.md`
shows an arbitrarily long cyclic closure for a fixed original policy using
disjoint equal-sized singleton topics and arbitrary ties. That policy can be
replaced in a small catalog. Here every full-game decision is strict and every
proper catalog fails under **all** replacement policies preserving the order.

The exchange lane's five-customer example shows one outside topic can be
necessary when deleting to the actual support. Here an arbitrarily long chain
of outside topics is mandatory, with two players fixed and even with the
optimal tuple already retained. Neither statement by itself advances the half
bound: this example has optimal welfare, and the obstruction concerns a
stronger outcome-preserving reduction.

## Reproduction

Run `python3 research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/independent/check_strict_compression_boundary.py`.
It computes payoffs directly from the nonnegative unit-customer types with
Fractions, checks strict replies and the unique root, enumerates all retained
subcatalogs containing T_0,T_1 for the stated finite lengths, and verifies the
first-missing-index profitable deviation. The all-L proof is the explicit
calculation above, not a no-counterexample scan.
