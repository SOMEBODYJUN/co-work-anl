# Signed harmonic与signed自背景：精确层级及真正待支付的余项

2026-10-23，Boss2内部独立核验；恢复main快照由父方给定为`50a9f871`。Q-CAG-HALF仍 **OPEN**。本页核对候选身份、静态归约和下一次判别，不给有限阴性扫描任何一般真值含义，无外审/新颖性声明。

## 1. 实际已推送的陈述

新actor `R-5d61c5324e744dc0a66133207fcbd010` 的 `RESEARCH_STATE.md` 明确给出：对每个原模型完整纯SPE，至少存在一个达到OPT_m的**恰m个目录主题的元组**，其客户负载为d、并集为O，满足

\[
 B_h(c,d):=\sum_x[H_{c_x+d_x}-H_{c_x}]
 \le W+|C\setminus O|.\tag{H}
\]

这里C是实际终局覆盖，c是其完整终局负载，H_0=0。d保留重复主题槽，也保留不同主题的共同客户重数；O只是`{d>0}`，不能替代元组。客户单位权、共同目录、全部有序历史、任意平局与空主题等主模型假设保留。当前`CLAIMS.md`只登记了目录剪枝和人数单调性反例，尚未给(H)一个完整独立Claim条目；不能据README推断已有更长证明或审查。

同页另提较强候选，把B_h换为

\[
 B_q(c,d):=\sum_x\frac{d_x}{c_x+1}.\tag{Qfee}
\]

两个都是**至少一个最优m元组**的存在桥，不是对任意最优元组的全称桥。某个不利最优组合失败不能反驳它们；最优并集相同但槽负载d不同时，费用也不同。

新actor `R-5dbadd913a00492e994a6cfca3ec53fc` 的README说正在探索signed harmonic，但当前实际可读的 `continuation/self_background_probe.py` 和 `signed_self_background_probe.json` 攻击的是较弱对象

\[
 |O|+\sum_{x\in C\cap O}\frac{d_x}{c_x+d_x}\le2W.\tag{S}
\]

脚本对任意比较计数q逐个测试，比只要求某个最优元组更强；所保存的34锥/1654次LP、数值最大1.95和无反例，仅是该有限较强测试的阴性结果，不是(H)证明。不得把(S)的浮点报告称为signed harmonic审查。

## 2. 必要静态归约：候选比half多要求什么

固定一个最优m元组，记U=`|O\C|`、G=`|C\O|`。由于`OPT=W+U−G`，精确分解为

\[
 B_h=U+R_h,
\quad
 R_h=\sum_{x\in O\setminus C}(H_{d_x}-1)
 +\sum_{x\in O\cap C}(H_{c_x+d_x}-H_{c_x})\ge0.
\]

因此

\[
 \boxed{(H)\iff\operatorname{OPT}_m+R_h\le2W.}\tag{1}
\]

这不是half的等价重写：它还要用half余量支付非负R_h。半覆盖只要求余量非负，不能从已有half结论自动推出(1)。若找到(H)反例，仍须单独判断原half，不得混同。

对同一元组，逐客户有

\[
 \frac d{c+1}\ge H_{c+d}-H_c\ge\frac d{c+d}\qquad(d>0).
\]

右式用于C∩O，O\C另有H_d−1≥0，故得到准确充分关系

\[
 \boxed{\text{signed query}\Longrightarrow(H)\Longrightarrow(S)
 \Longrightarrow\text{half}.}\tag{2}
\]

这些蕴含均使用同一个最优元组作见证；没有交换存在量词。若该元组每个被覆盖客户恰有d=1，三个signed候选完全相同。**只有最优元组存在重叠/重复负载d≥2时，harmonic与query、self-background才会真正分开。** 继续只用不交最优主题实例无法区分这三项一般机制。

实际未被最优覆盖的客户G在费用左端为零、在右端获信用；删除这项信用正是已失败unsigned接口，不是无害简化。

## 3. 旧反例和一般族的准确诊断

