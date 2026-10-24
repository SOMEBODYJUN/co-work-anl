# Individual credible deficits and an exact layer-cake repair

2026-10-24. General CAG-MODEL, arbitrary finite common catalog, arbitrary player count, unit customers and providers, full ordered-history pure SPE. This is a personal mathematical checkpoint. It sharpens the previously audited prefix insurer; it is **not** a half-coverage proof or a target counterexample. Parent independently reconstructed the main bank and layer accounting before this draft. Independent internal analytic review is complete: see `../potential/blind_repair_reconstruction.md` (saved before reading this draft) and `../potential/heterogeneous_repair_independent_review.md` (full comparison, no fatal objection). External review and novelty remain uncertified.

## 1. Exact input and statement

Fix m>=2, 1<=j<m, an arbitrary complete target path z=(A_1,...,A_m), and a genuine complete pure SPE pi after the fixed ordered prefix (A_1,...,A_j) realizing its target tail. Write W for target welfare, O=OPT_m, and u_i for target final payoffs. No incentive assumption is made on the first j target positions.

For i<=j set h_i=(A_1,...,A_(i-1)) and define

    ell_i(A) = min { current player's final payoff after (h_i,A):
                     all later players use a complete pure SPE },
    M_i = max_A ell_i(A),
    delta_i = (M_i-u_i)_+,
    D = max_(i<=j) delta_i,
    R = sum_(i<=j) delta_i.

All minima are attained in these finite games; fix an attaining genuine child SPE rho_(i,A) for every i,A, including A=A_i. Values are rational.

**Repair theorem.** If D>0, there is a finite unit-customer, common-catalog instance with the same number m of players and a complete pure SPE whose old-coordinate target path is z, and whose welfare and optimum, before an optional common integer scaling L, are exactly

    W_new = W + mD + R,
    OPT_new,m = O + (2m-1)D.

Thus the exact half deficit is

    OPT_new,m - 2W_new = O-2W - (2R+D).             (HET)

If any added customer block has rational size, multiply *all old and new customer blocks together* by a common positive integer L. They then denote distinct unit customers; all payoffs and both sides of (HET) multiply by L. The providers remain unit weight and there remain m providers.

Consequently a legal input with O-2W>2R+D yields a genuine counterexample to Q-CAG-HALF. No such input has been found here. Conversely, if general half holds then every such target path satisfies O<=2W+2R+D. This is a stronger robust consequence than the earlier uniform bound O<=2W+(2j+1)D, since R<=jD. It is an equivalence-style repair reduction, not a proof of that robust inequality.

When D=0, the old path itself is realizable by a complete pure SPE: retain pi at the normal length-j child, use rho_(i,A) for nonnormal main actions, and induct backwards over normal i. A same main action cannot be a deviation in this old instance, so its normal child is retained. Every alternative gives at most M_i<=u_i. No insurance or limiting zero-size blocks are required.

## 2. Marked-position bank game

Fix a nonempty marked set I subset {1,...,m-1}, k=|I|, d=m-k>=1, and a scale s>0. The customer blocks are disjoint:

* k banks B_i, indexed by i in I, each of size 2s;
* one reservoir Y of size ds;
* d-1 leaf blocks, each of size s.

The insurance catalog consists exactly of these m blocks. Its desired ordered path chooses B_i at position i in I, and Y at every unmarked position. In particular the final position chooses Y. It covers (m+k)s customers; its optimum with m actions is the union of all m blocks, of size (2m-1)s.

At any normal prefix, let p be the number of used banks and q the number of earlier Y actions. All used banks are distinct. At every decision position i<=m, q<=d-1; the last desired Y has not occurred yet.

**Low-exit lemma.** Force any current insurance action T after such a normal prefix. There is a complete pure SPE of the remaining insurance subgame in which this fixed current player's insurance payoff is at most s. This includes forcing exactly the desired insurance action; it will be needed when another coordinate changes.

Scale s=1 for the proof. A repeated bank is already shared by two players and has payoff at most 1 in every continuation. A leaf has size 1 and also has this raw cap. Take arbitrary complete BI continuations in these cases. If i=m there are no fresh banks; these two cases and the following Y case cover everything.

