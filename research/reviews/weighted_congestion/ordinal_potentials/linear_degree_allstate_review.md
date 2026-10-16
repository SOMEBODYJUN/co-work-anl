# 线性次数全状态无均衡族的独立重构、冻结攻击与合并核查

## 精确审查对象与实际阅读顺序

本次审查的精确结论是：对每整数 `p≥2^20`，显式有限 MODEL 博弈全部资源费用为正有理系数乘 `x^p`、全部玩家权重为正有理数、每人两个非空不交资源子集动作，且每个纯状态存在严格 `α=p/10` 改善；由此严格否定原题绝对 `C,d0` 的普遍 `Cd/ln d` 上界。成本始终不乘玩家权，偏离后真实负载包含偏离者自身。它不是仅改善环或仅方法障碍。

先阅读 MODEL、ACCEPTANCE、适用 AGENTS 和旧循环窗口正文，未看健康族作者稿前独立记录了权谱、系数归一化、逐人秩、全部状态成本和整数端点瓶颈。随后审查健康族冻结稿：

- `healthy_linear_sweep_family.md`，SHA256 `485e22718ddf7f0323785f91d1d6ce351ea8bdc6dc8de2daee8277c77584fb5c`。

收到全前沿问题后，只据精确目标、此前健康族和规范前沿费用表独立推导 endpoint 费用、incoming 最坏 margin、短相位累计及 parity return 出口，先向主研究者报告完整重构。之后才阅读：

- `healthy_front_coverage.md`，SHA256 `caa9b4d8e0c13d988680499f94205048a86df664230206bf5066708e4f4dce4d`。

最后逐段通读自足合并候选：

- `linear_degree_allstate_lower_bound_candidate.md`，SHA256 `c1f846520baa918b5506013e7a2704fb059e64f1f03c6699c0183b799ee0029c`。

原合并候选发现两项符号完整性修复：`W=(1+1/p)^p` 漏显式定义；`B_actual` 应定义或删去其使用。最终正文已补W并删除B_actual，详见文末最终差异核查。

## 独立结论与状态边界

上述冻结材料的一般证明经过独立重构和逐式攻击，没有发现尚成立的实质反驳。健康族的余量及全状态成本、全部 product-front 覆盖、非法状态修复、实际次数 `D=p` 预算和否定量词全部闭合。所获结论可支持 `WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1` 与原题严格否定身份；仓库整合、相关地图和账本、其他独立攻击、文献核查及推送确认属于主研究者另外完成的交付义务，本审查不冒充已完成它们。

数学真值、可复用机制、外部评审和新颖性分别记录。本审查不声称世界首次、最优常数或某有限游戏达到全类上确界；没有外部同行评审。

## 1. 基体关联、完整双扫和全状态成本

构造参数 `α=p/10,Q=p^4,m−1=ceil(log_2(p²)),N=p^(4m−5)` 在 `p≥20` 给正整数 `N≥Q`。`m` 个测试各建 `N` 对独立资源，共 `2mN` 个；每名玩家每对参与资源恰取一侧，故两个动作非空且不交。

所有测试有 `a<b`，所以窗口始于与 heavy 相同 clone index 的 light 玩家。固定一名 light clone，它恰属 `K` 个窗口且窗口圆周秩恰枚举 `1,...,K`，不是平均或期望分配。正向单窗口旧 light 数与新 light 数按反秩和顺秩枚举，故总成本恰为相应幂和。负向只交换 light 相位，旧/新总成本交换。第二轮对应第一轮的逐位补集，两侧同费使真实当前及偏离成本重复。权重不被额外乘入玩家成本。

标量证明重算结果：

`4/Q≤H/L≤40/Q`，`Z/J>3/(p²ε)`，`A_RZ/(A_(m−2)L)>3·2^(m−1)/p²≥3`。

Riemann 和上下方向正确，`Y≤2^(−p)X` 来自逐项 `r/Q≤(1+r/Q)/2`。返回 `rε≤1/p` 给 `Z≥9N/10`。闭环比中的 `ε=Q^(−(m−1))` 恰抵消，没有指数差一。类0 margin 精确 `H/2`；中间类和末类严格更大。因此精确最小环余量为 `η_cycle=H/2`。

