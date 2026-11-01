# 跨族真实菜单的共同客户运输包络

Status: proved necessary inequalities, exact matching checks, and exact
noncompletion of a new unrestricted-type relaxation point. The general
Q-CAG-HALF target remains **OPEN**. No new welfare bound is proved here.
The closed-form algebra has received an independent teammate attack; parent
audit and formal asset integration are separate.

## 1. General final-player comparisons and the shared coupling

Fix any complete ordered-history pure SPE of an arbitrary-player common
catalog instance. Take any q>=1 genuine decision histories of its final
player. Repeated histories are allowed. Their actual actions are F_i.
Take d indexed lists Z_i^r of catalog topics, with arbitrary origins in that
same strategy. No action from another history is treated as a continuation
at this history: it is only a legal final-player query.

For a client x let p_i be its load in source history i, f_i its membership
in F_i, and z_i^r its membership in Z_i^r. Write

\[
 d_i={1\over p_i+1},\quad A_x=\sum_i f_i d_i,\quad
 D_x=\sum_i d_i,\quad K_r=\sum_i z_i^r.
\]

Actual source payoffs and counterfactual query payoffs have the same positive
denominator p_i+1. Summing genuine best-response comparisons gives rows

\[
 \mathcal D_r=\sum_x[A_x-\sum_i d_i z_i^r]\ge0,
\quad
 \mathcal O_r=\sum_x[(q-1)A_x-K_rD_x+\sum_i d_i z_i^r]\ge0. \tag{1}
\]

The first uses matching i=j; the second uses every ordered i!=j. These
comparisons remain legal with empty/repeated topics and all history-dependent
ties. Crucially, two rows involving the same target tuple share one matching
of that tuple to source histories. They cannot each choose a different
maximizing matching.

Suppose a compressed client state retains the source inverse denominators
and the target tuple histogram, each divided by the same known index label
t_i. The application below uses t_i=1_{x in T_i}, the membership in the
common optimal comparison topic. Several shared membership bits can instead
be used as the label. A real client always supplies a label-preserving
matching. We may maximize over all such matchings as a necessary-condition
relaxation. This does not assume independence of the families.

For nonnegative weights alpha_r,beta_r on diagonal/offdiagonal comparisons,
define

\[
 a=\sum_r[\alpha_r+(q-1)\beta_r],\quad
 b_x=\sum_r\beta_rK_r,\quad
 v(z)=\sum_r(\beta_r-\alpha_r)z^r.
\]

Within each label t sort the source d_i and the target scores v(z_i) in the
same order. The rearrangement inequality gives the exact per-client maximum

\[
 U_x(\alpha,\beta)
 =aA_x-b_xD_x+\sum_t\sum_{k=1}^{q_t}d_{t,(k)}v_{t,(k)}.
\]

Every real SPE therefore satisfies the **joint envelope**

\[
                     \boxed{\sum_x U_x(\alpha,\beta)\ge0.} \tag{2}
\]

In general this is stronger than the sum of separately maximized envelopes,
because max(f+g)<=max f+max g. Each per-client extremum is exact for the
stated marginal matching problem. Their sum is still a deliberate relaxation
of any additional topic equality or cross-client consistency in the original
game. It is not called the exact maximum of a globally consistent full SPE.

## 2. Three explicit two-menu formulas

For two target lists M,N, within each label t let k_t,l_t,h_t count M, N,
and their same-index intersection. Their union count is u_t=k_t+l_t-h_t.
Let K=sum k_t and L=sum l_t. Write Top_t(r) and Bottom_t(r) for the sum of
the r largest/smallest source inverse denominators d_i in group t; empty
sums are zero. Three useful special cases of (2) are the following, where
each bracket is summed over clients and the resulting total is nonnegative:

\[
\begin{aligned}
 OO_x={}&2(q-1)A_x-(K+L)D_x
       +\sum_t[\operatorname{Top}_t(h_t)+\operatorname{Top}_t(u_t)],\\
 DD_x={}&2A_x-
       \sum_t[\operatorname{Bottom}_t(h_t)+\operatorname{Bottom}_t(u_t)],\\
 DO_x={}&qA_x-LD_x+
       \sum_t[\operatorname{Top}_t(l_t-h_t)-\operatorname{Bottom}_t(k_t-h_t)].
\end{aligned}\tag{3}
\]

Here D refers to M and O to N in the last line. The OO score is two on h_t
slots and one on u_t-h_t slots. The DO score is +1 on N-only slots and -1
on M-only slots. This directly proves (3), including q=1 and empty groups.

Separate OO maximization uses Top(k_t)+Top(l_t), instead of the smaller
Top(h_t)+Top(u_t). The exact information recovered is the target menus'
same-index intersection, even when their source family is different.

