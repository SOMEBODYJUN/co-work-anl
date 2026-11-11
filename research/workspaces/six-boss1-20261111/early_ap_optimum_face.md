# AP39 排除完整共同 X 必要 LP 的整个 W10 最优面

Boss1；RUN `six-boss1-20261111`；独占工作区 `early_ap_optimum_face/`。

**最终结论：已给出并独立精确核验整面恒等式。** 对冻结的 `22297×21021` 完整共同 X 必要 LP，每一个目标值等于

\[
W_{10}=
\frac{41418833157785254128446533347783719656800199407573523353330084664882709}
{83821400169176597880954822390709624066211318077718478066891770484527716}
\approx0.4941319647988424
\]

的可行点，都满足

\[
\boxed{
\operatorname{AP39}(x)=\alpha=
-\frac{2387360308883849167939463658247160398139890481107232380975950684899327}
{167642800338353195761909644781419248132422636155436956133783540969055432}
<0.}
\]

这里 `α≈−0.014240756561364065`。所以追加普遍必要行 `AP39≥0` 会排除**整个原 W10 最优面**，不是只切去显示的 `5b1b` 最优点。

成功证书使用从原对偶互补松弛、全局等式与非负性严格推出的面等式和零列。**本包没有给出追加系统的新定量下界、精确新最优值、SPE 实现或六人 half 结论。** 原先只允许使用旧对偶正行与正残差列的窄 span 确实失败；失败证据和后续成功证据均完整保留。

## 1. 输入、坐标和 AP39 身份

全部输入按字节 SHA256 绑定；没有修改原矩阵、原 primal、原 dual 或 AP 行包。

| 输入 | SHA256 |
|---|---|
| [完整矩阵](maxb_augmented_lp/full_lift/exact_matrix.json.gz) | `c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b` |
| [精确 primal](maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json) | `5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe` |
| [精确 dual](maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json) | `4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f` |
| [旧任意锚 AP 的 51 行包](early_x_anchor_queries/rows_51.json) | `0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb` |

AP39 是行包从零起算的索引 39：actual 玩家 3、背景 `(A1,A2)`、剩余人数 4、`Q=A6`、共同常数 23。写 `b2=1_A1+1_A2`，其确切形式为

\[
C=23u_3-22\sum_X\frac1{b_2+4}
-\sum_{A_6}\frac1{b_2+1}
+\sum_{X\cap A_6}\frac3{(b_2+1)(b_2+4)}.
\]

该行恰有 25 个非零系数，不含 420 个交叠上包络 y 列。其普遍必要性来自已有任意锚 AP 的合法代入，见 [early_x_anchor_queries.md](early_x_anchor_queries.md)；本包不重授新引理。

独立核验器从完整矩阵的六位 `actual_bits` 重新计算 `u3`、`A6`、背景负载和 16 个共同 X 系数，再与保存的 AP39 全部 21021 个坐标逐项比较。全部 16hist、六个原零 hist `1,59,366,449,524,574` 和全部辅助列始终保留。已证某列在原最优面上为零，与删去该列或把点上零权设为先验，是不同操作。

## 2. 原窄 span 的精确失败与五列障碍

原精确对偶有 463 条严格正行乘子、5379 个严格正列残差。首次检验只允许恒等式

\[
C=\alpha o+\sum_{i:\lambda_i>0}\beta_i A_i
+\sum_{j:r_j>0}\delta_j e_j,
\]

其中 `o` 是归一化向量。完整保留 15642 个零残差列方程，不以 primal 正支持筛列。前 453 个去重方程消元到已建立秩 280 时出现精确矛盾 `0=1/2`；这里的 280 是失败时已处理子系统的秩，不宣称是整个系数系统的最终秩。

矛盾可压缩为以下整数向量 d，其余 21016 个坐标均为零：

| 共同 X 列 | 所属 hist 列 | d 系数 |
|---:|---:|---:|
| 20585 | 1 | 1 |
| 20590 | 225 | 4 |
| 20592 | 308 | −12 |
| 20594 | 424 | −3 |
| 20598 | 524 | 10 |

独立逐项检查得到

\[
o\cdot d=0,\qquad A_i\cdot d=0\;(\lambda_i>0),\qquad
d_j=0\;(r_j>0),\qquad C\cdot d=5.
\]

