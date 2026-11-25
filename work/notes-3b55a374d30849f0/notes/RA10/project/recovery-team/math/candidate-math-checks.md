# RA10-P001-U01 — forward/backward mathematical checks

The checks below test mathematical coherence of each candidate against the visible symbols. A passing check means the candidate is a valid theorem/proof pattern and is compatible with the page; it does not prove that the unreadable handwriting intended that candidate.

## Candidate A: finite algebraic operations preserve measurability

### Forward check

Let `(X, Sigma)` be a measurable space and let `f_1,...,f_n : X -> R` be measurable. The product map

`F = (f_1,...,f_n) : X -> R^n`

is measurable. For a continuous operation `Phi : R^n -> R` (for example finite addition, subtraction, multiplication, `max`, or `min`), `Phi o F` is measurable because, for every Borel set `B`,

`(Phi o F)^(-1)(B) = F^(-1)(Phi^(-1)(B)) in Sigma`.

For the common finite-sum special case, measurable level-set checks also work directly:

`{x : max_j f_j(x) > a} = union_j {x : f_j(x) > a}`,

and analogous finite combinations follow from the sigma-algebra operations. A quotient is covered on the set where the denominator is nonzero, provided the intended statement includes that condition.

**Result:** PASS. The candidate is mathematically sound and naturally explains a proof with finite indexed expressions.

### Backward check from P001-U01

- The Borel/measurable map at the top is necessary context for Candidate A.
- The lower finite indexed and indicator/sum-like marks are compatible with a finite-operation proof.
- The visible `f^{-1}` can be the standard proof mechanism for a composition/operation claim, but the page does not expose enough of `Phi` or the exact operation list to force this reading.

**Evidence strength:** compatible but non-diagnostic. The finite union and explicit inverse-image marks have a more direct fit with Candidate B.

## Candidate B: inverse images of Borel sets and finite measurable-set closure

### Forward check

For a measurable function `f : (X, Sigma) -> (R, B(R))`, the definition gives

`B in B(R)  =>  f^(-1)(B) in Sigma`.

If `F_1,...,F_n in Sigma`, then the sigma-algebra axioms give

`union_(j=1)^n F_j in Sigma`.

Finite intersections follow by complements (or directly by repeated binary intersections):

`intersection_(j=1)^n F_j = (union_(j=1)^n F_j^c)^c in Sigma`.

For a union `E = union_(j=1)^n F_j`, membership can be checked pointwise as `x in E` iff `x in F_j` for at least one `j`, matching the visible arbitrary-`x` proof style. If the page is proving measurability of a function built from preimages, the same closure step applies after taking `f^(-1)`.

**Result:** PASS. This exactly accounts for the visible `f^(-1)`, finite `⋃`, and pointwise union argument.

### Backward check from P001-U01

- `B(X) -> B(R)` plus nearby “Borel/可测” is the expected ambient notation for a measurable map into the real Borel space.
- The displayed inverse-image expression is a direct match to the defining criterion.
- The finite union sign, finite upper index, and arbitrary-point wording are direct matches to closure of measurable sets under finite unions; intersections are plausible but not forced if their glyph is unclear.
- The lower indexed decompositions can be intermediate set-family notation rather than a separate algebraic-operation theorem.

**Evidence strength:** strong semantic fit, while exact title and whether finite intersections are explicitly named remain unresolved.

## Comparative decision

Candidate B is the preferred recovery for the semantic audit because it requires fewer unreadable assumptions: every key visible structure (`B(X)`, Borel, `f^{-1}`, finite `⋃`, and a pointwise membership argument) has a direct role. Candidate A remains a live alternate because the lower sum/indicator-like notation could indicate finite algebraic operations. Preserve both until visual adjudication; do not insert either as an exact transcription solely from these checks.
