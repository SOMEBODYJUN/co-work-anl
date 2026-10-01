# Research state — 2026-10-01

The current shared-catalog result is an **internally audited candidate theorem with a concrete algorithm**, not a refereed theorem or an instance-optimal solver. For explicit incidence, positive binary rational customer weights and two facilities allowed the **same** finite catalog, the manuscript claims a bit-polynomial construction of a pure-location, exact-customer-Nash subgame-perfect outcome within the golden ratio. Its returned certificate can be checked for a given instance independently of believing the universal existence proof. See [the model](MODEL.md), [the proof reconstruction](math/SHARED_PHI.md), and [the full source](manuscripts/shared_phi/main.tex).

The companion heterogeneous-catalog candidate gives an arbitrary-catalog factor-2 pure-continuation construction and a matching positive-integer family approaching 2. The narrower factor $2\cos(\pi/7)$ requires **both** a catalog of size at most two and pair overlap at most one. Neither theorem changes the scope of the other. See [heterogeneous proof map](math/HETEROGENEOUS.md).

## What is established inside the record

| Result | Actual evidence | Remaining boundary |
| --- | --- | --- |
| Shared $\phi$ upper | Integrated 25-page proof, fixed finite menu and exact-rational constructor, internal quantifier/strong-chord audits, 753 seeded certificates. | Independent reconstruction of arbitrary-cycle and polynomial local exchange; no external referee. |
| Heterogeneous 2 upper/lower | Separate manuscript, four-seed implementation, strict six-vertex lower family and internal audits. | Independent proof and literature-priority review. |
| Local chord and exact computation | Detailed local iff, exchange algorithm, support-cell enumeration, weak hardness reduction, pseudo-polynomial and exponential exact solvers. | Some reductions/complexity proofs lack independent external review; finite tests are not proof. |
| Certificate checks | Exact conditional customer deviations and actual first-stage deviations on concrete inputs. | The phi CLI wraps the same checker, and its free-text default metadata is ignored; a genuinely independent checker is pending. |

The [claim registry](CLAIMS.md) gives each statement its quantifiers and status; [evidence ledger](EVIDENCE.md) records finite checks separately. The interactive [mathematical hypergraph](research/index.html) and its [machine-readable graph](research/graph.json) encode *joint premises*, objections, implementation and source relations.

## Priority review tasks

1. Independently rederive the shared proof's full-catalog menu quantifier, arbitrary response-cycle star/anchor split, and the **two true uniqueness** deductions; read the manuscript §§2–14 and the [menu audit](evidence/audits/shared_menu_quantifiers.md).
2. Independently verify Appendix B's pair-local box-slice exchanges, pivot/flip bound, exact rational bit bound, and the three-mixer boundary. The earlier global quadratic-maximizer argument is historical and is not used by the algorithm.
3. Construct a global adversarial instance whose selected on-path witness invokes C. Existing 753 full-game tests selected 662 P, 88 E, 3 T and **0 C**; local C tests do not close this implementation coverage gap.
4. Implement a separate certificate checker with a defined continuation-default schema and test large rational bit lengths. The present CLI wrapper is useful for concrete certificates but shares checking logic with the producer.
5. Check current related literature and the common-catalog/rational interpretation of the published $\phi$ lower example before claiming sharpness or novelty.

## Open questions with the exact remaining scope

- Does the sparse heterogeneous $\rho=2\cos(\pi/7)$ bound persist with **both** catalogs arbitrarily large and every cross pair having at most one common customer? The existing theorem only covers at least one short catalog.
- Can the response-core principle be turned into a generally efficient algorithm when exact local minima are weakly NP-hard? The finite-menu proofs use extra geometry and do not furnish an abstract polynomial theorem.
- Which other nonlinear cost families preserve a useful customer equilibrium correspondence? The quadratic same-at-both-facilities identity works; arbitrary convex functions fail to preserve mixed NE.

The [failed routes](FAILED_ROUTES.md) include exact counterexamples and scope corrections. Source provenance, snapshots and historically superseded frontier notes are identified in [PROVENANCE.md](PROVENANCE.md). A usable input contract is in [USAGE.md](USAGE.md).
