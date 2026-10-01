# Local equilibrium geometry and constructive lemmas

**Scope:** one labeled pair of two facilities, with the model and notation in [`MODEL.md`](MODEL.md). The statements here concern customer equilibrium and have value independently of either global approximation theorem. Source proof authority: [`manuscripts/shared_phi/main.tex`](../source/manuscripts/shared_phi/main.tex) §§2–3 and Appendices A–B; supporting exact derivations in the repository history at `math/proofs/shared/strong_chord_existence.md` and `math/proofs/local/exact_methods.md`.

## L1. Support cells: points and intervals

For each common customer choose one declared state: pure facility 1, pure facility 2, or designated mixer. A pure-1 customer has $c_i=w_i$ and requires $\Delta\le w_i$; a pure-2 customer has $c_i=-w_i$ and requires $\Delta\ge-w_i$; a mixer has $c_i=\Delta$ and $|\Delta|\le w_i$. With $m$ designated mixers and signed pure sum $P$,

$$
 (1-m)\Delta=A-B+P.\tag{L1}
$$

For $m=0$, this fixes a pure point. For $m\ge2$, it fixes the point $\Delta=-(A-B+P)/(m-1)$ (rational for rational input). For $m=1$, the numerator must vanish; then the pure-action inequalities and the mixer weight cut out an attainable **closed interval** (with rational endpoints for rational input). All three cases require checking the remaining support inequalities. The union of at most $3^k$ cells is the *entire* local independent mixed NE load spectrum. Endpoints may have repeated representations. This fact drives exact local optimization and `LOCAL-HARD`'s NP-membership argument; it does not imply an efficient unrestricted search.

## L2. Guarded pure repair

Start with a pure assignment whose lower and higher loads are $Q<P$. Require every common customer initially on the lower side to weigh at least the gap $P-Q$. If it is already an NE, keep it. Otherwise move the **largest strictly improving** common customer from the originally higher side toward the originally lower side. Stop at the first load-order reversal or when no move remains.

Each move has weight smaller than the current gap, so both new loads stay strictly inside the previous load interval. Before the first reversal the gap decreases and moved weights do not increase. At reversal the new gap is smaller than the last moved weight; hence no moved customer or protected original lower-side customer wishes to return. All others are stable. At most $k$ moves occur, and the original lower load remains a lower bound on *both* final loads. This extra quota property is why an arbitrary improvement sequence is not a substitute in the shared and heterogeneous menus. The mathematical repair idea is attributed to Vos in the integrated manuscripts; the specified deterministic implementation is [`facility_spe/heterogeneous_two.py`](../../facility_spe/heterogeneous_two.py).

## L3. Strong cross-chord witness, exact scope

Set $U\ge V$ for the two *reaches* (private plus all common weight), $C$ for common mass, $q=1/\phi$, and $c=\phi/2$. In the regime $V>cU$ and $C<qV$, the local theorem analyzes existence of an exact NE meeting the **two simultaneous** quotas

$$
 L_U\ge qV,\qquad L_V\ge qU.\tag{L3}
$$

Its fuller iff describes a largest-weight obstruction: for largest common weight $x$, a quota NE exists if and only if $x\le U-qV$ **or** $C-x\ge U-V$ (with the zero-common and equality conventions of Appendix A). If both inequalities fail, a pure unique-NE obstruction remains. The global shared proof uses only a *sufficient* interface: if in addition $\max_iw_i\le(1-q)U$, a quota NE exists. Do not identify that sufficient C-menu condition with the entire local iff, and do not let the witness depend on a subsequently chosen global threat $d_F$.

The integrated Appendix B replaces an existence proof's global quadratic maximizer by pair-endpoint local exchanges on a box slice. Its pivot/flip argument gives $O((k+1)^4)$ exact rational operations with polynomial intermediate bit lengths. It finds a **pair-local**, not necessarily global, maximum. The old note's explicit box-slice counterexample (weights $(14,13,19)$, target $-10$, objective values $582<654$) prevents a false global-optimality claim. [`facility_spe/local/strong_chord.py`](../../facility_spe/local/strong_chord.py) implements the local routine. Its `assert` statements are internal invariants; mathematical correctness rests on the appendix proof.

## L4. Why two mixers do not suffice

At private masses $A=40,B=39$ with three common customers of weight $20$ each, reaches are $(100,99)$. The simultaneous L3 quotas are met at loads $(277/4,279/4)$ by independent probabilities $(39/80,39/80,39/80)$ on the first facility. Exhaustive support enumeration gives pure loads $(60,79)$, two-mixer loads $(79,60)$, and no one-mixer equilibrium; those alternatives fail at least one quota. This is a **local counterexample** to a proposed two-mixer shortcut, not a global $\phi$ lower bound. The exact support calculation is reproduced by [`tests/audits/shared_menu.py`](../../tests/audits/shared_menu.py).

For a different local extremal objective, $2r$ unit-weight common customers at equal private masses have minimum gap $-(r-1)/r$, attained with $r+1$ genuine mixers. Thus even *extremal* local mixed supports need not have bounded size. See [`math/proofs/local/hardness.md`](../source/notes/local/hardness.md), final sections.

## Logical use

`{M2 exact NE conditions, L2 guarded repair, L3 local iff, Appendix B polynomial exchanges}` jointly make the shared finite menu constructible. None of these alone proves the global $\phi$ theorem. `L1` enables exhaustive exact or parameterized solvers; their output is not a premise of the polynomial finite-menu proof. The theorem statuses and objections remain separate in [`CLAIMS.md`](CLAIMS.md).
