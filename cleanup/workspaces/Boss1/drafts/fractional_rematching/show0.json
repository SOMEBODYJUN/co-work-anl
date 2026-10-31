# Fractional rematching and deterministic explicit-XOS robust-gap boundary — author Proof v5

Date: 2026-10-18. Author role: internal mathematical author for root/boss11. Drafting began after the reading described below; the source-reading checkpoint was 2026-10-18T13:17:00Z. This is a new author proof of the frozen Exact v5, not an independent or blind review, and not a replacement proof retroactively attached to an earlier version.

## 0. Frozen target, sources, and status

The target is `fractional_rematching_extension_statement_only_v5.md`, SHA256 `3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e`. It was the first substantive file read for this author task and was displayed and read in full before reading the following materials. The following supplied hashes were also actually recomputed and matched:

| Material actually read | SHA256 | Actual reading scope |
|---|---|---|
| `sol_nsw_v5_exact_first_attack.md` | `a900867a462b030db5cb2556f68f992b89efce28936a5c2658b13aeb03d7d306` | Full text, after Exact v5 |
| `weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md` | `891c56ecb28481957e93adb3e70e80ae946e152d440e901aebcdcb17421584c7` | Full text |
| `finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md` | `8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad` | Full text |
| `dlrv_2023_subadditive_nash_social_welfare_v1.txt` | `10fb320d3a7aaccb3baf579b657b3bcfecd931c45133df3f14337ce1e94829fb` | Full supplied text, physical lines 1–1391, in displayed segments |

An initially truncated display of the primary source's lines 226–450 was subsequently replaced by a separate, untruncated display of that entire interval. No unshown portion is being counted as read. No PDF was read, and no PDF hash is claimed. No earlier v1–v4 file or other review was read for this task. References here to the earlier process are limited to the disclosures in the frozen v5 and the explicitly listed materials. Those earlier files and objections are not edited by this proof.

The primary source is Dobzinski, Li, Rubinstein, and Vondrák, *A constant factor approximation for Nash social welfare with subadditive valuations*, arXiv:2309.04656v1, [source URL](https://arxiv.org/html/2309.04656v1). Its Sections 2.1–2.5 and Appendix B supply the inherited singleton-matching, splitting, iteration, and rematching framework. Its published integral-OPT approximation theorem is not used as a fractional log-CONFIG theorem. We prove the fractional matching interface separately. We also prove the explicit-XOS residual solver, support-respecting deterministic welfare rounding, shifted additive inverse moment, and finite-grid derandomization below, rather than importing the disputed generic-subadditive numerical route.

Reading a previously frozen independent attack and the two author tools before writing makes this an informed author reconstruction. It is not a new blind test or a new independent verdict. The argument below is self-contained at the level of the theorem: the only standard computational primitives used without rederiving their algorithms are deterministic rational linear programming, bipartite matching, exact integer/rational arithmetic, and their usual polynomial bit complexity. The logarithmic approximation and product-separation details needed here are supplied explicitly.

The algorithms are mathematical specifications. No backend executable was implemented or tested for this proof, and there is no software-audit claim, asset registration, external communication, source-hardness claim, or global-novelty claim.

## 1. Conventions and elementary computational facts

An allocation is a family of pairwise disjoint subsets of the original item set; it may leave items unallocated. Write \(v_i(j)=v_i(\{j\})\). Products and geometric means use all the original \(n\ge1\) agents. A positive fractional benchmark means that every configuration with positive mass has strictly positive actual value, so all logarithms in that benchmark are finite.

For explicit XOS tables, all maxima are over the given finite indexed clause lists. A deterministic attaining clause can always be chosen by its first index. The valuation is monotone and subadditive: if \(s\) attains \(v_i(S\cup T)\), then

\[
v_i(S\cup T)=\sum_{j\in S\cup T}p_{i,s,j}
\le\sum_{j\in S}p_{i,s,j}+\sum_{j\in T}p_{i,s,j}
\le v_i(S)+v_i(T).
\tag{1.1}
\]

In particular \(v_i(T)\le\sum_{j\in T}v_i(j)\), and removing one item \(j\) decreases value by at most \(v_i(j)\). A positive XOS-valued set contains a positive singleton. Rational sums, comparisons, products, division by a nonzero rational, and floors of rational numbers have polynomial bit cost in their binary representations. A division creates a binary numerator/denominator representation; it does not mean making a number of copies equal to a reciprocal.

### 1.1 Certified rational approximations to logarithms

For a positive rational \(x\), find an integer \(e\) with \(x=2^e y\) and \(1\le y<2\). Its absolute value is bounded by the combined binary lengths of the numerator and denominator of \(x\), plus a constant. Set \(z=(y-1)/(y+1)\in[0,1/3)\). Then

\[
\ln y=2\sum_{k=0}^{\infty}\frac{z^{2k+1}}{2k+1}.
\tag{1.2}
\]

After \(N\) terms the tail is at most

\[
\frac{2z^{2N+1}}{(2N+1)(1-z^2)}\le 9^{-N}.
\tag{1.3}
\]

The same series with \(z=1/3\) approximates \(\ln2\) with that bound. Thus the rational approximation to \(e\ln2+\ln y\) has error at most \((|e|+1)9^{-N}\). Given a positive rational absolute tolerance \(\alpha\), take \(N\) so this is at most \(\alpha\). This requires polynomially many rational operations and polynomial bit length in the binary description of \(x,\alpha\); in particular the number of terms is polynomial in the bit length of \(x\) and \(\log(1+1/\alpha)\). Exact rational summation of these polynomially many terms remains polynomial in those lengths. Negative logarithms are obtained by changing sign.

This construction handles positive rational arguments smaller than any fixed numerical constant. Its cost depends on their bit lengths, not on their reciprocals by value.

### 1.2 Exact maximum-product matching using finite precision

Consider a bipartite graph with \(n\) left vertices, with every left vertex to be matched to a different right vertex. Edge factors are nonnegative rationals. Delete zero-factor edges and first test ordinary matching feasibility. If a positive perfect matching exists, let \(L\ge1\) bound the binary magnitudes of every positive edge numerator and denominator: each is at most \(2^L\).

Every matching product can be written as \(P=A/B\), with positive integers \(A,B\le2^{nL}\). For two distinct products \(P=A/B>Q=C/D\), the integers satisfy \(AD-BC\ge1\), and hence

\[
\ln P-\ln Q
=\ln\frac{AD}{BC}
\ge\ln(1+2^{-2nL})
\ge 2^{-2nL-1}=:G.
\tag{1.4}
\]

Approximate each edge logarithm by a rational within \(G/(4n)\), using §1.1. The error in any matching's total weight is at most \(G/4\). Therefore the approximate weight order of every pair with unequal true products is correct: its gap is at least \(G-2(G/4)>0\). Exact maximum-weight matching on these rational approximate weights consequently returns a true maximum-product matching. Equal true products may be resolved by any fixed deterministic tie rule.

The required precision has \(O(nL+\log n)\) binary bits, so all of this is polynomial in the finite rational input. The right side may have more than \(n\) vertices, as in the initial singleton matching. This argument needs no exact symbolic logarithm and no comparison with an irrational benchmark. It will apply to A's factors, B's initial singletons, and B's final actual bundle-plus-singleton factors.

## 2. Proof of A: a general subadditive fractional-benchmark matching

Here are the hypotheses of A in full. The set \(U\) is finite, \(H\subseteq U\) consists of exactly \(n\ge1\) distinct items, and \(B=U\setminus H\). Each \(v_i:2^U\to\mathbb Q_{\ge0}\) is finite, monotone, subadditive and has \(v_i(\varnothing)=0\). Nonnegative rational targets \(V_i\) and a rational \(c\ge1\) are given. Put \(A=\{i:V_i>0\}\) and assume \(v_i(B)=0\) for \(i\notin A\). The finite rational configuration list \(y\) obeys

\[
y_{i,S}\ge0,\quad \sum_S y_{i,S}=1,\quad
\sum_{i,S:j\in S}y_{i,S}\le1\quad(j\in U),
\tag{2.A}
\]

and every listed positive entry has \(v_i(S)>0\). Its benchmark is

\[
\mathcal B(y)=
\exp\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right)>0.
\tag{2.B}
\]

Assume further that every feasible fractional family \(z\) on the agents \(A\) and residual items \(B\), with nonnegative masses, row sums one and item columns at most one, satisfies

\[
\sum_{i\in A,T\subseteq B}z_{i,T}\frac{v_i(T)}{V_i}\le cn.
\tag{2.C}
\]

For \(A=\varnothing\) this condition is vacuous; the stronger upper bound \(c|A|\) also suffices. These are precisely A1–A2 of the frozen Exact. The proof uses the semantic valuation assumptions and only finitely many values; it does not require a representation of all subsets or a procedure for verifying (2.C).

Set \(a_{ih}=v_i(h)\) and \(f_{ih}=V_i+a_{ih}\) for \(h\in H\). The set \(H\) here is any specified set of \(n\) distinct original items; no optimality property of \(H\) is needed in A.

### 2.1 A configuration-labelled fractional perfect matching

