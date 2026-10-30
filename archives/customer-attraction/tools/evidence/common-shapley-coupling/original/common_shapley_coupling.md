# Conservation does not recover common customers; a local Shapley coupling interface

Research backup, 2026-10-21. Model: CAG-MODEL, unit providers and unit customers,
one common finite catalogue, every ordered-history pure SPE, arbitrary ties.
The general Q-CAG-HALF statement remains **OPEN**. This note supplies an exact
representation and finite proof-template separations, not a half proof or a
game counterexample. Root has independently checked the representation and
clock-coupling mechanisms in this session; final full-text review is pending.
There is no external or novelty review.

## 1. Exact objects and the positive marginal representation

Write P for the p topic labels. A customer has a nonempty interest type
B subset P and mass w_B. Nonnegative integral masses encode distinct unit
customers; signed masses below are only an algebraic representation. For
S subset P put C(S)=sum_B w_B 1_(B intersects S), C(empty)=0.

Let q be a terminal topic-count vector, sum q=k, and q_a>0. A provider choosing
a has payoff row F_(q,a)(B)=1_(a in B)/q(B). There is an exact positive
cross-topic formula, valid for every set function represented by signed masses:

\[
 U_a(q)=\sum_{R\subseteq\operatorname{supp}(q)\setminus\{a\}}
 b_R(q,a)\bigl[C(R\cup\{a\})-C(R)\bigr],
\tag{1}
\]

\[
 b_R(q,a)=\int_0^1 t^{q_a-1}
 \prod_{b\in R}(1-t^{q_b})
 \prod_{b\in\operatorname{supp}(q)\setminus(R\cup\{a\})}t^{q_b}\,dt>0.
\tag{2}
\]

The coefficients sum to 1/q_a. To prove (1), fix a customer B. The marginal
C(R+a)-C(R) is one precisely when a belongs to B and B avoids R. The sum of
the integrands over those R is then 1_(a in B) t^(q(B)-1). Integrating gives
F_(q,a)(B), and linearity gives the result for signed masses as well.
For distinct terminal topics this is the ordinary Shapley marginal formula;
the t^(q_a-1) factor handles other providers choosing the same topic.

All payoffs with k<=m use only C(S) with |S|<=m. Conversely every arbitrary
assignment of these truncated C(S) values has a signed customer realization:
extend C arbitrarily to larger subsets, with C(empty)=0, and set

\[
 w_B=\sum_{D\subseteq B}(-1)^{|B|-|D|}
       [C(P)-C(P\setminus D)].
\tag{3}
\]

Boolean inversion verifies the represented coverage function is C. Equation
(3) makes no nonnegativity claim. Thus (1) is the exact common-*signed*-customer
linear space, not a relaxation of that linear space and not the common
nonnegative-customer cone.

## 2. A local extended formulation for the same linear space

Instead of substituting (1), introduce U_a(q) for all 1<=sum q<=m and q_a>0.
The same common set function representation is equivalent to the two families

\[
 \sum_a q_a U_a(q)=C(\operatorname{supp}(q)),
\tag{E}
\]

\[
 U_a(q)-U_b(q)=U_a(q-e_b)-U_b(q-e_a)
 \quad(a\ne b,\ q_aq_b>0).
\tag{BC}
\]

These are efficiency and balanced contributions for Shapley sharing, specialized
to repeated topic labels; no novelty claim is made for the general Shapley
characterization. Each customer satisfies BC: if it likes both a,b, both
differences vanish; if it likes only a, both sides are 1/q(B); and similarly
for only b or neither. E is immediate.

For sufficiency, induction on sum q proves uniqueness for any C. At size one,
E fixes U. At size k, BC fixes every difference U_a(q)-U_b(q) from size k-1
data. E then fixes their common additive shift, since sum q=k>0. Formula (1)
supplies existence. More explicitly,

\[
 U_a(q)=\frac1k\left[C(\operatorname{supp}q)+
  \sum_{b\in\operatorname{supp}(q)\setminus\{a\}}
    q_b\{U_a(q-e_b)-U_b(q-e_a)\}\right].
\tag{4}
\]

