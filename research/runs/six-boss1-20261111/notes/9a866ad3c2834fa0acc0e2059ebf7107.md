# 同一个 X 在 actual 玩家 1–3 的旧任意锚 AP 查询

Boss1；RUN `six-boss1-20261111`；工作区 `early_x_anchor_queries/`。

**结论：Main 给出的三个代入全部成立。** 旧任意锚 AP 已经允许任意合法锚标签；actual 前四背景下选定的同一个全目录最大主题 X，可直接用于 actual 玩家 1、2、3，不需要它在这三个较早背景下加权最大。三个统一常数分别为 `43、65/2、23`。

本包交付 **51 条有理稀疏必要行、5124 个非零系数、0 新列**，坐标严格复用冻结 `22297×21021` 系统的全部描述符。158 个字面查询表达式的 17 个 S6 轨道从原标签重新生成；全部 16hist、六个旧零 hist、16 个共同 X 质量与 420 个旧交叠上包络均保留。输入矩阵未追加、未修改；没有打开旧 cb45 点文件、读取其权重、评价任何点或调用优化器。

本结论的数学身份是**已存在 AP 引理的精确代入及坐标接口**，不是新的 AP 引理，不是六人 half 的付款闭合，也不证明冻结必要 LP 加这些行后最优值提高。

## 1. 完整实读来源与真正适用的旧命题

以下三个主原件及现行对象均完整实读；另有独立只读源审 `/root/early_x_anchor_queries/ap_source_audit`，其常数、真实后继及付款分解与本稿一致。源码/对象 SHA 和准确文件路径保存在 [source_reading.json](early_x_anchor_queries/source_reading.json)。

| 来源 | 本次承重位置及版本边界 |
|---|---|
| [原主稿 background_near_saturation.md](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md) | 第 8–26 行定义任意完整纯 SPE、任意有序历史、真实当前收益及 `M≤总人数`；第 33–112 行保全真实偏离分支、末位查询与整数核；第 132–155 行明确任意合法 `C,D` 的 AP，第 149–151 行明言可用总人数作共同常数且无需加权最大锚。 |
| [原 CLAIMS.md](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/CLAIMS.md) | `B10-AP-v1` 使用全客户 M；`B10-AP-v2` 使用同一锚的共同 M_C；第 14–17 行说明 M 的两处用途及空锚直接证明。不能逐列替换共同常数。 |
| [原 README.md](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/README.md) | 区分原解析证明、内部重构、有限审计和固定支持点。原稿较早写“解析候选”，后 CLAIMS/README 记内部重构；本包不把它们改成外审或新颖性认证。 |
| [现行任意背景 BNS/AP 对象](../../../archives/customer-attraction/state/引理/任意背景加权近饱和交换与统一锚主题上界--引理.md) | 对象 `customer-attraction/background-weighted-near-saturation-exchange-and-common-anchor-cap`；“量词、背景与两个版本”给 AP1/AP2，“任意锚主题 AP 的完整新增误差”给完整证明，“从真实实例到线性固定支持的准确合同”给统一支持上界。 |
| [共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md) | 保留有限非空标签目录、空覆盖、同覆盖异标签、重复行动、零客户与任意历史依赖弱平局。 |

原 AP1 的准确量词如下：任意固定完整纯 SPE σ、任意合法有序历史 h、剩余 `r≥2` 人（包括当前），客户过去负载为非负整数 b。令 u 为 σ 在 h 的当前人的真实最终收益，`M=r+max b`，空客户时 max 取 0。对每个合法锚 X 和每个合法 Q，同时有

\[
s_X=\sum_{j\in X}\frac1{b_j+r},\qquad e=u-s_X\ge0,
\]

\[
F_b(X,Q)=\sum_{j\in X\cap Q}\frac1{b_j+r}
+\sum_{j\in Q\setminus X}\frac1{b_j+1}
\le s_X+\left[(r-1)(M-1)+\frac{r^2}{2}\right]e.
\tag{AP-old}
\]

本包只需要 **AP1 及 M≤6 的共同放宽**，不依赖 v2 的更紧常数，也不使用任何旧固定支持点、1867 行有限可行声明或旧审计计数来证明普遍必要性。

## 2. 同一 X 的身份与三个 actual 代入

固定六人完整纯 SPE 的实际终局 `(A1,…,A6)`。actual 前四客户负载为

