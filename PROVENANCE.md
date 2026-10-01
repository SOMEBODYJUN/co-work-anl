# Source provenance and status of inherited assets

The second curation pass moved 58 imported assets by mathematical role. [The full old-to-new path manifest](research/path_migration.json) is versioned, and [ASSETS.md](ASSETS.md) ties each current claim to its precise input restrictions, unique implementation, controlling proof and finite evidence. [check_assets.py](research/check_assets.py) checks these relationships and rejects unclassified repository files. Ten old implementation paths and seven old test/audit paths remain as **thin compatibility entry points**, never duplicate implementations.

This curation read **each individual ZIP entry**, the integrated manuscripts, proof notes, scripts and recorded certificates. The two supplied snapshot ZIPs are delivery containers: the shared ZIP's 19 entries matched imported tracked files byte-for-byte; the heterogeneous ZIP's 24 entries matched imported tracked files after the original two_facility_research/ prefix became asym_research/. The ZIPs themselves are omitted from Git to avoid duplicate snapshots. The initial Git checkpoints are 4089160 (shared import), 9ede373 (heterogeneous import) and 70026ad (certificate-verifier fixes). Earlier versions remain recoverable with git show or git log.

## Authority order and new organization

| Question | Read first | Underlying proof or executable source |
| --- | --- | --- |
| Model and quantifiers | [MODEL.md](MODEL.md) | The two manuscripts' formal model sections. |
| Shared finite-menu theorem | [math/SHARED_PHI.md](math/SHARED_PHI.md), [CLAIMS.md](CLAIMS.md) | [manuscripts/shared_phi/main.tex](manuscripts/shared_phi/main.tex) controls all theorem corrections; [facility_spe/shared_phi.py](facility_spe/shared_phi.py) implements the menu. |
| Local game / strong chord | [math/LOCAL_GAME.md](math/LOCAL_GAME.md) | The shared manuscript Appendices A–B, [strong chord note](math/proofs/shared/strong_chord_existence.md), and [constructor](facility_spe/local/strong_chord.py). |
| Heterogeneous upper/lower | [math/HETEROGENEOUS.md](math/HETEROGENEOUS.md) | [manuscripts/heterogeneous/main.tex](manuscripts/heterogeneous/main.tex), [lower family proof](math/proofs/heterogeneous/tight_two_lower.md), [four-seed solver](facility_spe/heterogeneous_two.py). |
| Exact optimization / extensions | [math/COMPUTATION_AND_EXTENSIONS.md](math/COMPUTATION_AND_EXTENSIONS.md) | [hardness proof](math/proofs/local/hardness.md), [exact methods](math/proofs/local/exact_methods.md), [overlap proof](math/proofs/exact/bounded_overlap.md), [extension proof](math/proofs/extensions/quadratic.md). |
| Evidence and objections | [EVIDENCE.md](EVIDENCE.md), [FAILED_ROUTES.md](FAILED_ROUTES.md) | Tests, JSON certificates and adversarial audit notes retain their exact original context. |

## Superseded assertions still present in historical source notes

- The older [global existence candidate](history/proofs/shared/existence_candidate.md) discusses true local minima and an unused leveling selection. Its detailed inequalities are historical derivations; the **fixed-menu bit-polynomial** theorem is controlled by the integrated manuscript. Never silently import the old exact-minimum computation into the algorithm.
- The [strong chord note](math/proofs/shared/strong_chord_existence.md) includes an existence-oriented quadratic maximization. The current implementation requires only the **pair-local** exchange theorem in Appendix B; pair-local need not be globally optimal.
- [history/proofs/heterogeneous/sparse_lower_prior.md](history/proofs/heterogeneous/sparse_lower_prior.md) §§1–10 contain a restricted sparse lower analysis; its §11 states an obsolete unrestricted interval. The later [positive-integer two lower family](math/proofs/heterogeneous/tight_two_lower.md) supersedes it.
- [history/proofs/heterogeneous/universal_two_prior.md](history/proofs/heterogeneous/universal_two_prior.md) explores a larger pure menu; the current four-seed full-catalog proof is in the integrated heterogeneous manuscript.
- [math/proofs/local/exact_methods.md](math/proofs/local/exact_methods.md) §6, [history/proofs/local/mitm_research_log.md](history/proofs/local/mitm_research_log.md) §8 and [math/proofs/local/chord_exchange.md](math/proofs/local/chord_exchange.md) §7.3 retain dated “polynomial phi open” text. The manuscript now contains an **internally audited candidate** algorithm, not a peer-reviewed resolution. The ring README also refers to absent historical benchmark files; its documented commands should be checked against present scripts.
- [history/handoffs/heterogeneous.md](history/handoffs/heterogeneous.md), [upper.md](history/proofs/heterogeneous/upper_prior.md), [general_four_cycle.md](history/proofs/heterogeneous/four_cycle_prior.md) and [general_six_cycle.md](history/proofs/heterogeneous/six_cycle_prior.md) show proof development. Read their claims in the context of the later full manuscript.

Historical files are retained as **provenance and audit evidence**, not placed in the current navigation as parallel theorem authorities. Git history preserves prior snapshots and corrections. The [interactive graph](research/index.html) cites individual mathematical sources for each joint-premise edge instead of linking every raw file as an undifferentiated node.