If T=Y, it leaves q'=q+1<=d copies of Y and p banks used. In a clean subtree require every bank count at most one, every leaf count zero, and Y count at most d. Prescribe an unused bank while one exists, then Y. Any first action violating cleanliness enters a permanently chosen complete BI subtree. Clean terminal play has each bank once and Y exactly d times. A fresh bank earns 2; a Y earns 1. At a fresh-bank node, choosing another fresh bank earns 2 and choosing clean Y earns 1. All first exits have raw payoff at most 1: repeated bank, leaf, or Y with count at least d+1. At an all-banks-used Y node, every alternative is capped by 1. Backwards induction proves every clean node optimal; every exit child is a genuine SPE by construction. The initially forced Y earns exactly 1.

If T is a fresh bank F, keep F at count one until a final prescribed duplication. Clean histories have each bank count at most one, leaves unused, and Y count at most d-1. Prescribe other unused banks, then Y until its count is d-1, then duplicate F as the final action. At the initial forced child there are precisely

    (k-p-1) + (d-1-q) + 1 = m-i

actions left, so these phases fit exactly. When d=1 there is no Y phase. Clean future fresh banks earn 2; clean future Y actions, when present, earn d/(d-1) between 1 and 2; the final F duplicate earns 1. A first nonprescribed repeated bank, a leaf, or a Y beyond the d-1 cap has raw payoff at most 1, so use permanent arbitrary BI there. At a fresh-bank node another fresh bank earns 2 and clean Y earns at most 2. At a Y-phase node all nonclean alternatives have cap 1, and a clean Y earns at least 1. At the final duplicate node switching to Y gives d/d=1 and every bank/leaf alternative gives at most 1. Backwards induction again proves the whole remaining ordered tree is SPE. The initially forced F is duplicated and earns exactly 1.

These proofs are genuinely full-history constructions: each first clean exit gets an independent permanent BI tree; it does not return to the clean mode later. Distinct ordered histories may use distinct BI selections. Nothing is inferred merely from a static equilibrium occupancy.

## 3. The normal insurance continuation is credible

The marked path itself can be completed to a pure SPE. At every normal node choose its desired bank or Y. Every nonnormal insurance action switches permanently to its low-exit SPE from Section 2. A marked normal player obtains 2s and an unmarked player obtains s; each deviation obtains at most s. Induct backwards along the normal path. This includes the final Y action, whose alternatives all have payoff at most s.

For the eventual product construction it is enough to use a simpler prescribed tail after original position j, since I subset {1,...,j}. All banks have then been used and there were j-k normal Y actions. Prescribe Y at *all* ordered tail histories. The total possible Y count is at most (j-k)+(m-j)=d, hence any prescribed current Y earns at least s. Every bank deviation has count at least two and payoff at most s; every leaf deviation also gives at most s. This is therefore a complete SPE after the fixed normal insurance prefix, even after arbitrary later insurance deviations.

## 4. Layer cake and one common fixed product instance

List the distinct positive numbers among delta_1,...,delta_j in increasing order

    0=e_0<e_1<...<e_L=D.

For layer l define s_l=e_l-e_(l-1)>0 and I_l={i<=j:delta_i>=e_l}. Make an independent marked-position bank game for each layer, with its own k_l=|I_l| and d_l=m-k_l. These are fixed components of a single instance, not state-dependent customer weights. Their identities give

    sum_l s_l=D,
    sum_(l:i in I_l) s_l=delta_i,
    sum_l k_l s_l=R.

Let the whole new catalog be the full Cartesian product of the old catalog and all layer catalogs; the actual set associated with a product action is the union of its disjoint component blocks. Hence every action and every joint deviation is legal. The normal insurance payoff at original prefix position i<=j is D+delta_i; at every tail position it is D.

## 5. All-coordinate deviations and full-tree strategy

While the first i-1<=j-1 product actions are exactly normal, prescribe the normal old action A_i and each layer's normal insurance action. If position i<=j chooses any different product action, say old action A and layer actions T_l, switch its entire later subtree permanently to

    rho_(i,A) times the product over l of the Section 2 low-exit SPE for T_l.