71客户完整二人例的原文是
`R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md`。
其唯一最优集合T,Q不交，U=36、G=33、W=35，C∩O有两名客户且c=d=1。故

\[
 B_q=B_h=36+2/2=37,\qquad W+G=68,
\]

而(S)左端为38+1=39≤70。它否定unsigned费用37≤35，**不否定任何上述signed桥**，且由于d=1也不区分它们。

作为精确压力边界，任意m≥2取一个含m名客户的大主题、m−1个不交单客户主题。全选大主题可以延拓为完整SPE（见既有三人锐界正文的同机制）；实际W=m，OPT=2m−1，最优m元组各主题一次，d=1。此时

\[
 B_q=B_h=(m-1)+\frac m{m+1}
 =m-\frac1{m+1}.
\]

三个signed桥均成立，却仅剩1/(m+1)费用余量。它们不能靠一个固定正松弛系数粗化；这仍不是一般桥证据。

本次只作一次明确的有限攻击：固定71客户例的完整两人策略（根A，末位回复B,S,R,S,S,R），放开全部63个非空客户类型的非负重数，规范化W=1，要求TQ严格优于其他比较对至少10^−6，对signed harmonic/query各作一个LP。浮点目标`fee−W−G`均约为−1/6，未产生反例。复现脚本为本目录 `signed_harmonic_single_policy_probe.py`，报告为同名json；记录42条含自身动作的SPE比较、20条其他最优对、SciPy/NumPy版本和HiGHS。没有随机性，也没有恢复有理对偶，因此这不是整个策略锥的精确负证书，不保存为新定理；本轮不据此继续扩扫描。

## 4. PAY是另一个存在接口，不能换名

来源是 `R-fa8dd4ddea574a74a634ebc71e6f9ccb/background_induction/prefix_penalty_interface.md`。
其已证(P)是对任一实际剩k人前缀、任一最优m元组、任一t∈[0,4]成立的比较式；PAY要求**存在**实际前缀k、最优m元组及t，使总收费不超过前缀实际最终收益2E。

PAY允许中途欠债；(H)只在实际完整终局比较c,d。两者的背景、负载、费用和存在量词不同，目前没有已证明的蕴含。R5db README已经准确将PAY和signed harmonic分开，但保存的self-background报告既不检查所有PAY断点，也不证明(H)。

## 5. 一个能区分一般机制的下一步

先在全部最优m元组中选择使

\[
 Z(d)=B_h(c,d)+|C\cap O|
\]

最小的元组。此成本的逐客户增量为

\[
 Z_c(d+1)-Z_c(d)=\frac1{c+d+1}+1_{\{c>0,d=0\}}.
\]

若把其中某一槽T换成目录主题A后仍达到OPT_m，则最小性给**必要静态交换行**

\[
 \sum_{x\in A\setminus T}
 \left[\frac1{c_x+d_x+1}+1_{\{c_x>0,d_x=0\}}\right]
 \ge
 \sum_{x\in T\setminus A}
 \left[\frac1{c_x+d_x}+1_{\{c_x>0,d_x=1\}}\right].\tag{3}
\]

该式只用一个合法m槽替换和最小成本择优，允许重复槽、空主题与零客户；不假设替换保留同一个并集，只要求覆盖仍为OPT。现有R5db `independent_attack/independent_obligations.md` 的E1/E2只依最优覆盖、再最大化与C交集，尚未写出这个harmonic成本择优条件；二者不能自动互换。

建议两组共同执行的判别是：**在最小成本最优元组上保留(3)，找一条此前未使用的真实中继节点比较，明确它如何支付R_h中的重叠增量；或给一个所有最优元组均违规的完整SPE。** 若选择计算诊断，优先强制最优元组有不可去掉的d≥2，并精确比较query/harmonic/self三种费用；不要再用d=1样本混称三项都受支持。若仍只能重写`OPT+R_h≤2W`而无新的真实节点不等式，就应明确没有支付进展。

这一步既能区分三组候选的真实强弱，也能检查“存在一个有利最优元组”是否提供新信用，而非继续增加固定人数样本。
