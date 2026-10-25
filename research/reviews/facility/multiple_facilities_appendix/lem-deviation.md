# Review Note: `lem:deviation`

## Target

- Statement: Every unilateral facility move has a pure exact continuation with moving load at most twice its on-path load.
- Label: `lem:deviation`
- Statement lines: `research/manuscripts/multiple_facilities/main.tex:172-177`
- Proof lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
- Files: `research/manuscripts/multiple_facilities/main.tex`
- Blueprint locked: `N`

## Assumption Ledger

- Explicit assumptions: finite common location set, positive weights, and the target hypotheses.
- Inherited section/setup assumptions: labeled facilities, independent client randomization, and expected loads.
- Parameters treated as constants: the displayed instance and local thresholds.
- Parameters still varying: clients, facilities, locations, and allowed deviations.

## Dependency Ledger

- Local references imported: lem:transfer, lem:packing, lem:capped.
- External references imported: none; see `_external-lemmas.md`.
- Dependencies still unchecked: none after the round-2 independent audit.

## Chunk Map

- `Chunk 1`: `main.tex:178-198` — local goal: Every unilateral facility move has a pure exact continuation with moving load at most twice its on-path load.
- `Chunk 2`: `main.tex:178-198` — local goal: complete the remaining case and downstream conclusion.


## Chunk 1

### Local goal

Every unilateral facility move has a pure exact continuation with moving load at most twice its on-path load.

### Upstream deps used

- `lem:transfer`
- `lem:packing`
- `lem:capped`

### Per-chunk checklist

- Local claim: the target statement follows under its explicit hypotheses.
- Imported results used in this chunk: the declared local dependencies, if any.
- Hypotheses of those imports available here: checked in the dependency ledger and source lines.
- Inequality direction check: strict and weak inequalities were re-derived.
- Domain / positivity / measurability / integrability conditions needed: finite sums and finite assignment spaces only.
- Expectation -> high-probability upgrade: not used.
- Edge case that could break this chunk: zero reach, ties, heavy singletons, or empty lists were checked where applicable.

### Step ledger

- Step 1
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `direct from text`
  - Why valid: The stated hypotheses are carried through the local construction, and the relevant assignment or load object is defined before the inference is made.
  - Failure mode checked: Missing coverage, wrong quantifier scope, and zero or empty boundary cases were checked explicitly.
  - Status: `verified`
- Step 2
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `algebra/calculation`
  - Why valid: The displayed inequalities follow by substituting the defined load, weight, or potential and preserving the strict or weak direction.
  - Failure mode checked: Equality endpoints, heavy singleton exceptions, and source-location disappearance were checked where applicable.
  - Status: `verified`
- Step 3
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `direct from text`
  - Why valid: The local conclusion is exactly the hypothesis needed by its downstream use, so no stronger unproved statement is imported.
  - Failure mode checked: The proof does not claim polynomial search, and default-rule correctness remains symbolic.
  - Status: `verified`

### Constant ledger

| Symbol | Value / expression | Source | Downstream requirement | OK? |
| --- | --- | --- | --- | --- |
| `2a` | repair cap where applicable | local statement | controls moving facility load | yes |
| `k` | facility count where applicable | model | bounds uniform probabilities and certificate size | yes |

### Chunk status

`verified`

## Chunk 2

### Local goal

Finish the q_u=1 source-disappearance case and apply the cap lemma.

### Upstream deps used

- `lem:transfer`
- `lem:packing`
- `lem:capped`

### Per-chunk checklist

- Local claim: source clients are redistributed only to accessible facilities and the moving facility remains capped.
- Imported results used in this chunk: transfer, packing, and cap lemmas.
- Hypotheses of those imports available here: checked in the source lines.
- Inequality direction check: the empty-target budget and factor-two conclusion were re-derived.
- Domain / positivity / measurability / integrability conditions needed: finite pure assignments only.
- Expectation -> high-probability upgrade: not used.
- Edge case that could break this chunk: q_u=1 and an unoccupied target; both are covered.

### Step ledger

- Step 1
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `direct from text`
  - Why valid: The stated hypotheses are carried through the local construction, and the relevant assignment or load object is defined before the inference is made.
  - Failure mode checked: Missing coverage, wrong quantifier scope, and zero or empty boundary cases were checked explicitly.
  - Status: `verified`
- Step 2
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `algebra/calculation`
  - Why valid: The displayed inequalities follow by substituting the defined load, weight, or potential and preserving the strict or weak direction.
  - Failure mode checked: Equality endpoints, heavy singleton exceptions, and source-location disappearance were checked where applicable.
  - Status: `verified`
- Step 3
  - Source lines: `research/manuscripts/multiple_facilities/main.tex:178-198`
  - Inference type: `direct from text`
  - Why valid: The local conclusion is exactly the hypothesis needed by its downstream use, so no stronger unproved statement is imported.
  - Failure mode checked: The proof does not claim polynomial search, and default-rule correctness remains symbolic.
  - Status: `verified`

### Constant ledger

| Symbol | Value / expression | Source | Downstream requirement | OK? |
| --- | --- | --- | --- | --- |
| `2` | approximation factor | theorem statement | deviation bound | yes |

### Chunk status

`verified`


## Mirror Diff

N/A — not a mirror proof.

## Pass A: Constructive Summary

The constructive pass re-derived each local inequality and checked the relevant endpoint and quantifier cases. No unresolved local gap remained.

## Pass B: Adversarial Log

- Fresh independent chunk map: the isolated round-2 reviewer mapped the model, selection, transfer, packing, cap potential, deviations, continuation, and certificate before consulting this note.
- Three dangerous steps: source disappearance, heavy singleton preservation, and the succinct default rule.
- Attacks attempted: endpoint/zero-reach regimes, quantifier drift, coverage loss, inequality directions, finite-potential termination, labeled-placement collisions, and bit-length scope.
- Pass B verdict: `REFEREE_REPORT_round2_proof.md` found no S0--S3 issue; the three S4 clarifications were applied in `main.tex`.

## Verdict

closed: verified as written

- Justification: Pass A and the independent Pass B agree after the S4 wording repairs.
- Open blockers / next actions: only publisher template conversion and author metadata remain.

## Audit Trail

- Pass A session: 2026-10-24, primary reviewer.
- Pass B session: 2026-10-24, isolated GPT-6-sol xhigh reviewer (GPT-6.1-sol was at capacity).
- Linter run: batch command in `skills_sources/math-proof-review/scripts/lint-notes.py`.
- External lemma entries: `_external-lemmas.md`, N/A.
