# 有限次局部矩、全成本压缩与暂态择证对偶

本稿保留局部矩、成本压缩与暂态择证的三个原始Claim；异权成本刚性和奇环补偿另有独立身份。均不完成全类匹配上界。

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

## 11. 奇环缺陷择证的无界移动者支撑与补偿阈值

**ID/version：`WC-SELECTOR-UNBOUNDED-MOVER-SUPPORT-v1`。** 中文数学名称：奇环缺陷择证的无界跨玩家补偿与锐支撑门槛。完整证明与内部独立重构、冻结攻击分开记录；不是全类存在或非存在结论。

### 11.1. 精确身份

固定任意奇数 n≥3、整数 d≥1。任意共同正权u均适用；各degree-k列除以正数u^k归一化，以下取u=1。取 n 名权重均为1、动作标签均为0和1的玩家，状态空间 Ω={0,1}^n。考虑所有非空完整动作关联签名和次数 k=0,…,d 的矩阵 B_h(α)；也可只保留每个玩家块均为真子集的非空 proper/core 签名。

圈下标以 Z/nZ 计，程序以0,…,n−1计。对每个状态 s，任选一个下标 i 满足 s_i=s_(i+1)，令 h(s)选择玩家 i 翻转其动作。因为 n 为奇数，所有相邻位置不可能都不等，这类合法selector对每个状态都有定义，且没有自环。第1–3项结论适用于每个这样的defect-resolving selector；第4项端点证书则指定其中的最小下标selector。

Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion 如下。

1. 对每个实 α≥1，上述完整签名矩阵均有概率dual λ≥0、Σλ=1、B_h(α)^Tλ≤0。可取仅支撑恰有一条相等邻边的2n个状态的均匀概率，在 α=1 时全部列积恰为0。
2. 若 1≤α<2^d，则任意这样的dual均须对每名玩家的两个翻位方向分别给正质量。写 μ_i=Σ_(s:h(s)选i)λ_s，μ_(i,a)=Σ_(s:h(s)选i且s_i=a)λ_s，则 μ_(i,a)>0 对每个 i,a 成立。因此dual至少使用全部n名移动者，其状态支撑至少为2n；第1项均匀环证书达到2n，所以最小支撑恰为2n。不能统一限制为固定数目的移动者或状态；n在固定d、α下可无界。
3. 更定量地，置 A=2^d−α>0，B=α2^d−1>0，r=A/B∈(0,1]。每个dual均满足 μ_(i+1)≥r μ_i。特别地

   μ_i ≥ r^(n−1)/(Σ_(j=0)^(n−1) r^j) >0。

   此外 μ_(i,a)≥μ_i/(1+α)≥r^(n−1)/[(1+α)Σr^j]。当 α=1 时 r=1，于是每名移动者质量恰为1/n，每个翻位方向质量恰为1/(2n)。这些下界只是必要条件，不宣称对任意参数可达到。
4. 指定 h 总取最小缺陷下标时，门槛 2^d 对“全部移动者必须正质量”结论是准确边界：当 α≥2^d，存在只由玩家0移动的二状态支撑dual。取 s^0=(0,…,0)、s^1=(1,1,0,…,0)，各质量1/2。两状态都由 h 选择玩家0。

该结论在完整签名和proper/core签名两种锥下分别成立。proper签名实际可通过零费用单点marker保持非空、空交且反链的动作策略；不依赖空策略、固定玩家、必选正费用或自偏离。

### 11.2. 唯一相等邻边构成显式2n环

恰有一条相等邻边的状态有2n个：指定该边和一名端点的bit后，沿其余n−1条不等边唯一确定全部状态；奇n保证绕回一致。若唯一相等边是(i,i+1)，翻转玩家i后该边变不等，而边(i−1,i)由不等变相等，其他边不动。因此缺陷向下标减1方向移动。走n步后每名玩家恰翻转一次，得到原状态逐位补集；再走n步回到原状态。缺陷位置在前n步互异，后n步同位置的状态是补集而不同，故这2n点构成一个长度2n的简单有向环Q。

