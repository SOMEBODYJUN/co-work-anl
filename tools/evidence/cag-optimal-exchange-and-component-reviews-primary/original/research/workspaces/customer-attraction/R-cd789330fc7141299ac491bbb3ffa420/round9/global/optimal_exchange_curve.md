# Optimal-comparator exchange curve on every full leaf

2026-10-24, Boss10 round 9, global subagent. **Q-CAG-HALF remains OPEN.**
This note proves one joint actual/comparator incidence relation for arbitrary
numbers of players and arbitrary common catalogs. It uses optimality, not SPE.
It gives no new unconditional welfare approximation. Exchange9 independently
checked (EX-t), (EX-q), (EX-H), and (EX-1), including the event factorization,
slot independence, beta integral, and endpoint limits; no fatal issue was
found. Review is recorded in `../exchange/peer_component_reviews.md`. No
external review or novelty claim is made.

## Exact relation

Fix an optimal ordered tuple of legal themes
`T=(T_1,...,T_m)`, and let `C=union_i T_i`. Fix *any* other full legal tuple
`S=(S_1,...,S_m)`; it can be the actual SPE leaf, any off-path true leaf, or
another arbitrary tuple. Put

\[
k_x=\#\{i:x\in T_i\},\qquad c_x=\#\{j:x\in S_j\},
\]

and write `B=union_j S_j`, `I=C intersection B`, `R=C minus B`,
`E=B minus C`. For `1<=k<=m` and `0<=c<=m`, define

\[
q_m(k,c)=\frac{\binom{m-c}{k}}{\binom m k},
\]

where the numerator is zero when `k>m-c`. For every real `0<=t<=1`,

\[
\boxed{\quad
\sum_{x\in E}\bigl[1-(1-t)^{c_x}\bigr]
\le
\sum_{x\in C}q_m(k_x,c_x)t^{k_x}(1-t)^{c_x}.
\quad}\tag{EX-t}
\]

All customers are still unit customers; sums include their integer
multiplicities. Repeated comparison themes, repeated themes in `S`, empty
themes, and zero multiplicities are permitted. `t` is a proof parameter,
not a mixed action or a provider weight.

## Proof by legal equal-cardinality replacement

Choose a uniform random bijection `pi` from the `m` slots of `S` to the `m`
slots of `T`. Independently select every `S` slot with probability `t`.
For every selected slot `j`, replace `T_{pi(j)}` by `S_j`. The resulting
tuple has exactly `m` legal themes, for every realization. Consequently its
coverage is at most `|C|` pointwise, by optimality of `T`.

A customer in `E` is gained precisely when at least one of its `c_x`
covering `S` slots is selected, with probability `1-(1-t)^{c_x}`.

A customer in `C` is lost precisely when (a) none of its `c_x` covering
`S` slots is selected and (b) all of its `k_x` covering `T` slots are
replaced. The inverse images under `pi` of those `k_x` slots form a
uniform `k_x`-subset of the `S` slots. They must all avoid the `c_x`
covering slots, which has probability `q_m(k_x,c_x)`. Conditional on that
event, all `k_x` inverse-image slots must be selected and the disjoint
`c_x` covering slots must not be selected. This gives the exact loss
probability `q_m(k_x,c_x)t^{k_x}(1-t)^{c_x}`.

Coverage difference equals gains from `E` minus losses from `C`. Take its
nonpositive expectation to prove (EX-t). There is no assumption about
incentives or about how the tuple `S` was reached.

## Fixed-cardinality and harmonic forms

Selecting exactly `q` uniformly random `S` slots and replacing an independent
uniform `q`-subset of the `T` slots yields, for `0<=q<=m`,

\[
\sum_{x\in E}\left[1-\frac{\binom{m-c_x}{q}}{\binom m q}\right]
\le
\sum_{x\in C}
\frac{\binom{m-k_x}{q-k_x}}{\binom m q}
\frac{\binom{m-c_x}{q}}{\binom m q}.
\tag{EX-q}
\]

The first factor on the right is the probability that all `k_x` comparison
covering slots are removed. This experiment is distributionally identical to
the matched replacement conditional on the number of selected slots being
`q`. Thus (EX-t) is the binomial mixture of (EX-q), not an extra dynamic
assumption.

Integrating (EX-t) against `dt/t` on `(0,1)` is valid because all sums are
finite and every term has a finite nonnegative integral. With `H_c` the
ordinary harmonic number and `Beta` the Euler beta integral, it gives

\[
\boxed{\quad
\sum_{x\in E}H_{c_x}
\le \sum_{x\in C}q_m(k_x,c_x)\operatorname{Beta}(k_x,c_x+1)
=\sum_{x\in R}\frac1{k_x}
 +\sum_{x\in I}q_m(k_x,c_x)
   \frac{(k_x-1)!c_x!}{(k_x+c_x)!}.
\quad}\tag{EX-H}
\]

The identity on the left uses
`[1-(1-t)^c]/t=sum_(j=0)^(c-1)(1-t)^j`. On `R`, `c_x=0`, so
`q_m(k_x,0)=1` and `Beta(k_x,1)=1/k_x`.

The first-order limit `t downarrow 0` gives the useful single-swap summary

\[
\sum_{x\in E}c_x
\le\sum_{x\in C:k_x=1}\left(1-\frac{c_x}{m}\right).
\tag{EX-1}
\]

This records that repeated coverage of customers outside an optimal union
requires comparator-private customers that are not too heavily covered by
the replacement tuple. At `t=1`, (EX-t) reduces to `|E|<=|R|`, the usual
comparison of the two full unions.

## Relation to the general proof obligation

All displayed inequalities hold simultaneously for every leaf in a fixed
full strategy tree, with the *same* comparator `T` and the same `k_x`.
They could therefore be included when deriving a dynamic budget involving
actual and off-path leaves. They retain actual load and optimal incidence
together, rather than retaining only union sizes.

The direction is essential. (EX-H) bounds external repeated coverage by a
weighted missing/private-comparator quantity. It does **not** pay missing
customers from actual profits, and cannot be substituted for
`|R|<=|I|+2|E|`, which would prove half coverage. In particular, an action
whose theme label is outside `{T_1,...,T_m}` may still be entirely inside
`C`; these inequalities do not control that label mismatch.

For the prescribed pressure test, the same mechanism at `m=5` gives

\[
\sum_{x\in E}[1-2^{-c_x}]
\le\sum_{x\in C}2^{-(k_x+c_x)}
\frac{\binom{5-c_x}{k_x}}{\binom5{k_x}}.
\]

This is valid for every five-player input and every true leaf but does not
imply `OPT_5<=2W`. For example, on the large valid input class where an
optimal tuple covers the entire catalog universe, `E` is empty on every
leaf and (EX-t) alone has a zero left side. It must be combined with a new
SPE relation. This observation identifies the actual mathematical limit;
no finite search or special-five-player project is being used as evidence.

## Derivation attempts not promoted

Random optimal-prefix forcing does not justify treating the last forced
theme as an exchangeable owner conditional on the continuation leaf. The
given strategy can depend on the full ordered prefix, so the continuation
can correlate with the last forced topic. No payment was obtained by that
route. Likewise, no all-background extra-slot or individual security floor
was assumed; those stronger statements have existing counterexamples.
