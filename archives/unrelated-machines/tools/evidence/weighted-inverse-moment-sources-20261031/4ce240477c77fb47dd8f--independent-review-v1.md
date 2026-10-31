# Weighted Bernoulli shifted inverse moment — independent Exact-first review v1

Date: 2026-10-18. Reviewer: fee_cascade_review.

## 1. Provenance, scope, and verdict

I actually read the complete statement-only file
`/workspace/scratch/038d9dcc4cac/weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md`
and checked SHA256
`148cfe5ba2f6da74d9ce178281310373a31a057db2cfb0811216a4f7332c5801`.
No author Proof, other agent's new derivation, repository canonical, or external source was read for this task. The proof below was independently reconstructed from that statement. This review is scratch-only; it neither changes a repository asset nor certifies an implementation.

Verdict: **PASS in the stated domain.** Both the weighted inverse-moment inequality and the explicit nonnegative XOS log-expectation corollary follow. No high-probability, simultaneous-agent, exact transcendental evaluation, or broader valuation-class guarantee is inferred. The finite nonzero-mean inverse-moment inequality is in fact strict, although its first upper bound is sharp as a limit.

## 2. Independent proof of the inverse-moment statement

Let the finite independent Bernoulli family, weights, random sum, and mean be as stated:

\[
0\le a_j\le1,\qquad Z=\sum_j a_jX_j,\qquad
\mu=\sum_j a_jp_j>0.
\]

For every real \(z\ge0\),

\[
\frac1{1+z}=\int_0^1 t^z\,dt.
\]

For \(0<t<1\), the function \(a\mapsto t^a\) is convex. Its value on \([0,1]\) is at most the line segment between its endpoint values, so

\[
t^{a_j}\le 1-a_j+a_jt.
\]

Independence and this inequality give

\[
\begin{aligned}
\mathbb E[t^Z]
&=\prod_j(1-p_j+p_jt^{a_j})\\
&\le\prod_j\bigl(1-a_jp_j(1-t)\bigr)\\
&\le\exp\!\left(-\sum_j a_jp_j(1-t)\right)
=e^{-\mu(1-t)}.
\end{aligned}
\]

All factors are nonnegative; the last step uses \(1-x\le e^{-x}\) for \(x\ge0\). The support is finite, so the integral and expectation can be interchanged without any convergence issue. Values at the two integration endpoints do not matter. Therefore

\[
\mathbb E\frac1{1+Z}
\le\int_0^1e^{-\mu(1-t)}\,dt
=\frac{1-e^{-\mu}}\mu
\le\frac1\mu.
\]

If \(\mu=0\), every nonnegative summand has expectation zero, hence \(Z=0\) almost surely and the expectation is exactly 1. This also covers the empty index set. Thus there is no hidden division by zero or continuity convention in that case.

For finite \(J\) and \(\mu>0\), at least one \(a_jp_j>0\). For every \(0<t<1\), the corresponding exponential comparison is strict. Thus the first displayed bound is strict in this finite nonzero-mean domain. Nevertheless it is sharp as a limit: fix any \(\mu>0\), take \(n\ge\mu\), \(a_j=1\), and \(p_j=\mu/n\). Then

\[
\mathbb E\frac1{1+Z_n}
=\int_0^1\left(1-\frac\mu n(1-t)\right)^n dt
\longrightarrow\int_0^1e^{-\mu(1-t)}dt.
\]

The integrands are bounded by 1, so this limiting sharpness statement is valid. It is not needed for the asserted inequality.

## 3. Independent proof of the scaled log-expectation consequence

Let \(\nu>0\), \(0\le w_j\le\nu\), \(W=\sum_jw_jX_j\), and \(M=\sum_jw_jp_j>0\). Put \(a_j=w_j/\nu\), so \(Z=W/\nu\) and \(\mu=M/\nu\). The preceding result implies

\[
\mathbb E\frac1{\nu+W}
\le\frac{1-e^{-M/\nu}}M
\le\frac1M.
\]

For any \(V>0\), concavity of the logarithm, applied to the positive random variable \(V/(\nu+W)\), gives

