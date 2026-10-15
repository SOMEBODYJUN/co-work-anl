# Independent review: resource-local weight bands and Shapley potential

This account was reconstructed from `MODEL.md` and the proposed mathematical objects before reading any candidate proof in `assets/R3/dense_bands/`. No novelty claim is made. The mathematical conclusion is affirmative; external-source comparison is a separate obligation.

## Exact statement reviewed

Let `R >= 1`. Consider any finite game in WC-TARGET v1, with arbitrary positive real player weights, arbitrary finite nonempty families of resource-set strategies, and resource latencies

\[
c_e(x)=\sum_{k=0}^{d}a_{e,k}x^k,\qquad a_{e,k}\geq 0.
\]

The player cost is the unweighted sum of used resource latencies. Put

\[
U_e=\{i:\exists t_i\in\mathcal S_i\text{ with }e\in t_i\}.
\]

For every resource with `U_e` nonempty, suppose

\[
\frac{\max_{i\in U_e}w_i}{\min_{i\in U_e}w_i}\leq R.
\]

Then the game has an `R`-PNE. Neither polynomial degree nor number of resources, players, or strategies enters the factor.

## Shapley bound, independently proved

For a nonempty finite active player set `S`, write `W = sum_{i in S} w_i`, and consider

\[
v(T)=W_T c(W_T),\qquad v(\varnothing)=0.
\]

Let `phi_i(S)` be its ordinary Shapley value, averaging marginal increments over all permutations of `S`. The required inequality is true:

\[
\min_{j\in S}w_j\,c(W)\ \leq\ \phi_i(S)\ \leq\ \max_{j\in S}w_j\,c(W).
\tag{1}
\]

It suffices by linearity to prove (1) for `c(x)=x^k`. Put `r=k+1` and `p_i=w_i/W`. Draw `r` independent labels from `S`, with label probabilities `p_i`. Denote the resulting ordered sequence by `Z`, its nonempty support by `A`, and its label counts by `N_i`.

Expand `W_T^r` as the sum of products over ordered `r`-tuples of labels in `T`. Each fixed tuple contributes its product exactly when every label in its support is present. Its Shapley allocation divides that product equally among the labels in its support: a label receives the marginal contribution precisely when it is last among that support in the random permutation, an event of probability `1/|A|`. Thus

\[
\phi_i(S)=W^r q_i,\qquad
q_i=\mathbb E\left[\frac{{\bf1}_{\{i\in A\}}}{|A|}\right].
\tag{2}
\]

Two elementary comparisons establish the bound.

**Ordering of the allocations.** If `p_i >= p_j`, then `q_i >= q_j`. Tuples whose support contains both labels or neither label contribute zero to `q_i-q_j`. Pair each tuple containing `i` and not `j` with the tuple obtained by swapping these labels. The support sizes are equal. If the first tuple contains `i` exactly `h >= 1` times, the probabilities of this pair have ratio `(p_i/p_j)^h >= 1`. Every paired contribution to the difference is nonnegative.

**Conditional count comparison.** Fix an attainable support `A` containing `i,j`. Conditional on this support, the positive counts `n_l >= 1`, with total `r`, have probabilities proportional to

\[
\frac{r!}{\prod_{\ell\in A}n_\ell!}\prod_{\ell\in A}p_\ell^{n_\ell}.
\]

When `p_i >= p_j`, pairing a count vector with the vector that swaps `n_i,n_j` gives

\[
\mathbb E[N_i\mid A]\geq\mathbb E[N_j\mid A].
\tag{3}
\]

In detail, pair vectors with `n_i > n_j`. Their contribution to the numerator of the conditional expectation difference is `(n_i-n_j)` times the difference of their unnormalized probabilities. The factorial denominators agree, and the probability ratio is `(p_i/p_j)^(n_i-n_j) >= 1`, so this contribution is nonnegative. Equal counts contribute zero.

Choose a global maximum-probability label `b` and a global minimum-probability label `a`. Whenever `b` belongs to `A`, (3) and the identity `sum_{j in A} N_j=r` imply

\[
\mathbb E[N_b\mid A]\geq r/|A|.
\]

When `b` is absent both relevant expressions vanish. Taking expectations therefore gives `q_b <= E[N_b]/r = p_b`. Similarly `q_a >= p_a`. The ordering comparison yields, for every label `i`,

\[
p_a\leq q_a\leq q_i\leq q_b\leq p_b.
\]

Multiplying by `W^r` proves (1) for the monomial. Nonnegative linear combination over `k` proves (1) for the stated latency polynomial. The argument uses arbitrary positive real weights and does not need integrality or rationality.

## Explicit potential and equilibrium consequence

