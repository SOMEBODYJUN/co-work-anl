# Independent cleaner review: repeated last theme

Review date: 2026-10-21. Object: the formula communicated by the root and
counterexample agents, before reading the author's eventual proof file.
Result: no fatal issue; the following is an independent all-parameter proof.
This is an internal review, not external peer review or a novelty finding.

## Exact scope and statement

Use the unchanged Q-CAG-HALF model at the empty root. Fix any complete
ordered-history pure SPE and its actual terminal profile of m>=1 players.
Let B be the actual last player's coverage, k the number of actual players
choosing that same coverage, and u the last player's payoff. Choosing a
different catalog label with identical customer coverage counts toward k;
counting exact labels instead merely weakens the resulting lower bound.

Then

    OPT_m <= W+(m-1)u,
    W >= [k(2m-k)/m]u,

and consequently

    OPT_m <= [1 + m(m-1)/(k(2m-k))] W.

In particular, (m-k)^2<=m implies OPT_m<=2W. Equivalently, this holds for
k>=m-floor(sqrt(m)). No bounded-directory assumption is used.

## Independent proof of the first inequality

Fix an arbitrary comparison tuple of m catalog themes. For one customer,
write c for its actual terminal coverage count, b=1 if B covers it, and d for
the number of comparison themes covering it. Put b/c=0 when c=0. The sum of
last-player deviation payoffs to the comparison themes at this customer is

    d/(c+1-b).

This denominator is always positive. Pointwise,

    1_(d>0) <= 1_(c>0) - b/c + d/(c+1-b).

If d=0, the right side is nonnegative because b/c<=1_(c>0). If d>0 and
c=0, then b=0 and the right side is d>=1. If d>0, c>0, and b=0, the covered
indicator already supplies one. In the remaining case b=1, d>=1 gives
d/c>=1/c, exactly replacing the removed last-player share.

Summing over all customers yields comparison coverage <=W-u+sum_j V_mj.
All V_mj<=u by optimality at the actual last-player node. Taking an optimal
comparison tuple proves OPT_m<=W+(m-1)u. This proof does not freeze a follower:
there are no followers after that last decision.

## Independent proof of the second inequality

Every actual player covering exactly B receives the same final payoff u;
there are k such players. At any other actual decision node, changing to the
fixed legal coverage B gives at least |B|/m under every possible continuation:
every B customer has at most m final covering players. The prescribed action's
payoff is therefore at least |B|/m by that node's SPE condition. The strategy
after the change is its original specified continuation and may depend on
the whole changed ordered history.

In the actual terminal profile every B customer has load at least k, so
u=sum_(x in B)1/c_x<=|B|/k. Therefore the other m-k players each get at least
k*u/m. Summing the k exact u payoffs and these remaining lower bounds proves
the claim. Finally,

    k(2m-k)/m = m-(m-k)^2/m >= m-1

precisely under the square condition. Since W>=coefficient*u and the
coefficient is positive, substitution proves the ratio formula without
assuming u>0.

## Boundaries and limitations

For m=1, k=1, the first inequality already says OPT_1<=W and the ratio is one.
For k=m, the formula recovers OPT_m<=(2-1/m)W. That all-equal-coverage case
already appears in `general_tax_counterexample.md`, Section 5; it must be
credited as an existing special case. Empty B means u=0. Last-node optimality
then implies every catalog theme has zero coverage, so OPT_m=W=0, although
the displayed inequalities are already valid without this extra observation.
Zero customers, empty actions, repetitions, and arbitrary history ties cause
no additional division or existence issue.

The theorem provides a sufficient condition on the actual terminal profile,
not a theorem that every SPE has that condition. For a possible half-coverage
counterexample, the last coverage must occur fewer than m-floor(sqrt(m))
times. The condition is not claimed necessary for half coverage, nor is the
ratio formula claimed sharp for k<m. It cannot be imported unchanged to a
nonempty fixed background while treating remaining-player profits as W.

## Existing-asset overlap checked

The maximum-theme K/m guarantee and its consequence K<=W are already in
`tail_profit_lift.md`, Section 2. The last-node aggregated comparison and tax
bound OPT_m<=m*u+tau_0(c_<m) are already in `two_remaining_tax.md`, Section 6.
The all-equal-coverage factor 2-1/m is already in
`general_tax_counterexample.md`, Section 5. The exact combination using k
copies, and the square criterion, were not located in the current
customer-attraction text during a targeted search. This is a repository
overlap check, not a literature novelty review.

`check_repeated_last.py` independently checks the pointwise inequality in
691,950 valid integer membership/count cases for m<=100 using Fraction, and
audits the elimination and threshold equivalences for all 1<=k<=m<=100. The
preceding case proof and algebra establish the universal statement; finite
arithmetic verification is only a formula audit.
