# Shared menu loads: universal convex components and the exact sign boundary

2026-10-25. Personal draft, independently aligned with root's `../parent/shared_load_bregman_working.md`. Q-CAG-HALF, root aggregate security, AFC and the shared-load candidate remain OPEN. There is no new unconditional welfare bound here. These calculations identify a genuinely weaker joint query relaxation, its positive convexity credit, and the precise term which still needs full-history payment. The last section rejects only the stronger auxiliary sign C<=0, on an already known original-model SPE.

## 1. The general shared-load candidate

Fix any original CAG input, any m and a complete ordered-history pure SPE sigma. Its actual path is S and total utility is W. At actual position i force B and execute the same sigma, then delete current i. Write ell_i(B) for the resulting m-1-slot customer load. No successor is frozen. Set

    K=(1/m) sum_i conv{ell_i(B):B in catalog},
    F_p(L)=sum_x rho_x/(1+L_x),  rho_x=Pr_(A~p)[x in A].

Every L in K is a legal fractional catalog background of total mass m-1. The candidate is

    for every p: min_(L in K) F_p(L)<=W/m.       (SHARED?)

The convex minimax theorem makes it equivalent to the existence of one L in K capping every pure query at W/m. This implies W>=m delta_m and the known static comparison OPT_m<=(2m-1)delta_m would prove half. This is a sufficient open bridge, not an equivalence to half. In m=5 the same conditional calculation gives OPT_5<=9W/5; no unconditional m=5 conclusion follows without SHARED.

If AFC holds then SHARED follows by Jensen. The reverse has no proved implication. Unlike AFC, SHARED evaluates a single reciprocal after averaging loads, rather than averaging reciprocal query payments. It also retains far more flexibility than using only scaled actual loads or a specified tail stationary distribution.

## 2. A genuine nonnegative convexity credit

For arbitrary independent column mixtures q_i, sample I uniformly in {1,...,m}, then B~q_I, and put Z_x=ell_I(B)_x and L_x=E Z_x. For any p, exact reciprocal Taylor expansion gives

    (1/m)sum_i E_B F_p(ell_i(B))-F_p(L)
      =sum_x rho_x E[(Z_x-L_x)^2/((1+Z_x)(1+L_x)^2)] >=0.   (VAR)

This identity is valid for all finite catalogs, all p/q, every complete strategy and all empty/zero boundaries; it does not need SPE. Thus a shared-load proof can spend this nonnegative variance credit, which an AFC proof would have to discard. Equation VAR alone does not bound an AFC deficit or pay the mixed query term below.

For a pure query p=e_T the candidate does hold universally: choose each column B=T, so L_diag=(1/m)sum_i ell_i(T). Jensen and each actual-position whole IC yield

    F_(e_T)(L_diag)<=(1/m)sum_i d_i(T)<=W/m.

All these branches are real sigma continuations. This does not extend by mixing T because L_diag depends on T, while SHARED needs one background after minimax.

## 3. The exact remaining mixed-query balance

Let L* minimize F_p over K and t_x=1/(1+L*_x). Define

    IC_i=u_i-E_A d_i(A)>=0,
    C=sum_i E_A sum_(x in A) t_x^2[ell_i(A)_x-L*_x],
    D=sum_i E_A sum_(x in A) t_x^2[ell_i(A)_x-L*_x]^2/[1+ell_i(A)_x]>=0.

The exact all-input identity is

    W-m F_p(L*)=sum_i IC_i-C+D.                  (BAL)

This independently verifies root's signs and factors. The KKT condition says each supported chosen column in every realization of L* maximizes sum_x rho_x t_x^2 ell_i(B)_x. KKT controls the decorrelated coefficient rho_x; C contains the same-branch indicator 1_(x in A). That is the unpaid adaptive correlation.

