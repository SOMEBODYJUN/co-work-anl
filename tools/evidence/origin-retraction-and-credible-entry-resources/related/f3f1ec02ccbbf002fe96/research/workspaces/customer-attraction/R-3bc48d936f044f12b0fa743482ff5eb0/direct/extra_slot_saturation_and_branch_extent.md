# Extra-slot saturation and the extent of a low-payoff branch

2026-10-24. General CAG-MODEL; arbitrary finite unit clients, common finite nonempty catalog, all m, every fully history-dependent pure SPE and every off-path tie. **Q-CAG-HALF remains OPEN.** The branch-extent inequality below is proved directly. The saturation-to-SPE implication is an unproved candidate, not a positive welfare theorem. No novelty or independent-review claim is made.

## 1. A pure extra-slot comparison

For a multiset B of exactly m legal topics write b_x=c_x(B), and define

\[
 q_B(T)=\sum_{x\in T}\frac1{1+b_x},\qquad
 \vartheta_{m+1}=\min_{B\in\mathcal S^m}\max_{T\in\mathcal S}q_B(T).
\]

The subscript counts the queried unit player in addition to the m competitors. This is the pure worst-best-reply quantity with one extra competitor relative to the original m-player game. It is not the previously disproved floor using \(\vartheta_m\).

For every m-topic comparison union C and every B,

\[
 |C|\le\sum_{j=1}^m q_B(T_j)+\sum_x\frac{b_x}{1+b_x}.
\]

The second sum is exactly \(\sum_{j=1}^m q_B(B_j)\), hence each of the 2m displayed topic-query terms is at most \(\max_Tq_B(T)\). Minimizing B proves the unconditional static relation

\[
 \boxed{\operatorname{OPT}_m\le2m\vartheta_{m+1}.} \tag{1}
\]

Scope correction: (1) is the old shared static counting lemma, also implied by the stronger existing comparison \(\operatorname{OPT}_m\le2m v_{m+1}\) and \(v_{m+1}\le\vartheta_{m+1}\); it is not new half-coverage credit.

Thus the following general dynamic candidate would suffice:

\[
 \boxed{\sum_i u_i\ge m\vartheta_{m+1}.} \tag{2?}
\]

The stronger individual version \(u_i\ge\vartheta_{m+1}\) would also suffice. Neither is proved here. The static mixed security value satisfies \(v_{m+1}\le\vartheta_{m+1}\); so an individual theta floor would imply an individual extra-slot mixed-security floor. The pure unrestricted theta value and the mixed value over a restricted real full-menu need not be ordered merely from their definitions; do not identify this candidate with Mfull.

## 2. What the free-entry potential really proves

Fix t>0 and allow an arbitrary finite multiset q of legal topics, including the empty multiset. Define

\[
 \Phi_t(q)=\sum_xH_{c_x(q)}-t|q|,\qquad H_0=0.
\]

This function has a global maximum. If L is the finite number of coverable clients and k=|q|, then \(\Phi_t(q)\le L H_k-tk\to-\infty\). Therefore only finitely many cardinalities can attain a value at least \(\Phi_t(\varnothing)=0\), and each cardinality has finitely many catalog multisets. Empty topics cannot invalidate this argument because they decrease the objective by t.

For every global maximizer q*, adding one topic cannot improve the objective, so

\[
 \max_T\sum_{x\in T}\frac1{1+c_x(q^*)}\le t. \tag{3}
\]

For every occupied topic occurrence j, deleting that occurrence cannot improve the objective, so its current unit payoff is at least t. These are one-slot insertion/deletion statements in a fixed multiset. They do not make q* a continuation of the given SPE.

If a maximizer has at most m topics, pad it with arbitrary legal topics to cardinality m. Queries decrease under this padding; (3) yields \(\vartheta_{m+1}\le t\). Consequently

\[
 \vartheta_{m+1}>t\quad\Longrightarrow\quad
 \text{every global maximizer of }\Phi_t\text{ has more than m topics}. \tag{4}
\]

There may be small locally saturated multisets even when all global maximizers are larger; (4) does not assert their absence. In particular it is not an equivalence between theta and the population of global potential maximizers.

**The unproved step:** infer (2?), or infer \(u_i\ge t\), from \(\vartheta_{m+1}>t\) and the complete SPE tree. A suffix SPE need not maximize \(\Phi_t\). Changing an earlier action can reset many later actions. Replacing a root by a profitable extra query and then recomputing the suffix is not a one-slot potential improvement. No exchange argument repairing this step has been obtained. General set catalogs do not supply the needed matroid-type exchange law.

## 3. A proved extent bound for every true deviation branch

Let \(K=\max_{T\in\mathcal S}|T|\), and fix any actual position i with actual final payoff \(u_i>0\). Force its action to A, write k=|A|, and follow the **same original full strategy** in all later histories. Let z_i(A) be that true complete branch and d_A the deviator's final payoff. Full SPE gives \(d_A\le u_i\).

