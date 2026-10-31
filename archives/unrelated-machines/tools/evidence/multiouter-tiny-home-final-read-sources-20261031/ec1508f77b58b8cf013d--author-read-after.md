# tiny-home 多 outer 19/10：作者 Proof 实际全文读后审查

日期：2026-10-18。审查者：`/root/sol_nsw_independent_attack`。仅 scratch；不修改既有 Exact-first 记录。

## 1. 真实顺序、身份与阅读范围

先实际全文读 Exact `sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md` 第 1–32 行，实核 SHA256 `38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a`，然后冻结独立记录：

`/workspace/scratch/038d9dcc4cac/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md`

SHA256 `c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a`，16573 bytes、205 行、0444。该记录独立闭合的是 floor-simplex 强凸势、逐 helper 固定 state、有理投影 subgradient、fixed-state allocation LP 舍弃至多 k 个 split items 的不同算法。该记录没有看本作者算法的 MW、Efron–Stein 或请求位后端。

root 表示已实际全文读完该 205 行记录之后，才释放本作者 Proof。此后我本轮唯一新增实际打开的是

`/workspace/scratch/038d9dcc4cac/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md`

实核 SHA256 `ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332`，17024 bytes、193 行、当时权限 0644。实际分 **1–100、101–193** 两块完整阅读；两块均未截断。

这是知情作者读后审查，不是第二次 blind Exact-first。我此前知道单 outer SA1、一般多 outer 条件点拼接障碍和普通 flat 全 jobs 语义；本新 Exact-first 的独立算法与作者算法不同。本轮没有打开作者提到的 `.py`、运行日志、其他审查或学习记录；未读或改 repo、Git、Work、token。Proof 第 189–193 行只是作者对有限软件的文字范围说明；我读过这些文字，**没有实际读取或复核该软件**。

结论：作者这份独立于我算法的 MW + 请求位 + variance/CE 证明未发现 fatal，数学上支持同一个限定 19/10 Exact。下面逐项重构其不同承重处。没有以旧 Exact-first PASS 代替新 Proof 检查。

## 2. ordinary P 与 LP 判定：仍是同一对象

作者始终保留所有 indexed states、selectors、listed incidence jobs，zero jobs 最后放原 private，inactive payload 不删除。每个 state 的正 payload 和为 1；每个资源端 incidence 时间 1。若 group 资源分配最小值是 V，选一条达到对应值的 state 就给 C<=2-V；反向实际 C<2 时所有资源至多一份 unit job，selector 所在 state 输出的正系数至少 2-C，只保留所选 state 输出即得 disjoint bundles。有限 assignments 使最优达到，OPT=2 时由正向式排除 V>0。因此

    OPT(P)=2-V,  1<=OPT<=2

包括 V=0 的边界都正确。没有把 inactive exports 本身当作 selected bundle 的必要部分。

源系统确实是 epsilon=15/16 的完整 common primitive-SA1：全部 base row × 每个同一原 A/Z primitive 及其补，binary diagonal，共同对称表；没有 PSD 或 unit-FSLP 假设。integer allocation 的 Dirac 使此系统必要。LP infeasible 则 V<15/16，OPT>17/16，完整 private baseline C<=2 给 ratio<32/17<19/10。

源 LP 是从 Q 显式生成并求解，给定点不是输入 oracle。d 个 primitives 的二阶表和 lifted rows 数均多项式；box lifts 把所有 pair 限在 [0,1]，有理基本点长度由普通 LP determinant 界给多项式。所有 state/resource incidences 的 zeros、重复 indices、unused resources 留在 P；忽略其随机请求只使后续 packing 更弱。

own helper 的关键整数化也正确：own quality (Z-epsilon A)(1-Z)>=0 给 E(AZ)>=EA；gate (A-Z)A>=0 给反向；box (1-A)Z>=0 与 gate (A-Z)Z>=0 给 E(AZ)=EZ。故 EA=EZ。home cap 继而给 fallback state 总质量 f_j>=outer home claim x_j；每个 outer 只有一个 state 给 sum_{j in i}w_j f_j>=epsilon。

