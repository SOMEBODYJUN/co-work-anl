---
id: customer-attraction/payoff-comparison-workspace-menu-quotient-and-Markov-boundaries
kind: resource
type_tag: 资源
title: 收益比较图工作区的菜单商与Markov边界
status: primary-entry-and-five-necessary-related-originals-fully-read
truth_status: exact-menu-cone-quotient-and-anonymous-counterexample-with-historical-CAG-search-status-corrected
review_level: full-original-mathematics-code-data-and-current-repository-comparison
scope: 固定完整策略的菜单商；四人二题正客户例；三人三动作匿名表；旧CAG20k有限探索另列，计数净化现已被真CAG反驳
summary: 自足保任意深度菜单锥商、完整正质量例、匿名缺失终局手工见证和计数统一排除；程序实际枚举终局映射，cap/跳过未记；SCC空间与图商不等于Markov归约或一般half付款。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/README.md
related_source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/cone_abstraction/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/cone_abstraction/menu_quotient_audit.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/abstract_markov.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/abstract_markov_counterexample.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/markov_outcomes.py
---

# 收益比较图工作区的菜单商与Markov边界

3101B主入口全文及所需7201B菜单稿、4705B菜单审计、1440B匿名探针、1558B完整匿名表、2275B计数映射程序均正常取得并完整实读。原件见[证据](../../tools/evidence/payoff-comparison-graph-and-source-contracts-primary/README.md)，五related合17179B，不额外primary done。其数学不是一张旧图或研究路线：SCC证明与64原记录已分别落[定理](../定理/真实收益比较图的强连通商与非负流编译--定理.md)、[程序](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/52b0b7d604fe86df827b.md>)，本页保入口另有的菜单/净化及状态义务。本批0原运行、新数学checker、旧SPE/LP搜索。

## 同菜单的任意深度真实行商

固定m≥1、p≥1及全部有序历史形式策略σ。节点h和当前行动a给q(h,a)：强制a后沿**同一σ**完成的终局计数。定义带行动索引的完整终局菜单M_h=(q(h,a):a∈[p])。不同节点可深度不同/当前玩家不同；相同菜单只要求这些真实终局逐行动相同，不是当前前缀计数相同。

[注入引理](../定理/真实收益比较图的强连通商与非负流编译--定理.md)保证固定a的全类型F(a,q)唯一识别q；故M_h=M_g当且仅当全部行动的全类型收益菜单向量相同。令类C的收益菜单U_C(a)=F(a,q_C(a))，实际指定行动集合A_C={σ(h):h∈C}，取b_C∈A_C及某代表节点g_C满足σ(g_C)=b_C。

同菜单两个节点分别选a/b时，原真实行有相反方向

$$\Gamma_{h,b}=U_C(a)-U_C(b)=-\Gamma_{g,a}.$$

因此H_C=span{U_C(a)−U_C(b_C):a∈A_C}的任意符号方向可由原真实行非负支付，H_menu=Σ_CH_C。对任意h∈C、偏离t，

$$\Gamma_{h,t}=[U_C(\sigma(h))-U_C(b_C)]+[U_C(b_C)-U_C(t)].$$

第一项在H_C；t∈A_C时第二项亦在H_C，其余t是原代表g_C的真实行。反向代表行本来存在、±H可编译，故精确

$$\boxed{\operatorname{cone}\{\Gamma\}=H_{menu}
+\operatorname{cone}\{\Gamma_{g_C,t}:t\notin A_C\}.}\tag{1}$$

对客户w≥0，原σ为SPE当且仅当H_menu·w=0及全部保留代表行·w≥0。任意目标d的原行+非负型余项证书也等价于d=h+ΣμΓ_rep+s，h∈H_menu、μ,s≥0。没有保证一般d=2c−o可行，也未修改σ。同菜单双向差是收益图中两向真实边，所以H_menu⊆H_SCC；全部“同计数末节点却指定不同动作”的末端平局空间又包含于H_menu。均不称最大lineality。

## 四人二题严格扩大末端平局空间

四玩家、共同A/B。完整策略：根A，A/B后第二人均A；第三人在AA/AB/BA/BB后分别B/A/B/A；末位此前A至少两次则B，否则A。全部1+2+4+8=15有序节点都有规定动作。按(A数,B数)简记终局为40、31、22、13、04，真实菜单分类可直接手工展开：

| (强制A终局,强制B终局) | 节点 | 该类指定行动 |
|---|---|---|
| (40,31) | AAA | B |
| (31,22) | AA,AAB,ABA,BAA | B |
| (22,22) | ∅,A,B,AB,BA | A，唯BA处为B |
| (22,13) | BB,ABB,BAB,BBA | A |
| (13,04) | BBB | A |

