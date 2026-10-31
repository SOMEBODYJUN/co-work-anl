# 多输出加权状态预算的独立重构与冻结全文攻击

## 来源及独立程度

本次先按精确均匀q输出Claim发给cover_consistency和shared_label_attack，两者各自重构顺序q色闭包、任意两缺一状态的三半逃逸和树锐例。cover随后自行提出有权β加强及真实OPT总和预算；root独立核对后形成正文。shared是在收到有权算法说明后才写规范代码，其有权实现不冒称先陈述盲重构。

原有权独立来源冻结稿SHA256为`d0b849b173dcef28337a1393c747307257bb939bc16e4605cb523ddff8accfa7`。全部数学对象、机制与证明已保存在现行正文，不能从源稿“候选”字样推断主目标状态改变。简化树root直接为a的陈述另交cover独立核，源补审SHA`0681c21601c627810640c8c63e7e2421ae06b4c46af98c6ce524ec206aebf224`；未倒写原先额外接入job的盲稿。

## root代码阅读、独立来源和实际回算

root逐段读规范源端时间闭包、K局部权和全部预载回加，并亲自运行规范、独立和具体例CLI。规范共8118次weighted实际构造、2706局部预算及1263缺一pair最优值检查；18加权星向量81个facet profiles，22树形98个精确missing OPT，所有输入/零值边界通过。T0的free状态按集合判定，不按数值预载是否为0误判。

独立代码把四个最初单独开发的程序中13个函数依赖内联，root另逐AST比对，函数体全部相同，只有main更名和合并入口。它不导入规范实现或scratch文件。保留400随机实例、6722局部K预算、8376实际weighted输出、140非均匀星等号、32975完整分配；简化树64形状×3尺度共192例、140844完整分配。两个有限oracle都对原矩阵实际分配枚举，生产构造不用未知OPT；有限通过不替代一般证明。

具体例包含一个零权星任务、非全体候选K和非均匀β，CLI输出的每job有限资格、最终blocked集合及全机负载经root从原矩阵重算。所有哈希、stdout和实际例结果在新冻结记录，未覆盖三host阶段旧证据。

## 最终冻结全文读后攻击（shared_label_attack）

# 多输出加权状态预算：冻结全文读后审查

审查对象：`research/current/unrelated_machines/weighted_fanout_profile_boundary.md`。
实际读取前后 SHA256 均为 `7bb7e967d492751f0f92fb547608af56e5aaffff387dca559b54d20ef283d78d`。

结论：**standing fatal objection: NONE**。未发现需要修订后才能保留两个精确Claim的数学问题。本记录只审此冻结正文；不宣称外审、新颖性或独立论文价值已认证。

## 独立程度与来源

先前均匀选择器、缺一pair存在三半、q-star和满二叉树锐族均在仅给精确陈述时独立重构，详见scratch `q_host_uniform_claims_statement_first_review.md`。后来收到weighted/source-time算法说明后才实现规范候选，详见 `weighted_fanout_read_after_algorithm_review.md`；不能把有权算法实现称为盲审。本次实际阅读主稿全文，属于最终全文读后攻击。

## 两个ID的对象与量词

UM-WEIGHTED-FANOUT-PROFILE-BOUNDARY-v1 固定同一套基础不可拆jobs、非负有理时间与资格、显式两个实际YES witnesses；状态仅切换独立host的0/T不可迁移预载。原q≥2且q+1个互异host，任意候选K⊆B、|K|≥2、任意显式有理simplex β。输出是一个完整实际σ及chosen，不是估值或分数解。其余输出全free，K外输出按internal处理，正是定义P_{K,i}。未发现状态中偷偷改变基础资格、时间、共同负载或任务的问题。

UM-FANOUT-MISSING-ONE-THREE-HALVES-v1 的ν_i是a和b_i blocked，其余outputs free。K={u,v}时P_{K,u}=missing-v，P_{K,v}=missing-u；顺序互换不影响和式，实际返回的两个状态之一亦一致。pair sum、至多一个严格超三半和全体求和界均准确。没有把“至多一个”升级成“全部≤三半”。

## 有权闭包与所有pins

