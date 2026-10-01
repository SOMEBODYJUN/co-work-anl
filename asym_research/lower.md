> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../README.md), [claim registry](../CLAIMS.md) and [source-status guide](../PROVENANCE.md) for current scope. Section 11's unrestricted interval is superseded by the strict overlap-two lower family approaching factor 2.

# Heterogeneous two-facility lower bounds: a sharp structural subclass

Research checkpoint: 2026-09-30. This note does **not** claim a universal upper bound for arbitrary heterogeneous allowed sets. Its main theorem resolves an entire subclass, rather than improving the existing decimal lower bound.

## 1. Model and the class being resolved

There are two facilities with finite allowed sets `U₁,U₂`, and `min(|U₁|,|U₂|)≤2`. One side may have arbitrarily many choices. The central classification proof first treats `U₁={A,B}`, `U₂={C,D}`; §6.3 lifts it to the full stated class. Every customer has a positive weight, reaches an arbitrary subset of the locations, and, when covered, must choose one reachable facility. Its cost is the realized total weight at that facility, evaluated in expectation. Facilities maximize expected assigned weight. A continuation may choose **any exact independent mixed customer Nash equilibrium** separately at each labeled layout.

Write `S_v` for the set of customers reaching location `v`, and `R_v=w(S_v)` for its reach. The **single-common-customer condition** is

> For every `u∈U₁` and `v∈U₂`, `|S_u∩S_v|≤1`.

Customers may reach several locations of the same facility; there is no assumption that all customers are exclusive to one location or one pair. In the initial strict version assume `R_u≠R_v` whenever a cross pair shares a customer. This makes every continuation unique. A limit argument below removes the strict-reach assumption.

Let `φ=(1+√5)/2` and let `ρ` be the largest real root of

`q(z)=z³−z²−2z+1`.

Thus `ρ=2 cos(π/7)≈1.8019377358`.

## 2. The sharp theorem

**Theorem.** Within the class above, the optimal universal approximate-SPE factor is exactly `ρ`.

1. Every instance has a pure facility layout and a complete **pure** exact customer continuation selection giving a `ρ`-approximate SPE. Keeping a best-response column for each of the at most two rows reduces the problem to at most four layouts, under one fixed pure continuation rule.
2. When all cross pairs sharing a customer have different reaches, some layout actually has factor strictly below `ρ`.
3. For every `α<ρ`, there is a six-customer instance in the strict class, with disjoint two-element allowed sets and positive rational (or integer) weights, for which no continuation selection gives an `α`-approximate SPE. Every layout in these lower-bound instances has a unique customer NE; indeed it has a unique CCE.

The upper bound requires at most two choices on one side, and at most one common customer per cross pair. The other side may have arbitrarily many choices. The proof gives a classification of every four-cycle whose improvement ratios exceed `φ`: the common customer at `AC` and at `AD` must be the same heavy customer, reaching all three sites `A,C,D`.

## 3. Unique-continuation lemma

At a cross pair `u,v`, if no customer reaches both, all choices are forced. Otherwise let the unique common customer have weight `w`. All other covered customers are forced, with private loads `R_u−w` and `R_v−w`. The common customer's two costs are the constants

`(R_u−w)+w=R_u`, and `(R_v−w)+w=R_v`.

If `R_u<R_v`, it strictly chooses `u`. Thus the load vector is

`(R_u, R_v−w)`.

In particular, the lower-reach facility receives its entire reach. The customer's strict dominance makes the full customer equilibrium unique, even under CCE: putting positive probability on the other choice would make an unconditional switch strictly profitable. When reaches tie, any probability for this one customer is an exact NE; the possible first-facility loads form `[R_u−w,R_u]`.

## 4. The forced structure of a hard four-cycle

Here first assume every cross pair sharing a customer has distinct reaches. An edge with no overlap is harmless if its reaches tie: both facility payoffs are simply their reaches. The proof below handles these unshared ties directly; it does not need a perturbation for the strict conclusion.

Fix `r>φ`. Suppose **each of the four layouts has a deviation improving its facility payoff by a factor at least `r`**. Treat a move from zero payoff to positive payoff as an improvement of every finite factor; a move from zero to zero is not an improvement. A layout with both facilities unable to earn a positive payoff is stable and therefore cannot occur in this assumption.

