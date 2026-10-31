---
id: customer-attraction/cyclic-parent-review-auxiliary-contracts-and-evidence
kind: review
type_tag: 审查
title: 圆环可信性父审的旁支合同与证据身份
status: historical-internal-review-and-self-contained-auxiliary-scope; no-new-independent-runtime-audit
summary: 保父审先验及GAP伪摘要、自由t删除45/2对11ε、坏maxhub规则和PseatCov/r2边界，引用源不额外done。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/parent/review_summary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/parent/review_summary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/relay_transport/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/relay_transport/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/tail_credit/gap_and_deletion_obligations.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/tail_credit/gap_and_deletion_obligations.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/shared_seats/parallel_omission_obligation.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/shared_seats/parallel_omission_obligation.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/mixed_menus/max_standalone_hub_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/mixed_menus/max_standalone_hub_boundary.md"
---

# 圆环可信性父审的旁支合同与证据身份

## 这份父审究竟覆盖什么

3667B `parent/review_summary.md`是2026-10-23内部审查记录，不靠同意人数投票，不认证外审或新颖性。本轮完整读它，以及对应圆环作者/代码/全输出；其圆环独立先验与完整参数分类见[圆环完整可信子局](../定理/八标签圆环族的完整可信子局与最小首位收益--定理.md)。父审称先独立按会员位重建、再收到作者最终表逐行核；这保原历史，本轮已知情读双方不是新blind。

父审另指独立`audit_cyclic_credibility.py`/`cyclic_credibility_independent.json`生成全部正分界与区间代表。**这两独立程序/报告本批未取未读未执行**；本批真正全读的是作者5060B仿射程序及7476B报告，不能按“独审通过”补造其日志。其余四类父审摘要不是圆环定理的推论，下面用必要related原稿补定义和精确逻辑范围；未给这些related源额外primary receipt。

## GAP-r是什么，伪孩子摘要究竟反什么

原候选在任意合法完整有序历史h、背景b、余r人、同一完整纯SPE的真实终局尾负载c上定义
\[
P_h=\sum_x\frac{c_x}{b_x+c_x},\qquad
F_r(b)=\max_{q\in\mathcal S^r}\sum_x\frac{c_q(x)}{b_x+c_q(x)}.
\]
零分子项取0。P只算剩余玩家利润，不能换成全覆盖或背景玩家利润。候选(G)为F_r(b)−P_h≤r min_j u_j，等价逐个j有F_r≤P_h+r u_j。若它对所有这些对象成立，由r min u≤P得到F≤2P，空背景便推出half；相关10055B原稿没有证明或真SPE反例，本父审也不提供它的全人数证明。

父审核的是**摘要归纳模板**失败：任意k≥3，r=(k−1)²+1，目录恰r个互不交、各k客户主题。对每个强制根a，指定伪终局先k次a、再r−k个不同非a题。所有根收益1，全部根间比较相容。孩子背景1_a中尾利润(k−1)+k(r−k)，最优r−1主题全部选非a，F_child=k(r−1)，孩子min利润1，故孩子gap=(k−1)²=r−1，恰满足每份孩子(G)摘要。

父根F=kr、P=k(r−k+1)、minu1，gap=k(k−1)>r，严格差k−2。k3/r5时父F15/P9/gap6>5，孩子F12/P8/gap4=4。因此“每个孩子只交一个(G)结论+根全部偏离最优性”不够归纳父(G)。

这不是完整SPE：在r个等大不交题、r玩家的每个历史，总有未用题；末位fresh得k、old至多k/2，逆向归纳后继总fresh，使此前fresh也保留k而old≤k/2。因此真SPE全fresh，伪列k重复不可信。任意预先固定d，可取k大到r−k≥d，把最后d个不同新题补为该节点真正完整SPE；前面的复制仍不可信。不能把“最后固定d深可信”替换成孩子整个r−1人可信，更不能把这个伪菜单称GAP-r或half反例。

## 硬删除守恒与自由门槛亏空的反例

