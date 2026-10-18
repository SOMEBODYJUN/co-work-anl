# 同菜单 token 的标签压缩：M1 可提升，M2 不能免费提升

ClaimVersion: SCRATCH-TOKEN-LABEL-M1-POSITIVE-M2-NO-CP-v1.

Author proof and learning record for the separately frozen statement-only `sol_token_label_lift_exact_v1.md`, SHA256 5a953ed6365e2be029ef31d3ee0184447d626971ad8af7369ee5190eac69a86d. It is not independently reviewed. The purpose is to settle the proposed uniform token-label lift before using it for growing-depth common-capacity searches. The degree-four counterexample below is fully rational and passes an exact 67-by-67 input M2 PSD check. It is not a scheduling approximation lower bound, not a near-two instance, and not a statement about Bamas's final witness. It identifies a genuine missing family of PSD constraints in this attempted compression.

## 1. The proposed local stochastic kernel

One source has k>=1 distinct interchangeable original jobs. An active source exports exactly r<=k of them to distinct unit destinations and retains h=k-r jobs at home. An inactive source retains all k jobs. Write A for the source activity and X_w for its anonymous exported occupancy of destination w. Required aggregate relations include Boolean A,X_w, X_w A=X_w, and sum_w X_w=rA, with the corresponding common moment equations. These relations hold in every actual canonical schedule. They are also the precise relations required in the M1 argument below.

Given a true selected export set, choose a uniformly random injection of its distinct destinations into the k original token labels. For t specified distinct labels assigned to t distinct exported destinations, and s further specified labels retained at home, the conditional moment is

\[
 \frac{(h)_s}{(k)_{s+t}}\prod_{w\text{ specified head}}X_w
 \quad(t\ge1).
\]

For s home-only requests it is

\[
 1-\left(1-\frac{(h)_s}{(k)_s}\right)A.
\]

Repeated requests are reduced Booleanly; incompatible requests have moment zero. A formal degree-at-most-four map applies these formulas separately per source and multiplies the resulting expressions. The degree does not increase. For actual global laws this produces an actual stochastic lift. The counterexample shows why the same sentence cannot be applied to a degree-four pseudoexpectation.

## 2. Exact M1 coefficients, including inactive/home mixing

For k>=2, let x_a,w be original label a's unit endpoint and t_a its home endpoint. With a!=b and w!=v the formal first and second moments are

\[
\begin{aligned}
 L'x_{a,w}&=L X_w/k, &L't_a&=1-rL A/k,\\
 L'x_{a,w}x_{b,v}&=L X_wX_v/[k(k-1)],
 &L'x_{a,w}x_{b,w}&=0,\\
 L'x_{a,w}x_{a,v}&=0,
 &L't_ax_{a,w}&=0,\\
 L't_ax_{b,w}&=hL X_w/[k(k-1)],
 &L't_at_b&=1-L A+h(h-1)L A/[k(k-1)].
\end{aligned}                                                    \tag{1}
\]

Each variable's diagonal equals its first moment. The formulas remain correct when r=0 or r=k. For k=1 there is no division by k-1: the lift is simply t=1-rA and x_w=X_w, so it is a linear substitution.

Here is a complete M1 PSD proof, not a CP claim for M2. Introduce category counts

\[
 n_0=k-rA\quad\text{(home)},\qquad n_w=X_w\quad\text{(heads)}.
\]

Their sum is k. The permutation average of a linear polynomial in labelled variables is linear in the n_c/k and hence in aggregate variables. Independent token permutations at different sources make cross-source contrast covariances zero. It is enough to check each source's label-contrast block.

Write coefficients as their mean over a plus contrasts d_a,c with sum_a d_a,c=0 for every category c. Direct substitution of (1) gives the contrast squared norm

\[
 \frac1{k(k-1)}\sum_a
 \left[k\sum_c d_{a,c}^2L n_c
       -L\left(\sum_c d_{a,c}n_c\right)^2\right]
 =\frac1{k(k-1)}\sum_a\sum_{c<e}
      (d_{a,c}-d_{a,e})^2L(n_cn_e).                       \tag{2}
\]

