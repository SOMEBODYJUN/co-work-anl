# Polynomial-Time Golden-Ratio Equilibria for Two Facilities with Weighted Atomic Clients

Updated September 30, 2026. This is an internally audited research manuscript;
no external peer review or acceptance is claimed.

## Result

For two facilities sharing one explicit finite location catalog, with positive
binary rational atomic customer weights, the manuscript proves a deterministic
polynomial-time construction of a phi-approximate SPE. Every customer
continuation is an exact independently mixed NE for the original weights.
The arithmetic bound is O(|S|^2(n+1)^4), with polynomial intermediate bit lengths.

The result uses a fixed polynomial menu at each site pair. It does not compute
minimum payoffs over the entire customer-equilibrium set. The original IJCAI
2024 lower bound motivates the sharp golden-ratio target; the theorem here is
restricted to one common catalog, including co-locations.

## Files

- `main.tex`: authoritative complete LaTeX source.
- `main.pdf`: compiled 25-page A4 manuscript.
- `build_manuscript.py`: two-pass compiler for the authoritative source.
- `build/compile_polynomial_pass2.log`: final compilation log.

Section 2 defines all menu families and the sufficient certificate criterion.
Sections 3--13 prove the closed-cycle contradiction directly for menu minima.
Section 14 gives the algorithm, quantifier audit, and bit complexity.
Appendix A supplies the complete strong-chord proof. Appendix B supplies its
polynomial exchange construction, including the termination and bit bounds.

## Compile

On a standard TeX installation, run twice from this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

In the current runtime, use:

```sh
python build_manuscript.py
```

The build script compiles the edited source. It no longer regenerates the
manuscript from the earlier existence-only Markdown files.

## Verification

- Two-pass compilation with pdfTeX 1.40.25 / TeX Live 2023.
- 25 A4 pages; embedded Type 1 fonts.
- Final log: no errors, undefined references/citations, overfull/underfull boxes,
  or warnings.
