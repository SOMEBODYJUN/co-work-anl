---
id: "unrelated-machines/fixed-literal-sa-unit-assignment-gap-two"
kind: "obstruction"
type_tag: "障碍"
title: "固定轮literal-SA的单位指派趋二间隙"
status: "proved-parameterized-local-relaxation-gap-with-explicit-base-domain"
summary: "r轮定义为至多r−1 literals乘式；m≥r、m+1单位任务在T=1+1/(m−r+1)有完整局部注入伪解而OPT2，只阻断相对该阈值的统一舍入。"
legacy_ids:
  - "UM-FIXED-SA-ASSIGNMENT-GAP-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/fixed_sa_assignment_gap.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/fixed_sa_assignment_gap_review.md"
---

# 固定轮literal-SA的单位指派趋二间隙

固定整数r≥1，采用**本页轮次约定**：对Boolean变量x_ij，把每个原LP约束乘任意至多r−1个literal（x_e或1−x_e），在x_e²=x_e下线性化；所需moment总次数至多r。其它文献轮次编号可平移1，不能静默换用。

单位指派基底为每任务∑_i x_ij=1、每机∑_j x_ij≤T、0≤x_ij≤1。所有任务不可拆分的真实解仍为完整机器分配，原调度允许不同任务同机；下面的局部“注入”是伪解构造，不是给原问题新增每机只能一件的约束。

对**每对**整数m≥r≥1，取m台相同机器、n=m+1任务、全部p_ij=1，阈值

\[
T_{m,r}=1+\frac1{m-r+1}\in(1,2].
\]

则SA_r(T_{m,r})有完整可行伪解，而真实OPT=2，故

\[
\frac{OPT}{T_{m,r}}=2-\frac2{m-r+2}\longrightarrow2
\quad(m\to\infty,\ r\text{固定}).
\]

T_{m,r}是本构造给出的可行证书阈值，未声称已求出该SA的精确最小可行阈值；这个比值已足够给其整数间隙下界。

所以任何固定r和固定ε>0，都不可能对这一全族的每份SA_r阈值证书统一输出峰≤(2−ε)T的真实调度。障碍是比较基准T过低；本族本身可直接构造最优调度，未给一般算法困难性。

## 一致的局部概率与Boolean moments

对任意任务子集Q、q=|Q|≤r，取Q到[m]的**均匀注入**局部分布μ_Q，共(m)_q=m(m−1)…(m−q+1)个映射，q0取1。m≥r保证分母非零。忘记任务时分布一致：任何较小注入恰有相同数量的扩展，因此投影仍均匀。

对含至多r个literal的事件Λ，Q取其中涉及的任务。令A_Λ为满足全部literal的注入集合，定义

\[
y_\Lambda=\frac{|A_\Lambda|}{(m)_q}.
\]

显然y_∅=1且所有事件概率非负。互相矛盾literal、同一任务被指定到不同机器、不同任务同时指定到同机等可能使A_Λ空；不能只凭文字无直接矛盾就假设可注入。后两类事件在原调度中并非都禁止，局部伪解主动给其权0。

标准SA的正单项moment可等价写成：把指定的(x_ij=1)去重后，若对每涉及任务恰给一个机器且机器互异，则为1/(m)_q；否则为0。负literal事件由同一局部分布的补集或容斥展开得到，不是任意另外指定的独立数。Boolean重复化简和所有重叠局部moment的一致性因此成立。

## 任务等式、盒约束和零概率事件

任取|Λ|≤r−1，Q为其任务集，q≤r−1。对不在Q的任务j，每个Q上的注入有m−q个合法扩展，且(m)_(q+1)=(m)_q(m−q)，于是

\[
\sum_i y_{\Lambda\wedge x_{ij}}=y_\Lambda.
\]

j∈Q时，是每个已有注入上∑_i1_{φ(j)=i}=1的恒等式。因此每个任务等式及所有允许乘式满足。盒约束乘式是y_{Λ∧x}≥0和y_Λ−y_{Λ∧x}=y_{Λ∧(1−x)}≥0，同一局部分布也给出。

若y_Λ=0，任何加一个literal的扩展事件投影回Λ都无满足映射，所以其所有term为0。由此零事件下的赋值/容量乘式均正确，不能通过除以y_Λ略去这个分支。

## 含补literal的容量乘式也成立

只需讨论y_Λ>0。在μ_Q条件于Λ的注入φ上，对固定机器i分两种情况：

- i已被Q占据：已查询任务总贡献1，每个未查询任务的单独注入扩展都不能再用i，贡献0。
- i未被Q占据：已查询任务贡献0；每个未查询任务在单独扩展中以1/(m−q)概率取i，共m+1−q件。

这里没有同时把全部m+1任务注入m机的真实全局分布。以下“条件期望”是由相容的q+1任务moments逐项相加的线性记号：

\[
\frac{\sum_jy_{\Lambda\wedge x_{ij}}}{y_\Lambda}
=\mathbb E_{\phi\mid\Lambda}\left[
\mathbf1_{i\in\operatorname{im}\phi}
+\frac{m+1-q}{m-q}\mathbf1_{i\notin\operatorname{im}\phi}
\right].
\]

