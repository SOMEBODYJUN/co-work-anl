# 四源可见菜单的全 PAIR 闭包与 31／25／19 平均前缀投影

Boss1；RUN `six-boss1-20261111`。本轮只写新目录及本稿。
原 [early_shared_x_joint](early_shared_x_joint.md) 的 1920 列、436 行、128 质量式、
固定点模板和 36 条投影证书全部保持冻结。本轮无数值点、无优化器。

## 1. 已得到的可接续结果

在每个强制 X 分支的同一真实最后两位前缀，补齐所有可见查询描述符的无序含自对
PAIR。共 **394 个候选**，逐精确向量分类如下。

| 分类 | 数量 |
|---|---:|
| 与旧 436 行完全相同 | 84 |
| 零向量 | 0 |
| 候选内部精确重复 | 0 |
| 直接由 μ 每坐标非负推出 | 4 |
| 按上述直接标准保留的新增候选 | **306** |

394 个候选向量全部互异。可用的 306 行共 **131721 个非零系数**，**没有新列、
没有新等式**，全部在已有 22941 列顺序上表示。保留旧 436 行后，不等式总数为
**24418**；另保原 128 条质量等式、原归一化和全部变量下界。

306 是直接过滤后的精确候选集，不是独立锥射线的声明。另已明确证明其中 **42 条**
由旧末位 BR 加 μ 非负性推出，并保存完整付款。若采用这份附加消冗证书，可只留
**264 行、116034 个非零系数**而保持对全部 306 行的蕴含。此视图的 GE 尺寸为
**24376×22941**，仍保原 128 条质量式；没有声称 264 行已经进一步不可约。

同时从**旧 436 行**单独投影出九条新平均前缀行：前三源各有 T/B/C 三条，常数
分别为 **31、25、19**。这些投影不需要新 PAIR 行，所有 Π 修正按原公式保存。
当前支持上三条 T 平均没有修正；B 平均的修正也恰为零，但仍保留通用 Π 定义。
C 平均有四个非零 Π，见第 6 节。

## 2. 原模型、可见角色和真正最后两位前缀

采用有限单位客户、有限非空共同标签目录、六个单位玩家与完整有序历史纯 SPE。
固定 actual 路径 `(A1,…,A6)`，按 actual 前四负载 P 只选一次全目录 `f_P`
最大合法 X。允许空覆盖、同覆盖异标签、重复行动及任意历史依赖弱平局。

对 source `i=1,2,3,4`，`r=7−i`、`m=r−2=5−i`。强制 X 后的真实尾角色为
`Y1,…,Ym,T`，其中 Z=`Ym` 是第五位，T 是第六位。全部新尾共有 14 个命名角色，
不假设它们是互异标签，也不假设它们与 X、A 或旧菜单标签不同。

本次 PAIR 的真实前缀始终是

\[
h_i=(A_1,\ldots,A_{i-1},X,Y_1,\ldots,Y_{m-1}).
\]

它准确有四个行动。对客户设原 source 背景为 b，X 位为 x，中间位为 y，末位为 t。
记

\[
p=b+x+\sum_{\ell<m}y_\ell,\qquad d_{\rm loc}=p+1\in\{1,\ldots,5\},\qquad z=y_m.
\]

每源的可见纯角色为

\[
\{X,A_1,\ldots,A_6,Y_1,\ldots,Y_m,T\},
\]

共 `m+8` 个；再加入 T/B/C 三个六索引菜单描述符，共 `m+11` 个。
这些菜单描述符只是合法纯查询的平均方式，不增加分数行动。

| source | 纯角色数 | 含三菜单后的描述符数 | 无序含自对候选 |
|---:|---:|---:|---:|
| 1 | 12 | 15 | 120 |
| 2 | 11 | 14 | 105 |
| 3 | 10 | 13 | 91 |
| 4 | 9 | 12 | 78 |
| 合计 | | | **394** |

所有查询位或旧菜单会员计数都在同一个 μ 分支中可见。本包不加入不同强制 X 分支
之间的交叠，也不扩展旧 R/Z 或其它未观测标签。

