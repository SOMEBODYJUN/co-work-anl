---
id: customer-attraction/seven-topic-five-player-native-integer-search-recursion-and-two-best-identities
kind: resource
type_tag: 资源
title: 七标签五人原生整数搜索的集合递归与两份best身份
status: complete-three-primary-read;bounded-integer-recursion-analytically-reviewed;restart-packet-exactly-reconstructed;zero-compile-or-run
summary: C++固定7题5人/L60，标准集合值真SPE递推，main权重0…200下整数范围足够；两同schema快照47/35与9/5不能连作同次递增best。前者仅静态覆盖及原minimum字段，后者由全历史常大题策略与逐人1保底精确证明minimum5；未编译或运行。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/credible/exact_integer_search.cpp
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/credible/search_best.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/credible/restart_best.json
---

# 七标签五人原生整数搜索的集合递归与两份best身份

3976B C++、632/299B两个packet共4907B全部实读，原size/SHA256/blob/正常show齐。没有因exact/native名称授运行PASS；没有编译、执行--evaluate、重跑随机搜索或生成新的全集/IC程序。整数边界、递推及小packet的下述解析证明与原执行证据分开。

## 固定模型和精确缩放的实际范围

C++常量T7/M5/L60/K128：7个可区分共同标签A…G、5名单位玩家，非空兴趣类型mask1…127，K是mask数组大小而非搜索截断人数。w[mask]表示不同单位客户重数，允许0、空覆盖标签、同覆盖标签和重复选择；完整有序历史任意弱平局保留。

终局q七维非负整数和5。每个被覆盖类型的分母d=Σ_(a∈mask)q_a在1…5，L60可被这些d整除，所以代码w·(L/d)是实际份额的60倍整数，没有用float比较SPE。未覆盖d0时跳过，未占用主题效用坐标置0；真正孩子a的终局必含a，所以其当前查询不是未占用虚值。

main重启/变异始终使每类型0≤w≤200：纯sharp重启为一个5客户主题加四个单客户，带噪重启最多再加10；另一重启12次各1…15，即单坐标最多180；变异前v+delta在−10…210再clip0…200。因此N=Σw≤25400。对至少32位int、至少64位long long的实现，以下界足够：

| 量 | 足够上界 |
|---|---:|
|单项w·(60/d)|12000|
|一个主题最多涉及64类型的整数效用和|768000|
|福利/OPT/minimum|25400|
|比值比较交叉乘积|25400²=645160000|

所以main上述域内不会因这些乘积/效用累加超32位。源码没有编译环境/二进制/机器位宽记录，不把条件性整数审查称原本次运行认证。

--evaluate则直接从stdin取127个int，**没有**数量、非负、取值界或流成功检查，不继承main的0…200合同；负数不是原单位客户模型，过大数可能溢出。对给定非负完整输入，在32位int、至少64位long long实现中，一个更宽的充分域是60N≤INT_MAX，即N≤35791394，且此N的平方仍在64位内；其它位宽实现需同时核效用累加与比值交叉乘积。缺少或失败的读取会留下初始化0等，不把该入口当通用输入验证器。

## 集合值真BI，不是按计数固定同一selector

init列出深度0…5全部计数态，数C(12,7)=792；终局C(11,6)=462。先完整生成所有态再连接每行动孩子，孩子深度加1；按逆state顺序处理便已取得全部孩子集合。它没有物化Σ_(d=0)^4 7^d=2801个有序决策动作或全部完整策略。

每个非终局用所有孩子终局上的当前行动最低收益l_a，floor=max_a l_a，然后并入所有满足U_a(q)≥floor的孩子终局；mark只删除同一state内重复的终局索引。此正是[完整历史SPE全集递推](../算法/完整历史纯SPE终局全集--算法.md)：

\[
R(k)=\bigcup_a\{q\in R(k+e_a):U_a(q)\ge\max_b\min_{z\in R(k+e_b)}U_b(z)\}.
\]

