---
id: "customer-attraction/real-child-price-switching-old-counterexample-and-optimal-query-quantifiers"
kind: "resource"
type_tag: "资源"
title: "真实child价差的旧反例与最优查询量词"
status: "fixed-actual-max-payment-refuted; shorter-optimal-query-budget-open; complete-source-priors"
summary: "旧13人36客户完整SPE只否13maxg≤W+G，静态gap37/66；新P*允许k≤m、不同固定m槽K0，旧例P*=557/66/K0=724/33均过。保OPT-CREDIT、同叶不跨child和cap/ALL真实停止点及非盲读序。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/credible/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/credible/joint_child_slack_support.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/fresh/child_support_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/convex/aggregate_payment_attempt.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/convex/README.md"]
---

# 五源的数学与历史身份

8263B child主稿、7536B非盲审查、1080B credible入口、5093B aggregate付款尝试、1141B convex英文入口，共23113B，全部全文主读。child主稿/审查此前仅作MY related并未primary done，本次完整数学在[整数支持/同叶cut](../定理/整数背景静态支持与同叶截口共同信用--定理.md)自足给出。cap/ALL/运输的域在[固定actual退出引理](../引理/固定实际叶的可信退出重选与共同列门槛--引理.md)完整重构；没有因旁读或入口导航免原源处置。

原主稿/credible README写“尚待独审”是其时点，7536B后来已逐定义核SUPPORT/MIX/SLACK/整数B/截断/非空背景/cut/false状态通过。但其首次工具读取返回作者全文，见过证明，准确身份为**非盲独立重构**。没有外审/新颖性认证。作者将一般静态对偶/Fenchel支持归已有数学，不认领一般工具首次。

convex入口记录三种实际聚合尝试：共同query的Mpath全部列矛盾，保own列actual的有利cap端点选择，和停时运输避免重复提款。每种都未产新一般金额；后两行已由旧whole-IC去相关/插入税付，不把它们重复收钱。另导航父方后来有限字典LP独审，收到公式提示后核grid/epi/有理负点实现/EJ，而非blind；该父稿/独审已在MY主源完整整理，不由本入口重复done。

当前five半覆盖另真；原一般/五人OPEN不抹现定理，也不从现定理推Mpath、SUMmin-full、最优查询价或任意背景五人已付。六人缺前四位实际聚合预算，和背景/切枝换价仍未由这些静态工具闭合。

# 固定actual纯max付款已被旧完整SPE否定

价格g_z(T)=Σ_(x∈T)1/(1+c_z(x))，M=max_Tg_z(T)，G=Σ_(c>0)1/(c+1)，K=Σ_(c>0)c/(c+1)=W−G。这里M是**固定actual静态pure-max价格**，非真当前floor，也非自由背景minimax。

完整旧证书为13名提供者、36名单位客户、六主题A,B,T,D,E,P。兴趣型为A:2，B:2，T:1，TD:1，TE:1，ADE:3，BDE:1，P:25。已发表[反例](../反例/实际均匀缩放负载的弱付款桥--反例.md)和[全自动机核验](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/73b21aa15b684ae93481.md>)保27243节点/18675决策节点/112050含own整数IC成功的完整身份，actual P^10,A,A,B，W33、OPT13=36；本批不重跑旧自动机。

actual客户负载是5客户c2、3客户c1、3未覆盖、25客户c10。所以直接静态价格

\[
 (g(A),g(B),g(T),g(D),g(E),g(P))
 =(5/3,3/2,3,5/2,5/2,25/11),\quad G=359/66,
\]
\[
 K=1819/66,\quad 13M-W-G=13M+K-2W=37/66>0.
\]

这否定fixed actual mM+K≤2W，不能继续称OPEN。审查原回归只从packet走actual并算这些标量，未重审13层IC；完整SPE身份由既有全自动机承担。本次为已知输入的解析对照，非新实例或新程序运行；更不是half反例，half余额2W−OPT=30。

# 新P*允许少于m槽，不能偷换为旧K0

本源较弱候选：所有覆盖达到OPT_m的主题组，可去冗余只留k≤m个主题，

\[
 P^*(z)=\min_{\cup_{j=1}^kT_j\text{达OPT}_m,\ k\le m}
 \sum_{j=1}^kg_z(T_j),\qquad P^*\stackrel{?}{\le}W+G.
\tag{P*}
\]