For each positive entry \((i,S)\) with \(S\cap H\ne\varnothing\), choose an item \(h(i,S)\in S\cap H\) maximizing \(a_{ih}\), and send its entire mass \(y_{i,S}\) to edge \((i,h(i,S))\). The partial matrix has row sums at most one. Its column sum at \(h\) is at most the original total mass of configurations containing that actual item, so it is at most one. This argument uses original item identities, not independently reusable configuration coordinates.

The deficit in row \(i\) is exactly the mass of configurations with \(S\cap H=\varnothing\). If \(i\notin A\), monotonicity and \(v_i(B)=0\) imply that such a set has value zero, so no positive entry in that row has this form. Every deficit row is therefore in \(A\), where \(V_i>0\).

Total row deficit equals total column deficit, since there are \(n\) rows and \(n\) columns. Fill these deficits by a nonnegative transportation matrix between the deficit rows and deficit columns. Keep the configuration labels by splitting each \(H\)-empty entry among the items used to fill its row. This yields numbers \(\widetilde y_{i,S,h}\ge0\) with

\[
\sum_h\widetilde y_{i,S,h}=y_{i,S},\qquad
q_{ih}:=\sum_S\widetilde y_{i,S,h},\qquad
\sum_hq_{ih}=1,\quad\sum_iq_{ih}=1.
\tag{2.1}
\]

Every used edge has \(f_{ih}>0\). For \(i\in A\) this follows from \(V_i>0\). For \(i\notin A\), the entry has a representative maximizing the singleton in \(S\cap H\). If that maximum were zero, subadditivity would give

\[
v_i(S)\le v_i(S\cap B)+\sum_{h\in S\cap H}v_i(h)=0,
\]

contrary to the benchmark's positivity. Thus its representative singleton, and therefore \(f_{ih}\), is positive.

### 2.2 The residual fractional premise controls the total ratio

For a coupled entry define \(T=S\cap B\) and \(k=|S\cap H|\). If \(i\in A\) and \(k>0\), the representative property and subadditivity imply

\[
v_i(S)\le v_i(T)+k a_{ih},\qquad
\frac{v_i(S)}{f_{ih}}\le\frac{v_i(T)}{V_i}+k.
\tag{2.2}
\]

If \(i\in A\) and \(k=0\), the second inequality follows simply from \(f_{ih}\ge V_i\). If \(i\notin A\), we have \(k>0\), \(v_i(T)=0\), and \(f_{ih}=a_{ih}>0\), so the ratio is at most \(k\).

Project the configurations of the rows in \(A\) onto \(B\), adding masses of equal projected subsets. Their row sums remain one and their item columns remain at most one. This is a feasible *fractional* residual configuration family. The full fractional quantifier in A2 gives

\[
\sum_{i\in A,S}y_{i,S}\frac{v_i(S\cap B)}{V_i}\le cn.
\tag{2.3}
\]

The original item capacities also give

\[
\sum_{i,S}y_{i,S}|S\cap H|
=\sum_{h\in H}\sum_{i,S:h\in S}y_{i,S}\le n.
\tag{2.4}
\]

Combining (2.2)–(2.4), and observing that splitting a configuration preserves its total mass, yields

\[
\sum_{i,S,h}\widetilde y_{i,S,h}
 \frac{v_i(S)}{f_{ih}}\le(c+1)n.
\tag{2.5}
\]

All ratios occurring with positive mass are strictly positive, and total coupled mass is \(n\). Jensen's inequality for \(\ln\), with weights \(\widetilde y/n\), therefore gives

\[
\sum_{i,S}y_{i,S}\ln v_i(S)
\le \sum_{i,h}q_{ih}\ln f_{ih}+n\ln(c+1).
\tag{2.6}
\]

### 2.3 Extracting a permutation and implementing the conclusion

A doubly stochastic matrix \(q\) is a convex combination of permutation matrices supported on its positive edges. For completeness, its positive graph satisfies Hall: the mass \(|I|\) of any row set \(I\) can only reach its neighboring columns, of total capacity \(|N(I)|\). A perfect matching therefore exists. Subtract the smallest positive entry on such a matching; if residual mass is nonzero, rescale and repeat. Each nonfinal subtraction removes at least one positive edge and creates none, so this gives a finite permutation decomposition.

At least one permutation in that decomposition has log product at least \(\sum q_{ih}\ln f_{ih}\). Equation (2.6), followed by division by \(n\) and exponentiation, proves

\[
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}
\ge\frac{\mathcal B(y)}{c+1}.
\tag{2.7}
\]

This also proves that the positive-factor graph has a perfect matching. A true maximum-product matching on those factors, computed by §1.2, satisfies the same bound and uses only \(V_i\) and the \(n^2\) singleton values on \(H\). It does not compute \(\mathcal B(y)\), solve an exponential configuration LP, or verify A2. Its exact guarantee immediately implies the allowed approximate version for every explicit \(\epsilon>0\).

The argument includes \(A=\varnothing\), \(B=\varnothing\), zero singleton values, zero \(V_i\), and repeated subset entries. With \(A=\varnothing\), no row deficit is present and the residual sum is empty. With \(B=\varnothing\), residual values vanish. Neither case introduces a zero logarithm on a used edge. This completes A in its general monotone-subadditive semantic scope.

## 3. Proof of B1–B2: the total branch and rational residual solver

From now on \(n\ge1\), \(U\) is any explicit finite set of \(m\ge0\) items, and each agent has a nonempty finite indexed list of clauses specifying

\[
v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},
\qquad p_{i,s,j}\in\mathbb Q_{\ge0}.
\tag{3.X}
\]

All coefficients are explicitly binary encoded. Their totals may be unequal, unbounded, or zero. This is the arbitrary explicit-XOS input domain of B, without normalization or a numerical-grid promise.

### 3.1 The no-positive-matching branch is correct

Build the singleton graph on all agents and all original items, retaining exactly the edges with positive singleton value. If it has no matching covering all agents, Hall gives an agent set \(I\) with \(|N(I)|<|I|\). A positive actual allocation would allow each agent in \(I\) to choose a positive singleton from its bundle, and disjointness would give \(|I|\) different neighboring items. This is impossible. Thus optimal actual NSW is zero.

If a finite positive fractional benchmark existed, each of its support configurations for every \(i\in I\) would contain at least one item in \(N(I)\). Hence

\[
|I|\le\sum_{i\in I,S}y_{i,S}|S\cap N(I)|
\le\sum_{j\in N(I)}\sum_{i,S:j\in S}y_{i,S}
\le|N(I)|,
\tag{3.1}
\]

a contradiction. Returning empty bundles is consequently a valid total output in this branch. It includes \(m=0\), \(n>m\), and an agent with no positive singleton.

In the other branch compute a true maximum-product positive singleton matching \(\tau\) over **all original items**, by §1.2, and put \(H=\tau([n])\), \(B=U\setminus H\). The global optimality over \(U\) will be needed only in the rematching lemma below.

Let \(A=\{i:v_i(B)>0\}\). If \(A=\varnothing\), set every target \(V_i=0\), take no residual configurations or candidates, and use the final matching branch described below. This includes \(B=\varnothing\). Otherwise put \(a=|A|\ge1\).

### 3.2 Exact row normalization and the fixed lift

For \(i\in A\), compute \(W_i=v_i(B)>0\). Directly evaluating every original clause on \(B\) finds it and an attaining clause. Define \(\widehat p_{i,s,j}=p_{i,s,j}/W_i\) on \(B\). Each residual normalized clause has total at most one; an attaining clause has total exactly one. The divisions have polynomial binary length in the explicit input. There is no iteration proportional to \(1/W_i\).

Let \(P\) be the following fixed lift polytope, with \(i\in A\), original indexed clauses \(s\), and \(j\in B\):

\[
\lambda_{i,s}\ge0,\qquad\sum_s\lambda_{i,s}=1,\qquad
0\le z_{i,s,j}\le\lambda_{i,s},\qquad
\sum_{i\in A,s}z_{i,s,j}\le1\quad(j\in B).
\tag{3.P}
\]

Let \(R\) be its image under

\[
u_i=\sum_{s,j\in B}\widehat p_{i,s,j}z_{i,s,j}.
\tag{3.2}
\]

All lift coordinates lie in \([0,1]\), and

\[
0\le u_i\le\sum_s\lambda_{i,s}\sum_{j\in B}\widehat p_{i,s,j}\le1.
\tag{3.3}
\]

For each active agent choose a normalized total-one clause, put its \(\lambda=1\), and put \(z=1/a\) on all its residual items in that clause. All other coordinates are zero. Each item column sums to one, and each utility is \(b_i=1/a\). This is the specified feasible lift of \(b\).

The lift contains the utility vector of **every** feasible fractional residual configuration family. To see this, choose an actual attaining indexed clause for each configuration \(T\). Let \(\lambda_{i,s}\) be the total mass assigned to clause \(s\), and \(z_{i,s,j}\) the mass assigned to it that also contains \(j\). The row, domination, and item-capacity constraints of \(P\) hold, and (3.2) is exactly that family's expected actual normalized utility. This is a semantic inclusion for all feasible families; the algorithm never enumerates them.

