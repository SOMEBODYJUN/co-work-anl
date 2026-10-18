# 18m17j full-row-law family：独立 Exact-first 重构

审查者：`/root/sol_nsw_independent_attack`。本候选的新输入只读 Exact；冻结前未读它的作者 Proof、PSD分解、代码或 run，也未向作者索要推导。已知旧 14m13j Exact/Proof 和自己的独立审查，以及 raw K2/S3/canonical primitive 的背景，不宣称全方向盲审。特别是三位 functional 与旧例相同，但本次新的 all-local-law 族和全参数断言须另核。

## 1. 实际读取与精确输入

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_local_law_canonical_pullback_exact_v1.md`

- 实核 SHA-256：`f958afc5baac6c031415c735c97ecb1febaa2240149b10c111e70ec2dac6b18b`。
- 实核 5,479 bytes、76 行、mode `0644`。
- 真正一次显示、逐行读完 **1–76**，无截断。
- 未读取新候选的其他文件；没有以作者旧程序给这个新全参数合同签字。

以下用 `κ` 表示输入参数 c，用 `a=b1,b=b2,d=b3` 表示三个形式位，以免参数与第三位混淆。域为每个二进制有理 `0<κ<1`；`T=1+κ`，`epsilon=1−κ`。

## 2. Ordinary input 与完整 finite endpoints

五组各两 indexed states，故有 10 个不同 private roots；八资源 `u,v,r,s,w_u,w_v,w_r,w_s` 互异，共 **18 machines**。M 的两个 states 各两正 incidence，共四枚；四 helpers 各两 singleton incidence，共八枚。总 **12 incidence jobs+5 selectors=17 jobs**。Selectors 各两 finite endpoints、incidences 各两 finite endpoints，共 **34 endpoints**。

M/0 的两系数 κ、1−κ 及 M/1 的 1−κ、κ 都正且和一；helpers 的 singleton 系数一。输入没有隐式 zero incidence。某些 assignment variables 的替换恒 0，并不允许删除这些原 finite endpoints 或原 jobs。

每个 incidence 的两端互补，每个 selector 的两端也互补；包括 Hv/Hr 的 constant 0/1 endpoints。所以所有原 job one-hot/exclusivity、Boolean identities 及乘至 degree4 的等式都在同一个三位 Boolean 商内成立。原变量都是 constants 或单 literals，故完整共同 L 的全部 degree≤4 entries 定义一致。

没有引入 `export≤activation` 逻辑 guard。特别 M 的 state0 v incidence 与 state1 r incidence 的 resource endpoints 都恒1；它们是独立不可拆 ordinary jobs，物理端的 private assignments 恒0但该端仍保留。

## 3. 全局 M2：同一三位 functional，有限精确证明

三位 square-free moments 是 `p=3/10,q=3/80,r=−1/160`，仅按不同位数取值。任意原 quadratic 经 affine substitution 位于 `(1,a,b,d,ab,ad,bd)` 的七维 span。

这里可复用我对相同 functional 已独立建立的表示分解，且将数值列全：对称 span `(1,a+b+d,ab+ad+bd)` 的 Gram 是

\[
\frac1{160}\begin{pmatrix}160&144&18\\144&180&33\\18&33&12\end{pmatrix},
\]

整数 leading minors 为 `160,8064,35280`，全正。与之正交的四维 standard 部分，对 sum-zero x,y 的 form 是

\[
\frac1{160}(42\|x\|^2-14\langle x,y\rangle+7\|y\|^2),
\]

即两份 `[[42,−7],[−7,7]]/160`，其整数 minors 为 `42,245`。故 bit M2 正定，全部 34-variable physical M2 是该同一 Gram 的 PSD pullback。常数端没有增加未控制的全局方向。

这个证明不把 r 当成真实 probability，也没有借用一般 slice theorem；它只认证 degree≤2 squares 的 PSD。Global triple `abd` 仍负，这正是允许的合同范围。

## 4. 对所有 κ 的全部 physical affine localizers

从每个 ordinary job 的原端实际相加，逐机 raw loads 为：

| 机器 | load 的 literal substitution | T−load |
|---|---|---|
| M/0 private | `a+κ(1−b)` | `(1−a)+κ b` |
| M/1 private | `(1−a)+κ d` | `a+κ(1−d)` |
| 四 helpers 的八个 private roots | `1` | `κ` |
| 资源 u | `b+(1−b)=1` | `κ` |
| 资源 v | `1+0=1` | `κ` |
| 资源 r | `1+0=1` | `κ` |
| 资源 s | `(1−d)+d=1` | `κ` |
| w_u | `b` | `κ+(1−b)` |
| w_v,w_r | `1` | `κ` |
| w_s | `1−d` | `κ+d` |

所有 κ 在域中严格正。对任意 **全物理变量** affine q，代换后仍 affine；每个 Boolean literal z 满足 degree-four identity

\[
L(zq^2)=L((zq)^2)\ge0,
\]

因为 `(z²−z)q²` 的 Boolean multiplier degree≤2，且 zq 是 quadratic，M2 可用。每个表中 slack 都是非负 constants/literals 的正系数线性组合，所以相应 `L((T−load)q²)≥0`，全部全局 affine localizers 同时成立。

这是全参数符号证明，不是仅核几个 c，也不是只核 q 为原坐标或补。没有 1/κ 或 1/(1−κ) 循环和任何小角度数值容差。

## 5. 显式完整 row laws，保所有局部次数

三位 functional 的任何一位 marginal 为 Bernoulli(p)。任意两位 X,Y 的共同 **真实** law 为：

| (X,Y) | probability |
|---|---|
| 00 | `70/160` |
| 10 | `42/160` |
| 01 | `42/160` |
| 11 | `6/160` |

它匹配所有 degree≤2 moments；因为 X,Y Boolean，任意次数的两位多项式都由 `(1,X,Y,XY)` 决定，所以它其实匹配 ell 对该两位的 **全部** 局部多项式。不能据此拼成三位真实 law。

M/0 root 的三个原端是 selector A=a、private u incidence B=1−b、private v incidence C=0。用上述 (a,b) law push forward：

| 配置 | 权 | load |
|---|---|---|
| `{B}` | `70/160` | κ |
| `{A,B}` | `42/160` | 1+κ=T |
| empty | `42/160` | 0 |
| `{A}` | `6/160` | 1 |

C 永不出现但仍是该机器的原 endpoint。所有配置合法，包括边界 load **等于** T；全 row 的所有 membership moments（含 C 的任意子集项）与 L 一致。

M/1 root 的原端是 selector A'=1−a、private r incidence B'=0、private s incidence C'=d。用同一两位 law 的 (a,d) marginal push forward：

| 配置 | 权 | load |
|---|---|---|
| `{A'}` | `70/160` | 1 |
| empty | `42/160` | 0 |
| `{A',C'}` | `42/160` | 1+κ=T |
| `{C'}` | `6/160` | κ |

同样保该 row 所有 Boolean 局部矩，B' 仍保但恒不出现。

其余机器各自至多依赖一个位或 constants。每 helper root 的 unit selector/private incidence 为互补 literal（或 0/1），故用两 singleton 权 p/1−p 或其交换；constant 情形为一个确定 singleton。资源 u、s 各两互补 unit heads；v、r 各一端恒1、另一恒0；使用对应 singleton laws。w_u,w_s 只有一个 unit job，按其 literal first 给 singleton、以补给 empty；w_v,w_r 确定接其唯一 unit job。每台机器全部 eligible jobs 都包含在这个描述里。

这些 laws 的端指标在 row 内只依赖≤2形式位，且 underlying one/two-bit marginal 精确匹配 ell。因此 **每 row 任意子集 S 的 product**、所有 Boolean powers/literals、所有本地 degree≤4 乃至任意本地次数都共享，不只 first/pair。Global negative triple 未出现在任何单 row 内。这里未引入 CONFIG weights 的全局 moment variables 或跨 row joint schedule law。

## 6. 全部原 jobs 的真实 makespan 1

可选 M/0，令 Hu/Hv 选 fallback，Hr/Hs 选 own：五 selectors 分别去 M/0、Hu/1、Hv/1、Hr/0、Hs/0。

- M/0 的 u,v incidences 分别 export 到 u,v。
- M/1 两 incidences 均留其共同 private，合计 `(1−κ)+κ=1`。
- Hu/1、Hv/1 incidences 分别 export 到 w_u,w_v；其未选 own incidences 各留 unit private。
- Hr/0、Hs/0 incidences 分别 export 到 r,s；其未选 fallback incidences 各留 unit private。

全部 17 原 jobs 各且仅一次被执行；selected roots 只有 unit selector，unselected roots incidence 总负载1；u,v,w_u,w_v,r,s 各一 unit，w_r,w_s 空。故 C=1。每份完整 schedule 必执行 unit selector，给 OPT≥1，故 **actual OPT(P(Q_κ))=1** 对全参数成立。

这个 actual schedule 是另一个点，不保指定的伪矩；反例只关同点 map，不关 actual 可行性或近似比。

## 7. 跨三机器的 canonical 负值

按指定 product map：`A_M0=a,Z_M0u=ab,Z_M0v=a,A_Hs0=d`。故

\[
F(Z_{M0u}A_{Hs0})=\ell(abd)=-\frac1{160}<0.
\]

这违反 claim 非负行乘另一 canonical primitive 的 plain-SA1 row。M/0 的 quality polynomial 因 `epsilon=1−κ` 化简为

\[
\kappa ab+(1-\kappa)a-(1-\kappa)a=\kappa ab.
\]

乘 d 得 `−κ/160<0` 对每个 κ>0。取原 affine q=d，原 L 对 canonical activation polynomial 的 pullback `g(a,aE)d²` 也给同负值：物理次数≤4，再用 d²=d 约去。因此若额外要求该 activation localizer，它也失败；这里没有把仅定义至 canonical degree2 的 F 免费扩成三阶。原 private raw slack 是 `(1−a)+κb`，其 affine-localizer 正性不强制跨矩 `L(((1−a)+κb)ad)` 非负。

三个负 triple 原端可分别为：M selector 去 M/0 private（a）、M/0 u incidence 去 resource u（b）、Hs selector 去 Hs/0 private（d）。它们是三个不同原 jobs 在三台不同机器上的 endpoints，确实不是某个单 row 的未共享 triple。

因此这个新全 local-law family 排除了旧14m“只因一机 triple 未链接”的解释。但它仍以全局负 triple 为基础；若额外要求所有 global triple literals 非负，这个点会被排除。不能把完整各机局部 law 自动解读为 global triple 正性。

## 8. 有限生成、结论与限制

输入大小固定为上述18m/17j/34端，只有 κ、1−κ、T 的 bitlength 随输入变化。Assignment substitution 只含 constants/literals，故完整 degree≤4 moment 表 entries 分母整除160；所有 row laws 的 weights 也均固定 rational numbers。输出所有 moment entries 与全部有限 row laws 只需固定规模 exact affine/Boolean 运算，matrix coefficients 的算术位长 O(bitlength(κ))，因而可确定性总位多项式生成；不需 SDP solver。对 κ 趋零或趋一没有隐含精度门槛。

**独立结论：新 Exact 的 full-row-law raw K2、actualOPT1、全部参数下 direct-product plain-SA1 失败均已重构，未发现 fatal。PASS 限于这个给定点的同点接口反例。** 不声称 actual gap、一般 UM 近似下界或改点/另求R不可能；也不否定 typed one-outer 算法。

本次没有写或运行新候选 checker，没有读取作者新 Proof/code/run。M2 的有限算术来自此前我独立证明的同一七维块；全参数 localizers/row laws 采用上述直接符号推导。数学规格而非通用软件。全球新颖性未认证；一般 UM 主目标仍 OPEN。
