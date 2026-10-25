# Crossed last replies give a one-sided two-follower decorrelation tax

**Status:** analytic lemma proved below; parent independent check requested. This is an additional necessary inequality, not a proof of ROW3 or half coverage. Model is CAG-MODEL, arbitrary common finite catalog, integer unit-client background, all ordered-history pure SPE, all ties/repetitions/empty topics retained.

Fix a complete ordered history h with three players left. Its old customer loads are b_x. Let q>=1 legal query themes be T_i (repetitions allowed). In the one given full pure SPE write R_i= sigma_(penultimate)(h,T_i), S_i= sigma_last(h,T_i,R_i), and let

    d_i = U_b(T_i;R_i,S_i).

Set

    V_b(A;B,C) = sum_(x in A) 1/(b_x+1+1_B(x)+1_C(x)),
    F_i(X) = sum_(x in X) 1/(b_x+1+1_(T_i)(x)),
    g_i(X,Y) = sum_(x in X cap Y)
                 1/[(b_x+1+1_(T_i)(x))(b_x+2+1_(T_i)(x))].

Then F_i(X)-g_i(X,Y)=V_b(X;T_i,Y). Define the private first-follower tax

    tau_i = g_i(R_i,R_i)-g_i(S_i,R_i)
          = sum_(x in R_i minus S_i)
                 1/[(b_x+1+1_(T_i)(x))(b_x+2+1_(T_i)(x))].

The lemma is

\[
\boxed{\quad
\sum_i d_i-\frac1q\sum_{i,j} V_b(T_i;R_j,S_j)
       +\sum_i\tau_i\ \ge0.\quad} \tag{1}
\]

This does not claim ordinary decorrelation is nonnegative. The tax is precisely a valid payment for its potentially negative deletion-return term.

## Legal crossed replies and the exact identity

Let i,j be independent uniform indices. Every K_ij=sigma_last(h,T_i,R_j) is the original strategy's true reply at that exact ordered history. Introduce three nonnegative SPE slacks:

\[
\begin{aligned}
L^1_{ij}&=V_b(R_i;T_i,S_i)-V_b(R_j;T_i,K_{ij}),\\
L^2_{ij}&=V_b(K_{ij};T_i,R_j)-V_b(S_j;T_i,R_j),\\
L^3_{ij}&=V_b(S_i;T_i,R_i)-V_b(K_{ij};T_i,R_i).
\end{aligned} \tag{2}
\]

The first is the genuine first follower's deviation to R_j, followed by K_ij. The second is K_ij's last-node best response compared with S_j. The third is S_i's last-node best response compared with K_ij. No altered continuation is frozen, and every named theme is in the common catalog.

Write Phi_b(X,Y)=sum_x sum_(k=1)^(1_X+1_Y) 1/(b_x+k). The usual exact-potential telescoping gives the pointwise algebraic identity

\[
\begin{aligned}
V_b(T_i;R_i,S_i)-V_b(T_i;R_j,S_j)
={}& L^1_{ij}+L^2_{ij}
 + F_i(S_i)-F_i(K_{ij})\\
&+\Phi_b(R_j,S_j)-\Phi_b(R_i,S_i).
\end{aligned} \tag{3}
\]

Moreover, by expanding the final slack in (2),

\[
F_i(S_i)-F_i(K_{ij})
=L^3_{ij}+g_i(S_i,R_i)-g_i(K_{ij},R_i). \tag{4}
\]

Average (3)-(4). The two Phi terms cancel because i and j have the same law. Adding E_i tau_i leaves the exact decomposition

\[
\boxed{\quad
\Delta+\mathbb E_i\tau_i
=\mathbb E_{i,j}(L^1_{ij}+L^2_{ij}+L^3_{ij})
 +\mathbb E_{i,j}\big[g_i(R_i,R_i)-g_i(K_{ij},R_i)\big]\ge0,
\quad} \tag{5}
\]

where Delta=E_i d_i-E_(i,j)V_b(T_i;R_j,S_j). The final remainder equals g_i(R_i minus K_ij,R_i minus K_ij), hence is nonnegative for every client. Multiplying (5) by q proves (1).

## Direct histogram row for five queries

For one customer write p=b_x, t_i,r_i,s_i in {0,1}, j_T=sum_i t_i. The coefficient of (1) is

\[
\boxed{\quad
\sum_{i=1}^5\frac{t_i}{p+1+r_i+s_i}
-\frac{j_T}{5}\sum_{j=1}^5\frac1{p+1+r_j+s_j}
+\sum_{i=1}^5\frac{r_i(1-s_i)}{(p+t_i+1)(p+t_i+2)}.
\quad} \tag{6}
\]

