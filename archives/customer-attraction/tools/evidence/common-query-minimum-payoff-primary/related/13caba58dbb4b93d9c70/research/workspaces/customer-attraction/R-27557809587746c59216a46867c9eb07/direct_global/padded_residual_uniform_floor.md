# An all-history four-payoff floor for the padded residual family

This is an analytic, family-specific lemma. It does not resolve Q-CAG-HALF and does not establish a particular SPE path for arbitrary family size. The parent researcher independently reconstructed its induction and found no defect; external review and novelty are not certified.

For any integer k>=0 let m=k+2. The common core topics A,B,T,D,E have unit-client incidence multiplicities

| Interest set | Multiplicity |
| --- | ---: |
| {A,D} | 2 |
| {A,E} | 2 |
| {B} | 3 |
| {T} | 3 |
| {B,D,E} | 2 |
| {T,D,E} | 2 |

Add k topics P0,...,P{k-1}, each containing four private unit clients and disjoint from all other topics. All providers have unit weight, all client values are one, repeated choices are legal, and every ordered history has its own prescribed continuation.

**Lemma.** At every legal ordered decision history in this m-provider instance, the current provider's final utility in every complete-history pure SPE continuation is at least four.

Prove this by backward induction on remaining providers, simultaneously for all histories and all SPE continuations. A restriction of the fixed full SPE to any deviating child history is again an SPE, so the induction applies on genuine off-path branches.

Suppose some Pj has never been selected. The current provider can deviate to Pj. If no later provider selects Pj, this deviator obtains exactly four. If any later provider selects Pj, the two providers have identical topic sets and therefore equal final utilities on that same branch. That follower obtains at least four by induction, so the deviator does too. Current optimality proves the required floor. This handles every prefix with an unused P, independent of its other action counts.

It remains to consider a prefix where all k padding topics have appeared. Its length t is at least k, while t<=m-1=k+1, so at most two providers remain.

If two remain, t=k and each padding topic has appeared exactly once; no core action has appeared. The current provider can choose B. The final provider's best core replies are T,D,E, all with utility five; its occupied-padding alternatives give at most two. Against T the B chooser obtains five, and against D or E it obtains four. Thus this genuine deviation guarantees four against every final best reply, including arbitrary ties.

If one remains, at most one earlier action was a core action: the k distinct padding topics already use k of the k+1 earlier positions. Earlier padding choices leave core utilities unchanged. The following exact table gives the last provider's maximum core utility:

| Earlier core action | none | A | B | T | D | E |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Maximum core query utility | 6 | 5 | 5 | 5 | 4 | 4 |

Each entry follows directly by dividing the six incidence blocks by their loads after one new action. In particular every entry is at least four. Final optimality proves the base case and completes the induction.

The proof also covers k=0: there are no padding topics and only the two terminal cases occur. No ordered histories are merged and no tie rule is imposed.

Summing the lemma along any actual root SPE gives W>=4m for this family. Its optimal m-topic coverage is 4m+2: two core topics cover at most ten clients and leave room for all k padding topics, while three or more core topics cover at most fourteen and leave room for at most k-1 padding topics. The construction B,T plus all padding topics attains ten plus 4k. Its total union is 4m+6. The inequality W>=4m does not by itself certify the particular path P0,...,P{k-1},A,B. For that path this workspace supplies only the independently checked finite m=6 complete-SPE DAG in `padded_residual_m6_dag.json`.
