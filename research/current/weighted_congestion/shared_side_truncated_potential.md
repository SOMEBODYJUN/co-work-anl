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

上述旧两Claim未控制跨source的真实侧反馈；第八节另在(UFmulti)下覆盖同权hub的多light跨source side，并给平方根界。任意hub权、UFmulti失败且无可用直接预算的情形，以及全类状态覆盖仍开放。当前结果改变的是“共享多个同权hub side即可逃过私有双人割”的路线边界；不是主目标完成。

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

## 八、新 Claim：跨源多轻玩家共享侧资源的平方根存在界

**ID/version / 中文数学名称：** `WC-MULTISOURCE-SHARED-SIDE-ROSENTHAL-v1`，跨源多轻玩家共享侧资源的统一强迫 Rosenthal 势均衡。此为独立首登身份，不静默修改旧UF/直接预算两个Claim。作者先冻结较弱临时候选，再独立重构并攻击下述更强倍率域；两次freeze和规范diff在新审查中分别记录。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 量化下面全部有限拓扑、正实权u,w、非负实费用系数、整数d≥2及实α≥1+√d；所写(UFmulti)为承重假设。结论为有限势任一单hub局部最小点配全anti lights给α-PNE。允许常数/零费用及所有指定空集合。只覆盖同权hub、唯一main source、二元对称副本和所写最坏负载强迫；异权hub、非对称副本、多main source、强迫失败仍开放。

**Dependencies / Status / Evidence / Objections：** MODEL的真实负载、同权hub离散Rosenthal求和、非负多项式导数及有限最小点；源预算在下文自足，不依赖旧A_d或(M)。完整一般证明、独立先重构后冻结攻击及两路精确审计；未外审/新颖性未认证。Truth限子类；Value为跨source外场重置的可付预算；Mechanism为κ重置和源标量超可加估计；Ambition仍为唯一全类题OPEN。旧奇环下界允许异权hub；本结果不改变其Claim或全类下界。

### 8.1. 精确对象及结论

整数d≥2，全部hub权同为u>0，任意有限非空hub集V，任意有限light集L。每light l正权w_l且唯一source o(l)∈V，W_v=Σ_{o(l)=v}w_l。每source主资源副本A_v^0,A_v^1同费F_v。每side j有副本B_j^0,B_j^1同费G_j，任意hub子集H_j和任意light子集L_j；两个子集均可空。同一light可参加任意多个side，同一side可含多个不同source的light。所有F,G为非负系数次数≤d多项式，副本资源全部互异。设m_j=|H_j|，T_j=Σ_{l∈L_j}w_l。

hub v位b策略为{A_v^b}∪{B_j^b:v∈H_j}；light l位b策略为{A_o(l)^b}∪{B_j^(1-b):l∈L_j}。

取任意实数α≥1+√d。假设每名light满足

 F_v(u+w_l)+Σ_{j:l∈L_j}G_j(w_l)
 ≥α[F_v(W_v)+Σ_{j:l∈L_j}G_j(T_j+m_ju)], v=o(l).  (UFmulti)

结论：存在全anti的α-PNE；特别给出(1+√d)-PNE。α=2d/ln d亦适用于所有整数d≥2。仍有同权hub、对称副本、唯一source、二元动作和UF承重限制，不判定WC-TARGET。

### 8.2. 固定light的真实Rosenthal势

令hub位h∈{0,1}^V，light位固定为1−h_o(l)，即其side副本位h_o(l)。定义

 n_jb(h)=|{v∈H_j:h_v=b}|,
 x_jb(h)=Σ_{l∈L_j:h_o(l)=b}w_l,
 E(h)=Σ_jΣ_{b=0,1}Σ_{r=1}^{n_jb(h)}G_j(x_jb(h)+ru).

固定light side位时，hub在副本中加入/离开的Rosenthal边际等于真实G费用；所以若v翻位h→h^v但light保持旧位，真实side普通成本差等于辅助势差。α成本差不超过普通成本差，因为新成本非负且α≥1。这里没有把真实偏离错当light跟随。

E(h^v)按定义随后把所有source为v的light侧位重置。其移出副本的势改变量≤0；只需支付移入副本的势增加。可任意逐名light重置，各中间侧总light权仍≤T_j。

