# Round 4: full ordered-tree policies and completion limitations

Personal research and independent review, not a claim that Q-CAG-HALF is solved.
All files in this subdirectory are owned by the credible-full-tree subagent;
parent handles checkpointing and any shared mathematical registration.

The most substantive result here is an **independent analytic review of the
weak iid auxiliary-bridge counterexample**, in `weak_iid_policy_review.md`.
It proves the supplied policy is a genuine pure SPE at every ordered history
for m>=2,K>=2, and independently reconstructs an explicit iid bridge failure
for every m=K>=53. The actual W=2m and OPT=2m+min(K,m-1), so the family's
inefficiency is below 3/2 and it does not refute half coverage. The review
includes parameter boundaries, root indifference, arbitrary repeated and
out-of-order off-path histories, all intermediate and terminal deviations,
and the precise iid minimax crossing argument. Its `.py` and `.json` contain
exact full-tree finite checks and exact rational checks of certificate constants.

## Direct full-tree search: narrow family, no counterexample

`late_reply_family.py` fixes all first m-2 players to A at every ordered history,
then generates a complete last-two backward-induction policy from a four-block
late-reply incidence family and six deterministic tie selectors. The resulting
full policy, including all off-path histories, is optimized in all 21 five-topic
comparison portfolios for m=5,p=7. The canonical exact cone is used only for the
selected best witness. Search uses count-state policies as a restricted subset;
it does not assume all pure SPE have that restriction.

`late2_m5p7_fixed.json` records 70 distinct policies, each with a nonzero
floating LP feasible region. The best selected witness has exact OPT/W=9/5,
with exact cone dual bound 9/5 for its selected comparison portfolio. Its full
2801-history policy is checked both by the canonical verifier and independent
literal deviations. This does not certify exact upper bounds for the other
69 policies and proves no universal theorem. The originally attempted seed
expression had a bitwise-precedence error and was corrected before the retained
run; only the corrected frozen result is kept.

## Pair-closure versus exact completion: small mechanism illustration

`pair_completion_gap.py/json` exhibit the legal unit-client catalog
A-only 2, A-intersection-T 2, T-only 4, B-only 5. The advertised non-equilibrium
path A,B has u_A=4,u_B=5,W=9 and H=11. B is a valid best reply after A, and
all nine retained-overlap two-query inequalities hold, with equality for T,B.
But B is the unique best reply after T and the earlier mover then earns6>4.
The only genuine two-player SPE ordered path is T,B, with welfare11.
Thus the necessary pair inequalities can hide a negative earlier-deviation
slack behind g(A,A)-g(A,Q); they are not exact SPE completion constraints.
This is a mechanism illustration, not a new general welfare result.

For an arbitrary fixed legal two-player prefix, f(T),g(T,Q) as in the pair
identity give BR(T)=argmax_Q[f(Q)-g(T,Q)]. Put
L(T)=min_(Q in BR(T))[f(T)-g(T,Q)]. Then the exact advertised-path completion
criterion is B in BR(A) and U(A,B)>=max_T L(T). Replies after distinct actions
can be selected independently, and this criterion applies independently at
each ordered prefix. It imposes no consistency between different histories
with equal counts. The script checks it against the exact solver on all nine
ordered paths of the small catalog.

## New unrestricted 557-row point: easy extra rows do not remove it

`mixed_pair_audit.py/json` check the exact 60-atom point frozen by the pricing
agent at `../round4_pricing/exact_primal_overlap1.json`, SHA-256
`11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825`.
All **2016** checked necessary rows are nonnegative by Fraction arithmetic:

- Strong retained-overlap Cartesian pair-query sums across all 21 recorded
  fixed-topic and indexed-menu lists, at each original two-player node and
  the aggregate of each of the three indexed branch families: 1386 rows.
- Diagonal/offdiagonal split of one own-family query index against its branch
  index, with the other query ranging over every recorded menu: 420 rows.
- Direct optimizing-node menu comparisons in the three branch families and
  the three original indexed last-reply families: 210 rows.

These rows include redundancies with older constraints. They require no
cross-family membership coupling: full Cartesian sums factor through menu
membership totals within each customer atom. For example, lists of lengths
n_M,n_N and per-client totals M,N contribute at an indexed branch family

n_M n_N sum_i H_i
 - (n_N M+n_M N) sum_i 1/(p_i+1)
 + M N sum_i 1/((p_i+1)(p_i+2)).

The point surviving this audit remains only a necessary-row relaxation point.
No full strategy, complete common-catalog instance, actual optimal comparison
portfolio, SPE completion, or half-coverage counterexample is claimed.

## Newer 717-row point: two cross-family direct comparisons rule it out

The later 61-atom source `../round4_pricing/exact_primal_cross_pair.json`,
SHA-256 `7d58f6ca319c527bfd7b2922fb1178759a08c8e2cffdfa5a799d534704711197`,
is audited separately in `mixed_pair_cross_point_audit.json`. It violates two
of the same 2016 necessary rows, so cannot have a true SPE completion retaining
these exact marginals and advertised branch meanings:

1. `AB:direct:2:all-AE.S` has exact value
   -3964329822969904743633834560253951293954370792687779921 /
   29562913345350958514120661166215532942293036122027957610 < 0.
   This is the **exact final-player** comparison, in each AB branch i, against
   each AE terminal menu topic S_j. Write p=a+b and N=sum_j 1_(AE.S_j).
   Its per-client coefficient is
   5 sum_i s_i/(p+t_i+r_i+1) - N sum_i 1/(p+t_i+r_i+1).
   The row's value is about -0.1340980768. Every comparison is at a real
   ordered-history final node and uses a topic in the same common catalog.
2. `SB:direct:1:all-AE.S` has exact value
   -63829227858899184861464417022392379683241418308874267 /
   4927152224225159752353443527702588823715506020337992935 < 0.
   Here the genuine third player after (A,T_i) compares all AE.S_j and the
   three remaining choices bound the deviation denominator by a+t_i+3.
   Its coefficient is
   5 sum_i h_i/(a+t_i+h_i+i_i+j_i) - N sum_i 1/(a+t_i+3),
   with zero-numerator terms interpreted as zero. This value is about
   -0.0129545882.

These two rows use no coupling of individual AB and AE indices: sum over every
AE menu index converts the query memberships to the already-recorded total N.
This rules out the newer frozen point only. It does not show that the entire
717-row relaxation, or an augmented unrestricted relaxation, has optimum<=2.
