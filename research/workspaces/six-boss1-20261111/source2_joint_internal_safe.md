# 第二源最大 C 的联合内部 SAFE：完整参数域与 16 个重配端点

Boss1；RUN `six-boss1-20261111`。**精确推导与检查 PASS；优化器调用 0。**

在实际第二源历史 \((A_1)\) 强制全目录最大裸大小标签 C，保留同一策略的四个真实后继。三个内部真实源 3、4、5 的 SAFE 可以同时付费。令 \(p=\mathbf1_{A_1},c=\mathbf1_C,o=\mathbf1_O\)，其中 O 是任意六个合法查询标签的覆盖并，并定义

\[
B=\sum_x\frac{c_x}{p_x+5},\qquad
M=\sum_x\frac{o_x}{6(p_x+4c_x+1)},\qquad
N_j=\sum_x\frac{o_x}{6[p_x+(j-2)c_x+7-j]}.
\]

## 1. 完整三权域与全正联合行

非负内部权的完整仿射包络域恰为

\[
\theta_5\le\frac5{12},\qquad
\theta_4+\frac{\theta_5}{36}\le\frac5{12},\qquad
\theta_3+\frac{\theta_4}{72}+\frac{\theta_5}{36}\le\frac5{12}.
\]

三个单中间覆盖态给出必要性；六面域的全部八顶点均通过 128 隐藏态，给出充分性。全正饱和点为

\[
(\theta_3,\theta_4,\theta_5)=\left(\frac{12425}{31104},\frac{175}{432},\frac5{12}\right).
\]

它给出普遍行

\[
\boxed{777600u_2+7597K\ge746496B+31104M+12425N_3+12600N_4+12960N_5.}
\]

原始推荐文件按 \(u_2\) 系数 25 保存，[SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE.json](source2_joint_internal_safe/SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE.json)；上式是该文件的正尺度 31104 倍，另保存为 [整数钱包版本](source2_joint_internal_safe/SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE_INTEGER_WALLET.json)。全部八条行见 [eight_vertex_family.json](source2_joint_internal_safe/eight_vertex_family.json)。

## 2. Main 提出的源 IC 重配扩张

Main 随后提出 \(\Theta=\theta_3+\theta_4+\theta_5\)、\(\alpha=25+\Theta-s\) 的扩张。本包独立从真份额核验，其完整域为上面的三权域乘以 \(s\in[0,9]\)，并有

\[
\boxed{(25+\Theta-s)u_2+\frac{s}{5}K\ge24B+M+\theta_3N_3+\theta_4N_4+\theta_5N_5.}
\]

源 IC 权始终至少 16。两个 s 边界的必要余项分别为 \(s/30\)、\((9-s)/20\)；全部 16 端点的 2048 隐藏态和完整 8208 行系数通过精确检查。原八个源 IC 权为 25 的钱包是同一 \(\theta\) 两端点的凸组合，所以后续可直接使用 [sixteen_reweighted_vertex_family.json](source2_joint_internal_safe/sixteen_reweighted_vertex_family.json)。所有行保留末 BR 权 1 的共同尺度，正数值除数统一为 25。

这个重配方案及乘积域的提出归于 **Main**；本席完成独立来源核验、完整有限域证明和全部系数重建。

其中 \(\theta=(0,0,5/12),s=9\) 给出简洁普遍行

\[
\boxed{985u_2+108K\ge1440B+60M+25N_5.}
\]

[SOURCE2_MAXIMUM_C_REWEIGHTED_NS5_985.json](source2_joint_internal_safe/SOURCE2_MAXIMUM_C_REWEIGHTED_NS5_985.json) 保存该尺度。与旧整数 NS5 的关系准确为

\[
\mathrm{row}_{985}/5=\mathrm{NS5}-103(u_2-K/5).
\]

## 3. 当前 1003 行系统上确有新增信息

只读正式冻结的 1003 输入与精确证书，独立重放全部原行、513 对偶列、两等式和互补性后，重新对整个最优面做 Fraction 行消元。16 个新端点均有完整 513 列面身份。

旧 NS5 在该面取等，而 \(u_2-K/5\) 恒为正。985 整数行的固定值为

\[
-\frac{215307806202650425854790890033472993016461}
{6132101236429418752884629220503361982820472}<0.
\]

原全正三权行在 \(u_2\) 系数 25 的共同尺度下也已严格为负，约 \(-0.00731540799\)。16 个重配端点中最负的是 V111、s=9，固定值为

\[
-\frac{1662713433947719228497912011431524329842570361}
{211925418731000712099692785860596190126275512320}
\approx-0.00784574802.
\]

这些行不被当前 1003 行必要系统蕴含。这里没有重新求解加行后的系统，也没有声称新的全局最优值或福利系数。

## 4. 完整证明、证书与范围

- [proof.md](source2_joint_internal_safe/proof.md)：真实付款、三权完整域、八顶点、四参数扩张、16 端点、全部尺度和最优面比较。
- [parameter_polytope.json](source2_joint_internal_safe/parameter_polytope.json) 与 [reweighted_polytope.json](source2_joint_internal_safe/reweighted_polytope.json)：参数域的完整必要/充分证书。
- [joint_hidden_states.json](source2_joint_internal_safe/joint_hidden_states.json) 与 [reweighted_hidden_states.json](source2_joint_internal_safe/reweighted_hidden_states.json)：全部精确隐藏态余项。
- [current1003_face_identities.json](source2_joint_internal_safe/current1003_face_identities.json)：16 条行、收益差和 985 行的完整面身份。
- [comparison_frozen1003.json](source2_joint_internal_safe/comparison_frozen1003.json)：同尺度精确比较。
- [checker_output.json](source2_joint_internal_safe/checker_output.json) 与 [reweighted_checker_output.json](source2_joint_internal_safe/reweighted_checker_output.json)：检查结果及来源 SHA。
- [freeze_manifest.json](source2_joint_internal_safe/freeze_manifest.json)：最终冻结清单。

从仓库根目录依次运行 `source2_joint_internal_safe/derive_exact.py` 和 `source2_joint_internal_safe/derive_reweighted.py` 即可重放，完整命令见 proof。程序只用标准库有理运算，不执行或导入 Main、builder、solver 或旧审计代码。有限单位客户、空覆盖、别名、重复标签、所有有序历史和弱平局均保留；O 不作为行动，X 不参与来源。所有旧包保持原字节。

参数域的完整性仅针对本文明确给定的仿射最小值与非负真实预算权；没有任意 SPE 钱包的全局最优性、完整 SPE 实现或 half 定理声明。
