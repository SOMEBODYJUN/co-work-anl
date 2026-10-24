# Optimal-completion recurrence: retained-credit stopping point

2026-10-24. Research target is exactly Q-CAG-HALF: every number of unit providers, every finite common catalog, every complete ordered-history pure SPE, including all ties, repetitions, empty topics and the zero instance. **No new positive full-input inequality is proved in this note.** The work below isolates the missing inference; it does not present the existing identity as progress and does not turn a failed proof attempt into a claim about the target.

## Fixed objects and actual logical resources

Fix the original full SPE and an arbitrary precise history h, possibly off path. Use all notation from `research/current/customer_attraction/optimal_first_action_branch_gap.md`. In particular r is the number of remaining providers, S is the prescribed action, A is an optimal-first-action menu topic, and Y_A is the actual ordered continuation under the same original strategy after forcing A. The quantities rho, xi and eta retain their exact original definitions. No continuation is frozen, transported to a different history as an SPE, or reselected favorably.

The current IC and static same-tail calculation prove

\[
r(\delta-u)=(r-1)(\rho_A-f_A-\xi_A)-\theta_A-\eta_A-r\Gamma_A.
\tag{1}
\]

This formula uses the current IC but does not use the full incentive constraints at the later nodes in A's subtree. Summed along the actual path, it gives an identity for OPT-2W. Thus proving its summed right side nonpositive still needs an additional relation involving genuine later-node incentives. Choosing a different distribution on the optimal menu does not change the right side of (1).

The offspring-menu lemma additionally proves, for the true tail topics B_1,...,B_(r-1),

\[
\sum_\ell \lambda_{B_\ell}\le(r-1)(t_A+\eta_A),\qquad
\lambda_B=F_r(P)-F_{r-1}(P\cup B).
\tag{2}
\]

This is a real full-input static relation, but it controls only the first static loss of querying B at h. It does not control B's genuine new continuation.

To make that precise, write C_A=|P union A union Y_A| and let C_B be the covered union in the original strategy after instead forcing B at the *same* h. If R_B is B's true child loss, then

\[
R_B=\rho_A-\lambda_B+(C_A-C_B).
\tag{3}
\]

The term C_A-C_B is the restart of the continuation at a different ordered history. It has no established sign. It is not the omitted xi or eta term: xi compares the **same tail** Y_A under backgrounds P union A and P union S, whereas (3) compares two **different true tails** Y_A and Y_B. Eta is a share surplus in the A leaf. Neither quantity by definition is a bound on C_A-C_B.

The exact unsuccessful step in this attempt was to select a low-lambda B using (2), then substitute its new true child loss for rho_A as though (3) had no positive restart. This step is invalid before any further incentive analysis. The existing all-big family already detects it: at the root, force a singleton A and take the big topic B from its genuine tail. Then lambda_B=0, eta_A=0, rho_A=m-2, R_B=m-1 and C_A-C_B=1, despite every history satisfying SPE. This is an existing example and an existing restart observation, not a new obstruction or a counterexample to half. It shows exactly why the chosen inference cannot be completed from menu proximity alone.

Consequently the missing useful theorem must constrain either this restart together with all the credits in (1), or some different aggregate of true successor incentives. Rewriting (3), summing (1), or independently minimizing eta does not provide that theorem.

## The retained-xi / omitted-eta candidate remains unproved

A precise stronger sufficient condition still available for attack is

\[
\sum_i\frac{r_i-1}{r_i}\mathbb E(\rho_{i,A}-f_{i,A}-\xi_{i,A})
\le\sum_i\left(\frac{\mathbb E\theta_{i,A}}{r_i}+\mathbb E\Gamma_{i,A}\right).
\tag{4?}
\]

Existence of menu distributions satisfying (4?) is exactly equivalent, by the full-credit identity and independence of the choices at each actual history, to