固定真实终局中的根主题A、背景b，其他玩家分保留H与删除L，负载h_x/l_x。这是终局代数删除，删除后不自动是较少人数SPE。根释放
\[
\Gamma_A(L)=\sum_{x\in A}\frac{l_x}{(b_x+1+h_x)(b_x+1+h_x+l_x)}.
\]
删除组原在A上利润P_L(A)=Σ_(x∈A)l_x/(b_x+1+h_x+l_x)，故0≤Γ≤P_L(A)≤P_L。更一般若所有保留者负载k_x>0，每名保留者增加l_x/[k_x(k_x+l_x)]，乘k_x恰l_x/(k_x+l_x)，等于删除组原利润；k_x=0客户消失。**绝对利润**有守恒意义，“低于某门槛的亏空”没有这项守恒。

父审的精确数字来自固定13人、36单位客户、六题A/B/T/D/E/P原SPE。兴趣重数是A2、B2、T1、TD1、TE1、ADE3、BDE1、P25；actual P^10,A,A,B，前12人各5/2、末位3，W33/OPT36。原10055B稿和父审称已独立重放完整自动机，27243节点/112050项真偏离；本批未重跑该DAG或读取其新执行日志，不把这次读父审称一次新SPE认证。

六根强制分支（A,B,T,D,E,P）根都5/2，tail总利润依次61/2、63/2、63/2、61/2、61/2、61/2。任取0<ε≤1/24、t=5/2+ε，全部根d<t且全部tail≥12t。P分支低尾L恰后9个P与2个A，删后根P独享25，所以Γ=25−5/2=45/2，而低尾总亏空Σ(t−u_j)=11ε。任意有限K≥0再取ε足够小，都违Γ≤KΣdeficit；K<0更立即失败。

承重是**自由外定t**，不能改为t=v、OPT相关内生门槛或一份普遍安全值反例。此例F13−P=36−33=3，而13minu=65/2，所以它不反(G)，也不是half反例。原根返还45/2和删除组总亏空11ε属于不同费用定义，不可用“低尾很接近t”就说绝对稀释小。

## hub反的是唯一最大单独收益的选根规则

related4914B给正偶k≥12，M=C(k,k/2)、p=M/2−1。M=2C(k−1,k/2−1)为偶数，p是正整数。目录是H与k个外围P_i；对每个k/2子集J造1核心客户，喜欢H及J内外围，共M；各外围另p名独有客户。H大小M、外围M−1，所以H唯一maxstandalone。两个不同外围核心交集B=M(k−2)/[4(k−1)]。

完整两人策略：H后末位选P0；P_i后选P_(i+1)；根选P0。H后的所有外围末BR给3M/4−1>H的M/2，强制H首位d_H=3M/4。P_i后所有其他外围末BR给v=M−1−B/2，严格超过H的3M/4及复制P_i的(M−1)/2。根外围值v>d_H，所以完整SPE根由外围救回，实际W=OPT2=2M−2−B。

三个静态iid提供者的对称分布q在外围均匀、H概率0。g3(t)=1−t+t²/3，支持外H值7M/12，外围共同λ=(M/2)7/12+(M/2−1)g3(1/k)，λ>H值，故是真正对称iid Nash。唯一maxstandalone强制分支却满足
\[
\lambda-d_H=M(k^2-12k+4)/(24k^2)-g_3(1/k)>0.
\]
首项对k≥12递增、M按偶k递增，至少77/72，g≤1，严格正；但实际根v>7M/8−1，λ≤19M/24−1，所以v>λ。k12的M924/p461/B210，共6456客户/13题，d_H693、λ=299441/432=693+65/432、v818、W=OPT1636。

因此只反“先选唯一最大单独收益主题，其每个真末BR都会支付iid值”的辅助规则，**不反实际SPE首位iid保底**，也不反BR支持递归闭包、自由Mfull或half。父审记不同研究员先盲重建/再单位展开的一般偶参数与两人比较；本批仅全文读作者MD，未读或运行其audit/独审程序，不造新的k12/14或偶k至100日志。

## P-seat必须保块可实现性，r≥3仍只定位交换缺口

related4652B的v2固定完整SPE实际覆盖C，U⊆N\C划为不交非空块Q_j、a_j=|Q_j|，要求每个合法A的U截面是空或一个完整Q_j（P），并且每个块确由某合法A实现（Cov）。C上兴趣任意，同块可被多个不同极大题共享，不要求全局私有或主题包含。

