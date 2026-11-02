# Shared maximum-topic root certificate: exact recovery

This folder addresses only five-player Q-CAG-HALF. The half bound remains OPEN.
No relaxation point is asserted to be a complete-history SPE or a counterexample.

## Exact author-layer statement

For the finite common-catalog unit-customer model, every complete ordered-history
pure SPE satisfies

`OPT_5 <= beta W`,

where

`beta = 183538199237294659142159872004505983652023685928609569 / 90987354041588112882665017023745484527941187490861917`

`     ≈ 2.017183609421193 > 2`.

In particular the simpler exact bound `OPT_5 <= (5043/2500)W = 2.0172 W`
follows by rational comparison.

Empty topics, repeated topics, all off-path histories and arbitrary history-dependent
pure ties are retained. For `W=0` the ordinary non-strict inequality still holds.
This improves the previously independently reviewed 557-row constant, but does not
settle the requested factor two. The new mathematical peer audit is separate from
the arithmetic checks below and has passed internal independent review; see
`../countersearch/shared_root_independent_review.md` and its independently
implemented `audit_shared_root_math.py/.json`. No external review or novelty
certification is claimed. The relaxation primal optimum is not reviewed here.

## Input and logical dependencies

The floating discovery input is the existing, unmodified file
`R-a27734a8bba345cbb5fad186c120d0bf/root_shared_max_copy_cg.json`, with SHA256
`4ec84c25c17ae2737d7b75fd1a296345aee2a6cfdbb79acb5337e84b03a7cd3a`.
Its last floating value is approximately `2.017183609421193`, not a rounded
`2.018` and not an independently certified theorem before the present work.

The certificate has 61 positive multipliers. All old rows belong to the previously
reviewed 557-row full-type system, whose semantic and separability obligations are
recorded in `R-c4732bee2f7b4e50a70568170e3334ae/round4_independent/full_pricing_review.md`.
The newly active rows are only:

* `MAX:fixed:i`: `K-|S_i| >= 0`, for the one common global maximum topic size `K`.
* `KRS:fixed:3:4` and `KRS:fixed:5:3`: thirty times the reviewed COPY-M row
  `(44/3)u_1+(13/5)K-(16/3)|T|-F_T(Q) >= 0`, where
  `F_T(Q)=|Q minus T|+|Q intersect T|/5`.
* `KCAP:4`: `574700u_1-12000OPT_5-88940K >= 0`, which is twenty times
  `28735u_1-600OPT_5-4447K >= 0`.

The fixed labels are `ABCDEUVWXY`, with genuine paths `ABCDE`, `AEUVW`, `ABEXY`.
COPY-M and KCAP are proved using the same original strategy's genuine off-path
histories and a true maximum topic; no branch-tail profits are added to the actual
welfare budget. Their exact source proofs and earlier internal reviews are in
`R-a27734a8bba345cbb5fad186c120d0bf/five_closure/root_copy_reply_rigidity.md`,
`five_structure/max_theme_root_capacity.md`,
`five_independent/root_saturation_review.md`, and
`five_aggregate/max_capacity_independent_review.md`.

## What is checked

`exact_shared_root.py` recovers a rational dual from the floating active basis,
checks every generated column exactly, clears a common 56-digit denominator,
and calls the original full-type integer pricing method. Its saved result
`exact_shared_root.json` has minimum integer residual zero and common-K column
residual zero. This is author-layer certificate recovery, not an independent audit.

`separate_shared_root_audit.py` imports neither the discovery Universe nor any
old row evaluator. It adapts the earlier independently implemented active-row
pricing audit, reconstructs every currently active old and new definition, and
checks all 1024 fixed masks, all six shared optimal multiplicities, every one of
the 792 third-family and 15504 second-family histograms, and all four legal
menu-overlap corners per family. Conditional separability is unchanged because
every new customer coefficient depends only on the fixed mask and optimal
multiplicity, while K is one scalar column. The saved independent-implementation
arithmetic result has 6144 conditional cases, 160 cached score contexts, no
negative residual, 43 zero conditional residuals, and K residual zero. Adapting
an earlier independently reviewed implementation is not claimed to be a blind
mathematical review of the present statement.

Writing the saved integer multipliers as `L_r`, the integer numerator as `B`,
and the common denominator as `D`, the exact certificate is

`B W - D OPT_5 = sum_r L_r row_r + sum_types rho_type n_type`,

where all `L_r` and all priced `rho_type` are nonnegative, and the combined
coefficient of the auxiliary maximum `K` is exactly zero. Thus the one global
maximum is eliminated without giving each row an independently chosen capacity.
No primal optimum or exact realization is needed for this upper certificate.

## Diagnostics that do not add a theorem

The obvious maximum-topic prefix floors
`K <= (6-i)u_i + sum_x p_i(x)/(p_i(x)+6-i)` are valid, but all are slack at the
old discovery primal, so no column-generation budget was spent on them.
The parent's new three-tail split row likewise has positive slack about
`0.17546298415` on that point. The new third-floor COPY row
`763 F_T(Q) <= 11033u_1+2085K-4139|T|` does separate it at `(T,Q)=(U,D)`:
its unscaled slack is approximately `-2.58331772458`. This is only a diagnostic
for the floating relaxation point; it is not a further certified welfare bound.