\[
P_j=\sum_{k=1}^{4}\mathbf1_{j\in A_k},\qquad
X\in\arg\max_{T\in\mathcal S}\sum_{j\in T}\frac1{P_j+1}.
\]

从有限非空目录取任意一个最大标签后固定它。对 `i=1,2,3`，置

\[
h_{i-1}=(A_1,\ldots,A_{i-1}),\quad
b_j^{(i)}=\sum_{k<i}\mathbf1_{j\in A_k},\quad r_i=7-i.
\]

由于 `0≤b_j^(i)≤i−1`，原 AP 的实际常数满足

\[
r_i\le M=r_i+\max_j b_j^{(i)}\le r_i+i-1=6.
\]

`e≥0` 保证将 M 提高到 6 的方向正确。由此对**全部合法 Q 同时**成立

\[
\boxed{C_i u_i-(C_i-1)\kappa_i(X)\ge L_{b^{(i)},r_i}(X,Q),}
\tag{EAP-X}
\]

\[
\kappa_i(X)=\sum_{j\in X}\frac1{b_j^{(i)}+r_i},\qquad
L_{b,r}(X,Q)=\sum_{j\in Q}\frac1{b_j+1}
-\sum_{j\in X\cap Q}\frac{r-1}{(b_j+1)(b_j+r)}.
\]

| actual 玩家 i | 源历史 | r_i | C_i | 完整行 |
|---:|---|---:|---:|---|
| 1 | 空历史 | 6 | 43 | `43u1−42κ1(X)−L_b,6(X,Q)≥0` |
| 2 | `(A1)` | 5 | 65/2 | `(65/2)u2−(63/2)κ2(X)−L_b,5(X,Q)≥0` |
| 3 | `(A1,A2)` | 4 | 23 | `23u3−22κ3(X)−L_b,4(X,Q)≥0` |

X 的最大性只用于它在既有共同 X 系统中的身份；以上三个 AP 代入的证明仅使用其合法性。AP 的任意锚量词允许先选定这个 X，再在较早节点代入，因而没有额外的因果或量词要求。三个 i、全部 Q 和全部客户共用同一个 X；不按背景、Q 或 hist 换锚。

这里的 `u_i` 是原 actual 完整终局中的玩家 i 收益。它既不是强制 X 后的偏离收益，也不是较早背景下的人为最优值。

## 3. 原 AP 在 M=6 下的完整显式付款

本节把旧证明写成可逐项核验的非负恒等式，补全收益来源与后继身份。固定一个 i，省略 i 上标，写 `r=r_i,u=u_i,s=κ_i(X)`。

仅强制当前人在原有序前缀 h 选择 X，其后沿**同一份 σ 在改变后有序历史上的真实后继**得到

\[
B_2,\ldots,B_r=L.
\]

令 v 为强制选择 X 的当前人收益，t 为该分支真实末位 L 的收益；`n_j` 为此分支剩余 r 人对客户 j 的覆盖次数。定义

\[
w_j=\frac1{b_j+r},\qquad e=u-s,\qquad
d=\sum_{j\in X}(r-n_j)w_j,\qquad
d_L=\sum_{j\in X\setminus L}w_j.
\]

当前真实激励给 `u−v≥0`；最坏分母给 `v≥s`。对每个实际后继标签 B_ℓ，令

\[
g_\ell=u-\sum_{j\in B_\ell}w_j\ge0\quad(2\le\ell\le r).
\tag{S}
\]

每条 (S) 的完整付款发生在**原当前源 h**：当前人真改 B_ℓ 后，沿该偏离自己的真实 σ 后继取得收益 `v(B_ℓ)`；于是

\[
g_\ell=[u-v(B_\ell)]+\left[v(B_\ell)-\sum_{j\in B_\ell}w_j\right]\ge0.
\]

这没有冻结 X 分支的其他行动。B_ℓ 在 X 分支被看到，只说明它是同一目录中的合法标签，足够作原当前源的偏离比较。若这些标签重复，可在同一非负预算上使用相应固定乘子。

记 X 外的末主题质量与中间总关联为

\[
c_L=\sum_{j\in L\setminus X}w_j,\qquad
I=\sum_{\ell=2}^{r-1}\sum_{j\in B_\ell\setminus X}w_j.
\]

定义直接给出两条精确等式：

