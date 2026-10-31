# 单位任务上的全局四阶负载伪矩与趋二间隙

精确身份：`UM-C2-LOAD-UNIT-GAP-v1`。本稿只研究既有 `C2-load(T)` 合同：全局次数四 PSD 矩、one-hot 守恒、以及次数一测试的逐机负载 localizer；**不含**任意三阶条目非负、不含单机完整配置约束。本稿给该精确松弛的显式间隙族，不给一般 UM 算法困难性，也不声称 `C2+CONFIG` 仍有此间隙。本文给自足一般证明；独立冻结审查见文末。全球新颖性及外审未认证。

## 1. 精确命题

对每个整数 `m>=3`，取 `m` 台相同机器、`n=m+1` 个任务，所有处理时间都是1。令

` t=n/m=1+1/m. `

存在显式有理、总位长多项式的 `C2-load(t)` 证书。因此该实例的 C2 最优阈值恰为 `t`，而真实 `OPT=2`，比值为

` 2/t=2m/(m+1) -> 2. `

该证书有

` rank(M1)=1+m(m-1), `

` rank(M2)=1+m(m-1)+m^2(m-1)(m-2)/2. `

任何三个不同任务在同一机器上的矩是 `-1/m^4<0`。故只要另加这些三阶单项式非负约束，**本证书**就被排除。实际上这里 `CONFIG(T)` 在所有 `T<2` 不可行，故此例证明 C2-load 不蕴含 CONFIG 可行性；没有证明两个一般松弛之间的全局支配关系，也不能用来判定二者合取的间隙。

## 2. 显式矩及线性递推

记 `x_{j,a}` 为任务 `j` 选机器 `a`；`j=1,...,n`、`a=1,...,m`。重复相同变量按布尔关系合并；同任务不同机器的单项式定义为0。

令 `(z)_k=z(z-1)...(z-k+1)`、`(z)_0=1`。对包含 `k<=4` 个不同任务的相容端集 `S`，记其中机器 `a` 的端数为 `c_a(S)`，定义

` y_S = product_a (t)_{c_a(S)} / (n)_k. `               (2.1)

所有分母非零，因为 `n>=4`。令 `L(x_S)=y_S`。记 `N_a=sum_j x_{j,a}`。

当 `|S|=k<=3` 且任务 `j` 尚未出现在 `S` 中时，

` y_{S union {(j,a)}} = [(t-c_a(S))/(n-k)] y_S. `       (2.2)

因此，若 `j` 未出现，

` sum_a y_{S union {(j,a)}} = [(mt-k)/(n-k)]y_S=y_S; `

若 `j` 已出现，one-hot 给出同一等式。故全部要求到三次乘子的任务守恒成立。

同理，已出现的任务对 `N_a` 贡献 `c_a(S)y_S`，其余 `n-k` 个任务按 (2.2) 贡献 `(t-c_a(S))y_S`。于是

` L((N_a-t)x_S)=0     (|S|<=3). `                     (2.3)

特别地，每个逐机负载 localizer 全部条目都为0：

` L((t-N_a)x_S x_U)=0    (|S|,|U|<=1). `              (2.4)

所以只剩全局 `M2` PSD 需要证明。

还需用到 (2.3) 的一个纯代数后果：对任意一次多项式 `ell` 和任意二次多项式 `q`，

` L([(N_a-t)ell] q)=0. `                              (2.5)

即所有 `(N_a-t)ell` 都在二次双线性型 `L(pq)` 的 radical 中；这里直接由四次矩递推得出，不以尚未证明的 PSD 或 Cauchy–Schwarz 为前提。

## 3. 二次空间的初等分解

下文用 `B(X_j,X_k)` 简记 `sum_{a,b}B_ab x_{j,a}x_{k,b}`；`X_j` 只是 one-hot 形式符号，不宣称存在真实分布。

每个次数至多二的多项式可写成常数、单任务函数之和，以及不同任务对上的任意机器矩阵核之和。先把每个机器矩阵分成对称与反对称部分。因此任务对系数空间相应分成：

- 对称数组 `u_jk=u_kj,u_jj=0`；
- 反对称数组 `u_jk=-u_kj,u_jj=0`。

