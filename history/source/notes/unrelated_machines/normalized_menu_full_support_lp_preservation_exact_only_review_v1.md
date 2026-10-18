# Normalized 菜单 full-positive-support LP 保持：statement-first 独立审查

审查者：general_query_response_review。2026-10-18。

## 1. 顺序、pre-Exact知识及正式判断

先按root要求冻结新Exact读取前的独立checkpoint：
row_three_degree_nine_sc_independent_pre_exact_research_v1.md，
SHA b33a165fd22dd77b3ce8c93317a9754c52a60675a2d6366edbd9e99f0668d0f6。

随后才首次全文读：
/workspace/scratch/038d9dcc4cac/normalized_menu_full_support_lp_preservation_exact_v1.md

Exact SHA-256：9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763。

未读作者Proof、rainbow策略或其它agent推导。此前已审过tree/path的integral positive V/完整UM保持；pre-checkpoint只新证fractional正向及SC桥forward，反向和CONFIG最高≤1并未在旧checkpoint冒称已证。本轮仅据新陈述独立补证全部新量词。

另有定义差别必须保留：pre-checkpoint用全部state membership的较强LP（即使有零项也计），而本Exact明确FSLP只计positive support。下文按新positive定义重新核zero；不将旧record回改成已经使用新定义。

**明确结论：新Exact全域有效，无fatal。FSLP↔T↔D/N及↔SC CONFIG(1)均成立，可对给定显式有理证书det-bit-poly转换；CONFIG最高≤1、自足D族的row3/degree9无界gap均独立闭合。无需BS原gap构造或外部未读证明。**

只scratch新增；未改repo/Work/Git及任何旧记录。没有小样本枚举或软件优化认证。

## 2. Tree双向FSLP转换

记原group g的leaf s概率lambda_s，正full-support资源容量按0/1计。

### 正向

按lambda_s选择leaf s，沿root到s路径：internal顶点选child-own singleton，终leaf选原完整state，其余顶点选own singleton。每个fresh own资源每次恰用一次，旧positive资源边缘usage恰为原lambda usage。因此各新group的state概率和1、全部positive资源usage≤1。

可直接用子树lambda和计算这些边缘概率，无需枚举跨groups的联合选择。K1的root-leaf只有原state，保持不动。原0项完整保留在实际对象中，但不进入当前LP容量。

### 反向：允许off-path有额外fractional激活

给任意T对象FSLP。对非root顶点v，记q_v为parent选择child-v singleton的概率，o_v为v选择own singleton的概率。Fresh a_v只在这两种positive singleton中出现，故

q_v+o_v≤1。

v选择非own branches的总概率B_v=1−o_v≥q_v。若v为internal，B_v为两个child状态概率和；若v为leaf，B_v就是其原state概率w_s。Root internal向children送概率总量1。逐层用上述不减关系，或对每个subtree归纳，得原g全部leaf原state概率总和

W_g=sum_s w_s≥1。

K1时W_g=w_s=1。令源lambda_s=w_s/W_g。每原group和1，且lambda_s≤w_s。所有原positive资源在T中只由对应leaf原states使用，所以源usage≤T证书的原资源usage≤1。重复indexed states只作为不同leaf分别计算，无合并身份。

这是任意目标证书的真正逆向，不假定只有一条活路径，不把额外leaf原state质量同时当成源多状态。除以W_g≥1合法，位长按证书部分和控制。

## 3. Port-path双向FSLP，含zero和d0/d1

对资源u，按全部菜单membership（含0项）列d个incident groups。设a_j为第j组所有p_(g,s,u)>0 states的证书概率和，注意不把零权state计入a_j。

### 正向

源FSLP给sum_j a_j≤1。d≥1时选hole分布h_j≥a_j、sum h_j=1，例如h_1=a_1+(1−sum a)、其余h_j=a_j。

以hole h的概率h_h令helper r在r<h时选left z_r，在r≥h时选right z_(r+1)。每helper概率和1，各port的helperusage恰1−h_j。加原group positive usage a_j，总≤1。旧group的state概率不变。

当某group只以0项列入u时，其a_j可为0，仍可参与完整path/helper结构；LP不虚占原zero项。即使u全部membership都为0，上述sum a=0也给合法helper匹配。d1无helper；d0为真正无membership的unused资源，保持0容量usage。

### 反向

给任意D对象FSLP，保所有旧groups的state概率，删helpers并将ports合回原u。d个port约束求和时，d−1个helpers各自state概率和1、每个singleton恰用一个port，所以helper总positive usage精确d−1。于是

sum_j a_j+(d−1)≤d，

得原u的sum a_j≤1。d1直接其port约束，d0源usage0。每个u独立聚合，所有源正support容量均满足。

因此D本身双向保持，且D∘T同样双向。实际normalform需先T后D以保最终degree3；本LP论证不把positive membership与物理所有incidences混淆。

## 4. State-dummy桥与SC CONFIG(1)双向

固定group g有K个normalized states，real positive support P_s非空且总值1。目标有K名state-agents、K−1枚本组dummy，每dummy对本组全部agents价值1。

### FSLP→CONFIG(1)

对agent s，以lambda_s使用配置P_s，价值恰1；K>1时，对每枚dummy使用singleton配置的概率(1−lambda_s)/(K−1)。每agent概率和1，每dummy总usage

sum_s(1−lambda_s)/(K−1)=1，

原real item usage就是FSLP容量。K1只有lambda=1，直接P_s，无除以0。支持数及配置列表总长度显式多项式。

### 任意CONFIG(1)→FSLP

先删每配置中对其agent价值0的items，不改价值且只减容量。每个agent s的全部real items总值严格1：