\[
c_L=d_L+e-g_r,\qquad
I=d-d_L+(r-2)e-\sum_{\ell=2}^{r-1}g_\ell.
\tag{B}
\]

以下三个余项非负：

\[
R_d=5(v-s)-d\ge0,
\tag{D}
\]

\[
R_t=r c_L-\frac65d_L-(t-v)\ge0,
\tag{T}
\]

\[
R_Q=p_Q-L_{b,r}(X,Q)+\frac r2 I\ge0.
\tag{Q}
\]

其中 p_Q 是在真实末节点 `(h,X,B2,…,B_{r−1})` 改选 Q 的真实查询收益，故末位 IC 是 `BR_Q=t−p_Q≥0`。三个余项的理由分别为：

- 对 X 内缺失至少一席的客户，`b+n≤5`；所以 `v−s=Σ_X(r−n)/[(b+n)(b+r)]≥d/5`。零缺失项等于零，不需除以 d。
- 在 `L\X` 上，`1/(b+n)≤1/(b+1)≤r/(b+r)`；在 `X\L` 上，`1/(b+n)≥1/(b+r−1)≥6/[5(b+r)]`，最后一步使用 `b+r≤6`。交集中 v 与 t 使用同一终局分母而精确取消。
- 在 `Q∩X` 上，末位查询分母不超过 `b+r`；在 `Q\X` 上，中间覆盖数 z 是 `0,…,r−2` 的整数，并且

  \[
  \frac1{b+z+1}\ge\frac1{b+1}-\frac{z}{(b+1)(b+2)}
  \ge\frac1{b+1}-\frac r2\frac z{b+r}.
  \]

  第一个差为 `z(z−1)/[(b+1)(b+2)(b+z+1)]≥0`；第二步来自 `r(b+1)(b+2)−2(b+r)=b[rb+3r−2]≥0`。再把 Q 外部关联放宽为全部 I，只添加非负量。

取 `C=5(r−1)+r²/2`。代入 (B) 后，完整付款恒等式为

\[
\boxed{
\begin{aligned}
Cu-(C-1)s-L_{b,r}(X,Q)
={}&5(r-1)(u-v)+r g_r+\frac r2\sum_{\ell=2}^{r-1}g_\ell\\
&+BR_Q+R_t+R_Q\\
&+\left(r-\frac65\right)R_d
+\left(\frac r2-\frac65\right)(d-d_L).
\end{aligned}}
\tag{PAY}
\]

所有乘子在 `r=6,5,4` 均非负，且 `d−d_L≥0`。u 的总系数恰为 `5(r−1)+r+(r/2)(r−2)=C`。这是原 AP 链的显式展开，不额外假设中间后继的局部最优性，也不把各条全局激励或 (S) 当成逐客户非负。

| r | 当前改 X 激励乘子 | 末主题 safety 乘子 | 每个中间 safety 乘子 | R_d 乘子 | d−d_L 乘子 |
|---:|---:|---:|---:|---:|---:|
| 6 | 25 | 6 | 3 | 24/5 | 9/5 |
| 5 | 20 | 5 | 5/2 | 19/5 | 13/10 |
| 4 | 15 | 4 | 2 | 14/5 | 4/5 |

全空 X、零客户或 e=0 均无除法异常。空 X 时 `d=d_L=R_d=0`，(PAY) 仍成立；没有对空锚计算不存在的最大客户。弱平局、重复行动和同覆盖异标签都保留，因为每个分支使用精确有序标签历史。

## 4. 51 行的完整坐标接口

对一个固定 hist h，记原总质量为 m_h，同一个 X 的质量为 x_h，源 i 的固定背景负载为 b_h，某查询的真实质量为 q_h、真实交叠为 c_h。单个查询行是

\[
C_i u_i-\sum_h\frac{(C_i-1)x_h}{b_h+r_i}
-\sum_h\frac{q_h}{b_h+1}
+\sum_h\frac{(r_i-1)c_h}{(b_h+1)(b_h+r_i)}\ge0.
\tag{ROW}
\]

实际收益从固定 hist 的六位字面描述符计算：若玩家 i 位为 1，该 hist 对 u_i 的系数为六位总覆盖数的倒数；若为 0，系数为 0。程序将全部六个 `u_i−κ_i(X)` 与冻结完整矩阵的 `actual-safe-X` 行逐分数比对，完全一致。

### 4.1 从 158 字面表达式重建 17 轨道

