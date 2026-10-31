# 稀释共享终端原矩阵的近二 raw K2 gap：Exact-only 独立重构

作者：/root/sol_identity_coupling，2026-10-18。仅实际全文读 sol_diluted_shared_terminal_raw_k2_exact_only.md，SHA256 25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b；未读作者 Proof、code 或其他 reviewer 的推导。本人已有原矩、raw K2、normalized-flat、SA3/CONFIG 背景，并刚独立审过其他 raw 接口；不称全方向盲审。本候选的新分布及其定量推导此前未读。

**重构结论：Exact 的实际 OPT、共同 raw M2、全部机器 CONFIG first/pair、所有全局 affine load localizers，以及明确多项式参数和证书生成界均通过；未发现 fatal。** 以下完整证明不使用固定维数连续性、未知充分小常数或作者程序。

## 1. 对象、量词及合同边界

对每整数 \(k\ge2\)，置
\[
L=2k^2,\quad M=1+60Lk^4,\quad a=1/M,\quad T_0=1+1/k.
\]
每个 component i 有一台 \(U_i\)、L 台 \(B_{i,b}\)、k 台 \(Z_{i,t}\)，所有物理机器不同。唯一跨 component 的原 job h 在各 U 上时间一。每个 \(f_{i,j}\) 在其 U 上时间 \(1/k\)，可在本 component 的全部 B 上时间一；每个 \(e_{i,b,\ell}\) 在其 B 上时间 \(1/k\)，可在本 component 的全部 Z 上时间一。所有其他端无穷，全部 jobs 独立、不可拆且各执行一次。

本证明核的是 Exact 明列的 raw K2：共同 raw degree-four moments、全部原 Boolean/exclusivity/cover identities、global M2、每机一个 legal CONFIG(\(T_0\)) law 共享全部 first 与 same-row pair，以及对任意**原全局 affine q** 的 load localizer。没有要求 same-row triple 与 CONFIG 相同，没有把 CONFIG 指标另放入一个未知高阶共同表，也没有 canonical activation/claim 条件。

这是普通多资格原矩阵；一枚原 job 的多个 unit heads 不被拆成不同 jobs。它不被本记录擅自改称每 incidence 只有一个固定 head 的 P(Q)。全族提供实际近二 relaxation gap，不是 NP-hardness、真实 YES/NO 源或任何算法下界。

## 2. 真实普通 OPT 的完整上下界

令 \(r=\lfloor\sqrt{k}\rfloor\)。上界 schedule 任选一个 component i 放 h。把该 component 恰 r 枚 f 送到 r 台不同 B；每台这样的 B 再把恰 r 枚 e 送到不同 terminals，全部 \(r^2\) 枚导出 e 使用互异 terminals。其余全部 f/e 留各自 tiny home，其他 components 也全部 tiny-home。

所选 U 及 r 台被 unit 占用的 B 负载均为 \(2-r/k\)；其余 U、B 负载至多一，terminals 至多一。所有原 jobs 各执行一次，故 OPT 至多 \(2-r/k\)。

反向，考虑任一 makespan \(C<2\) 的完整 schedule。设 h 去 \(U_i\)，并令
\[
q=\left\lceil k(2-C)\right\rceil.
\]
U 上负载限制迫至少 q 枚本 component 的 f 导出到 B。因为每件导出 f 在 B 上耗一，\(C<2\) 迫这些 f 去互异 B。每个这种 B 另有 k 枚自己的 e；为了使负载至多 C，至少 q 枚 e 必须导出。所有这些导出 e 也为 unit，故使用互异 terminals。只有 k 个 terminals，因而
\[
q^2\le k,\qquad k(2-C)\le q\le r.
\]
所以 \(C\ge2-r/k\)。若 C 至少二，这个下界更显然。没有只核一个 selector 模式；h 在任一 U 都给相同论证。因此
\[
\boxed{\operatorname{OPT}(P_k)=2-\lfloor\sqrt{k}\rfloor/k.}
\]

## 3. 共同真实 moment law 与身份

令 I 在 M 个 components 中均匀选取，h 去 \(U_I\)。Conditional on I，selected component 用 H，其他 components 独立用 Q，均为 Exact 的完整 assignment laws。

H 中每个 f 由 uniform injection 去不同 B，所有 e 均留 tiny home。Q 中以概率二分之一全部 tiny-home；以概率四分之一选 \((j,b)\)，仅该 f 去 B，并用 uniform permutation 将该 B 的 k 个原 e 一一送往 k terminals；以概率四分之一仅选一枚原 e 导出到一个 terminal。每个 sample 仍给**每个原 job 恰一个合法端**。没有原 job 被复制、漏掉或只记录 presence。

