#!/usr/bin/env python3
"""Write the actual v5 theorem/report after all exact checks; no optimization."""
from fractions import Fraction as F
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, digest, load_verified_certificate, read_json, require


def main():
    bundle, cert, check = load_verified_certificate()
    face = read_json(HERE / "optimal_face.json")
    face_check = read_json(HERE / "optimal_face_check_result.json")
    diag = read_json(HERE / "true_branch_equality_diagnostic.json")
    independent = read_json(HERE / "true_branch_independent_check.json")
    require(independent["status"] == "PASS_INDEPENDENT_CURRENT_SOURCE_STATES_AND_FULL_FACE_SAFE_CONTRADICTION"
            and independent["diagnostic_sha256"] == digest(HERE / "true_branch_equality_diagnostic.json"),
            "Actual independent true-source verification is required")
    alpha, K = F(cert["objective"]), F(cert["K"])
    D, L = alpha.denominator, int(cert["common_denominator"])
    positive = cert["dual"]["positive_raw_indices"]
    y = list(map(F, cert["dual"]["raw_row_weights"]))
    dual_table = ["| raw 索引 | 名称 | 精确分子系数 qᵢ（yᵢ=qᵢ/D） | 原付款近似 |", "|---:|---|---|---:|"]
    for i in positive:
        dual_table.append(f"| {i} | `{bundle['rows'][i]['name']}` | `{y[i]*D}` | {float(y[i]):.16g} |")
    primal_table = ["| 列 | 九位类型／K | 整数质量 Lzⱼ |", "|---:|---|---:|"]
    for j in cert["primal_support"]:
        bits = format(j, "09b") if j < 512 else "K"
        primal_table.append(f"| {j} | `{bits}` | `{F(cert['primal'][j])*L}` |")
    zeros = ["| p | c | o | 两个实际正 C 行的全部共同弱零态 r₃r₄r₅r₆ |", "|---:|---:|---:|---|"]
    for item in diag["all_common_C_branch_weak_zero_states"]:
        tails = ", ".join("`"+"".join(map(str, tail))+"`" for tail in item["all_common_weak_zero_tails"])
        zeros.append(f"| {item['p']} | {item['c']} | {item['o']} | {tails} |")
    gaps = ["| 全面固定泛函 | 精确常数 | 近似 |", "|---|---|---:|"]
    for name in ["K_over5_minus_N3", "K_over5_minus_N4", "K_over5_minus_N5"]:
        value = F(independent["functional_values"][name])
        gaps.append(f"| `{name}` | `{value}` | {float(value):.16g} |")
    replacements = {
        "@@ALPHA@@": str(alpha), "@@ALPHA_DEC@@": format(float(alpha), ".17g"),
        "@@D@@": str(D), "@@L@@": str(L), "@@K@@": str(K), "@@K_DEC@@": format(float(K), ".17g"),
        "@@HALF_GAP@@": str(F(1, 2)-alpha), "@@ETA_C@@": cert["dual"]["equality_multipliers"][1],
        "@@DUAL_TABLE@@": "\n".join(dual_table), "@@PRIMAL_TABLE@@": "\n".join(primal_table),
        "@@ZERO_TABLE@@": "\n".join(zeros), "@@GAP_TABLE@@": "\n".join(gaps),
        "@@N5_N4@@": independent["N5_minus_N4"], "@@N5_N4_DEC@@": str(independent["N5_minus_N4_decimal"]),
        "@@OUTSIDE@@": independent["O_outside_C_mass"],
        "@@INPUT_SHA@@": cert["input_sha256"], "@@CERT_SHA@@": digest(HERE / "exact_certificate.json"),
        "@@FACE_SHA@@": digest(HERE / "optimal_face.json"), "@@RELEASE_SHA@@": digest(HERE / "main_release.json"),
    }
    proof = r'''# 完整 3056 行必要系统：精确最优值及整个最优面的真实 SPE 不可达性

Boss1；RUN `six-boss1-20261111`；profile `full`；实际 agent `/root/visible_joint_v5_solve`。

## 1. 已证明的结论与原问题边界

在 Main 明确释放的完整 3056 条 raw 不等式、513 个非负变量和两条自由等式上，唯一一次完整 LP 的返回已恢复为精确 primal-dual 证书，最优值为

\[
\boxed{\alpha=
\frac{108858965563724169521890917325832631652315417}
{246421667899918066927761529101381586610108429}
\simeq 0.44175890250014965.}
\]

所有当前来源均已由 Main 按原模型审查并冻结，独立精确核验覆盖全部 raw 行、全部列、两条自由等式、原尺度、仿射 RHS 和互补。因此该对偶组合给出原完整模型的必要福利界。

进一步，**本次全部 18 个零对偶余量列上的完整最优面，都不能由原模型的完整有序历史纯 SPE 实现**。证明只用这次实际正付款的最小帽 C 行和真实内部 SAFE；不移植旧正行、旧零态或旧效用/K 等号。

因此，对于可作正 OPT 归一化的原模型 SPE，归一化福利不等于 α，实际逐实例满足 W>α。这个结论没有给出统一增加的正 epsilon，也没有构造一个完整 SPE 或识别原模型的精确最坏值。α 与 half 的差为 `@@HALF_GAP@@`。**原六人 half 目标仍为 OPEN。**

## 2. 原模型、完整输入及唯一调用

模型为有限单位客户、有限非空共同合法标签目录、恰六名参与者、任意完整有序历史上的纯 SPE；所有离轨节点均为弱最优。空覆盖、重复标签、覆盖别名、任意菜单重叠和零客户边界保留。O 是六个合法查询标签的覆盖并，不被当成一个合法行动；C 是真正达到全目录最大裸大小 K 的合法标签。

完整客户轴为 `(a1,a2,a3,a4,a5,a6,x,o,c)`，全部 512 型都存在；第 512 号列是独立非负 K。归一化等式为 |O|=1、|C|−K=0。目标 W 是原六个实际标签的覆盖并大小。

| raw 索引区间 | 完整来源 | 行数 |
|---|---|---:|
| 0–1585 | 原冻结 v4 全部 raw，逐对象 literal 保留 | 1586 |
| 1586–1766 | 固定帽完整 ordered cells | 181 |
| 1767–1794 | 固定基底 CAP 耦合 C-only | 28 |
| 1795–1822 | 任意 τ 最小帽 C-only | 28 |
| 1823–2918 | 全五源 minimal CAP、八个合法纯目标 | 1096 |
| 2919–3055 | 适应五查询最小帽 ordered | 137 |
| 合计 | 完整原始顺序 | 3056 |

原零行、重复行、30 条 rhs=−1、原正尺度均完整保留。新增 1470 行的数值除数逐条为25；真实 IC 权 a 另按来源解释。一般行保留未消元的 K，C-only 的大小等式改写允许带符号自由乘子。额外研究的 λ 族未读入或纳入本轮。

Main 的 `main_visible_c_v5_preflight.json` 已核完整 literal 来源拼接和1,567,728个行列位置。本席的 `released_preflight_result.json` 随后核同一输入、完整轴、两等式、父1586行、全部原尺度和30条仿射行。

唯一一次 `highs-ds` 使用60秒、`presolve=False`、两项可行性容差均1e−9，完整矩阵不删行、不剪列。先排他写入并 fsync 消费标记，再调用优化器。结果 status=0、61次迭代，数值目标为0.4417589025001496。此后均为精确线性代数、Fraction复核或有限穷举，优化调用总数仍为1；没有第二LP、固定K、支持受限优化、旧点补全或734 phase I。

## 3. 原尺度精确 primal-dual 证书

原行记作 Az≥b，原等式为 Ez=h，非负变量为z。对偶付款 y≥0、等式乘子 η 自由，残差为

\[
r=c-A^Ty-E^T\eta\ge0,\qquad
\alpha=b^Ty+h^T\eta.
\]

数值行是 −Aᵢz/dᵢ≤−bᵢ/dᵢ，因此原付款为 `yᵢ = −SciPyMarginalᵢ/dᵢ`。所有原始 marginal 与尺度都保留；精确恢复未覆盖原始数值。

令

\[
D=246421667899918066927761529101381586610108429.
\]

恰有下列10个正 raw 付款，其余3046个均为零：

@@DUAL_TABLE@@

两自由等式按 |O|=1、|C|−K=0 排列，乘子为

\[
\eta_O=\alpha,
\qquad
\eta_C=\frac{17560299240390358516980000298183461273047505498589}
{815345722290510704602695537321963513643503383586318}.
\]

本次 bᵀy=0，hᵀη=α；这是30条 rhs=−1 行的实际付款全部为零的结果，不能据此删除这些仿射行。等式乘子始终不加符号限制。

返回点的精确正支持共12列。令共同分母 L=`@@L@@`，下表记录精确整数质量 Lzⱼ，其余501列为零：

@@PRIMAL_TABLE@@

原尺度恢复的 primal 与 dual 线性代数秩均为12。独立 `verify_certificate.py` 从原始 coefficient 字符串重算全部3056个 raw slack、513个 dual residual、两条等式残差、全部缩放记录和所有互补乘积；全部符合非负、零残差和零互补。

完整仿射恒等式为

\[
c^Tz-\alpha
=\sum_i y_i(A_i z-b_i)+\sum_j r_jz_j
+\sum_k\eta_k(E_kz-h_k).
\]

精确 primal 目标与对偶目标均为 α，故这的确是完整必要系统最优值。可整数化的客户型质量只提供该必要系统的代表点，不提供完整历史策略或 SPE 实现。

## 4. 全部零余量列上的完整最优面

零对偶余量列恰为

```text
0, 2, 3, 14, 15, 18, 19, 22, 23, 50, 51, 74, 75,
331, 459, 483, 499, 512
```

其余495列在每个最优解中都强制为零。面等式是两条原等式和全部10条实际正付款等号，限制到这18列后的秩为12。精确 RREF 选择自由坐标

```text
z0, z15, z19, z23, z51, z75.
```

`optimal_face.json` 给出完整坐标参数化，仍保留全部3056条原 raw 参数不等式和全部513个坐标非负条件。6是无约束仿射参数个数，不直接声称它等于最终可行面的相对维数。`verify_optimal_face.py` 使用独立 Fraction RREF 复核所有列、方程、秩、参数条件及固定泛函的全513列带符号恒等式。

整个面上 K 固定为

\[
K=\frac{99544754486880443492045505264159012847352877}
{492843335799836133855523058202763173220216858}
\simeq0.20198052252310278<1.
\]

18个允许列中没有 c=1,o=0 型，所以全脸 |C∖O|=0。允许列中也没有 p=a1=1,o=1,c=0 型。以上是完整零列域的事实，不是只查看代表点的正支持。

## 5. 本次新正付款的真实参数

全部新正付款都来自第二真实源；新的 ordered137行本次付款均为零。

| raw | 强制合法目标 | τ₃,τ₄,τ₅ | s | 真实IC权 a |
|---:|---|---|---|---|
| 1803 | C，C-only | 0,5977/6912,43/48 | 61273/6912 | 859/48 |
| 2563 | A5 | 0,0,8/9 | 9 | 152/9 |
| 2564 | A6 | 0,0,8/9 | 9 | 152/9 |
| 2606 | C，一般行 | 0,5977/6912,43/48 | 0 | 184969/6912 |

两条 C 行的中间帽权相同：

\[
(\beta_3,\beta_4,\beta_5)
=\left(\frac{59833}{497664},\frac{6725}{6912},\frac{47}{48}\right),
\quad S=1+\beta_3+\beta_4+\beta_5=\frac{1528993}{497664}.
\]

三个帽权均严格正，τ₄、τ₅严格正而τ₃为零。末CAP和末BR六查询均值的真实权均为1。A5/A6两行的帽权为 `(35/324,35/324,35/36)`，S=709/324；它们也已按各自真实分支和完整列重新核对。

本次两个实际正 C 行给出准确全513列身份

\[
A_{1803}-A_{2606}
=s\,(K/5-u_2)+S\,(|C|-K),\qquad s=61273/6912>0.
\]

在本次面上两行均紧且 |C|=K，因此新推得 u₂=K/5。这是本轮真实参数和系数的推导，没有作为先验条件加入求解器。

## 6. 真实成本和所有弱零态

在真实第二源节点(A1)强制C，保持该完整策略自己的真实后继 R3,R4,R5,R6。记p=1_A1、c=1_C、尾会员r3,r4,r5,r6，L=p+c+r3+r4+r5+r6。内部收益始终记作真实分支的vⱼ，不换成原实际uⱼ。

按照当前来源预算，正权相加源IC、三个中间帽、末帽、末BR均值和真实内部SAFE均值；再按真实六查询会员d≥o弱化后，逐客户成本为

\[
\Psi=\frac{ac-r_6-\sum_{j=3}^5\tau_jr_j}{L}
+\sum_{j=3}^5\beta_jr_j+r_6
+\frac{o}{6(p+c+r_3+r_4+r_5+1)}
+\sum_{j=3}^5\frac{\tau_jo}{6(p+c+\sum_{h=3}^{j-1}r_h+7-j)}.
\]

L=0时首分子为零，首项取零。源给出的准确最小值为

\[
m=c\left[S+\frac{24}{p+5}-\frac s5\right]
+\frac{o}{6(p+4c+1)}
+\sum_{j=3}^5\frac{\tau_jo}{6[p+(j-2)c+7-j]}.
\]

本席从每个人的真实份额和各预算重新枚举四条新正行的全部512个隐藏态、32张全弱平局最小表、16384个真实六菜单模式，并重构全部4×513=2052个原行系数；全部精确通过。第二份标准库Fraction程序独立重算全部状态、完整最小态与菜单差，未导入第一份诊断程序或优化器。

两条实际正 C 行在同一真实C分支上的完整共同弱零态为：

@@ZERO_TABLE@@

特别保留了 p=1,c=1,o=0 的 `1011`、`1101` 替代态，以及C外全部弱态。它们没有被人为删去。它们在某些局部等号中确实合法；只有全脸 |C∖O|=0 才使 c=1,o=0 客户不承载质量。

更强地，1803单行在 c=o=1 时就已经只有 p=0→1111、p=1→1110。此事实也独立逐态核验；不必先使用另一C行来删除其他o=1零态。

## 7. 从本次零态到真实中间覆盖

假设某个原完整SPE达到α。精确对偶互补使1803原行紧。其来源中的源IC权、三个CAP权、末CAP/BR权及τ₄、τ₅均严格正，非负付款分解的这些分量必须分别取等。C大小自由等式项为零，不要求它的系数非负。

因为面上C⊆O，每个C客户使用上节c=o=1的真实零态。因此R3、R4、R5都包含C。三个正CAP分别强制 |Rj|=K，而 |C|=K，所以三者在客户覆盖上都恰等于C，C外质量均为零。这里不把覆盖相等的不同标签历史合并；只使用该一条真实历史的覆盖集合结论。

每个C客户在这些真实零态中总负载恰为5。因此

\[
v_3=v_4=v_5=K/5.
\]

这个结论是在新零态、全脸C⊆O与正CAP之后才得到，不能在这些步骤之前假设R4/R5=C。τ₃=0也没有被错误地当成正付款。

真实菜单弱化差的核含末查询正权1，严格正；它取等强制d=o。因此实际正τ₄、τ₅的真实内部SAFE取等后，其下界恰为

\[
N_4=\sum_x\frac{o_x}{6(p_x+2c_x+3)},\qquad
N_5=\sum_x\frac{o_x}{6(p_x+3c_x+2)},
\]

从而必要地 N4=N5=K/5。每个内部SAFE使用它自己的完整偏离续局上界，仍符合原有序历史弱最优性；没有固定偏离后的后继。

## 8. 整面矛盾：真实 SAFE4/5 不能同时取等

Main独立指出的结构差在全部513列得到独立精确核验：

\[
\boxed{
N_5-N_4=\sum_x\frac{o_x(1-c_x)}{6(p_x+2)(p_x+3)}.
}
\]

因为p∈{0,1}，且整面 |O|=1、C⊆O、K<1，有

\[
N_5-N_4\ge\frac{1-K}{72}>0.
\]

这与正τ₄、τ₅的真实等号要求N4=N5矛盾。当前完整面进一步强制p=1,o=1,c=0质量为零，故准确有

\[
\boxed{N_5-N_4=\frac{1-K}{36}
=\frac{393298581312955690363477552938604160372863981}
{17742360088794100818798830095299474235927806888}
\simeq0.02216720770769156>0.}
\]

因此不只是代表点，而是完整3056必要系统的整个最优面都被原模型真实内部SAFE排除。

另有全脸固定泛函提供直接不等式矛盾。N3在R3前真实历史(A1,C)上定义为Σo/[6(p+c+4)]；N4、N5在上节已经证明的中间覆盖条件下定义。准确值为：

@@GAP_TABLE@@

所以SAFE4和SAFE5各自的必要不等式也已违反。N3的差为正，它不能作为排除理由。`true_branch_face_functionals.json` 对上述固定泛函保存带符号面等式权及强制零列权，并在全部513列验证恒等式；它们不是新的普遍非负付款行，也没有添加到LP输入。

## 9. 工件、复核和实际障碍保存

| 工件 | 作用 |
|---|---|
| `main_release.json`、`single_lp_consumed.json` | Main实际一次释放与永久消费记录 |
| `source_pins_at_solve.json`、`released_preflight_result.json` | 实际输入/来源/代码/证据指纹及完整输入门禁 |
| `discovery_output.json`、`numerical_summary.json`、`solver_run.log` | 唯一实际求解及完整原数值记录 |
| `exact_certificate.json`、`all3056_raw_row_checks.json`、`all513_column_checks.json` | 原尺度完整精确证书与逐行/逐列结果 |
| `independent_check_result.json` | 独立Fraction全域/等式/尺度/互补核验 |
| `optimal_face.json`、`optimal_face_check_result.json` | 全18零列面、所有原行条件与独立RREF核验 |
| `positive_payment_diagnostic_queue.json` | 本次全部实际正付款来源义务；是当时的队列快照 |
| `current_positive_source_state_checks.json` | 四条新正源全部弱态、菜单模式与完整系数 |
| `true_branch_face_functionals.json` | 全脸固定泛函的精确全列身份 |
| `true_branch_equality_diagnostic.json`、`true_branch_independent_check.json` | 当前真分支排除及独立状态/结构差复核 |
| `metadata_read_attempt1_obstacle.json` | 实际一次只读元数据路径错误及更正记录 |
| `scaffold_manifest.json`、`scaffold_summary_before_release.md` | 原等待阶段历史快照，不冒充当前释放状态 |
| `final_source_verification.json`、`freeze_manifest.json`、`SHA256SUMS` | 最后来源/程序不变性及实际成果冻结 |

唯一记录的操作失败是一个额外只读元数据提取命令用 `Path('.')` 再取`.parent`，导致找错已释放输入的相对路径；随后改用`Path.cwd()`完成同一只读提取。它未调用优化器、未改核心程序，也不影响数值求解或精确恢复。求解、恢复、独立证书、完整面及真分支核验本身均成功。原失败记录保留，没有用删除记录的方式重跑任何优化器。

当前来源正文为 `source2_minimal_cap_safe/proof.md` 与 `all_source_minimal_cap_safe/proof.md`；其真实预算、正帽、弱最小态、C自由等式和一般K付款经过实读，并与Main全来源准入证据一起绑定。所有释放时核心程序保持原SHA；实际结果之后新增的诊断、独立诊断核验和本正文生成代码另行保存，没有改写已消费输入或冻结核心。

主要指纹：

- 输入：`@@INPUT_SHA@@`
- 实际Main释放：`@@RELEASE_SHA@@`
- 精确证书：`@@CERT_SHA@@`
- 完整最优面：`@@FACE_SHA@@`

最终结论是完整必要系统的精确最优性和该整个最优面的真实SPE不可达性。half仍OPEN；没有第二LP、没有新增输入行、没有统一epsilon结论。
'''
    for key, value in replacements.items():
        proof = proof.replace(key, value)
    require("@@" not in proof, "Unfilled proof placeholder")
    with (HERE / "proof.md").open("x") as output:
        output.write(proof)
    adjacent = HERE.parent / "visible_maximum_joint_v5_solve.md"
    with (HERE / "adjacent_summary_before_release.md").open("x") as output:
        output.write(adjacent.read_text())
    summary = f'''# 可见最大 C 联合 v5：完整3056精确界与整个最优面不可达

Boss1；RUN `six-boss1-20261111`；profile `full`；实际 agent `/root/visible_joint_v5_solve`。

**已消费且仅消费1次完整LP；精确证书、完整面和本次真实来源排除均通过独立核验。原half仍OPEN。**

完整3056 raw／513非负列／2自由等式的必要系统精确最优值为

`{alpha}` ≈ **{float(alpha):.17g}**。

原1586行、全部零/重复行、30条rhs=−1、原正尺度、完整客户轴与独立K均保留。求解使用highs-ds、60秒、presolve=False、1e−9容差，61迭代成功。所有新行numerical divisor25与真实IC权分开保存；原付款逐条以−marginal/divisor恢复。

全部正raw索引为 `46,47,134,218,221,868,1803,2563,2564,2606`。完整零余量列有18个，面等式rank12，自由坐标 `z0,z15,z19,z23,z51,z75`；全部3056参数不等式与513非负条件保留并独立复核。K在整面固定为 `{K}`。

本次真实正C行1803与全脸C⊆O共同强制R3=R4=R5=C覆盖，故真实v3=v4=v5=K/5。真实正SAFE4/5取等要求N4=N5，而独立全列身份给出整面

`N5−N4=(1−K)/36={independent['N5_minus_N4']}` >0。

所以**整个最优面均不能由原完整有序历史纯SPE实现**。完整c=0弱零态及c=1,o=0的1011/1101替代态都保留；覆盖等号是在新零态、全脸C⊆O和正CAP之后推出，没有预置旧u2/K或真实v4/v5关系。N3差为正，实际矛盾来自SAFE4/5。

这给出必要系统精确最优值以及最优面不可达性，不给统一提升epsilon、不构造SPE、不证明half。没有第二LP、734/phaseI、固定K、支持限制、旧点补全或新增λ族输入。

完整正文与实际失败保存见 `visible_maximum_joint_v5_solve/proof.md`；原等待阶段摘要已保留在 `scaffold_summary_before_release.md` 与 `adjacent_summary_before_release.md`。最终来源核验、成果冻结及SHA见同目录 `final_source_verification.json`、`freeze_manifest.json`、`SHA256SUMS`。Git、RUN和登记仍由Main管理。
'''
    adjacent.write_text(summary)
    print(json.dumps({"status": "ACTUAL_V5_PROOF_WRITTEN_AFTER_ALL_EXACT_CHECKS", "objective": str(alpha),
                      "proof_sha256": digest(HERE / "proof.md"), "half_status": "OPEN", "optimizer_calls_in_writer": 0}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