同一 LP 点给 alpha_js、zeta_jsu，且

    0<=zeta<=alpha,
    sum_u p_jsu zeta_jsu>=epsilon alpha_js,
    sum_{j,s}zeta_jsu<=1.

这是同一份 global cap 1，不是各 outer 的独立容量。alpha=0 时 zeta=0，无 0/0；helper 没有 fallback 的情况也覆盖。

## 3. 请求者 priority oracle：必须保留请求语义

作者人为构造的 product space 是：每 helper 选一个 fallback state 或 empty；所有 positive-mass state 的各正 incidence 再各自预抽 Bernoulli coin，概率 r=zeta/alpha；只读取所选 state 的 coins。不同 helpers 整块独立。该空间来自 LP 边际，但不声称其二阶矩等于源 SA1 表。

固定 nonnegative outer 权重 lambda 和为 1，对每资源按 lambda_i w_j p_jsu 给**实际请求者**排序。winner formula

    P((j,s) wins u)
      = zeta_jsu * product_{h!=j}
          (1-sum_{t:(h,t) precedes (j,s)} zeta_htu)

是精确的：对 helper h，互斥 states 的高优先请求概率相加；不同 helpers 的事件才相乘。当前 helper j 的其他 state 不可能同时出现，所以不能再加一个同 helper 的乘积因子。ties 的固定索引顺序没有破坏此式。

阈值积分重构给 lambda dot g(lambda)>=(5/8)epsilon^2=1125/2048：对每资源的高于阈值请求概率 a_j，总和<=1 来自**全部 helpers、全部 states 的同一个** zeta packing cap；independent-helper product 给 1-product(1-a_j)>=1-exp(-sum a_j)>=(5/8)sum a_j。再用各 fallback quality 与各 outer 的 sum w f>=epsilon。这里用到了状态条件下 request probability，而不是把所有 selected-state resources 免费交给这些 helpers。

g_i in [0,1] 也正确，因为每 helper 只读一个 normalized state 的资源，outer 自己所有 w 和为 1。这个界没有要求每个 p 都 tiny；tiny 的是整个 helper 的 home 权重 w_j。

我的 Exact-first 使用的是 selected-state 最大 welfare，作者此处使用 requesting-winner welfare。两个随机目标不同。**我没有将自己的“可重分配到最高 selected clause”步骤移植到本作者 CE 结果**；作者第 175 行明确禁止这样的改分配，后文也确实一直保留实际请求 winner。

## 4. Floored MW 的均值、轮次数与分母

作者取 N=1024k、eta=1/32，p_i=b_i/sum b，lambda_i=(7/8)p_i+1/(8k)，b_i 更新为 b_i(1-eta g_i)。全部 b 正，lambda floor 是 1/(8k)，无 k 固定常数假设。

weighted oracle 下界 a=1125/2048 加上 uniform mean<=1 给

    p dot g >=(a-1/8)/(7/8)=869/1792.

令 B_t=sum b_i。由 log B_N<=log k-eta sum_t p^t dot g^t，及每个 i 的 log b_i>=-eta sum_t g_i^t-eta^2 N，得到

    mean_t g_i^t >= mean_t p^t dot g^t-eta-(log k)/(eta N).

log k<=k 给后两项之和<=1/16，故

    mu_i >=757/1792>2/5,
    757/1792-2/5=201/8960>0.

这是逐 outer 的均值保证，并非只保住某个 weighted sum。k=1 也正确；此时 log k=0、lambda=1，没有边界特例缺失。

分母论证可独立闭合：所有 helper categorical probabilities 和所有预抽 request coins 是固定的一份有理 product distribution，取其各分母之积 D0；所有 payoff coefficients w_j p_jsu 的分母之积取 D1。log D0、log D1 都是输入及源 LP 点长度的多项式。MW 改变的只有 priority orders，不把 b 或 lambda 递归当新请求概率。因此**所有轮次** g_i 的共同分母可取 D0 D1；每个 b_i 的分母可取 (32D0D1)^N。其位长随 N 线性增长，仍为多项式。p 的归一化和 score 比较也只有多项式位长；没有隐藏的指数精度。

## 5. 两层方差：明确核全 global k 因子