原标签入口为 `actual_pair_20910/labels_and_orbits.json`。使用其 `labels` 字段，不采用保存的轨道表或旧点数字。158 个表达式为六个 A、各六个 T/B/C、66 个 R、66 个 Z、两个 H；R/Z 包含 family 0 的 30 个非对角有序对及 family 1 的全部 36 个有序对。被原合同省略的 family 0 对角别名不另造标签。

S6 同时重命名六个菜单索引；A 的实际玩家位置和 H 不移动，同一个 X 也固定。所有 720 个置换从每个代表生成轨道并核等频。每个表达式在真实游戏中是合法纯标签；不同表达式可能恰好指向同一个真实标签，这种重复查询不破坏固定平均，也不把平均当成可行动的分数标签。

| 查询轨道类型 | 轨道数 | 每轨道大小 | 每成员在 S6 中的频数 |
|---|---:|---:|---:|
| A1,…,A6 | 6 | 1 | 720 |
| T、B、C | 3 | 6 | 120 |
| R/Z family 0 非对角 | 2 | 30 | 24 |
| R/Z family 1 对角 | 2 | 6 | 120 |
| R/Z family 1 非对角 | 2 | 30 | 24 |
| H1、H2 | 2 | 1 | 720 |

每个 hist 从八词计数展开六个字面 `(T,B,C)` 会员词；对 R/Z 使用 `(family,是否同索引,词_i,词_j)`，不能把“同词”误当作“同索引”。H 只读取其两个真实角色位；B4 的第三个聚合字段不变成新行动标签。

全部 `16×17×720=195840` 个代表图像的 token 频数已核对。每位玩家另从逐字面查询与按 token 频数两条路径生成行并逐系数一致，共检查 `3×16×158=7584` 个字面 hist 查询。

### 4.2 未知 XQ 的正上包络

A 与 T/B/C 的会员在 hist/词上确定，因此 XQ 恰是 0 或相应 x_h。R/Z 的旧查询边缘从 raw `joint-reply` 三个存储态重建，H 边缘从 raw `actual-B-family-state` 的两真实角色位重建；420 个结果与冻结完整列描述符的 `query_marginal` 逐项一致。

剩余未知 c_h 的系数始终严格为正：

\[
\gamma_{i,h}=\frac{r_i-1}{(b_h+1)(b_h+r_i)}>0.
\]

故可沿用原 420 个共同上包络，取规范值

\[
y_{h,Q}=\min(x_h,q_h)\ge c_h.
\]

把 (ROW) 的 c_h 换成 y_h 是合法必要放松。完整旧矩阵中每个 y 只在两条上界行带负系数 `−1`，其余出现均非负；本包三组行只增加正系数。因此“同时提高到各自 min 不损必要系统可行性”的规范化继续有效。

这不要求 420 个 min 同时来自同一份真实客户交叠；没有把上包络真实化。若以后增加含负 y 的物理共同完成约束，需按那项新任务重新审查规范化，不能把这里的结论无条件沿用。

### 4.3 冻结尺寸及零质量类型

| 项目 | 精确结果 |
|---|---:|
| 原完整矩阵 | 22297×21021，3296061 非零，未修改 |
| 复用共同 X 质量列 | 20585…20600，共 16 列 |
| 复用交叠上包络列 | 20601…21020，共 420 列 |
| 玩家 1 新行 | 17 行，1707 非零 |
| 玩家 2 新行 | 17 行，1697 非零 |
| 玩家 3 新行 | 17 行，1720 非零 |
| 合计 | 51 行，5124 非零，0 新列 |
| 新行中的上包络正系数出现次数 | 1260，每个既有 y 恰出现 3 次 |

六个原零 hist 索引 `1,59,366,449,524,574` 全部保留；其零身份只读取既有结构记录，未读取 cb45 权重。全部 51 行都覆盖 16 个 X 质量坐标，未通过删除零质量 hist 或隐藏态缩小定义域。共同 M=6 先对全部允许类型有效，不逐列改为 `r+b_h`，也不因点上某列零权而收紧它。

## 5. 与 SAFE 和已审 H3-X 的有限准确关系

完整 AP 的“全部合法 Q”族包含 `Q=X`；此时 `L(X,X)=κ_i(X)`，故该行退成 `C_i(u_i−κ_i(X))≥0`，与对应 SAFE 等价。

