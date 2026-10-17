# 私有注入树的全配置阈值五三界与严格承诺判定

读取目的：确定均匀小端私有树何时必有实际低负载调度，从而核对任意菜单、任意端口重编号的近二困难性编译是否可能。本文是限定结构类的配置整数间隙上界及判定结论，不是一般UM算法，也不是一般UM不存在统一改进的证明。

现行身份仅 `UM-Q-PRIVATE-INJECTIVE-TREE-CONFIGURATION-FLOOR-v2`。v1先给共同full-state分数点的hitting/Haxell界，v2另加全CONFIG(T)与非注入菜单过滤判定；旧Exact/证明/独立重构原字节保留为来源，不另复制成一套现行资产。证明完成、陈述先行独立重构及全文读后攻击已发生；无standing fatal。外审、新颖性、独立成文价值及任意变参下输出σ的多项式算法均未认证。

## 精确合同

### 精确模型与域

任意整数d,h≥1，非空有限root集合U，每u非空有限菜单S_u；外部机器有限集合Z。每(u,s)是满d叉高h的完全私有树，不同状态内部机器互异，深0..h−1是内部机器，叶地址[d]^h。每u一枚selector，时间1、全部可用端是其状态树根。每内部edge job仅有父端1/d、子端1；每leaf job仅有父端1/d及由显式f_us:[d]^h→Z指定的唯一单位外端。其它端∞，无其它任务或预载。所有状态、树、叶资格均显式列出，不把巨大binaryd/h展开的成本藏掉。

CONFIG(T)为完整原P的通常配置LP：每machine配置是负载≤T的其合法jobs子集，非负配置权重，每machine权重和1、每原job覆盖恰1；向下封闭下与至少覆盖版等价。非空selector给OPT,Tconf≥1。空U单独返回OPT0/空σ，不套此下界。

### A. 注入模型的严格配置等价

本项要求每个f_us单射。存在一个共同λ_us≥0满足Σ_sλ_us=1且Σ_us λ_us |f_us^−1(z)|≤1（每z），当且仅当CONFIG(1)可行。λ、所有资源行必须共同；不是逐机另选边际。λ系统规模及位长按显式P为多项式。

### B. 全部配置阈值的实际存在性

仍要求全部f_us单射。任取有理T∈[1,2)使CONFIG(T)可行，令s=floor(d(T−1))，a=d−s∈[1,d]。

对任意r∈[1,a]满足(a−r+1)^h≥2r^h−1，完整原P存在实际合法σ使Cmax≤2−r/d。

特别取r=floor((a+2)/3)，对全部d,h,T可行，且

OPT(P) ≤ 2−r/d ≤ (5/3)(1+s/d) ≤ (5/3)T。

因此该完整**注入状态**结构类的配置整数间隙至多5/3。T≥2时可全port父置、selector任选根给实际C≤2，亦符合该上界。这里仅给实际σ存在性，未宣称任意变参d,h下可总位poly构造它；配置LP可行性本身有多项式规模精确系统。

### C. 去掉状态注入假设后的严格(1,5/3)承诺判定

本项允许原f_us任意，含同一state多leaf共外机。存在确定性总位多项式**判定器**，区分承诺YES OPT(P)≤1与NO OPT(P)>5/3。具体程序：删除每个非单射state作为selector候选（其原机器和jobs不实际删除，原jobs仍须解释）；若某root无剩余state返回NO；否则只在剩余state上解A的共同λ LP，可行返回YES，不可行返回NO。

声称：LP不可行（含空菜单）保证原OPT>1；可行保证原全部jobs存在实际C≤5/3调度，被排除状态原port jobs可全父置。中间带1<OPT≤5/3的回答不作承诺。此不声称一般变参下输出σ，也不声称非注入原P的CONFIG间隙≤5/3。

### 依赖与边界

继承v1精确组合对象：私有满树叶命中数以及Haxell超图匹配存在定理，全部适用条件须另核primary。配置行、边际和全原P负载要自足核对；不能仅凭有限实验。旧v1只给共同fullbundle λ与阈值条件，新增A/B/C量词另立本v2，不倒改其冻结字节。

不包括共享内部机器、其它processing times、原leaf多单位端或异构树。没有外部新颖性认证/实际生产实现，UM-TARGET-v1保持OPEN。


## 证明一： 全部阈值的精确边际系统

先不要求单state叶映射注入。T<1时任一selector无可用配置，故非空模型不可行。T≥2时全部ports父置，每selector任选根，真实C≤2。

固定1≤T<2，s=floor(d(T−1))，a=d−s。对每state根给selector边际y_us，Σ_s y_us=1。每SU内部或leaf job给unit端边际t_e，small端1−t_e。每internalmachine的incoming边际q_v是根y_us或父job的t_parent。则CONFIG(T)当且仅当

0≤y,t≤1；Σ_s y_us=1；Σ_out(v)(q_v−t_e)_+≤s q_v；Σ_leaf e:f(e)=z t_e≤1（每z）。

