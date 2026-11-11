# 全可见联合层 v3：1050原行的来源审查与路由

Boss1；RUN `six-boss1-20261111`。本包状态为 **PREPARED_NO_OPTIMIZER**，只准备精确输入、来源和独立字面检查，不运行优化器。最终合同为1003旧原行＋16源2重配端点＋31跨源纯T行＝**1050 raw / 513非负列 / 2等式**。

## 1. 原模型与冻结基线

原模型仍为有限单位客户、有限非空共同标签目录、恰六人完整有序历史纯SPE；保留空覆盖、同覆盖异标签、重复行动与全部弱平局。actual动作A1,…,A6、同一actual前四负载下的全目录潜力最大合法X、全目录最大裸大小合法C及K，均沿用既有含义。O是OPT6六合法可重复查询的覆盖并，不是行动。

基线实际路径是 `visible_maximum_joint_v2/exact_input.json`，SHA `0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4`。其全部1003 raw行字典按原序深复制，包括名称、族、所有metadata、每个系数字符串、显式零系数和rhs；不对旧行重建、缩放、去重或清零。全部恒零、重复及冗余合法行继续保留。

512客户型的位序、所有atom记录、K512、非负列、目标W及两等式完全相同。两等式为O=1和Σcz−K=0。完整基线非行metadata另外逐字典归档到本输入的baseline_metadata，当前v3自身的scope/count/provenance明确单列，避免混淆历史与新准备状态。

旧数值尺度文件SHA `db5f70c7e531fc9feafc66806523713d917838f614eb35a7a5b096fa2b88293e`，全部1003个raw尺度字符串及次序原样继承；特别是已有NS5整数行继续使用其300除数。

## 2. 同一第二源最大C分支的16重配端点

完整亲读 `source2_joint_internal_safe/proof.md`，SHA `e4ba6dd0e4cde35a9c899d35e85c53a98a042b257e6bb14a01078726138210e4`。所用端点文件是顶层16行列表 `sixteen_reweighted_vertex_family.json`，SHA `a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e`。

在actual第二源历史(A1)强制真实最大C，保留同一策略的真实R3,…,R6；内部三个SAFE都使用各自真实前缀和自身真实偏离后继。令Θ=θ3+θ4+θ5，α=25+Θ−s，三权域为

\[
\theta\ge0,\quad\theta_5\le5/12,\quad
\theta_4+\theta_5/36\le5/12,\quad
\theta_3+\theta_4/72+\theta_5/36\le5/12,
\quad 0\le s\le9.
\]

该域有八个三权顶点，分别配s=0和9，共16端点，α≥16。真实预算权为源IC α、三个中间大小帽各1/2、末帽1、同末BR均值1，以及三个内部SAFE均值θ3、θ4、θ5。没有给被强制C新的第二源最优性。

每客户p=a1、c=C会员，准确投影成本为

\[
m=\frac52c+\frac{24c}{p+5}
+\frac{o}{6(p+4c+1)}-\frac{sc}{5}
+\sum_{j=3}^5\frac{\theta_jo}{6[p+(j-2)c+7-j]}.
\]

将C质量自由等式乘以5/2−s/5后相加，得到源文件所保存的原行

\[
\alpha u_2+\frac{s}{5}K
-\sum_x\left[
\frac{24c}{p+5}+\frac{o}{6(p+4c+1)}
+\sum_{j=3}^5\frac{\theta_jo}{6[p+(j-2)c+7-j]}
\right]\ge0.
\]

新raw index1003–1018按16行源列表原顺序逐字复制。虽然源IC系数α随端点变化，**数值除数一律继承源文件的25**，不改成α。所有端点均保留，包括可能已由旧行与等式推出的端点，不做未经授权的删减。

本包字面checker从真实份额重算16×128＝2048隐藏态、128个最低值，逐六真实查询索引核65536个菜单/尾态，并重建16×513全部系数。O在该来源中允许任意六合法查询并；放入全局输入时才沿用O=OPT6及原归一化。

