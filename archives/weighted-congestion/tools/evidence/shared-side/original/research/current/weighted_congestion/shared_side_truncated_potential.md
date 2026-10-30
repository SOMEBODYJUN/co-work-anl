# 共享侧资源的强迫均衡：同权截断势与异权排序势

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

### 9.8. 新版本：保留主资源增量后的加强倍率域

**ID/version / 中文数学名称：** `WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v2`，跨源共享侧资源的主增量支付与精确均衡强迫阈值。此版本更改了 v1 的倍率假设，独立列出精确身份；v1 正文、原冻结审计和原审查不因此改写。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 量化第9.1节完全相同的全部有限资源拓扑、任意实正 hub 同权 `u`、任意实正 light 权、唯一 main source、非负系数次数至多整数 `d≥2` 的多项式费用与任意实 `τ>1,α≥1`，保持同一个(UFτ)，将倍率条件改为

    α(τ−1)≥d.                                        (FT2)

结论不变：第8.2节同一有限势 `E` 的每个单 hub 翻位局部最小点，配以全部 light 与 source 反位，是原真实负载游戏的 `α-PNE`。允许所有此前所列零/常数费用和空用户子集边界。特别允许 `α=1`，没有将 `τ=1` 纳入量词域。

**Dependencies：** 第8.2—8.3节固定 light Rosenthal 边际和逐 light 重置引理，第9.3节从(UFτ)得到(P)的预算接口，以及下述新的主增量源标量引理。一般证明不调用 v1 的结论，不调用外部均衡定理。

**Evidence / Counterevidence / Objections / Status：** 下文给出完整一般推导；审查和精确证据的状态另行记录，不由作者候选预设。同权 hub、唯一 source、二元同费副本和(UFτ)均承重；没有覆盖异权 hub、强迫失败或一般游戏的选态。未外审、新颖性未认证。此版本扩大可保证的参数域，不声称(FT2)是该结构类中必要或最优的均衡判据。

### 9.9. 主增量源标量引理

对任意有限正数列 `t_l`、`T=Σ_l t_l`（允许空列）、`u>0`、整数 `d≥2`、实数 `τ≥1` 与非负系数次数至多 `d` 的多项式 F，有

    Σ_lκ_d(t_l)[F(u(1+t_l))−τF(uT)]
      ≤d[F(u(1+T))−F(u)].                            (SΔ)

证明：空列时两边零。左侧随 `τ` 单调不增，只需证 `τ=1`。逐单项式证明；常数项 `k=0` 在 `τ=1` 时为零，在更大 `τ` 时非正。以下 `1≤k≤d`，先令 `u=1`，最后乘 `u^k` 并非负线性组合。

若 `0<T≤1`，每个 `(1+t_l)^k−T^k≥0`，用 `κ_d(t_l)≤dt_l` 得

    Σ_lκ_d(t_l)[(1+t_l)^k−T^k]
      ≤dT[(1+T)^k−T^k]
      ≤d[(1+T)^k−1].                                (D1)

末步在 `T=1` 时取等号；在 `0<T<1` 时等价于

    (1+T)^k≥(1−T^(k+1))/(1−T)=Σ_{r=0}^k T^r,

由二项式系数均至少一成立。

若 `T≥1`，复用第9.2节(C)及 `f_k(t)/t` 单调的超可加证明（它不含强迫倍率），将和压成

    Σ_lκ_d(t_l)[(1+t_l)^k−T^k]
      ≤κ_d(T)[(1+T)^k−T^k].                         (D2)

`k=1` 时右侧为 `κ_d(T)≤T+1≤dT`，即所需界。若 `k≥2`，记 `x=T/(1+T)∈[1/2,1)`。递减等比数列的均值满足

    (1/k)Σ_{r=0}^{k−1}x^r≤(1+x)/2.

具体可由 `Σx^r≤1+(k−1)x` 和 `(k−2)(1−x)≥0` 验证。另由 `k≥2` 及

    2x−x²−(1+x)/2=(2x−1)(1−x)/2≥0,

有 `1−(1−x)^k≥2x−x²≥(1+x)/2`。因此

    Σ_{r=0}^{k−1}x^r≤k[1−(1−x)^k].

乘 `(1+T)^k` 并用 `1−x=1/(1+T)`，得到

    (T+1)[(T+1)^k−T^k]≤k[(T+1)^k−1].              (GΔ)

由 `κ_d(T)≤T+1` 及 `k≤d`，(D2)至多 `d[(1+T)^k−1]`。完成单项式、缩放和非负线性组合证明。源标量引理没有使用(UFτ)，也不要求各 light 的源括号分别非负。

### 9.10. 保留主资源增量的付款与真实均衡

仍定义 `Q_l=F_v(u+w_l)−τF_v(W_v)`。由第9.3节(P)和第8.3节逐 light 重置界，source v 的全部重置满足

    R_v≤1/(τ−1)Σ_{l:o(l)=v}κ_d(w_l/u)Q_l
       ≤r Δ_v,
    r=d/(τ−1),  Δ_v=F_v(u+W_v)−F_v(u)≥0.           (RΔ)

若 source 无 light，`R_v=Δ_v=0`。主资源真实 `α` 成本差仍为

    −M_v(α),   M_v(α)=αF_v(u+W_v)−F_v(u).

若 `r≤1`，直接有 `R_v≤rΔ_v≤Δ_v≤M_v(α)`。若 `r≥1`，(FT2)给 `α≥r`，且

    M_v(α)−rΔ_v
      =(α−r)F_v(u+W_v)+(r−1)F_v(u)≥0.              (Pay2)

