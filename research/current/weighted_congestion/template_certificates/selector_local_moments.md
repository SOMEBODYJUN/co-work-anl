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

## 9. 异权仿射全签名成本射线的刚性

### 9.0. 新Claim精确身份

**ID/version：** `WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1`。

**Exact Statement / Objects / Domain / Quantifiers。** 对每个n≥2、每个不全相等的正实权向量w，固定每玩家两个动作标签0、1及成本表

\[
 V_i(s)=s_i\sum_{j=1}^n w_j s_j,\qquad s\in\{0,1\}^n.
\]

任何同玩家/同权/同两个动作标签、以任意有限数量资源和任意有限次数非负系数多项式费用构成、逐玩家逐状态成本恰为V的MODEL表示，必具有以下刚性：忽略零费用资源及无人使用资源后，每个资源均在且仅在每名玩家的动作1使用，费用恰为a_e x、a_e>0，且Σ_e a_e=1。特别地每个有使用者的正费用资源都具有全部n名潜在用户；不可能通过提高费用次数/增加资源，把V保真压到全部正资源支持小于n。

**Cone consequence。** 固定w及binary标签，令K_fin为所有由有限非负系数多项式资源得到的完整成本表向量之锥（每个表示可有自己的有限最高次数）。V生成K_fin的极射线：V=U+Z、U,Z∈K_fin必有U=θV、Z=(1−θ)V，0≤θ≤1。只说K_fin，不声称其闭包的极射线或暴露射线。

**Definitions / Assumptions / Scope。** 正费用表示多项式不恒为0，潜在用户是至少一个合法动作使用该资源的玩家。全部偏离按真实负载；零费资源可用于保持非空/反链/空交及标签，不计正资源支持。保持全部cost table即保持全部真实偏离成本。原V由一条费用x、人人仅动作1使用的资源实现；另添每动作私人零费marker即可成为空交反链core，故scope不依赖空策略。原游戏有全0精确PNE；这只是cost-preserving表示障碍，不是PNE不存在或全类目标结论。允许改玩家权或只保近似不等式的归约不被排除。

**Dependencies / Evidence / Status。** 直接非负费用、两人参与时真实负载、二项式及成本锥的有限非负叠加；不调用外部均衡定理。独立审查先仅由statement重构并强化到“不全等权”，再读本freeze攻击。独立重构后冻结攻击已PASS，无未结数学fatal；状态为complete structural proof; independently reconstructed and exactly audited; unrefereed。有限审计只核代数，不替一般证明。未外审、未认证新颖性。

### 9.1. 零成本动作强迫正资源的方向

每名玩家选择动作0时其成本在所有对手状态都为0。若某正费用资源被玩家i动作0使用，因为w_i>0且非负系数非零多项式在正负载上严格正，就会贡献正成本，矛盾。因此任何正费用资源只可能由各玩家的动作1使用。记其非空潜在用户集为S_e；无人用资源贡献零向量，可忽略。

令e_i为仅玩家i动作1的状态。由V有

\[
 C_i(e_i)=w_i,\qquad
 \Delta_{ij}:=C_i(e_i+e_j)-C_i(e_i)=w_j.
\]

共享资源的Δ贡献为c_e(w_i+w_j)−c_e(w_i)，没有冻结偏离后负载。

### 9.2. 一对异权排除其共同资源的高次项

选一对p,q使a=w_p>b=w_q。目标表给aΔ_pq−bΔ_qp=0。对任一共同资源c(x)=Σ_k c_k x^k，其贡献为

\[
 \sum_k c_k\{(a-b)(a+b)^k-a^{k+1}+b^{k+1}\}.
\]

k=0、1时花括号为0。k≥2时它等于

\[
 (a-b)\left[(a+b)^k-\sum_{r=0}^k a^{k-r}b^r\right]>0,
\]

因为二项式系数均≥1且某个内项系数严格>1。所有c_k≥0，故总和为0强迫每个p,q共同资源都无k≥2项，即均为A_e x+B_e、A_e,B_e≥0。

由Δ_pq=b及b>0，共同资源斜率Σ_(e:p,q∈S_e)A_e=1。它们给p在e_p的成本至少Σ A_e a=a，恰已用完其目标solo成本a。各资源费用非负，所以：这些共同资源所有B_e=0，且p不能使用任何其他正费用资源。故p全部正资源恰为这些A_e x，A_e>0且ΣA_e=1。

