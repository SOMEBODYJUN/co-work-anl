# Literature audit — cutoff 2026-11-22

Target: a **strong** rational polyhedral fundamental domain for the image of `PsAut(X/S,Δ)` on `C = overline(Mov)(X/S) ∩ Eff(X/S)`, for every Q-factorial terminal log Calabi–Yau fibration of relative dimension ≤2, with arbitrary normal base and absolute dimension. Here “strong” requires trivial stabilizer in the **linear image**, not in the potentially nonfaithful geometric group.

## Source summaries (each below 200 words)

### Li–Zhao, arXiv:2206.13701v8; PLMS DOI 10.1112/plms.70099

Read: [full v8 HTML](https://arxiv.org/html/2206.13701v8), dated 2025-11-04. The [arXiv metadata](https://arxiv.org/abs/2206.13701) explicitly calls this the published version and records a correction to Theorem 2.5, Step 2. Theorem 1.3(1) derives only the **weak effective-cone** result under `R¹f_*O_X=0`; (2) derives the strong result under nondegeneracy. Theorem 1.4 concerns **Δ=0 K3 fibrations**: weak in general, strong if nondegenerate, particularly for Q-factorial base. Proposition 4.5(3)'s Q-factorial-base conclusion is inside its `R¹f_*O_X=0` hypotheses; it is not a universal claim for elliptic fibrations. Proposition 5.3 and Remark 5.4 explicitly distinguish the effective cone from `Mov_+`, citing Kawamata 3.8(2). Thus this version does not establish the full target.

The [publisher page](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/plms.70099) confirms PLMS 131(5), e70099 and first publication 2025-11-08. Its full-text link redirected to the abstract; direct PDF failed. The journal body was **not independently retrieved or compared**.


### Zhan Li, arXiv:2309.04673v1; JAG DOI 10.1090/jag/864

Read: [full v1 HTML](https://arxiv.org/html/2309.04673v1), 2023-09-09; [metadata](https://arxiv.org/abs/2309.04673) lists only v1, 32 pages. Theorems 1.3, 1.4 and 1.8 are stated for **terminal log pairs**, assuming good minimal models in relative dimension and a polyhedral covering of the generic movable cone by a cone contained in the generic effective cone. Theorem 1.3 gives coverage of rational movable classes; 1.4 gives finiteness of models; 1.8 gives a **weak** domain on **`Mov_+`**, not the requested effective cone. Corollary 1.9 (=6.3+6.4), the explicit relative-dimension-≤2 application, is written for **Δ=0** terminal Calabi–Yau fiber spaces and still concludes only weak `Mov_+`.

AMS indexed primary table-of-contents metadata identifies online publication 2026-08-24, J. Algebraic Geom. 36 (2027), 1–50, DOI [10.1090/jag/864](https://doi.org/10.1090/jag/864). The [author’s institution page](https://math.sustech.edu.cn/e/lizhan) corroborates volume/pages. The journal article body was **inaccessible and unread**; no assertion that its theorem numbering or scope equals the 32-page preprint is justified.


### Moraga–Stark, arXiv:2409.13068v1

Read: [full HTML](https://arxiv.org/html/2409.13068v1), 2024-09-19; [metadata](https://arxiv.org/abs/2409.13068) lists only v1. Conjecture 1.1 separates (1), finite orbits of Mori chambers/faces and contractions, from (2), existence of rational polyhedral fundamental domains. Theorem 1.2 proves **(1), expressly named the geometric cone conjecture**, in relative dimension at most two for klt log Calabi–Yau pairs. This is broad enough in singularity and boundary scope to contain the target's terminal log-pair cases, but its conclusion does not supply the requested strong domain. Corollary 1.3 concerns finiteness of minimal models. Introductory shorthand must not turn this geometric theorem into an RPFD theorem.


### Faucher, arXiv:2603.22457v1

Read: [HTML](https://arxiv.org/html/2603.22457v1) and [30-page PDF](https://arxiv.org/pdf/2603.22457v1). Metadata says submitted 2026-03-23, only v1; PDF internally dated March 25, 2026, while served HTML internally says August 24, 2026. The cited relevant statements agree, but the date discrepancy should be disclosed rather than treating the HTML as a separately verified revision.

Conjecture 1.2 defines the movable conjecture on **`Mov⁺`**. Theorem A treats specified quotient-product very-general fibers; Theorem C treats terminal Q-factorial log pairs with good minimal models for effective perturbations on the very general fiber and generic effective polyhedral coverage. Both give **weak `Mov⁺`**, upgrading to strong only with nondegeneracy; Theorem 4.6 makes this explicit. They do not remove the target’s missing hypothesis. The introduction, PDF p.4 / HTML lines 130–133, records `Mov = Movᵉ ⊊ Mov⁺` in Kawamata’s example and cautions against automatic transfer between formulations. It does **not** establish that strong RPFD on the effective cone fails there.


### Kawamata, alg-geom/9701006v1, Example 3.8(2)

Read: [primary HTML](https://arxiv.org/html/alg-geom/9701006v1) and [PDF](https://arxiv.org/pdf/alg-geom/9701006), 1997-01-13. Example 3.8(2) takes the versal deformation of a Kodaira I₂ curve over a **germ of a smooth two-dimensional base**, with smooth total space, relative Picard number two, and Δ=0. Writing `d(z)=z·F`, it computes `overline(Mov)={d≥0}` and `Movᵉ={d>0}∪{0}`. It describes infinitely many alternating flops and a birational fiberwise translation identifying the first flop over the identity of the base. Nonzero boundary classes are not effective. This is an actual geometric demonstration that the rational hull and effective movable cone differ; it is **not a demonstrated counterexample to strong RPFD on Movᵉ**. Its analytic/local germ formulation also needs an algebraization/globalization argument before use against a target restricted to quasi-projective algebraic varieties.


### Additional recent check: Choi–Li–Li–Zhou, arXiv:2512.01516v1

Read relevant parts of [primary HTML](https://arxiv.org/html/2512.01516v1). Definition 1.2 assumes polyhedral movable coverage as part of being an MKD fiber space. Proposition 3.8 proves equality of movable and effective movable cones, with equality to the rational hull additionally requiring nondegeneracy; it again cites Kawamata 3.8(2). Remark 3.5 says a Siegel property for degenerate cones is currently unavailable. This is an axiomatic extension and does not independently prove the entire target.

## Independent synthesis and remaining gaps

The retrieved preprints do not prove the full strong effective-cone target, but this is **not an exhaustive novelty certification**. The journal body of Li II is a material unchecked version gap (50 pages versus the preprint's 32); the PLMS body was not independently compared, although arXiv explicitly labels v8 the published version.

Two separate upgrades are required: **weak → strong**, and **rational hull → effective movable cone**. Geometric finiteness alone is a third, weaker conclusion. Also distinguish explicit Δ=0 corollaries from general log-pair theorems with generic-fiber hypotheses. Merely adding Q-factoriality of the base is not established to remove every degeneracy outside the `R¹f_*O_X=0` setting.

The Kawamata cone computation supplies no convex obstruction to the requested strong result. In coordinates `(x,d)`, an integral shear `T(x,d)=(x+a d,d)` has a strong rational polyhedral domain `cone((0,1),(a,1))` on `{d>0}∪{0}` (for rational `a>0`), because `x/d` is translated by `a`. By contrast, covering nonzero boundary rays of `{d≥0}` forces a closed polyhedral covering cone to include those rays, which can obstruct a strong domain for that modified cone. This elementary model explains why cone inequality does not establish failure on the effective cone. Identifying the full geometric group exactly was not needed for that logical warning; no global geometric counterexample to the requested target was verified here.

Searches used both engines, including primary-source checks and date-restricted recent queries through `before:2026-11-23`; search hits are evidence of nearby work, never evidence that all work has been excluded.
