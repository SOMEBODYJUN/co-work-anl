# Round 11 direct netROW: terminal bank and endpoint boundary

2026-10-25. Scope: arbitrary finite unit-client common catalog, arbitrary m
unit providers, full ordered-history pure SPE, empty themes/duplicate coverages
allowed. **Q-CAG-HALF remains OPEN.** No new unconditional half proof or target
counterexample was found. No novelty or external review is claimed.

## 1. Precise dynamic targets

Fix the original complete SPE sigma, actual terminal Z, W=|union Z|. At actual
role i and actual prefix h_i define d_i(T)=u_i(finish_sigma(h_i,T)). Future
actions follow the original history policy, rather than a frozen suffix.
For any m-slot comparator tuple with union C, the old sufficient targets are

    sum_j d_i(T_j) >= |C|−W                         (ROW?, unproved)
    max_pi sum_i d_i(T_pi(i)) >= |C|−W              (WM?, unproved).

ROW at a minimum-actual-payoff role gives |C|−W<=m min_i u_i<=W. WM gives the
same conclusion since every permutation sum is <=W by the actual ICs.
The aggregate double-sum average implies WM, but the quantifiers differ.
True WM is already in round3/credible/general_root_regret_working.md section 7,
so it is not a new round11 candidate.

At m=5 these same implications prove OPT_5<=2W if ROW at a minimum role or WM
is established for every catalog. The identities below do not prove either
premise, so the pressure test remains conditional.

## 2. Terminal bank identity: only actual last BR is used

Let b_x be the load just before the actual last player, P={x:b_x>0}, S the
actual last theme, and W=|P union S|. For any legal T let

    Gamma(T)=sum_(x in S)1/(b_x+1)−sum_(x in T)1/(b_x+1).

The exact pointwise identity is

    W−|T| = Gamma(T)
             +sum_(x in P\T)b_x/(b_x+1)
             +sum_(x in P\S)1/(b_x+1).            (TERM)

For x in (P\T) intersect S, the two right-hand contributions are 1/(b+1)
and b/(b+1), totaling 1. For x in (P intersect T)\S, the contributions
−1/(b+1) and 1/(b+1) cancel. The other binary membership cases are immediate.
Last BR makes Gamma nonnegative, so

    W>=|T|+sum_(x in P\T)b_x/(b_x+1)
             +sum_(x in P\S)1/(b_x+1).            (TB)

This retains two explicit actual-prefix banks beyond W>=max_T|T|. If an
earlier fixed background has load beta, support H, then b>=beta and H subset P;
dropping the second bank and using monotonicity gives

    W>=|T|+sum_(x in H\T)beta_x/(beta_x+1).        (BG)

Only the actual last player's BR was used. Earlier prescribed actions may be
arbitrary. All themes remain whole legal actions. Tree11 independently split
the last BR into old/new clients and checked TB/BG; this superseded its first
all-tail bound with denominator beta+r. TERM is source-near the familiar
terminal static decomposition, not a claim of new welfare scope.

The missing payment remains: applying TERM in each forced query branch gives
different b_j,P_j,S_j. Those banks live in mutually exclusive histories.
TERM supplies no inequality charging their sum to the one original actual W;
replacing them by original actual b,P,S is invalid.

## 3. Root-free sharpening and exact endpoint boundary

RF? drops current-node optimality but keeps every strict descendant subgame a
complete SPE. The prescribed current action A may be arbitrary. With its
actual leaf Z and same true query menu, it asks

    sum_j d(T_j)>=|C|−W(Z).                        (RF?, unproved)

At the empty global root there are m players and m comparator slots. A local
extension would include full fixed-prefix coverage in W; it is not assumed.
Tree11 attacked RF on three named complete root-only policies: the compact10,
old huge StrongA5, and disjoint sizes (3,3,1,1,1,1) policies. No separation was
found; see ../tree/rootfree_named_pressure.json. This is no general evidence.

Here is the exact universal inequality left after eliminating policy choices.
At fixed prefix h let E_h(T) be all terminal count outcomes realizable by
complete SPE continuations after h,T. Set

    p_h(T)=min_(Y in E_h(T))u_current(Y).

