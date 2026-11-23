# Current-runtime implementation notes

Read-only audit of `/workspace/scratch/b46ebabc059e/co-work-cone-boss2`. Read root `AGENTS.md`, current runtime/main/review prompts, `research/agent-design/HYPEREDGE_WORKFLOW.md`, spec template, actual `work.py`, `tools/research_runtime.py`, `tools/research_studio.py`, `tools/registration.py`, and sample current registry records. No repository edits, Git mutations, credentials or network operations performed.

## Main conclusions

1. The new archive and two future assignments can use the existing research runtime unchanged. Do not revive phase workflows, boards, registration-task/map queues, queue baselines or stage identities. `research/IMPLEMENTATION.md` contains historical commands and stale board language; current root `AGENTS.md` overrides them. The actual current CLI is the authority for executable commands.
2. Startup and studio initialization are preparation, never theorem success. `start` explicitly returns `research_status: runtime-ready-problem-not-started`; studio initialization returns `agents_launched: 0`. `research check` returns `structure-valid-not-a-mathematical-verdict`. A passed check, accepted edge, reviewed artifact, structural frontier closure, or successful push cannot set G1–G8 PASS.
3. Keep **INTAKE_READY** separate from **THEOREM_PASS**. The latter means all eight mathematical/document gates pass. A fully prepared intake can expose a genuinely open bridge, a blocked source download, or a target already known; report those outcomes accurately.

## Smallest useful archive

Use `archives/relative-mk-cone/README.md` as the entry, with exact original scope, links to the target/definition contract, the two prompts, current status, real RUN IDs when created, and accurate next action. A practical minimal layout is:

```text
archives/relative-mk-cone/README.md
archives/relative-mk-cone/问题--问题.md
archives/relative-mk-cone/state/定义/relative-cones-and-strong-domain--定义.md
archives/relative-mk-cone/prompts/pro1-intake.md
archives/relative-mk-cone/prompts/pro2-proof.md
archives/relative-mk-cone/workspaces/BossN/             # created by start
research/workspaces/RUN/spec.json                      # real per-RUN contract
research/workspaces/RUN/{main,independent,informed-a,informed-b}/...
research/workspaces/RUN/records/...
research/runs/RUN/...                                  # created by studio
tools/evidence/relative-mk-cone/...                     # acquired sources + provenance
map/edges/relative-mk-cone/...                          # actual relation declarations
```

Do not create an empty `state` hierarchy, dummy mathematical objects, sample edges, author IDs, journals pretending research happened, or dummy six-deliverable manuscripts merely to populate the archive. Create substantive files when their contents exist. The target may be registered as `open` later; registration is not a prerequisite to opening a RUN. Formal math returned by a bound studio must have object bodies under this archive's `state/` (studio promote enforces this). Definition and problem files must contain only the original input contract, not post-intake proof hints; independent receives them.

The six mandatory Pro2 outputs should have one specified location, e.g. `archives/relative-mk-cone/workspaces/BossN/manuscript/`: `main_theorem.tex`, `proof.tex`, `literature_audit.md`, `counterexample_audit.md`, `research_paper.tex`, `verification.md`. Pro2 creates real contents even if FAIL; no invented proof section to fill a template. Final formal Markdown objects can point to these files as precise evidence. No duplicate registry or alternative truth store.

## Actor selection and executable startup

`start` requires an explicit actor; it does **not** allocate one. `tools/research_studio.py` additionally requires `Boss[1-9][0-9]*`. `workspace_init` detects an existing actor's incompatible instance in the chosen archive and requires `--resume` only for a genuine continuation. There is no repository-wide atomic Boss-number allocator in the inspected code. Thus do not declare Boss2/Boss7/etc. unused from a sparse directory listing. Use the explicitly assigned actor for a continuation, or select/reserve an actor against the latest complete workspace/RUN metadata and pass it explicitly; distinguish that local collision check from a global uniqueness guarantee. A new archive and a different already-bound save require an independent clone.

Actual startup interface (replace all capitalized arguments with real values; credential path remains outside clone):

```sh
python /ACTUAL/BOOTSTRAP/work.py --repo /ACTUAL/NEW/CLONE start --actor BossN --role boss --branch rebuild/research-v2 --save relative-mk-cone --create-archive --token-file /ACTUAL/OUTSIDE/CREDENTIAL.txt
```

Once the archive is published, future starts omit `--create-archive`. True same-identity continuation adds `--resume`; do not use it to bypass a collision. Enter the returned clone and use its root `work.py`. Expected remote must match actual configured origin; default in current code is `https://github.com/SOMEBODYJUN/co-work-anl.git`.

## Valid spec

