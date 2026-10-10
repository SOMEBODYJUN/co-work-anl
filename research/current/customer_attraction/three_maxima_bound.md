# Three maximal coverages: all-history half coverage with arbitrary subthemes

**Direct proof, 2026-10-10.** Proposed claim ID:
`CA-THREE-MAXIMA-HALF`. The input class has at most three distinct
inclusion-maximal coverage sets. All catalog subthemes remain legal; they may
omit private customers, shared customers, or the entire common maximal core.
Every complete ordered-history pure SPE satisfies the theorem. The general
common-catalog conjecture, with four or more distinct maxima, remains open.
External peer review and novelty have not been certified.

## 1. Statement and exact scope

Use [CAG-MODEL](model.md): a common finite nonempty catalog, unit customers,
`n>=1` unit providers choosing sequentially, equal customer shares, and pure
SPE specified at every ordered history. Repetition, empty actions, and
different labels with identical coverage are allowed.

Let `B_1,...,B_s` be the distinct inclusion-maximal coverage sets, where
`1<=s<=3`. Put

\[
U=\left|\bigcup_{j=1}^s B_j\right|,\qquad
C=\bigcap_{j=1}^s B_j,\qquad c=|C|.
\tag{TM1}
\]

**Theorem.** Every complete ordered-history pure SPE with root welfare `W`
satisfies, for `n>=2`,

\[
\boxed{\operatorname{OPT}_n\le U\le c+2(W-c)=2W-c.}
\tag{TM2}
\]

For `n=1`, the sole provider maximizes coverage and
`W=OPT_1`. With a single distinct maximal coverage, the last provider chooses
that coverage and `W=U=OPT_n` for every `n`. When `n>=s`,
`OPT_n=U`, since the maxima themselves are legal catalog choices.

This covers three-maximum catalogs outside the laminar maximal-incidence
class: three maxima may have crossed customer incidences. The two input
classes are incomparable, since the laminar theorem also allows arbitrarily
many maxima. For example, for four disjoint nonempty
blocks `X,Y,Z,V`,

\[
B_1=X\cup Y,\quad B_2=X\cup Z,\quad B_3=Y\cup V
\tag{TM3}
\]

have crossed incidences `{1,2}` and `{1,3}`. Arbitrary catalog subthemes of
these three maxima may be added. Neither maximal selected actions nor static
Nash behavior is assumed.

## 2. A universal superset seat floor, including omitted cores

For this section only, the number of distinct maxima may be arbitrary but
is at least two; the unique-maximum case was handled in Section 1.
Fix a routing map `a(A)` assigning every catalog label `A` to a containing
maximal coverage `B_{a(A)}`. A full maximal label is routed to its own coverage.
This is a proof device; actions, customer loads, and histories are unchanged.

For each maximum define its globally private block and residual shared size:

\[
P_j=B_j\setminus\bigcup_{k\ne j}B_k,\qquad
w_j=|P_j|,\qquad v'_j=|B_j\setminus(P_j\cup C)|.
\tag{TM4}
\]

For at least two maxima, `P_j` and `C` are disjoint. Its residual seats are

