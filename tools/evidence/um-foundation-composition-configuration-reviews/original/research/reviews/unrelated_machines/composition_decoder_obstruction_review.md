# 组合放大与物理解码接口的独立审查

审查角色：内部 independent decoder attack；未建立独立 Work 身份，不执行 Git 推送。本稿只把现有两项精确合同放在同一量词下，避免把局部 gap 或 decoder 接口升级为 `UM-TARGET-v1` 困难性。

## 审查对象

1. `UM-PRIVATE-GRAFT-NO-AMPLIFICATION-v1`（正文 `private_graft_and_resource_repetition.md` §2–3）：需求树的私有终端替换和固定整数需求根门。
2. `UM-PREFIX-ATOMIC-DECODING-v1`（正文 `succinct_prefix_atomic_decoding_bridge.md`）：给定全局原子前缀权的确定性逐任务解码。
3. `UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1` 及其 tiny 推广（正文 `unit_presence_two_witness_sharp_gluing.md`）：给定同一输入的两份严格见证时，裸 unit-presence 混合的胶合界。

## 独立重构与结论

私有串接的需求值满足
\[
 b^*(G\circ H)=\min\{b^*(G),b^*(H)\},
\]
而固定整数根门是有限 `max/min` 格式。对单一变量 β 的任意有限私有组合，值函数为 `max(a,min(b,β))`；若 YES 端保真（`f(1)=1`），则 `f(β)\ge β`。因此这类组合无法把固定 NO 比例继续压低。该结论是组合恒等式，不依赖有限枚举或复杂度假设。

前缀原子证书的逐项解码也闭合：正权前缀总能选到正延伸，完整正权只支持所有机器负载≤T 的原子。因此“给定证书即可构造 T-可行调度”正确；反向 Dirac 证书给出存在性等价 `certificate exists iff OPT≤T`。所以若有总位多项式生成器同时对所有输入输出该证书或一个可靠 `FAIL`，便可判定 `OPT≤T`；半单位共同选择的已知 NP 障碍禁止把该生成接口当免费算法（除非 P=NP）。这不是一般近二困难性，因为一般 `(2−ε)` 算法不必生成该 T 证书。

裸 presence 的两见证合同也通过独立流重构。两份 `C≤T=1+1/k` 实际调度可在每个指定混合 presence 上构造 `C≤1+ceil((k+2)/2)/k≤3T/2`；其四机、`2k+6` 任务族让 mixed 最优值恰为该界，并随 `k→∞` 趋近 `3/2`。tiny 时间 `≤a<1` 的加权二选流给统一 `3T/2`。故任何复制器只观察同一 Boolean 的裸 unit-presence、允许匿名 tiny/任务身份自由切换、且无跨模块共享锁时，不能用两份 strict witness 强迫近二费用；必须引入任务身份、medium 端、不可私有化共同资源或全局 source decoder。

## 范围与未决义务

以上三条均未证明 `UM-TARGET-v1` 的算法或困难性。私有恒等式不覆盖跨模块共享；presence 胶合不覆盖未知 witness、额外外部模式或被锁定的任务身份；前缀证书障碍不排除别的近二机制。真正未决的是：构造位多项式、可验证的跨模块整数一致性/全局 source decoder，同时避免私有 `max/min` 无放大、完全共享导致分数整数化，以及裸 presence 的 `3/2` 胶合逃逸。

Evidence：三份正文与对应内部审查；本稿没有新增实验或外部 theorem import。Status：声明范围内无 standing fatal；外审、新颖性、一般复杂度结论均未认证。


## boss11：公共尺寸判定的冻结核心遗漏（2026-10-18）

原实现和正文未先拒绝 `B<max f_i`，其“满流 iff 全机峰≤B”陈述在此处错误。root实际运行原程序确认：`f=(2,0), q=1, E_j={machine2}, B=1` 返回True，而完整矩阵枚举最优值为2。该原fatal属于判定证明/代码，非定理输入域或最优值定义的变更。

内部审查者fee_cascade_review先仅据修复Exact独立证明：guard必要；通过后各`floor((B-f_i)/q)`非负，容量满流与每台原机完整负荷约束双向等价；候选集的`t=0`保留孤立冻结机器，空新任务应返回`max f`。随后实际阅读现有正文/代码，作者修复后再核读另记。root加guard与两条反例/空任务回归，并逐候选检查判定值等于真实最优阈值比较；没有改写原有来源字节，也不将这项精确接口当一般近似算法。

最终独立审查原字节见`history/source/notes/unrelated_machines/unknown_target_common_size_guard_independent_review.md`：修复/孤立机通过；当前脚本仅tiny feasible+brute审计，无二分/分配后端，1200长链实际RecursionError已记录。独立scratch扩大核验不冒称root运行或一般证明。