因此 C 不在上述窄 span 中，甚至不允许通过换另一个 α 来修复。完整分数证书见 [exact_span_obstruction.json](early_ap_optimum_face/exact_span_obstruction.json)，原始整数障碍及全部 463 个行点积见 [primitive_obstruction.json](early_ap_optimum_face/primitive_obstruction.json)。首次独立审计为 [PASS_EXACT_REQUESTED_SPAN_OBSTRUCTION](early_ap_optimum_face/independent_audit.json)。

**d 不是原最优面的可行移动方向。** 一个足够的具体原因是：hist 列 1 的原对偶残差严格正，因此每个 W10 最优点的第 1 列都为零；原行 20910 为 `x1−x20585≥0`，再结合非负性，迫 `x20585=0`。d 在该坐标却取 1。沿 +d 会违反该上界行，沿 −d 会违反该列非负性。首次窄 span 只允许线性使用原正对偶项，没有自动包含这条非负性推理；其失败不能解释为原最优面仍能满足 AP39。

## 3. 全局有效的面零传播

记完整可行域为

\[
P=\{x\ge0:A_i x\ge0\ (0\le i<22297),\ o x=1\},
\qquad F=\{x\in P:c x=W_{10}\}.
\]

原精确对偶恒等式是

\[
c=W_{10}o+\sum_i\lambda_iA_i+r,
\qquad\lambda_i\ge0,\ r\ge0.
\]

对任何 x∈F，所有非负项的总和为零，故 `λ_i>0⇒A_i x=0`，`r_j>0⇒x_j=0`。**这给出的 5379 个正残差零列是传播的全部初始零列。** 显示 primal 的其他零权不进入前提。

随后枚举完整矩阵全部精确相反行。共发现 377 对非零相反行，以及由 100 条原零行组成的一个零行组；合计 378 组、854 个原行索引。每对 `A_i=−A_k` 连同两条原不等式推出全局等式。它们与 463 条正对偶行的并集包含 1004 条初始等式。相反关系按完整原行系数精确确认；哈希只用作索引，不替代系数核验。

传播只使用以下规则，每次都保存原行、此前已证零列和本步新迫零列：

1. 原必要行 `A_i x≥0` 删去已证零坐标后，若剩余非零系数全部严格负，则每个剩余非负变量必须为零，该行也成为等式。
2. 已证明的等式 `A_i x=0` 删去已证零坐标后，若剩余系数全部同号，则所有剩余变量必须为零。负号情形已被规则 1 覆盖，正号情形另外记录。
3. 原行全部支持已被证明为零时，该行自然成为等式。这类零支持等式不创造新的变量零前提。

这些规则逐步对整个 F 成立。完整证明 DAG 保存在 [closure_certificate.json.gz](early_ap_optimum_face/facial_zero_closure/closure_certificate.json.gz)，所有新列的首次来源及所有等式的成立来源均可回溯。

| 轮次 | 新强制零列 | 新证明步骤 | 累计强制零列 |
|---:|---:|---:|---:|
| 初始 | 5379 | — | 5379 |
| 1 | 3480 | 2667 | 8859 |
| 2 | 928 | 717 | 9787 |
| 3，收敛检查 | 0 | 0 | 9787 |

共 3384 个实质传播步骤，其中 3198 步来自负系数原不等式，186 步来自正系数已证等式。最终得到 9787 个真零列、6376 条真等式，并对全部 22297 行确认上述规则已无可继续新增之处。

原五列障碍中的 20585 和 20598 都被严格传播为零。最短的两段来源是：

- 第 2393 步：初始正残差列 1 已为零，原行 20910 `x1−x20585≥0` 迫列 20585 为零。
- 第 779 步：列 2777…2784 均有原对偶严格正残差；原行 5488 `−x524+Σ_{2777…2784}x_j≥0` 迫列 524 为零。第 2397 步再由原行 20923 `x524−x20598≥0` 迫列 20598 为零。

这些均未使用“它在 5b1b 点上恰为零”作为理由。

## 4. 扩展恒等式与整面排除

在已证零列 Z 上允许带符号坐标向量 `e_j`，在已证等式行集合 E 上允许带符号行组合。先把等式投影到其余坐标；相同或成比例的投影只保留代表，并记录被省略行与代表的比例及仅支撑于 Z 的差。这是线性代数去冗余，不是删去原系统的约束或坐标。