The four layouts form a square. There cannot be a directed two-cycle of strict improvements along one edge, because the same facility's payoff cannot strictly increase both ways with its opponent fixed. Every vertex has an outgoing edge, so a directed four-cycle is forced.

Relabel the facilities if necessary so that a location of globally largest reach is the second facility's `D`, and let `A` be a largest-reach location of the first facility. Write

`a=R_A, b=R_B, c=R_C, d=R_D`.

If `d=a` and `AD` shares a customer, this violates the strict assumption. If `d=a` and there is no common customer, both facilities at `AD` receive their maximum possible reach, so `AD` is already an exact SPE. Under the hard-cycle assumption this is impossible. Therefore `d>a≥b`. At layout `AD`, the first facility receives its full maximum reach `a`. It cannot improve. Therefore the four-cycle must be

`AD → AC → BC → BD → AD`.

At `AC`, the move from `A` to `B` is an improvement. If `a<c`, the facility at `A` would receive its full maximum reach and could not improve. If `a=c`, either the pair has a common customer, violating the strict assumption, or it has none and `A` again receives full reach. Hence

`c<a<d`.

At both `BD` and `AD`, the first facility is at the lower-reach location and receives respectively `b` and `a`. The last cycle inequality is therefore

`a ≥ r b`.                                                    (4.1)

Here `b>0`: otherwise the preceding move `AC→BC` could not be a strict improvement.

### 4.1 The fourth reach must be the smallest

Let `X` be the weight of the common customer at `AC` (put `X=0` if there is none). Its first-facility load is `a−X`, and `X≤c`. If `b≥c`, then the first-facility payoff at `BC` is at most `b`, so the first cycle inequality and (4.1) give

`b ≥ r(a−X) ≥ r(a−c) ≥ r(a−b) ≥ r(r−1)b`.

Thus `r(r−1)≤1`, contradicting `r>φ`. Consequently every such hard cycle has the strict order

`b<c<a<d`.                                                    (4.2)

### 4.2 The two overlaps touching A are the same atomic customer

Let `Z` be the common-customer weight at `AD`, with zero if absent. The cycle inequalities `AC→BC` and `AD→AC`, using (4.2), are

`b ≥ r(a−X)`,         `c ≥ r(d−Z)`.

Equivalently,

`X ≥ a−b/r`,          `Z ≥ d−c/r`.                            (4.3)

If the common customers at `AC` and `AD` were distinct, both would be counted in the reach of `A`, giving `a≥X+Z`. Together with (4.3), this gives

`r d ≤ b+c`.

But `b≤a/r<d/r` and `c<a<d`, hence

`r d < (1+1/r)d`,

which again implies `r<φ`. This is impossible. Thus the overlaps at `AC` and `AD` are one and the same customer `x`, of weight `X=Z`.

Furthermore, by (4.1) and (4.3),

`X ≥ a−b/r ≥ (r−1/r)b > b`.

The customer `x` therefore cannot reach `B`. It reaches exactly `A,C,D` among these four choices. If `Y` is the common-customer weight at `BC`, it is a different customer, and

`c ≥ X+Y`.                                                   (4.4)

An optional common customer at `BD` is also different from `x`; call its weight `T≥0`. It can be the same customer as `Y` or a different one. Nothing further about this optional overlap is needed.

This classification is the structural content beyond the previously known six-vertex template.

## 5. The cubic bound for every classified instance

In the forced order (4.2), the unique payoff matrix is

| First / second | C | D |
|---|---:|---:|
| A | `(a−X,c)` | `(a,d−X)` |
| B | `(b,c−Y)` | `(b,d−T)` |

The four cycle inequalities are

`b≥r(a−X)`, `d−T≥r(c−Y)`, `a≥rb`, `c≥r(d−X)`.

The first and third imply

`a ≤ r² X/(r²−1)`.

The second and (4.4) imply

`d ≥ d−T ≥ r(c−Y) ≥ rX`.

The fourth consequently implies

`c ≥ r(d−X) ≥ r(r−1)X`.

Here `X>0`. Since `c<a`, combining these bounds gives

`r(r−1) < r²/(r²−1)`.

For `r>1`, this is equivalent to

`r³−r²−2r+1<0`.                                              (5.1)

