# Figures and Provenance

## Decide whether a figure is needed

Retain or create a visual only when it materially carries geometry, topology, an orientation convention, a construction, or a multi-step relationship. Omit decorative or redundant sketches when formulas and prose are clearer.

Choose the least risky useful method:

1. crop a legible source figure;
2. use an attributed external figure when permitted by the project's distribution scope;
3. redraw a simple diagram in TikZ or tikz-cd;
4. use Mathcha as an authoring aid and keep editable vector/TikZ output;
5. omit the visual and preserve the mathematical explanation.

Never infer missing mathematics solely from a generated or redrawn image.

## Safe figure experiments

Before a Mathcha, TikZ, vector-editor, or replacement-figure experiment:

- make a timestamped backup of every affected `.tex` and figure asset in the project's approved backup location;
- select one bounded figure;
- keep the original figure and code intact until the experiment is accepted;
- compile and compare both versions;
- make rollback immediate.

## Mathematical visual QA

Verify dimensions, arrow directions, source and target labels, tangent and normal spaces, stable/unstable conventions, flow direction, boundary orientation, pullback variance, handle indices, and whether the picture represents a level set or a sublevel set. A visually attractive but conventionally reversed diagram is a mathematical error.

## Figure log

For every retained visual record:

```text
Figure label:
Topic:
Source PDF page:
File or code location:
Method: source crop / external crop / TikZ / Mathcha / synthesized
Provenance:
Related notation and conventions:
QA notes:
```

For public or open-source distribution, run a copyright and licensing audit before publishing copied figures. Prefer original redraws, public-domain or openly licensed sources, and explicit attribution. A figure acceptable for private notes may be unacceptable for a public repository.
