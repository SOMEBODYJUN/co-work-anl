# Fixed-population disjoint catalog padding preserves every old complete SPE

2026-10-23. Personal research checkpoint. The construction below is a general lemma for the exact CAG-MODEL, including all ordered histories, arbitrary pure-SPE ties, empty topics, and zero customers. It does **not** prove or refute Q-CAG-HALF, the direct floor `u_i >= OPT_m/(2m)`, the mixed full-root-menu bridge, or the true aggregate security bridge. Author proof and definition-level exact implementation check completed; the parent’s independent cleaner replayed the audit and checked the proof, identifying the t=0 duplicate-empty-topic issue that is corrected here. This is internal review only. No novelty claim.

## Statement

Fix a nonempty old finite catalog S, m>=1 players, and any complete pure SPE sigma. Let

    K = max_(A in S) |A|.

For 0<t<=K/m, adjoin p>=m new themes D_1,...,D_p, each with t customers, where all these customers are disjoint from each other and every old customer. For rational t, scale every customer multiplicity by a common denominator so that the entire instance still consists of distinct unit customers. If t=0 (in particular K=0), add no themes, or optionally the single empty theme if it is absent: a set-valued catalog cannot contain several distinct copies of the empty set. The preservation conclusion and formula (1) still hold, because max_r OPT_old,r=OPT_old,m when t=0.

**Padding lemma.** There is a complete pure SPE sigma+ of the enlarged catalog which agrees with sigma at every history made solely of old themes. In particular the original actual action path and every actual player payoff are preserved (up to the common integer scaling). The enlarged optimum satisfies the exact convolution

    OPT+_m = max_(1<=r<=m) [ OPT_old,r + (m-r)t ].           (1)

Here OPT_old,r is the optimum using at most r old themes. Repeated choices are allowed; the old catalog is nonempty. An all-new optimal choice need not be listed separately because `OPT_old,1=K>=t`, so the r=1 expression dominates mt. The formula also holds when t=K=0.

This holds with the **same number m of players**. It does not assert a direct-sum theorem after adding players or composing separate equilibrium paths.

## Full-history proof

A current player can always choose a maximum old theme C. Whatever the future does, every customer in C has at most m covering players. Hence that deviation gives at least K/m. This elementary guarantee holds at every legal history in the enlarged game, because new-theme choices never cover old customers.

At a history containing a new theme, choose any pure SPE of the restricted subgame in which all remaining players must choose old themes. This restricted finite game has an SPE by backward induction; retain its policy on all descendants that continue to use old themes. Its current prescribed payoff is at least K/m: choosing C guarantees K/m against any restricted continuation. A deviation to a new theme pays at most its whole size t<=K/m, independently of all subsequent choices. Thus any restricted best response is also optimal against every new-theme action.

For a completely formal recursive specification avoiding inconsistent choices of overlapping restricted subgames, fix one backward-induction selector for the restricted old-action game at every possible old-count background and number of remaining players. At a history containing a new theme use this selector. Each old-action descendant remains within this restricted recursion. New-action descendants may enter another selected restricted recursion, but a new-theme deviator's payoff remains <=t regardless of those choices.

At an all-old history prescribe the original sigma action. An old-action deviation follows sigma at all subsequent all-old histories, exactly as in the original complete SPE, so it is not profitable. A new-action deviation pays at most t. The original prescribed payoff is at least K/m: in the original SPE, choosing C guarantees K/m against its actual original continuation. Hence the new-action deviation is not profitable either.

These two cases cover **every ordered decision history**. They prove complete SPE directly by the one-step deviation inequalities, and do not impose anonymous ties. The actual path remains all-old and exactly equals the original path.

For t>0 and (1), any m-theme choice uses r old themes and at most m-r distinct new themes. Its old coverage is at most OPT_old,r and its new coverage at most (m-r)t. Conversely select an old optimal r-tuple and m-r distinct new themes. There are p>=m available new themes, and all their customers are disjoint, so equality is attained. The r=0 option is dominated as noted above.

## Consequence for the direct all-player floor

