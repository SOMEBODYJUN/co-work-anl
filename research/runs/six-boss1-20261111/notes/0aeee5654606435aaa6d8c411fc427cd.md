# 同一 X 的第四源真实两尾：精确排除 universal 217 行点

Boss1；RUN `six-boss1-20261111`。冻结完成；只写本摘要及 `universal_true_x_tail/`。一次小型 phase-I 发现，之后全部标准库精确核验。

## 结果

释放的 13 正原子点 W=`0.4258960956295508…` **不能补成所指定四个真实强制 X 分支**。六条非负加权预算已经证明第四个分支单独不可补全。该点不是 SPE 反例；此结论不证明 half，也不排除旧必要系统整个最优面。

得到全 256 客户类型上普遍有效的必要切面：

\[
4096u_4+900u_5+1700F_X+71K-\sum_v m(v)z_v\ge0.
\]

其中 m(v) 是[证明正文式 (M)](universal_true_x_tail/proof.md)给出的真实第四源两个尾会员 y,t 的四态最小值。所有原子，包括当前零支持、o=0、全零客户型，均参与普遍定义和独立检查。

当前精确点违反该切面：

\[
-\frac{128742478797765148513379}{2572043380472564711298}
=-50.05455186922669\ldots.
\]

六项整数权依次为：第四源真改 X IC **4096**；MAX(Y) **800**；CAP(T) **71**；该真末节点 BR(Omean) **384**；该真末两位 PAIR(A6,Omean) **512**；actual RC(T,Omean) **900**。它们共用同一 X 和同一真实 T，未使用根最大标签的新加强行。

## 完整系统和验证

本轮使用 **780 μ 变量、52 质量式、608 原始不等式**：4 IC、84 SAFE、14 MAX、14 CAP、14 actual MX、42 真末位 BR、290 完整可见 PAIR、146 actual RC。只建本分支新尾之间的交叠；不同分支未知尾交叠未耦合。PAIR 包含真末标签本身和 Omean；Omean/Omean 确实由全 36 查询对付款并弱化为 o/36。

独立标准库 checker 不导入 builder，逐项重造 474240 矩阵项和 155648 原变量系数，重放原点 217 行。全类型消元核了 1024 个 source/type 最小值和 15360 尾态余项，全部非负；其中 14612 零、748 正。最终[输入检查](universal_true_x_tail/literal_input_check.json)与[证书检查](universal_true_x_tail/literal_certificate_check.json)均为 PASS。

phase-I 唯一浮点发现值为 `0.007401234935565079`；精确证书给共同放松量下界
`128742478797765148513379/17394729382135955142508374 > 0`。不依赖浮点最优性。

## 可接续接口

| 文件 | 用途 |
|---|---|
| [proof.md](universal_true_x_tail/proof.md) | 六条真钱包、全类型四态最小值、Farkas 符号与点上精确矛盾 |
| [derivation.md](universal_true_x_tail/derivation.md) | 优化前全部 608 行的语义推导 |
| [exact_input.json.gz](universal_true_x_tail/exact_input.json.gz) | 完整精确系统；SHA `367ab0932172ce10e459bdf390121d0a5ad825a1475b30e5bb5ae6105b797375` |
| [exact_certificate.json](universal_true_x_tail/exact_certificate.json) | 精确 Farkas 与全 256 cut；SHA `467d2b0f7415c8b51cce1aebe0a5784ece6da31822ce6630b767ab001883837e` |
| [universal_cut_256.tsv](universal_true_x_tail/universal_cut_256.tsv) | 全部 256 类型的原子切面系数 |
| [universal_minima.json.gz](universal_true_x_tail/universal_minima.json.gz) | 全 1024 最小值与全部极小尾态 |
| [universal_state_residuals.tsv.gz](universal_true_x_tail/universal_state_residuals.tsv.gz) | 全 15360 非负余项 |
| [check_literal.py](universal_true_x_tail/check_literal.py) | 确定性独立标准库字面检查 |
| [freeze_manifest.json](universal_true_x_tail/freeze_manifest.json) | 新包哈希、冻结状态与旧 75 文件不变记录 |

原释放输入 SHA `f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41`，原证书 SHA `ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85`；全部 75 个既有冻结来源字节不变。没有修改旧 16-hist 层、RUN、登记表或公共文件，没有追加优化调用。
