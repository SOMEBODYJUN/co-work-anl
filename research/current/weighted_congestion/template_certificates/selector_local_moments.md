# 有限次局部矩、全成本压缩与暂态择证对偶

本稿三个独立Claim提供精确表示，不完成全类匹配上界。

## Exact scope and status

The model is the repository's `MODEL.md`: finite positive player weights,
nonnegative-coefficient polynomial resource costs of degree at most `d`, and
unweighted player costs. Each player has finitely many labelled actions; every
deviation below recomputes its true load. The labels can always be distinguished
by zero-cost singleton-signature resources.

The three registered claims are:

1. **WC-DEGREE-LOCAL-COST-COMPRESSION-v1.** For fixed action counts `m_i`, weights,
   and degree `d`, let

   `D = sum_i m_i sum_{T subset N\{i}, |T|<=d} product_{j in T}(m_j-1)`.

   Every model game has a labelled-action cost-equivalent representation with at
   most `D` positive-coefficient monomial resource types, plus at most
   `M=sum_i m_i` zero-cost singleton-signature resources. In particular all player
   costs at all states and all actual deviations are preserved, not merely a
   selected set of margins. If the original game is an empty-intersection
   antichain core, the representation can be chosen to remain such a core.

2. **WC-SELECTOR-LOCAL-MOMENT-INTERFACE-v1.** Every degree-`d` selector dual is
   exactly an intersection of a selector-dependent convex hull in `R^D` with a
   resource-cone polar. The hull coordinates are signed, discounted moments of
   the selected action transition and at most `d` other players' actions. Any
   existing dual has another dual supported on at most `D+1` states. Transient
   states are unrestricted. For binary actions and a dual supported only on
   states where one specified player is selected and flips, existence at
   `alpha=1` is equivalent to equality of all degree-at-most-`d` context moments
   of its two movement directions, and to failure of strict polynomial
   separation of the two labelled context sets at degree `d`.

3. **WC-TRANSIENT-PARITY-SELECTOR-DUAL-v1.** For every `d>=0` and every positive
   weight vector of length `d+3`, there is a binary-action selector with no
   self-loop and a unique two-cycle, for which a probability distribution
   supported entirely on transient states is a dual at `alpha=1` for all
   complete-signature resource columns of degrees `0,...,d`. The same
   distribution is a dual for every `alpha>=1`. This remains true after
   restricting columns to empty-intersection core signatures.

**Dependencies:** finite categorical polynomial expansions, elementary conic
Caratheodory elimination and ordinary convex Caratheodory elimination (both
proved below), the finite-action selector alternative already in the repository.
The core lift is the repository's existing normal-form result; no new use of an
external equilibrium theorem occurs.

**Status:** complete structural proof; independently reconstructed and exactly audited; unrefereed. The independent reviewer first reconstructed the precise cost-space and support statements, then attacked the fixed proof hash. All three results are representation/mechanism
results. None yields a uniform `C,d0`, bounds all template sizes, or establishes
a growing nonexistence family. An audit is not substituted for a general proof.

## 1. Proper signatures exactly describe the core resource cone

Write the action set of player `i` as `A_i`, with `m_i>=2`. A resource signature
is a tuple `sigma=(sigma_i)` with `sigma_i subset A_i`. In an empty-intersection
core, every `sigma_i` is proper: some action of each player omits the resource.
There are

`product_i (2^{m_i}-1) - 1`

nonempty proper signatures. These, with monomial degrees `0,...,d`, are exactly
the allowable core columns. No signature is required to involve every player.

Conversely include one resource of every proper signature, permitting zero
cost. Associate action `a` of player `i` with the resources whose `sigma_i`
contains `a`. All these actions are nonempty and incomparable: the singleton
signature `sigma_i={a}`, all other blocks empty, distinguishes `a` from every
other action in both directions. Their intersection is empty because every
resource's `i`-block is proper. Thus arbitrary nonnegative coefficients on the
proper columns give a genuine core template. This also explains why merely
deleting mandatory columns without retaining label-distinguishing zero
resources would need care.

