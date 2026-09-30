# Reusable witness tools for heterogeneous location sets

Research note, 2026-09-30. This note gives a general closed-response-core theorem, a polynomial guarded-pure-menu algorithm for the sharp universal factor 2 with arbitrary heterogeneous catalogs, a verifiable transfer of the common-catalog golden-ratio theorem, an exact target-dependent feasibility reduction, and an exact solver for the cross-intersection-one class. Their guarantees come from response-core preservation, transport structure, and explicit local reductions, rather than the generic assertion that a finite list can be scanned.

The universal factor-2 result is proved by the legal-chord argument in universal_two.md and independently audited here. It uses no co-location argument. The earlier short-catalog construction below records the four-cycle stepping stone; Section 2C states the final universal algorithm and four-seed reduction.

## 1. Notation and the imported menu lemma

Facilities choose from finite nonempty sets U1,U2. Sites have fixed customer coverage; customer weights are positive binary rationals. For a legal ordered layout (s,t), write N(s,t) for the independent mixed customer NE set. Every such NE has constant total facility load V(s,t), the weight of customers covered by at least one site.

For every pair on which it is used, let F(s,t) be the deterministic menu in the uploaded Pro result: repaired all/single-customer pure seeds, equal-reach half splitting, the two-mixer templates, and one reach-based strong-chord witness. The menu is nonempty, polynomial to construct, label symmetric, and all its members are exact NE. Put

    u(s,t) = min_{sigma in F(s,t)} L_s(sigma).

The imported common-catalog result has the following stronger, and crucial, ring form. Suppose T is a set of sites on a directed cycle b, and positive numbers d(t) satisfy

    u(s,t) <= d(t) for all s,t in T,
    u(b(t),t) = d(t) for all t in T.

Then some s,t in T and sigma in F(s,t) satisfy

    L_s(sigma) >= d(t)/phi,   L_t(sigma) >= d(s)/phi.

The d(t) may include threats from outside T. This is precisely the scope of the common proof's closed-ring argument: its normalization, all co-locations, all chords and every customer witness are on T, while d retains the full-set maximum. Equivalently, one can simply apply the common-catalog finite-menu theorem to the catalog T: the two displayed premises imply max_{s in T}u(s,t)=d(t). Thus this note does not need a new audit of that proof's individual witness calls.

## 2. Balanced-response-cycle theorem

Let J=U1 intersect U2. Only compute pair menus with at least one opponent site in J. For t in J define the two full-catalog threat values

    D1(t)=max_{s in U1} u(s,t),
    D2(t)=max_{s in U2} u(s,t).

Build a directed graph G on J. Include an arc t -> s exactly when

    u(s,t)=D1(t)=D2(t).

Self-loops are allowed. Note that equality is not a numerical approximation: all menu loads and maxima are exact rationals.

**Theorem 1.** If G contains a directed cycle, the heterogeneous game has a phi-SPE that can be constructed in deterministic polynomial bit time without an exact m oracle. The on-path locations belong to that cycle. The construction needs only O(|J|(|U1|+|U2|)) pair-menu calls, followed by an ordinary graph cycle search and a scan of menus on one cycle. It does not need the whole rectangle U1 x U2.

**Proof.** Let T be the vertices on a cycle and set d(t)=D1(t)=D2(t). Every s in T belongs to both catalogs, so u(s,t)<=d(t). The successor b(t) attains equality. The imported menu lemma gives an on-path (s,t), with loads x>=d(t)/phi and y>=d(s)/phi. For a deviation r in U1, use a menu NE attaining u(r,t); its deviator load is at most D1(t)=d(t)<=phi x. For a deviation r in U2 use an NE attaining u(r,s), with the labels reversed; its deviator load is at most D2(s)=d(s)<=phi y. The two families of unilateral off-path ordered profiles are disjoint, except for the original profile, which is excluded from actual deviations. Hence these continuation choices are consistent. Fill every other ordered profile with the standard descending-weight pure-NE constructor. Every continuation is exact, and every facility deviation obeys the claimed factor. All loops, comparisons and local constructions are polynomial; rational bit lengths are those of the Pro menu. QED.

