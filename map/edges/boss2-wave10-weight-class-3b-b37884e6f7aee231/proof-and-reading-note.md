# 有限全局可动权类的全体社会成本正则化输入证书

任务：`boss2-wave10-weight-class-3b-b37884e6f7aee231`。作者/实读核验：`Boss2-wave10-weight-class-formal-worker`。本笔记是本任务的一条输入类应用贡献的完整论证，不新建数学对象，不更改三条端点的定义或证明状态。

## 端点、问题与实际作用

记 F=`WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1`，T=`WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1`，R=`weighted-congestion/common-scale-full-welfare-regularization`。本边以 F、T 为 ALL 输入，终点为 R，作用限于给 R 提供一个已经解析付清共同尺度、资源边际和全体社会包络的具体输入类，并写出其应用公式。一般 R 对任意共同尺度势的证明仍由 R 自己的正文承担。R 不列入本边的 source_ids，不建立 ALL(F,T,R)⇒R 的循环，也不填写 whole_result。

F 已证明真正单策略玩家背景的精确吸收，但其自身 scope 明说不自动保持含固定玩家的社会包络。T 已证明有限全局权类的三角共同尺度势和严格改善下降。本笔记利用 T 中势的凸组合结构，独立补全系数为 1 的固定基线及其较强包络，并把它用于 R 的必用背景扩展所采用的“相关可选边际＋完整社会包络”证明。R 已有正确的 q_min b c(b) 通用修复；这里不是发现或修补 R 的缺陷。

## 模型、全局类别与社会目标

玩家集、资源集均有限；每个玩家权 w_i 为正实数，策略族 Σ_i 是非空有限资源子集族，允许空策略。费用 c_e(x)=Σ_{p=0}^d a_{e,p}x^p，a_{e,p}≥0，整数 d≥2。个体成本 C_i(s)=Σ_{e∈s_i}c_e(x_e(s))，不再乘其自身权；每个偏离重算包含该玩家的新真实负载。β-PNE 指对全部合法真实单方偏离有 C_i(s)≤β C_i(s′)。

只有 |Σ_i|=1 的玩家被吸收为固定玩家。它们的唯一策略可为任意资源子集，包括空集。在 e 上形成与状态无关的背景 B_e≥0。其余玩家组成 M，要求 M 非空，实际全局不同可动权值数为 k≥1，按 a_1>⋯>a_k 排序。所有资源使用同一类别标签；某资源缺类时只删空区段，不重新编号。固定玩家的权类不计入 k。仅有“某条路径中没有动”的玩家不符合本背景假设。

记 X_e(s)=Σ_{i∈M:e∈s_i}w_i 和 L_e(s)=B_e+X_e(s)。本应用采用

\[
 W(s)=\sum_{i\in N}w_iC_i(s)
     =\sum_e L_e(s)c_e(L_e(s)),\qquad \mathrm{OPT}=\min_sW(s).
\]

这是全体加权社会成本。W_M(s)=Σ_e X_e(s)c_e(B_e+X_e(s)) 则只计可动玩家，二者差为 Σ_e B_e c_e(B_e+X_e(s))，一般随状态变化；不加权 Σ_i C_i 又是另一个目标。固定玩家虽无可替换策略，其所支付成本仍可受可动玩家的负载外部性影响。

若输入只给可动权类数的上界，先按实际 k 构造下述 λ、S 和 A。不能把实际前缀尺度与另一个根的归一化混用。本任务不涉及窄簇取整、局部每资源权类数替代全局 k，或更细的逐资源必用用户压缩。

## 固定平移、三角混合与共同边际

F 的精确平移为 c'_e(x)=c_e(B_e+x)。其 x^r 系数为 Σ_{p=r}^d a_{e,p} binom(p,r) B_e^{p-r}，仍非负，次数不增。删除固定坐标与恢复各固定唯一策略给原状态空间的一一对应，每个可动玩家在每个状态及真实偏离后的费用逐项保持。