By the existing core normal form, the universal existence problem is therefore
equivalent to the selector alternative on these proper-signature cones, with
arbitrary `n,m,w`. This is an exact scope reduction, not a size cutoff.

## 2. A resource cost is degree `d` in its user's opponents

For a signature write `f_j(a)=1_{a in sigma_j}`. A degree-`k` resource's cost to
player `i`, as a function of the state, is exactly

`g_{i,sigma,k}(s) = f_i(s_i) (w_i + sum_{j!=i} w_j f_j(s_j))^k`.       (1)

When `f_i(s_i)=1`, its own weight is included; when it is zero the product
vanishes. This is valid also for constants and unused resources.

Fix one baseline action `a_j^*` for every player. The functions

`1`, and `y_{j,b}(s_j)=1_{s_j=b}` for `b != a_j^*`

form a basis of all real functions of one action coordinate. Every `f_j` is
affine in these functions. Expanding (1), then using
`y_{j,b}^r=y_{j,b}` and `y_{j,b}y_{j,c}=0` for `b!=c`, shows that it belongs to
the space `W_i` spanned by

`1_{s_i=a} product_{j in T} 1_{s_j=u_j}`,

where `a in A_i`, `T subset N\{i}`, `|T|<=d`, and every
`u_j != a_j^*`. These tensor-product basis functions are linearly independent.
Hence

`dim W_i = m_i sum_{T subset N\{i}, |T|<=d} product_{j in T}(m_j-1)`.

The full vector of all player cost tables lies in the direct sum
`W=direct_sum_i W_i`, of dimension `D`. In particular for binary actions,

`D = 2n sum_{r=0}^{min(d,n-1)} binom(n-1,r) = O_d(n^{d+1})`.          (2)

More generally, if `M=sum_i m_i`, the elementary-symmetric-sum bound gives
`D <= M sum_{r=0}^{min(d,n-1)} (M-n)^r/r! = O_d(M^{d+1})`.

For fixed degree this replaces an exponential-in-action-count ambient cost
space by a polynomial-dimensional space. If `d>=n-1`, the bound is simply
`D=n product_i m_i`, the complete player-cost-table dimension.

### Cost-preserving conic compression

Let `v_(sigma,k) in W` be the full player-cost-table vector of a unit monomial
resource. Splitting resource polynomials and merging identical signatures
expresses any game's cost table as a nonnegative combination of finitely many
such vectors. If more than `D` positive coefficients occur, these vectors are
linearly dependent. Choose a nonzero relation `sum_l beta_l v_l=0` with at least
one `beta_l>0`, and replace positive coefficients `a_l` by

`a_l - t beta_l`, where `t=min_{beta_l>0} a_l/beta_l`.

All remain nonnegative, at least one becomes zero, and the complete cost table
does not change. Repeat until at most `D` positive terms remain. This proves
the asserted conic bound without any approximate calculation. Each remaining
term is a legal resource with its selected signature and monomial coefficient.

Sparse selection might identify action resource subsets. Add at most `M`
distinct zero-cost singleton-signature resources to preserve all action labels.
These leave every cost table unchanged. In the core case the selected original
signatures and all these added singleton signatures are proper, so every
player still has nonempty incomparable actions with empty total intersection.
This claim does not assert unit coefficients or preserve original resources.

## 3. The exact selector marginal polytope

Fix a selector `h(s)=(i(s),t_i(s))`, permitting current-action choices. The
functional on a cost table `C in W` is

`L_(h,s)(C) = C_i(s) - alpha C_i(t_i,s_-i)`.

In the basis of section 2 its coordinate vector is

`Psi_h(s)[i,a,T,u]`
` = 1_{i(s)=i} [1_{s_i=a} - alpha 1_{t_i(s)=a}] product_{j in T}1_{s_j=u_j}`.
                                                                    (3)

Thus only the chosen action edge and at most `d` opponent actions are inspected
in each coordinate. The whole selector remains present through the admissible
feature points, including features of its transient states.

