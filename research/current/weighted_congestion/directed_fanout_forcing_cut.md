# 分叉双人侧资源反馈：统一轻玩家强迫下的割均衡

本稿由主研究者团队直接推导，并经另一研究者先独立重构、再攻击冻结证明。实际冻结版本、修订和覆盖见配套审查；未外审，未认证新颖性。
本稿只限制下述精确资源拓扑与统一强迫假设。WC-TARGET 的全类匹配上界和严格否定均未解决。
没有使用外部文献定理；标量包络与仓库奇环包络相同，并在下文重建所需性质。

## 精确 Claim（供审查者先独立重构）

ID/version：`WC-DIRECTED-FANOUT-FORCING-CUT-v1`。

中文数学名称：分叉双人侧资源反馈在统一轻玩家强迫下的割均衡。

- **Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 完整精确对象、全部参数、承重假设(UF)及结论逐项如下，不扩大到任意拥塞拓扑。
- **Dependencies：** MODEL；下文自足标量f_k包络、非负多项式展开、有限二染色局部最小化；T_d与既有奇环包络同一定义，无外部定理导入。
- **Evidence：** 完整实参数证明；先独立重构后冻结攻击；Fraction实际资源和全部小状态核验，详见末节。
- **Counterevidence / Objections：** 一侧资源有多个hub、非对称动作副本、多个主源或(UF)失败不在范围；局部最小light稳定元无需存在。
- **Status：** complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述结构存在定理；Value为排除有向分叉私有侧资源的统一强迫放大；Novelty未认证；Mechanism为共享强迫预算与加权割；Ambition不判定全类目标。
- **Related Files：** 正文末节的独立审查、审计代码及冻结结果；定义和比较入口为MODEL与奇环包络总稿。

固定整数 d≥2，令

    f_k(R) = [R(1+R)^k+1]/[(1+R)^k+R^(k+1)],
    T_d = sup_{R>1} f_d(R).

有限非空 hub 集 V；有限 light 集 L（允许为空）。Hub v 权 u_v>0；light ℓ 权 w_ℓ>0，并指定唯一源点 o(ℓ)∈V。另有有限侧资源索引集 J，每个 j 指定唯一 light ℓ(j) 和目的 hub t(j)。允许多个 j 有相同端点，允许 o(ℓ(j))=t(j)。每个 light 的侧索引集 J_ℓ 可为空。

每个 hub v 有两个主资源 A_v^0,A_v^1，两者费用为同一个非负系数次数≤d 多项式 F_v（可为零）。每个侧索引 j 有 B_j^0,B_j^1，两者费用为同一个此类多项式 G_j（可为零）。全部资源互异。

Hub v 的动作 b∈{0,1} 为

    {A_v^b} ∪ {B_j^b : t(j)=v}.

Light ℓ 的动作 b 为

    {A_{o(ℓ)}^b} ∪ {B_j^(1-b) : j∈J_ℓ}.

故每个 B_j 只有该 light 和目的 hub 两个潜在使用者；一个 light 可连接多个 hub，各 side 费用可不同，源群组内的 light 权重也可不同。每个 A_v 可有任意多名潜在 light 使用者。模型、真实偏离成本及弱 α-PNE 约定与 MODEL 一致。

令 W_v=Σ_{o(ℓ)=v}w_ℓ。取任意实 α≥T_d，并假设每个 light ℓ 都满足以下**弱统一 aligned-light 强迫**不等式（严格版是其特例）：

    F_v(u_v+w_ℓ) + Σ_{j∈J_ℓ}G_j(w_ℓ)
       ≥ α [F_v(W_v) + Σ_{j∈J_ℓ}G_j(u_{t(j)}+w_ℓ)],   v=o(ℓ).    (UF)

**结论：** 该有限游戏存在 α-PNE，且可选成全部 light 均与其源 hub 反位。Hub 位可通过有限加权割目标的任意局部最小点取得。因此，满足严格 (UF) 的此类有向分叉/异形 side 强迫机制不能在 α≥T_d 证明全状态非存在。