最终有 254 条等式代表、11234 个非强制零坐标的完整方程，其中 437 个去重方程用于有理消元。消元满秩 254，得到

\[
\boxed{C=\alpha o+\sum_{i\in E}\beta_i A_i+\sum_{j\in Z}\delta_j e_j.}
\]

非零 β 共 223 个，非零 δ 共 5682 个；全部精确分数保存于 [expanded_signed_identity.json](early_ap_optimum_face/facial_zero_closure/expanded_signed_identity.json)。完整 21021 个系数均精确相等。恒等式每项的成立来源另列于 [identity_support_provenance.json.gz](early_ap_optimum_face/facial_zero_closure/identity_support_provenance.json.gz)。

任意 x∈F 都满足 `o x=1`、`A_i x=0 (i∈E)`、`x_j=0 (j∈Z)`，于是 `C x=α<0`。这就是整面排除的完整逻辑，不依赖显示 primal 的正支持是否唯一或是否能代表其他最优点。

这里 223 个行系数中有 19 个来自原零对偶权的真等式；5682 个零列系数中有 351 个来自原零残差、经传播才证明为零的列。特别有 17 个新行系数为正、99 个新零列系数为正。因此不能直接沿原 λ、r 套用 `t=min λ/β,r/δ` 得到正步长。这份恒等式没有把它们冒充原对偶严格正权。若以后要从这里取得新的显式定量下界，需要另给覆盖这些生成元的正权面暴露证书或其他合法对偶构造。

## 5. 独立核验与保全

成功后的独立入口为 [verify_closure_and_identity.py](early_ap_optimum_face/facial_zero_closure/verify_closure_and_identity.py)，未导入构造器。其 [independent_audit.json](early_ap_optimum_face/facial_zero_closure/independent_audit.json) 状态为：

```text
PASS_EXACT_WHOLE_W10_OPTIMUM_FACE_EXCLUDED_BY_AP39
```

核验覆盖：原 primal 全 22297 行、原 dual 全 21021 列、全部原列描述符、所有相反行组的完整性和精确系数、3384 个传播步骤的此前零前提、全行闭包收敛、最终 9787 个零列和 6376 条等式的来源、254 个等式代表的去冗余合同、11234 个列方程、254 个消元基步骤，以及最终恒等式的全部 21021 个坐标。AP39 另从原六位 hist 描述符独立重建。

| 核心文件 | SHA256 |
|---|---|
| 原窄 span 障碍 `exact_span_obstruction.json` | `910b2ad85282ffadbc1b3ea4df5ef34bb1c8b5a9b9927d057717135ff56b5811` |
| 原五列整数障碍 `primitive_obstruction.json` | `57fc939cfed10b63166d8808dfd8a13f8a7c4f50ddf584b8512c4d17c7275eb5` |
| 闭包证明 `closure_certificate.json.gz` | `967c5c1c03f28c6e63bed7afdf4fd40e0a21a204294c9eb8a5532be3850bf6d1` |
| 成功恒等式 `expanded_signed_identity.json` | `f181007406679ad16da7c6999abeaf26083a7d1302a023fd31f8f2d1ac94404d` |
| 成功独立核验器 `verify_closure_and_identity.py` | `ddfd0df82d3d810b6ad00d44df135ed0811ebfbea6256cc0fc52d554369633cd` |

工作区同时保留两次构造和两次独立验证的实际命令、源码 SHA、标准输出、标准错误、退出码、完整有理方程、消元记录、全行/列检查数组及原始输入固定哈希。原始输入按本稿第 1 节路径保留在原位置，未另造变体覆盖它们。两个构造器及两个核验器均只用 Python 标准库，优化器调用数为 0。

构造入口是 [build_optimum_face.py](early_ap_optimum_face/build_optimum_face.py) 与 [build_closure_and_span.py](early_ap_optimum_face/facial_zero_closure/build_closure_and_span.py)；原失败检查入口是 [verify_obstruction.py](early_ap_optimum_face/verify_obstruction.py)。所有脚本默认拒绝覆盖现有证明产物；复跑须先保全现包，在等层级空副本保留相同输入路径关系。

最终文件清单与全部准确 SHA 见 [freeze_manifest.json](early_ap_optimum_face/freeze_manifest.json) 和 [SHA256SUMS](early_ap_optimum_face/SHA256SUMS)。本包冻结后释放工作席；不改 Git、RUN 或 registry。
