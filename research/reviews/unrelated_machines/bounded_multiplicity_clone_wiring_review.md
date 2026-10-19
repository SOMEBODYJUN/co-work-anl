# 有界重数接线与共同循环坍缩的独立重构和实际后审

日期：2026-10-19。仅覆盖正文§9的 `UM-BOUNDED-MULTIPLICITY-CLONE-ENVELOPE-v1` 与 `UM-COMMON-CYCLIC-TWO-WIRING-NEAR-TWO-COLLAPSE-v1`；不重审正文§1–8，不认定新颖性或外部审查，不升级UM-TARGET-v1。

| 实际最终读取对象 | SHA-256 |
|---|---|
| `research/current/unrelated_machines/private_graft_and_resource_repetition.md`，仅§9数学范围 | `e4a4b3a4dd693946da8c52533b85f38c44e434714bfbb04e264fe5a07114449d` |
| `tests/audits/unrelated_machines/bounded_multiplicity_clone_audit.py` | `0e671a934710df3c542a1e863d339a8eae5a68a5c07807316c1583c7e86a12d9` |

## 独立性与实际顺序

`consistency_gadget`先只收到精确对象与等式陈述，未读作者证明，自行重构经验配置投影、有理分母实例化、星边分色及补成置换。其后才实际通读作者全文与代码，并执行新路径下的精确重跑。该研究者同时贡献了所有incidence共用一次循环移位的更强实际见证，因此这份见证不标为完全不知证明的独立作者审查。root另行重构两向配置恢复、逐类型占位与实际全部负载，并重跑规范审计。

最终实际通读canonical§9与代码后，修正过的唯一标题行也重新读过；上表是实际最终字节，未冒用早期稿hash。

## 关键攻击与结论

- 机器副本对每原job类型最多有c个不同邻居，故实际计数确在0..c；覆盖期望精确1来自全部q个带标签原job，而非匿名任务。
- 反向构造先分配全部q个真实job副本到所需slots。每incidence的使用边在job侧度≤1、机器侧度≤c；逐星分色后每色是部分匹配，能补成完整置换。不同颜色允许重复补边是定义的必要部分。
- 不需额外假设q≥c。即使q=1<c，正权配置的单类型计数也不能超过q，否则其至少1/q权重已违反该类型总覆盖1；零权配置不实例化。代码实际覆盖q=1<c边界。
- 原调度可用每incidence的第一置换提升到任意接线，逐机副本负载恰保持。这只给上下包络，不声称每个c接线均坍缩。
- 有限配置负载集合及有理基本解给最小阈值实际取得；Hadamard只给复制数的多项式位长，不能据此声称显式复制规模多项式。
- 相邻cap严格族在T=1时，private覆盖迫非unit概率≥1/c，全部行unit概率总和不足所需c；1与1+1/(c+1)之间没有配置负载断点。c+1配置证书反向给精确1。
- 共同id/shift见证的所有private副本逐类型零/二/一占位，reserved机只有unit，其余机恰m枚1/m；所有原job各执行一次。c1时每clone被迫接每private类型一份，故原趋二值确保持。

## 实质修正与可复现证据

作者早稿的有限总量统计被独立回算纠正为1784台clone机器、21776件job、46816条有限边；不是数学定理变更。证书检查器曾对不可用端的显式零坐标作字典索引，现仅在非零坐标计算负载，并新增真实两机两job的零/不可用边fixture。两项修正均在最终审读和规范重跑之前完成。

运行：`python3 tests/audits/unrelated_machines/bounded_multiplicity_clone_audit.py --output <未存在的结果路径>`。规范[冻结结果](../../../evidence/runs/unrelated_machines/bounded_multiplicity_clone_audit.json)保留Python版本和代码hash；全部81种两标签接线、2448份真实分配、16种c1接线、22份有序两分母配置阵列/8种law，以及m=2..17全部实际负载均精确核对。实现为audit-only，无一般MC_c优化器或NP源归约。

**判定：在上述精确对象和最终字节内，无尚成立fatal objection。** 有价值的是指定复制接口的真实失败机制；不存在一般算法不可能性、所有接线失败或新的困难性结论。
