# 第二源统一1110锚的完整局部族

Boss1，研究标识 six-boss1-20261111。**0优化器、0全局LP输入或候选点读取**；本包不加入当前3056计划。原230条窗口包已独立冻结并保持不变。

Main提出撤去人为λ下界后，本包从真实成本重新核得：两种 $q_0\in\{1/6,1/5\}$ 的完整域都为 **10个不可约面、16个顶点**。所有约束是

\[
\tau_j\ge0,\qquad\lambda\le16,\qquad
\frac34\tau_j+\operatorname{cross}_j
\le\frac{\lambda}{20}-\frac{q_0}{2},
\qquad
\frac34\tau_j+\operatorname{cross}_j
\le\frac34-\frac{q_0}{2}.
\]

A帽自动推出 $\lambda\ge10q_0$，底层唯一点为 $\tau=0$。六均值底点λ为 $5/3$，ordered底点λ为2；再各加λ为15的7个非零角和λ为16的8角。原窗口域准确等于本完整域与λ≥9的交。

统一锚为真实尾1110；源收益分母是 $p+4=D-1$，末query和全部内query分母仍是 $p+5=D$，故

\[
m_1(p,q)=\sum_j\beta_j+\frac{\lambda}{p+4}
+\frac{1+\sum_j\tau_j}{p+5}q.
\]

Ordered沿同一六菜单、内排当前索引，条件均值准确为 $(d-t)/5$。整个连续域上

\[
W-Z\ge\frac35+\frac{19}{20}\sum_j\tau_j>0,
\]

所以正重数 $d=1$ 唯一最弱；底点两个p同时取得准确差 $3/5$。

全部 **160条raw、每条513列** 完整保留：

| 行族 | raw行数 | 独立K系数 |
|---|---:|---|
| 六均值八合法纯目标 $A_1,\ldots,A_6,X,C$ | 128 | $S=1+\sum\beta_j$ |
| 六均值C-only | 16 | 1 |
| 同六菜单ordered | 16 | $S$ |

C-only与通用C行逐列满足

\[
R_{\rm general,C}=R_{\rm C\text{-}only}-(S-1)(|C|-K).
\]

独立字面checker不导入生成器。82080个完整列、8208个自由C等式列、8192个真实尾态、512张物理条件最小值表及全部900个弱平局达到态出现均准确核过。几何另由所有四面交点、真边裁切和三角递推互证。12个明确来源SHA首末保持一致。

正文与工件：

- [完整证明](source2_lambda_anchor_complete/proof.md)
- [完整几何](source2_lambda_anchor_complete/geometry.md)
- [全部端点](source2_lambda_anchor_complete/endpoint_table.md)
- [精确160行](source2_lambda_anchor_complete/exact_family.json)
- [独立检查结果](source2_lambda_anchor_complete/literal_checker_output.json)
- [冻结清单](source2_lambda_anchor_complete/freeze_manifest.json)

本结论只覆盖指定真实预算、坐标最小帽和统一1110锚，不声称任意钱包最优性、完整SPE实现、新全局最优值或六人half结论。冻结后停止写入本目录及同名索引。