不需要断言全h只有这一个循环，也不需要断言所有其他状态都进入Q。

### 11.3. 等权资源势给出全签名可行dual

对任意签名σ，令 z_j(s)=1_(玩家j当前标签在σ_j中)，负载 L(s)=Σ_j z_j(s)为非负整数。次数k的单资源定义离散原函数

    F_k(L)=Σ_(a=1)^L a^k，F_k(0)=0。

对任意翻位 s→t，若移动玩家对该资源的使用不变，则其当前与真实偏离后费用相等，且负载相等；若其离开资源，F_k(L(s))−F_k(L(t))=L(s)^k；若其加入资源，差为−L(t)^k。因此对所有完整签名和0≤k≤d，

    B_h(1)[s,(σ,k)]=F_k(L(s))−F_k(L(H(s)))。

沿Q求和恰为0，故Q上均匀分布是α=1的全列dual。α增大时，每列额外减去(α−1)乘以非负真实arrival费用，故同一分布对所有α≥1仍可行。常数项k=0的约定由F_0(L)=L覆盖；未使用资源由指示量消去，不涉及0/0。

### 11.4. 每条邻边的两个正资源迫使相邻移动者补偿

固定邻边(i,i+1)。取两个资源列，均为次数d、系数1：

- r_i^0只由玩家i和i+1的动作0使用；
- r_i^1只由玩家i和i+1的动作1使用。

其他玩家都不使用这两个资源。二列都是proper/core列，故下面必要条件对完整与core锥都有效。

对状态s，其两列margin的和记D_i(s)。若移动者不是i或i+1，D_i(s)=0。若移动者属于这两个端点，则：

- 若当前两端动作相等，移动者当前费用为2^d，翻位后为1，故D_i(s)=2^d−α=A；
- 若当前两端动作不等，当前费用为1，翻位后为2^d，故D_i(s)=1−α2^d=−B。

h选择i时，按定义s_i=s_(i+1)，所以必为第一种；h选择i+1时两种均可能，所以总有D_i(s)≥−B。任一dual对两列分别非正，相加给

    0 ≥ E_λ D_i ≥ A μ_i−B μ_(i+1)。

所以 μ_(i+1)≥r μ_i。若某 μ_i=0，沿反方向由A>0逐次迫所有μ为0，与Σμ=1矛盾。因此全部μ_i>0。

对于定量下界，固定i，沿反向逐次用 μ_(i−j)≤μ_i/r^j，j=0,…,n−1。归一化给

    1=Σμ≤μ_i Σ_(j=0)^(n−1) r^(−j)，

即 μ_i≥r^(n−1)/(Σ_(j=0)^(n−1)r^j)。当r=1，环上所有不等式迫相等且归一化为1/n。

对每名玩家i，另取两个只在其动作a使用的私人常数资源列（degree0）。dual分别给 μ_(i,0)≤α μ_(i,1) 和 μ_(i,1)≤α μ_(i,0)。故每个方向至少为 μ_i/(1+α)，特别地全部2n个玩家方向都有正质量。每个状态仅选择一个玩家的一种方向，所以任何dual至少支撑2n个状态；第11.3节的均匀环证书恰有2n点，故最小状态支撑恰为2n。当α=1时两个方向相等，均为1/(2n)。

注意：此处将两条正资源列相加，仅推出必要的dual约束；没有用负费用、负资源系数，也没有把一般极锥换成带符号全部多项式矩。

### 11.5. 端点的单移动者dual

令两个支持状态分别为s^0=(0,…,0)、s^1=(1,1,0,…,0)，各质量1/2。边(0,1)在这两状态均相等且下标最小，故h都选择玩家0翻位。

固定任意签名σ和次数k≤d。

