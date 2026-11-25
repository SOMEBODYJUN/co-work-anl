# RA11 visual candidate record

This is the independent visual candidate log, written after the full-page and all-84-tile pass. It records at least two candidates for each requested ambiguity and returns to the high-resolution crop before selecting a provisional visual reading. It is not a ledger or正文 edit.

## RA11-P001-U01 / RA11-ISSUE-01

- **Physical page / target:** page 1 (`p0001`), dyadic partition line in the upper-middle band; source-unit bbox is the full page `[0, 0, 3306, 4678]` at 400 dpi. The relevant writing lies in the left-to-center line immediately below “将 t=2^k 等分成 2^k 段” and continues toward the grid at the right.
- **High-resolution evidence:** `target-crops/RA11-P001-U01-formula-800dpi.png` (400-dpi source bbox `[80,700,2900,1800]`, rendered at 800 dpi) and `target-crops/RA11-P001-U01-grid-800dpi.png` (bbox `[2400,650,3306,1800]`, 800 dpi). Existing full-page 800-dpi reference: `autonomous-recovery/crops/p0001-f9cd5200fee2.png`.
- **Observed strokes/adjacency:** the set is written as `E_{k,j}=E((j-1)/2^k ≤ f < j/2^k)`; the denominator strokes are stacked `2` over `k`; the upper endpoint has a `j` over `2^k`. After the closing parenthesis there is a comma and a short sequence that visually ends at a superscripted `2^k` near the right side. The blue/red grid marks are annotations over an axis and do not form part of the formula.

### Candidate A (provisional strongest visual reading)

`j=1, …, 2^k`. The final visible terminal is a standalone `2` with a small superscript `k`, and the preceding short strokes are comma/ellipsis separators. The range is adjacent to the partition formula and agrees with the drawn `2^k` equal-bin grid.

### Candidate B (rejected but retained)

`j=1, …, k 2^k` (or a terminal `k·2^k`). This reading is suggested if a faint short stroke before the terminal `2^k` is interpreted as a separate `k`; however, that stroke is aligned with the comma/ellipsis baseline and lacks the clear tall `k` shape used elsewhere on the page.

### Forward check

With Candidate A, the intervals `[(j−1)/2^k, j/2^k)` partition the finite range used in the subsequent piecewise definition of `φ_k`, and the displayed bound `φ_k(x)≤f(x)<(k+1)`/the later `φ_{k+1}≥φ_k` argument follows. Candidate B would introduce `k·2^k` bins although the page’s sketch and subsequent `E_k` union notation use the dyadic `2^k` grid; no later line uses an extra factor `k`.

### Backward check

The later proof invokes the union of the dyadic cells and the endpoint error at most `2^{-k}`. That requires the terminal index to be `2^k` (or, at most, a dyadic index with no extra factor); the observed grid has `2^k`-style equal divisions. The back-check therefore favors Candidate A.

### Return-to-image result

At 800 dpi the rightmost superscript is a distinct small `k` over `2`; there is no connected tall `k` immediately before the terminal. Candidate A is the best source-faithful reading, confidence **0.78**. Candidate B remains documented because the comma/ellipsis stroke is faint. No 1200-dpi escalation was needed after the 800-dpi crop.

## RA11-P005-U01 / RA11-ISSUE-02

- **Physical page / target:** page 5 (`p0005`), Egoroff tail-set argument at the upper and upper-middle bands; source-unit bbox is full page `[0, 0, 3306, 4678]` at 400 dpi. The page-edge writing continues from the left into a long union/intersection formula.
- **High-resolution evidence:** `target-crops/RA11-P005-U01-tail-800dpi.png` (bbox `[40,500,3260,1900]`, 800 dpi), plus `...-left-tail-800dpi.png` (bbox `[0,500,1800,1600]`) and `...-right-tail-800dpi.png` (bbox `[1400,500,3260,1600]`). Existing full-page 800-dpi reference: `autonomous-recovery/crops/p0005-83b5632ca5ed.png`.
- **Observed strokes/adjacency:** the tail set is named `E_n(ε)`/`\bar E_n(ε)` beside a union over `k≥n`; the overbar, where present, is a long horizontal stroke above `E_n` and can be mistaken for a page-margin continuation. The set braces and the condition `|f_n(x)−f(x)|≥ε` are visibly connected; later lines contain nested unions/intersections and `m(·)=0`.

### Candidate A (provisional strongest visual reading)

`\bar E_n(ε)=⋃_{k=n}^{∞}{x∈E: |f_k(x)−f(x)|≥ε}` (barred tail-set symbol). The horizontal stroke over `E_n` continues with the same pen weight as the author’s other set bars, and the later intersection line uses the corresponding barred-tail notation.

### Candidate B (rejected but retained)

`E_n(ε)=⋃_{k=n}^{∞}{x∈E: |f_k(x)−f(x)|≥ε}` without a bar, with the apparent horizontal mark treated as a page-edge flourish/underline. This is syntactically possible because the union and threshold condition remain unchanged, but it does not account for the deliberate overbar stroke seen at the left of the symbol and repeated in the subsequent null-intersection line.

### Forward check

Candidate A makes the decreasing tail sets explicit: as `n` grows the union starts later, and the page then takes `m(⋂_{n=1}^∞ \bar E_n(ε))=0` / `lim m(⋃_{k≥n}E_k(ε))=0` before selecting `N(ε,δ)`. Candidate B can still yield the same measure estimate, but would leave the repeated bar strokes unexplained.

### Backward check

The later line writes a barred/intersection tail object before the measure-zero conclusion and then uses `U E_n(ε)` in the epsilon–delta selection. Reading the first tail object as barred is the only candidate consistent with the repeated horizontal mark and the notation transition.

### Return-to-image result

The 800-dpi left and right crops show a continuous overbar immediately above the `E_n` symbol; the line is not a stray margin stroke. Candidate A is the best source-faithful reading, confidence **0.84**. The crop is sufficient; no 1200-dpi escalation was needed.

## Unresolved visual reservations

The two provisional readings are handed to the mathematics and adversarial reviewers for independent forward/backward checks. Blank-looking overlap tiles listed in `blind-read.md` require mapping review; this visual agent did not alter source/target units, ledger, recovery, issues, or page checks.