令 A=A_(d,k)∈[1,d) 为唯一满足

\[
 A=\sum_{j=0}^{k-1}\left(\frac{d-1}{A}\right)^j
\]

的根。存在唯一性由右侧减 A 在正轴严格递减、在 1 非负且在 d 负得到。设

\[
 t=(d-1)/A,\quad \lambda_r=t^{r-1}/A\ (1\le r\le k),
 \quad S_j=\sum_{r\le j}\lambda_r,\quad S_0=0.
\]

根方程给 λ_r>0、Σ_r λ_r=1、S_1=1/A、S_k=1，故 min_j S_j=1/A。没有使用无限几何级数，t<1、t=1、t>1 均无分母奇点。

对每个 r，按 π_r=(k,k−1,…,r+1,1,2,…,r) 将当前可动资源用户排序。类内可用固定玩家身份次序；等权相邻交换不改变势。若排列权序列为 v_1,…,v_n，u_ℓ=Σ_{q≤ℓ}v_q，则

\[
 P_{r,e}=\sum_{\ell=1}^n v_\ell c_e(B_e+u_\ell),
 \qquad F_e^{\rm opt}=\sum_{r=1}^k\lambda_rP_{r,e}.
\]

空序列给 F_e^opt(∅)=0。T 的真实插入和凸交换可直接用于 c'_e。为明确承重步骤，插入权 w、旧前缀 X、后缀权 v_ℓ 时，令 Y=X+w+Σv_ℓ、z_ℓ=X+w+Σ_{q≤ℓ}v_q，边际为

\[
 \Delta P=w c'_e(X+w)+\sum_\ell v_\ell[c'_e(z_\ell)-c'_e(z_\ell-w)].
\]

它非负。对单项式 x^p（1≤p≤d）用导数差界和 u=(X+w)/Y 得 ΔP≤wY^p[u^p+p(1−u)]≤d wY^p；常数项恰为 w 倍常数。凸交换使重先轻后的排序和不大于轻先重后；把插入者换至末尾时，删除它总恢复同一旧排序，故可合法比较边际。后缀全重给 ΔP≥w c'_e(Y)，后缀全轻给 ΔP≤w c'_e(Y)，后缀为空给等号。

对 class(i)=j 的可动插入，在 π_r 中分别有 r<j 全后缀更重，r=j 末尾，r>j 全后缀更轻。因此 T 的逐排序夹逼与混合给

\[
 S_jw_i c_e(B_e+Y)\le\Delta_i F_e^{\rm opt}
 \le[1+(d-1)S_{j-1}]w_i c_e(B_e+Y)
 =A S_jw_i c_e(B_e+Y).
\tag{1}
\]

最后等式用 1+(d−1)S_{j−1}=Σ_{q=0}^{j−1}t^q=A S_j。共同尺度 h_i=w_i S_class(i)>0 在该玩家的全部资源上相同。该解析证书对所有相关潜在可动用户子集和插入成立，无需待求的局部校准 YES 条件。

## 系数为 1 的固定基线与完整 W 包络

对任一排序、X=Σ_ℓ v_ℓ、L=B_e+X，单调性使每段积分不超过右端矩形：

\[
 \int_{B_e}^{L}c_e(z)\,dz
 \le P_{r,e}\le Xc_e(L).
\]

Σλ=1 且 λ≥0，所以同样有

\[
 \int_{B_e}^{L}c_e(z)\,dz
 \le F_e^{\rm opt}\le Xc_e(L).
\tag{2}
\]

这一步只需单调性；前节边际的排序交换才使用凸性。定义

\[
 \widehat F_e=F_e^{\rm opt}+B_ec_e(B_e),\qquad
 \widehat\Phi(s)=\sum_e\widehat F_e(T_e(s)).
\tag{3}
\]

