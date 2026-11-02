# R-3d253 credible extra-slot finite audit

This packet preserves the frozen `probe_extra_slot_floor.py` and `two_block_extra_slot_probe.json` sources plus the exact replay output. The script tests one fixed three-player, six-topic history-complete policy cone against uniform, `v3_original`, and `v4_original` query distributions. The companion JSON is a five-player/two-block count-state summary.

The three HiGHS LPs have normalized root 1 and guarantees 0.8081729146, 0.7972906250, and 0.7806883069. Uniform and v4 Fraction reconstructions have zero IC slack; the v3 reconstruction has a negative Fraction IC slack of approximately -1.2456091138041423e-11 and is not an exact certificate. The JSON reports root threshold 29/3, 6188 count states, 4368 terminals, and 9496 retained outcomes. The original report alone is a finite LP audit; the later independent rational check below certifies two fixed three-player SPE points, without proving a universal floor or six-provider half result.

## Reproduction

Run `python3 replay.py` with NumPy and SciPy installed. The harness recreates the source path and supplies the original complete strategy JSON under `runtime/evidence/certificates/`. The original LP may choose another optimum in a different solver version; the saved replay remains the historical finite result. Its v3 root after Fraction recovery is approximately 1.0000000000116744 and its recovered IC slack is strictly negative, so that row is not an exact feasible witness.

## Independent saved-point check

`python3 verify_recovered.py` checks the saved rational weights directly, without SciPy or the source probe. It verifies 258 ordered-history IC comparisons and 216 ordered three-background query values per row. Uniform and v4 have nonnegative exact IC, and scaling by 329 and 61776 realizes them with 1722 and 227556 unit customers respectively. The v3 row has strictly negative IC and is rejected. These are fixed feasible points, not exact LP optimality certificates or new counterexamples.