五类中三类跨深度；这张表是当前从完整策略的解析展开，不冒原stdout记录。末位同计数规定动作从不不同，所以上述特指末端平局空间H_terminal=0，**不是**说末位全部行的线性span为零。

AB与BA同菜单(22,22)却分别选A/B，原行是±(1/2,−1/2,0)，类型顺序A,B,AB；故H_menu恰一维，严格大于H_terminal。全部其余非零行形如(−1/3,1/2,0)、(1/2,−1/3,0)、(−1/4,1,0)、(1,−1/4,0)。因此原完整策略客户锥恰w_A=w_B≥0、w_AB≥0：两个相反早期行给必要性，其余行在该面非负给充分性。取(1,1,1)是三个不同单位客户，A/B覆盖不同且全部三类型正；actual AABB、W=OPT4=3，完整SPE，不是half反例。

4705B原脚本只用标准库defaultdict/Fraction/product/json，从该完整策略重建terminal、菜单及全部30含自身行；每对15×15节点比较“整数菜单相等”与“全行动F向量相等”，逐类核相反行/全部30行分解。它对(1,1,1)核所有行非负、两条早期向量、每行common坐标0和私有坐标和≥0，并检查每末计数类只有一规定动作，输出全文30个比较值及锥/维数/菜单分类字段。它不求通用SCC、LP、全部策略锥或一般half。原入口记“已核15/30/5/3”，这里保历史声明；没有另取得该脚本的独立冻结JSON/进程事件，也不运行来补造。main guard内仅pretty sort_keys stdout加LF，无外部输入、CLI参数或输出文件。

主入口与SCC原稿称已由cone_abstraction内部攻击确认。实际取得的README/程序完整承担上面的**菜单商及四人例**，未另附逐命题SCC攻击回执；本页保原自述与已获证据范围，不升级成外审/盲审或当前新过程成功。

## 泛匿名终局表的完整缺失终局例

1440B探针固定p=m=3、seed643，从每个终局计数q给每个已占行动独立抽0/1/2收益（未占行动给0），这是更宽匿名玩家表。1558B原输出iteration11、10个终局收益完整为：

| q | u_A,u_B,u_C | q | u_A,u_B,u_C |
|---|---|---|---|
| 003 | 0,0,2 | 111 | 0,2,1 |
| 012 | 0,1,0 | 120 | 2,0,0 |
| 021 | 0,0,1 | 201 | 0,0,0 |
| 030 | 0,1,0 | 210 | 0,1,0 |
| 102 | 0,0,2 | 300 | 0,0,0 |

原完整根终局集合记{012,111,003}，计数统一集合{111,003}，missing={012}。迭代11为零起始候选编号，不记成功完成枚举数。下面给012的自足**当前解析见证与排除**，不冒原数据曾输出策略或本轮运行。

全历史策略根B；第二人在A/B/C后选B/C/B；末位回复表如下：

| 首/次 | A | B | C |
|---|---|---|---|
| A | B | C | B |
| B | C | A | C |
| C | B | A | C |

从十表逐格：末位最佳菜单AA={B}、AB/BA={C}、AC/CA={B,C}、BB={A}、BC/CB={A,B,C}、CC={C}，表内均合法。第二人A后各候选收益(0,2,1)，B后(0,0,0)，C后(0,2,2)，规定均最佳。根A/B/C真实收益(0,1,1)，故根B可选，actual BCC即012；全部有序历史/平局完整，非计数处BC选C而CB选A。

任何计数统一SPE要实现012，仅可能有序路径BCC、CBC、CCB。CC后末位C收益2严格大于B1，故CCB不可能。C后若B且CB末C成012，第二B仅1，小于改C后CCC收益2，所以CBC不可能。剩下BCC要求BC末C；计数统一迫CB也末C。于是C后第二人比较A0、B1、C2，必C，根改C真实得2，严格大于BCC根B1，亦不可能。这个排除针对所有计数统一实现，不只是展示原一棵策略非Markov。

该表不能来自任何非负单位客户CAG：003的每个C玩家收益2强迫|C|=6；而012时C已被两人选，每个C客户总负载≤3，故该C玩家至少|C|/3=2，表却给0。非负实客户同样矛盾。它只否定不利用CAG结构的泛匿名净化，不是原客户反例、非half数据。

## 2275B计数终局映射枚举与原CAG探索

