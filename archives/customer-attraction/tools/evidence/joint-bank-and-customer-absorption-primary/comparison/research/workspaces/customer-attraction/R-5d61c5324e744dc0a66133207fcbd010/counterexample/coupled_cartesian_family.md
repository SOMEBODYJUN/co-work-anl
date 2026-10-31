# Two early choices can couple Cartesian factors, but this insurance architecture stays below 5/4

2026-10-23. Personal research asset; author proof, exact finite DAG replay, independent review pending. Original CAG-MODEL throughout. This is an all-population complete-SPE construction and an architecture bound, **not** a counterexample to Q-CAG-HALF. No claim of external review or novelty.

## 1. Construction and exact statement

Let `n>=2`, `m=n+2`, and let positive integers `b,s,d` obey

\[
0<d\le b,\qquad nd\le2s.
\tag{1}
\]

Make six pairwise disjoint groups of distinct unit customers. The three groups in the first coordinate have sizes

\[
|A|=2b-d,\quad |B|=b,\quad |C|=bn,
\]

and those in the second coordinate have sizes

\[
|X|=|Z|=s,\quad |Y|=s(n+1).
\]

The common catalog consists of all nine unions `P union Q`, `P in {A,B,C}`, `Q in {X,Y,Z}`. All nine customer subsets are distinct. Each provider still selects exactly one common-catalog theme, and all customers/providers have unit weights. A selected union obtains the sum of its two resource payoffs, because the six groups are disjoint.

There is a complete ordered-history pure SPE with actual path

\[
AY,AY,(CY)^{n-2},CX,CZ.
\tag{2}
\]

(The order after the first two moves can be changed within the component policy below.) Its final coordinate counts are `(2,0,n)` and `(1,n,1)`. Consequently

\[
W=b(n+2)-d+s(n+3),\quad
\operatorname{OPT}_{n+2}=W+b.
\tag{3}
\]

Indeed the actual outcome misses only the `b` customers in B; three product themes can cover all six groups, and `m>=4` allows repetition to fill the remaining choices.

For this entire architecture,

\[
\frac{\operatorname{OPT}_{n+2}}W
\le 1+\frac1{n+2}=\frac{n+3}{n+2}\le\frac54.
\tag{4}
\]

To prove this, (1) gives `d<=2s/n<=s(n+3)`, and hence `W>=b(n+2)`. The first inequality is a supremum: fixing n,s,d and sending integer b to infinity makes the ratio tend to `(n+3)/(n+2)`.

Thus cross-coordinate continuation coupling is real, but this specific two-early-choice insurance mechanism cannot amplify toward a violation of half coverage.

## 2. A full first-coordinate continuation policy

Write `(a,e,c)` for the past counts of `(A,B,C)`; `e` is used for the B count to distinguish it from the size parameter b. The following prescriptions define complete SPE continuations on their stated state domains:

* If `a>=2` or both `a>=1,e>=1`, prescribe C at every subsequent history in that domain.
* If `a=1,e=0`, prescribe B; apply this rule again after a C deviation.
* If `a=0,e=1`, prescribe A; apply this rule again after a C deviation.
* If `a=e=0`, prescribe A; apply this rule again after a C deviation.
* At states `a=0,e>=2`, use backward induction with the already prescribed child continuations. This fills every remaining history.

Here and below the policy at each ordered history may be computed from its count state; this is a legal special policy, not a restriction on the model's SPE class.

Proof of the prescriptions:

1. In the first domain, at least two past choices lie outside C, so prescribing C forever gives each future C mover payoff at least `bn/n=b`. In the `a>=2` subdomain an A deviation earns at most `(2b-d)/3<b`, and a B deviation at most b. In the `a>=1,e>=1` subdomain the corresponding bounds are `(2b-d)/2=b-d/2<b` and `b/2`. The domain persists after every action. Thus C is optimal at every such history.
2. If `a=1,e=0`, choosing B leads to the first domain, and gives b. An A deviation is at most `b-d/2`. A C deviation is followed by the same prescription, giving at most b: if another player remains, B is then chosen and final C count is n; if no player remains, C count is n+1. This is a descending induction on remaining players.
3. If `a=0,e=1`, choosing A leads to the first domain and gives `2b-d>=b`. A B deviation earns at most `b/2`; a C deviation, followed recursively by A and then C, earns at most b (the final-move boundary gives C count n+1). Again this is an induction.
4. If `a=e=0`, choosing A followed by case 2 gives `2b-d>=b`. A B deviation enters case 3 and gives b; a C deviation stays in case 4 and eventually gives at most b. At the last-move boundary A is at least b, B is b, and C is `bn/(n+2)<=b`.