定义 F 为这个有限真实 assignment law 的期望。所有 Boolean、同 job 不同端 exclusivity 及 cover identities 在每个 sample 上恒成立，乘到任何所需次数仍成立；global M2 由 \(F(p^2)\ge0\) 直接得到，覆盖全部 raw degree \(\le2\) 的 p。

这里并非所有 samples 是 \(T_0\)-schedule：每个 H component 有恰 k 台 B 的实际负载为二。事实上该真实 law 不提供 strong schedule；CONFIG 的第一、二矩替换是本合同中允许的独立 row certificates。

## 4. U 和 terminal 的 CONFIG 付款

U 的真实 row law 已 legal：h 单独出现概率 a；每个恰少一枚 \(f_j\) 的 home configuration 概率 \((1-a)/(4k)\)；全部 k 枚 home f 的配置概率 \(3(1-a)/4\)。这些配置的负载均至多一，总质量一，自动匹配全部同 row 矩。

Terminal 在 H 下为空。Q 的 full-permutation alternative 给每个 terminal 恰一件 unit e，single-export alternative 至多给一件。对任一指定 endpoint \(e_{i,b,\ell}\to Z_{i,t}\)，其概率为
\[
(1-a)\left(\frac1{4Lk}+\frac1{4Lk^2}\right)
=\frac{(1-a)(k+1)}{4Lk^2}.
\]
同 terminal 不同 endpoint pair 始终零。因此真实 empty/singleton law 就是合法 CONFIG law，全部 singleton 总质量为 \((1-a)(k+1)/(4k)<1\)。

这两类机器的 load 在每个 sample 上均至多一，故它们针对任意全局 affine q 的 load localizer 也已逐点非负。

## 5. B 的 first/pair 与合法 CONFIG law

固定一台 B，记
\[
p=ak/L,\quad \beta=(1-a)/(4L),\quad \gamma=(1-a)/(4L).
\]
其真实 row 的四类事件为：

| 真实 row event | 质量 | unit 数 | tiny-home 数 |
| --- | ---: | ---: | ---: |
| H injection 命中该 B | p | 1 | k |
| Q full-export alternative 选该 B | \(\beta\) | 1 | 0 |
| Q single-export alternative 选该 B | \(\gamma\) | 0 | \(k-1\) |
| 其余 | \(1-p-\beta-\gamma\) | 0 | k |