For a pure query, KKT itself gives C<=0, since L_diag belongs to K and the first-order inequality is -sum_(x in T)t_x^2(L_diag_x-L*_x)>=0. For a genuinely mixed query, the next section proves C can be strictly positive even at the exact global minimizer. Thus the correct payment target is C<=D+sum IC, retaining both positive terms. Replacing it by C<=0 is too strong.

## 4. Exact original-model rejection of C<=0 at the optimizer

Use the already proved peer family `R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md` with m=6. This note does not claim a new game or repeat its complete-history SPE proof. There are six economy customers e_0,...,e_5 and five disjoint two-client banks B_0,...,B_4. Every common topic is (a,b)={e_a} union B_b. The full BASE/PUNISH/EXIT controller is exactly the source theorem.

The actual leaf is

    (0,0),(0,1),(0,2),(0,3),(0,4),(1,0),

with utilities 6/5,11/5,11/5,11/5,11/5,2 and W=12. OPT=16, so the half conjecture has ample slack. Choose p uniform on all 30 topics. In compressed bank coordinates rho_e=1/6, rho_B=1/5 and bank multiplicity is two.

The exact global shared-load minimizer is

    L*_e0=8/3;  L*_e1=...=L*_e5=7/15;
    L*_B0=...=L*_B4=1.

Here is a concrete feasible q certificate; an omitted column has mass zero:

| Actual role | Forced menu columns and masses |
|---|---|
| 1 | (1,0):1/5; (4,0):7/20; (5,0):9/20 |
| 2 | (2,0):1 |
| 3 | (0,0):3/5; (2,0):1/5; (3,0):1/5 |
| 4 | (1,0):1 |
| 5 | (1,0):1 |
| 6 | (0,0):1 |

The resulting total column load is 6L*. All selected column bank loads are exactly one per bank. Economy-0 column counts are respectively 1,1,2,3,4,5, while the five other coordinates each sum to 14/5 across the six rows.

Global optimality can be checked without trusting any numerical optimizer. Every menu column at roles 1,...,6 has economy-0 load at least 1,1,2,3,4,5, respectively, so every L in K has L_e0>=8/3. Each economy load vector sums to five. For fixed anchor l>=8/3, Jensen bounds its contribution below by

    (1/6)[1/(1+l)+5/(1+(5-l)/5)].

This expression is increasing for l>=8/3, so it is minimized at the stated anchor. Bank loads also sum to five, and Jensen gives a bank contribution of at least one. The displayed q attains both bounds. Equivalently, the exact script verifies every chosen q column maximizes the KKT weighted column load.

Thus

    min_(L in K) F_p(L)=71/44,
    C=3269/7260>0,
    D=81349/54450,
    sum IC=1147/900,
    W-6 F_p(L*)=51/22=sum IC-C+D>0.

The main shared-load candidate and BAL payment are not refuted. Only the stronger universal sign C<=0 is false, even with exact globally optimal q and t. The loss cannot be fixed by choosing a different realization q of L*: F_p is strictly convex on every customer with rho>0, so the optimizer load vector is unique, and C depends only on that vector and the fixed true menus.

`insurance_shared_covariance_exact.py 6` reconstructs this inherited controller's 180 actual-prefix menu branches, verifies the displayed rational q, KKT, all exact balances and C>0. It uses no numerical optimizer. The complete ordered-history SPE status is inherited from the source's all-m analytic proof and its independent audits; this script is explicitly not a new all-tree SPE verification. `insurance_shared_covariance_probe.py` and m6 JSON preserve discovery arithmetic, while `check_shared_load_old36.*` is an earlier unsuccessful sign diagnostic whose rational columns were feasible but whose floating minimizer was not certified.

### 4.1 The sign can remain positive at the true global saddle

The preceding uniform query is not active at the outer query maximization. Therefore it alone does not reject a sign theorem restricted to the true saddle. The same inherited game gives an exact saddle version too.

