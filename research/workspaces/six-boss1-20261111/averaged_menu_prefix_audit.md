# 六菜单平均前缀界：普遍罚项、19/25/31 受限锥及完整最优面审核

Boss1；RUN `six-boss1-20261111`。审核对象为
[Main 六菜单平均稿](main_averaged_menu_prefix.md)及其 `.py/.json`。
本包只写全新 `averaged_menu_prefix_audit/` 与本稿；不改任何先前冻结文件。

## 1. 审核结论

**Main 的普遍带罚项结论、强化参数 a*、零罚项条件、粗上界以及固定 θ=1/6 锥最优值全部正确。**
没有发现需要修复的数学错误。以下三种结论必须保留不同的范围：

1. 对任意六个合法标签，使用显式 Π 的普遍不等式成立。
2. 对 X 外客户满足适当菜单重数上限时，Π 才能统一删去。
3. 固定每型 θ=1/6 的完整非对称系数锥有最优值 19、25、31；这个局部锥结论不替代第 1 项的罚项。

| 源 i | r | α | C̄ | a0=(r−1)/12 | a* | 对 X 外客户保证零罚项的最大统一整数 d 上限 | 相对旧 C* 降低 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 15 | 19 | 1/4 | 7/6 | 4 | 4/3 |
| 2 | 5 | 20 | 25 | 1/3 | 19/20 | 2 | 21/4 |
| 1 | 6 | 25 | 31 | 5/12 | 4/5 | 1 | 51/5 |

此外，本审核完整确定了受限锥的非唯一最优面：各有序中间 MAX 权可**独立**取
`[1/4,85/72]`、`[1/3,23/24]` 或 `[5/12,29/36]`，详见第 6 节。
这些区间的上端略大于普遍界使用的 a*，不能把二者混用。

后续新增的[并集桥接补充](averaged_menu_prefix_audit/union_bridge.md)进一步证明：
任意六标签的覆盖并集可用 θ=o/6∈{0,1/6} 的较弱真实预算，因此包括 OPT6 并集在内均有
无重数条件的 31/25/19 无罚界。该补充另给条件 half 引理；不改变本稿原 d 版的正确范围。

## 2. 实际模型、全部定义域与真实预算

采用[共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)。
固定任意完整有序历史纯 SPE 和其实际路径；对源 `i=7−r`，令
`m=r−2,N=7−r,n=b+1∈{1,…,N},k∈{0,…,m},D=n+r−1`。
同一 X 始终最大化 actual 前四负载 `P=b+k` 下的全目录 `f_P`。
强制原源选 X 后，沿同一策略真实继续得到有序中间标签 `Y1,…,Ym` 和末标签 T。

取六个合法标签 `Q1,…,Q6`，允许重复。客户会员总数 `d∈{0,…,6}`，
`θ=d/6`。按 d 压缩只用于**同一末节点的六份线性查询和**：
每个查询的分母相同，所以六个纯行动 IC 的平均查询份额恰为 `θ/(n+x+Σy)`。
不需要把 θ 当成分数行动，也不需要六个会员事件独立。

对每个客户，`x,y1,…,ym,t` 均为布尔值，j=Σy；k 与强制分支会员仍是不同对象。
枚举域的大小分别为 `7N(m+1)2^r=1008,1792,2240`，总计 5040。
全部 64 个六菜单会员串都由 d 的七个取值精确涵盖，计数为 `1,6,15,20,15,6,1`。

记原源收益 u、强制 X 后源收益 v、真实末位收益 w。使用的非负预算是

\[
D_X=u-v\ge0,\qquad
S_T=u-\sum\frac{t}{D}\ge0,
\]
\[
M_{Y_\ell}=f_P(X)-f_P(Y_\ell)
=\sum\frac{x-y_\ell}{n+k}\ge0,
\qquad
\overline B=w-\frac16\sum_{h=1}^6\sum\frac{q_h}{n+x+j}\ge0.
\]

SAFE 的付款是：在原源真的改成合法标签 T，另沿 T 自己的真实续局，源 IC 与分母至多 b+r 给出下界。
它不冻结强制 X 分支的中间行动。末预算则在同一个真实末节点逐份使用合法 Qh 的 IC，再平均。

对任意 `a∈[a0,a*]`，取 `α=5(r−1),s_mid=0,sT=r,a_mid=a,aT=0,δ=1,C̄=6r−5`，
从目标减去 `αD_X+rS_T+aΣM_Y+overline B`，精确得到

