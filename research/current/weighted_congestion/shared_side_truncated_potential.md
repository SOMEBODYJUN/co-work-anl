# 同权主玩家共享侧资源：统一轻玩家强迫下的截断 Rosenthal 势均衡

本稿为独立推导并完成内部冻结攻击的结构定理；仅讨论下述严格子类，既不是全类存在上界，也不判定 WC-TARGET。没有导入外部定理。统一强迫定理的 Claim ID/version 为 `WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1`；独立的直接预算定理为 `WC-SHARED-SIDE-BUDGET-POTENTIAL-v1`，二者的量词与假设分列，不能静默替换。

## 精确对象和结论

固定整数 d≥2。有限非空 hub 集 V，全部 hub 权重为同一实数 u>0；任意有限 light 集 L（可空），light ℓ 权重 wℓ>0，唯一 source o(ℓ)∈V。每个 source v 的总 light 权为 W_v=Σ_{o(ℓ)=v}wℓ。

每个 hub v 有互异主资源 A_v^0,A_v^1，二者费用同为非负系数次数≤d 多项式 F_v。有限 side 索引集 J；每个 j 指定唯一 light ℓ(j)，以及任意 hub 子集 H_j⊆V。允许 H_j 为空、包含 source、包含全部 hubs，不同 j 的 light/hub 子集完全相同亦可。记 m_j=|H_j|。每个 j 有互异副本资源 B_j^0,B_j^1，费用同为非负系数次数≤d 多项式 G_j。所有资源副本互异。

hub v 的动作 b∈{0,1} 是 {A_v^b}∪{B_j^b:v∈H_j}。light ℓ 的动作 b 是 {A_{o(ℓ)}^b}∪{B_j^{1-b}:ℓ(j)=ℓ}。允许零费用和常数项；每人只有所写两动作。

定义

    A_d = [1−(d−1)d^{−d/(d−1)}]^(−1).

取任意实 α≥A_d。假设每名 light ℓ 满足弱统一 aligned-light 强迫

    F_v(u+wℓ)+Σ_{j:ℓ(j)=ℓ}G_j(wℓ)
      ≥ α[F_v(W_v)+Σ_{j:ℓ(j)=ℓ}G_j(wℓ+m_j u)],  v=o(ℓ).       (UF)

则该有限游戏存在 α-PNE，而且可选成每名 light 的位与其 source hub 相反。下述有限势的任意单 hub 翻位局部最小点均给出这样的状态。弱端点和零费用均直接按成本不等式处理。

范围：任意有限拓扑、实正 u,wℓ、非负实多项式系数和任意 α≥A_d，前提是全部 hub 同权、资源动作副本费用相同、每 side 只有唯一 light、每 light 只有唯一主资源 source，且满足所写最坏侧负载 wℓ+m_j u 的 (UF)。不扩大到异权 hub、共享多个 light 的 side 或 (UF) 失败。A_d≤2d/ln d 对所有 d≥2 成立，但只是这个子类的显式保证。

Dependencies：模型真实单方偏离；非负多项式展开；有限局部最小点；下述自足标量不等式。Evidence：完整证明、先自主重构瓶颈后冻结攻击及两路独立Fraction审计。Counterevidence/Objections：承重范围之外无结论。Status：complete structural proof; independent bottleneck reconstruction and frozen attack; exactly audited; unrefereed。Truth仅所写结构条件；Value为共享侧资源选态接口；Mechanism为截断边际和源重置预算；Ambition保留全类目标OPEN；未外审、未认证新颖性。

## 一、截断 Rosenthal 标量界

对 0≤k≤d 和 x∈[0,1]，

    x−x^k ≤ c_d := (d−1)d^{−d/(d−1)}                 (1)

成立（k=0 时左侧非正；k=1 时为零；k≥2 时 x^k≥x^d，而 x−x^d 的最大值在 x=d^(−1/(d−1))，值恰为 c_d）。α≥A_d 等价于 αc_d≤α−1。因此

    1−αx^k ≤ α(1−x).                              (2)

取 r∈Z_{≥1}、t>0，x=r/(r+t)。由 (2)，

    [(r+t)^k−αr^k]_+ ≤ αt(r+t)^(k−1)
      ≤ αt[(r+t)^k−(r+t−1)^k],                    (3)

其中 k≥1；末步用 y=r+t≥1 和 (1−1/y)^k≤1−1/y。k=0 的左侧为零，单独处理。对任意非负系数多项式 G，利用正部的次可加性、非负线性组合和缩放 t=w/u，得

    [G(w+ru)−αG(ru)]_+
      ≤ α(w/u)[G(w+ru)−G(w+(r−1)u)].              (4)

求和并记

    H_{G,w,u}(m)=Σ_{r=1}^m[G(w+ru)−αG(ru)]_+,

便有对全部整数 m≥0

    0≤H_{G,w,u}(m)
      ≤ α(w/u)[G(w+mu)−G(w)]
      ≤ (w/u)[αG(w+mu)−G(w)].                     (TR)

m=0 时左侧为空和 0，最后右侧为 (w/u)(α−1)G(w)≥0。常数项无需删除。这里的 α≥A_d 不需要先导入 T_d。

