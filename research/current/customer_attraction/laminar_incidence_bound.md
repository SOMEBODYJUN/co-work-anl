# Hierarchical maximal incidence: a sharp all-history sequential welfare bound

**Direct proof, 2026-10-10; independently reconstructed internally.** This file
does not change canonical claim registries. The general common-catalog
half-coverage conjecture remains open. Proposed IDs are
`CA-LAMINAR-INCIDENCE-MAXIMA-2M1` and
`CA-LAMINAR-INCIDENCE-THETA`.

The input class strictly contains the sunflower-maxima class: customers can be
shared by nested groups of maximal themes, and different groups can have
different common cores. Every internal catalog action is retained, including
actions that omit any or all such cores. The proof uses actual continuations
and allows unrelated tie choices at every ordered history.

## 1. Exact input class and theorem

Use [CAG-MODEL](model.md): `n≥1` identical unit providers, a common finite
nonempty catalog, unit customers, observed sequential choices, and equal
`1/k` customer shares. Repeated actions, empty actions, duplicate labels with
identical coverage, and arbitrary ordered-history pure SPE continuations are
allowed.

Identify the distinct inclusion-maximal coverage sets as
`B_1,...,B_s`. Every catalog action is contained in at least one `B_j`.
For each coverable customer `x`, define its **maximal incidence**

\[
I_x=\{j\in[s]:x\in B_j\}.
\tag{LI1}
\]

Assume these nonempty incidence sets form a laminar family: for every pair of
customers `x,y`, the sets `I_x,I_y` are disjoint or one contains the other.
This is a condition on customer incidence among distinct maximal coverages,
not a requirement that the catalog themes themselves form a laminar family.

For an ordered prefix `h`, let `h_x` be the number of earlier actions containing
`x`, and define its immediate best joining payoff

\[
M(h)=\max_{A\in\mathcal S}\sum_{x\in A}\frac1{h_x+1}
=\max_{j\in[s]}\sum_{x\in B_j}\frac1{h_x+1}.
\tag{LI2}
\]

The equality holds because every catalog action has a maximal superset and all
customer shares are nonnegative. Define the common last-slot floor

\[
\theta_n=\min_{h\in\mathcal S^{n-1}}M(h).
\tag{LI3}
\]

For `n=1`, this minimum has the single empty prefix. This definition keeps every
legal ordered prefix, regardless of whether it lies on a root equilibrium path.

**Theorem.** Under the maximal-incidence laminar condition, every complete
ordered-history pure SPE, at every legal prefix, gives each remaining player
final payoff at least `θ_n`. Consequently its root welfare `W` satisfies

\[
\boxed{W\ge n\theta_n\ge
\frac{n}{2n-1}\operatorname{OPT}_n,
\qquad
\operatorname{OPT}_n\le\left(2-\frac1n\right)W.}
\tag{LI4}
\]

More sharply, put `C=∩_jB_j` and `c=|C|`. Even when catalog subthemes omit
customers of `C`,

\[
\boxed{\theta_n\ge\frac cn+\frac{\operatorname{OPT}_n-c}{2n-1},
\qquad
\operatorname{OPT}_n\le c+
\left(2-\frac1n\right)(W-c).}
\tag{LI4C}
\]

The welfare factor `2−1/n` is sharp within this class. No part of the theorem
claims SPE outcomes are static PNE or that all selected themes are maximal.

The sunflower condition gives incidences consisting of the whole set `[s]`
and singleton indices, hence is included. A strict extension is

\[
B_1=\{c,d,a\},\quad B_2=\{c,d,b\},\quad B_3=\{c,e\}.
\tag{LI5}
\]

Their customer incidences are `{1,2,3}`, `{1,2}`, and singletons, which are
laminar. The pairwise maximal intersections are `{c,d}`, `{c}`, `{c}`, so
the three maxima do not form a sunflower. One may freely add any catalog
subsets, for example `{a}`, `{d,b}`, or the empty set, without leaving the class.

## 2. Source mechanism and the additional subset-action obligation

