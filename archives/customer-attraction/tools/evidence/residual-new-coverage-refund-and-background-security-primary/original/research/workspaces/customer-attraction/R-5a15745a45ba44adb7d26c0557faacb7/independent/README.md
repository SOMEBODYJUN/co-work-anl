# 独立一般重构与盲审接续

2026-10-24，actor R-5a15745a45ba44adb7d26c0557faacb7 内部分支。
只研究 CAG-MODEL 的任意人数、任意有限共同目录、全部历史纯 SPE。
Q-CAG-HALF 仍 OPEN。此目录不改变共享命题的成熟度。

- `prefix_and_terminal_amount_review.md`：先凭精确陈述重构父稿的最小坏剩余人数归约，
  再独立证明末层 AMOUNT-cap2。包含原 m、合法旧背景、同 cut 多孩子和零利润边界。
- `amount_cap1_family_review.md`：先从精确实例独立重构全 n、全部历史的 SPE 补全，
  再对照 coupling 正文；确认末层 cap1 反例及常数二的锐性。实际 W=OPT。
- `background_security_candidate.py`：仅攻击精确的一般加强候选：任意合法背景 b、
  r 位剩余人的任意子 SPE 总利润至少 r v_r(b)。有限随机检验未反驳，
  **不支持该候选的一般真值**；按父方指令不再扩样。
- cap1 的 n=3 检查只重放了 [coupling 原脚本](../coupling/audit_amount_cap1_family.py)，
  相同结果见 [coupling 原输出](../coupling/amount_cap1_family_n3.json)。
  不称独立实现；本目录不保留重复程序或 JSON。

下一步：深层 AMOUNT-cap2 的结构攻击。若有 r 位尾部可变，末层证明中每 j 的
直接质量界 2 会退化为 r+1；真实 IC 是否恢复合计 cap2 尚无证明。
本目录只存可接续推导和真实停点。
