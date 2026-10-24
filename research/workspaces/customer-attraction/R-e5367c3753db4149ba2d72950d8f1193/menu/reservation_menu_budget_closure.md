# Disjoint reservation lifts preserve compatible path-menu budgets

2026-10-24. Personal general construction lemma, not a proof of Q-CAG-HALF.
The unrestricted Mpath bridge remains OPEN. This statement quantifies arbitrary
old player counts, arbitrary finite old common catalogues, and all query
distributions. It concerns the complete **literal** reservation lift described
below, rather than every SPE of the enlarged instance. No external novelty or
independent-review claim is made.

## Setup and the exact all-history construction being used

Take any old n-player instance, n>=1, and a complete history-dependent pure SPE
sigma. Let z be its actual terminal and W its welfare. A **literal reservation
lift** adds one new first player and a new topic B consisting of J new unit
customers disjoint from all old customers. Its complete SPE has actual terminal
(B,z), and after the initial B, at every ordered history without an additional
B, it literally follows sigma on the old ordered history. We assume such a
lift exists and

    M := max_T sum_(x in T) 1/[1+c_x(z)] <= J,
    (n-1)J/2 <= W.                                 (GEN)

The menu result does not construct a lift merely from GEN. It includes n=1
and zero old welfare whenever such a literal lift exists and GEN holds.

Here is a stronger sufficient credible constructor for n>=2, independently
reconstructed in [the constructor audit](new_constructor_review.md). It
strengthens the existing
[all-history disjoint reservation lemma](../../R-6bb0323d87294932af2aa23b47b9d4ad/parent/disjoint_reservation_lift.md)
by removing its former additional strict condition |T|/2>J/n.
Suppose every old decision history has prescribed final player payoff at least
eta>0. Write

    delta_T = min_(S in old catalogue) |T intersect S|.

Let J be a positive integer satisfying

    J/2 <= eta,
    J >= max_T (|T| - delta_T/2).

Then a literal reservation lift exists. Its preservation of all ordered
off-path old-action children is essential for the menu result. This credible
construction implies GEN, as checked below.

For completeness, prescribe B at every no-B history, and at every exactly-one-B
history erase B and execute the old sigma. In subtrees beginning at the second
B, fill arbitrary complete SPE. Exactly-one-B old deviations reproduce genuine
old IC rows, and B deviations pay at most J/2<=eta. At every no-B history,
prescribed B pays J; a forced old T has at least one other old S in its
terminal because n>=2, so its payoff is at most |T|-|T intersect S|/2<=J.
This includes no-B last histories. The resulting policy is a complete SPE
and retains the entire old policy after root B. There is no frozen-suffix
assumption. The constructor audit supplies the full proof and exact boundary
checks.

For every old actual position i and forced old A, let Z_i(A) be its complete
n-slot terminal. Define

    K_i(T,A) = sum_(x in T) 1/[1+c_x(Z_i(A))],
    psi_i(p) = min_A sum_T p_T K_i(T,A).

Let lambda be any probability distribution on old positions. Introduce its
scaled menu-budget defect

    E_lambda(p) = n sum_i lambda_i psi_i(p) - W.

Uniform lambda gives exactly the uniform-time defect sum_i psi_i(p)-W.
In the lifted game define

    lambda'_1 = 1/(n+1),
    lambda'_(i+1) = n lambda_i/(n+1).

These weights are nonnegative and sum to one.

## A quantitative closure inequality

Every new query distribution has the form

    p' = alpha delta_B + (1-alpha)p,  0<=alpha<=1,

with p an old query distribution (arbitrary when alpha=1). Let

    L_z(p) = sum_T p_T sum_(x in T) 1/[1+c_x(z)].

Then the literal lifted policy satisfies the following nontrivial bound:

    E'_(lambda')(p')
      <= (1-alpha) E_lambda(p)
         - (1-alpha)[J-L_z(p)]
         - alpha[W-(n-1)J/2].                         (CL)

Both displayed deductions are nonnegative under GEN:

    L_z(p) <= J,
    W-(n-1)J/2 >= 0.                               (RES)

Under the stronger credible-construction assumptions, the second deduction
is at least eta>0.

Consequently, if the old policy obeys

    n sum_i lambda_i psi_i(p) <= W   for every p,

then the lifted policy obeys

    (n+1) sum_j lambda'_j psi'_j(p') <= W+J   for every p'.

In particular, a uniform-time menu budget is preserved by every such literal
reservation lift. This is a full-query closure statement, not a finite-sample
claim.

### Proof

For a shifted old position i+1, restrict its defensive menu to old actions A.
The complete terminal is then exactly (B,Z_i(A)); the B customers have load
one, and old customer loads are unchanged. Therefore

    psi'_(i+1)(p')
       <= alpha J/2 + (1-alpha) psi_i(p).            (TAIL)

The new root's actual B column is (B,z), hence

    psi'_1(p') <= alpha J/2+(1-alpha)L_z(p).         (ROOT)

