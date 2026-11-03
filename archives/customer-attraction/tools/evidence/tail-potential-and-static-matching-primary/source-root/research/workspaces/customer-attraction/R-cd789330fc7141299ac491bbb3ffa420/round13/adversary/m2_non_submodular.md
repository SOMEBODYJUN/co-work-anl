# The optimized two-tail potential M2 is not submodular

2026-10-25. Exact function-level counterexample in the original unit-client
common-catalog model. This does not assert an equilibrium and does not refute
ONE-GAP or five-provider half coverage. External review and novelty are unknown.

Take disjoint unit-client blocks L,R,Z of sizes 6,6,9. The common catalog is
`A=L`, `B=R`, `C=L union R`, `D=Z`. All four themes are different. Define
`Phi(profile)=sum_x H_(client load)` and
`M2(q)=max_(T,S in catalog) Phi(q+T+S)`.
Use the legal ordered prefix q=(D). Its depth is one; the prefixes obtained
by adjoining A, B, or A then B have depths two, two, and three, respectively.
They therefore all fit in the five-provider model with two tail additions.

| Prefix | best CC potential | best CD potential | DD potential | M2 |
| --- | ---: | ---: | ---: | ---: |
| D | 27 | 51/2 | 33/2 | 27 |
| D,A | 29 | 57/2 | 45/2 | 29 |
| D,B | 29 | 57/2 | 45/2 | 29 |
| D,A,B | 31 | 63/2 | 57/2 | 63/2 |

Only CC,CD,DD need be considered for the maximum: replacing any tail A or B
by its legal superset C weakly increases every client load, and H is increasing.
The exact certificate nevertheless evaluates all ten unordered pairs, including
repeats, separately at all four prefixes.

Consequently

`M2(q+A)+M2(q+B)-M2(q)-M2(q+A+B)=-1/2<0`.

Equivalently, adding A increases M2 by 2 at q and by 5/2 at q+B. Thus even on
legal prefixes of the relevant depths, one cannot apply a submodular valid-
utility argument to the derived marginal `Q_i(P)=M2(P)-M2(P minus i)` without
a further restriction. This counterexample does not settle whether any such
restriction holds along particular actual SPE paths.

The standalone Fraction checker `audit_m2_non_submodular.py` produces the
frozen forty-pair evidence `m2_non_submodular_exact.json` without importing the
SPE solver or any prior audit.