Consequently, a terminal array y_(q,a), sum q=m, has a common signed customer
representation iff it admits this extension to smaller counts. The number
of U variables is p binomial(m+p-1,p). This gives local cross-topic equalities
in place of a dense payoff-to-moment matrix. It does not enforce nonnegative
customer realizability or prove that the genuine SPE inequalities pay half.

## 3. Conservation alone still permits an exact 9/4 budget

Use precisely the complete 3-provider, 6-topic strategy in the existing
`R-d7f409d6a5914bdeb09875ab32618466/tree_duality/pair_dilution_obstruction.json`.
Its 43 ordered decision histories give all 258 history/action comparisons.
The root support is {0,3,4}; the single fixed comparison support here is
T={1,2,4}. Every claim in the table below concerns this one formal strategy
and this one T. It does not maximize over comparison supports or strategies.
Its complete finite rule is: root chooses 0; the second provider chooses 3
after a label in X={0,1,2}, and 0 after a label in Y={3,4,5}; the last provider
chooses the smallest as-yet unused label from the group containing the second
provider's label. Each group has three labels, so the last choice always
exists at every ordered history.

As in the existing fixed-strategy cone interface, all LPs use six
distinguishable labels and permit equal covered customer sets at boundary
points. Their exact maxima are for that labeled closed cone. They are not
assertions of attained maxima with exactly six distinct coverage subsets.

For all 126 terminal payoff vertices retain nonnegativity, every true
full-history incentive edge, and every sharp same-topic dilution inequality

\[
 y_{q,a}\le\max_{B\ni a}\frac{r(B)}{q(B)}\,y_{r,a}.
\]

Also impose **every** equality saying sum_a q_a y_(q,a) depends only on
supp(q). Even with these additional 15 conservation equalities (plus root
normalization), the exact optimum of comparison coverage/root coverage is
9/4. Both a rational feasible vector and a matching rational dual are saved.
This strictly strengthens the existing obstruction, whose vector violated
same-support conservation.

The new vector still cannot arise from any common signed customer masses.
For three providers every common signed representation satisfies

\[
 U_0(2e_0+e_1)-U_1(e_0+2e_1)
 =\frac32[U_0(3e_0)-U_1(3e_1)].
\tag{5}
\]

One can check this on the four Boolean interest patterns for labels 0,1;
other labels do not affect either side. The saved vector has U_0(3e_0)=
U_1(3e_1)=1/4, U_0(2e_0+e_1)=3/8, U_1(e_0+2e_1)=1/4.
Thus its left side is 1/8 and its right side is zero. Conservation cannot
replace cross-topic Shapley consistency even on a two-topic subsystem.

There is a further exact separation. Add, for every distinct pair a,b, both
of the common-customer identities

\[
 U_a(ke_a+(3-k)e_b)-U_b((3-k)e_a+ke_b)
 =\frac3k[U_a(3e_a)-U_b(3e_b)],\qquad k=1,2.
\tag{6}
\]

The exact optimum with these selected difference identities is 15/7>2.
**Correction after root's independent attack:** these are not complete
two-topic coupling. The conservation equation is dependent on the two
difference identities, leaving a spurious extra degree of freedom per pair.
For pair variables a=U_a(3e_a), b=U_b(3e_b), x=U_a(2e_a+e_b),
y=U_b(2e_a+e_b), z=U_a(e_a+2e_b), w=U_b(e_a+2e_b), a third independent
necessary equation is 2x+2w=z+3b. The saved vector's derived pair coverage
range max(C(a),C(b))<=C(ab)<=C(a)+C(b) does not make its specified utilities
compatible with those coverages. The original JSON field containing
`all-two-topic-coupling` is a preserved incorrect layer name, not the scope
of its certified constraints. No conclusion that complete two-topic
coupling fails is supported by the 15/7 vector. The corrected complete-pair
version in `round2/complete_pair_v2.json` has exact optimum 2, with independent
optimizer-free verification and direct pair-payoff reconstruction; see
`round2/pair_scope_correction.md`.

## 4. Exact finite hierarchy on that fixed strategy and comparison

