# 跨枝金额预算与共同容量

当前只研究 Q-CAG-HALF 的任意人数、有限共同目录、单位客户与全部有序历史纯 SPE。原目标仍 OPEN。

- [跨枝 AMOUNT-CAP1 的全历史反族](amount_cap1_family.md)：对每个 n≥3 构造完整 SPE，证明各 sender 的总输入金额由其同一 parent 利润支付，仍可使一个 parent recipient 的系数达到 (2n−1)/(n+1)，趋于二。父方、[credible](../credible/review_amount_cap1_family.md) 与 [independent](../independent/amount_cap1_family_review.md)分别解析重构通过，无外审或新颖性认证。该实例自身 OPT=W，不是 HALF 反例。
- [定义级有理审计](audit_amount_cap1_family.py) 与 [n=3 复现](amount_cap1_family_n3.json)：不导入规范 solver，按定义核验全部历史及归一请求；一般 n 的证明由正文承担。父方和 independent 的同实现重放不是独立实现。
- [深层耦合交接](deep_amount_handoff.md)：固定策略的闭式最坏请求、AMOUNT 已有总金额守恒、尚未付的覆盖初始化与整树共同库存；DEEP-cap2 无证明或反例，不扩样。

已核对父目录的[末层金额 cap2](../parent/terminal_amount_cap.md)全范围证明和零利润处理，该系数由上述全 n 族证明不能统一减小。下一步是同页 DEEP-AMOUNT-CAP2：多尾真实子 SPE 是否仍给系数二。末层的二由每个 prefix 利润最多缩小二分之一得到；不能无证推广到更深分枝。
