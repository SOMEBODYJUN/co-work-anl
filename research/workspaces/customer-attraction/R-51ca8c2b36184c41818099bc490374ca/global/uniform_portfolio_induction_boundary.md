# Why a direct uniform-portfolio backward induction loses a sharp tail reserve

Exploratory analytic observation, not a proof or disproof of UP or Q-CAG-HALF.
The model is the original finite unit-customer common-catalog model, with all
complete ordered-history pure SPE and arbitrary tie choices.

## An unproved background extension

At a fixed prefix b with r remaining providers, take n comparison topics and
let C be their union. Write

    L_b(C) = sum_(x in C) 1/(b_x+1),

P for remaining actual profit, and Q for the sum of all r*n true
actual-prefix deviation queries. A possible extension of the known two-player
interface is

    r L_b(C) <= n(r-1)P/r + Q.                       (BG-UP)

For r=2 this is the existing proved averaged portfolio inequality. For r=1
it follows by summing topic utilities. For r>=3 it is **unproved here**.
At b=0, r=n=m it gives UP and hence the stronger 2-1/m welfare ratio.

Suppose the actual next action is A, with utility u, and write P_tail for the
remaining r-1 providers' profit and Q_1 for the n first-position queries.
Substituting only the nonnegativity of the BG-UP tail slack would require

    Q_1 + n(r-1)u/r + n P_tail/[r(r-1)]
      >= L_b(C) + (r-1)[L_b(C)-L_(b+A)(C)].          (LOCAL)

This is merely a sufficient condition for that naive induction, not a
consequence of SPE. It is already false in the elementary sharp family.

## Exact failure on the all-big family

For every m>=3, let A contain m unit clients, and let B_1,...,B_(m-1) be
pairwise disjoint singleton topics, also disjoint from A. The complete policy
chooses A at every ordered history. It is SPE: a current provider who chooses
A and is followed by A obtains at least m/m=1, whereas choosing any singleton
obtains at most 1. This argument holds at every off-path prefix as well.

At the root, actual W=m and every actual provider gets 1. Take comparison
portfolio A,B_1,...,B_(m-1); its union has size 2m-1. Every query V_ij is 1,
so the original root UP inequality is **exactly tight**:

    (m-1)W + Q - m O
      = m(m-1) + m^2 - m(2m-1) = 0.

After the first A, b=1_A and r=m-1. The same n=m comparison topics give

    L_(1_A)(C)=3m/2-1,
    P_tail=m-1,
    Q_tail=m(m-1).

The BG-UP tail slack is therefore

    m(m-2) + m(m-1) - (m-1)(3m/2-1)
      = (m-2)(m+1)/2 > 0.

At the root, LOCAL has left side 2m and right side

    2m-1 + m(m-1)/2.

Its slack is exactly

    -(m-2)(m+1)/2 < 0,

the negative of the tail reserve. Thus even a hypothetical proof of BG-UP
cannot simply discard its tail slack and close by LOCAL. A successful
induction would have to carry a state quantity retaining this reserve, or
use different comparisons. This failure is independent of numerical search
and uses a complete SPE for every m>=3.

The boundary does not disprove BG-UP: the family satisfies it at both the root
and displayed tail. It only rules out this particular strengthened local
step, even on the sharp disjoint family.