任意纯状态中，邻接资源全部潜在用户总重为 `2w_a`，归一化系数消去 `w_a^p`；heavy 参与1对、light 参与Q对，所以每玩家来自该测试的费用至多 `QA_a2^p`。返回资源全部潜在总重 `1+1/p`，每玩家参与至多N对，费用至多 `NA_RW`。这些都是逐资源、逐玩家、全状态上界。相加得到 `B*=mQ^(m−1)2^p`，并非环上费用或平均参与数。全部系数均正有理，全部资源次数恰p。

## 2. 全 product-front 覆盖的承重义务

共同扭转平移的资源侧交换由 wrap 指示给出；动作中的 wrap 与用户关联中的 wrap 抵消，全部玩家权及对应费用保持。故 mover 类相位可归零，其他类保留真实相对相位。Backward 精确使用前一相位 forward 边的反向，另一类相对相位因此是 `r+1`，没有错写 `r−1`。

对于邻接 heavy，`n(r)` 分段正确，闭短区间 `[0,Q]∪[N,N+Q]` 外存在真实 endpoint，贡献恰 `A_aH`。作者的 incoming light 新费用上界 `A_(a−1)X` 对两方向均成立。因而中间类总 margin `>H/2`；class0 的返回 heavy 干扰给作者较弱但正确的下界 `H(J−1)/(2J)>H/3`，其中 `J>3`。没有忽略附加测试。

若没有上述出口，每个邻接相位差均写为 `k_aN+t_a`，`k_a∈{0,1},0≤t_a≤Q`。累计 `T≤(m−1)Q≤p^5<N`，所以最后一类相对第一类的相位解包成 `T` 或 `N+T`，未丢失 parity。

返回测试末类 light 的 literal 费用为

`O(r)=Σ[((N−k)ε)+e_k(r)]^p`，`Qnew(r)=Σ[((k+1)ε)+1−e_k(r)]^p`，

其中 `h_k=−k modN`，`σ0=1,σk=0(k>0)`，`e_k=1[B_r(h_k)=σk]`。

- 偶 parity，选 forward：相对理想全1，`T=0` 恰1异常；`1≤T<N` 恰 `T+1` 异常。
- 奇 parity，选 backward 并检查 `r+1`：相对理想全0，`T=0` 无异常；`1≤T<N` 恰T异常。

理想两种方向 margin 同为Z。一个异常对 margin 的损失至多 `(α+1)W`。因此统一 defect 不超过 `3p^6/5≤Z/30`，最后一步在 `p≥20` 闭合。减 incoming 新费用后，总 margin

`>(29/30)A_RZ−αA_(m−2)X>(9/10)A_(m−2)L>H/2`。

所以全部前沿均有保前沿真实出口，统一取 `η0=H/4` 合法。`η0` 不是 actual min-max 的精确值。独立 clean 推导还能用 incoming margin `≥−AL` 得到更强下界，但合并证明不需要它。

## 3. Fresh 同类时钟确实覆盖全部状态

新三元 `(0,i,j)` 只使用自己类的三名同权玩家，动作侧与010异或；两侧同费 `M[x/(3w_a)]^p`，`M=2αB*`。玩家参与数至多 `L_c=binom(N−1,2)`，其他类无其参与新资源。完整010/101触发时费用M，非触发用户费用至多 `Mδ,δ=(2/3)^p`。

全部锚定三元不触发 iff 位串至多一次相邻变化，即所需前沿。非前沿时首位的最早反位i之后必有同首位j，给一个完整触发时钟。

预算 `4α²B*L_cδ≤η0` 下：

1. 在 product-front，使用已证基体 margin 至少η0的保前沿单人偏离。两端全部参与时钟均不触发，新 clock 总成本至多 `L_cMδ`，完整 margin `≥η0−αL_cMδ≥η0/2`。
2. 在非前沿，翻最早反位i回首位。旧至少一个 clock 完整触发；翻后其每个参与三元均不触发：i居中则与锚点同位，i居末则更早中位按最早性与锚点同位。新 clock 总成本至多 `L_cMδ`，真实基体新成本至多B*，完整 margin `≥M−αB*−αL_cMδ≥αB*−η0/2≥η0/2`。

这两类覆盖全部纯状态，不要求非法修复一步就到前沿，不同步移动其他人，不需要原环仍留在最终游戏。两动作的合法性和互异性保留。零偏离成本直接由严格 margin 处理。

## 4. 同次数预算及原题否定量词

`B*/η0≤(40/9)mQ^(m−1)`、`L_c≤N²` 给预算倒数

