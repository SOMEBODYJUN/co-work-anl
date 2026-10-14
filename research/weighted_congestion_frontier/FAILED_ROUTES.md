# 失败机制与回收

## 2026-10-14：simultaneous forcing 的次数边界

尝试：在每个 odd-ring 节点强制 matching light 改善，然后由 parity 迫某 hub 改善；继续调整整数 cohort 数、权比、费用次数和正系数，争取 Θ(d) 下界。

失败步骤：OC-INTERFACE-BARRIER-v1 由 N_i,Q_i>0 和 weight closure 推出 ∏n_i<(α^(1/d)−1)^(−2m)，每个系数传输因子又小于 n_i/(α−1)²；可行 product>1 必须有 (α−1)(α^(1/d)−1)<1。因此该证书不能超过 d/ln d 的 leading order。这是机制限制，非命题 a_*(d)=Θ(d/ln d) 的证明。

独立回收：OC-LIGHT-FORCING-EXACT-v1 证明所有 light 条件成立但某 hub 条件失败时，可令该边唯一同色、其余交替、全部 cohort 反位，得到真实 α-PNE，包括等号端点。偶数环全交替也给 PNE。实际边界 witnesses 与全部偏离保存在 assets/R1/odd_ring_audit/verify_state_review.py 和 state_verification.json。

未排除其他 topology、不要求所有 matching light 在每个配置改善的新 state-covering 机制，以及全类 O(d/ln d) 存在性。只有绕开 light-forcing 或换机制后值得重试更大阶下界。

完整证明与 scope：../current/weighted_congestion_frontier.md；原 asset：assets/R1/odd_cycle/INTERFACE_BARRIER.md；独立审查：assets/R1/odd_ring_audit/state_review.md。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。
