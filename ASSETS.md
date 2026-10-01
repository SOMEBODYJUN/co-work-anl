# 研究资产与严格适用条件

本页按**数学命题 → 前提 → 证明 → 唯一规范实现 → 验证证据**组织文件。完整的机器可读对应表在 [research/assets.json](research/assets.json)，数学前提之间的合取超边在 [research/graph.json](research/graph.json)，旧路径到新路径在 [research/path_migration.json](research/path_migration.json)。所有旧 Python 入口只是兼容转发；规范实现集中于 [facility_spe](facility_spe)。

| 主张 / 用途 | 必须同时满足的条件 | 证明、实现与核验 | 明确边界 |
| --- | --- | --- | --- |
| 共同目录黄金比例构造 SC-PHI-E/A | 两家设施有**同一**非空有限目录；显式可达关系；正有理数权重；覆盖客户必须参与；客户最小化实际负载；允许逐布局选择精确独立混合 NE。位复杂度结论要求二进制有理输入。 | [整合手稿](manuscripts/shared_phi/main.tex) → [证明重构](math/SHARED_PHI.md) → [规范代码](facility_spe/shared_phi.py)；[753 例测试](tests/test_shared_phi.py)与[记录](evidence/runs/2026-09-30/shared_phi.json)。 | 输出某个至多 $\phi$ 的证书，**不计算实例最优因子**；普遍证明尚未外审；测试未使 C 成为全局在轨见证。 |
| 异构目录因子 2 HC-2-UP/LOW | 两个目录各非空，可不同；同一线性负载模型与正有理权重；上界构造用**纯**客户 NE。 | [异构手稿](manuscripts/heterogeneous/main.tex) → [四种子实现](facility_spe/heterogeneous_two.py) → [两组测试](tests/test_heterogeneous.py)和[严格下界](math/proofs/heterogeneous/tight_two_lower.md)。 | 异构严格下界不能当作共同目录下界；不是实例最优算法。 |
| 稀疏类 $\rho$（HC-RHO） | **同时**满足一侧目录至多两个地点、每个跨目录地点对公共客户至多一人。 | [异构证明 §8](manuscripts/heterogeneous/main.tex)、[单交叠精确程序](facility_spe/exact/single_overlap.py)、[下界实例](examples/heterogeneous/rho_lower.json)。 | 双侧目录都任意大时的同一 $\rho$ 结论仍开放；单交叠程序算具体实例，不自动证明普遍定理。 |
| 强弦局部见证 LOCAL-CHORD-IFF/POLY | 局部可达量 $U\ge V>\phi U/2$、公共质量 $C<V/\phi$；两个配额须同时满足。 | [附录 A–B](manuscripts/shared_phi/main.tex)、[局部构造](facility_spe/local/strong_chord.py)、[分支记录](evidence/runs/2026-09-30/strong_chord.json)。 | 可能需要三名以上真实混合客户；成对局部极大不是全局二次极大。 |
| 给定实例最优因子 EXACT-KAPPA / MITM-EXACT | 线性成本、正有理数、精确独立混合 NE；有界交叠法对最大重叠人数 $\kappa$ 指数增长；MITM 对公共客户数指数增长。 | [支持区间证明](math/proofs/exact/bounded_overlap.md)、[有界交叠程序](facility_spe/exact/bounded_overlap.py)、[MITM 程序](facility_spe/exact/mitm.py)、[小例子](examples/shared/tiny.json)。 | 短证书只证明**达到**该因子；最优性依赖完整支持枚举证明。 |
| 整数局部谱 DP-W 与局部困难性 LOCAL-HARD | DP 要求公共客户正整数权重，总重 $W$；弱 NP 困难性是**一个局部均衡最小收益**问题。 | [局部计算推导](math/proofs/local/exact_methods.md)、[困难性证明](math/proofs/local/hardness.md)、[DP 程序](facility_spe/exact/threshold_dp.py)。 | $O(n^2W)$ 是伪多项式；局部困难性不能推出黄金比例全局构造困难。 |
| 同设施二次成本等价 QUAD-EQ | **恰好两设施**、覆盖客户必须参与、每名客户在两设施使用相同的严格递增二次函数。 | [代数证明](math/proofs/extensions/quadratic.md)。 | 仅局部均衡对应是直接代数事实；黄金比例迁移**依赖 SC-PHI-E**；一般凸函数不保持混合 NE。 |

## 目录职责

- [facility_spe](facility_spe) 是唯一实现；共享 P 菜单和异构四种子共用 [受保护纯修复](facility_spe/local/pure.py)。不同证书格式保留各自字段，避免把不同定理强行合并。
- [manuscripts](manuscripts) 是完整证明的权威源；[math/proofs](math/proofs) 保留可独立复核的局部推导；[math](math) 顶层是重新阅读后写成的规范证明导览。
- [tests](tests) 与 [evidence](evidence) 分开：测试默认只输出到终端，只有显式给出报告路径才写文件；已发表的 JSON 记录不会被重跑覆盖。[examples](examples) 是输入实例，[evidence/certificates](evidence/certificates) 是输出证书。
- [history](history) 保存被后续结果取代的证明路线和交接说明。它们可作来源，不拥有当前命题状态；[PROVENANCE.md](PROVENANCE.md)列出具体失效段落。

## 量词与证书的阅读顺序

先在 [MODEL.md](MODEL.md)确认输入和客户成本，再看 [CLAIMS.md](CLAIMS.md)的精确量词，随后沿 [数学超图](research/index.html)打开共同前提与手稿。若只需要使用算法，按 [USAGE.md](USAGE.md)运行，并用精确验证器检查**该实例**的客户 NE 与实际单方偏离。有限测试、菜单内见证和全体局部 NE 真最小值是三种不同对象，不能互相代替。
