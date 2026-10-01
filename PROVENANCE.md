# Source provenance and status of inherited assets

This curation read **each individual ZIP entry**, the integrated manuscripts, proof notes, scripts and recorded certificates. The two supplied snapshot ZIPs are delivery containers: the shared ZIP's 19 entries matched imported tracked files byte-for-byte; the heterogeneous ZIP's 24 entries matched imported tracked files after the original two_facility_research/ prefix became asym_research/. The ZIPs themselves are omitted from Git to avoid duplicate snapshots. The initial Git checkpoints are 4089160 (shared import), 9ede373 (heterogeneous import) and 70026ad (certificate-verifier fixes). Earlier versions remain recoverable with git show or git log.

## Authority order and new organization

| Question | Read first | Underlying proof or executable source |
| --- | --- | --- |
| Model and quantifiers | [MODEL.md](MODEL.md) | The two manuscripts' formal model sections. |
| Shared finite-menu theorem | [math/SHARED_PHI.md](math/SHARED_PHI.md), [CLAIMS.md](CLAIMS.md) | [phi_n_manuscript/main.tex](phi_n_manuscript/main.tex) controls all theorem corrections; [common_phi_algorithm.py](common_phi_algorithm.py) implements the menu. |
| Local game / strong chord | [math/LOCAL_GAME.md](math/LOCAL_GAME.md) | The shared manuscript Appendices A–B, [strong chord note](strong_cross_chord_arbitrary_n_proof.md), and [constructor](astra_local/construct.py). |
| Heterogeneous upper/lower | [math/HETEROGENEOUS.md](math/HETEROGENEOUS.md) | [asym_research/paper/main.tex](asym_research/paper/main.tex), [lower family proof](asym_research/tight_two_lower.md), [four-seed solver](asym_research/r_menu_solver.py). |
| Exact optimization / extensions | [math/COMPUTATION_AND_EXTENSIONS.md](math/COMPUTATION_AND_EXTENSIONS.md) | [hardness proof](astra_alg/hardness_proof.md), [exact methods](astra_alg/exact_algorithms.md), [overlap proof](asym_research/bounded_overlap_theorem.md), [extension proof](astra_ext/results.md). |
| Evidence and objections | [EVIDENCE.md](EVIDENCE.md), [FAILED_ROUTES.md](FAILED_ROUTES.md) | Tests, JSON certificates and adversarial audit notes retain their exact original context. |

## Superseded assertions still present in historical source notes

- The older [global existence candidate](phi_global_proof_candidate.md) discusses true local minima and an unused leveling selection. Its detailed inequalities are historical derivations; the **fixed-menu bit-polynomial** theorem is controlled by the integrated manuscript. Never silently import the old exact-minimum computation into the algorithm.
- The [strong chord note](strong_cross_chord_arbitrary_n_proof.md) includes an existence-oriented quadratic maximization. The current implementation requires only the **pair-local** exchange theorem in Appendix B; pair-local need not be globally optimal.
- [asym_research/lower.md](asym_research/lower.md) §§1–10 contain a restricted sparse lower analysis; its §11 states an obsolete unrestricted interval. The later [positive-integer two lower family](asym_research/tight_two_lower.md) supersedes it.
- [asym_research/universal_two.md](asym_research/universal_two.md) explores a larger pure menu; the current four-seed full-catalog proof is in the integrated heterogeneous manuscript.
- [astra_alg/exact_algorithms.md](astra_alg/exact_algorithms.md) §6, [astra_ring/README.md](astra_ring/README.md) §8 and [astra_local/local_chord_algorithm.md](astra_local/local_chord_algorithm.md) §7.3 retain dated “polynomial phi open” text. The manuscript now contains an **internally audited candidate** algorithm, not a peer-reviewed resolution. The ring README also refers to absent historical benchmark files; its documented commands should be checked against present scripts.
- [asym_research/README_HANDOFF.md](asym_research/README_HANDOFF.md), [upper.md](asym_research/upper.md), [general_four_cycle.md](asym_research/general_four_cycle.md) and [general_six_cycle.md](asym_research/general_six_cycle.md) show proof development. Read their claims in the context of the later full manuscript.

Historical files are retained as **provenance and audit evidence**, not placed in the current navigation as parallel theorem authorities. Git history preserves prior snapshots and corrections. The [interactive graph](research/index.html) cites individual mathematical sources for each joint-premise edge instead of linking every raw file as an undifferentiated node.
