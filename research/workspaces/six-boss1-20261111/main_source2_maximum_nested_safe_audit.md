# 第二源最大 C 分支的内部第五源 SAFE：独立普遍来源与精确系数审计

Boss1；RUN `six-boss1-20261111`。独立审计者：`early_shared_x_source_audit`。

**结论：PASS，无待修正项。** Main 提出的新行

\[
\boxed{300u_2+K\ge288B+12M+5N}
\tag{NS5}
\]

是原完整有序历史纯 SPE 模型的普遍必要式，不要求旧 P25 取等。这里 C 是全共同目录中真正达到最大裸大小 K 的合法标签，\(u_2\) 是原实际第二源收益，\(p=\mathbf1_{A_1}\)、\(c=\mathbf1_C\)、\(o=\mathbf1_O\)，并且

\[
B=\sum_x\frac{c_x}{p_x+5},\qquad M=\sum_x\frac{o_x}{6(p_x+4c_x+1)},\qquad N=\sum_x\frac{o_x}{6(p_x+3c_x+2)}.
\]

O 可以是任意六个真实合法查询标签的覆盖并。它不需要最优，也不需要作为一个合法行动存在。X 在这条行的来源中没有作用，其会员位仍在完整输入列中保留。

独立核验覆盖全部 128 个隐藏态、8 个精确最小值、4096 个实际六索引菜单位情况和完整 513 列原始系数。原始支付中的 C 大小自由等式乘子准确为 **+29**。新行在已冻结 1002 行必要锥的整个最优面上固定为

\[
\boxed{-\frac{15981204499895866953854050884598865236619}
{86426960107246755980438461555855802597096}<0.}
\tag{FACE}
\]

该固定值另有完整 513 列面身份。本包没有调用优化器，没有向旧输入加入任何行，也不声称新的全局 LP 最优值或新的数值普遍福利系数。

## 1. 冻结对象与重放方式

| 被审对象 | SHA-256 |
|---|---|
| [Main 普遍来源证明](main_source2_maximum_nested_safe/proof.md) | `1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067` |
| [Main 冻结清单](main_source2_maximum_nested_safe/manifest.json) | `3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269` |
| [Main 精确摘要](main_source2_maximum_nested_safe/exact_certificate.json) | `97694ec0496d52b428fe6a9cfee7030944312709a11de8a67b201bd724e751ac` |
| [全 513 列新增行](main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json) | `a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba` |
| [128 隐藏态表](main_source2_maximum_nested_safe/hidden_state_checks.json) | `f376eeb57404bdcd07fc42b6e72e23ecc30c2ed830cba42f1b6e43b77bfdc782` |
| [8 型最小值表](main_source2_maximum_nested_safe/minimum_table.json) | `140badf8d40d7e7c6a1c544bac7f55f8087a13c3f581a0244af9e6e4ce3a066a` |

可从仓库根目录运行新的独立标准库检查器：

```bash
python research/workspaces/six-boss1-20261111/main_source2_maximum_nested_safe_audit/check_exact.py
```

本包文件为 [check_exact.py](main_source2_maximum_nested_safe_audit/check_exact.py)、[audit_result.json](main_source2_maximum_nested_safe_audit/audit_result.json)、[independent_residuals.json](main_source2_maximum_nested_safe_audit/independent_residuals.json) 和 [face_violation_certificate.json](main_source2_maximum_nested_safe_audit/face_violation_certificate.json)。程序从字面真实份额和索引平均重新构造成本；没有执行或导入 Main、builder、solver 或旧审计的代码。

## 2. 同一真实分支和七项非负预算

按[原模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)，固定任一完整纯 SPE。原实际第一行动是 A1；在实际第二源历史 \((A_1)\) 强制合法 C，随后取给定策略自己的真实后继 \(R_3,R_4,R_5,R_6\)。记此同一分支的收益为 \(v_2,\ldots,v_6\)。真实后继不随终端查询重新挑选，强制的 C 也不被赋予新的最优性。

令 \(\theta=5/12\)。使用如下七项非负预算：

| 预算 | 权 |
|---|---:|
| 原第二源 IC：\(u_2-v_2\) | 25 |
| \(K-|R_3|\) | 1/2 |
| \(K-|R_4|\) | 1/2 |
| \(K-|R_5|\) | 1/2 |
| \(K-|R_6|\) | 1 |
| 同一末节点对六个真实查询的 BR 平均 | 1 |
| 同一分支真实第五源对六个查询的 SAFE 平均 | 5/12 |

末节点的前缀是 \((A_1,C,R_3,R_4,R_5)\)，所以一个查询位 q 的直接收益系数是 \(q/(p+c+r_3+r_4+r_5+1)\)。第五源的真实前缀是 \((A_1,C,R_3,R_4)\)。它真改任意查询后只剩一个真实末回复，该回复至多再覆盖此客户一次，故 SAFE 查询下界为 \(q/(p+c+r_3+r_4+2)\)。这里支付的源收益必须是 **同一分支的 \(v_5\)**，既不是原实际 \(u_5\)，也不是强制第二人的 \(v_2\) 或原 \(u_2\)。