markov_outcomes(inst,cap=200000)预计算全部终局行动收益。由深到浅，对每个深层终局映射deep、当前每个计数状态q，得到各动作的真实终局ends和当前收益，保所有并列最佳的**不同终局**集合，再对同深度全部状态取笛卡尔积，和deep合为一个全续局终局映射。

这与模块注释“every state policy”需精确区分：动作不同但产生同一最佳终局时被set合并，因此枚举的是**终局映射**，并非逐个动作policy。根可实现计数集合仍完备：给定深层映射，每个被保终局至少有一个最佳动作实现，可逐状态选证人形成统一计数策略；反向每个计数策略的所有续局终局映射按归纳落入这些候选。共同深层map强制所有父状态共享同一孩子状态的终局，正是计数统一约束，不能把父分支各自的孩子集合独立拼接。

每深度next_maps数超过cap就抛OverflowError；返回len(maps)以及各根终局，不返回所有动作表。cap/日志max_policies实为该终局映射数，不是全部动作策略数，也不是只限制根终局个数。中止后无完备结论。

模块顶层按原相对布局parents[5]加ROOT，再import已发表canonical的Instance、CustomerType、ExactSPESolver、verify_certificate（后者未调用）；即使abstract探针只要vectors/increment，也会经过这一导入。可移置源文件不能盲import，必须保持包路由。规范包四件此前已全文读、同SHA复用于本闭包；其缓存计数递归保**所有**完整历史SPE终局集合，不等于要求原策略计数统一。

主guard接受两个位置参数p/n（默认3/3），seed14037，每次为全部2^p−1非空类型抽重数0,…,3，零项省去，造Instance。每输入调用ExactSPESolver.outcomes与完整计数映射枚举比较；OverflowError直接continue且不计跳过数。计划20000候选，未给每项原数据/完成数；全零、空主题或同覆盖别名可出现，不宣称全部是严格互异集合目录样本。发现差异会覆盖同目录markov_counterexample.json（indent2、无额外末LF）并stdout带COUNTEREXAMPLE前缀；否则每1000的progress、最后No mismatch均纯文本，不是结构化审计事件。No mismatch仍可含未知数量cap跳过。

主入口称(3题3人),(3题4人),(4题3人)各20000次未见差异，仅保存其**原历史源述范围**；本批没有这些运行trace/每项输入，也不重跑。abstract脚本则固定10000尝试、直接Table匿名数据，用自身集合值逆推full_outcomes（每个有序孩子可独立拼接的阈值递推），再调用上述Markov枚举、cap跳过；发现本原差异后固定相邻写abstract_markov_counterexample.json（pretty、无末LF），stdout紧凑JSON加LF。两程序有guard，但import时已有路径/包导入副作用；不能当纯标准库独立CAG验证器。

## 当前状态与旧入口的精确校正

原CAG净化问题现在已有[三人五题24831客户严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)：31类型全正、五覆盖互异；完整终局7个、计数统一6个，目标023只能完整历史实现，完整最差22428<计数最差22429，OPT22431仍half。已发表证据穷尽648末层映射及130776第二层选择。本批全文比较其完整31类型/31动作/末位菜单/排除量词，0重跑。故旧20k阴性不维持普遍净化开放，也不能用泛匿名不合法例代替这个合法CAG证据。

[终局见证DAG](../等价/终局见证DAG的完整历史可实现性--等价.md)状态保(k,目标c)、允许同k不同c选择不同动作，精确表示完整历史根终局存在性；与计数统一净化失败相容。本SCC/menu表示则固定原σ不变，三个压缩合同不能互换。

入口其余探索均按时态保存：probe_bridges/probe_existing_cones被述在若干3人6题、4人6题指定锥及前8锥未见正值，六人8题大批主动停止；这些原代码/完整点未在本scope取得，不冒精确上界或新核验。原“残余≤W已被global_proof两人例否定”是其旁引，未把负数日志当新完整证书。原“逐人OPT≤2m u_i未证未驳”已由[银行完整反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)校正：m5给25/26倍门槛失败；不是等到本目录浮点搜索才判状态。

入口另称内部独立强iid桥W≥Z审查，不能混成half/真正静态安全值。现[强弱iid支付反例](../反例/独立同分布福利支付--反例.md)已分清Z是静态对称混合Nash的iid覆盖：八客户三人W6<Z₃；弱系数(1−1/(2m))桥也另被花瓣族否定，真正v_m与half在这些例中仍通过。这里不因入口“保持原状态”把弱iid普遍桥继续列开放，也未额外primary done其旁引代码。旧私有工作区/公屏操作说明只保来源身份，不执行原研究安排；外审、新颖性和一般half付款仍不由本资产获得。
