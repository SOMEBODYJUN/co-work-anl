# Round 11 credible: genuine punishment closure and the minimum net gap

2026-10-25. Original Q-CAG-HALF, arbitrary player count, arbitrary finite
common catalog, every complete ordered-history pure SPE. **OPEN.** This
directory contains a construction attempt and a precise pressure test. It
contains no target counterexample or new unconditional welfare bound.

- [Construction working note](credible_construction_working.md): records why
  a Cartesian insurance rescaling does not produce a target counterexample,
  the additional closure imposed by jointly changing the economic and bank
  action, and the exact unpaid all-input minimum-net-gap obligation.
- [Pressure script](minimum_netgap_pressure.py) and
  [frozen result](minimum_netgap_pressure.json): one existing round10 full
  strategy cone, all 255 nonempty incidence types allowed. The named general
  bridge is `OPT_m-W <= m min_i u_i`. The accepted endpoint is checked on
  all 4,681 ordered decision histories and all 32,767 nonself comparisons.
  Its bridge gap is negative. This is no evidence for a universal positive
  statement; there was no policy, player-count, or instance scan.
- [Independent kernel check and source match](prefix_kernel_review_and_dedup.md):
  verifies geometry11's actual-prefix harmonic coefficient and identifies
  the exact already existing formula, including comparison multiplicities.
  The density note records that the full insurance family has
  `rho=O(1/m)` on both coordinates, so low query frequency alone does not
  supply private-seat structure.

- [Saddle shadow-bank ledger](saddle_shadow_bank_ledger.md): records exact
  price-discount and weighted-rent identities at the parent's shared saddle,
  plus the old credible capped-tail reselection freedom. The outstanding
  cross-history amount inequality remains unpaid.

Only this directory was written. No git, work.py, token, or external service
calls were used. The parent owns integration and any independent review.
