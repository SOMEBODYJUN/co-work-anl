---
id: "unrelated-machines/seven-state-star-global-quadratic-audit-scope"
kind: "computation"
type_tag: "计算"
title: "七态星全局二次审计与root重放边界"
status: "finite-audit-record-preserved"
truth_status: "finite-experiment; no universal theorem"
review_level: "full-frozen-json-read-and-scope-classification"
scope: "12组参数的Fraction七态星审计、其中3组完整small M3/global-q2矩阵及一次root fresh CLI字节重放"
summary: "完整保存并核对两个冻结运行JSON；只认证其精确有理有限案例、PSD秩和作者/root输出字节一致性，不将12参数、3组small矩阵或代码哈希升级为任意d,s定理、递归接线或一般调度算法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_root_replay_scope.json"
---

# 七态星全局二次审计与 root 重放边界

本对象是两个冻结 JSON 运行记录的有限证据登记。它们对应同一七态原星局部核，但承担不同证据身份：

1. ec117f60f81d65a9953b 是审计输出，报告12组参数、精确 PSD 与有限 assignment/moment 检查；
2. 177bb999d00126ea6ea9 是 root 重放范围，记录129行审计源码的 hash、实际命令、fresh output 与作者 output 的字节一致性，以及明确未检查项目。

这两份 JSON 没有构造新数学对象，也不能替代主源中对任意偶数 \(d,s\) 的解析证明。有限证据只用于检查实现输出与既有局部核合同相符。

## 1. 审计输入与精确算术

审计使用
\[
(d,s)\in
\{(4,2),(8,2),(8,4),(16,2),(16,4),(16,8),
(64,2),(64,16),(64,32),(1000,2),(1000,100),(1000,500)\},
\]
并令 \(\eta=s/d\)。每行还记录
\[
p=\eta^3/1000,
\]
以及相应的 bad mass（例如 \(1/8000\)、\(1/64000\)、\(1/512000\)、\(1/32768000\)、\(1/125000000000\)、\(1/1000000\)）。

全部计算使用精确 fractions.Fraction、Boolean monomial basis 和无 pivot 的精确 PSD 消元。不是浮点抽样，也没有随机 seed。每个案例报告原星机器数 \(d+2\)、原 jobs 数 \(d+1\)、有限资格条目数 \(2(d+1)\)，并给出把所有原 jobs 放回其唯一 home 的完整 \(\mathrm{OPT}=1\) 调度。

## 2. 12 组参数中实际检查的项目

对全部12组，JSON 报告：

- row CFG 的 first/pair 精确匹配；
- 5维 symmetric signed-slack 矩阵 rank=5、exact PSD；
- 对小参数 \((4,2),(8,2),(8,4)\)，完整 M3 与 global quadratic signed-slack 检查；
- 全部实际 assignment states 的有限枚举数量和 degree≤6 true moments。

小参数的完整矩阵数据为：

| \((d,s)\) | full M3 维数/秩 | global quadratic 维数/秩 | assignment states | degree≤6 moments |
| --- | ---: | ---: | ---: | ---: |
| \((4,2)\) | 26 / 18 | 16 / 16 | 18 | 32 |
| \((8,2)\) | 130 / 76 | 46 / 46 | 90 | 466 |
| \((8,4)\) | 130 / 116 | 46 / 46 | 130 | 466 |

对其余9组，记录只报告 row CFG、5维 signed-slack 和实际 home assignment；没有声称生成对应的完整高维 M3 或全局 q2 矩阵。审计报告中出现的 full_M3 字段只存在于前三组，不能按目录名扩展到大 \(d\)。

所有12组都保留同一个局部语义：坏样本质量随 \(\eta^3\) 缩放但不随 \(d\) 直接增加；原星本身有峰值1的 home 调度，审计中的 PSD 通过不是 actual OPT 大于1的证据。

## 3. root 重放范围

第二份 JSON 记录：

- version=1，date=2026-10-18；
- 审计代码路径 tests/audits/unrelated_machines/seven_state_star_global_quadratic_audit.py；
- 代码 SHA256 86d05b9013dda128a753f610eaeb9eec4146212c34fa9afcd2bbea3ccab382bd；
- 实际命令以 Python3 执行 sol_seven_state_star_quadratic_audit.py --output ...；
- exit_code=0；
- fresh output SHA256 9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335；
- author_output_byte_identical=true；
- precision 为 exact Fraction、Boolean monomial basis、exact no-pivot PSD elimination；
- parameters 列出上述12组，full_small_parameters 列出前三组。

因此可以认证的是：冻结代码所指向的一次 fresh exact CLI 输出与作者输出逐字节一致，并且输出内容与第一份审计 JSON 相同。不能由此认证任意未列参数、审计程序以外的源码、运行环境复现，或 root 对未列软件的独立数学证明。

## 4. 未检查项目与可推广边界

root 范围 JSON 明列未检查：

- 任意参数的全称定理，而非12组有限枚举；
- 显式 sparse-support 构造软件；
- affine classification 软件；
- AND extension 软件；
- deep shared-owner common law；
- general scheduling algorithm；
- SDP finder。

主源解析正文另有数学结论：对任意偶 \(d,s\) 的真实 assignment law、共同 M3、全局 degree-two load localizers、row first/pair CONFIG 证书、Fisher–Yates first/pair 稀疏压缩，以及仿射/忠实 AND 的边界条件。这些结论来自解析证明和明确合同；本 JSON 只支持其中有限参数的实现核对，不把有限 audit 当作解析证明。

尤其不能从 audit 的 exact PSD 推出：

- growing-depth shared-owner law；
- 原始星之外任意接线的共同低载证书；
- relaxation integrality gap、near-two hardness 或 NP/UGC 下界；
- 一般 unrelated-machines 调度算法；
- 任意新增 payload 后的所有机器局部化。

## 5. 与全仓相关对象的关系

主源 canonical research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md 已将四个精确身份分开：全局 quadratic local、uniform cardinality first/pair sparse support、affine Boolean owner boundary、忠实 AND localizer obstruction。关联审查 research/reviews/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundary_review.md 又区分各 Exact-first、作者 read-after、最终稿读后与 root 软件范围。

本对象只保存 evidence/runs 两份 JSON；不重复登记 canonical 的解析 theorem，也不把历史先行/作者读后顺序改写为本轮独立数学证明。实际 OPT=1、坏质量、PSD rank 和 CFG 矩匹配都属于同一原星局部身份。任何新增 child payload、共享 owner、不同 machine 合并或 AND 接线都必须回到 canonical 的单行 slack、pair 和全部原 jobs 合同，不能由这里的有限 passed 或字节一致性自动承接。

## 6. 证据字节与重放限制

本轮 clean show 后保存的原始证据副本为：

- tools/evidence/private-tree/seven-state-star/seven_state_star_global_quadratic_audit.json，6210字节，SHA256 9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335；
- tools/evidence/private-tree/seven-state-star/seven_state_star_global_quadratic_root_replay_scope.json，1985字节，SHA256 365f4b15b962accb5a88626708136e0873a6012480c6d1dff1e7ca3d10357b07。

这两份副本是 JSON 结果和范围记录，不是审计源程序。主源报告的129行代码 hash、作者输出 hash、fresh CLI 命令和 not_checked 清单均按第二份 JSON 原样保留。本轮没有重跑审计程序，也没有声称可以从网络或缺失 promisor 对象取得更多代码；最初 clean show 的代理连接失败后按原命令重试成功，未见认证错误。