An independent strict example uses q=2, one client and one label, source
d=(1,1/2), f=(0,1), hence A=1/2. The two target menus partition the two
indices: tuples (0,1),(1,0). All four separately optimized D/O envelopes
are zero; the joint OO envelope is -1/2. Thus these four separate rows do
not enforce the shared matching. This example is not claimed to satisfy
the other preexisting SPE rows.

## 3. Cross-family last-two-player query pairs

Take q genuine histories with two players left. At source branch i let
p_i be the background load and let A_i,B_i be its actual actions. Define

\[
 f_i(T)=\sum_{x\in T}{1\over p_i+1},\quad
 g_i(T,S)=\sum_{x\in T\cap S}{1\over(p_i+1)(p_i+2)},
\quad H_i=u(A_i,B_i)+u(B_i,A_i)+g_i(A_i,A_i).
\]

The retained-overlap tax proved in round3 is

\[
                  H_i\ge f_i(M_j)+f_i(N_k)-g_i(M_j,N_k).\tag{4}
\]

For completeness, let Q be the same strategy's actual reply after M_j.
The difference in (4) equals the first player's real deviation slack plus
the last player's Q-versus-N_k slack at M_j, plus its B_i-versus-Q slack at
A_i, plus g_i(A_i,A_i)-g_i(A_i,Q)>=0. Thus no continuation is frozen.

Unlike the within-family round3 rows, let the query menus M,N now come
from a different recorded family. With B=sum z_j, C=sum w_j and
K=sum z_jw_j, the client's coefficient for each equality pattern of (i,j,k)
is n H_{i,x}-L/(p_i+1)+M/((p_i+1)(p_i+2)), summed over source i, where
H_{i,x} is this client's contribution to H_i:

| Pattern | n | L | M |
| --- | ---: | --- | --- |
| i=j=k | 1 | z+w | zw |
| j=k, j!=i | q-1 | B-z+C-w | K-zw |
| j=i, k!=i | q-1 | (q-1)z+C-w | z(C-w) |
| k=i, j!=i | q-1 | B-z+(q-1)w | (B-z)w |
| all distinct | (q-1)(q-2) | (q-2)(B-z+C-w) | (B-z)(C-w)-(K-zw) |

For a fixed target tuple histogram, maximize this coefficient over a
**single** label-preserving assignment of target tuples to source states.
This is a finite transportation/assignment problem. Its maximum is a valid
upper envelope on the true row, so summing that maximum over clients gives
a necessary nonnegative row. Any nonnegative combination of these rows can
be maximized jointly using one assignment and gives another joint cut.
The code evaluates individual orbit rows; it does not yet optimize arbitrary
combinations of pair-orbit rows.

For source-state counts u_alpha and target-tuple counts v_beta in one label
group, the upper envelope is the transport optimum
max sum C_alpha,beta n_alpha,beta subject to the two marginal constraints.
Its dual is min sum u_alpha r_alpha+sum v_beta s_beta subject to
r_alpha+s_beta>=C_alpha,beta. Integer margins give an integral transport
optimum. These per-client primal/dual statements do not assert a common
globally consistent SPE realization of all those optima.

Two of these assignment problems admit closed forms. Set
a_i=1/(p_i+1), e_i=1/(p_i+2), b_i=a_i-e_i. For target union and intersection
counts u_t,h_t as above, let Top_a/Bottom_a and Top_e/Bottom_e use the
corresponding source lists. The following client coefficients have
nonnegative sums:

\[
\boxed{\begin{aligned}
 E_x={}&(q-1)\sum_iH_{i,x}-(B+C)\sum_i a_i+K\sum_i b_i
       +\sum_t[\operatorname{Top}_{a,t}(u_t)+\operatorname{Top}_{e,t}(h_t)],\\
 F_x={}&\sum_iH_{i,x}
       -\sum_t[\operatorname{Bottom}_{a,t}(u_t)+\operatorname{Bottom}_{e,t}(h_t)].
\end{aligned}}\tag{5}
\]

E uses j=k!=i, and F uses i=j=k. The variable target score is
a_i(z+w)-b_i zw. For membership cardinality r=z+w this is
psi_p(r)=sum_{v=1}^r 1/(p+v). If p<p', the gain from raising r from 0 to 1,
and from 1 to 2, is larger at p than at p'. The exchange argument therefore
matches larger r to smaller p for the maximum, and to larger p for the
minimum. Both a_i and e_i have this same order, proving (5).

There is an important exact simplification in the five-player application,
noticed independently by the unrestricted-pricing teammate. For a source
AB or AE family, the two-player background is p_i=a+b+t_i or a+e+t_i.
It is **constant within each retained t group**. Therefore every orbit's
query-cost sum is independent of the unknown matching: source contributes
only n sum H_{i,x}, and target contributes

\[
 \sum_{\text{target tuples }z}
 \left[-{L(z)\over p_{t(z)}+1}
       +{M(z)\over(p_{t(z)}+1)(p_{t(z)}+2)}\right]. \tag{6}
\]

