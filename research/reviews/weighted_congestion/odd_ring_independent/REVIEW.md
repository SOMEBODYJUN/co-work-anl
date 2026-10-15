# 奇数环资源策略：逐负载、全状态覆盖与闭环独立审查

日期：2026-10-14。贡献：R3 内部独立数学审查子 agent；配置标记为
`gpt-6-astra ultra`。这是内部重构与审查，不是外部同行评审。

审查顺序：先读取分支 `MODEL.md`、两层 `AGENTS.md`、`ACCEPTANCE.md`，
在未读取公屏、其他候选参数或证明的情况下重构下述局部不等式、奇环覆盖和系数闭环，
并先发送给 R3 主 agent；收到其反馈后才审查给定的成长参数。
本文件没有文献优先权结论。计算文件是本目录 `verify_literal.py`，实际结果为
`verification.json`。

## OR-IND-1 v1：精确对象与一般证书

**Objects / Domain.** 给定奇整数 (m\ge3)，下标在 \(\mathbb Z/m\mathbb Z\)
中解释。给定整数 (n_i\ge1)、整数 (1\le k_i\le D)、整数 (D\ge1)，
正实权 (u_i,v_i)，以及目标因子 \(\alpha\ge1\)。玩家是 hub
\(H_i\) 和 \(n_i\) 个不同的 light 玩家 \(L_{ij}\)。所有玩家各有两个策略。

每个 \(i\) 有两个资源 \(A_i^0,A_i^1\)，均采用费用 \(a_i z^{k_i}\)；
每个 \((i,j)\) 有两个不同资源 \(B_{ij}^0,B_{ij}^1\)，均采用费用
\(b_i z^D\)。这里 \(a_i,b_i>0\)，同一 cohort 的所有 B 资源共享同一个
\(b_i\)，不是玩家专属费用。

权 \(u_i\) 的 \(H_i\) 在 bit \(h\) 下使用

\[
 \{A_i^h\}\cup\{B_{i-1,j}^h:1\le j\le n_{i-1}\}.
\]

权 \(v_i\) 的 \(L_{ij}\) 在 bit \(\ell\) 下使用
\(\{A_i^\ell,B_{ij}^{1-\ell}\}\)。资源负载为使用者权重之和；玩家成本只加费用，
不再乘玩家权。没有其他资源、策略或成本。

**Exact Statement / Quantifiers.** 定义

\[
\begin{aligned}
p_i&=(u_i+v_i)^{k_i}-\alpha(n_i v_i)^{k_i},\\
q_i&=\alpha(v_i+u_{i+1})^D-v_i^D,\\
r_i&=(u_i+v_{i-1})^D-\alpha u_i^D,\\
s_i&=\alpha(u_i+n_i v_i)^{k_i}-u_i^{k_i}.
\end{aligned}
\]

如果对每个 \(i\)，

\[
 a_i p_i>b_i q_i, \qquad
 n_{i-1}b_{i-1}r_i>a_i s_i,                 \tag{1}
\]

则对每个纯状态，都存在一名玩家翻转其 bit，严格满足
\(C_{\rm before}>\alpha C_{\rm after}\)。因此不存在 \(\alpha\)-PNE。
这也排除每个 \(1\le\beta\le\alpha\) 的 \(\beta\)-PNE。

**Coefficient iff.** 对固定的权、cohort 大小、次数与 \(\alpha\)，正系数
\(a_i,b_i\) 满足整个系统 (1)，当且仅当

\[
 p_i>0,\quad r_i>0\quad(\forall i),\qquad
 \prod_i\frac{n_{i-1}r_i p_i}{s_iq_i}>1.    \tag{2}
\]

这是**局部充分证书系统**的充要条件，不是此策略拓扑下任意参数产生非存在的充要条件，
更不是 WC-TARGET 全类的刻画。由于 \(D,k_i\ge1\)、权正且 \(n_i\ge1\)，
这里 \(q_i,s_i\) 自动严格正，因此所有商有定义。

## 独立全状态推导

若 cohort \(i\) 中恰有 \(t_i\ge1\) 名 light 与自己的 hub 同 bit，考虑其中任一人。
它当前的 A 负载为 \(u_i+t_i v_i\)，翻转后目的 A 负载为
\((n_i-t_i+1)v_i\)。令 \(\varepsilon=1\) 表示下一 hub 与本 hub 同 bit，则

