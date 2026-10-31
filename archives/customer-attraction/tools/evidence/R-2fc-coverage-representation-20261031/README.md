# R-2fc coverage-representation 六源复核（Boss2，2026-10-31）

本证据包对应 Boss2 认领的六个冻结源版本，全部通过 `python3 co-work-anl/work.py clean show <ID> --out ...` 导出后逐字节读取。两个冻结来源 `legacy-cleanup`（`68fad804ec5946cb296f77dc5b336308a66abf12`）与 `main`（`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`）对每个路径给出同一源版本；以下 SHA-256 为实际导出字节。

| ID | 实际对象 | 大小 | SHA-256 | 处置与正文归属 |
|---|---|---:|---|---|
| `237a9c14a68cbe08a526` | `audit_coverage_geometry.py` | 11506 B | `6a750484993f99a3893bc63306c50cce9c59400370bdbeea430194b39085db6a` | **integrated**：有限空间秩、正势展开、策略秩、极射线、不交 SPE、末层方向障碍、五组稀疏化；归入既有 `state/计算/覆盖矩表示与非负实现的精确核验--计算.md`、`state/定理/固定人数完整策略的覆盖矩表示--定理.md`、`state/定理/覆盖矩锥极射线与自适应类型稀疏化--定理.md`、`state/障碍/精确保留激励数值的折叠与末层方向边界--障碍.md`。 |
| `3bcc00f6fc8a8ac6756c` | `audit_positive_moment_locality.py` | 5238 B | `f12d1fc0f9184ee597b12b3957b104ff8b519b35e8ee8e75f74e0561b14fe568` | **integrated**：PM-1/PM-2/PM-3 的有限 r=1..6 精确回归；归入 `state/障碍/覆盖矩锚预算与真子目录的全局缺口--障碍.md` 与 `state/资源/边际势预算与全局正矩原稿的精确证据层次--资源.md`。 |
| `10b27e972bf58a53c84e` | `coverage_geometry_audit.json` | 13248 B | `082fd97754bf5928ec971677054f49fe89975454a0e07e15cc4fd92a0cd655d6` | **integrated**：是几何脚本的冻结计算结果；保留原字节并与新回放逐字节比较。 |
| `ae25ad82555f3e1b6d27` | `positive_moment_locality_audit.json` | 3779 B | `3d82206e629fc5256bb91a1ddc1a08b6f64da666a269ce121b4894f5722f08a8` | **integrated**：是正矩局部性脚本的冻结计算结果；不把假全局矩当合法 CAG 输入。 |
| `b1ce857888be2dae3928` | `root_independent_audit.json` | 4654 B | `a932d3a123ed5a30c2954b506b7d82dbd6e50d5ffe58ce5621abb1b246a721da` | **integrated**：独立有限秩/暴露检查结果；归入同一 `state/计算` 对象和两个覆盖矩定理。 |
| `02ff2fdb8846b201e378` | `root_independent_audit.py` | 4905 B | `a1212f6dff9d1f847e37d53635c1ca3ca55de12b287186aa6619b3ada7ecc5c3` | **integrated**：无求解器的独立标准库 `Fraction` 秩/暴露核验；原字节保存在 clean-show/replay。 |

“integrated”表示数学内容已经并入准确的既有定理、障碍、资源或计算对象；六个原始字节、回放副本和 stdout/stderr 均**retained** 于本证据目录。没有发现同一内容可直接丢弃的多余源版本，故无 `duplicate` 处置。

## 读取与运行记录

