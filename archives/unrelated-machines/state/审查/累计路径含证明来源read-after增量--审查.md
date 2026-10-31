---
id: "unrelated-machines/cumulative-path-source-proof-read-after-increment-20261031"
kind: "review"
type_tag: "审查"
title: "累计路径含证明来源 read-after 增量"
status: "integrated-source-proof-read-after"
truth_status: "full-source-read-confirming-existing-counterexample-and-scope"
review_level: "clean-show-full-read-cross-archive-comparison"
scope: "partial_sum_take_continue flat-menu actual escape source-proof read-after"
source_refs:
  - "source:65d6824ea7742ca5603d:history/source/notes/unrelated_machines/partial_sum_take_continue_source_proof_read_after_review.md"
source_sha256: "fcad85bc9d4142f883a515dae08e72e3a421a9ab244f3c98c8c32c122e236d77"
evidence_paths:
  - "../../tools/evidence/cumulative-path-read-after-20261031/original/partial_sum_take_continue_source_proof_read_after_review.md"
related_objects:
  - "累计路径反例的误标签纠正与陈述先行全任务证书--审查.md"
  - "均匀线菜单原证与累计路径合并稿的版本审查--审查.md"
  - "../计算/双见证查询染色与固定矩阵证书的原程序核验--计算.md"
---

# 累计路径含证明来源 read-after 增量

## 1. 来源和身份纠正

本次完整读取 `history/source/notes/unrelated_machines/partial_sum_take_continue_source_proof_read_after_review.md`。
来源 ID 为 `65d6824ea7742ca5603d`，大小 5,454 字节，SHA-256
`fcad85bc9d4142f883a515dae08e72e3a421a9ab244f3c98c8c32c122e236d77`，原文保存在
`tools/evidence/cumulative-path-read-after-20261031/`。

它实际读后的对象是含完整构造、达界 allocation、actual schedule 和 lower proof 的
`partial_sum_take_continue_flat_menu_actual_escape_exact_v1.md`（源 SHA
`27d2926563eeb34591ca44a75cf09ca623719827a67eedff485edf78e22053ac`）。因此本页沿用
现有《累计路径反例的误标签纠正与陈述先行全任务证书》的历史区分：这不是 statement-only
盲审，而是作者 proof-aware 的 read-after。其结论是“source-proof read-after 通过、无
standing fatal”；它确认已有反例和完整 lower，没有创造第二个反例。

## 2. 反例对象与实际任务计数

对象为 3 名 agents、2 枚不可拆全局资源 `u1,u2`，每人每件原值 `3/5`，take state
沿路径采用 additive split `c` 与 `1-c`，随后有 off/own 和 fresh accept。每个 agent
五个 indexed states：`take1`、off、`take2`、off、accept；每 agent 7 incidences、
3 selectors。完整矩阵保留 26 台机器、30 个 jobs、57 个有限资格：9 selectors、21
incidences、15 private 与 11 resources。未选 state、off state 和零负载 resource
机器都保留；没有把同名资源端上的不同 jobs 合并。

作者读后核对的达界 allocation 对三人分别取 take1/take2/accept，领 `x_a,y_a,z_a`，
质量分别 `2/5,3/5,1`，故 max-min `V>=2/5`。若所有组 minimum 都大于 `2/5`，
每个 take1 必须领唯一共享 `u1`，三个 agents 不能同时领取，故 `V=2/5`。

完整 actual schedule 的 9 selectors 中，每 agent 选上述三种 states；9 个
`x/y/z` incidence 外送，其余 12 个 incidence 留在各自 private。每个 agent 的
private loads 是 `8/5,1,7/5,1,1`，辅助资源各负载 1，完整峰值为 `8/5`。读后强调
这不是只对 selected bundle 的 partial certificate：全部原 jobs 都执行，off-state
jobs 和未选 state jobs 不删除。

## 3. 任意完整调度 lower 与 decoder 范围

若完整调度峰值 `C<8/5`，每个 `r` 的 selector 只能在唯一 take1 private；其
`u1` incidence 若留在 private，则 selector 与该 incidence 已合载 `1+3/5=8/5`，
所以三枚 `u1` incidence 必须都导出到同一 resource machine，形成单位负载 3，矛盾。
这一 lower 不限制 m/l 的 state、其他未选 state exports 或 job 顺序，故与具体 schedule
上界合起来给 actual `OPT=8/5`。

反例的 decoder 目标是对每个原 agent 给出统一正 partial value（源中 `delta=2/5`）。
但原 allocation 里最多一名 agent 能取 item，三人同时正值根本不存在；即便允许重新
分配全部原 items，也不能得到所有 agent `>=c delta` 的证书（任意 `c>0`）。失败是
输出存在性，不是算法慢、选错 path、数值近似或删掉某条 take edge。

范围必须保持局部：该对象只否定上述 additive partial decoder 合同，不否定完整
normalized-leaf selector-tree、只要求 welfare、另给 source positive promise、完整
AND/guard、不同 processing times 或其他 DAG compiler。读后没有把外部 selector-tree
文件的引用和 SHA 当成本次已读或已认证接口。

## 4. 与已有版本和证据的关系

已有《累计路径反例的误标签纠正与陈述先行全任务证书》已经承重：

- 含证明 Exact 原 source 与实际 30 行时间表；
- 旧 review 的 proof-aware Fraction/矩阵核验及 scope 纠正；
- 真 statement-only 与其先行独立 30 行证书；
- selector-tree normalized leaf 与新增 additive split/ fresh accept 规则的合同分界。

本源的唯一增量是对“先读 statement-only，再首次读含证明 source”的顺序、完整任务
计数、`8/5` lower 的量词和未读取外部 selector-tree 的明确记录。它与既有正式计算页的
`26 machines/30 jobs/57 finite entries/peak 8/5` 证据一致；本次没有运行软件、枚举
或重新生成时间表，也不把已有 Fraction 证书冒称本次运行。

## 5. 处置和后续

本源处置为 **integrated-source-proof-read-after**：原字节保存，正文登记到既有累计
路径反例版本链，数学主承重仍在已有反例/计算页，不建立新定理。第三阶段可将
“statement-only → 先行独立重构 → source-proof read-after → scope correction”作为
证据关系；不可将 read-after 说成盲审，不可把该常数反例推广成所有 partial-sum DAG、
一般 UM hardness、全球新颖性或六人 SPE 目录覆盖结论。
