# RA07 math-context blind reading (first pass)

Scope: read-only inspection of `project/source.pdf` (13 A4 pages; p0013 is blank) and full-page PNGs before consulting other reviewer conclusions. Native page render is 2480x3509 px. This is an independent source reading; unresolved marks below are observations, not final restorations.

## Page sequence and stable notation

- **p0001** opens with “6 代数” and a countable/additive-measure reminder: `m_i`, a partition `A_i`, `m(∅)=0`, and `m(⋃ A_i)=Σm(A_i)` for pairwise disjoint sets. It then states a lemma about translation and a countability argument, introduces Dirac measure `δ_x`, the map `z^X→R^+`, cardinality `c^2=(2^{aleph_0})^2=2^c`, and writes Jordan content (`U(f|P)`, `L(f|P)`). The long Chinese question line near y≈2670 is visibly uncertain; a circled question mark is part of the original writing.
- **p0002** continues Jordan/Riemann integration. It writes `sup_P U(f|P)=inf_P L(f|P) ⇒ Riemann 可积`, “可测度外测度”, and the criterion `E⊂R^n, E Jordan可测 ⇔ m^*(∂E)=0`; a starred measure/outer measure appears. A lemma places a dense subset of `[0,1]` in a countable union of intervals `[a_i,b_i]`, followed by a definition of Jordan measurability using finite rectangular boxes and a proof note (“内逼外包”).
- **p0003** starts with an `R^n`/Lindelöf statement (finite/countable open cover), then `L(f|P)` and the Darboux/Jordan bounds. It defines an outer-measure extension `m^*` on `R^n`, gives a finite/countable-cover infimum formula, and writes “约为外测度” near the middle. At the bottom it has `Remark` and item “12)” with a line ending in `proof`; this is the source of the p0003 U007/U009 ambiguities. The following displayed condition uses `∀ B_i∈B`, `⋃B_i` and `⋃B_i∈…`.
- **p0004** states a countable-cover/infimum argument for outer measure and the Carathéodory measurable-set condition. It explicitly uses `m^*(T)=m^*(T∩E)+m^*(T∩E^c)` (or a visibly equivalent complement notation), then “若 E 可测…”. A Tonelli-style inequality and `m^*(E)≤m^*(… )` follow.
- **p0005** develops the Carathéodory criterion. It gives `m^*(E)=m^*(E∩T)+m^*(T\E)` and the reverse inequality, then a line “可测性” and the notation `m^*(E)=m^*(\bar E)`/complement. The line at y≈1810 is a short symbol/word bridge attached to this equality (U007).
- **p0006** is headed “Caratheodory”. Definition: `E⊂R^n` is measurable when for every `T⊂R^n`, `m^*(T)=m^*(T∩E)+m^*(T∩E^c)`. It sketches a two-circle intersection Venn diagram and writes the subadditivity decomposition. Below are “不可测集合” and a set-algebra exercise (`A∪?`, `E`/`E^c`, generated σ-algebra); the lower-left edge contains a partial symbol/word at y≈2410–2630 (U014), while the line around y≈2480–2615 contains an equality/decomposition (U009).
- **p0007** proves closure properties for Carathéodory measurable sets: complements, finite unions/intersections, then a countable-union proof with partial sums and a limit. This fixes the intended direction of `E`, `E^c`, and `m^*` notation used on p0005–p0006.
- **p0008** continues the countable-union proof and concludes the σ-algebra property. It also records `m^*(A∪B)≤m^*(A)+m^*(B)` and the measurable disjoint-union equality.
- **p0009** lists measurability checks: `φ∈M`, `m^*(φ)=0`, and “对任意集合…” criteria, then defines `A∩B=φ`, `A\B=A∩B^c`, and an inclusion chain. This supplies the backward notation check for p0003/p0006.
- **p0010** starts with `Q,A,B` and countable additivity (`A_i`), then a Vitali construction. It writes `A`/`A^c`, an interval `[2,3]` (or a translated copy), “Vitali” (handwritten `Vatelli`-like), and a line containing `V⊂[0,1]` and `m^*(V)`/measurability. The lower line states that the measure of a countable disjoint family is bounded by the interval; U008 is the bridge phrase in this Vitali prompt.
- **p0011** gives a three-circle/overlap sketch and the identity `m^*(T∩A)+m^*(T∩A^c)=m^*(T)` (or the same with `E`). It then writes a finite/countable union identity and a disjointness condition. The first unresolved bridge (U008, y≈1940) lies immediately before the displayed additivity identity; the second (U010, y≈2400) is the bridge before the final finite-union equality.
- **p0012** returns to basic set algebra: `B⊂A^c`, `A,B∈M`, `m(A∪B)`, the inclusion–exclusion formula, and a countable-union equality. It is the nearest backward check for the p0011 bridges.
- **p0013** is blank (ordinary blank page, no missing content inferred).

## Source-level ambiguous loci observed

1. p0001 Q001: long Chinese question after the cardinality line; legible components include “无穷…/不…”, `AM`, “平移…”, “非平凡测度”, and a circled `?`. It is not visually safe to force a unique quantifier or theorem.
2. p0003 U007/U009: short text around the outer-measure definition and Remark item 12; the symbols are partly legible (`m^*`, `R^n`, `proof`) but one connective/interval phrase is not unique.
3. p0005 U007: bridge word/symbol in the Carathéodory equality; surrounding formulas force an outer-measure complement decomposition but not a unique Chinese connector.
4. p0006 U009/U014: decomposition line and lower-left edge fragment; `E`, `E^c`, `m^*` are stable, while the preceding connective and one edge glyph are not.
5. p0010 U008: Vitali prompt bridge before `Vitali`, `[2,3]^c`/translated interval and `V⊂[0,1]`; likely a choice/translation verb, but handwriting does not uniquely distinguish the candidates.
6. p0011 U008/U010: two connective phrases around the Carathéodory identity and finite-union equality; displayed formulas are clear, connective Chinese remains ambiguous.

The first-pass conclusion is therefore to preserve at least two readings at each locus and use formula-level forward/backward checks, without silently changing the source transcript.