### 9.3. 该玩家的资源被迫包含全体，继而排除余项

固定任意j≠p。p在e_p+e_j的Δ_pj=w_j，且其全部正资源已是线性，所以

\[
 w_j=w_j\sum_{e:p,j\in S_e}A_e.
\]

因此Σ_(p,j共同)A_e=1。p的全部斜率总和就是1且逐项严格正，故每个p正资源都必须含j。任意j均成立，所以这些资源全部具有S_e=N。

它们在任意玩家i的solo状态恰贡献Σ A_e w_i=w_i，用完其目标solo成本。任何其他有使用者正资源都将对至少一个玩家增加严格正solo成本，矛盾。于是没有余下正资源，证明完整刚性。

若V=U+Z，将两表示资源并置就得到V的有限表示；按刚性，每个正资源是同一完整成本向量V的正倍，分属U、Z的斜率相加分别给θ与1−θ。故V是K_fin极射线；不需要锥闭性。

### 9.4. 不全等权假设与等权边界

等权时刚性确实可能失败。取n≥3、w_i=1，任意整数q≥1使2^q≥n。为每对玩家增加一条仅其动作1使用的资源，费用x^q/(2^q−1)；每名玩家再有只在动作1使用的私人常数资源

\[
 1-\frac{n-1}{2^q-1}\ge0.
\]

当玩家i动作1且另有m名玩家动作1时，成本恰

\[
 \frac{m2^q+(n-1-m)}{2^q-1}
 +1-\frac{n-1}{2^q-1}=1+m.
\]

动作0成本仍0，故逐状态精确保持V，却只用支持至多2的正资源。加入零费动作marker仍保core结构。n=3,q=2已经是显式小例；因此“不全等权”不是可无证删除的条件。

### 9.5. 与局部成本空间压缩的关系

有限d的cost-space维数小，不表示该正资源锥由小潜在支持的资源生成。上面原费用只有degree1，仍在非等权时刚性要求全n支持，即使表示方任意提高次数。该例有精确均衡；它不限制只保均衡/单向lift、改变权重、引入辅助玩家或非保真表示，也不给全类Cd/ln d上界或更强无均衡族。

## 10. 刚性证明的独立核验合同

本新Claim由同一[独立审查文件](../../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)新增的刚性部分单独审查，挂冻结`7a2ee0b7…`，不把先前三Claim的f454审查自动外推。审查者在读稿前独立从较弱statement重构出“不全等权/n≥2/完整极射线”强化，再攻击本稿。

运行`python3 tests/audits/weighted_congestion/template_certificates/verify_affine_full_signature.py`；[冻结结果](../../../../evidence/runs/weighted_congestion/template_certificates/affine_full_signature_rigidity.json)记录命令/Python/source hash/精度及完整输入。225个pair代数/符号、2331个有限单项式signature列的逐face消元和7160个等权边界真实成本位置全部通过。每个后续face只在先前face上核非负，不假冒它对整个cone非负。无需会话暂存文件、solver、随机性或浮点容差；一般任意有限degree/实正权证明由第9节承担。


## 11. 完整空交反链签名锥中暂态择证质量的必要性

**ID/version：** `WC-FULL-CORE-TRANSIENT-MASS-NECESSITY-v1`。本节是既有奇偶暂态构造与真实坏环路由的同时化推论，新增范围为完整proper签名锥及近d倍率，而非删列子锥；不提供任意selector的统一构造。

此处概率dual均指μ_s≥0、Σ_sμ_s=1且B_H(β)^Tμ≤0，排除零向量。B_H(β)的(s,σ,k)列为所选玩家在s的真实资源成本减β倍偏离后真实成本。proper签名对每名玩家只能是不参与、仅动作0参与、仅动作1参与；锥包含全部非空proper签名及0到d单项式次数的非负组合。

