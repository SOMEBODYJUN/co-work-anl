# Boss6.3：弱 iid 桥的有限全历史反例

当前主目标 Q-CAG-HALF 仍 OPEN。本目录仅研究谐和凹势最优 iid 值的辅助桥。

- [weak_iid_star_counterexample.md](weak_iid_star_counterexample.md)：三十人、102 主题、160 单位客户的自足有限反例；证明完整策略在全部有序历史上是纯 SPE，精确认证真正凹势最大者的共同收益 lambda 满足 W < (m-1/2)lambda。作者解析检查完成，已送 6.2 独立审查，审查结果尚未写入本目录；外审及新颖性未认证。
- [verify_weak_iid_star.py](verify_weak_iid_star.py)：Fraction 独立重算有限端点、严格不等式及一般历史分类的收益；有限实现检查不替代正文的全历史分类证明。
- [weak_iid_star_exact.json](weak_iid_star_exact.json)：上述脚本的冻结输出。

lambda = Z_m/m；Z_m 来自谐和凹势全局最大 iid 分布，不是任意 iid 分布、真正安全值 v_m 或最大 iid 覆盖。

下一步：独立审核后整理此辅助桥边界，并回到一般目标的真实跨分支覆盖支付；本例的 OPT=89、W=60，不反驳半覆盖。
