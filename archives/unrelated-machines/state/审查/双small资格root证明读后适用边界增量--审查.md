---
id: "unrelated-machines/two-small-incidence-root-proof-read-after-boundary"
kind: "review"
type_tag: "审查"
title: "双 small 资格 root 证明读后与适用边界增量"
status: "integrated-read-after-prior-overlap"
truth_status: "restricted-class-proof-confirmed-prior-overlap-recorded"
summary: "全文读取双 small 资格三半对象的 root frozen proof、read-after literal 与 independent shared source；CONFIG/ordered-slot 全 OPT 包装和 selector-leaf 3DM 锐界均成立。2018 bounded-job machine-plan 论文与 common-unit 适配有直接机制重叠，不能宣称新算法框架或一般 UM 结论。"
source_refs:
  - "clean:adb4060c7c11e0737fbc"
  - "clean:90a327a76285c1743a37"
  - "clean:6b68f29bc397b15f6496"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_read_after_literal_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_read_after_shared_scope_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_root_frozen_proof_source.md"
related_objects:
  - "unrelated-machines/two-small-incidence-sharp-v2-three-source-review"
  - "unrelated-machines/two-small-incidence-sharp-v2-finite-audit"
---

# 1. 读后对象身份与范围

三份来源绑定同一 Exact 对象 `UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`（Exact SHA
`051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`）。root proof 的实际 SHA 为
`63da068c732421f76efa84cac37ad15d3e6fd24cc86af605403a344eadaf809a`。三份不是三篇独立论文：root frozen proof 承载主链，read-after 与 independent shared source 分别给读后核对及另一种正确推导。

域为显式 unrelated-machines 矩阵：给定共同 (b>0)，每行不同正 small 资格至多两条，unit 资格恰为 (b) 且数量任意；zero 资格、跨行任务支持和共享机器均允许。该结构不能扩展到三条以上 small、不同的大时间或一般 UM。

# 2. root 证明主链核对

* 对 (T<b)，去掉 zero 任务后，每行至多两条 eligible small；同机两条和不超过 (T) 时容量为 2，否则容量为 1。整数二部流与真实 (C\le T) 调度等价；候选最优值只来自单端或同机两端之和，数量和位长多项式。
* 对 (b\le T<2b)，写 (T=b+a)。枚举真实 CONFIG（每行至多一枚 unit 与两枚 small）得到完整配置 LP；按处理时间降序铺有序槽，分数 matching 整数化。若 (Q_i>2)，正权三任务配置必为一枚 unit 加该行两 small，故两 small 之和不超过 (a)；若 (Q_i\le2)，把 unit 及 (p>b/2+a) 的 small 视为 big，任一可行配置至多一 big，最终负载不超过 (3b/2+a\le3T/2)。
* 若 (OPT\ge2b)，普通 assignment-load LP 的最优值 (L\le OPT) 经同一 ordered-slot 舍入给出 (L+b\le3OPT/2)。在中间区间收集有限真实阈值并取最小可行者，合并得到全输入 3/2 近似，不调用 OPT oracle。
* selector/leaf 3DM 归约中，每个 A 元素是一枚 unit selector；每个 triple 根有两枚 1/2 leaf，分别连接 B、C unit resource。YES 调度峰值 1；若峰值严格小于 3/2，每个 selector 根的两 leaf 必须外送且 B/C 资源不能撞，从而解码 perfect 3DM。该下界仅针对 common-unit、双 small 行域。

这些步骤与 independent source 使用的直接 machine-capacity flow / triple-job 构造互相独立而都正确；不把两套归约拼成一份来源，也不把有限脚本 PASS 当作全称证明。

# 3. 与已有技术的重叠

本次 read-after 另读 Page--Solis-Oba--Maack, COCOA2018 accepted author version 的 bounded-job machine-plan、Fig.5 和 Theorem 2。其字面定理按每机全部 eligible jobs≤2/3/4 给 exact/3/2/5/3；本文的 common-unit 域并不字面满足“全部资格≤3”，但在阈值 (b\le T<2b) 时可把所有 unit 作为一个真实 unit 组容量一，small 至多两条，复用其 big-buffer/slot 机制。由此可得相同的 (3/2) 上界，但这属于直接适配和机制重叠，不能写成独立新算法框架或新颖性认证。统一缩放可处理有理时间的编码；这也不把文献定理的整数声明偷换成本文全域定理。

# 4. 处置与未决

三源完整阅读、比较和去向均已记录。本增量页保留 root proof 的承重细节、read-after 的 prior 重叠和范围边界；正式数学对象仍由《双小资格三半锐界三源精读》承载。没有生产实现、一般 UM 近二正反面、外审或论文新颖性结论。严格阈值 (C<2b) 与 common-(b) 假设必须在后续引用中保留。