### 8.3. 逐light重置引理

设κ_d(t)=min{dt,t+1}，t≥0。对任意非负系数次数≤d多项式G，整数n≤m，S≥0、w>0、S+w≤T，

 Σ_{r=1}^n[G(S+w+ru)−G(S+ru)]
 ≤κ_d(w/u)G(T+mu).                                  (R)

证明：m=0时两边非负且左0。设u=1，经变量缩放即可。对0≤x≤Y=T+m，逐项有G'(x)≤dG(Y)/Y。因此左侧≤nw·dG(Y)/Y≤dwG(Y)。另写左侧为Σ_r∫_{S+r}^{S+w+r}G'(x)dx。长度w、起点间距1的区间族的重叠数几乎处处≤ceil(w)≤w+1；且全部积分区间包含于[0,Y]。故左侧≤(w+1)∫_0^YG'(x)dx≤(w+1)G(Y)。取两界最小。常数项的导数为0，无需删除。

于是source v重置势增量至多

 R_v≤Σ_{l:o(l)=v}κ_d(w_l/u)Σ_{j:l∈L_j}G_j(T_j+m_ju).

P_lj=αG_j(T_j+m_ju)−G_j(w_l)≥(α−1)G_j(T_j+m_ju)，因为w_l≤T_j且G单调。
UFmulti给Σ_jP_lj≤F_v(u+w_l)−αF_v(W_v)。所以

 R_v≤1/(α−1) Σ_{l:o(l)=v}κ_d(w_l/u)[F_v(u+w_l)−αF_v(W_v)].       (B0)

每名light所有side同时占用其主预算，没有重复领取。

### 8.4. 源标量预算

对所有有限正t_l、T=Σt_l和非负系数次数≤d多项式F，若α≥1+√d，则

 Σ_lκ_d(t_l)[F(u(1+t_l))−αF(uT)]
 ≤(α−1)[αF(u(1+T))−F(u)].                           (B1)

T=0对应无light，左0，右≥0。以下T>0。

若T≤1：κ_d(t)≤dt，F单调，丢负项给左≤dT F(u(1+T))≤dF(u(1+T))。右≥(α−1)^2F(u(1+T))≥dF(u(1+T))。

若T≥1：逐单项式证明。固定k∈{0,…,d}。κ_d凹、κ_d(0)=0，因此Σκ_d(t_l)≥κ_d(T)。k≥1时函数f_k(t)=κ_d(t)[(1+t)^k−1]超可加，因为f_k(t)/t单调：t≤1/(d−1)时为d[(1+t)^k−1]；t≥1/(d−1)时为Σ_{r=1}^k binom(k,r)(t^r+t^(r−1))，均单调且接点连续。故Σf_k(t_l)≤f_k(T)。k=0时f=0，亦然。

由于1−αT^k≤0，

 Σκ(t_l)[(1+t_l)^k−αT^k]
 =Σf_k(t_l)+(1−αT^k)Σκ(t_l)
 ≤κ(T)[(1+T)^k−αT^k].                              (B2)

若方括号非正，已≤0；否则用α≥1和κ(T)≤T+1：

 κ(T)[(1+T)^k−αT^k]
 ≤(T+1)[(1+T)^k−T^k]
 =(1+T)^(k+1)[1−(T/(1+T))^k]
 ≤k(1+T)^k≤d(1+T)^k.

末步用1−x^k≤k(1−x)，0≤x≤1（几何级数）；k=0方括号非正已单独覆盖。逐非负线性组合并乘u^k，左侧≤dF(u(1+T))。右侧≥(α−1)^2F(u(1+T))≥dF(u(1+T))，即(B1)。没有使用A_d或旧稿(M)。

(B0)+(B1)给R_v≤M_v:=αF_v(u+W_v)−F_v(u)。

### 8.5. 真实PNE核查

E在有限hub状态空间有单hub翻位局部最小点h。令所有light anti。hub v主资源当前负载u，真实偏离后u+W_v，α成本差−M_v；side α成本差≤E(h)−E(h^v)+R_v。因此总α成本差≤−M_v+0+R_v≤0。