新增 Σ_e B_e c_e(B_e) 是状态常数，不改变任何边际、偏离势差，也不改变给定 η 下的局部或全局最小点。对每资源，B_e c_e(B_e)≥∫_0^{B_e}c_e(z)dz，故由 (2)

\[
 \widehat F_e
 \ge B_ec_e(B_e)+\int_{B_e}^{L}c_e(z)dz
 \ge\int_0^{L}c_e(z)dz
 =\sum_{p=0}^d\frac{a_{e,p}L^{p+1}}{p+1}
 \ge\frac{Lc_e(L)}{d+1}.
\]

上界同样由 (2) 和单调性得

\[
 \widehat F_e\le B_ec_e(B_e)+Xc_e(L)
 \le(B_e+X)c_e(L)=Lc_e(L).
\]

逐资源求和便独立证明

\[
 \boxed{\frac{1}{d+1}W(s)\le\widehat\Phi(s)\le W(s)}.
\tag{4}
\]

因此本输入类可取 m=1/(d+1)、M=1。上述链在 X=0、B_e=0、纯固定资源、c_e≡0、全零社会成本时均成立，没有除以成本。它给充分包络，不宣称每个实例达到端点。

注意 \widehat F_e(∅)=B_e c_e(B_e) 一般非零；不能字面声称满足 R 开头的全用户归一化 F_e(∅)=0。实际使用的是 R 的“逐资源必用背景的全社会成本修复”节中明确允许的可选边际及完整 W 包络论证。R 通用恢复项 q_min b_e c_e(b_e) 已正确证明粗 m/M；本应用采用不同的系数 1，必须如上独立证明 (4)，不能只引用通用粗界。若为匹配该节的全玩家记号给固定玩家补 h_i/w_i=1/A，它们不产生可选插入义务，q_min=1/A；两种基线差为状态常数 (1−1/A)Σ_e B_e c_e(B_e)。常数平移保持最小点并不自动保持相同包络。

## 完整社会边际、倍率和真实偏离

令 G_e(T)=(B_e+X(T))c_e(B_e+X(T))。插入权 w_i 后完整负载 L，旧完整负载 z=L−w_i≥0。对 c(x)=x^p，包含 p=0，

\[
 L^{p+1}-z^{p+1}
 =w_i\sum_{q=0}^{p}L^{p-q}z^q
 \in[w_iL^p,(p+1)w_iL^p].
\]

非负系数相加给

\[
 w_ic_e(L)\le\Delta_iG_e\le(d+1)w_ic_e(L).
\tag{5}
\]

这是完整 G 的差，包含固定玩家成本的负载外部性；不能用仅可动玩家的 X c_e(B_e+X) 来冒名替换。

对每个有限实数 η≥0，设 Ψ_η=\widehatΦ+ηW。由 (1)、基线不变和 (5)，class(i)=j 的共同下尺度为 h'_i=w_i(S_j+η)>0，上尺度为 w_i(A S_j+η(d+1))。比值

\[
 r_\eta(S)=\frac{AS+\eta(d+1)}{S+\eta},\qquad
 r'_\eta(S)=\frac{\eta(A-(d+1))}{(S+\eta)^2}\le0.
\]

A<d<d+1，且最小 S 为 1/A，故这些界的最大比值恰为

\[
 \boxed{\beta_\eta=\max_{j=1,\ldots,k}r_\eta(S_j)
 =\frac{1+\eta(d+1)}{1/A+\eta}}.
\tag{6}
\]

η=0 时 r_0≡A，公式仍成立。最大值只取可动玩家/类别；固定玩家无非平凡偏离，其均衡约束恒真，任意另选固定玩家尺度不应改变所报倍率。(6) 是由本证书获得的充分稳定倍率，不声称为游戏真实最优近似率。

对一次可动玩家真实偏离，记删除、加入、保留资源的个体费用分别为 D,N,H≥0；C_i(old)=D+H，C_i(new)=N+H。保留资源用户集不变，完整负载也不变。删除用旧端点下界、加入用新端点上界，得