\[
\begin{aligned}
E_a={}&\frac{\alpha x}{n+j+t}+\frac{rt}{D}
-\frac{(\overline C-1)x}{D}
-\theta\left(\frac{x}{D}+\frac{1-x}{n}\right)\\
&-\frac{a(mx-j)}{n+k}-\frac{t-\theta}{n+x+j}.
\end{aligned}
\tag{E}
\]

独立程序从每份真实付款重建此式，不导入 Main 的余项函数。
原源形式量 u 的系数完全消去，所有分母至少为 1。

## 3. 全参数族与全客户域的非负部分

当 x=1，θ 的系数非负，k=0 最不利；对相同会员串，E 随 a 增大而不增。
因此只须在 `a=a*,θ=0,k=0` 证明。置 `z=m−j,e=n+m≤5`。

当 t=1，直接化简为

\[
E\ge z\left[\frac{\alpha-1}{(n+j+1)D}-\frac{a_*}{n}\right].
\]

若 z≥1，只需 `G(n)=a*(n+m)D/n≤α−1`。G 在正 n 上凸，端点值依次为

| r | α−1 | G(1) | G(N) |
|---:|---:|---:|---:|
| 4 | 14 | 14 | 35/3 |
| 5 | 19 | 19 | 57/4 |
| 6 | 24 | 24 | 24 |

当 t=0，记 `B=a*D/n`，则

\[
DE\ge\frac{\alpha(z+1)}{e-z}-(r-1)-zB.
\]

z=0 时由 `α/e≥r−1` 非负；相对 z=0 的增量为
`z[α(e+1)/(e(e−z))−B]`，而 `eB≤α−1` 使方括号至少 `(α+e)/e²>0`。
故 x=1 对全部 θ∈[0,1]、所有指定 n,k 和整个参数区间成立。

当 x=0,t=1，

\[
E_a=\frac{aj}{n+k}+\frac rD-\frac\theta n-\frac{1-\theta}{n+j}
\ge\frac{aj}{n+k}+\frac{(r-1)(n-1)}{nD}\ge0.
\]

唯一需要补偿的情形为 x=0,t=0，此时严格等式为

\[
E_a=j\left[\frac a{n+k}-\frac d{6n(n+j)}\right].
\tag{NEG}
\]

这些解析结论覆盖参数区间内每个 a；不是把两个端点的有限检查误当成非线性修正项的插值证明。

## 4. 精确 Π、粗界及零罚项阈值

令

\[
\Pi_{r,a}(n,k,d)=\max_{0\le j\le m}
j\left[\frac d{6n(n+j)}-\frac a{n+k}\right].
\]

j=0 已提供零，因此加正部或不加正部等价。由 (NEG) 和上一节其余情形，

\[
\boxed{
\overline C u-(\overline C-1)\kappa_X-L_{\rm av}
+\sum_{c:x_c=0}\Pi_{r,a}(n_c,k_c,d_c)\ge0.}
\tag{AM}
\]

对于固定 n,k,d 且只要求消去隐藏 j,t，这是最小非负**逐型**修正：
每个 j 都有一个有序布尔串，x=0,t=0 在最大项处恰给余项 `−Π`，且其他情形非负。
这不声称这些局部最坏型可联合实现为完整 SPE。
Π 随 a 增大而不增，故 Main 采用区间上端 a* 正确。

对任何 a≥a0、j≥1，有

\[
\frac a{n+k}\ge\frac{r-1}{12(n+m)}
\ge\frac1{6n(n+1)}\ge\frac1{6n(n+j)}.
\]

中间不等式等价于
`(n−1)[(r−1)n+2r−4]≥0`。因此 d≤1 时 Π=0，且

\[
0\le\Pi_{r,a}(n,k,d)
\le\frac{(d-1)_+m}{6n(n+m)}.
\tag{COARSE}
\]

最后一步使用 `j/(n+j)` 随 j 增大。强化的统一零罚项条件为
`d≤12a*/(r−1)`，整数范围正好为 4、2、1。
这三个整数上限在所定义的逐型消去范围内不能增大：

| r | 首个超限 d | n,k,j,t,x | E at a* | 必需 Π |
|---:|---:|---|---:|---:|
| 4 | 5 | `(1,2,1,0,0)` | −1/36 | 1/36 |
| 5 | 3 | `(1,3,1,0,0)` | −1/80 | 1/80 |
| 6 | 2 | `(1,4,1,0,0)` | −1/150 | 1/150 |

