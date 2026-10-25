# Root-to-terminal rigidity from a nearly saturated topic

Status: new self-contained derivation, pending independent review. This is a
valid inequality for every finite common-catalog complete-history pure SPE,
with arbitrary ties, repeats, empty topics and unit customers. It does **not**
yet close five-player half coverage. It is qualitatively outside the old
557-row model: it eliminates the real root-deviation branch, rather than
expanding queries at already-recorded final-two histories.

## Exact statement

Let m>=2, let u be player 1's actual final payoff in a fixed full-history pure
SPE, and fix any catalog topics T,Q. Put

    delta_T = m u - |T|,
    F_T(Q) = |Q\T| + |Q intersect T|/m.

Then delta_T>=0 and

    F_T(Q) <= u + (3m-4)/2 * delta_T.                 (RIG)

For m=5 this is the linear necessary row

    (57/2)u - (11/2)|T| - F_T(Q) >= 0.             (RIG5)

No assumption says T is actually selected, maximal, optimal, nonempty, or
distinct from Q. The same inequality holds for each ordered-history-dependent
choice of ties, since every action below comes from the fixed original
strategy. At m=1, the separate trivial statement is |Q|<=u.

## The real branch and four legitimate inequalities

Force player 1 to choose T and thereafter follow the same full strategy. Write
the resulting leaf as (T,B_2,...,B_m), its first-player payoff r, its last-player
payoff v, and the last-player payoff from querying Q while fixing the other
m-1 actions as k. Root IC and genuine last-node IC give

    r <= u,                 v >= k.                 (1)

For every catalog topic B, root deviation to B followed by its own real
continuation yields at least |B|/m. Hence

    |B_j| <= m u   for j=2,...,m.                    (2)

The branches witnessing (2) need not be the displayed T branch, and no
continuation is frozen in deriving them. This common upper bound over every
catalog topic is precisely what the new cross-node argument uses.

## Pointwise transfer inequality

Fix one customer, and write

    p = 1_T,  z = 1_(B_m),  q = 1_Q,
    n = sum_(j=2)^(m-1) 1_(B_j),  c = p+n+z.

Here n is an integer in [0,m-2]. A zero numerator over c=0 is assigned zero.
In particular (z-p)/c means z/c-p/c and is zero when c=0. The following
pointwise inequality is the full algebraic step:

    q/[1+(m-1)p] - q/(1+p+n) + (z-p)/c
    <= (n-(m-2)p)/2 + (z-p)
       + m(m-2) [p/c-p/m].                          (3)

All denominators in query terms are strictly positive.

For p=0, the left side is q*n/(n+1)+z/(n+z), and the right side is n/2+z.
If z=0, n/(n+1)<=n/2 for n>=1, while n=0 gives zero. If z=1, the left
side is at most [n+1]/[n+1]=1 and the right side is at least 1.

For p=1, the q coefficient on the left is 1/m-1/(n+2)<=0, so the worst
case is q=0. For z=0 the right side minus left side factors exactly as

    [(n+1-(m-1))(n+1-2(m-1))] / [2(n+1)] >= 0.     (4)

Both factors in the numerator are nonpositive because n+1<=m-1. For z=1
that residual is

    [(m-2-n)(2m-n-6)] / [2(n+2)] >= 0.             (5)

When m=2 the first factor is zero. When m>=3, either the first factor is zero,
or n<=m-3 and then 2m-n-6>=m-3>=0. This proves (3) for all m>=2, rather
than extrapolating from finitely many values of m.

## Summation and elimination of the genuine root branch

After summing (3) over customers its left side is

    F_T(Q) - k + v - r.

It is at least F_T(Q)-r by v>=k. The right side becomes

    (1/2) sum_(j=2)^(m-1) (|B_j|-|T|)
       + (|B_m|-|T|) + m(m-2)(r-|T|/m).

By (1)-(2), each displayed size difference is <=delta_T and
r-|T|/m<=delta_T/m. Therefore

    F_T(Q) <= r + [(m-2)/2 + 1 + (m-2)] delta_T
            <= u + (3m-4)/2 delta_T,

as claimed. This proof uses neither a static Nash assumption nor the
intermediate players' IC. Full SPE supplies more information than the part
used here.

## Saturated-topic meaning and exact exclusion of the frozen 557 point

If |T|=m u, then root deviation to T can earn at least |T|/m=u, so it earns
exactly u. Every T customer must be covered by all m players in that real
branch, since each contributes at least 1/m. Every B_j therefore contains T.
But |B_j|<=m u=|T|, forcing B_j=T as customer sets. At the genuine last
node, all m-1 earlier actions are T, giving F_T(Q)<=u for every Q.
Consequently **all topics with size m u are identical sets**.

The frozen 60-atom source
`R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_primal_overlap1.json`
(SHA256 11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825)
has |C|=|D|=|U|=|V|=|W|=|X|=5u but different fixed-topic memberships.
It cannot be completed to a full SPE preserving those marginals. Exact
(RIG5) slack for T=D,Q=E is

    -94973318525132495345880313189888225389373576366303830999959 /
      266975572915498442232620349200554253524135992119166676693673
    = -0.3557378582916007... .

This exclusion does not depend on unresolved cross-family topic matching.
Both D,E memberships and actual root payoff already occur among fixed bits.
Of the 100 ordered fixed-topic pairs, 66 violate (RIG5). This is not an
SPE counterexample and does not certify the augmented relaxation's optimum.

## An immediate coverage corollary and remaining five-player obligation

For any m comparison topics with union O, summing (RIG) gives

    |O| - (m-1)|T|/m <= m u + m(3m-4)/2 * delta_T.

Thus, with O an optimal union,

    OPT_m <= (2m-1)u
             + [m(3m-4)/2-(m-1)/m] delta_T.         (6)

For m=5, (6) is OPT_5<=9u+(267/10)delta_T. In particular a saturated topic
forces OPT_5<=9u, the all-big ratio's natural root scale. This is useful
near root-size saturation but does not bound delta_T on an arbitrary SPE.
A five-player half proof still needs a joint nonnegative payment of
2W-OPT_5 using these rows and actual/other genuine nodes. A parent branch
is checking whether (RIG5), including all fixed-topic pairs and indexed
aggregates, closes the full old histogram universe; no success is assumed.

## Evidence and scope

`audit_root_rigidity.py` imports no optimizer, strategy evaluator or old row
implementation. It checks (3)-(5) using Fraction at every p,n,z,q for
m=2,...,100 (39,600 states), and independently evaluates all 100 fixed-topic
rows on the frozen point. `audit_root_rigidity.json` stores the exact results.
The all-m proof is the displayed factorization; the finite audit checks code
and arithmetic only. New inequality and point exclusion await independent
mathematical review; no external review or novelty assertion is made.