\[
 \begin{aligned}
 \Psi_\eta(s')-\Psi_\eta(s)
 &\le h'_i(\beta_\eta N-D)\\
 &=h'_i[\beta_\eta C_i(s')-C_i(s)-(\beta_\eta-1)H]\\
 &\le h'_i[\beta_\eta C_i(s')-C_i(s)].
 \end{aligned}
\tag{7}
\]

β_η≥A≥1，故最后一步合法。所有严格 β_η 改善都使 Ψ_η 严格下降；任何单方局部最小点都是 β_η-PNE。状态空间有限，全部这种严格改善路径终止且局部/全局最小点存在。空策略、正成本改至零、双零和平局由原不等式处理，不除成本；等号不强迫下降。

## 只有全局最小性支付社会质量

令 s_η 为 Ψ_η 的全局最小点，o 为 W 的全局最小点。由 (4)

\[
 \left[\frac1{d+1}+\eta\right]W(s_\eta)
 \le\Psi_\eta(s_\eta)
 \le\Psi_\eta(o)
 \le(1+\eta)W(o).
\]

因此

\[
 \boxed{W(s_\eta)\le
 \frac{1+\eta}{1/(d+1)+\eta}\,\mathrm{OPT}}.
\tag{8}
\]

左侧系数严格正。OPT=0 时该链直接推出 W(s_η)=0，不写 0/0。只有局部最小点时没有中间的全局比较，所以不能声称 (8)。若另有有效全局目标 gap，可按 R 独立的 gap 结论处理；本应用没有为任意局部最小点提供该证书。

η=0 时 (6) 返回 A 稳定、(8) 给 d+1 的充分质量界。k=1 时 A=1、λ_1=S_1=1，η=0 为精确稳定。有限 η>0 时 A≤β_η<d+1，质量系数介于 1 与 d+1；η=∞ 只可作为形式极限，不是本合同输入。d=0、1 用 T 的独立精确势端点，本应用不使用根公式。若 M=∅，原状态唯一，精确均衡且 W=OPT，单独处理，不定义 A_(d,0) 或空类最大值。

任意正实权、实系数以及可能无理的代数根 A 都由有限状态数学存在性处理。本笔记不承诺紧凑输入的多项式全局优化、位复杂度或多项式改善步数，也不认定外审、全球新颖性或更强全类稳定界。

## 本轮实读、继承记录和已有边的范围

本 worker 已读 AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md、任务全文及 registry 中三端点的完整记录。任务当前给定 input_pins 为 F=93d33edeb95f5257122583259d5347ea913e25f04dfefe41e9e5f281c1c2b704、T=1a0edceaed3cbc80e104df06697385be3406c7aa2b6eed26b2203f66c2609413、R=2064d4dcea77a85b0b3d5cd4a82fa4f44edcbc717a4f920fcc146fc65e9fe005；Boss 在派工时核对了最新领取与输入。worker 只读本地状态，不另作远端所有权承诺。

本轮六个不同源文件均已全文实读并核原字节 SHA256；审查和账本也在本轮全文读取，任务中特定 section 是最小定位而非本轮实际读取上限：