这两个菜单均值使用同一六个真实合法标签。令其客户会员重数 \(d=\sum_{j=1}^6q_j\)、并会员 \(o=\mathbf1_{d>0}\)。两个查询成本先分别逐索引平均，随后才按 \(d\ge o\) 弱化。没有独立性或分割假设。

## 3. 隐藏成本及完整有限域最小值

记四个真实尾位为 \(r=(r_3,r_4,r_5,r_6)\)，负载 \(L=p+c+r_3+r_4+r_5+r_6\)。七预算相加并作菜单弱化后的准确客户成本是

\[
\Psi_\theta(p,c,o;r)=
\frac{25c-r_6-\theta r_5}{L}
+\frac{r_3+r_4+r_5}{2}+r_6
+\frac{o}{6(p+c+r_3+r_4+r_5+1)}
+\frac{\theta o}{6(p+c+r_3+r_4+2)}.
\tag{COST}
\]

当 \(L=0\) 时首分子也为零，首项取零。完整最小值为

\[
m_\theta(p,c,o)=\frac52c+\frac{24c}{p+5}+\frac{o}{6(p+4c+1)}+\theta\left(\frac{o}{6(p+3c+2)}-\frac c5\right).
\tag{MIN}
\]

对 \(\theta=5/12\)，独立重算的全部 8 型结果如下；尾位按 \(r_3r_4r_5r_6\) 排列。

| p | c | o | 最小值 | 全部达到最小值的尾态 |
|---:|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | 0000、0001 |
| 0 | 0 | 1 | 29/144 | 0000、0001、0010 |
| 0 | 1 | 0 | 433/60 | 1111 |
| 0 | 1 | 1 | 523/72 | 1111 |
| 1 | 0 | 0 | 0 | 0000 |
| 1 | 0 | 1 | 23/216 | 0000 |
| 1 | 1 | 0 | 77/12 | 1110 |
| 1 | 1 | 1 | 2789/432 | 1110 |

检查器对每个隐藏态以单独的源份额函数重建七预算的成本，并分别核对 Main 保存的 base、increment、cost、minimum、residual。128 个余项全部非负，所有最小值都有达到的实际尾位；这给出完整有限域证明，不依赖数值近似。

真实菜单平均与弱化成本之差逐客户准确为

\[
\frac{d-o}{6}\left[
\frac1{p+c+r_3+r_4+r_5+1}+\frac{\theta}{p+c+r_3+r_4+2}
\right]\ge0.
\tag{MENU}
\]

对 \(p,c\) 四种取值、64 个真实六菜单位串和 16 尾态，共 4096 情况，程序直接把六个单查询份额相加，并检查 (MENU) 的等式和非负性。不同索引允许同一标签，也允许同覆盖标签；没有把 o/6 当成一个可选行动的会员。

## 4. 为什么 5/12 是当前仿射段的准确端点

对每个隐藏态，将余项写成 \(a+\theta b\)。检查器核验 \(\theta=0\) 和 \(\theta=5/12\) 两端非负，所以整个区间非负；每个 \((p,c,o)\) 型又有两端共有的零态，因此 (MIN) 在该整个区间确实是最小值，不只是一个下界。

对所有 \(b<0\) 的态计算准确阈值 \(a/(-b)\)，其中最小值为 \(5/12\)，唯一限制态为

\[
(p,c,o;r)=(0,0,1;0,0,1,0).
\]

它的余项恰为 \(5/12-\theta\)。因此当前同一仿射最小值公式不能延伸到 \(\theta>5/12\)。这仅认证这一预算组合及这一仿射包络段的端点，没有声称它是所有可能内部付款或所有普遍行中的最优权。

该证明不把真实尾限定为表中最小态；真实尾可以有正余项。尤其允许末尾不覆盖 \(A_1\cap C\)，没有恢复此前已否定的“四尾必全等于 C”说法。

## 5. 普遍付款的符号、K 列和正尺度

令 T 为第 2 节七个真实非负预算的加权和，令 \(\Delta\) 为 (MENU) 的客户总和，\(\rho\) 为 \(\Psi_\theta-m_\theta\) 的客户总和。它们都非负，并且

\[
25u_2+\frac52K-\sum_xm_\theta(p_x,c_x,o_x)=T+\Delta+\rho.
\]

在 \(\theta=5/12\) 时，精确的独立质量付款为

\[
\boxed{
300u_2+K-288B-12M-5N
=12T+12\Delta+12\rho+29(|C|-K).
}
\tag{PAY}
\]

