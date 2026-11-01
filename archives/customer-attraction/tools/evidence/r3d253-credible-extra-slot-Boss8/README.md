# R-3d253 credible extra-slot finite audit

This packet preserves the frozen `probe_extra_slot_floor.py` and `two_block_extra_slot_probe.json` sources plus the exact replay output. The script tests one fixed three-player, six-topic history-complete policy cone against uniform, `v3_original`, and `v4_original` query distributions. The companion JSON is a five-player/two-block count-state summary.

The three HiGHS LPs have normalized root 1 and guarantees 0.8081729146, 0.7972906250, and 0.7806883069. Uniform and v4 Fraction reconstructions have zero IC slack; the v3 reconstruction has a tiny floating pseudo-negative and is not an exact certificate. The JSON reports root threshold 29/3, 6188 count states, 4368 terminals, and 9496 retained outcomes. These are finite audits only: no unit-customer realization, complete SPE certificate, universal floor theorem, or six-provider half result.
