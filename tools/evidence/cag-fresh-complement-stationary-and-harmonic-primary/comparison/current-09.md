---
id: customer-attraction/actual-coverage-and-overlapping-optimal-catalog-static-harmonic-boundary
kind: resource
type_tag: 资源
title: 实际覆盖与重叠最优目录的静态调和边界
status: 静态全参数边界与五入口范围保全；不是真SPE的signed预算反例
summary: 半覆盖等号及最优元组唯一仍不能仅静态支付调和重叠余项，m≥2/a≥2族全式自足；原中继/席位/CC/PAY工作区结论与历史先验准确去重。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/FAILED_ROUTES.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/construction/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/harmonic/README.md
---

# 实际覆盖与重叠最优目录的静态调和边界

## 净预算与同一最优元组

有限单位客户、共同目录、m名单位玩家。固定完整有序终局a（本节静态式先不假定SPE），负载c、覆盖C、W=|C|。比较达到OPT_m的恰m槽元组T，允许重复，客户负载d、并集O。令G=|C\O|、U=|O\C|、H₀0，
\[
B_h(c,d)=\sum_x(H_{c_x+d_x}-H_{c_x})=U+R_h,
\]
\[
R_h=\sum_{O\setminus C}(H_{d_x}-1)+
\sum_{O\cap C}(H_{c_x+d_x}-H_{c_x})\ge0.
\tag{1}
\]
OPT=W+U−G，所以B_h≤W+G等价OPT+R_h≤2W，必须由half余量支付非负重复/重叠费用。不是half的等价重写。真正候选是在每份**完整SPE**下存在一个真最优m元组满足此预算，不是每个最优元组，不可把元组换成并集或随意删除重复补满而称同一合同。

对同一元组，逐客户d/(c+1)≥H_(c+d)−H_c≥d/(c+d)（d>0）；得到query净预算⇒harmonic净预算⇒较弱self预算
\[
|O|+\sum_{x\in C\cap O}\frac{d_x}{c_x+d_x}\le2W
\]
⇒half。每步都用同一最优元组作存在见证；d1时三项一致，区分它们需不可去掉的d≥2。当前[净预算元组/支持证明](../证明/终局净预算的元组支持量词与条件付款--证明.md)已完整承载这些静态归约，不再授新候选证明。7044B协调审查及4214B上游入口必要全文比较保[原件](../../tools/evidence/structural-tail-review-and-signed-boundary-primary/comparison-source-manifest.json)，不额外primarydone；它们的有限LP不由此被认证。

## 原harmonic入口未另成稿的静态族

任意整数m≥2、a≥2。目录有m个两两不交实际题A_i，各a名单位客户；另m个比较题T_j=K∪P_j，|K|=m(a−1)、|P_j|=a+1。K、所有P_j和所有A_i客户块全部不交；所有主题真实不同。取有序终局(A₁,…,A_m)，W=ma、c1在C上，c0在全部比较客户上。

全部T_j覆盖|K|+m(a+1)=2ma。若m槽中有r个不同T、s个不同A，r+s≤m：r0时覆盖≤ma；1≤r<m时覆盖≤|K|+r(a+1)+(m−r)a=2ma−m+r<2ma；r=m则必须全T各一次。因此
\[
OPT_m=2ma=2W,
\]
唯一最优无序m元组是全部T_j（有序排列多份），没有重复补满余槽的自由。它们全与C不交，G=W、C∩O空，K客户d=m、P_j客户d1。于是
\[
B_h=|K|H_m+m(a+1)=2W+|K|(H_m-1)>W+G.
\tag{2}
\]
R_h=|K|(H_m−1)>0而half余量0。m1或a1会使这个严格差消失，故保原m≥2/a≥2条件。若看query fee，B_q=m|K|+m(a+1)≥B_h；弱self式则只剩|O|=2W取等。它们在这个静态域确有不同强度，不是三项真实SPE存在桥的反例。

每次把一个T_j换成任何A_i，共同K仍由另外m−1个T覆盖，丢私有a+1、得a，净覆盖严格少1。所有最优排列d相同，所以在最优元组中再最小化Z=B_h+|C∩O|也只得到原元组；并不会制造一个对A_i适用的等覆盖交换。

具体地，一般静态最小Z最优元组只有在替T→A后仍OPT时才给
\[
\sum_{x\in A\setminus T}\left[\frac1{c_x+d_x+1}+1_{c_x>0,d_x=0}\right]
\ge\sum_{x\in T\setminus A}\left[\frac1{c_x+d_x}+1_{c_x>0,d_x=1}\right].
\tag{3}
\]
式由客户增量Z_c(d+1)−Z_c(d)=1/(c+d+1)+1_(c>0,d0)逐项相减，净成本非负来自在所有OPT元组中取最小。这里T包含客户时原d≥1，分母合法。该族的T_j→A_i都损1而不满足前提，不能由(3)付(2)债；仅有half和静态最优交换仍不够。[等槽交换矩](../引理/最优覆盖等槽交换的调和矩--引理.md)也是静态OPT的合法组合，不能替原全部真实后继激励。