light l当前主资源负载W_v，每条side当前负载≤T_j+m_ju；偏离后主资源负载u+w_l，每条side新负载≥w_l。UFmulti给αC_l(s)≤C_l(dev)，蕴含α-PNE式。零费和端点按不等式处理，无任何0/0。

### 8.6. 显式倍率和范围

本稿直接给α=1+√d。若需与目标量级比较，ln d≤√d（例如log x/√x在e²处最大2/e<1），故2d/ln d≥2√d≥1+√d。没有把本子类推广为全类；UFmulti、同权hub等假设仍承重。d≥2为本Claim固定域；主证明实际上只需d≥1，未声明扩大次数域。零费用、F常数、G常数、空L、空side的H或L、source同时属于H、source没有light均由上面非负和空和解释覆盖。


### 8.7. 审查与精确核验合同

- 作者：`python3 tests/audits/weighted_congestion/verify_multisource_shared_side.py`；冻结结果`evidence/runs/weighted_congestion/shared_side_truncation/multisource_author.json`。
- 独立：`python3 tests/audits/weighted_congestion/independent_multisource_shared_side.py`；冻结结果`evidence/runs/weighted_congestion/shared_side_truncation/multisource_independent.json`。
- [独立重构与冻结攻击](../../reviews/weighted_congestion/multisource_shared_side_review.md)单独审查本新ID，旧UF审查不能代替。

两份审计均只向stdout写JSON，保留真实生成参数、seed（适用时）、有理倍率、Python及源码hash；从literal资源重新计算偏离，包含非单位hub权、跨source、多light、空H/L、零常数、source在side及source无light边界。阈值前提以(α−1)²≥d精确检查，不用浮点舍入充当证明。重跑另存临时路径，不原位覆盖冻结证据。


## 九、新 Claim：轻玩家强迫倍率与目标均衡倍率的分离

**ID/version / 中文数学名称：** `WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v1`，跨源共享侧资源的强迫与目标倍率乘积预算均衡。此为新 Claim；第一、七、八节的三个既有 Claim 及其域和假设保持不变。它把第八节同一机制中的两个倍率分开，不能解读为删去强迫假设。

### 9.1. 精确身份与冻结陈述

**Objects / Domain / Quantifiers / Definitions / Assumptions：** 量化第8.1节的全部有限对象：有限非空 hub 集、同一实正 hub 权重 `u`；有限 light 集、各自实正权重与唯一 main source；每 source 的两个同费主资源副本；任意同费 side 副本对及任意 hub/light 用户子集；非负实系数、次数至多整数 `d≥2` 的全部 `F_v,G_j`。全部资源策略、`W_v,m_j,T_j` 及全 anti 形状沿用第8.1节精确定义。另量化任意实数

    τ>1,  α≥1,  (τ−1)(α−1)≥d.                         (FT)

对每名 light l，v=o(l)，假设

    F_v(u+w_l)+Σ_{j:l∈L_j}G_j(w_l)
      ≥τ[F_v(W_v)+Σ_{j:l∈L_j}G_j(T_j+m_j u)].         (UFτ)

**Exact Statement / Scope / Conclusion：** 第8.2节定义的有限势 `E` 的每个单 hub 翻位局部最小点，配以全部 light 与各自 source 反位，均为原真实负载博弈的 `α-PNE`。不要求 `τ≤α`、`τ=α` 或 `τ≥α`；两个倍率的大小顺序均可。结论覆盖弱等号、零费用、常数费用、空 light 集、空 side 用户子集、source 属于 side hub 集以及同一 side 含不同 source 的多名 light。

**Dependencies：** MODEL 的真实单方偏离，第8.2节的固定 light 普通 Rosenthal 边际恒等式，第8.3节逐 light 重置界，以及下文对任意 `τ>1` 的源标量引理；有限状态局部最小点。不调用第八节以 `τ=α` 表示的结论，不调用外部均衡定理。

