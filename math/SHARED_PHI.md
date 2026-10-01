# Shared catalog: the finite-menu golden-ratio construction

**Claim identity:** `SC-PHI-E` (existence), `SC-PHI-A` (bit-polynomial construction), and `SC-PHI-SHARP` (matching lower-bound interpretation). Their exact statements/statuses are in [`CLAIMS.md`](../CLAIMS.md). This note is a navigable **proof reconstruction**, not a replacement for the complete [`25-page manuscript`](../phi_n_manuscript/main.tex). No external line-by-line referee report exists.

Let $U_1=U_2=S\ne\varnothing$, $q=\phi^{-1}$, $a=q^2=1-q$, $c=\phi/2$, and $R_s=w(C_s)$. The label order matters even at a co-location. All customer continuations are exact independent mixed NE under M1–M3 of [`MODEL.md`](../MODEL.md).

## S1. An explicit menu, not the whole NE correspondence

For each unordered physical pair build one menu $F(s,t)$ of exact local NE and reflect it consistently when facility labels reverse. With $(A,B)$ private loads and common weights $w_i$, the families are:

| Family | Construction | Why it is present |
| --- | --- | --- |
| **P** | Two all-common-on-one-side and both orientations of each singleton seed. Keep an already pure NE; otherwise perform L2 guarded repair **only if** each initially lower-side common customer weighs at least the initial gap. | Arbitrary pure edge NE, protected-heavy-client transport, return and anchor witnesses. Guard cannot be dropped. |
| **E** | If $A=B$, every common customer independently chooses each facility with probability $1/2$. | Exact co-location loads $(R_s/2,R_s/2)$, which initiate the normalized cycle bound. The older algorithm note calls this H. |
| **T** | For each designated pair $(h,j)$, put every other common customer on the higher-reach site. With lower/higher private loads $a_0\le b_0$, $Z=C-w_h-w_j$, $D=b_0-a_0+Z\le\min(w_h,w_j)$, give $(h,j)$ probabilities $((1+D/w_h)/2,(1+D/w_j)/2)$ on the lower-reach site. Use both orientations if reaches tie. | The two-large-customer pair contradiction; the boundary $D=w_h$ or $w_j$ is legal. |
| **C** | In the fixed reach regime $U\ge V>cU$, common mass $C<qV$, largest common atom $\le aU$, call the polynomial local strong-chord routine and include an NE with $L_U\ge qV$ and $L_V\ge qU$. | The final cross-chord in both anchor cases. It is computed **before** response-cycle threats are known. |

Every member is Nash-checked and $F(s,t)\ne\varnothing$ because P has a qualified all-common seed. There are $O((k+1)^2)$ members for $k$ common customers. The menu itself is a concrete selectable continuation set; its completeness for the global theorem is a separate obligation.

Define

$$
u(s,t)=\min_{e\in F(s,t)}L_s(e),\qquad
d_F(t)=\max_{s\in S}u(s,t),\qquad
b(t)\in\arg\max_{s\in S}u(s,t).\tag{S1}
$$

The old true minimum $m(s,t)$ obeys $m(s,t)\le u(s,t)$; we never claim equality. A menu witness $e$ at $(s,t)$ with

$$
 L_s(e)\ge qd_F(t),\qquad L_t(e)\ge qd_F(s)\tag{S2}
$$

is **sufficient** for a $\phi$-SPE: choose a menu-minimizing exact NE after each *actual* unilateral deviation. The two labeled deviation families are disjoint, and the other pairs receive a deterministic pure NE. The exact-$m$ criterion of `MODEL.md` is iff; S2 is deliberately not asserted necessary outside the menu.

## S2. The central global hyperedge: excluding all bad cycles

Assume **no** menu witness satisfies S2. Choose a directed response cycle $T$ of $b$, but keep each $d_F(t)$ maximized over the **entire** $S$, including sites outside $T$. Let $M=\max_{s\in T}d_F(s)$. The zero case is handled by E; otherwise normalize $M=1$. Failure at co-location and at every edge $s\to t=b(s)$ yields

$$
 d_F(s)>cR_s,\quad 1\le\max_{s\in T}R_s<2q,\quad
 \forall e\in F(t,s):\ P=L_t(e)\ge d_F(s),\quad Q=L_s(e)<qd_F(t)\le q.\tag{S3}
$$

The **universal quantifier is over the fixed menu on an edge**, not over all actual customer NE. Every later contradiction witness must be in P/E/T/C. Two arguments infer uniqueness among *all* customer NE by independent strict dominance; only then may a menu minimum be identified with the unique true payoff. The detailed membership matrix is the historical [`menu quantifier audit`](../asym_research/common_phi_menu_quantifier_audit.md), and §14 of the integrated manuscript incorporates it.