这些重数条件只需对 X 外客户满足，X 内客户无需相应限制。
零客户、空覆盖、同覆盖异标签、重复标签与弱平局不改变付款或分母。

## 5. 固定 θ=1/6 完整非对称锥的三支撑精确对偶

本节允许全部 `2r` 个非负独立权
`p=(α,s1,…,sm,sT,a1,…,am,aT,δ)`，`C=α+Σs+sT`，
但每个客户型的 θ **固定为 1/6**。没有罚项。
全零会员型给 `δ≥1`，全 X 会员型给 `δ≤1`，所以可行点确有 δ=1。

更直接地，不先代入 δ=1，取合法三型

\[
A=(1,0,0,0^m,0),\qquad
G=(1,m,0,0^m,1),\qquad
H=(N,0,1,1^m,0),
\]

元组顺序为 `(n,k,x,y,t)`；三者的 θ 均为 1/6。真实付款给

\[
E_A=\frac{\delta-1}{6},\quad
E_G=\frac{s_T}{r}+\frac{a_T}{r-1}-\frac{5\delta+1}{6},\quad
E_H=\frac\alpha{30}-\frac{s_T}{6}-\frac{a_T}{N}+\frac{5+\delta}{36}.
\]

对**任意实数独立原权**，逐列恒有

\[
\boxed{
C-(6r-5)
=(30r-5)E_A+6rE_G+30E_H
+\sum_{\ell=1}^m s_\ell+B_r a_T,}
\tag{DUAL}
\]
\[
B_r=\frac{30}{7-r}-\frac{6r}{r-1}
=2,\frac{15}{2},\frac{114}{5}\quad(r=4,5,6).
\]

所有乘子、各中间 SAFE 的 reduced cost 1 和 B_r 均严格正。
可行点立即满足 `C≥6r−5`，而第 2–4 节在 d=1 给出达到该值的可行权。
因此精确最优分别为 19、25、31。

等号时 (DUAL) 逐项迫使全部中间 SAFE 权为零、aT=0、EA=EG=EH=0，进而

\[
\boxed{\delta=1,\quad s_T=r,\quad\alpha=5(r-1),\quad s_\ell=a_T=0.}
\tag{FIXED}
\]

这是完整非对称系数锥的结论；没有遗漏通过非对称 SAFE 或末 MAX 降低目标的方向。

## 6. 审核补充：受限锥的完整最优面恰为一个盒

令 θ0=1/6，并定义

\[
a_\theta^+=\frac{\alpha-1+\theta_0}{r(r-1)}
=a_*+\frac1{6r(r-1)}.
\]

在 (FIXED) 下，任取一个有序位置 ℓ：

\[
D_\ell=(1,m,0,e_\ell,0),\qquad
B_\ell=(1,0,1,1-e_\ell,1)
\]

分别给

\[
E_{D_\ell}=\frac{a_\ell}{r-1}-\frac1{12},\qquad
E_{B_\ell}=a_\theta^+-a_\ell.
\]

故每个最优点必有 `a0≤aℓ≤aθ+`。反过来这些条件也充分。
对 x=0，E 随每个 aℓ 不减，最差是全部取 a0，该点 d=1 已证非负。
对 x=1，E 随每个 aℓ 不增，最差是全部取 aθ+。
后一个点的 t=1 证明只须将第 3 节的 `α−1` 换为
`β=α−1+θ0`，其 G 端点仍不超过 β。

对 t=0，保持 `e=n+m,z=m−j` 并令 \(B=a_\theta^+D/n\)，精确式比第 3 节多出
`θ0 z/(e+1−z)`。相对 z=0 的增量方括号有下界

\[
\frac{\alpha(e+1)}{e^2}-\frac\beta e+\frac{\theta_0}{e+1-z}
=\frac{\alpha+e(1-\theta_0)}{e^2}+\frac{\theta_0}{e+1-z}>0.
\]

所以整个盒都可行。独立程序还枚举其所有 4/8/16 个角点与全部 144/256/320 型，
共 7744 次验证全部通过。最优面的完整描述为：

| r | 除中间 MAX 外的权 | 每个有序 aℓ 的独立区间 | 最优面维数 |
|---:|---|---|---:|
| 4 | (FIXED) | `[1/4,85/72]` | 2 |
| 5 | (FIXED) | `[1/3,23/24]` | 3 |
| 6 | (FIXED) | `[5/12,29/36]` | 4 |

