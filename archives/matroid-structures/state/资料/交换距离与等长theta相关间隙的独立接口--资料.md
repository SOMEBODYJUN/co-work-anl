---
id: matroid-structures/exchange-distance-and-equal-theta-ledger-interfaces
kind: resource
type_tag: 资料
title: 交换距离与等长theta相关间隙的独立接口
summary: "逐来源保留交换距离与等长theta相关间隙的独立接口的精确模型、量词、关键论证和证据/版本边界，不升级外审或新颖性。"
status: proof-candidates-with-internal-reconstruction; applications-and-novelty-pending
legacy_ids: [SEL-MATROID-EXCHANGE-DISTANCE-v1, CS-THETA-EXACT-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/CLAIMS.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_and_girth.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_and_girth.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_independent_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_independent_review.md
---

# 交换距离与等长theta相关间隙的独立接口

一个对象是公共基profile生成的有向图距离，另一个是graphic rank的独立/相关期望比；共同拟阵背景不产生相互推导。两证明说明及距离独立重构全文实读，均保原proof-candidate等级和未核新颖性，不把本批阅读称statement-blind复核。完整来源见[证据](../../../../tools/evidence/retired-topic-claims/README.md)。

## 完整可行单交换图的距离候选

有限拟阵$M=(E,\mathcal I)$秩$k$，若有回路令$g$为最小回路大小；给非空有限基列表$B_1,\ldots,B_N$，可重复。$D$顶点$E$，有弧$r\to s$当且仅当某$i$满足$r\in B_i,s\notin B_i,B_i-r+s$为基。任意不同可达$u,v$的候选界

$$\operatorname{dist}_D(u,v)\le k-g+3.$$

允许loops、coloops、平行元与不连通；无回路自由拟阵没有弧，另作空断言。这不是两个基之间的基图距离，也不能用于任意删弧子图。

前向证明：对源$u$的距离层令$H_j=\{e:d(u,e)\ge j\}$，含不可达点。基本回路给每基$H_{j+1}\subseteq\operatorname{cl}(B_i\cap H_j)$。最短路第$j$边的见证基有一个距离$j$元素可加入$B_i\cap H_j$仍独立，故$\operatorname{rk}H_{j+1}\le\operatorname{rk}H_j-1$。末边基本回路落在$H_{L-1}$，给秩至少$g-1$；累计$L-2$步得到$g-1\le k-L+2$。

原独立反向重构另证稳定引理：$P(S)=S\cup\{r:\exists s\in S,r\to s\}$，若$\operatorname{rk}P(S)=\operatorname{rk}S$，则$P(P(S))=P(S)$；必须用基本回路和闭包证明，不能只断言“秩不涨即停止”。从终点反向层的首回路秩$g-1$、其后严格增秩导出同界。原全小抽象拟阵审计和GF(2)独立审计覆盖域不同，均不是全部拟阵证明替代。

候选PoA应用另要求对称无权公共拟阵拥塞、非负非减延迟、实际PNE，以及所有已用资源$c_f^+(e)\le zc_f(e)$。路径内部点有出弧故已使用，串单交换最优性得$c_f(u)\le z^{L-1}c_f^+(v)\le z^{k-g+2}c_f^+(v)$。端点条件可用于原交换流而不改流路或容量；$\rho(D),z(D)$的完整函数域、零成本、最终文献版本及优于一般PoA的区间仍未闭合，不能把指数候选$\delta+2$称已完成全部应用或PNE/UM算法。

## 等长多路theta的相关间隙候选

整数$k,\ell\ge2$，图由两端点及$k$条内部互不相交的长度$\ell$路径组成，graphic rank为$r$。独立边缘$x$的$F(x)=\mathbb E[r(R_x)]$；$r^+(x)$是在同边缘任意联合分布中的最大秩期望；$CG=\inf_xF/r^+$，$0/0=1$。令$b=((\ell-1)/\ell)^\ell$、$a_q=((\ell-1+1/q)/\ell)^\ell$。源完整证明草案给

$$CG=\min_{2\le s\le k,\ 1\le q\le s}\left(1-\frac{q a_q+(s-q)b-1+(1-a_q)^q(1-b)^{s-q}}{s(\ell-1)+1}\right).$$

公式对所有整数$k,\ell$，是有限有理最小值；未给全参数argmin分类。不能漏掉$s$的restriction最小化：原定位定理只给最坏$x$对其**support** tight，不给全图base。支持中不完整路径片段都是coloops；其概率一，删除它们使比值不增，剩$s$条完整路径核心，其他路径补零。

设核心路径总质量$a_i$，base域等价于$a_i\ge\ell-1,\sum a_i=s(\ell-1)+1$与$0\le x_e\le1$。令$t_i=a_i-\ell+1\ge0,\sum t_i=1$。秩恒等式给$F=\sum_e x_e-\sum_i p_i+1-\prod_i(1-p_i)$，$p_i=\prod_{e\in P_i}x_e$。固定$a_i$时$F$对各$p_i$不增，AM–GM让路径内均匀取最坏。剩余最大化$H=\sum p(t_i)+\prod(1-p(t_i))$，$p(t)=((\ell-1+t)/\ell)^\ell$。

固定两$t$之和，令$m=\ell-1+(t_i+t_j)/2,z=((t_i-t_j)/2)^2$、$R=\prod_{h\ne i,j}(1-p(t_h))$。依$z$的非恒定部分是

$$\frac{1-R}{\ell^\ell}[(m+\sqrt z)^\ell+(m-\sqrt z)^\ell]+\frac{R}{\ell^{2\ell}}(m^2-z)^\ell.$$

前项为非负系数$z$多项式，后项二阶导非负，故凸。取全局最大点中正$t$最少者，不等的两个正坐标可移到端点而不减$H$并减少支持，矛盾；某最坏点所有正$t$等于$1/q$，代入得显示公式。

源已修$\ell=2,k=3$：非对称$t=(1/2,1/2,0)$给$3565/4096$，旧全对称$637/729$较大，不能当最坏。$k=2$为$229/256$；$k=4,\ldots,16$的某argmin观察及$(3k+5)/(4k+4)$不能升级全部$k$公式。源数值SLSQP与rank小例只为有限证据，外部定位定理导入、系列扩张文献覆盖和不等长路径都各有复核义务。两ID保持证明候选、新颖性未知；第三阶段分别解释来源/组合推导/应用条件，不因同档造边。