完整弱等号保留。对非负客户，各孩子集合由归纳非空，floor初始化0不丢负值之外的合法模型。相同计数缓存的是**全部可实现终局集合**，不同有序孩子可分别选最坏子SPE；它不强迫所有同计数历史用同一行动，故不是Markov策略子类。

eval在全部462终局取最大覆盖OPT₅，在根可实现终局集合取最小福利minimum，ti只记其中一个最小终局索引。静态OPT允许重复主题，少于五个不同标签可重复补齐。原代码不输出完整有序策略；集合递推给终局的可实现性机制，不等于已独立验证某份完整σ。

--evaluate输出OPT/minimum/根终局集合大小，继而每个可实现终局计数；不输出动作树。非--evaluate搜索则只保存一份best实例/一个最差终局，不保存根全部终局、SPE数或每状态门槛。不能拿792/462/2801三个不同计数冒实际检查次数。

## 搜索只是有界启发式，非全部权重穷尽

普通位置参数为rounds（默认200000）、seed（默认1）、path（默认best.json），没有JSON输入或项目helper。使用mt19937，不把Python/NumPy种子序列代入。每3000轮或stay>1000重启：有时用sharp不交大题/单例（隔一阶段加噪），每第三阶段12个随机非空类型增1…15。proposal通常改1坐标，1/10分支改2…9坐标；有时偏向已有非零坐标，delta通常±1、1/5时绝对值1…10，最后clip0…200。

正福利比用64位交叉乘积严格比较OPT/minimum，接受改善，等比以1/4接受；否则stay增加。保存只在best严格改善时发生。没有ratio>2或找到反例的提前退出条件，也没有将有限盒子穷尽；200000轮完成仍不覆盖全部0…200的127维盒子，更不覆盖任意人数/目录/客户重数。

零客户可经变异达到。其真正福利/OPT均0，所有终局SPE；代码对比值没有0/0特判，交叉乘积会使该状态与任何状态都被判“等比”，可影响随机walk。它不被保存为正best，却不能拿canonical软件的0/0约定自动修补此原搜索逻辑。这个边界不改变前述非负输入的集合递推正确性，也不等于原两个packet的生成轨迹已知。

每次改进save用ofstream覆写path，按mask升序写全部非零整数类型，没有稀疏浮点打印阈值；完整模型即这些整数记录。文件打开/写成功未另核，stdout打印seed/iteration/近似ratio/类型数，stderr每10000轮进展；packet本身不含seed、rounds、耗时/退出码/编译器或源码hash。--evaluate和普通搜索均无独立证明级验证器。当前未执行任何分支，旧输出不存在的日志不补造。

## search_best：47客户/14类型，minimum35仍为原搜索字段

两个JSON顶层都恰players/topics/customers/search四字段，players5、topics A…G；search恰opt/minimum/iteration/terminal四字段。第一packet完整客户表如下，未列mask即无该类型客户：

| mask | 喜欢标签 | multiplicity |
|---:|---|---:|
|1|A|1|
|2|B|2|
|4|C|3|
|8|D|5|
|12|C,D|1|
|16|E|1|
|17|A,E|1|
|33|A,F|1|
|48|E,F|1|
|54|B,C,E,F|2|
|66|B,G|9|
|93|A,C,D,E,G|7|
|105|A,D,F,G|11|
|121|A,D,E,F,G|2|

总47名不同单位客户，原search为opt47、minimum35、iteration21081、terminal=[0,0,0,2,0,0,3]。终局2D+3G覆盖mask8/12/66/93/105/121，其重数5+1+9+7+11+2=35；五标签A/B/C/D/E覆盖全部47，因此OPT₅47是直接静态证明。

