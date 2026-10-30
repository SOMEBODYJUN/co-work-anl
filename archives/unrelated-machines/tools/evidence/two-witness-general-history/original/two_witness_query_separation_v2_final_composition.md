# 一般双见证查询分离 v2：最终组合审查冻结

审查者：boss11 内部 typed_edge_gap，2026-10-18。

读取对象：
`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/two_witness_query_separation.md`

读取时 canonical SHA-256：
`89d4629b55e985c2a1351e8fa6b7331b61939c9be10710f83bff772fa94fbf12`

**结论：数学正文通过最终组合审查，未发现超出 UM-TWO-WITNESS-QUERY-SEPARATION-v2 Exact 的量词、对象或结论。审计代码仍 pending；本审查没有运行、见证或确认任何代码审计。**

先后顺序：先只据 v1 Exact 独立重构一般 P 的上界；再只据 v2 Exact 独立构造五机锐例并冻结；之后读作者 proof v2 并冻结 read-after 对照；最后读本次 canonical 最终组合。前序独立稿分别为 `two_witness_query_separation_independent_typed_edge_gap.md` 与 `two_witness_query_separation_v2_sharpness_independent_typed_edge_gap.md`，均在本次最终正文读取之前完成。

## 逐项核对

1. **一般 P 域。** 没有引入 unit/home、两端、单正小端、图度数或权值比例限制。输入是同一显式非负有理/∞矩阵的两个完整实际 T-feasible 见证。D 以 owner 不同定义，允许两使用端时间不同、任一或两端为0。构造从已合法见证使用端二选一，不触碰∞；每 job 恰分配一次。
2. **单 query 及不交支持。** 每 query 保持自己初始颜色，只有非 query 出弧由其唯一 source 赋色。触发机器每台至多一次，每非 query 弧至多一次；总目标注入≤T 排除两个颜色同时超过 T/2。终止条件对未触发机器和其它颜色机器均有效。τ_q 恰移动 q 与 A_q，其他 queries 全留初始 owner。A_q 两两不交；正文明确未升级为所有查询子集的同界 cube。
3. **全机负载。** 未标 q 的机器≤baseline T+流入 T/2。标 q 的机器已移走其全部非 query 改派出弧；固定 jobs 加已入 jobs 是 σ1 在该机的子集，≤T，唯一可能额外留下的旧负荷是 Q\{q}，≤δ_q。故 max(3T/2,T+δ_q) 同时适用全部机器，而非平均界。
4. **3/2 sharpness。** 六机五 job 表是我先行五机例（两个 query homes 合并，各 query a=η/2）的同型机制。σ0/σ1 均 load≤1。每 singleton 真可达 load1，而对 B<3/2，q_i 的 unit 占据强迫 x_i 回 R，其1/2与 f 的1−γ相加>B，故共同 f 必须改派。所有 jobs 二端、唯一正小 home、其余端为 unit、p≤1。baseline 预导出的 x_i 权0，f baseline small、on unit；新增费真实为1，无预付费/退款伪装。只证明分离/费用合同的阈值锐性，正文多处明确 OPT≤1、没有 UM ratio hardness。
5. **费用解释。** W 是全部非 query 指定改派权总和，并非任意实际成本或净退款。仅给 σ0 非 unit、σ1 为 unit 的非 query 任务以非零权，其余权0，才可把它实例化为新增 unit 费。已有 baseline unit 背景费用和被移除旧 unit 的退款另算；canonical 已明确禁止用退款后的净值冒充 W。权不参与染色，非负性仅用于费用求和上界。
6. **T=0 与有限边界。** 两实际见证使用端全0，阈值无触发，A_q=∅，仅 q 改 owner仍全0负载。Q 非空自动令 D 非空；空 task 域不产生伪查询。任何有限见证都保证每 job 有可用端。
7. **终止与字长。** 至多 m 次触发、|D| 次弧赋色；显式 m|Q| 表、固定顺序扫描及 n|Q| 输出均多项式。只做有限有理和与比较，部分和分母位长至多输入分母位长总和，分子再加多项式位数；没有数值大小、精度倒数或2^|Q|循环。锐例的 η,B 若作有理输入，可显式取 γ=(3/2−B)/2（B≥1时满足所有严格界）、a=η，得到常数规模和多项式字长；B 若仅为固定实常数，则选相应区间内有理 γ，不能把实数直接当二进制处理时间。

## 审计状态保留

本次仅核自足全量词证明、显式锐例和最终文本组合。没有执行尚 pending 的 `tests/audits/unrelated_machines/two_witness_query_separation.py`，没有确认32个混合分配枚举、运行输出或 certificate 文件已生成。canonical 的 Evidence/Related Files 文字若后续保留“32个混合分配/对应运行”，其完成状态须由实际审计另行确认；不能引用本审查作为已跑证据。