The global contradiction has three connected layers (all assertions below are conditional on S3):

1. **Reach and heavy-atom structure** (§§3–8). An all-common P witness and strict dominance give $R_s\ge q\Rightarrow d_F(s)\le R_s$ and a return rule. In §3.2, responder-exclusive mass $E>R_s$ makes all common customers strictly choose the source in **every** NE: the first true-uniqueness deduction. Singleton P seeds rule out any cycle-visible atom of weight $\ge q$. Pure P edges show at most two large atoms per location. Pair avoidance, one-member chords and the T witness rule out a triangle and repeated-pair edge; all large-atom pairs are empty or form a star. These are **joint** restrictions, not a chain where any one lemma proves the theorem.
2. **Star and unique transport** (§§9–10, 12.1). A reverse-singleton P witness first rules out too much common mass leaving a heavy $h$. The resulting inequalities make $h$ strictly choose the responder in every customer equilibrium; then every other common customer strictly chooses the source. This is the second true-uniqueness mechanism, after the return rule in §3.2. Upward $h$-chords, two protected singleton anchors and inclusion–exclusion give an abstract center contradiction for a nondegenerate star. The general first-edge lemma in §12.1 is logically used in §10.2 despite its later placement in the paper.
3. **Empty or single-pair cases** (§§11–13, Appendices). Select a maximum-reach first edge and an $h$-only anchor. If $H\ge R/2$, a fixed C witness caps every no-$h$ reach and yields the center contradiction. If $H<R/2$, a second consecutive anchor and C yield a similar cap; the two-anchor covering lemma excludes the remaining cycle. Every C use first verifies its *reach-based* hypotheses, and only then uses the reach bound to compare quotas with $d_F$. There is no d-adaptive search for a new local equilibrium.

`{S3 edge quantifier, P protected repairs, T pair witness, true uniqueness at two steps, heavy-pair/star classification, two-anchor covering, polynomial C witness}` **jointly** exclude every possible finite bad response cycle. A missing guard or full-catalog maximum in any one branch is a proof obligation, not a cosmetic detail. The internal audits found no fatal flaw, but agreement among related derivations is not independent external certification.

## S3. Constructive hyperedge and bit bound

Build all pair menus, their oriented minima $u$, the full-catalog threats $d_F$, and one response cycle. The proof already guarantees an S2 witness on $T^2$; the code scans all $S^2$ menus to choose a smaller factor **within this menu** if available. P and T cost $O((k+1)^3)$ operations per pair, C costs $O((k+1)^4)$, giving $O(|S|^2(n+1)^4)$ exact rational operations. The manuscript separately bounds intermediate bit length by input sums and bounded divisions. Exact comparisons with $q$ reduce to the sign of $z^2+z-1$ for rational $z\ge0$. This is a bit-polynomial claim for rational input, not an empirical running-time measurement.

The output records one on-path witness, at most $2|S|-2$ unilateral-deviation witnesses, and a specified pure-NE default for all remaining labeled profiles. [`common_phi_algorithm.py`](../common_phi_algorithm.py) checks the constructed witness against customer NE and actual facility deviations. [`verify_phi_certificate.py`](../verify_phi_certificate.py) is a separate CLI entry point but imports the same checker; it is **independent of the menu search**, not an independently implemented verifier. Its metadata for the default rule is not itself validated. The existential extension is justified by the proved deterministic pure-NE default, not by trusting arbitrary metadata. Individual certificates have checkable instance-specific meaning even if the universal proof is later revised.

## S4. Sharpness and boundaries

Krogmann et al.'s IJCAI 2024 Theorem 5 gives a $\phi-\varepsilon$ lower bound for the weighted two-facility model and calls tightness open. The integrated manuscript argues its unrestricted example is common-catalog and strict inequalities permit rational perturbation. **That mapping and perturbation are a distinct proof obligation**, not an automatic consequence of a paper title. Conditional on both it and S2's universal proof, $\phi$ is the sharp shared-catalog *universal* threshold.

The claim does not compute a fixed instance's optimal $\alpha^*$; it does not guarantee a $\phi$ factor for differing catalogs; and it does not preserve arbitrary mixed NE when client costs become arbitrary convex functions. See the separate heterogeneous and extension notes.

## Remaining audit targets

- Independently reconstruct the arbitrary-cycle star/anchor split and the S3 menu quantifier without first reading the existing audit. A single fatal objection blocks promotion.
- Check Appendix B's pivot/flip termination and all rational bit bounds independently.
- Produce a *global* directed instance whose selected on-path witness genuinely uses C. Existing 753 seeded full-game checks choose 662 P, 88 E, 3 T, 0 C; the local three-mixer case exercises C but not its global selection.
- Build a genuinely independent certificate checker and verify the prescribed default continuation rule/schema; current separate CLI is only a wrapper.