该终局中两个D玩家各得(5+1)/2+(7+11+2)/5=7，三个G玩家各得9/3+(7+11+2)/5=7。但平衡利润或静态计数不自动给完整SPE；本packet没有完整σ或原执行输出，当前没有新认证“minimum35”或该终局可实现性。它保为原有限native搜索断言，不能以代码命名/源码审查/静态覆盖同值当新native PASS。比例47/35不是half反例，甚至即使该原SPE断言成立也远小于2。

## restart_best：九客户的minimum5可独立纸上证明

第二packet五种互不交单例类型：A1、B1、C5、D1、E1，F/G为空覆盖标签。search为opt9、minimum5、iteration0、terminal=[0,0,5,0,0,0,0]。

完整策略取**每个有序历史都选C**。任意历史已有t人，剩r=5−t；若当前遵从，最终C人数n_C+r≤5，收益5/(n_C+r)≥1。改任一小题，未来仍选C，所得至多1/(n_small+1)≤1；空F/G为0。因此每个有序子博弈、全部再次偏离和平局均最优，常C完整纯SPE的福利5。

反向，对任何完整SPE的实际每位玩家，该节点改C不论后继怎样最多五人覆盖C，保证收益至少1。真实最优性给每人u_i≥1，效率和W=Σu≥5。结合常C策略得所有SPE最小福利恰5；五个正主题恰五槽盖全9，OPT₅9。所以本小packet的opt9/minimum5及终局由解析完整证明，而非当前运行C++；9/5=2−1/5只是该实例比值，不证明一般五人最优常数。

两空标签、过去小题重复/空行动和零收益分支均包含在这个常C策略定义中，没有悄悄缩成五主题或只验证在轨。

## 两packet不能连作一次递增best

它们的输出schema、固定人数/标签及整数范围均与本C++相容，但没有各自seed/命令/源码绑定，不能由文件名证明都是当前版本同次生成。若把iteration0的restart_best视为该次已保存9/5，再把iteration21081的search_best当后来best，则与代码严格保存改善矛盾：47·5=235<315=9·35，47/35反而更低。

这只排除所述**同一次递增best序列的对应**，不猜两个packet究竟来自另一seed、旧版本、单独调用或外部复制；也不通过概率直觉排除任何未给RNG轨迹。零状态的搜索比值边界更不能被隐去后用默认初始化反推所有未给过程。保存文件iteration只是改进时点，不证总rounds完成或后来没有更多结果。

## 数学比较、身份与当前运行

此源是全部终局集合的整数BI和有界客户搜索；[固定策略锥](../定理/固定完整策略的客户重数锥--定理.md)的LP只研究一份σ，二者不能互借有限成功。[旧两尾复制障碍](../障碍/两尾公共锚点族的旧组逃生与复制路径障碍--障碍.md)只排另一个具体参数族/拟路径，不因同credible目录就判本两个实例真假。

单组43动作的2/3证明和两组1111动作的半上界/打印点反证也不是本C++的验证器。单组两页面现已真实19XO数学checkpoint d6f42323a2ed6e55ff39534749e3503369e2f84d、pushed head caf4133fddec7e8251bfddfbb7ebdeed6921810b；原捕获与当前字节SHA在本包另绑，故前一two-group包所列single冻结链接依赖已有真实出版闭合，不再称尚未发布。不修改旧冻结包字节，也不据数学checkpoint预报任何来源done。

本3实际16源claim9f40d769…pushed，本3Boss4 owner/sourceSHA/normal-show齐；原raw needs-attention与独立**2 untracked/2 tracked**全同、missing/different/unmerged空、stash保留回执并列，不假改synced。C++独立只标准头，无项目运行helper/JSON输入；两个packet为输出资产。全部来源/完整数据/元字段和逐源收据见[证据](../../tools/evidence/native-anchor-integer-discovery-three-primary/README.md)。当前0编译/原main/--evaluate/RNG/全集或IC/旧成功重跑，只JSON/YAML/字节hash/字段/链接自查，C++不冒AST或编译检查。无外审、新颖性、全局最优或half结论，第三阶段不建图。
