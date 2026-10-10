# Six maximal coverages without globally private customers

Direct proof, 2026-10-10; independently reconstructed internally. Registered claim IDs:
`CA-SIX-MAXIMA-NO-PRIVATE-HALF`; Section 5 adds
`CA-SIX-MAXIMA-NINE-PLUS-HALF`. The separate [CA-SIX-MAXIMA-HALF joint-budget theorem](six_maxima_joint_bound.md) now also covers the unrestricted critical counts `n=5,...,8`. External peer review and novelty have not been certified. The finite
rational coefficient certificates in Section 4 are part of this proof;
the finite SPE tests in Section 8 are a separate implementation audit.

## 1. Exact statement

Use [CAG-MODEL](model.md): a finite nonempty common catalog of customer
subsets, `n>=1` unit providers, unit customers, observed sequential actions,
and equal final customer shares. Strategies specify an action at every
ordered history. Repeated choices, empty actions, duplicate coverage labels,
and unrelated tie choices at different histories are allowed.

Let `B_1,...,B_s` be the distinct inclusion-maximal coverage sets, where
`1<=s<=6`, and put

\[
 U=\left|\bigcup_j B_j\right|,
 \qquad C=\bigcap_j B_j,
 \qquad c=|C|.
\tag{NP1}
\]

Assume **no customer outside `C` belongs to exactly one maximal coverage**:

\[
 x\in\bigcup_j B_j\setminus C
 \quad\Longrightarrow\quad
 |\{j:x\in B_j\}|\ge2.
\tag{NP2}
\]

This is a condition on the full maximal coverages, not on the actual
selected actions. Internal catalog subthemes can omit any private-looking
part of a maximum, shared block, or common core.

**Theorem.** Every complete ordered-history pure SPE satisfies

\[
 \boxed{\operatorname{OPT}_n\le2W\quad(n\ge1).}
\tag{NP3}
\]

For `n>=5` the stronger union conclusion holds:

\[
 \boxed{U\le2W-c.}
\tag{NP4}
\]

In this range `OPT_n=U`: with at most six maxima, any five of them cover
every residual customer under (NP2), and cover the common core. The theorem
permits arbitrary crossed incidence, for example six maxima whose customer
blocks are all fifteen distinct pair incidences. This class contains
six-maxima instances outside both the five-maxima and laminar-incidence
theorems.

## 2. A history-specific floor

Assign each catalog label `A` to one containing maximal coverage `B_{a(A)}`.
Full maximal labels are assigned to their own coverage. No action or final
customer load is changed. For a legal ordered prefix of length `t`, let
`p_j` count earlier actions assigned to `j`, and put `r=n-t`.

Partition the residual customers by their maximal incidence:

\[
 X_I=\{x:\{j:x\in B_j\}=I\},\qquad w_I=|X_I|,
 \qquad 2\le |I|\le s-1.
\tag{NP5}
\]

The omitted incidence `[s]` is the core; singleton incidences have zero mass
by (NP2). Define

\[
 p_I=\sum_{k\in I}p_k,
 \qquad f_j(p,r)=\sum_{I\ni j}\frac{w_I}{p_I+r},
 \qquad F(p,r)=\max_{1\le j\le s}f_j(p,r).
\tag{NP6}
\]

All denominators are positive. If the current player deviates to the whole
`B_j`, every residual customer it covers has true earlier load at most
`p_I`, because any earlier action covering it is assigned to an index in
`I`. Including the deviator and all followers adds at most `r` covers, so
its true final load is at most `p_I+r`. Every core customer has load at
most `n`. Against every actual continuation, the deviation payoff is
therefore at least `c/n+f_j(p,r)`. This step needs no follower equilibrium
condition.

The extra fact unavailable for general private/shared incidence is

\[
 f_j(p+e_k,r-1)\ge f_j(p,r)\qquad(r\ge2).
\tag{NP7}
\]

Indeed, the denominator of a type `I` stays fixed when `k` belongs to `I`,
and decreases by one otherwise. Consequently `F` is nondecreasing along
every legal routing successor, including off-path successors.

