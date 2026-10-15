# A precise scaling interface for the fourteen-resource construction

Authoring date: 2026-10-14 UTC. This is a separate derivation from the degree-32 audit. Its limiting table, general witness cone, strict endpoint, rational interval construction and uniform transport have now been independently reconstructed and attacked in `../limit_review/review.md`. External review and priority remain unverified. The calculations in `verify_limit.py` are exact evidence within their stated finite scope.

## Objects, parameters, and claim identities

Keep the seven mask representatives and their complementary resources from `README.md`. For every integer `m>=1`, put

`D_m=32m^2`, and `w(m)=(1,1/(10m),1/(20m),1/(50m))`.

Choose any fixed positive rational amplitude vector

`t=(a,b,c,d,e,f,g)`.

For the first six pairs use `c_e(x)=t_j*(x/T_j(m))^D_m`; for the last pair use `c_e(x)=g*(x/T_j(m))^2`. Here `T_j(m)` is the sum of weights of the players supported by its mask. Every instance is a finite four-player game in `G_{D_m}`; all coefficients are nonnegative rationals and all weights are positive. The strategy sets do not change with `m`.

There are three separate statements:

1. **WCF-R3-SCALED-ORIGINAL-v1.** With the original amplitudes `(127,231,145,139,28,41,289)`, the best equilibrium factors tend to `65/34`. For every real `alpha` with `1<=alpha<65/34`, there exists an integer `M(alpha)` such that for every integer `m>=M(alpha)` and every pure state there exists a unilateral deviation with current cost strictly greater than `alpha` times its resulting cost. Additionally, the exact checks for `m=1,...,12` and the uniform bound for `m>=13` prove the specific `9/5` obstruction for every integer `m>=1`.
2. **WCF-R3-SCALED-RETUNED-v1.** With amplitudes `(49/100,11/10,49/100,3/5,1/50,3/100,1)`, the limiting best factor is `100/49>2`. There is an explicit strict `2` obstruction for every integer `m>=52`. Separately, exact complete enumeration at `m=3`, degree `288`, already proves no `2`-PNE, with best factor approximately `2.0131229640941752`. The uniform proof does not assert anything about `4<=m<=51`; those degrees are unnecessary for its quantified conclusion.
3. **WCF-R3-SCALED-TEMPLATE-v1.** Let `r` be the unique real root greater than 2 of `r^3-r^2-2r-1=0`. For every real `alpha` with `1<=alpha<r`, there exist fixed positive rational amplitudes and an explicit integer threshold `M` such that for every integer `m>=M`, every pure state of this family has a strict alpha-improving unilateral deviation. The supremum `r` describes feasibility of the particular prescribed witness-player template below. No optimality claim is made about the whole seven-pair topology, other witness assignments, or general four-player games.

**WCF-R3-SCALED-RETUNED-v2** separately strengthens v1: with exactly the same retuned amplitudes, every integer `m>=20` has no `2`-PNE; the degree-288 `m=3` certificate remains valid. Versions v1 and v2 do not assert an obstruction at `m=1,2`, which are refuted by exact equilibrium certificates. No conclusion is asserted about every `4<=m<=19`. The smaller uniform threshold follows from the directional error estimate and exact positive margin `2735869393/1048576000000` in the independent review. Thus v1 remains a proved subcase rather than silently changing its quantifier domain.

None of these claims grows without bound in degree. The known fixed-player upper bound precludes using this four-player interface for an unbounded lower bound. In particular these claims do not improve the known growing asymptotic lower-bound baseline recorded in `LITERATURE.md`, and they do not close `WC-TARGET v1`. Priority and possible usefulness as a small-instance mechanism remain unaudited.

## Literal limiting costs

For a first-six resource, all supported players using it gives `x=T` and exactly latency `t`. If at least one supported player is absent, the missing load is at least `1/(50m)`, its capacity is at most `117/100`, and hence

`(x/T)^D_m <= exp(-64m/117) -> 0`.

The last pair supports all players. If player 1 of weight 1 uses the resource, `x/T -> 1` and the quadratic latency tends to `g`. If that player does not use it, `x/T -> 0` and the latency tends to zero. Thus the limiting first-six fee is `t` precisely at full support, whereas the limiting quadratic fee is `g` precisely when its users include player 1.

These limits only define a convenient finite cost table. They are not asserted to be an additional polynomial congestion game in the target class. Every game used for nonexistence is a finite, positive-weight, finite-degree member of the class before taking a limit.

