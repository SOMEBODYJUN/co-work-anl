# New CAG frontier: independent internal review (2026-10-10)

Scope: CA-THREE-MAXIMA-HALF and CA-FIVE-UPPER-221-100 in the common-catalog unit equal-sharing CAG. These reviews do not certify global novelty or external peer review. The unrestricted half-coverage claim remains open.

# Independent internal review: three maximal coverages

Reviewed `research/current/customer_attraction/three_maxima_bound.md` on 2026-10-10. This is internal mathematical review, not external peer review or a novelty determination. The review applies to the stated common-catalog, unit-customer, unit-provider model and complete strategies on all ordered histories.

The proof of `OPT_n <= U <= 2W-c` for `n >= 2` and at most three distinct inclusion-maximal coverage sets is sound after the explicit Section 2 restriction to at least two maxima. The unique-maximal case is handled separately, since its private block equals its maximal core and must not be counted twice. The single-provider case also has its direct optimality proof. The relationship with laminar maximal incidence is correctly described as incomparable.

The all-history induction (TM7) uses a true deviation to a full maximal theme. Routing counts bound the load on its globally private customers. If a later action is routed to that maximum, it is a subset of the deviator's action and its same-terminal payoff is bounded above by the deviator's payoff. Otherwise, the private contribution stays at its routing-count bound, while each selected residual-shared and core customer contributes at least `1/n`. Thus the proof accommodates subthemes that omit any core, and does not assume that stripping the core preserves the given SPE.

The seat-order step counts only seats strictly greater than the nth-largest value. This gives `sum e_j <= n-1`, `a_j=e_j+1 <= n`, and `g_j(a_j) <= nu`, including ties and `nu=0`. The three-coordinate allocation has enough capacity to reach sum `2n`. Its private coefficients are at least one, and each residual pair block has coefficient `(2n-y_l)/n >= 1`. Every non-core covered customer has exactly one or two maximal incidences, so the weighted sum pays the entire residual union once.

The sharper scalar certificate is also sound: `S=max(sum a_j,n+max a_j,3n/2)` is both necessary and sufficient for all three pair constraints. The intervals `[a_j,S-n]` prove sufficiency; summing lower bounds and pair constraints proves necessity. The claimed factor follows from `W >= c+n*nu`, with no division by `nu`.

The barrier family (TM16) has `nu=M+1` and `a=(n,1,1)`: the private maximum's first `n-1` seats strictly exceed `M+1` exactly when `M>n-1`, and the two remaining first seats equal `M+1`. Its three maxima are distinct because of the two different private unit petals. The example only limits the static union-to-seat interface, and is correctly not asserted to attain worst SPE welfare.

An independent `Fraction` check, importing no project model or solver, verified all 40,919 admissible seat-count triples for `2 <= n <= 30`, the constructive `S` allocations and their private/pair coefficients, plus 116 direct seat-order instances of (TM16). These finite arithmetic checks support implementation consistency; the mathematical review above checks the universal reasoning.

The final manuscript explicitly defines the two-maxima `e_j,a_j` by (TM8). No remaining mathematical gap was found in TM7--TM16.

The separately authored `tests/audits/customer_attraction_three_maxima_independent.py` was read and rerun successfully: 292,824 admissible threshold patterns, 2,049,768 customer-membership coefficients, 292,824 exact normalized primal extremes, 19,683 exhaustive integer-weight cases, 1,000 rational-weight cases, 196 barrier-family cases, and 49 genuine four-maxima scalar obstructions. Its declared scope is static seat-budget arithmetic without SPE enumeration. Its positive result does not replace the all-history induction review.

The final additional incidence certificate (TM17) is sound for the Section 2 setting of at least two distinct maxima. It multiplies `g_j(a_j)<=nu` by nonnegative `y_j`. A nonempty private block has coefficient `y_j/a_j>=1`; each nonprivate, non-core incidence block has coefficient `sum_{j in I} y_j/n>=1`. A zero-private maximum needs no private-block restriction. The original-game floor `W>=c+n*nu` then gives the stated instance certificate. The one-maximum case is already independently handled.

The four-maxima obstruction (TM18) is an exact legal unit-customer barrier to that scalar interface. Maximum 1 contributes exactly `n-1` seats strictly above two; each of maxima 2, 3, 4 contributes `n` seats equal to two. Hence `nu=2` while `U=5n`. These four maxima are distinct and incomparable. More explicitly, any (TM17) half-certificate weights would require `y_1>=n`, while the three pair constraints force `y_2+y_3+y_4>=3n/2`, so their total is at least `5n/2>2n`. This is a genuine impossibility certificate for the scalar half budget. It gives no SPE welfare counterexample, and the manuscript correctly preserves that distinction.

The separately authored primary audit `tests/audits/customer_attraction_three_maxima.py` was also read and rerun successfully against manuscript SHA-256 `71050d111dd32078dfe956a4e221f1efc3e6c4863057e5fb297502ed6a86ebf4`: 798 finite cases, 44,008 count states, 1,085 root outcomes, 333,941 seat-floor checks, and 461 complete ordered strategies with 9,299 histories and 38,867 direct deviation comparisons. The tested catalogs include 152 crossed-incidence cases and 524 core-omission cases. Its menu recurrence preserves arbitrary ordered-history child choices, while its materialized certificates check each true deviation directly. These are correctly stated as finite verification rather than a replacement for the universal proof.


## Five-player independent reconstruction

A reviewer independently reconstructed the raw utility rows from the ordered paths ABCDE, AEUVW, and ABEXY without importing the primary coefficient generator. The 21 multipliers are nonnegative, their independent OPT coefficient is -1, and all 1024 customer-type residuals are nonnegative (43 zero). A separate mathematical review checked the actual deviation histories, common-catalog action legality, arbitrary-prefix two-remaining-player tax identity, and ten indexed pairs of five optimal topics, including repeated topics.

The exact bound is beta=24236714656727/10967499015623. The headline 221/100 follows by a positive exact rounding gap145816779983/1096749901562300. No forced deviator is assumed locally optimal at its new history; branch node inequalities are used only for subsequent optimizing players. Customers absent from the ten recorded labels remain accounted for by the independent global OPT symbol.

Scope approved: exactly five unit providers, arbitrary finite common catalog and finite unit customers, every complete ordered-history pure SPE, zero root background, empty and repeated topics allowed. The theorem does not establish half coverage, sharpness, arbitrary-background five-remaining profit, or six-plus providers. Zero welfare is covered by the nonstrict algebraic identity.

## Reproducible evidence

- customer_attraction_three_maxima.json: finite exact continuation menus and expanded ordered-history strategies; proof is the all-history seat induction and global weighted incidence budget.
- customer_attraction_three_maxima_independent.json: independent threshold and coefficient arithmetic; tests do not replace the induction.
- customer_attraction_five_player.json and customer_attraction_five_player_independent.json: universal finite membership-type identity, independently rebuilt.
- customer_attraction_five_player.py and customer_attraction_five_player_independent.py import neither floating LP discovery nor one another.

Root independently read both final manuscripts, reconstructed the seat weights and raw slack legality, ran the audit commands and the 11 canonical CAG regressions. No unresolved fatal objection was found within the stated scopes. Unsuccessful finite root-tax and mixed-security bridge searches were not promoted into claims or research assets.