The polynomial `q` is strictly increasing on `[φ,∞)`, since `q'(r)=3r²−2r−2>0` there. Its unique zero in that interval is `ρ`. Thus (5.1) forces `r<ρ`.

Now if every layout had maximum unilateral improvement factor at least `ρ`, the preceding proof with `r=ρ` would contradict (5.1). Hence some layout has maximum unilateral improvement factor strictly below `ρ`. Because all continuations are unique, that layout is already a complete approximate SPE with the unique customer continuation at every layout.

## 6. Equal reaches and co-location do not create a gap in the subclass theorem

For an instance with reach ties, replace each labeled allowed location by a distinct copy carrying the same original customer incidence. If two allowed labels represented the same original physical location, their copies initially have identical incidence; this is merely a relabeling of the original layout game.

Add at each copy a new private customer of weight `ε h_v`, with positive pairwise distinct constants `h_v`. Choose a sequence `ε→0` avoiding the finitely many exceptional values that cause cross-reach equalities. This perturbation preserves the single-common-customer condition: new customers reach only their own copies. Every perturbed instance has a layout and complete continuation with factor below `ρ`.

There are finitely many labeled layouts, so a subsequence uses the same on-path layout. There are finitely many customer probabilities at the four continuations, all in `[0,1]`; take a convergent subsequence of all original-customer probabilities together. The Nash inequalities for linear expected congestion and all facility `ρ`-approximation inequalities are closed polynomial inequalities in weights and probabilities. Passing to the limit preserves them. The new private customers have vanishing weight and can be discarded. The remaining continuation is an exact independent mixed customer NE at every original labeled layout and is a `ρ`-approximate SPE.

This argument checks all feasible layouts, including co-location when the original allowed sets overlap. The subclass condition is restrictive there: a shared physical candidate point may cover at most one customer, since its co-location pair otherwise violates `|S_u∩S_v|≤1`.

### 6.1 A direct algorithm, requiring only pure continuations

The limit proof has a stronger constructive form. Give the four labeled locations fixed pairwise distinct integer priorities `h_v` (for example `1,2,3,4`). At **every** cross pair, send its unique common customer to the location with lexicographically smaller pair `(R_v,h_v)`. All other customers are forced. This specifies a pure exact customer NE at all four layouts before the on-path layout is chosen.

For all sufficiently small positive `ε`, the private perturbation `εh_v` used above induces exactly these same four customer assignments: unequal original reaches keep their sign, and equal reaches are ordered by the priorities. Thus all perturbed layout payoffs converge to those under the fixed pure continuation just specified. If all four original layouts had a deviation factor strictly above `ρ`, each would have a strict additive inequality `u_new−ρ u_old>0`; the finitely many positive margins would persist for small `ε`, contradicting the strict-instance theorem. Hence one of the four layouts has factor at most `ρ` under this **single predetermined pure continuation selection**.

An algorithm therefore computes reaches, applies the fixed tie-breaking rule, evaluates four payoff pairs, and selects the smallest maximum deviation factor. It uses a linear number of rational arithmetic operations in the customer-incidence input and polynomial bit complexity. No equilibrium-support enumeration, irrational probabilities, or limiting computation is needed. A rational factor `t≥φ` can be compared to `ρ` by the sign of `q(t)`, since `q` is strictly increasing on `[φ,∞)`; factors at most `φ` are automatically below `ρ`.

### 6.2 Robustness to increasing congestion costs

The entire subclass result, including the exact customer-equilibrium sets, is unchanged if customer `i` has any strictly increasing cost function `f_i` of the realized load, provided its function is the same at both facilities. A unique common customer compares the two deterministic costs `f_i(R_u)` and `f_i(R_v)`. Their order and ties agree exactly with those of `R_u,R_v`. There is no uncertainty from other strategic customers in this subclass. Thus the theorem and its fixed pure continuation algorithm hold for these nonlinear and customer-specific costs as well.

### 6.3 A two-column reduction lifts the theorem to `2×m`

Assume `|U₁|≤2`, and let `U₂` be any nonempty finite set. Give **all labeled allowed choices** fixed pairwise distinct priorities. At every full-game layout, send its unique common customer to the lexicographically lower `(reach,priority)` choice, as in §6.1. This is one fixed pure customer NE continuation selection for the entire game. Let `P₁(u,v),P₂(u,v)` denote the resulting rational facility payoff matrix.