- `clean-show/`：六个 `clean show` 导出原件，文件名保留源 ID；每个文件均与冻结 inventory 的大小和 SHA-256 相同。`*.show.stdout.txt`、`*.show.stderr.txt` 和 `show-execution.json` 保留了 clean-show 自身的 stdout/stderr、退出码与摘要字节。
- `replay/execution.json`：三份工作区脚本的命令、隔离 cwd、退出码、stdout/stderr 字节数与 SHA-256，以及生成报告对冻结 JSON 的逐字节比较。
- `replay/237a9c14a68cbe08a526/`：几何脚本。Python 3.12.14、标准库 `Fraction`，退出 0，stdout 340 B，stderr 0 B；22 空间组、56 份固定种子完整形式策略、p≤7 的 21343 个暴露类型对、稀疏支持 `[4,15,15,24,7]`；生成 13248 B 报告与 `10b27e972bf58a53c84e` 逐字节相同。
- `replay/3bcc00f6fc8a8ac6756c/`：正矩脚本。退出 0，stdout 287 B，stderr 0 B；r=1..6、21834 个非空形式类型、502 个局部单/双矩；生成 3779 B 报告与 `ae25ad82555f3e1b6d27` 逐字节相同。
- `replay/02ff2fdb8846b201e378/`：根独立脚本。退出 0，stdout 75 B，stderr 0 B；20 个秩案例、p≤8 的 86368 个暴露类型对、m=1 例外；生成 4654 B 报告与 `b1ce857888be2dae3928` 逐字节相同。
- `replay/report-verifier/`：本批辅助核验器只检查报告结构、有限计数及三份报告的逐字节一致性，`status=pass`，不承担普遍定理。
- `replay/related-ledger-verifier/`：既有 `coverage-moment-and-potential-ledger-primary/new-definition-check/verify_two_boundaries.py` 与其精确输入的一次复跑，退出 0、stdout 118462 B、stderr 0 B。它核验扩大 DR 势与 11 单位客户定义边界（168 monotonicity、252 DR、258 全历史激励、21 静态背景），只作为相邻 ledger 的 verifier，不能改名为 CAG half 证据。

## 逐源数学阅读与边界

`audit_coverage_geometry.py` 的对象是固定人数 m、有限标签 p 上的覆盖行 k_T、终局收益行 F_{q,a}、调和势 Φ_q、完整有序历史策略的真实比较行。代码逐项实现并检查：

1. 覆盖、收益、势三类行的秩均为 d=Σ_{j≤min(m,p)} C(p,j)，末层比较差为 (d-1)，加根覆盖恢复 (d)。这只是有符号线性空间核验，不能把负系数的 signed span 当成非负 SPE 乘子锥。
2. 调和势的覆盖展开系数逐项为正，并核验 F_{r+e_a,a}=Φ_{r+e_a}−Φ_r。它支持 `CR-1/CR-2` 的有限版本，但不构造一般 λ≥0 的支付证书。
3. p≤7 的暴露泛函检查逐类型验证 |C∖B|+|C∩B|(|B|−|C∩B|)≥0，唯一零列为 C=B；m=1、p=1 边界分别保留。`root_independent_audit.py` 的 p≤8 检查同样只是独立有限回归。
4. 不交单客户主题的指定策略在 m=1..4 的有限节点中是完整纯 SPE 且 W=OPT=m。把客户折成全兴趣类型会保留不等式真值但改变真实比较数值并产生重复覆盖标签；这正是“精确保留数值”与“仅保留 SPE 不等式”的合同区分。
5. 仅末层策略的有限障碍在 m=2,3,4 中末层比较全非负、全树最小比较为 −1、W=1, OPT=m，且 `is_SPE=false`；m≥3 的 half 失败属于非 SPE 放松，不是主问题反例。
6. 五组有理/整数支持做核消元并清分母，支持自适应至多 d 类的有限实例归约；不提供固定全局非负生成器，也不限制 p 或整数重数。

`audit_positive_moment_locality.py` 的对象是 m=2 的单/双覆盖矩。每个 r 的锚预算在所有非空形式客户列上非负；删任一变量或锚点的最大真子目录由显式有理客户模型实现；同一矩在全目录上使锚预算为负。因而“每个真子目录可实现”不能替代“全目录属于共同客户锥”。假全局矩不是合法 CAG 客户资料，也不是 SPE/half 反例。

相关正文已全文回读：`coverage_moment_geometry.md`、`positive_moment_locality.md`、`aggregate_security/dr_boundary.md`、`global_proof/harmonic_potential_obstruction.md`、`CLAIMS.md`、`FAILED_ROUTES.md`、`RESEARCH_STATE.md` 与已有 `coverage_representation_independent_review.md`；正式对象为覆盖矩表示定理、非负锥/稀疏化定理、精确保留激励数值与末层方向障碍、覆盖矩锚预算障碍和势支付资源。它们共同保留以下缺口：全树真实比较的非负乘子方向、共同客户锥 K_m 的全局非负余项、一般六人 half 仍 OPEN。有限秩或局部矩回归均未被升格为全局 half。

本批没有新建重复数学对象，也没有把旧图、有限扫描或扩大 DR 模型跨模型挪作 CAG 结论。
