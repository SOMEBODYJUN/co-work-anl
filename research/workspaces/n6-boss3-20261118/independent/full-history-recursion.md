# Exact full-history continuation-set recursion

## Model and scope

Exactly six equal-weight providers, unit clients, a finite nonempty common catalogue of labels, arbitrary overlaps, duplicate labels and arbitrary history-dependent tie choices. Mathematical input is only `packet-obstacle.json` for this RUN. This is an independently derived finite-instance characterization and a general lower bound; neither result proves the desired half-coverage theorem.

## 1. Continuation-set lemma

Fix a finite instance. For a history h of length d, let E(h) be the set of terminal action-count vectors attainable by some pure SPE of the subgame rooted at h (only the remaining 6-d players are required to optimize in this subgame). Let q(h) be the vector counting each catalogue label in h. For an integer count vector y of total 6 and a catalogue label a with y_a>0, define

    U_a(y) = sum_{x in cov(a)} 1 / sum_{b: x in cov(b)} y_b.

Then E(h) depends only on q(h), even though an individual SPE need not depend only on counts. Write E(q) for this attainable set. At total count 6, E(q)={q}. For total count d<6 define

    L_a(q) = min_{y in E(q+e_a)} U_a(y),
    L(q) = max_a L_a(q).

The exact recursion is

    E(q) = union_a { y in E(q+e_a) : U_a(y) >= L(q) }.

All sets are nonempty and finite.

### Proof

Use downward induction on remaining players. Terminal nodes have the claimed singleton set. Suppose the assertion holds at all children. In a given subgame SPE the current player chooses some a and the terminal count vector is y in E(q+e_a). For every alternative b, the same strategy specifies a genuine SPE in the separate child subgame (h,b); its terminal vector z_b lies in E(q+e_b). Optimality gives U_a(y)>=U_b(z_b)>=L_b(q). Therefore U_a(y)>=L(q).

Conversely, take a and y in E(q+e_a) with U_a(y)>=L(q). In the chosen child, select a subgame SPE attaining y. For every alternative b different from a, choose an attaining minimizer z_b for L_b(q), and select a subgame SPE attaining z_b. These child subtrees are disjoint histories, so these independently chosen strategies combine into one strategy on the whole rooted subtree. Choose a at the root. Its utility is at least every alternative's prescribed genuine continuation utility, and all child strategies already satisfy SPE at every descendant history. This is a subgame SPE attaining y.

The recurrence only uses q and the catalogue, proving count-invariance of the attainable sets by induction. This does NOT assert that the given strategy is Markovian, nor that the independent child continuation choices can be frozen across different histories. Duplicate coverage labels remain separate action coordinates and separate child subtrees. Thus the proof preserves arbitrary history-dependent ties and complete off-path optimality.

### Practical interpretation

A terminal path alone is not a certificate. The exact test additionally requires recursively feasible punishment continuations at every alternative action, which is precisely the minimum L_a(q). When a state can be reached by distinct ordered histories, the recurrence reuses its attainable set only; different copies may choose different attainable elements.

For up to six catalogue labels, the optimum six-set coverage is exactly the union of all catalogue sets, so a computed ratio is directly comparable with the target. For a larger catalogue, the true OPT_6 must be computed separately.

## 2. A universally valid residual-cover bound

Fix any full pure SPE with welfare W, realized payoffs u_1,...,u_6, and realized union C. Let T_1,...,T_6 be an optimum tuple and R=OPT_6-W (if the optimum has clients outside C, their number is at least R). Define M=max_j |T_j minus C|. At player i's on-path history, deviating to any T_j obtains at least |T_j minus C|/(7-i): none of those clients are covered in the prefix, and at most 6-i later providers can share them. This bound applies to the true continuation under the same strategy and uses no assumption on its behavior. Hence

    u_i >= M/(7-i),
    W = sum_i u_i >= H_6 M = (49/20) M,
    OPT_6 <= W + 6M <= (169/49) W.

Equivalently 169 W >= 49 OPT_6. This remains valid in the zero-coverage case without division. It falls well short of 2W>=OPT_6; its purpose is to locate the weakness of deviation guarantees that ignore successor incentives.

## 3. Exact finite computation implementation

`exact_spe_search.cpp` implements the lemma for exactly six players and A<=8 catalogue labels using all nonempty membership masks as client atoms. Integer weights represent that many distinct unit clients. Each payoff is multiplied by 60, so all comparisons are exact integers (all loads are between 1 and 6). Every state of total count 0,...,6 is built, and every feasible terminal count vector is retained. No sampling occurs inside the SPE test; sampling changes only the input instances searched.

The current driver searches sparse integer atom-weight instances with A=6; this is a counterexample search, not a proof or an exhaustive search over all catalogues. Its output is an exact attainable root outcome but does not yet export all child choices as a stand-alone strategy certificate. The mathematical recursion proves such a certificate can be reconstructed by selecting argmins at every alternative child.

## Remaining obligation

No half-coverage proof or original-model counterexample is established here. Search for low attainable ratios and inspect whether the exact recursion exposes a strengthening of the crude outside-cover guarantee. For any claimed counterexample, export a full recursively checked strategy certificate, compute exact OPT_6, and verify 2W<OPT_6 with integer arithmetic.