For each row `u∈U₁`, retain a column

`v(u)∈argmax_{v∈U₂} P₂(u,v)`.

Let `T₂={v(u):u∈U₁}`. There are at most two retained columns. All rows are retained, so the restriction to `U₁×T₂` has at most four layouts and inherits exactly the same fixed continuation rule.

If there are two rows and two retained columns, the `2×2` result in §6.1 gives a restricted `ρ`-stable layout `(u*,v*)`. Every deviation by facility 1 is already in this restricted game. Moreover, a full-game best deviation column for facility 2 at row `u*` is retained by construction. Thus restricted stability is full-game stability, with exactly the same pure customer continuation at all profiles.

If only one row is available, choose its retained best column and obtain an exact SPE. If two rows but only one retained column are present, choose a row maximizing facility 1's payoff in that column. The retained column is a best response for facility 2 at both rows, so this again gives an exact SPE.

When every pair sharing a customer has unequal reaches, the `2×2` theorem gives a factor strictly below `ρ`, and the identical argument transfers that strict bound to the full game. The smaller restrictions give factor 1.

The construction uses `O(n|U₁||U₂|)` straightforward incidence-processing operations, followed by a scan of the two best-response columns and at most four layouts; its rational arithmetic has polynomial bit complexity. The six-customer lower bound already has `2×2` choices, so it remains sharp for this entire `2×m` class. It is not necessary to compute any minima over mixed equilibria, select new punishments, or adapt the continuation to the chosen on-path layout.

A more general closed-response-cycle argument also works using true minimum equilibrium payoffs `m` and their opposite-side maxima `D`: follow alternating maximizing successors, obtain a cycle with at most two vertices of each color, and note that all full-game `D` values at its vertices are preserved inside the cycle. The direct two-column proof above is simpler for this subclass because its fixed pure continuation already suffices.

## 7. Matching positive-rational lower bound

Use six positive-weight customers named `A,B,C,D,x,y`; the first four reach only their corresponding locations. Customer `x` reaches `A,C,D`, and customer `y` reaches `B,C`. Let their weights be

`(a₀,b₀,c₀,d₀,X,y₀)`.

Facility 1 may choose only `A,B`, and facility 2 only `C,D`. These allowed sets are disjoint, so co-location is infeasible and there are exactly four layouts.

For `a₀>c₀+y₀`, `d₀>a₀`, `b₀<c₀+X`, the exact customer continuations are unique (indeed unique CCE), and the payoff matrix is

| First / second | C | D |
|---|---:|---:|
| A | `(a₀,c₀+X+y₀)` | `(a₀+X,d₀)` |
| B | `(b₀+y₀,c₀+X)` | `(b₀+y₀,d₀+X)` |

For `ρ` as above, put

`X=1`, `d₀=ρ−1`, `a₀=1/(ρ²−1)=ρ²−ρ−1`, `b₀=d₀−a₀`,

`y₀=a₀−η`, `c₀=η/2`,

where `η>0` is sufficiently small. The identities `ρa₀=d₀` and `1+a₀=ρd₀` follow from `q(ρ)=0`. The four cycle improvement factors tend to `ρ`:

`ρ−η/a₀`, `ρ/(1+η/2)`, `ρd₀/(d₀−η)`, `ρ−η/(2d₀)`.

All six weights are positive for small `η`; the strict client-choice inequalities also hold. Therefore every fixed `α<ρ` is beaten at all four layouts for sufficiently small `η`. The finite strict inequalities persist under a sufficiently small rational perturbation of all weights. Clear denominators to obtain positive integers.

A concrete exact integer example is

`(a₀,b₀,c₀,d₀,X,y₀)=(44504187,35689587,1,80193774,100000000,44504185)`.

Its minimum improvement factor is exactly `80193772/44504187≈1.8019376918401`. This number is illustrative; the symbolic family gives the rigorous limiting constant.

## 8. Reusable search tool and limits of the search evidence