\[
g_j(k)=\frac{w_j}{k}+\frac{v'_j}{n},
\qquad 1\le k\le n.
\tag{TM5}
\]

Let `nu` be the `n`th largest value, with multiplicity, among all these seats.
Then every provider in every root SPE has final payoff at least `nu+c/n`:

\[
\boxed{W\ge c+n\nu.}
\tag{TM6}
\]

Here `nu` is the ordinary [universal private/shared seat
floor](sunflower_maxima_bound.md#8-任意共同目录可用的-superset-席位接口),
shifted by `c/n`; the proof below explicitly handles core omissions.

**Proof.** For `L>0`, define

\[
d_j(L)=\max\bigl(\{0\}\cup\{k\le n:g_j(k)\ge L\}\bigr).
\]

At a legal prefix let `p_j` count earlier providers routed to maximum `j`,
and let `r` be the number of remaining providers. We prove by induction on
`r` that

\[
\sum_j\max\{d_j(L)-p_j,0\}\ge r
\quad\Longrightarrow\quad
\text{each remaining provider's final payoff is at least }L+c/n
\tag{TM7}
\]

for every complete SPE continuation at that prefix. Any one action increases
only one routing count, so the left side decreases by at most one.
Choose an available maximum `B_j`, with `p_j<d_j(L)`, as a current
deviation. Its actual continuation is a subgame SPE; all its followers
therefore meet the inductive floor.

If a follower is routed to `j`, its selected action is a subset of the
deviator's full `B_j`. Both receive the same share on each commonly covered
customer in this same terminal history. Hence the deviator's payoff is at
least that follower's payoff, and thus at least `L+c/n`.

If no follower is routed to `j`, no follower covers `P_j`. Earlier load on
each such customer is at most `p_j`; consequently its private contribution
is at least `w_j/(p_j+1)`. Every residual shared customer in `B_j` and every
core customer in `C` contributes at least `1/n`, because the deviator really
selects the entire maximum and total load is at most `n`. Its payoff is at
least `g_j(p_j+1)+c/n>=L+c/n`.

With `r=1`, only the latter case is needed, which proves the base case.
Current SPE optimality transfers the actual deviation guarantee to the
actual current action, and the induction also covers actual follower
histories. No follower action is frozen across a deviation, and no two
ordered histories are identified.

If `nu>0`, at least `n` seats meet `nu`, so (TM7) applies at the root with
`L=nu`, proving (TM6). If `nu=0`, each provider can choose any maximum and
receive at least `c/n` from its core under every continuation. SPE gives
that same floor, again proving (TM6). This also covers the all-zero case.
∎

## 3. A three-maximum global union budget

Assume now `s=3` and `n>=2`. For each maximum, let

\[
e_j=|\{k\le n:g_j(k)>\nu\}|,
\qquad a_j=e_j+1.
\tag{TM8}
\]

The definition of the `n`th largest seat implies

\[
\sum_j e_j\le n-1,\qquad
1\le a_j\le n,\qquad
\sum_j a_j\le n+2\le2n.
\tag{TM9}
\]

Since the seats of each maximum are nonincreasing, its first seat after all
strictly larger ones has

\[
\frac{w_j}{a_j}+\frac{v'_j}{n}=g_j(a_j)\le\nu.
\tag{TM10}
\]

Choose real weights `y_j` satisfying

\[
a_j\le y_j\le n,\qquad y_1+y_2+y_3=2n.
\tag{TM11}
\]

They always exist: start with `y_j=a_j`; the deficit to `2n` is nonnegative,
and the available capacity to increase the three coordinates to `n` is
`3n-sum_j a_j`, which exceeds that deficit by `n`.

Every customer outside `C` belongs to either one maximum or exactly two
maxima. In the weighted sum of (TM10), a private customer of maximum `j`
has coefficient `y_j/a_j>=1`. A shared customer belonging to maxima `j,k`
has coefficient

\[
\frac{y_j+y_k}{n}
=\frac{2n-y_\ell}{n}\ge1,
\quad\{j,k,\ell\}=\{1,2,3\}.
\tag{TM12}
\]

Thus this single weighted sum counts the whole residual union at least once:

\[
\boxed{U-c\le\sum_jy_jg_j(a_j)\le2n\nu.}
\tag{TM13}
\]

Combining (TM13) with (TM6) gives (TM2). This is a global shared-customer
budget, not a per-provider residual guarantee or a matching of single
deviations to optimal themes.

For `s=2`, define `e_j,a_j` by (TM8), now indexed by `j=1,2`, and choose
`y_1=y_2=n`. Residual customers are all private, so
`U-c=sum_jw_j<=sum_j n g_j(a_j)<=2n nu`; the same conclusion follows.
Alternatively the sharper sunflower theorem applies. `s=1` was handled in
Section 1. These conventions avoid adding fictitious catalog actions.

If `nu=0`, (TM10)--(TM13) still hold and give `U=c`; no division by `nu`
occurs. Zero coverage, empty subthemes, duplicated labels, and ties in the
seat order therefore require no limiting argument.

## 4. A sharper instance-specific certificate

For three maxima, put

\[
A=a_1+a_2+a_3,\qquad
S=\max\{A,n+\max_j a_j,3n/2\}.
\tag{TM14}
\]

There are weights `y_j>=a_j` with sum `S` and each pair sum at least `n`.
Indeed, choose `y_j` in the intervals `[a_j,S-n]` with total `S`.
Each interval is nonempty because `S>=n+max a`; the lower endpoints sum to
`A<=S`, and the upper endpoints sum to `3(S-n)>=S`. Filling these intervals
constructs the required weights. For each pair,
`y_j+y_k=S-y_l>=n`.

The same customer counting yields

\[
\boxed{U-c\le S\nu,
\qquad
\operatorname{OPT}_n\le c+\frac Sn(W-c),
\qquad S\le2n.}
\tag{TM15}
\]

`S` is exactly the minimum weight sum if all three pair constraints are
imposed: any feasible weights have sum at least `A`; summing the pair
constraints gives at least `3n/2`; and the pair complementary to a largest
`a_j` gives sum at least `n+max a`. This asserts optimality of this scalar
certificate, not sharpness of the SPE welfare theorem. If some pair block
is empty, omitting its constraint may give a smaller certificate.

The scalar method alone cannot improve its uniform factor below two even
with three distinct maxima. Fix `n>=2` and integer `M>n-1`. Take disjoint
blocks: `B_1` is a private block of size `nM`, while `B_2` and `B_3` share
another block of size `nM` and have distinct unit private petals. Then
`c=0`, `nu=M+1`, `a=(n,1,1)`, and

\[
\frac{U}{n\nu}
=\frac{2nM+2}{n(M+1)}\longrightarrow2.
\tag{TM16}
\]

The actual SPE welfare may be much larger than `n nu`; this is only a
barrier to tightening the static union-to-seat step. No sharp welfare
example or counterexample to a factor `2-1/n` is asserted.

For an arbitrary number of maxima, the same calculation gives a usable
incidence certificate. Define `a_j` by (TM8). If there are nonnegative
weights `y_j` with `y_j>=a_j` on every nonempty private block and
\[
\sum_{j:x\in B_j}y_j\ge n
\quad\text{for every nonprivate customer }x\notin C,
\tag{TM17}
\]
then `U-c<=nu sum_j y_j`, and therefore
`OPT_n<=c+(sum_j y_j/n)(W-c)`. The condition `sum_j y_j<=2n` is sufficient
for half coverage. Zero-private maxima do not need the private-block lower
bound. This is a certificate for a particular incidence pattern, not a
claim that such weights always exist.

The corresponding unrestricted scalar budget already fails at four distinct
maxima. Take a private block of size `2n` on `B_1`. Among `B_2,B_3,B_4`,
place three disjoint blocks of size `n` each, respectively shared only by
the pairs `{2,3}`, `{2,4}`, and `{3,4}`. Then `c=0`, all residual seats of
the latter three maxima equal two, and the first maximum's seats are `2n/k`.
Thus its `n`th largest seat is `nu=2`, whereas
\[
U=5n>4n=2n\nu.
\tag{TM18}
\]
All masses are integer unit-customer multiplicities and all four maxima are
distinct. For `n>=3`, the three legal choices `B_1,B_2,B_3` already cover
the full union, so `OPT_n=U` and the optimal-coverage-to-seat budget also
fails. This disproves the universal union-to-seat budget with four
maxima; it supplies no SPE welfare counterexample. Actual credible
continuations may provide a larger welfare budget than `n nu`.

## 5. Exact verification and remaining scope

The audit `tests/audits/customer_attraction_three_maxima.py` independently
computes literal customer shares with `Fraction`, reconstructs maximal
coverages and seats, checks the weighted union coefficients, and evaluates
all retained SPE continuation menus in its finite test families. Selected
menus are expanded into complete ordered-history strategies and directly
checked at every history. A second independent coefficient audit checks the
weights and the formula for `S` without importing the first audit.

These are finite implementation checks. Sections 2--4 supply the proof for
arbitrary numbers of providers and arbitrary legal internal subthemes in
the stated class. Four or more maximal coverages may contain customers
shared by two maxima whose complementary maxima consume most of the seat
budget; (TM12) is then unavailable. The general half-coverage conjecture
therefore remains open.
