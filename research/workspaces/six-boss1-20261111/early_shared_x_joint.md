# 四个 actual source 共用同一最大 X 的可见隐藏尾层

Boss1；RUN `six-boss1-20261111`。本包只生成无点权重的精确必要层及未填写的固定点输入模板，不调用优化器、不修改 23676 行旧核心。原六人问题仍 OPEN。

## 1. 本轮结果和准确范围

固定实际路径的前四负载 `P`，选择一次全目录 `f_P` 最大合法标签 `X`。
在实际第 1、2、3、4 个 source 分别强制这同一个 X，并保存各自真实后继的全部
可见会员位。各分支共有 14 个新命名的尾标签角色，**不假定它们是 14 个互异目录标签**。
四源合计新增 **1920 个非负变量、128 条质量等式、436 条不等式**。
436 个原始来源行在精确稀疏向量意义下没有重复；去重映射仍完整保存。

| 实际 source i | 剩余人数 r | 中间标签数 m | 每 hist 状态数 | 新 μ 列 |
|---:|---:|---:|---:|---:|
| 1 | 6 | 4 | 64 | 1024 |
| 2 | 5 | 3 | 32 | 512 |
| 3 | 4 | 2 | 16 | 256 |
| 4 | 3 | 1 | 8 | 128 |
| 合计 | | | 120 | **1920** |

原 21021 列从最终描述符逐项保留，新列紧接在其后，合计 **22941 列**。
原 23676 条不等式只在右端补 1920 个零系数，完全保持旧行与旧归一化；追加后为
**24112 条不等式 + 128 条新等式**，另保原归一化一式。若不等式与新等式合计，
是 **24240 × 22941**，此数不包含原归一化和变量非负下界。

新不等式共 **163957** 个非零系数，新等式共 **2112** 个，合计 **166069**。
旧核心 3313758 个非零项保持原样；因而追加后的这两类行共 3479827 个非零项。
不把 1920 条非负变量下界另写成冗余单位矩阵。

**必要性的量词。** 以下公式对任意有限共同标签目录和任意完整纯 SPE 普遍成立。
本包继承旧核心固定的 16 个 hist 支持，因此这个具体有限矩阵包含的是其旧投影
落在该支持的所有真实 SPE。它没有声称 16 个 hist 能表示任意客户类型的 SPE。
即使新增层可行，也不认证完整 SPE。

## 2. 固定模型、索引语义与同一 X

