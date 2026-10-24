# exchange9：一般最优指派与早期真实交换

2026-10-24。任意人数、任意有限共同目录、每份完整历史纯 SPE；一般 Q-CAG-HALF 和弱最优冻结指派均 OPEN。

| 文件 | 中文用途、身份及连接 |
| --- | --- |
| [harmonic_terminal_wallet.md](harmonic_terminal_wallet.md) | 全输入跨实际前缀复制付款组件：(2H_m+1)C'<=W，含完整逐客户证明和精确退款；直接代 m=5，C'<=30W/167<W/5。仅支付末对，不闭合三个早期项或一般目标。 |
| [audit_harmonic_terminal_wallet.py](audit_harmonic_terminal_wallet.py) | 只读取上一轮两份已有完整策略，重核全部 IC，再检查 COPY、CLIENT、同一 W 及 REFUND；不生成新实例或扫描固定人数。 |
| [harmonic_terminal_wallet_exact_audit.json](harmonic_terminal_wallet_exact_audit.json) | 1554+258 条有理 IC 及新公式实现审计的冻结结果；有限证据不承担普遍性。 |
| [attack_weak_assignment_existing_cones.py](attack_weak_assignment_existing_cones.py) 与 [输出](weak_assignment_existing_cones_floating.json) | 仅在两份已有强指派反例的完整策略锥中，一次定向攻击一般 WEAK-Q；保留全部真实 IC、最优多重集唯一性及全部排列。浮点均报 infeasible，无精确对偶、无一般或该锥精确定理，不继续固定人数扩样。 |
| [menu9独立数学检查](../menu/terminal_wallet_independent_review.md) | menu9 先根据口头定义盲重构完整证明，后读作者稿核 REFUND；全部通过，非外审和新颖性认证。 |
| [peer_component_reviews.md](peer_component_reviews.md) | 独立审查 global9 最优交换曲线概率/积分，以及 credible9 COV-REFUND/ROOT 和旧 UNIVERSAL-S 的背景域后果；通过，未重跑旧证书。 |

已继续检查最优指派共同 base/H 分解、最优组合替换和早期源退款；尚无将实际 off-history 响应升级合法变成最优组合负交换环的新关系。fresh 客户只给共同列 base，不能由其捕获税自动推出指派环改进。后续应继续真正的早期交换或直接一般证明，不能把调和尾钱包常数作为新的专项。