Copy `research/agent-design/spec-template.json` directly into `research/workspaces/RUN/spec.json`, remove `template_only`, fill real refs and no placeholders. There is no nested `math_spec`. Required operational fields are `problem_id`, `problem`, `definitions`, `obstacles`; use explicit `collaboration_scope: archives/relative-mk-cone`, `seed_ids: []`, `hops: 0` until genuinely relevant IDs are established. Preserve target_contract and useful execution notes. Every reference is exactly `{path,sha256}` plus optional exact unique Markdown `section`; SHA is over the **entire file's raw bytes**, even when section selected. No line-number anchors, URL anchors or section-only hashes. A problem already under archives binds the deepest archive, which must agree with the spec and clone.

```sh
python work.py research studio init RUN --spec research/workspaces/RUN/spec.json --expect-branch rebuild/research-v2 --expect-remote https://github.com/SOMEBODYJUN/co-work-anl.git
python work.py research studio status RUN --session-tag ACTUAL-SESSION
```

Do not mutate original inputs after init; saved packets and spec pins preserve their exact versions. A changed mathematical target/model/input contract gets a new spec/RUN. Each new Boss needs an independent RUN spec even for the same target.

## Pro1 prompt requirements

Pro1 is **one continuous substantive assignment**: acquire the relevant primary literature and exact versions → read and identify precise mathematical objects → prepare/publish justified ALL hyperedges. These are functions within a research assignment, not revived historical phases. Do not stop after creating a bibliography or delegate the remainder to an unstarted future phase. Scope is enough verified material for this target, not an impossible claim to exhaust all literature.

Require source provenance with title/authors, publication/preprint version, date, stable URL/identifier, downloaded path, SHA, theorem/definition numbers, and exact pages/sections. Distinguish metadata/search hits from actual readable primary text. A failed/unavailable download is a named obligation, never a fabricated local PDF. Extract exact definitions, hypotheses, quantifiers, conclusions, cited dependencies and proof location. Keep article excerpts/copyright handling appropriate; mathematical summaries must preserve scope. Avoid inventing a node for every reference or ordinary proof step.

The target is the strong relative Morrison–Kawamata cone statement for **all original terminal Calabi–Yau fibre spaces of relative dimension ≤2, without movable-cone nondegeneracy**. Identify the exact source/version of Definition 3.4 and preserve its real strong-domain condition. Fix the base field, projectivity/base assumptions, numerical spaces, cones (open/closed/effective variants), group and action, equivalence of canonical triviality, rational polyhedrality, and interior convention from the original contract. Never silently add Q-factoriality, smoothness, strict convexity, a quotient by lineality, a group quotient, or a weaker covering statement. If such a reduction is useful, register the missing reduction bridge as an obligation.

For actual logical relations: all jointly needed theorems, hypotheses and transfer bridges belong to one ALL support; independent complete proofs are different alternative edges. Open premises require `relation_mode: conditional`; a correct conditional implication can be accepted after real review while its debt stays open. A mere proposed heuristic relation must remain proposed; citations/context links cannot act as proof. A local result uses `contribution:{result,remaining}`; complete target implication uses `whole_result`. Do not label a route whole when the degeneracy or disjoint-interior bridge remains unpaid. Evidence of a literature theorem does not by itself prove its application to every original object.

Pro1 completion report: INTAKE_READY / NOT_READY / BLOCKED, accurate source and object/edge refs, exact obligations and next action, and no theorem claim. An honest prepared conditional route may be intake ready if the acquisition/reading/catalog/relation work is actually complete and explicitly exposes its missing proof. Unavailable essential text or an unaudited central theorem is not intake ready.

## Current registration and edge interfaces

Canonical registry schema is 2 with `objects`, `materials`, `edge_files` (existing registry also preserves `retired_objects`). Object required fields: `object_id`, positive integer `version`, `title`, `kind`, `truth_status`, `model`, `statement`, `quantifiers`, `assumptions` list, `scope`, `objections`, `body`, `evidence` list, `sources` list. Truth values: definition/proved/conditional/conjecture/open/refuted/finite/unassessed. Every live body needs a matching `materials` row with disposition `objects` and its owner; attachments need owners whose evidence actually refers to the bytes. Sources strings do not replace body/evidence refs. Preserve identity/version; changed records increment version.

A current batch is `{schema:2,objects:[...],materials:[...],edge_files:[]}` in this RUN workspace. It is a **delta**, not a replacement canonical registry: never pass that delta directly to `research register` in a live populated repository. Studio promote merges the reviewed batch with the current canonical registry and creates a complete guarded candidate.

An edge needs `edge_id`, `kind`, `status`, nonempty `source_ids` and `target_ids`, `premises_mode:"all"`, `relation_mode`, `conditions`, `roles` covering every endpoint exactly, `explanation`, `scope`, and nonempty precise `evidence`. Accepted edges additionally need real `reviewed_by`, `review_note`, and current generated `endpoint_pins`, `evidence_pins`, `review_digest`. Accepted logical edges require a `whole_result` or `contribution`. Logical kinds: implies/refutes/specializes/transfers/equivalent_to; contextual kinds: motivates/cites/sourced_from/implements/checks/corrects/supersedes. An accepted unconditional logical edge can only have definition/proved source objects. Do not hand-invent pins.