## 3. 任意两纯查询的真实三 IC 付款

在固定真实前缀 h_i，定义

\[
f(L)=\sum_c\frac{l_c}{d_c},\quad
g(L,R)=\sum_c\frac{l_cr_c}{d_c(d_c+1)},\quad U(L,R)=f(L)-g(L,R),
\]

其中此节的 d=`d_loc`。真实最后两标签为 Z、T，分支收入记
`s=U(Z,T)`、`w=U(T,Z)`。对于任意合法纯查询 L、R，令
`J_L=σ6(h_i,L)` 为在这个准确前缀改 L 后的真实末回复。则

\[
\begin{aligned}
TP(L,R)&=s+w+g(Z,Z)-f(L)-f(R)+g(L,R)\\
&=[s-U(L,J_L)]
 +[U(J_L,L)-U(R,L)]\\
&\quad+[w-U(J_L,Z)]
 +[g(Z,Z)-g(Z,J_L)]\ge0.
\end{aligned}\tag{TP}
\]

前三项分别是该第五 source 的真实 IC、偏离 L 后真实末节点的 IC、原真实末节点
对合法 J_L 的 IC。最后一项为 `Σ z(1−j_L)/[d(d+1)]≥0`。
所有收入都来自这个 μ 分支，没有使用 actual u5、actual u6 代替。

逐 μ 状态，局部钱包是

\[
H=\frac z{d+t}+\frac t{d+z}+\frac z{d(d+1)},
\]

纯查询系数为

\[
H-\frac{l+r}{d}+\frac{lr}{d(d+1)}.
\tag{K}
\]

因为 g 对称，最终行对 L、R 对称，所以枚举无序描述符对足够；付款分解仍使用
选定方向的同一真实 `J_L`。若两个角色实际为同一标签，恒等式仍然成立。

## 4. 完整 6×6 平均与旧同索引对角不能混用

旧 hist 的词仍是 `(T_k,B_k,C_k)`，分别对应合法最优菜单标签及在原前三历史下
强制 T_k 后的真实第五、第六回复。每客户对六个标签的会员数 `d_T,d_B,d_C`
由 hist 确定。写菜单 S 的平均位 `θ_S=d_S/6`。

### 4.1 纯／纯及纯／菜单

纯查询的交叠用两个保存位的乘积。纯 L 与菜单 R 的六条平均交叠为

\[
\frac16\sum_k l r_k=l\theta_R.
\]

分支钱包和分母都不随查询索引改变，故直接把式 (K) 的 r 换为 θ_R 即得精确行。

### 4.2 菜单／菜单：全部 36 个有序索引对

本次对菜单 S、R 使用

\[
\frac1{36}\sum_{k=1}^6\sum_{\ell=1}^6 TP(S_k,R_\ell).
\]

每名客户上，分配律给

\[
\frac1{36}\sum_{k,\ell}s_kr_\ell
=\frac{(\sum_ks_k)(\sum_\ell r_\ell)}{36}
=\theta_S\theta_R.
\]

这是全体有序索引对的精确求和，不是假设两个会员事件独立。包括 S=R 时，仍按
全部 36 对求和，因此平均交叠是 **θ_S²**。各标签重复或别名不影响这个等式。

旧 436 行中的 `TP(Q,Q)` 菜单对角则是
`(1/6)Σ_k TP(Q_k,Q_k)`，其交叠为 `average(q_k²)=θ_Q`。
两种平均都合法，但不是同一行。它们的准确关系为

\[
TP_{\rm diagonal}(Q,Q)-TP_{\rm full36}(Q,Q)
=\sum\mu\frac{\theta_Q(1-\theta_Q)}{d_{\rm loc}(d_{\rm loc}+1)}\ge0.
\tag{D}
\]

所以完整 36 对自配行用更小的左端给出更强的必要不等式。12 份差向量已经逐项
保存与核验；旧 12 行的物理字节仍保留。这里没有声称这种逐点支配已构成相对于
整个旧系统的严格可行域分离。
Main 的独立[全配对平均稿](main_full_average_pair.md)使用同一真实三 IC 付款和
字面 36 对分配律；本包没有把那里的并集弱化另冒作当前重数平均行。