## 3. 跨actual源的31条纯T行

完整来源为 `all_source_nested_safe_family/proof.md`，SHA `80a6ce05d8fc236298ff2e6b9fe0cc47073b5cbd7afbb155b560cce1ec95e212`；完整36族SHA `340267bbe7148107a685eb260ffc24029de1a93f77f4a4fd3f201cc109e5aa8b`。

actual源i=1,…,4，n=6−i、p为此前actual负载、D=p+n+1、ci=(n+1)/2。任意合法T的原行是

\[
25u_i+c_iK-\sum_x\left\{
c_it+\frac{24t}{D}+\frac{o}{6(p+1+nt)}
+\frac5{12}\left[
\frac{o}{6(p+(5-i)t+2)}-\frac{t}{\min(D,5)}
\right]\right\}\ge0.
\]

它支付该actual源的IC及其强制T后的同分支内部第五源SAFE。p+n=5时末位不覆盖的旧弱平局给真正较低成本，必须用min(D,5)；全部416完整隐藏态、40最低值已由原证明和本checker分别核验。

从原36列表保持顺序，仅选T=A1,…,A6,X,C的32纯角色行，再排除i2C，留下31条，原样追加于raw index1019–1049。全部行系数、metadata、原25ui尺度与数值除数25均不变。本族中的X仅作为合法标签，C的额外潜力最大性未被使用。

## 4. 明确排除的五个来源候选及全列证据

排除的是原36族中的候选，不是从旧1003原行删除任何东西。

| 排除候选 | 准确理由 |
|---|---|
| NESTED_SAFE5_i2_TC | 已有NS5＝12R_2(C)＋29(Σcz−K)，在当前C等式上等价 |
| NESTED_SAFE5_i1_TouterOmean | 被既有PORTFOLIO25_i1_T8_Q8逐客户支配 |
| NESTED_SAFE5_i2_TouterOmean | 被既有PORTFOLIO25_i2_T8_Q8逐客户支配 |
| NESTED_SAFE5_i3_TouterOmean | 被既有PORTFOLIO25_i3_T8_Q8逐客户支配 |
| NESTED_SAFE5_i4_TouterOmean | 被既有PORTFOLIO25_i4_T8_Q8逐客户支配 |

四个外均值的差为Σoδ_i(p)，全部十个δ严格正；它们比较的是旧30异索引双均值，不是36对或假设独立的菜单。`excluded_rows.json`存每条排除对象、原族索引、原行和全513列证据；独立checker对全部5×513列重新核验。C2排除仅避免这次追加等价来源，已有1003中的NS5和全部原行均留存。

## 5. 只读诊断及准备边界

可选的旧点诊断只读取冻结1003证书 `visible_maximum_joint_v2_solve/exact_certificate.json`，SHA `b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea`。先核旧点非负性、1003原行和两等式，再分别计算47追加行值。诊断独立保存，不向新输入增加点等式、不固定K、不缩支撑，也不将旧点作为新1050系统的可行点。

新输入仍是全512型必要投影，没有SPE存在性、half或新最优值声明。全部构建、检查只使用标准库Fraction；不执行任何旧builder、solver或审计脚本，不包含新求解入口。Main完成此输入复核后才可能另行授权一次数值发现；本包不会自动释放。

## 6. 冻结产物

`exact_input.json`保存全部1050原行及不变的513列/两等式。`row_catalog.json`、`column_routing.json`与相应TSV明确来源和坐标；旧行目录及列路由原样继承。`numerical_scaling.json`保留全部1003旧尺度并追加47个25。`source_pins.json`合并三份冻结包、它们的来源及旧冻结追溯SHA，并在生成后重新核对。

独立字面checker不导入本builder，从真实份额重建47新行，核旧1003的字面保留、全部尺度、坐标和五条排除证据。最终以manifest和SHA256SUMS冻结，状态仍为PREPARED_NO_OPTIMIZER。
