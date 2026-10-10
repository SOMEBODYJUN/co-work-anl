# CA-MOBIUS-SECURITY-BIAS-BARRIER: uniform-bias compilation cannot refute the individual security bridge

**Status and version:** 2026-10-10, self-contained universal proof; internally reviewed. External peer review and worldwide novelty are not certified.

Input: a finite common catalog with topic-label set P={0,…,p−1}, n≥2 unit providers, p≥n, and a customer type for every nonempty topic subset B⊆P (zero multiplicity is allowed). Let x_B be arbitrary signed real multiplicities, M=Σ_B |x_B|, and let the legal multiplicities r_B=x_B+K be nonnegative integers. The input is [CAG-MODEL](model.md). For a competitor tuple b, let h_B(b) be the number of its n−1 topics belonging to customer type B, and define

\[
f_b^r(a)=\sum_{B\ni a}\frac{r_B}{1+h_B(b)},\qquad
v_n(r)=\max_{\pi\in\Delta(P)}\min_{b\in P^{n-1}}\sum_a\pi_a f_b^r(a).
\]

Competitors may correlate but do not observe the sampled query action. This is the [oblivious mixed security value](oblivious_security.md). This statement does not impose equilibrium on the terminal profile.

**Proposition.** Put

\[
b_{p,n}=\frac{2^p-2^{p-n}}n,\qquad
c_{p,n}=\frac{2^{p-n}(2^n-n-1)}{np}.
\]

For every terminal profile s containing n different topics and every player i,

\[
\boxed{u_i^r(s)-v_n(r)\ge Kc_{p,n}-M.}
\tag{1}
\]

Consequently, the sufficient bias K=4M+1 in the full-history Möbius compiler guarantees

\[
\boxed{u_i^r(s)-v_n(r)\ge\frac14\quad\text{for every player of every n-distinct profile}.}
\tag{2}
\]

In particular, every root pure full-history SPE produced by that compiler satisfies the individual bridge and the aggregate bridge. The obstruction applies to any signed table, any auxiliary SPE, and all root-path players. It is stronger than a welfare-ratio bias obstruction.

## Proof

Choose a legal dual opponent distribution Q: select an (n−1)-element subset C of the p topics uniformly, then put one opponent on every topic of C. Ordering those opponents arbitrarily gives a legal oblivious competitor tuple. For a query topic a, its unit-uniform-bias payoff equals b_{p,n} when a∉C. When a∈C, let its value be b_old. Since C has distinct topics,

\[
b_{\rm old}=2^{p-n+1}\sum_{j=0}^{n-2}\frac{\binom{n-2}{j}}{j+2}.
\]

The fresh-minus-old difference is

\[
\delta_{p,n}=b_{p,n}-b_{\rm old}
=\frac{2^{p-n}(2^n-n-1)}{n(n-1)}.
\tag{3}
\]

For example, the finite sum follows by integrating t(1+t)^{n−2} on [0,1]. The probability a∈C is (n−1)/p. Thus every query topic has exactly the same expected unit-bias value

\[
\mathbb E_Qf_C^{\boldsymbol1}(a)
=b_{p,n}-\frac{n-1}{p}\delta_{p,n}
=b_{p,n}-c_{p,n}.
\tag{4}
\]

For a fixed player i in an n-distinct terminal profile, its own unit-bias payoff is b_{p,n}. Write d_B(a) for the probability-average coefficient of x_B in the query payoff against Q, and e_B(i,s) for its coefficient in the actual player's payoff. Both coefficients belong to [0,1], including the case where the customer does not like the respective chosen topic. Therefore

\[
\begin{aligned}
\mathbb E_Q f_C^r(a)-u_i^r(s)
&=-Kc_{p,n}+\sum_Bx_B[d_B(a)-e_B(i,s)]\\
&\le-Kc_{p,n}+\sum_B|x_B|\\
&=-Kc_{p,n}+M.
\end{aligned}
\tag{5}
\]

The same upper bound holds for every legal query a. The finite minimax definition implies v_n(r)≤max_a E_Qf_C^r(a). This proves (1).

For completeness, c_{p,n}≥1/4 throughout p≥n≥2. For fixed n, the successive ratio of 2^{p−n}/p is 2p/(p+1)>1, so its minimum occurs at p=n. Let a_n=2^n−n−1. The base a_2=1=2²/4 holds, and the exact recurrence gives

\[
a_{n+1}=2a_n+n\ge\frac{n^2}{2}+n
\ge\frac{(n+1)^2}{4},
\]

where the last difference is (n²+2n−1)/4>0 for n≥2. Thus a_n≥n²/4 and c_{p,n}≥a_n/n²≥1/4. Consequently,

\[
(4M+1)c_{p,n}-M=(4c_{p,n}-1)M+c_{p,n}\ge\frac14,
\]

proving (2). Summing (1) also gives W(s)−n v_n(r)≥n(Kc_{p,n}−M), and the sufficient-bias compiler has the explicit aggregate margin W(s)−n v_n(r)≥n/4.

The [full-history Möbius compiler theorem M2](mobius_compiler.md) separately guarantees every root SPE has n distinct topics, including the preservation of all ordered-history continuation incentives. The current proposition itself uses none of those incentives. For n=1, the equilibrium player selects a maximum-size topic, so its security value is its actual payoff, with equality. That boundary is separate from formula (3).

## Exact interpretation and limits

The displayed Q is a valid static safety dual using many tails that need not occur in the specified SPE. It is not a mixture of the actual root reply menu. No hidden randomization or continuation decorrelation is assumed.

The inequality permits noninteger signed x and K algebraically. Unit-customer instances require legal integer multiplicities r_B; the standard compiler has those. Zero multiplicities cause no difficulty. The all-zero signed table has M=0,K=1 and still gives the strict n≥2 margin.

This rules out attacks through the compiler's prescribed sufficient bias. Smaller uniform biases and nonuniform positive compensations remain outside the result. It does not prove the individual security bridge for arbitrary CAGs, or the half-coverage conjecture.

## Finite audit

[The independent exact audit](../../../tests/audits/customer_attraction_compiler_security_barrier.py) independently enumerates each static dual background and checks its exact uniform-bias value for p=2,…,8 and every 2≤n≤p. It then checks (1) on all distinct terminal subsets and all chosen topics for deterministic signed tables at those sizes, using only integer arithmetic with an LCM utility scale. Finally it applies the same static dual to the existing 12-topic four-player full-history certificate and compares its exact cap with all four actual path payoffs. These checks corroborate the formulas; the universal proof is above.

From the repository root:

```sh
python3 tests/audits/customer_attraction_compiler_security_barrier.py
```

The audit only prints by default. Its optional `--output PATH` creates a new JSON report and rejects an existing path. It resolves the saved input from its own repository location, so invocation does not depend on the working directory.
