#!/usr/bin/env python3
"""Write the actual-result proof and preserve the previous waiting-stage summary."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = HERE.parent
read = lambda name: json.loads((HERE / name).read_text())
sha = lambda path: sha256(path.read_bytes()).hexdigest()
cert = read("exact_certificate.json")
face = read("optimal_face.json")
diagnostic = read("true_branch_equality_diagnostic.json")
checked = read("independent_check_result.json")
functionals = read("true_branch_face_functionals.json")
changes = read("positive_payment_changes.json")
discovery = read("discovery_output.json")
values = {entry["name"]: F(entry["value"]) for entry in functionals["functionals"]}
assert checked["status"] == "PASS_FULL1586_RAW_FRACTION_VERIFICATION"
assert diagnostic["status"] == "WHOLE1586_OPTIMAL_FACE_EXCLUDED_BY_TRUE_C_INTERMEDIATE_SAFE"
assert cert["optimizer_calls"] == 1 and discovery["optimizer_calls"] == 1
alpha = F(cert["objective"])
D = F(117930501880516132220686794356653888579401900821412887)
assert alpha.denominator == 4 * D
positive_table = [
    r"| raw 索引 | 原始行 | 原尺度付款 \(D y_i\) | 正数值除数 |",
    "|---:|---|---:|---:|",
]
for row in cert["dual"]["positive_raw_rows"]:
    positive_table.append(
        "| " + str(row["index"]) + " | " + row["name"] + " | "
        + str(D * F(row["weight"])) + " | " + row["prepared_positive_divisor"] + " |")
zero_table = [
    "| p | c | o | s=0 的全部零态 | s=9 的全部零态 | 同一 C 历史的交集 |",
    "|---:|---:|---:|---|---|---|",
]
lookup = {(entry["s"], entry["p"], entry["c"], entry["o"]): entry["all_zero_tails"]
          for entry in diagnostic["all16_endpoint_minimum_tables"]}
tailstr = lambda tails: "、".join("".join(map(str, tail)) for tail in tails)
for entry in diagnostic["all8_common_zero_tables"]:
    p, c, o = (entry[key] for key in ["p", "c", "o"])
    zero_table.append("| " + " | ".join([
        str(p), str(c), str(o), tailstr(lookup[(0, p, c, o)]),
        tailstr(lookup[(9, p, c, o)]), tailstr(entry["all_common_zero_tails"]),
    ]) + " |")
gap_table = [
    r"| 真内部源 j | 整个面的 \(K/5-N_j\) | 近似值 |",
    "|---:|---:|---:|",
]
for j in [3, 4, 5]:
    value = values["K_over5_minus_N" + str(j)]
    gap_table.append("| " + str(j) + " | " + str(value) + " | " + format(float(value), ".17g") + " |")

proof = r"""# 可见真最大 C 联合 v4：1586 行精确最优与整个最优面的真源排除

Boss1；RUN six-boss1-20261111。Main 对准确输入明确释放的一次 LP 已完成，**本轮优化器调用恰为 1 次**。精确恢复、独立 Fraction 核验、完整面消元和真实付款诊断均未新增优化调用。

## 1. 普遍福利界与准确范围

采用原有限单位客户、有限非空共同标签目录、恰六人完整有序历史纯 SPE 模型。空覆盖、同覆盖异标签、重复行动、六查询重复和全部弱离轨平局均保留。实际行动为 A1…A6；X 只在原实际前四背景上承担已证明的共同势最大性；C 是全目录裸大小最大标签，\(|C|=K\)。O 是六个最优合法标签的覆盖并，不作为一个合成合法行动。

