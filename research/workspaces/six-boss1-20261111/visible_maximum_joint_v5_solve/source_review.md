# 可见最大 C 联合 v5：求解骨架、释放合同与数学边界

Owner **Boss1**；RUN **six-boss1-20261111**；实际 agent **/root/visible_joint_v5_solve**；profile **full**。

当前状态为 **WAITING_FINAL_INPUT_SHA_AND_EXPLICIT_MAIN_RELEASE**。本目录只完成静态准备，当前优化授权为 **0**，实际优化调用为 **0**。没有新输入 SHA、已释放输入认证、数值结果、证书、最优面或真分支排除结论。`main_release.template.json` 是空模板；本阶段不创建 `main_release.json`。

## 1. 原数学模型和本次工作范围

目标模型保持有限单位客户、有限非空共同合法标签目录、恰六位参与者、任意完整有序历史上的纯 SPE。所有离轨历史都要求弱最优；允许并保留空覆盖标签、重复标签、覆盖别名和零客户边界。目录与真实历史的合法性不能由可见类型投影或一个 LP 可行点替代。

可见必要系统以全部 512 个九位客户类型为原子，位顺序固定为

\[
(a_1,a_2,a_3,a_4,a_5,a_6,x,o,c).
\]

第 513 列是独立非负变量 \(K\)，不固定其数值，也不将它吸收进任意一类一般行。所有原子质量和 \(K\) 均非负。两条仿射等式完整保留：

\[
\sum_v o_vz_v=1,\qquad \sum_v c_vz_v-K=0.
\]

目标为实际覆盖福利

\[
W=\sum_v\mathbf 1\{a_{1v}+\cdots+a_{6v}>0\}\,z_v.
\]

这里的 \(O=1\) 是正基准福利分支的归一化；它不删去原模型中的空标签、零客户或弱平局情形。若以后对原模型陈述普遍界，还必须清楚处理归一化适用范围与其余边界。

Main 已说明：旧 1586 行完整必要系统的精确最优值约为 0.4411521416736506，其全体 20 个零对偶余量列、秩 13 的面已被真实内部 SAFE 义务排除。该历史背景不提供 v5 的输入、返回支持、正付款、零态或等号结论；本程序不读取旧证书和旧点，也不调用已消费的 v4 求解入口。原六人 half 目标仍为 **OPEN**。

## 2. 规划计数不是输入认证

以下仅为 Main 给定的编译规划。最后三项来源尚须 Main 完成冻结审查。即使某个目录或文件已经存在，也不能触发读取或运行。

| 半开 raw 索引区间 | 规划块 | 规划行数 |
|---|---|---:|
| `[0,1586)` | 原 v4 完整 literal raw 前缀 | 1586 |
| `[1586,1767)` | 固定帽 ordered cells | 181 |
| `[1767,1795)` | 固定基底 CAP 耦合 C-only | 28 |
| `[1795,1823)` | 任意 tau 最小帽 C-only | 28 |
| `[1823,2919)` | 全五源 minimal CAP 纯 8T | 1096 |
| `[2919,3056)` | 适应五查询最小帽 ordered | 137 |
| 合计 | 1586 原行 + 1470 新行 | 3056 |

`contract.py` 的 3056/513/2 是待确认的严格合同，绝不是已读取的新输入事实。实际释放必须明确填入相同的精确计数及六段边界，并给出冻结 manifest 中三个维度的明确 JSON pointer。若最终输入、manifest 或分段与规划不符，程序立即报告不匹配，不自行改数、选用旧输入、剪行或放宽合同。Main 必须先处理差异，再决定是否需要另行审阅合同修订。

原 1586 行要求整段 JSON 逐对象相等，包含 raw 顺序、名称、全部精确系数、rhs 和元数据。它不仅检查数值矩阵相等，也保留原零行和重复行的独立位置。原尺度字符串逐条与冻结 v4 尺度文件相等。整个新输入还必须恰有原来的 **30 条 rhs=-1** 仿射行。

新增 1470 行的数值除数逐条为 **25**。这是数值预处理，不能替代各来源真实 IC 权重 \(a\)。输入中的稀疏行字段 `a` 是整行系数对象；来源证明中的标量 IC 权重另由各自的精确元数据和正文确定。

两个 C-only 块已经使用 \(|C|=K\) 做等式改写；相应自由等式乘子可以为负。一般 8T 和 ordered 行必须保留未消元的 \(K\)。这项来源语义由 Main 当前来源审查与全列证据负责，程序不从行名、旧结论或数值缩放猜测它。

## 3. 释放门禁

`status()` 与 `solve_once.py --status` 只检查本目录中的本地门禁状态，不对 v5 输入目录做存在性检查、列举、轮询或读取。导入静态合同不触发任何输入读取。

未来真正运行前，Main 需要在实际明确指令下填写 `main_release.json`，至少包括以下内容。

