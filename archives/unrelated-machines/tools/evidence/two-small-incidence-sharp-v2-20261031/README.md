# Two-small incidence sharp-v2 finite audit

This directory preserves source `427a196bda944014458f`,
`evidence/runs/unrelated_machines/two_small_incidence_flow_audit.json`, exactly as
read by `work.py clean show`.  The run record is finite evidence for the
restricted unrelated-machines class identified by
`UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`:

* common binary-rational upper bound `b` on every finite processing time;
* at most two distinct positive non-unit finite qualifications in each machine row;
* arbitrary job support, arbitrary number of time-`b` qualifications, and allowed
  zero qualifications.

The run reports Python 3.12.14, `local_membership_checks=16128`,
`random_matrices=300`, `threshold_checks=7997`,
`q2_3dm_all_subsets=256`, and `status=PASS`.  Its `source_sha256` is the
SHA-256 of the 7,763-byte independent audit script, not of this JSON record.
The exact JSON record is retained under `source/` and has its own hash in
`manifest.json`.

The adjacent script snapshot is a read dependency from source
`4e687930a16eef8a9594`; it is preserved to make the recorded checks inspectable,
but it is not a separate claim or disposition in this round.  It implements an
integer max-flow threshold oracle, an explicit per-row capacity table for
`T>=b`, candidate-threshold scanning, a brute-force oracle for small test
matrices, the 16,128 local table checks, 300 random matrices, 7,997 threshold
checks, and all 256 q=2 perfect-3DM subsets.  No source file was modified and
this snapshot was not re-run in this round.

The finite output does not itself prove the universal 3/2 theorem or the
P=NP hardness statement.  Those quantifiers, bit-complexity argument, and the
common-`b` restriction are recorded in the previously read current page
`research/current/unrelated_machines/joint_slot_prefix_rounding.md` (v2 §7) and
its reviews.  The run is retained as a reproducible boundary check of the
capacity table and the small perfect-3DM reduction only.