作者为每个资源 u **独立**选一轮 t_u。这一独立性只用于 rules；helpers 的同 state 跨资源相关性仍保留。每个单资源均匀混合的期望等于逐轮平均，故 E W_i=mu_i，不要求同一个全局随机轮次。

固定全部 helper blocks X，记 d_u=max_actual_requester w_j p_jsu。因为每 helper 只实际读取一个 state，

    d_u<=delta,
    sum_u d_u<=sum_j w_j sum_{u requested by j}p_jsu<=k.

给定 X，各资源 contributions 因 t_u 独立而独立，均在 [0,d_u]，所以 Var(W_i | X)<=sum_u d_u^2<=delta k。不能在这里把一个 helper 的多个 states 同时放进 normalized sum；作者使用的是实际 selected state，正确。

再替换整个 helper block X_j，固定其他 blocks 和全部 resource rules。其他 helpers 的相对 priority 完全不变，只有旧 j 或新 j 成 winner 时，该资源 winner 才可能变化。对目标 outer i：若它的旧 contribution 被新 j 抢走，其 value<=新 j 的 value 乘 lambda_{i(j)}/lambda_i；若旧 j 释放给它，同样由旧 j score 控制。若 i=i(j)，两边自己价值的差也至多旧/新 own contributions 的和，不需另加漏项。因此逐资源 absolute difference 确实至多

    (lambda_{i(j)}/lambda_i) w_j
      (p_old,j,u * 1_oldrequest + p_new,j,u * 1_newrequest).

各资源可能选不同规则，但每轮 lambda 比值都<=8k。旧、新 normalized state 各最多贡献 1，故整个 W_i 的替换差<=16k w_j；对 rules 先取期望得到 F_i(X)=E_rules W_i 的替换差也满足同一界。所有 MW orders 在这一替换论证中固定；MW 没有根据实际 X 重跑。

独立块的 Efron–Stein inequality（可由 product-variance tensorization / Doob 分解得到）于是给

    Var F_i <=(1/2)sum_j (16k w_j)^2
             <=128 k^2 delta sum_jw_j=128delta k^3.

全方差再对**所有 k 个 outer**求和，准确为

    sum_i Var W_i<=delta k^2+128delta k^4
                  <=129delta k^4<=129/4096<1/25.

没有把单 outer 的 variance 偷换成全体的 variance，也没有为各 outer 复制资源 cap。129/4096 与 1/25 的差是 871/102400>0。tiny 条件在此支付了整个 k^4，而非只支付某个 fixed-k 常数。

## 6. 平方势 CE：shared state、请求 coins 与双资源事件

中心 mu_i 是之前算出的**固定**有理均值，不随 CE 变化。Psi=sum_i(W_i-mu_i)^2，初始期望=sum_i Var W_i<1/25。固定顺序是 helpers 的 categorical states、全部 positive-mass states 的正 incidence coins、各资源独立 t_u；各步只选正概率分支且精确计算 conditional E Psi，所以最终 Psi<1/25，逐个 W_i>mu_i-1/5>1/5。

我重新展开了作者双资源因子的合同。对 distinct u,v 和指定 winners (j,s),(l,t)：每个 helper h 只对**一个 shared state q**求和；若 h 是一个指定 winner，q 必须等于那个指定 state；若它是两个 winner，必须 s=t。给定 q，资源上要求它 winning 时 coin=1；它不是 winner 但 candidate 排在指定 winner 前面时要求 coin=0；排在后面则无约束。不同 u,v 的两枚 coins 是独立预抽变量，但只有在同一个 q 下才可相乘。之后才按 q 求和、再按 helpers 相乘。

特别地，同 helper 同 state 赢两资源的基本因子是

    alpha_hq * r_hqu * r_hqv,

不是两个边际 zeta 的乘积；同 helper 不同 state 的双 winner 因子是 0。指定 winner 的 helper 在另一个资源上不是 winner 时也必须遵守该资源的“若排前则不请求”，未漏跨资源阻挡。同 state/resource 至多一个 incidence 的 Exact 条件保证 distinct u,v 使用不同 coins。u=v 的平方直接枚举一个 winner 的 Y_iu^2，不重新独立抽两次 rule 或两个 winner。

