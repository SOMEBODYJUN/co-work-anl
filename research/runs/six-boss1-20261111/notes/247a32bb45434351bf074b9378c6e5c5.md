# 全可见真实最大标签联合层 v3：1050 行冻结准备

状态：**PREPARED_NO_OPTIMIZER**。所有数值优化调用为 **0**；本包保留为 Main 审定用的完整中间输入，后续数值求解另由 Main 明确释放。原 half 问题仍为 **OPEN**。

## 输入与追加合同

`visible_maximum_joint_v3/exact_input.json` 的 SHA256 为：

`c5ddba49b71303083b07b96f90888d56f11b291d7c307f0c3e8280b7385d280e`

完整输入有 **1050 条 raw 不等式、513 个非负列、2 个等式**。客户型位序仍为 `(a1,a2,a3,a4,a5,a6,x,o,c)`，512 个客户型全部保留，`K` 位于列 512。目标、非负列、两等式及旧坐标路由均直接继承 1003 输入。其中 `C` 是目录最大裸大小的合法标签，满足 `|C|=K`；`O` 是任意六个合法、可重复查询标签的覆盖并，源预算不依赖它必须达到 OPT。

以下 raw 索引从 0 开始。

| raw 索引 | 数量 | 来源及处理 | 正数值除数 |
| --- | ---: | --- | --- |
| 0–1002 | 1003 | `visible_maximum_joint_v2/exact_input.json` 的全部原始行，字典、系数字符串、显式零、顺序及行 metadata 完整继承 | 逐字保留旧值 |
| 1003–1018 | 16 | `source2_joint_internal_safe/sixteen_reweighted_vertex_family.json` 的全部端点，保持来源顺序 | 25 |
| 1019–1049 | 31 | `all_source_nested_safe_family/exact_family.json` 的 32 条纯目标行，排除与旧 NS5 等价的 `i2,C` | 25 |

1003 输入的全部非行 metadata 原样保存在 `baseline_metadata`。新顶层 metadata 只说明本次追加范围。新 47 行保存来源未缩放系数，数值除数独立记录在 `numerical_scaling.json`；16 端点的源 IC 权重可以变化，除数仍依合同为 25。

本次未加入另外 4 条 `outerOmean` 行。完整选择、排除依据及 513 列证据见 `excluded_rows.json`。旧 1003 行以及本次追加行均未去重、未删零；`raw_identity_diagnostics.json` 仅记录现有 1 条零行、69 条重复行及 980 条不同的非零仿射行，不改变输入。

## 两个来源的真实预算与路由

### 源 2、同一真实分支的三个内部 SAFE

16 个端点来自真实强制 `C` 后的同一分支。预算由源 2 IC、后三个中间回复的大小帽、末回复大小帽、末回复对六个合法查询的均值 BR，以及内部第 3、4、5 个源的真实 SAFE 均值组成。内部 SAFE 的查询仍逐一对应六个真实标签；不存在将覆盖并 `O` 当作合法行动的步骤。

参数域为

\[
\theta_5\leq\frac5{12},\qquad
\theta_4+\frac{\theta_5}{36}\leq\frac5{12},\qquad
\theta_3+\frac{\theta_4}{72}+\frac{\theta_5}{36}\leq\frac5{12},\qquad
\theta_j\geq0.
\]

8 个顶点分别配上 \(s\in\{0,9\}\)，得到 16 行。设 \(p=a_1\)，\(\alpha=25+\theta_3+\theta_4+\theta_5-s\)，存储行是

\[
\alpha u_2+\frac{s}{5}K-
\sum_v z_v\left[
\frac{24c}{p+5}+\frac{o}{6(p+4c+1)}+
\sum_{j=3}^{5}\frac{\theta_j o}{6\bigl(p+(j-2)c+7-j\bigr)}
\right]\geq0.
\]

它由原始预算加上自由等式 \((5/2-s/5)(|C|-K)=0\) 得到。权重 \(\alpha\geq16\)，其余预算权重也均非负。原证明全文复核及预算、客户型路由记录在 `source_review.md`；独立检查器从真实负载重新重建最小式及全部系数，不导入来源生成代码。

### 跨实际源的内部第五个源 SAFE

对实际源 \(i=1,2,3,4\)，令 \(n=6-i\)、\(p=\sum_{j<i}a_j\)、\(D=p+n+1\)、\(c_i=(n+1)/2\)。对任意合法纯目标 \(T\) 及其会员位 \(t\)，预算是

\[
25u_i+c_iK-\sum_vz_v\left[
c_it+\frac{24t}{D}+\frac{o}{6(p+1+nt)}+
\frac5{12}\left(
\frac{o}{6\bigl(p+(5-i)t+2\bigr)}-
\frac{t}{\min(D,5)}
\right)\right]\geq0.
\]

