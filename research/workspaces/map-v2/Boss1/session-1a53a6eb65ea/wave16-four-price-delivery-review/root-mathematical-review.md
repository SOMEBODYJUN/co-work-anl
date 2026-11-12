# Boss1 mathematical review: four-player frozen terminal-price policy

The reviewed core is the single fixed six-customer, four-player, six-label input with SHA256 `14e813bb26898416354020f4a2b620dd661208353c4798712cfb8bfbc8da83da`. This note does not interpret the historical floating score or certify a price cone.

## Baseline and the exact exceptional history

Write U for the four customers interested in {0,1,2,3}, C for the customer interested in {0,1,3,4,5}, and D for the customer interested only in 5. Labels 0,1,3 all cover A=U∪C. Label 2 covers U, label 4 covers C, and label 5 covers C∪D. The pure A query against three A choices has t=5/4 and deviations D_j=(5/4,5/4,1,5/4,1/4,5/4). The pure-saddle lemma therefore supplies a complete-history constant-A SPE. Replacing an A label by an A alias at an arbitrary history preserves this baseline proof because all downstream coverage sets remain A; it does not identify distinct ordered histories.

The frozen policy has exactly one non-A action, σ(2,1,2)=5. Define τ by changing only this action to 0. The complete frozen action-table reading, rather than its terminal counts, establishes this comparison.

At h=(2,1,2), the U,C,D background loads are 3,1,0. Both A and label 5 yield 3/2; label 2 yields 1 and label 4 yields 1/2. Thus changing the prescribed action to 5 preserves all six last-player inequalities, with equal prescribed utility.

At h=(2,1), σ prescribes 0 and the prescribed completion stays in A, so its utility is 4/4+1/3=4/3. Deviation 2 now reaches the exceptional leaf (2,1,2,5) and yields 4/3. Under τ that same deviation yielded 4/4=1. This single nonself slack decreases from 1/3 to 0 and remains valid.

The proper earlier ancestors are h=(2) and the root. At h=(2), forcing 1 reaches (2,1), whose prescribed action is 0, not 2; hence it does not reach the exceptional node. The root's forced 2 continuation is likewise (2,1,0,3). All earlier prescribed and one-step-deviation continuations therefore agree with τ. Histories outside this ancestor chain cannot reach h=(2,1,2). This pays the entire propagation obligation; merely knowing a different constant-A SPE exists would not have sufficed.

## Welfare, optimum, and evidence responsibility

The actual frozen leaf is (3,0,1,1), so each player receives 5/4 and W=5. Label 5 and any of 0/1/3 cover all six customers, so OPT_4=6, allowing repetition in the four slots. Thus W−OPT_4/2=2. The 259 complete ordered nodes give 1554 self-included and 1295 nonself comparisons; self-comparisons ensure minimum slack zero once all inequalities are paid.

Boss1 read the complete core page and the full 34-line definition-level Fraction auditor. That auditor follows the original policy after every forced action and checks the top-level and certificate action maps. The worker independently reads the entire frozen policy and mature comparison table through reversible views. Neither this review nor the new relationship requires rerunning that scientific audit. The relationship must keep the exact frozen policy distinct from a price optimization claim and from the general constant-policy existence result.
