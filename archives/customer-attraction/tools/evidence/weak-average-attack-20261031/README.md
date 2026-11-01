# Strategic relay weak-average finite attack

This evidence package preserves the two assigned source versions and the four policy JSON inputs used by the script.

| assigned source | bytes | SHA-256 |
|---|---:|---|
| `5230e8814c0e4be3160c` `attack_weak_average.py` | 3461 | `2f5c8eae327bfbde074797d98e7c20f91c6e478fefee3aa5210ec80cfb842c04` |
| `3bef4b37dc76bc2265f9` `weak_average_attack.json` | 4476 | `7d1b3aa84216486b33305e55f322dbd23140cd79ebfd712bda002d452c881835` |

The driver was replayed in a path-preserving source tree with the four named policy inputs. It exited 0 with empty stderr and regenerated the frozen JSON byte-for-byte. The four fixed cases have `(histories, true IC rows, optimal portfolios)` counts `(259,1295,126)`, `(259,1295,126)`, `(43,215,56)`, and `(6,24,15)`. Their best LP objective gaps are respectively `1.0`, `1.0`, `1.5579710144927537`, and `1.0`; no negative gap was observed. The independent checker verifies the byte identity, history-count formula, portfolio-count formula, and nonnegative gaps.

The script's objective is the strengthened weak-average interface

\[
\sum_{i,j}V_{ij} \ge m(\operatorname{OPT}_m-W),
\]

on a fixed complete-policy cone. It imposes all ordered-history IC rows and requires the selected portfolio to dominate every portfolio in coverage. The result is a finite floating-point `scipy.optimize.linprog` diagnostic over four named policies. It supplies no LP dual, exact rational cone certificate, integer reconstruction, universal SPE quantifier, or six-player half theorem. The stored nonnegative gaps are evidence that these four targeted cones did not expose the proposed inequality, not a proof of the inequality.
