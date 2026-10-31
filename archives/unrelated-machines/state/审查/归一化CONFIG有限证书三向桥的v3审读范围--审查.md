---
id: "unrelated-machines/normalized-unit-config-v3-review-full-finite-certificates"
kind: review
type_tag: 审查
title: "归一化CONFIG有限证书三向桥的v3审读范围"
status: complete-primary-read-and-mathematical-reconstruction
summary: "正support状态LP、完整flat machine CONFIG(1)、state-dummy SC CONFIG(1)及树/两种路径的有限证书方向，Q_D实际NO与旧v3审读历史分开。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md"
evidence_manifest: ../../../../tools/evidence/um-following-review-primary/source-manifest.json
---

# v3身份与当前追加章节

主源26cb8710d1912b82a43f全文7276B/46行实读，包含原v3与后来raw K2 §12两个身份。本文承载UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3；[四次矩续页](raw四次矩单位路径的双向证书与新旧量词--审查.md)另承载后者。当前7d0842cc19e53d2607fe全文536行已读，SHA1617f791…f10b。前35022B恰338行、SHA1dd80c98…9469，机械核与主review所记旧prefix一致；它包含后来§8–11，不能把它们回填到原v3仅header/§1–7的be1a7aa…审查。

域为非空有限groups、每组非空indexed states、非负二进制有理p且每state总量1。同state资源互异；允许零incidence、重复index和unused资源。完整flat UM每state独立private root，每资源unit资源机；每group一个unit selector、每incidence一个原job（private p/resource1），全部未选state/零job保留。

正support P_gs={u:p_gsu>0}。FSLP为λ≥0、各组Σλ=1、各资源Σ_(u∈P_gs)λ≤1，用0/1正support而非p权/all-membership。

# FSLP、完整machine CONFIG(1)与normalform

从λ构造private配置：以λ_gs取{selector}∪本state全部零job，以1−λ取全部incidences，两者真实负载1。positive job private覆盖1−λ、零job覆盖1、selector跨roots覆盖1。每资源给positive incidence singleton权λ，余量empty。所有job恰覆盖1，支持O(states+incidences+resources)。

反向给有限有理machine CONFIG(1)（每机权和1、每job覆盖≥1），α_gs为private含selector概率，各组Σα≥1。positive incidence不能与selector同处private，private覆盖≤1−α，故unit资源覆盖≥α。unit资源配置至多一job，给资源Σα≤1；各组向下减为和1的λ，得FSLP。零job可与selector共居，不能用其作排斥下界。覆盖冗余可逐job剪除、必要时拆分一次，负载不增且显式支持只多项式增长；不保原给定证书全部边际。

二叉选择树T每顶点一group：root选child-own，非root internal own/两child共3态，leaf own/原state，K1直接原state。λ正向以子树概率x_v选child/原leaf，以1−x_v选own，每own资源占用恰1。反向根发1单位流，parent流≤其菜单概率；own容量保证可按非own菜单分流，leaf旧state流不超过原概率，允许多条off-path激活。每原组叶流和1，旧资源只减。

旧菜单路径D按全部语法incident groups列d个ports，包括只出现零项的组；helper d−1个，各相邻singleton unit states。旧正占用x_i和≤1，选hole π_i≥x_i且和1；helper按hole两侧matching，port占用1−π_i+x_i≤1。反向d列相加扣d−1个完整helper行得旧positive占用≤1。d0保unused，d1无helper；零membership影响标签但不占positive容量。N=D∘T同时保FSLP和各自完整machine CONFIG(1)，实际V/UMOPT保持由独立全任务normalform证明提供，不从分数等价免费推出。

# State-dummy与SC路径的准确阈值方向

SC(Q)每state一agent、每原资源一real item、每group K_g−1个只对本组agents值1的dummy；每agent real row1、完整row K_g。实际SCOPT=菜单不交bundle值V：每组至少一个dummy-free agent反解一个原state，反向其余agents各一dummy。

FSLP给agent real完整positive support配置概率λ，其余1−λ均分K−1个dummy singleton（K1没有除法）。反向SC CONFIG(1)含own dummy可剪为一dummy，无own dummy的合法配置必须含整个positive real support。若其概率ρ_gs，则K−1个dummy容量迫Σρ≥1，组内削到1得FSLP。目标t>1时每agent必须有own dummy，K需求>K−1容量，故最高SC CONFIG阈值≤1，可行时恰1。不可混成UM的最小阈值。

SC层路径P_SC按每item的positive agents建d copies和d−1个相邻unit helper agents。实际正向只需0<v≤1，为old owner留hole、helpers各一copy；反向任意v>0，每helper至少占一copy（可两枚），合计留旧agents至多一枚，合回原item保值。故oldOPT≤1时精确保actualOPT，old0也由正值逆向排除。oldOPT>1不作最优值保持。

有限SC CONFIG正向需0<t≤1，以旧item marginals取hole分布；反向任意t>0，helpers配置非空，所有copy列相加可给old总边际≤1。t>1不能把helper强行剪singleton；0用empty配置另处理。old最高阈值≤1才保最高阈值；保old rowtotal，helper row2，copy正度≤3，不能单独把一般SC无界row归到3。

# Q_D真实NO、规模与独立顺序

D≥2，Q_D的main有D态，第a态在一行D个g_(a,j)各权1/D；每(a,j)有helper二选singleton g_(a,j)或A_a。FSLP取main各1/D、helper以1−1/D取g、以1/D取A，所有列恰1。任何正最小值分配中main在一行领r个g，会使相应r个helpers共享一枚A_a，故r≤1；取一g/对应helper一A、其余各本g达到V1/D。经N、state-dummy、SC路径，最终row≤3、item positive-degree≤3、正值仅1和1/D，CONFIG最高1、实际SCOPT1/D；完整flat machine CONFIG(1)可行、实际UMOPT2−1/D。

基础Q_D有D²+1 groups、2D²+D states、3D² incidences、D²+D资源，后转换poly(D)，不是polylog(D)。这是actualOPT<1的SC NO，不是actualOPT≥1 promise的反例，不能据CONFIG gap否定常数finder或提供near2困难源。

给定有限有理证书的转换仅用有限支持、部分和、组内削减、树流、配置剪枝及hole混合；按输入/证书总位长多项式，不取得未知指数CONFIG或不明certificate oracle。完整UM零job与SC可删零价值item不是同一对象。

历史general先冻pre-Exact再仅v1 Exact独立全证，v3只Exact另证machine bridge/SC路径，未读v2/作者Proof；root读两独立记录才释放v1/v3 Proof，再作者读后与最终header/§1–7全文审。v2没有独立Proof可补造；pre-Exact的all-membership LP没有追改成positive。早期只读BS2006作者摘要，未读其CONFIG-gap原Proof；Q_D自足证明不依赖之。BCG路径、tree与state-dummy/selector-parking已知思路均扣除，无软件/有限实验/外审/全球原创认证。

当前§8–11另为阈值叶R_leaf/R_cons与D_+投影gap：其共同叶边边际不是多core共同matching law。此处旧v3不签该增量；其Q_t在弱流中趋二也不升级下一页raw K2 gap。原记录/旧进度均不改。
