# Fixed bivariate reply marginal / common-threshold core support

Core: `customer-attraction/fixed-bivariate-reply-marginal-common-threshold-diagnostic` (pin `1bc60566825554fc78329cbfb26edfb42a1b3fd959bb3f6229786adfb0022d94`). This package records a self-context check only; it does not add a cross-object implication or a full-game claim.

The frozen `cc48d8` input has 16 histograms (10 positive, 6 zero), 194 reply groups, 582 explicit 01/10/11 states, 1306 stored RR-overlap columns, and `O=1`, `W=2590607258266118042503848518699183/5430547020889608346592960056661140<1/2`. The fixed domain holds every own `(R,Z,RZ)` four-state mass and puts every `R_g` on a common threshold axis. For `R_e` and `Z_f`, the cross overlap bound is

`M_ef = min(v_f,r_e)` when `r_e≤r_f`, and `v_f+min(o_f,r_e−r_f)` otherwise.

The simultaneous interval assignment `Z_f=[0,v_f) ∪ [r_f,r_f+o_f)` attains every `M_ef` at once. Since the cross-overlap coefficient in each ZZ row is positive, all 60 aggregate slots are synchronously maximized in this domain. The exact vector is 33 positive, 21 zero and 6 negative; the minimum is `-269116452255245004437772368580110652437/530195166743494242094563876251940420480`. The six negative keys are `(0,1,0100)`, `(0,1,0102)`, `(0,1,0122)`, `(1,1,0100)`, `(1,1,0102)`, `(1,1,0111)`.

The independent interval audit parses all 267881 bytes, checks all columns nonnegative, recomputes `O` and `W`, verifies 194 four-state groups, 34 positive physical interval cells, 148104 literal edge-pair terms and 1531 cross-RZ equalities, with zero original-script imports, zero original-main invocations and zero LP calls. Its six negatives, minimum, row count and `W` match the 1278-byte direct replay report. The direct replay report itself is limited to the fixed-domain fields and does not print the other 54 slot values.

The common-threshold substitution changes 164 of the 1306 old RR overlaps (maximum raise `1118725340347623934923883665585697/10861094041779216693185920113322280`), so this is not a claim that all 1905 old coordinates remain fixed. The result excludes only a completion satisfying the stated fixed hist/own-four-state/common-R domain. It does not exclude arbitrary cross-group `R` unions, released `Z/RZ` domains, a full labelled-catalogue strategy/SPE, or `OPT_6≤2W`.
