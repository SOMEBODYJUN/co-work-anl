# OPT-specific exchange rows for a true-query menu

**Status:** elementary valid inequalities, not a proof of HALF5 or ROW3. Menu-budget agent proposed using static optimality to exchange the private query-external banks; this note supplies exact histogram rows for parent integration. Use only when T_1,...,T_5 actually attain OPT_5. They are not valid for an arbitrary comparison tuple.

Write O=union_j T_j. For any legal theme R and any index k, replacing T_k by R yields

\[
|R\setminus O|\le |T_k\setminus(R\cup\bigcup_{j\ne k}T_j)|. \tag{1}
\]

This follows by comparing the two unions. The gained part is precisely R minus O; the lost part is precisely the displayed right side. No equilibrium property is needed.

For indexed legal themes R_i with bits r_i, query bits t_i, and j_T=sum_i t_i, summing the paired replacements k=i yields the globally nonnegative row with per-client coefficient

\[
\boxed{\sum_i t_i\mathbf1_{j_T=1}(1-r_i)
       -\mathbf1_{j_T=0}\sum_i r_i.} \tag{2}
\]

Summing all 25 replacements (R_i,T_k) gives

\[
\boxed{\mathbf1_{j_T=1}(5-\sum_i r_i)
       -5\mathbf1_{j_T=0}\sum_i r_i.} \tag{3}
\]

The same rows hold for indexed S_i. For one fixed legal theme C the five replacements give

\[
\boxed{\mathbf1_{j_T=1}(1-c)-5c\mathbf1_{j_T=0}.} \tag{4}
\]

If only the combined load b=1_A+1_B of two actual prefix themes is kept in the histogram, summing (4) for A and B gives the valid row

\[
\boxed{\mathbf1_{j_T=1}(2-b)-5b\mathbf1_{j_T=0}.} \tag{5}
\]

Thus (2)-(5) are compatible with the parent's b,C,D,E and five (t,r,s) histogram without introducing new labels. They use optimality, not an anonymous continuation or frozen deviation.

For the crossed-reply private tax tau_i, customers outside O have t_i=0 and

\[
\tau_i(x)=\frac{r_i(1-s_i)}{(b_x+1)(b_x+2)}\le\frac12r_i.
\]

Consequently (1) at k=i gives

\[
\frac45\cdot\frac15\sum_i\tau_i(N\setminus O)
\le\frac{2}{25}\sum_i|R_i\setminus O|
\le\frac{2}{25}\sum_i
 |T_i\setminus(R_i\cup\bigcup_{j\ne i}T_j)|. \tag{6}
\]

The right side consists of specific private optimal clients missing their paired R_i, so it is not free actual W credit. Those clients may still be covered by S_i; their query payoff can be only 1/2 (before accounting for old background). Hence (6) alone does not upperbound the total tax by an unused part of the actual payoff budget. This distinction prevents silently spending their query profit twice.

More generally, for any index subset I and legal replacement themes H_i (i in I), exact optimality gives

\[
\sum_x\left[\mathbf1_{j_T>0}
 -\mathbf1_{\sum_{k\notin I}t_k+\sum_{i\in I}h_i>0}\right]\ge0. \tag{7}
\]

Sums of (7) over all subsets of a fixed cardinality are histogram-compatible when h_i is r_i or s_i. They retain the joint index pairing and can be stronger than summing the one-replacement rows. No claim is made here that these rows close ROW3.
