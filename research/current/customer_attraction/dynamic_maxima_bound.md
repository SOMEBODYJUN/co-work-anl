# Dynamic maximal-cover routing budget

Direct self-contained proof, 2026-10-10. The general arbitrary-maxima
half-coverage conjecture remains open. Proposed claim IDs are
`CA-DYNAMIC-MAXIMA-FLOOR`, `CA-DYNAMIC-MAXIMA-MIXED`, and
`CA-FIVE-MAXIMA-HALF`. External peer review and novelty have not been certified.
This proof covers every complete ordered-history pure SPE, and retains every
catalog subset action, including actions omitting the common maximal core.
Finite verification is separate from the proof.

## Exact statement

Use [CAG-MODEL](model.md): a finite nonempty common action catalog of customer subsets,
n >= 1 unit providers, unit-valued customers, sequential observed actions,
and equal final 1/load customer shares. A pure SPE specifies an action at
every ordered history. Repeated actions, empty actions, identical coverage
labels, and unrelated ties at different histories are allowed.

Let B_1,...,B_s be the distinct inclusion-maximal coverage sets, with s >= 2.
Let U=|union_j B_j|, C=intersection_j B_j, and c=|C|. Fix n and define, for
0 <= t <= n-1,

\[
D_t=\max\left\{t+\frac{s(n-t)}2,\ n+s-1\right\},\qquad
\Gamma_{n,s}=\sum_{t=0}^{n-1}\frac1{D_t}.
\tag{1}
\]

**Theorem (all catalogs, incidence unrestricted).** At every legal prefix
of length t, the current provider's final payoff in every complete pure SPE
continuation is at least

\[
\boxed{\frac cn+\frac{U-c}{D_t}.}
\tag{2}
\]

Thus every root pure SPE with welfare W obeys

\[
\boxed{W\ge c+\Gamma_{n,s}(U-c).}
\tag{3}
\]

For s <= 4 and n >= 3, each D_t <= 2n, hence Gamma_{n,s} >= 1/2 and

\[
\boxed{\operatorname{OPT}_n\le U\le 2W-c.}
\tag{4}
\]

With one distinct maximal coverage, the last provider selects it, unless all
customer payoffs are zero, in which case every coverage is empty; therefore
W=U=OPT_n. For n=1 the only provider selects a largest legal coverage and
W=OPT_1. For n=2 the unconditional [two-provider bound](two_remaining_tax.md)
OPT_2 <= (3/2)W already implies half coverage. Consequently **every common catalog with at
most four distinct maximal coverages satisfies OPT_n <= 2W for all n >= 1.**
The strengthened union assertion (4) is only claimed for n >= 3.

A stronger mixed private/shared calculation below also handles n=5 and
s <= 5. Together with the known one-, two-, [three-](three_player_sharp.md),
and [four-provider](four_player_bound.md) general bounds, and a direct
Jensen estimate for n >= 6, it proves:

**Five-maxima theorem.** Every common catalog with at most five distinct
inclusion-maximal coverage sets, arbitrary internal actions, and every
complete ordered-history pure SPE satisfies OPT_n <= 2W for all n >= 1.
For n >= 5 the stronger union inequality U <= 2W-c holds.

The exact gain for s=4 is Gamma_{3,4}=1/2,
Gamma_{4,4}=31/56, and Gamma_{5,4}=211/360. In particular, the argument gives
more than a strict enlargement of the three-maximum input class. As n tends
to infinity with s=4 fixed, Gamma_{n,4} tends to log 2.

## 1. Fixed routing and actual customer loads

Assign every catalog label A to one containing distinct maximal coverage
B_{a(A)}. A full maximal label is assigned to its own coverage. This is only
a proof device: A's actual customer set and the specified SPE remain unchanged.
There exists such an assignment because the catalog is finite.

For each nonempty I subset of [s], let

\[
X_I=\{x:\{j:x\in B_j\}=I\},\qquad w_I=|X_I|.
\tag{5}
\]

The core is X_[s]. Remove its contribution when writing residual sums. At an
arbitrary actual ordered prefix h of length t, let p_j count earlier actions
assigned to j and put p_I=sum_{j in I}p_j and r=n-t. Any earlier action
covering x in X_I is assigned to an index in I. Hence the true earlier load
of each such customer is at most p_I. No action is expanded in the game.

Define the auxiliary residual value