- 若配置没有本组dummy，要达到≥1必须含完整P_s；遗漏任何positive项都会低于1。
- 若配置有dummy，可确定性保留其中一枚dummy，删其它全部items，仍为合法价值1配置、边缘usage不增。

令w_s为前一种（全real support）配置总概率。剩余1−w_s都使用一枚dummy。固定g仅有K−1枚dummy容量1，因此

sum_s(1−w_s)≤K−1，故W_g=sum_s w_s≥1。

同时全部real资源的full-support概率w满足容量≤1。令lambda_s=w_s/W_g，和1且lambda_s≤w_s，于是为源FSLP。K1时无dummy，w_s=1。

该逆向处理任意给定有限配置证书，不要求证书原本已canonical，也不漏掉一个配置里多枚dummy或dummy加real的情况。概率归一只降低real usage。没有以实际allocation替代fractional证书。

### CONFIG最高阈值≤1

任取threshold tau>1。每个state-agent仅real items的全部总值1，所以任何tau配置必须含至少一枚本组dummy。一个g的K名agents各配置概率和1，dummy总边缘usage因此至少K；但只有K−1枚dummy各容量1，矛盾。K1时无dummy已无tau配置。G非空保证至少一个这样的group，故SC CONFIG最高≤1；FSLP可行时已构造CONFIG(1)，其最高值精确1。

这不声称一般SC CONFIG等于FSLP；只对本明示state-dummy像成立。

## 5. 实际值、row3/degree9及全部zero原jobs

State-dummy integral桥也可直接核：每g的K−1枚dummy最多照顾K−1名state-agents，因此任一SC allocation中至少一名agent没有dummy，其效用全来自自身原state资源。各g抽一名给flat one-state partial分配，质量不低于SC最小值。反向给flat分配，选中state-agent取该bundle、其它K−1各给一dummy；因V≤1，min不降。故实际SCOPT=V，含0端点。

树/path的integral V与完整UM OPT保持按既有normalform合同；zero原incidence jobs仍在实际UM矩阵、可留private0，不占本positive LP或SC utility。当前没有把zero原jobs删除成不同实际实例，也没声称保存一般UM CONFIG。

N(Q)每group K≤3，所以state-agent row positive总值=1+(K−1)=K≤3。每real item跨全部菜单至多3groups，每group至多3states，positive agent度≤9；dummy度K≤3，正值均≤1。Unused资源正度0，重复states不改变上界。两种容量类型被明确区分：FSLP项系数为positive-support0/1；SC行效用才用p。

## 6. 自足D族：无需任何BS原gap proof

D≥2。原Q_D有main group D个states，各含一整行D枚g_(a,j)权1/D；另D²个helpers各有g_(a,j)或A_a两个unit singleton states。

### 实际V=1/D

任何正质量allocation选定main行a。Main每领取一个g_(a,j)，对应helper(a,j)不能再领它，要正质量只能领同一个A_a。因A_a全局只能给一helper，main最多领取一枚g，质量≤1/D。若min质量0也已≤1/D。

达界：main取任意一枚g_(a,j0)；其对应helper取A_a；其余全部helpers各取自己的g_(b,j)。资源不交，helpers质量1，main质量1/D。因此V(Q_D)=1/D。

### 显式FSLP

Main各state概率1/D；每helper(a,j)以1−1/D选g_(a,j)，以1/D选A_a。每g资源usage=1/D+(1−1/D)=1；每A_a usage=D·(1/D)=1，各group和1。因此FSLP可行，是完全自足有理证书。

### 目标间隙

应用已证T/D的双向FSLP及既有integral V保持，再应用本记录§4/§5的SC桥，I_D=SC(N(Q_D))满足：
CONFIG最高=1，实际SCOPT=1/D，row total≤3、每item positive-degree≤9，正值只有1或1/D。

原Q_D的groups D²+1、states 2D²+D、incidences 3D²、资源D²+D；tree/path/SC对象和positive条目均poly(D)，dense也poly(D)，权和显式证书位长poly(D,logD)。不称poly(logD)输出这些对象。没有枚举toy D数值来代替一般证明。

所以本强类型上的CONFIG gap无界；CONFIG(1)可行不能推出任意固定c>0的实际minutility，甚至不涉及效率。这一新审查使用自足D族，完全不需要未亲读的BS原proof或其摘要PaperFact。Pre-checkpoint的外部依赖限制保持其历史，不回改。

## 7. 证书复杂度、范围与真正promise问题

T forward用子树和，reverse用leaf和归一；D forward用hole prefix，reverse聚合port约束；SC forward列support/dummy singleton，reverse逐显式配置strip/canonicalize及组内归一。只作有理部分和/乘除显式非零量，位长按原输入及给定证书长度多项式，不按1/p、1/V或分母数值展开。

原n groups、S states、I incidences的T计数2S−n groups、5S−4n states、I+4S−4n incidences均对K1正确；D helpers≤中间incidences，SC agents/state数、items/resources加dummy、dense估值矩阵均poly。一般SC CONFIG反向只承诺给显式有限证书时转换，不枚举指数配置。

FSLP是显式多项式LP，可用标准有理LP求可行点；它不求实际V、真实SCunit allocation或未知最优owner。没有给定最优分配当输入。

I_D的真实OPT=1/D，违反“实际OPT≥1”的promise，故这个gap不否定那一promise常数算法；也没有NP-hardness、新near2源或一般UM算法。已存tree/path/state-dummy与标准selector/parking模式的原创性不认证。BCG单纯degree路径保原agent全部行值，不能直接提供row3归约；这里的strong type来自显式normalized menus加上述桥。

**最终statement-first判断：FSLP双向保持、新SC分数桥/LP最高1、自足D族row3 degree9无界CONFIG gap全部通过，无fatal；真正OPT≥1 promise算法仍未由这些结论决定。未读作者Proof。**
