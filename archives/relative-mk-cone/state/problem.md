# RMKC-STRONG-REL2: immutable mathematical target

## Original target

Over the complex numbers, prove that every terminal Calabi–Yau fibre space
\(f:(X,\Delta)\to S\), in the sense of Li–Zhao (2025), with
\(\dim X-\dim S\leq2\), satisfies the strong relative Morrison–Kawamata movable cone conjecture. The total space is normal, projective and \(\mathbb Q\)-factorial and \(K_X+\Delta\equiv_S0\).

Set
\[
 V=N^1(X/S)_{\mathbb R},\qquad
 C=\overline{\operatorname{Mov}}(X/S)\cap\operatorname{Eff}(X/S),\qquad
 \Gamma=\operatorname{Im}\bigl(\operatorname{PsAut}(X/S,\Delta)\to\operatorname{GL}(V)\bigr).
\]
Find a rational polyhedral cone \(\Pi\subset C\) with
\[
 C=\bigcup_{\gamma\in\Gamma}\gamma\Pi,\qquad
 \operatorname{Int}(\Pi)\cap\operatorname{Int}(\gamma\Pi)=\varnothing
 \quad(\gamma\ne1).
\]
The domain must also satisfy the exact fundamental-domain convention in Li–Zhao Definition 3.4: weak-domain separation is \(\gamma\Pi\cap\operatorname{Int}(\Pi)=\varnothing\) unless \(\gamma\Pi=\Pi\), and the setwise stabilizer must be trivial. Do not replace this with a weak domain.

## Scope that must not change

No nondegeneracy assumption on the closed movable cone; no \(\mathbb Q\)-factoriality of the base; no restriction to K3 fibres or special deformation types; no bound on absolute dimension. Include relative dimensions zero, one and two. Preserve all pairs admitted by the chosen original definition. Do not silently replace pairs by \(\Delta=0\), replace numerical by linear triviality without justification, or replace the effective movable cone by its rational hull.

Technical convention differences (terminal pair versus terminal total space, boundary coefficients, projectivity of the base and relative equivalence conventions) must be checked against the original papers and recorded explicitly. Such an audit does not authorize narrowing this target.

## Required mathematical work

A. Check original statements and later work: theorem numbers, complete hypotheses, cone used, nondegeneracy dependence and known counterexamples. Certify novelty only to the extent actually supported by original sources.

B. Study lineality and quotient actions. The task's \(L=C\cap(-C)\) must be distinguished from \(W=\overline{\operatorname{Mov}}\cap(-\overline{\operatorname{Mov}})\). Prove rationality, saturation, quotient nondegeneracy and lifting when used. Control the kernel on the quotient, its action on lineality and any extension/shear terms.

C. Prove precise lemmas and the full theorem, with complete proofs and uses of every hypothesis. If a route fails, preserve its exact smallest outstanding obligation and keep working on it or challenge it.

D. Audit possible counterexamples, including nontrivial lineality, infinite stabilizers, non-\(\mathbb Q\)-factorial bases and special low-relative-dimensional fibrations. A purely linear cone example is not a geometric counterexample.

## Success and output

The eight gates in acceptance.md are conjunctive. A partial theorem, conditional route, finite example or an already known proof is not success. If the target is false, the proof task still FAILS and an admissible counterexample is reported separately. Final proof-stage output starts exactly `✅ PASS` or `❌ FAIL`.

Required files: `main_theorem.tex`, `proof.tex`, `literature_audit.md`, `counterexample_audit.md`, `research_paper.tex`, `verification.md`. Unresolved steps must be visible in the English manuscript; never place an unsupported proof-ending symbol at the end of the target.