\[
f_j(p,r)=\frac{w_{\{j\}}}{p_j+1}
+\sum_{\substack{I\ni j\\2\le |I|\le s-1}}
\frac{w_I}{p_I+r}.
\tag{6}
\]

All denominators are positive. The residual types partition the coverable
customers outside C. A term of weight zero may simply be omitted.

Consider the legal deviation to the **whole** B_j, followed by the actual
continuation specified at that deviating history. If no subsequent action is
assigned to j, no later action covers a customer of X_{ {j} }; its final
load is at most p_j+1. For any nonprivate residual customer covered by B_j,
its final load is at most p_I+r, since at most r-1 followers can cover it.
Every core customer is really covered by the deviator and has load at most n.
Therefore this actual deviation payoff is at least

\[
f_j(p,r)+c/n.
\tag{7}
\]

If a subsequent action is assigned to j, that later action is a subset of
B_j. In their common actual terminal history the earlier deviator receives
the same share on every customer covered by that follower, and may cover
additional customers. Thus the deviator's payoff is at least that follower's
payoff. This comparison requires neither an equilibrium follower action nor
maximality of that action; it uses only its true subset relation.

## 2. Dynamic union counting at every prefix

When r >= 2 set y_j=p_j+r/2. Its total is

\[
\sum_j y_j=t+sr/2.
\tag{8}
\]

A private residual type X_{ {j} } has coefficient

\[
\frac{y_j}{p_j+1}=\frac{p_j+r/2}{p_j+1}\ge1.
\tag{9}
\]

A nonprivate residual type X_I has coefficient in the weighted sum of (6)

\[
\sum_{j\in I}\frac{y_j}{p_I+r}
=\frac{p_I+|I|r/2}{p_I+r}\ge1.
\tag{10}
\]

The last inequality uses |I| >= 2. Hence

\[
U-c\le\sum_j y_j f_j(p,r)
\le(t+sr/2)\max_j f_j(p,r).
\tag{11}
\]

In particular max_j f_j(p,r) >= (U-c)/D_t.

When r=1, instead use y_j=p_j+1. Then sum_j y_j=n+s-1. A private coefficient
is one. For a nonprivate residual incidence I the coefficient is

\[
\frac{p_I+|I|}{p_I+1}\ge1.
\tag{12}
\]

The same union counting gives max_j f_j(p,1) >= (U-c)/(n+s-1), which is
at least (U-c)/D_{n-1}. In fact D_{n-1}=n+s-1 for s >= 2.

These inequalities use each customer's true maximal incidence; they do not
pretend shared blocks are globally private. The old root scalar seat bound
w_j/k+v_j/n is replaced by a budget depending on the routed prefix.

## 3. All ordered histories, backward induction

For fixed s >= 2, the sequence D_t is nonincreasing: its first argument is
sn/2-(s/2-1)t, and its second argument is constant. Accordingly

\[
\ell_t=c/n+(U-c)/D_t
\tag{13}
\]

is nondecreasing in t. We prove (2) by backward induction on remaining
providers, simultaneously for **all legal ordered prefixes** and **all pure
SPE continuations**.

For the last provider, choose a full maximal coverage attaining the maximum
in Section 2. There are no later actions, so (7) gives at least ell_{n-1}.
SPE optimality gives this bound for the actual last action.

Suppose t <= n-2 and the theorem is proved at every longer prefix. At the
current prefix choose a whole B_j maximizing f_j(p,r). After this real
deviation, the continuation of the given complete strategy is an SPE at the
new prefix. If there is a follower assigned to j, apply the inductive
statement to that follower's actual ordered decision prefix, of length
q >= t+1. Its payoff is at least ell_q >= ell_t; the subset domination from
Section 1 gives the same lower bound to the current deviator. If there is no
such follower, (7) and Section 2 give the deviator at least ell_t directly.
Current SPE optimality transfers this deviation guarantee to the actual
current action. This proves (2).

Along the root terminal history the current prefix lengths are precisely
0,...,n-1. Summing (2), and using W=sum_i u_i, proves (3).

This proof keeps every deviating continuation as actually prescribed by the
same complete strategy. It does not freeze replies after a deviation, merge
ordered histories having identical counts, assume any tie rule, or assert
SPE outcomes are static Nash equilibria.

## 4. Four maxima and boundary cases

For 2 <= s <= 4 and n >= 3,

\[
t+s(n-t)/2\le2n-t\le2n,\qquad n+s-1\le n+3\le2n.
\tag{14}
\]