Conversely, any rational lift can be converted to a polynomial-support configuration family. For each \(\lambda_{i,s}>0\), sort the marginals \(q_j=z_{i,s,j}/\lambda_{i,s}\) in nonincreasing order \(q_1\ge\cdots\ge q_b\), where \(b=|B|\). Put \(q_0=1,q_{b+1}=0\); give the nested set containing the first \(k\) items probability \(q_k-q_{k+1}\) for \(k=0,\ldots,b\). This distribution has exactly the stated marginals. Multiply its probabilities by \(\lambda_{i,s}\) and combine the clauses. There are at most \(b+1\) subsets per positive clause. Its expected value under the assigned clause is exactly (3.2), and its expected *actual* XOS value is at least (3.2). Its item columns are the original lift columns. All probabilities have polynomial bit length whenever the lift does.

### 3.3 Termination of the rational iteration

Set \(\ell=1/(4a)\), \(h=\ell^2/2=1/(32a^2)\), and \(R'=b/4+3R/4\). Convexity gives \(R'\subseteq R\). Every coordinate of a point in \(R'\) lies in \([\ell,1]\), and \(b\in R'\). Maintain a full feasible lift of the current \(x\), starting from the above lift of \(b\).

Solve the rational LP

\[
M=\max_{w\in R}\sum_iw_i/x_i,
\tag{3.4}
\]

on the fixed lift \(P\), returning a basic optimal lift. If \(M\le2a\), stop. Otherwise form \(y=b/4+3w/4\in R'\), and update the full lift by the same convex operation giving \(x\leftarrow(1-h)x+hy\). This preserves membership in \(R'\).

For analysis only let \(F(x)=\sum_i\ln x_i\); the algorithm does not evaluate it. Write \(D=y-x\). If \(M>2a\), then

\[
\nabla F(x)\mathbin\cdot D
=\tfrac14\sum_i b_i/x_i+\tfrac34M-a>a/2.
\tag{3.5}
\]

Along the update segment all coordinates are at least \(\ell\), the Hessian of \(F\) is diagonal with entries \(-1/x_i^2\), and \(\sum_iD_i^2\le a\). Taylor's theorem with its integral remainder therefore gives

\[
\begin{aligned}
F(x+hD)-F(x)
&\ge h\nabla F(x)\mathbin\cdot D
 -\frac{h^2}{2\ell^2}\sum_iD_i^2\\
&>\frac{\ell^2a}{8}=\frac1{128a}.
\end{aligned}
\tag{3.6}
\]

Initially \(F(b)=-a\ln a\), and always \(F\le0\). For \(a\ge2\), the number of updates is less than \(128a^2\ln a<128a^3\). For \(a=1\), \(x=1\) initially and \(M\le1\), so there are no updates. The claimed bound of at most \(128a^3\) updates follows.

### 3.4 Fixed-vertex bit bounds, without an objective-length recurrence

Let \(D_P\) be the explicit number of lift variables. The constraints of \(P\) have coefficients in \(\{0,1,-1\}\) and right sides in \(\{0,1\}\); this matrix is fixed throughout the iteration. At any vertex, choose a full-rank square system of active equations defining it. Cramer's rule and Hadamard's determinant bound give a numerator/denominator bound of \(O(D_P\log(D_P+2))\) bits per coordinate, independent of the current objective coefficients \(1/x_i\). One may use a single determinant as a common denominator for the coordinates of that vertex.

A deterministic rational LP solver may return a basic optimum. Equivalently, after optimizing (3.4), successively optimize coordinates on its optimal face to obtain a fixed lexicographic vertex. Each restriction is a face; the final singleton face is a vertex of the original \(P\), so the same objective-independent bound applies. This uses polynomially many rational LP calls and no enumeration of vertices.

To bound the maintained lift, use a common denominator. If its current denominator is \(D_t\), an optimal basic lift has a denominator with the fixed bound just given, and the lift of \(b\) has denominator \(a\). The convex operations with \(1/4,3/4,h,1-h\) can therefore use a next denominator that is the product of \(D_t\), one new fixed-bound vertex denominator, and factors of polynomial bit length in \(a\). Thus the denominator's bit length increases additively by a polynomial amount per update. Coordinate numerators are no larger than that common denominator, since coordinates lie in \([0,1]\). After polynomially many updates all lift coordinates still have polynomial bit length.

The coefficients \(\widehat p\) have a fixed polynomial-size common denominator, for example the product of their finitely many denominators. Consequently their utility map, the coordinates \(x_i\), the reciprocals \(1/x_i\), and each objective coefficient have polynomial bit length. Every LP and exact comparison with \(2a\) has polynomial bit cost. This establishes total-bit polynomial time without recursively inserting the current objective length into an unspecified LP-output bound.

### 3.5 Recovering targets and the full fractional bound

Recover nested configurations from the final lift as in §3.2, evaluate their actual normalized values, and set

\[
\widehat V_i=\sum_Tx_{i,T}\widehat v_i(T),\qquad
V_i=W_i\widehat V_i\quad(i\in A),\qquad V_i=0\quad(i\notin A).
\tag{3.7}
\]

They have row sums one, item columns at most one, polynomial support and polynomial rational bit length. We have \(\widehat V_i\ge x_i\ge1/(4a)\), and \(\widehat V_i\le1\), so \(0<V_i\le W_i\).

For an arbitrary feasible fractional residual family \(z\), let \(u^z\in R\) be its actual normalized utility vector, whose inclusion was proved in §3.2. At termination,

\[
\sum_{i\in A,T}z_{i,T}\frac{v_i(T)}{V_i}
=\sum_i\frac{u_i^z}{\widehat V_i}
\le\sum_i\frac{u_i^z}{x_i}
\le M\le2a.
\tag{3.8}
\]

This proves B7 for all feasible fractional families, not merely integral allocations or the recovered family. Since \(a\le n\), A2 holds with \(c=2\). Agents outside \(A\) satisfy \(v_i(B)=0\) by their definition, as required by A.

## 4. Proof of B3: deterministic support-respecting welfare rounding

Take any finite rational feasible configuration family on \(q\) agents, with positive actual expectations \(U_i\). If \(q=0\), return no bundles. Otherwise fix an actual attaining original clause for each positive-probability configuration, and regard the agents' configuration draws as independent. For item \(j\), let its random bid from agent \(i\) be \(b_{ij}=p_{i,s,j}/U_i\) if the drawn configuration contains \(j\), and zero otherwise.

### 4.1 Expected proxy welfare

For a positive threshold \(t\), put \(p_i(t)=\Pr(b_{ij}\ge t)\), \(s(t)=\sum_i p_i(t)\). A positive bid requires membership of \(j\) in that agent's drawn configuration. Configuration feasibility therefore implies \(0\le s(t)\le1\). Across agents these events are independent. The elementary second-order union bound, or \(1-e^{-s}\ge s-s^2/2\), gives

\[
\Pr(\max_i b_{ij}\ge t)
=1-\prod_i(1-p_i(t))
\ge s(t)-s(t)^2/2\ge s(t)/2.
\tag{4.1}
\]

Integrate this finite step function over \(t>0\), or sum its successive finite bid-level intervals. Then

\[
\mathbb E\max_i b_{ij}\ge\tfrac12\sum_i\mathbb E b_{ij}.
\tag{4.2}
\]

For each drawn configuration its chosen clause attains its actual value. Hence

\[
\mathbb E\sum_j\max_i b_{ij}
\ge\tfrac12\sum_i\mathbb E\frac{v_i(T_i)}{U_i}
=q/2.
\tag{4.3}
\]

Correlations between different items within one configuration play no role: (4.1) uses independence across agents for a single item, and expectation is then added over items.

### 4.2 Exact rational conditional expectations via finite CDFs

Fix the agents one at a time. For the next agent enumerate all its positive-probability configurations and compute the conditional expectation of the proxy \(\sum_j\max_i b_{ij}\) for each choice. The parent expectation is the probability-weighted average of these child expectations, so taking a maximizer cannot decrease it.

Here is the exact computation, including ties and zero bids. For item \(j\), list all distinct possible nonnegative bid levels as \(0=t_0<t_1<\cdots<t_K\), dropping absent positive levels. Then, conditional on the already fixed agents and the proposed next choice,

\[
\mathbb E\max_i b_{ij}
=\sum_{\ell=1}^K(t_\ell-t_{\ell-1})
 \left[1-\prod_i\Pr(b_{ij}<t_\ell)\right].
\tag{4.4}
\]

For an already fixed agent its CDF value is zero or one. For an unfixed agent it is the sum of the explicitly listed configuration probabilities with the specified strict bid comparison. The use of \(<t_\ell\) in the product makes (4.4) valid at every equal-bid boundary. All terms are rational. There are polynomially many listed bid levels, probabilities, items, agents, and choices. Rational products have bit length bounded by the sum of the operand bit lengths, and only polynomially many arithmetic operations are used, so recomputing these quantities directly is total-bit polynomial.

After all configurations are fixed, give an item with a positive maximum bid to one maximizing claimant using a deterministic tie rule; leave zero-maximum items unallocated. Each claimant's actual bundle is a subset of its chosen original positive-support configuration. On that bundle, its chosen clause gives an additive lower bound to actual XOS value. Thus

\[
\sum_i\frac{v_i(A_i)}{U_i}
\ge\sum_j\max_i b_{ij}\ge q/2.
\tag{4.5}
\]

The output bundles are disjoint, actual, and support-respecting. This is B8, with its deterministic and finite-bit assertions. It uses no masks or labels. In the rest of the proof we deliberately use the weaker welfare parameter \(d=5/2\), for which \(q/2\ge q/d\).