`4α²B*L_c/η0≤(8/45)m p^(12m−12)≤m p^(12m−12)`。

`m−1≤5lnp,lnm≤lnp,ln(3/2)≥1/3` 给充分整数次数 `D*≤180(lnp)^2+3lnp+1`。对 `p≥2^20`，起点与导数证明 `lnp≤p^(1/4)`，所以 `D*≤184sqrt(p)≤p`。实际直接令新资源次数p，所有费用仍是正有理纯p次，预算成立。`184²=33856≤1048576=2^20` 已用 Python 整数计算并反查。

任给 `C≥1,d0≥2`，选整数 `k≥max{20,ceil(20C),ceil(log_2d0)}`、`p=d=2^k`。则 `p≥d0` 且 `lnp=kln2>k/2≥10C`，故 `p/10>Cp/lnp`。每个状态的同一真实合法偏离严格满足更强α不等式，也严格违反目标倍率。非负偏离成本保证弱乘数比较不丢失前一严格号，即使偏离成本为0也成立。量词正是 `∀C∀d0∃d∃G∀s∃i∃t_i`。

## 5. 独立精确审计、代码与实际范围

第一程序 `tests/audits/weighted_congestion/cyclic_clone/independent_linear_degree_sweep.py`，SHA256 `45ea962bdbd9c030154819ff70cfa6b19edbf5fe99c5b33e55ccfda89c3f637e`。它独立构建 literal 资源集合并重算真实负载，不导入作者窗口实现。标准输出保存 `evidence/runs/weighted_congestion/cyclic_clone/linear_degree_sweep_independent.json`。通过范围：168个literal两轮参数案例、2504个任意状态cap案例、`p=20,...,36,40,50` 共19个实际巨大参数的 Fraction 幂和检查。

第二程序 `tests/audits/weighted_congestion/cyclic_clone/independent_linear_degree_front.py`，SHA256 `3be2409adf1ee00d8b55e8daea41e3f634b307dda99be141e517e88b94260591`。它复用第一份独立 literal 构建器，不读取新 front 作者实现。实际标准输出冻结为 `evidence/runs/weighted_congestion/cyclic_clone/linear_degree_front_independent.json`。通过范围：

- 336个邻接 endpoint 全相位案例，检查 exact-heavy 区间和两向 incoming `−L` 下界。
- 70个 full-return 成本案例，另70个 exact 异常位计数案例。
- 类宽3至10全部二元串中1936个非前沿状态，核对首位锚定触发等价及最早反位修复的每个参与三元。
- 上述19个实际巨大参数，精确核对相位累计与 defect 预算。
- 在实际端点 `p=2^20`，整数交叉乘法直接验证完整 `(CLOCK)`，实际取 `D=p`；没有浮点或对数近似。

运行：

`python3 tests/audits/weighted_congestion/cyclic_clone/independent_linear_degree_sweep.py`

`python3 tests/audits/weighted_congestion/cyclic_clone/independent_linear_degree_front.py`

均用标准库 Fraction 和整数；无随机 seed，无截断精度。有限审计只覆盖所列输入及实现，不代替全部参数证明。一般结论由前述完整分析承担。

## 最终修订核查

最终正文为 `research/current/weighted_congestion/linear_degree_allstate_lower_bound.md`，SHA256 `04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33`。

已将它与c1f846合并冻结稿逐行diff核对：补W定义、删除未定义B_actual、删除无引用的外部上界陈述并改为现有Claim入口、更新状态和证据链接，并明确clock前沿在线性顺序0,...,N−1中计相邻变化、补独立攻击代码入口；其余所有构造、费用表、相位覆盖、clock预算和否定量词均无数学漂移。两项字面修复已完成。最终正文在上述hash下通过本次独立审查；没有尚成立的fatal objection。该结论与别的独立审查、仓库检查或远端确认分别记录。

持久化独立程序为 `tests/audits/weighted_congestion/cyclic_clone/independent_linear_degree_sweep.py` 和 `independent_linear_degree_front.py`；只修改import和CLI/metadata输出，不改变数学核验实现。两程序结果分别位于 `evidence/runs/weighted_congestion/cyclic_clone/linear_degree_sweep_independent.json` 与 `linear_degree_front_independent.json`。实际代码hash、依赖hash、输入、命令、Python版本、精度和seed信息以这些冻结JSON为准；运行拒绝覆盖既有结果。