If the proposed universal direct floor

    OPT_m <= 2m u_i                                         (F)

holds for every complete SPE of every common catalog, then every old complete SPE necessarily satisfies all the stronger instance-specific inequalities

    OPT_old,r + (m-r)K/m <= 2m u_i,   1<=r<=m.              (PF_r)

Conversely the universal collection `(PF_r)` contains `(F)` at r=m, so as universal conjectures they are equivalent. The nontrivial use is **counterexample construction**: a fixed old policy violating some `(PF_r)` immediately yields a genuine enlarged-catalog violation of `(F)`, without building or searching the enlarged complete strategy cone. Clear denominators by scaling old clients by m and giving each new theme K original-scale customers when t=K/m.

This produces a linear cone diagnostic. Fix the old formal policy sigma, an on-path player's payoff row u, an r-topic portfolio J, and a candidate maximum-size theme C. On the full nonnegative customer-type cone impose every true ordered-history SPE row, plus `|A|<=|C|` for every old A. Then maximize

    coverage(J) + (m-r)|C|/m - 2m u.

A positive **exactly feasible** point is enough for a direct-floor counterexample via the padding lemma. A positive floating LP objective is only a discovery candidate; it must be rationalized and all original complete-policy rows checked exactly.

## The universal cap K/m is sharp for preserving arbitrary old SPE

For m>=2 take an old catalog consisting of a single K-customer theme A. Its unique actual path is A repeated m times; every player obtains K/m. Pick a rational t satisfying

    K/m < t < K/(m-1).

Adjoin any positive number of pairwise disjoint t-customer themes. If the root deviates to one new theme, then at every later history there are at most m-1 old-theme players in total. Choosing A guarantees at least K/(m-1)>t, whereas any new-theme choice can never give more than t. Therefore every follower strictly chooses A in every SPE of that deviated subgame. The root deviator receives all t>K/m, so **no** complete enlarged-game SPE preserves the old all-A actual path. For m=1, any t>K is already a profitable root deviation. Thus the bound K/m cannot be increased uniformly over old catalogs and old complete policies. This sharpness concerns preservation; it is not a half counterexample.

A policy-dependent stronger sufficient cap is also available. Let L_sigma be the minimum prescribed mover payoff over **all** old ordered decision histories. For m>=2, the same proof works for

    t <= min{ L_sigma, K/(m-1) }.                          (2)

At all-old histories use L_sigma. At a history containing a new choice, at most m-1 total players can ever choose an old theme, so the restricted old-action game gives the stronger K/(m-1) guarantee. This refinement requires all-history prescribed payoffs, not merely the actual minimum. The basic K/m lemma needs none of this additional policy information.

## Consequence for the primary half target

The same preservation and optimum formula show: if any old m-player complete SPE satisfies

    OPT_old,r + (m-r)K/m > 2W

for some r, then padding yields a genuine Q-CAG-HALF counterexample, with exactly the same original welfare W. Conversely, if Q-CAG-HALF is universally true, then every old complete SPE must satisfy all these strengthened comparison inequalities. Thus `(1)` provides a general counterexample amplification test, not only an auxiliary per-player-floor test. No such violation is asserted here.

## Reproducible evidence and limits

`audit_safe_catalog_padding.py` imports only Python's standard library. It generates complete old policies independently by exact Fraction backward induction, constructs the enlarged full ordered-history policies by the proof above, and checks every action at every history. For m=1,...,4, old catalog sizes 1,...,3, three deterministic random inputs each, it verifies 36 constructions, including zero multiplicities. Before building a policy the audit quotients equal-coverage old labels, and when K=0 it adds no new empty-theme copies; the printed/frozen report gives the exact comparison count. It independently enumerates the enlarged optimum and verifies (1). This is a finite implementation regression; the all-m proof is the preceding argument.

`safe_padding_probe.py` implements the full-policy cone diagnostic `(PF_r)`. The float reports record only their explicit finite scopes. The direct-floor probe separately attacks unpadded `(F)` on random history-dependent tie selections. No finite no-separator report proves a universal floor.
