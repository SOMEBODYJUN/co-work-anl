# Independent check of bridge calculations

Date: 2026-11-23. Reviewer role: independent obstruction worker.

Reviewed file: `research/workspaces/ultimate-boss2-20261123/informed-b/bridge_and_refinement.md`.

Reviewed SHA-256: `782ebaa79c41948a0cf4f5b8a6ea729b0a0ae7496bb0596fa7c9788c2ba4bab5`.

Scope: Sections 2, 3 and 7 only. This is a conventional mathematical review of the stated elementary arguments, not an audit of the complete literature or a verification of either geometric manuscript.

## Section 2: finite-index covering

Valid. The right coset decomposition \(G=\bigcup_i Hg_i\) and the rational polyhedral Minkowski sum \(Q=\sum_i g_iP\subset C\) give \(HQ=C\). Closure of a convex cone under addition, and the origin in every polyhedral summand, justify the inclusions. No pointedness or separation follows or is claimed. The finite-index observation for support-preserving versus coefficient-preserving boundary groups is correct.

## Section 3: rational coverage and missing real boundary

Valid. I checked the two eigenvectors and eigenvalues of the integral matrix, the positive decomposition of \(v\), and the exact coordinate-ratio interval of each \(A^nP\). These intervals cover every positive ratio and neither endpoint ray. The endpoint rays have no nonzero rational point. Every interior real ray lies between rational interior rays, which proves the stated rational-hull equality. Thus coverage of the rational points does not establish coverage of the specified closed cone. The report correctly restricts this to an abstract convex counterexample.

## Section 7: finite vertical kernel from finite chamber orbit

Valid under exactly the two stated hypotheses. A finite \(K\)-orbit of \(N\) gives a finite-index **setwise** stabilizer \(K_N\); the finite action on \(T\) gives a finite-index kernel \(K_T\). No normality of \(K_N\) is needed. An element of their intersection fixes both \(T\) and \(V/T\), so \((h-I)^2=0\). Setwise preservation of \(N\) permits both positive and negative powers. The two rescaled limits lie in \(N\); its closure and pointedness force \((h-I)x=0\) for every \(x\in N\). Full dimension then gives \(h=I\) on \(V\), and faithfulness identifies it with the group identity. The finite-index conclusion is therefore sound.

The application paragraph is also correct: the relative nef cone is closed and pointed in the space defined by intersection against contracted curves, and projectivity supplies an open relatively ample cone. The substantive unproved geometric input is a **finite orbit of marked nef cones**. Merely having finitely many unmarked models does not supply that hypothesis, and the lemma does not assert that it does.

No blocking mathematical error was found in the reviewed sections. Earlier terminology and explanatory corrections in Sections 2 and 3 have been incorporated in the hash above. No conclusion about the full all-dimensional Morrison–Kawamata mission is certified here.