其中 `min(D,5)` 保留末回复在相应边界的弱平局，不能统一替换成 `D`。每个源选取 `A1,…,A6,X,C` 共 8 个纯合法标签；实际源 IC 来自实际历史，强制目标不会获得一个新的源 IC。31 条入库行保留原式，适用有限共同目录、空覆盖、别名、重复查询及弱最优回复。

本包只确认这些真实预算及其精确系数。除已明确的点分离和等价关系外，不声称 31 条预算每条都独立于旧行锥。

## 五条排除行及可核验证据

令 \(E_C=|C|-K\)，令 \(R_{2,C}\) 为以上未缩放跨源 `i2,C` 行，旧输入的 NS5 行满足

\[
\mathrm{NS5}=12R_{2,C}+29E_C.
\]

`excluded_rows.json` 保存完整 513 列零残差，故本次不重复追加 `i2,C`。

4 条 `outerOmean` 行逐条被旧输入的 `PORTFOLIO25_i{i}_T8_Q8` 蕴含。新行减旧行等于 \(\sum_v o\,\delta_i(p)z_v\)，其余系数差为零，且下表所有值均为正：

| 源 i | p=0 | p=1 | p=2 | p=3 |
| --- | --- | --- | --- | --- |
| 1 | 1/162 | — | — | — |
| 2 | 7/1440 | 5/2592 | — | — |
| 3 | 11/1728 | 1/1620 | 11/5184 | — |
| 4 | 23/2592 | 11/5184 | 7/8640 | 7/2592 |

这些结论保持旧双均值的 **30 个异索引配对**，没有将同一六标签列表拆成独立分布，也没有假设六标签覆盖形成分割。被排除的仅是本次来源族中的这 5 行，基线原有行全部保留。

## 独立精确预检

`check_literal.py` 独立重建真实份额、隐藏负载和客户型系数；仅使用 Python 标准库及 `Fraction`。它未导入 builder 或来源代码，未调用优化器。本包的“独立”指实现路径独立，未声称另有外部盲审。

`literal_check_result.json` 的结果为 `PASS_INDEPENDENT_LITERAL_PREPARATION_CHECK`，SHA256：

`9dc2b0e2fd3328529857f99e5923e8a96239e86b9422c334c2a7723c3c1de106`

| 检查 | 精确数量或结果 |
| --- | ---: |
| 旧 raw 行字典、顺序及 metadata | 1003 行逐字一致 |
| 旧客户型和 K 系数 | 514539 项一致 |
| 新端点／跨源纯目标行 | 16／31 |
| 新行全列重建 | 24111 项，残差全零 |
| 排除行全列等价或蕴含检查 | 2565 项通过 |
| 端点隐藏状态／最小值域 | 2048／128 |
| 跨源隐藏状态／最小值域 | 416／40 |
| 端点真实六查询会员展开 | 65536 项通过 |
| 跨源真实六查询会员展开 | 13312 项通过 |
| 原数值除数字符串／新增除数 | 1003／47 项一致且为正 |
| 冻结来源文件 | 187 件 SHA 未变 |

完整隐藏状态见 `literal_source_checks.json`，全列 residual 见 `appended_column_checks.tsv`。目标、两等式、列路由以及全部 512 个客户型均通过一致性检查。

## 旧 1003 点的只读诊断

只读证书 `visible_maximum_joint_v2_solve/exact_certificate.json` 的 SHA256 为 `b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea`。对这一个既有有理数点作代入，47 条追加行中有 8 条负值：7 条端点 `V001_S9、V011_S0、V011_S9、V101_S0、V101_S9、V111_S0、V111_S9`，以及跨源 `NESTED_SAFE5_i2_TA4`。

每行的完整有理数 slack 已保存在 `frozen_1003_point_diagnostics.json`。这仅是旧点的分离诊断；本包未求解 1050 系统、未把旧点绑定到新系统，也未断言新系统的可行性、最优值或 SPE 存在性。

## 首次检查中断及冻结范围

第一次检查在读取过程文件时遇到 `FileNotFoundError`。Main 确认其正规 `work.py sync` 与本目录的新未跟踪写入发生竞态。原始 traceback 和前后输入 SHA 已保存在 `checker_attempt1_sync_race.json`，不将该中断描述为数学失败。随后按 Main 指令停写；同步恢复并明确释放后，只重跑同一份无优化器检查器，得到上述 PASS。未重跑 builder，未改输入。

最终冻结清单为 `visible_maximum_joint_v3/freeze_manifest.json`，逐文件摘要为 `visible_maximum_joint_v3/SHA256SUMS`。本次写入仅限该目录与本说明。没有修改旧包、Git、RUN、registry 或凭据，没有固定 K、缩减 support、具体点补全、优化器调用或新 SPE 声明。后续家族不属于本次 1050 冻结范围。