All moment-based layers have C(empty)=0, C(S)>=0 for 1<=|S|<=3, the common
payoff map (1), every complete-history incentive, root C({0,3,4})=1, and all
sharp same-topic dilution comparisons. The extra conditions differ as follows.

| Feasible description | Exact maximum of C({1,2,4}) |
| --- | ---: |
| Independent nonnegative terminal payoffs, dilution, same-support totals | 9/4 |
| Previous row plus two selected payoff-difference identities per topic pair | 15/7 |
| First row plus complete common signed payoff coupling on all topic pairs (v2 correction) | 2 |
| Common signed moment representation, all terminal payoffs nonnegative | 8/5 |
| Common moment representation, monotone C on the truncated domain | 198/127 |
| Common moment representation, monotone and submodular C on that domain | 3/2 |
| Common moment representation, every locally available coverage-alternation inequality | 3/2 |
| One genuine nonnegative customer mass vector on all 63 nonempty types | 33/23 |

The locally available alternation conditions are

\[
 \sum_{R\subseteq A}(-1)^{|R|+1}C(S\cup R)\ge0,
 \quad A\ne\varnothing,\ A\cap S=\varnothing,\ |A\cup S|\le3.
\]

They include monotonicity and submodularity. The strict 3/2 versus 33/23 gap
shows they do not characterize the projection of the genuine nonnegative
customer cone, even after full-tree incentives and all dilution constraints.
These layers are not all asserted to form a nested chain: monotonicity alone
was not supplemented by explicit terminal-payoff nonnegativity, but it implies
that property through the positive marginal representation (1).

Every displayed optimum has an exact rational primal and dual certificate.
The genuine customer layer's rational primal can be cleared to integral
unit-customer multiplicities, but labels 0 and 3 then have equal coverage.
It certifies the 33/23 labeled-closure optimum, not attainment with six
distinct topics. Its statement also remains about the fixed T, not the
true optimum over all T. The source 22-customer vector has six distinct
coverages and satisfies the same complete strategy; the independent verifier
checks both facts. Adding any positive rational epsilon times that source
to the 33/23 primal preserves all full-tree SPE inequalities and distinguishes
every label pair, so distinct-topic instances approach 33/23. No exact
attainment claim under that extra requirement is needed here.
None of the relaxed vectors is a game
counterexample. In particular the 9/4 vector has no common signed realization.

## 5. Reproduction, scope, and remaining positive obligation

From the repository root:

```sh
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/tree_coupling/coupling_probe.py
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/tree_coupling/verify_coupling.py
```

The first script uses floating LP only to discover candidates and accepts a
result only after Fraction primal and dual checks. It also checks the
positive-integral payoff coefficients on every Boolean customer type. The
second does not import the probe or an optimizer: it rebuilds the common
payoff rows using a different Boolean Möbius formula, reconstructs every
real ordered-history terminal, and checks all rational constraints and dual
coordinates. `coupling_layers.json` stores all seven complete finite witnesses.

A possible broader positive target is: full-tree incentives plus one common
monotone submodular truncated C, with payoffs given by (1), imply
2C(root support)>=C(T) for |T|<=m. This would imply Q-CAG-HALF. It is an
unproved stronger conjecture. The fixed-cone table above additionally imposes
all sharp same-topic dilution constraints. Lemma TC-DIL-1 in
`submodular_dilution_coupling.md` now proves these constraints automatic for
all nonnegative decreasing Shapley marginals, including monotone submodular
truncated C. Thus its 3/2 submodular result also applies to that same fixed
strategy/T without separately imposing dilution. A separate `submodular_probe.py` run
(m=5,p=7,seed=749811,12 complete Markov policies sampled from sums of
budget-additive functions, all 21 five-topic comparison supports per policy)
omits every dilution constraint. Its largest exactly checked feasible value
was 9/5; this is finite failure to find a counterexample, not an upper bound
on those cones or evidence for arbitrary policies. The run is saved in
`submodular_probe.json`. A counterexample in that broader class would not
refute Q-CAG-HALF.
The exact local representation E+BC makes this target accessible without
pretending that independent terminal payoffs are common customers.
