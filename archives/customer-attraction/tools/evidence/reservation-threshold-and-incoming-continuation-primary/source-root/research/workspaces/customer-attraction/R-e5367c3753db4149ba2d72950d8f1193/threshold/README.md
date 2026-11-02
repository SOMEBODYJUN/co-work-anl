# Dynamic continuation floors: exact candidate and present limit

2026-10-24. Personal research checkpoint. **Q-CAG-HALF, SM-opt-exists and
TB remain OPEN.** This directory contains no general half proof and no
counterexample to any of those three statements. No board messages or Git
commits were made by this subtask.

## Exact scope and candidates

Use the original model: an arbitrary finite common catalogue, arbitrary
number m of unit providers, unit customers, and each complete ordered-history
pure SPE, with arbitrary history-dependent ties. Fix its actual path z and
its actual prefix h_i before role i. After forcing legal action A, let
R(h_i,A) contain all terminal outcomes realizable by complete local pure SPE
of the followers. Define

    L_i(A) = min_{y in R(h_i,A)} u_i(y),
    Theta_i = max_A L_i(A),
    O = OPT_m,    W = W(z).

These child sets are not restricted to those selected by one ancestor
policy. They can be chosen independently on disjoint ordered subtrees.

The precise existence candidate is

    max_{T in S^m: W(T)=O} sum_i L_i(T_i) >= O-W.      (SM-opt-exists)

The all-optimal-tuples candidate instead takes the minimum over that same
set. A failure of the latter does not refute the former. In particular,
`R-b28.../independent_attack/theta_dp.py` minimizes over optimal tuples: its
negative test is a test of the stronger universal version.

The threshold candidate on actual SPE paths is

    O <= W + sum_i Theta_i.                            (TB)

SM-opt-exists implies TB. Each genuine SPE satisfies u_i(z)>=Theta_i by
its own full-strategy one-action IC and membership of the selected child
continuation in R(h_i,A). Thus sum_i Theta_i<=W, and either candidate would
imply the original half target. This implication has not been closed in
the opposite direction and is not itself new progress.

At a single history, Theta is exactly the minimum current-player payoff
among all SPE there. For attainment, pick in every child a continuation
minimizing that incumbent's payoff, then select a child maximizing those
minima. This gluing theorem does not make the minimizers at different
actual prefixes one common continuation or give their joint coverage
budget.

Primary repository sources read:

- `research/current/customer_attraction/model.md` and `exact_solver.md`;
- `research/workspaces/customer-attraction/boss20/route_theta/README.md`;
- `research/workspaces/customer-attraction/R-b28b3013e6464e70862b4993359a6964/theta_matrix/obstruction_and_audit.md`;
- that actor's `notes/direct_farkas_and_static_lp_boundary.md`;
- `R-b6d.../direction_review/continuation_general_scope/threshold_candidate.md`;
- `R-f81.../security_minimax/threshold_budget_obligation.md`.

The local clone contains no `wcg/board` remote-tracking ref, so no claim is
made here to have read that live branch. The parent identified board 223
as the earlier worst-denominator obstruction; its repository source is
the `direct_farkas_and_static_lp_boundary.md` file above.

## Independent deterministic rational audit

`ordered_threshold_audit.py` imports neither the normative solver nor its
model. It expands multiplicities into distinct unit customers; recursively
retains complete ordered terminal paths; and computes all payoffs with
Fraction. At each history it glues all children independently using the
exact max-min threshold rule. This is an ordered-tree implementation,
not a count-dependent policy restriction.

For each of four pre-existing inputs it independently verifies every
action comparison in the frozen complete policy, takes that policy's
actual path, and enumerates **all** optimal ordered m-tuples when finding
both the minimum and maximum assignment sums. It also checks the known
m=4 all-big UV witness. These five diagnostics are not a scan and not a
proof of a universal candidate.

| Existing fixture | W | O | O-W | min optimal sum L | max optimal sum L | sum Theta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| root_tax_failure | 38 | 61 | 23 | 69/2 | 38 | 38 |
| aggregate_theta_failure | 34 | 36 | 2 | 85/3 | 34 | 34 |
| individual_security_failure | 32 | 34 | 2 | 28 | 32 | 32 |
| portfolio_matching_failure | 44 | 45 | 1 | 41 | 41 | 44 |
| known all-big, m=4 | 4 | 7 | 3 | 4 | 4 | 4 |

The four frozen full policies respectively contain 259,43,43,6 decision
histories; all 1554,258,258,30 comparisons, including the self action,
pass exact verification. The root-tax local marginal failure and the
aggregate static-floor failure do not refute the dynamic candidates.

Reproduce from repository root:

    python research/workspaces/customer-attraction/R-e5367c3753db4149ba2d72950d8f1193/threshold/ordered_threshold_audit.py

The frozen output is `ordered_threshold_audit.json`.

## A narrow stop for replacing L by arbitrary-follower denominators

This is a diagnostic of a **weaker substitute**, not an SM or TB
counterexample. It overlaps the earlier actor's broader worst-denominator
LP obstruction; no new general impossibility claim is made.

Write b_i(x) for actual prefix load and r_i=m-i+1. Ignoring all follower
optimality gives exactly

    F_i(A) = sum_{x in A} 1/(b_i(x)+r_i) <= L_i(A).

It is exact for the relaxation to arbitrary follower actions: every
denominator is at most b_i(x)+r_i, and having all remaining followers copy
A attains all those upper denominators simultaneously. The general
substitute candidate

    exists optimal ordered T with sum_i F_i(T_i) >= O-W

is false, even where the original L-candidate has positive slack.

Reuse the known all-big family: B has m private customers and there are
m-1 singleton themes with mutually disjoint private customers. The actual
path is all B; W=m and O=2m-1. The constant-B policy on every complete
history is a pure SPE. At an all-B history, deviating to a singleton gives
1 and continuing B gives 1. After any previous singleton, all remaining
B choices give more than 1, while a singleton always gives at most 1.

Along the all-B path, **the true L matrix is all 1**. For forced B, the
direct bound is 1 and the constant-B continuation attains 1. After forcing
any singleton, every follower can guarantee a B payoff at least
m/(m-1)>1 against every further continuation, while any singleton payoff
is at most 1. Thus every follower chooses B and the forced singleton
player obtains exactly 1. Consequently every optimal ordered tuple has
sum L=m, exceeding O-W=m-1.

In contrast,

    F_i(B)=1,    F_i(S_j)=1/r_i.

Every optimal tuple uses B and each singleton exactly once. Assigning B
to the first position maximizes its total F value, so

    max_{optimal T} sum_i F_i(T_i) = 1+H_(m-1) < m-1    (m>=4).

The strict inequality starts at 1+H_3=17/6<3 and persists because its
left side then increases by 1/m per increment of m while its right side
increases by 1. The independent m=4 audit gives substitute slack -1/6,
while true SM-opt-exists, SM-opt-all and TB all have slack +1.

This closes only this specific substitute for SM-opt-exists. It does not
exclude another use of denominator inequalities, a threshold-max version,
full-history IC multipliers, or other proof methods. The earlier actor's
singleton obstruction already treats a wider static multiplier system.

## Remaining actual obligation

No added full-scope relation paying

    max_{optimal T} sum_i L_i(T_i) >= O-W

or the weaker TB budget was established in this subtask. The pointwise
worst-denominator bound loses the follower incentives needed even on the
existing all-big family. Single-node max-min gluing and exact assignment
enumeration do not supply the missing cross-prefix inequality. The five
positive fixture checks should remain finite evidence, not be presented
as progress toward a completed general proof.