If k>0 then d_A>0, and

\[
 \boxed{W(z_i(A))\le2k+(m-1)K-\frac{k^2}{d_A}
 \le2k+(m-1)K-\frac{k^2}{u_i}.} \tag{5}
\]

Proof: write c_x=c_x(z_i(A)). The m-1 other topics have at most (m-1)K incidences in total. Their incidences within A are \(\sum_{x\in A}(c_x-1)\); consequently

\[
 \begin{aligned}
 W(z_i(A))
 &=k+\left|\bigcup z_i(A)\setminus A\right|\\
 &\le k+(m-1)K-\sum_{x\in A}(c_x-1)\\
 &=2k+(m-1)K-\sum_{x\in A}c_x.
 \end{aligned}
\]

Cauchy gives \((\sum_{x\in A}c_x)(\sum_{x\in A}1/c_x)\ge k^2\), and the second factor is precisely d_A. This proves the first inequality. The map \(d\mapsto-k^2/d\) is increasing on d>0, so \(d_A\le u_i\) proves the second. For k=0, the direct incidence bound \(W(z_i(A))\le(m-1)K\) replaces the expression containing d_A.

In particular, forcing any maximum-size topic yields

\[
 \boxed{W(z_i(A))\le(m+1)K-K^2/u_i\qquad(|A|=K).} \tag{6}
\]

This is valid at all actual positions; fixed past topics remain in the same branch and count among the m-1 other topics. It does not compare old players' payoffs across branches. A low actual payoff therefore constrains the *entire coverage* of every real maximum-topic deviation branch. The relation is an upper bound on those branches, not a lower bound on the actual root welfare. A common payment connecting these branch restrictions to OPT is still missing. It does not prove (2?).

## 4. One targeted diagnosis using already certified games

Only to attack the precise new theta-extra floor, theta was recomputed by exact rational enumeration of the m-topic backgrounds in eight stored actual full-SPE inputs. The complete-SPE identity of these strategies is inherited from their existing certificates; this calculation was not a fresh independent recheck of every IC. No new instances or strategies were generated.

| Existing example name | m | min actual payoff | theta extra | A minimizing background |
| --- | ---: | ---: | ---: | --- |
| individual_security_failure | 3 | 29/3 | 23/3 | (0,1,2) |
| aggregate_theta_failure | 3 | 10 | 15/2 | (0,1,2) |
| five_individual_security | 5 | 81/5 | 69/5 | (0,1,2,3,4) |
| local_security_increment | 3 | 95/3 | 51/2 | (0,1,2) |
| eight_cce_welfare_gap | 3 | 2 | 2 | (0,0,1) |
| dynamic_iid_local | 5 | 10 | 8 | (0,1,2,6,6) |
| root_tax_failure | 4 | 9 | 26/3 | (0,0,4,4) |
| worst_cce_welfare_failure | 3 | 3 | 11/4 | (0,0,4) |

All names identify the existing files in examples/customer_attraction and evidence/certificates/customer_attraction. No counterexample here proves the candidate, gives evidence for every strategy cone, or licenses further finite negative scans. The equality in the eight-customer example also shows a fixed strict improvement of the individual candidate is impossible.

The exact diagnostic is preserved in [reproduce_extra_theta_diagnosis.py](reproduce_extra_theta_diagnosis.py). It lists all eight relative input/certificate paths explicitly, reconstructs the actual ordered path from the stored policy, evaluates all payoffs with Fraction, and enumerates the m-topic background multisets to minimize the maximum extra-player query. It retains the first minimizing multiset in lexicographic order, matching the displayed witnesses. The policy is not restricted to count dependence; only the static background query depends on counts. From the repository root, reproduce the calculation with:

```sh
python research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/direct/reproduce_extra_theta_diagnosis.py
```

The script preserves the original computation; no additional cases or checks were run when saving it.

## 5. General derivation specialized to m=5, without a new method

Equation (1) gives \(\operatorname{OPT}_5\le10\vartheta_6\). If the unproved aggregate payment (2?) were established, it would give \(W\ge5\vartheta_6\), and hence \(\operatorname{OPT}_5\le2W\). This five-player consequence is **conditional**, exactly as the general consequence is.

For (6), substitution alone gives \(W(z_i(A))\le6K-K^2/u_i\) for any maximum-size theme. It still gives no unconditional half-coverage bound.

The already proved general path-product bound, with the universally available cover weight tau<=m, gives at m=5 only

\[
 W\ge\frac{6049}{15625}\operatorname{OPT}_5,
 \qquad\operatorname{OPT}_5\le\frac{15625}{6049}W>2W.
\]

Thus this reconstruction has not crossed the requested five-player pressure test unconditionally. The only proved additional relation here is (5); it has not closed a positive general welfare step. The saturation mechanism is stopped at its exact exchange gap rather than calling global potential existence a half-coverage payment.