The minimum exists. Identical-count histories have the same available outcome
count-outcome set, but minimizing continuations at different ordered histories remain
independent policies; no common Markov selector is imposed.
Fix actual A, actual endpoint Z in E_h(A), t=u_current(Z), and comparator
multiplicities n_T. The least comparator-row value among descendant-complete
policies with this fixed actual endpoint is exactly

    n_A t+sum_(T != A)n_T p_h(T).                   (ENV)

The diagonal must use t, not p_h(A), because the actual child already realizes
Z. Other immediate children are disjoint histories and may independently use
their minimizing complete SPEs. Thus RF is equivalent to

    W(Z)+n_A t+sum_(T != A)n_T p_h(T)>=|C|.         (RF-END?)

For full current-node SPE restrict endpoints to t>=max_T p_h(T). This is
necessary and sufficient: pessimistic off-children support the prescribed Z.
At the empty global root, universal root ROW is exactly RF-END? on this
restricted endpoint set. At nonempty h this characterizes the stronger local
node class; an endpoint need not extend to a whole-game SPE reaching h, so it
must not be called equivalent to the original actual-global-role quantifier.
ENV is an exact quantifier reduction, not a proof or a welfare advance.

Attempted induction stops at a concrete selection interface. The actual next
role's deviations use (h,A,T), while a current-query branch uses (h,T,B_T).
Even if B_T=A, histories (h,A,T) and (h,T,A) may specify different credible
tails. Available endpoint sets can coincide; chosen profits cannot be
identified. TERM does not resolve this difference, and the endpoint minimum
does not automatically commute with W(Z).

## 4. Optimal comparison exchange: useful counts, unpaid share matching

ROW/RF above quantify arbitrary comparisons. A weaker route may use only
optimal m-tuples. Fix such a tuple with union C. Any k legal alternative
topics A_1,...,A_k and k comparator indices J satisfy

    |(union_l A_l)\(union_(j notin J)T_j)|
      <=|C\(union_(j notin J)T_j)|.                (OPT-EX)

Indeed replacing those k topics cannot increase optimal coverage. For k=1,
every legal B obeys, for each j,

    |B\C|<=|(T_j\union_(l != j)T_l)\B|.          (ONE-EX)

Thus off-optimum insurance forces unserved optimal-exclusive clients in every
removable comparator theme. It is stronger than comparing just their total
block sizes. A hoped-for use is pairing insurance rents to these retained
clients. No reciprocal-share matching under their different branch loads was
obtained. Applying ONE-EX separately to all later actions reuses retained
clients and is invalid; joint OPT-EX must be retained.

## 5. Bounded numerical attack and exact limitations

These scripts test named general candidates only. `attack_netrow.py` generates
full ordered-history policies by backward induction with exact integer-scaled
terminal utilities. Policy choices remain separate at each ordered history;
only terminal count utilities are cached. A 600-game exploratory run found no
ROW counterexample; most random games cover the relevant universe and were
diagnostically weak. It was not continued as a main route.

`attack_netrow_cone.py` took 12 such policies with (m,k) in
{(3,5),(4,5),(3,6)}. It retained every original all-history IC row, formed exact
integer coefficients for every m-slot comparator multiset and each early
actual role, and minimized W−|C|+sum d over nonnegative type weights summing to
1. There were 861 floating HiGHS optimizations; no negative objective was
returned. This is **finite numerical nonseparation only**, not an exact LP
certificate and not a general proof. A found candidate would be rationalized
and all ICs checked exactly before reporting a witness.

`attack_root_free_row.py` repeated these policy-cone checks after deleting only
global root IC rows: 861 optimizations, including other early actual-role rows
on these root-only plans. Again no negative objective was returned. This does
not prove RF. No original-target or named-assistant counterexample was found.

No fixed-m positive project, external network action, git operation, or
work.py action was performed. TERM/TB/BG and OPT-EX/ONE-EX are valid general
identities/inequalities; ENV is an exact endpoint reduction. None supplies a
common actual bank for mutually exclusive query histories. RF-END?, original
netROW, true WM, minimum-actual netgap, aggregate security and HALF remain
unproved here. This round does not improve the unconditional general factor.

## 6. Continued shared-load attack: an actual complement-bank interface

