# 同六菜单连续付款：181 行完整有限化

状态：**PREPARED_NO_OPTIMIZER**。本包将已证的同六菜单连续参数族按最大损失项的活跃区域完整细分，得到 **14 个 cell、181 个合并顶点、181×513 个准确行系数**。原 67 个顶点全部包含，新增 114 个交界顶点。两种独立几何算法及逐真实分支的完整检查均通过，优化器调用为 **0**。

完整家族：all_source_ordered_menu_cells/exact_family.json。

SHA256：**f1bca409d9927f9721764a327f1fcd52a18c38f0968d9c240fa20288aa95eac3**。

本包没有修改 1586 输入，没有读取新 LP 点，也没有将新族接入任何求解。half 仍为 **OPEN**。

## 为什么需要细分参数域

源定理使用实际源 i 的真实 IC、同一外层强制分支的大小帽、末回复 BR 和内部 SAFE。外层对六个合法菜单索引 k 平均，内层对同一列表的五个索引 l≠k 平均，允许重复标签、空覆盖、同覆盖别名、任意重叠及弱平局。

定义

\[
\ell_j(\theta)=\theta_j+\sum_{h>j}\frac{\theta_h}{5(7-h)(8-h)}-\frac25,
\qquad L_i(\theta)=\max(0,\ell_{i+1},\ldots,\ell_5).
\]

完整连续行是

\[
R_i(\theta,s)=a u_i+c_iK-\sum_xo_xG_i(p_x;\theta,s)\ge0,
\]

其中 \(a=25+\sum_j\theta_j-s\)、\(c_i=(7-i)/2\)，且

\[
G_i(p;\theta,s)=
\frac16\left[c_i+\frac{24}{p+7-i}+\frac1{p+1}
-\frac{s}{\min(p+7-i,5)}
+\sum_{j=i+1}^{5}\frac{\theta_j}{p+7-j}\right]
-\mathbf1_{p=0}\frac56L_i(\theta).
\]

最大值使行关于参数成为凸的分片仿射函数。旧 67 个参数顶点只提供合法样本，不能直接用旧域的凸插值代表整个连续族。

本包构造 cell0：所有 ell_j≤0；以及每个 cellj：ell_j≥0 且 ell_j≥ell_k。每个区域内最大值固定为同一个仿射项，所以该区域内的任意参数行准确等于区域顶点行的凸组合。这给出指定连续族的完整有限表示，不声称最小生成集或全部 SPE 预算的最优性。

## 几何结果与完整行目录

| 实际源 | 各 cell 顶点数 | 合并顶点 | 原顶点 | 新顶点 | 全家族 raw 索引 |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | 0:39，2:79，3:56，4:47，5:38 | 119 | 39 | 80 | 0–118 |
| 2 | 0:16，3:24，4:20，5:16 | 40 | 16 | 24 | 119–158 |
| 3 | 0:8，4:10，5:8 | 16 | 8 | 8 | 159–174 |
| 4 | 0:4，5:4 | 6 | 4 | 2 | 175–180 |
| 合计 | 14 个 cell、369 个顶点—cell 关联 | **181** | **67** | **114** | 0–180 |

边界平局完整保留；相同参数点合并后记录全部活跃 cell 出处。根源的 119 行全部保留，未将旧 39 个根样本的支配结论推广至新增 80 点。

derive_geometry.py 完整遍历 32448 组边界组合，用有理消元求交。独立的 check_geometry.py 从旧域顶点出发，用逐半空间的真边裁切复核，得到相同的全部顶点，并确认 14 个 cell 均满维。它没有导入或执行前一枚举器。

准确参数、原67包含关系及裁切记录分别在 parameter_cells.json、original67_inclusion.json、independent_cell_checks.json。完整行和数值尺度目录在 row_catalog.json、row_catalog.tsv、numerical_scaling.json。

## 精确插值及一个可直接检查的例子

old_vertex_interpolations.json 给出全部181点相对旧域顶点的非负有理凸插值，最大权重支持数为16。原67点使用权1；114个新点的所存插值全部满足严格的