所以两种分支均支付全部重置。取 E 的任一单 hub 局部最小点；真实 hub 偏离保持 light 动作不变，只在比较势时重置该 source 的 light。逐 hub 有

    C_v(s)−αC_v(s_v',s_−v)
      ≤−M_v(α)+E(h)−E(h^v)+R_v≤0.

每名 light 仍由(UFτ)满足 `τC_l(s)≤C_l(s_l',s_−l)`，它对全部 `α≥1` 蕴含目标均衡不等式。常数费用通过非负主预算处理；零成本与零偏离成本直接用不等式处理，不计算费用比值。全部真实单方偏离均已覆盖，证明 v2。

### 9.11. 精确均衡阈值、目标推论及版本关系

在本严格子类中：

- 若 `τ≥d+1`，取 `α=1` 满足(FT2)，同一势局部最小点给**精确纯 Nash 均衡**。
- 若 `τ=1+ln d`，取 `α=max{1,d/ln d}` 满足(FT2)。特别地 `d≥16` 时 `α=d/ln d>1`，给目标量级。

这两个结论都要求原文(UFτ)及全部结构假设。第一个结论不声称一般加权拥塞博弈存在精确均衡；第二个结论不解决全类匹配上界。

v1 的 `(τ−1)(α−1)≥d` 蕴含 v2 的 `α(τ−1)≥d`，故 v2 保留并严格扩展已保证的参数域。例如 `d=4,τ=5,α=1` 满足 v2 却不满足 v1；非零多 light 跨 source 实例也可满足此强迫式，配套审计提供显式有理参数。所谓严格扩展指充分条件的参数域严格扩大，不声称旧域以外曾无均衡。

### 9.12. v2 作者精确审计合同

运行

    python3 tests/audits/weighted_congestion/verify_multisource_forcing_exact_threshold.py

程序检查新(SΔ)、(FT2)、两种付款分支、真实固定 light 偏离与重置，并枚举 E 的全部单 hub 局部最小点；必须实际包含 `τ=d+1` 和 `τ>d+1`、`α=1` 的非零、多 source、多 light 共享 side 实例。该审计复用 v1 作者程序的真实资源重建与输入生成函数，输出所用依赖源码 hash，并不自称独立实现。v1 审计和冻结证据保持原字节；新运行另存新证据文件。有限审计仅核对实际参数，不替代实参数一般证明。

### 9.13. v2 独立攻击与冻结结果

[v2 独立审查](../../reviews/weighted_congestion/multisource_force_increment_review.md)先据加强陈述重构源增量界，再逐式攻击冻结9.8—9.12，记录所审版本/hash，核对 `α=1` 的非零跨源实例及其与 v1 的域关系。新独立程序为

    python3 tests/audits/weighted_congestion/independent_multisource_force_increment.py

该程序由审查者自己的 v1 literal 实现派生，独立于作者，运行时不导入任何 baseline；JSON 明列 baseline 路径/hash。两路新冻结结果为 `evidence/runs/weighted_congestion/shared_side_truncation/forcing_exact_threshold_author.json` 与 `evidence/runs/weighted_congestion/shared_side_truncation/multisource_force_increment_independent.json`，包括全部实际输入、参数、seed、Python/代码/依赖 hash。重跑保存到 stdout 或临时路径，不覆盖冻结结果。

v2 状态为 complete conditional proof; independently reconstructed and exactly audited; unrefereed。没有范围内尚成立的 fatal objection；未外审、新颖性未认证。主增量付款及精确均衡端点仍只覆盖所写强迫与同权结构；全类 WC-TARGET 保持 OPEN。

### 9.14. 新版本：重置增量与强迫倍率乘积

**ID/version / 中文数学名称：** `WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v3`，跨源共享侧资源的重置增量与强迫乘积预算均衡。此版本再次扩大倍率域；v1/v2 的原正文、审查与冻结证据保持原字节。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 量化第9.1节完全相同的全部有限资源拓扑、任意实正共同 hub 权 `u`、任意实正 light 权、唯一 main source、二元同费副本和非负系数次数至多整数 `d≥2` 的多项式费用；策略、`W_v,m_j,T_j` 和全 anti 形状均不变。保持同一(UFτ)，但现在量化

    τ≥1,  α≥1,  ατ≥d.                               (FT3)

结论是第8.2节同一有限势 E 的每个单 hub 翻位局部最小点配全 anti 均为真实 `α-PNE`。不要求两个倍率排序。允许 `τ=1`，特别 `τ≥d` 可以取 `α=1`。这仍是条件子类的充分保证，不声称整个乘积条件对 `α>1` 必要或最优。

**Dependencies / Evidence / Counterevidence / Objections / Status：** 固定 light 的真实等权 hub Rosenthal 边际、第9.9节主增量源标量引理(SΔ)、下面新的重置增量引理，以及有限局部最小点。没有调用 v1/v2 的均衡结论或外部均衡定理。本文给出完整一般推导；独立冻结攻击和精确证据另记。同权 hub、唯一 source、对称副本和(UFτ)仍全部承重，没有一般游戏的强迫表示或全类存在性结论；未外审，新颖性未认证。

### 9.15. 逐 light 的重置增量引理

设非负系数次数至多 d 多项式 G，`u>0,w>0,S≥0,T≥S+w`，整数 `0≤n≤m`，`Y=T+mu`。则

    Σ_{r=1}^n[G(S+w+ru)−G(S+ru)]
      ≤κ_d(w/u)[G(Y)−G(w)],  κ_d(t)=min{dt,t+1}.     (RI)

先处理 `n=0`：左侧为零，`Y≥w` 使右侧非负；同时覆盖 `m=0,Y=w`，无需除法。以下 `n≥1`，于是 `Y−w≥mu≥nu>0`。常数 G 时两边都零；一般非负系数多项式满足 `G'≥0` 且 G' 在非负半轴不减。

第一界：对 `k≥1`，`Y^k−w^k≥(Y−w)Y^(k−1)`；逐非负系数展开，对全部 `0≤x≤Y` 有

    G'(x)≤d[G(Y)−G(w)]/(Y−w).

全部 n 个积分区间 `[S+ru,S+w+ru]` 长度均为 w，包含于 `[0,Y]`。因此原和不超过

    nw · d[G(Y)−G(w)]/(Y−w)
      ≤d(w/u)[G(Y)−G(w)].                           (RIa)

第二界：令 `a=w/u+1`，c(x) 为这 n 个区间的覆盖密度。几乎处处 `0≤c≤ceil(w/u)≤a`，且 `∫_0^Y c=nw`。又

    a(Y−w)≥(w/u+1)nu=n(w+u)≥nw.

原区间可以穿过 w，不能直接说积分只位于 `[w,Y]`。令 `q=G'(w)≥0`，利用 G' 非减和 `a−c≥0`，

    ∫_0^w cG'≤q∫_0^w c,
    ∫_w^Y(a−c)G'≥q∫_w^Y(a−c).

相减得

    ∫_0^Y cG'−a∫_w^Y G'
      ≤q[nw−a(Y−w)]≤0.

所以原和至多

    (w/u+1)[G(Y)−G(w)].                              (RIb)

结合两界得(RI)。这是将 w 以下的原密度质量由 w 以上的剩余容量支付，依赖凸导数而非错误的区间位置假设。非单位 u、`w≫u,T=w,n=m` 及常数项均在所写量词中覆盖。

### 9.16. 不除以强迫余量的付款与真实均衡

固定 light 后，hub 的普通 side 成本差仍等于 Rosenthal 辅助势差。仅在势比较中逐名重置该 source 的 light；移出副本不增加势，移入副本使用(RI)，其余 light 总权 S 始终满足 `S+w≤T_j`。因此每名 light 对每条 side 的 reset 至多 `κ_d(w_l/u)[G_j(Y_j)−G_j(w_l)]`，`Y_j=T_j+m_j u`。

定义 `P_lj=τG_j(Y_j)−G_j(w_l)`、`Q_l=F_v(u+w_l)−τF_v(W_v)`，v=o(l)。因为 `τ≥1`，

    P_lj≥τ[G_j(Y_j)−G_j(w_l)]≥0,
    Σ_{j:l∈L_j}P_lj≤Q_l.                            (P3)

第二式恰是(UFτ)。先汇总每名 light 的全部 side 再领取一次源预算，没有重复领取。故 source v 的全部 reset 满足

    R_v≤(1/τ)Σ_{l:o(l)=v}κ_d(w_l/u)Q_l
       ≤(d/τ)[F_v(u+W_v)−F_v(u)],                   (R3)

末步为第9.9节(SΔ)，它本来就允许 `τ=1`。这里只除以正数 τ，没有除以 `τ−1`。无 light 的 source 两个增量都为零。由(FT3)、费用单调和 `α≥1`，

    R_v≤α[F_v(u+W_v)−F_v(u)]
       ≤αF_v(u+W_v)−F_v(u)=M_v(α).                 (Pay3)

取 E 的任一单 hub 局部最小点 h，配全 anti。hub v 真实偏离保持 light 不动，主资源 α 成本差为 `−M_v(α)`；side α 差不超过普通差。再用仅供势比较的 reset，得到

    C_v(s)−αC_v(dev)
      ≤−M_v(α)+E(h)−E(h^v)+R_v≤0.

Light 当前主负载 `W_v`、每条 side 至多 `Y_j`；偏离后主负载 `u+w_l`、每条 side 至少 `w_l`。原(UFτ)给 `τC_l(s)≤C_l(dev)`，在 `τ=1` 也足以推出全部 `α≥1` 的均衡式。保留原动作自动满足；每人仅有两个合法动作，全部真实偏离已覆盖。空集合、零/常数费用与零偏离成本均直接按不等式处理。完成 v3。

因此本子类中 `τ≥d` 给精确 PNE，`τ=1` 给 d-PNE；若 `d≥16,τ=ln d,α=d/ln d`，也满足(FT3)。这些推论全部保留(UFτ)及结构假设，不是全类题目的结论。v2 的条件蕴含 v3；参数域真扩大，例如 `d=2,τ=2,α=1` 满足 v3 而不满足 v2。

### 9.17. 独立 Claim：精确强迫边界的四状态反例

**ID/version / 中文数学名称：** `WC-SHARED-SIDE-EXACT-FORCING-THRESHOLD-v1`，共享侧资源的精确纯均衡统一强迫边界。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 固定任意整数 d≥2，在第9.14节完全相同的结构类和(UFτ)下：(a) 每个 `τ≥d` 的游戏存在精确 PNE；(b) 对每个实数 `1≤τ<d`，存在该结构类的有限游戏，严格满足全部(UFτ)，而每个纯状态均有严格改善出口，所以没有精确 PNE。因此 d 是本结构类保证精确 PNE 的统一强迫参数边界。这个“边界”不指 `α>1` 的最优乘积条件，不提供全类渐近下界或全类目标否定。

**Dependencies / Evidence / Counterevidence / Objections / Status：** (a) 由 v3 取 α=1；(b) 由下面显式两玩家构造及全部四状态覆盖证明。两个 Claim 分开登记，完整证明、独立攻击与精确核验状态分轴记载。未外审、未认证新颖性。

给定 `1≤τ<d`，定义

    ε=d−τ>0,
    K=τ(2^d−1)+d(τ−1)>0,
    t=ε/(2K),  D=1−(τ−1)t,
    A=[τ(1+t)^d−t^d]/D,
    a=(A+d)/2.

一名 hub 权 u=1，一名 source 为该 hub 的 light 权 w=t。两个主副本费用 `F(x)=ax`；一个 side 副本对费用 `G(x)=x^d`，其 `H={hub},L={light}`。Hub 位 b 用 `{A^b,B^b}`，light 位 b 用 `{A^b,B^(1−b)}`。资源互异，费用次数至多 d，属于模型。

先有 `K≥2^d−1≥d` 和 `0<ε≤d−1`，故 `0<t<1/2`；又 `K≥d(τ−1)`，所以 `(τ−1)t≤ε/(2d)<1/2`，`D>1/2`，包括 τ=1。分子正，故 A>0。二项式展开在 `t≤1` 时给 `(1+t)^d≤1+(2^d−1)t`，因此

    τ(1+t)^d−t^d−dD
      ≤−ε+[τ(2^d−1)+d(τ−1)]t
      =−ε/2<0.

于是 `0<A<a<d`。直接计算本实例强迫差：

    a(1+t)+t^d−τ[at+(1+t)^d]
      =(a−A)D>0.                                   (StrictUF)

该式正是严格(UFτ)，在 τ=1 也严格。

若 hub/light 两位 aligned，light 当前费用为 `a(1+t)+t^d`，真实翻位后为 `at+(1+t)^d`。由(StrictUF)及 `τ≥1`，light 严格改善。若两位 anti，hub 当前费用为 `a+(1+t)^d`，真实翻位后为 `a(1+t)+1`。二项式展开给

    (1+t)^d−1≥dt>at,

所以 hub 严格改善。全部四状态恰好分成这两类，没有遗漏循环外状态。这里 main 一次、side d 次是合法的混合多项式输入；只证明无精确 PNE，不把改善幅度趋近一偷换成任何固定 α>1 的反例。

### 9.18. v3 与精确强迫边界的审查和审计合同

[独立审查的 v3 追加节](../../reviews/weighted_congestion/multisource_force_increment_review.md)记录实际角色：原审查者提出重置增量加强，原作者先只据引理及精确陈述自主重构，再攻击冻结9.14—9.17，并给另一条离散积分证明。主研究者另核对密度容量、真实付款和两玩家全部实参数边界。所审新节 hash 保持；同步加入第十节和更改总标题不改变这段数学字节。

运行两份新程序，只向 stdout 输出 JSON：

- `python3 tests/audits/weighted_congestion/verify_multisource_reset_increment.py`，冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/reset_increment_author.json`。明确复用 v1 作者 literal helper 并记录依赖 hash；另检查重置引理的参数网格和两玩家全部四状态。
- `python3 tests/audits/weighted_congestion/independent_multisource_reset_increment.py`，冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/reset_increment_independent.json`。独立于原作者实现，由其本人 v2 独立 baseline 派生 standalone，记录来源 hash，未调用作者核心。

全部有限输入、参数、seed、Python/源码/helper 或 baseline hash 和确审稿 hash 随各自 JSON 固定。重跑另存临时位置，不覆盖任何 v1/v2/v3 冻结证据。计算只核实现与实际边界，不替代上述一般证明。

v3 与独立 exact 强迫边界均已完成一般证明、独立重构、冻结攻击和两路精确核验；无范围内尚成立的 fatal objection，未外审、未认证新颖性。精确边界只限 `α=1`，主目标的全类 `Cd/ln d` 判定保持 OPEN。下一项承重义务是低于对数级强迫或强迫失败时的选态、无界异权比下的控制，或新的全状态增长机制。

## 十、新 Claim：局部异权 hub 的降序侧势与源重置预算

**ID/version / 中文数学名称：** `WC-HETEROGENEOUS-HUB-SORTED-SIDE-v1`，局部异权主玩家共享侧资源的排序势均衡。独立身份；第八节同权 Claim 的对象和结论均不改。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 固定任意整数 d≥2。采用8.1的全部有限拓扑和二元同费资源副本，但每名hub v有任意正实权 a_v，而非共同u。light正权w_l、唯一source o(l)、各主费用F_v及侧费用G_j仍为非负系数次数≤d。记

    U_j=Σ_(v∈H_j) a_v,  T_j=Σ_(l∈L_j)w_l,  W_v=Σ_(o(l)=v)w_l.

每个H_j非空时定义A_j=min_(v∈H_j)a_v。令

    R=max({1}∪{a_v/A_j : H_j≠∅, v∈H_j}),
    K=max({1}∪{a_o(l)/A_j : H_j≠∅, l∈L_j}).

空索引的max按所写{1}处理。量化每个实数α满足

    α≥R,   (α−1)²≥Kd.                              (H)

假设每名light（v=o(l)）满足

    F_v(a_v+w_l)+Σ_(j:l∈L_j)G_j(w_l)
    ≥α[F_v(W_v)+Σ_(j:l∈L_j)G_j(T_j+U_j)].             (UFhet)

则下面降序侧势的任意单hub翻位局部最小点，配全部light与source反位，是α-PNE。允许零/常数费用、空light集、任意空H_j/L_j、source自身参加侧资源、自环和重复side。hub全局最大/最小权比可以无界，只要所定义R,K得到所需控制。固定全局hub权比R0时R,K≤R0，故α=max{R0,1+√(R0d)}充分。若所有hub同权，R=K=1，(H)恰恢复第八节的1+√d，排序势也退化为其原势。

**Dependencies / Evidence / Counterevidence / Status：** MODEL的真实单方偏离、下述降序边际与重置引理、第8.4节源标量估计（其证明实际上只需α≥1，且左侧≤dF(a_v+W_v)），有限势局部最小。没有导入外部均衡定理。已完成独立重构、原冻结攻击及凸性加强后重审；精确核验合同见10.5。R,K和UFhet仍为承重限制，不能从局部权比可计算推出全类统一界；未外审、未认证新颖性，唯一题保持OPEN。

### 10.1. 降序前缀势的真实边际

对side j固定light外场x≥0及hub用户子集S⊆H_j。按权a_v非增排列S（相同权用固定玩家序），前缀权为p_r。定义

    P_j(S;x)=Σ_(r=1)^|S| G_j(x+p_r),  P_j(∅;x)=0.

对v∈S，令a=a_v、z为其前面hub总权，后缀hub权为b_1,…,b_m≤a，q_r=Σ_(t≤r)b_t。删去v的边际为

    Δ_vP=G_j(x+z+a)
          +Σ_(r=1)^m [G_j(x+z+q_r+a)−G_j(x+z+q_r)].  (S)

所有后缀b_r≥A_j。记真实费用c=G_j(x+z+a+q_m)。若m=0，Δ_vP=c；以下m>0。

下界：区间[x+z+q_r,x+z+q_r+a]因b_r≤a而无间隙，其并覆盖[x+z+a,x+z+a+q_m]。对非负导数积分，因此(S)≥G_j(x+z+a)+c−G_j(x+z+a)=c。

上界：非负系数多项式G_j凸。令y=x+z，Y_r=y+q_r+a，Y_0=y+a。因0<b_r≤a，凸函数在区间右端的短尾平均斜率至少长区间平均斜率，故

    G_j(Y_r)−G_j(Y_r−a)
    ≤(a/b_r)[G_j(Y_r)−G_j(Y_r−b_r)]
    ≤(a/A_j)[G_j(Y_r)−G_j(Y_(r−1))].

末步用b_r≥A_j及G_j单调。将(S)的后缀差分求和望远镜，且a/A_j≥1，得到

    Δ_vP≤G_j(Y_0)+(a/A_j)[G_j(Y_m)−G_j(Y_0)]
         ≤(a/A_j)G_j(Y_m).

因此准确可用的边际夹逼为

    c≤Δ_vP≤(a/A_j)c≤Rc.                             (S1)

这项凸性尾均值估计由第二审查者在原1+a/A_j冻结上界后提出，重新独立核对后纳入首登Claim。常数、线性和零多项式均成立。排序始终按同一玩家身份，删去/插入v时其他hub次序不变。

### 10.2. 异权前缀的 light 重置

对任意S⊆H_j、x≥0、w>0、x+w≤T_j，若H_j非空，

    P_j(S;x+w)−P_j(S;x)
    ≤κ_d(w/A_j)G_j(T_j+U_j),  κ_d(t)=min{dt,t+1}.    (S2)

证明：设Y=T_j+U_j>0，n=|S|。对0≤t≤Y有G'_j(t)≤dG_j(Y)/Y。nA_j≤U_j≤Y给导数界ndwG_j(Y)/Y≤d(w/A_j)G_j(Y)。另一界把n个差分表示为长度w、起点x+p_r间距≥A_j的积分；几乎处处重叠数≤ceil(w/A_j)≤1+w/A_j，全部区间位于[0,Y]。积分总量≤(1+w/A_j)G_j(Y)。取最小即(S2)。S空时左0；H_j空时P恒0，不定义A_j也不收费。

κ_d单调、凹且κ_d(0)=0；对任意c>0,t≥0，κ_d(ct)≤max{1,c}κ_d(t)。因此对source v的每名light l及所参加的非空H_j，

    κ_d(w_l/A_j)≤K κ_d(w_l/a_v).                    (S3)

### 10.3. 势、合法偏离与重置费用

对hub位h，记S_jb(h)={v∈H_j:h_v=b}，x_jb(h)=Σ_(l∈L_j:h_o(l)=b)w_l。定义

    E_het(h)=Σ_j Σ_(b=0,1) P_j(S_jb(h);x_jb(h)).

真实hub翻位时light不动。由(S1)及α≥R，旧副本删去边际≥旧真实费用、新副本加入边际≤α新真实费用，故side的真实α成本差不超过固定light外场的势差。

势E_het(h^v)按定义随后把所有source=v的light侧位重置。逐名重置时，移出副本的变化非正；移入副本由(S2)控制，各中间light外场均≤T_j。由(S3)，总正向误差Q_v满足

    Q_v≤K Σ_(o(l)=v) κ_d(w_l/a_v)
                    Σ_(j:l∈L_j)G_j(T_j+U_j).        (S4)

空hub侧资源的实际hub成本和势均为零，删掉它们的非负收费只使此式更强。

设M_v=αF_v(a_v+W_v)−F_v(a_v)≥0。将UFhet改写，且用
αG_j(T_j+U_j)−G_j(w_l)≥(α−1)G_j(T_j+U_j)，得

    Q_v≤K/(α−1) Σ_(o(l)=v) κ_d(w_l/a_v)
                            [F_v(a_v+w_l)−αF_v(W_v)]. (S5)

其中每light的所有side共用同一个主预算，没有逐side重复领取。第8.4节T≤1与T≥1两分支都先证明该加权和≤dF_v(a_v+W_v)，只用α≥1；故

    Q_v≤Kd/(α−1) F_v(a_v+W_v)
        ≤(α−1)F_v(a_v+W_v)≤M_v.                    (S6)

无source light时直接Q_v=0，亦成立。此处使用Kd≤(α−1)²，不要求全局hub权比有界。

选E_het的单hub翻位局部最小点。hub v主资源α成本差为−M_v，side部分至多E_het(h)−E_het(h^v)+Q_v≤Q_v，所以总差非正。light当前成本至多UFhet右括号，偏离成本至少左侧，UFhet给αC_l(current)≤C_l(dev)，特别是α-PNE。保留动作、零成本和弱端点直接按MODEL不等式处理。

### 10.4. 范围与继续义务

本结果允许任意多hub权类；依赖的是side内部跨度R与source到side最小hub权的比例K，而不是全球权种数或全局跨度。有限固定R,K时给O(√d)子类界；R或K随实例无界时没有全类保证。任意异权hub的side-only对称副本不宜直接声称有普通Rosenthal精确势；第10.1节为它构造的是有比较损失的排序势。这个势的单副本边际损失R本身不能被统一常数替换：取G(x)=x、无light外场、一个权a=RA的插入hub和n名权A的后缀hub，R≥1，则ΔP=(n+1)RA，真实费用c=(R+n)A，故ΔP/c=(n+1)R/(R+n)→R。它只说明所写逐副本夹逼锐，不是一般存在性障碍；同一二元单side游戏中，取两副本总hub负载差的绝对值最小的状态，即为exactPNE（若某hub可改善，翻位会严格缩小该绝对差）。配套作者审计反算该式。

主目标仍缺：消去无界局部权比和强迫假设的全类选态，或构造次数效率可增长的全状态反例。第八节、旧截断势、既有奇环下界及所有方法障碍的身份不变。

### 10.5. 独立攻击与有限精确审计

[两名审查者的独立重构及冻结攻击](../../reviews/weighted_congestion/heterogeneous_hub_sorted_side_review.md)记录初始较弱条件、第二审查者的凸性边际加强、最终差异审查和各自未排除范围。数学正文没有把内部审查当成外部同行评审。

在仓库根运行以下两份程序，只向stdout输出JSON；重跑结果应写临时位置，不覆盖冻结记录：

- `python3 tests/audits/weighted_congestion/verify_heterogeneous_sorted_side.py`；冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/heterogeneous_author.json`。基函数逐身份子集边际、重置、源标量中间界、完整资源真实偏离与source重置预算；含两条件取等、零/常数、空集合、局部比有界而全局跨度任意大的构造，以及异权side-only无exact的三玩家范围检查。
- `python3 tests/audits/weighted_congestion/independent_heterogeneous_sorted_side.py`；冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/heterogeneous_independent.json`。独立实现降序势和literal策略负载，另检查κ缩放、源正预算与各势局部最小点。

代码、seed、参数生成、Python版本、Fraction精度和源码hash均由实际程序及JSON固定。有限核验只检查所列实例，不代替正实参数的区间覆盖、凸性尾均值与源预算证明。R,K无界仍缺全类控制，UFhet失败也未覆盖。

## 十一、异权 hub 的重置增量与强迫倍率分离

### 11.1. 精确身份与旧版本关系

**ID/version / 中文数学名称：** `WC-HETEROGENEOUS-HUB-SORTED-SIDE-v2`，局部异权主玩家排序侧势的重置增量乘积预算均衡。第十节 v1 的陈述和证据不改；新版本分离强迫倍率与目标倍率，并以增量重置预算放宽充分条件。

**Objects / Domain / Quantifiers / Definitions：** 完全量化第十节的有限模型：有限非空 hub 集 V、任意正实 hub 权 a_v；有限 light 集，正实权 w_l 和唯一 source o(l)；每 source 两个同费主资源副本，每 side 两个同费资源副本；任意 side hub/light 子集 H_j,L_j，可空；二元策略、全部资源互异及非负实系数、次数至多整数 d≥2 的 F_v,G_j，均原样保留。沿用 U_j,T_j,W_v，非空 H_j 的 A_j，以及侧内比 R 和 source-to-side 比 K。沿用第10.1、10.3节按身份破同权 tie 的降序前缀势 P_j 和 E_het。

**Assumptions / Exact Statement / Scope / Conclusion：** 对任意实数 τ≥1、α≥1，假设

    α≥R,   ατ≥Kd,                                  (H2)

且每名 light l（v=o(l)）满足

    F_v(a_v+w_l)+Σ_(j:l∈L_j)G_j(w_l)
      ≥τ[F_v(W_v)+Σ_(j:l∈L_j)G_j(T_j+U_j)].        (UFhetτ)

则同一 E_het 的**每个**单 hub 翻位局部最小点，配以全部 light 与各自 source 反位，均为真实 α-PNE。没有要求 τ 与 α 的大小排序。允许 τ=1、α=1（后者由 α≥R 强制 R=1）、零/常数费用、空 light 集、空 H_j/L_j、source 自身参加 side、source 不参加 side 及任意多 hub 权类。

**Dependencies：** 第10.1节固定 light 的边际夹逼、下面非均匀前缀的重置增量引理、第9.9节主增量源标量引理 (SΔ)、κ_d 的单调与次齐次性，以及有限势局部最小点。没有调用外部均衡定理，没有把 v1 的结论当成前提。

**Evidence / Counterevidence / Objections / Status：** 本草稿给出完整条件证明，有限 Fraction 审计另存；独立审查状态由主研究者在审查后填写。本范围仍依赖 R,K 和 (UFhetτ)，不能视为全类结论；下述独立方法反例给出全部全局最小点都坏的游戏，排除仅靠该势最小化删除 R 条件的推理，却不排除其他选态法。未外审、新颖性未认证。

取 τ=α 时，新域是 α≥R、α²≥Kd；v1 的 α≥R、(α−1)²≥Kd 蕴含新域，故保留旧保证。同权 R=K=1 时，P_j 退化为原 Rosenthal 势，新域恰恢复第9.14节的 ατ≥d。局部 R,K 有界时，对固定 τ 给 max{R,Kd/τ} 的子类保证；这些仍是实例结构参数。

### 11.2. 非均匀前缀的重置增量引理

设 A>0、w>0、x≥0、T≥x+w、U≥0；若 n≥1，令

    A≤p_1<p_2<⋯<p_n≤U,  p_(r+1)−p_r≥A,
    Y=T+U.

对任意非负系数、次数至多 d≥2 的多项式 G，有

    Σ_(r=1)^n[G(x+w+p_r)−G(x+p_r)]
      ≤κ_d(w/A)[G(Y)−G(w)],  κ_d(t)=min{dt,t+1}. (HRI)

也允许 n=0，此时不要求任何 p_r，左侧零，因 Y≥T≥w，右侧非负。U=0 时只能使用 n=0。若 G 为常数或零，两边均零。以下 n≥1；前缀起点和间距条件给 U≥nA，所以 Y−w≥U≥nA>0。仅写“相邻间距≥A”而删除首起点/总长条件不够：n=1、p_1=0、x=0、Y=w 会使非恒定 G 的左侧正而右侧零；实际 hub 前缀满足所写完整条件。

对每个 k≥1，Y^k−w^k≥(Y−w)Y^(k−1)。故逐非负系数比较，对 0≤z≤Y 有

    G'(z)≤d[G(Y)−G(w)]/(Y−w).

左侧是 n 个长度 w 区间 I_r=[x+p_r,x+w+p_r] 上 G' 的积分和，全部区间包含于 [0,Y]。因此其值至多

    nw·d[G(Y)−G(w)]/(Y−w)
      ≤d(w/A)[G(Y)−G(w)].                         (HRIa)

再令 a=1+w/A，c(z) 为这些区间的覆盖密度。相邻起点间距至少 A，所以几乎处处 c(z)≤ceil(w/A)≤a，且 ∫_0^Y c=nw。令 q=G'(w)≥0。G' 非减，故

    ∫_0^w cG'≤q∫_0^w c,
    ∫_w^Y(a−c)G'≥q∫_w^Y(a−c).

两式相减得

    ∫_0^Y cG'−a[G(Y)−G(w)]
      ≤q[nw−a(Y−w)]≤0,

因为 a(Y−w)≥a nA=n(w+A)≥nw。这一步以 w 以上的剩余容量支付可能落在 w 以下的积分质量，并未假定所有原区间都位于 [w,Y]。结合 (HRIa) 即 (HRI)。

应用到 side j 的任一 hub 子集 S：降序前缀 p_r 是相应 hub 权的部分和，首项及相邻间距都至少 A_j，末项至多 U_j。因此在 x+w≤T_j 时

    P_j(S;x+w)−P_j(S;x)
      ≤κ_d(w/A_j)[G_j(T_j+U_j)−G_j(w)].           (HRI-side)

空 H_j 或空 S 的势恒零，直接以零处理，不定义或除以不存在的 A_j。

### 11.3. 整名 light 领取一次预算，真实偏离闭合

固定 source v，定义

    Q_l=F_v(a_v+w_l)−τF_v(W_v),
    D_lj=G_j(T_j+U_j)−G_j(w_l)≥0.

由于 τ≥1，

    τD_lj≤τG_j(T_j+U_j)−G_j(w_l).

由 (UFhetτ)，每名 light 的全部 side 共同满足

    τΣ_(j:l∈L_j)D_lj≤Q_l,  Q_l≥0.                (HP)

固定 hub 翻位后，只在势比较中逐名重置 source=v 的 light。移出副本的势变化非正；移入副本使用 (HRI-side)，中间外场始终满足 x+w_l≤T_j。总正向误差 B_v 因而满足

    B_v≤Σ_(o(l)=v)Σ_(j:l∈L_j,H_j≠∅)
                  κ_d(w_l/A_j)D_lj
       ≤KΣ_(o(l)=v)κ_d(w_l/a_v)Σ_(j:l∈L_j)D_lj
       ≤(K/τ)Σ_(o(l)=v)κ_d(w_l/a_v)Q_l
       ≤(Kd/τ)[F_v(a_v+W_v)−F_v(a_v)].            (HB)

第二步使用 κ_d(w_l/A_j)≤Kκ_d(w_l/a_v)；(HP) 的 Q_l 非负，全部 side 只共领一次主预算。空 H_j 的实际势误差零，从其预算中省去非负项合法。末步直接使用 (SΔ)，取 u=a_v、t_l=w_l/a_v；它对 τ≥1 成立，不要求每个源括号自行非负（此处 UF 恰额外保证了非负）。这里只有除以正数 τ，没有除以 τ−1。

令 Δ_v=F_v(a_v+W_v)−F_v(a_v)≥0，M_v=αF_v(a_v+W_v)−F_v(a_v)。由 (H2)、α≥1，

    B_v≤(Kd/τ)Δ_v≤αΔ_v≤M_v.                     (HPay)

无 source light 时 B_v=Δ_v=0，不需要任何正成本假设。

取 E_het 的任一单 hub 局部最小点 h，并配全 anti。真实 hub v 单方翻位保持全部 light 动作固定。第10.1节边际夹逼和 α≥R 给真实 side 的 α 成本差不超过固定外场势差；随后仅供比较的 light 重置误差至多 B_v。因此

    C_v(s)−αC_v(dev)
      ≤−M_v+E_het(h)−E_het(h^v)+B_v≤0.

每名 light 当前主负载 W_v，当前 side 负载至多 T_j+U_j；真实翻位后主负载 a_v+w_l，side 新负载至少 w_l。因此 (UFhetτ) 给 τC_l(s)≤C_l(dev)，再由 τ,α≥1 推出 C_l(s)≤αC_l(dev)。各玩家只有两个动作，保留动作自动满足。零偏离成本按这个不等式处理，没有费用商或 0/0。完成 v2 的条件证明。

### 11.4. 独立方法 Claim：排序势的全部全局最小点均可损失 R 因子

**ID/version / 中文数学名称：** `WC-SORTED-SIDE-GLOBAL-MINIMUM-R-BARRIER-v1`，降序侧势全局最小化保证的局部权比障碍。

**Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：** 对每个实 R>1、每个实 1≤α<R、每个整数 d≥2 以及每个 τ≥1，存在第十节结构类的有限游戏：没有 light、全部主费用零、仅一个 side 副本对，侧费用 G(x)=x，侧内比恰 R、K=1，(UFhetτ) 真空成立。其降序势 E_het 的**全部全局最小点**都不是 α-PNE；每个全局最小点同时还是严格单 hub 翻位局部最小点。若还要求 ατ≥Kd=d，只需另选 τ≥d/α；同一反例保持。因此删去 α≥R 后，乘积预算不能保证该势任意局部最小点或任意全局最小点均为 α-PNE，且仅在全局最小点之间择优也不能修复。它不否定真实 exact PNE，更不是全类非存在下界。

**Construction / Proof：** 固定任意 A>0，令 a=RA。取正整数

    n>αR/(R−α).

有 n 名 hub 权 a 和 n 名 hub 权 A，全部参加这一个 side 对；其主资源费用均为零。状态 h 把全部 n 名重 hub 放副本0，全部 n 名轻 hub 放副本1。

任一重 hub 翻位时，重组部分的降序势减少 na，而目标副本的插入边际恰 (n+1)a，故 ΔE_het=a>0。任一轻 hub 翻位时，原副本势减少 nA，而新副本插入边际为 na+A，故

    ΔE_het=na−(n−1)A>0.

所以 h 是严格单 hub 翻位局部最小点，没有可供平坦移动规则离开的 tie。任一重 hub 当前真实成本是 na，翻位后真实成本是 a+nA，其严格改善比为

    na/(a+nA)=nR/(R+n)>α,

最后不等式与 n 的选择等价。固定 R 令 n→∞ 时该比趋于 R。没有 light 玩家，强迫假设对任意 τ 都真空成立；G 线性属于每个 d≥2 的次数上限，费用和权均合法。

为核对**全部全局最小点**，令任一状态的副本0有 x 名重 hub 和 y 名轻 hub；副本1相应有 n−x 名重 hub 和 n−y 名轻 hub。因为 a>A，降序势先计重 hub，再计轻 hub，所以其势值为

    P(x,y)=a/2[x(x+1)+(n−x)(n−x+1)]
           +a[xy+(n−x)(n−y)]
           +A/2[y(y+1)+(n−y)(n−y+1)].

全分离态 h 的值是 P_sep=(a+A)n(n+1)/2。令 k=n−x、l=y，直接展开得到精确恒等式

    P(x,y)−P_sep=a(k−l)^2+(a−A)l(n−l).          (GlobalR)

对全部整数 0≤k,l≤n，两项非负。因 a>A，等号要求 k=l 且 l=0 或 n，故仅有 (x,y)=(n,0),(0,n) 两个全分离态。每一类玩家在这两个态中全部同位，故计数态各对应唯一身份状态。两个全局最小点由副本互换对称，均具有上面严格局部最小性质及严格重 hub 改善。因此所有 E_het 全局最小点都坏。

**Dependencies / Evidence / Objections / Status / Related Files：** 仅依赖第10.1节势定义和 MODEL 的真实偏离。本构造把第10.4节的单副本边际锐性加强为完整对称游戏中全部全局最小点均坏；严格局部最小是同一 Claim 的附带结论，不另建重复身份。有限 Fraction 审计对所选适中 n 的实例枚举全部身份单人翻位，对其余参数精确核对两类对称闭式；另用精确多元多项式系数反算 (GlobalR) 并枚举有限计数格核对全局最小点。它排除仅以此排序势局部或全局最小化删除 R 的保证，不排除改用其他势、在非最小状态选择，或不同数学机制。主问题仍开放；独立审查、外审、新颖性分别另记。

本游戏本身存在 exact PNE：在有限二副本状态中取总负载差绝对值最小的状态；若某 hub 可严格改善，则其当前副本负载大于翻位后副本负载，翻位严格缩小绝对负载差，矛盾。因此不能把上面坏局部最小点冒认为不存在均衡的例子。

### 11.5. 冻结攻击、代码与有限证据

第11.1—11.4节冻结 SHA256 为 `bf4478c57a426b5fd0817a07d06686951596f717cd888620ae663fb0a24afb76`，其数学字节原样保留；该冻结稿中的待填状态在此明确更新：两个 Claim 均有完整证明、独立先重构后冻结攻击，未发现范围内尚成立的 fatal objection。详见[独立审查](../../reviews/weighted_congestion/heterogeneous_hub_product_budget_review.md)。未外审、未认证新颖性，WC-TARGET仍OPEN。

在仓库根运行以下程序，仅输出JSON，重跑不得覆盖冻结结果：

- `python3 tests/audits/weighted_congestion/verify_heterogeneous_reset_increment.py`；作者路，未导入旧程序核心，冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/heterogeneous_reset_increment_author.json`。
- `python3 tests/audits/weighted_congestion/independent_heterogeneous_reset_increment.py`；审查者独立 literal 实现，冻结结果 `evidence/runs/weighted_congestion/shared_side_truncation/heterogeneous_reset_increment_independent.json`。

参数生成、seed、Python版本、Fraction算术和源码hash由代码及JSON固定。核验覆盖非均匀重置、主增量、弱等号、零/常数费用、完整真实偏离及(GlobalR)系数反算；有限证据不替代一般证明。旧第九、十节及其冻结代码/结果均未改写。