## 5. 分类、可用 append 与明确的 42 条 BR 冗余

所有候选只在 1920 个 μ 列上有系数。任一非零候选不可能等于原 23676 行的
零延长，因为后者在全部 μ 列上为零；因此无需为了这次精确重复判定重新扫描
旧大矩阵。零向量单独分类，本次数量为零。

与旧 436 行的逐分数向量比较得到 84 份精确重复，恰是旧 96 PAIR 中除去
12 个同索引菜单对角的部分。全部 394 候选向量互异，没有族内重复。
只有四条向量在每个 μ 坐标上均非负：各分支的 `TP(Z,T)`，其系数正是
`z(1−t)/[d(d+1)]`，故直接省去。

每个原始对都保存源、两查询、平均规则、向量组、旧行匹配、平凡性标记以及 append
行号；没有只保筛选后的列表而丢失原始映射。使用的“重复”是完整有理向量相等，
不是仅比较行名、支撑、采样值或某个固定点。

直接过滤留下的 306 行还包含以下可明确证明的锥冗余。对该分支 penultimate Z
和任意可见 R，展开式 (TP) 得

\[
TP(Z,R)=\underbrace{w-U(R,Z)}_{\text{旧真实末位 BR(R)}}
 +g(Z,Z)-g(Z,T).
\tag{BRR}
\]

最后差仍是 `Σμ z(1−t)/[d(d+1)]≥0`。在 306 集内，R 为六个 actual、前
`m−1` 个 Y 或三个菜单，各源有 `m+8=12/11/10/9` 条，总计 **42 条**。
R=X 或 Z 的行已经在旧重复类中；R=T 正是上面的四条直接平凡行。

[direct_BR_redundancy.json.gz](early_shared_x_menu_pair_closure/direct_BR_redundancy.json.gz)
保留 42 份完整向量恒等式和可省略／保留行号。因此可选用 264 行视图并推出
全部 306 行。原 306 文件保持不变；不把这次有限消冗扩展成对 264 的锥独立认证。

## 6. 九条 31／25／19 平均前缀行及精确 Π

采用 [Main 平均前缀稿](main_averaged_menu_prefix.md) 的普遍预算。对 source
`i=1,2,3` 记 `r=7−i`、`m=r−2`、`n=b+1`、`k=P−b`、`D=n+r−1`。
菜单重数为 d_Q，`θ=d_Q/6`。取

| source | 原 source IC α | 末 SAFE 权 r | 每个中间 MAX 权 a* | C=α+r |
|---:|---:|---:|---:|---:|
| 1 | 25 | 6 | 4/5 | **31** |
| 2 | 20 | 5 | 19/20 | **25** |
| 3 | 15 | 4 | 7/6 | **19** |

再给原分支 terminal 平均 BR 权 1。所有这些行已经在旧 436 中；不需要本轮
新 PAIR。原 source IC、末 SAFE、MAX 和 BR 的钱包/真实历史与旧包完全一致。
末 SAFE 仍须回到原 source 改末标签后沿它自己的真实后继。

定义

\[
\Pi_i(n,k,d_Q)=\max_{0\le j\le m}
j\left[\frac{d_Q}{6n(n+j)}-\frac{a_*}{n+k}\right].
\tag{P}
\]

j=0 保证 Π 非负。目标为

\[
C u_i-(C-1)\kappa_i(X)-L_{\rm av}
+\sum_h\Pi_i(n_h,k_h,d_Q(h))(H_h-x_h)\ge0,
\tag{AM}
\]

其中 `κ_i=Σ_h x_h/D_h`，
`L_av=Σ_h θ_h H_h/n_h−Σ_h(r−1)θ_hx_h/(n_hD_h)`。
修正只作用于 X=0 质量，不能写成 ΠH 而漏掉 −Πx。

### 6.1 全类型余项与必要性