Unspecified states are genuinely filled: after their children have complete SPE continuations, select a current best action. Their choices cannot invalidate an earlier controlled node because the bounds used above apply to every terminal continuation at a deviation exiting the domain.

In particular, after a single root B or C this policy reaches `(1,1,n)`; after prefixes `AA` or `AB` it prescribes only C; after prefix `AC` it prescribes B and then only C.

## 3. Two complete second-coordinate policies

Write `(x,y,z)` for past counts, and let `l=x+z`.

**Low policy L.** Prescribe Y at every nonterminal history, except that the last player selects X if `l=0`. This is a full SPE.

If `l<=1`, its prescribed Y payoff is s, while any side action obtains at most s. If `l>=2`, prescribed Y's final load is `m-l<=n`, so its payoff is at least `s(n+1)/n>s`, and either side obtains at most s. At the last history with `l=0`, X gives s while Y gives `s(n+1)/(n+2)<s`. These cases also cover repeated side choices and all off-path histories. In particular, after any single root action a root provider earns at most s under L.

**High policy H.** In states with `x,z in {0,1}` and `y<=n`, select Y while `y<n`; when `y=n`, select a still missing side, X first. Outside this domain use L. This is a full SPE from every history in the domain; it ends at `(1,n,1)`.

When Y is prescribed its final payoff is `s(n+1)/n=s+s/n`; a side deviation is at most s. When a missing side is prescribed its payoff is s. Another fresh side also yields s, a repeated side is at most `s/2`, and an extra Y has load at least n+1 and hence payoff at most s. Exiting the domain is permanent (a repeated side or `y>n`), so L gives valid complete child continuations.

## 4. Full product policy and all deviations

At the empty history prescribe AY. After any first action `Ar`, with `r in {X,Y,Z}`, prescribe AY again. Below such a two-move history use the product of the first-coordinate policy and H if the second move was precisely AY; otherwise use the product of the first-coordinate policy and L. After a first move Br or Cr use the product with L immediately.

A product of two complete continuation policies is a complete product-game SPE: a tuple deviation's gain is the sum of its coordinate gains, because each continuation subsequently reads only its own coordinate history. This fact is used only below the two explicit coupling levels.

At a history whose first action was Ar, the prescribed second AY leads to `AA` in coordinate one and to H in coordinate two. Its current payoff is

\[
v=b-d/2+s+s/n.
\tag{5}
\]

For its other actions:

* `At`, `t!=Y`, leads to the first-coordinate C policy and L. Its first-coordinate share is `b-d/2`, and its side share is at most s, so it obtains at most `b-d/2+s<=v`.
* `Bt` leads to prefix AB, followed only by C, and L. Its payoff is at most `b+s<=v` by (1).
* `Ct` leads to prefix AC, followed by B then C, and L. Its first-coordinate share is b, and its second-coordinate share at most s, again giving `b+s<=v`.

For the L bounds at these second-level nodes: if t is a side, its share is always at most s; if t=Y, the first two moves have at most one side action and L ends with n+1 copies of Y, so its share is s. This explicitly checks the actual relevant background rather than applying the root L bound blindly.

At the root, AY obtains v. An alternative Ar with r a side is followed by the second AY and H, and obtains `b-d/2+s<=v`. A Br or Cr is followed by the product policy with L, so obtains at most `b+s<=v`. Thus every root action is checked, and every proper subtree was proved a complete SPE. This proves the claim for every n and every legal parameter triple, with no fixed tie rule or omitted history.

The actual policy order is `AY,AY,(CY)^(n-2),CX,CZ`. Each early AY receives v, each CY receives `b+s+s/n`, and CX,CZ receive `b+s`. Their sum agrees with (3).