The equality uses only the linear sum n_c=k tested against a linear polynomial. For two head categories, L(X_w X_v)>=0 follows from aggregate Boolean M2 PSD, since it is the squared norm of the degree-two monomial X_w X_v. For a home/head pair,

\[
 L(n_0X_w)=L((k-rA)X_w)=hL X_w\ge0.
\]

Thus every term in (2) is nonnegative. The trivial label sector is a linear aggregate polynomial and is PSD already under aggregate M1. This proves full labelled M1 PSD, simultaneously for all interchangeable groups and all untouched aggregate/context variables, under the stated common aggregate equations and M2 positivity. No unknown distribution is required for this M1 conclusion.

If the additional native identities identify A with the incoming-unit sum and give the destination same-head unit-pair zeros, the resulting full first/same-row-second moments of a canonical native row have a valid row law: inactive with all homes; active with one incoming original unit endpoint and a uniform h-subset of its home job labels. Incoming endpoint labels are distributed according to their lifted first moments. This observation is conditional on those extra native identities; it is not an extra conclusion from the abstract group equations alone. It is a mathematical configuration distribution, not a claim to list every h-subset in polynomial support or solve an arbitrary row-configuration oracle.

## 3. A degree-four aggregate point with a positive Gram

Take k=4, ten Boolean X_1,...,X_10 with sum X_i=4, and one further Boolean Y. Split the ten indices into two halves of size five. Let nu be the genuine uniform law on the 210 four-subsets of [10]. Let beta be the signed law with these weights:

* each four-subset entirely within one half: weight 1/8 (ten such subsets);
* each four-subset with two points in each half: weight -1/400 (100 such subsets);
* every other four-subset: weight zero.

The signed weights sum to one. Define delta=1/100 and the functional through total degree four by Boolean reduction and

\[
 L f(X)=\mathbb E_\nu f(X),\qquad
 L(Yf(X))=\delta\mathbb E_\beta f(X).
                                                               \tag{3}
\]

In the second formula f has degree at most three. All Boolean equations and the cardinality equation sum X=4 hold multiplied through total degree four, because every underlying subset has size four. Pure X first and second moments are a genuine full four-subset configuration law; Y has the genuine Bernoulli marginal delta.

The signed law's matrix M_beta=[E_beta X_iX_j] has diagonal 2/5, off-diagonal 7/20 within a half and -1/25 between halves. Its eigenvalues are

\[
 8/5\text{ on the all-one vector},\quad
 2\text{ on the half-sign vector},\quad
 1/20\text{ on the two within-half sum-zero spaces}.        \tag{4}
\]

They are strictly positive. A constant in a linear polynomial of X can be absorbed using sum X=4, so (4) gives the positive Gram for the whole linear-polynomial quotient of the signed law.

To prove global aggregate M2 PSD, write any Boolean degree-two polynomial as q_0(X)+Yq_1(X), where q_0 has degree at most two and q_1 is linear. Enlarge q_0 to an arbitrary function on the 210 four-subsets; proving positivity on this larger space suffices. Let B be the 210-by-10 subset-incidence matrix and W=diag(beta(S)). In this enlarged representation the squared norm has block matrix

\[
 \begin{pmatrix}
 I_{210}/210 & \delta W B\\
 \delta B^T W & \delta M_\beta
 \end{pmatrix}.                                          \tag{5}
\]

Its Schur complement is delta(M_beta-delta D), where D=210 B^T W^2B. The eigenvalues of D, on the same three spaces as (4), are

\[
 5271/100,\qquad105/2,\qquad5313/1600.                     \tag{6}
\]

Subtracting delta times these from (4) leaves three strictly positive rational numbers. Therefore (5), and hence the original aggregate M2, is PSD. The exact audit also checks the actual 67-by-67 Boolean-monomial moment matrix directly by rational Schur elimination; its rank is 55. No numerical SDP feasibility inference is used.

## 4. The labelled M2 has an explicit negative norm

Let s_i=+1 on the first half and -1 on the second. Under beta,

\[
 \mathbb E_\beta\left(\sum_i s_iX_i\right)^2=20,
 \qquad \sum_iX_i=4.
\]

Under the proposed uniform injection into four original token labels, consider the degree-two polynomial

