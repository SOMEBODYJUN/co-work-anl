# Canonical Python implementation

Run modules from the repository root with Python 3 and no third-party packages, or use the compatibility commands in [USAGE.md](../USAGE.md). This directory is the **only implementation copy**; old script paths contain import/CLI forwarding only.

| Module | Claim and exact domain |
| --- | --- |
| [shared_phi.py](shared_phi.py) | SC-PHI-A: same nonempty site catalog, positive rational weights, linear realized-load costs, exact independently mixed customer NE. Constructs a factor at most phi **within its fixed menu**. |
| [heterogeneous_two.py](heterogeneous_two.py) | HC-2-UP: arbitrary two nonempty catalogs, pure exact customer NE at all selected continuations, factor at most 2. |
| [local/pure.py](local/pure.py) | Shared guarded repair with the protected-lower-side quota invariant. Both finite menus import this same routine. |
| [local/strong_chord.py](local/strong_chord.py) | LOCAL-CHORD-POLY: local quota witness under the reach/common-mass/largest-atom conditions in [LOCAL_GAME.md](../math/LOCAL_GAME.md). |
| [exact/bounded_overlap.py](exact/bounded_overlap.py) | EXACT-KAPPA: all independent mixed NE support cells; computes a given instance's optimal factor with exponential dependence on pair overlap. |
| [exact/single_overlap.py](exact/single_overlap.py) | Exact optimization when each cross pair has at most one common customer; the *universal* rho theorem additionally needs one catalog of size at most two. |
| [exact/threshold_dp.py](exact/threshold_dp.py) | DP-W: local integer-weight spectrum in pseudo-polynomial total-weight time. |
| [exact/mitm.py](exact/mitm.py) | MITM-EXACT: unrestricted local/full-game optimum with exponential worst-case time. |

Certificate fields differ across algorithms because they encode different theorems. A short checked certificate proves the factor attained **for that input**. Universal existence and complexity statements require the relevant manuscript proof; exact instance optimality additionally requires full support enumeration. [ASSETS.md](../ASSETS.md) ties each module to its hypotheses, proof and evidence.
