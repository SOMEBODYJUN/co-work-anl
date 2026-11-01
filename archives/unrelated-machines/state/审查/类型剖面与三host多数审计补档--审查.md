---
id: "unrelated-machines/type-profile-three-host-audits-20261101"
kind: "review"
type_tag: "审查"
title: "类型剖面与三 host 多数审计补档"
status: "integrated-with-fixture-boundary"
truth_status: "scoped-source-read-no-runtime-claim"
review_level: "full-source-read-and-dependency-failure-record"
summary: "完整读取 santa_block_type_profiles 与 three_host_majority_selector 两个程序。两者的核心构造、精确输入合同和 audit 逻辑均已读；本轮运行分别因缺少 canonical type-profile note 和 three-host fixture 停在 provenance/fixture 读取，未伪造输出。"
source_refs:
  - "source:527e3ce1a38dd835a3041166ce4afed3ecbcefee:tests/audits/unrelated_machines/santa_block_type_profiles.py#sha256=64ffa9b8d6d3fb4ff253b53a2c1d1772f73c300363ad1dfa218517321b8dfd86"
  - "source:daa356b0c00acc6196c9855a0ba7cb6b46615b50:tests/audits/unrelated_machines/three_host_majority_selector.py#sha256=ffab0e3ea7e7317edeeb9ac2a3a86c110d31290d61da9eb0301afa2a3d65c437"
  - "clean:7feaa69432a70730e5ce"
  - "clean:1a8d415a8aa04385775e"
evidence_paths:
  - "../../tools/evidence/agent_um-20261101/batch11/"
related_objects:
  - "unrelated-machines/type-profile-compression"
  - "unrelated-machines/three-host-majority-selector"
---

# 实读和依赖边界

两项 source 均 clean show 导出并逐行读取。santa_block_type_profiles.py 生成 one-stage profile palette、rounding tags、block cuts、empty-zero copies、integer matching 和 exact face-chain audit；它在结果树中读取 type_profile_compression_and_matching_rank_bridge.md 以登记 note hash，但该 canonical path 不在当前树，运行停在 FileNotFoundError。three_host_majority_selector.py 实现三 host 单位预载接口、binary monotone splice 和 3T/2 constructor；其 audit 需要 examples/unrelated_machines/three_host_selector_sharp_profiles.json，当前树无该路径，未伪造输出。

# 类型剖面程序

程序对每个 processing time 采用 exact descending palette，按 epsilon/n 计算 cutoff、block sizes 和 bound；rounding 保证 rounded<=min(value,1)，非空 tag 保留 1/(1+delta) 比例。它随后检查 lambda vertex、face dimensions、integer choices、permutation matching、all final row loads<=C+B 和 support zeros never reopen。程序明示指数 lambda/integer enumeration 只是 audit，不是 production polynomial LP backend，也不提供 general UM approximation/hardness。

# 三 host majority selector

程序输入两份实际完整调度：S1 只让 host a free，S2 只让 hosts b,c free，固定 T 预载。它构造 actual complete schedule，使用 original finite edges 和 monotone binary bootstrap，再通过 finite assignment oracle 检查 3T/2 bound。代码严格区分 ordinary jobs、special host jobs、zero-valued/unused goods、arbitrary host IDs、empty and zero boundaries；缺少 fixture 只影响 registered sharp examples，不改变源码的输入校验和构造语义。

# 处置

两源均处置为 integrated。源码和两份依赖失败日志保存在 batch11 evidence；由于 canonical note/fixture 缺失，本批不宣称 runtime counts。结论限于类型剖面与三 host majority 的 scoped contracts，不升级为一般 unrelated-machines approximation、NP-hardness、外部新颖性或 customer-attraction/SPE 结论。