两个值分别为1和1+1/(m−q)，故该比值≤1+1/(m−q)≤T_{m,r}。由于q≤r−1，m−q≥m−r+1≥1，绝无零分母。乘回y_Λ得

\[
T_{m,r}y_\Lambda-\sum_jy_{\Lambda\wedge x_{ij}}\ge0.
\]

此论证条件于**完整literal事件**，同时处理正literal、补literal及同一任务多种排除；不是只核正单项就漏掉SA的其余容量约束。

## 真实整数值、显式参数和位长

m+1单位任务给鸽巢下界2；让一机接两件、其余各一件即达2。对固定ε，取m−r+2>2/ε便使上式gap>2−ε。m=r端点T2/gap1也保留；公式本身还覆盖m−r→∞的一些增长轮数，但没有排除所有随m增长的层数，尤其r接近m时此下界远离2，r>m不在本构造域内。

原输入有m(m+1)个整数1，阈值分母m−r+1位长O(log(m+1))。每正moment是0或倒数(m)_q，分子分母位长O(r log(m+1))，literal事件的精确计数/容斥同样具有此量级。对固定r，显式列出至多r阶SA向量规模(m(m+1))^{O(r)}，可由正moment公式和至多2^r项容斥精确生成；这是固定r的多项式说明，不是关于可变r的一致多项式算法。

原稿是完全符号证明，没有报告有限枚举实验或数值近似。本批亦不制造实验计数来替代以上所有乘式证明。

## 2T上界必须写明基底或阈值域

本族T_{m,r}≥1，所有单位端均满足p≤T。对这样的证书，或对显式删去p>T端的[剪枝LST基底](../定义/不相关机器与两个调度松弛--定义.md)，SA点投影成LST分数可行解，[有序槽定理](../定理/有序单位槽的支撑最大件舍入--定理.md)给实际峰≤2T。因此在**这一剪枝/阈值域**，结合本族下界，固定轮literal-SA的阈值gap上确界恰2。

原稿展示的裸unit LP若任意允许T<1，不能无条件把它叫作剪枝LST并套2T。具体r1、m机仅一任务、x_i1=1/m、T=1/m，满足裸LP，真实OPT1，gap=m；m≥3即超过2。这不影响主族，因为其T始终≥1。r≥2时容量式乘x_ij给(T−1)y_{x_ij}≥0，非空任务再由列和1已排除T<1；但统一r≥1的上确界陈述仍应保上面的基底条件。

## 与其它松弛和原问题的不同结论

当m>r、T_{m,r}<2时，单机configuration只能为空集或单件；m台机最多覆盖m份单位任务质量，无法覆盖m+1，因此configuration LP立即不可行。本族不是配置层的gap，也不认证SOS/Lasserre或其它联立约束失败。m=r时T2，不应把“任何T<2不可行”的句子套成该端点配置不可行。

[加工值格点算法](../定理/加工值格点的可计算统一余量--定理.md)在本族g=B=1可精确求调度：它搜索整数目标网格T*=2，而非接受这里接近1的连续/局部证书。固定值集上的可计算算法与低层局部松弛趋二gap并不矛盾。直接利用矩阵求OPT、采用更强配置或增长足够快层数都未被本页排除。

本页只排“固定r的此literal-SA证书→相对同一T统一次二舍入”合同，不排相对真实OPT的一般近似算法，不给P≠NP/NP-hardness/SA跨模型保真、外审或全球新颖性结论。原目标及其反面仍保持开放。

## 完整来源与内部审查范围

[原主稿](../../tools/evidence/fixed-sa-assignment/original/research/current/unrelated_machines/fixed_sa_assignment_gap.md)是本批唯一认领来源0168a2c67a96432d1caf。[原内部review](../../tools/evidence/fixed-sa-assignment/original/research/reviews/unrelated_machines/fixed_sa_assignment_gap_review.md)19754a51b44607548db4只旁读比较，未认领/登记；两原件完整commit/path/hash见[清单](../../tools/evidence/fixed-sa-assignment/source-manifest.json)。另外两个复制稿归其他owner，本批不读取其新主稿或重复处置。

review自报先行重构同一局部注入统计，再攻击条件容量计算、负literal混合、r≤m/r=m及位长，认为该主构造无尚存致命问题；它也明确固定r可显式生成证书、可变r不承诺多项式大小。没有记录程序、数据集、有限实验、外审或全球优先权结论。本批完整读主稿/review、重建全部乘式证明，并与剪枝LST、格点算法和配置覆盖界比较；这是知情数学核对，不冒充本轮新盲审。

原review没有另行处理裸r1/T<1的全类上界，本页已明确补上所需基底域。原冻结文本保持原样；[核验记录](../../tools/evidence/fixed-sa-assignment/verification.json)保这一解释与来源字节检查。一般证明由上述参数化构造承担，没有新增实验或用有限计数代替它。