令
\[
D=117930501880516132220686794356653888579401900821412887,
\]
\[
\boxed{\alpha_4=
\frac{208101173892952666162424962783956947305005629564084333}{4D}
\approx __ALPHA_DEC__.}
\]
则对每个原模型的完整纯 SPE，
\[
\boxed{W\ge\alpha_4\,\mathrm{OPT}_6.}
\]
这是冻结 **1586 raw／513 非负列／2 等式** 必要锥的精确最优值。相对上一个实际求解并认证的 1003 行系统，提升约 **__IMPROVEMENT__**。1050 行中间输入保持未求解，不能为它附会一个数值最优值。

当 \(\mathrm{OPT}_6>0\) 时，任何完整纯 SPE 都不能等号达到本值：第 5 节以实际正付款的固定 C 真分支排除整个最优面。此非达到结论不自动给出统一的 \(\alpha_4+\varepsilon\) 界，也没有构造 SPE 反例。**原六人半覆盖命题仍 OPEN。**

## 2. 冻结输入、来源及唯一数值发现

唯一输入为 [visible_maximum_joint_v4/exact_input.json](../visible_maximum_joint_v4/exact_input.json)，SHA256：

    fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839

准备 manifest SHA：

    21da98ff5b72702363824200e25320fc7d510633be48d91de6e2eea5e708c337

Main 实际授权文件 SHA：

    3c70842209dc14c79d040126a536f09cd89b9675399df81fe3c28c8bf577263e

Main 已亲验完整来源与全部系数；本席亦读完 [准备来源说明](../visible_maximum_joint_v4/source_review.md) 和 [新 536 行完整源证明](../all_source_joint_reweighted_safe/proof.md)。新族在实际源 i=1,2,3,4、任意纯合法 T 上联合支付同分支真实内部 SAFE，并允许源 IC 权 \(a=25+\Theta-s\) 重配。它保留真实分母 \(\min(p+6-i+1,5)\)，没有把第三、第四源的 H 擅自改为 \(|T|/5\)。

输入逐字保留 1050 个上游 raw 行，再追加 536 行。每个新增 source weight a 可以不同，但所有新增数值正除数仍为 25。原始 K 列、原等式、所有零行/重复行、30 个非零仿射 rhs 均完整保留。准备者的字面结果真实字段为 status=PREPARED_NO_OPTIMIZER、result=PASS_INDEPENDENT_LITERAL_PREPARATION_CHECK；未为了门禁改写原输出。

本轮先核准全部 258 个实际来源指纹和 Main 两份 PASS 证据，再由未修改的 solve_once.py 建立排他消费记录，之后进入唯一 highs-ds 调用。全矩阵为 1586×513；presolve=False；时限 60 秒；无固定 K、支持限制、旧点补全或 phase I。

唯一调用成功，用 65 次迭代得到数值目标 0.44115214167365147。实际输出、全部 marginal、余量、选项、源指纹及消费标记均原样保存。只利用这一次返回做后续精确线性代数，没有第二次调用。

## 3. 全行、全列、原尺度精确证书

写原系统为 \(Az\ge b,\ Ez=h,\ z\ge0\)。证书给出完整 513 维有理 primal z、完整 1586 维原尺度付款 y、两条自由等式付款 \(\eta\)，以及
\[
y\ge0,\quad \eta\in\mathbb Q^2,\quad
r=c-A^Ty-E^T\eta\ge0.
\]
精确核验了
\[
Az-b\ge0,\quad Ez=h,\quad
c^Tz=b^Ty+h^T\eta=\alpha_4,
\]
\[
y_i(A_iz-b_i)=0\quad(\text{全部 1586 行}),\qquad
r_jz_j=0\quad(\text{全部 513 列}).
\]
恢复只对本次返回的支持做有理线性代数；primal 和 dual 的恢复秩均为 13。独立 verify_certificate.py 使用标准库 Fraction，未导入恢复或面分析代码，再次直接逐原行、原列和仿射 rhs 核验一致。