Let p* be uniform on the 25 topics with nonzero economy coordinate a in {1,...,5} and arbitrary bank coordinate. Keep precisely the same L* and rational column certificate. Now rho_e0=0, all other economy marginals are 1/5, and all bank marginals are 1/5. The KKT test still passes: every selected column minimizes its economy-0 load, thereby maximizing the total equally weighted outside-economy load; the bank weighted load is constant on all columns.

Every supported topic has query value 15/22+1=37/22, while the excluded anchor topics have query value 3/11+1=14/11. Thus all query and column KKT conditions hold simultaneously: this is a genuine global shared-menu minimax saddle, with gamma=37/22. It is not merely a minimizer for some nonoptimal p.

For every supported topic T, its current-forced deleted-menu economy load is four at role 1, and zero at roles 2,...,6. Each such deleted-menu bank load is exactly one. Hence the individual C_i(T) is constant over all 25 supported queries:

    C_1(T)=795/484,
    C_i(T)=-105/484 for i=2,...,6.

Consequently

    C=135/242>0,
    D=2017/1210,
    sum IC=4/5,
    W-6 gamma=21/11=sum IC-C+D>0.

This also rejects repairing the stronger sign C<=0 by a favorable row/query transport with the same aggregate query marginal p*: each row's C value is constant over the entire allowed support, so redistributing those queries among the six rows cannot change total C. The exact matrix entry and marginal statement is all that is claimed; arbitrary new histories or a different balance objective are not covered by this row-transport observation.

The fixed-p* certificate alone does not exclude choosing a different optimal query p with a more favorable transported C sign. The additional uniqueness/complementarity argument in section 4.2 addresses that stronger quantifier separately. Matching11 independently rebuilt all 180 menus and verified this entire fixed-p* saddle certificate; see `../matching/insurance_saddle_independent_review.md` and its independent script/JSON. That review inherits the same all-history source theorem and makes no new all-tree enumeration claim.

`insurance_shared_saddle_exact.py 6` checks the hardcoded rational q, all active query equalities, the exact per-row constancy and these fractions, using no numerical optimizer. Complete-SPE status remains the inherited source theorem. This saddle counter-sign still does not refute SHARED or HALF: the actual shared cap is 37/22<2=W/m. It shows that both the nonnegative Bregman remainder D and actual incentive slack can be real payment, even after imposing the outer active-query equality.

### 4.2 Quantifier closure over every outer optimal query

Matching11 independently checked the following uniqueness/complementarity argument after checking the fixed-p* certificate. It closes the quantifier over favorable optimal queries; the review link is the same as in section 4.1.

Every minimax-optimal shared load L must also minimize F_p*: its maximum query is at most gamma, while min_K F_p*=gamma. The p* marginals are positive on all five nonanchor economy coordinates and all five banks. Strict convexity of F_p* fixes all of those coordinates to L*. Every L in K has total economy load five, so the anchor coordinate is then fixed too. Therefore the shared minimax optimizer L* is unique.

For any outer optimal query p, min_K F_p=gamma. At the unique L*, every query value is at most gamma, so F_p(L*)=gamma. A convex combination reaching gamma cannot put positive mass on an anchor query whose value is strictly smaller than gamma. Thus every outer optimal p is supported on the same 25 nonanchor topics. On that whole set, each row C_i(T) is already constant. Hence C=135/242 for every outer optimal p and every row/query transport preserving any such marginal. The stronger C<=0 sign is therefore false even with favorable selection among all global saddle queries. The full payment C<=D+sum IC remains unaffected. This is an internally checked auxiliary sign boundary, not a new welfare result, external review or novelty certification.

## 5. Current honest stop

The only new nonnegative all-input quantity isolated here is VAR, together with pure-query KKT payment. No relation has been proved bounding the mixed C by D+sum IC. The exact saddle positive-C example shows why a proof must retain the two genuine credits, rather than trying to force decorrelation itself or only redistribute active queries between actual rows. A further derivation must use complete-history successor IC to pay this specific optimal-weight mixed amount. There is no general proof or target counterexample, and no unconditional m=5 half theorem.