令 j=`Σy`，目标去掉 Π 后减去上述预算，逐客户余项为

\[
E=\frac{\alpha x}{n+j+t}+\frac{rt}{D}
-\frac{(C-1)x}{D}-\theta\left[\frac xD+\frac{1-x}n\right]
-\frac{a_*(mx-j)}{n+k}-\frac{t-\theta}{n+x+j}.
\]

实际加入非负变量付款的系数是

\[
\rho=E+(1-x)\Pi_i(n,k,d_Q)\ge0.
\]

其完整域是 `1≤n≤i`、`0≤k≤m`、`d_Q∈{0,…,6}` 和全部有序隐藏位。
非负性的四角理由如下。

1. x=1 时 θ 的系数 `1/(n+1+j)−1/D≥0`，MAX 负项在 k=0 最差。
   对 t=1，设 z=m−j，余项下界为
   `z[(α−1)/((n+j+1)D)−a*/n]`。凸函数
   `G(n)=a*(n+m)(n+r−1)/n` 的两个端点值均不大于 α−1。
   对 t=0，设 e=n+m≤5、B=a*D/n；乘 D 后下界为
   `α(z+1)/(e−z)−(r−1)−zB`。z=0 项非负，增量由 `eB≤α−1`
   下界为 `z(α+e)/e²≥0`。故 x=1 不需修正。
2. x=0、t=1 时，
   `E≥a*j/(n+k)+r/D−1/n≥0`。
3. x=0、t=0 时恰有
   `E=j[a*/(n+k)−d_Q/(6n(n+j))]`，由 (P) 得 E+Π≥0。

因此 Π 是这组固定权下、固定 n,k,d_Q 后覆盖全部 X=0 真实尾状态所需的最小
非负逐客户修正；这不是完整 SPE 的锐性声明。全 154 份 Π 表保留所有取到最大值
的 j，不丢弃平局。

### 6.2 用旧质量式消去 μ 的精确证书

逐预算相加再加 `Σρμ` 后，每个 `(hist,x)` 的剩余 μ 系数不依赖尾状态。
给对应质量等式的系数

\[
\beta_{h,x}=\frac{(C-1)x}{D}
+\theta\left[\frac xD+\frac{1-x}n\right]
+\frac{m a_*x}{P+1}-(1-x)\Pi_i(n,k,d_Q)
\]

即可把全部 μ 列消尽，得到 (AM) 的原坐标向量。证书保存 **54 个非负预算付款项、
5376 个含零 E/Π/ρ 记录、288 项质量式付款**；没有拿数值点替代向量恒等式。

另外逐项核了纯系数接口

\[
\text{new}_i=\text{old}_{C_i^*}
-\Delta_i\,[u_i-\kappa_i(X)]
+\sum_h\Pi_i(H_h-x_h),
\quad (\Delta_1,\Delta_2,\Delta_3)=(51/5,21/4,4/3).
\]

这条接口只检查坐标一致；新行的合法性来自上面的真实付款和 ρ 非负，不能从
“旧非负式减非负量”推断。

当前固定 16 hist 的 `d_T=1`，所以三条 T 平均 Π=0。B 的 Π 在这组支持上也全零。
C 的四个非零值为：

| source | hist 列 | X 列 | n | k | d_C | Π |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 449 | 20595 | 1 | 2 | 6 | 7/30 |
| 1 | 524 | 20598 | 1 | 3 | 6 | 3/10 |
| 2 | 449 | 20595 | 1 | 2 | 6 | 11/60 |
| 3 | 449 | 20595 | 1 | 2 | 6 | 1/9 |

这些项全部保留；不因旧材料曾将这些 hist 标为零质量而删除。

## 7. 覆盖并桥与固定支持边界

[Main 覆盖并稿](main_optimal_union_prefix.md) 的无罚并集目标不同于任意重数平均。
对于任意六个合法查询，写 `o=1[d_Q>0]`。真实末位的六次查询平均可减弱为

