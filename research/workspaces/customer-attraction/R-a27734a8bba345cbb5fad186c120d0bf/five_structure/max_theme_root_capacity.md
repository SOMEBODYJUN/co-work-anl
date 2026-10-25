# Five-player maximum-theme root capacity cuts

2026-10-25. Status: new analytic necessary inequalities for the exact five-player
model, conditional only on the already independently reviewed binary-background
four-tail theorem cited below. The parent independently reconstructed the two
final integer coefficient rows. No five-player half-coverage proof or SPE
counterexample is claimed. No external review or novelty certification.

## Exact domain

Fix any finite unit-customer instance with one finite nonempty common catalogue
and any complete ordered-history pure SPE with five unit providers. Empty
topics, repeated choices, all off-path histories, and arbitrary history-dependent
ties remain allowed. Let `O=OPT_5`, let `W` be actual root welfare, and let `u`
be the actual first provider's final payoff.

Write `K=max_{S in catalogue}|S|`. This is the **global** largest topic size,
not necessarily the actual root-topic size. If `K=0`, every quantity is zero.
Below assume `K>0`.

At each actual decision node, deviating to a largest topic guarantees at least
`K/5`: every customer's final total load is at most five. Thus each actual
provider earns at least `K/5`, and

`K/5 <= u <= K <= W`.                                                   (1)

The middle inequality follows because a provider's payoff never exceeds the
bare size of its chosen topic. These are inequalities of the given complete
SPE, without any selection or tie convention.

## 1. One true root branch and an integer-load capacity bound

Choose any catalogue topic `T` with `|T|=K`. Force the root to choose `T`, then
follow the **same original SPE** at every later ordered history. Denote the
four prescribed follower topics by `A,B,C,D`, and root payoff by `z`. Root IC
gives `z<=u`; also `K/5<=z<=K`.

For a customer of `T`, write `c` for its final load, so `c` is one of
`1,2,3,4,5`, and `z=sum_{x in T}1/c_x`. Write `V_0` for the followers' total
profit from customers outside `T`, and `V_1` for their total profit from `T`.
These have the exact meanings

`V_0=|(A union B union C union D) minus T|`,

`V_1=K-z`.                                                            (2)

Every follower topic has bare size at most `K`. Hence the followers' outside
coverage is at most their total outside membership:

`V_0 <= 4K-sum_{x in T}(c_x-1) = 5K-sum_{x in T}c_x`.                 (3)

For each `k in {1,2,3,4}` and each integer `c in {1,...,5}`,

`c + k(k+1)/c - (2k+1) = (c-k)(c-k-1)/c >= 0`.                         (4)

The sign is valid specifically because `c` is integral: no integer lies
strictly between `k` and `k+1`. Summing (4) and substituting into (3) proves
the four simultaneous bounds

`V_0 <= (4-2k)K+k(k+1)z`,    `k=1,2,3,4`.                            (5)

In particular, `V_0<=12z-2K` and `V_0<=20z-4K`. These are stronger than
using only the root's crude denominator guarantee. The elementary Cauchy
variant `V_0<=5K-K^2/z` is also valid, but is unnecessary for the integer rows.

## 2. Compare the five optimal complements to this same branch

Fix any optimal indexed tuple `T_1,...,T_5`; labels and topics may repeat.
For a comparator quartet `Q`, define

`R_{1_T}(Q)=sum_x e_x/(1_T(x)+e_x)`,

where `e_x` counts its four comparator memberships and zero numerator means
zero. The reviewed binary-background four-tail theorem states, for **every**
quartet of legal comparator topics, on this prescribed four-tail SPE,

`R_{1_T}(Q) <= a V_0+b V_1`,

`a=1999/1000`, `b=5/3`.                                                (6)

Dependency: R-febfdd131cde4128882ca0edd4d712ba/
`parent/five_root_binary_tail_credit.md`, local statement (1), and its
`independent/binary_tail_review.md`. This document does not silently replace
that theorem by a no-background coverage ratio.

