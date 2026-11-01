# signed 严格种子的福利缺口筛选

2026-10-25。作者初等解析引理，自检；待父方独立检查。全部模型和量词与 peer [signed 修复](../../../R-ab4b3c24c8f949198e194dd45bb66105/mixed/signed_credible_repair.md) 相同；不构造 universal price，不证明一般 half。

## 1. 精确陈述与证明

任取原输入的末位 BR 目标路径，m>=2。用 peer 定义的真实 `M_i`、`g_i=M_i-u_i`（i<m）、`B=2W-OPT_m`，并记

`P=sum(g_i)_+, N=sum(-g_i)_+, p=max(g_i)_+, n=max(-g_i)_+`，

`C=2P+p-N+n`。

则对全部这样的输入与路径，

`B+C >= W-OPT_m+u_m+max_(i<m)u_i`。                 (SCREEN)

证明：令 `d_i=(-g_i)_+=(u_i-M_i)_+`。所有客户非负，所有真实收益非负，故 `M_i>=0`，从而 `0<=d_i<=u_i`。有

`N-n = min_(j<m) sum_(i<m,i!=j)d_i`

`    <= min_(j<m) sum_(i<m,i!=j)u_i`

`    = W-u_m-max_(i<m)u_i`。

另一方面 `2P+p>=0`，所以

`B+C >= 2W-OPT_m-(N-n)`

`     >= W-OPT_m+u_m+max_(i<m)u_i`。

证明完。m=2 时右边就是 B；此时只有一个负坐标，N=n，原式 C>=0，端点一致。

因此严格 `B+C<0` 的必要条件为

`OPT_m-W > u_m+max_(i<m)u_i`。                    (NEC)

这不是充分条件，也没有证明任意真实 SPE 满足其反向。它只排除不可能生成严格 signed 种子的目标。特别 `W=OPT_m` 时右边非负，严格种子绝不可能。覆盖全部客户的旧 LAST/helper 反例可用来打价格或其他助手，但不能直接作为此修复的负预算种子。

若只有可信退出上界 U 而不是精确 M，要应用上述式子需先取 `U_i>=0`。真实收益非负，任何有效共同上界本来也可取非负；同样有 `(-[U_i-u_i])_+<=u_i`，所以同一筛选对 `B+C(U-u)` 成立。该筛选不会替代 U 的真实完整子 SPE 验证。

可以直接调用任一已证真实下界 `L_i<=M_i` 得到较强的便宜筛选

`B+C(g) >= B+C(L-u)`，

因为 C 是非负价格域 K_pm 的支撑函数，逐坐标非减。例如原模型的原始分母下界

`L_i=max_T sum_(x in T)1/(b_i(x)+m-i+1)`

即可使用。这里只复用 peer 已证的支撑函数单调性及原通用偏离下界，不另认领机制或证明一般非负。

## 2. 旧根 floor 的状态校准

round5 的 [真实保险族](../../round5_general/security/global_extra_individual_counterfamily.md) 对每个 m 给完整 SPE，根收益 `u_1=m/(m-1)`，最优覆盖 `OPT_m=3m-2`。真实 `M(empty)` 是全部完整 SPE 根收益的最小值，因此 `M(empty)<=m/(m-1)`。

而

`OPT_m/(2m-1) - m/(m-1)`

`= (m^2-4m+2)/[(2m-1)(m-1)] > 0`，m>=4。

故旧弱根 floor `M(empty)>=OPT_m/(2m-1)` 已由该已有全人数组件否定。m=4 分子为2，此后严格递增；m=5 差为 `7/36`。这只是既有完整 SPE 的直接数值推论，不认领新反族，也没有从个体失败推断 MP、signed seed 或一般 half 失败。

## 3. 原则上的限制

SCREEN 没有使用后继理性，除 M 的非负性外也没有使用其精确值。它用于在昂贵可信退出计算之前排除明显不合适的目标；它不支付一般主目标。它同时说明，从 W=OPT 的旧助手反例上寻找 exact-M 严格次可加并不能凭空变成 `B+C<0`：对该输入任意 M>=0 都已被 SCREEN 挡住。
