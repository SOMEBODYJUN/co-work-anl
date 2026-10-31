# Targeted attempt at the deletion-relevant factor-two contract

2026-10-24. General-input working note, not independently reviewed. No
novelty claim. Q-CAG-HALF remains OPEN.

The repeat-petal family in `all_history_regret_and_reset.md` is not a
single-deletion replay: it violates the known full-history factor-two
approximation condition at large m. This note therefore tests the stronger,
distinct contract

    full-history forced payoff <= 2 prescribed payoff,
    B = sum_i max_(|h|=i-1) R(h),
    OPT_m-2W <= C B                                    (F2?)

for an absolute C. The full-history factor-two property is guaranteed for
single virtual deletion by the existing `virtual_replay_regret.md`; it is
strictly more structure than a small B alone. The signed refund identity
of actual deletion is still additional structure not imposed in (F2?).

## 1. A general family forces C>=1

For every m>=2 let L=ceil((m-1)/2). Use one theme A consisting of L distinct
customers and m-1 other themes B_1,...,B_(m-1), each a distinct singleton.
All these customer sets are pairwise disjoint. Define a complete plan:

- Every position before the last chooses A at every ordered history.
- The last position chooses a true best reply. To make the rule unique,
  among payoff-maximizing singleton themes choose the least label; choose
  A only when it strictly beats all singleton themes.

This includes every off-path history. The actual leaf is

    A^(m-1), B_1,

with

    W=L+1,           OPT_m=L+m-1.                      (1)

The optimum takes all m disjoint themes once. The last player's actual
singleton payoff is 1, greater than L/m, so the leaf is as stated.

### Full-history factor-two condition

At an arbitrary earlier history, suppose the current player follows the
prescribed A, and write a for the total A count immediately before the
last player. There is at least one A at that point, so among the m-1
singleton themes at least one is still unused: the first m-1 moves include
at most m-2 singleton moves. The last player can therefore obtain singleton
payoff 1.

If the last player also chooses A, its best-reply condition gives
L/(a+1)>1. The current A player has that same final payoff, hence greater
than 1. If the last player chooses a singleton, the current prescribed
payoff is L/a>=L/(m-1)>=1/2. Any forced singleton action by the current
player gives final payoff at most 1, regardless of the last player's new
best reply. Forcing A gives the prescribed branch itself. Therefore every
earlier node satisfies

    max forced payoff <= 2 prescribed payoff.          (2)

The last player's full-history property is exact by construction. More
precisely the entire plan has multiplicative approximation at most
(m-1)/L<=2. No old continuation is frozen in these comparisons.

### Exact full-history additive defect

In the case where the last player chooses A, current prescribed payoff is
greater than 1 and regret is zero. Otherwise current prescribed payoff is
at least L/(m-1) and every singleton deviation earns at most 1. Thus, for
every earlier depth,

    max_h R(h) <= epsilon := 1-L/(m-1).                (3)

At the all-A history of that depth, following A gives L/(m-1). Deviating
to an unused singleton gives payoff 1: all other pre-last players still
choose A, and the final BR chooses A or a different unused singleton,
never that occupied singleton. For m>=3 a different unused singleton
exists; for m=2 the final player strictly prefers the unused A. Thus (3)
is attained at every earlier depth. Last regret is zero. Hence

    B=(m-1)epsilon=m-1-L,
    OPT_m-2W=m-3-L=B-2.                                (4)

For unbounded m, B tends to infinity and (OPT_m-2W)/B tends to 1 from
below. Any absolute coefficient in (F2?) must therefore satisfy C>=1.
The family has an exact final BR at every history and full-history
factor-two approximation; the lower bound does not rely on the
unrestricted approximate plans from the first note.

It does **not** disprove (F2?) with C=1, or any larger C. It is not claimed
to be a deletion replay. With C=1 this family has constant slack two,
before any uniform replication of all customers.

## 2. The targeted analytic attempt and remaining gap

The natural strongest coefficient consistent with this family is

    OPT_m <= 2W+B.                                     (C1?)

It is tempting to combine the factor-two pointwise inequalities with the
additive regret budget, but the following attempt does not close.

For every actual position i, the genuine branch-independent denominator
floor and fractional-cover accounting give

    O <= P_(i-1)+r kappa (u_i+rho_i),
    0<=rho_i<=u_i,
    rho_i<=e_i,          sum_i e_i=B.                  (5)

The second inequality is where full-history factor two enters, and in
fact it needs only the actual nodes. Substituting rho_i<=u_i replaces
kappa by 2 kappa in the product proof, which is weaker than retaining
the weighted errors. Keeping both inequalities gives the valid
regret-weighted product formula from the first note, whose coefficient
1/F_m(m) still grows as m/H_m. Neither operation produces the constant
2 coefficient of W in (C1?). The unclosed step is a genuinely dynamic
relation among different forced continuations, rather than a scalar
comparison between rho_i and u_i at the same prescribed leaf.

Moreover B=0 in (C1?) is exactly the full-history SPE case: every nonnegative
node regret then vanishes. Thus proving (C1?) would already prove the
general Q-CAG-HALF conjecture. It cannot be treated as an already available
robust theorem merely because the deleted strategy is factor-two
approximate. No universal-C proof or counterexample for (F2?) was obtained
in this targeted attempt.

For m=5, the same family has L=2, W=3, OPT_5=6, B=2. It satisfies half
with equality but is not an SPE. This is a substitution in one arbitrary-m
family, not a five-player positive result. The analytic relaxation (5)
still has no unconditional factor-two welfare consequence at m=5.

## 3. Precise relevance to deletion induction

The first note excludes deleting the factor-two structure and keeping
only B. This note preserves factor two and proves the necessary bound
C>=1 for the proposed absolute-C contract, but leaves that contract open.
Even if it were proved with C>=1, applying it to a deletion would require
checking whether the available **actual-path** ASD error budget can replace
the **full-history layer-supremum** B, or proving the stronger actual-path
version separately. ASD does not currently pay B. One must additionally
account for genuine suffix resets if using the peer prefix compiler;
its exit-floor Delta is not rho_i.

The next meaningful advance would therefore be a new general dynamic
inequality using the exact deletion refund identities, or a proof of
(F2?) with the exact norm and quantifiers checked. This attempt produced
the explicit C>=1 lower bound and the comparison above, not such an
inequality.