Section 2固定端点零行，前k−1色顺次闭包后冻结；任何未固定点只进入一次。早类同色权只增；最后未固定类在每个闭包停止时仍未着色，故到每个冻结早类的权严格低于β_i L_u。相减给末类配额。固定末端L=0自动成立。自环只在点入类后提高其同色权，不阻碍归纳；β_i=0可吸走全部剩余点，结论仍成立。不存在未经证明的多色局部最优收敛假设。

原S1中输出host已有预载T，非负任务时间推出其基础行和0，但仍允许零时间任务。Section 3明确用source时间p_{uj}聚合w，式(6)接收项按S2真实接收机u计费，未混淆两端成本。σ逐job只取两个见证中的原有限端。式(6)对自环亦恰计一次，W外没有流入或流出迁移。内部、a、chosen free输出、其余blocked outputs全计费；K外撤预载的outputs作为internal负载同样受控，没有遗漏机器。

## 轮廓和式不存在隐藏oracle

S1直接换目标预载给μ≤2T，a固定预载给μ≥T。合法assignment有限且非空，真实OPT存在并有理，故反证所定义d_i和β_i均有理。若和式失效，D<1且d_i≥0，β_i=d_i+(1−D)/k是非负sum1的合法有理输入，每个β_i>d_i。式(1)构造σ严格优于μ_i形成矛盾。程序不用μ；未知μ仅在存在反证中出现，不能误读为需可计算OPT才能执行算法。

T=0时直接用S1，在所有状态原使用边时间及所有预载均为0，因此确实所有μ=0。Section 4此断言成立；无需从“一个chosen”的构造错误推出“所有chosen”可达。

## 锐例与反例

加权star：任意有理ω≥0,sum1。若一job放blocked输出则负载2T，不低于目标(2−ω_i)T；否则除j_i外全部放a，与a预载给所述下界。ω_i=0和点质量均未破坏论证：分别可达2T和T。K上放star、其他outputs不接任务，给局部facet等号。T>0的锐性陈述明确，T0只是零值等式。

满二叉树：根就是a，无额外接入机器；q叶给2q−1个节点、2(q−1)条边jobs。S1每非叶两件T/2，S2每非根一件T。缺叶入job移回parent，parent原已有根预载T或唯一入job T，得到三半。严格低于三半时根必须全下放，每个已有T入job的非叶继续全下放，最终关闭叶承受2T矛盾；全部missing状态都等于三半。没有把额外根机器误计或忽略跨模块入边负载。

最后不全≤三半的3-output反例独立枚举了每profile全部4种σ：

- missing b1：OPT=5/4，σ=(a,b2)。
- missing b2：OPT=7/4，σ=(b1,a)。
- missing b3：OPT=1，σ=(b1,b2)。

确实符合所有pair sum≤3，并有一个状态严格超三半。

## 总位复杂度及实现对应

矩阵、见证及K/β均显式给定，k≤q≤m；每未固定machine至多吸入一次，最多k−1次闭包，每次只扫显式行/边。有理加法、β_iL_u乘法及比较的位长受原输入及β总位长多项式控制，无按处理时间数值迭代。构造σ线性读jobs，既不搜索未知YES，也不调用OPT。预载可用单可用机器真实job实现，故“实际调度”的定义没有放宽。

规范候选scratch代码 `multi_host_weighted_fanout.py` SHA `a6e95e781e0a8299396045bed550fa604c941897e98360ace89ba864e895714e` 已逐项核验源时间行、原L不归一化、K外free、全机减加恒等与T0状态集合。其8,118 weighted实际构造、2,706精确子集预算、1,263精确missing pair、18个加权star向量81个facet profiles、22树形98 missing OPT、177 pair实际σ及全部边界均通过。有限枚举只在audit内，非构造API依赖。此项有限证据不能替代上述一般证明。

## 状态

两个Claim在此冻结正文中证明闭合，内部攻击无尚存fatal。仍仅限制独立0/T预载、给两实际YES的接口；不提供源问题归约或解码，不证明UM-TARGET-v1存在或不存在。外部审查、新颖性和论文价值未认证。

## root最终裁定

无声明范围内尚成立fatal。证明完成、内部独立攻击、实际实现与有限核验分别记录；外审、全球新颖性、独立论文价值均未认证。两个Claim仅限制给定两真实YES和独立预载的明确接口，不升级成一般UM近二困难性或其否定。