**All-history floor.** At every legal ordered prefix, the current player's
final payoff in every complete SPE continuation satisfies

\[
 \boxed{u\ge c/n+F(p,r).}
\tag{NP8}
\]

At each ordered prefix, deviate to a full maximal coverage maximizing
`f_j`. The load bound just proved guarantees `c/n+F(p,r)` against the
continuation actually prescribed at that deviating history. Current SPE
optimality gives the same floor to the actual current action. This does
not freeze any replies or identify the choices at different ordered
histories. In the private-free case the direct worst-continuation load
bound already suffices; no backward propagation is required for (NP8).

Along the root terminal history, write `p^t` for the routed prefix counts.
Summing (NP8) gives the path-sensitive welfare certificate

\[
 \boxed{W\ge c+\sum_{t=0}^{n-1}F(p^t,n-t).}
\tag{NP9}
\]

## 3. Seven or more providers

For `r>=1`, set `y_j=p_j+r/2`. For every residual incidence `I`,

\[
 \frac{\sum_{j\in I}y_j}{p_I+r}
 =\frac{p_I+|I|r/2}{p_I+r}\ge1.
\tag{NP10}
\]

Unlike the mixed private/shared proof, this is also valid at the last slot.
Since `s<=6`,

\[
 U-c\le\sum_jy_jf_j(p,r)
 \le(t+sr/2)F(p,r)\le(3n-2t)F(p,r).
\tag{NP11}
\]

Thus (NP9) implies

\[
 W\ge c+H_n(U-c),\qquad
 H_n=\sum_{t=0}^{n-1}\frac1{3n-2t}.
\tag{NP12}
\]

For completeness, the following elementary estimate proves `H_n>1/2`
for every `n>=7`, without assuming monotonicity of these discrete sums.
The function `g(x)=1/(3-2x)` is convex on `[0,1]`. The integral is at most
its composite trapezoid sum, which equals the left endpoint sum `H_n`
plus `(g(1)-g(0))/(2n)=1/(3n)`. Hence

\[
 H_n\ge\frac12\log3-\frac1{3n}.
\tag{NP13}
\]

The positive geometric-series integral
`log((1+z)/(1-z))=2 sum_{k>=0} z^(2k+1)/(2k+1)`, at `z=1/2`, yields

\[
 \log3>1+\frac1{12}+\frac1{80}+\frac1{448}
 =\frac{7379}{6720}.
\]

Consequently, for every `n>=7`,

\[
 H_n>\frac{7379}{13440}-\frac1{21}
 =\frac{6739}{13440}=\frac12+\frac{19}{13440}>\frac12.
\tag{NP14}
\]

Equations (NP12)--(NP14) prove (NP4) in this range.

## 4. Five and six providers: finite rational coefficient proof

The coarser scalar sums in (NP12) equal `22003/45045<1/2` for `n=5` and
`2509/5040<1/2` for `n=6`. We therefore retain the entire path in (NP9).
The proof below is a finite coefficient argument over **arbitrary residual
block masses**, rather than testing finitely many games.

Use six proof indices. When `s<6`, append zero coordinates to `p` and zero
functions `f_j`; no fictitious game action is added. Residual incidences are
nonempty subsets of these indices of sizes two through five. For a fixed
routed prefix sequence `a=(a_0,...,a_{n-2})`, choose nonnegative integers
`d_{tj}` with

\[
 \sum_{j=0}^5d_{tj}=12\qquad(0\le t\le n-1)
\tag{NP15}
\]

such that every residual incidence `I` has

\[
 K_I(a)=\sum_{t=0}^{n-1}
 \frac{\sum_{j\in I}d_{tj}}{12(p_I^t+n-t)}\ge\frac12.
\tag{NP16}
\]

These conditions give, by expanding the nonnegative weighted sums,

\[
 \begin{aligned}
 \sum_t F(p^t,n-t)
 &\ge\sum_t\sum_j\frac{d_{tj}}{12}f_j(p^t,n-t)\\
 &=\sum_Iw_I K_I(a)\ge\frac12\sum_Iw_I
 =\frac{U-c}{2}.
 \end{aligned}
\tag{NP17}
\]

