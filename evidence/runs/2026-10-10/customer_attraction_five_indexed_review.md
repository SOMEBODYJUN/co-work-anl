# CA-FIVE-INDEXED-UPPER / CA-FIVE-INDEXED-ROWS-NO：independent exact certificate review

Review date: 2026-10-10. This is an internal reconstruction; no external peer review is asserted.

The independent audit passed. The exact constant is
145473820534756099649387160645076613709 / 70560308704423797361284609157664425493
= approximately 2.061694785720737, strictly above 2.

The auditor imports only Python standard-library modules. It does not import any discovery code, exact_compact_rows.py, or another row evaluator. Its utility(action, prior) computes the raw equal-share payoff from the individual customer's action and preceding/opposing membership bits. Every primal atom expands each histogram into five explicit indexed histories. All 437 row coefficients are reconstructed from those individual histories, safe catalog deviations, exact last-player comparisons, and the stated last-two-player tax inequality.

Primal verification: 64 positive rational atoms; normalized actual coverage 1; comparison coverage equal to the displayed constant; all 437 aggregated slacks nonnegative; 74 slacks exactly zero. All 57 active dual multipliers are nonnegative and complementary to zero primal slacks. Every positive primal atom has exactly zero dual residual.

Global dual verification: all 1,024 fixed-theme membership masks and six optimal multiplicities were audited, including customers outside every fixed theme. The AB and AE true third-action families were maximized over all 792 integer five-index histograms each; the true second-action family was maximized over all 15,504 four-bit histograms. Conditional on the optimal multiplicity, these score maxima separate. The older true final-reply menus were maximized over their full feasible aggregate domain; the active h coefficients cancel, reducing each maximum to ell=0 or ell=5. Exact integer arithmetic was used after independently deriving the utility coefficients with Fraction and a payoff scale of 120. All 6,144 separated cases had nonnegative residual; the minimum was exactly zero, with 37 zero cases. The audit took approximately 24 seconds.

Legality of the tax rows: at a fixed two-player suffix prefix, let D be the actual first action, and let L be the original final strategy's response to a deviation S. SPE supplies u4 >= U(S;L), u5 >= U(L;D), and U(L;S) >= U(T;S), for any catalog actions S,T. Adding and using 1_L*1_D <= 1_D gives H=u4+u5+sum 1_D/((p+1)(p+2)) >= U(S;T)+U(T;S). Summing this valid pair comparison gives the ordered menu-pair rows, including repeated actions. The optimal-menu tax-to-cover rows follow by summing over the five comparison actions and retaining each customer's actual prefix load. No continuation was frozen after a deviation.

Scope: these two certificates establish the universal upper bound for every genuine pure SPE and the exact optimum of the specified relaxation. Its rational feasible primal has cover/actual ratio greater than 2, so this particular 437-row relaxation cannot establish half coverage. The primal does not assert the existence of a game with those strategy histories and is not an SPE counterexample.

Replay:
```sh
python tests/audits/customer_attraction_five_indexed_independent.py
```

[Frozen independent report](customer_attraction_five_indexed_independent.json) records the canonical certificate and auditor SHA-256 digests. [Primary report](customer_attraction_five_indexed.json) has matching exact values and all32 actual-mask minima.
