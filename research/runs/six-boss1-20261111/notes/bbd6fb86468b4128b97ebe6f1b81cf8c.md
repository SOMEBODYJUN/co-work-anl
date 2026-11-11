# 同一 X 的全部旧 ZZ 条件上包络：5580 行零新列接口

Boss1；RUN `six-boss1-20261111`。本义务已完成通用接口、独立字面/轨道审计及新点完成器，现冻结等待 Main 返回新有理点。**新增候选 5580 行全部互异，共 27900 个非零系数，零新列；没有装配更大矩阵，没有读取任何旧或新原始点，优化器调用 0。** 原 `common_x_joint_lp/final/` 的 23676×21021 云输入保持原字节。

输入矩阵 SHA256：
`1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7`。

这是 Main [一般推导](main_X_conditioned_ZZ.md) 在全部旧 2790 个 ZZ 辅助上的完整接口，不是原六人定理的证明。原共同目录、完整有序历史、纯 SPE、弱平局、空覆盖、重复行动及同覆盖异标签均保留；`2W≥OPT6` 仍 OPEN。

## 1. 三个真实会员位给出的两个新增界

在一个固定客户块，令同一个目录标签 X 的会员位为 x，源标签 R 的会员位为 R，查询标签 Z 的会员位为 Z。逐客户有

\[
xR+Z-xZ-RZ=xR(1-Z)+(1-x)Z(1-R)\ge0,
\]

\[
R-xR+xZ-RZ=(1-x)R(1-Z)+xZ(1-R)\ge0.
\]

两条恒等式对全部八种 `(x,R,Z)` 独立核验；包括全零型，不除以任何质量。记质量为

\[
q=|R|,\quad v=|Z|,\quad r=|X\cap R|,\quad z=|X\cap Z|,
\]

则真实交叠 `J=|R∩Z|` 除了旧 `J≤q,v`，还满足

\[
J\le r+v-z,\qquad J\le q-r+z.
\]

所以四端上界为

\[
U(q,v,r,z)=\min(q,v,r+v-z,q-r+z)
=\min(r,z)+\min(q-r,v-z).
\tag{1}
\]

恒等式是分别从 `min(r,z)` 与 `min(q−r,v−z)` 中选端点后的四种和。独立布尔审计记录见 [literal_boolean_audit.json](x_conditioned_zz/literal_boolean_audit.json)。代码中的有限整数探针仅作算术自检；一般证明由上述代数恒等式给出。

X 在此只需是共同目录中的同一个真实标签，其最大性不参与这两个界。当前接口沿用其余行已选定的同一 X，不按 hist、源、查询、轨道或客户重新选择 X。

## 2. 真实历史与组平均的准确接法

旧真实节点沿用 [common_coupling_math.md](common_coupling_math.md) 的定义。设实际前三历史为 `h3`，前四为 `h4`，则

\[
E=\{(0,i,j):i\ne j\}\cup\{(1,i,j):1\le i,j\le6\},\qquad |E|=66,
\]

\[
R_{0ij}=\sigma_6(h_3,T_i,B_j),\quad
R_{1ij}=\sigma_6(h_3,T_i,C_j),\quad
Z_e=\sigma_6(h_4,R_e).
\]

在真实末节点 `(h4,R_e)` 查询合法的同目录标签 `Z_f`，逐字面 IC 为

\[
L_{ef}=\sum_c\frac{z_e(c)-z_f(c)}{P_c+1+r_e(c)}\ge0.
\]

这里不要求被强制的第五位行动 `R_e` 最优，也不把另一节点 `Z_f` 的收益当实际收益。固定 hist h 后 `P=P_h` 为常数，令 `D=(P+1)(P+2)`，则该块贡献为

\[
L_{ef,h}=\frac{v_{e,h}-v_{f,h}}{P+1}
 +\frac{J(R_e,Z_f)_h-t_{e,h}}{D}.
\tag{2}
\]

旧组标识是

\[
g_h(e)=(\mathrm{family}(e),1[i=j],w_i,w_j),\qquad w_i=(t_i,b_i,c_i).
\]

组内 `q,v,t,r,z` 都是字面节点的均匀平均，不是把相同 group 的不同节点视为同一事件。对一个固定完整字面查询轨道 C，以及其中落入 `E_hg×E_hk` 的非自查对集合 S，令 `n=|S|`。保持旧词的稳定子在每个单边组上传递，S 对同时置换不变，所以其源端与查询端各为等度。由于 X 没有比较索引，稳定子仍固定同一个 X 位。由此准确得到

\[
\sum_{(e,f)\in S}|X\cap R_e|=nr_{h,g},\qquad
\sum_{(e,f)\in S}|X\cap Z_f|=nz_{h,k},
\]

以及旧 `q,v,t` 的同样平均恒等式。分别汇总四条逐对线性上界后，才取最小值：

