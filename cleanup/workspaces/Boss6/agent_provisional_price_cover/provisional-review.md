# Provisional review: 1583fda34810e99e434b

- Source: `history/source/notes/unrelated_machines/arbitrary_sink_price_cover_final_full_read_review.md`
- SHA-256: `d45f00c0e7684bae520ae61ed53213cf20e91a24c18e7eed0972753f8b1a9a63`
- Size: 13,995 bytes; both frozen commits point to the same source blob.
- Read status: full 143-line source read, including sections 1–9, all tables and formulas.

## Mathematical content

This is an internal final read-after-review of the canonical source `arbitrary_sink_private_group_price_cover_rounding.md` (source SHA `6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580`). It records three identities: `UM-UPPER-COLUMN-BUDGET-BASE-ROUNDING-v1`, `UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1`, and the promise-search variant `UM-ARBITRARY-SINK-PRIVATE-GROUP-PROMISE-APPROX-v1`. The review rechecks the nonempty-mode rank condition, parallel-copy transversal matroid base rounding with a single `+b` row-budget loss, common macro matching, arbitrary sink eligibility, the multiplicative-weights price cover, and the promise-version integer-grid search.

The review's key correction is that the final source requires nonempty mode homes to match all macro elements; it no longer has the earlier empty-mode rank defect. The price-cover contract is conditional on explicit home groups, mode bases, sink eligibility, `W_h <= T`, `a_j <= delta T`, and the stated `rho, delta, tau, eta` inequalities. It does not extract these roles from an arbitrary unrelated-machines matrix and does not settle `UM-TARGET-v1`.

The source also reports a finite exact audit scope (187 cases for the upper-column component), the MW parameter check `epsilon=gamma=eta/4`, and a 3066-pattern integer search for the modified unknown-OPT threshold procedure. These are evidence about the stated interface only; the report explicitly does not claim a production rational-LP backend, general source extraction, external novelty, or a general near-two algorithm.

## Comparison and disposition recommendation

The existing integrated review `archives/unrelated-machines/state/审查/仿射线全局dummy与任意汇点价格覆盖双源审查--审查.md` already carries the canonical price-cover source, the same three IDs, and the conditional-model boundary. This note adds a distinct final read-after-review record and the unknown-OPT threshold correction/search details; it is therefore best treated as `integrated` into that review rather than as a new theorem or a pure duplicate. The external JSON mentioned by the note is not present in this checkout, so no new evidence object is claimed.

Formal claim/done/push was not run because the write endpoint is currently blocked. This directory is local provisional work only; it is not a completion receipt.