对称数组唯一分解成 `u_jk=c_j+c_k+h_jk`，其中 `sum_{k!=j}h_jk=0`：因为 `c_j+c_k` 的行和为 `(n-2)c_j+sum c`，此行和映射在 `n>=3` 可逆。反对称数组可分成 `u_jk=c_j-c_k+h_jk`、`sum c=0`，其行和为 `n c_j`，剩余 `h` 同样每行和0。

称剩余的行和0数组为任务 harmonic 数组。非 harmonic 部分可以降为一次多项式。例如，对对称核 `B`，

` sum_{j<k}(c_j+c_k)B(X_j,X_k)`

` =sum_j c_j sum_{k!=j}B(X_j,X_k)`

` =sum_j c_j sum_a x_{j,a}[t sum_b B_ab-B_aa]`

模掉 (2.5) 中的 radical 后成立。反对称核与 `c_j-c_k` 给同一降阶等式。

若任务 harmonic 数组 `h` 的每行和为0，则机器核中 `f(a)+f(b)` 的对称部分，或 `f(a)-f(b)` 的反对称部分，给出的二次多项式恒为0。因此可将机器核投影到

` B=B^T, B 1=0 `，或 ` C=-C^T, C 1=0 `。             (3.1)

最后，一次多项式模固定行计数和任务守恒后可写成

` c+sum_{j,a}U_ja x_{j,a}, `

其中 `U` 的全部行和及全部列和均为0。于是二次空间模 radical 由四类部分张成：常数、此类一次函数、对称任务 harmonic × 对称零行和机器核、反对称任务 harmonic × 反对称零行和机器核。

## 4. 一次块及正交性

对行、列和都为0的 `U,V`，由 (2.1) 直接展开得到

` L(q_U q_V)= [t/(n-1)] sum_{j,a}U_ja V_ja, `          (4.1)

且 `L(q_U)=0`。例如同任务项贡献 `(1/m)<U,V>`；不同任务的 `t^2/(n)_2` 项因行和消失，`-t delta_ab/(n)_2` 项因列和0贡献 `+t/(n)_2<U,V>`，两者之和即 (4.1)。

任务 harmonic 部分与常数、一次部分正交：固定单任务 `ell` 后，期望只依赖该任务是否为 pair 的端点；端点项的系数总和是对应 harmonic 行和，非端点项的总系数也为0。反对称情形按有向行和计算相同。

对称与反对称 harmonic 块也正交。对同一任务对，交换两个端点即令反对称核变号；对只有一个公共任务的两对，(5.1) 的混合式只含对称核与反对称核的 Frobenius 内积及对角内积，两者均为0；对无公共任务的两对，交换反对称 pair 的端点再次给0。

## 5. 对称 harmonic 块的精确 Gram

令 `B,C` 是对称零行和机器矩阵，记

` F=sum_ab B_ab C_ab, H=sum_a B_aa C_aa, d=tr(B)tr(C). `

对不同任务编号，按 (2.1) 及机器指标的相等关系展开，有

` D=L(B(X1,X2)C(X1,X2))=(t^2 F-t H)/(n)_2, `

` O=L(B(X1,X2)C(X1,X3))=(-t^2 F+2t H)/(n)_3, `

` Z=L(B(X1,X2)C(X3,X4))=[t^2(d+2F)-6t H]/(n)_4. `    (5.1)

这些式子可由 set-partition 展开逐项核对。三点概率的分子为 `t^3-t^2(delta12+delta13+delta23)+2t delta123`；零行和留下 `-t^2F+2tH`。四点式只有三个两两配对与全相等划分非零，分别给 `t^2 d,t^2F,t^2F,-6tH`。

对任意对称任务 harmonic 数组 `u,v`，令 `S=sum_{j<k}u_jk v_jk`。相同任务对的系数和为 `S`；有一个公共端点的有序不同 pair 对的系数和为 `-2S`；无公共端点的系数和为 `S`。因此

` L(q_{u,B}q_{v,C})=S K_S(B,C), K_S=D-2O+Z. `           (5.2)

