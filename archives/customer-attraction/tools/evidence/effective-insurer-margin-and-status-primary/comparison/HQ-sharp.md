---
id: disjoint-petal-fixed-root-three-dilution-sharp-bound
kind: theorem
type_tag: 定理
title: 不交花瓣同根保险的三倍损耗锐界
status: proved-sharp-in-independent-disjoint-petal-architecture
summary: "同一合法根两份真实完整纯续局有首人正收益差δ时，高分支2W−OPT_m≥|K|+3δ；任意多独立坐标允许异号，修根需总稀释至少3Δ且padded对每m≥2取等。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_insurer_three_sharp.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_three_statement.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/independent/insurer_three_sharp_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_insurer_spread.md"]
---

# 不交花瓣同根保险的三倍损耗锐界

7242B主稿、1827B仅陈述稿及7382B后续内部审查本次完整primary整理。HI的padded页曾作为全文相关材料保留这些源，本页现在独立展开其全部证明与精确停止域。它证明一个保险架构的锐成本，不解决一般六人半覆盖，也不证明所有旧root-only计划中常数3最优。

## 同根、全部主题共同核与高分支损耗

采用[同根跨度页](不交花瓣同根续局的跨度与客户成本--定理.md)的精确单位客户模型、m≥2、有限共同目录、全部有序历史纯策略。K是**全部合法主题**的交集，删除K后不同非空包含极大花瓣两两不交。允许任意内部交叠子主题、残余空主题、同覆盖标签和任意历史平局。固定同一合法首位主题A，取A后两份真实完整纯SPE H,L；根A自身无需最佳。首人收益差

\[
\delta=u_1(H)-u_1(L)>0.
\]

令W_H为H分支的实际覆盖，\(O=OPT_{\mathcal S,m}\)是**同一个保险实例**至多m主题的真实最优覆盖，则

\[
\boxed{2W_H-O\ge |K|+3\delta.}\tag{S1}
\]

特别注意K不是仅极大主题的交集。若极大主题为\(\{c,x\},\{c,y\}\)，另有合法内部根\(\{x\}\)，极大主题交集含c但该根不含c；此时每人c/m不再恒定，而全部主题交集为空、两个极大残余交叠，故目录不属本页输入类。该例只说明范围差别，不声称是(S1)反例。更宽sunflower目录的福利结果不能自动给本页同根差的工具。

删K后，每人的核心收益原为|K|/m，δ不变，W与O各减|K|，因此最后给2W−O加回|K|即可。以下证明无核版本。

## 真实后继资源与正差参数

[跨度页](不交花瓣同根续局的跨度与客户成本--定理.md)完整证明：singleton阈值余席保证所有SPE终局为静态PNE；逐点严格降低一资源不增加该资源的任意PNE占用；严格正递减资源的任意两PNE占用差≤1；两条真实后继的资源比较动态删除全部严格内部行动，固定根不被删除。

若无核根为空则首人收益恒0，不能δ>0。故令\(A\subseteq B, a=|A|>0,w=|B|\)，后继m−1人的B资源函数与其它花瓣为

\[
f_B(t)=\frac a{t+1}+\frac{w-a}{t},\qquad f_j(t)=\frac{w_j}{t}.
\tag{S3}
\]

它们严格正递减；两分支为同背景PNE。高首人收益意味着B后继人数更低，故H有k−1、L有k，\(1\le k\le m-1\)，并有

\[
u_{1,H}^{petal}=a/k,\quad \delta=\frac a{k(k+1)}.\tag{S4}
\]

内部根缺失的w−a不能省略。以下只用H的真实后继PNE。令μ为m−1名后继的最低最终花瓣收益。μ>0，因为有正资源而每位后继可静态投它。未被任何后继使用且不同于B的花瓣大小≤μ：最低收益后继可静态改投该空花瓣。

## k≥2：根花瓣被后继完整覆盖

此时H后继也用B，全部已用花瓣均完整覆盖。设其已用花瓣数ℓ，则1≤ℓ≤m−1，H的总覆盖W是这些花瓣大小和。已用普通花瓣大小q_j u_j≥μ，B也满足精确恒等式

\[
w=(k-1)f_B(k-1)+a/k\ge\mu.
\]

所以已用花瓣都不小于任意未用花瓣；最优至多m花瓣可以先含全部ℓ个已用花瓣，再加至多m−ℓ个未用花瓣。内部主题扩成合法极大主题不减覆盖，因此

\[
O\le W+(m-\ell)\mu.\tag{S5}
\]

均分预算恒等式对同一H分支给

\[
W=\sum_{i=2}^m u_i+a/k\ge(m-1)\mu+a/k.
\]

从而

\[
2W-O\ge W-(m-\ell)\mu
\ge a/k+(\ell-1)\mu
\ge a/k=(k+1)\delta\ge3\delta.\tag{S6}
\]

这使用actual W，不把整个目录并集客户C替代W。

## k=1：保留未被覆盖的B\A

H无后继选择B，根只覆盖A，B\A未覆盖。后继用r个普通花瓣，1≤r≤m−1，总大小P，故W=a+P。每个后继可静态投B，得

\[
\mu\ge f_B(1)=w-a/2,\qquad P\ge(m-1)\mu.\tag{S7}
\]

已用普通花瓣大小≥μ，未用普通花瓣大小≤μ；因此可把全部r个已用普通花瓣放入一个最优m支持，余下m−r席是否含B由同一个上界处理：

\[
O\le P+\max(w,\mu)+(m-r-1)\mu.\tag{S8}
\]

