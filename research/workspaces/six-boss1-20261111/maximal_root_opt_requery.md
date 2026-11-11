# 真第三源重查最优菜单：精确排除旧根点及全型切面

Boss1；RUN `six-boss1-20261111`。只写本摘要与 `maximal_root_opt_requery/`；已完成根 C 与 X-tail 包不变。一次局部 phase-I 后，精确 Farkas 与全域矩区间投影均已完成。

## 结果

`maximal_root_tail_wallet/` 的 10 正原子精确点，不能补成指定的真 source3 最优菜单平均重查层。新的普遍必要切面是

\[
\boxed{126000v_3+65719v_4+4962v_6-\sum_{h\in\{0,1\}^7}m(h)w_h\ge0.}
\]

v3、v4、v6 是原真实根 C 分支自己的收益。m(h) 按[证明式 (PHI)/(ENV)](maximal_root_opt_requery/proof.md)，在全部 128 旧型上先分别最小化 q=0/1 的八个真尾态，再对允许的平均会员区间 `[o/6,o]` 取极小值。没有假设最优菜单不交叠。K 和 actual 根 u 两参数系数均为零。

在指定释放点，切面左端为

\[
-\frac{26828130879519777790818450922693961}
{16138758469380629653371589538760}
=-1662.341680769288\ldots<0.
\]

这是固定点不可补全与新普遍投影，不是 SPE 反例、最锐全局根线、整个旧最优面排除或 half。

## 承重机制

在真历史 `(C,B2)` 对六个真实合法 Q_k 分别改选，保留 q 及同一次偏离的三个后继 R4_k,R5_k,R6_k。ν 已经是外层六分支平均；其 q 矩满足 `o*w/6≤Σqν≤o*w`。

九个真预算的整数权是：source3 平均 IC **126000**；旧 source4 对 R4/R5/R6 的 SAFE **43、31218、34458**；旧 source6 对三个新尾的 SAFE 各 **1654**；新真末位 SAFE(Omean) **5400**；新真末两位 full36 PAIR(Omean,Omean) **7740**。同一新尾在新终端钱包和旧 source 的合法查询中共用会员，体现真实跨分支约束。

全型 envelope 给 `a1−a0≥113681/4>0`，所以本证书的 upper 矩权恰全零、lower 矩权全正；这是在完整区间上优化后的结果，不是提前施加菜单分割。重叠只会增大这个加权列的下界。

## 系统、验证与接口

160 个 ν、10 条质量式、121 条真预算加 20 条矩界，共 141 原始不等式，零行与 15 个固定点仿射重复全保留。全域检查扩展至 **128 型、2048 状态**，所有余项非负：290 零、1758 正。独立标准库重建 22560 个矩阵项、全部全型投影及 K/u 参数列；原冻结 71 行和 22 个旧来源文件均核验不变。

| 文件 | 内容 |
|---|---|
| [proof.md](maximal_root_opt_requery/proof.md) | 九预算、显式 Φ、完整矩区间 Farkas 恒等式、固定点矛盾 |
| [derivation.md](maximal_root_opt_requery/derivation.md) | 优化前全部 121 真预算和双层查询平均来源 |
| [exact_input.json](maximal_root_opt_requery/exact_input.json) | 141×160 固定系统；SHA `55395a9c4e3c04015d9407c30e22657851c4c9cabc4f4a386ea7dfd9bb02f370` |
| [exact_certificate.json](maximal_root_opt_requery/exact_certificate.json) | 精确 Farkas 与全128切面；SHA `209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e` |
| [universal_cut_128.tsv](maximal_root_opt_requery/universal_cut_128.tsv) | 可接回旧 root128 系统的完整原子系数 |
| [universal_moment_envelope.json](maximal_root_opt_requery/universal_moment_envelope.json) | 全128 a0/a1/m 与扩展矩权、全部极小态 |
| [all_2048_state_residuals.tsv](maximal_root_opt_requery/all_2048_state_residuals.tsv) | 全新状态非负余项 |
| [check_literal.py](maximal_root_opt_requery/check_literal.py) | 不导入 builder 的独立标准库字面检查 |
| [literal_certificate_check.json](maximal_root_opt_requery/literal_certificate_check.json) | 全型 PASS 与精确正 phase-I 下界 |
| [freeze_manifest.json](maximal_root_opt_requery/freeze_manifest.json) | 最终冻结和新包哈希 |

唯一数值 phase-I 为 `0.0031481172772961164`，其精确恢复对偶给严格正下界；未声称已配对恢复 phase-I 精确最优解。未进行第二次 LP，未重优化旧点，未改 Git、RUN、登记表或旧冻结包。后续根线合账须等 Main 的独立释放。
