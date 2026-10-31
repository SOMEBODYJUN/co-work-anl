# Omitted-deletion exact certificate replay

This package preserves the three assigned source versions from the five-player, five-theme omitted-customer family:

| source ID | source path | role | SHA-256 |
|---|---|---|---|
| `a0b06b0a268963c3f318` | `omitted_deletion/certificate.json` | complete t=1 strategy certificate | `4270fc3848069fcf889d1e1adb14e5814560f5f6b4c2de4e68b4aed3b6518d86` |
| `c6688be8f0cdb447f2d8` | `omitted_deletion/threshold_certificate.json` | complete t=3/4 threshold certificate | `04dd566cfa5fe9779698949bf1424fa18107ec3d8e31f13fca8557b5f902e927` |
| `9b1e0ec175c74ebb0a67` | `omitted_deletion/verify.py` | exact parametric verifier | `86e785d0bfc5f314ffbcff0f06d20959c18d62ec7de9115c84d287b82d16071e` |

The two certificate files, `source/reduced.json`, `source/reduced_input.json`, and the original `verification.json` are byte-for-byte preserved. The verifier was run once with the repository's exact Fraction SPE package against the original `reduced.json`. It returned exit 0, empty stderr, and `exact_parametric_family_verified` with 211 affine utility lines and 129 representatives. The generated t=1 and t=3/4 certificates are byte-identical to the assigned `certificate.json` and `threshold_certificate.json` respectively.

The replay confirms the fixed five-player/five-theme one-parameter family and its exact threshold mechanics. It does not claim a universal Q-CAG-HALF theorem, a claim beyond the preserved original source inputs, or an external certificate beyond the preserved source files.