即使某已用普通花瓣小于B，它仍不小于所有未用普通花瓣，且r≤m−1，仍有一席可容B。由(S7)(S8)，

\[
2W-O\ge2a+P-\max(w,\mu)-(m-r-1)\mu
\ge2a+r\mu-\max(w,\mu).
\]

若w≥μ，右端≥2a+μ−w≥3a/2；若w≤μ，右端≥2a+(r−1)μ≥2a。因δ=a/2，均≥3δ。加回核心得到(S1)。m2只能k1，本段包含该边界；不存在后继的m1不属定理。

## 无正差时的基线：异号坐标所必需

对本目录类，任意固定合法根、任意完整suffix SPE，都有

\[
2W-O\ge |K|\ge0.\tag{S9}
\]

无核根a>0时，按当前分支B后继人数加一置k（此时可k=m），上述k≥2/k1证明并不依赖低分支的存在，分别给\(2W-O\ge a/k>0\)或\(\ge3a/2>0\)。若根残余为空、存在正花瓣，则m−1人是无背景singleton PNE。令最低收益μ>0、已用花瓣数ℓ≥1，有W≥(m−1)μ与O≤W+(m−ℓ)μ，所以2W−O≥(ℓ−1)μ≥0。若全花瓣空，残余W=O=0。加回K完成。仅一正花瓣时同根收益唯一，δ>0不发生；S9仍适用。

## 任意多个独立坐标、异号收益差及根修复

保险有有限多个客户不交坐标l，联合目录是全部坐标主题的Cartesian并集。每坐标都属上述精确类。固定同一联合保险根，H,L在每一根分支以下分别按该坐标的一份**完整suffix SPE独立执行**；选择该份策略只可在根分支确定，后面不跨坐标切换。

置\(\delta_l=u_l(H)-u_l(L)\)、\(D_l=2W_l(H)-O_l\)。δ_l可异号。若δ_l>0，S1给D_l≥3δ_l；若δ_l≤0，S9给D_l≥0。客户不交且目录完整积，覆盖最优的m元组可按位置任意配对，所以OPT和实际W准确相加，得

\[
2W_{ins}(H)-OPT_{ins,m}=\sum_lD_l
\ge3\sum_{\delta_l>0}\delta_l
\ge3\sum_l\delta_l.\tag{S10}
\]

也可保留每个共同核贡献Σ|K_l|，但修根只需显示的弱式。旧主计划τ正深度全为SPE，根缺陷Δ>0；取旧最大偏离B*并保持**同一联合保险根**，根IC要求Σδ_l≥Δ，因此

\[
\boxed{2W_{ins}(H)-OPT_{ins,m}\ge3\Delta.}\tag{S2}
\]

这不预设每个分量支付方向一致。只在根决定各分量模式允许；若根后继续联动选择续局，每个投影未必genuine SPE，S10前提不再自动成立。共享客户破坏利润/OPT相加，一般交叠极大覆盖破坏资源工具，本结论均未排除这些机制。

## 每个m的达到值与三种成本

\(|X|=2s,|Y|=(m-1)s,|Z_j|=s\)共m个不交保险主题，m≥2、s>0。固定根X的H为\(XY^{m-1}\)，L为\(XXY^{m-2}\)，同根收益差s。完整策略在[多主题修复定理](多主题独立保险的三倍根修复与半覆盖等价--定理.md)和[审查域页](../审查/独立保险两次内部审查的先验与证据域--审查.md)给出：H根X后所有历史Y；L第二人X而之后所有历史Y；根Y后首非Y为X则全Y、为Z则永久精确前缀BI；根Z任取完整BI。已有X时Y≥s而改X/Z≤s，第二人X/Y同s，纯Y前缀选X2s而其它≤s，保证全部历史可信。

actual保险只覆盖X∪Y，全部m块却能各选一次。因此

| 对象 | 两主题X/Y | m主题padded |
|---|---:|---:|
| 总并集客户C | (m+1)s | (2m−1)s |
| 高分支actual W | (m+1)s | (m+1)s |
| 同实例OPT_m | (m+1)s | (2m−1)s |
| 2W−OPT_m | (m+1)s | 3s |
| 同根δ | s | s |

padded精确达到3δ，对每个m≥2锐；m2两构造相同，无Z，低路径XX只覆2s而高XY覆3s。m>2新增Z未actual覆盖，OPT增加(m−2)s，损耗减少(m−2)s，但总C反而增加同量。所有s有理时，全旧新实例共同清分母才回单位客户。

本页的3对独立保险结构类锐，不是对所有旧计划的R4最优常数。原half等价的R4是\(OPT_{old,m}-2W_{old}\le3\Delta\)对所有正深度SPE计划；尚无违反者，本页不证明其全称或不存在更强的旧计划不等式。也不把fresh缺陷的相同编译减3s误当原half与fresh候选等价。

## 版本与证据

1827B是供未读证明者重构的**仅陈述候选**，列S1/S9/异号坐标三个结论；不能因该文件用“候选”把后续证明删掉，也不能回写它的原字节。7242B主稿有完整证明及多坐标追加；7382B独审逐项重构singleton工具、内部根w−a、k两段与K范围，并报告34实例/750同根终局对/90正差的有限Fraction审计。这些统计在本批只按原文保存；原程序字节未齐，本批该入口0。一般量词由上面解析证明承担，不由有限统计或状态标签承担。原完整字节、claim与当前比较快照见[证据目录](../../tools/evidence/insurer-span-and-sharp-dilution-primary/README.md)。