## 5. Proof of B4: splitting, inherited mass, and fixed candidates

Let \(\nu_i=\max_{j\in B}v_i(j)\), using zero for the maximum over an empty set, and

\[
A''=\{i\in A:V_i\ge6\nu_i\}.
\tag{5.1}
\]

For \(i\in A\), positivity of an XOS value on \(B\) implies \(\nu_i>0\). In particular, for \(i\in A''\),

\[
\alpha_i:=V_i/3-\nu_i\ge V_i/6>0.
\tag{5.2}
\]

### 5.1 Constructing the split family

Fix such an agent and its recovered family with actual expectation \(V_i\). Discard the configurations of value less than \(V_i/3\). For a remaining configuration \(T\), let

\[
k=\left\lfloor3v_i(T)/V_i\right\rfloor\ge1,
\tag{5.3}
\]

and choose a clause attaining \(v_i(T)\). Each of its weights on \(T\) is at most \(\nu_i\). Its total weight is at least \(kV_i/3\).

In a fixed item order, greedily accumulate weights until reaching at least \(\alpha_i\); the accumulated weight is at most \(\alpha_i+\nu_i=V_i/3\). Extract this set and repeat \(k-1\) times. There is enough remaining weight at every such step: after \(r\le k-1\) extractions, at most \(rV_i/3\) has been removed from an initial total of at least \(kV_i/3\). Use the entire remaining subset as part \(k\). Its clause weight is at least \(V_i/3\ge\alpha_i\). When \(k=1\), this simply means retaining \(T\) as the last part. Thus all parts have actual value at least \(\alpha_i\), because the chosen clause lower-bounds actual value on every subset.

If a part's actual value exceeds \(V_i\), delete items one at a time while its value exceeds \(V_i\). Monotonicity and subadditivity give a loss of at most \(\nu_i\) per deletion. At the first crossing below or to \(V_i\), the value is greater than \(V_i-\nu_i\ge\alpha_i\). If no deletion was needed, its lower bound was already valid. Therefore every resulting part \(T'\) satisfies

\[
V_i/3-\nu_i\le v_i(T')\le V_i.
\tag{5.4}
\]

Every part is a subset of its original configuration, and parts from one original configuration are disjoint. Deleted items may be left unallocated.

This construction does not expand by a reciprocal target. Since the attaining clause has weights at most \(\nu_i\),

\[
k\le\frac{3v_i(T)}{V_i}
\le\frac{3|T|\nu_i}{V_i}\le |T|/2.
\tag{5.5}
\]

Thus the number of generated parts is polynomial in the original support description and item count. Each deletion requires only rational table evaluation and there are at most \(|T|\) deletions. Equal resulting subsets may be kept as different entries or combined.

### 5.2 The inherited mass is at least one

Give every generated part the probability of its original configuration. Let \(M_i\) be the total inherited mass. The discarded configurations contribute at most \(V_i/3\) to the original expectation, so the retained ones contribute at least \(2V_i/3\). For \(r\ge1\), \(\lfloor r\rfloor\ge r/2\). Consequently

\[
\begin{aligned}
M_i&=\sum_{T:v_i(T)\ge V_i/3}x_{i,T}
       \left\lfloor\frac{3v_i(T)}{V_i}\right\rfloor\\
&\ge\frac{3}{2V_i}
       \sum_{T:v_i(T)\ge V_i/3}x_{i,T}v_i(T)
\ge1.
\end{aligned}
\tag{5.6}
\]

For a particular original item, one configuration contributes its inherited probability to at most one part, because the parts were disjoint. Before row normalization the new item marginal for every agent is at most its original marginal. Divide that agent's inherited probabilities by \(M_i\ge1\). This gives row sum one and can only decrease those marginals. Hence the modified family \(x'\), jointly over the agents in \(A''\), is feasible. Its probabilities have polynomial bit length, since \(k\) and the number of parts are polynomial and \(M_i\) is a finite rational sum.

Writing \(V'_i=\sum_Tx'_{i,T}v_i(T)\), (5.2) and (5.4) give

\[
V_i/6\le V'_i\le V_i.
\tag{5.7}
\]

This proves B9 and the normalization feasibility that is needed before any welfare rounding is applied.

### 5.3 Deterministic iteration without labels

Fix

\[
d=5/2,\qquad\delta=\frac1{7d}=\frac2{35}.
\tag{5.8}
\]

Start with all \(a_0=|A''|\) agents. At each round apply §4 to the restriction of \(x'\) to the current agents, using their expectations \(U_i=V'_i\). This restriction is feasible. If there are \(q\) current agents and its returned bundles are \(S_i\), then

