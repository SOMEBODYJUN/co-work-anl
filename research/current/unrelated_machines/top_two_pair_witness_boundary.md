# 双件超载证据的三半锐界与近二归约障碍

本页服务 `UM-TARGET-v1` 的反面研究：排除一种只用同机两件冲突证明 NO 的合同。主目标及其一般反面仍 **OPEN**。下列上界改变了目标函数，绝不作为普通 makespan 的新近似；下界也只到三半。机制为标准匹配与出现位置 SAT 编码的自足推导，不认证全球新颖性或外部评审。

## 1. 对象、定义与命题身份

输入严格沿用 [UM-MODEL-v1](model_and_classical_barriers.md)：显式矩阵、机器数至少一、任务可空、非负二进制有理时间及不可用边，每任务至少一个有限端。对完整合法分配定义

\[
B_2(\sigma)=\max_i\sum_{\text{机器 }i\text{ 上最大的至多两件 }j}p_{ij},
\qquad O_2(P)=\min_\sigma B_2(\sigma).
\]

不足两件以零补齐，因此单件也受控制，空行值零。普通目标仍记 `OPT`；逐点有 `B₂(σ)≤C_max(σ)`，故 `O₂≤OPT`。定义的是 inner top-2 / outer max 的不同目标，不改变 `UM-TARGET-v1`。

| ID/version | Exact Statement / Quantifiers | Scope / Status |
|---|---|---|
| `UM-TOP-TWO-MATCHING-APPROX-v1` | 存在确定性总位多项式算法，对每个合法 P 输出完整分配，`B₂≤3O₂/2`。给任意有理 T≥0，还可输出 `FAIL⇒O₂>T`，或单件≤T且 B₂≤3T/2 的分配。 | 全模型上的不同目标；完整自足证明、内部独立重构；审计实现不作为一般 makespan 算法。 |
| `UM-PAIR-WITNESS-HARDNESS-BARRIER-v1` | 对每个固定有理 ρ≥3/2，promise `YES:OPT≤T` / `NO:每个仅用p≤T端的完整分配都有同机双件和>ρT` 可确定性位多项式判别。NO 若量化所有有限端分配，结论也成立。 | 条件后果：P≠NP 时不存在以此精确 NO 合同归约 NP-hard 源的多项式编译器。不是一般反面。 |
| `UM-TOP-TWO-THREE-HALVES-HARDNESS-v1` | 对每个固定 1≤ρ<3/2，上述 promise NP-hard；普通 restricted assignment 的有限时间仅{1/2,1}、每 job 及每 machine 资格度≤3已足够。因而除非 P=NP，不存在 O₂ 的固定小于3/2近似。 | 标准 3SAT 源的自足归约；不是趋二 gap；来源/新颖性边界见§6。 |

**Dependencies。** 第一项只用非负性、显式有理比较及二部匹配。第二项只用第一项阈值接口，条件排除另用 P≠NP。第三项用 3SAT NP 完全性和§4完整矩阵。后述有限代码是 Evidence，不是一般证明的前提。当前没有 standing fatal objection；审查实际范围见[审查记录](../../reviews/unrelated_machines/top_two_pair_witness_review.md)。

## 2. 重任务匹配、可靠失败与精确阈值搜索

令 `q_j=min_i p_ij`。给 T≥0，保留有限端 `p_ij≤T`，令 `H_T={j:2q_j>T}`。在 H_T 与机器之间找覆盖全部 H_T 的二部匹配；失败返回 FAIL。成功则匹配任务按匹配分配，其他任务各选达到 q_j 的最小编号机器。

**FAIL 健全性。** 任意 B₂≤T 分配只用保留端；H_T 中每件在任何端都严格大于 T/2，因此任何机器至多接一件 H_T。这些真实目的地就是覆盖匹配。匹配失败故 O₂>T，进而 OPT>T；还可用标准增广路可达集给 Hall 缺额证书。不声称成功意味着 O₂≤T 或 OPT≤T。