数值层完整原行除以正 \(d_i\)，所以原付款是
\[
y_i=-\mathrm{SciPyMarginal}_i/d_i.
\]
原尺度证书直接使用 raw 系数，不把新行真实源 IC 权错当成数值除数。两自由等式乘子为
\[
\eta_O=\alpha_4,\qquad
\eta_C=\frac{180180368270326387558572238935294718493799710275007365}{54D}.
\]
此次全部正付款行的 rhs 恰好为零，因而 \(b^Ty=0\)；原有 rhs=−1 的仿射上帽仍全部参加 primal 检查和一般恒等式，不因零付款而删行。

__POSITIVE_TABLE__

其余 1575 条 raw 权为零。相对上一实际求解的 1003 系统，进入付款的是 raw134、1018、1433、1438、1439；退出的是 raw65、640、647、654、673、1002；保留的是 raw46、47、218、221、222、868。完整精确变化见 [positive_payment_changes.json](positive_payment_changes.json)。

全部 513 列给出
\[
\boxed{W-\alpha_4 O
=\sum_i y_iR_i+\eta_C(|C|-K)+\sum_{j=0}^{512}r_jz_j.}
\]
真实 \(|C|=K\) 支付自由等式；其余项非负，证明普遍界。O=0 时直接使用 W≥0。匹配有理 primal 只证明必要锥锐性，放大为整数质量也不提供完整策略实现。

## 4. 完整最优面而非代表点支持

零对偶余量列为
\[
\{0,2,3,10,11,14,15,18,19,22,23,50,51,74,75,331,459,483,499,512\}.
\]
全部 20 列保留，包括返回点上为零的列。11 条正 raw 行加两等式在这些列上的秩为 13，使用
\[
(z_0,z_{11},z_{15},z_{19},z_{23},z_{51},z_{75})
\]
作七个自由仿射参数。完整 [optimal_face.json](optimal_face.json) 保存每个允许坐标的仿射表达式、全部 1586 条原始不等式和所有坐标非负条件；其中 __NONCONSTANT__ 条 raw 限制在参数上非恒定。没有把整个七参数仿射空间都称为可行，也没有只检查返回点支持。

整个面上
\[
K=\frac{43726392048803656492555751030930610959547200783028231}{2D}
\approx __K_DEC__<1,
\qquad u_2=K/5.
\]
后一个身份也可直接逐列写成
\[
\boxed{u_2-K/5
=\frac{R_{1433}-R_{1018}}9+\frac5{18}(|C|-K).}
\]
这是有符号身份，只在两条正付款行取等和 C 大小等式上给出结论，未把相减后的表达当成新的普遍非负预算。

为审查原真实源定义，所有固定量另给出完整 513 列有符号身份：先用正行/两等式，再以强制零列的有符号系数补齐。结果见 [true_branch_face_functionals.json](true_branch_face_functionals.json)。

## 5. 同一真实 C 历史排除整个面

### 5.1 两条实际正 C 预算及原尺度路由

这两条行都在原实际历史 \((A_1)\) 强制**同一个合法标签 C**，继而按同一给定完整 SPE 得到 \(R_3,R_4,R_5,R_6\)。它们的中间 SAFE 权共同为
\[
(\theta_3,\theta_4,\theta_5)
=\left(\frac{12425}{31104},\frac{175}{432},\frac5{12}\right)>0.
\]
raw1433 是 s=0 的一般 T=C 原行，源 IC 权 \(a_0=815585/31104\)。raw1018 是 s=9 的已消去 C 大小等式版本，源 IC 权 \(a_9=535649/31104\)。其对应的一般原行 raw1441 满足
\[
\boxed{R_{1441}=R_{1018}-\frac7{10}(|C|-K).}
\]
该路由与前节源收益身份都独立核了全部 513 列。于是任意真实锥最优投影使 s=0 和 s=9 两条真实预算同时为零。

每条预算均是正源 IC、三个正中间大小帽、正末帽、同末节点六查询 BR 均值、三个正内部 SAFE 均值、菜单弱化非负差以及逐客户最小余项之和。所有后继和内部源收益来自这个同一强制 C 历史。内部真偏离使用该偏离历史自己的后继，未冻结外层 R 作为替代策略。

