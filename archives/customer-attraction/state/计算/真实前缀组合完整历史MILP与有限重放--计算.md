---
id: "customer-attraction/r51-portfolio-complete-history-milp-and-exact-reconstruction"
kind: "computation"
type_tag: "计算"
title: "真实前缀组合完整历史MILP与有限重放"
status: "four-finite-reconstructed-SPEs-checked; MILP-optimality-unproved"
summary: "逐行整理完整历史组合MILP包装器及四份45秒超时报告；从已知掩码顺序恢复四个有理实例并验证全部真实IC，但不认证原MILP全局最优性或普遍UP。"
source_ids:
  - "7cad09ff023607996bed"
  - "2bd1808c0c6f7a935fc6"
  - "c5036a7c5ea1e1e839ae"
  - "2328caaf40c8b1313a96"
  - "c4d557d5a94bf4affacc"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/portfolio_full_tree.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/full_tree_aabb_bcde.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/full_tree_abb_bcd.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/full_tree_abc_bcd.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/full_tree_abc_cde.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/full_tree_milp.py"
review_level: "full-frozen-sources-and-base-read; independent-Fraction-full-tree-audit"
truth_status: "finite-realizations-only; no-universal-interface-certificate"
---

## 数学对象和源程序

模型保持有限单位客户、有限非空共同目录、顺序单位提供者和完整有序历史纯SPE；空主题、重复覆盖主题和所有平局均允许。下述客户类型质量是同兴趣单位客户的压缩表示。有理质量经公分母缩放恢复整数客户；不引入客户侧博弈。

`portfolio_full_tree.py` 调用 R18 `full_tree_milp.build(m,k,0,'individual')`。底层逐一建立全部长度至多 (m) 的有序历史；每个内部历史有一个动作二元选择器，每个节点有所有玩家的最终效用变量。终端按每个非空掩码 (B=1,\ldots,2^k-1) 的质量 (x_B\ge0) 与覆盖者人数计算收益；选中边复制所有玩家收益，当前玩家收益至少为每个子节点的真实续局收益。因此它没有把同计数的两个历史强制用同一选择器。

基础模型把根动作固定为0、根第0玩家收益归一为1，并给每主题总客户质量及效用变量加上界 (m)。这个上界来自真实偏离：任意主题 (T) 的偏离收益至少为 (|T|/m)，根最优性和 (u_0=1) 给 (|T|\le m)。因此 Big-M 取 (m) 有该归一化范围内的依据；零根收益不能通过此归一化处理，不能因此删除原模型零客户边界。

包装器输入实际路径 (s) 和长度为 (m=|s|) 的比较元组 (P)，将路径上动作固定，并最小化

\[
F=(m-1)\sum_i v_{\varnothing,i}
  +\sum_{i=0}^{m-1}\sum_{a\in P}v_{s_{<i}a,i}
  -m\sum_{B:B\cap P\ne\varnothing}x_B.
\]

第一项是 ((m-1)W)，第二项是真实实际前缀查询和 (Q)，第三项是 (mC_P)。比较槽重复时第二项重复计入，覆盖并集不重复计入。它实现[真实前缀均匀组合候选](../候选/真实前缀均匀组合接口--候选.md)的固定路径/固定元组余量，而非直接优化 half 比值。只检查两列表等长；调用者还需保证编号合法和根路径以0开头。客户质量是连续变量，只有动作选择变量取整数。

## 四份冻结输出的独立身份

四份源均 `status=1`、HiGHS time limit，时限45秒，自标 `numerical complete-history MILP proposal only`。原JSON与哈希见[证据清单](../../tools/evidence/R-51-uniform-portfolio-probes/MANIFEST.json)。另一个冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径内容相同，清单保留两个定位。

| 报告 | (m,k)；路径；比较元组 | 原始 `fun` | 原始 `mip_dual_bound` | 节点数 |
|---|---|---:|---:|---:|
| AABB/BCDE | 4,5；0011；1234 | 11.999999999999755 | -15.340491246806163 | 156 |
| ABB/BCD | 3,4；011；123 | -2.233105697870611e-13 | -2.258823529411769 | 21 |
| ABC/BCD | 3,4；012；123 | 1.3333333333331676 | -1.0857798736438307 | 21 |
| ABC/CDE | 3,5；012；234 | -7.327471962526033e-15 | -4.0 | 31 |

