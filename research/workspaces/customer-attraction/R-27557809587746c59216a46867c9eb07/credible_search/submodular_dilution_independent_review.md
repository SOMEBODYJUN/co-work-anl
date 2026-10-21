# Independent review: decreasing-marginal dilution coupling

Review date: 2026-10-21. Verdict: **the sharp inequality, clock construction,
and stated truncated-submodular consequence pass independent mathematical
reconstruction**. No fatal objection found. This is a pairwise representation
inequality, not a general full-tree welfare proof.

Reviewed source: `../tree_coupling/submodular_dilution_coupling.md`, SHA256
`e876f04ad8b306b33c0b889cb6e60247adac52cdb51aed2b476fa3efc9bce3c2`.
The common-marginal context was read in `common_shapley_coupling.md`, SHA256
`a7fc8252469dd73f570d3e3500a0005b76e878a8cd8ec682baf73c3ec8150794`.
No finite search or author's optimizer conclusion is used in this review.

## Exact rate-vector quantifiers

P is finite, q,r≥0 coordinatewise, q_a>0 **and r_a>0**, and g is one common
nonnegative decreasing function on subsets of P\\{a}. The phrase “another such
vector r” in the source supplies r_a>0; spelling it out would remove ambiguity.
All rates may otherwise be arbitrary finite real numbers and may be zero.
Every q(T) with a∈T is positive, the finite maximum κ exists, and κ>0.

For s=κq, maximality of κ implies, for D={b≠a:r_b>s_b},

\[
s_a-r_a\ge\sum_{b\in D}(r_b-s_b)\ge0.
\]

This follows by applying s(T)≥r(T) to T={a}∪D. Conversely this inequality,
with that D, implies s(T)≥r(T) for every T containing a, because any sum of
deficits over a subset is bounded by the sum of all positive deficits. Thus
the kill budget condition is exactly the required subset-ratio domination,
not an extra unproved coupling assumption.

## Joint clock law and within-process independence

Construct independent primitive exponential clocks as follows:

- K, rate r_a, kills both processes.
- C_b, rate min(s_b,r_b), activates b in both.
- E_b, rate s_b−r_b when positive, activates b only in s.
- D_b, rate r_b−s_b when positive, activates b only in r and kills s.
- H, rate s_a−r_a−sum_b(r_b−s_b)_+, kills only s.

Omit zero-rate clocks. The s kill time is min(K,H,all D_b); its own activation
times are minima of C_b and E_b, when the latter exists. These use **disjoint
primitive families**, so its kill time is independent of all its own
activations; each activation rate is exactly s_b and the kill rate is s_a.
The r kill time is K, while its activations are minima of C_b and D_b. These
also use disjoint primitive families within r, giving rate r_a and independent
activation rates r_b. Activations for different b are mutually independent
within either process. A D_b clock being shared across the two processes is
therefore legitimate: it is not shared between kill and activation within
one marginal process.

Pathwise A_s≤A_r. Before A_s, no D_b has rung. Every b already activated in r
must then have activated through a common C_b, so R_r(t)⊆R_s(t) for t<A_s.
Decreasing g gives g(R_s(t))≤g(R_r(t)) on that interval. Nonnegativity pays
the remaining integral over [A_s,A_r). Hence

\[
\int_0^{A_s}g(R_s(t))\,dt\le
\int_0^{A_r}g(R_r(t))\,dt.
\]

Events at a kill endpoint have Lebesgue measure zero. Tonelli and the verified
within-process independence identify expected integrals with L_a(s;g) and
L_a(r;g). Rescaling time gives L_a(κq;g)=L_a(q;g)/κ, proving the inequality.
The bounds by g(empty)/q_a and g(empty)/r_a justify finiteness. Zero activation
rates and empty D are covered by the same construction.

For a maximizing T, g(R)=1_{R∩(T\\{a})=empty} gives integrals1/q(T) and1/r(T),
so κ is sharp. This witness is itself a single coverage-customer marginal,
so sharpness does not require an exotic non-realizable decreasing function.

The assumptions are load-bearing. Without decreasingness, q=(1,1), r=(1,0),
and g(R)=1_{b∈R} give κ=1 but L(q)=1/2>L(r)=0. Without nonnegativity,
g≡−1, q=(1,1), r=(1,3) give κ=2 but −1>−2. Neither excluded example is an
objection to the stated theorem.

## Independent reconstruction of the repeated-topic Shapley connection

For integer q, tag one provider choosing a and give every provider an
independent rate-one exponential priority. Their order is a uniform random
permutation. Conditional on the tagged priority being t, it has density
e^(−t). Its marginal contribution is zero if an earlier provider chose a;
the probability that none of the other q_a−1 such providers is earlier is
e^(−(q_a−1)t). Each other topic b appears earlier independently with
probability1−e^(−q_b t). Thus its Shapley payoff is exactly

\[
\int_0^\infty e^{-q_at}\,
\mathbb E[C(R_q(t)+a)-C(R_q(t))]dt.
\]

This independently recovers the claimed L representation, including repeated
labels, without using a nonnegative customer realization or assuming topics
are chosen distinctly. For noninteger rates the L inequality remains true;
only the literal tagged-provider interpretation uses integer q.

The same C must supply both q and r marginals. The result would not apply to
independently chosen set functions at different terminal counts. Ordered
histories and tie-breaking never enter this static pairwise identity, so it
can be imposed at any relevant pair of terminal states without constraining
how the strategy chose those states.

## Truncated domain: no missing submodular extension

Suppose C is specified only for |S|≤m, is monotone there, and satisfies
submodularity whenever the union in that inequality has size≤m. Define g on
|R|≤m−1 by C(R+a)−C(R). Monotonicity gives g≥0. If R⊆S and |S|≤m−1, apply
submodularity to R+a and S. Their union S+a has size≤m, yielding g(R)≥g(S).
No unavailable set-function value is used.

Positive integer q_a,r_a and integer total counts≤m imply
|supp(q)\\{a}|,|supp(r)\\{a}|≤m−1. Multiplication by κ changes no support, so
the s and r processes always evaluate g on its defined domain. Before A_s,
the actual inclusion R_r(t)⊆R_s(t) is between sets of size≤m−1, so the needed
decreasingness comparison is available. After A_s only r's nonnegative
integrand is used, also within that domain.

Alternatively set g(X)=0 on every previously undefined set |X|≥m. This is a
nonnegative decreasing extension of g, sufficient to invoke the full-domain
lemma. It is **not** an asserted monotone submodular extension of C, and no
such extension is needed.

The support-size argument is important: allowing arbitrary positive real
counts of total≤m would not by itself bound the support. For instance with
m=1 and q=(1/2,1/4,1/4), g is supplied only at the empty set but both other
topics can activate. The source correctly restricts its truncated consequence
to integer counts; the general full-domain rate lemma has no such restriction.

## Consequence and review boundary

Every same-topic sharp dilution constraint comparing integer count states of
total≤m is redundant once payoffs come from one common monotone submodular
truncated C via this marginal formula. Therefore removing these constraints
from the stated fixed-strategy/common-submodular LP leaves exactly the same
feasible set. Conditional on the separately certified fixed-cone optimum3/2,
its value remains3/2 after their removal. This review reconstructs the
redundancy theorem; it does not re-audit all numerical hierarchy certificates,
make a novelty claim, or turn the fixed-cone result into a general half bound.
