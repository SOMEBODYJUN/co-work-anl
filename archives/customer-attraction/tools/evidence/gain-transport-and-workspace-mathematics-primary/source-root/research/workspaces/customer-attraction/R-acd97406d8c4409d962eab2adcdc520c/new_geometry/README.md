# new_geometry：截断主题交集矩的精确表示

Boss6 研究员 6.4 的个人恢复备份，2026-10-21。Q-CAG-HALF 仍 OPEN；本目录不改变共享 Claim、审查或数学地图。

- `intersection_moments.md`：重构的自足证明。对 m 人、p 标签，d=min(m,p) 阶非空交集矩与完整终局收益表线性等价，因此保存全部有序历史上的 SPE 激励与全部 SPE；统一截断阶 d 和线性维数 Σ_{j≤d}binom(p,j) 都有精确最小性。区别单个实例/单条激励行、p=1、重复主题选择、重复覆盖标签、空客户等边界。
- 同一正文给出截断矩的精确可实现锥、布尔多项式正性对偶、原 full-tree half 证书的无损改写，以及按矩维数的客户类型稀疏化。它们是表示/接口，尚未产生一般 half 的非负乘子。
- `audit_intersection_moments.py`：只用标准库 Fraction 从客户类型定义独立核验收益公式、反演、所有有序历史行、奇偶 trade 最小性、缺失的矩正性约束与有理稀疏化。
- `intersection_moments_audit.json`：脚本冻结输出；运行范围和检查数明确记录，计算不承担一般证明。

复现：在仓库根目录运行

```sh
python3 research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_geometry/audit_intersection_moments.py --output research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_geometry/intersection_moments_audit.json
```

与旧 `strategy_geometry/` 及 Boss7 `full_tree_dual/` 的关系：收益图所有顶点和真实激励行均落在本页的低阶布尔多项式空间，故图/SCC/商锥可完全在该空间中运算。SCC 只给显式线性空间，矩正性保留所有客户类型信息；两者合并仍缺一般 half 的统一支付构造。

下一步：寻找利用特殊分母系数与所有真实分支结构的非负布尔余项构造；不把任意形式比较图或局部交集单调性当作充分条件。
