# Complementary triad mechanism and a growing-support extension

Author: R1 / cycle_family subagent. Date: 2026-10-14 UTC.

## Scope and evidence level

This asset reconstructs the given three-player instance, supplies an explicit four-player degree-four nonexistence certificate, and defines a family allowing the player count and resource support to grow. It does **not** prove a new asymptotic lower bound. The support obstruction in `resource_support.md` explains why resourcewise-local copies of triads cannot suffice. The full-support family below escapes that particular obstruction, but its asymptotic usefulness is open.

The four-player finite claim has a complete exact all-state certificate, without external peer review. Numerical screening outputs are discovery data only and are independently filtered by exact rational evaluation. No novelty claim is made: comparison to one published construction is not a search over all known constructions.

## Pair convention

Each mask m has entries 0,1,2. Entry 0 excludes that player; entry 1 selects action 0; entry 2 selects action 1. For every resource with this mask and latency f, include a separate resource with entries 1 and 2 exchanged and the same f. Every included player uses exactly one resource of the pair in either action. Global bit complement preserves every player's cost, so states with player 0's bit equal to 0 represent all profiles.

## Exact triad cost template

Weights of players H,M,L are x,y,z>0. Use three complementary resource pairs:

| Pair | Mask | Latency |
|---|---|---|
| A | (0,1,1) | A(t) |
| B | (1,1,2) | B(t) |
| C | (1,2,1) | C(t) |

Put T=x+y+z. The complete cost table modulo global complement is:

| State | H | M | L |
|---|---|---|---|
| 000 | B(x+y)+C(x+z) | A(y+z)+B(x+y)+C(y) | A(y+z)+B(z)+C(x+z) |
| 001 | B(T)+C(x) | A(y)+B(T)+C(y+z) | A(z)+B(T)+C(y+z) |
| 010 | B(x)+C(T) | A(y)+B(y+z)+C(T) | A(z)+B(y+z)+C(T) |
| 011 | B(x+z)+C(x+y) | A(y+z)+B(y)+C(x+y) | A(y+z)+B(x+z)+C(z) |

For a target factor α, a sufficient **all-state** certificate is the following four inequalities:

\[
\begin{aligned}
A(y+z)+B(x+y)+C(y)&\ge\alpha[A(y)+B(y+z)+C(T)],\\
B(x)+C(T)&\ge\alpha[B(T)+C(x)],\\
A(z)+B(T)+C(y+z)&\ge\alpha[A(y+z)+B(z)+C(x+z)],\\
A(y+z)+B(x+z)+C(z)&\ge\alpha[A(z)+B(y+z)+C(T)].
\end{aligned}
\]

They respectively certify M at 000, H at 010 (whose resulting 110 is complementary to 001), L at 001, and L at 011. The first three are a quotient improvement cycle. The fourth is logically separate and closes the otherwise missing class. If all four hold, no β-PNE exists for any β<α. At α itself the inequalities may be equalities, so nonexistence at the endpoint does not follow.

For x=1,y=1/3,z=1/9 and A(t)=67t², B(t)=19t, C(t)=10t², exact enumeration gives best-improvement factors

| State representative | Witness | Best ratio |
|---|---|---|
| 000 | M | 3214/2977 |
| 001 | L | 2450/2243 |
| 010 | H | 3229/3033 |
| 011 | L | 2792/2441 |

Thus the instance's exact best equilibrium factor is 3229/3033. The verifier retains every player ratio and all eight profiles, not merely these witnesses.

## WC-R1-SIGNED-COLUMNS v1: defined family

Let there be one heavy player 0 of weight h>0 and m light players with arbitrary weights w_1,...,w_m>0. Each has two actions. There is a pair A with mask (0,1,...,1), and for each j∈{1,...,m} a pair B_j whose mask is all 1 except entry j equal to 2. Give these pairs arbitrary nonnegative-coefficient polynomial latencies A and f_j of maximum degree d. This is a valid subclass of WC-TARGET v1, with no fixed bound on m. For m=2 it is exactly the triad template up to relabeling B,C.

Normalize a state by player 0's action 0. Let S be the light players taking action 0, W_S=Σ_{i∈S}w_i, W=Σ_i w_i, and

\[
\delta_j(S)=w_j(1-2\mathbf1_{j\in S}),\quad
X_j(S)=h+W_S+\delta_j(S),\quad
Y_j(S)=W-W_S-\delta_j(S).
\]

Here X_j is the load on the B_j resource containing player 0, and Y_j is its complementary resource's load. Costs are exactly

