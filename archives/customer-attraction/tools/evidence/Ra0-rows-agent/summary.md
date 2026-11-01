# Ra0 fixed-support rows: evidence summary

- Source: `24e8313ac2c86cbfbbfd`; frozen path `research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_rows_fixed_support.json`.
- Scope: 437 old rows plus all written background rows only on frozen 64 atom support.
- Rows: 437 old rows and 1430 newly written background rows.
- Floating objective: `2.0391979934373885`. Exact primal value: `301904989188813053163805000409977755377/148050846538890923800466562791232658950` (approximately `2.0391979934373885`).
- The exact primal is verified on the finite written-row system. The JSON explicitly reports `game_SPE_witness=false`, `universal_bound=false`, and `full_domain_dual_certificate=false`.
- The former point violates a newly written row: minimum slack `-512423714856196407772554710592954399663/564482469635390378890276873261315403944`, most violated row `['S3_indexed_background:C6:D7']`.

This is a finite support/row diagnostic. It does not establish feasibility for all customer weights, an SPE realization, or a Q-CAG-HALF conclusion.
