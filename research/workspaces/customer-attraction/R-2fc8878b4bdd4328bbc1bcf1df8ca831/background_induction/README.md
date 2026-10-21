# 合法背景封闭归纳：当前备份

目标仍为一般共同目录、任意人数、每份完整历史纯 SPE 的 Q-CAG-HALF。

当前最重要文件是 `coverage_opportunity_step_obstruction.md`：
23 单位客户、合法背景 (2,5)、剩余三人的完整 SPE，严格否定
`u+a+freshOPT_(r-1)(b+A)>=freshOPT_r(b)`。该局部充分条件原本可直接归纳
整体候选 `P+新增覆盖Δ>=freshOPT_r(b)`；反例只说明归纳须保留尾部正余额。
整体候选与一般半覆盖仍 OPEN。

精确复核：

    python3 research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/audit_coverage_step_v2.py --check-only

23 客户 v2 冻结证据为 `coverage_step_exact_audit_v2.json`。488 发现源保留在
`coverage_step_lp_candidate.json`，归一化重数乘 488 得最初整数实例；两者不可混同。
无 v2 的 audit 脚本与 JSON 是开发过渡文件，不再用作引用入口。

其他工具：`probe_coverage_step.py`（集合值 SPE oracle 局部式有限探针）、
`probe_coverage_step_lp.py`（完整固定策略锥及残余最优值 epigraph）、
`minimize_step_counterexample.py`（固定策略下整数压缩）。

`two_player_fresh_certificate.py` 尝试用两个根比较分支、其末回复和全部跨末节点比较
为整体候选的两人背景版本做统一非负系数证书。当前该三分支模板的非负乘子 LP
不可行；这只说明所选接口/逐客户余项模板不足，尚未产生合法完整策略反例。

额外有限攻击：真实合法 prefix 的 q6,r2 固定完整策略锥 1000 棵，
seed=293877，未找到整体候选负值；`artificial_background_probe.py` 允许每个类型
独立负载 0、1、2、5，q6,r2 400 棵策略亦未找到负值。后一个输入类刻意扩大，
没有把任意人工负载冒充由共同目录过去行动生成的背景。两项都不是普遍正面证据。

下一步：对 `P+Δ` 整体候选继续攻击；解析方面寻找可支付上述负首步余额的
尾部 surplus 状态。BNS/AP 的逐节点 δ 总和尚无合法全局预算，不能直接相加。
