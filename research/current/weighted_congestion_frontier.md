# Weighted congestion: source envelope and its topology boundary

This is a separate model from facility location and customer attraction.
The canonical model is [WC-TARGET v1](../weighted_congestion_frontier/MODEL.md):
finite players with arbitrary positive resource-independent weights, arbitrary
finite subsets as strategies, and nonnegative-coefficient polynomial resource
latencies of degree at most d. Player costs sum latencies; α-PNE has weak
deviation inequalities, while every nonexistence certificate is strict.

## R3-SOURCE-SHARP-ASYMPTOTIC-v1

Let F_d be exactly the supremum in the source formula (3), with integer
n≥1, 1≤k≤d, positive 0<w≤1, and 0≤β≤1:

    F_d = sup min{(1+nβ(1+w)^d)/((1+nw)^k+nβ),
                  ((1+w)^k+βw^d)/((nw)^k+β(1+w)^d)}.

Then, as integer d→∞,

    F_d ∼ (2/√e) √(d ln ln d)/ln d.

The [full proof](../weighted_congestion_frontier/assets/R3/sharp_source_review/proof.md)
constructs a legal attaining asymptotic family and proves the matching upper
over every source parameter. With D=ln d,H=ln D,J=H−ln(2H), choose
w=D/(2d), n=floor(4dH/D²), k=ceil(D/(2J)), and β(1+w)^d=(√e/2)D/√(dH).
The main-resource factor tends to e; the light denominator's extra monomial
is at most d^(−1/2). Both attack ratios, divided by √(dH)/D, tend to 2/√e.

The critical upper reduction, for f=min(A,B)>1 and x=nw, is

    (f−1)² ≤ n ((1+w)/(1+x))^k,
    w ≥ ln f/d,   k ≥ ln f / ln((1+w)/x).

Any parameter sequence competing with the lower scale has w,x→0 and
ln f=(ln d)/2+O(ln ln d). The sharp scalar supremum
sup_x x exp[−λx/ln(1/x)]∼ln λ/(eλ) then yields the constant 2/√e.
The [independent attack](../weighted_congestion_frontier/assets/R3/sharp_source_review/review.md)
also reconstructs the every-state coverage and checks floor/ceil signs.
The complete proof resides in the linked current research package; this
navigation account does not supersede its mathematical statement.

Consequently a_*(d)≥(2/√e−o(1))√(d ln ln d)/ln d. This refines the published
exhibited Ω(√d/ln d) scale within the same exact parameter supremum; it
does not exceed that supremum or establish new global priority.

## WC-R3-FULL-TOPOLOGY-REDUCTION v3

Allow the same one-heavy/equal-light two-column strategy topology to use
arbitrary nonnegative-coefficient principal and side polynomials F,G of
degree at most d and any w>0. Let ρ=(1+√3)/2. For every α≥ρ, absence of an
α-PNE implies existence of a source-domain monomial certificate with
minimum strictly greater than α. The new certificate may have different
parameters. Versions v1 (α≥2) and v2 (α≥φ) are proved subcases of v3.

The [complete proof](../weighted_congestion_frontier/assets/R3/full_topology/proof.md)
uses the nonempty interval of light-stable states. An interval intersecting
its reflection gives an α-PNE. Otherwise its left boundary translates F;
its right boundary gives n′α(α−1)<1. For α≥ρ the right case has n′=1,
which inverts the weight scale and exchanges the two attacks. Endpoint
convexity and elimination of polynomial coefficients recover monomials.

For the topology's actual supremum T_d this proves

    F_d ≤ T_d ≤ max{ρ,F_d}.

In particular T_d=F_d for every d with F_d≥ρ, hence T_d has exactly the
same sharp asymptotic. This is a restricted-topology upper bound. It does
not restrict a_*(d) from above; arbitrary strategy incidence and heterogeneous
light weights remain outside this theorem.

## Finite degree 32: asymmetric crossover exceeds the full symmetric topology

**WC-R3-SOURCE32-178-v1** proves F_32<=89/50 over every source integer
n,k and real w,beta. A strict violation forces n<=55; 1760 eliminated
polynomials have complete negative Bernstein interval certificates. Two
independent implementations check all 1768 leaves. The
[full real-domain proof](../weighted_congestion_frontier/assets/R3/source32_bound/PROOF.md)
is a restricted-family upper bound, with no a_*(32) upper implication.

