# Uniform reserve obstruction: independent mathematical review

2026-10-23. Reviewed by the continuation_geometry branch, independently reconstructing the proof from the statement before reading the author draft. This is an internal mathematical review, not external peer review or a proof of Q-CAG-HALF.

Reviewed draft: `/workspace/scratch/827ce59ec8f3/counterexample_search/uniform_reserve_obstruction.md`.

## Verdict

The stated implication is correct for every k,t>=1, x,b>0, a,d>=0 and every complete ordered-history pure SPE satisfying the stated actual C-then-D path. The proof preserves all off-path tie choices. No finite computation is needed for the all-parameter implication.

## Independent reconstruction

Write H=b+d. At the actual last D_s node, B_is offers b+x/2 and A_i offers a+x/2, so necessarily d>=x/2 and H>=a+x/2.

Fix any history at which all X_i are already covered at least once and at least n reserves Z_r remain untouched for n remaining players. Every legal action has immediate payoff at most H, using the preceding two parameter inequalities. An action touching an already-used reserve has immediate payoff strictly below H, because its b contribution is at most b/2, while its X or V contribution is at most x/2 or d respectively. The strict gap uses b>0.

Induct on n, universally over ordered histories and their complete continuation SPEs. If the current player chooses any fresh D_r, at least n-1 fresh reserves remain. The induction hypothesis applies to that actual deviation subtree, says that its future players all receive H, and excludes actions touching the now-used reserve r. Thus the current player retains all of Z_r and V_r and receives H. Optimality and the universal immediate upper bound show the current player also receives H, and the strict upper bound excludes already-used reserves. This proves the author's stronger reserve lemma with no circular invocation.

Take the actual last C_i player and deviate to A_i. All X_j are then covered once and t fresh reserves remain for t players, so the lemma applies. If a>0, any subsequent A_i has immediate payoff at most (x+a)/2 < x/2+a <= H. A subsequent C_i has payoff at most x/2 < H. Neither is possible. If two or more later B_ir cover X_i, each such player's final X_i share is at most x/3, and its reserve contribution is at most b. Its payoff is therefore less than b+d=H, a contradiction. Hence the deviator receives at least a+x/2, compared with its actual C_i payoff x. This gives a<=x/2. If a=0 the conclusion is immediate.

The ratio follows from OPT=k(x+a)+t(b+d) and W=kx+t(b+d), since k a<=kx/2<=W/2.

## Checks on quantifiers and boundary cases

- An action touches at most one reserve, so the fresh-reserve count decreases by at most one at every child history. This is the state invariant needed for the induction.
- The proof uses the original SPE restricted to the actual deviation subtree; it never selects an unrelated favorable continuation and never equates same-count ordered histories.
- The floor H and the exclusion of previously used reserves are simultaneous induction claims. Their dependence is downward in the number of remaining players, not circular at the same horizon.
- The action-upper-bound argument works even if some Y_i or V_r were covered earlier: discarding their existing loads only increases the upper bound.
- a=0 can make A_i=C_i. The target implication is then automatic. Treating equal sets as one catalog action causes no problem. d=0 is ruled out by the necessary inequality d>=x/2 because x>0.
- The proof does not require the two within-segment orders to agree with label orders.
- The ratio is defined here because kx+t(b+d)>0. The main model's zero-client boundary is outside this positive-parameter family and is not being excluded from the main question.

## Reusable content and remaining general gap

The reserve lemma has a useful abstract form: if all actions have payoff at most H, used reserves have strict upper bound below H, one action can consume at most one reserve, and a fresh-reserve action yields H whenever its reserve is untouched thereafter, then n fresh reserves for n remaining players protect H in every complete SPE. This is a genuine horizon induction using a capacity state.

For general catalogs the capacity property fails: one action may simultaneously hit several fresh reserve blocks. Also there need not be a common H bounding every action while excluding used-reserve actions. Consequently the lemma cannot be imported into the unrestricted half-coverage problem without a new decomposition or charging argument.