**全机输出界。** 每台至多一件匹配任务，用时≤T；其余全部≤T/2。两件普通任务之和≤T，一件匹配加一件普通≤3T/2，不会有两件匹配任务。每单件≤T，所以全部机器同时满足 B₂≤3T/2。所有原任务各执行一次，没有匿名替身或分数输出。

**零与空。** n=0 直接空输出。T=0 时成功当且仅当每任务有零端，成功输出全部为零；非负性又说明这恰是 O₂=OPT=0 的条件。不在零值上除法或使用近似比。

**未知最优值。** n>0 时精确排序

\[
\mathcal D=\{0\}\cup\{p_{ij}<\infty\}\cup\{2q_j:j\in J\}.
\]

随 T 增长，保留边只增、H_T 只减；成功谓词单调，且只在 D 的点变化。在端点 `p=T` 已保留、`2q=T` 已属于轻件，因此首次成功的实阈值就是某个 D 中的点。`T≥2 max_j q_j` 时 H_T 为空，必成功。用排序后的枚举或二分找最小成功 τ；因在 T=O₂ 时必成功，τ≤O₂。对应完整输出满足

\[
B_2(\sigma)\le3\tau/2\le3O_2(P)/2\le3\operatorname{OPT}(P)/2.
\]

**位复杂度。** 候选数至多有限端数加 n 加一；每个数是原有理数或它的二倍，比较用整数交叉相乘。每次二部匹配节点、边数由显式输入控制；排序后只需对数次匹配测试，也可多项式次枚举。没有依赖分母数值的循环、指数配置 oracle 或未知 OPT oracle。空任务单独处理，避免因没有矩阵条目而按二进制给出的巨大机器数循环。

## 3. 对反向归约的准确限制

对§1第二项的 promise，运行阈值算法：FAIL 时不可能 YES，回答 NO；成功时给出全机 pair 和≤3T/2≤ρT 的实际分配，故不可能 NO，回答 YES。离开 promise 时没有精确总负载可行性结论。

因此 P≠NP 时，一个 NP-hard 源不能多项式编译为 YES 普通 OPT≤T，而 NO **全部**保留端分配都必有一对超载（ρ≥3/2）。只对 canonical / 解码后 / 某类优选分配证明双件冲突不够：还必须证明任意实际低负载分配可健全地进入那一类。一般 NO:OPT>ρT 并不蕴含双件 NO，整行总量可由更多件造成。

两个标准补充边界：

- 若所有保留端时间都>T/2，则全部任务重，普通 T 可行性本身就等价于覆盖二部匹配。几乎单位大小的冲突图不能免费提供 NP-hard 一致性。
- 若每任务至多两个保留端，则任意 ρ 下 pair 可行性可写为 2SAT：每件的机器选择为 Boolean，逐对禁止同机且时间和>ρT的两个选择；单端固定、无端直接不可行。它控制双件，仍不控制整行。

**没有总负载保证。** 对任意整数 k≥1，k 台机器与 2k 件时间均为1/2、全资格任务，普通 OPT=1；本算法在阈值1时 H 为空，按最小编号平局规则把所有任务放同机，B₂=1而 C_max=k。这是无界分离；不是普通调度的三半算法。

## 4. 小于三半的锐困难性：完整出现位置矩阵

从非空 3CNF 开始，重复文字也作为不同出现位置。每次出现建新变量 y，替换对应原文字；对某原变量的所有出现副本 `y₁,…,y_d`，增加循环子句 `¬y_i∨y_(i+1)`，下标循环。d=1 保留恒真子句也合法。忽略从未出现的变量。循环子句全部为真当且仅当副本取同值；每个副本文字在一个循环子句与至多一个原子句出现，故各正/负文字出现次数≤2。

每个副本 y 建机器 M_y,+ 与 M_y,−，再建 unit 任务 U_y，仅可在这两台耗时1。每个替换后的原子句及循环子句建一件 half 任务，在该子句的文字机器上耗时1/2。其余端全不可用。这些是全部原任务，不加外部 incompatibility 约束。每 job 资格度≤3，每 machine 只接自己的 unit 及至多两件 half，资格度≤3。所有 finite 时间对同一 job 相同。显式 dense 输出规模仍为源长度的多项式。