Apply (6) separately to the five quartets `T_{-i}`. For a customer appearing
in `j>=1` optimal indices, the average of its five comparator contributions is

* outside `T`: `4/5` if `j=1`, and `1` if `j>=2`;
* inside `T`: `1-6/[5(j+1)]`, which is at least `2/5`.

For the second formula, the sum is
`j*(j-1)/j+(5-j)*j/(j+1)=5-6/(j+1)`, with the `j=1` zero numerator
interpreted as zero. Customers outside the optimal union contribute zero.
Therefore

`max_i R_{1_T}(T_{-i}) >= (4/5)O-(2/5)|T intersect optimal_union|`

`                         >= (4/5)O-(2/5)K`.                          (7)

All five left sides compare to the **same** follower-profit budget in (6).
Taking their maximum or average introduces no multiple payment of that budget.

## 3. Four simultaneous global-size inequalities

Combine (2), (5), (6), and (7). The coefficient of `z` is
`a*k(k+1)-b>0` for `k=1,...,4`; consequently `z<=u` gives

`(4/5)O <= [a(4-2k)+b+2/5]K+[ak(k+1)-b]u`.                            (8)

In exact integer form the four rows are:

| k | Necessary inequality |
|---|---|
| 1 | `1200O <= 9097K+3497u` |
| 2 | `1200O <= 3100K+15491u` |
| 3 | `1200O+2897K <= 33482u` |
| 4 | `600O+4447K <= 28735u` |

The negative `K` coefficient in the right-side versions of rows 3 and 4 is
essential for the following catalogue-wide consequence.

## 4. Final per-topic linear cuts, requiring no new root state

For **every** catalogue topic `Q`, `|Q|<=K`. Thus rows 3 and 4 imply

`1200O+2897|Q| <= 33482u`,                                             (9)

`600O+4447|Q| <= 28735u`.                                              (10)

These can be applied to any already represented actual topic, branch topic,
or indexed optimal topic. The proof uses the true root deviation to a global
largest topic, even when that topic is absent from the finite representation.
No root branch has been substituted for an incompatible ordered history.

For example, if any represented topic has `|Q|=5u`, (10) forces
`O<=(65/6)u`. The old 437-row obstruction has precisely `|Y|=5u`, and
`O/u` about `20.47`, so these rows strictly separate that relaxed point.
That point was not a complete SPE; separating it does not itself prove half.

## 5. Joint scalar boundary and remaining gap

The binary-tail theorem applied to the actual root topic `A` gives

`2400O <= 5997W-5000u+203|A|`.

Since `|A|<=K`, one may weaken this to

`2400O <= 5997W-5000u+203K`.                                          (11)

Here replacing `|A|` by `K` is safe because its coefficient is positive.
It does **not** assert that the actual root topic is globally largest.

The scalar system (1), `O<=5K`, all four rows (8), and (11) still admits
values above two. With `W=1`, its exact optimum is

`O=83705/36641`, `u=8897/73282`, `K=16741/36641`.

Its objective is about `2.2844627603`; the active rows are (11), `O=5K`,
and the `k=3` row. The exact dual certificate for this scalar optimum is:
take (11) divided by 2400, the `k=3` row divided by 1200, and `O<=5K`
with nonnegative weights, or equivalently eliminate the latter two by
`u>=8897K/33482` and then intersect with `O=5K`. The explicit machine audit
below verifies all primal rows. This is only a diagnostic for these scalar
inequalities; it is neither a feasible full-history SPE nor an assertion about
the sharp game bound.

Thus the capacity cuts supply genuinely new valid rows, but they still need
the represented actual-node and cross-branch IC budgets for half coverage.

## Verification

`audit_max_theme_root_capacity.py` uses exact fractions to check every
`(c,k)` integer identity, every optimal multiplicity `j=0,...,5` and binary
root membership in the complement estimate, the four coefficient rows,
the scalar diagnostic, and separation of the old exact 437-row point.
Finite coefficient checks supplement the complete analytic argument above;
they are not a finite-game replacement for its quantifiers.