**这个更大的上端仅适用于固定 θ=1/6 的锥。**
若把全部中间权 aθ+ 直接用于任意菜单，则在 `n=1,k=0,x=1,y=1−e1,t=1,d=0` 上

\[
E=-\frac1{6r(r-1)}=-\frac1{72},-\frac1{120},-\frac1{180},
\]

而 x=1 不在 Π 修正范围内。Main 的普遍定理使用 a*，没有此问题。
因此“受限最优面非唯一”和“普遍参数族使用较小上端”应当同时保留。

## 7. 当前 dT=1 前提的接口含义

在 Main 提供的比较菜单满足 `d_T=1` 的前提下，三个源的 Π 全部为零。
对应平均查询的系数变化确为

\[
\mathrm{new}_i=\mathrm{old}_i-\Delta_i(u_i-\kappa_i(X)),\qquad
(\Delta_1,\Delta_2,\Delta_3)=(51/5,21/4,4/3).
\]

原源真改 X 的 IC 与最坏分母保证 `u_i≥κ_i(X)`，所以这些新行确实更强。
其有效性由 (AM) 的真实付款独立给出，不能用旧非负式减去非负项来证明。

本审核没有读取 16hist 游戏点，因此只认证这一接口的数学条件与系数；
菜单会员数据是否满足 dT=1 由其原数据证书承担。
对 B/C 或任意其他六标签菜单，必须按实际重数保留 Π 或另证零罚项条件。
没有改动、重算或扩写已有 final23676 输入。

## 8. 独立核验与冻结工件

程序仅用标准库 `Fraction`，不调用优化器，不导入或执行 Main 程序，不读任何游戏数值点。
独立构造完成后，才逐项比较 Main JSON 的全部罚项表、端点统计与受限对偶系数；均一致。

| 核验内容 | 数量／结果 |
|---|---:|
| 完整菜单有序客户型 | 5040 |
| a0、a* 两端非负修正检查 | 10080 |
| 两端真实付款比较 | 20160 |
| 全部 `(n,k,d)` 精确罚项、粗界、最坏型 | 154 |
| 固定 θ 锥的原权仿射基比较 | 8272 |
| 完整最优盒的角点／客户型检查 | 7744 |
| 六标签会员平均恒等式 | 384 |
| 优化器、游戏点、Main 程序执行 | 0／0／0 |

复核命令：

```sh
python -B research/workspaces/six-boss1-20261111/averaged_menu_prefix_audit/verify_independent.py
```

| 工件 | 内容 |
|---|---|
| [verify_independent.py](averaged_menu_prefix_audit/verify_independent.py) | 真实预算重建、全域精确审计、三支撑对偶及完整最优面 |
| [audit_result.json](averaged_menu_prefix_audit/audit_result.json) | PASS、全部统计、阈值见证及参数范围 |
| [penalty_tables.json](averaged_menu_prefix_audit/penalty_tables.json) | 154 个 `(n,k,d)` 的两个参数端点 Π、极值 j、粗界和最坏余项 |
| [restricted_cone_certificate.json](averaged_menu_prefix_audit/restricted_cone_certificate.json) | 三锥全部三支撑有理系数、reduced cost 和最优盒角点 |
| [source_manifest.json](averaged_menu_prefix_audit/source_manifest.json) | 模型、原 SAFE/MAX 来源及 Main 新三文件的 SHA256 |
| [union_bridge.md](averaged_menu_prefix_audit/union_bridge.md)、[union_bridge.json](averaged_menu_prefix_audit/union_bridge.json) | 任意六标签并集的普遍无罚桥、两 θ 值最优盒及条件 half 覆盖引理；另附独立程序与证书 |
| [freeze_manifest.json](averaged_menu_prefix_audit/freeze_manifest.json)、[SHA256SUMS](averaged_menu_prefix_audit/SHA256SUMS) | 本审稿及所属工件冻结清单 |

本义务闭合的是以上明确的必要不等式和系数锥。继续比较原 d 版平均收入时，仍须正确处理 Π；
比较覆盖并集时，补充稿的预算弱化已免除这一重数条件。下一步是将这些界与真实联合结构正确合账。
本审核不把局部最坏型或对偶乘子解释成完整 SPE。