设 d≥0、α≥1，且某个 n 玩家二动作 MODEL 游戏 G（权向量 w>0、费用次数≤d）有一条非空严格 α 改善简单有向环 Q。要求 G 的每条正费用资源对每名玩家至多出现在一个动作中（即二动作 proper signature）；环无自环。令 n′=max{n,d+2}。任取 n′−n 个正附加权和一个正 flag 权，构造 n′+1 玩家二动作、全部非空 proper signatures 与次数 0,…,d 的完整列锥 K。

**定理。** 存在一个在每态都选择真实动作翻转的 selector H，满足：

1. H 唯一 recurrent cycle 是 G 原环 Q（附加玩家动作固定为0，flag动作固定为1）。
2. H 有一个完全支撑于 transient states 的概率 dual λ，且同一 λ 对该完整 K 在 β=1 以及每个 β≥1 都有 B_H(β)^Tλ≤0。
3. 在原给定 α，H 的任何 dual 都给 transient states 严格正质量；尤其不存在 recurrent-only dual。
4. 完整 K 没有任何模板共同 α-PNE，且 H 在任何倍率 β≥1 都没有点质量 dual：每态 s 的当前所选玩家动作 singleton signature 常数列在该行等于1。
5. 若 a 是原游戏 G 的列系数向量在 K 的零延拓，b(s)=(B_H(α)a)_s，η=min_{s∈Q}b(s)>0，M=max_{s∉Q}max{0,−b(s)}≥0，则每个 dual μ 都满足 μ(Transient)≥η/(η+M)>0。M=0时该界恰为1。这里 η,M 依实例，不给统一次数收益。

**接已有结果的明确推论。** WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1 的环来自二动作 proper resources。因此对每个整数 d≥2、每个 1≤α<ρ_d，存在正有理权、binary/full-proper-core selector 满足1–5。该推论仍不是全类存在上界，也不构造没有 α-PNE 的费用游戏。

**范围与价值。** 这是既有 parity transient dual 和唯一坏环路由的同时化；既有 stationary 稿§7已在删列子锥中给过 δ_empty 暂态必要，本命题的新增范围仅为完整 proper-signature cone、无共同 sink、无人为空动作、任何点质量均失败，并可到近 d 倍率。它不是一种能处理任意 selector 的构造。


### 明确构造

把原状态写成 y∈{0,1}^n。补 n′−n 个二动作玩家，补零得到嵌入环 Q′⊂{0,1}^{n′}。在 Q′ 取一个指定顶点 q。另加一个 flag 玩家 F；全部状态写成 (x,b)∈{0,1}^{n′}×{0,1}。选前 m=d+2 个 ordinary coordinates 为 active，记 p(x)=Σ_{j=1}^m x_j mod2。

* b=0,p(x)=0：翻转 ordinary 玩家1。
* b=0,p(x)=1：翻转 flag，使 b=1。
* b=1,x∈Q′：依原简单环翻转指定的原玩家。
* b=1,x∉Q′：取最小 j 满足 x_j≠q_j，翻转 j 使其等于 q_j。

最后一种有定义，因为 x=q 则已在 Q′。每条边均是恰好一名玩家的合法不同动作偏离。flag0 至多两步进入 flag1；flag1 永不返回 flag0；flag1 在首次进入 Q′ 前每步严格减少与 q 的 Hamming 距离，至多 n′ 步入环。故唯一 recurrent cycle 为 Q′×{1}。特别地 flag0 全部 transient。

### 完整锥的完全暂态 dual

固定非active普通坐标 x_j=q_j（j>m）。令 S 为 flag0、active even parity 的全部状态；其大小 2^{m−1}=2^{d+1}。令 λ 在 S 上均匀，别处0。S上 H 只选择 ordinary 玩家1；翻转1将 even active cube 双射到 odd active cube，非active与flag不变。

任取完整 proper signature σ、费用单项式次数0≤k≤d。令 f_j为各坐标动作的资源 membership predicate（可为0或一个动作的 indicator）。所选玩家1的真实资源费用在 flag0 是

    g(x)=f_1(x_1) [w_1 + w_F f_F(0) + Σ_{j≠1} w_j f_j(x_j)]^k.

指示量为0时乘积消去费用，故可把自己的权固定写在方括号内。把非active坐标固定，上式是 active binary cube 上多线性化次数≤k+1≤d+1<m的函数。对常数项 k=0 也成立；无需计算成本比或0/0。