采用[共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：
有限单位客户、有限非空共同标签目录、六个单位玩家、所有有序历史上的纯策略。
空覆盖、同覆盖异标签、重复行动及历史依赖的任意弱平局均保留。

记 actual 终局为 `(A1,…,A6)`。每名客户的六位会员为 `a1,…,a6`，令

\[
b_i=\sum_{j<i}a_j,\qquad P=\sum_{j=1}^4a_j,\qquad
f_P(Q)=\sum_{c\in Q}\frac1{P_c+1}.
\]

选定同一个全目录最大标签

\[
X\in\arg\max_{Q\in\mathcal L}f_P(Q),\qquad F_X=f_P(X).
\]

X 不随客户、hist、source、查询标签或分支背景重新选择。四个 source 的历史
分别是 `()`、`(A1)`、`(A1,A2)`、`(A1,A2,A3)`。

原直方图三位词的顺序由原始 `fourth_indexed_projection.py` 中
`PATTERNS=product((0,1),repeat=3)`、`new_reply_budget.py` 的 `(t,b,c)`
拆包，以及原字面标签构造器共同确定：

| 词位 | 原真实标签 | 精确身份 |
|---:|---|---|
| 0 | `T_k` | 原六元最优菜单的第 k 个合法标签 |
| 1 | `B_k` | `σ5(A1,A2,A3,T_k)` |
| 2 | `C_k` | `σ6(A1,A2,A3,T_k,B_k)` |

每个 hist 的六词计数给出 `d_T,d_B,d_C`。查询均值 `q=d_Q/6` 是六条合法
纯查询的固定平均，始终不是新添的分数行动。本包的新末标签写作 `T_at_sourcei`，
避免与原最优菜单 `T_k` 混淆。

## 3. 隐藏变量和两条不可替换的质量式

在 source `i` 强制 X 后，必须沿同一份完整策略的真实后继，依次得到
`Y1_at_sourcei,…,Ym_at_sourcei,T_at_sourcei`，其中 `r=7−i`、`m=r−2`。
最后一个 Y 总是第五位，T 总是第六位。记会员位为 `x,y1,…,ym,t`，引入

\[
\mu_{i,h,x,y_1,\ldots,y_m,t}\ge0.
\]

对每个 source、每个旧 hist，准确保留

\[
\sum_{y_1,\ldots,y_m,t}\mu_{i,h,1,y_1,\ldots,y_m,t}=x_h,
\qquad
\sum_{y_1,\ldots,y_m,t}\mu_{i,h,0,y_1,\ldots,y_m,t}=H_h-x_h.
\tag{M}
\]

这是 4×16×2=128 条等式；不是两种 x 的尾质量都等于 H。
其中 `H_h` 是原 hist 列，`x_h` 是原来的 16 个 common-X 列。
包括旧元数据记录的六个零 hist 在内，16 个 hist 全部保留，没有按旧点权重删列。

真实 SPE 直接按这些客户位分组产生 μ，因此满足 (M)。反过来，在每个
`(h,x)` 质量 `M>0` 上，可取四份尾边缘的条件乘积

\[
\nu_{h,x}(s_1,s_2,s_3,s_4)
=\frac{\prod_{i=1}^4\mu_{i,h,x,s_i}}{M^3}.
\]

`M=0` 时取零测度。它证明这些新尾边缘在共同 `(hist,X)` 上可合成一份测度，
但不证明原 R/Z 所有既有联合律、跨分支真实标签别名或全历史策略同时实现。
例如若 X=A_i，第 i 个强制分支就是 actual 的真实继续；若第四源 X=T_k，则其
`Y1_at_source4=B_k`、`T_at_source4=C_k`。有限必要层没有施加这些条件别名的
全部恒等约束；保留这一放松不损害必要性，但条件乘积不认证这些别名。
所以本包不增加需要跨两个强制 X 分支未知交叠的新 PAIR/RC 行。

## 4. 完整新增行域

以下每份预算在全客户求和后非负。除明确的份额差外，不将 IC 或 MAX 错当作
逐客户非负。实际收入 `u_j` 始终取原 actual 终局；新分支收入只从 μ 求出。

| 行族 | 数量 | 钱包 / 来源 |
|---|---:|---|
| 四个 source 的真实改 X IC | 4 | 对应原 actual `u_i` |
| 全六个 actual source 对 14 新尾标签的 SAFE | 84 | 对应原 actual `u_j` |
| 同一 actual P 的 MAX | 14 | 原 16X 列给出的 `F_X` |
| 全目录容量 | 14 | 原 `K` 列 |
| actual 倒二共同 X 封顶 | 14 | 原 actual `u5` |
| 四个强制 X 分支的真实末位 BR | 50 | 对应分支的真实末位收入 |
| 四个强制 X 分支的最后两位 PAIR | 96 | 对应分支两份收入及 self-tax |
| actual RC 的可见交叠行 | 160 | 原 actual `u5+F_X` |
| 合计 | **436** | |

### 4.1 原 source IC

强制 X 后 source i 的收益是

\[
v_i=\sum_{h,x,y,t}\mu_{i,h,x,y,t}
\frac{x}{b_i+1+\sum_\ell y_\ell+t}.
\]

分子 x=0 时取零；x=1 时分母正好是真实总负载。因此 `u_i−v_i≥0` 由原 source
的真实改 X 偏离直接给出，没有冻结实际后继。

### 4.2 六个 actual source 的 SAFE、MAX 与容量

对任意新尾合法标签 Q，以及任意 actual source `j=1,…,6`，令 `V_{j,Q}`
为在该原 source 改 Q 后沿 Q 自己真实后继得到的当前人收益。至多 `6−j` 位
后继还能覆盖一名 Q 客户，所以

\[
u_j-\sum_Q\frac1{b_j+7-j}
=(u_j-V_{j,Q})+
\left(V_{j,Q}-\sum_Q\frac1{b_j+7-j}\right)\ge0.
\tag{SAFE}
\]

j=6 没有后继，第二项为零，正是 actual 末位查询 Q 的真实 IC。
这里 Q 的会员由产生它的 μ 分支表示，但付款历史是原 actual source j；不把
那个产生分支的尾动作冻结到 Q 的偏离后。

每个 Q 还满足

\[
F_X-\sum_Q\frac1{P+1}\ge0,\qquad K-|Q|\ge0.
\tag{MAX/CAP}
\]

所有 MAX 均使用同一个 actual P，而不是各自强制分支背景。

### 4.3 分支真实末位 BR

在真实五步历史 `actual-before-i, X, Y1,…,Ym`，对合法查询 Q 有

\[
\sum\mu_i\frac{t-q}{b_i+x+\sum_\ell y_\ell+1}\ge0.
\tag{BR}
\]

查询为 X、六个 actual A、该分支全部 m 个中间 Y，以及 T/B/C 三组六标签平均。
四源分别有 14、13、12、11 条，共 50 条。对均值，分母不依赖旧菜单索引，
因此六条 IC 的平均逐客户恰给 `q=d_Q/6`，没有假设任何会员独立性。

### 4.4 分支 PAIR：三条真实 IC 加 self-tax 非负差

令 `z=y_m`。真实最后两位前缀包含 X 及前 `m−1` 个中间 Y，准确背景为

\[
p=b_i+x+\sum_{\ell<m}y_\ell,\qquad d=p+1\in\{1,\ldots,5\}.
\]

定义 `f(L)=Σl/d`、`g(L,R)=Σlr/[d(d+1)]`、`U(L,R)=f(L)−g(L,R)`。
令分支实际最后两标签为 Z、T，收入为 `s=U(Z,T)`、`w=U(T,Z)`。
第五位改 L 后的真实末回复 `J_L=σ6(this exact prefix,L)` 给出恒等式

\[
\begin{aligned}
TP(L,R)&=s+w+g(Z,Z)-f(L)-f(R)+g(L,R)\\
&=[s-U(L,J_L)]+[U(J_L,L)-U(R,L)]\\
&\quad+[w-U(J_L,Z)]+[g(Z,Z)-g(Z,J_L)]\ge0.
\end{aligned}\tag{TP}
\]

前三项是同一真实回复 J_L 对应的三条完整历史 IC。最后一项是
`Σz(1−j_L)/[d(d+1)]≥0`。全过程没有用 actual `u5` 或 `u6` 代替分支收入。

记局部钱包

\[
H=\frac z{d+t}+\frac t{d+z}+\frac z{d(d+1)}.
\]

本包保留的三个系数为

\[
\begin{aligned}
TP(Q,X)&:H-\frac{q+x}d+\frac{qx}{d(d+1)},\\
TP(Q,Q)&:H-\frac{2q}d+\frac q{d(d+1)},\\
TP(X,X)&:H-\frac{2x}d+\frac x{d(d+1)}.
\end{aligned}
\]

Q 取六个 A、该分支全部中间 Y、三组旧索引均值；每分支另留一份 TP(X,X)。
四源分别 27、25、23、21 条，共 96 条。均值对角是平均 `(Q_k,Q_k)`，故
交叠为 `average(q_k²)=q`，**不是 q²**；与 X 的交叠则是 `xq`。

### 4.5 actual cap 与 actual RC：两条 IC 加同一 MAX

这两类使用 actual 四步历史、原实际 `u5` 和同一个 `F_X`，与上节分支 TP
有不同的钱包。它们重用[旧共同潜力 owner](../../../archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md)，
不将既有引理重新声明为本轮新定理。

记 `U_P(L,R)=f_P(L)−g_P(L,R)`。若 `V=σ6(actual h4,X)`，则

\[
u_5-U_P(Q,X)
=[u_5-U_P(X,V)]+[U_P(V,X)-U_P(Q,X)]+[F_X-f_P(V)]\ge0.
\tag{MX}
\]

因此每个新尾 Q 都有一条准确的 `u5≥Σμ_i q/(P+1+x)`，共 14 条。

若改选 Q 后的真实末回复为 `V_Q=σ6(actual h4,Q)`，则

\[
\begin{aligned}
u_5+F_X-f_P(Q)-f_P(R)+g_P(Q,R)
={}&[u_5-U_P(Q,V_Q)]\\
&+[U_P(V_Q,Q)-U_P(R,Q)]+[F_X-f_P(V_Q)]\ge0.
\end{aligned}\tag{RC}
\]

这里是两条 IC 加 MAX，不是三条 IC。取同一分支 5/4/3/2 个新尾标签的
无序含自对，分别有 15/10/6/3 条，共 34 条；再取每个新尾 Q 配六个 actual
和三组 indexed 均值 R，有 14×9=126 条，合计 160 条。
新尾与均值的交叠是 μ 中 `q·d_R/6`；自对的位乘积仍是 q。不同强制分支之间
未保存的会员交叠没有被条件乘积臆造为真交叠。

## 5. 旧核心、输入字节和可接续格式

构造器实读两个当前描述符来源：`maxb_augmented_lp/full_lift/exact_matrix.json.gz`
与 `common_x_joint_lp/final/exact_matrix.json.gz`。前 20601 列逐项相同；最后
420 列在最终描述符中只增加已冻结的真实边缘语义字段，旧字段逐项不变。
本包完整复制最终 21021 个描述符后追加 μ，没有重写任何原坐标。

新增行只用原来的 16 个 hist、16 个 X 和 K，共 33 个旧列；旧 R/Z 与其它
辅助列的新增系数全部为零。所有旧输入在构造前后逐文件 SHA 检查保持相同。

| 文件 | 用途 |
|---|---|
| [build_layer.py](early_shared_x_joint/build_layer.py) | 点无关生成器；标准库精确分数，无优化器 |
| [symbolic_append.json.gz](early_shared_x_joint/symbolic_append.json.gz) | 1920 列、436 行、128 等式及逐行钱包/历史/查询来源 |
| [columns_22941.json.gz](early_shared_x_joint/columns_22941.json.gz) | 保全旧描述符的完整 22941 列顺序 |
| [base_coordinate_contract.json](early_shared_x_joint/base_coordinate_contract.json) | 16 hist、共同 X、actual 收入、F_X 与原标签身份 |
| [fixed_point_feasibility_template.json.gz](early_shared_x_joint/fixed_point_feasibility_template.json.gz) | 自足的 1920 变量固定点模板，全部右端仍为旧列的符号线性式 |
| [main_point_release_template.json](early_shared_x_joint/main_point_release_template.json) | 留空的 Main 下一 23676 精确点绑定格式 |
| [fill_fixed_point_template.py](early_shared_x_joint/fill_fixed_point_template.py) | 只绑定明确给出的全 21021 维有理向量；不查找点、不求解 |
| [audit/proof_review.md](early_shared_x_joint/audit/proof_review.md) | 独立付款与定义域审查 |
| [audit/verify_independent.py](early_shared_x_joint/audit/verify_independent.py) | 不导入生成器的字面重建核验 |

完整来源字节见 [source_manifest.json](early_shared_x_joint/source_manifest.json)。
最终冻结清单和所有输出 SHA 见包内 `freeze_manifest.json` / `SHA256SUMS`。

## 6. 固定点模板和不变的解释边界

模板当前没有旧点值，`point_binding.old_vector=null`、无目标、无优化器授权。
只在 Main 明确提供**下一份同一 23676×21021 矩阵的精确点**后才能填写。
绑定器要求 Main release 引用、精确点 SHA、相同旧矩阵/描述符 SHA，以及全部
21021 个非负有理数字符串；浮点数、缺失向量和空 release 都拒绝。

每条新增行分成 `A_mu·mu ≥/＝ b_old(v)`。固定原向量后，绑定器只用标准库
分数计算右端并生成可复核输入，不调用任何求解器。它检查形状、归一化及 H/X
边界；全部 23676 旧行的精确可行性仍由 Main 的旧点证书承担。

若将来该固定输入不可行，只排除所绑定的完整旧向量扩展，包括其中已经固定的
X 和 overlap 值；不自动排除重选 X、重选旧真实边缘或整个旧最优面。
若可行，只得到这份小可见层的必要可行性；没有补全所有历史或证明 SPE。

## 7. 从真实隐藏尾预算精确收回 36 条可见前缀行

Main 追加的小型承重检查已完成：只取六个 actual A 和 T/B/C 三组索引均值，
从本包 436 个预算和 μ 非负性、质量式中，逐向量投影出前三源各九条 C* 行，
以及第四源九条 H3 行。没有添加新列、约束或目标，也没有改动原 append 包。

统一记 `n=b+1`、`k=P−b`、`j=Σy`、`D=b+r`。采用下列固定非负预算权：

| source | source IC α | 每个中间 SAFE s_Y | 末 SAFE s_T | 每个中间 MAX a_Y | 末 MAX a_T | C |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 25 | 51/20 | 6 | 3/8 | 0 | 206/5 |
| 2 | 20 | 7/4 | 5 | 3/5 | 0 | 121/4 |
| 3 | 15 | 2/3 | 4 | 1 | 0 | 61/3 |
| 4 | 10 | 0 | 0 | 1 | 2 | 10 |

每份分支 terminal-BR 的权为 1，且 `C=α+m s_Y+s_T`。相应逐状态余项为

\[
\begin{aligned}
E={}&\frac{\alpha x}{n+j+t}+\frac{s_Yj+s_Tt}{D}
-\frac{(C-1)x}{D}-q\left[\frac xD+\frac{1-x}n\right]\\
&-\frac{a_Y(mx-j)+a_T(x-t)}{n+k}
-\frac{t-q}{n+x+j}\ge0.
\end{aligned}
\]

前三源正是已证明的 [Main SAFE/MAX 家族](main_prefix_safety_maxx_family.md)，
第四源正是 [H3](maxb_h3_bridge.md) 的 `10 IC+MAX(Y)+2 MAX(T)+BR`。
对每个 h,x，将预算行加 `ΣEμ` 后的剩余 μ 系数在全部尾状态上相同。
加质量式 (M) 的非负系数

\[
\beta_{h,x}=\frac{(C-1)x}{D}
+q\left[\frac xD+\frac{1-x}n\right]
+\frac{(m a_Y+a_T)x}{P+1}
\]

即可把全部新列精确消尽，得到原 21021 列上的

\[
C u_i-(C-1)\sum_h\frac{x_h}{b_i+r}
-\sum_h\frac{q_h H_h}{b_i+1}
+\sum_h\frac{(r-1)q_hx_h}{(b_i+1)(b_i+r)}\ge0.
\]

等式乘子本来允许任意符号；这里展示的系数恰也非负。对均值查询 q，E 对 q
仿射，已逐状态核 `E(q)=(1−q)E(0)+qE(1)`。共有 1568 个完整合法 Boolean
余项型：640/512/288/128，各源零余项分别 48/54/52/39，全部非负。
36 份具体向量恒等式另核 17280 个保存的 μ 余项以及 1152 项质量式付款。

独立实现没有导入上述投影器，也直接从 literal budget 重建同样的 36 个目标。
27 条目标逐向量等于冻结 `main_prefix_maxx_interface/rows_51.json` 中对应条目；
九条 H3 逐向量等于冻结 `maxb_h3_bridge/rows_17.json` 中对应条目。
**其余八个 R/Z/H 查询轨道没有建模；这不是完整 51 条或完整 17 条接口的支配声明。**

投影的完整非负付款、零/非零余项、质量式系数及旧目标行保存在
[visible_prefix_projection.json.gz](early_shared_x_joint/visible_prefix_projection.json.gz)；
全 1568 型表保存在
[visible_prefix_all_type_remainders.json.gz](early_shared_x_joint/visible_prefix_all_type_remainders.json.gz)。
生成器为 [project_visible_prefix_rows.py](early_shared_x_joint/project_visible_prefix_rows.py)，
独立入口为 [audit/verify_visible_projection.py](early_shared_x_joint/audit/verify_visible_projection.py)。

## 8. 验证、冻结与接续

独立 literal 审查已逐项重建 436 条稀疏向量、128 条质量等式、1920 个隐藏列，
并核对全部 564 条固定模板的 μ 局部索引和旧右端负号。它另从原份额直接核
全部 7680 个 actual/尾客户型、240 个 SAFE 偏离域、160 个 PAIR 三 IC 恒等式、
320 个 MX 与 320 个 RC 付款恒等式，以及 2560 种六索引平均。

无点入口检查已确认未填写的 Main release 被拒绝，模板仍为 null，未创建任何
已填固定点文件。完整 PASS 记录分别见
[audit/independent_verification.json](early_shared_x_joint/audit/independent_verification.json)、
[audit/visible_projection_verification.json](early_shared_x_joint/audit/visible_projection_verification.json)
和 [template_entry_verification.json](early_shared_x_joint/template_entry_verification.json)。

本层不重做已经精确闭合的 universal-C 系数锥，不读取旧点来调系数，不等待
云端计算。通用层在来源与字面两侧审核通过后冻结释放；下一动作仅是 Main
给出新的 23676 精确点后按明确授权另填固定点输入，不在本轮求解。