v1漏(Cov)。父审一句r1反例可显式化为N={x}、唯一合法空主题、U=Q1={x}、m1/z1：P成立、容量1，但唯一SPE利润0<1。这里只把该缺陷写清，不是新搜索；补Cov是改变输入假设，不能静默把v1标正确。用于U=O\C、O为合法比较并集时Cov自然成立。

对任意有序h，q_j为过去触块动作数。z>0，d_j=max({0}∪{s∈{1,…,m}:a_j/s≥z})，R(h,z)=Σ_j(d_j−q_j)_+。v2候选是余r且R≥r时每份完整子SPE每人≥z；一动作至多令R减少1。r1由Cov选live块给a_j/(q_j+1)≥z。

r2在固定背景b定义F_b(A)=Σ_A1/(b_x+1)，同终局两玩家差精确等于F_b(A)−F_b(B)。当前者选所有live组题中F_b最大B，真实末位至少z；若末位不碰B块，根独得该块≥z；若同块，末位题也属于原live集合，F_b最大性和同终局差使根≥末位≥z。SPE最优性给实际根保底，任意实际第一动作后剩R≥1给实际末位保底。因此r≤2成立。

r≥3时其他后继负载d会把差改为Σ_A1/(b+d+1)−Σ_B1/(b+d+1)，C上权重随真分支变。A=Q∪{x}、B=Q∪{y}、b0，若其他后继盖x不盖y，则原F_b并列而根减后继=−1/2。该小菜单只反固定最大F_b中继，未经完整SPE认证，不是P-seat-v2反例。

若全r候选成立，actual前缀q0可取多重谱{a_j/s}第r大λ_r，得u_i≥λ_(m−i+1)、W≥Σ前m大λ≥Σ前m大a_j；(P)下每个最优题至多一块，故D≤W进而half。U空时遗漏为0平凡，谱按零补足。这只是条件推论。一般比较O中I=|O∩C|、D=|O\C|、G=|C\O|、W=I+G，half实为D≤I+2G；原稿所引71客户完整例W35/OPT38/D36/I2/G33说明一般D≤W不能省G，且其遗漏结构不属P。本批不重验该71输入/策略，不借它反v2。

## 状态、依赖与接续边界

上述旁支数学的必要related3原稿共19621B全部真实读，sourceSHA/原版本独立保；它们不因被父审引用而额外done。已全文比较[普通尾删除恒等式](../障碍/聚合尾部删除稀释恒等式--障碍.md)：它保D3–D9/驻留余项和7节点例，不等于这里自由t的45/2对11ε；[固定旧背景停界](../障碍/固定旧背景正信用与连续调和替换的停界--障碍.md)仅短导航P-seat，不等于完整P+Cov定义/r2证明，故不能整页duplicate。

父审原末尾的一般EI/Mfull仍OPEN是当时状态；现在另有银行真SPE否定一般逐人extra-one/Mfull，五人half另证，本圆环/上述模板材料不解决六人half、全r GAP/P-seat或新全位置预算。本页保候选、已证局部代数、伪菜单障碍、旧真实反例报告、原内部复核范围各自身份，没有把方法停线句变成当前执行指令。

## 原件与证据资源

- [44b9984032aaaf8c1c03 3199 B 原件](../../../../tools/evidence/cyclic-complete-credibility-and-parent-review-primary/original/44b9984032aaaf8c1c03/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/relay_transport/README.md)
- [0529db2ca84292e185cb 3667 B 原件](../../../../tools/evidence/cyclic-complete-credibility-and-parent-review-primary/original/0529db2ca84292e185cb/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/parent/review_summary.md)
- [6b953dda924f48243d6b 10055 B 原件](../../../../tools/evidence/cyclic-complete-credibility-and-parent-review-primary/necessary-related-original/6b953dda924f48243d6b/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/tail_credit/gap_and_deletion_obligations.md)
- [857599e66de0a1b953e9 4652 B 原件](../../../../tools/evidence/cyclic-complete-credibility-and-parent-review-primary/necessary-related-original/857599e66de0a1b953e9/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/shared_seats/parallel_omission_obligation.md)
- [734269b6e8a84cfea402 4914 B 原件](../../../../tools/evidence/cyclic-complete-credibility-and-parent-review-primary/necessary-related-original/734269b6e8a84cfea402/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/mixed_menus/max_standalone_hub_boundary.md)
