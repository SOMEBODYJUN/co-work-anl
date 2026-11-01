# Independent review: dynamic thresholds and independent local-SPE cones

2026-10-24. This review reconstructs the Theta peer's precise threshold and
multi-cone contract, then inspects `../theta/multicone_attack.py`. Verdict:
the mathematical representation is valid. It is not a proof of its proposed
threshold budget, and no counterexample was supplied for this audit.

## Threshold is the minimum attainable local-SPE current payoff

Fix any legal ordered prefix h with a current player. For each action A,
let R(h,A) be the nonempty finite set of complete pure-SPE outcomes after
that forced action. Write

    ell_A=min_(z in R(h,A)) u_current(z),
    Theta(h)=max_A ell_A.

All minima and maxima exist because the extensive game is finite and pure
SPEs exist by backward induction. In any local SPE at h, the actual current
payoff is at least ell_A for every A: each genuine off-path child is itself
a local SPE. Thus every current local-SPE payoff is at least Theta(h).

For attainment, choose A* maximizing ell_A, and select a child SPE attaining
ell_(A*)=Theta(h). At every other ordered child choose a child SPE attaining
its own ell_A<=Theta(h). The current player can prescribe A*, because no
other action's prescribed continuation gives more. Pasting these independent
ordered subgames is a complete pure SPE. Therefore

    Theta(h)=min_(tau a local SPE at h) u_current(outcome(tau)).

No anonymous-history or common-tie selector is assumed. In particular,
different witnesses below may prescribe incompatible continuations on their
overlapping histories; they are separate SPEs, not a single common strategy.

## Independent witnesses and the exact budget quantifier

Fix one actual complete pure SPE sigma with terminal welfare W and actual
prefixes h_i. The proposed threshold-budget bridge is

    W+sum_i Theta(h_i) >= OPT_m.                            (TB)

Its exact equivalent witness form is:

> For every independently chosen family tau_i of local pure SPEs at h_i,
> W+sum_i u_i(outcome(tau_i)) >= OPT_m.

One direction uses each witness payoff>=Theta(h_i). The other chooses an
attaining minimizer separately at each h_i. There is no coupling constraint
between these separate witness choices. The equivalence relies on this
independence, not on them jointly extending sigma.

The actual payoff u_i is itself at least Theta(h_i), so sum_i Theta(h_i)<=W.
Thus TB would imply half coverage. TB has not been proved here, and may be
strictly stronger than the original target.

## Fixed-strategy cone contract

Fix the actual full strategy sigma, each witness strategy tau_i, and an
arbitrary legal comparison tuple T of at most m topics. With topic labels
fixed, every terminal payoff is a rational linear form in nonnegative client
type multiplicities. Every full-history SPE condition is consequently a
homogeneous rational linear inequality. The relevant cone is the
intersection of:

* all full-history IC inequalities for actual sigma;
* all local-history IC inequalities for each separate tau_i at h_i;
* nonnegative type multiplicities.

On this cone, W+sum_i witnesspayoff_i-coverage(T) is another homogeneous
rational linear form. A negative rational point gives a strict TB
counterexample after integer scaling to distinct unit clients. The witnesses
need only remain local SPEs after varying the type multiplicities; they need
not continue attaining their thresholds, because actual thresholds are no
larger than their current witness payoffs.

The comparison tuple need not remain optimal after varying multiplicities.
Negativity already gives

    W+sum_i Theta(h_i)
      <=W+sum_i witnesspayoff_i < coverage(T) <= OPT_m.

Conversely, certifying all fixed-strategy cones and all comparison tuples
would imply TB, because minimizing local witnesses and an optimal comparison
exist for each instance. A nonnegative minimum for one selected cone and
comparison does not certify the untested cones or comparisons.

Dropping the actual full-SPE cone while retaining witnesses at prefixes of an
arbitrary path attacks a different, stronger assertion TB-ANY. A negative
point in that relaxed domain must not be called a TB or half counterexample
unless that actual path is independently verified SPE.

## Script inspection and one reporting guard issue

The inspected script's `path is None` branch constructs a full actual SPE
certificate and includes its IC rows. Its explicit-path branch omits those
rows, and therefore is the TB-ANY mode. `local_certificate` correctly chooses
a child outcome with current payoff Theta and completes the other children
with their respective current-player minima. Its later fixed-strategy IC
rows retain all local ordered histories. Common integer denominator
lcm(1,...,m) correctly clears every unit-share payoff denominator.

Exact rational reconstruction checks normalization, nonnegativity, every
included cone row, and a strict negative objective before creating integer
client multiplicities. Recomputing exact thresholds then independently
checks the bridge inequality on the proposed instance.

At inspection time a reporting/postcheck guard was ineffective:

    if report.get('actual'):
        assert is_spe

No `actual` key was set in `report`, so the assertion was never executed.
The peer was notified to capture explicit TB versus TB-ANY mode before
overwriting `path`, assert actual-path SPE membership in TB mode, and label
the report's scope explicitly. The actual IC rows were already included in
the mathematical TB cone, so this was a redundant-check/report-contract
defect, not evidence of a mathematical failure of the cone representation.

The reviewer did not extend the finite search. Floating nonnegative outcomes
remain finite discovery evidence rather than exact universal certificates.
No threshold-budget counterexample or general closure is asserted.

## Follow-up inspection of the saved note and resolved guard

The peer's subsequently saved `../theta/README.md` states the same threshold
minimum, independent-family equivalence and rational-witness reduction with
the correct scope. Its discussion of the population consequence is also
logically valid: adding an empty topic leaves OPT unchanged and, when any
client is coverable, that topic has zero payoff while a nonempty topic gives
a strictly positive payoff at every finite history. Thus empty choices are
never prescribed in a local SPE, and do not change the local threshold on
the original nonempty actions. Applying a universal TB-ANY assertion to the
all-empty legal path yields sum_(r=1)^m Theta_r(empty)>=OPT_m. This is only
a necessary consequence of that unproved universal bridge; no POP inequality
has been established by the reduction. Numeric examples in the peer's note
were not independently re-audited here.

The script has now fixed the reporting guard: it captures
`mode='TB' if path is None else 'TB-ANY'` before modifying path, records that
mode in the report, asserts `is_spe` when mode is TB, and labels an exact
negative status with its mode. This resolves the specific issue above.
No negative witness was reported, and the correction does not change the
mathematical status of TB, TB-ANY, or the original half target.
