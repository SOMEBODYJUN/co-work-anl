# 双设施选址：可生长的研究基础

这里的**现行研究资产是重新写出的数学说明**，集中在 [research/current](research/current)；可执行算法集中在 [facility_spe](facility_spe)。原始手稿、旧证明笔记和上一轮整理稿进入 [history](history)。旧的 astra_alg、astra_local、astra_ring、asym_research 根目录已退出当前树；[迁移记录](research/path_migration.json)保留来源，而不让旧实验命名决定未来结构。

**Research Goal / 当前前沿：**从双设施选址的精确客户均衡与全部偏离续局出发，找能跨模型规模复用的近似 SPE 结构。双侧任意长、每跨对最多一共有客户时的尖锐因子现已由 [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) 的内部证明闭合为 $\rho$；任意设施数 $k$ 的统一近似因子或随 $k$ 增长下界仍开放。立方费用的跨成本机制和实例最优倍率的计算复杂度是有条件候选，不是封闭的题目清单。[实时研究状态](RESEARCH_STATE.md)、[命题入口](CLAIMS.md)、[失败路线](FAILED_ROUTES.md)与[路线图](research/ROADMAP.md)一起定位下一个证明义务。

**研究状态：**共同目录的黄金比上界已有完整主稿、现行 Markdown 全分支重写及多轮内部审读；[六地点共同目录下界](research/current/shared/sharp_phi_lower.md)现已补出全布局与有理化证明，二者联合给出尖锐阈值。异构目录的因子 2 构造有成文主稿。受限稀疏 ρ 命题已有逐分支重写，[双方任意长单交叠的 ρ 上界](research/current/heterogeneous/sparse_unbounded_rho.md)本轮给出新全称证明；与原 2×2 下界合并即为同类尖锐阈值。程序能为具体输入生成证书；共享证书另有[独立定义级检查器](facility_spe/cli/verify_phi.py)。以上都尚未经过外部同行评审；内部证明、实例证书与学术发表分别标注。参见[命题与状态登记](research/current/claims.md)及[五轴状态表](research/review_status.json)。

## 先判断输入属于哪条命题

| 目标 | 同时要求 | 可得到什么 | 从哪里开始读 |
| --- | --- | --- | --- |
| 共同目录的普遍构造 | 两设施同一非空地点目录；正权重、显式覆盖；强制服务；客户最小化实际负载；允许每个布局各选精确独立混合 NE | 因子不超过 \(\phi=(1+\sqrt5)/2\) 的一个纯选址证书；**不是**实例最优因子 | [共享定理、证明与算法](research/current/shared/README.md) |
| 任意异构目录的普遍构造 | 两个非空目录可不同；同一负载模型；选用纯客户 NE 延续 | 因子不超过 2 的证书；整数反例族表明异构类不能统一降到 2 以下 | [异构分支](research/current/heterogeneous/README.md) |
| 稀疏异构的较小常数 | **每个跨目录地点对至多一名共有客户，且一侧目录至多两地点** | 现行内部证明给出尖锐普遍因子 \(\rho=2\cos(\pi/7)\)；外部评审未进行 | [受限 \(\rho\) 全分支证明](research/current/heterogeneous/restricted_rho.md) |
| 双方任意长的单交叠目录 | 每个跨目录地点对至多一名共有客户；双方目录大小任意 | 新内部证明给完整纯 NE 续局的普遍因子 \(\rho\)；原受限类 2×2 下界证明同一阈值尖锐 | [SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) |
| 某一个输入的最优因子 | 两设施同一线性负载模型；接受对共有客户数指数增长的时间 | 支持区间枚举给该实例最优因子；短证书单独仅证明“达到” | [局部几何与精确方法](research/current/local_and_exact/README.md) |

完整的客户最优反应式、延续量词和编码界限在[规范模型](research/current/model.md)。[使用说明](USAGE.md)列出可直接运行的命令与证书语义。

## 定义和推导地图

- 输入的带标签布局、客户覆盖、正权原子与实际负载费用在 [model.md §1](research/current/model.md) 定义；两设施公共客户的独立混合 NE 在 §2 化为条件成本差。§3 对全部布局的 NE 选择定义完整续局及真实的全目录偏离威胁。
- `model/NE` → 局部支持几何 → 共同目录固定菜单与全目录环 → 局部强弦 → `SC-PHI-E`；编码有理输入加位复杂度给 `SC-PHI-A`，联合六地点同类下界才得 `SC-PHI-SHARP`。[共享证明顺序](research/current/shared/README.md)。
- `model/NE` → 异构纯菜单、全目录环 → `HC-2-UP`；与双交叠下界 `HC-2-LOW` 合取才得异构 sharp 2。`HC-RHO` 给单交叠且一侧最多两地点的已知锐性；移除长度条件由新 `SPARSE-RHO-ALL` 全称上界证明，结合该下界解决 [Q-SPARSE](research/questions/sparse_catalogs.md)。[异构证明顺序](research/current/heterogeneous/README.md)。
- `CORE-LIFT` 只保留全目录真实威胁而不保证核心短。[SPARSE-LONG-CYCLE](research/current/heterogeneous/sparse_long_cycles.md)在单交叠下构造任意长唯一环，反驳无条件短核心推断；它与普遍倍率 $\rho$ 问题之间没有反例蕴含。
- `model/NE` → 固定纯平局优先级 → 全目录最佳回应逐边比较 → `SPARSE-HIGH-ACYCLIC` → `SPARSE-BALANCED-R`：[高 reach 条件传播](research/current/heterogeneous/sparse_high_reach_barrier.md)对任意 `r≥1` 给出坏环低区必经和 reach 平衡子类上界；它是新全类 `ρ` 证明的依赖，而非全称证明本身。
- `SPARSE-HIGH-ACYCLIC` → 首个高到低边界、单客户同一身份容量、`q(ρ)=0` → `SPARSE-RHO-ALL`：新证明直接排除任意长坏环的首个低区入口，**不**压缩回应核心。旧条件结果仍是一般 `r` 的独立量化边界；原“低区回返阻碍”在 `r=ρ` 已消除。
- 两设施共同目录的 $\phi$ 不覆盖第三家或客户费用 $\mathbb E[L^3]$；分别见 [Q-K-FAC](research/questions/three_facilities.md) 与 [Q-CUBIC](research/questions/cubic_costs.md)。证书的达到性、实例最优性、普遍定理和论文新颖性各自独立。

