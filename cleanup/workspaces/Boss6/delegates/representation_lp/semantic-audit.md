# Semantic audit: complete pair-incidence LP obstruction

## Source identity

- Source ID: `a03e39c3ec6ec4a9319b`
- Frozen path: `research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/complete_pair_incidence_lp_obstruction.md`
- Source blob: `b7a7e945f7c6f5c3e25a91653d6d5bc0c212ed13`
- Frozen SHA-256: `802fcfd996656278cab1a96870c46e1a14504ba5a453f75b86066e242afd9fb1`
- Size: 3,409 bytes
- Source snapshots: `68fad804ec5946cb296f77dc5b336308a66abf12` (`legacy-cleanup`) and `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` (`main`)

The complete frozen file was read. Its status is an obstruction to one specified proof interface, not a low-welfare SPE, Q-CAG-HALF counterexample, or general impossibility theorem.

## Reconstructed mathematical content

The source fixes integers $s\ge m\ge2$. There is one unit customer $x_{jk}$ for every unordered pair $1\le j<k\le s$, and exactly $s$ maximal catalogue themes

\[
B_j=\{x_{jk}:k\ne j\},\qquad j=1,\ldots,s.
\]

There are no private customers and no other themes. The maximal-incidence hypergraph is $K_s$; every customer has incidence exactly $\{j,k\}$. Choosing $m$ themes is choosing $m$ vertices, so

\[
\operatorname{OPT}_m
={s\choose2}-{s-m\choose2}
=ms-\frac{m(m+1)}2.
\tag{1}
\]

At the empty prefix the routed incidence-LP calculation uses \(p_j=0\) and \(r=m\). Every maximal theme has

\[
f_j(0,m)=\sum_{k\ne j}\frac1m=\frac{s-1}{m}.
\tag{2}
\]

The LP has one constraint $\beta_j+\beta_k\ge m$ for each edge $\{j,k\}$. Summing all ${s\choose2}$ constraints gives

\[
(s-1)\sum_j\beta_j\ge m\frac{s(s-1)}2,
\]

so $\sum_j\beta_j\ge ms/2$. The constant assignment $\beta_j=m/2$ is feasible and attains equality. Therefore

\[
B(m)=\frac{ms}{2},\qquad D_0=B(m),\qquad
D_0\max_j f_j(0,m)=\frac{s(s-1)}2.
\tag{3}
\]

The final quantity is exactly the union of all $s$ maximal themes. Thus the LP root counting inequality is tight for the global union $U={s\choose2}$, while it does not encode the fact that the comparison optimum may use only $m$ themes.

The source then isolates the interface limitation. A putative root accounting that uses the routed single-deviation functions and one nonnegative incidence multiplier vector has no \(m\)-theme-sensitive credit in this family. The direct one-step variant

\[
\operatorname{OPT}_m\le 2m\max_j f_j(0,m)
\]

would require $\operatorname{OPT}_m\le2(s-1)$, which fails by an order-$m$ factor when $s\gg m$. The looser form written in the source,

\[
\operatorname{OPT}_m\le 2D_0\max_j f_j(0,m),
\]

has right side $s(s-1)$. It is numerically true here, but is an $s$-scale overbound rather than a contradiction; the precise obstruction is that this template closes against $U$, not against the $m$-theme cap in (1). For $s=4m$, the ratio of (1) to this doubled root credit tends to $7/32$; for $s\gg m$, it is asymptotic to $m/s$.

Accordingly, the source rules out using only: (i) routing each action to one maximal theme, (ii) bounding the current deviation by \(f_j\), and (iii) paying all uncovered comparison customers through one nonnegative incidence-LP multiplier vector, as a stand-alone \(m\)-sensitive half-proof. It explicitly leaves open cross-branch continuation credit, pair-edge load balancing, and direct comparisons using (1).

## Comparison with canonical and later material

1. [`极大关联LP动态预算半覆盖--定理.md`](../../../../../archives/customer-attraction/state/定理/极大关联LP动态预算半覆盖--定理.md) gives the general routed LP with
   $B(r)=\min\sum_j\beta_j$, the dynamic budget $D_t=t+B(n-t)$, and the bound $U-c\le D_t\max_jf_j$. Its boundary paragraph already records $B(r)=sr/2$ for all-pair incidence with no private block. The present source supplies the explicit arbitrary-$s$, exact-$\operatorname{OPT}_m$ calculation and the ratio/cap interpretation that the canonical theorem only summarizes.
2. [`六极大无私有强化覆盖界--定理.md`](../../../../../archives/customer-attraction/state/定理/六极大无私有强化覆盖界--定理.md) and [`九人以上六极大强化覆盖界--定理.md`](../../../../../archives/customer-attraction/state/定理/九人以上六极大强化覆盖界--定理.md) close bounded-$s$ classes by additional path or continuation mechanisms. They do not remove the unbounded-$s$ single-multiplier interface limitation recorded here.
3. [`governance-customer-attraction/original/3f5f44f5751b6a4ad709.md`](../../../../../archives/customer-attraction/tools/evidence/governance-customer-attraction/original/3f5f44f5751b6a4ad709.md) registers the same claim as `CA-PAIR-INCIDENCE-LP-OBSTRUCTION-v1`, with scope \(K_s\), \(s\ge m\ge2\), and the non-counterexample status. No later correction in the searched canonical material changes this calculation.
4. [`固定完整策略的二主题耦合二倍界--定理.md`](../../../../../archives/customer-attraction/state/定理/固定完整策略的二主题耦合二倍界--定理.md) and [`两两非负客户投影不能共同实现--障碍.md`](../../../../../archives/customer-attraction/state/障碍/两两非负客户投影不能共同实现--障碍.md) concern a different fixed three-provider/six-label payoff system. Their v2 rank correction does not alter the \(K_s\) incidence-LP family.
5. The route5a correction in [`terminal-query-probes/.../sequential_deviation_share_lemma.md`](../../../../../archives/customer-attraction/tools/evidence/terminal-query-probes/original/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md) likewise distinguishes an interface/payment shortfall from a Q-CAG-HALF counterexample. It is a scope analogue, not a correction to the exact LP arithmetic above.

## Unique-content disposition and evidence boundary

The source is retained as a formal obstacle because it gives a reusable, fully symbolic $K_s$ family for arbitrary $s\ge m$, the exact dual lower bound $B(m)=ms/2$, equality in the union counting inequality, and the explicit loss of the $m$-theme cap. The canonical dynamic theorem contains only the compressed boundary observation; no existing state object found in the comparison search preserves this construction and its ratios in a self-contained form.

What is proved or checked here is the incidence construction, (1)--(3), the dual summation argument, and the stated asymptotic comparisons. No finite optimizer, SPE search, external referee review, or novelty check was used. The catalogue is not asserted to admit a low-welfare SPE. The result does not rule out proofs that add continuation information, use a different multiplier/flow object, or exploit the \(m\)-theme cap directly. The phrase “obstruction” therefore refers only to the named one-deviation/single-multiplier interface.

