---
id: "customer-attraction/legal-prefix-static-extra-slot-budget-and-conditional-reduction"
kind: "lemma"
type_tag: "引理"
title: "合法前缀的静态额外槽预算与条件归约"
status: "static-bound-and-LP-duality-proved; conditional-half-implication-valid; universal-WP-and-individual-floor-refuted"
summary: "完整合法前缀预算v>=OPT/(2m)、安全最优查询接入及可分数删除LP对偶；保原条件归约却纠正旧WP开放状态，银行反族否定过强逐人保底而不否定half。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/weak_pushforward_individual_reduction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/weak_pushforward_individual_reduction.md"
---

# 合法前缀的静态额外槽预算与条件归约

## 来源、真值与原模型

[2167B弱推送归约](../../../../tools/evidence/weak-pushforward-and-static-prefix-primary/original/b82223f1516f80533ccd/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/weak_pushforward_individual_reduction.md)及[2590B历史路由](../../../../tools/evidence/weak-pushforward-and-static-prefix-primary/original/666061ceda2882cfd25d/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md)全文实读。静态下界、有限minimax条件推导及附属LP表示正确；原文“只剩WP仍OPEN/继续攻WP”是历史状态，普遍WP现在已被反例否定。保留有效条件蕴含，不把假前提误记为一般half证明，也不把整份静态数学随旧状态退休。

有限单位客户N、有限非空共同目录S、m≥1位单位提供者，全部有序历史纯SPE和任意平局；空主题、重复主题、零客户都保留。固定长度k的合法原主题前缀，负载b，r=m−k≥1名剩余。强制当前行动B后按同一原策略得完整r槽Z(B)，当前actual最优收益u。查询A与产生Z(B)的B独立同law p，

\[
C(p)=\mathbb E_{A,B\text{ iid }p}
\sum_{x\in A}\frac1{1+b_x+c_x(Z(B))},\qquad
D(p)=\mathbb E_B u_{current}(Z(B))\le u.
\]

强式为D(p)≥C(p)，弱式WP为每个p都有u≥C(p)。后者没有要求强制根的平均收益本身付款；但它仍是一个普遍个体节点命题，不等于总福利half。

## 合法前缀的静态下界

定义查询独立的r个合法静态对手安全值

\[
v_{r+1}(b)=\max_p\min_{z\in S^r}\sum_Ap_A
\sum_{x\in A}\frac1{1+b_x+c_x(z)}
=\min_{Q\in\Delta(S^r)}\max_T\mathbb E_Q f_{b,z}(T),
\]

其中f_(b,z)(T)=Σ_(x∈T)1/[1+b_x+c_x(z)]，等号用有限零和minimax。单纯形紧且收益连续，最优p和Q都取到。每个r槽Z(B)合法、查询A独立，所以对安全最优p*，C(p*)≥v_(r+1)(b)，不要求真实推送分布是静态最优对手。

任取Q，置L_x=b_x+E_Qc_x(z)，g(T)=Σ_(x∈T)1/(1+L_x)，M_Q=max_Tg(T)。倒数凸性逐查询给max_T E_Q f_(b,z)(T)≥M_Q。固定一个最优m元组，其客户重数d_x满足

\[
\mathbf1_{d_x>0}\le\frac{d_x+L_x}{1+L_x},\quad
OPT_m\le\sum_x\frac{d_x}{1+L_x}+\sum_x\frac{L_x}{1+L_x}.
\]

首项是m个合法比较主题的g值之和，≤mM_Q。第二项也≤mM_Q，关键不是任意b，而是b确由k个原合法主题组成：若mu_T为这k个主题计数加Q中r槽的期望主题计数，则mu≥0、Σmu=k+r=m且L_x=Σ_(T含x)mu_T，因此

\[
\sum_x\frac{L_x}{1+L_x}=\sum_T\mu_Tg(T)\le mM_Q.
\]

对所有Q得OPT_m≤2m max_T E_Q f，取min_Q便得到准确静态结果

\[
\boxed{v_{r+1}(b)\ge OPT_m/(2m).}\tag{STATIC}
\]

它不需要SPE，但**需要合法k主题前缀且k+r=m**。不能因为两人代数允许实背景，就把任意非负b代入这个按m付款的计数预算。

## WP若成立的条件蕴含

若所有合法节点及每个p均有WP，取各节点静态最优p*，便有u_i≥C(p*)≥v_(r+1)(b)≥OPT_m/(2m)。沿原实际路径求和给W≥OPT_m/2。全零客户时全式为0；前缀固定主题/真实完整后继和同目录没有被删去。