\[
\begin{aligned}
C_{\rm before}
 &=a_i(u_i+t_iv_i)^{k_i}
   +b_i\big(v_i+(1-\varepsilon)u_{i+1}\big)^D,\\
C_{\rm after}
 &=a_i((n_i-t_i+1)v_i)^{k_i}
   +b_i(v_i+\varepsilon u_{i+1})^D.
\end{aligned}                                                    \tag{3}
\]

\(C_{\rm before}-\alpha C_{\rm after}\) 的 A 部分随 \(t_i\) 单调不减，
最坏是 \(t_i=1\)。B 部分最坏是 \(\varepsilon=1\)；两个分支之差为
\((1+\alpha)b_i[(v_i+u_{i+1})^D-v_i^D]>0\)。因此 (3) 的差至少为
\(a_ip_i-b_iq_i>0\)。这是每名 aligned light 的保证，故只要状态有至少一名
aligned light 就已覆盖。

剩余状态中所有 lights 均与 own hub 反 bit。hub \(H_i\) 当前 A 负载为
\(u_i\)，翻转后为 \(u_i+n_iv_i\)。若 \(h_i=h_{i-1}\)，每个 incoming B
当前负载为 \(u_i+v_{i-1}\)，翻转后为 \(u_i\)，从而

\[
C_{H_i,\rm before}-\alpha C_{H_i,\rm after}
=n_{i-1}b_{i-1}r_i-a_i s_i>0.              \tag{4}
\]

若 \(h_i\ne h_{i-1}\)，incoming B 的这两个负载顺序相反；A 和 B 都在翻转后
严格增加，所以这个 hub 不能改善。当 \(m\) 为奇数时，不可能每条相邻边均异 bit，
故至少有一个同 bit 边，(4) 覆盖剩余状态。论证检查的是任意状态，未将一个改善环
误当作整个状态空间。

对每个指定的边 \((i-1,i)\)，存在恰以它为唯一同 bit 边的奇环标号。
故要求“每个全 anti 状态均有某个 hub 严格改善”时，(4) 对每个 \(i\) 均为必要条件。
第一组 (1) 也恰是“每个状态中的每名 aligned light 都严格改善”的局部条件，
因为其最坏情形 \(t_i=1,\varepsilon=1\) 可实现。

更强的一点：若第一组成立，则任何 anti light 都不能通过变成 aligned 获得
\(\alpha\)-改善；其反向移动在新状态中是一项严格 \(\alpha\)-改善。
因此在第一组成立的前提下，偶环的交替 hub / 全 anti light 状态实际上就是
\(\alpha\)-PNE。奇数性是此证书机制的实质条件。

## 系数闭环与无根号有理构造

第一组要求 \(a_i>\lambda_i b_i\)，第二组要求
\(a_i<\mu_i b_{i-1}\)，其中
\(\lambda_i=q_i/p_i\)、\(\mu_i=n_{i-1}r_i/s_i\)。必要性由正性及环乘积直接得到。
下述构造同时证明充分性，并表明有理输入可取有理系数。

使用更方便的无量纲记号

\[
x_i=v_i/u_i,\quad t_i=v_i/u_{i+1},\quad
\mathcal A_i=a_i u_i^{k_i},\quad
\mathcal B_i=b_i u_{i+1}^{D},
\]

\[
\begin{aligned}
N_i&=(1+x_i)^{k_i}-\alpha(n_ix_i)^{k_i},\\
M_i&=\alpha(1+n_ix_i)^{k_i}-1,\\
P_i&=\alpha(1+t_i)^D-t_i^D,\\
Q_i&=(1+t_i)^D-\alpha.
\end{aligned}
\]

这些与本审查最初的符号关系是
\(p_i=u_i^{k_i}N_i\)、\(s_i=u_i^{k_i}M_i\)、
\(q_i=u_{i+1}^DP_i\)、\(r_{i+1}=u_{i+1}^DQ_i\)。特别注意 \(Q_i\) 对应的是
**下一 hub** 的 incoming 优势，不能把 \(r_i\) 的下标无声替换成 \(Q_i\)。

系统成为