化简得到

` K_S(B,C)=alpha [F-m H/(n-2)+d/((n-1)(n-2))], `

` alpha=t^2/[n(n-3)]>0. `                             (5.3)

在本族 `n=m+1` 中，对角二次型为

` K_S(B,B)=alpha [||B||_F^2 -m||diag B||^2/(m-1)`

`                         +(tr B)^2/(m(m-1))]. `      (5.4)

因为 `B1=0`，每行 Cauchy–Schwarz 给

` B_aa^2=(sum_{b!=a}B_ab)^2 <=(m-1)sum_{b!=a}B_ab^2. `

总和后即 `m||diag B||^2 <=(m-1)||B||_F^2`，所以 (5.4) 非负。若其为0，每行非对角元素必须相同；由对称性所有非对角元素相同，且 trace 项为0，故 `B=0`。因此 `K_S` 正定。

选任务 harmonic 空间任意正交基，(5.2) 表明整个对称块是正定机器 Gram 的正数倍直和，故 PSD。

## 6. 反对称 harmonic 块

令 `C,D` 是反对称零行和机器核，`F=sum_ab C_ab D_ab`。直接展开得到

` L(C(X1,X2)D(X1,X2))=t^2F/(n)_2, `

` L(C(X1,X2)D(X1,X3))=-t^2F/(n)_3. `                 (6.1)

无公共任务的期望为0：交换第一 pair 的两个任务即变号。对反对称任务 harmonic 数组，考虑 pair 的方向后，有公共端点项的有符号系数总和仍是 `-2S`。所以

` L(q_{u,C}q_{v,D})=S K_A(C,D), `

` K_A(C,D)=t^2F/[(n-1)(n-2)]. `                       (6.2)

该机器二次型正定。结合 §4 的正交性和 §3 的张成性，全部次数至多二多项式的 `L(q^2)>=0`，即 `M2` PSD。由此 (2.1) 确实满足全部 C2-load(t) 条件。

## 7. 秩、阈值、位复杂度和范围

四个正定块的维数分别为

`1, (n-1)(m-1), [n(n-3)/2][m(m-1)/2], `

`[(n-1)(n-2)/2][(m-1)(m-2)/2]. `

代 `n=m+1` 即得 §1 的秩公式。这个秩计算使用已证明的张成性、正交性和各非零块正定，不由有限实验推断。

