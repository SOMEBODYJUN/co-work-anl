# Boss8 independent：一般机制重构与独立攻击

研究身份：本轮 Boss8 的独立一般机制研究员。对象固定为 CAG-MODEL：有限单位客户、共同有限主题目录、任意完整有序历史纯 SPE；一般 Q-CAG-HALF 仍 OPEN。只修改本目录。

## 可复用新增资产

- [population_nonmonotonicity.md](population_nonmonotonicity.md)：四主题、22客户同目录，三人全部 SPE 福利22，四人全部 SPE 福利21。它排除按人数福利单调的归纳，不是 half 反例。
- [population_audit.py](population_audit.py)、[population_audit.json](population_audit.json)：不导入规范 solver/verifier，展开单位客户，以 Fraction 在全部有序历史独立递推全部终局并审计完整策略。
- [population_small.json](population_small.json)：实例与三人/四人完整策略；最初发现和贪心减重过程在 [population_probe.json](population_probe.json)。

## 探索过程与已停止路线

- 固定实际覆盖 C 后试图加强为 OPT_m(N\C)≤|C|，已被旧 Boss8 的 `R-d51d7a410c12456aa5c44e84b78708d0/independent_attack/residual_cover_family.md` 明确反例否定，停止。
- 每个全历史根终局计数是否可由 count-Markov SPE 实现，已被 `R-18e993ca519949aba29e030d3d7b15b3/strategy_duality/markov_obstruction_audit.py` 的五主题三人合法实例否定，停止。本目录 [markov_root_probe.py](markov_root_probe.py)、[markov_3x3.json](markov_3x3.json) 只是此前三主题三人1000样本零反例过程记录，不提供正面结论。
- 研究最优 m 主题 O 的替换约束：设 P_j 为最优主题 T_j 的私有区，每个目录行动 A 满足 |A\O|+|A∩P_j|≤|P_j|。这是合法 cardinality 约束，但不足以比较终局 1/load 份额；未得到新全局机制。
- [product_nonNE.json](product_nonNE.json)：两个 singleton 选择块的直积目录也可有非静态 NE 的完整两人 SPE。只记录直积下跨块平局惩罚的边界，未尝试正式入库。

## 当前工作

受 root 指派，从 tree 的 blind JSON 输入独立审查其完备跨主题 Shapley 身份及有符号客户松弛障碍。先独立从模型重构，再对照代码；所有状态以实际精确审计为准。