**YES。** 满足赋值扩张为副本赋值，把 U_y 放在假文字机器；每个子句 half 选一个真文字机器。假机负载1；真机至多两件 half，负载≤1。完整分配峰≤1，有 unit 又迫 O₂≥1，因此非空 YES 有 O₂=OPT=1。

**任意分配的 decoder。** 若 B₂<3/2，unit 与 half 不能共机。每对 literal 机恰一台有自己的 unit，把另一台的文字声明为真。每件 clause half 的真实目的地都是真文字，故所有原子句和循环子句都满足。循环迫原变量副本一致，从而恢复原公式满足赋值。解码只扫描真实 assignment，不假定输出来自上述 YES 构造。

UNSAT 因而迫每份合法完整分配都有 unit+half 的同机对，和为3/2。这对每个固定 ρ<3/2 都严格超过ρ。每份合法分配的 B₂ 又至多3/2（每机至多一个 unit、两个 half），所以 NO 的 O₂ 精确为3/2。这里不声称每份分配的总负载≤3/2；三个任务可以总和2。

空公式无需进入困难实例族；可在源端直接判 YES，或补一个使用新变量的恒真三文字子句使源非空。3CNF 源不含空子句；unused 变量不影响输出。重复文字、单副本循环、二副本循环全保资格及 degree 界。ρ=3/2 时 unit+half 恰等号，严格 NO 条件消失；ρ=1 时 half+half 恰等号仍可行。由此三半转折确实锐，但没有趋二整数 gap。

## 5. 有限核验、实际文件与审查等级

主审计 [top_two_pair_witness_audit.py](../../../tests/audits/unrelated_machines/top_two_pair_witness_audit.py) 使用整数 half-units 与 Fraction，枚举有限矩阵、全部实际分配计算 O₂、逐断点查单调性，并对指定有限 CNF 集枚举全部 unit 放置查 decoder。独立审计 [top_two_pair_witness_independent.py](../../../tests/audits/unrelated_machines/top_two_pair_witness_independent.py) 另建出现位置环，枚举其全部实际分配并回算全机总量及 B₂。它与 literal-copy 表示经逐变量反转循环顺序后、按文字端口识别为同一构造；有限范围和实际哈希见[冻结记录](../../../evidence/runs/unrelated_machines/top_two_pair_witness_audit.json)及[独立记录](../../../evidence/runs/unrelated_machines/top_two_pair_witness_independent.json)。

独立研究者先只据精确陈述重构阈值算法；另一研究者先只据 sharpness 陈述重构出现位置环及所有机器负载；之后实际阅读作者 proof。root 另做精确小矩阵 oracle 后核读最终正文和代码。最终读后版本、未覆盖范围、root 的软件修复记录由[审查](../../reviews/unrelated_machines/top_two_pair_witness_review.md)明确区分。有限测试不作全称 derives；软件仅 audit，不把 Python 程序测试等同一般位复杂度定理。

## 6. Paper Fact、解释与下一义务

经典 LST 的普通 makespan 困难性仅排除固定小于3/2的近似，见既有[来源账本](../../unrelated_machines/LITERATURE.md)及 [CWI 原报告](https://ir.cwi.nl/pub/6083/6083D.pdf)。本页不声称§4逐字复现其原归约。top-k inner norms 与 outer max 已在 [Deng–Li–Rabani 的 generalized scheduling](https://arxiv.org/html/2202.06292v1) 中明确研究；这里的 elementary top-2 结论不因定向检索未见相同表述而获得新颖性认证。

**本轮真实增量**是把双件冲突 soundness 的精确可判别边界写成可调用的反向归约过滤器，并闭合 full-output、零值、位复杂度及锐端点。**仍缺**：对每个固定 ε>0 的近二真实整数 YES/NO 归约，以及从任意低总负载分配到源问题的健全 decoder。应研究同一实际矩阵中的多件共同容量、跨部件身份和源相关一致性；本页不排除这些机制，也没有证明统一 ε 不存在。
