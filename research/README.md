# Hypergraph schema and maintenance

[assets.json](assets.json) supplies the companion claim-to-proof/code/test/record mapping with exact input conditions; [path_migration.json](path_migration.json) records each moved source. Run [check_assets.py](check_assets.py) after adding or relocating research material. The graph and asset manifest answer different questions: mathematical inference versus where its implementation and evidence live.

The [viewer](index.html) is generated from [graph.json](graph.json). Each **node** is a mathematical definition, lemma, claim, counterexample, obligation, evidence item or implementation artifact. Each **hyperedge** records a typed relationship from a set of premise node IDs to one conclusion node ID. For a derives edge, all listed premises are required together; a single-premise attack or finite test is intentionally a different kind of relation.

| Field | Meaning |
| --- | --- |
| node.id / edge.id | Stable reference in notes and reviews. Canonical theorem IDs match [CLAIMS.md](../CLAIMS.md). |
| node.kind / track / status | Mathematical role, research branch, and level of established evidence. “Internal candidate” is not external review. |
| node.detail / refs | Exact mathematical meaning and current sources, with paths relative to repository root. |
| edge.kind | derives: logical argument in source; attacks: exact rejected overextension; checks: bounded executable observations; implements: program correspondence; limits: unresolved work. |
| edge.premises / conclusion | Joint input set and target; checks and limits never imply a universal theorem. |
| edge.statement / status / refs | The inference's own scope, provisional status and cited proof/evidence location. |

The graph is deliberately **not** a picture of old file links. Sources are attached to mathematical statements, and an individual old note may substantiate multiple nodes without becoming a theorem node itself. When a claim changes catalog quantifiers, cost symmetry, participation, equilibrium selection, or input encoding, create a new claim version and adjust every affected hyperedge. Retain counterexamples and historical proof attempts in [PROVENANCE.md](../PROVENANCE.md).

Regenerate and validate locally:

    python3 research/build_map.py
    python3 research/build_map.py --check
    python3 research/check_assets.py

The generator checks IDs, all premise and conclusion references, every source path, node connectivity and that each claim has an incoming edge. The resulting HTML embeds all data and assets: it opens directly as a local file with no server or external JavaScript. GitHub's repository preview displays HTML source; download the file to use its filters and node inspector in a browser. [README.md](../README.md) summarizes the principal joint mathematical dependencies without JavaScript.
