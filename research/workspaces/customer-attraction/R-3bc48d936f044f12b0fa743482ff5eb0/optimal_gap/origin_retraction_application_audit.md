# Audit of origin retraction and its common role cap

2026-10-24. First reconstructed the abstract theorem in `triangular_retraction_blind_audit.md`, then read:

- `../flow/origin_retraction_shared_capacity.md`;
- peer `R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md`.

This is an internal scope/soundness audit, not external review or a universal feasibility proof.

## Verdict

**Pass for the stated restricted, conditional repair theorem.** RETRACT, greedy feasibility, componentwise greatestness and the first-failure dual cut are correct under the fixed admissible-flow contract. No fatal mathematical assumption was found in that statement. The draft correctly uses the cut value z_j<0; it does not have the possible sign ambiguity in the parent shorthand.

The relaxation of d'_i<=u_i is legitimate for the final certificate as explicitly defined. It changes the certificate family; it does not preserve the peer's original INIT system. The draft says this plainly. No new IC follows from the relaxation, and no universal greedy-success theorem has been proved.

## Source split and inventory check

For a fixed admissible aggregate R flow, split each outgoing edge and terminal current in the proportions of the tagged incoming source masses. At h=0, every associated output is zero. Mandatory equality z=h/c_A is then preserved for each source; optional-common inequalities 0<=z<=h/c_A are likewise preserved. Coalescing histories create no problem because tags are kept and only amounts are split. The finite strictly future graph ensures the terminal masses K_il from origin i sum exactly to b_i and have l>i.

For b_i>0 set theta_i=y_i/b_i. An explicit coordinate implementation of the retention, which removes any ambiguity about its inventory, is

\[
\begin{aligned}
c'_{ix}&=c_{ix}+\theta_i\sum_j a_{ijx} &&(x\in R),\\
a'_{ijx}&=(1-\theta_i)a_{ijx} &&(x\in R).
\end{aligned}
\]

For x in I leave both coordinates unchanged. Then c'+sum a'=c+sum a=r coordinatewise, every initial edge bound is preserved by decrease, and d'_i=d_i+theta_i b_i=d_i+y_i. When b_i=0 all changed amounts are zero, and no ratio is formed.

Scale every subsequent tagged R amount from origin i by the same factor 1-theta_i. Each tagged homogeneous equation remains true; summing tags preserves each aggregate mandatory equality and common interval. All downstream aggregate h decrease, so an existing upper density bound stays valid. The construction does not combine separately paid same-role contexts or invoke another per-client IC.

The terminal current at role l decreases by sum_(i<l)theta_i K_il while its retained source current increases by y_l. Therefore

\[
F'_l=F_l+y_l-\sum_{i<l}(K_{il}/b_i)y_i
\]

with zero-row terms interpreted as zero. Row conservation gives sum F'=sum F=|O|. All costs remain nonnegative because the expression is realized by nonnegative retained inventory plus nonnegative scaled terminal flows, even if this is less obvious from the scalar affine formula.

## What the relaxed current can and cannot mean

The original d_i<=u_i is part of a local-IC construction of the seed flow. It need not remain true after retention; c'_{ix} can label customers not physically covered by actual B_i, just as the seed c_{ix} already does. Thus the retained source is not a new same-customer actual-profit coupon, and it cannot be justified by reusing the old IC separately.

For final soundness, that local justification is unnecessary once one *verifies the entire single common cap*

\[
F'_i=d'_i+H_i+J_i+\sum_{t:\operatorname{role}(t)=i,x}L'_{tx}\le2u_i.
\]

Each comparison customer is still counted exactly once in the conserved inventory. Summing this one cap per role therefore proves |O|<=2W. This is arithmetically sound even if d'_i>u_i; it does not spend two separate copies of u_i and does not assert that the original INIT constraints still hold.

Conversely, the original d_i<=u_i and H_i+J_i<=u_i prove only A_i<=2u_i before R arrivals. They do not supply a spare budget for every R retention. That spare is computed by the greedy z_i, and an overloaded role can still fail. A proof that it never fails would be a new theorem, not a consequence of this audit.

## Why this is useful and what is bookkeeping

The **nontrivial but elementary general relation** is the exact feasible-set transformation plus the triangular theorem: for a fixed routing and seed inventory, maximal early retention can never hurt a later cap, and the algorithm either gives the componentwise greatest feasible retention vector or an explicit nonnegative-price separator for *all proportional source retractions of this fixed routing*. This is more than an arbitrary proposed pruning rule or an unexplained LP feasibility assertion. It can turn a particular overloaded seed flow into a checkable capacity certificate without rerouting its surviving mass.

The implication mass conservation plus verified role caps implies half is bookkeeping; it is not by itself a new SPE inequality. In particular lambda=1 in the cut has q_i=1 on positive-b rows and yields exactly

\[
\sum_i(c_i-F_i)=2W-|O|.
\]

Thus universal cut nonnegativity would contain the original target. The draft explicitly leaves it unproved. Its price witnesses concern only the fixed-routing retraction family, so a failed greedy run does not separate all optional-common routings, all initializations, all comparison tuples, or the original half target. No strict enlargement on actual SPE data was proved merely by defining a larger certificate family.

## Five-player and boundary scope

The five displayed caps are the direct specialization of the general formula, with b_5=y_5=0 by strict future support. The first role has no incoming R mass, so A_1<=2u_1 guarantees nonnegative first z and greedy keeps that cap. The next four z values have no proved automatic sign. Therefore the stated m=5 diagnostic is accurate and provides no unconditional half theorem.

Zero inputs, empty source rows, equality at saturation and arbitrary complete-history ties are handled correctly. This operation changes only proof amounts, never actions or completion leaves. It preserves fixed histories rather than identifying equal-count histories. This audit checks the application conditional on the peer's established seed-flow/initialization facts; it does not independently re-prove those underlying general game lemmas or certify every fixture named by the draft.
