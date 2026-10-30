# Equal-light-flow global-minimum audit

This directory preserves a nine-file reconstruction tree for
`e68c8cf5ec1b83c3f1fd`, its four fixtures, the test helper, and the historical
pro report required only for source identity. `current_original_oracle_run.json`
records one exact original audit run: seed `20261007`, 5242 instances, 14995
legal assignments, 5720 global minimizers, 20066 option checks at minimizers,
12280 integer flow augmentations, 362 instances with multiple minimizers, and
32 invalid inputs rejected.

The audit searches all original legal assignments before applying any box or
H filter, so the finite check covers the all-minimizer property that a
single-witness test would miss. It also exercises negative bases, ties,
duplicate/order-sensitive menus, very large binary capacities, large
denominators, reverse rerouting, and empty cases. The output is finite
implementation evidence. It does not prove unequal-weight polynomial time,
universal termination, a runtime theorem, or an external literature claim;
the pasted source ZIP was not available.