**Paper Fact.** Groenland and Schäfer,
[*The Curse of Ties in Congestion Games with Limited Lookahead*](https://arxiv.org/pdf/1804.07107),
arXiv:1804.07107v1, Theorem 20 (printed page 12, PDF page 12), prove optimal
egalitarian cost for every subgame-perfect outcome of a symmetric network
congestion game on an extension-parallel graph. The theorem permits ties.
Its proof selects an initially cheapest path and a successor path of maximum
overlap, then uses the nested-intersection property.

**Adaptation here.** The protection argument below is the reward version of
that maximum-overlap mechanism. We prove it directly in the unit CAG model,
including arbitrary internal subset actions. Such actions need not be full
paths through the incidence hierarchy. Routing an action to a containing
maximal theme is only a proof device: we do not add customer covers or change
any final denominator. The source network theorem is therefore not being
applied to the enlarged catalog without this extra proof. Global novelty and
external peer review are not claimed.

## 3. Equivalent nested-intersection condition

The maximal-incidence laminar hypothesis is equivalent to

\[
\boxed{\text{For each }j,\quad
\{B_j\cap B_k:k\in[s]\}\text{ is a chain under inclusion.}}
\tag{LI6}
\]

**Proof.** Suppose two intersections for a fixed `j` are incomparable. Choose
`x∈B_j∩B_k` with `x∉B_\ell`, and
`y∈B_j∩B_\ell` with `y∉B_k`. Then `I_x,I_y` both contain `j`, while
`k∈I_x\setminus I_y` and `ℓ∈I_y\setminus I_x`. Their incidences cross, which
contradicts laminarity.

Conversely, if two incidences cross, select
`j∈I_x∩I_y`, `k∈I_x\setminus I_y`, and
`ℓ∈I_y\setminus I_x`. Then `B_j∩B_k` contains `x` but not `y`, whereas
`B_j∩B_ℓ` contains `y` but not `x`. These intersections are incomparable.
This proves both directions. The condition is vacuous for a single distinct
maximal coverage, including the zero-customer instance. ∎

## 4. Greedy maximal protection against arbitrary future catalog actions

Fix any legal ordered prefix `h`. Choose a maximal coverage `B_j` attaining
`M(h)`. Consider any nonempty future sequence of catalog actions
`A_1,...,A_r`, with no equilibrium requirement on that sequence. Let `d_x`
be the actual final customer load after the prefix, `B_j`, and this sequence.

**Protection lemma.** The player who chose the whole `B_j` receives at least
the final payoff of one of these later players:

\[
\boxed{u(B_j;h,A_1,\ldots,A_r)\ge
\min_{1\le t\le r}u(A_t;h,B_j,A_1,\ldots,A_r).}
\tag{LI7}
\]

**Proof.** For each future action, choose any containing maximal coverage
`A_t⊆B_{k_t}`. By (LI6), the finite intersections `B_j∩B_{k_t}` are nested.
Choose `t` whose intersection is largest and put

\[
I=B_j\cap B_{k_t},\qquad E=B_j\setminus B_{k_t},\qquad
F=B_{k_t}\setminus B_j.
\]

Every actual future action intersects `B_j` only inside `I`:

\[
A_\ell\cap B_j\subseteq B_{k_\ell}\cap B_j\subseteq I.
\tag{LI8}
\]

Thus no future player covers a customer of `E`; its final load is exactly
`h_x+1`. The leader's actual payoff is

\[
u(B_j)=\sum_{x\in I}\frac1{d_x}
+\sum_{x\in E}\frac1{h_x+1}.
\tag{LI9}
\]

Initial maximal greediness compares the two legal catalog themes `B_j` and
`B_{k_t}`. Cancelling their common immediate contributions gives

\[
\sum_{x\in E}\frac1{h_x+1}
\ge\sum_{x\in F}\frac1{h_x+1}.
\tag{LI10}
\]

The selected follower covers a subset of `B_{k_t}`. On its actually covered
customers, `d_x≥h_x+1`; its actual payoff therefore obeys

\[
\begin{aligned}
u(A_t)
&=\sum_{x\in A_t\cap B_j}\frac1{d_x}
+\sum_{x\in A_t\setminus B_j}\frac1{d_x}\\
&\le\sum_{x\in I}\frac1{d_x}
+\sum_{x\in F}\frac1{h_x+1}\\
&\le u(B_j).
\end{aligned}
\tag{LI11}
\]

All `d_x` in the first enlarged sum are positive because `I⊆B_j`, which the
leader really chose. For customers in `F` absent from the actual follower
action, the expression is merely the positive immediate bound `1/(h_x+1)`;
no uncovered final denominator is evaluated. The argument permits every
possible omission of shared cores and every choice of the routing maxima.
This proves (LI7). ∎

The conclusion compares the leader to at least one follower, not necessarily
to all followers. It suffices when every actual follower already has a known
floor. The leader must choose an immediate maximizing full maximal theme;
the lemma does not assert the same protection for every current action.

## 5. Every history inherits the last-slot floor

We prove the `θ_n` conclusion in (LI4) by induction on the number `r` of
remaining players, simultaneously over all legal ordered prefixes and all
their complete history-dependent SPE continuations.

If `r=1`, the prefix has length `n−1`. The last player's SPE action maximizes
immediate payoff, so its payoff is `M(h)≥θ_n` by (LI3).

Now let `r≥2`, and suppose the statement holds for every prefix with fewer
remaining players. The current player may legally deviate to any full maximal
theme attaining `M(h)`. After this deviation, the same complete strategy's
actual follower continuation is an SPE of that new prefix. By induction,
each of its `r−1` followers gets at least `θ_n`. The protection lemma (LI7)
therefore gives the deviator at least `θ_n`. Current SPE optimality gives the
actual current player at least this deviation payoff. Induction also applies
to the actual successor prefix, so every remaining player has the floor.

This proves the all-history statement and `W=Σ_i u_i≥nθ_n` at the root. The
proof never freezes successor actions after a deviation and never identifies
the responses at two ordered histories having the same customer loads.

## 6. A universal immediate-payoff counting bound

The following inequality does not require laminar incidence and applies to
every common catalog. Fix any prefix `h=(A_1,...,A_t)` and an optimal `n`-theme
portfolio `(T_1,...,T_n)`. Let `o_x` be the number of these optimal themes
covering customer `x`.

Every catalog theme has immediate joining payoff at most `M(h)`. Summing the
`n` optimal themes and the `t` already selected legal themes yields

\[
\begin{aligned}
(n+t)M(h)
&\ge\sum_x\frac{o_x+h_x}{h_x+1}\\
&\ge\sum_{x:o_x\ge1}1
=\operatorname{OPT}_n.
\end{aligned}
\tag{LI12}
\]

The second inequality holds customer by customer: on the optimal union,
`o_x≥1`, hence `(o_x+h_x)/(h_x+1)≥1`; outside it all terms are nonnegative.
Repeated portfolio themes and repeated historical actions are counted with
their true multiplicities. Setting `t=n−1` gives

\[
\boxed{\theta_n\ge\operatorname{OPT}_n/(2n-1).}
\tag{LI13}
\]

Combining (LI13) with the preceding all-history floor proves (LI4). This
distinguishes the universal counting statement from the structural protection
statement. In unrestricted catalogs, the missing implication is precisely
the ability to propagate the immediate last-slot floor backward.

For completeness, `M(h)≥θ_n` holds for every legal prefix of length at most
`n−1`: extend it arbitrarily to length `n−1`; adding covers cannot increase
any immediate joining payoff, so `M(h)≥M(extension)≥θ_n`. This fact alone
does not protect the current player's payoff from future dilution.

To prove (LI4C), remove the common maximal core `C` from every catalog action.
Expanding each action to a containing maximal action shows that the optimum
of this residual catalog is exactly `OPT_n−c`. The same counting argument
(LI12), applied to the stripped history of a last-slot prefix, gives residual
immediate maximum at least `(OPT_n−c)/(2n−1)`. Full maximal actions all contain
`C`, so their core immediate contribution is a common term. Every customer
load in a length-`n−1` prefix is at most `n−1`; hence this term is at least
`c/n`. Thus every such prefix has
`M(h)≥c/n+(OPT_n−c)/(2n−1)`, proving the first assertion of (LI4C).
Now `W≥nθ_n` gives `W−c≥n(OPT_n−c)/(2n−1)` and the second assertion follows.
This argument does not assume any earlier action contains the core.

## 7. Sharpness, boundaries, and the exact protection barrier

For `n≥2`, take one disjoint maximal theme of size `n` and `n−1` disjoint
unit themes. Their maximal incidences are singletons. The all-big path can be
extended to a complete SPE: following that path gives every player payoff
one, while any unit-theme deviation has payoff at most one under every
continuation; all other histories can use finite backward induction.
Therefore `W=n`, `OPT_n=2n−1`, and (LI4) attains equality. For `n=1`, the
factor is one and the player chooses maximum coverage.

If there is one maximal coverage, the last player selects it and root welfare
is optimal. If there are no coverable customers, `θ_n=W=OPT_n=0`. An empty
action or duplicate coverage label causes no problem in (LI8)–(LI13).
Uninterested customers may be deleted. The routing maxima are never required
to be uniquely determined or to agree across different actions.

The protection lemma already fails for three crossed maximal coverages.
Take four disjoint customer blocks with cardinalities

\[
|X|=|Y|=4,\qquad |Z|=|V|=3,
\]

and catalog

\[
B_1=X\cup Y,\quad B_2=X\cup Z,\quad B_3=Y\cup V.
\tag{LI14}
\]

With empty background, `B_1` is the unique immediate best action: its joining
payoff is eight, compared with seven for each alternative. Against the future
sequence `(B_2,B_3)`, the final payoffs are exactly `(4,5,5)`. Thus even a
strictly greedy leader can end below every follower. The crossed incidences
`{1,2}` and `{1,3}` violate (LI1); its two intersections `X,Y` are incomparable.
This is an exact failure of the structural protection obligation, not a
counterexample to the common-catalog SPE welfare conjecture.

The original globally-private superset seats also cannot pay a general union
budget. For `q≥2` disjoint clusters, let cluster `a` have a shared block `C_a`
of size `H` and two unit private petals, with its two maximal themes equal to
`C_a` plus either petal. With `n=q`, every global-private maximal block has
size one while its shared part has size `H`. The static seat values are
`f_j(k)=1/k+H/n`. Their `n`th-largest value is `ν=1+H/n`, because there are
`2q≥n` first seats. Hence `nν=H+n`, while choosing one maximal theme from
each cluster gives `OPT_n=n(H+1)`. As `H→∞`, the ratio of this optimum to
the static seat budget approaches `n`. This does not defeat the theorem above:
these clusters have disjoint or nested incidence sets and satisfy its sharp
bound. It shows exactly which old scalar budget the hierarchy repairs.

## 8. Finite attacks and remaining scope

The exact finite audit is
[`tests/audits/customer_attraction_laminar_incidence.py`](../../../tests/audits/customer_attraction_laminar_incidence.py).
It independently computes direct customer shares and checks the protection
lemma against arbitrary future action sequences, including nonmaximal
actions omitting cores. It also uses the canonical all-continuation SPE
solver to test every remaining player's `θ_n` floor in every legal prefix,
the sharpened core bound, and the root welfare conclusion. By default it
prints a fresh report; `--output` refuses to overwrite an existing report.
The frozen report records source hashes for the proof, audit, and canonical
model and solver. The exact crossed-incidence failure (LI14) is independently
recalculated using rational arithmetic.

The targeted run passed 221 exhaustive catalog/person-count cases with
42,045 direct protection comparisons, plus 30,000 seeded protection
comparisons across 300 weighted hierarchy cases. Its 521 exact SPE cases
produced 757 root outcomes; all 67,941 new-topic payoff comparisons in
85,962 canonical count states passed the `θ_n` floor, including the core
sharpening. These are finite tests, not a substitute for Sections 3–6.
The catalog families include the strict hierarchy (LI5), every addition of
at most two internal subsets, seeded weighted disjoint hierarchies with core
omissions, zero coverage, empty actions, duplicate coverage labels, unique
maxima, and `n=1`. The frozen
[audit report](../../../evidence/runs/2026-10-10/customer_attraction_laminar_incidence.json)
records these counts and all source hashes.

Run the audit from the repository root:

```sh
python3 tests/audits/customer_attraction_laminar_incidence.py
```

The direct proof establishes an arbitrary-player structural class and locates
an exact obstruction to its protection mechanism. It does not close the
unrestricted half-coverage claim, and it does not turn finite searches into
a universal bound beyond the stated incidence condition.