| 来源 | SHA256 | 实际用途 |
| --- | --- | --- |
| archives/weighted-congestion/state/定理/有限权类别三角排序势--定理.md | 4f6eb81eeda1730da6b72bdbc662ce5971ba0da66a0c040e02102231a4a3b7b2 | 全文：模型、根、排序插入/交换、共同乘子、真实偏离、固定背景及取整范围；本应用不用取整结论。 |
| archives/weighted-congestion/state/计算/有限权类网格与固定背景取整的作者核验--计算.md | 6e74512df2a8f064853e09b39c7cd71433fc63c8f6d308eabc9f1aa3344b834a | 全文：有限网格、四玩家背景例、计数和实现范围；不以有限核验代一般证明。 |
| archives/weighted-congestion/state/资料/拥塞结构势与规范形账本的全部陈述--资料.md | 9e14b51a1e19062674f69602052761645c99f10e0b55d0215e5e84a4adf2314d | 全文：共同模型、T/F/取整历史身份和量词；其它账本命题没有因此作为本应用前提。 |
| archives/weighted-congestion/state/审查/权类别排序势与共占高度的审查范围--审查.md | 5addca12a6cfc4cc59a84bbf40244d5f2ba884b4e3ea1401e195c7ead86a0b3a | 全文：三角承重代数、历史独立性和版本；两权/高度等无关历史不导入本边。 |
| archives/weighted-congestion/state/定理/共同尺度势的稳定与全社会成本正则化--定理.md | c55c041ea1d065a2b74e19ebb84a36cc1e53b42f62f37380a5ad1da07cd29a5f | 全文：一般输入、完整社会边际、增删保留证明、全局质量和已修复必用基线；终点是应用消费者。 |
| archives/weighted-congestion/state/定义/共同尺度稳定与社会质量的证书接口--定义.md | c17d6fb0d93bd42814ce807198beee8fc96217c38d317228ea52b3dbfb1c9a23 | 全文：共同尺度接口、W_M/全体 W 区别、局部/全局最小的不同保证。 |

已全文读父 Boss 的独立准备报告 research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/weight-class-full-welfare-independent-review.json，SHA256=9243280764def59be3693c0b92edd2f60e30b88d974bdf0d760a78c14031e500。该报告自身明说是读稿后独立代数/域核验而非独立发现或盲审，且其审查/账本读取范围分别只覆盖相关段落。本 worker 没把该报告的有限读取范围改称其已经全文读过；上述六文件全文范围是本 worker 本轮实际追加核验。报告不是正式 task receipt，不独立赋予覆盖信用。本轮未读其链接的历史程序源码、未复跑旧审计，也未把作者/独立计数合并成一般证据。

已全文比较以下两条已有 canonical 边及其精确 SHA：

1. map/edges/weighted-congestion-3a-3a-2e6caa865d8f839c/local-calibration-enables-full-welfare.json，SHA256=49032de3b81700293fc42a76c5711974b7efcff9f8b58861238a04be3fd646d4：源是有限局部校准，条件是实际获得全部相关可选插入边的局部 YES；应用的是通用 q_min 基线及粗包络。本任务解析给出有限 k 的尺度和单独重证的系数 1 包络，没有遗留该 YES 义务；两边输入和保证的具体参数不同。
2. map/edges/weighted-congestion-3a-3a-9fd1c1fae07348c6/triangular-potential-through-fixed-background.json，SHA256=ce3075ddc21f265bdea5c4d7cdd12bb7835e3ec26acd4429f832f9d3eca8e37d：已有 T→F 完整稳定迁移及严格 A 下降，scope 明确说含固定玩家的社会包络另证。本任务正提供此后与 R 联用的具体全体 W 输入及 η 权衡；旧边不需修复或替代。

此外按本地 registry.edge_files 检查了所有 source/target 命中 F/T/R 的边元数据、source/target、whole_result/contribution 和 canonical 清单身份，未见已经交付 F/T→R 的同一输入类应用；其它相邻边只做范围去重，没有声称全文重审其所有上游证明。此判断是本地快照，不冒充远端去重或发布核验。任务没有声明 overlap_comparisons，因此本轮三端点比较记录为 completed_in_scope_comparisons，不伪造 closed_overlaps，也没有未付 follow-up。

最终只需一条 accepted、unconditional、premises_mode=all 的 transfers contribution；unconditional 表示本域内解析证书与应用推导均已付清，不把域外任意共同势纳入。数学与证据均成熟；edge-bind、edge-check、Git checkpoint/push、队列 done 及全局覆盖集成由 Boss 串行完成。
