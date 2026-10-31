# Sharp approximation for two facilities with heterogeneous location sets

- `main.tex`: standalone English LaTeX source; no external figures or bibliography database.
- `main.pdf`: compiled 17-page manuscript.
- `build.sh`: two-pass build, including a local-format fallback for the minimal research environment.
- `main.log`: final LaTeX log.
- `preview/`: final rendered pages and a contact sheet used for visual checking.

On a normal TeX Live installation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

In the supplied workspace, run `./build.sh`. It writes only local outputs and does not modify the TeX installation. Standard packages include AMS math/theorems, Latin Modern, geometry, microtype, enumitem, booktabs, and hyperref.

## Results included

1. **Arbitrary heterogeneous catalogs: sharp universal factor 2.** The algorithm constructs pure facility locations and exact pure customer continuations with `O(N1 N2 (n+1)^2)` rational arithmetic operations and polynomial bit complexity.
2. **At most four pure witnesses per layout.** Guarded repair is applied to the two all-on-one-side seeds and the two seeds isolating the maximum-weight common customer. The completeness proof chooses a globally maximum cycle-visible customer using `(weight, -ID)` tie breaking and proves it is the predesignated common customer on every cycle edge.
3. **Complete proof for alternating cycles of arbitrary length.** Both branches use full global response maxima and legal opposite-color chords; the large branch establishes a customer-weight invariant and propagates it through both colors.
4. **Sharp undirected lower bound.** Six vertices with positive integer weights give exact optimum `2 - 18/(M+14)`, with unique customer NE and CCE at every layout.
5. **Sharp overlap-one refinement.** With at most one common customer per pair and at most two choices on one side, the optimal universal factor is `2 cos(pi/7)`, including tied reaches and a fixed pure continuation algorithm. This refinement is not claimed for arbitrary catalog sizes on both sides.
6. **General closed-response-core lifting.** The two-leader reduction applies to independently selectable exact continuation equilibria, provided payoff minima are attained.
7. **Increasing customer costs.** Both sharp guarantees extend to customer-specific strictly increasing realized-load costs. The manuscript does not assert preservation of arbitrary mixed equilibrium sets.
8. **FPT exact optimization appendix.** For linear costs and arbitrary catalogs, full ternary support enumeration computes the exact rational optimum and certificate in time exponential only in maximum pairwise customer overlap.

## Prior-work positioning

The manuscript directly acknowledges that IJCAI 2024 Observation 4 already states a general k-approximation bound. It distinguishes that statement from the accompanying common-location argument, which does not itself provide an applicable construction for arbitrary heterogeneous catalogs. The contribution is presented as a complete constructive proof with a four-witness menu, a matching factor-2 lower bound, and structural/computational refinements. No publication-priority claim is made based on this scope issue.

## Compilation and review

The final two-pass compilation succeeded without undefined references/citations, overfull or underfull boxes, or LaTeX warnings. All 17 PDF pages were rendered for visual inspection. The universal cycle proof, the six-vertex lower bound, the nonlinear corollary, and the four-seed completeness argument also underwent independent internal mathematical review.