`unique_milp.py` models arbitrary numbers of heterogeneous choices, under the single-common-customer condition and strict cross-reach order. A customer shared across the two players is a nonempty row subset times a nonempty column subset, i.e. a complete rectangle of cross pairs. A binary variable activates each rectangle; at most one activated rectangle may cover a given cross pair. Its continuous weight contributes to every incident location's reach. Arbitrary residual reach is supplied by private customers.

For a fixed total cross-reach order and proposed improvement factor `r`, all layout payoffs are linear: the lower-reach location gets full reach and the higher-reach one loses its overlap weight. Binary variables require at least one `r`-improvement at every layout. Thus the program searches all customer incidence patterns in this class for the given dimensions and reach order; it does not fix one continuation rule, because the strict class has a unique continuation at every layout.

The tool is an exploratory **floating-point MILP**, not an exact proof. In particular:

- solver infeasibility is not presented as a mathematical impossibility theorem;
- time limits are inconclusive;
- a reported feasible vector requires rational reconstruction and direct strict-inequality verification before it is a lower-bound certificate;
- tolerances must be below the chosen positive margin. A first test with margin `10⁻⁶` falsely admitted a zero-load tolerance artifact, which is why the retained tests use margin `10⁻⁴` and check actual gains.

At `2×2`, the program reproduced a factor above `1.8`. At `3×3`, all 20 relative orders preserving each player's internal reach order were reported infeasible for `r=1.82` with margin `10⁻⁴`. This is **only restricted numerical evidence**, and is not an upper bound for `3×3` or for the full model. The theorem above, proved without the MILP, resolves `2×m` for every finite `m`.

## 9. What this proves and what remains open

Proved here: the six-customer construction is extremal over **all** games with at most two choices on one side and any finite number on the other, satisfying the single-common-customer condition. This includes every incidence pattern and all tied reaches. Any attempt to exceed `ρ` must use either at least three choices for **both** facilities or a pair of allowed locations with at least two common customers.

Not proved here: that either escape route actually beats `ρ`; any general heterogeneous upper bound; or the exact optimum for arbitrary `U₁,U₂`. Those conclusions require additional arguments. In particular the standard common-maximum co-location argument does not itself provide an upper bound for disjoint allowed sets.

## 10. Independent review status

The `2×2` classification, cubic bound, positive rational lower family, and tied-reach passage were independently reviewed by the `asym_upper`, `witness_meta`, and `novelty_audit` agents. The review caught and repaired a wording issue concerning equal reaches at a pair with no shared customer: such a tie must be handled directly for the strict `<ρ` conclusion, as §4 now does. The closed response cycle lift was suggested by `asym_upper` and independently checked here; `novelty_audit` then gave the simpler fixed-payoff two-column reduction used in §6.3. These are internal mathematical reviews, not external peer review.

### Supplementary searches beyond the resolved class

`general_search.py` evaluates all ternary pure/mixed support patterns at each tested pair in floating point, including the one-mixer interval case, and searches incidence/weight mutations. It is an exploratory heuristic, not an exact certificate. Runs of 10,000 mutations at `2×2` and `3×3`, with eight customers and an overlap cap of seven for computational control, did not produce a value above `ρ`. This observation proves no upper bound and does not exclude untested multiple-common-customer instances. The `4×4` single-common MILP run at `r=1.82` was largely stopped by per-order time limits and is likewise inconclusive.

## 11. Audit of the separate arbitrary-overlap `2×m` upper bound

The later result in `upper.md` §§9–10 removes the single-common-customer restriction and proves a polynomial pure-continuation **2** upper bound whenever one facility has at most two allowed choices. I independently checked its four-cycle exclusion argument. In particular, the transferred set `X` satisfies exactly `w(X)=R_B−Q_B`; the two consecutive pure-NE gap constraints bound each member's weight; their weighted average excludes every member from `A`; and the resulting mandatory mass at `D` contradicts the last source-load quota. The initial heavy-customer repair step is valid because all improving move weights are below the decreasing load gap, which starts at most the heavy customer's weight, so that customer never leaves the initially lower-loaded facility.

That theorem does **not** settle sharpness for arbitrary overlap: the rigorous interval for the unrestricted-overlap `2×m` class is currently `[ρ,2]`. The sharp `ρ` theorem in this note resolves its single-common-customer subclass. Neither result, by itself, resolves the case where both facilities have at least three allowed choices and arbitrary overlap.