Write `h=d+e+f`. Direct evaluation gives the following costs. Complementing all state bits preserves every player's cost vector, so the other eight states duplicate these rows.

| State | Player 1 | Player 2 | Player 3 | Player 4 |
| --- | --- | --- | --- | --- |
| 0000 | d+g | a+d | g | a+g |
| 0001 | d+g | b+d | b+g | b |
| 0010 | d+e+g | a+d+e | e | a+g |
| 0011 | c+h+g | h | c+e+f | c+f |
| 0100 | g | g | g | g |
| 0101 | g | a+g | g | a |
| 0110 | g | b+g | b | b+g |
| 0111 | c+g | a+g | c | a+c |

All entries are strictly positive because every amplitude is positive. All limiting deviation costs are consequently positive as well: a deviation reaches another state in this same table. There is no `0/0` limit. With a finite number of states and players, continuity of division at these positive denominators, and continuity of finite maxima and minima, imply convergence of the exact instance factor to the corresponding factor of this table.

## The prescribed witness template

Select the following deviation for each state representative, and the same player for its complementary state. The target is always that player's opposite action.

| State | Witness player | Current limiting cost A | Deviation limiting cost B | Strict requirement |
| --- | ---: | --- | --- | --- |
| 0000 | 3 | g | e | g>alpha e |
| 0001 | 3 | b+g | c+e+f | b+g>alpha(c+e+f) |
| 0010 | 4 | a+g | c+f | a+g>alpha(c+f) |
| 0011 | 1 | c+h+g | g | c+h+g>alpha g |
| 0100 | 4 | g | a | g>alpha a |
| 0101 | 3 | g | c | g>alpha c |
| 0110 | 4 | b+g | a+c | b+g>alpha(a+c) |
| 0111 | 2 | a+g | h | a+g>alpha h |

The eight inequalities are jointly sufficient for a strict alpha obstruction at every state in the limiting table. Since the table is finite, they give the positive margin

`delta = min_eight_rows (A-alpha B) > 0`.

### Exact coefficients for every alpha below r

Normalize `g=1`. For `1<=alpha<r`, choose a rational `q` in the open interval

`max(0,(alpha^2-alpha-1)/(alpha+1)) < q < 1/alpha`.

This interval is nonempty. For a positive lower endpoint, the necessary comparison of endpoints is precisely `alpha^3-alpha^2-2alpha-1<0`; if the lower endpoint is nonpositive the interval is plainly nonempty. The polynomial is negative on `[1,r)` and has exactly one root greater than 2: its derivative is positive for all real `x>=2`, its value at 2 is -1, and its value at 3 is 11. Its derivative has only one positive zero below 2, where the polynomial has a negative minimum, which also establishes negativity on `[1,2]`.

Set `a=c=q`. Choose a positive rational `h` in

`max(0,alpha-1-q) < h < (q+1)/alpha`.

This interval is nonempty by the defining lower bound on `q`. Choose positive rationals `e,f` small enough that

`e+f<h`, `e<1/alpha`, and `f<(q+1)/alpha-q`.

All right hand bounds are positive. In particular the last is at least `1/alpha^2>0` when `q<1/alpha` and `alpha>=1` (strictly larger if `alpha>1`). Put `d=h-e-f>0`. Finally choose a positive rational `b` larger than

`max(0,alpha(q+e+f)-1,2alpha q-1)`.

Density of the rationals guarantees every listed choice, even for real irrational alpha. Substitution verifies all eight strict witness inequalities: the two `b` conditions cover states `0001` and `0110`; the `f` condition covers `0010`; the lower bound on `h` covers `0011`; the upper bound on `h` covers `0111`; the upper bound on `q` covers `0100` and `0101`; and the upper bound on `e` covers `0000`. All amplitudes are fixed after alpha is chosen; they do not vary with `m`.

Conversely, if these same eight prescribed inequalities hold after normalizing `g=1`, then

`a<1/alpha`, `c<1/alpha`, `h<(a+1)/alpha`, and `c+h>alpha-1`.

Therefore

`alpha-1 < c+(a+1)/alpha < 2/alpha+1/alpha^2`,

which implies `alpha^3-alpha^2-2alpha-1<0`. Thus this prescribed witness template cannot realize `alpha>=r`. The argument has no implication for different player witnesses or other games. Equality at `r` is not attained by this strict template.