对一个/两个资源分别平均至多 N/N^2 个独立 rule choices、枚举 winner nodes，即可精确得到 E W_i、E W_i^2。全局 state/resource profile 不需要枚举。候选/规则的宽松计数 O(|B|^2 N^2 I^2)，每项再做多项式个 state 求和与 helper 乘积，足够给出绝对次数多项式。none-winner 产生的 Y=0，无需另补非零 payoff 项。

各 CE 条件都是 product base variables 的具体值，而不是一个额外未知相关事件；尚未固定变量维持原分布。预抽 coins 即使对应未选 state 也可照样固定，不改变任何实际请求。r=0/1 只有一个正概率分支；alpha=0 的 state 从来不选择，不建立 0/0 coin。每个 partial prefix 的条件 payoff moments 仍只用原有理概率或 0/1、1/N 的加乘。其共同分母可由 D0 N^{|B|} D1^2 控制；固定中心 mu_i 及 mu_i^2 的额外分母也另有 §4 的多项式位长界。若改写为 conditional probability 的商，partial event numerator 同样有多项式位长；显式 factor 公式实际避免了这个大条件商的构造。由此没有免费 conditional-moment oracle。

这一阶段没有丢 coins，再用所有 selected states 重分资源。最终保留的就是 CE 固定的实际 requesting-winner allocation；这是均值/方差保证与最终 W_i 保证共同对应的那个 allocation。

## 7. 从 aggregate 到每个 group、并执行全部原 jobs

定义 Good 为 Q_j>=1/10。由于 Q_j<=1，令 z_i=sum_{j Good in i}w_j，有 W_i<=z_i+(1/10)(1-z_i)。W_i>1/5 推出 z_i>1/9>1/10。empty 永远不是 Good。保留 Good helpers 的原 winner B bundles，把它们互异的 homes 交给对应 outer；其余 helpers 取自己的 home。B 与 homes 不交，且所有 B bundles 来自同一份 winner allocation，所以资源是全局 disjoint。

Good 选原 indexed fallback state，其他 helpers 选 own，outer 选其唯一原 state。selectors 放这些原 private；所选 state 对这些 bundles 的正 incidence jobs 走 exact resource 端，其余 incidence jobs（包括全部 zero jobs、所有 inactive fallback states 的 payload）放各自 private。active private 负载<=2-1/10，inactive private payload 总量是 1，资源负载<=1。没有改变原矩阵、job 数或 finite endpoint；重复索引不合并，unused resources 可闲置。

因此可行分支 C<=19/10，OPT>=1 给 ratio<=19/10；不可行分支先前已有更小的 32/17 比值。所有输入边界（k=1、无 fallback helper、零概率/确定 coins、零 incidences、重复 indexed states、unused resources、任意二进制有理分母）均已在相应步骤覆盖。

## 8. 判定、软件角色与范围

本次实际全文读后的数学判定：**未发现 fatal**。独立 Exact-first 的强凸势算法与这份 MW+Efron–Stein+请求位 CE 算法是两条不同的充分路线；本记录逐核的是后者，未用前者 PASS 替代后者证明。作者请求位语义、同 helper 的 shared-state 双资源事件、所有 outer 的总方差、MW/CE 位复杂度及全 jobs 恢复均站得住。

本轮未运行算法、未读作者软件，也未代签任何小实例实验。Proof 自己第 189–193 行只声称一个有限 pair backend Fraction 核，不包含 tiny-profile 输入、LP、N 轮 MW 或完整 ordinary schedule；我没有把这段文字升级为自己验证过的证据。本轮无新增软件验证，前一记录的少量 Fraction 常数反算范围保持不变。

最终仍是仅数学算法规格、无端到端实现。结论限于 Exact 的 typed 输入：可变 k、每 outer 单 state、全部 positive homes 互异、每 home 一个 own-singleton helper、normalized 显式 B-fallback、没有其他 groups、w_max<=1/(4096k^4)。不推广到 multistate outer、home overlap、额外 auxiliary groups、一般 normalized Q 或一般 UM；全球新颖性未认证。历史其他对象的反例不因这里通过而追认或消失。
