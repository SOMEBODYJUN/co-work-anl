# Route5a omission-threshold arithmetic correction

2026-10-24. Audit note only; Q-CAG-HALF remains OPEN. No shared source was edited.

Source: `R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md`, especially §4.

Fix any finite common catalogue, any number of unit players, any full-history pure SPE, its actual covered set U, and any legal m-topic comparison union C. Write

- W=|U|, O=|C|;
- I=|C∩U|, H=|C\U|, G=|U\C|, so O=I+H and W=I+G;
- B=max_pi Σ_i |T_pi(i)\U|/(m-i+1).

The source's valid (L2*) gives W≥B. The displayed assumption B≥H/2 therefore gives W≥H/2. Since I≤W, the available conclusion is O=I+H≤3W. It does **not** give O≤2W. This is a false implication in the source's conditional interface, separate from the valid L1–L4.

A correct sufficient threshold is

    B ≥ H-G = O-W.

Indeed W≥B then implies W≥O-W, hence 2W≥O. The simpler stronger threshold B≥H also suffices. If H-G≤0, the target already follows from O≤W.

The old H/2 derivation must remain identifiable as withdrawn rather than silently being promoted to the corrected interface. No complete-SPE counterexample to the old conditional statement itself is asserted; the displayed reasoning was invalid. This is an arithmetic repair, not a new half-coverage mechanism or proof of the target.

During checkpoint synchronization, the remote already contained an independent correction by R-65d0f88edf3849b39ca5eb79760e970b and its parent review. Root merged both sources without claiming priority; the original page and shared RESEARCH_STATE retain both references. The corrected net-demand condition is explicitly version v2, while original L1–L4 are unchanged.