因此 C 真达到 K 时，等式最后一项为零，其余项非负，得到 (NS5)。这里 C 大小等式的自由乘子是 **+29**：十二倍真预算提供 \(30K\)，再加 \(29(|C|-K)\)，剩下目标中的 \(+K\)。该精确符号在检查器中按独立 K 列另行核验。

新增行采用全部 512 个 \((a_1,\ldots,a_6,x,o,c)\) 类型以及独立 K 列。每客户的 \(u_2\) 系数是原实际第二行动的真实份额 \(a_2/(a_1+\cdots+a_6)\)，零负载取零。行系数逐列重建为

\[
300\frac{a_2}{\sum_i a_i}-\frac{288c}{a_1+5}-\frac{12o}{6(a_1+4c+1)}-\frac{5o}{6(a_1+3c+2)},
\]

K 列为 1，右端为 0。全零、\(o=0\)、仅 C 型和所有 X 位均保留。程序又对每个客户型的 16 个隐藏尾态核 (PAY) 的投影系数，共 8192 项，所有结果与原行相符。文件保存的是上述原整数尺度；`numerical_divisor=300` 只是将来整行正缩放的接口，本审计没有使用它运行求解器。

## 6. 对整个冻结最优面的严格作用

前一个独立包 [visible_c_source2_equality_audit](visible_c_source2_equality_audit.md) 已用十二条正原行和两条质量式，在旧对偶的 21 个零余项列上得到精确面身份。其完整证书 SHA 为

`053325a1ae95209726c268064ad6867e478ae0a2c9545aa7099134a4f9565815`。

本次读取其中 K、\(u_2\)、真实第五源均值 SAFE 三个固定函数的系数和有符号乘子，先在原 513 列上分别重放其身份，再作组合；没有执行旧程序。

记 \(R\) 为输入原 raw927 的 `P25_2(C,Omean)`，\(S_5=u_2-N\) 为前包的条件 SAFE 向量，\(E_C=|C|-K\)。在不预先代入 \(|C|=K\) 的完整列上有纯代数恒等式

\[
\boxed{\mathrm{NS5}=12R+K-5u_2+5S_5+30E_C.}
\tag{COMPOSE}
\]

此处的 \(+30E_C\) 来自与旧 P25 原行作差，和 (PAY) 中直接真预算的 \(+29E_C\) 是两个不同展开；两者各自在完整 K 列上核验，不混用尺度或符号。

在旧最优面上 R 与 \(E_C\) 为零，三个固定函数的常数给出 (FACE)。本包保存新的十四条面等式乘子 \(\beta_r\)、完整 513 列目标向量和完整 513 列余项 \(\psi_j\)，满足

\[
\mathrm{NS5}(z)=\sigma+\sum_r\beta_r(E_rz-h_r)+\sum_j\psi_jz_j,
\]

其中 \(\sigma\) 正是 (FACE)，每个 \(\psi_j\ne0\) 的列都有旧对偶严格正余项，从而在最优面上被强制为零。这给出了整个面上的固定严格负值，既不固定六个 C 拆分参数，也不只检查一个代表点。

有符号面身份只负责说明旧面的违反值；**新行的普遍合法性独立由 (PAY) 证明**。没有把等号障碍直接当成无条件预算。

## 7. 最终审计范围

| 项目 | 独立结果 |
|---|---:|
| 同分支七真实预算与正确收益来源 | PASS |
| 完整隐藏态及全部最小值 | 128 / 8，全部精确 |
| 实际六查询菜单平均与弱化 | 4096，逐项精确 |
| 仿射段上端点及唯一限制态 | 5/12；0010 |
| 原 513 列系数、独立 K、零 RHS | PASS |
| 隐藏态付款投影 | 8192 项 |
| 旧面固定函数重放及新面组合 | 完整 513 列 PASS |
| 新行在整个旧面上的值 | (FACE)，严格负 |
| 优化器调用 / 外部或旧代码执行导入 | 0 / 0 |

模型范围保留有限单位客户、非空共同目录、全部合法有序历史、空覆盖、别名、重复行动及所有弱平局。新行无需最优比较菜单或 X 最大性；只需 C 的真实全目录最大裸大小，以支付四个真实尾大小帽并使用 \(|C|=K\)。零客户及所有零项按原份额定义处理。

本包只认证新增普遍必要关系及其对旧最优面的严格作用。没有新求解、完整 SPE 构造、最优根界、best-known 或 half 定理声明。旧 1002 输入、所有前序来源及审计包保持字节不变。冻结记录见 [proof_audit.json](main_source2_maximum_nested_safe_audit/proof_audit.json)、[freeze_manifest.json](main_source2_maximum_nested_safe_audit/freeze_manifest.json) 和 [SHA256SUMS](main_source2_maximum_nested_safe_audit/SHA256SUMS)。
