# RA10-P001-U01 candidate record (visual only)

- **Issue id:** `RA10-P001-U01`
- **Page / source:** RA10 page 1, rendered from `co-work-anl/input/pdf/实分析10(1).pdf`.
- **Directed crops:**
  - `visual/crops/RA10-P001-U01-directed.png` — 600-dpi heading + proposition + blue `proof` context.
  - `visual/crops/RA10-P001-U01-tight.png` — 600-dpi proposition-line crop.
  - `visual/crops/region-42-p1-r2c2.png` — middle-row/second-column 42-region crop (coordinate record in `crops/README.md`).
- **Observed marks:** Heading visibly reads as `B(X) → B(…R)` followed by `Borel 可测`. The next line begins `prop.` and contains a clearly finite/countable-looking qualifier, then a phrase whose last characters look like a measurability conclusion. Below it is a blue `proof`; the following formulas visibly use finite indexed sums, scalar coefficients, sets and `χ` indicators for `f` and `g`.

## Candidates

| rank | candidate reading | visual/math support | unresolved point |
|---|---|---|---|
| A (preferred, medium) | “有限个可测函数的线性组合仍可测” (finite linear combinations of measurable functions are measurable). | The line’s middle strokes look like a finite qualifier plus “函数”; the lower `f=Σ…`, `g=Σ…` formulas and subsequent example are exactly the setup for closure under finite linear combinations. | The Chinese connective before the measurability phrase is joined; “线性组合” is an interpretation, not a guaranteed character-by-character reading. |
| B (alternative, medium-low) | “可测函数的有限和、积（及数乘）仍可测” (finite sums/products/scalar multiples of measurable functions remain measurable). | Same closure context and the visible coefficient/indicator formulas support this broader statement. The proposition line may contain two operation nouns rather than the single phrase “线性组合”. | Product symbol/operation is not visibly secure; do not write a definite product claim into the source layer. |

## Decision / handoff

Keep the source transcript neutral at this unit: preserve the visible `prop.` line, the explicit `Borel 可测` heading, and the `f,g` finite-sum formulas. If a study layer needs a theorem statement, use candidate A as a **blue, explicitly labelled standard completion**, while retaining candidate B in the uncertainty ledger. Do not replace the black source text with either candidate without a second directed scan.