**Evidence / Counterevidence / Objections / Status：** 本节给出完整一般推导；独立审查、实际代码与冻结证据的状态由配套审查和账本分别记录，不由本节文字预设。`UFτ`、同权 hub、唯一 main source、二元同费副本仍是承重假设；`τ=1` 没有被除法或极限纳入。没有证明任意游戏存在满足这些条件的表示，亦未解决全类 WC-TARGET。Truth 仅指所写子类；Value 为可单独量化强迫和目标余量；Mechanism 为 source 重置预算的乘积支付；Novelty/外审未认证。

### 9.2. 任意强迫倍率的源标量引理

设有限正数列 `t_l`，`T=Σ_l t_l`；允许空列 `T=0`。记 `κ_d(t)=min(dt,t+1)`。对任意 `τ≥1`、`u>0` 及非负系数次数至多 `d` 的多项式 `F`，

    Σ_l κ_d(t_l)[F(u(1+t_l))−τF(uT)]
       ≤d F(u(1+T)).                                (Sτ)

证明直接给出全部量词，不假定源预算中的每个括号非负。空列时左侧零，结论成立。若 `0<T≤1`，用 `κ_d(t_l)≤dt_l`、单调性并丢弃非正项，左侧至多

    Σ_l dt_l F(u(1+T))=dT F(u(1+T))≤dF(u(1+T)).

若 `T≥1`，逐单项式处理。固定整数 `0≤k≤d`。`κ_d` 凹且在零点为零，故

    Σ_l κ_d(t_l)≥κ_d(T).                             (C)

对 `k≥1`，函数 `f_k(t)=κ_d(t)((1+t)^k−1)` 超可加：在 `t>0`，其比值 `f_k(t)/t` 在 `t≤1/(d−1)` 时为 `d((1+t)^k−1)`，在 `t≥1/(d−1)` 时为

    Σ_{r=1}^k binom(k,r)(t^r+t^(r−1)).

两段均单调不减且接点连续。因此 `f_k(t_l)≤(t_l/T)f_k(T)`，相加即得 `Σ_l f_k(t_l)≤f_k(T)`。`k=0` 时 `f_k` 恒零。因为 `1−τT^k≤0`，由(C)得

    Σ_lκ_d(t_l)[(1+t_l)^k−τT^k]
      ≤κ_d(T)[(1+T)^k−τT^k].                         (S1)

若右侧括号非正，已经得到(Sτ)的单项式版本。否则 `k≥1`，用 `τ≥1`、`κ_d(T)≤T+1` 和几何级数界 `1−x^k≤k(1−x)`，有

    κ_d(T)[(1+T)^k−τT^k]
      ≤(T+1)[(1+T)^k−T^k]
      =(1+T)^(k+1)[1−(T/(1+T))^k]
      ≤k(1+T)^k≤d(1+T)^k.

乘 `u^k` 后对非负系数相加，证明(Sτ)。常数项 `k=0` 的左侧非正，不需删除费用常数。

### 9.3. 从强迫预算支付真实重置

对每名 light l，定义 `Y_j=T_j+m_j u` 及

    P_lj=τG_j(Y_j)−G_j(w_l),
    Q_l=F_v(u+w_l)−τF_v(W_v),  v=o(l).

因为 `w_l≤Y_j`、费用单调且 `τ>1`，

    P_lj≥(τ−1)G_j(Y_j)≥0,
    Σ_{j:l∈L_j}P_lj≤Q_l,                            (P)

其中第二式恰为(UFτ)。特别地每个 `Q_l≥0`，但源标量引理本身不需要这个附加事实。第8.3节在真实 hub 翻位后逐 light 重置，给 source v 的势增加上界

    R_v≤Σ_{l:o(l)=v}κ_d(w_l/u)Σ_{j:l∈L_j}G_j(Y_j)
       ≤1/(τ−1) Σ_{l:o(l)=v}κ_d(w_l/u)Q_l
       ≤d/(τ−1) F_v(u+W_v).                         (Rτ)

一次 light 的全部 side 费用先求和后领取其主资源预算；没有逐 side 重复领取同一 `Q_l`。由(FT)及 `F_v(u)≤F_v(u+W_v)`，

    R_v≤(α−1)F_v(u+W_v)
       ≤αF_v(u+W_v)−F_v(u)=M_v(α).                 (Bτα)