Thus each D_t <= 2n and Gamma >= n/(2n)=1/2. Combining (3) with
OPT_n <= U proves (4). If n >= s, all maxima fit in an optimal portfolio and
OPT_n=U; if n < s we use only OPT_n <= U.

For s=4 and n >= 3 the first n-3 denominators are 2n,2n-1,...,n+4;
the last three denominators all equal n+3. Thus

\[
\boxed{\Gamma_{n,4}=\sum_{d=n+4}^{2n}\frac1d+\frac3{n+3},\quad n\ge3,}
\tag{15}
\]

where a sum with lower endpoint above the upper endpoint is zero. Formula
(15) agrees with (1), gives 1/2,31/56,211/360 at n=3,4,5, and tends to log 2.
The theorem uses the unambiguous definition (1).

Zero coverable customers give U=c=W=0 and satisfy every inequality without
a ratio. Empty actions and duplicated labels have fixed routing and cannot
invalidate any upper load bound. Full maximal labels exist in the catalog
by definition. Arbitrary internal subthemes, including those omitting C or
omitting all private customers, are covered by the subset domination and
load bounds. A maximum with no private customers simply has private weight
zero. For a unique distinct maximal coverage, all other actions are subsets
of it, and a last-player optimum covers it whenever its nonempty customers
have strictly positive shares; the zero case is immediate.

## 5. Mixed private/shared refinement

Let P be the total mass of globally private customers, and V the mass of
nonprivate customers outside C:

\[
P=\sum_{j=1}^s w_{\{j\}},\qquad V=U-c-P.
\tag{16}
\]

For r >= 2 put Z_t=t+s(n-t)/2. In (9), since p_j <= t, its private
coefficient has the stronger lower bound

\[
\frac{p_j+r/2}{p_j+1}
\ge a_t:=\frac{t+r/2}{t+1}=\frac{n+t}{2(t+1)}.
\tag{17}
\]

Indeed the left side is nonincreasing in p_j when r >= 2; at r=2 it is
constant. The shared coefficient in (10) remains at least one. Hence

\[
\max_j f_j(p,r)\ge\frac{a_t P+V}{Z_t},\qquad t\le n-2.
\tag{18}
\]

At the last position r=1 the private coefficient is one, while the shared
coefficient in (12) satisfies

\[
\frac{p_I+|I|}{p_I+1}=1+\frac{|I|-1}{p_I+1}
\ge1+\frac1n,
\tag{19}
\]

because p_I <= n-1 and |I| >= 2. Therefore

\[
\max_j f_j(p,1)\ge
\frac{P+(1+1/n)V}{n+s-1}.
\tag{20}
\]

For a reusable exact statement, define the raw coefficient sequences

\[
A_t=\begin{cases}a_t/Z_t,&t\le n-2,\\
1/(n+s-1),&t=n-1,\end{cases}\qquad
B_t=\begin{cases}1/Z_t,&t\le n-2,\\
(n+1)/(n(n+s-1)),&t=n-1.\end{cases}
\tag{21}
\]

Let underline A_t=min_{q>=t} A_q and underline B_t=min_{q>=t} B_q, where
q ranges over t,...,n-1. Both envelope sequences are nondecreasing and no
larger than the corresponding raw sequence. (For s >= 2, B is itself
nondecreasing; the last-step comparison reduces to s-2 >= 0.) The same
ordered-history induction as Section 3, with the monotone floor

\[
\boxed{\frac cn+P\underline A_t+V\underline B_t,}
\tag{22}
\]

proves this bound for every current provider at every legal prefix, and gives

\[
\boxed{W\ge c+P\sum_t\underline A_t+V\sum_t\underline B_t.}
\tag{23}
\]

This is a mixed-mass certificate for arbitrary numbers of maxima, not a
universal half-coverage assertion beyond the ranges proved below.

## 6. Five providers and at most five maxima

Assume n=5 and 2 <= s <= 5. In the r >= 2 calculation the actual total
weight is at most Z_t^*=t+5(5-t)/2. Thus (18) remains valid with this larger
fixed denominator. The following table records its exact coefficients.

| Prefix length t | Remaining r | Z_t^* | a_t/Z_t^* | 1/Z_t^* |
| --- | --- | --- | --- | --- |
| 0 | 5 | 25/2 | 1/5 | 2/25 |
| 1 | 4 | 11 | 3/22 | 1/11 |
| 2 | 3 | 19/2 | 7/57 | 2/19 |
| 3 | 2 | 8 | 1/8 | 1/8 |