真实调度有 `n=m+1` 个单位任务，所以 pigeonhole 给 `OPT>=2`；把两个任务放一机、其余各放一机给 `OPT=2`。任意 C2-load(T') 证书的常数 localizer 给每机平均负载至多 `T'`，合计任务守恒给总平均负载 `n`，所以 `mT'>=n`。结合本构造，C2 最优阈值精确为 `n/m`。

完整配置在 `T<2` 时每机配置至多含一个任务，故 `m` 机器最多覆盖 `m<n` 个任务；CONFIG 阈值为2。三阶同机矩由 (2.1) 化为

` (t)_3/(n)_3 = -1/m^4. `

这再次强调本证书不是概率分布，不满足三阶逐项非负，更不是真实最优凸包点。

输入有 `mn=O(m^2)` 条有限端。次数四兼容矩最多 `O((mn)^4)` 个，每个有理数分子分母仅 `O(log m)` 位（阶数固定为4），可用固定次有理乘除显式生成。故证书构造及写出均按原输入位长多项式；本结论不依赖一般精确 SDP 求解算法。

## 8. 精确有限审计

配套审计程序 `tests/audits/unrelated_machines/c2_unit_multislice_gap.py` 只用 Python 标准库 `fractions.Fraction`。默认检查：

- `m=3,4` 的完整 M2，精确零 pivot 安全 Schur/LDL 判 PSD、秩公式；
- 这两例全部 `|S|<=3` 的 one-hot 与行计数递推、全部逐机 localizer 条目恰为0；
- `m=3,...,8` 的指定非零对称核四点范数、反对称核三点 cycle 范数，逐颜色枚举与 (5.1)–(6.2) 精确核对；
- 同机三阶矩 `-1/m^4` 和真实/C2 阈值比率。

这些只是所列有限参数与公式实现的证据，不代替 §3–6 对全部 `m>=3` 的 PSD 证明。运行输出、代码 hash、Python版本和实际范围由文末冻结记录记载；重跑默认只写 stdout，不覆盖冻结证据。


## 9. 普遍上界、依赖及准确研究含义

令 `T_C2(P)` 为此处精确定义的 `C2-load(T)`（含端剪枝）可行阈值的下确界。任意可行矩的 `x_e=y_{\{e\}}` 非负、任务和为1、逐行分数负载不超过T；这是M2的对角非负及常数localizer的直接结果。因此经典 `UM-ST-ROUND-v1` 给实际存在的负载至多2T分配。结合本族，**一般该C2松弛的整数间隙上确界恰为2**，不是只有某个贪心算法表现差。这里的间隙比较只对正最优值，零最优值沿原模型逐任务选择零端处理。

- Objects / Domain：全局one-hot布尔四阶矩及次数一逐机负载localizer，定义原文为 [全局矩正文§2](global_assignment_moment_rounding.md#2-仅使用负载localizer的四阶共同矩)。本族m≥3、n=m+1、p全为1，量词及显式证书在§1–2。
- Assumptions：不要求三阶或四阶条目逐项非负，不含配置凸包及prefix-count localizer；这些界限属于命题身份。
- Dependencies：原模型 `UM-MODEL-v1`；§2–6自足代数。普遍supgap≤2另用经典 `UM-ST-ROUND-v1`，不导入精确SDP求解假设。
- Evidence：一般证明、冻结审查、两路独立精确矩阵消元及颜色Gram核对；有限范围见下列记录。
- Counterevidence / Objections：m=2不满足PSD，审查给显式负平方；三阶非负或单机CONFIG即排除本证书。没有声称更强共同系统的间隙，也没有得到NP困难性。
- Status：stated-scope proof complete; independently reconstructed and exactly audited; external review and novelty unverified。

本结果改变的是研究前沿中“普通C2-load共同容量是否自身已足以提供统一阈值改善”的义务：答案为否。它不否定从原输入直接得到更好调度的可能性；本族本身显然易解。下一可判别义务是共同矩与完整单机配置/有效计数约束合用后的实际舍入或真正间隙。不能只修本族后就免费认定一般保证。

## 10. 文件、复现和文献比较

- [规范Fraction审计](../../../tests/audits/unrelated_machines/c2_unit_multislice_gap.py)：直接生成所有one-hot矩、验证约束并做精确Schur消元，颜色公式逐项反算。
- [独立整数Bareiss审计](../../../tests/audits/unrelated_machines/c2_unit_multislice_independent.py)：不导入规范核心，独立生成完整矩并作整数对称消元，另核m=2边界。
- [实际m=3输入](../../../examples/unrelated_machines/c2_unit_multislice_m3.json)与[完整显式矩证书](../../../evidence/certificates/unrelated_machines/c2_unit_multislice_m3.json)：矩是伪矩，包含负三阶条目，绝不标为真实调度分布。
- [冻结双路运行](../../../evidence/runs/unrelated_machines/c2_unit_multislice_gap_audit.json)记录命令、代码/正文SHA256、版本与有限范围。
- [独立冻结审查](../../reviews/unrelated_machines/c2_unit_multislice_gap_review.md)记录statement-first重构、实际攻击和仍开放的更强合同。

针对性文献比较核读了 Verdugo–Verschae–Wiese, *Breaking symmetries to rescue Sum of Squares in the case of makespan scheduling*, [arXiv:1811.08539v3](https://arxiv.org/abs/1811.08539v3)，2020-05-16，PDF/印页3 Theorem1及AppendixB（PDF/印页33–34）。来源给的是CONFIG上高轮数的不同常数下界，不能用它替代本文特定degree-four负载合同的证明；本文也不声称超越其更强松弛下界。只核上述陈述及公式定义，未下载原始字节、未重构全文或认证本文全球优先权。原始文献的对称化及下降阶乘机制是相关背景，本稿的新增用途是精确判定仓库现行C2接口。详见专题文献记录。