1. 精确身份：`authorized_by=/root`、Boss1、当前 RUN、当前 agent、profile full；`optimizer_calls_authorized=1`。必须同时明确允许读取最终输入和 SHA 绑定的来源闭包。
2. 状态必须为 `MAIN_EXPLICIT_FULL3056_RAW_V5_SINGLE_LP_RELEASE`，并填写真实的 `explicit_main_instruction`。模板保持等待状态、授权 0、所有授权布尔量为 false。
3. 最终 `exact_input.json`、准备 `freeze_manifest.json`、`numerical_scaling.json`、`source_review.md`、`source_pins.json` 和本目录 `scaffold_manifest.json` 的 SHA256；另给 raw 名称顺序的规范 JSON SHA256。
4. `expected_dimensions` 与 `expected_row_blocks` 必须依据最终冻结结果明确确认。模板中的 `planned_*_reference_only` 不能充当确认；确认字段初始为 null。
5. 冻结 v4 原输入和尺度的精确路径与 SHA，用于 literal 前缀及原缩放比较。它们仅在此门禁通过后作为已释放父输入读取。
6. `preparation_manifest_count_pointers` 明确指定 manifest 中 raw 行数、非负列数、等式数的 JSON pointer，例如 `/counts/raw_inequalities`。实际字段名由 Main 对最终 manifest 确认，程序不猜测。manifest 自身还必须绑定同一 input 与 scaling SHA。
7. `required_evidence` 至少覆盖 `main_preflight`、`source_legality`、`all_raw_column_audit` 三种角色。每项包含路径、SHA、确切 PASS 状态；Main preflight 还必须绑定本次 input SHA。一个经确认的证据文件可以承担多种角色，各角色可分别列出。
8. `source_validity_scope` 的各项必须由 Main 的实际来源审查支持：原模型、所有新来源、全列系数、离轨弱最优、空/重复/别名/零客户、C-only 等式改写、一般行的独立 K，以及数值除数与真实 IC 权重的区别。

证据条目的支持结构如下；这是字段说明，不是可执行授权：

```json
{
  "role": "main_preflight",
  "path": "由 Main 明确指定的仓库相对路径",
  "sha256": "实际冻结 SHA256",
  "expected_status": "实际文件中的确切 PASS 状态",
  "status_pointer": "/status",
  "input_sha256_pointer": "/input_sha256",
  "expected_json_values": {}
}
```

准备 manifest 支持冻结 v4 已用的两种接口：`artifacts` 中的源目录相对路径，以及 `artifact_sha256` 中的仓库相对路径。所有被读文件必须来自 Main 释放的确切 SHA 闭包；同一路径若被赋予冲突 SHA 则失败。哈希后解析同一次读到的字节，避免先哈希、再解析其他字节的竞态。

这些检查能验证身份、文件一致性、完整矩阵、字面保持和精确系数，却不会把一个 PASS 标签自动变成来源数学证明。普遍界依赖的语义推导仍须 Main 实读审查并在最终正文中说明。

## 4. 唯一一次数值求解

唯一优化器调用位置在 `solve_once.py`。默认不带参数运行也只报告状态；实际入口是 `--run-released-once`。

门禁完成后构造完整的 3056×513 矩阵、原两条等式和原目标，包含全部零行、重复行和全部列。程序不以返回支持限制优化模型，不固定 K，不对旧点补全，不调用 734 phase I，也没有第二次 LP 路径。

求解参数固定为 `scipy.optimize.linprog(method="highs-ds")`、60 秒、`presolve=False`、primal/dual feasibility tolerance 均为 `1e-9`。所有变量统一使用 `(0,None)` 边界。

程序先排他写入并 `fsync` `single_lp_consumed.json`，再进入唯一一次优化器调用。消费标记永久保留：超时、失败、异常或进程中断均不重置预算，不允许删除标记重跑。若在来源快照写入后、调用前中断，入口也保守阻止自动重试，交 Main 审阅具体障碍。

全部返回值、原 raw 顺序、每条正尺度、全部不等式/等式/lower/upper 的 residual 与 marginal 均保存。无上界产生的 Infinity 等特殊数值以可逆字符串保存为标准 JSON，不截断或把它们伪装为有限值。

对原式 \(A_i z\ge b_i\)，实际交给求解器的是

\[
-A_i z/d_i\le-b_i/d_i,\qquad d_i>0.
\]

因此原尺度付款严格还原为

\[
y_i=-\frac{\operatorname{SciPyMarginal}_i}{d_i}.
\]

保存的数值 marginal 不会被精确恢复覆盖；原始数值与恢复值的差异单独记录。

## 5. 有理恢复和独立全域核验

`recover_exact.py` 只在唯一一次成功返回之后使用精确线性代数。原始返回的每个严格正 primal 分量均进入支持；每个严格负不等式 marginal 均进入待恢复的正付款支持。它不按阈值丢掉小正量。若付款等号不足以确定 primal，则只补入该次返回的数值 tight 行做精确方程求解，不启动优化器。

