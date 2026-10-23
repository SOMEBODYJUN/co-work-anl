# Current exact frontier

Q-CAG-HALF remains OPEN, with the original general catalog, arbitrary population,
all ordered histories and every pure SPE. We have no primary counterexample and
no complete general proof. This workspace contains real general lemmas and
method obstructions, not a sequence of increasingly large no-counterexample runs.

## Main surviving proof obligations

For actual root coverage C, actual loads c, a welfare-optimal m-tuple of topics
with loads d and union O, the signed harmonic candidate is

    sum_x (H_(c_x+d_x)-H_(c_x)) <= W+|C\O|.

It suffices that some optimal tuple satisfy it. Customers in O\C contribute
at least one on the left, so this would imply OPT<=2W. The stronger signed
query version replaces the left side by sum_x d_x/(c_x+1). Both remain OPEN;
finite cone checks do not support a status upgrade. Their unsigned versions
are already false by the archived 71-customer example. The new dynamic state
retains remaining-player profit and outside-optimum profit at arbitrary legal
backgrounds, but a positive one-step or proper-prefix deletion drift is false.
Its all-horizon cumulative payment still needs new inequalities from credible
intermediate continuation nodes. An identity for total debt is not that proof.

The security branch's direct per-player floor OPT_m<=2m u_i is another open
sufficient route, distinct from the false u_i>=v_m floor. Safe disjoint-theme
extension gives a general, fully credible amplification diagnostic:

    max_(1<=r<=m) [OPT_old,r+(m-r)K/m] > 2W

would be a genuine primary counterexample; replacing 2W by 2m u_i attacks the
direct floor. No such violation was obtained here. Floating fixed-cone results
remain discovery diagnostics with their actual finite scopes.

## What changed

* All-k maximal-only classification now explains exactly why discarding dominated
  topics loses a welfare theorem: min3k+1 versus the full-catalog SPE2k+2.
* Raw population monotonicity and support-preserving deletion fail. The strict
  four-topic witness has unique complete equilibria with W2=40,W3=39,OPT40.
* Catalog compression preserving an ordered SPE path cannot be bounded by a
  function of population, even at two players, all strict choices, and a unique
  optimal actual pair. Welfare-only compression remains a different question.
* Same-population safe catalog extension is a proved general construction,
  with exact OPT convolution and a repaired zero-customer/set-catalog boundary.
* A true Cartesian coupling uses one coordinate's continuation reward to
  compensate another coordinate's non-equilibrium projection. Its explicit
  architecture nevertheless has ratio at most5/4 and cannot cross2 under the
  analyzed safe extensions/products. Future amplification must change mechanism.

Exact statements, dependencies, review grades and file paths are in the
workspace README/CLAIMS and the individual branch notes. New coupled and signed
identities are reviewed only to their actual recorded extent. No external review
or novelty statement is implied by Git publication.

## Next information-bearing actions

An informative next step must either supply a previously unused credible-node
inequality paying signed debt, give a complete violation of the signed candidate
or direct floor, or construct a new coupling mechanism reusing compensation
without the large welfare mass in the current Cartesian family. Repeating local
nonnegative-drift assertions, pruning the menu, or extending the same random
cone scan is not a next general proof step. The six branch notes explain exact
remaining gaps and why their stopped subroutes failed.
