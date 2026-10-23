# Boss6第二独立研究支线

2026-10-22。原Q-CAG-HALF仍OPEN；根目录与工作区共享文件由root统一维护和提交。

- [外部主题等号边界](weak_outsider_boundary.md)：把small-outside guard中的
  outside大小`<λ`改为`≤λ`时，逐人λ保底及W≥mλ已被十一客户完整二人SPE反驳。
  含完整二人参数族及每个m≥2的解析族；这些均不是half反例，弱边界half仍未判定。
- [定义级核验](audit_weak_outsider_boundary.py)与[精确输出](audit_weak_outsider_boundary.json)：
  不导入规范求解器，展开单位客户检查全部有序节点、真实偏离、OPT和数值范围。
- [多源核单步障碍独审](multisource_pivot_obstruction_review.md)：从定义盲重构，
  m个不交二客户主题的最优来源中，任意clone节点唯一末回复均为横跨主题R，
  替换任一源后核严格减少1/m；不能宣称总有非降pivot。预算版和half仍开放。

研究中止的候选：`Σ_(x∈O)1/(c_x+1)≤W`已由Boss5的最优遗漏反例否定，
无需再扫；来源为`R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md`。
后续一般桥应保留比较并集外旧客户的负信用，继续处理跨真实分支的净覆盖。