无 light 的 source 直接有 `R_v=0≤M_v(α)`。即使全部费用为零也不作费用比值或 `0/0`。

### 9.4. 真实单方偏离与有限选态

在有限 hub 位空间中取 `E` 的任意单翻位局部最小点 h，全 light 按定义反位。hub v 真实偏离时 light 保持旧动作。固定 light 的侧费用普通差等于辅助势差，而真实 `α` 侧成本差不大于普通差，因为 `α≥1` 且偏离成本非负。其后仅在势的比较中将 v 的 light 重置，使用(Rτ)，所以

    C_v(s)−αC_v(s_v',s_−v)
      ≤−M_v(α)+E(h)−E(h^v)+R_v≤0.

这里的重置是势的定义比较，不是允许 light 在真实 hub 单方偏离中同时移动。

对 light l，当前主资源负载恰为 `W_v`，每条当前 side 负载不超过 `Y_j`；真实翻位后的主资源负载为 `u+w_l`，每条新 side 负载至少 `w_l`。因此(UFτ)直接给

    τ C_l(s)≤C_l(s_l',s_−l).

它蕴含 `C_l(s)≤αC_l(s_l',s_−l)`，只需 `τ>1,α≥1`，不需两个倍率间再有排序。保留原动作由 `α≥1` 自动满足。故原游戏的全部合法单方偏离都满足 `α-PNE` 不等式。

取 `τ=α=1+√d` 恰恢复第八节的条件与结论，但本 Claim 的量词还允许不同倍率，因此以新身份登记。

### 9.5. 目标量级的显式子类推论

对每个整数 `d≥16`，取

    τ=1+ln d,  α=1+d/ln d.

余量乘积恰为 `d`，故满足(UFτ)的上述子类具有 `α-PNE`。又 `ln d≤d`，故

    α≤2d/ln d.

因此在该子类，轻玩家只须满足对数级的统一强迫倍率即可保证目标量级。此推论仍量化全部该子类实例，常数不依赖人数、权重或费用系数；它没有覆盖(UFτ)失败或异权 hub 的一般游戏，也不是全类题目的 `C=2,d0=16` 结论。

### 9.6. 核验接口

作者精确审计：

    python3 tests/audits/weighted_congestion/verify_multisource_forcing_target_tradeoff.py

程序只向 stdout 输出 JSON，逐资源重建真实负载与单方偏离，用标准库 `Fraction` 检查(FT)、(UFτ)、固定 light Rosenthal 恒等式、source 重置上界及势局部最小点。它还包含 `τ<α`、`τ>α`、`τ=α`、`τ` 接近一的有理端点、零/常数费用、无 light/空用户子集，以及满足(UFτ)但不满足以 `α` 替换 `τ` 的强迫式的实例。完整参数、seed、Python 和代码 hash 随 JSON 输出；有限证据不替代本节的实参数证明。

### 9.7. 独立攻击、冻结结果与接续义务

[独立审查](../../reviews/weighted_congestion/multisource_force_tradeoff_review.md)先仅据精确陈述重构源预算，再攻击冻结第九节，记录所审 hash、倍率无序关系、真实偏离与重置的区别及全部承重条件。独立程序不调用作者实现：

    python3 tests/audits/weighted_congestion/independent_multisource_force_tradeoff.py

两路冻结结果分别为 `evidence/runs/weighted_congestion/shared_side_truncation/forcing_target_author.json` 与 `evidence/runs/weighted_congestion/shared_side_truncation/multisource_force_tradeoff_independent.json`。每份记录列实际生成输入、参数、seed、算术、版本、源码 hash 与有限覆盖范围；重跑仅向 stdout 或临时文件输出，不覆盖冻结字节。代码和结果由 `research/assets.json`、`research/catalog.json` 接入。

本 Claim 的一般证明已完成独立重构与冻结攻击，精确审计通过；状态为 complete conditional proof; independently reconstructed and exactly audited; unrefereed。它降低的是达到目标量级时所需的强迫倍率，未提供一般实例的强迫表示或稳定 light 选择。下一项承重义务仍是异权 hub、强迫失败时的反馈控制或无界交互高度的非势选态；全类题保持 OPEN。
