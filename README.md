# 双设施选址：可生长的研究基础

这里的**现行研究资产是重新写出的数学说明**，集中在 [research/current](research/current)；可执行算法集中在 [facility_spe](facility_spe)。原始手稿、旧证明笔记和上一轮整理稿进入 [history](history)。旧的 astra_alg、astra_local、astra_ring、asym_research 根目录已退出当前树；[迁移记录](research/path_migration.json)保留来源，而不让旧实验命名决定未来结构。

**研究状态：**共同目录的黄金比例构造已有完整主稿、现行 Markdown 全分支重写及多轮内部审读；异构目录的因子 2 构造也有成文主稿。两者的程序均可给具体输入生成可检查证书。它们尚未经过外部同行评审；内部证明、实例证书与学术发表分别标注。参见[命题与状态登记](research/current/claims.md)。

## 先判断输入属于哪条命题

| 目标 | 同时要求 | 可得到什么 | 从哪里开始读 |
| --- | --- | --- | --- |
| 共同目录的普遍构造 | 两设施同一非空地点目录；正权重、显式覆盖；强制服务；客户最小化实际负载；允许每个布局各选精确独立混合 NE | 因子不超过 \(\phi=(1+\sqrt5)/2\) 的一个纯选址证书；**不是**实例最优因子 | [共享定理、证明与算法](research/current/shared/README.md) |
| 任意异构目录的普遍构造 | 两个非空目录可不同；同一负载模型；选用纯客户 NE 延续 | 因子不超过 2 的证书；整数反例族表明异构类不能统一降到 2 以下 | [异构分支](research/current/heterogeneous/README.md) |
| 稀疏异构的较小常数 | **每个跨目录地点对至多一名共有客户，且一侧目录至多两地点** | 候选尖锐普遍因子 \(\rho=2\cos(\pi/7)\) | [受限 \(\rho\) 命题](research/current/heterogeneous/restricted_rho.md) |
| 某一个输入的最优因子 | 两设施同一线性负载模型；接受对共有客户数指数增长的时间 | 支持区间枚举给该实例最优因子；短证书单独仅证明“达到” | [局部几何与精确方法](research/current/local_and_exact/README.md) |

完整的客户最优反应式、延续量词和编码界限在[规范模型](research/current/model.md)。[使用说明](USAGE.md)列出可直接运行的命令与证书语义。

## 如何追踪一项研究结论

[命题登记](research/current/claims.md)固定适用域与状态；[现行资产索引](ASSETS.md)把命题连到新稿、实现、检验及历史来源。[数学超图](research/index.html)的节点是定义、引理、反例和结论；一条推导超边要求**所有列出的共同前提**，不是旧文件之间的链接。其[数据](research/graph.json)和[维护规则](research/README.md)可直接核查。GitHub 预览 HTML 时显示源码，下载 HTML 后可使用交互查看器。

[下一阶段研究路线](research/ROADMAP.md)区分新数学问题与现有资产的交付。新问题从 [research/questions](research/questions) 开始；新分支在 research/current/ 下增长，代码、证据、反例分别进入各自目录。[新增研究规则与命题模板](research/GROWTH.md)规定如何写量词、证明链、实现合同、状态和证据；[AGENTS.md](AGENTS.md)让后续研究协作者在改动前执行同一套规则。不能仅搬来一份旧稿或通过有限测试就升级定理。

| 仓库区域 | 职责 |
| --- | --- |
| [research/current](research/current) | 此轮重新撰写的现行模型、命题、数学推导和算法解释 |
| [facility_spe](facility_spe) / [tests](tests) | 唯一规范代码及有边界的回归、独立比较 |
| [examples](examples) / [evidence](evidence) | 输入实例、实例证书、冻结实验记录 |
| [history](history) | 原始手稿、旧笔记、失效路线和上一版整理文本；用作来源而非现行入口 |

当前没有选定公共软件许可或外部证明认证。要用于具体研究输入，请按[条件表](ASSETS.md)选择算法，运行后核查证书，并把普遍定理状态与实例验证结论分开报告。