量词：对所有上述有限拓扑、任意正实权、全部非负多项式系数和任意 α≥T_d；不是从某个数值实例或固定人数推出。此结论不涵盖同一 B 资源有多个 hub 潜在使用者、行动副本费用不相同、light 不具有唯一主资源源点、或不满足 (UF) 的真实游戏。尤其不能把它当作全类 O(d/ln d) 上界。

## 一、所需标量不等式

对每个 0≤k≤d 和每个 R>0，有 f_k(R)≤T_d。

当 0<R≤1 时，(1+R)^k≥Σ_{r=0}^k R^r（逐二项系数比较）给 f_k(R)≤1。R=1 和 k=0 时均为 1。对 R>1，把 f_{k+1}−f_k 通分；其正分母对应的分子为

    R(R−1)[(1+R)^k Σ_{r=0}^k R^r − R^k] ≥ 0.

因此 f_k(R)≤f_d(R)≤T_d；k=0 到 k=1 可以等号，之后严格。d≥2 时 T_d>1，但证明只使用 α≥1。

由 α≥f_k(R) 通分，逐单项式再非负线性相加，可得任意非负系数次数≤d 的 P 及任意正 u,w：

    u[P(u+w)−αP(u)] ≤ w[αP(u+w)−P(w)].                  (S)

同理，以 R=W/u，对 W>0 有

    W F(u+W)−α W F(W) ≤ u[αF(u+W)−F(u)].               (M)

这是同一 f_k，但 (S) 使用 R=u/w，(M) 使用 R=W/u。W=0 时 (M) 的左侧为 0，右侧为 u(α−1)F(u)≥0，仍成立。常数项和零多项式均已逐项覆盖；没有取费用商。

## 二、侧边预算与源点总预算

对每个 j，记 ℓ=ℓ(j)、t=t(j)、v=o(ℓ)、w=w_ℓ，定义

    Q_j = G_j(u_t+w)−αG_j(u_t),
    P_j = αG_j(u_t+w)−G_j(w),
    P'_j = αG_j(u_t+w)−G_j(u_t),
    λ_j = u_t max(Q_j,0).

所有系数均已包含在 G_j 中，不另漏乘 amplitude。单调性和 α≥1 给 P_j,P'_j≥0。由 (S) 及 wP_j≥0，

    0≤λ_j≤wP_j.                                       (B1)

又因 P'_j−Q_j=(α−1)[G_j(u_t+w)+G_j(u_t)]≥0，

    λ_j≤u_t P'_j.                                     (B2)

定义 M_v=αF_v(u_v+W_v)−F_v(u_v)≥0。将 (UF) 改写为

    Σ_{j∈J_ℓ}P_j ≤ F_v(u_v+w_ℓ)−αF_v(W_v).

乘 w_ℓ 后对同源 light 求和，利用 w_ℓ≤W_v、F_v 单调以及 (M)，得到

    Σ_{j:o(ℓ(j))=v}λ_j
      ≤ Σ_{ℓ:o(ℓ)=v} w_ℓ Σ_{j∈J_ℓ}P_j
      ≤ Σ_{ℓ:o(ℓ)=v}w_ℓ[F_v(u_v+w_ℓ)−αF_v(W_v)]
      ≤ W_v F_v(u_v+W_v)−αW_v F_v(W_v)
      ≤ u_v M_v.                                      (B3)

W_v=0 时各空和为0，不需要定义单名 light 或除 W_v。多个侧资源都在每名 light 的 ΣP_j 内，不可把同一主资源的 N_ℓ 为每个侧边重复使用。

## 三、加权割引理（含自环）

在 hub 位向量 h∈{0,1}^V 上取

    E(h)=Σ_j λ_j 1_{h_{o(ℓ(j))}=h_{t(j)}}.

有限状态中存在全局最小点；实际上任意单点翻位局部最小点足够。令 ε_j=+1（端点同位）或 −1（端点异位）。自环必有 ε_j=+1，且在翻位时对 E 的贡献不变。

在局部最小 h，翻 v 位产生

    Σ_{j:非自环入v} ε_jλ_j + Σ_{j:非自环出v} ε_jλ_j ≤0.

所以

    Σ_{j:入v} ε_jλ_j ≤ Σ_{j:出v} λ_j.                 (CUT)

这里将自环 λ 同时加到两边即得所写式。侧资源重复端点没有问题，逐索引相加即可。