负的最小化下界不是负可行解；超时也没有认证非负最优值。接近零的 `fun` 不是严格负反例。不能将这四份输出与[既有AAA/BCD报告](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/2241c0299950c9accb92.md>)拼成一次最优性证明：后者路径000、另有动作表及 status=0，仍只有浮点求解器状态。

## 从数值提案到四份精确有限实例

只说“没有原始客户文件”不足以终止审查：生成器明确按升序非空掩码存储 `types`，动作表也完整。本批以分母上限 (10^6) 恢复有理候选，随后**不使用容差**检查质量非负、所有有序节点、每个替代动作、根实际路径以及 (W,OPT_m,Q,C_P,F)。恢复方法不保证一般成功；这里四次成功由独立 `Fraction` 检查认证。

| 报告 | 恢复的非零掩码质量 | 全节点×全部动作比较 | (W=OPT_m=C_P) | (Q) | (F) |
|---|---|---:|---:|---:|---:|
| AABB/BCDE | (x_{31}=4) | 156×5=780 | 4 | 16 | 12 |
| ABB/BCD | (x_3=3) | 21×4=84 | 3 | 3 | 0 |
| ABC/BCD | (x_2=2/3,x_5=2) | 21×4=84 | 8/3 | 4 | 4/3 |
| ABC/CDE | (x_7=3) | 31×5=155 | 3 | 3 | 0 |

掩码 (b) 含主题 (a) 当且仅当 (b\mathbin{\&}2^a\ne0)。ABC/BCD 乘3后为2名只选主题1的客户和6名选主题0或2的客户，总8客户；(W=OPT=8,F=4)。其余三份已经是单位客户整数实例。所有比较的最小IC余量为0；合计1103次包括指定动作的比较，其中874次为真正替代动作。核验覆盖离轨历史，不仅根实际路径。

这补足了这**四张恢复动作表**的有限可实现性，没有补足原MILP最优性。恢复后的客户质量与原浮点向量不同，最大坐标改动分别约 (4.24\cdot10^{-13},1.09\cdot10^{-13},1.30\cdot10^{-13},8.0\cdot10^{-15})。不能倒写为原求解器已交付精确证书，更不能从四个非负余量推出全策略UP或六人half。

## 复现、用途和关系

[独立审计程序](../../tools/evidence/R-51-uniform-portfolio-probes/audit_reports.py)直接读取四份原JSON，输出[全部精确结果](../../tools/evidence/R-51-uniform-portfolio-probes/exact_reports.json)。它从动作表递归计算终局，逐节点比较当前玩家指定动作与每个真实偏离后沿同一表的收益；有限完全信息树的一步偏离原理给纯SPE。程序同时穷举至多 (m) 个主题的支持求 (OPT_m)，没有预设比较组合必最优。

包装器的两次独立smoke保留在证据目录：一人两主题、路径0、比较1、3秒得到数值0；三人四主题、路径000、比较123、5秒超时，`fun≈-3.31e-14`、下界-3。这两次不冒充原45秒运行。`replay_milp.py` 在临时目录还原原始路径布局，原程序和R18依赖均保持字节不变；数值重跑结果可能随求解器版本及时限变化。

关系判断：本程序是UP候选的**实现/发现器**，四份恢复实例是其**有限检查**；与[完整历史精确求解器](../算法/完整历史纯SPE终局全集--算法.md)共享均分模型和完整历史合同，但没有穷尽所有实例/策略。与旧入口[历史分层](../资源/正锥与均匀真实组合安全接口的历史分层--资源.md)相比，本页新增实际源码和四原报告审查以及有理核验，旧入口“本批未读代码/JSON”只描述当时批次。第三阶段可按这些明确语义登记关系，不能画成一般定理的证明边。
