# Uniform swaps and raw/real replay: independent checks

2026-10-25, tree12. Sources read:
[`../credible/uniform_copy_swap_component.md`](../credible/uniform_copy_swap_component.md)
and [`../geometry/conservative_raw_tail_replay.md`](../geometry/conservative_raw_tail_replay.md).
Original arbitrary-m/common-catalog/complete-history HALF remains **OPEN**.
These internal checks do not supply the missing covariance amount.

## 1. Uniform reset and excess signs

For a genuine source query z and one real future-j deviation z', put
delta=z'-z and F_i=sum_h lambda_ih Delta_h, Delta_h=1_h(M-u).
With r_i=eta_i+mu_i d_i+F_i-score>=0, exact subtraction gives

    delta score=mu_i delta d_i+delta F_i+r_i(z)-r_i(z').

Prefixes before j are identical. Therefore delta F_i is the sum of the
ancestor losses lambda(u_k(z)-u_k(z')), the current lambda_j Gamma_j, and
Sdesc(z)-Sdesc(z'). Both strict-descendant surpluses are nonnegative because
their respective post-j suffixes follow genuine SPEs. FIRST j=i+1 has no
ancestor sum. The stated upper bounds dropping target surplus and target
reduced cost have the correct signs.

For EXCESS over H_i=eta_i+mu_i u_i, the source canonical slack subtracts:
each ancestor target deficit is loss_k-s_k, current deficit is Gamma_j-s_j,
and strict descendants contribute -Sdesc(z'). This validates the supplied
EXCESS formulas. It does not license using the dual on excluded actual tags;
the uniform raw domain here analytically frees all actual tags.

## 2. Same-row raw swap and HALF-R

Let z=(h_i,A,B,Y), zswap=(h_i,B,A,Y), d=u_i(z), v=u_(i+1)(z), and
C_i=d_i+sum_(k>i)(M-u_k). Final counts agree and all deeper prefix counts
agree. The future continuation sets are count-isomorphic, so deeper M
values agree; no selected fixed-policy continuations are identified.

The entering and first-follower utilities swap; all later utilities agree.
Thus

    C_i(zswap)-C_i(z)=2(v-d)+M(h_i,B)-M(h_i,A),
    ell_i(zswap)-ell_i(z)=1_A-1_B.

For P_i(T)=a dot 1_T+mu_i M(h_i,T), reduced-cost subtraction gives exactly

    r_i(zswap)-r_i(z)=2mu_i(v-d)+P_i(B)-P_i(A).

If nonnegative source weights theta are action-balanced WITHIN this same
row/prefix, the P_i differences cancel. Since r_i(zswap)>=0,

    mu_i sum theta(d-v)
       =(1/2)sum theta[r_i(z)-r_i(zswap)]
       <=(1/2)sum theta r_i(z).

All signs and the factor 1/2 check, including mu_i=0. This is a signed
quantity, not an edgewise positive-part bound. Source masses must be
respected before using the parent's original R inventory. A collection of
replay intermediates does not inherit a fresh original r_i(z) bank each
time. Uniform mu across rows does not by itself cancel M(h_i,T), since the
actual prefixes h_i differ.

For the FULL-slot score a dot c, the raw swap preserves the score exactly.
Thus the same proof has P_i(T)=mu_i M(h_i,T), without the a dot 1_T term.
The balanced-flow HALF-R factor and source-capacity conditions are unchanged.

More generally a raw swap of the entering action with future role j keeps
full counts and all terminal utilities except exchanging d_i,u_j. It gives
delta C_i=2(u_j-d_i)+delta T_i, with T_i=sum_(k>i)M(z_<k), and hence
delta r_i=2mu_i(u_j-d_i)+mu_i delta T_i+a(B_j)-a(A).
This is only a fixed-potential identity until an applicable conservative
swap flow and its source capacities are supplied.

## 3. Geometry's raw coordinate flow and martingale

Geometry samples source Z~P_i and target Y~Q_i independently, freezes the old
source suffix while replacing its future action cells one at a time by the
target cells, and changes the tag last. The stated p_A Q_i(Y) masses are
nonnegative/unit-conservative with the correct endpoint Q_i. Fixed F_i and
common-shadow work telescope with their signs kept; taking positive parts
would be invalid. Final tag replacement changes no deleted-row-i load.

For the proposed reverse filtration G_k, b_k-c_k is G_(k-1)-measurable and
M_k=E[v_A|G_k] is a reverse martingale ending at E[v_A]. Therefore
sum E||M_(k-1)-M_k||^2<=Vp. Also

    M_(k-1)-E[v_A]=sum_(l>=k)(M_(l-1)-M_l),

so its DIAGONAL formula with the cumulative replaced prefix multiplier
sum_(k<=l)(b_k-c_k) follows exactly by exchanging the finite sums.
The prefix multiplier cannot be dropped or priced by Vp repeatedly.

The posterior retag variant preserves the complete (tag,raw-tail)
distribution at each refresh under its stated independent-target sampling.
It cannot replace a fixed original source label in adaptive work without
accounting for that additional change.

## 4. Distinguish the raw coordinate path from genuine replay

Geometry's intermediate tail freezes old source cells; it generally is not
the original strategy completion after its target prefix. Hence its local
coordinate edges do not automatically have genuine current-player IC.

The separate [tree replay](real_replay_covariance_flow.md) instead follows
the original sigma completion after EVERY imposed target-prefix action.
Each future edge has a true original whole-IC slack. For each passive A and
target Y both constructions have identical endpoints: source z_A, hybrid
(h_i,A,Y_future), and finally exact Y. For fixed A every adaptive linear
shadow and every fixed F_i/B_i is a state function. Their TOTAL signed work
therefore agrees pathwise between these two constructions.

This permits equating geometry's martingale/prefix representation with the
real replay's IC/variance representation without changing terminal law or
inventing a new bank. It does not identify individual edge banks, or prove a
bound for the prefix multipliers. Both constructions still stop at the same
quantitative covariance payment gap, also for m=5.