\[
\sum_{(e,f)\in S}J(R_e,Z_f)
\le n\min(q_{h,g},v_{h,k},r_{h,g}+v_{h,k}-z_{h,k},
q_{h,g}-r_{h,g}+z_{h,k}).
\tag{3}
\]

因此，不同完整轨道中相同 `(h,g,k)` 的真实交叠均值可以不同，但都被同一个 U 控制。复用一个虚拟上包络 p 不要求那些交叠相等。

本次不仅引用等度论证，还逐字面实核所有关联类。独立审计从 15 种四索引相等分割、两侧 family 及每个代表的全部 720 个置换重建 42 个合法轨道；其中恰有 3 个字面自查零轨道，其余 39 个预算与冻结矩阵逐系数相同。只有 `e=f` 被跳过；同 group 但不同 e/f 的 9944 个 pair×hist 项完整保留，`e=(0,i,j), f=(1,i,j)` 也完整保留。

审计总计 68640 个非自查 pair×hist 项，分成 5362 个 `(h,C,g,k)` 关联类；全部类都实核每个源节点度数相同、每个查询节点度数相同。每一类保存完整字面 node index 对、两侧组大小、两侧度数、平均系数与 p 在预算中的确切 `n/D` 系数，见 [literal_orbit_interface.json.gz](x_conditioned_zz/literal_orbit_interface.json.gz)。

## 3. 从真实描述符重建全部 2790 组对

构建器不导入旧 own 映射，也不把 `hist_column_old` 当当前列号。它从原 `joint-state-upper` 行的一个正 H 和三个负 `joint-reply` 状态恢复 194 个 own 组，再按 descriptor 的 state 形成

\[
q=\rho_{10}+\rho_{11},\qquad v=\rho_{01}+\rho_{11}.
\]

独立审计使用原 descriptor 的 hist 连续段作第二路径，并与这 194 条原状态上界逐项互核。然后分别通过真实 token

\[
(h,(R,g))\mapsto r,\qquad (h,(Z,k))\mapsto z
\]

找到现有真实 core；并将重建的 q/v 与各 y descriptor 中的 `query_marginal` 逐系数比较。

| 坐标/行接口 | 数量与位置 | 本层处理 |
| --- | --- | --- |
| 全部原坐标 | 21021 列 | 保留原索引、非负列及描述符 |
| 真实 core | `0…4848 ∪ 15593…21020`，10277 列 | 全部保持 |
| 共同 X 质量 | `20585…20600`，16 列 | 同一 X 的全部 hist 质量保持 |
| 真实 X 交叠 | `20601…21020`，420 列 | 禁止规范到 min；388 个 R/Z 被新行使用，32 个 H1/H2 仍完整保留 |
| 旧 max 辅助 | `4849…12802`，7954 列 | 新行完全不触碰，恢复规则保持 |
| 旧 ZZ min 辅助 | `12803…15592`，2790 列 | 旧两端规则改为四端 min |
| 旧 p 上界 | `13931…19510`，5580 行 | 原 q/v 上界保留 |
| 旧真实 ZZ 预算 | `19511…19549`，39 行 | 原字面行与系数保留 |
| 新 p 上界候选 | 5580 行，27900 非零 | 只新增下式两端界；零新列 |

每个 p 新增

\[
r+v-z-p\ge0,\qquad q-r+z-p\ge0.
\tag{4}
\]

全部 5580 条完整稀疏向量互异，且没有旧行同时含 ZZ p 与真实 X y，故没有旧重复行。候选到保留行的映射是 `0…5579` 恒等映射；未做删行。若将来显式追加，shape 才是 29256×21021；本轮没有创建该大矩阵。

16 个 hist 的 p 数量分别是：

| hist 列 | p 数量 | hist 列 | p 数量 |
| --- | ---: | --- | ---: |
| 1 | 360 | 366 | 360 |
| 59 | 360 | 424 | 63 |
| 117 | 360 | 449 | 63 |
| 175 | 63 | 474 | 63 |
| 200 | 63 | 499 | 63 |
| 225 | 63 | 524 | 63 |
| 250 | 360 | 549 | 63 |
| 308 | 360 | 574 | 63 |

每个 hist 唯一未列的自组对是一个单字面节点组的 `(e,e)`，16 个省略都有字面记录；并非按当前质量为零删组。历史上曾为零的 `1,59,366,449,524,574` 六个 hist 及其全部相关列照常保留。

完整 2790 映射与四个符号端点在 [column_interface.json](x_conditioned_zz/column_interface.json)，完整新增候选在 [conditioned_upper_rows.json](x_conditioned_zz/conditioned_upper_rows.json)。

## 4. 全列符号审计与四端规范化的准确范围

构建器与独立审计分别扫描冻结矩阵的全部 23676 行、3313758 个非零系数。结果是：