All 160 cross-family pair rows with AB/AE source consequently remain
additive across source and target histograms. They can enter the existing
unrestricted pricing scheme without introducing a coupled histogram
maximization. Both negative pair rows reported below are of this simpler
kind; their noncompletion does not depend on a transport relaxation. The
other 60 rows, with source second, can depend on matching because their
background also contains H_i. The code exposes (6) as `additive_row` and
checks it separately against the transport evaluator.

The mechanism has an arbitrary-player formulation. Fix any genuine history
h with exactly three players left. Let its antepenultimate player choose
each indexed anchor T_i in turn, and use the same strategy's actual final
two actions R_i,S_i. For a client, source background in that last-two
subgame is p_i=p_x(h)+t_i. Thus it is constant in each t=0,1 group for
**every total player count**, not only five. Take arbitrary indexed legal
query menus M_i,N_i from anywhere in the game. Put n_t=#\{i:t_i=t\},
a_t=1/(p_x(h)+t+1), b_t=1/((p_x(h)+t+1)(p_x(h)+t+2)), and retain their
k_t,l_t,h_t as above. Then the j=k!=i inequality is exactly

\[
\boxed{(q-1)\sum_iH_i\ \ge\
 \sum_x\left[(B+C)\sum_t n_ta_t-K\sum_tn_tb_t
       -\sum_ta_t(k_t+l_t)+\sum_tb_th_t\right].}\tag{7}
\]

This is the literal sum of real tax comparisons, with no matching
maximization or loss. All five equality patterns similarly collapse by
the preceding table. The hypothesis is a common-prefix antepenultimate
deviation family; it is not an assertion about arbitrary source histories.
Equation (7) supplies a genuinely arbitrary-player cross-family constraint,
but no argument here turns its collection over histories into half coverage.

## 4. Exact evidence and limits

`joint_transport.py` checks 8160 generic sorted-score maxima against literal
permutations. For the original 64 atoms and the later 42-atom 447-row point
it checks respectively 10368 and 6804 literal joint matchings. The original
point violates `AE:second:1O+1*3O` while both separate component envelopes
are strictly positive. This is concrete strictness of joint coupling on an
existing relaxation point, beyond the elementary q=2 example.

`new_point_separation.py` evaluates the new 60-atom exact point from
`../round4_pricing/exact_primal_overlap1.json`. That point satisfies all 557
stated rows over unrestricted histogram types, has W=1 and comparison cover
about 2.04202004419; it is not an SPE and its comparison cover is not
certified OPT. SHA-256:
`11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825`.
It violates 22 of 162 joint final-menu envelopes after 9720 exact matching
checks. For example `AB:AE:1O+1*2O` has slack

\[
 -{1996456868586172483674258348477230789698004041227208957222543\over
 8009267187464953266978610476016627605724079763575000300810190}<0.
\]

For this new point each negative joint final-menu row already has a negative
separate cross-family component. Its exclusion must not be attributed
specifically to joint strengthening.

`pair_transport.py` evaluates 220 cross-family pair-orbit rows on the same
point, checking 13200 exact assignment-DP results against all permutations,
5280 closed-form identities (5), and 684 compact-versus-literal triple sums.
It also checks all 9600 source-AB/AE additive identities (6).
Two rows are negative: AB source versus AE(R,S), j=k!=i, and AB source
versus second(I,J), j=k!=i. The latter slack is

\[
 -{787666402463169489247192662090163381396856775798217752504989\over
 8009267187464953266978610476016627605724079763575000300810190}<0.
\]

Thus the new unrestricted-type 557-row point cannot have a full SPE
completion retaining these recorded family marginals. No fixed-support
optimization or unrestricted welfare optimization has been performed with
the added rows. Excluding this point does not exclude all above-two points.

## 5. Exact scope of the joint support-function interface

For any finite selected menu comparisons, let each compressed client state
have the finite set of coefficient vectors produced by its allowed
matchings. Convexify that set, weight it by the client mass, and sum these
sets. Feasibility of the selected aggregate inequalities in this **convex
matching relaxation** is equivalent to nonnegativity of every nonnegative
joint support-function query (2). If the summed convex set misses the
nonnegative orthant, separation gives a nonnegative lambda with strictly
negative maximum; conversely such a lambda excludes every matching mixture.

This equivalence is a finite-dimensional convex separation statement. It
does not provide integral matching feasibility, all-history sequential
optimality, or a proof of half coverage. Further source/target family
couplings produce a multi-marginal transport problem; independent pairwise
couplings need not glue. The next mathematical obligation is to exploit
these shared-incidence cuts in unrestricted pricing or an arbitrary-player
charging argument, not to re-optimize only the old 64 types.

Reproduce from the repository root:

```sh
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/joint_transport.py
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/new_point_separation.py
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/pair_transport.py
```
