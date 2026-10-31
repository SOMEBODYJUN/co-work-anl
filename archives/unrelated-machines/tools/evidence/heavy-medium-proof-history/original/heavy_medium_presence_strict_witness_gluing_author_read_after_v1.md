# HEAVY–MEDIUM STRICT-WITNESS PRESENCE：作者 Proof read-after v1

审查者：general_query_response_review。2026-10-18。

## 冻结对象与先后次序

先只读新 Exact 及获准的既有 unit-presence 基础，独立重构并冻结完整证明文件；之后才首次读取新作者 Proof。以下哈希标识本次审查内容：

- Exact：`f9dad0a0f70f272446042091e0bb400c7a87c6a3f96bae512cfbed34c230183e`
- 独立 Exact-first 审查：`ab6b2472da757bed7428fdb629b386d06b51b78429b0c3c90a1fd15bcbb7a3a9`
- 作者 Proof：`48f5ac5459cfcc5ef62244b830207c72b4700521df9e9e68bc6e5fb8ae82dee1`

独立审查原文件字节冻结不改。本记录不读取或改动其它作者新证明、repo 正文或 Work。

**结论：作者 Proof v1 通过，与独立重构一致；未发现 fatal、边界漏洞或 domain 偷换。**

## 对照与攻击结果

1. **真实 job–machine 二部 heavy 图。** 两实际调度每机至多一枚 heavy，来自 `2(1−ε)T>T`，不是来自精确 unit 或 T=1+a。共同边固定，其端点不可能另有 heavy 边；其余交替分量分析合法。没有把允许任务跨角色误当成 heavy-only 原 job。
2. **两 measurement 分量不同。** v,w 都是仅颜色1存在的 machine 端点；machine–machine 路两端颜色相反，job–machine 路只有一个 machine 端点，因此不能同分量。measurement 不可能是两方向均占位的内部 machine。这足以同时固定 mixed，而不是独立实现两个单机状态后未胶合。
3. **near-heavy 翻转增量没有遗漏。** 单 job–machine 翻转的内部机器可能换成更重的 heavy，作者明确计入至多 εT；唯一新 medium 可落在同一台机器，作者也明确加 aT。因此全机≤(1+ε+a)T≤BT。使用 ε+a<1 正确，不把 heavy 身份交换误写成时间不变。
4. **全部 active 分支与 virtual 选择。** 另一分支把全部 job–machine 分量 active，确实只删去两见证 medium 均值中的 half-medium；job–job 每方向恰留一个真实端点 job 于其另一见证 medium 端。virtual item 是选择编码而非额外执行任务；其选择能恢复完整分量，所有原 jobs 恰一次。
5. **不等成本、同机 virtual 两选项。** 两成本可不同；目的机相同时先选较便宜项，medium 负载不超过半半均值。该选择可能改变其它机器上的 heavy 身份，但那些机器仍至多一枚 heavy、时间≤T，作者后续逐机界已覆盖这种关联，不需要假定所有 heavy 成本相同。
6. **共同加权舍入合法。** incidence 的 job 对与机器对各是匹配，其并图只有路径或交替偶环，可二着色；每 item 恰选一项。按成本排序后的交替差≤最大 incidence 成本，给每台机器相对 half 均值的增量≤aT/2。该性质对全部机器由同一选择同时满足，非各机独立期望。
7. **三类完整机器界。** 两见证都有 heavy 时 medium 均值≤εT，最终总量≤(1+ε+a/2)T；presence 不同时≤[3/2+(ε+a)/2]T；两见证都无 heavy 时 heavy 并图无边，最终只有 medium，总量≤(1+a/2)T。第一、三类均不超过目标 B，第二类正是目标。没有漏掉非测量机或只测量端点。
8. **只要求 witness-used ends。** 作者从头仅保留每 job 两个实际已用端。未使用有限端可在 gap 中、可任意大或为零，不进入分类、匹配、舍入或输出。全部实际任务仍只放 σ0/σ1 原合法端。
9. **退化与位复杂度。** a=0 全成本零仍可配对二着色；ε=0 的 heavy 增量零；相同原端固定；相同 virtual 目的机成本不等可按所选方向解码；静止 heavy 不重复执行。图与 item 数线性于显式原任务数，有理排序、求和、二着色及实际分配输出均为按输入位长的确定性多项式，不按 a、ε、gap 倒数循环。
10. **结论范围。** B<2 用 ε+a<1。物理复制合同的否定来自同一 P 上构造出的实际 mixed，不锁定具体 job 身份、其它外部边界或源标签；不给一般 UM 算法、一般困难性或全参数锐性。原 unit/tiny 身份、时间域与既有锐性不被改写。

作者三行界与 flip 界均与独立证明相同；未发现需要修改作者数学证明的差异。

**最终冻结判断：新 Exact 与作者 Proof 在声明全域内通过。**