There is a self-contained formula for the resource Shapley potential. For `S` nonempty, set

\[
H_e(S)=\sum_{k=0}^{d}a_{e,k}
\sum_{(j_1,\ldots,j_{k+1})\in S^{k+1}}
\frac{\prod_{t=1}^{k+1}w_{j_t}}{|\{j_1,\ldots,j_{k+1}\}|},
\qquad H_e(\varnothing)=0.
\tag{4}
\]

The same tuple expansion as (2) shows exactly that

\[
H_e(S)-H_e(S\setminus\{i\})=\phi_{e,i}(S).
\tag{5}
\]

Thus (4) is also the normalized Hart–Mas-Colell potential, but the proof does not require invoking an external potential theorem.

For each nonempty potential-user set use the fixed, resource-local scale

\[
m_e=\min_{j\in U_e}w_j,
\qquad
\Psi(s)=\sum_{e:U_e\ne\varnothing}\frac{H_e(S_e(s))}{m_e}.
\tag{6}
\]

Define auxiliary player costs

\[
\widehat C_i(s)=\sum_{e\in s_i}\frac{\phi_{e,i}(S_e(s))}{m_e}.
\tag{7}
\]

Since active users form a subset of potential users, (1) gives, term by term,

\[
c_e(x_e(s))\leq\frac{\phi_{e,i}(S_e(s))}{m_e}
\leq R c_e(x_e(s)).
\]

Consequently

\[
C_i(s)\leq\widehat C_i(s)\leq R C_i(s).
\tag{8}
\]

For any unilateral deviation `s -> s'=(t_i,s_{-i})`, (5) gives the exact identity

\[
\Psi(s)-\Psi(s')=\widehat C_i(s)-\widehat C_i(s').
\tag{9}
\]

Resources appearing in both old and new strategies have exactly the same active set, so their terms cancel in both sides. Removed resources use the old-set marginal; added resources use the new-set marginal. This verifies (9) for arbitrary multiresource strategies.

The finite nonempty state space has a minimizer `s*` of the real-valued function `Psi`. For each player and deviation, (9) gives `hat C_i(s*) <= hat C_i(t_i,s*_{-i})`. Together with (8),

\[
C_i(s^*)\leq\widehat C_i(s^*)
\leq\widehat C_i(t_i,s^*_{-i})
\leq R C_i(t_i,s^*_{-i}).
\]

This is exactly the requested weak-boundary `R`-PNE condition.

## Boundary and scope audit

- **Zero latency:** all tuple, Shapley, and potential terms are zero. No quotient of costs is used.
- **Zero deviation cost:** (8) implies zero auxiliary deviation cost. If current cost were positive, (9) would provide a strictly decreasing potential deviation, contradicting its minimum.
- **Both costs zero:** the equilibrium inequality holds directly.
- **Degree zero:** `r=1`; `phi_i(S)=w_i c_e`, so the argument remains valid. These games also have exact PNE by choosing individually cheapest strategies.
- **Empty strategy:** its original and auxiliary costs are empty sums equal to zero. The finite-state minimum argument is unchanged.
- **Unused resource:** when `U_e` is empty it is never active. Give it zero potential and do not take its minimum weight.
- **Singleton active set:** the Shapley value equals `w_i c_e(w_i)`, and (1) is equality.
- **Equal potential-user weights:** `R=1` gives exact PNE, even when equal weights differ between disjoint resource-user components.
- **Common resources in a deviation:** they have the same active set and cancel, as explicitly checked in (9).
- **Strict improvement and endpoint:** a violation is `C_i(s)>R C_i(s')`; (8)-(9) then force a strictly decreasing potential. The result therefore includes the factor `R` itself, with no limiting or infimum argument.
- **R must be explicit:** state `R>=1`. If every strategy is empty, the resource condition is vacuous; this does not justify calling a value below one an approximate equilibrium factor.
- **Potential users rather than current users:** the denominator in (6) must remain fixed across a deviation. Replacing it with the minimum active weight would destroy the asserted exact potential identity.
- **Algorithmic and global frontier claims:** the finite minimum proves existence, without a polynomial-time constructor and without an `o(d)` guarantee for unrestricted weights. Novelty is not assessed here.

## Independent finite check

An exact `Fraction` calculation checked (1) for all ordered integer-weight vectors in `{1,2,3,4}^n`, `n=2,3,4,5`, and all monomial exponents `r=1,...,12`, using the original subset/permutation Shapley formula. All passed. This finite check is supporting evidence only; the proof above covers all stated parameters.

## Review status

Independent reconstruction: complete. Exact small-domain check: passed. Candidate-proof comparison: pending at the time this account was first written. Literature and novelty assessment: not claimed.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
