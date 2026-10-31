# 多小端柔性密度流障碍的独立攻击

## 审查对象

`UM-SMALL-DENSITY-FLOW-BARRIER-v1`，正文为 `research/current/unrelated_machines/mixed_small_endpoint_density_flow_barrier.md`。

## 先行重构

审查者独立重写了 `S_j`、`d_j`、`t_i`、`b_i` 与 `rho_i`，在 small 端图上给任务 `j` 的每个端点质量 `1/d_j`。该分数流的任务列和为 1，机器行和为 `rho_i`。容量 `ceil(rho_i)` 的整数二部流因此覆盖每个任务，叠加 `Q` 的容量 1 unit 匹配后逐机得到 `1+ceil(rho_i)/k` 的负载界。

## 攻击结果

1. `b_i≥γt_i` 必须逐机成立；若只给全局平均柔性密度，柔性 incidence 可集中在少数机器，结论不成立。
2. `d_j=1` 只说明 small 端没有跨机选择；若同一任务还有 unit 端，不能把它称作整任务没有其它标签通道。
3. `Q` 无容量 1 匹配时，任意 `C<2` 调度都会给出每机至多一件 `Q` 的匹配，故 `OPT≥2`。这里要求 `Q` 的所有有限边确为时间 1。
4. `Q=∅` 时只能得到绝对 small 负载界，不能无条件改写成相对 `OPT` 比率；正文已明确这一点。

## 结论

证明范围内没有剩余致命漏洞。该命题是 `{1,1/k}` 物理编译的结构性流障碍，不是一般 UM 算法或复杂度下界；尚未审查多尺度、medium 端和任意联合 decoder。