GEN directly proves RES. To verify GEN under the stronger constructor's
hypotheses, choose any old T and any old action S occurring in z. Its presence gives
c_x(z)>=1 on T intersect S and c_x(z)>=0 elsewhere. Thus

    sum_(x in T) 1/[1+c_x(z)]
       <= |T|-|T intersect S|/2
       <= |T|-delta_T/2 <= J.

Average this inequality over p to obtain the first part of RES. Also, every
old actual payoff is at least eta, so W>=n eta. Since J/2<=eta,

    W-(n-1)J/2 >= W-(n-1)eta >= eta.

Multiply TAIL by n lambda_i, add ROOT, and subtract W+J. Expanding the result
gives CL exactly. This proves both the inequality and its consequences.

## Actual insertion pressure also cannot be created from a nonpositive source

Define the actual-terminal cap

    L_max = max_T sum_(x in T) 1/[1+c_x(z)].

Suppose L_max<=W/n and GEN holds. Then the new actual-terminal cap is at most
(W+J)/(n+1); consequently every lifted position satisfies

    psi'_j(p') <= (W+J)/(n+1)  for every p'.         (NOPRESSURE)

The new actual-terminal cap is exactly max{L_max,J/2}. Let
t=(W+J)/(n+1). Since L_max<=min{W/n,J}, we have L_max<=t: if J>=W/n then
t>=W/n, while if J<=W/n then t>=J. The bank cap J/2<=t is exactly
(n-1)J/2<=W. This proves the asserted cap, including n=1. That actual
terminal is a legal column at every lifted position, so it also proves
NOPRESSURE. This shorter general proof was supplied by the parent researcher.

## Relevance and limit of the general component

PRODUCT-MENU-TIME-v1 uses positive pressure vectors
psi_i(p)-W/m to separate a common time distribution. The formula above gives
an explicit compatible-time extension for every literal reservation lift,
and preserves the uniform budget with a quantitative reserve. Products also
preserve a common time budget by ordinary componentwise additivity. Thus
products and these reservation lifts, starting from policies with a valid
uniform budget, cannot manufacture a counterexample to that budget.

This does not assert that every old policy has a compatible budget, that
every enlarged-instance SPE is a literal lift, or that all Mpath pressure
vectors are nonpositive. It supplies no general payment for arbitrary
conditional reciprocal covariance. Its exact positive contribution is CL:
the aggregate old menu defect contracts under this all-history construction
and the two displayed reserves pay the new query/old-query interaction.

## Focused direct Mpath cone attack, and its stopping point

`strategy_cone_mpath_attack.py` tested Mpath<=W/m directly on the existing
eight-player, eight-topic, 13,872-node complete policy DAG from
`R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json`.
The customer variables were all 255 nonempty topic-membership types, rather
than only the old ten types. The LP enforced 37,546 distinct nonzero genuine
IC rows, the simplex normalization of customer mass, and all 64 actual-prefix
forced-action columns, including the actual terminal columns.

Two explicit mixed-query starts were used: uniform on all eight topics and
uniform on topics (2,3,6,7). For each, one query best-response step was also
attempted. The best floating gap was -1/72, attained on the all-common type;
no strict proposal was produced. That optimizer collapses the catalogue
labels to the same customer set and is only a point in the labelled cone
relaxation, not a new legal eight-distinct-topic instance. A strict positive
proposal would still need rational recovery and a distinct-catalogue audit;
a sufficiently small mixture with the original legal cone point would
preserve a strict margin and restore its distinctions. The JSON records the exact starts and
numerical output. This is neither an exact dual certificate nor a proof of
the cone restriction or of Mpath. No further negative sampling was done.

No full Mpath counterexample or arbitrary-SPE covariance payment was found.