恢复使用原始精确系数和 rhs，求解完整仿射方程。如果返回支持不能给出唯一有理解、恢复值违反任一原行/列/等式，或对偶剩余不能全非负，则写出具体 `recovery_obstacle.json`；没有优化重试或旧证书替代。

两条等式的乘子 \(\eta\in\mathbb Q^2\) 保持自由。验证原尺度残差

\[
r=c-A^Ty-E^T\eta\ge0,
\]

以及包含全部仿射行的对偶目标

\[
\alpha=b^Ty+h^T\eta.
\]

30 条 \(b_i=-1\) 的付款不会丢失。若 C-only 改写造成第二个等式乘子为负，这不构成符号错误；只有不等式付款 \(y\) 受非负约束。

`verify_certificate.py` 不导入恢复或求解器代码，使用标准库 `Fraction` 独立重读原始 coefficient 字符串，重算全部 3056 个 raw slack、全部 513 个 dual residual、两条等式残差、全部原尺度记录和两侧互补乘积。

它逐项验证恒等式

\[
c^Tz-\alpha
=\sum_i y_i(A_i z-b_i)
+\sum_j r_jz_j
+\sum_k\eta_k(E_kz-h_k).
\]

精确 primal 与 dual 目标相等才形成必要系统最优性证书。只有在当前来源对原完整 SPE 模型确实合法且全列证据充分时，才可以把对偶组合解释为原模型的普遍福利界。一个精确 primal、甚至可按公分母整数化的原子向量，也不构成完整有序历史上的纯 SPE。

## 6. 完整最优面与全部参数条件

`analyze_optimal_face.py` 从所有满足 \(r_j=0\) 的列开始，而非仅从返回点的正支持开始。所有 \(r_j>0\) 的列强制为零。面上的线性等式包括两条原等式与全部 \(y_i>0\) 的 raw 等号：

\[
Ez=h,\qquad A_i z=b_i\quad(y_i>0).
\]

程序给出精确 RREF 参数化，但保留每一条原 raw 不等式和全部 513 个非负坐标条件。零行、重复行、原 rhs=-1、未付款行都保留为原顺序下的参数条件。无约束仿射参数个数不自动等于加上所有不等式后的可行面相对维数。

`verify_optimal_face.py` 使用独立标准库 Fraction 消元，重算全部零 residual 列、正付款方程、秩、自由坐标、完整参数化、每条 raw 参数不等式和全部坐标非负条件。它还核对代表点重建、目标常数及所有固定泛函的全 513 列恒等式。

初始泛函仅包括 W、K、六人的实际效用、C/X 大小及 C 在 O 外的质量。不会预置旧的效用/K 等号。固定泛函的表示允许带符号面等式系数，并以强制零列补足到全 513 列；这种面上恒等式不冒充普遍非负付款证书。

## 7. 真分支诊断的后续接口

`diagnose_true_payments.py --queue` 只在精确证书和完整面都经独立核验后运行。它依据本次实际 \(y_i>0\) 构造完整队列，保存每条原行身份、精确付款、数值尺度、K 系数和完整来源元数据。没有预设正行编号、旧内部 SAFE 参数、旧零态表或旧 `u2=K/5` 结论。

本阶段尚未获得最终新来源定义，故诊断入口诚实停在**待实读当前来源并实施对应公式核验**这一数学接口，不会输出 `true_branch_equality_diagnostic.json` 或伪造一份来源排除证明。Main 释放所需的新来源后，再基于实际付款实施针对性诊断：识别真实权重与历史、重算全部弱最小态和全部并列零态、核对原 full-column 行、从各自非负分解的正付款推导必要等号，并将结论推广到完整面和全部参数条件。

如果只能排除必要系统最优面的可达性，仍应区别于统一提高一个正 epsilon，以及证明 half。若诊断不足，保留具体未完成义务，不通过固定 K、缩小支持、添加新 LP 或把某个旧零态集粘贴进来完成证明。

## 8. 复现顺序与当前可运行操作

当前阶段仅运行静态检查、等待状态和本地静态指纹：

```bash
python -B preflight.py --static --write-report
python -B solve_once.py --status
python -B freeze_scaffold.py
```

这些命令不读取输入目录、不导入优化器、不创建消费标记。`scaffold_manifest.json` 与 `SCAFFOLD_SHA256SUMS` 只冻结静态骨架，不是输入冻结或执行许可。

在 Main 明确释放最终输入和单次调用后，未来运行链为：

```bash
python -B preflight.py --released
python -B solve_once.py --run-released-once
python -B recover_exact.py
python -B verify_certificate.py
python -B analyze_optimal_face.py
python -B verify_optimal_face.py
python -B diagnose_true_payments.py --queue
```

该列表不是当前授权。每一步先验证实际前置文件绑定；数值失败、有理恢复障碍、核验失败或来源不匹配都会停止相应链条。最终数学正文、真正来源诊断和结果冻结只能在实际证据产生后完成。本 agent 不写 Git、RUN 或登记状态；这些由 Main 串行管理。