* 每个旧 p 恰有两次负出现，均为旧 q/v 上界中的系数 −1，共 5580 次。
* 其余出现全部为 39 条真实 ZZ 预算中的正系数，共 5362 次；目标和归一中全部为零。
* 每个旧 max 仍只有一条正系数 1 的阈值行，其余出现全负；新层不含任何旧 max。

2790 个 p 的**每一处**旧正负出现均已逐列保存，而不是只按行名前缀推断，见 [old_aux_sign_audit.json](x_conditioned_zz/old_aux_sign_audit.json)。

固定任意满足旧 core 合同的全部非 p 坐标。现有 y 非负及 `r≤q,z≤v` 保证四个端点均非负，例如 `r+v−z=r+(v−z)≥0`；对应现有行索引也独立保存。若某个 p 选择满足旧系统及 (4)，将它提高到 (1) 的 U，旧四条上界继续满足，所有其余旧行只增不减。因此

\[
\exists p\text{ 满足此完整包络层}
\iff p_{h,g,k}=U_{h,g,k}\text{ 同时满足全部预算}.
\tag{5}
\]

这是**虚拟上包络层**的精确存在性规范；不是说这些 U 都能成为同一全目录客户律中的真实交叠。它不解决跨组或跨历史共同实现，也不改变 420 个 y 的真实 core 身份。

将来如果把新层接入另一轮有理恢复，p 的线性片只能从接口中给出的四个 core 端点选择；平局可以添加相等端点之差为零的活动方程。q/v/r/z 中的 y 仍是独立核心未知量，不能再沿旧虚拟 y 规则消去。当前恢复器和云输入未修改。

## 5. 新有理点接回后的精确路径

[complete_point.py](x_conditioned_zz/complete_point.py) 已准备，默认不读取点。Main 给出新文件及 SHA256 后，调用格式为：

```bash
python -B research/workspaces/six-boss1-20261111/x_conditioned_zz/complete_point.py \
  --point /absolute/path/to/new/augmented_lp_exact.json \
  --point-sha256 NEW_EXACT_POINT_SHA256 \
  --tag main_new_point
```

接收器先核冻结合同、矩阵 SHA、完整 21021 描述符及精确有理权值，然后实算输入的全部 23676 行、列非负与 `O=1`。不合法输入只给输入失败，不输出 core 排除。对合法输入，它保存所有坐标，只将 `12803…15592` 的 2790 个 p 改成四端 min，并逐项断言 10277 core、420 个 y 与 7954 个 max 均保持。

随后精确重算全部 23676 旧行及全部 5580 新行，保存完整前后余量、全部端点/平局选择和 39 条真预算。

1. **全部通过：** 保存完整 `completed_point.json.gz` 和 `EXACT_FIXED_CORE_CONDITIONED_ZZ_COMPLETION`；这关闭该固定 core 的本层完成义务。
2. **存在负预算：** 选择继承原尺度上最负的真实 ZZ 预算，保存完整最大 p 候选和 exact core 排除证书。

排除证书的核心并不是“旧 p 违反新上界”。若预算为 `B=b(core)+Σ a_j p_j`，其中 `a_j>0`，为每个 p 选一个达到 U 的活动线性端点 `u_j(core)`，则精确恒等式为

\[
B+\sum_j a_j\bigl(u_j(core)-p_j\bigr)
=b(core)+\sum_j a_j u_j(core)=C(core).
\]

左边全是应非负的真预算与合法上界的非负组合；所有 p 消掉。只有核得固定 core 上 `C<0`，才输出严格排除。因为预算无旧 max，这也排除任何其它辅助选择对该 core 的补救；不排除别的 core 或整个最优面。

输入若已经按旧两端 min 规范，所有 p 只能减小；接收器也允许其它旧可行 p，并逐项记录是否原本规范，不把“只能减小”错误用于非规范输入。

## 6. 已实际完成的检查与冻结状态

以下三个标准库程序已经实际执行成功：

| 程序 | 实际检查 | 回执 |
| --- | --- | --- |
| `build_interface.py` | 描述符/原状态行映射、5580 候选、完整符号扫描、字面关联 | `build_manifest.json` |
| `verify_interface.py` | 不导入构建器；720 置换轨道、逐字面重建39行、八布尔型、全部映射与符号复核 | `independent_audit.json`：PASS |
| `complete_point.py --self-check` | 只用明确合成向量，验证2790替换不动core/max、11160个旧新上界和39份消元恒等式 | `completion_selfcheck.json`：PASS |

合成向量没有被称为 LP 可行点，其预算值没有被用于任何排除。准备阶段没有打开任何原始点文件，也未对已处理的 `5b1b/cb45` 点重新评价。所有代码仅使用 Python 标准库，没有优化器调用或有理支持搜索。

产物及代码 SHA 统一见 [freeze_manifest.json](x_conditioned_zz/freeze_manifest.json)。本任务到此冻结并释放；收到 Main 的**新有理点**后，才沿第 5 节继续完成或给出真实预算承重的 core 排除。