The factorization of the cross-query term uses independent summation, not a claim that the query is hidden from the actual followers. At role 3 of a five-player SPE, p is the true AB load and belongs to {0,1,2}. Formula (6) depends only on the joint histogram of (t_i,r_i,s_i) and p. The row is globally nonnegative after summing clients; its individual customer coefficient need not be nonnegative.

No actual C,D,E optimality, root comparison, restriction on ties, or claim about anonymous strategies is used. Actual C,D,E constraints can therefore be coupled with (6) without changing the query branches.

## Weighted query distributions and verification

Uniformity is only used to write (1) as an unweighted query sum. For every probability vector p on the query labels, the same proof gives

\[
\mathbb E_{i\sim p}d_i-
\mathbb E_{i,j\sim p\otimes p}V_b(T_i;R_j,S_j)
+\mathbb E_{i\sim p}\tau_i\ge0.
\]

The independent Fraction audit `audit_crossed_reply_tax.py` verifies the pointwise identities (3)-(4) on all 64 relevant membership assignments for b=0,1,2,3,4,10,100 (448 cases). It also evaluates the existing 34-unit complete-SPE fixture at its old fixed safe-query distribution p*=(10,10,21,10,10,21)/82: Delta=-11/82, E tau=5/2, three-slack sum=91/164 and remainder=297/164. Thus Delta+E tau=97/41 exactly. This fixture check is not a new complete-SPE verification; its source is the already recorded full-history fixture. The universal lemma rests on (2)-(5), not finite instance success.


## Sharpening by deleting identical index pairs

The original tax coefficient in (1), (5), and (6) can be improved. On the diagonal i=j, the exact same ordered history gives K_ii=S_i. Consequently the query difference, all three slacks, and the two-pair potential difference are zero. The diagonal contributes only the unnecessary equal quantities tau_i on both sides of (5). Delete these diagonal pairs before summing. The off-diagonal Phi differences still cancel, since every index occurs q-1 times on either side. The sharpened result is

\[
\boxed{\quad
\sum_i d_i-\frac1q\sum_{i,j}V_b(T_i;R_j,S_j)
+\frac{q-1}{q}\sum_i\tau_i\ge0.
\quad} \tag{7}
\]

Thus the best displayed five-query histogram row is (6) with tax coefficient **4/5**. For general query probabilities p_i, deletion of diagonal pairs gives

\[
\boxed{\quad
\mathbb E_i d_i-\mathbb E_{i,j}V_b(T_i;R_j,S_j)
+\sum_i p_i(1-p_i)\tau_i\ge0.
\quad} \tag{8}
\]

No diagonal was removed by an anonymous-strategy assumption: K_ii=S_i follows from equality of the exact full ordered history. The more conservative versions remain true, but (7)-(8) should be used in further relaxations.

## Coupling to the actual third-player branch

At a five-player actual prefix AB, write the actual remaining branch C,D,E and u_3=V_b(C;D,E). It is itself another legal query branch, with private first-follower tax

\[
\tau_C=\sum_{x\in D\setminus E}
\frac1{(b_x+1+1_C(x))(b_x+2+1_C(x))}.
\]

Apply the q=2 version of (7) separately to the pair of queries (T_i,C). The resulting pair-curl inequality is

\[
d_i+u_3-V_b(T_i;D,E)-V_b(C;R_i,S_i)+\tau_i+\tau_C\ge0.
\]

After summing over the five comparison queries this becomes the additional, independently valid histogram row

\[
\boxed{\quad
\sum_i d_i+5u_3-\sum_iV_b(T_i;D,E)-\sum_iV_b(C;R_i,S_i)
 +\sum_i\tau_i+5\tau_C\ge0.
\quad} \tag{9}
\]

For a customer whose actual memberships are c,d,e, the row coefficient is

\[
\sum_i\frac{t_i}{b+1+r_i+s_i}
+5\frac{c}{b+c+d+e}
-\frac{\sum_it_i}{b+1+d+e}
-c\sum_i\frac1{b+1+r_i+s_i}
+\sum_i\frac{r_i(1-s_i)}{(b+t_i+1)(b+t_i+2)}
+\frac{5d(1-e)}{(b+c+1)(b+c+2)}.
\tag{10}
\]

The c/(b+c+d+e) term is zero when c=0, including a zero denominator. All other denominators are positive. The hidden crossed last replies in this pair argument are the true sigma_last(AB,T_i,D) and sigma_last(AB,C,R_i). Thus (9) does not freeze D,E after a query, and it does not require either crossed reply to equal an already listed theme.

The same anchored row holds for any other true three-player continuation (Z,P,Q) after that exact AB prefix, replacing C,D,E and u_3 by Z,P,Q and its forced-query leader payoff. Its reuse requires the original full strategy's actual replies at that Z query.