**WCF-R3-CROSS32-AUDIT-v1** constructs one G_32 with weights
(1,1/10,1/20,1/50) and seven complementary resource pairs. Every pure
state has a strict 9/5 improvement. Literal Fraction costs, all sixteen
states and sixty-four deviations, exact instance factor, and a second
strategy-set reconstruction are in the
[crossover package](../weighted_congestion_frontier/assets/R3/crossover_audit/README.md).

Together with full-topology v3, **WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1** gives
T_32<=89/50<9/5<B(G). The
[combined proof and review](../weighted_congestion_frontier/assets/R3/crossover_audit/separation.md)
lists every joint dependency. The symmetric class here allows arbitrary
nonnegative principal/side polynomials and all positive common light weights.
This is a finite-degree topology separation; global priority is unverified.

**WCF-R3-FIXED-DEGREE-FAIL-v1** precisely blocks a proposed extrapolation:
keeping those weights and amplitudes while increasing the six high degrees
has an exact 9/5-PNE at degree 40. Its best factors tend to
5235403/2930833<9/5. This does not restrict reweighting or increasing the
number of players.

## Local weight bands and their genuine boundary

**WC-R3-DENSE-SHARE-v1** and **WC-R3-DENSE-LOCAL-v1** give a self-contained
Shapley interface: for each resource, if all its potential users have weight
ratio at most R>=1, every minimum of the resource-minimum-scaled Shapley
potential is an R-PNE. The factor is independent of degree and cardinality.
The [multinomial coefficient proof](../weighted_congestion_frontier/assets/R3/dense_bands/README.md)
and [independent iid-support proof](../weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md)
both prove minw*c(W)<=phi_i<=maxw*c(W); arbitrary multiresource deviations,
empty strategies and zero costs are covered.

The same package separately records **WC-R3-DENSE-POT-SHARP-v1**,
**WC-R3-BAND-CURL-v1**, and **WC-R3-BAND-LINEAR-v1**: the stated selector's
R guarantee can be approached, band-specific normalization violates ordinary
exact-potential mixed differences, and the unchanged selector can lose at least
d/6 across two equal-weight bands despite exact PNE elsewhere. These are
specified-mechanism obstructions; they do not refute equilibrium existence.
The Shapley mechanism and bounded-weight literature already exist; exact
priority for these reconstructed interfaces has not been certified.

**WC-R3-POTENTIAL-DENSITY-PADDING-v1** is a different, full-model reduction:
adding positive-weight players with empty/{e} choices preserves every finite
alpha-equilibrium existence question by projection/lift. It can make every
occupied potential-weight interval contain at least any prescribed L users.
Therefore this minimum-potential-density subclass has exactly the same
universal threshold as the full class. The
[proof and separate audits](../weighted_congestion_frontier/assets/R3/potential_padding/proof.md)
use positivity of every nonzero nonnegative polynomial at positive loads.
This does not attack maximum sparse density, active density, or obligatory
participation; a nondecreasing-step example shows why the projection theorem's
polynomial condition must remain explicit.

## Shrinking-weight constant crossover interface

The [scaling package](../weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md)
keeps four players and fourteen resources, takes degree 32m^2 and light
weights (1/(10m),1/(20m),1/(50m)), and proves a uniform finite-to-limit
transport. **WCF-R3-SCALED-ORIGINAL-v1** has limiting factor 65/34 and
retains the original 9/5 obstruction for every integer m>=1. Retuned amplitudes
give **WCF-R3-SCALED-RETUNED-v2**: no 2-PNE for every m>=20, plus an exact
m=3, degree288 certificate; m=1,2 do have 2-PNE. The v1 m>=52 range is retained
as a proved subcase. The independent review gives the sharper uniform margin.

**WCF-R3-SCALED-TEMPLATE-v1** proves exactly the selected-witness template's
strict feasibility for alpha below the unique root r>2 of
r^3-r^2-2r-1=0. For each such alpha, fixed rational amplitudes are chosen
first, then a finite starting m, and all subsequent states are covered.
The [independent symbolic review](../weighted_congestion_frontier/assets/R3/limit_review/review.md)
checks all quantifiers and the endpoint. The template is not declared optimal
over the entire topology. These constant four-player families do not improve
the known growing lower envelope.

## State and continuation

Both general proofs have undergone separate internal reconstruction and
boundary attack; finite exact checks and diagnostic decimals are recorded
separately. External review and global novelty are unverified. WC-TARGET
remains OPEN: a full-class o(d) upper bound and an infinite lower family
strictly beyond the known exact source envelope are still missing.

The next valuable mechanism must change the topology or attack coverage.
Finite asymmetric high-support candidates are explored separately; no
finite test is used to infer an infinite-family result.