```sh
python work.py research search 'precise target terms' --model 'actual model'
python work.py research show OBJECT-ID --body
python work.py research context TARGET-ID --edge EDGE-ID --hops 0
python work.py research frontier TARGET-ID --edge EDGE-ID --expect-branch rebuild/research-v2
python work.py research edge-bind map/edges/relative-mk-cone/EDGE.json --batch-file research/workspaces/RUN/records/registration-batch.json --write
python work.py research edge-check map/edges/relative-mk-cone/EDGE.json --batch-file research/workspaces/RUN/records/registration-batch.json
```

Finalize mathematical edge wording and real review metadata before binding; later changes need re-review/rebind. `--batch-file` checks new endpoints in memory without canonical admission. `context --hops 0` still retains complete selected ALL support. A selected conditional edge's free-text conditions are not automatically paid by context/frontier.

For mature results use existing artifact → freeze → real nonauthor review → review record → promote; JSON schemas and exact command forms are in `HYPEREDGE_WORKFLOW.md`. `publication_refs` must include the final batch and edge bytes before freeze. Promote `claim_scope:"local-result"` for intake results or a partial theorem. `whole-target` requires an established artifact, no unpaid debt, and explicit reviewed discharges for every inherited contribution remaining; even then G1–G8 still need genuine checking.

```sh
python work.py research studio artifact RUN --record-file research/workspaces/RUN/records/artifact.json
python work.py research studio freeze RUN --artifact RESULT-ID --freeze-id ACTUAL-REV
python work.py research studio review RUN --record-file research/workspaces/RUN/records/review.json
python work.py research studio promote RUN --record-file research/workspaces/RUN/records/backflow.json
```

Main serially runs promote's returned register/edge-check/check/build commands and checkpoint with its returned immutable `--review-plan` path. Report remote saved only after actual `pushed`. Ordinary useful drafts use journal/save and checkpoint without pretending formal admission. Use `research check/build` **without `--final`** for new increments.

Sparse checkout is a real boundary: `search` reads metadata with `verify=False`; selected reads check their actual refs. But promote ultimately calls `runtime.load` over the entire merged registry, as do register/check/build. Missing canonical files must be materialized before full validation/publication. Do not replace the full canonical registry with a local subset, omit old unrelated objects, use fake hashes, or reopen old stage baselines to make a sparse check pass.

## Pro2 prompt and independent-input requirements

Pro2 must attack the unchanged theorem, use the acquired graph and actual primary texts, and persist with meaningful proof/counterexample work. A preparation success, partial lemma, conditional reduction or absent counterexample never closes the theorem. Record failures precisely; a counterexample to an auxiliary bridge is not automatically one to the original conjecture. Every G gate is separately PASS/FAIL with evidence and unresolved obligations; overall PASS iff all eight PASS:

| Gate | Required condition |
|---|---|
| G1 | Original target not already completely proved as of the audit date; no-hits search cannot certify novelty. |
| G2 | All original objects covered, with no extra assumptions. |
| G3 | Full covering `Gamma Pi = C`. |
| G4 | Actual strong Definition 3.4, including no nonidentity interior overlap. |
| G5 | Full degenerate case, including lines in the closed movable cone. |
| G6 | No proof gaps. |
| G7 | Rigorous independent check, with no unproved computation, conjecture or circularity. |
| G8 | Complete English LaTeX draft with accurate references. |

G1 must use an explicit dated audit and source versions, recognizing publication/preprint chronology; do not weaken the target to manufacture novelty. If the exact target is already known, report G1 FAIL with source, scope and proof location. For G3/G4 distinguish covering, rational polyhedrality and strong nonoverlap, and check the precise group action/identity convention from the fixed definition. For G5 no unproved passage to quotient or lifting of a quotient domain. For G6/G7 preserve ALL conjunctions, common witnesses, condition debt, conditional literature results, equivalence cycles and finite/general distinctions.

The current studio has main/full, independent/obstacle, informed-a/full idea, informed-b/full execution. Only actual Work launches count. Record actual agent ID, session tag and launch configuration with `studio line`; current repo default worker settings are gpt-6.1-sol / ultra / fresh history, subject to user-selected settings. The independent slot gets only exact original problem, definitions, preallowed obstacles and its own notes—not Pro1 literature, registry edges, Main's route, manuscript or other-line results. Use `fork_turns:none`. A read ledger is optional but if present independent entries must be exact refs from its saved obstacle packet or its own workspace. Shared filesystem is not access control. If it sees informed material, preserve contamination details and stop calling its later reasoning original-input independent; use a fresh nonauthor informed reviewer for G7 rather than silently repurposing independent. A fresh reviewer must actually read frozen proof/evidence; an accepted review JSON is not itself rigorous checking.

Pro1 and Pro2 prompts should explain resume/status, ordinary journal saving, exact breakpoints and fresh continuation, meaningful original-scope stop conditions, and how to report a real tool/context/source boundary. Never promise unattended background research, certify an open theorem in a prompt, force proof despite a real gap, or claim verification from eight checked boxes.