- 若玩家0的两个动作都不用资源，则两行均为0。
- 若两个动作都用资源，则每次玩家0翻位保持该资源用户集不变，因此各行均为(1−α)乘以非负费用，非正。
- 若仅一个动作用资源，则两行一个是departure费用、一个是负α倍arrival费用。两处除玩家1外的资源使用完全相同；玩家0被使用时总贡献自身1，玩家1的贡献至多改变1。故两个正负载L,L'≥1且|L−L'|≤1，因而 max(L^k/L'^k,L'^k/L^k)≤2^k≤2^d。于是α≥2^d时，两行等质量的列积非正。

这覆盖所有完整签名，也覆盖其proper子集。α=2^d时第11.4节A=0，所推μ约束不再迫所有玩家有正质量，与显式二状态证书一致。任一单状态点质量都违反所选玩家当前动作的degree0私人列（该行恰为1），故在此端点及其上，最小状态支撑恰为2。

### 11.6. 准确含义与主目标的缺口

本族的玩家全部等权，所有此类游戏都具有标准离散资源势；本文甚至给出这个selector在α=1的显式全列dual。它不是无均衡反例，也不是一般dual不可行证据。

它排除的是统一有界移动者支撑的dual构造：每个固定d≥1和1≤α<2^d，所需移动者数可无界。尤其任何拟定常数C，当C d/ln d<2^d的次数范围内，不能希望通过固定数量玩家的局部证书保证完整selector dual。不同玩家的资源成本补偿无法被无证拆成独立的单玩家矩匹配。

仍未解决：任意selector在统一O(d/ln d)倍率是否存在dual；一般权向量下如何组织无界数量玩家之间的补偿；是否存在比已知d/ln d下界更强的全状态非存在机制。

Dependencies：MODEL、完整动作签名矩阵定义、奇环缺陷图、逐资源离散原函数及两个proper pair列的必要不等式。无需外部PNE定理；不以有限穷举证明任意参数。

Evidence：审查者仅据精确statement独立重构奇环与必要补偿链，然后攻击冻结正文SHA256 `736cff453a3a750c58ebdac2b7fe133e2128a56b8d203abd54ebe31610a7ca28`；方向质量、最小2n支撑及端点二点证书另作独立攻击。

Counterevidence / Objections：任意全类存在证明仍可使用无界数量玩家；不排除小于D+1的其他依模板支撑界，亦不否定一般dual。等权全类具有精确势，原例不是均衡非存在；奇数n、d≥1与严格α<2^d均承重。完整与proper两锥的身份分别成立，零费marker只区分动作。

Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth仅所述择证补偿/支撑定理；Value为排除统一有界移动者局部拼接；Mechanism为正pair列迫循环补偿；Novelty和外审未认证；Ambition保持WC-TARGET OPEN。

Related Files与复验合同见下节。

## 12. 奇环补偿的独立核验与继续义务

[独立重构与冻结攻击](../../../reviews/weighted_congestion/template_certificates/selector_mover_support_review.md)只覆盖新ID，不将本稿原始三Claim及刚性审查自动外推。

在仓库根运行：

- `python3 tests/audits/weighted_congestion/template_certificates/verify_selector_mover_support.py`：作者按真实资源签名核验全部允许defect移动者、pair列公式、私人方向行、全签名环dual和端点二点dual；冻结输出为`evidence/runs/weighted_congestion/template_certificates/selector_mover_support.json`。
- `python3 tests/audits/weighted_congestion/template_certificates/independent_selector_mover_support.py`：独立实现重算相同承重身份，另覆盖共同正分数权、偶数n/degree0不适用边界及支撑计数；冻结输出为`evidence/runs/weighted_congestion/template_certificates/independent_selector_mover_support.json`。

两份代码均为整数/Fraction、无随机seed、无solver与浮点容差；完整参数、命令、Python版本及源码SHA在代码/JSON中明确。一般实α和任意奇n证明由第11节承担。现在真正缺少的是组织任意权、任意selector上无界多玩家的全局补偿，不能再无证限制为固定数量移动者。
