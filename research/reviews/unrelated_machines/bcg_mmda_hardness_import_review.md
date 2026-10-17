# BCG/MMDA/Santa 困难性导入的独立审查

## 审查对象与冻结来源

本审查针对反面路线的精确问题：已有 Santa/Max-Min 或 MMDA 文献是否提供当前需求树模型的多项式 gap
\[
 b^*=1\quad\text{vs.}\quad b^*\le\delta
\]
对每个固定 \(\delta>0\) 的 NP-hardness。审查人先按目标量词重构，再读取来源，不把 SA/配置间隙当计算困难性。

- Bateni–Charikar–Guruswami, TR-848-09, [作者PDF](https://mhbateni.com/academic/pubs/maxmin-tech09.pdf)，本地字节 `history/source/literature/unrelated_machines/bateni_charikar_guruswami_2009_maxmin.pdf`，SHA256 `7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`；目标位置 Theorems 3.1/4.2、Definition 4.3/Lemma 4.6、§7 Definition 7.1/Lemma 7.2。
- Bamas–Lindermayr–Megow–Rohwedder–Schlöter, arXiv:2307.08453v1，Theorem 1/Section 2.1.2；原字节与版本已在文献清单登记。
- Bamas, arXiv:2406.18273v2，MMDA定义、Theorem 1/2 和 p.44 Open Question 4；原字节与版本已在文献清单登记。

## 结果核对

BCG Theorems 3.1 和 4.2 的困难性对象是 additive utility 的 DegreeTwo 与 InfDegreeOne Max-Min Allocation，给出 factor 小于 2 的困难性。其 Definition 4.3/Lemma 4.6 的 M-pyramid 是一个 forest，必须包含全部 graph sources，允许省略非源点，且 sinks 不收费。把来源图加一个 super-root 并设根需求等于源数不能保留 soundness：当前 (b^*) 允许省略任意比例的源点，根比例只线性惩罚；BCG 的 NO 只禁止“包含全部 sources 的 M-pyramid”，不禁止选取 \(\delta q\) 个源点的高比例子树。

BCG 的 2/1 或 \(\infty\)/1 additive item values 也不是当前树的子出度计数。把值2物品复制成两个叶会允许两个玩家分裂副本；把它放在一个星下只产生一条父边。故没有从 BCG 直接得到当前单根、正需求叶收费的 (b^*) gap。BCG §7 的 duplication gadget 只说明简单路线在低于2处受限，并明确没有给出 \(\alpha\ge2\) 的 gadget；这不是更强硬度定理。

BLMRS Theorem 1 的方向是：若有 Makespan \((2-1/\alpha)\)-近似，则可得 Santa \((\alpha+\eta)\)-近似（\(\alpha\ge2\)）。它是算法归约，不能反向推出 Makespan 困难性；已知 Santa 的 factor-2 困难性在这里也不能与 \(\alpha+\eta\ge2\) 形成矛盾。

Bamas 2024 的 MMDA 与当前 (b^*) 桥梁在对象上相近；但 Theorem 1/2 是 Sherali–Adams/层级间隙，p.44 Open Question 4 仍询问 MMDA 的 ETH-hardness，并指出朴素转换会产生指数规模。没有可导入的 NP-hardness 或固定 \(\delta\) 实际整数 gap。

## 结论、反驳与下一义务

**结论。** 截至本次审查，没有来源定理给出当前模型所需的每固定 \(\delta>0\) 的 (b^*=1) 对 (b^*\le\delta) 位多项式 gap。把 BCG factor-2、Bamas SA gap 或 BLMRS 算法方向写成 UM-TARGET 反面证明都是模型或逻辑错误。

**保留的可复用障碍。** 任何新的归约必须同时：强制全部必要 source/player 参与，或证明任意高比例子集都能解码；用多项式大小的不可分裂 gadget 表示 additive 2/∞ 值；并处理当前模型中正需求叶的收费。两份内部无冲突完整复制的二着色一半地板已另立 `UM-DUPLICATION-TWO-COPY-FLOOR-v1`，正好阻断最简单的 duplication 方案。

**状态。** 这是 Paper Fact 导入范围的独立审查，不是一般困难性证明；未发现可升级主目标反面的定理。`UM-TARGET-v1` 保持 OPEN。