\[
\sum_i\min_{A\in\mathcal A^*(h_i)}\frac{\eta_{i,A}}{r_i}
\le 2W-\operatorname{OPT}_m.
\tag{5?}
\]

This is a candidate, not a new theorem. The current work found no analytic way to pay the restart in (3) and therefore does not prove (4?) or (5?). The known all-big family does not refute them. Complete retention of eta in (1) instead returns the original target exactly and does not close it.

## General-formula stress test at m=5

For arbitrary five-provider input, define Q_(r,A)=rho_(r,A)-f_(r,A)-xi_(r,A). The actual-path identity is

\[
\begin{aligned}
\operatorname{OPT}_5-2W={}&
\tfrac45\mathbb E Q_{5,A}+\tfrac34\mathbb E Q_{4,A}
+\tfrac23\mathbb E Q_{3,A}+\tfrac12\mathbb E Q_{2,A}\\
&-\sum_{r=1}^5\left(\mathbb E\theta_{r,A}/r+
\mathbb E\eta_{r,A}/r+\mathbb E\Gamma_{r,A}\right).
\end{aligned}
\tag{6}
\]

At r=1, rho=xi=0 and the coefficient of f is zero, so no missing endpoint is hidden. If (4?) were proved for all input sizes, its same specialization in (6) would give OPT_5<=2W with the additional eta credit. Without that unproved payment, (6) supplies no unconditional half conclusion. This work therefore **does not pass the five-provider half stress test**.

As a separate established full-input benchmark, the general prefix-profit product gives, on substituting m=5 and tau=5,

\[
W\ge\left[1-\prod_{r=1}^5(1-1/(5r))\right]\operatorname{OPT}_5
=\frac{6049}{15625}\operatorname{OPT}_5.
\]

Its reciprocal exceeds two. This is a specialization of an existing bound, not a five-provider project or an improvement. For the existing five-provider all-big family, full retained-credit (6) is exactly -1 because W=5 and OPT=9; that check verifies arithmetic only and cannot establish the general five-provider conclusion.

## An alternative sufficient statement, also unproved

For a globally minimum-payoff position i on the original actual path, let

\[
R_i=\sum_{j=1}^m u_i(h_i,T_j,\text{original true continuation})
\]

for an optimal m-slot comparison tuple. The following would suffice:

\[
R_i+\sum_{j>i}(u_j-u_i)\ge\operatorname{OPT}_m-W.
\tag{7?}
\]

Indeed current IC gives R_i<=m u_i, and global minimality gives
(i-1)u_i<=sum_(j<i)u_j. Hence the left side of (7?) is at most
`i u_i+sum_(j>i)u_j<=W`, proving half. This only records an exact sufficient interface; no claim is made that it follows from (1), (2), or existing last-two rows. Multi-successor true-query decorrelation has a signed deletion-return term, so the one-successor proof cannot be iterated without paying that term. The parent was informed of (7?) as unproved.

## Finite diagnostic and boundary conditions

`test_eta_budget.py` implements one targeted diagnostic of (5?), using complete count-based backward-induction policies (a legal subclass of full-history pure SPE). It runs 1,000 samples at seed 723, with m sampled from {2,3,4,5}, catalog size from {3,4,5,6}, and each nonempty type independently active with probability .35 and integer multiplicity uniform in {1,...,30}. It computes every optimal-first-action menu along each actual path exactly, using integer-scaled utilities and rational eta. The retained `eta_budget_attack.json` reports no violation; **this is finite negative test evidence only**, proves neither (5?) nor half, and is not a reason to promote the candidate. Additional sampling stopped after the parent requested analytic work.

All analytic formulas above are multiplication identities or inequalities and remain valid in the zero instance; no efficiency ratio is used. Menu minima exist because the catalog is finite nonempty. At arbitrary off-path h, all true continuations and current IC are still those at that exact history in the given complete strategy; no equality of replies at equal-load histories is assumed.
