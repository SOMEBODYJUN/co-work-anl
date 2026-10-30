# Revision notes

## Round-1 referee repairs

- **main.tex:131--134 (family C):** removed the false assertion that the
  equal-half menu member E meets the stronger \(qR\) quotas at co-location.
  E remains the equal-half witness; the strong chord is retained whenever its
  strict hypotheses hold.
- **main.tex:325--342 (large-pair chord):** made the normalized no-witness
  hypothesis explicit and derived \(d(s)>\phi(R_t-H)\) from the two quota
  inequalities. The repair branch is now stated to produce a quota witness
  directly.
- **main.tex:471--477 (common-h transport):** expanded the compressed
  reach-order step. If \(R_t\ge R_s\), the upward chord gives
  \(d(s)=u(t,s)\le R_t-H\le R-H=K<q\), contradicting the edge hypothesis
  \(d(s)>q\); hence \(R_t<R_s\) before \(\Delta=R_s-R_t\) is used.
- **main.tex:837--843 (largest-client branch):** recorded the bound
  \(L_B-L_A\le x+S-\delta<x\) for every intermediate assignment, so the
  fixed largest client remains stable throughout pure repair.
- **main.tex:1088--1096 (polynomial chord):** replaced the phrase “follow the
  finite case choices” by an ordered branch table with exact tests for
  positive and negative gap cases, including the third-mixer scan, prefix
  selection, and symmetric pure repair.

These edits preserve all formal theorem statements, labels, assumptions, and
quantifiers. They must be followed by a fresh targeted proof audit of the
cycle transport and polynomial constructor before the theorem is marked
verified.
