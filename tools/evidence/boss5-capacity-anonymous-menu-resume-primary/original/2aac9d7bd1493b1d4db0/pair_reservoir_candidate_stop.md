# Pair-reservoir target attack: a general-size credible-floor obstruction

2026-10-24. Personal checkpoint for the original CAG-MODEL and Q-CAG-HALF.
The target remains **OPEN**. This note closes one already proposed all-size
counterexample source, rather than proving half or starting a structural
positive-result project. No finite search is used as evidence for a universal
statement. No independent review has yet been claimed.

## 1. Exact candidate being tested

The source is Section 4 of
`R-3bc48d936f044f12b0fa743482ff5eb0/credible/target_attack_checkpoint.md`.
For every integer k>=4, there are m=k+1 players. Distinct customer blocks are:

* X_i of size 2 and Q_i of size 3, for i=1,...,k;
* E_0 and E_1, each of size 4.

Put A_i=X_i union Q_i and D=E_0 union E_1. The exact common catalog is

    C_i=X_i,
    H_i^e=A_i union E_e,  e=0,1,
    P_ij=A_i union A_j,  i<j,
    D.

The proposed old target path is C_1,...,C_k,D. Its last action is a genuine
best reply: it gives 8; an H gives 1+3+4=8, a P gives 2(1+3)=8, and a C
gives 1. Its welfare is W=2k+8. At most ceil(k/2) pair actions cover all
A_i, and one D action covers the reservoir; hence OPT_m=5k+8. The old
half gap is therefore

    OPT_m-2W=k-8.

For the heterogeneous prefix insurer, define ell_i(T), M_i=max_T ell_i(T),
and delta_i=(M_i-2)_+ at the normal prefix C_1,...,C_(i-1), for i<=k.
The already proved insurer would need the strict inequality

    k-8 > 2 R + Delta,
    R=sum_(i=1)^k delta_i,  Delta=max_i delta_i.

The task here is to test that exact source, keeping genuine complete
continuation SPEs in ell_i. Assumed punishments are never substituted.

## 2. Fresh pairs force utility at least 8

Fix any normal prefix C_1,...,C_(i-1) and write n=k-i+2 for the number of
players still to act. Suppose k>=2n. Every complete pure SPE after this
normal prefix gives its current player a final payoff at least 8.

More strongly, consider any ordered history obtained from this normal
prefix by l<n arbitrary additional actions, not necessarily prescribed
actions of the SPE. Call a group A_j dirty if one of these l actions
intersects A_j. Every legal action dirties at most two groups, so at least
k-2l groups remain clean. Since k>=2n, there are at least two clean groups
at every such nonterminal history.

We prove backwards over the n-l players remaining that their current
player receives at least 8 in every complete pure SPE at every such
ordered history. At the final decision, take two clean groups a,b. Their
Q blocks have no background cover. Each X block has background at most
one, from the fixed normal prefix only. Thus choosing P_ab pays at least

    3+2/2 + 3+2/2 = 8.

There are no later actions in this base case.

For the induction step, force the current player to choose such a clean
P_ab. The child is an ordered history with l+1 added actions; every future
player has payoff at least 8 by the induction hypothesis, in every
complete SPE of that child and at all its deeper histories. No future
player can select any theme intersecting A_a or A_b:

* A pair theme meeting one of those groups has a final payoff at most
  5/2+5=15/2<8. In the already covered group, its Q contribution is at
  most 3/2 and its X contribution at most 2/2; the other group contributes
  at most its raw size 5. A pair meeting both groups has a smaller bound.
* An H theme meeting one has final payoff at most 5/2+4=13/2<8.
* A C theme has raw payoff at most 2.
* D does not intersect either group.

These are continuation-independent bounds: they use only the one fixed
coverer just supplied by P_ab, and can only decrease if more providers
cover these clients. Consequently every genuine continuation SPE avoids
both A_a and A_b completely. The forced current player therefore retains
the same payoff at least 8 from P_ab. Its actual SPE choice must give at
least that much. This completes the simultaneous induction for all
ordered histories, including every repeated or off-path action.

The argument uses the future players' actual optimality, rather than an
assigned low final payoff. It remains valid when the normal prefix has
covered some X blocks once, because clean means clean relative to the
additional actions; the normal X background is explicitly included in
the lower bound 8.

## 3. Apply the bound to true credible floors

At a normal node i with k>=2(k-i+2), force any clean P_ab. The preceding
argument shows that **every** complete continuation SPE gives this fixed
deviator at least 8. Thus ell_i(P_ab)>=8 and M_i>=8. In fact, the value is
exactly the static fresh-pair value 8, 9, or 10 depending on which X blocks
belong to the fixed normal prefix; the lower bound alone is sufficient.

The condition holds at every

    ceil((k+4)/2) <= i <= k.

There are floor(k/2)-1 such positions. Each has delta_i>=6, so

    R >= 6(floor(k/2)-1),
    Delta >= 6,
    2R+Delta >= 12(floor(k/2)-1)+6.

For even k this last bound is 6k-6, and for odd k it is 6k-12. Both exceed
k-8 for every k>=4. Therefore this all-k family cannot meet the strict
heterogeneous repair threshold at **any** size. Increasing k cannot rescue
this source.

This statement does not rule out other source paths in the same catalog,
other common catalogs, arbitrary nonstationary threats, or the repair
theorem itself. It supplies no conclusion about the truth of general
half. Its purpose is to stop this particular proposed positive-gap source
before spending effort on supposed low punishments that its true children
cannot realize.

## 4. Consequence for the current attack

The attractive old gap k-8 was created by replacing size-5 A groups with
size-2 C groups on the target. Once the remaining horizon is short relative
to the number of groups, the full pair catalog supplies two clean groups
at every history. A future provider who actually touches a previously
chosen pair is then strictly below the clean option. There is a linear
number of large unavoidable credible defects, rather than a bounded
endgame defect.

At m=5, the same formula has k=4 and already gives one delta>=6, while the
old gap is -4. This is only the direct substitution of the all-size
candidate analysis, not a five-player project or a five-player half proof.

No further parameter sweeps of this pair-reservoir source are warranted.
The remaining constructive obligation is to find a genuinely different
common catalog with a bad old gap that survives its true credible floors,
or to construct the complete SPE directly.
