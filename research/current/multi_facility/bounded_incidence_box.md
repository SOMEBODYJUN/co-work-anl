# SC-K-INCIDENCE-BOX-DP: exact boxed equilibrium on sparse incidence

Version 1, 2026-10-04. This reconstructs an algorithmic claim whose earlier local checkpoint was not present in the remote repository. The mathematical proof below, rather than that missing checkpoint, is the evidence for this version. It uses a standard fixed-treewidth decomposition algorithm [Bodlaender, *SIAM J. Comput.* 25 (1996), 1305–1317, DOI 10.1137/S0097539793251219]; that imported algorithm is not a new contribution. No external review or canonical software implementation is recorded.

## Exact objects and statement

Use MF-MODEL with explicit positive binary rational client weights, a common finite site catalog and explicitly listed `k>=2` labeled facilities. Run SC-K-GREEDY-BUDGET on a positive-reach input, obtaining occupied sites `O`, multiplicities `q_s>=1`, a last positive insertion score `gamma`, and the original client-to-site assignment. A client with just one occupied option is fixed there. Also fix each client with `w_i>=gamma` at its original greedy site. Let `I*` be the remaining clients, all of weight `<gamma` and with at least two occupied options. Let `B` be the bipartite **individual-client incidence graph** on `I*` and `O`, with an edge `is` exactly when `s` is an occupied option of `i`. Include isolated occupied sites. Let `d` bound the maximum degree on **both** sides of `B`, counting clients individually, and let `tau` bound its treewidth.

**SC-K-INCIDENCE-BOX-DP.** For any fixed nonnegative integers `tau` and `d`, there is an input-bit-polynomial algorithm that decides whether some assignment of every client in `I*` to one of its occupied sites makes the resulting site-pure, within-site independent-uniform profile an exact customer NE and satisfies all full greedy boxes

\[
                 q_s\gamma\le W_s\le(q_s+1)\gamma\qquad(s\in O).       \tag{B}
\]

If so, it constructs one. It also works with a supplied width-`tau` tree decomposition. The runtime has a constant depending on `tau,d`, and may be exponential in those parameters; fixing only treewidth while allowing unbounded individual-client incidence degree is **not** covered. The algorithm is an exact feasibility test on arbitrary inputs of this sparse class; it does not assert that the answer is always yes.

**SC-K-HEIGHT-TWO-INCIDENCE-2.** If, in addition, every client in `I*` has exactly two occupied options and the graph directed from the earlier-opened to the later-opened site has longest directed path at most two edges, then the decision above always returns yes by SC-K-HEIGHT-TWO-BOX-EXISTS. The resulting profile, followed by SC-K-GREEDY-BOX-TO-2, gives an input-bit-polynomial construction of a labeled layout and a **complete exact customer-equilibrium continuation** in which no unilateral facility deviation gains more than factor two. Both the depth and `tau,d` hypotheses are simultaneous; bounded treewidth alone gives neither this existence assertion nor this runtime.

Zero-reach inputs have no served client and admit the trivial zero-payoff continuation; the theorem above focuses on positive reach. The conclusion concerns this exact site-pure/within-site-uniform on-path profile and pure off-path continuations. It says nothing about the difficulty of finding arbitrary independently mixed equilibria across occupied sites.

## Local constraint formulation

For each site `s`, let `F_s` be the total weight of clients fixed there and `D_s=N_B(s)` its individually named movable clients. Define a site variable `X_s` with domain all subsets of `D_s`, at most `2^d` states. A state has exact rational load

\[
                 W_s(X_s)=F_s+\sum_{i\in X_s}w_i.                       \tag{1}
\]

Discard states violating (B), a unary constraint. For every movable client `i`, impose one constraint on the site variables indexed by its full occupied option set `N_B(i)`: exactly one of their subsets contains `i`, say `X_s`, and, for every `t\in N_B(i)\setminus\{s\}`,

\[
             q_t\bigl(W_s(X_s)-w_i\bigr)\le q_sW_t(X_t).                \tag{2}
\]

The conditional cost of choosing an individual facility at `s` is `w_i+(W_s-w_i)/q_s`; the alternative at `t` is `w_i+W_t/q_t`. Thus (2) is exactly its best-response condition, including self-weight subtraction. There are no constraints against an unoccupied site on path. A fixed singleton-option client has no alternative. For a fixed heavy client `i` at `s`, (B) and `w_i>=gamma` imply

\[
 (W_s-w_i)/q_s\le ((q_s+1)\gamma-\gamma)/q_s=\gamma
 \le W_t/q_t
\]

for every occupied alternative `t`; hence it is stable in every feasible state. Consequently the local constraints are equivalent in both directions to a boxed site-pure/within-site-uniform exact customer NE with these fixed clients. In particular the solver cannot return a state that is boxed but has a profitable cross-multiplicity move.

## Width conversion and dynamic program

Take a width-`tau` tree decomposition of `B`. In each bag replace every client vertex `i` by **all** sites `N_B(i)` and retain its original site vertices. Each new bag has at most `d(tau+1)` site vertices (or at most `(tau+1)max(1,d)` if empty cases are included). Every scope `N_B(i)` lies in a new bag: use any original bag containing `i`. Each site `s` has connected new occurrences: its old bag subtree intersects the old subtree of every adjacent `i` in a bag containing their edge, and the latter subtree is precisely the extra occurrence set contributed by `i`. Thus these bags give a valid decomposition of the site primal graph of width at most `d(tau+1)-1`.

Assign each unary box and each client constraint to one bag containing its scope. Standard bottom-up finite-domain tree-decomposition DP stores compatible values of `X_s` on the current bag; forget a variable only after all assigned constraints involving it have been evaluated. The state count per bag is at most

\[
             (2^d)^{d(tau+1)}=2^{d^2(tau+1)}.                         \tag{3}
\]

Introduce/forget/join operations and witness backtracking require a polynomial number of rational additions and comparisons per state, for fixed `d,tau`. Each load is a sum of at most `d` variable weights plus the fixed-client sum; even without the degree bound, addition of explicitly represented binary rationals and multiplication by `q_s<=k` have polynomial encoding length. The total arithmetic bit complexity is polynomial in the input length for fixed `d,tau`. Bodlaender's fixed-width algorithm supplies the decomposition, or a supplied decomposition can be checked directly. We assert no uniform polynomial dependence on varying `d,tau`.

The initial greedy assignment is boxed, but it need not satisfy (2). The DP returns `no` when these exact constraints have no solution; a failed search has no implication about the all-input factor-two target. Under the directed depth-two assumption, the independent existence proof in `height_two_box.md` supplies a solution, so this DP is a total constructor there. Its output then meets the explicit input contract of `SC-K-GREEDY-BOX-TO-2`, including singleton-source reset and all labeled deviation layouts.

## Boundaries and remaining obligations

- Counting only adjacency between *sites* does not bound domains: many separately weighted clients can share one site pair. The degree in this claim counts the actual client vertices at each site.
- A forest can have arbitrarily high degree, so treewidth `1` without bounded degree does not yield the bound (3).
- Arbitrary sparse incidence does not inherit the shallow directed graph existence theorem. In that case `no` means only that this specific fixed-heavy boxed selector has no witness.
- No general all-input bit-polynomial factor-two algorithm, new complexity lower bound, or optimal factor improvement follows. The next proof obligation is a selector or different off-path interface without the bounded-degree and shallow-depth restrictions.
