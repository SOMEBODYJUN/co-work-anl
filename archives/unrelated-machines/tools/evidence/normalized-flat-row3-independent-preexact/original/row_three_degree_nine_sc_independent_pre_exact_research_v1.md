# Row≤3、item support≤9 的 SC 子问题：新Exact读取前的独立checkpoint

审查者：general_query_response_review。2026-10-18。

## 时间顺序、已知前提与未读取界限

任务：显式非负有理additive SC，每agent整行总值≤3，每item正值agents≤9，promise真实OPT≥1；是否有det-bit-poly算法输出固定常数c>0的所有agents效用？另检验能否只靠CONFIG LP(1)可行来round常数。

本checkpoint冻结时，尚未读取root刚提供的normalized_menu_full_support_lp_preservation_exact_v1.md，也未读rainbow策略或其它agent推导。先前会话中已独立审过normalized flat binary selector-tree及port-path正规形（先行独立记录SHA 642049e4d872554efad0d8ebb5398713a922ca0524a80f1a33070407e8e9fa3d）；这是既有知识，不伪装本轮第一次发现其integral V保持。

本轮独立新增推导为下述fractional full-state正向lift及state-dummy桥。此checkpoint只认证所写正向，不提前声称tree/path LP反向、state-dummy CONFIG反向或CONFIG最高值≤1的完整新合同；这些尚待新Exact后的单独审查。

没有算法或已知定理在本轮被核到能解决真正OPT≥1的promise问题。不能将“未找到匹配结果”写成文献不存在性或复杂性否定。

## 1. 当前已独立闭合的transfer命题

设一个普通general SC实例有CONFIG LP(1)可行的有限有理support见证。可对这份显式support在det-bit-poly内构造另一个普通SC实例J，满足：
- 每agent row total≤3；
- 每item正支撑≤9；
- CONFIG_J(1)可行，且可从给定support构造该解；
- 真实OPT(J)≤真实OPT(原SC)。

构造无需原SC最优allocation，但输入须有显式配置support；不能把它误用成对general SC promise实例保unit完整性的算法归约。

### 1.1 从配置support到normalized full-state菜单

写原agent i的正配置概率lambda_(i,S)，每S的原值W_(i,S)=sum_(u∈S)v_(i,u)≥1。可将各agent概率归一到和1，资源usage仍≤1。为该配置建一个indexed menu state，其资源身份仍为原u，权

p_(i,S,u)=v_(i,u)/W_(i,S)。

该state质量严格1，且p≤v。Lambda给每group选一个full state的fractional witness：每group概率和1，每资源sum_(i,S:u∈S)lambda≤1。

若这个菜单能给每group某state的disjoint partial子集质量c，则原SC按同一原item分配的效用≥c，所以菜单integral V≤原SC OPT。这里不把未在lambda support中的unit配置补入菜单。

### 1.2 Fractional full-state LP定义

对任意normalized explicit menu，FSLP变量lambda_(g,s)≥0，sum_s lambda_(g,s)=1，每资源u容量

sum_(g,s:u∈S_(g,s))lambda_(g,s)≤1。

这是每个indexed state领取其全support的fractional模式；系数为membership0/1，不是把资源按private权收容量。权只要求各state总质量1。

### 1.3 Tree步骤的正向FSLP lift

对每原group随机选一leaf s，概率lambda_s；按既有tree正规形给每vertex选full state：root到leaf路径各internal选下个child-own singleton，末leaf选原state，所有off-path vertices选own singleton。

每次选择中每个fresh own resource恰用一次。取边缘概率后所有新groups状态概率和1，所有fresh own资源usage恰1；旧资源的总usage恰为原lambda usage。概率可用子树lambda前缀和精确算出，多项式。

K1直接原state，无own、无新增group，亦保FSLP正向可行。

### 1.4 Port-path步骤的正向FSLP lift

对某资源u的d个incident groups，令a_j为第j组所有包含u states的lambda概率和，sum_j a_j≤1。把旧group统一改用自身port z_j，旧usage为a_j。

选一个hole分布h_j≥a_j、sum h_j=1：例如将全部剩余1−sum a放h_1，其余h_j=a_j。若hole为h，helper r在r<h时选left z_r，在r≥h时选right z_(r+1)。取这一匹配的边缘概率，则每helper状态概率和1；各port helperusage恰1−h_j，连旧usage a_j总≤1。

d1无helper，d0无usage/可保unused原资源。全部概率由有理前缀和算出。树先于path，最终K≤3、资源跨group≤3；所用integral positive V精确保持是既有正规形合同。

## 2. State-dummy普通SC桥：forward CONFIG及integral值

对最终每个flat group g的K_g≤3个states，建K_g名state-agents a_(g,s)。每个原资源u是普通item，给a_(g,s)原state权p_(g,s,u)。另建K_g−1个private-to-group dummy items，每个对g的全部K_g名state-agents价值1、对其它agents0。