This includes A=A_i when an insurance coordinate changes, and includes all desired insurance actions when only A changes. At a normal position i the prescribed total payoff is

    u_i+D+delta_i.

Every alternative joint product action has actual continuation payoff at most

    ell_i(A)+D <= M_i+D <= u_i+delta_i+D.

Thus *all* joint deviations are paid, rather than just coordinatewise deviations.

If the first j product actions are all normal, use pi times every layer's all-Y full tail SPE from Section 3. Once a first deviation or this normal tail mode is chosen, each component reads only its own subsequent ordered history and the mode never resets. The Cartesian product of complete component SPEs is complete SPE: any later joint deviation changes total payoff by the sum of the component payoff changes, each nonpositive under its genuine component continuation. Thus every off-path ordered history is covered. Backwards induction over the normal first j nodes proves the full product strategy is SPE and retains target old path z.

Each insurance layer has welfare (m+k_l)s_l and optimum (2m-1)s_l. Disjoint customer universes and the full Cartesian catalog make both old target welfare and the optimum exactly additive: choose each component's m-action optimum and pair its m actions by position. Therefore

    W_new=W+sum_l(m+k_l)s_l=W+mD+R,
    OPT_new,m=O+sum_l(2m-1)s_l=O+(2m-1)D,

proving (HET).

## 6. General and m=5 consequences, and the remaining problem

This exact construction applies to all m and arbitrary common finite catalogs. For a full input specified by an arbitrary target path whose last action is a BR, take j=m-1. A true counterexample follows if

    O-2W > 2 sum_(i=1)^(m-1) delta_i + max_i delta_i.

At m=5 this same general deduction becomes

    O_5 <= 2W + 2(delta_1+delta_2+delta_3+delta_4)
                   + max(delta_1,delta_2,delta_3,delta_4)

*only conditional on general half being true*, or an equivalent universally valid robust budget. It is not an unconditional new upper bound. A genuine complete SPE has all delta_i=0, so applying the desired robust inequality to it is precisely the missing half conclusion, not a proof of it. Unlike the uniform repair's 9 max(delta) loss at m=5, an isolated deficit now costs only 3 delta, wherever it occurs. This makes nonuniform defects a concrete more favorable counterexample mechanism, but there is no positive old half gap exceeding the new loss in this checkpoint.

Next useful work: construct a target path with a positive old half gap and deficits concentrated on a few roles, or prove an independent globally paid budget for 2R+D. Finite failure to find such a path would establish neither half nor the impossibility of the construction route. Do not resume blind fixed-strategy-cone sweeps.

## 7. Sources and validation

The uniform prefix compiler and its two clean bank modes are due to the earlier personal asset `R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md`, with its recorded internal independent audits. The present draft changes the actual bank action order to arbitrary marked positions and then combines fixed insurer components by the exact layer-cake identities. It does not claim the insurer idea or credible child floors are new.

`audit_marked_bank.py` is a standalone Fraction audit with no repository solver imports. It checks the general bank rules on every nonempty marked subset through a fixed small maximum m, all normal positions, all forced insurance actions, every later ordered history, and every legal deviation. Finite checking only validates the implementation; Sections 2-5 carry the general quantifiers.

Its completed run covers m=2,...,5, all 26 nonempty marked games, 518 forced-action children, 15,353 later ordered decision histories, and 75,913 legal-action IC comparisons. All pass exactly.

`audit_heterogeneous_product.py/json` separately reconstructs one complete product instance from definitions with 75 distinct unit customers and 18 themes, and does not import repository model or SPE solvers. The old target is AAB with disjoint A size1 and B size4, scaled6. Its actual old profits are (3,3,24), and its exact individual credible deficits are (5,9). Two layers use marked sets {1,2} at scale5 and {2} at scale4, so the latter layer explicitly tests an unmarked Y preceding a marked bank. The complete new strategy has 343 ordered decision histories and passes all 6,174 joint-action IC comparisons. Its profits are (17,21,33), W_new=71, OPT_new=75; the half-gap cost is37 rather than the uniform45. The old half gap is negative, and this is only an exact compiler regression, not a target attack witness. The JSON retains every ordered-history prescribed action.