\[
0\le\frac{v_i(S_i)}{V'_i}\le6,
\qquad\sum_i\frac{v_i(S_i)}{V'_i}\ge q/d.
\tag{5.9}
\]

The upper bound uses the support containment from §4 and the support upper bound \(V_i\le6V'_i\). Declare satisfied those agents with \(v_i(S_i)/V'_i\ge\delta\), fix their actual \(S_i\), record the current round \(t_i\), and remove them.

If fewer than \(\delta q\) agents were satisfied, their contributions in (5.9) would be less than \(6\delta q\), and those of all the others less than \(\delta q\). The total would be less than \(7\delta q=q/d\), a contradiction. Thus at least \(\lceil\delta q\rceil\) leave each nonempty round. In particular the iteration terminates in at most \(L=a_0\) rounds. Candidates fixed in one round are pairwise disjoint, and every fixed candidate obeys

\[
\delta V_i/6\le\delta V'_i\le v_i(S_i)\le V_i.
\tag{5.10}
\]

No labels or future masks have been used in this entire procedure. In particular all \(S_i,t_i\), and their attaining clauses, are fixed deterministic data before considering random formal labels. Candidates from different rounds may overlap; the eventual use of one common label for each original item will handle those overlaps.

Order the \(a_0>0\) agents by their satisfaction rounds, using a fixed order inside each round. If agent \(k\) in that order leaves in round \(t\), the current population contains at least \(a_0-k+1\) agents, and is at most \(a_0(1-\delta)^{t-1}\). Therefore

\[
p_{t_i}:=\delta(1-\delta)^{t_i-1}
\ge\delta\frac{a_0-k+1}{a_0}.
\tag{5.11}
\]

Give each original residual item an independent formal label in \(\{0,1,\ldots,L\}\), with probabilities \(p_t\) for \(1\le t\le L\) and \(p_0=(1-\delta)^L\). These positive rational probabilities sum exactly to one by the finite geometric-series identity. Their binary lengths are polynomial in \(L\), since \(\delta=2/35\) is fixed. This is a finite analysis distribution, not a randomized step of the final algorithm. If \(A''=\varnothing\), no splitting, rounds, or masks are needed, and put all residual \(T_i=\varnothing\).

## 6. Proof of B5: the local grid, shifted inverse moment, and mask DP

Suppose \(a_0>0\). Then \(m_B=|B|\ge1\). For each already fixed \(S_i\), choose an original clause attaining its actual value and denote its original weights on \(S_i\) by \(w_{i,j}\). They satisfy

\[
\sum_{j\in S_i}w_{i,j}=v_i(S_i)\in[\delta V_i/6,V_i],
\qquad0\le w_{i,j}\le\nu_i.
\tag{6.1}
\]

### 6.1 Candidate-local relative flooring

Define

\[
Q=210m_B,\qquad
a_{i,j}=\frac1Q\left\lfloor\frac{Qw_{i,j}}{V_i}\right\rfloor,
\qquad\beta_i=\nu_i/V_i>0.
\tag{6.2}
\]

Each floor is an ordinary integer floor of a binary rational with polynomial bit length. It causes a loss of less than \(1/Q\) in that item's relative weight. Since \(\delta/12=1/210\),

\[
\begin{aligned}
\sum_{j\in S_i}a_{i,j}
&\ge\frac{v_i(S_i)}{V_i}-\frac{|S_i|}{Q}
\ge\frac\delta6-\frac1{210}=\frac\delta{12},\\
\sum_{j\in S_i}a_{i,j}&\le1,
\qquad0\le a_{i,j}\le\beta_i.
\end{aligned}
\tag{6.3}
\]

The weak lower bound is valid even though the actual floor loss is strict. The integer weights \(h_{i,j}=Qa_{i,j}\) have row total at most \(Q\). This is a polynomial-size internal state space because \(Q=210m_B\), independent of the values of original denominators or targets. Neither the original XOS table nor any physical item, state, incidence, or processing time has been changed.

For any label assignment define

\[
A_i(r)=\sum_{j\in S_i}a_{i,j}\mathbf1[r_j=t_i],
\qquad \Phi(r)=\sum_{i\in A''}-\ln(\beta_i+A_i(r)).
\tag{6.4}
\]

The positive shift makes all these logarithms finite, including assignments that retain no positive weight.

### 6.2 Proof of the weighted Bernoulli shifted inverse moment

Let \(\beta>0\), \(0\le a_j\le\beta\), and let \(X_j\) be independent Bernoulli variables of probabilities \(p_j\). Assume \(M=\sum_j a_jp_j>0\). Put \(d_j=a_j/\beta\in[0,1]\), \(Y=\sum_jd_jX_j\), and \(\mu=M/\beta>0\).

For \(0<t<1\), the function \(d\mapsto t^d\) is convex. Its chord between zero and one gives

\[
t^{d_j}\le1-d_j+d_jt=1-d_j(1-t).
\tag{6.5}
\]

By the finite independence of the \(X_j\),

\[
\mathbb E[t^Y]
=\prod_j(1-p_j+p_jt^{d_j})
\le\prod_j[1-p_jd_j(1-t)]
\le e^{-\mu(1-t)}.
\tag{6.6}
\]

Since \(1/(1+Y)=\int_0^1t^Y\,dt\), finite expectation and integration may be interchanged. Therefore

\[
\mathbb E\frac1{\beta+\sum_ja_jX_j}
\le\frac1\beta\int_0^1e^{-\mu(1-t)}dt
=\frac{1-e^{-\mu}}{M}<\frac1M.
\tag{6.7}
\]

Concavity of the logarithm on the positive inverse variable now yields

\[
\mathbb E\ln\frac1{\beta+\sum_ja_jX_j}
\le\ln\mathbb E\frac1{\beta+\sum_ja_jX_j}
\le\ln\frac1M.
\tag{6.8}
\]

This is B15. The convex-chord step (6.5) is the precise reason for its inequality direction. The argument is additive and requires independent Bernoulli inclusion for the items within the row. It asserts no correlated-mask extension or generic-subadditive concentration theorem. In our application the common labels correlate different agents' retained sets, but for any one fixed candidate its different original items have independent labels. This is exactly the independence needed for (6.6).

### 6.3 A complete deterministic mask procedure with total error one

Precompute, for every \(i\in A''\) and \(k=0,\ldots,Q\), a rational \(\widehat f_i(k)\) approximating

\[
f_i(k)=-\ln(\beta_i+k/Q)
\]

with absolute error at most

\[
\alpha=\frac1{2a_0m_B}.
\tag{6.9}
\]

Section 1.1 supplies such approximations. Every argument is a positive rational of polynomial bit length. A small \(\beta_i\) affects only the binary description and precision; it does not generate a number of DP states proportional to \(1/\beta_i\).

Process residual items in a fixed order and fix one positive-probability label for each. At a current prefix, row \(i\) has an already fixed integer contribution \(b_i\). For undecided items in \(S_i\), the retained integer weight has generating polynomial

\[
\prod_{j\ \mathrm{undecided},\ j\in S_i}
 [(1-p_{t_i})+p_{t_i}z^{h_{i,j}}].
\tag{6.10}
\]

Its degree is at most \(Q\). A convolution DP with \(Q+1\) entries computes its exact rational coefficient distribution. More generally, for one Bernoulli probability \(P_j/D_j\), if a DP uses integer numerators \(N_k\) over a common denominator \(D\), appending that item gives

\[
N'_k=(D_j-P_j)N_k+P_jN_{k-h_{i,j}},
\qquad D'=DD_j,
\tag{6.11}
\]

with out-of-range entries zero. A zero weight simply combines the two terms at the same index. The numerators are nonnegative and sum to the common denominator, so their bit lengths are at most the sum of the actual probability denominator lengths. Probabilities zero or one, if present in the general tool, cause no difficulty.

For each possible positive-probability label \(t\) of the next item \(j\), first add \(h_{i,j}\) to row \(i\)'s offset precisely when \(j\in S_i\) and \(t=t_i\). Compute the DP over the remaining undecided items and sum its expectations of \(\widehat f_i\) at the shifted indices. All indices remain between zero and \(Q\). This gives a rational score \(\widehat H_t\) for the conditional potential. Its error from the true conditional potential \(H_t\) is at most \(a_0\alpha=1/(2m_B)\), because each row's probability distribution sums to one.

Choose a label \(t_*\) minimizing these rational scores, with deterministic ties. If \(t_{\min}\) minimizes the true child potentials, then

\[
H_{t_*}\le\widehat H_{t_*}+a_0\alpha
\le\widehat H_{t_{\min}}+a_0\alpha
\le H_{t_{\min}}+2a_0\alpha.
\tag{6.12}
\]

The true parent conditional expectation is the probability-weighted average of the true child expectations. Its value is therefore at least \(H_{t_{\min}}\). Conditioning previous independent item labels does not change the remaining original label probabilities. Thus the chosen step raises the true conditional potential by at most \(1/m_B\). After \(m_B\) choices no labels remain random and

\[
\Phi(r)\le\mathbb E\Phi+1.
\tag{6.13}
\]

This algorithm never divides by a small prefix-event probability and never compares transcendental quantities exactly. Even recomputing every candidate DP from scratch uses only polynomially many operations in \(a_0,m_B,L,Q\); for example the number of convolution operations is bounded by a constant times \(m_B(L+1)a_0m_BQ\). Every DP probability and every rational log approximation has polynomial bit length by (6.11) and §1.1. Since \(L\le n\) and \(Q=210m_B\), this is total-bit polynomial in the original explicit input and its polynomial-bit intermediate representations. There is no expansion by an original coefficient's reciprocal, a target's reciprocal, or a probability's reciprocal.

### 6.4 Recovering actual disjoint residual bundles

Return \(T_i=\{j\in S_i:r_j=t_i\}\) for \(i\in A''\) and \(T_i=\varnothing\) otherwise. If one original item belonged to both \(T_i\) and \(T_h\), its one chosen label would satisfy \(t_i=t_h\), so these candidates would have been fixed in the same round. Their disjointness in that round rules out the overlap. Hence all returned residual bundles are globally disjoint, including zero-weight items that happen to be retained.

The original attaining clause of \(S_i\) lower-bounds the actual value of its subset \(T_i\). Since \(w_{i,j}\ge V_ia_{i,j}\),

\[
v_i(T_i)\ge\sum_{j\in T_i}w_{i,j}\ge V_iA_i(r).
\tag{6.14}
\]

This proves B17 with the original unfloored valuation. Also \(v_i(T_i)\le v_i(S_i)\le V_i\).

### 6.5 The complete B18 numerical estimate

For agent \(k\) in the ordering of §5.3, its mean retained auxiliary weight is

\[
M_i=p_{t_i}\sum_{j\in S_i}a_{i,j}
\ge\frac{\delta^2(a_0-k+1)}{12a_0}>0.
\tag{6.15}
\]

Apply (6.8) row by row and add expectations; no cross-row independence is needed. Writing \(a=a_0>0\),

\[
\begin{aligned}
\mathbb E\Phi
&\le\sum_{k=1}^a\ln\frac{12a}{\delta^2(a-k+1)}\\
&=a\ln\frac{12}{\delta^2}+a\ln a-\ln(a!)
\le a\left(\ln\frac{12}{\delta^2}+1\right).
\end{aligned}
\tag{6.16}
\]

The last inequality follows, for example, by integrating the increasing function \(\ln x\) to obtain \(\ln(a!)\ge a\ln a-a\). Combining (6.13) and (6.16),

\[
\left(\prod_{i\in A''}\frac1{\beta_i+A_i(r)}\right)^{1/a}
\le\frac{12}{\delta^2}e^{1+1/a}
\le\frac{12e^2}{\delta^2}
<\frac{200}{\delta^2}.
\tag{6.17}
\]

The strict last inequality follows already from \(e<3\), since \(12e^2<108<200\). By (6.14),

\[
\left(\prod_{i\in A''}\frac{V_i}{\nu_i+v_i(T_i)}\right)^{1/a}
\le\left(\prod_{i\in A''}\frac1{\beta_i+A_i(r)}\right)^{1/a}
<\frac{200}{\delta^2}
=9800d^2<10000d^2.
\tag{6.18}
\]

This is B18, including the local-floor loss and the complete additive potential error one. Its strict margin is a numerical inequality, not a random-success assertion or an unbudgeted approximation loss.

## 7. Proof of B6: rematching for every comparison bijection

### 7.1 The rematching lemma, including cycles and zero edges

Let \(a_{ih}=v_i(h)\) be singleton values of monotone valuations on \(U\). Let \(\tau:[n]\to U\) be a true maximum-product singleton matching whose product is positive, let \(H=\tau([n])\), let \(B=U\setminus H\), and let \(\nu_i=\max_{j\in B}v_i(j)\) with the zero convention. For arbitrary nonnegative numbers \(W_i\) and every bijection \(\pi:[n]\to H\), there is a bijection \(\rho:[n]\to H\) satisfying

\[
\prod_i\max\{W_i,a_{i\rho(i)}\}
\ge\prod_i\max\{W_i,a_{i\pi(i)},\nu_i\}.
\tag{7.1}
\]

If the right product is zero, choosing \(\rho=\tau\) makes every factor on the left positive and proves the claim. Assume henceforth that the right product is positive. Define

\[
E=\{i:W_i<\max(a_{i\pi(i)},\nu_i)\},
\quad N=\{i\in E:\nu_i>a_{i\pi(i)}\}.
\tag{7.2}
\]

For \(i\notin E\), the right factor is \(W_i>0\). For \(i\in E\setminus N\), it is \(a_{i\pi(i)}>0\). For \(i\in N\), it is \(\nu_i>0\).

On the vertex set \(E\), draw the directed edge \(i\to\tau^{-1}(\pi(i))\) whenever its endpoint also belongs to \(E\). The full map \(\tau^{-1}\circ\pi\) is a permutation, so in this restricted graph every indegree and outdegree is at most one. Let \(E_\tau\) consist of \(N\) and all vertices whose forward path reaches \(N\); put \(E_\pi=E\setminus E_\tau\). Assign \(\rho(i)=\tau(i)\) on \(E_\tau\), and \(\rho(i)=\pi(i)\) on \(E_\pi\).

These partial assignments do not conflict. A conflict could only be \(\pi(i)=\tau(k)\) with \(i\in E_\pi\), \(k\in E_\tau\). But then \(i\to k\) is an edge and \(i\) reaches \(N\), contradicting \(i\in E_\pi\). They therefore extend arbitrarily to a bijection on the unassigned agents and unused items in \(H\).

To prove the product bound, consider the graph on \(E_\tau\) and delete every outgoing edge from every \(N\)-vertex. Every vertex outside \(N\) in this graph has exactly one outgoing edge, following its forward route to \(N\). Every \(N\)-vertex has outdegree zero; indegrees remain at most one. There is no directed cycle, because a cycle without \(N\) cannot reach \(N\). Thus its components are disjoint directed paths, each ending at exactly one \(N\)-vertex. This construction covers cycles of the original permutation, including cycles containing several \(N\)-vertices: deletion cuts them into these paths. A self-loop at an \(N\)-vertex becomes a one-vertex path.

Take a path \(P=(i_1,\ldots,i_r=s)\), ending at \(s\in N\). For each nonterminal vertex \(\pi(i_\ell)=\tau(i_{\ell+1})\). Choose an item \(j_s\in B\) attaining \(\nu_s>0\). Modify \(\tau\) on this single path by assigning \(\pi(i_\ell)\) to each nonterminal \(i_\ell\), and \(j_s\) to \(s\); keep \(\tau\) elsewhere. This is a valid singleton matching on all original items: it uses the distinct path items \(\tau(i_2),\ldots,\tau(i_r)\), one item outside \(H\), and untouched distinct \(\tau\)-items elsewhere. All its factors are positive. The optimality of \(\tau\), with its positive unchanged factors cancelled, gives

\[
\prod_{i\in P}a_{i\tau(i)}
\ge\nu_s\prod_{i\in P\setminus\{s\}}a_{i\pi(i)}.
\tag{7.3}
\]

Different paths might have the same maximizing residual item \(j_s\). That is harmless: (7.3) is proved with a separate valid alternative matching for each path. We multiply already established numerical inequalities, rather than allocating all those residual maximizers simultaneously.

Multiplying (7.3) over the disjoint paths yields

\[
\prod_{i\in E_\tau}a_{i\tau(i)}
\ge\prod_{i\in N}\nu_i
   \prod_{i\in E_\tau\setminus N}a_{i\pi(i)}.
\tag{7.4}
\]

For \(i\notin E\) lower-bound the left factor in (7.1) by \(W_i\), for \(i\in E_\pi\) by \(a_{i\pi(i)}\), and for \(i\in E_\tau\) by \(a_{i\tau(i)}\). Equation (7.4) then gives exactly all the right factors classified after (7.2), proving (7.1). It is not necessary that every edge used by the completed \(\rho\) have a positive singleton: outside \(E\), \(W_i>0\) protects the factor. The argument nevertheless includes zero comparison singletons, \(W_i=0\), and empty \(B\).

### 7.2 Applying rematching to actual residual bundles

Write \(b_i=v_i(T_i)\) for the disjoint bundles returned by §6, including the empty-bundle conventions. On \(H\), compute a true maximum-product matching \(\sigma\) for factors

\[
v_i(T_i\cup\{h\}),
\tag{7.5}
\]

using §1.2. These are finite rationals obtained directly from the original clause table. A positive perfect matching exists because \(\tau\) gives factors at least \(v_i(\tau(i))>0\). Thus the algorithm's final product is positive.

For every comparison bijection \(\pi:[n]\to H\), apply (7.1) with \(W_i=b_i\). Monotonicity, then product optimality of \(\sigma\), imply

\[
\begin{aligned}
\prod_i v_i(T_i\cup\{\sigma(i)\})
&\ge\prod_i v_i(T_i\cup\{\rho(i)\})\\
&\ge\prod_i\max\{b_i,a_{i\rho(i)}\}
\ge\prod_i\max\{b_i,a_{i\pi(i)},\nu_i\}.
\end{aligned}
\tag{7.6}
\]

These final bundles are disjoint subsets of the original \(U\): the \(T_i\) lie in \(B\), and \(\sigma\) uses every item of \(H\) once.

### 7.3 Comparing to all targets and accounting for every constant

Fix a comparison \(\pi\). If \(\prod_i(V_i+a_{i\pi(i)})=0\), B19 is vacuous and the output is still positive. Otherwise every comparison factor is positive. Put

\[
D_i=b_i+\nu_i+a_{i\pi(i)}.
\tag{7.7}
\]

All these denominators are positive. For \(i\in A''\), \(b_i\le V_i\), \(\nu_i\le V_i/6\), so \(0<b_i+\nu_i\le2V_i\). For a nonnegative \(a\) and \(0<s\le2V_i\),

\[
\frac{V_i+a}{s+a}\le\frac{2V_i}{s}.
\]

It follows that

\[
\frac{V_i+a_{i\pi(i)}}{D_i}
\le\frac{2V_i}{b_i+\nu_i}\quad(i\in A'').
\tag{7.8}
\]

For \(i\in A\setminus A''\), we have \(b_i=0\), \(0<V_i<6\nu_i\), and the corresponding ratio is at most six. For \(i\notin A\), \(V_i=b_i=\nu_i=0\), and positivity of the comparison requires \(a_{i\pi(i)}>0\), making the ratio one. Consequently (6.18), when \(A''\ne\varnothing\), gives

\[
\prod_i\frac{V_i+a_{i\pi(i)}}{D_i}
\le(20000d^2)^{|A''|}\,6^{n-|A''|}
\le(20000d^2)^n.
\tag{7.9}
\]

When \(A''\) is empty, the same inequality follows directly from the outside ratios; no empty-set geometric mean is used.

Also \(\max\{b_i,a_{i\pi(i)},\nu_i\}\ge D_i/3\). Thus (7.6) and (7.9) prove

\[
\left(\prod_i v_i(T_i\cup\{\sigma(i)\})\right)^{1/n}
\ge\frac1{60000d^2}
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}.
\tag{7.10}
\]

This is B19 for **every** comparison bijection, including arbitrary permutation cycles and zero comparison singletons. The factor three from sum versus maximum is explicitly retained.

Now take any finite positive fractional benchmark \(y\) on this same original XOS object satisfying A1. The targets and residual configurations constructed in §3 satisfy A with \(c=2\), by (3.8). Section 2 supplies a comparison \(\pi\) with target product geometric mean at least \(\mathcal B_v(y)/3\). The algorithm need not know this matching or this benchmark. Substitution in (7.10) gives

\[
\mathsf{NSW}_v
\ge\frac{\mathcal B_v(y)}{60000\cdot3\cdot(5/2)^2}
=\frac{\mathcal B_v(y)}{1125000}
\ge\frac{\mathcal B_v(y)}{2250000}.
\tag{7.11}
\]

The same output satisfies this inequality simultaneously for every such benchmark, since none was an algorithm input. The factor-two weakening in the last inequality is an explicit reserve; the earlier proof already paid the full DP error and logarithm precision cost.

### 7.4 Total running time and exact domain

All preprocessing consists of explicit finite table evaluation, matching, and rational arithmetic. The fixed-lift solver uses polynomially many rational LP calls and updates, with polynomial-bit coordinates. Threshold recovery has polynomial support. Splitting has at most \(|T|/2\) parts per retained configuration, and the iterative welfare procedure runs for at most \(n\) rounds on polynomial-support families. Each CDF evaluation is polynomial. Local floors have polynomial bit cost, and the DP has \(Q+1=210m_B+1\) states per row and \(L+1\le n+1\) candidate labels per item. The final factors are polynomial-bit rational table values, and exact product matching has polynomial bit cost by §1.2.

Thus the complete deterministic backend is total-bit polynomial in the explicit agent, item, clause and rational input description. Zero coefficients, duplicate indexed clauses, unused items, zero-total clauses, and empty residual branches all have the prescribed behavior. The proof used no globally normalized original clause table, common denominator grid by value, global positive utility floor, optimal allocation, benchmark as input, sampling success event, weighted objective, or oracle-only representation. This completes B.

## 8. Proof of C: normalized unit-FSLP and low-quality group counts

Here the original table has \(n\ge1\) groups, \(m\ge1\) original resources, nonempty finite indexed menus, and every original clause has total exactly one. Thus

\[
0\le v_g(T)\le1\quad\hbox{for every original bundle }T.
\tag{8.1}
\]

This original normalization is used for C's counting consequences. It was not assumed in B.

### 8.1 From a feasible unit-FSLP to a benchmark of one

For original state \(s\), put \(P_{g,s}=\{u:p_{g,s,u}>0\}\). The state value on its positive support is exactly one; (8.1) then implies \(v_g(P_{g,s})=1\). These supports are nonempty because their coefficient totals are one.

The explicit unit-FSLP used here is exactly

\[
\lambda_{g,s}\ge0,\qquad\sum_s\lambda_{g,s}=1,\qquad
\sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1\quad(u\in U).
\tag{8.F}
\]

Take a feasible \(\lambda\) of the explicit FSLP. For group \(g\), use each support \(P_{g,s}\) as a configuration with mass \(\lambda_{g,s}\), merging equal subsets if desired. Its row mass is one. The expected item usage is exactly

\[
\sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1.
\tag{8.2}
\]

In particular the coefficients in this capacity constraint are the indicators of *positive* support, not the private coefficients \(p_{g,s,u}\) or zero-incidence indicators. Every positive-mass configuration has actual value one, so this is a finite positive fractional benchmark with

\[
\mathcal B_v(y)=1.
\tag{8.3}
\]

All finite positive log-CONFIG terms have \(\ln v_g(T)\le0\) by (8.1), while this witness has objective zero. Hence the unweighted log-CONFIG optimum with item inequalities is zero.

The item-equality version also has optimum zero. Here is an explicit monotone filling argument for existence of an equality witness. Suppose a column \(u\) currently has mass \(c_u\le1\). Across the \(n\) rows there is total mass \(n-c_u\) on configurations not containing \(u\), which is at least the deficit \(1-c_u\). Select that much mass from such configurations, splitting an entry if necessary, and add \(u\) to precisely those configurations. Row sums are unchanged; only column \(u\) changes. Each changed configuration still has value one by monotonicity and (8.1). Process each item in turn. An entry may be replaced in full, and at most one partially selected entry is needed per item, so finiteness is preserved. Already processed columns are unchanged by later additions of other items. The resulting witness has every item column equal to one and objective zero. This reasoning does not supply a solver for a general exponential log-CONFIG LP.

### 8.2 Original queries and preservation of original states

Value and attaining-clause queries are evaluated by rational summation of the original clauses. Demand is also explicit: for rational prices \(r_u\),

\[
\max_T\left[v_g(T)-\sum_{u\in T}r_u\right]
=\max_s\sum_u\max\{p_{g,s,u}-r_u,0\}.
\tag{8.4}
\]

For the maximizing state choose its positive-surplus resources; ties at zero may be handled deterministically. Formula (8.4) follows by interchanging the two finite maxima over \(T\) and \(s\). All computations have polynomial bit cost.

The residual normalization of §3 and relative floors of §6 are internal numerical operations. The final bundles remain subsets of original resources. For every final bundle, choose a state maximizing its value under the original unfloored table. This recovers a genuine original indexed state with the claimed actual quality. There is no global floor of the menu table, and no alteration of a state coefficient, physical processing time, or item identity.

### 8.3 Deterministic NSW and explicit thresholds

Find a rational feasible FSLP certificate by deterministic rational LP if it was not supplied. In the feasible case its benchmark (8.3) precludes B's no-positive-singleton-matching branch. Applying B therefore gives an actual allocation with NSW at least \(1/1125000\), and in particular

\[
\mathsf{NSW}_v\ge\frac1{3000000}
>\frac1{2^{24}}=\rho^{-1},
\qquad \rho=2^{24}.
\tag{8.5}
\]

This proves C3 with slack even if one retains B's explicit factor-two reserve. No optimal actual allocation is an input. If the FSLP is infeasible, C makes no claim of a unit allocation or of general UM infeasibility.

Fix a rational \(0<\eta<1\), and put

\[
K=\lceil1/\eta\rceil,\qquad
q_\eta=\rho^{-K},\qquad
c_\eta=q_\eta/2=2^{-24K-1}.
\tag{8.6}
\]

Let \(r_g\in(0,1]\) be the returned original quality. If \(k\) groups have \(r_g<q_\eta\) and \(k\ge\eta n\), then

\[
\prod_g r_g<q_\eta^k=\rho^{-Kk}\le\rho^{-n},
\tag{8.7}
\]

because \(K\eta\ge1\). The strict inequality holds since \(k\ge\eta n>0\) and each of those \(k\) factors is strictly below \(q_\eta\); all remaining factors are at most one. This contradicts (8.5). Thus

\[
\#\{g:r_g<q_\eta\}<\eta n.
\tag{8.8}
\]

Since \(r_g\le c_\eta=q_\eta/2\) strictly implies \(r_g<q_\eta\), we also have

\[
\#\{g:r_g\le c_\eta\}<\eta n.
\tag{8.9}
\]

These strict count bounds require no divisibility assumption on \(\eta n\). For fixed \(\eta\), the thresholds are explicit rational constants. For variable \(\eta\), writing \(q_\eta,c_\eta\) already uses \(O(K)\) bits; arithmetic and the corresponding output comparisons are polynomial in \(K\) and the original input length. No polynomial bound in \(\log(1/\eta)\) alone is asserted.

### 8.4 The robust-small-quality exclusion

If every actual allocation of these same \(n\) groups had at least \(\gamma n\) qualities at most \(\delta\), where \(\gamma>\eta\) and \(0\le\delta\le c_\eta\), then the output of (8.9) would have at least \(\gamma n>\eta n\) qualities at most \(c_\eta\). This is a contradiction. This proves C6.

The conclusion is about the original menu-group population. It is not a group count measured in machines, incidence jobs, state indices, or a larger collection of auxiliary agents. Equations (8.8)–(8.9) allow a small number of arbitrarily low positive qualities; they give no constant minimum quality for every group.

## 9. Proof of D: shared singleton REPAIR and the LP promise decider

The augmentation keeps the same \(n\) groups and every original resource, state, and coefficient. It adds shared resources \(d_1,\ldots,d_D\), and to each group adds exactly one total-one singleton alternative on each such resource. On a bundle \(T\subseteq U\cup\{d_1,\ldots,d_D\}\), its XOS value is exactly

\[
v_g^+(T)=
\max\left\{v_g(T\cap U),
             \max_{1\le\ell\le D}\mathbf1[d_\ell\in T]\right\},
\tag{9.1}
\]

where the maximum over an empty repair list is zero. In particular original unit normalization is preserved.

### 9.1 Completeness and the loss of at most \(D\) bad groups

Suppose an original actual allocation gives quality one to at least \(n-D\) groups. Keep those quality-one groups' original bundles and states. At most \(D\) groups remain; if \(D\ge n\), at most \(n\le D\) remain even when none were kept. Give each remaining group a different repair resource and its singleton alternative. This is a disjoint actual unit allocation of all the original \(n\) groups in \(Q^+\). For \(D=0\), the original allocation was already unit for all groups. This proves D1.

For D2, take any disjoint augmented allocation and remove all its repair resources. The restricted bundles in \(U\) are a valid original disjoint allocation. By the original robust premise, at least \(\gamma n\) groups have restricted quality at most \(\delta\). At most \(D\) groups received any repair resource, since those \(D\) resources were globally disjointly allocated. For every group receiving none, (9.1) says its augmented quality equals its restricted original quality. Thus at least \(\gamma n-D\) groups in the augmented allocation still have quality at most \(\delta\). The count remains a count of original groups, even for the repaired groups. A negative numerical lower bound is simply vacuous.

### 9.2 Separation by feasibility of the augmented FSLP

Fix the constants in D3: \(0\le a<\gamma\le1\), a rational \(0<\eta<\gamma-a\), and \(0\le\delta\le c_\eta\). Suppose \(D\le an\).

The promise is that \(Q\) is either YES, meaning an original actual allocation gives quality one to at least \(n-D\) groups, or NO, meaning every original actual allocation has at least \(\gamma n\) groups of quality at most \(\delta\). The decision rule returns YES exactly when the augmented unit-FSLP is feasible.

In the YES case, D1 gives a unit actual allocation in \(Q^+\). For every group choose a state attaining its value one. Since that state's nonnegative coefficient total is exactly one, the group's bundle contains all its positive support: omitting any one positive coefficient would make its value strictly below one. These supports are disjoint. Setting that state's \(\lambda\) to one in every row gives a feasible augmented FSLP witness.

In the NO case, D2 forces every augmented actual allocation to have at least

\[
\gamma n-D\ge(\gamma-a)n>\eta n
\tag{9.2}
\]

groups of quality at most \(\delta\le c_\eta\). If the augmented FSLP were feasible, C would give an allocation with fewer than \(\eta n\) groups of quality at most \(c_\eta\), contradicting (9.2). The augmented FSLP is therefore infeasible.

Its explicit incidence LP has rational data (indeed its constraint coefficients are zero or one), so deterministic rational LP feasibility separates the two promised cases in total-bit polynomial time. It need not run the NSW finder or decide an unknown integral optimum numerically. Under \(D\le an\), the \(nD\) added states have polynomial explicit size; under dense representation all their zero entries are polynomial as well. Outside the promise, either LP outcome is permitted.

The proof used the positive fixed gap \(\gamma-a\) to choose a fixed positive \(\eta\) and hence a fixed constant \(c_\eta\). It does not establish such a threshold when that slack vanishes. It also used the same group count \(n\) in every step. The case \(D=0\) gives the stated original-instance promise decider. If an NP-complete language has a polynomial Karp reduction into this explicit promise gap with these fixed constants, composing the reduction and this deterministic LP test puts that language in P and yields P=NP. This is a conditional consequence, not a construction or assertion of such a reduction. It relies on the strong fractional unit-FSLP implication C, rather than on a published approximation guarantee relative only to actual integral OPT.

## 10. Proof of E: a complete ordinary flat-UM schedule

We now describe the ordinary matrix and all jobs explicitly. For each original indexed state \((g,s)\), there is its own private root machine \(R_{g,s}\). There is one resource machine \(M_u\) for each listed original resource. For each group \(g\), its one original selector job has processing time one at each of that group's roots, and is ineligible elsewhere. Every listed state-resource incidence has its own job \(e_{g,s,u}\), of processing time \(p_{g,s,u}\) at \(R_{g,s}\), time one at \(M_u\), and infinity at every other machine. Include every positive coefficient incidence and retain every explicitly listed zero incidence. Distinct indexed states always give distinct roots and distinct incidence-job identities, even if their clauses coincide.

Take the actual disjoint allocation from C and denote its final original bundles by \(Z_g\), to distinguish them from B's residual bundles. Choose an original state \(s_g\) attaining \(v_g(Z_g)\), and let

\[
r_g=\sum_{u\in Z_g}p_{g,s_g,u}=v_g(Z_g).
\tag{10.1}
\]

Schedule every original job as follows:

1. Execute the selector of \(g\) at its selected root \(R_{g,s_g}\).
2. For that selected state, execute \(e_{g,s_g,u}\) on \(M_u\) precisely when \(u\in Z_g\) and \(p_{g,s_g,u}>0\). Execute all its other incidence jobs at \(R_{g,s_g}\).
3. For every unselected indexed state, execute all its incidence jobs at that state's own original root.

This specifies exactly one eligible endpoint for each selector and incidence identity. A zero incidence stays at its original root with processing time zero; it is not discarded. Jobs of unselected states are retained in full. No job is executed on a mask-DP state, algorithmic slot, copied resource, or altered processing time.

The selected state had total original private weight one. The coefficient sum moved off its root is exactly \(r_g\). Its selected root load is therefore

\[
1+(1-r_g)=2-r_g.
\tag{10.2}
\]

An unselected root has no selector and all its original private coefficient jobs, of total one. A resource receives at most one incidence job: only the selected state of a group receiving that resource can send a job there, and the bundles \(Z_g\) are globally disjoint. Its load is thus at most one. Every machine is covered by these cases, so the whole original matrix has a complete actual schedule of makespan at most two.

For the output guaranteed by C, a selected root exceeds \(2-q_\eta\) exactly when \(r_g<q_\eta\). By (8.8), there are fewer than \(\eta n\) such selected group roots. This does not bound every root by \(2-c_\eta\); the conclusion remains an exceptional-group count, not a constant max-min guarantee.

If a disjoint actual unit allocation exists, choose attaining states for that allocation and run the same complete construction. All its selected roots have load one, all unselected roots have load one, and all resources have load at most one. The makespan is at most one. Since \(n\ge1\), at least one unit selector must be executed at one of its eligible unit-time endpoints in every complete schedule; hence ordinary makespan OPT is at least one. In this unit case ordinary OPT is exactly one.

This applies unchanged to \(Q^+\). The shared repair resource machines are actual new original machines of that augmented object, each repair alternative has its own actual root, and each of its singleton incidences is an actual job. D1 supplies the unit allocation in the augmented YES case, so the resulting makespan-one schedule includes every old job and every new repair-state job.

If \(S\) is the original indexed-state count and \(I\) its explicitly listed incidence count, the original matrix has \(S+m\) machines and \(n+I\) jobs. The selector endpoints total \(S\), with exactly one selector identity per group. The repair augmentation adds \(nD\) roots, \(D\) resource machines, \(nD\) positive singleton incidence jobs, and \(nD\) selector endpoints. It retains the original \(n\) selector identities and all old jobs. Any additional explicitly listed zero incidences are counted in \(I\) and retained as just explained. Writing a dense matrix with infinity on the other endpoints or a complete finite-endpoint job schedule takes polynomial size in the explicit augmented input. Thus E concerns every original job and every original machine, with exactly its stated at-most-two and selected-root-count guarantees.

## 11. Proof of F's quantitative consequence and its quantifiers

Assume a normalized object has feasible unit-FSLP. Let \(0<\delta<1\), and suppose every actual allocation has at least \(\gamma n\) groups of quality at most \(\delta\). Apply that premise to the output of C, whose qualities lie in \((0,1]\). If \(k\ge\gamma n\) of them are at most \(\delta\), then

\[
\ln\mathsf{NSW}_v
=\frac1n\sum_g\ln r_g
\le\frac{k}{n}\ln\delta
\le\gamma\ln\delta.
\tag{11.1}
\]

Combining with \(\mathsf{NSW}_v\ge\rho^{-1}\), or with the stronger strict bound (8.5), gives the claimed necessary inequality

\[
\gamma\ln(1/\delta)\le\ln\rho,\qquad \rho=2^{24}.
\tag{11.2}
\]

For \(\delta=0\) and \(\gamma>0\), the premise is already contradicted by C's positive output; (11.2) is deliberately stated only for \(0<\delta<1\).

The implication has the following exact quantifiers. For every fixed rational \(\eta\in(0,1)\), C supplies the fixed explicit constants \(q_\eta,c_\eta\). It rules out the robust condition when \(\gamma>\eta\) and \(0\le\delta\le c_\eta\). It does not rule out every pair of positive constants \(\gamma,\delta\). More generally (11.2) gives a constant restriction for each fixed target \(\delta\); it has no dependence on the source input size. A fraction \(\gamma\) may depend on that chosen target and stay positive for every fixed target. Nothing here requires choosing a sequence \(\delta=\delta(n)\to0\), and without such an extra assumption nothing forces \(\gamma\to0\) as \(n\) grows. Nor is there an inference that auxiliary size must grow with source input size instead of with a fixed target parameter.

All population counts in this proof use exactly the \(n\) original menu groups. The distinct counts of roots, resources, indexed states, jobs, incidences, or auxiliary variables do not replace this \(n\). The complete UM schedule established in §10 does not assert an all-machine \(2-\epsilon\) bound, a universal near-two barrier, or an approximation theorem for arbitrary unrelated-machine instances.

## 12. Executable specification, dependencies, and version boundary

For clarity, the deterministic B finder proved here has the following finite sequence of operations.

1. Evaluate the original positive singleton graph. If no covering matching exists, return all-empty bundles as in §3.1. Otherwise find the true maximum-product positive singleton matching on all of \(U\), and form \(H,B,A\).
2. If \(A\ne\varnothing\), exactly normalize its residual rows, run the rational fixed-lift iteration, recover threshold configurations, and evaluate original-unit targets \(V_i\). If \(A=\varnothing\), set all \(V_i=0\).
3. On \(A''\), split and normalize the configurations. Repeatedly apply the support-respecting exact-CDF welfare procedure to the remaining agents. Fix every satisfied agent's candidate and round, independently of all labels.
4. If \(A''\ne\varnothing\), floor only the fixed candidates' relative additive-support weights with \(Q=210|B|\). Use the rational finite-grid DP and certified logarithm table to choose every original item's one label with total potential error at most one. Return the actual masked subsets of the original candidates. If \(A''=\varnothing\), use empty residual bundles.
5. Find the true maximum-product matching on \(H\) for the original values of each residual bundle plus each candidate singleton, and return the resulting disjoint actual bundles.

The proof of its benchmark comparison uses §2 and the full fractional residual inequality (3.8). The proof of the deterministic masks uses only the additive shifted inverse moment and the explicitly budgeted DP, not the source paper's generic-subadditive tail calculation. The proof of final rematching uses global singleton-product optimality and handles cycles, separate residual maximizers, and zero branches explicitly. Thus the constants in (7.11) are derived here rather than imported from a source's actual-OPT theorem or from a verdict in the already read independent record.

C then applies this finder to the original normalized table, with a unit benchmark supplied by feasible FSLP; the returned states are always evaluated on the original table. D's promise decision itself requires only the explicit augmented FSLP feasibility test, using C for its soundness proof. E converts C's actual output to a schedule with all original job identities, without substituting numerical-normalization or local-grid values as physical times. F's quantitative restriction follows from bounded original utilities and the same \(n\)-group product.

This is a full author proof for Exact v5 alone. Section A retains the general monotone-subadditive semantic interface, while B is restricted to the stated finite explicit unweighted XOS representation. C additionally uses the original total-one normalization; D covers only its stated shared singleton REPAIR alternatives. General XOS was never assumed submodular. There is no weighted-agent extension, general-subadditive backend extension, all-group constant minimum, different dummy mechanism, state-dummy SC bridge, generic UM configuration-relaxation conclusion, source-hardness proof, implemented backend, external-review certificate, or global-novelty assertion.

The original v1–v4 texts and all prior numerical objections remain process sources with their identities intact. In particular this proof does not validate or erase the disputed old generic-subadditive numerical chain. The supplied v5 describes its exact residual normalization and candidate-local relative flooring as a strengthening of v4's globally gridded input scope; proving v5 now is not a claim that a full v4 NSW author proof or a new independent v4 review previously existed. The tool proofs and the prior independent attack were knowingly read, as disclosed in §0. Any subsequent independent read-after review of this author manuscript must be recorded separately after that reviewer has actually read the frozen text.

After final author checking, this file is to be frozen read-only and its SHA256 recorded externally, avoiding a self-hash loop. Freezing certifies the identity of this author manuscript, not an execution audit or independent mathematical approval.