\[
w-\sum\frac{o}{6d_{\rm last}}
=\left[w-\sum\frac{d_Q}{6d_{\rm last}}\right]
+\sum\frac{d_Q-o}{6d_{\rm last}}\ge0.
\]

把 θ 改为 `o/6∈{0,1/6}` 时上节余项无需 Π，即得到普遍的覆盖并前缀界；
不把并集 U 作为合法动作，不删除 U 外客户，也不把重叠主题切成目录外片段。
任意 OPT6 菜单可以用于这个桥，但不能据此宣称其原重数平均自动无罚。

当前支持 d_T=1，使字面 T 平均与对应并集目标一致；这只是本固定支持的接口
便利。PAIR 公式和 (AM) 付款普遍必要，但本次 22941 列矩阵仍是旧 16 hist 支持的
必要提升，不是任意类型实例的完整 SPE 表征。

## 8. 验证、文件和接续

PAIR 构造逐项核了 **209920 个隐藏状态系数**，并按原六词展开 **937600 个字面
有序查询对**：纯/纯 133504 个状态，纯/菜单 64896 个状态，菜单/菜单 11520 个
状态。全三 IC + 非负差在一般合法背景成立；这些计数检查的是实现，而不是
客户可实现性或全局福利证明。

九前缀投影的全部 **5040 个合法修正余项**均非负：523 个零、4517 个正。
154 份 Π 全等于直接遍历 X=0 尾域得到的最小修正；5376 个保存态余项为
503 个零、4873 个正。同一 5040 域上的覆盖并弱化与 θ=o/6 余项也全部非负。

独立审查程序不导入本包生成器；它另造所有候选、分类和九个目标，并逐项核对
已保存的向量、映射、Π 表、付款证书及 42 条 BR 冗余。
全部检查已 **PASS 并冻结**；完整结果见
[PAIR 独立结果](early_shared_x_menu_pair_closure/audit/independent_verification.json)、
[九投影独立结果](early_shared_x_menu_pair_closure/audit/averaged_prefix_verification.json)
和[独立审稿](early_shared_x_menu_pair_closure/audit/independent_review.md)。

| 文件 | 内容 |
|---|---|
| [all_pair_candidates.json.gz](early_shared_x_menu_pair_closure/all_pair_candidates.json.gz) | 全 394 对、完整向量组、来源与筛选映射 |
| [usable_pair_append.json.gz](early_shared_x_menu_pair_closure/usable_pair_append.json.gz) | 306 条直接过滤后的可用精确行；零新列 |
| [diagonal_menu_dominance.json.gz](early_shared_x_menu_pair_closure/diagonal_menu_dominance.json.gz) | 12 个 full36 相对旧对角的非负差 |
| [direct_BR_redundancy.json.gz](early_shared_x_menu_pair_closure/direct_BR_redundancy.json.gz) | 42 个精确 BR 支配式及 264 行保留视图 |
| [averaged_prefix_rows_9.json](early_shared_x_menu_pair_closure/averaged_prefix_rows_9.json) | 九条新前缀行与逐 hist Π；与 PAIR append 分开 |
| [averaged_prefix_projection.json.gz](early_shared_x_menu_pair_closure/averaged_prefix_projection.json.gz) | 九份从旧 436 行投影的完整精确证书 |
| [averaged_prefix_full_domain.json.gz](early_shared_x_menu_pair_closure/averaged_prefix_full_domain.json.gz) | 全 154 份 Π 和 5040 个余项域 |
| [build_pair_closure.py](early_shared_x_menu_pair_closure/build_pair_closure.py) | PAIR 构造与直接分类 |
| [project_averaged_prefix.py](early_shared_x_menu_pair_closure/project_averaged_prefix.py) | 九行与 Π 付款生成器 |
| [identify_direct_BR_redundancy.py](early_shared_x_menu_pair_closure/identify_direct_BR_redundancy.py) | 42 条无优化消冗恒等式 |

原 436 层、128 质量式和旧 36 证书没有任何修改。新行仍未对数值点评价，也未
运行固定点可行性或全局优化；所有数值发现与后续装配均须是 Main 的下一项明确任务。
