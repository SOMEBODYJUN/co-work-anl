---
id: fair-allocation/recent-literature-frontier-checks-and-laminar4-key-core
kind: resource
type_tag: 资料
title: 近期文献排雷与四代理laminar核候选
status: literature-frontier-resource-no-independent-proof-certification
scope: retired topic-selection source frontier checks; coverage warnings and one precise laminar four-agent trial core
summary: 完整实读近期文献排雷记录，保存六个母文覆盖警报、已被新结果改变的公平/GAP题源、SEL-LAMINAR4-KEY-v1的精确模型量词和首个判别动作。摘要/预印本声称未被独立审完，不能把文献覆盖、有限探针或候选核升级为定理。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_frontier_checks.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_frontier_checks.md
related_objects:
  - ../../../fair-allocation/state/审查/多线候选池实际比较与去重边界--审查.md
  - ../../../fair-allocation/state/审查/公平参数化选题战报与实质试攻边界--审查.md
  - ../../../customer-attraction/state/资料/同行选题比较与候选优先级边界--资料.md
  - ../../../customer-attraction/state/资料/退役选题核验与有限复现合同--资料.md

# 近期文献排雷与四代理laminar核候选

## 来源和使用范围

source_frontier_checks.md 为 4,956 字节，SHA-256 e74ab497f2708ad19a7f7391292a928d0d0822fef6c2831cadbccae34a674202；legacy-cleanup 与 main 版本内容相同。核查日期为2026-10-20，报告来自 boss6 的选题分支接续。它明确是候选扩充前的原始文献和覆盖警报记录，不是新数学定理，不把最新预印本摘要自动当作独立审查事实。

本对象完整实读六条文献覆盖警报、SEL-LAMINAR4-KEY-v1 精确域、依赖、有限探针边界和使用规则；与已有多线候选审查、公平参数化战报和退役核验资料对照。文献标题/摘要层的“已覆盖”“声称”均保留为来源陈述，不替代正文证明核查。

## 六个覆盖警报

1. **Cookson–Shah，Constrained Fair Allocations via Partition Matroid Reductions，2608.31121v1。** 相关 §5 和 Appendix B Def.13–14/Lem.11–12：四代理 laminar 问题约化到两个有限 key matroid 的 EF1 加预指定次序无嫉妒；原文明确未完成。三代理 laminar 与任意代理 transversal 存在性在该论文中已解决。因此三代理/transversal 原题退出前排，但四代理 key 核仍是候选，不能把有限物品枚举误作连续估值全称证明。
2. **Afshinmehr 等，EFX Allocations Exist on Multi-Graphs，2606.18665v1。** 摘要声称 cancelable 多重图估值下存在并可多项式计算 EFX；本轮未独立复核全文。因此不能继续把“多重图 additive EFX 普遍存在”当无覆盖开放题；若研究新输出限制，必须写出真实差额。
3. **Garg–Murhekar，Existence of 2-EFX Allocations of Chores，AAAI 2026。** 官方会议页摘要陈述所有 additive chores 有 2-EFX，并以 Mahara 的 EF1+PO 存在性为起点。旧 4-EFX 目标不再是当前最优前沿；2-EFX 的存在、计算和效率量词仍需分开核验。
4. **Nguyen–Elbassioni–Rothe，Improving the Bounds on Approximating WMMS for Chores，2610.15520v1。** 摘要声称二进制有理输入可多项式取得 4.12424-WMMS，并给严格正共同排序成本族的最优因子趋 \(e\)。证明未独立审完；旧 WMMS [2,12] 区间不能继续作为现状，研究局部类前先检查新上下界族是否落入同一模型。
5. **Liu–Zhang，Revisiting Fair and Efficient Allocations for Bivalued Goods，2604.08345v1。** 摘要/Future Directions 声称修复旧算法不终止并给共同 bivalued 设定 WEFX+fPO；personalized 扩展必须与已有兼容性反例比较。不能从 Future Directions 把无条件 personalized 存在性当开放猜想。
6. **Viswanathan，Improved Hardness Results for Nash Social Welfare, Budgeted Allocation and GAP via UGC，2605.27098v2。** 摘要明确 UGC 假设下 MaxGAP 更强近似困难性；这不是 MinGAP 容量扩张、也不是无条件不可能性。GAP 候选必须先统一 max/min、比值方向、硬容量和资源增强语义。

这些警报改变的是候选排序和查重，不是本仓库对这些母文证明的独立认证。

## SEL-LAMINAR4-KEY-v1：准确候选核

来源身份为 Cookson–Shah 的 A 类问题，不能冒称团队新题。模型是四代理共同 laminar 独立集约束、非负实值可加估值；两种 key ground set 分别按 \((3,3,2)\) 或 \((3,3,3,3)\) 分组，每组每人至多一件，每人总件数至多2或3，全部物品必须分完。

量词是：对每组估值、每个预先指定代理次序，是否总存在合法完整分配，同时 EF1，且次序靠前代理不嫉妒次序靠后代理？每种 key 单独回答。目标是完整存在证明/算法，或精确反例；单个 key 失败不否定普通 EF1 存在。

依赖包括原文 key 定义、可行性保持约化、有序无嫉妒拼接接口。首个判别动作是针对真实 EF1 与 ordered 量词构造全估值的有限线性/逻辑证书，或找到有理反例；随机整数估值不够。最大障碍是估值连续无界，且原文已指出三代理 top-k 分离充分条件在四代理失败，不能重复证明它总能满足。报告称本轮已有有限探针，但没有一般新证明。

## 与既有候选对象的关系

[多线候选池实际比较与去重边界](../../../fair-allocation/state/审查/多线候选池实际比较与去重边界--审查.md)保存 59 条候选、图公平参数主线、资源LP分类、Nash克隆和已知 Leontief/Fisher 覆盖；本对象补充六条 2026 文献覆盖警报和 laminar4 精确核，不把摘要级覆盖写成完成证明。

[公平参数化选题战报与实质试攻边界](../../../fair-allocation/state/审查/公平参数化选题战报与实质试攻边界--审查.md)处理 FP01--FP06 的算法草稿与P1--P5 Source Audit；本源处理新母文覆盖变化与 Cookson–Shah key 核，二者的候选量词分开。

[同行选题比较与候选优先级边界](../../../customer-attraction/state/资料/同行选题比较与候选优先级边界--资料.md)和[退役选题核验与有限复现合同](../../../customer-attraction/state/资料/退役选题核验与有限复现合同--资料.md)保存同行排序与有限脚本核验；它们不能替代本源的母文阅读，也不跨模型合并候选。

## 处置和边界

本源处置为 integrated 资料资源，保留文献版本、摘要级覆盖警报、未独立审查标记、四代理 laminar key 核和下一判别动作。它不创建 EFX/EF1/WMMS/GAP 定理，不认证新颖性，不把 2026 预印本当外部证明，也不将 fair allocation 候选迁入 customer-attraction 或 weighted-congestion。后续若推进 SEL-LAMINAR4-KEY-v1，必须全文核母文、构造连续估值证书，并明确两个 key 域、EF1、ordered 无嫉妒和全部物品分完的量词。