## Uniform finite-degree transfer with an explicit threshold

Let `S=a+b+c+d+e+f`. At any pure state, any player's cost in the finite game differs from its limiting table entry by at most

`E_m = S exp(-64m/117) + 17g/(50m)`.

For the first six pairs, each player uses at most one of the two resources of a pair. Full-support fees agree exactly with the limit; every other fee is bounded by `t_j exp(-64m/117)`, as proved above. Summing those fees bounds their total difference by the first term.

For the quadratic pair, when player 1 uses the resource,

`1-(x/T)^2 <= 2(T-x)/T <= 17/(50m)`.

When player 1 does not use it, `x<=17/(100m)` and `T>=1`, so its fee is at most `289g/(10000m^2) <= 17g/(50m)` for `m>=1`. These two cases prove the second term. This is a uniform bound over all states, players, and therefore all deviation costs.

For a prescribed witness with positive limiting margin at least delta, its finite strict margin is at least

`delta-(1+alpha)E_m`.

Any integer `M` strictly larger than

`max(1,34g(1+alpha)/(50delta),(117/64) log(2S(1+alpha)/delta))`

ensures each summand of `E_m` is smaller than `delta/(2(1+alpha))` for every `m>=M`. For example, one plus the ceiling of this maximum is an explicit admissible integer threshold. Hence every such finite game has a strict alpha-improving deviation at every pure state. This proves the full quantifier order

`for every alpha in [1,r), there exist fixed rational t>0 and integer M, such that for every integer m>=M, for every state s, there exists a player i with C_i(s)>alpha C_i(flip_i(s))`.

### Two rational threshold certificates

The code also verifies completely rational bounds without floating point logarithms. Since `exp(1)>8/3`, put `K=floor(64M/117)`. Then for all `m>=M`,

`E_m < S(3/8)^K + 17g/(50M)`.

For the original coefficients and alpha `9/5`, the eight limiting margins have minimum `delta=28`. At `M=13`, `K=7`, and the rational comparison

`28-(14/5)*(711*(3/8)^7+4913/650)>0`

proves the uniform strict obstruction for every `m>=13`. The second summand equals `17*289/(50*13)`. Together with exact all-state checks for `m=1,...,12`, this proves the specific original-coefficient `9/5` obstruction for all positive integer `m`.

For the retuned coefficients and alpha `2`, `S=273/100`, `g=1`, and `delta=1/50`. At `M=52`, `K=28`, the rational comparison

`1/50-3*((273/100)*(3/8)^28+17/2600)>0`

proves the uniform strict obstruction for every `m>=52`.

## Limiting factors and frontier interpretation

For the original coefficients, the complete limiting table has best equilibrium factor `65/34`, attained at `0110` and `1001`. For the retuned coefficients it is `100/49`, attained at `0100`, `0101`, `1010`, and `1011`. `verify_limit.py` checks all states and deviations exactly, rather than only the prescribed witnesses. The decimal root `r` is approximately `2.147899035704787`, but its polynomial and interval above define it exactly.

Embedding games of degree `D_m` into every class `G_d` with `d>=D_m` and choosing `m=floor(sqrt(d/32))` transfers each constant strict obstruction to all sufficiently large degree bounds. Thus the template proves the mathematical implication `liminf_{d->infinity} a_*(d) >= r`. This is a bounded constant consequence and is weaker than the growing lower bound already recorded in the project. It is neither a novelty claim nor an asymptotic frontier improvement.

## Evidence, review obligations, and reproduction

Run `python tests/audits/weighted_congestion/crossover/verify_limit.py`. Its default mode recomputes and compares `limit_evidence` without changing frozen data. `--generate NEW_DIRECTORY` writes new evidence only to a directory that does not yet exist. The four evidence files contain the complete rational limiting tables, finite scans for their stated parameter values, the degree-288 all-state `2`-obstruction certificate, and exact rational uniform error comparisons.

The general convergence argument and rational coefficient interval construction are mathematical proofs written here; they are not inferred from the finite scans. [Independent second review](../../../reviews/weighted_congestion/crossover_limit_review/review.md) reconstructed the limiting resource rules first, then checked the complete table, the eight costs, the normalization, the strict endpoint exclusion, and the uniform error bound. It corrected two a/c labels in its own preliminary general-amplitude message and found no mathematical error in the author's correctly labeled table. External peer review, priority search, broader witness optimization, and any bridge to a player-count-growing construction remain open.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