行总值为1+(K_g−1)=K_g≤3。原item跨≤3groups，每组≤3state-agents，正支撑≤9；dummy item支撑K_g≤3。因此全部目标值非负有理、确为请求的row/support域。

给FSLP lambda时，对state-agent(g,s)，以lambda_(g,s)取完整原state support（效用1），以剩余概率取某一dummy singleton。K_g>1时对每个dummy item给该agent概率(1−lambda_(g,s))/(K_g−1)。每agent配置概率和1，每dummy使用和为1，旧item usage仍为FSLP容量，因此得到真实SC CONFIG(1)解。K1时lambda=1，直接其原full-state配置。

Integral方向：每g只有K_g−1枚dummy，故任一目标allocation中至少一名state-agent未拿dummy，其全部效用来自原state资源。每g抽这样一名agent及其真实原bundle，得到flat one-state disjoint partial allocation，质量不低于目标min。反向给flat分配，选中state-agent拿原bundle，其余K_g−1 agents各给一个dummy。由于flat V≤1，目标min不降。故这个桥精确保integral V。

结合已有tree/path integral保持与§1.1，目标真实OPT≤原SC OPT，同时FSLP正向lift和本节CONFIG lift保LP(1)可行。

## 3. Support大小与位复杂度；不能偷用最优分配

CONFIG LP有每agent概率=1、每item容量≤1的0/1矩阵。可行时存在basic feasible解，正配置变量数量≤agents+items；加资源slack后，基矩阵维度同阶，0/1 determinant的Hadamard界给多项式bit有理概率。因此即使全配置族指数大，也有多项式大小support见证存在。

给出该support后，state内W及p=v/W有理位长多项式，support资源总项≤items·support数；tree/path及state-dummy对象数均多项式，概率计算只加减除显式整数，不按分母展开。目标可按dense总规模输出。

但“support存在”不表示它含真实最优unit allocation所用配置。即使原SC OPT≥1，任意LP basic support生成的菜单可能只有tiny integral V。不能用此transfer把真正OPT≥1 promise保到目标，不能据此把目标promise算法当作general SC常数算法；更不能使用未知最优allocation来选择support。

## 4. CONFIG障碍的已证部分与外部PaperFact界限

上面的transfer已独立证明。因此，若导入一般SC CONFIG LP存在任意大integrality gap的已发表事实，则这一row≤3/support≤9子类同样存在CONFIG(1)可行但真实OPT任意小的实例。这将直接排除“CONFIG LP1可行本身足以round固定c>0”的合同，甚至不论运行时间。

本checkpoint对该外部事实实际核到的primary范围仅为：
- Bansal–Sviridenko, The Santa Claus Problem, STOC2006，作者IBM页面的摘要明确报告general arbitrary valuations的Omega(sqrt(m))配置LP gap。
- 作者页：https://research.ibm.com/publications/the-santa-claus-problem
- 原论文DOI：https://doi.org/10.1145/1132516.1132522
- 本轮直接请求ACM全文PDF返回403；没有亲读BS原gap构造或完整proof，不能写成该原proof已核，亦未在本checkpoint给一个全自足显式gap族。

因此“transfer命题”是本轮独立数学证明；“由BS得到无界受限gap”仍明确依赖上面仅核摘要的PaperFact。下一份真正statement-only新Exact若给自足family，应另审后再独立闭合，不回写本历史。

这个CONFIG障碍不反驳真正OPT≥1的promise算法：gap实例不满足该promise。它也不构成任何P≠NP结论、无算法证明或near2主目标反面。

## 5. 其它实际primary读取及未适用结论

本轮读了已存BCG2009 PDF §2.2 Theorem2.4/Fig2（印8–9）的degree-three路径归约。原agents的全部原边值逐item-copy保留，故原row total并未被常数化；dummy玩家的infinite-valued两端也须区别对待。这不能直接解决row≤3的当前问题。该PDF：
/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/history/source/literature/unrelated_machines/bateni_charikar_guruswami_2009_maxmin.pdf
SHA 7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f。

另以pdftotext实际读Bamas的Lift-and-Project Integrality Gaps for Santa Claus v2引言及Appendix A有关restricted assignment部分；它没有在所读位置给出当前异权row/support promise的常数算法。其normalized/canonical restricted-assignment定义不等于当前普通异权SC，不能借用其constant restricted算法。PDF：
/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf
SHA e1120098a847eb10689c529579af5d44b93ee5f6e655eae7621a2333bf76e8de。

网页搜索读到的restricted SC常数结果同样要求item-independent positive values，不适用于任意v_ij。经典additive slot误差maxv也没有解决big/tiny共同选择，本checkpoint未提出错误的完整算法。没有做小样本枚举或软件优化实验。

**本checkpoint最终状态：独立证明FSLP正向transfer及row3/degree9 state-dummy桥；受限CONFIG无界gap的应用暂带仅核primary摘要的外部前提。真正OPT≥1的det常数算法问题仍未由本工作解决。此文件冻结后才允许首次读取新LP-preservation Exact。**