### 5.2 全部弱零态，先保留再取同历史交集

置 p=a1、c 为 C 会员，四位尾依次 r3r4r5r6。直接重算两端点全部 256 个局部状态，并逐一比对冻结源表的 16 个完整最小值/全部达到态；又直接核了 8192 个六菜单位弱化差。没有删掉 s=9 在 p0c1 的 1110，也没有删掉 s=0 在 p1c1 的 1111。

__ZERO_TABLE__

每个端点各有 15 个零态；同一历史的交集有全部 13 个零态。c0o1 的 0010、0100、1000 单中间弱态都保留在列表中。全状态、源表比对和准确成本见 [true_branch_equality_diagnostic.json](true_branch_equality_diagnostic.json)。

在交集的每个 C 客户上，三个中间会员均为 1；p=0 的尾为 1111、p=1 的尾为 1110，故该客户的最终负载恰为 5。由于两预算的中间 CAP 付款都严格正，取等还要求每个中间标签大小为 K。它们已经覆盖全部大小 K 的 C，于是
\[
\operatorname{cov}(R_3)=\operatorname{cov}(R_4)
=\operatorname{cov}(R_5)=\operatorname{cov}(C).
\]
这里只推出覆盖相等，不把不同标签认同。c0o1 的单中间弱态因此被这些真实大小帽取等排除；它们没有在局部枚举或数值模型中被先行删除。

于是同一分支上
\[
v_2=v_3=v_4=v_5=K/5.
\]
原真实源 IC 取等给出 actual \(u_2=v_2\)，与全行直接身份一致。末标签 R6 的缺失/补充仍按真实零态保留，未擅自认定其覆盖也是 C。

### 5.3 真正内部 SAFE 的完整面矛盾

固定上述覆盖关系后，在真正内部第 j 源，其六查询 SAFE 的合法弱均值成本为
\[
N_j=\sum_h\frac{o_hw_h}{6[a_{1,h}+(j-2)c_h+7-j]},
\qquad j=3,4,5.
\]
它来自各真实查询自己的续局，故 \(v_j\ge N_j\)。上段已给出 \(v_j=K/5\)，所以任何可实现最优点必须同时满足 \(K/5-N_j\ge0\)。

然而整个必要锥最优面上三个量均为固定负数：

__GAP_TABLE__

每一项均有完整 513 列的精确有符号面身份。第三源一项已经严格矛盾，故**整个最优面均不能由原模型完整有序历史纯 SPE 实现**，并非只排除了一个返回点。

另一个同枝读法也验证了该矛盾：仅 s=9 正预算的每个 C 零态就已经让三个中间都覆盖 C，正 CAP 使三者覆盖恰 C，于是 v3=v5。正 \(\theta_3,\theta_5\) 的真实六查询 SAFE 同时取等，其查询成本差为
\[
\sum_x\frac{d_x(1-c_x)}{3(a_{1,x}+2)(a_{1,x}+4)}.
\]
每个 O 中客户有 d≥1，故该差为零迫使 \(O\subseteq C\)。整个面却有
\[
|O\setminus C|=1-K
=\frac{192134611712228607948817837682377166199256600859797543}{2D}>0.
\]
这同样只用已冻结的真实预算，未使用尚未释放的新菜单族。

## 6. 其他廉价诊断和边界

已知 ROOT270 加强余项
\[
R_{868}\ge\eta\,|C\setminus O|,\qquad
\eta=\frac{1087978231314917}{84387869309613600}
\]
在原根证书全部 128 客户余量上重新核验；32 个 C 在 O 外类型的最小余量恰为 η，扣除后全部非负。本轮整个面上的两边均为零，所以它不再分离此面，且没有追加到输入。

旧 P25(C,Omean) 与旧 NS5 的全脸松弛分别为 __P25_SLACK__ 和 __NS5_SLACK__；均严格正。本轮没有沿用它们的旧取等排除。