必要性：在内部机任一配置，若incomingunit出现，则可同时放smalljob数量≤s；对每outjob，其unit去别处边际t_e，home出现边际1−t_e，所以它与incoming同时出现的概率≥(q_v−t_e)_+。相加得行不等式。externalmachine在T<2至多一unitjob，给资源行。精确覆盖可从至少覆盖配置删额外jobs取得，不增加任何负载。

充分性可逐行显式分解。记c_e=(q−t_e)_+，a_e=1−t_e。incoming概率区间长度q上，把长度c_e的段串接再模q投影，每点至多s个small，因为Σc_e≤sq且c_e≤q；剩余无incoming区间长1−q，各small用初段[0,a_e−c_e)。均有效，且每job marginal为a_e。q0/1时省略相应空区间。无incoming时所有d个small总工作1，有incoming时≤s个small负载1+s/d≤T。external用各leaf singleton配置概率t_e和empty补齐。每machine概率和1、所有原jobs恰覆盖1，selector所有state端概率和1。配置无需由一个全局joint调度分布产生。

引入z_ve≥0、z_ve≥q_v−t_e、Σz_ve≤sq_v即多项式有理LP。标准deterministic rational LP可行性位poly；显式树控制d,h及各行/全部变量数。阈值只在1+j/d改变，故可二分j求精确Tconf；此不意味着整数σ已可poly构造。

## 2. CONFIG(1)的共同full-state λ消元

s0时各outgoing t_e≥q_v，沿任一state树下传归纳每leaf的unit边际≥根y_us。因此λ_us=y_us满足每root和1和外机容量Σλ_us |f_us^−1(z)|≤1。这里即使f不注入也以multiplicity计，不把重复资源偷算一次。

反过来，任意共同λ令该state所有edges/leafs t_e=λ_us、root y_us=λ_us。每internal机用incoming singleton权λ、全部d small权1−λ；external每leafsingleton权λ，资源行剩余empty补齐。每SUjob覆盖λ+(1−λ)=1；selectorΣλ=1。故精确等价。A项在注入模型当然成立；这一步本身不需要注入，但B的Haxell叶集合需要。

## 3. 一般T的a-分枝共同分布

现在假设全部f_us注入，在第1节有理系数可行LP中选一份有理可行点，取其共同边际。行不等式等价于Σ_out min(q_v,t_e)≥a q_v。

对每state从根以概率y_us被选，递归定义实际激活质量b_v≤q_v（根b=y_us）。若b=0全部后继激活质量设0。若b>0，则q>0，且对0<b≤q有

Σ_e min(b,t_e) ≥(b/q)Σ_e min(q,t_e) ≥a b。

选有理b_e≤min(b,t_e)，Σ_e b_e=a b；例如按固定次序贪心装至总量ab。向量b_e/b∈[0,1]^d、和a，是uniform-matroid base polytope，因此可分解成恰a个children的子集分布。给定该节点激活，按此分布选恰a个outgoing jobs导向unit端，递归所有选中children。不同节点分布可条件独立。

所有实际激活质量与此递归一致，且child b_e≤t_e=q_child。每root先按Σ_s y_us=1选一个state，再内部随机生成满a叉高h子树。所得是有限分布（可指数多支持），每leafunit激活概率≤原t_leaf；于是全部root/state/subtree的联合**各root边际分布**满足每外机期望请求≤Σ_leaf t_e≤1。

这一步不是把完整CONFIG certificate当整数调度联合分布。它利用私有树及uniform行单调性，另外构造每root的一份局部随机a-subtree；不同root尚未互斥，互斥由第4节定理提供。single-state injective f保证每个生成的a-tree的全部a^h leaf外机不同。

## 4. 精确树阻断数与Haxell全部条件

先述纯组合引理。满a叉高h树中，打中每个满r叉高h子树的叶集合最小大小为B_h=(a−r+1)^h。h0为1；递归时若至少r个child保留r-subtree则根也保留，故要破坏至少a−r+1个child，每个至少B_(h−1)；相同递归删除给上界。因此等号。若一棵state的leafmap注入，资源hitting集合X打中它每个r-subtree时，|X∩fullleafimage|至少B_h，不能因多叶共外机降低此数。

对每root，取第3节局部分布中的所有正权a-tree为辅助states；每个a-tree内的每个r-subtree形成资源集合，大小R=r^h。构造bipartite hypergraph：一侧为root U，另一侧为external resources Z；每候选集合加其root成一条edge。每edge恰1root和R个resources，总大小R+1。可以指数多edges，但有限；本节为存在性，不称已poly展开。

任意非空I⊆U及其资源邻域超图的transversal X：每个I-root的每个辅助state均被X打中其所有候选r-subtrees，所以至少B_h个不同fullleaf资源在X。对共同局部分布λ加权，

B_h |I| ≤ Σ_{u∈I,state}λ_state |X∩fullleafimage_state| ≤ |X|。

最后不等式用的是第3节同一份资源期望容量，不是逐resource重选分布。故τ(H_I)≥B_h|I|。