## 四、真实偏离成本

固定上述 h，让 light ℓ 取 1−h_{o(ℓ)}。这是合法的全反位状态 s。

Light ℓ 的当前主资源负载为 W_v，其侧资源负载逐项不超过 u_t+w；偏离后的主资源负载为 u_v+w，侧资源负载逐项不小于 w。因此

    C_ℓ(s) ≤ F_v(W_v)+Σ_j G_j(u_t+w)
           ≤ [F_v(u_v+w)+Σ_jG_j(w)]/α
           ≤ C_ℓ(偏离)/α.

最后一式直接来自真实新负载；因 α≥1，得到 C_ℓ(s)≤α C_ℓ(偏离)。也可全程乘 α 写而不作除法。零费用不导致 0/0。

Hub v 的主资源当前负载为 u_v，翻位后为 u_v+W_v。侧索引 j 入 v 时，如果源 hub 与 v 同位，当前 B_j 负载 u_v+w，翻位后为 u_v；如果两 hub 异位，两负载相反。自环也属于前一类，因为 light 在 hub 单方偏离时保持原动作。故 hub 的精确 α-改善差 D_v=C_v(s)−αC_v(翻位) 为

    D_v = −M_v + Σ_{入v,ε=+1}Q_j − Σ_{入v,ε=−1}P'_j.

由 λ 定义及 (B2)、(CUT)、(B3)，

    u_v D_v
      ≤ −u_v M_v + Σ_{j:入v} ε_jλ_j
      ≤ −u_v M_v + Σ_{j:出v}λ_j
      ≤0.

u_v>0，所以 D_v≤0。每人仅有另一二进制动作，保留原动作亦自动满足 α≥1 的均衡式，故 s 是 α-PNE。α=T_d 使用的全是弱不等式，无端点间隙假设。

## 状态、回收与接续

这是一个经过内部独立攻击的精确结构存在定理与方法限制：分叉可让一个 light 影响任意多 hub，但多个侧成本共同占用其唯一主资源强迫预算；加权割把全部入反馈压到该出预算内。它没有依赖各源群组存在唯一最小 light 稳定元，所以不受一般分叉的不可比稳定元直接反驳；但 (UF) 是承重假设，不能从真实非存在自动推出。

若要超越当前下界机制，可攻击：不满足 (UF) 的状态覆盖；同一侧资源由多个 hub 共享；action-asymmetric 副本；或让 light 主资源不是唯一源 hub 分组。上述任何改动都需要重新计算真实负载，当前割证明不能直接迁移。

配套审计从原资源集合重新计算费用并枚举小实例；有限枚举只验证实现，不代替本实参数证明。现有资产检索使用 rg 搜索 current/questions/reviews 内 weighted_congestion 的 max-cut / min-cut / 最大割 / 最小割 / 有向图 / 分叉 等关键词，未发现本割推广；不构成外部新颖性检索。


## 审查与可复算合同

- 独立审查：`research/reviews/weighted_congestion/directed_fanout_forcing_cut_review.md`。
- 规范代码：`tests/audits/weighted_congestion/verify_directed_fanout_forcing_cut.py`。
- 冻结结果：`evidence/runs/weighted_congestion/directed_fanout_forcing_cut_audit.json`。

在仓库根运行规范代码，默认stdout；`--output NEW_PATH`独占创建不覆盖旧证据。实际seed、输入生成规则、Python版本、代码哈希和有限覆盖以输出为准。样本的α参数适用域须与包络假设分开核对。

二次样本可取α=6/5：对R>1，把6倍f_2分母减去5倍分子，得R³−4R²+7R+1；令x=R−1>0，该式等于x(x−1/2)²+7x/4+5>0，故T_2≤6/5。这是准确的样本参数前提核验，不是对T_2数值最优点的浮点估计。

三次样本取α=3：3倍f_3分母减去分子为2R⁴+6R²+8R+2>0（R>0），故T_3≤3。

[同权hub共享侧资源推广](shared_side_truncated_potential.md)另给unique-light/source、任意hub子集的UF存在界A_d≤2d/ln d，并抽出AS+B判据。它改变拓扑且收窄hub权，保留独立ID；本稿异权私有side、精确T_d范围不变。