特别将 (TR) 取 m=1，base increment=u'=W、external shift=w'=u，便得 W>0 时

    W[F(u+W)−αF(W)]
      ≤ u[αF(u+W)−F(u)].                          (M)

若左侧为负也成立，因为右侧非负；W=0 时直接为 0≤u(α−1)F(u)。因此共享主资源预算不另需 α≥T_d。反过来 (M) 对单项式作全部 u,W 的量词蕴含 α≥T_d，所以 A_d≥T_d 也是本推导的推论，而非未经检查的额外前提。

## 二、全部出侧共用的 source 预算

记

    P_j=αG_j(wℓ+m_j u)−G_j(wℓ)≥0,
    M_v=αF_v(u+W_v)−F_v(u)≥0,
    H_j(m)=H_{G_j,wℓ,u}(m),  ℓ=ℓ(j).

(UF) 改写后，先把每名 light 的全部 side 项相加，再乘 wℓ；同 source 求和，并用 wℓ≤W_v、F_v 单调及 (M)，得

    Σ_{j:o(ℓ(j))=v}H_j(m_j)
      ≤ (1/u)Σ_{ℓ:o(ℓ)=v}wℓ Σ_{j:ℓ(j)=ℓ}P_j
      ≤ (1/u)Σ_{ℓ:o(ℓ)=v}wℓ[F_v(u+wℓ)−αF_v(W_v)]
      ≤ (W_v/u)[F_v(u+W_v)−αF_v(W_v)]
      ≤ M_v.                                      (B)

W_v=0 时各 light/side 和都空，直接使用 M_v≥0。不得为每条 side 重复领取该 light 的完整主资源预算。

## 三、势的精确定义：hub count 和 light 位置分开

对 hub 位向量 h∈{0,1}^V，令 n_{j,b}(h)=|{v∈H_j:h_v=b}|，它只数 hubs、不数 light。令 light ℓ 的位为 1−h_{o(ℓ)}，于是它的 side 副本位为 h_{o(ℓ)}。定义

    R_j(k)=Σ_{r=1}^k G_j(ru),
    E_j(h)=α[R_j(n_{j,0}(h))+R_j(n_{j,1}(h))]
           +H_j(n_{j,h_{o(ℓ(j))}}(h)),
    E(h)=Σ_j E_j(h).                              (E)

当 H_j 为空，E_j=0。有限状态中有局部最小点，无需 α 改善动态终止。

为了核查真实单方偏离，另定义固定 light side 位 q∈{0,1} 的辅助势

    E_j^q(h)=α[R_j(n_{j,0})+R_j(n_{j,1})]+H_j(n_{j,q}).

固定 q 后，在有 light 的副本第 r 名 hub 的势增量为

    αG_j(ru)+[G_j(wℓ+ru)−αG_j(ru)]_+
      = max{αG_j(ru),G_j(wℓ+ru)}.                 (L)

它介于真实该副本费用 G_j(wℓ+ru) 与其 α 倍之间。在无 light 的副本增量为 αG_j(ru)，同样介于真实费用及其 α 倍。故对任意 hub v∈H_j 的真实单方翻位 h→h^v，固定 light 位 q 时，逐 side 的成本差满足

    C_{v,j}(h;q)−αC_{v,j}(h^v;q)
       ≤E_j^q(h)−E_j^q(h^v).                     (D)

这里采用旧副本增量≥旧费用、新副本增量≤α新费用。v∉H_j 时两边都零。此处 light 不随 hub 偏离，是实际博弈的单方偏离。

## 四、source light 重置的势误差

初态全 anti，故 q=h_{o(ℓ(j))}。若 v不是 source，(E) 的 light 位不随 h→h^v 改变，故 (D) 直接适用。

若 v=o(ℓ(j))，真实偏离仍固定 light；但 E(h^v) 在定义上把该 light 重置到新 source 位。两种辅助势之差为

    E_j(h^v)−E_j^q(h^v)
       =H_j(n_{j,1−q}(h^v))−H_j(n_{j,q}(h^v))
       ≤H_j(m_j).                                (R)

这只用 0≤H_j(k)≤H_j(m_j)，且覆盖 source同时属于H_j、source不在H_j、H_j为空；没有把 source翻位误当作 light真的跟随偏离。把 (D)、(R) 对全部 side 求和，得每个 hub

    D_v^side ≤ E(h)−E(h^v)+Σ_{j:o(ℓ(j))=v}H_j(m_j).

## 五、真实均衡检查

选 E 的单 hub 翻位局部最小点 h，让每 light全 anti。