\[
 Q=Y\sum_i s_i(x_{1,i}-x_{2,i}).
\]

The formal lift (including Y unchanged) forces

\[
\begin{aligned}
 L'(Q^2)
 &=\frac{2}{4\cdot3}\,
       L\left[Y\left(4\sum_i X_i-(\sum_i s_iX_i)^2\right)\right]\\
 &=\frac{2\delta}{12}(16-20)
   =-\frac1{150}<0.                                      \tag{7}
\end{aligned}
\]

Thus the degree-four lift is not PSD, even though its input global M2 and local row moments are valid. Formula (2) is not contradicted: after multiplying its contrast by Y, one needs conditional contrast positivity not supplied by aggregate M2 alone.

This obstruction is stronger than failure of one selected extension kernel. Suppose a full original-token M2 extension preserves the aggregate moments in (3) through degree four. Average it over all permutations of the four original token labels. This preserves original job one-hot equations, same-head unit-capacity row distributions, and PSD. For distinct labels and distinct heads, the averaged moment is forced to be the aggregate product moment divided by the falling factorial (4)_t: expand each aggregate X_i=sum_a x_a,i, discard repeated-label/different-head terms by original one-hot, and use token-permutation invariance. Higher moments of two distinct jobs sharing one head vanish as well, because that same-head degree-two monomial is null in M2. Therefore the averaged extension has exactly the moments used in (7), a contradiction. No original M2 extension preserving this whole aggregate point exists.

## 5. A complete ordinary native context, and its limitation

The anonymous group and the unaffected context Y can occur in a genuine small ordinary home-unit input with one fixed external root:

* thirteen machines: r, ten destinations z_i, and two destinations y_0,y_1;
* g fixed at r, time one;
* four distinct interchangeable jobs f_a, home r at time 1/8, unit at each z_i;
* one further job y, home r at time 1/2, unit at y_0 and y_1.

There are six original jobs and 48 finite endpoints. The home budget at r is one. At target one g forces all five other jobs away from home. A full ordinary assignment is g at r, f_a at four distinct z_i, and y at y_0. Its peak is one, so the actual OPT is one.

In an identity-erased aggregate model, X_i is destination z_i's occupancy and Y is y's endpoint y_1 (the other endpoint is 1-Y). Root home variables vanish. The aggregate point (3) has full anonymous unit-capacity row distributions, the exact root export count, and positive global M2. Its no-extension result concerns the original f identities. It is not a feasible point of the full original-job relaxation, and is not a makespan integrality gap: this ordinary input has an actual strong-one schedule. A compressed solver must reject this particular aggregate point or retain more information; it may find another point.

## 6. A concrete missing PSD block

For a source group of k labels and an untouched Boolean context Y, the token-permutation standard representation forces the aggregate conditional-contrast matrix

\[
 \left[k\,\mathbf1_{i=j}L(YX_i)-L(YX_iX_j)\right]_{i,j}
 \succeq0.                                                \tag{8}
\]

It follows from the common original M2 norms of Y times token-label contrasts. At the point above its half-sign eigenvalue is delta(8/5-2)=-2delta/5. More generally, external linear contexts Z,Z' produce the block with entries

\[
 k\,\mathbf1_{i=j}L(X_iZZ')-L(X_iX_jZZ'),                  \tag{9}
\]

through total degree four, when the contexts are untouched by this source's label permutations. This is one explicit standard-label Gram block, not a sufficient characterization of the whole original M2. Quadratic requests involving two labels from the same group bring further label-partition/Johnson-scheme blocks. Their complete positivity and exact feasibility equivalence remain open here; (8) and (9) do not claim to finish that compression.

The self-contained exact audit is `sol_token_label_hypergeometric_lift_audit.py/json`. It records the full 67-by-67 rational input Gram of rank55, the positive 46-by-46 labelled M1 of rank38 including four zero home variables, all cardinality ideal checks, the three Schur eigenvalues, the negative original quadratic norm, and all six actual original jobs and a complete peak-one assignment. Replays compare fixed output bytes and never overwrite an existing frozen output. Runtime and encodings are finite polynomial for this fixed counterexample. There is no main-target completion, free exact oracle, external review, or general impossibility assertion.