\[
\gamma(q)=\sum_v\mu_vL(v)-L(q)>0.
\]

对应完整行身份是

\[
\sum_v\mu_vR_i(v)-R_i(q)
=\frac56\gamma(q)\sum_{x:p_x=0}o_x.
\]

例如源4的两个新点是 \((\theta_5,s)=(2/5,0)\)、\((2/5,9)\)。对这两个 s 值，各自准确有

\[
R_4(2/5,s)=
\frac1{25}R_4(0,s)+\frac{24}{25}R_4(5/12,s)
-\frac1{75}\sum_{x:p_x=0}o_x.
\]

这里 \(\gamma=2/125\)。旧顶点的凸平均确实给出更弱的行；这不排除旧完整系统通过其他预算支付某条新行，故没有宣称114条新行逐条锥独立。

在同一细分 cell 内，上述损失差消失，行对参数仿射。interpolate_cell.py 提供无优化器的准确边界下降算法，把任意给定的有理参数点写成所在 cell 顶点的非负凸组合。14个cell的重心已实际计算全部权重并核验全513列身份。

## 来源与独立真实菜单核验

基础 all_source_ordered_joint_menu 已最终冻结：

| 来源 | SHA256 |
| --- | --- |
| 基础 manifest | eb01d5539bc6b6182871df3e14fa800896e46ba63fa3f52176cb2aee562052fe |
| 连续证明 | b9049f3c6b9faec5360d17acdcff6f2a16d8900674538b200fcd20ec713f3f08 |
| 原67样本 | d405ead895234dcaa9355cbd61056a7f81013f230d214b108578ead068784510 |
| 连续 G 机器接口 | f9ea0d2788925965a999a204c3b9b4ad6eded30a529f962f1f0355eb5be15b85 |

本包亲读该准确证明。Main 另已亲读全部10节并完成独立状态和系数核验，记录 main_ordered_joint_menu/producer_comparison.json 的 SHA 为 787ef20b1e4dc8451b215770d4ff80c471052f5e9b1f839b9d80878bd6637298，随后明确释放本包最终冻结，未释放 LP。

独立 check_family_literal.py 没有导入 builder 或来源程序。它逐个人真实收益、大小帽及内五查询份额重新构造客户成本，保留实际 (d,t) 相关性与所有达到尾态，再重建所有矩阵列。其结果为 **PASS_INDEPENDENT_TRUE_ORDERED_MENU_CELLS**：

| 核验对象 | 准确数量 |
| --- | ---: |
| 真实隐藏状态 | 66816 |
| 物理条件最小值 | 3252 |
| 外层 f 值／G 上下文 | 1897／271 |
| 全64菜单模式 | 17344 |
| 实际外索引检查 | 104064 |
| 字面内五查询份额身份 | 2304 |
| 181行全列重建 | 92853 |
| 原67样本全列包含 | 34371 |
| cell 仿射标量系数 | 34884 |
| 369个顶点—cell全列身份 | 189297 |
| 14个cell重心全列插值 | 7182 |
| 181点旧顶点插值的整行损失身份 | 92853 |

全部残差和最小值条件通过。全512客户型与独立K列均保留，K权仍为 c_i，数值除数统一25。181个系数向量互异；没有据此作线性独立性声明。159件来源工件在生成和检查首尾保持SHA不变，Main来源审查记录另行绑定。

## 工件与边界

数学证明在 proof.md；全列证据在 full_column_checks.tsv 和 cell_incidence_column_checks.tsv；隐藏状态、所有条件最小值、菜单模式、仿射形式及准确插值均有完整JSON工件。最终逐件身份见 freeze_manifest.json 和 SHA256SUMS。

几何阶段工件保留其当时“尚未绑定 ordered 来源”的历史标识；最终来源绑定由 exact_family.json、source_pins.json 和最终 manifest 记载。本次仅写 all_source_ordered_menu_cells/ 及本说明，没有修改旧包、Git、RUN、registry 或凭据，没有新LP点诊断、求解、support筛选、SPE实现或新全局最优值声明。