这是在所有k≤m的最优覆盖组中最小化价格，**不是另要求先使支持基数k全局最小再比价格**。OPT0可用空组或零价主题处理。对具体最优组并集O、重数d_x，逐客户精确得

\[
 K-[|O|-\sum_jg_z(T_j)]
 =\sum_{x\in C\setminus O}\frac{c_x}{c_x+1}
 +\sum_{x\in O}\frac{d_x-1}{c_x+1}\ge0.
\tag{OPT-CREDIT}
\]

故OPT_m≤P*+K，(P*)若真足以half。给其右侧再加全部OPT-CREDIT只变成目标等价账，不是新增付款。原SPE如何共同支付具体最优查询价仍未证，尤其不能将query总和重新放大成已false的m maxg。

已有[固定m槽fresh候选](../想法/最优覆盖查询的自留份额预算--想法.md)定义K0=min_(最优**m元组**)Σ_(j=1)^m g_z(T_j)，保重复补齐槽。P*≤K0，但二者不一般相等：P*可以直接删冗余，K0仍付补齐费用。该旧页精确保padding从全目录最小价g_min选重复，不能把“支持少于m”误成m槽定义删了。

旧13例中，私有A/B/T/P客户迫每个覆盖全36的组都含A,B,T,P，这四主题各自覆盖互不交的5/3/3/25客户，恰好全覆盖。其它主题价非负，故

\[
 P^*=5/3+3/2+3+25/11=557/66.
\]

原13槽元组至少这四个主题，余九槽按全目录最便宜B、价3/2补齐且不变覆盖，因此

\[
 K_0=557/66+9(3/2)=724/33,
\quad W+G=2537/66.
\]

两候选均在此旧例通过：W+G−P*=30，W+G−K0=33/2。四主题最优支持的OPT-CREDIT为0；13槽补齐元组的重复B信用为9·(3/2)=27/2。重复13个最大主题T费用39根本不覆盖最优，不能否(P*)或K0。以上是读完整旧单位输入后的静态分数代入，**没有**重跑packet/新扫描或新SPE认证。固定旧M桥失败、P*开放和K0更强开放是三种量词，不因同一价格g合并。

# child支持、actualcut与换价的共同缺口

SUPPORT本身任意叶可用，SPE只保证所给child叶是真实可选；混合必须同一Q，查询不能依抽叶换最有利子SPE。SLACK保真实负载支持比(d,L)两数有内容，但不将任意αslack变非负。CUT仅同一实际叶价格恒定、所有Θ总额受同一U_a；单Θ可超当前利润、非空背景B1可正，不赋予每cut一份W。

换child分支改变总负载L/价格，原相消不跨枝；Mpath ALL也只覆盖原actual前缀，不能将t当新子树统一门槛。cap拼合保actual只需首次异常当前收益cap，own列必须原z；选势最大端点不让别输入尾成为可行比较。这是源精确停止点，不是证明所有换价/运输方法不可能。

旧原13纯共同查询失败不能越界判最优具体查询价；同叶支持的peer银行m5压力67/5<20只对那族真实Q。源未寻找新固定规模正面工程、未重开PF/SHARED阴性扫描/旧端点/KKT-Bregman，入口无Git/work.py或spawn是原分支历史，不是本worker的外部stage权限。

# 原有限证据及本次阅读边界

fresh原审查报告972系数与1275单客户cut链回归，另从压缩packet重走actual算37/66；它不声称再审完整13层IC。generic SUPPORT/整数余项/cut由解析核查承担，不以有限点替代。convex三尝试无新程序，原字典Fraction伴随核重建资源菜单不导作者/规范求解器，只是后来工具的finite算术支持。

本批数学依据为五全文、已发表whole模型/菜单/旧13反例与自动机/fresh定义比较；准确原件、程序与输入可得性、0重复旧run、自查和逐源处置另保证据。新有信息的下一步仍是同一最优指派上的真实后继IC价差或可共同支付的原actual预算，不是复包装fixed M、同cut余额或仅行次随机的停时矩阵。

原件、旧成功同SHA复用、真实0-run范围、关系和逐源处置见[本批证据](../../tools/evidence/integer-child-support-and-cap-selection-primary/README.md)。
