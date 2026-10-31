# D/E canonical 最终 scope note 与 E 固定 checks 实际读后

本次实际全文重读 canonical：`co-work-anl-boss11/research/current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md`。

Current SHA-256：`f740e8daec3e837c58b14ff227eb6835c1720e00f89639fc2b9595677b187633`。

旧 canonical 的 read-after 记录 `line_and_take_continue_canonical_read_after_review.md` 仍为 SHA `7d889ec99de26316b9c81be7b2e0ebcce4b75e3d6bdfdc79e3c2684fa493498b`，原字节未改。本次另存补充，不覆盖旧记录。

## 1. 两处变更精确闭合

实际核 current 的 D tuple-as-group 句已经改为“不再自动保证 r_x≤R 与直线不重合，须重证这些不变量”，不再断言每个实例必然破坏。该措辞正确维持：constraints-as-groups 的 3/2 合同不排除其它 tuple-as-group 加 dummy compiler。

E 的 evidence 句已写成完成的五行 state 表独立重建、全部 finite rows/原jobs/loads/bundles 的 Fraction 回算，并链接实际 audit 与冻结结果。root 也明确告知本次运行已完成，取代旧任务时的 pending 状态。

在内存中只逆替换上述 D 句与 E evidence 段，整文件 SHA 精确恢复旧 `c50fb9792f101967a996913f2c6ac4269035143fe2a137b831dfdbdcd6c40eee`。所以数学主体、完整矩阵及先前已审的两份 proof 没有其它字节变动。

## 2. 实际读取的 E audit/evidence 文件

已实际全文读取：

- `evidence/runs/unrelated_machines/query_return_source_obstructions_v1/root_full_matrix_verification.json`，SHA `07d0f020b04ae45bfc3a00495414e56ea7da1078c73be16dccafa89de096f757`。
- `tests/audits/unrelated_machines/audit_query_return_source_fixed_certificates.py`，SHA `5a338e62d31512260d6ab41c479cda482f6fd0d4cb3b28e31e8a956ccd339a74`。

这两个文件也含 sharp/C 的另一固定例。本审查读到了这些内容，但**正式 checker/evidence 认证范围只为 E 的 take_check 分支与 take_continue 输出**；不发 C 算法、5184 枚举或其它 source 的通过结论。

## 3. E 分支代码职责确实与声明相符

`take_check` 从 canonical 的每 a 五行 state 表独立重建 states、private/resource IDs 和每原 job 的全部 finite entries，不调用证书生成器。它比较输入 cert 的 states/jobs 与重建字典精确相等，核26台不同 machines、30jobs、57finite entries、9selectors、21incidences。57=15个 selector finite ends+42个 incidence finite ends，和解析计数一致。

`actual_loads` 要求 assignment job keys 恰等于全部原 jobs；逐 job 校原目的机资格，并按重建 processing times 用 Fraction 累加，包括所有 unselected state jobs。结果含全部26台机器，与 cert loads 精确相等、峰精确8/5。它核 assignment/load 证书，不校另给的 start/finish 区间；普通 UM 可逐机串行，先前解析30-row证书已给相应实际时间表。

bundles 分支对全部9个 groups 校 selected state、组内资源无重复、资源在所选 row 内、全局互不相交；校 selector 的真实目标与每 bundle incidence 的真实 export；Fraction 回算全部 group qualities，minimum精确2/5。

E 分支没有 optimization enumeration；脚本的 product 枚举位于另一个 sharp_check 分支，不把它归给 E。输出明示 audit_only，take_continue.optimization_run=false，lower bound 来自 canonical proof 而不是这些 checks，scope 正确。

## 4. root 冻结结果的内容和归属

已读 JSON 的 take_continue 部分记录：machines26、jobs30、finite_entries57、exact_witness_peak8/5、witness_partial_value2/5、all_original_jobs_and_loads_checked=true，并指明 analytic lower 不由该 check 推出。与所读 E checker 及先前独立解析证明一致。

该结果记载其输入 take certificate SHA 为 `9cf13ec0f81346889d177095e1c04b0dac13230ff8fd13f3fc8d23e537edd2f7`。本审查本次没有另行读取那个 raw certificate 文件，故此 SHA 只按 root 输出的输入归属记录，不冒称亲核其原字节。

**执行归属：软件是 root 实际运行，本审查没有运行它。** 本次贡献是实际读 current/代码/冻结输出并核职责、范围与数学一致性；不把 root 或 general 的 Fraction 运行改记为自己的实验。E general 早期 proof-aware误标签与更正、本人真正 statement-only→独立30job→source-proof 的先后仍按旧记录严格分开。

## 5. 最终结论

**Current f740e8…的 D/E 主数学保持通过；旧记录的两处 scope/provenance 意见已闭合。** E 固定实际证书的 checker/evidence 职责与输出相符，保持 audit_only，不替代 V upper、任意 actual schedule lower 或一般 decoder 量词证明。

认证范围不含 C 算法、未读 raw input certificate、其它 compiler 或一般 UM 目标。只在 scratch 写本 note；未改 repo、旧记录、Work 或 Git，未运行 root 软件或做其它枚举。