这是正确条件归约，非WP证明。定义K_(T,B)=Σ_(x∈T)1/[1+b_x+c_x(Z(B))]、Mfull=min_Q max_T(KQ)_T，则C(p)=p^TKp。弱WP对每个p是自由Q完整根Mfull的充分条件：这里调用有限对称两人博弈的对称混合Nash存在定理（Brouwer固定点，不是构造算法承诺）；在该p上max_T(Kp)_T=p^TKp；若全p WP则这个值≤u，取Q=p即给Mfull≤u。这里只用该充分方向，不把不同量词的合同写成等价。[菜单资料](../资料/完整根菜单的联合势义务与排序边界--资料.md)保完整合同及抽象矩阵的逻辑区别。

## 当前WP和逐人结论都已有一般反驳

已证[银行完整SPE族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)使用m个经济客户、m−1个各含两客户的银行块、完整乘积主题T_ab={e_a}∪B_b；其全历史控制器给

\[
u_1=\frac m{m-1},\quad W=2m,\quad OPT_m=3m-2,
\quad t_{m+1}(0)=\frac12+\frac{2(m-1)}{2m-1}.
\]

这里t是自由**分数均值**值，真正整数静态v另由Jensen满足t_(m+1)≤v_(m+1)，不宣称相等。m4时u4/3<19/14=t5≤v5；安全最优p*使其真实完整推送C(p*)≥v5>u，故全p WP已假，无需求出p*或运行新搜索。零背景根节点即可失败，也就不能以“仍欠任意合法背景”保留普遍WP。

更强的逐人OPT/(2m)结论本身也不是一般真命题。该同一族给

\[
\frac{OPT_m}{2m}-u_1
=\frac{m^2-5m+2}{2m(m-1)}>0\quad(m\ge5).
\]

m5为5/4<13/10、差1/20；m6为6/5<4/3、差2/15。它不反驳half，因为W2m而2W−OPT=m+2>0；个体保底与总体补偿不同。旧“WP充分half”的蕴含仍有效，但假前提和这个过强逐人目标不能继续当作待证普遍步骤。

## 覆盖采购预算的精确LP表示

附属表示单独取v≥0（应用v=u_i确满足），A_(x,T)=1_(x∈T)，z_T≥0为辅助**实采购量**，不要求Σz=m、也不是原玩家分数承诺。令

\[
B(v)=\max_{z\ge0}\left[\sum_x\min(1,(Az)_x)-v\sum_Tz_T\right].
\]

用s_x∈[0,1]、s≤Az写成有限LP：max Σs−vΣz。其对偶minΣbeta_x，约束alpha,beta≥0、alpha_x+beta_x≥1、A^Talpha≤v。任一alpha>1可截成1，保后一个约束且不增加所需beta，故可取0≤alpha≤1、beta=1−alpha。有限LP强对偶遂给

\[
\boxed{B(v)=|N|-\max\{\sum_xy_x:0\le y_x\le1,
\ \sum_{x\in T}y_x\le v\ \forall T\}.}\tag{DELETE}
\]

v≥0时z0和y0都可行，0≤B(v)≤|N|；保留质量多面体紧，最优y取到。因此B(u_i)≤W恰等价于存在一份**可分数删除**，总删除质量Σ(1−y_x)≤W，使所有原主题保留容量≤u_i。不是要求删除整数个客户，也没有从SPE构造这份y。v0时没人接受的客户可全部保留，不误把B0一概等于|N|；零客户全式0。

DELETE是精确表示，不自动给WP、早期玩家付款或一般half。这里的z域也不同于STATIC中恰m槽的目录计数，不能因都写覆盖预算而共用费用或量词。

## 历史搜索和缺失实现的范围

README称search_individual_floor.py从合法SPE路径转固定策略锥作浮点LP交替，原记号p7/m5、8seed×10轮最低比1/9未到1/10；没有其代码/完整输出，不把80当真实LP调用数或有限阴性当普遍floor证明。search_terminal_pushforward.py分别攻击D≥C及--weak的u≥C，浮点candidate_*不自动认证；exact标签也须有实际输入/完整SPE和精确算式，不能只看文件名。

原路由2026-10-22记k2复制的弱推送“阳性”因额外查询漏+1而撤销，保其软件错误历史，不当真实反例。后来的Mfull替换、后继价格比较、270/348势排序是不同接口；270和381原JSON本地未取得，README数字/发现叙述只保作者范围。已核348及其他当前反例见菜单资料，不回填成这两缺件已认证。

本批无新数学CLI/LP/全SPE或样本扫描；完整静态/对偶与当前真值的比较均为解析推导。四个被引用代码/报告和两旧JSON的本地缺失有真实回执，不补网络、不冒读/复现；旧角色/下一步路线只存历史，不成为本轮cleaner命令。