**Why this is more than restricting to U1 intersect U2.** A solution of the common subgame can be destroyed by a catalog-specific outside deviation. The graph explicitly checks all such threats, for both players. Conversely, an arbitrarily large population of outside sites and customers is allowed; their mutual interactions never have to be solved. The criterion is a verifiable sufficient condition, not a claim that every heterogeneous game has a balanced cycle.

### 2.1 A modular version that does not even construct outsider menus

Start with any nonempty common core K subset J. Construct only its menus and define

    dK(t)=max_{s in K}u(s,t).

For every t in K and every outsider r in Ui\K, obtain **one** exact customer NE at (r,t) whose deviator load is at most dK(t). Different pairs and different providers may use unrelated NE generators. Then the core's phi construction is already a phi-SPE of the whole heterogeneous game.

The proof is the same two inequalities as above. The external certificates can be supplied independently, combined by set union, and independently rechecked. They need not minimize anything, belong to the Pro menu, or use the same customer support structure.

An inexpensive sufficient condition is

    R_r <= min_{t in K} dK(t)  for every catalog-specific outsider r,

because every continuation payoff at r is bounded by its reach R_r. Under that condition any exact pure NE works. This gives an infinite class with arbitrary heterogeneous outside coverage patterns and arbitrarily many outside actions. A sharper implementation uses the opponent-specific bound R_r<=dK(t), and only generates a certificate for the pairs failing that bound. The common-core theorem and the outsider certificate generators are interchangeable modules.

This condition is meaningful even though it is sufficient rather than necessary. For example, take a common core with pairwise disjoint site populations of equal total weight H and at least two sites. Then dK(t)=H (deviation to another core site gives its whole reach). Arbitrarily many catalog-specific sites of reach at most H, with completely arbitrary incidence among themselves and with the core, preserve the certificate. Their incidence with core sites may share many atomic customers, and no local extremum needs to be computed. Larger, nontrivial common cores are covered by the identical criterion.

### 2.2 Finding the part of a core that matters

The graph criterion does not need to enumerate all subsets K. Compute D1,D2 on J once, discard vertices with unequal values, and retain only common-site arcs attaining both maxima. A linear-time strongly connected component computation finds a cycle or certifies that this particular balanced-cycle criterion fails. An SCC with more than one vertex works; a singleton works exactly if it has a self-loop.

The negative result is deliberately limited: an acyclic graph does not imply that no phi-SPE exists. The method reports a structural failure of the common-core route, not a game-theoretic impossibility.

## 2A. General closed-response-core reduction

This is the reusable structural theorem behind the preceding constructions. It is not specific to congestion, spatial coverage, linear follower costs, or finite witness menus.

### Model and exact quantifiers

Two leaders simultaneously choose s in A and t in B, where A,B are finite nonempty sets. Their labeled action pair is publicly observed and starts a separate continuation subgame. For each pair (s,t), let E(s,t) be a nonempty collection of permitted exact continuation equilibria. A member e gives the leaders nonnegative payoffs g1(s,t,e),g2(s,t,e). Assume the minimum of each payoff over E(s,t) is attained. Compact equilibrium sets with continuous payoffs suffice; finite menus also suffice. The two minimizers need not be the same continuation.

The continuation selected at one labeled pair may be chosen independently of that at another pair. There is no ex ante commitment restricting the continuation rule across different pairs. If the follower play has additional stages, each member of E is required to be an equilibrium of the appropriate type for that whole continuation subgame, such as an SPE. The theorem itself does not change that equilibrium requirement.

Write

    m1(s,t)=min_e g1(s,t,e),   m2(s,t)=min_e g2(s,t,e),
    D1(t)=max_{s in A}m1(s,t), D2(s)=max_{t in B}m2(s,t).

An alpha-stable witness consists of an on-path pair (s,t) and e in E(s,t) whose payoffs x,y satisfy

    x >= D1(t)/alpha,   y >= D2(s)/alpha.                 (K1)

Here alpha>=1. Nonnegativity is used in the equivalence between this definition and ordinary multiplicative stability: the maxima D include the option of staying at the original action. That option causes no problem because its minimum payoff is at most the actual payoff, and actual payoff <= alpha times actual payoff. The theorem as written should not be applied to negative leader payoffs.

**Exact selection lemma.** Such a witness exists if and only if an alpha-stable leader profile can be completed by permitted continuations at every pair.