Hub v 的主资源当前负载为 u，真实偏离负载为 u+W_v，所以主资源 α成本差恰为 −M_v。由局部最小性 E(h)−E(h^v)≤0 和 (B)，

    C_v(s)−αC_v(s_v',s_−v)
       ≤−M_v+E(h)−E(h^v)+Σ_{source=v}H_j(m_j)≤0.

Light ℓ 当前主资源负载恰 W_v，每条 side 当前负载至多 wℓ+m_j u；真实翻位后的主资源负载恰 u+wℓ，每条 side 新负载至少 wℓ。因此 (UF) 给

    αC_ℓ(s)≤C_ℓ(s_ℓ',s_−ℓ),

比所需 C_ℓ(s)≤αC_ℓ(s_ℓ',s_−ℓ) 更强。零费用、零偏离费用和空侧集均按弱不等式覆盖，不取费用商。保留原动作由 α≥1 自动成立。故是 α-PNE。

## 六、显式子类常数

令 z=(ln d)/(d−1)>0。因为 c_d=(1−1/d)e^(−z)≤e^(−z)，且 e^z≥1+z，

    A_d≤1/(1−e^(−z))≤1+1/z=1+(d−1)/ln d≤2d/ln d.

最后一步等价于 ln d≤d+1，由标准 ln d≤d−1 即得。故 C=2,d0=2 对本稿子类成立；不能把它当作全模型的 C,d0。

## 审计合同与未解义务

[独立审查](../../reviews/weighted_congestion/shared_side_truncated_potential_review.md)区分先自主重构的瓶颈、阅读冻结机制后的攻击与AS+B新ID的后置抽象审查。程序从真实资源集重建负载，全部使用标准库Fraction，无外部定理或浮点误差。

在仓库根运行：

- `python3 tests/audits/weighted_congestion/verify_shared_side_truncation.py`：作者标量、真实资源、source重置及α=A₂边界；冻结记录`evidence/runs/weighted_congestion/shared_side_truncation/author.json`。
- `python3 tests/audits/weighted_congestion/independent_shared_side_truncation.py`：独立标量、真实资源/势局部最小、空/零/重light边界；冻结记录`evidence/runs/weighted_congestion/shared_side_truncation/independent.json`。
- `python3 tests/audits/weighted_congestion/independent_shared_side_budget.py`：新AS+B假设与UF确有区别的实例和d=0/α=1边界；冻结记录`evidence/runs/weighted_congestion/shared_side_truncation/budget_boundaries.json`。

代码生成规则、seed、精度、参数和运行hash由代码及JSON明确；有限检查不替代实参数一般证明。

下一步须超出当前源预算条件，或控制跨source的真实侧反馈。更一般任意 hub 权、side 多 light、(UF)失效且下述直接预算亦未成立的情形，以及全类状态覆盖仍完全开放。当前结果改变的是“共享多个同权hub side即可逃过私有双人割”的路线边界；不是主目标完成。

## 七、独立 Claim：直接侧势预算充分条件

ID/version：`WC-SHARED-SIDE-BUDGET-POTENTIAL-v1`。

中文数学名称：同权主玩家共享侧资源的直接侧势预算均衡。

Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对第一节之前列出的完全相同有限资源拓扑、唯一 light、唯一 source、同权 hub 对象，将次数域改为任意整数 d≥0，将倍率域改为任意实数 α≥1。使用第二节定义的 H_j(k)、M_v 及第三节的 E(h)，不假设 α≥A_d，也不假设 (UF)。仅要求以下两组条件：

    F_v(W_v)+Σ_{j:ℓ(j)=ℓ}G_j(wℓ+m_j u)
      ≤α[F_v(u+wℓ)+Σ_{j:ℓ(j)=ℓ}G_j(wℓ)]              (AS)

对每名 light ℓ（v=o(ℓ)）；以及

    Σ_{j:o(ℓ(j))=v}H_j(m_j)≤M_v                      (B*)

对每个 source hub v。则 E 的任意单 hub 翻位局部最小点，配以全部 light 反位，都是 α-PNE。允许零费用、常数费用、空 side hub 子集、空 light 集及等号端点。

Dependencies：本稿第三、四节的固定light边际比较与source重置误差，以及有限局部最小点。无需第一节标量 (TR)/(M)，也无需第二节从(UF)推预算。

Proof：第三、四节只用非负费用单调、α≥1 及 H 定义，故在新域原样成立。每个 hub 的真实 α成本差仍不超过 −M_v+E(h)−E(h^v)+Σ_{source=v}H_j(m_j)，由局部最小性与(B*)非正。每名 light 的真实当前成本不超过(AS)左侧，真实偏离成本不小于其右侧括号，故其 α均衡不等式成立。保留原动作自动满足。没有调用次数下界或强迫行为。

Evidence：上述一般证明；已完成新假设和次数域的独立后置抽象审查及非UF实例核验。Counterevidence / Objections：AS与B*仍为承重充分条件，不声称每个该拓扑游戏都能满足；不含多light或异权hub side。Status：complete conditional proof; independently attacked after abstraction; exactly audited; unrefereed；未外审、未认证新颖性。Related Files：本稿第三至五节与配套 Fraction 审计；本Claim的独立后置审查见配套审查末节，UF审查本身不替代该核查。

两个 Claim 的关系：`WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1` 在 d≥2、α≥A_d、(UF) 下，由第一、二节推出(B*)，并由(UF)及α≥1推出(AS)，再调用本直接预算定理。因此是带可识别充分条件的推论。直接预算 Claim 的域更宽，但不提供统一选择AS/B*的方法，更没有去掉全类研究缺口。
