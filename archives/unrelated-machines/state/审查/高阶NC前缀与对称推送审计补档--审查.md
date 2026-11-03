---
id: "unrelated-machines/higher-nc-prefix-symmetric-audit-programs-20261101"
kind: "review"
type_tag: "审查"
title: "高阶负相关、前缀原子解码与对称推送审计补档"
status: "integrated-finite-evidence"
truth_status: "scoped-exact-audits-with-explicit-open-boundaries"
review_level: "full-source-read-and-local-replay"
summary: "完整读取三份遗留审计程序。高阶 NC 程序本地精确复跑 15 个 tail case、5 个 expectation case 和 50559 个带标号原子；前缀原子程序三类边界全部通过；对称推送程序在 q=2..8 精确复跑，保留 q=9..32 仅公式未运行。三者都只是合同级有限证据，不给一般 UM 算法、hardness 或客户 SPE 结论。"
source_refs:
  - "source:4af61e3549a5f57f1f5f5e7d2afc26c24a800a4a:tests/audits/unrelated_machines/private_sink_higher_order_nc_independent.py#sha256=bb818bb741c8c4b0aac5405caa4170a8e134bd1c50c987193e91a2d0e69c0b8c"
  - "source:d54d4195dbb67f14ad2bdec977f0cc35ad13a4f3:tests/audits/unrelated_machines/succinct_prefix_atomic_decoding.py#sha256=8e83d068c1476bb422f9a4705df0e0bfa32a577cebb1ea95acf0b36b197773b4"
  - "source:d08d3dacb33f17e9a91849ee77539325f360bdbd:tests/audits/unrelated_machines/symmetric_reset_pushforward.py#sha256=58b2b76dbcd98fbbe3c25d8ef3588660a4ad37d9d9a2d7f4e03eb736644cf0fa"
  - "clean:695f8593e5221aefac5b"
  - "clean:25ea4bfacaf863243a72"
  - "clean:1166d32390520857ca08"
evidence_paths:
  - "../../tools/evidence/agent_um-20261101/batch4/"
related_objects:
  - "unrelated-machines/higher-nc-duplication-cycle-review-20261030"
  - "unrelated-machines/review-prefix-atomic-relative-gram"
  - "unrelated-machines/symmetric-reset-pushforward"
---

# 来源读取和复跑

三份遗留 source 均已 clean show 导出并逐行读取。高阶 NC 程序完全独立，不导入仓库实现；前缀程序只构造 Dirac、uniform、异质端点和不可行原子边界；对称推送程序构造 2q 台相同机器、2q² 项任务的旧 pair matrix、删除机 0 后的确定性 fallback pushforward，以及同一 first moment 下重新构造的真实最优 pair matrix。

高阶 NC 本地复跑输出 Fraction/整数精确，tail_case_count=15、expectation_case_count=5、total_atoms_checked_with_multiplicity=50559、passed=true。它检查每组 B 边际 1/r、每个 small sink 边际 1/r、同 sink 正 cylinder 的 2..d 阶上界、实际 makespan 成功概率与 sharp p* 一致，并验证五个 expectation case 的期望峰值。

前缀原子程序本地输出 prefix atomic decoding exact audit: ok。它核验两任务均匀 law 能选到可行 atom、全零 Dirac 保持零峰值、三件全一任务在两台机器上无可行 atom，以及异质三端点 Dirac 的精确回放。它没有写 JSON，输出保留为 out.txt。

对称推送程序用 --max-q 8 本地复跑，结果 q_range=[2,8]、negative_parameter_checks=70、positive_conditional_formula_checks=70；q=2 的全 balanced assignments 穷举、c=0..4 的 pushforward matrix、same-base reconstruction 和真实 pair matrix 差异检查均通过。源程序默认 q=32 的参数扫描未在本轮运行，故 q=9..32 只按代码读取并保留为未重跑范围。

# 高阶私有汇点 NC

程序实现的有限 law 对固定 k,r,d,q 取 t=min(d,q)，令 p* 为 1 或 min(1, binom(k,t)/(r^(t-1) binom(q,t)))。它以概率 p* 在 B 所在组把 q 个 small 送入同一 sink，并在其它组各送一个；其余概率在 B 组送一个、其它组各送一个。逐原子重算每个机器 home/sink load，确认 Cmax=2-D_h/k，成功概率恰为 p*。程序还枚举计数向量，检查 D_h<q 时阶乘矩组合数下界。

本源独有的是另一份完全展开的独立实现和可执行输出；既有高阶 NC 审查承担一般组合上界、adaptive 量词和边界。有限原子不证明所有参数的 universal upper bound，也不覆盖 all-zero NC、重选 x、采后重排或一般 scheduler。它不产生 UM-TARGET-v1 困难性。

# 前缀原子解码边界

前缀程序的 uniform case 以两个任务、两个端点的交叉匹配 law 运行 greedy；Dirac case 只输出唯一 atom；heterogeneous case 用四项任务和三端点权重测试多个 Dirac atom。不可行边界是三项任务各可去两台 unit machine，8 个完整 assignments 全部峰值至少 2，因此没有 feasible atom；任何 localizer 若强迫非负 atom 权重只能全为零，和 one-hot 归一矛盾。

这些有限例只说明 exact law 下的 greedy 选择和不可行原子边界，不能生成一般守恒 law、全 promise verifier、近似 oracle 或调度器。相关 finite-precision/Gram 审查已经给出一般 sharp bound、相对 localizer、满行秩和误差稀释边界；本源只补充小型自包含程序。

# 对称条件矩推送

对称程序固定 m=2q、n=mq，每任务大小 1/q，D 在每台机器恰 q 项的 assignments 上均匀。删除 machine 0 的 q-job package、保留 q 个 fallback groups，并只将旧 machine-0 choice 映到 deterministic fallback，得到 pushforward 的 x=R x_old 与 y=R y_old。程序逐项检查 row count、true/false conditional capacity 和 pair-matrix 对称性。对 c<2q 的平衡组大小，merged_same 条件行超过 q 至少 (q-1)/(2(n-1))，形成精确 2T 阈值反例；c=2q 时另造同一 first moment 的 regular bipartite decomposition，得到每个 schedule peak=1 的新 pair matrix。

q=2 的全 balanced assignments 被完全枚举，且 pushforward 计数和旧 moment 矩阵一致。q=2..8 的代码公式检查保留 c<2q 的负界和 c=2q 的正重建；q=9..32 未在本轮运行。结论只针对“固定旧 pair matrix、只重定向 machine-0 choice、其它 choice 不变”的合同；同一 first moment 可以有另一个真正可行的 second-moment certificate，因此不能写成一般矩推送障碍或 UM hardness。

# 比较和处置

三源均为 integrated。高阶 NC 接入既有 private-sink higher-order review；前缀程序接入 prefix-atomic review；对称推送接入 symmetric-reset 对象并明确 old matrix pushforward 与 same-base rebuild 的身份差异。源代码和本轮输出保存在 batch4 evidence，q=9..32 未重跑与前缀文本输出格式均如实记录。三源没有一般 unrelated-machines approximation、NP-hardness、外部新颖性或 customer-attraction/SPE 结论。
