# Boss6 active phase 2.5.1

This is an active-work recovery note, not a handoff or mathematical content.

Latest user authorizes completing step 1 now, then delivering the step 2 prompt with actual programs. Do not end at a partial batch. User assigned six gpt-6-sol/high agents; all six lane agents are running. Stage 2.5.3 and graph/research-agent design remain out of scope.

Root worktree is repo-phase25, branch phase25/design. Frozen snapshot 0c767a5cf74951a27079e41aec22a62afde3a486 has 4608 files (~49MB). The root worktree's formal files stay fixed while agents read. A normal merge was published using git merge-tree/commit-tree to preserve this reading tree; last publication is recorded in refs/wcg/curation-published and phase25_work/triage-publication.json. Do not merge peer formal-file updates into the reading worktree until lane reading completes. Later classify only new/changed remote versions as an increment, reusing unchanged decisions.

Actual tools: tools/triage.py (init/next/ingest/status/export), tools/curation_tasks.py (local plan and remote CAS claim/submit/complete/handoff), tools/triage_clean.py (full-coverage cleanup plan/apply). work.py wraps them and start --curation-run isolates people/workspaces. 101 full regression tests passed before clean helper; six clean-helper tests passed; local bare-remote task lifecycle fixture passed. No new public board has been created. Step 1 is single-Boss internal batches.

Agents triage_lane1..6 own their corresponding lane, write batches and canonical records, and loop until lane-complete. No agent changes original mathematics or Git. Root classified 19 additional small materials. Four pure UUID/identity pages were actually deleted, actions bind their original SHA; originals remain in frozen Git. No mathematical prose has been rewritten.

Important calibration: algorithm-result must mean a reusable mathematical solver/decision/reduction with guarantee, not merely a script with input/output. All six agents were asked to revise their earlier A labels; these corrections and backups are being saved. Fixed LP/Fraction replay normally evidence-only, actual mathematical explanations M or mixed. Mathematical identity (e.g. UM convex-hull identity) is not actor metadata.

For speed, normal mathematical pages need content/structure classification, not line-by-line proof verification. X/E candidates must be checked across all sections to avoid hidden proof loss. Large mechanical data may be projected, but all mathematical explanation blocks must be covered. No regex-generated classifications or header-only claims.

After full classification: inspect plan-clean output, apply only human-assigned X/E cleanup; helper retains directly/indirectly cited E as attachments, deletes unused wrappers, preserves substantive mathematics, and rewrites current links. It refuses partial coverage or changed source/classification. Keep mixed pages for step 2 extraction. Then export final math/catalog/second-step candidates, build actual object-group tasks, publish normal merge, handle remote deltas, and provide ready step2 prompt. No third-stage schema/IDs/edges.

Current observed progress (not final):

```json
{
  "run": "20261103-boss6-triage",
  "snapshot_commit": "0c767a5cf74951a27079e41aec22a62afde3a486",
  "materials": 4608,
  "classified": 2381,
  "remaining": 2227,
  "categories": {
    "math-exposition": 1821,
    "evidence-only": 317,
    "math-fragment": 12,
    "algorithm-result": 76,
    "numeric-witness": 26,
    "mixed/needs-context": 108,
    "non-math": 21
  },
  "routes": {
    "retain": 1897,
    "attach": 317,
    "restore": 12,
    "distill": 26,
    "extract": 108,
    "delete": 21
  },
  "stale_record_bindings": []
}
```