It remains to provide and verify the `d` arrays for every possible path.
Relabel indices by their first appearance in the prefix. The canonical
paths are exactly the restricted-growth strings of length `n-1`: the first
entry is zero and each next entry is at most one plus the largest earlier
entry. There are fifteen paths for `n=5` and fifty-two for `n=6`; at most
five indices occur, so the six-index limit excludes none of these strings.

The complete arrays are frozen in
[`customer_attraction_six_maxima_no_private_certificates.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_no_private_certificates.json).
Every entry is an integer between zero and twelve. As one example, for
`n=5` and prefix `(0,1,2,3)`, the array is:

| Prefix length t | d_t0 | d_t1 | d_t2 | d_t3 | d_t4 | d_t5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 12 | 0 | 0 | 0 | 0 | 0 |
| 1 | 4 | 8 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 12 | 0 | 0 | 0 |
| 3 | 3 | 0 | 0 | 9 | 0 | 0 |
| 4 | 0 | 4 | 0 | 0 | 4 | 4 |

The accompanying independent audit enumerates the entire canonical path
set, checks that the file has exactly one certificate for every path, checks
(NP15), and checks (NP16) for all fifty-six residual incidence masks using
`Fraction`. This is 3,752 exact coefficient inequalities. The minimum
verified coefficient is exactly `1/2` in both provider counts.

For clarity, the whole logical obligation is the following short checker;
`certificate[n][a]` denotes the stored integer array:

```python
for n in (5, 6):
    assert set(certificate[n]) == set(restricted_growth_strings(n - 1))
    for a, d in certificate[n].items():
        assert all(sum(row) == 12 for row in d)
        p = [0] * 6
        coefficients = {I: Fraction(0) for I in residual_masks}
        for t in range(n):
            for I in residual_masks:
                pI = sum(p[j] for j in range(6) if I >> j & 1)
                numerator = sum(d[t][j] for j in range(6) if I >> j & 1)
                coefficients[I] += Fraction(numerator, 12 * (pI + n - t))
            if t < n - 1:
                p[a[t]] += 1
        assert min(coefficients.values()) >= Fraction(1, 2)
```

Here `residual_masks` consists of all masks from one through sixty-two with
at least two set bits. Equations (NP15)--(NP17), the explicit certificate
arrays, and these exhaustively checked rational identities close the
five- and six-provider branches of the universal proof. Inserting (NP17)
into (NP9) proves (NP4).

## 5. Nine or more providers: unrestricted six maxima

**Corollary (`CA-SIX-MAXIMA-NINE-PLUS-HALF`).** Remove assumption (NP2),
retain `s<=6` and arbitrary internal catalog actions, and assume `n>=9`.
Every complete ordered-history pure SPE satisfies

\[
 \boxed{\operatorname{OPT}_n=U\le2W-c.}
\tag{NP20}
\]

This follows from the general mixed private/shared interface in
[the dynamic proof, Section 5](dynamic_maxima_bound.md#5-mixed-privateshared-refinement),
with the following exact uniform six-maxima estimates. Let `P` be total
globally private mass and `V=U-c-P`. For `t<=n-2` put

\[
 A_t=\frac{n+t}{2(t+1)(3n-2t)},\qquad
 B_t=\frac1{3n-2t},
\]

and at `t=n-1` put

\[
 A_{n-1}=\frac1{n+5},\qquad
 B_{n-1}=\frac{n+1}{n(n+5)}.
\tag{NP21}
\]

The actual six-or-fewer-maxima weight sums are no larger than these fixed
six-index denominators; hence the cited interface gives

\[
 W\ge c+P\sum_t\min_{q\ge t}A_q+V\sum_t B_t.
\tag{NP22}
\]

Here `B_t` is nondecreasing: the interior denominators decrease with `t`,
and its last-step comparison is `(n+1)(n+4)>=n(n+5)`, whose difference is
four. For `n>=5`, every interior private coefficient is at least `1/(2n)`.
Indeed, the required inequality is

\[
 \begin{aligned}
 n(n+t)-(t+1)(3n-2t)
 &=2\left(t-\frac{n-1}{2}\right)^2
   +\frac{n^2-4n-1}{2}\ge0.
 \end{aligned}
\tag{NP23}
\]

Also `A_{n-1}=1/(n+5)>=1/(2n)`. Therefore the private envelope sum in
(NP22) is at least `1/2`.

For the shared coefficient, write the previously defined `H_n` as
`sum_{r=1}^n 1/(n+2r)`. Then

\[
 \begin{aligned}
 \mathcal B_n:=\sum_tB_t
 &=\sum_{r=2}^n\frac1{n+2r}+\frac{n+1}{n(n+5)}\\
 &=H_n-\delta_n,\qquad
 \delta_n=\frac{2(n-1)}{n(n+2)(n+5)}.
 \end{aligned}
\tag{NP24}
\]

The correction `delta_n` decreases for integer `n>=2`: after putting
`delta_n-delta_(n+1)` over its positive common denominator, its numerator
is

\[
 2\bigl(2n^3+7n^2-9n-18\bigr)
 =2(n-2)(2n^2+11n+13)+16>0.
\]

Thus (NP13), the same positive series bound for `log3`, and `n>=9` give

\[
 \mathcal B_n>
 \frac{7379}{13440}-\frac1{27}-\delta_9
 =\frac{665881}{1330560}
 =\frac12+\frac{601}{1330560}>\frac12.
\tag{NP25}
\]

For comparison, the exact endpoint sum is
`mathcal B_9=229324183/456326325>1/2`. Equations (NP22)--(NP25) imply
`W>=c+(P+V)/2`, proving (NP20). All six maxima fit when `n>=9`, so
`OPT_n=U`. This corollary supplies the stronger core bound for `n>=9`. The separate [joint-budget theorem](six_maxima_joint_bound.md) now covers ordinary half coverage at `n=5,6,7,8` without (NP2); the no-private theorem above retains its stronger stated core bound.

Independent internal review checked the private polynomial inequalities,
the shared identity, the decreasing correction, and all six-or-fewer-maxima
denominator comparisons. Its frozen exact report is
[`customer_attraction_six_maxima_nine_plus_review.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_nine_plus_review.json).