\[
\begin{aligned}
C_0(S)&=\sum_{j=1}^{m} f_j(X_j(S)),\\
C_i(S)&=A(W_S)+\sum_{j\ne i}f_j(X_j(S))+f_i(Y_i(S)) &&(i\in S),\\
C_i(S)&=A(W-W_S)+\sum_{j\ne i}f_j(Y_j(S))+f_i(X_i(S)) &&(i\notin S).
\end{aligned}
\]

For the heavy player's deviation the new cost is `Σ_j f_j(h+Y_j(S))`. For a light player's deviation, substitute `S △ {i}` in its appropriate formula. These formulas cover all 2^m complement classes and are a reusable exact interface. Terms with zero load are evaluated only when their player actually uses that resource; the displayed sum for a light player always has its own positive weight on every charged term.

### Remaining general proof obligation

To prove a growing lower bound L(d), specify m(d), all weights, and all latency coefficients/exponents. Then prove for **every** S⊆{1,...,m} either the heavy deviation or some light deviation satisfies `C_i(S)≥L(d) C_i(S△{i})` (using the heavy formula when i=0). The finite existence of a selected improvement cycle and the mere availability of growing support do not satisfy this obligation.

## WC-R1-SIGNED-COLUMNS-4 v1: finite exact degree-four certificate

Take weights (27,9,3,1). The four latency pairs are:

| Mask | Latency |
|---|---|
| (0,1,1,1) | 251(t/13)^4 |
| (1,2,1,1) | 365t/40 |
| (1,1,2,1) | 194(t/40)^4 |
| (1,1,1,2) | 191(t/40)^4 |

All coefficients are nonnegative rationals and all weights positive. The complete profile space has 16 states. Complement symmetry reduces the following proof table to eight representatives; player labels are 0,1,2,3 in weight order.

| State | Improving player | Current cost / deviation cost |
|---|---:|---:|
| 0000 | 3 | 49419310365425/20639097173504 |
| 0001 | 2 | 47306277973504/21656734257025 |
| 0010 | 3 | 39292710438656/19061736634145 |
| 0011 | 0 | 1437492305/1208353264 |
| 0100 | 3 | 30312152133104/12288983226545 |
| 0101 | 2 | 31268459066545/25622089551136 |
| 0110 | 3 | 29959367204225/24429345633056 |
| 0111 | 1 | 6077048724448/5133066349015 |

Every entry is at least

\[
L_4=\frac{6077048724448}{5133066349015}>\frac{59}{50}=1.18.
\]

The table and its complemented profiles prove that this game has no α-PNE for every α<L_4. The full exact enumeration also confirms each row is that state's maximum deviation ratio; therefore L_4 is the instance's exact best equilibrium factor. The endpoint itself is attained at 0111 and its complement.

This is a finite degree-four result, hence also a constant lower bound for degree-at-most d≥4. It is not an asymptotic improvement over the existing Ω(√d/log d) bound. The original primary source's displayed optimization (3) reports approximately 1.153 at d=4; the stronger finite number here is only a comparison against that specific construction, pending comprehensive literature review.

## Screening and exact-validation boundary

`search_layers.py` uses SciPy/HiGHS mixed-integer optimization for fixed n, weights, selected exponents, and target α. Coefficients lie on a normalized nonnegative simplex. Binary selectors require at least one chosen witness per complement class; the objective maximizes an additive inequality margin. This is a floating search, not a proof of infeasibility or optimality in the exact cone.

The first saved batch is in `screening.json`. Five positive outputs survive rationalization and exact all-state recomputation, including the rounded four-player example above. A sixth output, n=5, q=4/5, degree 32, target 1.3, reported margin approximately 1.4×10^−6 but fails exact evaluation (and even direct floating evaluation) with a minimum best ratio below one. It is a numerical false witness and must not be promoted. A zero margin also does not prove exact impossibility.

`verify.py` uses only Python's `Fraction`, reconstructs both resources of every pair, evaluates all states and every unilateral deviation, checks the support potential inequality at every move, and emits `verification.json`. To reproduce from the repository root:

```
python tests/audits/weighted_congestion/signed_columns/verify.py
```

The exact finite certificates require no SciPy. Screening requires the primary runtime's NumPy and SciPy and is reproducible with the command-line flags in `search_layers.py`; solver time limits and floating tolerances prevent interpreting its status as exact mathematical proof.

## Source and review boundary

Primary source inspected: Christodoulou et al., arXiv:2002.07466v3, §3, Theorem 1 and equation (3), https://arxiv.org/html/2002.07466v3#S3 (2026-10-14). The source reports the finite-d values for its own gadget and proves its growing lower bound. The full-support signed-column family and the certificates here were generated in this session from the parent-supplied triad; no independent literature novelty assessment has been completed. The initial triad was supplied by the parent, and its source discovery is credited there.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