Let `K` be the cone generated by coefficient vectors of all allowable resource
cost tables in `W`. For unrestricted templates use all nonempty signatures;
for the core use precisely the proper signatures of section 1. Denote the
negative polar by `K^-={z: z dot v<=0 for every v in K}`. The selector dual is
exactly

`conv{Psi_h(s): s in Omega} intersect K^- != empty`.                   (4)

Indeed `B_h[s,(sigma,k)]=Psi_h(s) dot v_(sigma,k)`, and taking a convex
combination of rows is exactly taking a probability distribution on states.
No sign restriction on basis coefficients is claimed; `K^-` is not generally
an ordinary negative orthant in this basis.

Any convex combination in `R^D` can be reduced to at most `D+1` terms: if more
are positive, the augmented vectors `(Psi_h(s),1)` are dependent; subtract an
appropriate multiple of that relation to eliminate one term while preserving
nonnegativity, the feature vector, and total mass. Iteration proves the dual
support bound. This neither requires nor implies selector stationarity.

**Remaining general bridge.** A uniform upper bound requires (4) for *every*
selector, at `alpha=C d/log d`, uniformly in all `n,m,w`. Replacing the hull by
arbitrarily chosen locally consistent moments would be an unproved relaxation:
the selector-support marginal-polytope condition cannot be omitted. Nor does
the polynomial dimension produce a uniform bound on `n` or a finite search
cutoff. A stronger requirement that the feature vector be zero also is not
equivalent to the general polar-intersection condition.

### Equivalent nonnegative expansion

For completeness, without baseline coordinates one can expand for binary
membership variables `z_j`:

`(w_i + sum_{j!=i}w_j z_j)^k = sum_{T subset N\{i}, |T|<=k} theta_(k,i)(T) product_{j in T}z_j`,

where

`theta_(k,i)(T) = sum_{R subset T} (-1)^{|T|-|R|} (w_i+sum_{j in R}w_j)^k`.

For `|T|<=k` these coefficients are positive: the multinomial expansion sums
exactly those terms in which every `j in T` occurs at least once, with arbitrary
nonnegative exponent on `w_i`. If `|T|>k` the coefficient is zero. In
particular the selector column is

`[f_i(s_i)-alpha f_i(t_i)] sum_T theta_(k,i)(T) product_{j in T}f_j(s_j)`. (5)

This expresses the exact resource test as weighted low-order rectangle
moments. Imposing each rectangle term's inequality individually would be a
stronger, unjustified restriction.

## 4. One selected binary player: threshold-degree duality

Fix one binary player `i`. Let `S_i` consist of states where `h` selects `i`
and flips its action. Consider only probability distributions supported on
`S_i`. Split their context measures on `Omega_-i` into `mu_0,mu_1`, according
to the current action of `i`.

At `alpha=1`, use signatures that include player `i` only at action 0, or only
at action 1, with all other blocks unchanged. Their selector-column functions
are negatives of each other, so any dual must give both expectation zero.
Consequently the exact conditions are

`integral (w_i+sum_{j!=i}w_j f_j(s_j))^k d mu_0`
` = integral (w_i+sum_{j!=i}w_j f_j(s_j))^k d mu_1`                   (6)

for all membership predicates and all `0<=k<=d`. They are also sufficient:
signatures containing `i` at both actions give zero at `alpha=1`; signatures
omitting `i` give zero. Proper core signatures need only the two one-action
choices, so the same equivalence holds in the core.

The tests in (6) span every context polynomial of categorical degree at most
`d`. One direct proof uses a product `product_{j in T}1_{s_j=u_j}` with
`|T|=r<=d`: expand
`(w_i+sum_{j in T}w_j 1_{s_j=u_j})^r`; its coefficient on the full product is
`r! product_{j in T}w_j>0`, and every remaining term is a product on a proper
subset. Induction, starting with the constant resource, isolates the desired
product. Thus (6) is exactly equality of all context moments up to degree `d`.

Let `V_d(x)` be the vector of these basis moments at a context `x`, including
the constant. Write `X_a={s_-i: s in S_i, s_i=a}`. A nonzero such dual exists
iff