## 6. Small provider counts and boundary cases

For `n=1`, the sole provider maximizes coverage. For `n=2`, use the
unconditional [two-provider bound](two_remaining_tax.md), `OPT_2<=3W/2`.
For `n=3`, use the unconditional
[three-provider sharp bound](three_player_sharp.md), `OPT_3<=5W/3`.
For `n=4`, use the unconditional
[four-provider bound](four_player_bound.md), `OPT_4<2W` for positive coverage.
These prove (NP3) for the remaining counts; no union conclusion is asserted
for `n<5`.

A unique distinct maximum gives `W=OPT_n=U`: the last provider chooses the
whole maximum, since every omitted customer has strictly positive joining
share. The all-zero instance is immediate. Duplicate labels and empty
actions have fixed routings and cannot invalidate any load upper bound.
Nonmaximal selected actions and omitted common-core customers are already
covered in Section 2. Every proof compares payoffs within the actual
continuation prescribed at the deviating ordered history.

## 7. An exact obstruction to a stronger unrestricted-six seat budget

This section is a mechanism limitation, not an SPE welfare counterexample.
For arbitrary incidence, one can strengthen the old static seats at a
prefix by defining

\[
 v_j(p,r)=\sum_{\substack{I\ni j\\|I|\ge2,I\ne[s]}}
 \frac{w_I}{p_I+r},\qquad
 q_{j,k}(p,r)=\frac{w_{\{j\}}}{p_j+k}+v_j(p,r),
 \quad1\le k\le r.
\tag{NP18}
\]