Necessity follows because the actual continuation after a deviation pays its deviator at least the corresponding m. Sufficiency chooses a minimizer of m1 at every true first-leader deviation (r,t), and a minimizer of m2 at every true second-leader deviation (s,r'). These two sets of off-path labeled profiles are disjoint: their intersection could only be (s,t), excluded from actual deviations. Thus there is no incompatible requirement to minimize both payoffs at one off-path profile. Choose arbitrary permitted continuations elsewhere. This also proves that different local punishment procedures can be composed without a common optimizer.

### The theorem

Choose arbitrary maximizers

    b1(t) in argmax_{s in A}m1(s,t),
    b2(s) in argmax_{t in B}m2(s,t).

Treat the action sets as disjoint colored copies even when an action label or physical location occurs in both. Draw arcs t -> b1(t) from B to A, and s -> b2(s) from A to B. Every node has one outgoing arc. Let T be any directed simple cycle, and put A_T=T intersect A and B_T=T intersect B.

**Theorem 1A (closed-response-core lifting).**

1. The cycle has 2 ell vertices, with |A_T|=|B_T|=ell<=min(|A|,|B|).
2. For every cycle opponent, restricting both leaders to A_T,B_T preserves its full-game threat value exactly:

       max_{s in A_T}m1(s,t)=D1(t)  for t in B_T,
       max_{t in B_T}m2(s,t)=D2(s)  for s in A_T.          (K2)

3. Any alpha-stable profile of this restricted game, using the unchanged permitted continuation sets E(s,t), lifts to an alpha-stable profile of the full game with the same on-path pair and continuation.
4. Consequently, if every induced ell-by-ell game with ell<=k has an alpha-stable permitted continuation selection, then every game with min(|A|,|B|)<=k has one. It is enough to know this property for the closed response cores that arise; requiring all such induced games is a convenient sufficient hypothesis.

**Proof.** Every arc changes color, so a simple cycle alternates and uses equally many vertices of each color. This proves part 1, including the two-vertex case. For a cycle vertex t in B_T, its outgoing maximizer b1(t) belongs to A_T. The restricted maximum is at most the full maximum D1(t), and at least m1(b1(t),t)=D1(t); hence equality. The second equality is identical with the colors reversed. This proves part 2. By the exact selection lemma, a stable restricted profile satisfies (K1) with restricted threats. Equation (K2) replaces those by full threats, and the lemma supplies all full-game punishment continuations. This proves part 3. The selected cycle is one of the cores assumed in part 4. QED.

### What the theorem does, and what it does not do

This is a reduction in the **size of the leader action obstruction**, not an enumeration bound. A theorem proved for small balanced rectangles transfers to arbitrarily long catalogs on the other side. A failure of global alpha-stability necessarily survives in a closed square core of size at most the smaller catalog. A merely arbitrary small subgame does not have this property: the two equalities (K2), separately for the two colors, are essential.

The theorem requires the *full-game* maxima while choosing the response core. Taking best responses only in an arbitrary selected subgame and then adding the omitted deviations is invalid. It does not say that the small core can always be found in polynomial time: computing exact m can be NP-hard. If E is a supplied polynomial menu, however, its minima are available by scanning, and the theorem applies to that same menu correspondence. One then needs a small-core existence theorem that is valid for those menus, not a theorem that freely uses excluded continuations.

This also explains the distinction from ordinary best-response cycles. The arcs maximize minimum attainable continuation payoffs, and (K2) makes the off-path punishment threats survive restriction. They are not best responses to a continuation already chosen on the cycle edges.

### Algorithmic corollary: the sharp rho theorem with one short catalog

Combine Theorem 1A with the 2-by-2 cross-intersection-one theorem proved in asym_research/lower.md. If every legal layout has at most one common customer and

    min(|U1|,|U2|) <= 2,

then a rho-SPE exists for rho=2 cos(pi/7), regardless of the other catalog's size. This factor is sharp because its 2-by-2 subclass already has the matching lower-bound family. No strict-reach assumption is needed: the small-core theorem handles ties, and the local minima at a tie are the two endpoints of the attainable load interval.

Let M be the larger catalog size. The formulas of Theorem 3 compute both exact local minima over at most 2M legal pairs in O(Mn) straightforward incidence-processing time and polynomial bit complexity. Choose the two maximizer maps and find a cycle. It contains at most four vertices and hence at most four legal on-path layouts. At those layouts, the exact balancing/clamping formula of Theorem 3 finds a rational factor alpha<=rho and its on-path probability. Store the corresponding exact minimum continuations for every genuine deviation. There is no algebraic probability or irrational output requirement: rho is the universal guarantee, while the instance certificate uses its attained rational alpha.

Equal-reach mixing and overlapping physical catalogs are both safe. A tied pair contributes its exact endpoint minima and an entire on-path load interval; the clamp formula uses that interval. A shared physical site appears as two colored action nodes, and all continuations are still indexed by labeled pairs, so the punishment families remain disjoint.

The theorem also transfers this sharp guarantee to arbitrary strictly increasing customer-specific realized-load costs in the same cross-intersection-one class. The local equilibrium correspondence is unchanged by those costs, as proved below. This is an application to a distinct follower-cost family, without asserting that generic nonlinear multi-customer continuations behave like linear ones.

## 2B. A polynomial pure-witness closure for arbitrary overlaps and one short catalog

The transport proof in asym_research/general_four_cycle.md has now been independently checked against the generic theorem above. Its initially stated exact-m result has a stronger finite-menu form.

For a pair with k common customers, define R(s,t) as follows. Start all common customers on either side, or put one specified common customer on one side and all others on the other side, using both orientations. For each of these 2(k+1) seeds, retain it immediately if it is already a pure NE. Otherwise let g be its initial absolute load gap: retain a repaired witness only if every common customer on the initially lower-load side has weight at least g. Under that guard, repeatedly move a largest-weight improving customer from the originally higher side and stop at the first load reversal or when no improvement remains. Discard unqualified seeds. The quota-preserving repair lemma proves the output is a pure NE. Keep every retained assignment as both an on-path candidate and a possible punishment. All-on-one seeds ensure the menu is nonempty. Each guarded repair has at most k moves and can be implemented by O(k^2) arithmetic operations, so the whole pair menu takes O((k+1)^3). No half-mixing, two-mixer, strong-chord, or local m optimization is used.

**Theorem 1B.** If min(|U1|,|U2|)<=2, with arbitrary positive rational customer weights and arbitrary overlaps, the R menus alone contain a factor-2 stable witness relative to their own punishment minima. Consequently a 2-SPE with pure facility actions and exact pure customer continuations after every layout can be constructed in polynomial bit time. The constant 2 is sharp already with two actions per provider and at most two common customers per legal pair, by the independently checked family in tight_two_lower.md. If the larger catalog has M actions, a conservative arithmetic bound is O(M(n+1)^3); all intermediate rational bit lengths are polynomial in the input bit length.

**Complete closure audit.** Set u_i=min over R of the corresponding load, define full two-color D values from these u values, and take a simple response cycle. It has length two or four. A two-cycle is immediate because every menu member gives both facilities at least their respective full D values. Suppose a four-cycle contains no factor-2 stable R witness, and normalize max D=1. On every directed edge every R member has responder P>=D(source) and incumbent Q<D(target)/2. Then:

1. Select a menu member minimizing the responder. Constant total covered load gives R_source<=P+Q=D(source)+Q<3/2. This uses no minimization outside R.
2. A visible customer H>=1/2 must be visible at the next cycle site because otherwise every R member would force an incumbent load >=1/2. Thus it covers the whole cycle.
3. The assignment putting H on the incumbent and all other common customers on the responder is exactly an R seed. If R_target>=R_source minus the other-common mass, either this seed is already an NE or its largest-weight repair preserves incumbent load at least H. The reach bound <3/2 supplies the repair premise. Its output belongs to R and contradicts Q<1/2. Therefore every edge would strictly decrease reach, impossible on a cycle. All visible customers consequently weigh <1/2.
4. Every subsequent equilibrium used in the four-cycle transport proof can be any pure menu member. On the edge whose source has D=1, no common customer can be sent to its responder: the gap exceeds 1/2, larger than every visible weight. Hence the original source reach R1 is below b/2, and the next site's population outside it has weight at least one.
5. With D values (1,b,c,e) in cycle order, the set inclusions in that proof give b>2e, c<e+1/2, c+e>1 and therefore e>1/4 and b-c/2>e/2. They use only forced private loads and menu payoff inequalities.
6. Choose a pure menu member on edge 2->3. Its transferred customer set X has total weight >1-c/2>=1/2, and each member has weight >b-c/2>e/2. In a pure menu member on edge 3->4 every member of X must therefore move to site 4, because incumbent load is <e/2. Pure stability gives a second individual bound w>c-e/2. Combining them yields w>(4b-e)/6>b/2>R1. Every member of X is thus absent from site 1 and forced to site 4 in layout (4,1). Their total weight >1/2 contradicts that edge's incumbent bound <1/2.

Thus the contradiction is entirely within the pre-generated R menus. By Theorem 1A, the found cycle witness lifts to the full heterogeneous game using R-minimizing pure off-path continuations. All remaining layouts use the deterministic pure-NE routine. This proves both menu completeness and the stated algorithm. The fixed seed index, at most one named customer and one orientation, does not depend on the D values or on the discovered cycle. QED.

**Nonlinear cost corollary.** The same algorithm and sharp guarantee hold if each customer has an arbitrary strictly increasing function f_i of its realized facility load, with the same f_i at the two providers. Every continuation produced here is pure. At a pure profile the comparison f_i(L_current) versus f_i(L_other+w_i) has exactly the same sign as the linear-load comparison, so every constructed pure NE remains an exact NE. No evaluation of f_i and no equivalence of mixed-NE sets is needed. The tight two-common-customer lower-bound family has a unique continuation at every pair by successive pointwise strict dominance; these strict comparisons are also preserved by every such f_i. Thus the sharpness statement survives, not just the upper bound.

This is a second, independent use of the Pro witness idea. In the common-catalog phi theorem, complicated mixed templates are necessary for its proof. For the short-catalog factor-2 theorem, a strictly smaller pure menu is closed under every required construction, and the guarantee does not depend on the common-catalog theorem. The result is not an assertion that an arbitrary realizable upper bound table works.

## 2C. Final universal theorem and the four-seed algorithm

The completed argument in `universal_two.md` removes the short-catalog assumption entirely. Its proof has been independently checked, including both long-cycle cases, purity of the minimizing menu witness, all color constraints, and the full-game scope of every D value.

**Theorem 1C (universal finite-menu closure).** For arbitrary finite U1,U2, the guarded pure menus R contain a factor-2 stable witness relative to their own minimum punishment values. Thus the algorithm constructs a sharp universal 2-SPE with pure customer NE after every layout, for arbitrary heterogeneous catalogs. With N1=|U1| and N2=|U2|, the full-singleton implementation uses O(N1 N2 (n+1)^3) rational arithmetic operations. The local-m NP-hardness is bypassed entirely.

For clarity, the new part of the closure proof is summarized with all logical dependencies. Under failure of all menu quota witnesses, take a cycle of even length ell>=4, normalize max D=1, and name its first three, last, and penultimate vertices A,B,C,F,G. Their D values are 1,b,c,e,g. The initial edge and the heavy-customer argument already give all visible weights <1/2, E=C_B\C_A of total weight at least one, R_A<b/2, b>2e, and R_F<e+1/2. A pure witness on B->C sends a set X of E-customers of total weight >1-c/2>=1/2 to C, each with weight >h=b-c/2. Since weight(C_F\C_A)<1/2, some member of X is absent from F. The legal C--F chord gives z=weight(C_C\C_F)>h and z<=e; hence c>2b-2e>2e and c>b.

* If h>=e/2, C has private load >e/2 at chord (C,F), so every menu witness there must give F load <c/2. Select the pure menu witness minimizing C: its C-load is <=e<c/2. Therefore every customer visible at C or F has weight <c/2. For **any** action s of A's color, the full-game private inequality weight(C_s\C_F)<=e now forces every customer visible at s to have weight <c/2. Consequently all common customers on all cycle edges have weight <c/2. Starting from C, where D=c and R_C>=b>=c/2, a successor with D<=c would have responder-incumbent gap >c/2, so no common customer could move forward in a pure menu NE. That would force the incumbent's entire reach below c/2, a contradiction. Inductively every successor has D>c and reach >=c, eventually contradicting D(F)=e<c.
* If h<e/2, then c>2b-e>3e, so e<1/3. If g>=(1+e)/2, the G->F edge has gap >1/2 and can transfer no common customer, implying R_G<e/2. The legal B--G chord then gives g>=weight(C_B\C_G)>1-e/2, whereas g<=R_F<e+1/2, impossible for e<1/3. Thus g<(1+e)/2 and g+e<1. The set inclusion E intersect C_G subset (C_G\C_F) union (C_F\C_A) bounds its weight by <e/2+1/2. Hence B's private load at chord (B,G) exceeds (1-e)/2>g/2. Failure of stability forces every G-load there below b/2. Choose the menu witness minimizing B, whose B-load is <=g: total load is then <g+b/2, yet at least R_B>=1. Therefore b>1-e and c>2b-e>2-3e>1, contradicting normalization.

Both chords are opposite-color for every even ell>=4, including ell=4 where G=C. Every minimizing witness is in the fixed pure menu. No mixed-extremum claim or same-color layout is used. This proves the universal closure.

### Four seeds suffice

For each pair retain only the all-left and all-right seeds and the two seeds that isolate its **largest-weight common customer**, resolving equal weights by the same fixed global customer-ID priority at every pair. Apply the identical guarded repair rule. The resulting menu has at most four witnesses and is nonempty.

The only place the proof names a particular customer in a seed is the exclusion of a cycle-visible customer of weight at least 1/2. If such customers exist, choose the cycle-visible customer H maximizing (weight, fixed priority). The forced-load argument propagates H to every cycle vertex. On every cycle edge H is therefore common and is exactly that pair's chosen largest common customer: any larger or higher-priority tied common customer would itself be visible on the cycle, contradicting the choice of H. Thus every single-H seed actually used by the proof belongs to the four-seed menu. The rest of the proof requires only nonempty pure menus, shared by the two load orientations. It is unchanged.

**Four-seed corollary.** The sharp universal 2-SPE can be constructed using at most four exact pure customer NE witnesses per legal layout. A conservative arithmetic bound is

    O(N1 N2 (n+1)^2).

The weights and all intermediate sums have B=O(L+log(n+1)) bits after an analysis-only common-denominator scaling; the output ratio divides two such sums. A conservative ordinary bit bound is O(N1 N2 (n+1)^2 B^3). The compact continuation certificate stores one on-path pure assignment and N1+N2-2 deviation assignments, plus a fixed default pure-NE procedure. Direct verification uses O((N1+N2)(n+1)) rational operations and never checks optimality of a punishment.

`r_menu_solver.py` uses the independently tested four-seed implementation by default; `--all-singletons` selects the larger audit menu and `--maximum-only` remains a compatibility alias for the default. Both modes use the same global response values, cycle search, and direct output-certificate checks. The nonlinear-cost corollary applies unchanged because every constructed continuation remains pure.

## 3. Exact target-dependent feasibility reduction

At a fixed pair, let A,B be forced private loads and w1,...,wn the common weights. Let V=A+B+sum_i wi and Delta=L_A-L_B. A request L_A>=a,L_B>=b is equivalent to

    Delta in I=[2a-V, V-2b].

When I is empty, the request fails just by total mass. Otherwise it is an exact NE-feasibility question, which can be hard.

**Theorem 2 (separated-interval reduction).** Suppose I=[ell,h] lies strictly on one side of zero. Let eta=min_{z in I}|z| and retain only the k customers with wi>=eta. If I is positive, replace B by B+sum_{wi<eta}wi; if I is negative, replace A by A+sum_{wi<eta}wi. Remove the light customers from the strategic customer list. There is a bijection between NE of the original game with gap in I and NE of the reduced game with gap in I, obtained by forcing every removed customer to the lower-load facility. It preserves both facility loads exactly.

**Proof.** A customer's conditional first-minus-second cost difference is

    gamma_i=Delta+wi(1-2pi).

If Delta>=eta>wi, gamma_i>0 for every pi in [0,1], so the customer must use the second facility with probability one. If Delta<=-eta<-wi, gamma_i<0, so it must use the first. Absorbing its deterministic load into the corresponding private load changes neither the total expected load nor any remaining customer's conditional costs. Thus restriction and forced extension are mutually inverse equilibrium-preserving maps. The strict cutoff matters: a customer with wi=eta may be indifferent at the endpoint and must be retained. QED.

**Algorithmic consequence.** Feed the reduced game to the exact threshold/MITM constructor from astra_ring. Test the nonnegative single-valley objective dist(Delta,I), with target any point of I. Its minimum is zero exactly when the quota request is feasible. The runtime is

    poly(n,L) + poly(k,L) 3^{ceil(k/2)},

with exact rational witnesses. This is an explicit reduction to k strategic customers and two aggregate private loads; it should not be called a polynomial-size kernel in the parameterized-complexity sense, since retained binary weights need not have O(poly(k)) bits.

The reduction can be much smaller than raw overlap. A pair may have millions of tiny common customers and only three weights above the requested gap distance. The exact target feasibility query then has only three strategic atoms; all tiny jobs are processed in one linear input pass and never enter support enumeration.

**Composition with Theorem 1.** An outsider certificate against core t needs only one equilibrium with L_r<=dK(t), equivalently a one-sided gap bound. Partition that bound by sign and existing weight thresholds; on each separated interval use the reduction. If an easy pure/strong-chord witness already succeeds, no exact kernel call is needed. Any successful local witness can be spliced into the global core certificate. The kernel is an optional exact local fallback, not a general polynomial guarantee for arbitrary quota queries.

### 3.1 An important false simplification

Even the factor-2 quotas L_A>=R_A/2,L_B>=R_B/2 do not have a simple “failure means unique dominant atom” characterization. Take

    A=1, B=0, common weights (2,4).

The reaches are 7 and 6, and the quota gap interval is [0,1]. The complete equilibrium gap set is {-1,3}: the two stable pure split assignments have gaps -1 and 3; the equilibrium with both customers mixing has gap -1; no one-mixer equilibrium exists because its required constant equation cannot vanish. Thus both quotas fail despite multiple equilibria. This is a genuine local nonconvexity obstacle, not a lack of total mass.

For beta=9/5 a mass-feasible example is A=18,B=3, common weights (20,3,28). The own-reach quota interval is [14/3,12]. Exact support enumeration rejects it although equilibria with gaps -18 and 20 exist. The smaller two-customer example already supplies a complete hand-checkable obstruction to the proposed general simplification.

## 4. Second substantive class: cross-intersection at most one

This class allows U1 intersect U2 to be empty, arbitrarily many sites and customers, and arbitrary binary rational weights. Assume every legal cross pair (s,t) has at most one common customer. No restriction is placed on how many same-provider locations a customer can access.

**Theorem 3.** The exact best attainable approximation factor alpha* and a witnessing continuation selection can be computed in deterministic polynomial bit time for this class. The theorem remains valid when every customer has an arbitrary strictly increasing cost function of realized load, using the same function at both providers. The functions need not be quadratic or differentiable.

**Local proof.** With no common customer, the loads are fixed at (A,B). With one common customer of weight w, its cost from choosing the first facility is f_i(A+w), and from choosing the second is f_i(B+w). These quantities do not depend on its mixing probability. Strict increase therefore gives:

* A<B: the unique continuation is (A+w,B);
* A>B: the unique continuation is (A,B+w);
* A=B: every p in [0,1] is an NE, giving first load x in [A,A+w] and second load V-x.

The same characterization holds for linear costs. In the unequal-reach case, the common customer chooses the lower-reach site; in the equal-reach case the full interval, not merely its endpoints, must be retained.

**Global algorithm and proof.** These formulas compute both exact deviation minima m1(s,t),m2(s,t) for every cross pair. Form

    d1(t)=max_{s in U1} m1(s,t),
    d2(s)=max_{t in U2} m2(s,t).

For any layout with an attainable first-load interval [l,h] (a singleton in a unique case), minimize

    max{1, d1(t)/x, d2(s)/(V-x)}   over x in [l,h].

If d1+d2>0 the unconstrained balancing point is

    x0 = V d1(t)/(d1(t)+d2(s));

clamp x0 to [l,h]. This is optimal because d1/x is decreasing and d2/(V-x) increasing. If both threats are zero, use any feasible x and factor one. Interpret a positive numerator over zero load as infinity and 0/0 as zero. Handle the zero-covered-mass layout accordingly. Take the best factor over all cross pairs. The chosen probabilities and all minimizing off-path witnesses are rational of polynomial bit length. The construction costs O(|U1||U2| n) straightforward incidence-processing work, plus polynomial arithmetic.

For necessity, any continuation after a deviation gives that facility at least the corresponding exact m, so every SPE at the given layout has factor at least the displayed objective. For sufficiency, the minimizing continuation of each actual unilateral deviation can be selected separately, because the two unilateral-neighbor families have no common off-path labeled profile. All other layouts may use their explicit local NE formulas. Hence the minimum computed by the algorithm equals alpha*, rather than merely giving an upper bound. QED.

This is useful for the asymmetric lower-bound program: the four-site rho=2cos(pi/7) constructions lie in this class. Any candidate with cross-intersection one can be evaluated exactly without restrictions on mixing supports, without an m oracle, and without invoking a claimed general heterogeneous upper bound. With nonlinear costs it is also a second application beyond the quadratic strategic-equivalence class: the local reason is deterministic conditional loads, not quadratic cancellation.

## 5. Why none of this contradicts hard local m

The local minimum-equilibrium-load problem is weakly NP-hard for unrestricted binary-weight common-customer lists, even with no private loads, as proved in astra_alg/hardness_proof.md.

Theorem 1 never requests m: it uses attainable upper bounds u and a structurally checkable common response core. Arbitrary outside pairs need only one punishment witness, and never need proof that this witness is optimal. Theorem 2 retains an exponential dependence on the number of strategically unforced atoms; when the target interval approaches zero, that number can equal all n customers. Theorem 3 restricts every queried cross pair to at most one strategically shared customer, making the hard subset-selection mechanism unavailable. The unchanged NP-hard class is excluded in a different, explicit way by each theorem.

## 6. Claims and open boundaries

Established here: the general closed-response-core theorem; the guarded-R-menu closure and polynomial factor-2 construction for arbitrary catalogs, after independent audits of both the four-cycle proof and the universal legal-chord proof; the separated-interval reduction; and the exact cross-intersection-one solver. The heterogeneous balanced-common-core phi result additionally uses the supplied common-catalog menu theorem. Combined with lower.md, the generic core theorem gives the sharp rho guarantee for cross-intersection-one games with one catalog of size at most two. Arbitrary increasing realized customer-cost functions preserve the latter class exactly.

Not established: polynomial arbitrary-quota feasibility or a first-in-literature novelty claim. A universal factor below 2 for arbitrary heterogeneous catalogs is excluded by the explicit six-customer lower-bound family. The finite menu is valuable because its templates and exact verification can be reused by these procedures, not because every finite game admits a polynomial list.

## 7. Runnable implementations and checks

`r_menu_solver.py` implements Theorem 1C with the guarded R menu, exact `Fraction` arithmetic, the colored response-cycle search, pure on-path/off-path witnesses, and a direct certificate verifier that does not inspect menu minima or D values. `cross_one.py` implements Theorem 3 and computes the exact instance optimum rather than merely a universal bound. Both accept JSON with `weights`, `locations`, `U1`, and `U2`. The latter implementation passed 200 seeded exact-rational random certificate checks. Additional R-menu validation is recorded in `r_menu_verification.json`.

The guarded-R implementation passed 500 seeded random full certificate checks, 150 comparisons against an independent exhaustive ternary-support oracle, four directed edge/lower-bound checks, and a deliberately corrupted certificate rejection. Tests are implementation evidence; Theorem 1B supplies the universal guarantee. The kappa=2 instance in `cross_two_above_rho.json` was additionally evaluated by three independent routes: the R-menu solver, the ternary-support oracle, and `bounded_overlap.py`. All returned `1101031071/611004109`, strictly above rho and below 2. This refutes extending the sharp rho theorem from cross-intersection one to two; it is fully consistent with the arbitrary-overlap factor-2 theorem.

The stronger six-customer epsilon family in `tight_two_lower.md` was independently checked at epsilon=1/100, 1/1000, 1/10000 using all three routes. Its exact factors are 35/19, 335/169, 3335/1669, respectively, and symbolically alpha*(epsilon)=(2+10 epsilon)/(1+14 epsilon) tends to 2. Pointwise strict-dominance checks rule out every additional mixed equilibrium, so this is a sharp lower-bound proof rather than numerical evidence alone. Details and full certificates are in `tight_two_independent_audit.json`.
