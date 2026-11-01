# Independent audit: stationary successor-source restriction fails

2026-10-24. **Audit passed for the precise restriction below.** This is a new interpretation of an already-existing legal eight-player full SPE; the input and strategy are not new. It is not a counterexample to freely mixed Mfull, a leader safety bound, or Q-CAG-HALF. The general half target remains OPEN.

## 1. Exact statement being audited

At a root with r>=2 remaining providers and zero old background, let Z(A) be the full r-slot outcome after forcing root action A and then following the original full strategy. Define

    K(T,A) = sum_(x in T) 1/[1+c_x(Z(A))],
    P(T|A) = (number of successor providers selecting T in Z(A))/(r-1).

The additional restriction asks whether one can always choose a column distribution Q satisfying both

    P Q = Q,       K Q <= u 1,

where u is the root's actual SPE utility. Stationarity is imposed on the source distribution for full-menu columns; the independent extra query is still evaluated against all r original players. This is a restriction on how Q is selected, rather than the original freely mixed Mfull conjecture.

## 2. Independent reconstruction and full-history verification

The only mathematical input read by the audit program is the original raw file

    research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json.

The source contains the unit-customer incidence list, eight topic labels, eight providers, and the full strategy DAG. I did not import the CAG model, solver, certificate verifier, old audit outputs, or the new menu discovery outputs. I did read the old schema/prose description to determine the certificate format.

The audit expands all 32 customers individually. It verifies that every reachable nonterminal DAG node has all eight legal action edges, every edge adds exactly one topic to the prefix count, and terminal depth is exactly eight. It reconstructs every node's actual continuation by following prescribed edges, independently of the stored `target`, and then checks that the reconstructed leaf equals that target. It checks every prescribed action's exact utility against all eight alternatives evaluated at their true reconstructed child continuations.

Results are 13,872 reachable DAG nodes, 6,435 terminal DAG nodes, 59,496 comparisons including self-action, and minimum SPE slack zero. Counting expanded path multiplicities through the DAG gives 2,396,745 ordered decision histories and 16,777,216 terminal histories. Thus the verification covers every ordered history; it does not silently impose a count-only selector on an arbitrary strategy.

The recovered actual path is

    (D0,A0,C0,D0,A1,A1,B1,C1)

with utilities

    (13/4,21/4,17/4,13/4,13/4,13/4,17/4,21/4).

Hence u=13/4 and W=32. The legal four-topic tuple (A0,D0,A1,D1), padded by repetitions to eight slots, covers all 32 customers, so OPT_8=32 as well.

## 3. Stationary distribution is unique and violates the cap

Write the per-block action order as (A,B,C,D). For any root action in block j, its seven successor providers have topic counts

    own block:   (1,0,1,1),
    other block: (2,1,1,0).

These counts were reconstructed from the actual paths, not taken from the claimed root-column table.

If Q has total block-0 mass x, stationarity of block mass requires

    x = (3/7)x + (4/7)(1-x),

so x=1/2. Individual coordinate stationarity now forces

    Q = (3/14,1/14,1/7,1/14) repeated in the two blocks.

This gives a direct uniqueness proof. Independently, exact rational row reduction returns rank(P-I)=7 and rank eight after adding normalization. The vector is nonnegative and normalized.

Using the independently rebuilt K, this unique stationary source gives

    KQ = (38/15,221/105,831/280,2773/840) repeated.

Its maximum is 2773/840, while u=13/4=2730/840. Therefore every stationary Q fails the cap, with exact gap

    2773/840 - 13/4 = 43/840 > 0.

Existence of a stationary source alone is therefore insufficient; in this example there is exactly one, and it has the wrong query cap.

## 4. Free Q succeeds, with a matching exact minimax certificate

Define a freely chosen column distribution by Q(C_j)=1/14 and Q(D_j)=3/7 for each block j, all other probabilities zero. The reconstructed matrix gives

    KQ = (577/210,67/35,851/280,851/280) repeated.

For the independent query distribution p(C_j)=2/7 and p(D_j)=3/14,

    p^T K = (443/140,443/140,851/280,851/280) repeated.

Thus primal and dual bounds match, proving the free-menu value is exactly

    Mfull = 851/280 < 13/4,

with slack 59/280. The free Q is not stationary: (PQ-Q) in each block is (3/14,1/14,1/14,-5/14). This is precisely why the stationary restriction and free-menu statement separate.

## 5. Relation to minimal-leader expansion

The companion `minimal_leader_failure.md` assumes a benchmark G_r(b) that is monotone under legal prefix embedding and chooses a least-r failure u<G_r(b)=t. Its proof then forces all branch followers to earn at least t>u and forbids a follower from copying the forced root action.

This witness is not such a minimal leader failure. Every forced-root branch has some follower earning exactly 13/4; the A, C and D root branches each contain one successor copying the root action. For instance, the actual D0 branch contains a later D0 player with the same 13/4 utility. Hence the lemma's necessary strict separation would fail for every t>13/4. Stationary menu cap has not been shown to satisfy the required prefix embedding, and stationarity restriction failure need not be a leader-benchmark failure.

There is also a direct feasible fractional background showing the stronger FF leader comparison is safe here. Take

    q = (6/35,0,11/70,6/35) repeated.

Its total mass is one. Against seven fractional opponent slots, reciprocal query values are

    (292/99,202/99,292/99,292/99) repeated,

so t_8(0)<=292/99<13/4. This is an explicit feasible cap, not a claim that q is the unique optimizer. The free full-menu certificate likewise gives true extra-one safety v_9(0)<=851/280<13/4.

The minimal-leader expansion therefore neither repairs the stationary restriction nor contradicts its counterexample. It explains why this witness cannot be repurposed as a minimal failure of the prefix-monotone leader interfaces.

## 6. Audit artifacts and scope

- `audit_stationary_source.py`: independent raw-DAG, unit-customer, Fraction audit.
- `stationary_source_independent_audit.json`: exact reconstructed matrices, all root branch payoffs, ranks, primal/dual certificates and source SHA256.

No claim was promoted and no git operation was performed. The audited conclusion rejects only the stationary successor-source restriction. Freely mixed Mfull and Q-CAG-HALF remain OPEN.

After completing the blind reconstruction, I read the new author's draft `menu/stationary_source_failure_and_free_source_interface.md`. Its stationary-restriction statement and failure match this audit. The later FQ equation is the direct identity obtained from xi=w-slack and epsilon=K-xi. Its customer numerator t'-t-a and the resulting integer sign conditions are algebraically correct. I did not treat that accounting identity as a proof of the remaining free-Q payment or expand this audit into a search for such a payment.