All four private coefficients are at least 1/9. At t=4, the actual last
weight sum is 5+s-1 <= 9, so (20) gives

\[
\max_j f_j(p,1)\ge P/9+(2/15)V.
\tag{24}
\]

Define

\[
(b_0,b_1,b_2,b_3,b_4)=(2/25,1/11,2/19,1/8,2/15).
\tag{25}
\]

This sequence is strictly increasing. At every prefix the no-same-route
case of Section 1 therefore guarantees the current deviator at least
c/5+P/9+b_t V. A same-route follower has an at least as large floor by
backward induction. SPE optimality transfers the floor to the current
actual action, exactly as before. Hence every complete root pure SPE has

\[
\begin{aligned}
W&\ge c+\frac59 P+
\left(\frac2{25}+\frac1{11}+\frac2{19}+\frac18+\frac2{15}\right)V\\
&=c+\frac59P+\frac{67027}{125400}V
\ge c+\frac{67027}{125400}(U-c).
\end{aligned}
\tag{26}
\]

Both 5/9 and 67027/125400 exceed 1/2. Thus

\[
\boxed{U\le c+\frac{125400}{67027}(W-c)\le2W-c.}
\tag{27}
\]

No fictitious catalog actions are added when s < 5: only the arithmetic
upper bounds Z_t <= Z_t^* and 5+s-1 <= 9 are used.

## 7. At least six providers and at most five maxima

For 2 <= s <= 5, write r=n-t. Then

\[
D_t\le n+\max\{3r/2,4\}.
\tag{28}
\]

For n >= 2 the sum of these upper bounds is exactly

\[
\begin{aligned}
\sum_{r=1}^{n}\left(n+\max\{3r/2,4\}ight)
&=n^2+\frac32\frac{n(n+1)}2+\frac72\\
&=\frac{7n^2+3n+14}{4}.
\end{aligned}
\tag{29}
\]

The extra 7/2 consists of 5/2 at r=1 and 1 at r=2; for r >= 3 the maximum
is 3r/2. Cauchy-Schwarz (equivalently convexity of reciprocal) gives

\[
\Gamma_{n,s}=\sum_t\frac1{D_t}
\ge\frac{n^2}{\sum_tD_t}
\ge\frac{4n^2}{7n^2+3n+14}.
\tag{30}
\]

For n >= 6 this final fraction exceeds 1/2, since n^2-3n-14 is positive
at n=6 and strictly increases thereafter. Equation (3) gives U <= 2W-c.
Together with Section 6, this proves the union strengthening for every
n >= 5. For n=1,...,4 use the existing unconditional general-catalog
bounds cited in the statement, proving the five-maxima half-coverage
claim for every n. This argument does not use an unproved monotonicity
claim about the exact sequence Gamma_{n,5}.

## 8. Scope, old obstruction, and exact finite audit

The static globally-private superset seat budget fails at four maxima, as
shown in [the three-maxima proof](three_maxima_bound.md), equation (TM18).
That instance has a large private maximum next to three maxima sharing
three pair blocks. The present dynamic proof uses the actual routed prefix
in every shared denominator and in the coefficient weights; it therefore
escapes that static obstruction. It does not rely on propagation of the
last-slot worst immediate floor theta, which already fails in general.

The audit
[`tests/audits/customer_attraction_dynamic_maxima.py`](../../../tests/audits/customer_attraction_dynamic_maxima.py)
is independent of the canonical solver, model, and earlier audits. It
uses direct integer-scaled rational customer shares and all-continuation
menus. Each child menu may choose a different supported terminal, which
retains arbitrary ordered-history ties. Selected menu outcomes are expanded
into full ordered-history strategies and directly replayed against every
legal deviation. This algorithm is a finite verifier, not a complexity
claim or substitute for Sections 1-7.

The tested cases include every graph-only four-index incidence pattern,
the old four-maxima static obstruction, arbitrary positive incidence blocks,
internal actions omitting cores, empty actions, duplicate labels, zero
coverage, and one maximum. The report distinguishes exact implementation
checks from the universal proof. The audit also tests the mixed envelope
floor (22) directly on all retained action choices at every count state.

Run from the repository root:

```sh
python3 tests/audits/customer_attraction_dynamic_maxima.py
```

The unrestricted arbitrary-number-of-maxima conjecture is still open.
No attaining example or optimality certificate for the constants in this
page is claimed. External peer review and global novelty are unverified.