Root asked for continued attack on ../parent/shared_load_bregman_working.md,
using TERM against its covariance amount. No further scan was run. For its
shared-menu convex body K define V=max_p min_(L in K)sum rho/(1+L). At a
convex-minimax saddle (p*,L*) put t_x=1/(1+L*_x), rho=marginal(p*). Query-side
optimality adds to the parent's load KKT the whole-topic facts

    P_t(A)=sum_(x in A)t_x<=V for all legal A,
    P_t(A)=V on supp p*.                           (QUERY-KKT)

Every L in K is m−1 total mass of legal topics, so the static menu slack

    Q=(m−1)V−sum_x L*_x t_x>=0.                    (MENU-SLACK)

Actual actions also have nonnegative static-price slack V−P_t(S_i). No
customer reweighting of original IC is involved in these static inequalities.

Average TERM over this SAME p*. At the actual last prefix b,P,last action S,
put

    B=sum_(x in P)(1−rho_x)b_x/(b_x+1)
        +sum_(x in P\S)1/(b_x+1),
    IC_m=u_m−E_p d_m(A)>=0.

The exact relations are

    W−E_p|A|=IC_m+B,
    E_p|A|−V=sum_x rho_x L*_x t_x,
    W−mV=IC_m+B−Q−sum_x(1−rho_x)L*_x t_x.         (COMP)

All four displayed quantities on the final right side are nonnegative before
their signs. The aggregate shared-load floor is therefore equivalent to

    IC_m+B>=Q+sum_x(1−rho_x)L*_x t_x.              (COMP-PAY?)

Matching11 independently checked all signs, the legal m−1 topic-mass argument
for Q>=0, and absence of hidden actual/optimal-overlap assumptions. This is an
exact residual payment interface, not an amount inequality. Earlier full-tree
IC must still control the menu-dependent right side through K. Neither TERM
nor KKT has supplied that payment.

The left bank is actual, with the same complement factor 1−rho that appears
in covariance calculations. Multiplying TERM's Gamma customer-by-customer by
t_x^2 would not preserve Gamma>=0; COMP instead uses legal whole-theme queries.
B cannot be spent again after spending the same earlier actual-client profits
elsewhere. The currency remains the single original W.

There is also a pointwise nonnegative query-holes expression:

    Q+sum_x(1−rho_x)L*_x t_x
      =sum_x rho_x t_x[(m−1)−L*_x].                (HOLES)

The bracket is nonnegative since every L in K has client load at most m−1.
For a menu representation, HOLES averages the t-price of query clients missed
by each competing provider, counted with multiplicity. Also for each legal B,
E_p P_t(A\B)=V−P_(rho t)(B)>=0. This suggests owner/client transport against
the actual complement bank, but no common reciprocal-share injection under
the original-history utility comparisons was obtained.

## 7. Last actual-load consequence of shared KKT; remaining early budget

For m>=2, each menu contains its actual column L_i(S_i)=c−1_(S_i), where c is
the original actual load. Hence their average is ((m−1)/m)c and belongs K.
The minimizer's gradient condition with w=rho t^2 gives

    sum_x rho_x t_x^2 L*_x
       >=((m−1)/m)sum_x rho_x t_x^2 c_x.

Using t L*=1−t and V=sum rho t, this is the valid further constraint

    sum_x rho_x t_x^2 c_x
       <=m/(m−1)[V−sum_x rho_x t_x^2].             (ACTUAL-LOAD)

It is a weighted linear actual-load bound, not an IC or variance payment.
It may be retained alongside tree11's insertion-error potential R_t when
checking whether the actual terminal error can fund accumulated r_beta gaps.
It does not remove the harmonic part H_c or pay the changed-prefix resets.

The exact remaining early budget is COMP-PAY: the original earlier whole-tree
ICs must prove that the actual terminal complement bank IC_m+B covers Q and
the shared-load query-complement term, jointly. Tree11's DEMAND/SWAP route
instead leaves mean r_beta(B(A))−r_beta(A) plus genuine changed-prefix resets.
My independent algebra review of those exact relations is
review_tree_saddle_variance.md. No matching or total bound on either debt was
derived here. Ending this branch is an execution checkpoint, not a claim of
mathematical impossibility. All original general targets remain OPEN.