所用外部Paper Fact为Haxell hypergraph Hall条件：若每超边恰含一root、至多k−1个resource，且每I的资源transversal number > (2k−3)(|I|−1)，则有覆盖全部root的matching。入库前root已实际打开AFS2008作者稿Theorem2（物理PDF5）、Theorem3（物理PDF6）和Annamalai arXiv1509.07007v2 Theorem1.1（物理PDF2）及Theorem1.3（物理PDF3）的准确陈述；未取得/完整重构Haxell1995原proof，不冒称外部完整重证。令k=R+1，阈值即(2R−1)(|I|−1)。当B_h≥2R−1时，上述τ≥B_h|I|严格大于所需阈值。I空条件自动；R1退化Hall，d1/a1/r1均合法。重复候选edges可去重但保一份state/tree witness，有限菜单和λ0 states无碍。

于是有每root一个真实state、一个r-subtree，全部末外资源互异。

## 5. 回到所有原jobs和数值界

selector放选中真实state根。每激活节点恰r个ports向child或外资源，其余原d−r个ports父置；不在该r-subtree的全部节点、所有未选/零权states，原ports全部父置。每个原job恰排一端。

active internal机恰incomingunit1及d−r个small jobs，总2−r/d。inactive internal无incomingunit，原d个small总1。每外机最多一个选中leafunit。未选a-tree只用于存在性，它们不是新增原任务，也不能遗漏同state其他原d-branches。因此完整P actualC≤2−r/d。

令r=floor((a+2)/3)=ceil(a/3)≥1，则a−r+1≥2r−1，(2r−1)^h≥2r^h−1（对r≥1,h≥1可由二项式/凸性逐幂证）。故所需B_h条件成立。写x=a/d∈(0,1]，T0=1+s/d=2−x，C≤2−x/3≤(5/3)(2−x)，最后等价于x≤1。T0≤T，所以OPT≤(5/3)T。T≥2的全父置补齐全阈值；没有声称5/3锐。

## 6. 任意非注入状态的严格promise判定

允许原f非单射。任何actual C≤1调度，selector所在根incomingunit1强制所有正smallports外送；递归强制整个选中full tree所有leafunit在外机执行。这些leaf必须互异，否则某外机≥2。所以每root所选state一定单射，且全root的选中full images互斥。其0/1状态选择本身给过滤后共同λ LP可行。

反过来，过滤后的λ LP可行时，对保留injective states用第2–5节s0得到actual C≤5/3。对每个被过滤state，不删除任何原job，而是全部ports父置，每内部机负载1；selector从未在该state取端，因此无额外incoming。不同states内部全私有确保此回填不干扰保留部分。故给原P的全部jobs确有此actual调度。

逐state查f单射及写共同λ资源行均按显式P多项式；某root无保留state时返回NO，其它情况用标准确定性有理LP判可行。NO答案保证原OPT>1，YES答案保证原OPT≤5/3，故正确区分promise。中间带任意回答合法。该程序不输出σ；非注入原P CONFIG可行不保证过滤λ可行，不能把此结论错误升级成非注入类的CONFIG gap5/3。经典近二配置族不受B项否定。

v2是限定结构类的新范围，非一般UM算法或主反证；无生产实现/全球新颖性认证。若需要实际sigma的uniformpoly算法，尚须单独核constructive Haxell的rank/隐式超边/参数条件，不能从本存在性投票得到。


## 已有技术、反例边界与下一条真实义务

Haxell的transversal匹配定理是外部已有技术；AFS2008 Theorem3已经将普通集合的所有定长子集、分数容量和命中集计数接到同一匹配框架。因此这里不把Haxell、分数计数或超图匹配框架称作新方法。本文可复用的具体增量是：完整私有树的精确叶阻断数、CONFIG(T)向同一份a叉树分布的支配桥、完整原d叉任务回填和严格过滤判定共同适用的范围；全球新颖性未认证。

本结论覆盖任意显式菜单和任意叶外端编号，只要每个完整state的leaf map单射。特别是，一个编译若对任意源输入（包括NO源）都落入该结构并提供CONFIG(1)，则其实际OPT总≤5/3；独立随机重编号端口不会消除这个结论。此为该合同的直接应用，不是对任意随机覆盖或任意UM算法的否定。

注入性仅在B的叶阻断资源计数承重；A的multiplicity消元本身可不要求注入，C也允许非注入输入，但只输出严格promise的判定。已有非注入近二配置间隙族没有被B覆盖。若把严格YES放宽至1+1/d、允许重复叶色并让height随输入增长，C不再排除困难性；固定参数局部枚举与变参展开也须分清。共享内部机器、每行多个incoming、非均匀processing times、多单位叶端、额外任务和预载均在本文结构域外。

5/3仅为已证上界，未证明锐利。没有将Haxell的有限存在/指数局部搜索称作确定性位多项式输出σ。Annamalai2016 Theorem1.3的算法另外要求固定超边rank及固定正slack；本文辅助r^h可随输入变动、超边族可指数大，故未把该算法直接导入。配置LP小型系统与C判定器的位多项式性有各自自足证明，与σ构造状态分开登记。

没有新增生产实现或有限运行证书；有限树枚举不作为一般证明。UM-TARGET-v1正反面仍OPEN。
