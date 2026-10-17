# 列表 agreement 度数预算：真正陈述先行独立重构

审查者：boss11 内部研究者 literal_gap_implementation。
仅先读 Exact：`list_agreement_degree_budget_exact_statement.md`，SHA256 `2c36eff940c9918105631b40908df15a3d5dfe334761a7bb3d7bfe26cca2f454`。未读 root/pcsp 的证明、交流或其他相关新稿。
Claim candidate：`UM-LIST-AGREEMENT-DEGREE-BUDGET-v1`。

结论：四条均可独立完整重构，无 standing fatal objection。下述是确定性有限组合证明；没有使用 YES witness、源困难性、随机性、调度编译或有限测试。新颖性未审查。

## 对象和预处理

G=(A,B,E) 有限简单，B非空；每 a 度 d>=1，每 b 度 D>=2。因简单及 D>=2，各 b 有 D 个不同邻居，特别 A非空。|A|d=|B|D，所有度与邻居都在显式图中。

固定任意 total maps pi_ab:Sigma_A->Sigma_B，common-image 假设保证对每 b 能确定性找到一个 z_b，属于所有 a in N(b) 的 image。逐 b 枚举显式字母和映射值、取交，选择某个固定顺序最小 z_b；并为每条 incidence (a,b) 取一个 x_ab，使 pi_ab(x_ab)=z_b。全部操作按 full explicit maps 大小多项式。这里不需要一个同时满足各 b 的全局赋值：x_ab 允许同一 a 在不同 b 使用不同原像，将由列表预算控制数量。

把在某 a 的一个选中 incidence 视为一张 ticket。即使不同 tickets 最终使用相同 x_ab，也分别计数；最后列表去重只会缩小大小，因此 ticket 上界足以保证 list 上界。

## 1. 确定性线性下界

初始每 a ticket 数 r_a=0、已服务右集 S为空。只要存在 b notin S 有两个不同邻居 a,a' 满足 r_a<L、r_a'<L，就选定一个固定顺序的此类 b 和邻居对，给这两条 incidence 各发一 ticket，令对应 r 加一并将 b 加入 S。最后令 Lambda_a 为该 a 全部选中 incidence 的 x_ab 集合。

每步增加一枚右顶点，因此至多 |B| 步；各 r_a 不超过 L，也不超过 d。输出列表大小 <=r_a<=L。每个 b in S 的两个不同邻居均把其 preimage 放进列表，且两映射值同为 z_b，所以这些 b 全 agree。别的 b 可以额外 agree，不会损伤下界。

令 U=B minus S，T={a:r_a=L} 为终止时饱和左顶点。每个 b in U 至多有一个未饱和邻居，否则算法还能继续；故每个此 b 至少有 D-1 个 T 邻居。另一方面总 tickets 为2|S|，所以

    (D-1)|U| <= |E(T,U)| <= d|T|,
    L|T| <= sum_a r_a = 2|S|.

L>=1 可以相除，合并得到

    L(D-1)(|B|-|S|) <= 2d|S|,
    |S|/|B| >= L(D-1)/(2d+L(D-1)).

故实际 agr(Lambda) 至少此数。所有分母正。若 U为空，则比率为1，自然满足该小于1的下界；若 L>d，则不存在饱和左点，终止条件强制 U为空，同样没有边界失效。

复杂度：固定顺序扫描 b 和邻居对，朴素实现最多 |B| 次全图扫描，已是多项式；不需优化，也没有按 L 次数循环。只比较 r_a 与二进制 L，比较位数为 O(log d+log(L+1))。可在 L>=d 时直接为每 b 任取两邻居并完成全部服务；也可在 L>=|Sigma_A| 时直接给全部字母。均避免巨大 L 的数值展开。

## 2. all-agree 的 ceil(2d/D) 阈值

作容量流网络：source->每 b 容量2，每 b->其每个邻居 a 容量1，每 a->sink 容量 min(L,d)。需要总流2|B|。

给每 incidence 流2/D。D>=2 保证边容量1不被超过；每 b 的流量恰2；每 a 的流量恰2d/D。因此当 L>=ceil(2d/D) 时，左容量合法。又 ceil(2d/D)<=d，所以用 min(L,d) 截容量也无害。

由整数最大流存在同值的整数流。每 b 的两枚单位流经过两个不同邻居（中间边容量1且图简单），每 a 的选中数<=L。为这些选中 incidences 放入前述 x_ab，所有 b 都 agree。算法确定性、返回实际列表，全部容量<=max(2,d)，网络显式多项式，不展开二进制巨大 L。

## 3. 每个给定简单 biregular 图上的普遍阈值锐性

给任意上述 G，人为定义 common alphabets

    Sigma_A = {ell_b : b in B},
    Sigma_B = {zero} union {private_a : a in A},

其中所有 private_a 互异且不同于 zero。对每条 incidence (a,b) 定义 total map

    pi_ab(ell_c) = zero       if c=b,
                  private_a if c!=b.

每个 neighbor image 都含 zero，故满足 common-image 条件。两个不同邻居 a!=a' 的 private 符号互异，因此在 b 上跨邻居 equality 只能发生于 zero。即

    b agrees iff 至少两个不同邻居 a 的 Lambda_a 含 ell_b.

若所有 b agree，则计数这些 incidences 至少2|B|。每个 a 的列表最多 L 个不同符号 ell_b，每个符号仅能支付一个特定右顶点 b（放入非邻居的符号也不能支付），所以这些 incidences 总数至多 |A|L。由 biregularity

    |A|L >= 2|B| = |A|*2d/D,

从而整数 L>=ceil(2d/D)。因此任一 1<=L<ceil(2d/D) 的列表都不能让全部 b agree。

该构造一次同时排除所有低于 cutoff 的 L，不需要为不同 L 改地图。字母表大小 |B| 和 |A|+1，总 map table |E||B| 项，按图编码大小多项式。若 |B|=1，所有边映射都仅取 zero，仍成立；此时 d=1、ceil(2d/D)=1，所述低 L 区间为空，sharpness 陈述是正确的空量词。其他 cutoff=1 情形同理。

锐性针对第2条“保证所有右点 agree”的通用整数阈值，不声称第1条分数下界本身对每张图或每套地图最优；不声称这些人为地图构成 hard source。

## 4. soundness 约束和精确代数

若每个 <=L 列表的 agr<=alpha，第一条实际输出立即给

    alpha >= L(D-1)/(2d+L(D-1)) > 0.

所以 alpha=0 不可能（alpha<0 也不可能）。若 alpha<1，第二条说明不可能有 L>=ceil(2d/D)，故 L<该 cutoff。

alpha>0 时可正数交叉相乘：

    2alpha d >= (1-alpha)L(D-1),
    d/L >= (D-1)(1-alpha)/(2alpha).

未把未知 satisfying assignment 导入此推论，亦没有把计数预算当作一项 NP-hardness。

## 结论与限制

common-image 条件只用于为每个 b 选择 z_b 和 incidences 原像。不同 a 可用不同原像，因此无需全局 YES。简单图及边容量1真正保证“两个不同邻居”，不可默默改为 incidence 多重图。B非空使 agr 的分母有定义；L,d正、D>=2使全部显示分母正；L>|Sigma_A| 时集合大小语义保持正确。全文仅组合证明和标准整数流，不靠实验升级一般结论。