没有调用 734 固定 C 模板，没有 phase I，没有使用未冻结 ordered-menu 行，没有更改输入、尺度或任何旧结果。正付款 A5/A6 行的真实参数也完整保留于精确证书，当前整个面已有上述更直接 C 分支矛盾，无需进一步构造完成树或重复可行性求解。

## 7. 产物、初始骨架与最终冻结

[exact_certificate.json](exact_certificate.json) 给出全部有理向量；[all1586_raw_row_checks.json](all1586_raw_row_checks.json) 和 [all513_column_checks.json](all513_column_checks.json) 逐项保存余量和互补积。[independent_check_result.json](independent_check_result.json) 是独立 Fraction 重算记录。[optimal_face.json](optimal_face.json)、[true_branch_face_functionals.json](true_branch_face_functionals.json) 及 [true_branch_equality_diagnostic.json](true_branch_equality_diagnostic.json) 给出整个面的精确描述与源排除。

初始 source_review.md、scaffold_manifest.json 和 SCAFFOLD_SHA256SUMS 保留为未授权准备阶段的原字节记录。相邻摘要更新为本轮实际结果前，其初始字节另存 scaffold_summary_before_release.md；scaffold_snapshot_recheck.json 明确核对这一个摘要的历史路径映射，其余骨架程序原字节不变。初始骨架清单不是当前最终证书清单。

最终实际输入、全部源 pins、授权、消费记录、唯一数值返回、原尺度证书、全脸与诊断由 freeze_manifest.json 和最终 SHA256SUMS 冻结。完整必要锥最优性和真实 SPE 的不可达到性严格区分；原六人 half 仍 OPEN。
"""
proof = proof.replace("__ALPHA_DEC__", format(float(alpha), ".17g"))
proof = proof.replace("__IMPROVEMENT__", format(changes["objective_improvement_decimal"], ".17g"))
proof = proof.replace("__POSITIVE_TABLE__", "\n".join(positive_table))
proof = proof.replace("__ZERO_TABLE__", "\n".join(zero_table))
proof = proof.replace("__GAP_TABLE__", "\n".join(gap_table))
proof = proof.replace("__NONCONSTANT__", str(sum(
    any(F(value) for value in row["parameter_coefficients"])
    for row in face["all1586_raw_inequality_restrictions"])))
proof = proof.replace("__K_DEC__", format(float(values["K"]), ".17g"))
proof = proof.replace("__P25_SLACK__", str(values["raw_slack_927"]))
proof = proof.replace("__NS5_SLACK__", str(values["raw_slack_1002"]))
assert values["raw_slack_927"] > 0 and values["raw_slack_1002"] > 0
assert "__" not in proof
with (HERE / "proof.md").open("x") as output:
    output.write(proof.lstrip())

adjacent = HERE.with_suffix(".md")
scaffold = read("scaffold_manifest.json")
adjacent_key = str(adjacent.relative_to(REPO))
assert sha(adjacent) == scaffold["artifact_sha256"][adjacent_key]
backup = HERE / "scaffold_summary_before_release.md"
with backup.open("xb") as output:
    output.write(adjacent.read_bytes())
summary = r"""# 可见真最大 C 联合 v4：精确界与整个最优面排除

Boss1；RUN six-boss1-20261111。Main 明确释放的唯一 1586 行 LP 已完成，实际优化调用 **1 次**；后续精确恢复、独立核验、全脸及真实源诊断均为 **0 新优化**。

\[
\boxed{W\ge\alpha_4\mathrm{OPT}_6,\qquad
\alpha_4=\frac{208101173892952666162424962783956947305005629564084333}
{471722007522064528882747177426615554317607603285651548}
\approx0.4411521416736506.}
\]

完整 **1586 raw／513 非负列／2 等式** 必要锥的原始与原尺度对偶准确匹配。相对上一个实际求解的 1003 行系统提高约 0.0008119780473412091；1050 中间输入未求解。完整保留所有零/重复原行、全 512 客户类型、独立 K、仿射 rhs 和两条自由等式付款。

