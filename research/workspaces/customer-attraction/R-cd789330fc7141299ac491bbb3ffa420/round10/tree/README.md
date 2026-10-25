# tree10：全树退款与独立核查

一般 Q-CAG-HALF 仍 OPEN。本轮独立检查 [exchange_terminal_refinement_review.md](exchange_terminal_refinement_review.md)：exchange10 的 all-m 静态余量确实完整吸收末对 C'，但 EARLY 未付，没有 HALF 结论。

随后按 root 指令独立读取一个原始完整证书，确认 StrongA 的全称候选被严格反驳；全部有序历史 IC 精确通过，原 HALF 未反驳，弱最优指派未测试。见 [strong_adjacent_raw_review.md](strong_adjacent_raw_review.md)、[独立脚本](audit_strong_adjacent_raw_packet.py)及[精确输出](strong_adjacent_raw_independent_audit.json)。

[direct_static_floor_review.md](direct_static_floor_review.md)核对 direct10 的静态 star minimax 值；该辅助候选不要求 q 为 SPE，不能扩大为实际策略或 HALF 否定。

[compact_strongA_review.md](compact_strongA_review.md)另从 exchange10 的十单位客户陈述独立重构更小的同候选反例；全21历史/63 IC通过，W9、OPT10、冻结 regret总和2、相邻税1。附[独立脚本](audit_compact_strongA.py)与[精确输出](compact_strongA_independent.json)。

[existential_adjacent_family_review.md](existential_adjacent_family_review.md)独立全历史重构 root 的一般反例族：全部 k>=1 政策确为完整 SPE，最优多重集唯一，全最优指派穷尽后 `min Q-W=(k-3)/2` 而相邻税恒1。k>=6 严格否定存在性相邻税桥，任意固定倍数亦不能修复；HALF及原较宽弱冻结预算未被否定。

全树直接尝试另记 [whole_tree_all_refund_working.md](whole_tree_all_refund_working.md)：使用全部活跃利润检查归纳，保留全部旧玩家退款；未取得跨真实叶共同支付。没有固定人数或特殊目录项目、没有无反例扫描。