**本次输出的 17 个旧查询轨道没有另加新标签 X。** 因此不能据此声称这 17 行自身推出 SAFE；冻结系统中的 SAFE 保持原样。对一般 Q，AP 记录的是 `C_i(u_i−κ_i(X))≥L(X,Q)−κ_i(X)` 的目录报价付款；单条 SAFE 只保证左侧缺额非负，并未给这份具体上界。

在 actual 玩家 4 的同一个源、同一 b、同一 X 和 Q 上，旧任意锚 AP 的统一常数为 `29/2`，已审 H3-X 的常数为 10。两者有精确行恒等式

\[
\operatorname{AP}_{4,29/2}(X,Q)
=\operatorname{H3\!\! -X}_{4,10}(X,Q)
+\frac92\,\operatorname{SAFE}_4(X).
\]

程序已对既有 17 个 H3 查询轨道逐系数核此式，包括相同 420 上包络替换。因此 H3-X 加 SAFE 推出该指定的玩家 4 旧 AP 族。

本包玩家 1–3 使用不同的 `u_i,b,r`；上述同源恒等式不提供跨玩家支配关系。没有证明新 51 行被现有 H3 或冻结全部行推出，也没有证明它们逻辑独立、分离任何点或提高最优值。根部 `i=1` 的 AP 是旧任意主题对根行在同一 X 上的应用，也不重授新引理。

## 6. 精确验证、交付与冻结

构造与检查入口：

```text
python -B research/workspaces/six-boss1-20261111/early_x_anchor_queries/build_and_check.py
```

已运行结果为 `EXACT_EARLY_X_AP_51_ROWS_PASS`。检查包括旧完整矩阵 1387 条共同 X 行的重映射、全部六条 SAFE 的 actual 字面重建、420 个 raw 旧边缘、176 个付款系数型、22 个整数核 `(b,z)` 型，以及本稿全部频数和坐标检查。176 型遍历各 i 的 `b∈{0,…,i−1}`、`z∈{0,…,r−2}` 和 X/末主题/查询三布尔位；这是有限系数恒等式检查，普遍有效性由第 3 节解析证明承担，不是 176 个 SPE 的枚举。

默认入口拒绝覆盖已有产物。冻结入口 `--freeze` 重新核全部只读输入 SHA 后封存；不调用优化器、不装配新的总矩阵、不改 Git、RUN 或 registry。完成后本代理释放工作席。

| 文件 | 内容 / SHA256 |
|---|---|
| [rows_51.json](early_x_anchor_queries/rows_51.json) | 全部有理稀疏行、源玩家、常数、字面查询、hist 频数与绑定；`0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb` |
| [columns_21021.json.gz](early_x_anchor_queries/columns_21021.json.gz) | 全部原 21021 列描述符的无权副本；`3124805fa567d06c200bbe37bdf9c72a1d890aad57b85f3fee0f4622b876399b` |
| [build_and_check.py](early_x_anchor_queries/build_and_check.py) | 仅标准库的点无关构造、精确付款与坐标检查程序；实际构造时的源码另存 `executed_build_and_check.py`，随后仅扩充冻结资产名单以保独立审稿。 |
| [ap_source_audit.md](early_x_anchor_queries/ap_source_audit.md) | 实际 canonical agent ID 与独立只读源审的完整最终反馈；不冒称独立代码审计。 |
| [proof_atoms_176.json](early_x_anchor_queries/proof_atoms_176.json) | 全部 176 个精确系数型及非负余项。 |
| [orbit_frequency_audit.json](early_x_anchor_queries/orbit_frequency_audit.json) | 158 字面表达式、17 轨道、全部 hist token 频数和 720 置换重数。 |
| [verification.json](early_x_anchor_queries/verification.json) | 完整通过状态、输入 SHA、检查范围与未执行事项。 |
| [source_reading.json](early_x_anchor_queries/source_reading.json) | 完整阅读与独立只读审查定位、原件版本身份。 |
| [freeze_manifest.json](early_x_anchor_queries/freeze_manifest.json) / [SHA256SUMS](early_x_anchor_queries/SHA256SUMS) | 所有交付文件与主文的最终 SHA、冻结范围。 |

冻结矩阵 SHA 保持 `c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b`。本包为 Main 提供可审阅、可另行追加的 51 行；其在完整共同 X 新点上的实际作用仍待新点返回后单独判断。