有 unit 时 label 在 k 个 f 中均匀；single-export 时缺失 home e 的 label 均匀。因此对 unit endpoint \(X_j\)、home endpoint \(Y_\ell\)：
\[
\begin{aligned}
F(X_j)&=(p+\beta)/k,& F(X_jX_{j'})&=0\ (j\ne j'),\\
F(Y_\ell)&=1-\beta-\gamma/k,&
F(Y_\ell Y_{\ell'})&=1-\beta-2\gamma/k\ (\ell\ne\ell'),\\
F(X_jY_\ell)&=p/k.
\end{aligned}
\tag{1}
\]

现在以 Exact 的五类合法配置及其质量：
\[
\begin{array}{c|c}
\text{配置类型}&\text{总质量}\\ \hline
\text{one unit + one home}&kp\\
\text{one unit + no home}&\beta-(k-1)p\\
\text{no unit + no home}&p\\
\text{no unit + }k-1\text{ homes}&\gamma-kp\\
\text{no unit + all }k\text{ homes}&1-\beta-\gamma+(k-2)p
\end{array}
\tag{2}
\]
Incoming label 均匀，单 home label 独立均匀，缺失 label 均匀。总质量逐项相加为一。非负性由
\[
M-1=60Lk^4\ge4k^2\ge4k(k-1)
\]
支付两项可能含差的质量；最后一项至少 \(1-1/(2L)>0\)。所有配置负载至多 \(1+1/k=T_0\)。

从(2)重算：unit 总质量为 \(p+\beta\)；unit/home 指定 pair 为 \(kp/k^2=p/k\)；home first 为
\[
p+(\gamma-kp)(k-1)/k+1-\beta-\gamma+(k-2)p
=1-\beta-\gamma/k;
\]
home distinct pair 为
\[
(\gamma-kp)(k-2)/k+1-\beta-\gamma+(k-2)p
=1-\beta-2\gamma/k.
\]
所以(1)全部匹配，包含所有 incoming/incoming、home/home、incoming/home pairs 及由 Boolean 得到的重复 pair。

这没有匹配 triples：实际 \(F(X_jY_\ell Y_{\ell'})=p/k>0\)，而 legal CONFIG 中 one unit 不能再含两枚 homes。这一限度与 Exact 完全一致。

## 6. 全局 localizer 的局部定量估计

以下是不使用维数连续性的核心。固定 component 及一台 B，记其 raw slack 为 h。H 下
\[
h=\frac1k-\mathbf1_{\{\text{injection hits B}\}},\quad
E_Hh=\frac1k-\frac{k}{L}=\frac1{2k},\quad |h|\le1.
\tag{3}
\]
Q 下每个 assignment 的此 slack 至少 \(1/k\)。

任意原全局 affine q，可利用原 job covers 消去所有 tiny-home indicators。对每个 component 的部分，减去全部 tiny-home assignment 的基线，写为
\[
g=\sum_{j,b}\alpha_{j,b}X_{j,b}
+\sum_{b,\ell,t}\beta_{b,\ell,t}Y_{b,\ell,t},
\tag{4}
\]
这里 X、Y 分别是 f、e 的 unit-head indicators。于是整个 q 是一个常数、selector endpoints 的线性组合及各 component 的 \(g_i\) 之和。每个 g 在全-home assignment 为零。

令 \(V=\operatorname{Var}_Q(g)\)。Q 以至少二分之一概率处于全-home，所以 Cauchy 给
\[
(E_Qg)^2\le\frac12E_Qg^2,\qquad E_Qg^2\le2V.
\tag{5}
\]
Single-e alternative 因而给
\[
\sum_{b,\ell,t}\beta_{b,\ell,t}^2\le8Lk^2V.
\tag{6}
\]
对 permutation \(\pi\)，记 \(S_b(\pi)=\sum_\ell\beta_{b,\ell,\pi(\ell)}\)。Full-export alternative 给
\[
\sum_{j,b}E_\pi(\alpha_{j,b}+S_b(\pi))^2\le8kLV.
\tag{7}
\]
又由 Cauchy 及 permutation 的单项均匀边际，
\[
E_\pi S_b(\pi)^2
\le k\,E_\pi\sum_\ell\beta_{b,\ell,\pi(\ell)}^2
=\sum_{\ell,t}\beta_{b,\ell,t}^2.
\]
利用 \(\alpha^2\le2(\alpha+S)^2+2S^2\)，结合(6)(7)，得
\[
\sum_{j,b}\alpha_{j,b}^2
\le16kLV+16Lk^3V
\le20Lk^3V
\quad(k\ge2).
\tag{8}
\]
H 下没有 e exports，各 f 的 injection 边际均匀，所以
\[
E_Hg^2
\le k E_H\sum_j\alpha_{j,\sigma(j)}^2
=\frac{k}{L}\sum_{j,b}\alpha_{j,b}^2
\le20k^4V
\le20Lk^2V.
\tag{9}
\]
这对任意 coefficients、任意 k 和 L 的指定关系成立，没有随全局 raw 变量数恶化的未明常数。

对**任意实截距 d**，用(3)对 d 完成平方，并用 \(|h|\le1\)，得
\[
\begin{aligned}
E_H[h(d+g)^2]
&\ge E_H[hg^2]-\frac{(E_H[hg])^2}{E_Hh}\\
&\ge-(2k+1)E_Hg^2\\
&\ge-60Lk^3V.
\end{aligned}
\tag{10}
\]
Q 的逐点正 slack 则对任意 d 给
\[
E_Q[h(d+g)^2]\ge\frac1kE_Q(d+g)^2\ge V/k.
\tag{11}
\]

## 7. 任意跨 component、含全部 selector 的 affine q

仍固定被测 component i 的 B 行。Condition on I=r 后，其余 components 与 component i 独立。把这些其他 components 的 \(g_j\) 写成 conditional mean 加零均值噪声；全部 selector endpoints 在此条件下为常数。

因此对每个 r，q 可写成
\[
q=d_r+g_i+\xi_r,
\]
其中 \(\xi_r\) 与 component i 独立且均值零，其方差为其他 components conditional variances 的和。于是
\[
E[hq^2\mid I=r]
=E[h(d_r+g_i)^2\mid I=r]
+E[h\mid I=r]\operatorname{Var}(\xi_r).
\tag{12}
\]
最后一项非负：r=i 时 slack 均值为 \(1/(2k)\)；r 不等于 i 时它至少 \(1/k\)。这付清所有其他 components、任意数量原变量与全部 selector contexts，没有删去它们或只测一个小 principal block。

在 r=i 项用(10)，r 不等于 i 项用(11)。它们对所有 \(d_r\) 都成立，故
\[
\begin{aligned}
F[hq^2]
&\ge\left(\frac{1-a}{k}-60aLk^3\right)\operatorname{Var}_Q(g_i)\\
&=0,
\end{aligned}
\]
最后等式恰用 \(a=1/(1+60Lk^4)\)。因此**每台 B 的全部原全局 affine localizers** 统一成立。加 §4 已付的 U 与 terminals，全部原机器均已覆盖。

## 8. 明确输入和证书生成位成本

机器数为 \(M(1+L+k)\)，jobs 为 \(1+Mk(1+L)\)。完整 finite endpoints 数
\[
N=M+Mk(1+L)+MLk(1+k)=O(k^{10}).
\]
L、M 是 k 的明确整数多项式，times 只有 \(1,1/k\)。无自洽选择某个“足够大 M”或把维数固定的步骤。

可枚举 \(O((N+1)^4)\) 个 raw total-degree 至多四 monomials，并计算所列真实 law 的对应期望；无需枚举完整 support。每个 monomial 至多查询四个原端，先合并重复、检测同 job 互斥；然后枚举 I 的 M 种取值，只需计算至多四个 components 的 local probabilities。

H 的 f constraints 至多指定四个 injection images，合法时概率由 falling factorial \((L)_r^{-1}\) 给出；e 全 home 的判断直接完成。Q 的全-home分支直接判断；full-export 分支可枚举全部 kL 个 \((j,b)\)，剩余 permutation 至多固定四个 images，以 \((k)_r^{-1}\) 计算；single-export 分支可枚举 Lk² 个原 triples。\(k<r\) 时先判是否存在合法 partial permutation，绝不除零。

每步只作多项式数量的整数/有理运算，falling factorial 长度最多四。对一个 monomial，只有常数个非平凡 local probability 因子，故分母和总位长受显式输入多项式控制；保守按全部加法共同清分母也仍为多项式总位长。全表可据此确定性生成。

每 B 的 CONFIG support 至多 \(k^2+2k+2\)，U 为 \(k+2\) 种，terminal 为 \(Lk+1\) 种；所有权重是所给明确有理式。每个 localizer matrix 在 raw affine basis \(1,x_1,\ldots,x_N\) 下有 \((N+1)^2\) 个 entries，每项用已给至多三阶 moments 与本机显式 processing coefficients 求和，故全部原机器的矩阵也能在多项式时间、总位长内生成。

这是显式给定证书的生成规格，不是 SDP 可行点 finder。此次未读或执行任何候选程序，Software 为 none；没有用浮点 PSD 试验承担无限 k 的证明。

## 9. 更强系统、缩放及实际意义

记 \(A_i\) 为 h 在 \(U_i\) 的原 endpoint，\(C_{i,b}\) 为该 B 的 unit-f incoming occupancy。则
\[
F[A_iC_{i,b}(T_0-\operatorname{load}_{B_{i,b}})]
=-\frac{k-1}{k}\frac{ak}{L}<0.
\]
其展开含原 physical slack 乘两个 raw positive endpoint literals。这不在本 Exact 的 affine-square localizers 内；该 stronger conditional family 会切掉本证书。§5 的同 row bad triple 也表明不能宣称 full local CONFIG law 或 canonical higher consistency 已被支付。

将所有 finite times 乘 \(k/(k+1)=1/T_0\)，保留同一 raw moment table 和 CONFIG weights：每个 CONFIG load 至多一，新的 load slack 只是旧 slack 的正倍数，全部 localizers 保持。真实 optimum 变成
\[
\frac{2-\lfloor\sqrt{k}\rfloor/k}{1+1/k}\longrightarrow2.
\]
故本 family 确实是所列 **raw K2** 的真实 ordinary OPT 近二 gap，既不靠一个 actual-OPT-one 例子，也不靠只给定 selector 的 NO。

但这是无输入承诺的显式 relaxation gap family，不是 polynomial hardness reduction、真实 YES/NO source theorem、native canonical-C2 gap 或一般算法不可能性。S3/条件 Hall 等更强来源仍可能排除此点；一般 UM 主目标未被解决。

## 10. 冻结状态

本记录为该 Exact 的知情背景下独立完整重构，通过后才可释放作者 Proof 作实际读后对照。未用作者 Proof、code、外部审查或固定维度存在性填补 §6–7。全部原矩阵、旧冻结 records 与 repo 字节保持不变。
