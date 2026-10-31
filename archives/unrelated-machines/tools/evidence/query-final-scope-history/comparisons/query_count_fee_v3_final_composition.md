# UM-TWO-WITNESS-QUERY-COUNT-FEE-v3：read-after 与最终组合审查

审查者：boss11 内部 typed_edge_gap，2026-10-18。

**结论：v3 Exact、作者 Proof 与 canonical 新 §5/heavy 的数学组合通过；没有发现域、整数等号、费用或版本结论的 fatal。没有导入一般 UM 困难性或算法结论。**

## 实际来源与读取顺序

1. 先只读 count-fee v2 Exact，独立证明 rich-machine 单射、η=0 分支、正η严格计数与 s=floor(c/η)+1 整数界。
2. 在未读本 count 合同作者 Proof 的情况下，我独立提出 H/S 加强：rich 含heavy可归给一heavy，不含heavy至少2枚非heavy，故 Rβ≤H+floor(S/2)，继而 W≥ceil(S/2)F、H≥d−2floorκ。该来源已先冻结在 `two_witness_query_count_fee_independent_typed_edge_gap.md` 并向 root 发出消息，不是读 root Proof 后重述。
3. root 接纳后另立 v3，不改原 v2 字节。本次正式先读 `two_witness_query_count_fee_v3_exact.md`，再读 `two_witness_query_count_fee_v3_proof.md`，最后读 canonical 当前全文及新 §5/heavy。

本次 canonical：
`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/two_witness_query_separation.md`

本次读取的 canonical SHA-256：
`fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c`

## 逐项最终核对

- **身份与域。** 分离主合同仍为 SEPARATION-v2；新增 §5 明确另立 COUNT-FEE-v3，使用同一一般 P、同一对实际 strict 见证及同一 I>T/2 染色族。计数要求 T>0，β∈[3/2,2)，不把正质量比值强加到原 T=0 分离域。原 T=0 分支保留完好。v3 Exact 历史说明中的“本v2单列”按历史修正来源理解，不把当前 ID 错读成 v2。
- **合格与低费是同一 query。** 作者 Proof 取全部实际 τ_q≤βT 的 G；坏 q 的超载机器必须标 q，且 LQ_i>cT。各机器唯一色给坏 q→rich 机单射。Σ_G fee≤W，平均在同一个 G 内取，故可行与低费没有被分给不同 queries。
- **零η。** η=0 时全部旧 query 质量为0，Rβ=0，所有 d 个合格，至少一费≤W/d；没有保留 v1 的“严格多于d”。v3 heavy 此时给的 ceil(d/2) 只是较弱同时成立界，不替代前述全部 d 界。
- **正η严格阈值。** Rβ>0 时 Rβ cT<Σ_rich LQ≤M≤ηTd；Rβ=0 则 ηd/c>0，所以严格 Rβ<ηd/c 仍成立。整数下界 floor((1−η/c)d)+1 正确。W=0 时费用只断言≤0，没有误用严格平均费。
- **s 的等号。** rich 总量严格>cT，所以 query 数严格>c/η；当 c/η 恰为整数，也必须 s=floor(c/η)+1，不能改 ceil(c/η)。s≥2 的前提仍为 0<η<c。不同 source query 组不交，Rβ≤floor(d/s)，同一个 G 的数量及平均费用同步成立。
- **heavy 的等号。** H 以单件 old size **严格>cT** 定义；等于 cT 属于非heavy。没有heavy的 rich 机，单枚非heavy至多cT，严格rich故至少2枚；允许0时间 queries也不破坏此计数。rich 含heavy的机数≤H；无heavy的rich机数≤floor(S/2)，两类合并不重复占用 source query。得到 good≥ceil(S/2) 以及收费合同下 W≥ceil(S/2)F。
- **κ 非整数。** ceil(S/2) 是整数且≤W/F≤κ，因此≤floorκ，S≤2floorκ，H≥d−2floorκ。没有把未取整的κ当作整数处理；d−2κ虽是可推出的较弱实数界，正文保留了正确且更强的floorκ界。κ<1、S=0、负的右侧必要界均允许结论平凡；没有据此声称相应 gadget 一定存在。
- **费用条件与背景。** W≥ceil(S/2)F 只在上述“每个合法 βT 单 query 模式都至少费 F>0”的合同下使用。W 始终是原非负指定改派权总和；实例化新增 unit 费时只给 σ0 非unit、σ1 unit 的非query改派收费，不能减旧 baseline 退款代入 W。β=2−ε 的 near-unit 结论是这一合同的必要形状，既非充分性，也非 OPT gap。
- **终止、字长与筛选。** 沿用已验证的分离染色终止与唯一颜色。不重新染色、不依赖β/权选择支持；只增加 LQ/实际 τ_q 的有限有理回算、rich 统计和整数除法。s 数值可大但不按 s 或1/η 的数值迭代；所有数的位长及 m|Q|、n|Q|输出仍总位多项式。

## 状态边界

本次只核数学、read-after 来源和 canonical 最终组合；没有运行新增审计代码，没有证明已有32混合枚举或任何 certificate 的完成状态。本记录不是 Work/Git 操作，也不构成外审或新颖性认证。`UM-TARGET-v1` 的正反面没有因此完成。