\[
\begin{aligned}
\mathbb E\ln\frac V{\nu+W}
&\le\ln\mathbb E\frac V{\nu+W}\\
&\le\ln\left(\frac VM\bigl(1-e^{-M/\nu}\bigr)\right)\\
&\le\ln\frac VM.
\end{aligned}
\]

This argument does not assume \(V\ge M\), that the logarithms are nonnegative, or that the weights or probabilities are rational. The positive shift \(\nu\) makes every logarithm finite, including the event \(W=0\). Finite support makes its expectation finite. If \(M=0\), the logarithmic right side in the proposed consequence is deliberately not defined; only the preceding inverse-moment zero-mean case applies.

## 4. Independent proof of the explicit XOS corollary

Write the given finite nonnegative additive representation as

\[
v(A)=\max_{\ell\in L}\sum_{j\in A}b_{\ell j},
\qquad b_{\ell j}\ge0.
\]

Since the representation is finite, some actual clause \(\ell_*\) attains the maximum on \(S\). Set \(w_j=b_{\ell_*j}\) for \(j\in S\). Then

\[
\sum_{j\in S}w_j=v(S)>0,
\qquad 0\le w_j\le v(\{j\})\le\nu.
\]

Let \(X_j=\mathbf1[j\in T]\) for \(j\in S\), with actual probabilities \(p_j\ge p>0\). These indicators are independent by hypothesis. Set

\[
W=\sum_{j\in S}w_jX_j,
\qquad M=\sum_{j\in S}w_jp_j\ge p\,v(S)>0.
\]

The same original additive clause is a lower support at every set. Nonnegativity also permits ignoring any elements of \(T\) outside \(S\). Thus pointwise

\[
v(T)\ge\sum_{j\in T\cap S}b_{\ell_*j}=W.
\]

The map \(x\mapsto\ln(V/(\nu+x))\) decreases on \([0,\infty)\). The scaled inequality therefore yields

\[
\begin{aligned}
\mathbb E\ln\frac V{\nu+v(T)}
&\le\mathbb E\ln\frac V{\nu+W}\\
&\le\ln\frac VM
\le\ln\frac V{p\,v(S)}.
\end{aligned}
\]

Only independence of the inclusion indicators on \(S\) is needed. If \(T\) is allowed to contain other elements, their dependence on these indicators does not affect this proof. If the intended convention is \(T\subseteq S\), it is simply the same argument with no outside elements. Feasible inclusion probabilities automatically require \(p\le1\). Zero clause coefficients and elements of singleton value zero are harmless; \(v(S)>0\) ensures the selected clause has positive total weight and \(M>0\).

## 5. Boundary attacks and limits of the conclusion

The weight cap and independence are genuine hypotheses, rather than unused wording. For example, a single term with \(a=2\), \(p=1/2\) has \(\mu=1\) and inverse expectation \(2/3>1-e^{-1}\), so the first asserted bound cannot simply allow arbitrary larger weights. Likewise, two unit-weight terms with perfectly correlated common indicator of probability \(1/2\) have the same counterexample value \(2/3\) and mean 1. Both examples lie outside the Exact and therefore do not refute it.

The corollary uses an attained supporting additive clause, not submodularity, and makes no claim for a generic subadditive valuation given without this support property. Different inclusion probabilities cause no loss because the actual mean \(M\) is at least \(p\,v(S)\). There is no demand-oracle, NSW-approximation, numerical-source-constant, or promise-algorithm premise hidden in this proof. In particular, this standalone lemma does not by itself validate any previously proposed full NSW backend constant.

## 6. Finite-bit and implementation scope

The Exact is semantic for real parameters. The proof uses exact integral, exponential, and logarithm identities and inequalities; it does not purport to evaluate those transcendental expressions exactly with rational arithmetic. No software audit or enumeration was needed or run. An explicit rational XOS representation would allow finding the selected clause and its rational weights by finite exact scans, but no such algorithmic output requirement occurs in this statement.

All assertions in the Exact, including the stated zero case and the XOS expectation consequence, are independently established above. This review does not add an all-agents high-probability statement or resolve a downstream algorithm unless that algorithm's further hypotheses are separately checked.
