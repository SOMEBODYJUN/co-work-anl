# 第二源 λ∈[9,16] 完整局部族

Boss1，`six-boss1-20261111`。本包独立于当前3056计划；**0优化器，0全局LP输入或点读取**。

从真实源IC、大小帽、末节点BR与内部SAFE重建成本后，确认两种 $q_0\in\{1/6,1/5\}$ 的候选域均完整：每域 **11个不可约面、23个顶点**，分别位于 $\lambda=9$ 的8角、$\lambda=15$ 的7个非零角、$\lambda=16$ 的8角。没有遗漏多缺中间会员面。

本段 $t=1$ 的准确锚是尾1110。其源收益分母为 $p+4=D-1$，末query及全部内query分母则仍是 $p+5=D$。因而

\[
m_1(p,q)=\sum_j\beta_j+\frac\lambda{p+4}
+\frac{1+\sum_j\tau_j}{p+5}\,q.
\]

Ordered 同六菜单、内排当前索引的条件均值准确为 $(d-t)/5$。整个连续域上 $W-Z\ge2+19\sum\tau/20>0$，所以正重数 $d=1$ 唯一最弱。

完整输出保留 **230条raw、每条513列**，不作任何筛选：

| 行族 | raw行数 | 独立K系数 |
|---|---:|---|
| 六均值八合法纯目标 $A_1,\ldots,A_6,X,C$ | 184 | $S=1+\sum\beta_j$ |
| 六均值 C-only | 23 | 1 |
| 同六菜单 ordered | 23 | $S$ |

C-only 形式为

\[
a u_2+K\ge\lambda\sum_x\frac{c_x}{p_x+4}+M(C,O)+\sum_j\tau_jN_j(C,O),
\]

其与通用 $T=C$ 行的自由等式关系逐列准确满足

\[
R_{\rm general,C}=R_{\rm C\text{-}only}-(S-1)(|C|-K).
\]

生成器与不导入生成器的独立字面检查器全部PASS：11776个真实隐藏尾成本、736张物理条件最小值表、1231个弱平局达到态出现、117990个完整列及11799个C等式列身份。几何另经全部四面交点、独立真边裁切、三角角递推三种方法互证。五个准确来源SHA首末均一致。

正文与工件：

- [完整证明](source2_lambda_strip/proof.md)
- [完整几何](source2_lambda_strip/geometry.md)
- [全部端点](source2_lambda_strip/endpoint_table.md)
- [精确230行](source2_lambda_strip/exact_family.json)
- [坐标合同](source2_lambda_strip/coordinate_contract.json)
- [独立检查结果](source2_lambda_strip/literal_checker_output.json)
- [冻结清单](source2_lambda_strip/freeze_manifest.json)

结论只覆盖指定局部预算与参数族。$\lambda\ge9$ 是本段窗口，不是由隐藏状态推出的全局下界。本包不产生新全局最优值、完整SPE实现或六人half声明；冻结后停止写入。