Let `xi(p,r)` be the `r`th largest of the `sr` seat values. The same
seat-capacity and subset-domination induction proves an all-history current
floor `c/n+xi(p,r)`. Here is the extra monotonicity detail. A routing
successor increases every shared term. On the selected route, private
seats shift from indices `1,...,r` to `2,...,r`; other routes retain their
first `r-1` seats. If at least `r` old seats meet a threshold, at least
`r-1` new seats do: absent a route with `r` old qualifying seats, only the
selected route can lose a qualifying seat; if some route has all `r`
qualifying seats, it alone retains at least `r-1`. Thus `xi` is nondecreasing
along successors, and the induction is valid.

However the aggregate budget `sum_t xi(p^t,n-t)` cannot universally pay
half of `OPT_5` even with six distinct maxima. Take these nine disjoint
customer blocks, with one-based maximal incidences:

| Incidence | Number of unit customers |
| --- | ---: |
| `{3}` | 27 |
| `{5}` | 1 |
| `{6}` | 1 |
| `{1,4}` | 9 |
| `{2,4}` | 9 |
| `{1,5}` | 21 |
| `{4,5}` | 4 |
| `{2,6}` | 21 |
| `{4,6}` | 4 |

Let each of the six maxima consist of exactly the blocks whose incidence
contains its index; the catalog can consist of these maxima alone. They
are distinct and incomparable, `c=0`, and `U=97`. Choosing maxima
`1,2,3,5,6` covers the whole union, so `OPT_5=97`. Along routed prefixes
`(),(1),(1,2),(1,2,3),(1,2,3,4)`, exact seat sorting gives

\[
 (\xi_0,\xi_1,\xi_2,\xi_3,\xi_4)
 =\left(6,\frac{15}{2},9,10,\frac{27}{2}\right),
 \qquad \sum_t\xi_t=46<\frac{97}{2}.
\tag{NP19}
\]

The audit recalculates these seats directly with rational arithmetic. The
prefix sequence need not be an equilibrium sequence, and (NP19) does not
assert that an actual SPE has welfare forty-six. It identifies the precise
missing global payment in this stronger seat mechanism. The proof of
(NP3) requires (NP2) and does not extend it silently to unrestricted six
maxima.

The [expanded mechanism audit](six_maxima_seat_obstructions.md) also gives
integer customer instances at `n=6,7,8`, with exact budget-to-OPT ratios
`55/112`, `140687/282485`, and `3283/6624`, respectively, all below `1/2`.
Thus the same unrestricted dynamic-seat path payment fails at every
critical count `n=5,...,8`. These are legal-path budget failures; no
equilibrium welfare counterexample is asserted.

## 8. Independent exact audit

[`tests/audits/customer_attraction_six_maxima_no_private.py`](../../../tests/audits/customer_attraction_six_maxima_no_private.py)
imports no repository model, solver, or earlier audit. It verifies the
complete rational coefficient family, checks the analytic constants,
recomputes (NP19), and tests the history-specific floor against independently
constructed full continuation menus. Selected outcomes are expanded into
complete ordered-history strategies and checked directly for every legal
deviation. The test families include six crossed maxima, core-omitting
subthemes, repeated coverage labels, empty actions, and zero coverage.

The initial frozen run is
[`customer_attraction_six_maxima_no_private.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_no_private.json).
Its default run passed 89 finite games, 48,194 count states, 30,760
history-floor payoff comparisons, and 199,398 literal ordered-history
deviation comparisons over 24 complete strategies. Independent internal
review rechecked all 3,752 coefficients, all 9,072 labeled prefix strings,
and 6,252 incidence checks after padding; its report is
[`customer_attraction_six_maxima_no_private_review.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_no_private_review.json).
The expanded audit, including the unrestricted nine-provider corollary,
is frozen in
[`customer_attraction_six_maxima_no_private_final.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_no_private_final.json):
92 finite games, 63,209 states, 39,811 history-floor comparisons, 9,051
additional mixed-floor comparisons, and the same complete-strategy
deviation checks. Neither finite game family substitutes for the universal
proof.
Finite SPE testing is separate from the arbitrary-customer and
arbitrary-provider proof above. Run from the repository root:

```sh
python3 tests/audits/customer_attraction_six_maxima_no_private.py
```
