# A common-query regret bridge fails: six providers, nine topics

Research target: **Q-CAG-HALF**, unchanged and **OPEN**. This note disproves only the auxiliary assertion

\[
F(T):=\sum_{i=1}^m u_i(T,s_{-i})\le W(s)+\min_i u_i(s)
\tag{CQ-min}
\]

for every topic T and every full ordered-history pure SPE s. The deviations in F freeze all other actual terminal actions; they are not the genuine sequential deviations. The witness below has W=25 and OPT_6=26, so it satisfies the main half-coverage inequality comfortably.

## Why this was a sufficient bridge

For actual customer loads c_x and actual covered set C, a direct customer-wise calculation gives

\[
F(T)=m|T\setminus C|+\sum_{x\in T\cap C}\frac{m+1}{c_x+1}.
\tag{1}
\]

Indeed, if c_x>0, the c_x incumbent coverers each face load c_x after switching to T, while the other m-c_x providers face c_x+1. Their total is 1+(m-c_x)/(c_x+1)=(m+1)/(c_x+1). If c_x=0, every one of the m queries earns one.

Put alpha=(m-1)/m,

\[
g(T)=\sum_{x\in T}\frac1{1+\alpha c_x},\quad M=\max_T g(T),\quad
G_C=\sum_{x\in C}\frac1{1+\alpha c_x}.
\]

Jensen's inequality applied to the m frozen opponent loads c_x-1_{x\in S_i} gives F(T)>=m g(T). Also min_i u_i<=W/m<=G_C, because c_x<=m. Therefore (CQ-min) would imply the still-separate refined fractional bridge mM<=W+G_C. The converse does not hold, and this counterexample does not disprove that refined bridge.

## Exact instance and numerical violation

There are nine common topics A,B,T,D,E,P0,P1,P2,P3. The following rows specify different unit clients by the complete set of topics that cover them.

| Client interest set | Multiplicity |
| --- | ---: |
| {A,D} | 2 |
| {A,E} | 2 |
| {B} | 3 |
| {T} | 3 |
| {B,D,E} | 2 |
| {T,D,E} | 2 |
| {Pj}, for each j=0,1,2,3 | 4 each |

All provider weights and client values are one; these multiplicities only compress 30 distinct unit clients. The first six rows are the established 14-client residual-counterexample core. The P topics are disjoint from that core and one another.

The complete pure SPE certified below has ordered root path

\[
(P0,P1,P2,P3,A,B),\qquad u=(4,4,4,4,4,5),\qquad W=25.
\]

T's five clients are all missed. Equation (1) consequently gives

\[
F(T)=6\cdot5=30>25+4=29.
\]

Thus (CQ-min) fails by exactly one. OPT_6=26: four P topics plus B,T cover 26 clients. For an upper bound, if at most two core topics are used, they cover at most 10 clients and at most four P topics contribute 16. If at least three core topics are used, at most three P topics remain, and the entire core contains only 14 clients. Both cases give at most 26. This OPT calculation concerns six actions, not the 30-client union of all nine topics.

All actual covered clients have load one. Hence G_C=25/(1+5/6)=150/11. The missed topic T has g(T)=5; every other topic has smaller g value, so M=5. The refined fractional bridge has positive slack

\[
W+G_C-6M=95/11>0.
\]

A legal static oblivious opponent background (P0,P1,P2,P3,D) caps every query at four, so v_6<=4 and W-6v_6>=1. This witness therefore does not refute the true aggregate security bridge either.

## Complete-history SPE evidence

`padded_residual_m6_dag.json` is a compact complete-SPE certificate, not an on-path transcript. It contains 5,440 nodes. Each node records a prefix count vector k and a desired full terminal count vector c. A nonterminal node records a selected action a and a child node for **every** one of the nine possible next actions. Different nodes with the same k can carry different c, preserving arbitrary ordered-history ties.

The local certificate contract is:

1. Every child's prefix counts are k+e_b for its action b.
2. The chosen child's target is c.
3. For every b, the payoff of a in c is at least the payoff of b in that child's target.
4. Terminal nodes satisfy k=c.

Induction on remaining depth proves that following these transitions unfolds to a strategy at every ordered history, with the advertised terminal at each node, and all local sequential deviation inequalities. Nodes merge only identical count-and-target continuation problems; they do not force identical continuations for equal counts with different targets.

The builder `padded_residual_dag.py` uses the canonical exact all-outcome recursion to discover and construct the certificate. This is separate from verification. The independent standard-library audit

`../security_global/audit_padded_residual_dag.py`

imports neither that builder nor the canonical model/solver. It expands the 30 clients, checks the DAG state/target/action/edge contract, recomputes all 21,933 action comparisons with Fraction arithmetic, counts the unfolded ordered histories, and independently enumerates OPT. Its report is

`../security_global/padded_residual_m6_independent_audit.json`.

Run the builder from the repository root with:

```sh
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_dag.py 6
```

Run the independent audit from the repository root with:

```sh
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/audit_padded_residual_dag.py research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_m6_dag.json
```
 The finite certificate and definition-level audit prove the stated finite bridge counterexample. They do not establish a general family of target SPEs or resolve Q-CAG-HALF.

## A separate analytic floor for the padded family

For k>=0, use the same core and k disjoint four-client P topics, with m=k+2 providers. At every legal history, every current provider in every complete pure SPE continuation receives at least four.

Proof: induct on remaining players, simultaneously over all histories. If an unused P exists, deviate to it. With no later copy its payoff is four; with a later copy its payoff equals that follower's payoff, at least four by induction. If no unused P exists, the prefix length is at least k, so at most two players remain. With two remaining, the prefix consists of the k distinct P topics exactly once. Choosing B guarantees at least four against every final best reply: in the residual core, the final best replies after B are T,D,E, giving the B chooser respectively five,four,four; occupied P topics offer the last provider at most two. With one remaining, at most one earlier core action exists. The core best reply is at least four after each possible earlier core action (and is six if none exists), while earlier P choices do not affect core utilities. SPE optimality completes the induction.

This floor is a universal theorem for this explicitly specified padded family, not for arbitrary catalogs. It does not by itself prove that the proposed P0,...,P{k-1},A,B root path is an SPE for every k. Only the finite m=6 path above is promoted here, after independent audit.