关键 dependency、attacks 和 scope 边可交互查看[数学超图](research/index.html)，精确文字与证据状态以[现行命题登记](research/current/claims.md)和证明页为准。

## 如何追踪一项研究结论

[命题登记](research/current/claims.md)固定适用域与状态；[现行资产索引](ASSETS.md)把命题连到新稿、实现、检验及历史来源。[数学超图](research/index.html)的节点是定义、引理、反例和结论；一条推导超边要求**所有列出的共同前提**，不是旧文件之间的链接。其[数据](research/graph.json)和[维护规则](research/README.md)可直接核查。GitHub 预览 HTML 时显示源码，下载 HTML 后可使用交互查看器。

[下一阶段研究路线](research/ROADMAP.md)区分新数学问题与现有资产的交付。新问题从 [research/questions](research/questions) 开始；新分支在 research/current/ 下增长，代码、证据、反例分别进入各自目录。[新增研究规则与命题模板](research/GROWTH.md)规定如何写量词、证明链、实现合同、状态和证据；[AGENTS.md](AGENTS.md)让后续研究协作者在改动前执行同一套规则。不能仅搬来一份旧稿或通过有限测试就升级定理。

| 仓库区域 | 职责 |
| --- | --- |
| [research/current](research/current) | 此轮重新撰写的现行模型、命题、数学推导和算法解释 |
| [facility_spe](facility_spe) / [tests](tests) | 唯一规范代码及有边界的回归、独立比较 |
| [examples](examples) / [evidence](evidence) | 输入实例、实例证书、冻结实验记录 |
| [history](history) | 原始手稿、旧笔记、失效路线和上一版整理文本；用作来源而非现行入口 |

## 下次接手时先读哪些文件

| 完整路径 | 为什么存在；什么时候使用 |
| --- | --- |
| `README.md`、`RESEARCH_STATE.md`、`CLAIMS.md`、`FAILED_ROUTES.md` | 恢复目标、前沿、命题身份和失效机制；接手任何新问题先读。它们是地图，证明仍在链接的现行数学稿。 |
| `research/current/model.md`、`research/current/claims.md` | 核对客户 NE、完整续局量词、各定理的精确作用域及审查状态；提出新命题或改模型前读。 |
| `research/ROADMAP.md`、`research/questions/three_facilities.md`、`research/questions/sparse_catalogs.md` | 两个当前主攻的价值门槛、首个判别关口、已知上下界与停损理由；选题时读。 |
| `research/current/heterogeneous/sparse_long_cycles.md`、`FAILED_ROUTES.md` | 任意长精确威胁环的正整数构造、完整证明及其**仅限于无条件短核心**的排除范围；攻击稀疏证明路线时读。 |
| `research/current/heterogeneous/sparse_high_reach_barrier.md` | 新增 `SPARSE-HIGH-ACYCLIC` 与 `SPARSE-BALANCED-R` 的全部量词、平局与零 reach 证明、两处独立边界攻击；研究坏环如何穿越低 reach 区时读。 |
| `research/current/heterogeneous/sparse_unbounded_rho.md` | `SPARSE-RHO-ALL` 全类尖锐阈值的精确范围、固定完整纯续局、首个高到低边界引理、客户身份强制相同、三次式矛盾与独立攻击；接手 Q-SPARSE 或审查新上界时先读。 |
| `tests/audits/sparse_high_reach.py`、`evidence/runs/2026-10-01/sparse_high_reach.json` | 不调用规范求解器的精确分数审查、固定 seed 和冻结结果：包含原六客户下界、修正后长环小例、随机矩形 incidence；复核新定理边界时运行脚本重生记录。有限审查不代替全称证明。 |
| `research/questions/cubic_costs.md`、`research/questions/instance_complexity.md` | 非线性费用机制和实例最优判定的条件性预研；遇到跨成本原则、参数算法或困难性归约时读。 |
| `research/graph.json`、`research/review_status.json`、`research/assets.json` | 数学合取/反例边、逐命题审查层、证明与实现和证据的对照；状态升级或新增 Claim 时一起更新。 |
| `research/GROWTH.md`、`AGENTS.md` | 新问题、证明、代码和冻结证据的落点与检查命令；开始修改前读。 |

当前没有选定公共软件许可或外部证明认证。要用于具体研究输入，请按[条件表](ASSETS.md)选择算法，运行后核查证书，并把普遍定理状态与实例验证结论分开报告。