**这个终局确定不是SPE。** 末位前全是别的A_i，与每个T_j不交；实际选A_m得a，改T_j得m(a−1)+a+1>a。已遗漏一条严格真实末位比较，不能称完整均衡、signed桥的真实反例或half反例。作者当时判断它不足单列一般进展，只留入口；本页保为有输入/量词/公式的静态边界资源，不升级其等级。

## 五主稿逐项数学与真实时态

原五MD为FAILED2560B、根README3468B、construction README3377B、harmonic README1912B、RT-r独审3793B，共15110B，全篇实读及size/SHA256/blob核。完整[原件清单](../../tools/evidence/structural-tail-review-and-signed-boundary-primary/source-manifest.json)保双冻结来源；下表只说明已完整去向，不以路由表取代上述证明或既有完整对象。

| 主源 | 独有内容与完整数学去向 |
|---|---|
| FAILED_ROUTES | 联合前缀β席位+全部分数覆盖行的v1 m13、v2 m5匹配遗漏松弛反模型，均真实倒二排SPE，完整[共享遗漏障碍](../障碍/联合前缀席位与全部分数覆盖行的共享遗漏障碍--障碍.md)承载；静态占用者桥allm债1但真实末位Γ2可付，见既有[两核心反族](../反例/静态最坏背景的占用收益与真实末位修复--反例.md)；CC跨组重复尾限制3/2及PAY非单调只反辅规则；singleton重建已有更强Hamming旧机制，不称新发现。 |
| 根README | 六分支真实完成交接及各scope：PAY参数/路径而非存在前缀证明、relay首次偏离容量而非总债、omission两非SPE接口障碍、harmonic没有新真实付款、security静态源桥反例非网络反例、construction结构类饱和非一般half。历史程序身份R-7c3db…与用户沿称Boss13/9分开，旧actor不改写；源称六gpt-6.1-sol/ultra分支是当时历史，不代表本次生成代理或常驻任务。 |
| construction README | 从RT-r→单组CC→跨组v2的所有目录条件、最后非均匀组/query变体/zero边界和逐客户饱和，现[跨组定理](../定理/共同核心独立储备目录的任意跨组重复尾屏障--定理.md)及[原合同资源](../资源/重复奖励尾目录扩展与前缀收费的原始合同--资源.md)已全证；代码仅指定k4/r3/x2/a2/b6/d3 fixedtail、25客户/183节点/2379含self/2196非self，非七人根SPE。不把当时未提交/待统一checkpoint当今天保存状态。 |
| harmonic README | signed存在桥尚未真实付款、(1)/(3)层级及本页静态全参数边界；内部RT-r statement-first独审与后来的跨组query重构为不同source/scope，不以引文代全文。[本批独审](../审查/首个非储备动作后的公共尾独立重构--审查.md)完整保公共占用n相消的独有路线。 |
| review_reward_tail | 原只审RT-r精确目录和均匀推论，先陈述自行证明、后读作者四步；首nonD后的真实分类在两条当前偏离分支都成立，第二Bk改D时n相同才能消b/n，所有r1/xk0/d>0先后/zero/平局边界完整入独审对象；不能倒填CC-v2扩目录scope。 |

## 已解局部义务不等于全称付款

原[末偏离中继](../定理/末偏离剥离中继的精确总账与首次偏离容量--定理.md)已把每条全部有序历史非自身IC写成原Γ，末位查询能无债初始化，首次偏离位置的至多单位源能根容量≤W；未付的是跨终局换标总债扣Γ/ρ/初始化信用后的净额，任意源容量仍另证。静态p*最坏背景每占用U≥v已被反，不能继续据零静态regret或ρ自动无债；反点非SPE，仍不反带真Γ网络。

联合显式G谱已被更强完整利润F/G对象充分吸收；仅在这些必要行内调乘子无法排两银行松弛点。CC-v2排同B/隔离E/重复D/分割X前缀的全部跨组脚印，不能再靠同类惩罚参数扩展突破uniform3/2。PAY允许先欠后付并重选t，真正有利前缀仍未证，[左跳族](../反例/真实前缀支付未成立时的最优参数左跳--反例.md)只关闭单调右扫，非PAY/half反例。

security早singleton截断与旧Hamming全参数保护带机制重复，完整[去重资源](../资源/静态源占用反例与零遗憾紧族的审查和范围--资源.md)已保存真实漏行/适用域，本文不再造同一输入/跑同类阴性。一般目标保持未由本组解决；既有五人half他证成立不被私人旧OPEN否定，恰六人仍需原完整策略量词。

原源没有向本轮承诺后台进程、无限扩样或自动审查完成。有限程序/输出只以实际读到及真实事件为准；本批0原/新数学CLI，旧3响应者诊断只是原MD声明，若原代码后续补取须另核依赖/输入/同SHA旧成功，不伪造复跑。未读的上游子文件仅保源“当时已读”历史记录，不把恢复入口当本次全子树已主处置。