`conv V_d(X_0) intersect conv V_d(X_1) != empty`.                       (7)

The total mass of each direction is `1/2` by the constant test. This includes
the case where the same context belongs to both sets, giving a two-cycle.

If both sets are nonempty and their compact convex hulls are disjoint, their
closest-point separating hyperplane gives a degree-at-most-`d` polynomial
strictly positive on `X_0` and strictly negative on `X_1` (subtract the midpoint
threshold; constants are available). Conversely any such polynomial precludes
(7). If one set is empty, a signed constant supplies the separating polynomial
and no probability dual exists. This proves the threshold-degree equivalence.

For `alpha>1`, the exact one-player criterion is the multiplicative sandwich

`integral g d mu_0 <= alpha integral g d mu_1`,
`integral g d mu_1 <= alpha integral g d mu_0`,                         (8)

for every nonnegative primitive test
`g=(w_i+sum_{j!=i}w_j f_j(s_j))^k`. Equality of ordinary moments is sufficient
but need not be necessary. Passing from (8) to all signed polynomials would
lose the nonnegative resource cone and is not justified.

This is a sufficient submechanism for the complete dual, not a theorem that
every selector has a single-mover-supported certificate. The general interface retains cross-player compensation; no one-mover-supported certificate is guaranteed for an arbitrary selector.

## 5. Explicit entirely transient duals at every degree

Put `m=d+2`. There are active binary coordinates `1,...,m` and a flag player
`F=m+1`, all of arbitrary positive weights. Write a state as `(x,b)` with
`x in {0,1}^m` and flag `b in {0,1}`. Let `par(x)=sum_j x_j mod 2`.

Define a selector, always flipping one genuine action:

* If `b=0` and `par(x)=0`, flip player 1.
* If `b=0` and `par(x)=1`, flip the flag to 1.
* If `b=1` and some `j>=2` has `x_j=1`, clear the least such coordinate.
* If `b=1` and all `x_j=0` for `j>=2`, flip player 1.

On flag 1, the number of 1s among coordinates `2,...,m` strictly decreases
until reaching the unique two-cycle

`q=(0,...,0;1) <-> q'=(1,0,...,0;1)`.

Every flag-0 state enters flag 1 in one or two steps; flag 1 never returns to
flag 0. Thus all flag-0 states are transient, this two-cycle is unique, and
there are no self-loops.

Let `lambda` be uniform on

`S={(x,0): par(x)=0}`,

which has size `2^{m-1}`. Only player 1 is selected on this support. Flipping
player 1 maps its even `x` bijectively to all odd `x`. For any resource column
define its player-1 cost function at flag 0 by

`g(x)= f_1(x_1) (w_1 + w_F f_F(0) + sum_{j=2}^m w_j f_j(x_j))^k`.

As a multilinear polynomial in active binary coordinates, `g` has degree at
most `k+1<=d+1<m`. (Each unary binary predicate is affine.) Therefore

`sum_{par(x)=0}g(x) - sum_{par(x)=1}g(x)=0`:                          (9)

each monomial misses some active coordinate, whose two choices cancel in the
alternating sum. Equation (9) is precisely the unnormalised column product
`B_h(1)^T lambda`. It vanishes for every signature, all weights, and every
`0<=k<=d`. In particular it vanishes for all proper core signatures. For
`alpha>=1` the column product only subtracts `(alpha-1)` times a nonnegative
expected arrival cost, hence is nonpositive.

The complete proper-signature resource template of section 1 realizes two
nonempty incomparable empty-intersection strategies for each player, so this
construction does not obtain its transient support from empty strategies,
mandatory resources, fixed players, or self-moves. The selector is not asserted
to be everywhere improving for any game; its dual proves precisely the
opposite for the tested degree cone.

Its unique two-cycle also has a dual: both edges move player 1 at the same
opponent context, so equal mass cancels all its resource costs at `alpha=1`.
Thus this family does **not** establish that transient mass is necessary, that
it improves the best multiplier, or that it solves a selector that recurrent
certificates cannot solve. Its exact claim is feasibility of entirely transient
certificates and the moment-cancellation mechanism alone.

