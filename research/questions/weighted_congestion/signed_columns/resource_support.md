# WC-R1-RESOURCE-SUPPORT v1 — bounded resource support blocks local-gadget amplification

Author: R1 / cycle_family subagent (requested configuration: gpt-6-astra / ultra, as reported by the parent; the tool result supplied no runtime model metadata). Date: 2026-10-14 UTC.

## Claim identity

- **Exact statement.** Every finite weighted atomic congestion game with nonnegative nondecreasing resource costs and at most `r ≥ 1` potential users per resource has an `r`-PNE. A global minimizer of the **unweighted** social cost is such an equilibrium. Every strictly `r`-improving move strictly decreases that social cost.
- **Objects/domain.** Finite nonempty player and resource sets; positive real player weights; arbitrary nonempty finite strategy families consisting of resource subsets. Resource costs may be arbitrary nonnegative nondecreasing functions. In particular this includes the full polynomial class WC-TARGET v1, with all nonnegative coefficients and any degree.
- **Definitions.** `U_e = {i: e belongs to at least one strategy of player i}`, `r = max_e |U_e|`. If all `U_e` are empty, every profile is a 1-PNE; this degenerate case is separate from the displayed r-bound. Player cost is `C_i(s)=Σ_{e∈s_i} c_e(x_e(s))`, without multiplication by `w_i`. Define `Φ(s)=Σ_i C_i(s)=Σ_e n_e(s)c_e(x_e(s))`, where `n_e` is the number (not total weight) of current users.
- **Quantifiers.** For every game in this class and every unilateral deviation, the potential estimate below holds; hence every finite such game has an r-PNE. No restriction on n, degree, weight ratios, strategy size, or overlap graph is imposed.
- **Scope.** A subclass obstruction, not an upper bound `o(d)` for WC-TARGET v1. The support bound r may itself grow arbitrarily with d. Arbitrarily many overlapping triads with support at most three still have a 3-PNE.
- **Dependencies.** Only nonnegativity, monotonicity, and finite pure profile space. The proof below is complete. The interpretation as a resourcewise refinement of the published n-PNE argument is literature attribution, not a required external premise.
- **Status.** Complete elementary proof; independently reconstructed by parent-assigned `cone_duality` before reading this file, according to the parent's 2026-10-14 message. Frozen-file adversarial review is pending and must not be conflated with that independent reconstruction. No external peer review or novelty claim.
- **Evidence.** Exact derivation below; `verify.py` checks all 24 moves of the supplied triad and the numerical certificate. Search programs are not evidence for this universal theorem.
- **Counterevidence/objections.** Replacing potential-user support by observed support on a non-deviation-closed sample is invalid. Weighted social cost is not the potential used here. Negative or decreasing costs invalidate the sign bounds.
- **Related files.** `TRIAD_AND_EXTENSION.md`, `verify.py`, `verification.json`, `search_layers.py`, `screening.json`.

## Resourcewise proof

Fix a profile s, player i, and deviating strategy t_i. Write s'=(t_i,s_{−i}), and partition the old/new strategy resources into

`D=s_i\t_i` (deleted), `A=t_i\s_i` (added), and `O=s_i∩t_i` (retained).

Resources outside D∪A have unchanged load and multiplicity, including O. For a deleted resource e, let m=n_e(s)≥1, x=x_e(s), and w=w_i. Its potential change is

\[
 (m-1)c_e(x-w)-m c_e(x)
 =-c_e(x)+(m-1)[c_e(x-w)-c_e(x)]
 \le -c_e(x).
\]

If m=1 the first term after departure is zero, regardless of the convention for c_e(0); polynomial costs have a defined nonnegative value at zero. For arbitrary positive-load functions this term is simply interpreted as zero and no value at zero is needed.

For an added resource e, let m=n_e(s), x=x_e(s). Since its new occupant count is m+1≤r,

\[
 (m+1)c_e(x+w)-m c_e(x)
 \le (m+1)c_e(x+w)
 \le r c_e(x+w).
\]

Define `C_D=Σ_{e∈D}c_e(x_e(s))`, `C_A'=Σ_{e∈A}c_e(x_e(s'))`, and the unchanged common cost `C_O=Σ_{e∈O}c_e(x_e(s))≥0`. Summation yields the sharper estimate

\[
 \Phi(s')-\Phi(s)\le rC_A'-C_D.
\]

Since `C_i(s)=C_D+C_O` and `C_i(s')=C_A'+C_O`, it follows that

\[
 \Phi(s')-\Phi(s)
 \le rC_i(s')-C_i(s)-(r-1)C_O
 \le rC_i(s')-C_i(s).
\]

A strictly r-improving move satisfies `C_i(s)>rC_i(s')`; consequently its potential change is strictly negative. A global minimizer exists because the pure state space is finite, and no such move can leave it. This is exactly the r-PNE condition, with the required weak boundary `≤`.

## Boundary cases and stronger interface

The proof permits zero coefficients, identically zero resource costs, empty strategies, common resources, and arbitrary positive real weights. It never divides by a cost, so zero deviation costs and `0/0` cause no problem. For r=1 it proves exact PNE existence. For r=0 all strategy resources are absent and all costs are zero.

An equivalent interface is that **every profile in the full pure product space** has at most r simultaneous users on each resource. Equivalence is exact: for a fixed resource e, each potential user can independently select a strategy containing e, so some profile simultaneously realizes every member of U_e. Thus max_s n_e(s)=|U_e|. The potential-user version is preferable for compositional gadgets because it is immediate from incidence lists and cannot hide missing states.

## Consequence for layered gadget construction

Take any finite number of base gadgets, with arbitrary overlapping player sets, coefficients, polynomial degrees, weights, and resource-disjoint copies. If every resource belongs to the possible strategies of at most b players, the entire composed game has a b-PNE. In particular attaching or overlapping copies of the three-player six-resource gadget cannot yield a superconstant nonexistence factor as long as every resource support stays at most three. An attempted growing lower bound must introduce at least one resource with growing possible occupancy; merely increasing the number of gadgets or players does not suffice.

This is a necessary condition only. Growing support alone does not supply a sink-free improvement orientation or establish any lower bound.

## Literature import and novelty boundary

Primary source inspected on 2026-10-14: Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann, *Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*, arXiv:2002.07466v3, §6, Theorem 4 and equations (17)–(18), https://arxiv.org/html/2002.07466v3#S6. Their theorem gives n-PNE for arbitrary nonnegative nondecreasing costs using the same unweighted social-cost potential and bounds each other player's cost increase by the deviator's new cost. The proof here sums increases per added resource and replaces n by the occupancy bound r. This is an elementary refinement; no claim that it is unpublished or novel has been verified. The import matches the unweighted player-cost convention in WC-TARGET v1.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
