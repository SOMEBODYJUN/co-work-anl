# round7/fresh：primary 核查后的概率优先权一般尝试

原 Q-CAG-HALF 仍 OPEN。本目录没有新的无条件福利界或目标反例。

[一般推导稿](priority_whole_row_working.md)先直接核查 Deng 等原论文的全历史 SPE 和双人证明，再研究 winner 表示的跨 context 付款。

- 固定 global priority 的 missed 来源路径确实终止，但这不合并不同整查询，也不使条件 IC 有效。
- ENV / ENV-SOURCE 是旧 NEW-CAP / ONE-WHOLE-IC、query COVER/PAY 与 same-action 聚合的概率支配特例，已实际读源去重；没有新 cap 或新钱。它只澄清单个固定查询能用完整 u_i 支付，即使随机加权 IC 差为负。
- 每角色未曝光彩票保持条件期望 IC，却回到既有递增角色捕获核，未当作新机制。
- 独立客户彩票将 conditioning 债局限到 missed-source 协方差；该债仍未支付。

一般式代 m=5 后仍缺行包络/净信用构造，未推出 half。数学状态、primary 来源与 parent 来源分别记录于正文；无新扫描、外审或新颖性认证。未运行 git、work.py 或编辑本分支以外的文件。

## 新增独立内审

[child 支持与 CUT-LEDGER 审查](child_support_independent_review.md)按原始定义重构并对稿，通过一般背景 SUPPORT/MIX/SLACK、整数 max_d<=c、非空初始背景端点及所有 actual cut 的 B 唯一合账。首次读取已接触作者证明，因此准确身份是**非盲独立内审**。

[Fraction 回归](audit_child_support.py)、[冻结输出](audit_child_support.json)通过972组系数及1275条单客户cut链；并从旧13人packet重走实际路径，静态重算 mM+K-2W=37/66>0，确认该固定付款为FALSE。没有重审旧13层全部SPE，也没有新输入或参数扫描。

此审查确认通用组件正确，未新增真实后继共同付款；一般 half 和最优主题组价格桥仍OPEN。

[priority 诊断独立审查](priority_counterexample_review.md)通过父方两套两人完整 SPE：条件化 Γ 可负、adaptive query 的点态 rowmass1 也不保证一份 u 支付。确定上包络没有被否定；两例 R 都为空，不是固定 missed-source 流的反例。源游戏不新。独立 [脚本](audit_priority_counterexamples.py) 与 [输出](audit_priority_counterexamples.json)核完全部历史、winner 均值、N=0/m=1；审查为非盲，未运行父方会覆写root输出的脚本。