## 6. Consequences and unresolved obligation

The substantive general interface is a polynomial cost-space replacement for
the exponential signature ambient space at fixed degree. The parity family
illustrates that high-order correlations can cancel its resource tests even
when the chosen certificate support is transient; as just noted, that example
does not separate transient from recurrent certificate power.

For an arbitrary selector, there is still no proof that its low-order
transition-moment hull intersects the weighted resource polar at
`C d/log d`. The single-mover threshold-degree criterion need not hold for any
one player, and sparse support is a representation bound rather than a
construction of a feasible certificate. These are the exact remaining
obligations; the main acceptance target remains open.

## 7. Audit

`tests/audits/weighted_congestion/template_certificates/verify_selector_local_moments.py` uses only Python
standard-library exact integers/Fractions. It checks direct resource loads,
the Möbius expansion, the graph and transient support, all core signatures for
`d=0,...,4`, and all full signatures for `d=0,...,3`. It also checks exact
column-space ranks and positive conic compression on specified small fixtures.
The frozen JSON states actual coverage, interpreter, and source hashes.

The audit has no mathematical role in the arbitrary-weight, arbitrary-degree
proofs. In particular its finite ranges must not be reported as evidence for
the missing uniform existence theorem.

## 8. 精确身份字段、独立审查与规范运行

- **中文数学名称：** WC-DEGREE-LOCAL-COST-COMPRESSION-v1为“有限次局部成本空间与全成本资源压缩”；WC-SELECTOR-LOCAL-MOMENT-INTERFACE-v1为“全状态择证的低阶矩极锥与小支撑接口”；WC-TRANSIENT-PARITY-SELECTOR-DUAL-v1为“完全暂态奇偶支撑的择证对偶”。
- **Objects / Domain / Quantifiers / Assumptions / Definitions：** 前两Claim对每个有限n≥1、整数d≥0、m_i≥1、正实权向量和合法MODEL费用/策略；selector接口另固定任意实α≥1。core部分明确人人m_i≥2且策略空交反链；第三Claim对每个d≥0和每个d+3维正实权向量。所有成本均按真实偏离负载，非负系数、零费/空策略及singleton动作都依第1–5节的分别范围处理，不计算0/0。
- **Dependencies / Scope / Conclusion：** 依赖MODEL、有限动作签名/严格替代、局部张量展开、正文自足两种Caratheodory消元及空交core接口。保持全state/deviation成本与标签，不保持旧资源身份、单位系数或均衡算法效率；所有n/m/w无界时仍没有统一C,d0。parity只证明暂态dual可行，唯一二循环本身亦有dual，不证明暂态必要。
- **Evidence / Objections / Status：** [独立先重构后固定版本攻击](../../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)审查三个Claim及one-mover门槛接口，无未结数学fatal；本稿scope为表示/机制，未外审，Novelty未认证。freeze原位变动已在审查中逐项记录并以实际f4541469固定副本校正；不把早先误报hash挂到所审版本。
- **作者运行：** `python3 tests/audits/weighted_congestion/template_certificates/verify_selector_local_moments.py`；冻结结果`evidence/runs/weighted_congestion/template_certificates/selector_local_moments.json`。34776个有限parity列、Mobius公式及3个成本锥压缩fixture；无随机性、solver或浮点容差。
- **独立运行：** `python3 tests/audits/weighted_congestion/template_certificates/independent_selector_local_moments.py`；冻结结果`evidence/runs/weighted_congestion/template_certificates/independent_selector_local_moments.json`。7组压缩/标签/core边界，1730高阶差分、两组dual支持压缩逐1023列保全部期望、6组one-mover span。完整输入在各源码；命令/Python/hash/精度在冻结记录。

两份程序均只向stdout输出JSON，运行者可另存新路径；不依赖会话暂存正文路径、不原位重写已冻结run。一般实参数与任意degree的结论由解析证明承担，有限审计不承担全类增长界。
