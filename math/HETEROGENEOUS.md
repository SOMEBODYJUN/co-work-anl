# Heterogeneous catalogs: two sharp but differently scoped thresholds

Here $(U_1,U_2)$ are arbitrary finite nonempty facility-specific catalogs unless a theorem adds restrictions. Model M1–M3 is in [`MODEL.md`](../MODEL.md). This line does **not** depend on the shared-catalog $\phi$ theorem. Source proof authority: [`manuscripts/heterogeneous/main.tex`](../manuscripts/heterogeneous/main.tex), §§2–7 and appendix; exact lower family in [`math/proofs/heterogeneous/tight_two_lower.md`](proofs/heterogeneous/tight_two_lower.md). Status is internally audited research manuscript.

## H1. The four-seed pure menu and factor-2 upper bound

At each legal labeled pair, use the guarded repair of at most four seeds: all common customers sent to either facility, and the maximum-weight common customer alone sent to either facility. Fix ties by a global customer ID. Repair is the L2 procedure of [`LOCAL_GAME.md`](LOCAL_GAME.md), and all retained outputs are **pure exact customer NE**. The nonempty menu and its menu-minimum threats $D_1^F(t),D_2^F(s)$ (distinct from the true all-NE threats $D_1,D_2$ in MODEL.md) are defined over the *whole* $(U_1,U_2)$, not a restricted cycle.

Suppose no menu witness at any legal pair meets the simultaneous factor-2 quotas. The maximizing-minimum response map alternates between the two catalog colors. After normalizing its largest threat, every edge's **every menu witness** has a responder load above its source threat and an incumbent load below half the next threat. A maximum-edge transport identifies a batch of shared customers of mass above one half. The key compression proof chooses the heaviest customer visible on the bad cycle and shows it is exactly the predesignated heaviest common customer on each edge where a singleton seed is invoked. Thus the four-seed menu, rather than every singleton, suffices.

The cycle proof uses *legal cross-color chords*, not hypothetical within-facility pairs. An initial transfer and one chord give scalar bounds on a high-load batch. With $h=b-c/2$ and final threat $e$, the branch $h\ge e/2$ uses a pure minimizing chord witness to bound every common atom and propagate an impossible strict threat increase around **any** cycle length. The branch $h<e/2$ uses the penultimate edge, another legal chord and set inclusion to force $e<1/3$, $b>1-e$, then $c>1$, contradicting normalization. Two-cycles are separately exact-stable; zero threats and co-location have separate clauses. The complete inequalities appear in manuscript §5 and [`history/proofs/heterogeneous/universal_two_prior.md`](../history/proofs/heterogeneous/universal_two_prior.md) (the latter is a historical larger-menu version).

Joint hyperedge:

$$
\{\text{guarded pure repair},\ \text{four-seed completeness},\
\text{full-catalog threats},\ \text{legal alternating chords},\
\text{both arbitrary-cycle branches}\}
\Longrightarrow\text{factor-2 menu witness}\Longrightarrow\text{pure-continuation 2-SPE}.\tag{H1}
$$

The stated construction uses $O(|U_1||U_2|(n+1)^2)$ rational operations and polynomial bit lengths, with at most $|U_1|+|U_2|-2$ deviation witnesses. It does not find the true minimum over all mixed customer NE. The original IJCAI paper already *states* a general $k$ upper bound; the contribution here is the particular self-contained two-facility constructive proof, not first mention of the numeral 2.

## H2. Exact positive-integer lower family

Take an undirected graph with vertices $A,B,C,D,E,F$, edges $AB,AC,BD,CD,BE,CF$, and customer weights

$$
(w_A,w_B,w_C,w_D,w_E,w_F)=(M,1,M+8,M+2,10,6),\quad M>4\text{ integer}.
$$

Let $U_1=\{A,B\}$, $U_2=\{C,D\}$. Each legal pair has exactly **two** common customers. Pointwise strict dominance at each of the four customer games yields unique pure NE (indeed unique CE/CCE), with facility payoff matrix

|  | $C$ | $D$ |
| --- | --- | --- |
| $A$ | $(M+9,2M+8)$ | $(2M+8,M+3)$ |
| $B$ | $(2M+13,M+14)$ | $(M+11,2M+10)$ |

The four strict unilateral improvements form $AC\to BC\to BD\to AD\to AC$. The least gain ratio is exactly

$$
\alpha^*(M)=\frac{2M+10}{M+14}=2-\frac{18}{M+14}\longrightarrow2.\tag{H2}
$$

Because the local continuations are unique, no equilibrium-selection trick avoids this lower bound. The explicit graph and exact formula are a reproducible obstruction to transferring the shared $\phi$ bound to all unequal catalogs. `facility_spe/examples/tight_two.py` generates instances; `tight_two_M1000.json` and its certificate are fixed checks. H1 + H2, **jointly**, give sharp universal 2 for this heterogeneous class, conditional on the upper manuscript proof.

## H3. The restricted $\rho=2\cos(\pi/7)$ class

Now impose **both** $\min(|U_1|,|U_2|)\le2$ and $\max_{s\in U_1,t\in U_2}|C_s\cap C_t|\le1$. The sharp universal factor in this restricted class is claimed to be $\rho\approx1.8019377358$, the largest root of $z^3-z^2-2z+1=0$.

With at most one common customer at a pair, a fixed consistent tie rule yields a pure local equilibrium; unequal reaches force a unique pure response. The 2-by-2 bad improvement cycle classification produces the cubic bound. To lift from 2-by-2 to a 2-by-$m$ game, retain for each of the at most two rows a best-response column of the other facility (at most two columns); a $\rho$-stable retained cell is automatically stable against *all* columns. A separate six-customer strict lower family approaches $\rho$ and survives rational perturbation to positive integers. Exact derivations are in manuscript §8 and [`history/proofs/heterogeneous/sparse_lower_prior.md`](../history/proofs/heterogeneous/sparse_lower_prior.md) §§1–10; that historical note's §11 is **superseded** and must not be used for current status.

The factor-2 family H2 shows that relaxing the overlap cap from one to two already allows a sharp factor of 2 with two choices each. Nothing in H3 proves that $\rho$ persists when **both** catalogs have arbitrarily many locations. That exact open question is retained in [`RESEARCH_STATE.md`](../RESEARCH_STATE.md).

## H4. A broader but conditional response-core tool

For finite two-leader continuation games with nonnegative payoffs, independently selectable nonempty continuation sets at each labeled action pair, and attained coordinate minima, follow a best response that maximizes the *minimum attainable* payoff against each fixed opposing action. A simple cycle of this full-action response map induces a balanced square core that preserves each retained action's full-game threat. An approximate stable continuation selection in the core lifts back by choosing minimizing punishments for omitted deviations. This is an abstract **existence transfer**, not automatically an efficient procedure, since true minima may be hard to compute. The final H3 pure algorithm uses the simpler fixed-payoff two-column reduction above. Source: manuscript §3 and [`math/proofs/heterogeneous/response_core.md`](proofs/heterogeneous/response_core.md) §2A.

## Status and review boundary

The four-seed solver's generated certificates have been checked on seeded cases and exact lower instances, but finite checks are implementation evidence. An internal adversarial read-through found no fatal flaw in H1's arbitrary-cycle branches; external reconstruction and a literature-priority check remain. The code's old verifier had accepted illegal on-path layouts; commit `70026ad` adds explicit catalog and deviation checks, preserving the theorem's distinction from implementation soundness. A returned factor-2 certificate remains an *instance-specific* exact check, not a proof of H1 for unbounded inputs.