\[
 \mathcal A_iN_i>\mathcal B_iP_i,\qquad
 n_{i-1}\mathcal B_{i-1}Q_{i-1}>\mathcal A_iM_i.
\]

置 \(\ell_i=P_i/N_i\)、\(w_i=n_{i-1}Q_{i-1}/M_i\)、
\(\rho_i=w_i/\ell_i\)，其环乘积为

\[
G=\prod_i\rho_i=\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1.
\]

取 \(\mathcal B_0=1\)，并对 \(1\le i<m\) 取

\[
c_i=1-\frac{i}{m}(1-G^{-1}),\qquad
\mathcal B_i=c_i\prod_{j=1}^i\rho_j.
\]

由于 \(1=c_0>c_1>\cdots>c_{m-1}>G^{-1}\)，每个环边严格满足
\(\mathcal B_i<\rho_i\mathcal B_{i-1}\)，包括回到 0 的边。于是可取

\[
\mathcal A_i=\frac{\ell_i\mathcal B_i+w_i\mathcal B_{i-1}}2,
\quad a_i=\mathcal A_i/u_i^{k_i},
\quad b_i=\mathcal B_i/u_{i+1}^D.
\]

不用选择代数根，也不用数值误差来制造严格余量。

## 给定成长族的审查

审查对象为整数 \(s\ge6\)、\(r=2^s\)、\(D=2sr\)、\(\alpha=r/4\)，
\(m\) 是不小于 \(s\) 的最小奇数。参数为

\[
x_0=r^{-(2m-1)},\quad n_0=\lfloor r^{2m-1}/s\rfloor,\quad k_0=s;
\qquad x_i=r,\quad n_i=1,\quad k_i=D\ (i\ge1);
\quad t_i=1/r.
\]

无量纲权必须满足 \(\prod_i x_i=\prod_i t_i\)，该族两边均为 \(r^{-m}\)。
一组显式整数权为

\[
u_0=r^{2m-1},\quad v_0=1;\qquad
u_i=r^{2i-1},\quad v_i=r^{2i}\quad(1\le i<m).
\]

由此包括最后一条回环边在内，每个 \(t_i\) 都严格等于 \(1/r\)。资源最高次数
为 \(D\)，所有玩家数、权和策略均有限。cohort 数虽极大，但这不违反 WC-TARGET v1；
本构造不声称多项式规模或高效显式输出。

写 \(E=(1+1/r)^D\)，\(P=\alpha E-r^{-D}\)、\(Q=E-\alpha\)。普通节点满足
\(N_i/M_i=Q/P\)，故

\[
G=n_0\frac{N_0}{M_0}\left(\frac QP\right)^{2m-1}.
\]

以下界对全部 \(s\ge6\) 成立：

* \((1+1/r)^r>2\)，故 \(E>2^{2s}=r^2\)。
* \(Q/P>(E-r/4)/((r/4)E)=4/r-1/E>3/r\)。
* \(N_0\ge1-\alpha/s^s>1/2\)。实际上 \(s\ge2\) 时已有 \(N_0>3/4\)。
* \(M_0\le\alpha(1+1/s)^s-1<3\alpha\)。
* \(r^{2m-1}/s\ge2\)，所以 \(n_0\ge r^{2m-1}/(2s)\)。

因此

\[
 G>\frac{9^{m-1}}{sr}>\frac r{6s}>1.
\]

第二步由 \(m\ge s\) 和 \(9^{s-1}>4^s/6\) 得到；最后一步由
\(2^6>6\cdot6\) 及归纳得到。于是所有局部严格不等式闭合。不存在需要补充的
“边界状态”或只覆盖改善环的量词缺口。

## 与成长参数有关的必要限制

对于上述参数形状（允许另选奇数 \(m\)），有 \(Q/P<1/\alpha\)，因为
\(\alpha^2>r^{-D}\)。又有
\(N_0\le(1+x_0)^s\)、\(M_0\ge\alpha-1\)、
\(n_0\le r^{2m-1}/s\)。因此

\[
G<\frac{16^m(1+x_0)^s}{s(r-4)}.
\]

要让此证书可行，必有

\[
16^m>\frac{s(r-4)}{(1+r^{-(2m-1)})^s}.       \tag{5}
\]

