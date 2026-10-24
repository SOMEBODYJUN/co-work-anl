# General proof attempt: optimal-tuple interaction cannot be discarded

This is a derivation and self-attack record, not a proof of Q-CAG-HALF. All inputs have finite unit clients, common finite nonempty catalogue, unit providers, and arbitrary full ordered-history pure SPE. No fixed-size or restricted-catalogue positive project is claimed.

## 1. Actual insertion price and true deviations

Fix a full SPE with actual terminal profile z, coverage U, client loads c_x, welfare W, and actual profits u_i. Write

\[
 e(T)=\sum_{x\in T}\frac1{1+c_x},\qquad
 G=\sum_{x\in U}\frac1{1+c_x}.
\]

At actual position i, force T and then follow the same original full strategy at every successor. Let d_i(T) be the forced player's terminal profit. The only direct IC comparison used here is

\[
0\le d_i(T)\le u_i,\qquad \sum_i u_i=W.
\]

There is no frozen-successor interpretation of d_i(T).

For any m-topic comparison tuple (T_1,...,T_m), with union C, the elementary clientwise inequality gives

\[
 |C|\le W-G+\sum_{j=1}^m e(T_j).
\]

Consequently the root's current H4 candidate is sufficient: for some OPT-attaining tuple and permutation pi,

\[
\sum_i d_i(T_{\pi(i)})\ge\sum_j e(T_j)-G.
\]

Indeed its left side is at most W by actual-path IC. This deduction is only the announced sufficiency of H4; it does not prove H4.

## 2. Exact obstruction to a query-by-query proof

A tempting independent-query lemma would be

\[
\sum_i d_i(T)\ge m e(T)-G\quad\text{for every legal }T.\tag{P}
\]

If (P) held, averaging it over the m comparison topics would give

\[
\frac1m\sum_{i,j}d_i(T_j)\ge\sum_j e(T_j)-G.
\]

The average over all permutations of the assignment payoff is its left side, so a permutation meeting H4 would exist. This is a legitimate sufficient argument, including repeated comparison topics.

But (P) implies the actual-load endpoint budget

\[
m e(T)\le W+G
\]

for every T, because every d_i(T) is at most u_i. Thus **whenever a complete SPE violates that endpoint budget, (P) necessarily fails on the same query**. True successors do not repair this independent-query version: their summed payoffs already have the ceiling W. Root reported a latest endpoint counterexample; that source was not independently reconstructed here, so this note does not certify its numbers. The logical implication itself is exact and does not depend on that report.

This identifies a real proof obligation rather than a general impossibility claim: H4 must use the optimal tuple jointly, its assignment structure, or some other credit that does not demand (P) for every individual query.

## 3. Independently checked old counterexample to the stronger insertion shortcut

The shortcut max_T e(T)<=W/m is already false in the existing complete two-player residual certificate, independently of the reported newer endpoint example. The actual profile is (A,B), W=9, and the five clients of T are completely uncovered. Hence e(T)=5 and m e(T)=10>9. The true forced profits for T are d_1(T)=4 and d_2(T)=5, as tabulated in `research/current/customer_attraction/continuation_lemmas.md`.

This is an exact reuse of that old certificate, not a new instance or a counterexample to H4 or half coverage. It also illustrates why a full-load insertion query still retains the old residual obstruction.

## 4. A valid optimal-tuple replacement constraint

Let (T_1,...,T_m) attain OPT_m, C its union, and t_x the number of these labelled slots containing x. Let B_1,...,B_k be any k legal replacement topics, 0<=k<=m, and B their union. Then

\[
 |B\setminus C|
 \le
 \sum_{x\in C\setminus B}
 \frac{\binom{m-t_x}{k-t_x}}{\binom mk},\tag{E}
\]

where a summand is zero for t_x>k.

Proof. For each k-element labelled slot subset J, replace precisely those optimal slots by B_1,...,B_k. Optimality implies

\[
 |B\setminus C|\le
 \left|C\setminus\left(B\cup\bigcup_{j\notin J}T_j\right)\right|.
\]

Average over uniform J. A client x in C\B is lost precisely when all its t_x labelled covering slots lie in J; its probability is the binomial ratio in (E). This proves the stated all-input relation.

For k=1, (E) becomes

\[
m|B_1\setminus C|\le
|\{x\in C\setminus B_1:t_x=1\}|.
\]

For k=m, it reduces to the familiar welfare comparison |B\C|<=|C\B|. Neither endpoint assumes distinct comparison topics.

This is not claimed novel. Root identified existing owner-indexed/Bernoulli subset exchange in `owner_hybrid_transport.md` and a Boss20 clean audit as the mechanism to compare before reusing it. This fixed-replacement formula retains the entire optimal multiplicity spectrum, but no extra SPE strength follows merely from writing it.

## 5. Unclosed connection, stated exactly

At each forced (i,T_j) branch, the tail topics are legal and therefore their union satisfies (E), with k=m-i. The inequality controls their clients outside the chosen optimal union C. It does not control how the tail redistributes clients inside C, and it supplies no inequality comparing those off-path tail profits to the actual profits u_{i+1},...,u_m. In particular, it is invalid to replace a tail profit in that forced branch by its actual-path counterpart.

A usable continuation would need to combine those replacement inequalities with actual IC rows at the forced branch's later ordered histories and then cancel all new off-path profit terms. No such cancellation was established here. The independently derived replacement constraint therefore remains an unused elementary tool, not a positive step to the general half theorem.

## 6. Self-checks and excluded claims

- The early/late payoff monotonicity route was discarded; full-history ties invalidate it as recorded in the shared failure map.
- The stronger omission bound |C\U|<=W was discarded after root pointed to the known failure; it is not used in any derivation here.
- Full histories remain separate throughout. A count-vector representation is not used to equate chosen continuations.
- The assignment average in Section 2 is valid even for repeated labels, but its prerequisite (P) is the excessive step.
- No finite absence of a counterexample is invoked. There is no new SPE counterexample, no universal H4 proof, and no proof of Q-CAG-HALF in this note.
