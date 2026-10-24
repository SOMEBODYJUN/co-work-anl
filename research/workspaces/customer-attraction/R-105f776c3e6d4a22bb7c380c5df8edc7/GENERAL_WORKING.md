# 一般半覆盖的本轮直接工作稿

2026-10-24；存档 customer-attraction，程序身份 R-105f776c3e6d4a22bb7c380c5df8edc7。
严格采用 [CAG-MODEL](../../../current/customer_attraction/model.md)：任意有限单位客户、
任意非空共同目录、任意 m、全部有序历史上的任意纯 SPE。主目标
`Q-CAG-HALF: 2W>=OPT_m` **仍 OPEN**。

## 本轮父方直接推导

固定实际并集 C、最优比较并集 O，记
I=O∩C、H=O\C、G=C\O。因此

    W=|I|+|G|, OPT=|I|+|H|,
    OPT-W=|H|-|G|, 2W-OPT=|I|+2|G|-|H|.

所有一般收费必须保留 G；只支付 H 的更强桥已有真实反例，不能把它作为
新归纳前提。已知71客户两人完整 SPE 有 W35、OPT38、|H|36、|I|2、|G|33，
见 [原记录](../R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md)。
本轮没有重新生产该反例。

父方试图把共享遗漏解释为对 C 外客户的顺序入场，并用实际 C 利润支付全部
可信稀释。这个直觉没有给出合法归纳：将真实强制分支移回实际前缀时，
旧玩家返还、整个后继的重选及互斥叶容量必须同时保留。只用 fixed-leaf
返还池会把多条不同强制叶重复支出。本轮改为精确核算删除背景后的
原完整策略失真，得到 [目录敏感 regret 包络](parent/deletion_regret_envelope.md)：

    sum_j R_j <= sum_j K_j-E_d(q).

这是对任意原背景和任意删除背景的全输入组件；作者证明与盲独立重构完成。
它没有证明 sum K_j 可由原同一实际利润支付，因此不是新福利界。

继续直接推导，父方将各实际删位 i 的所有 j>i 误差放入同一预算，
得到 [平均后缀删除界](parent/average_suffix_deletion.md)：

    sum_(i<j)R_ij + D/2 <= sum_(i<j)min{u_j,K_ij},
    sum_(i<j)R_ij <= [(m−1)W−D]/2.

D为实际负载至少2的客户数，K_ij使用真实 b_j，唯一正文固定完整定义。
独立研究员先只见合同重构，再比较旧回放公式，确认此全输入关系及精确D/2退款。
较早实际节点可用旧式保留成(VR)，但各离轨分支的退款仍会重置；没有得到
小损失精确SPE修复或稳健half归纳。这个缺口不能用“误差平均小”消除。

## 另一项必须纠正的承重接口

global_payment 研究员发现、父方独立确认：旧 route5a §4 从
`W >= (OPT-W)/2` 推 `2W>=OPT` 是算术错误，实际只得 `3W>=OPT`。
保留 L1–L4；半遗漏门槛不能据此充当 half 接口。正确充分条件可写为

    B = max_pi sum_i |T_pi(i)\C|/(m-i+1) >= OPT-W,

因为原 L2* 给 W>=B；更强 B>=|H| 也充分。这里不声称正确门槛在一般输入
恒成立。详见 [精确纠错](global_payment/route5a_arithmetic_correction.md)。

## 实际并行义务与去重

- dynamic_exchange：真实交换/owner 信用；正在攻击同行 seq242 的静态最优匹配加强桥。
- terminal_query：旧 FTA/AP-extra 以及真正单步 hybrid 的全树付款；PAIR 已有反例。
- harmonic_menu：中间背景漂移及插入/删除稳定性；不把 PEEL/H4 恒等式当付款。
- credible_attack：共享遗漏的完整可信坏构造及根可达补偿；末位收益 cap 已被
  一个完整二主题 SPE 否定，作为本轮已丢弃直觉，不另生产特殊正面结论。
- global_payment：一般共同容量/真实 IC；同时完成上述算术纠错。
- independent_general：独立重构一般机制；其负载表达式是旧 full-terminal-tax
  候选的独立重遇，已查重并停止同策略锥扩样，转为盲审本轮一般组件。

重新检索到 Brethouwer 2018 primary thesis 不构成新文献发现；当前
[文献边界](../../../current/customer_attraction/literature.md)已区分 singleton
shared-misery、异构目录和一般共同主题模型。本轮没有导入该定理或宣称没有后续文献。

## 当前真正停止线

尚无一般证明、主目标反例或新 half 已证范围。每一条候选仍须由真实后继最优性
给跨枝共同付款，不能把静态后继、低人数阴性、代数等价或多人赞同替代该步骤。
六分支本轮已完成，父方的继续聚合推导也已到此停止；阶段备份只保存可接续推导，不将保存本身报告成数学突破。

本轮静态排列精确反例见 [唯一正文](dynamic_exchange/static_optimal_assignment_counterexample.md)。
原始1953客户及完整策略已由三路重放，并成功发给seq242候选提出者；只排除辅助桥。
root可达性lemma及原PB参数的父方复核亦已完成，见 [解析复核](parent/root_reachability_review.md)。