## 5. What coupling changes, and what it does not

The first-coordinate projection of this actual full policy is **not** a stand-alone SPE. It prescribes A at the root, another A after that, and then the section 2 policy. Its root A provider obtains `b-d/2<b`; deviating to B enters the section 2 continuation ending `(1,1,n)` and obtains b. Thus its root inequality fails. In the product game this improvement triggers L in the second coordinate. Y's reward drops from `s+s/n` to s, enough to remove the incentive when `d/2<=s/n`.

Consequently, one cannot infer that an arbitrary Cartesian-product SPE projects to a component SPE, nor assume the selected first-coordinate continuation can be used unchanged above the coupling levels. This is the missing mechanism in the prior product-policy no-amplification lemma; its componentwise-policy hypothesis matters.

The finite instances `b=3n,s=2n,d=3` (n>=2) have

\[
W=5n^2+12n-3,\qquad OPT=5n^2+15n-3.
\]

Exact finite all-SPE diagnostics for m=4,...,12 found component minimum-welfare sum exceeding this product W by n. This finite component-minimum statement is not promoted to a general theorem here. It is unnecessary for the explicit full-SPE proof or architecture bound. The general product ratio bound (4) shows that these finite deficits do not constitute worst-ratio amplification beyond the second coordinate's own explicit low-policy ratio `(n+3)/(n+2)`.

## 6. Safe disjoint-catalog padding still cannot cross half

The same-team [safe padding lemma](../security/safe_catalog_padding.md) permits adding arbitrarily many pairwise disjoint new themes, each of size `t<=K/m`, while preserving this full SPE and its W. Here the maximum old theme size is

\[
K=bn+s(n+1).
\]

The exact old r-theme optima are

\[
O_1=K,\quad O_2=K+2b-d+s,\quad O_r=W+b\quad(r\ge3).
\]

The padded optimum is `max_r[O_r+(m-r)t]`. It suffices to test `t=K/m`, since this expression is nondecreasing in t. For r=1 the value is `(2-1/m)K<2W`. For r=2 and r>=3, respectively, direct expansion gives

\[
\begin{aligned}
m\,[O_2+(m-2)K/m-2W]
 &=-(4n+4)b-(5n+8)s+(n+2)d<0,\\
m\,[W+b+(m-3)K/m-2W]
 &=-(4n+2)b-(5n+7)s+(n+2)d<0.
\end{aligned}
\]

Both strict inequalities follow already from `d<=b` and positivity. The r>=3 line bounds every such r by using the largest available padding budget m-3. All-new choices are dominated by the r=1 expression. Therefore **no standard safe padding of this insurance family yields a half counterexample**, for any population or number of new themes. This conclusion uses the padding lemma only for SPE preservation; the displayed coverage comparison is independent algebra.

Finite componentwise Cartesian products of these families at the same m do not repair this obstruction. Their `O_r`, K and W add exactly, so each padded comparison is the sum of the negative component comparisons. This statement concerns the componentwise product of the already constructed coupled policies; it makes no decomposition claim for arbitrary new cross-component SPEs.

## 7. Reproduction and remaining direction

`verify_coupled_cartesian.py` is self-contained and uses Fraction arithmetic. It builds the full policy DAG from the prescriptions, checks every legal tuple-action edge and every node's actual continuation payoff, and reports the complete ordered-history count represented by that DAG. It also checks unit-group counts, actual coverage, and the optimal full-coverage witness. No normative SPE solver is imported. General quantification comes from sections 2–4; finite replay checks the implementation.

`cartesian_scout.py` is an exact exploratory all-SPE marginal-state solver for Cartesian products of disjoint menus. It found the initial five-player diagnostic and checks whether arbitrary coupled equilibria improve or worsen over componentwise policies. Finite searches do not prove general welfare bounds.

A next counterexample architecture must preserve this real continuation compensation while also removing the `bn` welfare mass needed to make C an attractive continuation throughout the remaining n slots, or reuse one compensation account across many omitted groups. Independent products of the present construction only average the displayed ratios. No such reuse or half counterexample is claimed.