每个次数<m单项式都遗漏一名 active 坐标。按该坐标取0/1配对，完整cube的 signed parity sum为0。因此 Σ_even g=Σ_odd g。翻转1双射即给该列 (B_H(1)^Tλ)_(σ,k)=0。由于偏离后真实资源费用非负，β≥1时 B_H(β)=B_H(1)−(β−1)Arrival，故同一 λ 逐列≤0。证明甚至允许每名玩家同时两动作使用该资源的完整签名；但主命题只需 proper cone。

全proper模板可把每个signature保留成零费用资源，并含每动作的 singleton signature，故人人两个策略都非空、互不包含、空交，标签不会合并。λ构造无需空策略、固定玩家或共同零成本动作。

### Recurrent 支撑被原游戏分离

把原游戏的全部正资源和系数 a 延拓：附加 ordinary 玩家、flag不使用旧资源。它们的任一动作可用私人零费用 marker 区分。环 Q′×{1} 的真实旧/新成本逐项与 G 原环相同，所以 b(s)=(B_H(α)a)_s>0于全部recurrent states。

若 μ 是完整锥的概率dual而只支撑Q′×{1}，则

    0 < Σ_s μ_s b(s) = a·B_H(α)^Tμ ≤0,

矛盾。这里仅用 a≥0；没有把有限计算当作一般证明。

对任意dual μ，令 t=μ(Transient)，η=min_Q b>0，M=max_Transient(−b)_+。则

    0 ≥ E_μ b ≥ η(1−t)−Mt,

给 t≥η/(η+M)>0。这里一般界只需 M≥0；若恰有 M=0，则界强迫t=1，完全允许。η>0保证分母严格正，不需要除任何玩家成本。

### 无点质量dual和无共同均衡

对任意态s，令i为H当前所选玩家。取只由玩家i当前动作使用、其他玩家不用的singleton signature，费用为1。其B_H(β)行值恰为1−β·0=1。所以δ_s不是任意β≥1的dual。

同一singleton资源游戏中，s的玩家i从成本1偏离到0，因此s不是任何有限β-PNE。由于每态都能单独这样选择一个允许费用游戏，模板不存在被所有费用游戏共享的PNE状态。它不说明这些游戏没有各自的PNE。



### 11.1. 近d推论的binary域与无共同均衡的量词

应用循环窗口定理时，先取其第3–4节构造中的两个互补动作，删去其后为原方法障碍添加的全部2^E策略；严格环仍在，每名玩家的资源proper性仍保持。必要时从严格闭walk中抽取简单有向环，再应用本节。不得把原全文的2^E输入直接称作binary。新增零费用signature资源区分动作，MODEL允许费用为零。

“没有模板共同均衡”的准确量词为¬∃s∀a≥0：s是费用a游戏的α-PNE；不是∃a≥0∀s：s非α-PNE。singleton列依s变化，不能交换量词。每个具体游戏仍可能有均衡；本节不构造无均衡增长族。

### 11.2. 独立攻击与有理重现

独立审查先仅接收statement，自主重构parity层、flag路由和质量分离，再攻击冻结statement c55819d7与proof c2cde533；见[同一local-moment审查稿新增部分](../../../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。内部未发现本范围内fatal。Status：complete interface corollary; independently reconstructed and exactly audited; unrefereed。Value为完整锥下暂态必要性的范围闭合，Mechanism为低阶奇偶抵消加唯一真实坏环，Novelty未认证，Ambition全类OPEN。

运行`python3 tests/audits/weighted_congestion/template_certificates/verify_transient_core_implant.py`及`python3 tests/audits/weighted_congestion/template_certificates/independent_transient_core_implant.py`。默认stdout，`--output NEW_PATH`独占创建。冻结结果为`evidence/runs/weighted_congestion/template_certificates/transient_core_implant.json`及`evidence/runs/weighted_congestion/template_certificates/independent_transient_core_implant.json`。作者审计从literal重建二次、三次两fixture的所有proper及全部签名列；独立审计使用不同附加权，重建二次例所有726列并核验超次数一列不再抵消。代码、参数、次数、Python与hash记录在各JSON；任意d及任意给定坏环的证明由本节承担，有限检查不替一般证明。