## 精确最优面及真源排除

正付款共 11 条：46、47、134、218、221、222、868、1018、1433、1438、1439。后四条具有实际 source IC 权，数值除数仍为 25。

整个最优面保留 20 个零对偶余量列，正行加两等式的秩为 13，自由列为 0、11、15、19、23、51、75；全部 1586 原始不等式和坐标非负条件均保存。

两条正 C 预算使用同一个真实历史 (A1,C,R3,R4,R5,R6)，共同内部权为
\[
(\theta_3,\theta_4,\theta_5)
=(12425/31104,\ 175/432,\ 5/12),
\]
分别 s=0、s=9。全部端点弱零态先保留，再在同一历史取交；正中间大小帽迫使 R3、R4、R5 覆盖恰 C，交集源份额为 c/5。因此这三个真正内部源收益均为 K/5。

但它们的真实菜单 SAFE 在整个面上的差 K/5−N3、K/5−N4、K/5−N5 均为固定负数，近似为 −0.002172959、−0.013486980、−0.036115021。每项均有全 513 列精确有符号身份。**整个最优面都不可由原模型完整纯 SPE 实现。**

全部 256 个端点局部态、30 个端点零态及 13 个共同零态保留；另核 8192 个菜单差。s=9 的 p0c1/1110、s=0 的 p1c1/1111 和 c0o1 的三个单中间弱态均没有被预先删除。没有固定 C 734 绑定、phase I、未冻菜单行或新输入行。

## 交付

- [完整证明](visible_maximum_joint_v4_solve/proof.md)
- [完整精确证书](visible_maximum_joint_v4_solve/exact_certificate.json)
- [独立全域核验](visible_maximum_joint_v4_solve/independent_check_result.json)
- [完整最优面](visible_maximum_joint_v4_solve/optimal_face.json)
- [全列固定量身份](visible_maximum_joint_v4_solve/true_branch_face_functionals.json)
- [真实 C 分支排除](visible_maximum_joint_v4_solve/true_branch_equality_diagnostic.json)

初始等待骨架的摘要字节另存 scaffold_summary_before_release.md，原骨架 manifest 保留为历史记录；最终证书使用本目录最终 freeze_manifest.json 和 SHA256SUMS。

这确立必要锥的准确最优值及真实 SPE 不可等号达到性，没有给出统一更大的 epsilon，也没有证明原六人半覆盖；原题仍 **OPEN**。
"""
adjacent.write_text(summary.lstrip())
snapshot_checks = {}
for relative, expected in scaffold["artifact_sha256"].items():
    current = backup if relative == adjacent_key else REPO / relative
    assert sha(current) == expected, relative
    snapshot_checks[relative] = {
        "sha256": expected,
        "actual_snapshot_location": str(current.relative_to(REPO)),
        "history_snapshot_preserved": True,
    }
with (HERE / "scaffold_snapshot_recheck.json").open("x") as output:
    output.write(json.dumps({
        "status": "PASS_ORIGINAL_WAITING_SCAFFOLD_SNAPSHOT",
        "original_scaffold_manifest_sha256": sha(HERE / "scaffold_manifest.json"),
        "only_summary_path_relocated_for_historical_readback": adjacent_key,
        "original_snapshot_checks": snapshot_checks,
        "all_core_scaffold_code_unchanged": True,
        "reason": "The adjacent summary now reports the actual released result; its old waiting-stage bytes are preserved exactly.",
        "optimizer_calls": 0,
    }, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({
    "status": "ACTUAL_PROOF_AND_SUMMARY_WRITTEN",
    "proof_sha256": sha(HERE / "proof.md"), "summary_sha256": sha(adjacent),
    "original_scaffold_snapshot_checks": len(snapshot_checks),
    "optimizer_calls": 0,
}, indent=2))