特别地固定 \(m\) 不可能承载无限成长族。随着 \(s\to\infty\)，任何可行的这种
参数形状必须满足
\(m\ge s/4+(\log_2s)/4+O(1)\)。这里是必要限制，不是已经证明的充分常数。
候选 \(m\approx s\) 保留了充分余量；这说明增长的环长不是无关冗余。

本族 \(\alpha=D/(8s)=\Theta(D/\log D)\)，玩家数和最大整数权为
\(\exp(\Theta((\log D)^2))\)。这给出构造的尺度，但**不构成相对文献基线的
严格新无限下界证明**；新旧常数、全部次数的插值、优先权必须另外审查。

## 边界与 objection 清单

1. **系数零或次数零。** 本 claim 刻意构造正系数与正次数，不把适用于
   \(q_i,s_i>0\) 的商扩展到退化情形。若某 \(k_i=0\)，第一组的
   \(p_i=1-\alpha\le0\) 不可能配合 \(b_iq_i>0\)。若 \(D=0\)，全 anti 时
   B 费用不变，hub 的 A 成本不降，故这里要求的 hub 改善机制失败。
   这些不等于一般 WC-TARGET 在退化输入下的非存在结论。
2. **零成本与 0/0。** 构造中每个策略有资源、系数和载荷均正，当前与偏离成本都正。
   证明直接用严格差，不使用可能无定义的改善比。
3. **边界方向。** 所有证明用 \(>\alpha\)，符合 \(\alpha\)-PNE 定义中的
   非严格 \(\le\) 边界。乘积等于 1 无法满足这个严格系统。
4. **资源共享。** A 只由自己的 hub/cohort 使用；每个 B 只由一个 light 和下一 hub
   使用。hub 的 incoming B 数量是 \(n_{i-1}\)，不是 \(n_i\)；B 的旁边 hub 权是
   \(u_{i+1}\)，不是 \(u_i\)。费用没有依使用者身份变化。
5. **cohort 内混合状态。** 式 (3) 检查每个 \(1\le t_i\le n_i\)，未把同一 cohort
   的所有 lights 强制为一个联合行动者。每个 light 仅移动自己的权 \(v_i\)。
6. **有限性与无限族。** 对每个固定整数 \(s\) 是一个有限博弈；跨 \(s\) 无上界的
   人数允许。无“一个固定有限游戏覆盖所有次数/因子”的断言。
7. **范围。** 有正系数的 iff 属于 (1)，不是所有可能的非存在机制。
   全类目标、文献改进以及外部审查仍未因此自动完成。

## 实际计算证据与状态

运行：

```text
python tests/audits/weighted_congestion/odd_ring_independent/verify_literal.py --output evidence/runs/weighted_congestion/odd_ring_independent/verification.json
```

所有比较使用 Python `Fraction`；无浮点判断、随机 seed 或近似误差。

独立选取的有限实例为 \(m=3,D=10,\alpha=11/10\)，
\(u=(32,2,8)\)、\(v=(1,4,16)\)、\(n=(3,1,1)\)、\(k=(2,10,10)\)。
由上述有理构造产生系数，逐一建立 16 个资源和 8 个真实玩家。枚举 256 个状态，
每次单人偏离均重新计算每个资源的负载与成本：

* 248 个状态有 aligned light，检查 640 个相应严格改善。
* 8 个全 anti 状态，检查 12 个同 bit 边 hub 严格改善及 12 个异 bit 边 hub 不改善。
* 字面资源成本与式 (3)/(4) 的成本表达式共检查 1328 个精确等式。
* \(\alpha\)-PNE 数量为零。

候选成长族额外精确检查 \(s=6,7\)，相应 \(G\) 的整数部分为
283772、119062；所有上述显示界均通过。这两例只检查了精确证书，
没有声称枚举其天文规模状态空间。

**Evidence / Status.** 一般证书、系数 iff 和给定族闭合有完整独立重构；
有实际精确有限核验；未发现上述输入域内的 fatal objection。
本文件是内部审查资产，尚无外部同行评审、文献新颖性核对或由本子 agent 执行的
远端 checkpoint。下一有价值动作是核查同尺度已知基线与机制出处，并在确有目标差距时
研究如何减少 \(m\)、cohort 规模或提高常数，避免把已成立的 \(\Theta(D/\log D)\)
构造直接升级为主目标突破。


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
