# Independent audit of the insurance shared-load saddle and transport sign

2026-10-25, matching11. Reviewed aggregate11's
`../aggregate/shared_load_components_and_exact_sign_boundary.md` §4/4.1,
the two rational packet JSONs, and the source's full BASE/PUNISH/EXIT
proof `R-d398.../round5_general/security/global_extra_individual_counterfamily.md`.
This is an auxiliary-sign review, not new HALF progress or a new game.

The source's all-history proof covers the controller used here: EXIT earns
the bare maximum3; nonterminal PUNISH earns3 and its final step earns2;
BASE middle obedience exceeds2 while every deviation earns at most2;
the root resets its anchor after every action and earns6/5. I found no
controller mismatch. This review inherits that analytic SPE proof and does
not claim to enumerate the full thirty-action six-player ordered tree.

Reconstructing all180 actual-prefix deleted menus independently gives the
reported actual path and utilities, W=12. The exact shared q realizes
L*=(8/3;(7/15)^5;1^5). The inner convex KKT signs and maximizing-column
supports all check, including the zero weight on anchor0 for the active p*.
Supported nonzero-anchor queries have g=37/22; excluded anchor0 queries have
g=14/11. Hence both saddle directions are certified without a numerical
optimizer. The objective is convex in load and linear in p, so these are
global saddle conditions, not merely stationary equalities.

For every supported query (a,b), a is nonzero. The deleted competitor
load on that a is4 at the root and0 at every later actual role. All five
bank coordinates have competitor load1 in every one of these branches.
Consequently the exact linear correlation entry is independent of the
supported topic within each row:

    C_1(A)=795/484,
    C_i(A)=-105/484   (i=2,...,6).

Any nonnegative role/query transport preserving p* has no mass on its
zero-mass excluded topics. Its row mass is1, so total C is therefore
135/242>0 for **every** such transport. There is no matching minimization
left to change this amount. The exact positive credits are D=2017/1210 and
IC=4/5; they give IC-C+D=21/11=W-6(37/22)>0.

Thus the universal stronger claim that each fixed p (even when p is at a
global saddle) admits a zero-C transport is false. The shared-load cap,
the original mixed payment C<=D+IC, and HALF are not refuted.

Aggregate11 then supplied a uniqueness argument, independently checked
here, that also closes the favorable-outer-p escape for this sign. Write
G(L)=max_A g_A(L) and gamma=37/22. If L' is any primal minimax optimum,

    gamma=min_L F_(p*)(L)<=F_(p*)(L')<=G(L')=gamma.

Thus L' minimizes F_(p*). Strict convexity in the five nonzero-anchor
economy coordinates and five bank coordinates fixes each of those loads
to L*. Every member of K has total economy load5, so the remaining anchor0
coordinate is fixed too. The primal minimax load is unique.

For any dual-optimal p',

    gamma=min_L F_(p')(L)<=F_(p')(L*)<=G(L*)=gamma.

Since anchor0 queries have value14/11<gamma there, p' must assign them zero
mass. Every dual optimum is therefore supported on the same25 topics,
where the row C values above are constant. Every optimal p' and every
transport preserving it has C=135/242>0 at the unique primal load. This
does not require characterizing the remaining p' marginals. It still
rejects only zero-C, with D and IC retained in the real payment.

For comparison, uniform p on all30 topics has C=3269/7260>0 but admits the
exact minimum transported C=-477/484. `insurance_transport_exact.py/json`
certifies that distinct named marginal by an integer Hungarian primal/dual:
assign anchor i to row i and mix uniformly over its five banks. This
earlier rescue cannot be used for p*, which assigns zero mass to anchor0.

`audit_insurance_saddle.py` and `insurance_saddle_independent.json` record
the independent exact arithmetic, q balances, all180 actual-prefix ICs,
all active query values, KKT, row constancy, and final identity. No policy
cone or new-instance scan was used. No global novelty or external review
claim is made.
