# 7497-row rational necessary point: mathematical review

## Read scope and identity

This review reads the assigned computation in full, the complete common-catalog/full-history pure-SPE definition in full, and every byte of the saved exact certificate. The endpoint pin is `8250237a06c99911bbbc96cbdd7319189e40706580c64458ee8439f944f1b22d`. The certificate SHA is `8b28de8d89c76684bc95c3eb3f890e6f4ee4492cb152102281d125912e2a30e2`; it contains 64 projected atoms, 85 explicit actual-HQR lifts, and 7,497 named row slacks. The reading ledger records exact byte/line spans and all deferred candidates that were not used.

The computation is a finite necessary-row relaxation for five providers: 6,750 legacy rows plus 747 shared actual-HQR rows, 623 restricted columns, and a rational point with 85 positive explicit masses that aggregate to 64 positive projected masses. Its `W` and `O` are linear quantities of the chosen five-slot comparison tuple. The computation explicitly preserves the distinction between a necessary record induced by a full SPE and a reverse realization by a common labelled catalog.

## Exact certificate checks

The saved rational certificate has

* `W = 1`;
* `O = 73745874512537136912045667037136103721897252249253849928575784832725352114820061819/36872251370914845129122446268330093231606609939275954263930505839551418835954045112`;
* `O-2 = 1371770707446653800774500475917258684032370701941400714773153622514442911971595/36872251370914845129122446268330093231606609939275954263930505839551418835954045112 > 0`.

An independent parser check (without rebuilding the 7,497 by 85 coefficient matrix) confirms that every saved mass is a rational number, all 64 projected and all 85 explicit masses are strictly positive, the two mass representations sum to the same `O`, all 7,497 slacks parse as rationals, and their signs are exactly 7,398 positive, 99 zero, and 0 negative. All 747 actual-extension slacks are included; 39 of those are zero. It also confirms the complete row-key set is unique, every histogram has the declared five-count shape, and the 85-to-64 projection multiplicities are 48 keys with one lift, 12 with two, 3 with three, and 1 with four. These are identity and saved-data checks, not a second coefficient-generation audit.

## Necessity and the realization boundary

The common-catalog model quantifies over finite labelled themes, all ordered histories, and every unilateral deviation in a complete pure SPE. Under that model, an actual SPE record can satisfy the finite necessary rows, so the certificate is relevant as a relaxation witness. The converse is absent: a nonnegative rational solution to these rows does not supply a finite labelled catalog, a strategy on every history, or the true continuation after an off-path deviation. The computation itself says that `O` is only the union quantity for the specified five-slot comparison tuple and is not automatically `OPT_5`.

Consequently the point is a sharp *sufficiency boundary*: finite necessary rows alone permit `W=1` with `O>2`, so they cannot by themselves prove a half inequality. This does not refute the game theorem and is not a game/SPE counterexample. The source computation invokes the mature five-person half-coverage result to explain why a full five-person SPE cannot realize this same `W,O` pair; that imported theorem is not reproved or promoted here. Multiplying by a common denominator yields integer customer weights for the finite relaxation only; it does not manufacture a shared catalogue or full-history IC.

## Migration limits

The exact point may be used to compare how added actual-HQR rows affect a fixed restricted relaxation, or to test candidate certificates after binding the same 8b28… certificate. It must not be migrated to: (i) another 63-atom/437-row/old-A13 point, (ii) a different actual-HQR convention, (iii) a complete SPE or exact-OPT claim, or (iv) the six-provider half problem. The computation records distinct historical versions (6,751+747 versus current 6,750+747); these row counts must not be mixed.

## Edge interpretation

The accompanying `checks` edge is contextual. It records that this exact point checks the model boundary between finite necessary-row feasibility and full-history SPE/OPT semantics. It carries no reverse implication from rational feasibility to game realization and no whole-result claim.
