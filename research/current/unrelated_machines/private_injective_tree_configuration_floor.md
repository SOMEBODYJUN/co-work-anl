# 私有树的重数配置界、锐渐近与严格承诺判定

读取目的：确定均匀小端私有树何时必有实际低负载调度，从而核对任意菜单、任意端口重编号的近二困难性编译是否可能。本文是限定结构类的配置整数间隙上界及判定结论，不是一般UM算法，也不是一般UM不存在统一改进的证明。

本页保留 `UM-Q-PRIVATE-INJECTIVE-TREE-CONFIGURATION-FLOOR-v2`，并另立下文有界重数v3与间隙一阶锐渐近身份。v1先给共同full-state分数点的hitting/Haxell界，v2另加全CONFIG(T)与非注入菜单过滤判定；旧Exact/证明/独立重构原字节保留为来源，不另复制成一套现行资产。证明完成、陈述先行独立重构及全文读后攻击已发生；无standing fatal。外审、新颖性、独立成文价值及任意变参下输出σ的多项式算法均未认证。

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


## UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3：有界完整状态叶重数

此为新对象/量词，旧v2注入合同未倒改；固定μ时才有与其它输入无关的离二常数。证明及真实两阶段内审完成，无生产实现、外审或新颖性认证。 本附节的证明编号1–7均只指v3局部段落；下文渐近证明另编号，不与旧v2的编号混用。

### Objects / Domain / Quantifiers / Assumptions

任意整数 d,h,μ≥1。μ 允许作为二进制输入，不预设固定；“统一常数离二”仅在 μ 固定时解释为与其它输入无关的常数。有限非空 root 集 U，每 u 有非空有限显式状态菜单 S_u；共享有限外机集合 Z。

每 (u,s) 是完全私有的满 d 叉高 h 树，深 0,…,h−1 为内部机器，叶地址为 [d]^h；不同状态内部机器也不共享。完整普通调度输入 P：每 u 一枚 unit selector，其全部合法端恰为各状态根；每内部 edge job 父端时间 1/d、子端时间 1；每 leaf job 父端时间 1/d、唯一外机端时间 1，其外机由显式 f_us:[d]^h→Z 给出。其它端∞，没有额外 jobs、预载或其它有限时间。

全部状态、机器、jobs 和 leaf 资格都显式列出。**不要求 f_us 单射**，而要求每个完整状态的每个资源实际重数均有同一个上界：

\[
 |f_{us}^{-1}(z)|\le\mu\qquad(\forall u,s,z).
\]

不同状态／root 间可任意共享资源；μ 不限制跨状态总重数。

CONFIG(T) 是完整原 P 的通常配置 LP，配置负载≤T，每机器权重和 1，每原 job 覆盖恰 1；向下封闭下与至少覆盖版等价。非空 U 的 selector 保证 OPT,T_conf≥1。空 U 仅作单独空任务情形，不套该下界。

## Definitions

一个真实 state 中的满 r 叉高 h 子树称为 **rainbow**，当且仅当其 r^h 个叶映到 r^h 个互不相同的实际外机。选出子树必须包含该 state 的原根并在每一活跃内部节点恰选 r 个原 children，不能逐路径更换 state。

对任意满 a 叉高 h 抽象树的叶子集 A，q(A) 为 A 中所含满 r 叉高 h 根子树的最大整数 r∈[1,a]；若不存在则 q(A)=0。这个辅助定义仅用于精确解释下列局部陈述。

## Exact Statements

### L. 局部有界重数 rainbow 与资源 blocker 下界

任意整数 a,h,μ≥1，给满 a 叉高 h 树任意叶资源映射 f，每资源在该整树出现至多 μ 次。

1. 存在满 `ceil(a/μ)` 叉高 h 的 rainbow 子树。特别地，μ=2、a=3 时，对任意 h≥1 均存在 binary rainbow 子树。
2. 对任何整数 r∈[1,a] 且 μ(r−1)<a，任意资源集合 X 若命中该树中**所有 rainbow 满 r 叉高 h 子树**的资源像，则

\[
 |f^{-1}(X)|\ge [a-\mu(r-1)]^h.
\]

第二项仅声称下界，不声称对所有 a,r,h,μ 都达到等号。计数对象是原叶逆像的 multiplicity，不是把一个资源直接当作一个叶。

### A. 共同 full-state 分数点的实际离二存在性

给共同非负有理 λ_us，满足

\[
 \sum_{s\in S_u}\lambda_{us}=1\quad(\forall u),
 \qquad
 \sum_{u,s}\lambda_{us}|f_{us}^{-1}(z)|\le1\quad(\forall z).
\]

所有资源行必须来自同一份 λ，按实际 multiplicity 计。则对每个整数 r∈[1,d]，若

\[
 \mu(r-1)<d,
 \qquad[d-\mu(r-1)]^h\ge2r^h-1,
\]

存在对每 root 选一个真实状态及其中一个 rainbow 满 r 叉高 h 子树，使全部选中叶资源在所有 root 间也互不相交。完整原 P 存在实际合法 σ，满足

\[
 C_{\max}(\sigma)\le2-r/d.
\]

所有未选 state、未选分枝和零 λ state 的原 jobs 均在该 σ 内。

### B. 全部 CONFIG(T) 阈值与配置整数间隙

对任意有理 T∈[1,2)，若完整原 P 的 CONFIG(T) 可行，设

\[
 s=\lfloor d(T-1)\rfloor,\qquad a=d-s\in[1,d].
\]

对任何整数 r∈[1,a]，若

\[
 \mu(r-1)<a,
 \qquad[a-\mu(r-1)]^h\ge2r^h-1,
\]

则完整原 P 存在真实状态／rainbow 满 r 子树的全 root 不交选择，及实际合法 σ 满足 Cmax≤2−r/d。

特别取

\[
 r=\left\lceil\frac{a}{\mu+2}\right\rceil,
 \qquad\alpha_\mu=2-\frac1{\mu+2},
\]

对所有这些参数均满足上述数值前提，且

\[
 \operatorname{OPT}(P)
 \le2-r/d
 \le\alpha_\mu(1+s/d)
 \le\alpha_\mu T.
\]

T≥2 时有完整实际 C≤2 的直接调度，补齐全部配置阈值。因此此有界**每完整 state 叶资源重数**结构类的配置整数间隙至多 α_μ；μ=1 恢复 v2 的五三上界，μ=2 给七四上界。α_μ 是已证候选上界，不声称锐利。


### 证明：raw q、rainbow blocker与全CONFIG桥

 raw 叶估值 q 的子可加性

对满 a 叉高 h 树，q(A) 是叶集 A 所含的最大同深完整分叉数。需要的是 raw 叶集合估值，不是对带重复色资源直接套一个已假定单射的 resource-demand theorem。

对任意有限叶集族 A_1,…,A_m，有

\[
 q\left(\bigcup_i A_i\right)\le\sum_iq(A_i).
\tag{1}
\]

独立归纳证明如下。h=1 时 q(A)=|A|，结论是普通并集计数。设 h≥2 且已知孩子树上的结论。令 Q=q(∪A_i)，b_i=q(A_i)。若 Q=0 或 Σb_i≥Q，无需证明。否则存在 Q 个孩子，每个孩子下面 ∪A_i 都含 Q 叉高 h−1 子树。对每 i，根的 q(A_i)=b_i 表明“孩子树 q(A_i∩L_child)>b_i”的孩子至多 b_i 个，否则可在至少 b_i+1 个孩子下各取 b_i+1 叉子树，组合出更大根子树。因为 Σb_i<Q，在上述 Q 个孩子中至少有一个孩子对所有 i 都满足 q_i(child)≤b_i。孩子归纳结论给该处的 union value≤Σb_i<Q，与其含 Q 叉子树矛盾。

此归纳也覆盖 a=1、空 A_i、重复 A_i；h=0 不在主域，不需要给 q 的叶辅助值另设约定。该结论与既存 `UM-PRIVATE-TREE-Q-VALUATION-v1` 的 raw 单树部分一致；没有新增 demand/oracle 合同。

## 2. bounded multiplicity 的 rainbow 与 blocker

令 f 为满 a 叉高 h 树的叶资源映射，每个资源出现至多 μ 次。按每个资源的 occurrence 固定顺序，把它的第 j 次出现放入第 j 个叶类，j=1,…,μ；不足的类留空。于是每个叶类本身 rainbow。这只是有限证明划分，μ 为 binary 大整数也不把 μ 的显式展开当作运行时间结论；实际非空类数不超过显式叶数。

全叶的 q 值为 a。由 (1)，某个类 q≥ceil(a/μ)，其对应子树为 rainbow。这立即给 μ2、a3 的任意高度 binary rainbow 子树，故不存在该参数的局部反例。

现固定 r∈[1,a] 且 t=μ(r−1)<a。设资源 X 命中所有 rainbow 满 r 子树。去掉 X 的全部叶逆像，留下 A=f^{-1}(Z\X)。A 中不含 rainbow 满 r 子树。再按相同 occurrence 方法把 A 划为至多 μ 个 rainbow 叶类 A_j；每个类 q(A_j)≤r−1，否则类内的 r 子树就是避开 X 的 rainbow 候选。由 (1)，q(A)≤μ(r−1)=t。

因此删除集 f^{-1}(X) 命中原满 a 树中的**所有 raw 满 t+1 子树**。满 a 叉高 h 树的这类叶 blocker 最少有

\[
 (a-(t+1)+1)^h=(a-t)^h
\]

个叶：若根处仍有至少 t+1 个孩子各自保留 t+1 子树，则根也保留；故至少 a−t 个孩子必须各自被阻断，按高度递归给下界并可递归达到。于是

\[
 |f^{-1}(X)|\ge[a-\mu(r-1)]^h.
\tag{2}
\]

这里没有把 raw 子树误当 rainbow 超边；(1) 和 occurrence 划分正是两者之间的额外桥。(2) 计数 raw 叶逆像，后续要与原共同 λ 的 multiplicity 容量相接，不应先除以 μ。

## 3. 共同 full-state λ 的 rainbow Haxell 匹配

先证明 Exact A 的纯选择部分，令树分叉数为 d。对每 root u、每真实 state s，枚举全部 rainbow 满 r 叉高 h 子树，取其真实资源集。每集恰 k=r^h 个不同外机。加上 root tag u，得到有限二部超图，总超边大小 k+1。重复超边可去重但保留一个真实 state／子树 witness。

对任意非空 I⊆U，设资源集合 X 命中所有 I-root 的候选边。按 (2)，每个 (u∈I,s) 都满足

\[
 |f_{us}^{-1}(X)|\ge B,
 \qquad B=[d-\mu(r-1)]^h.
\]

使用同一共同 λ 及其 multiplicity 容量，交换有限求和：

\[
\begin{aligned}
 B|I|
 &\le\sum_{u\in I,s}\lambda_{us}|f_{us}^{-1}(X)|\\
 &=\sum_{z\in X}\sum_{u\in I,s}
      \lambda_{us}|f_{us}^{-1}(z)|\\
 &\le|X|.
\end{aligned}
\tag{3}
\]

所以资源 transversal number 至少 B|I|。若 B≥2k−1，则它严格大于 `(2k−1)(|I|−1)`。对总超边大小 k+1，Haxell 条件恰为该常数 2(k+1)−3；因此有覆盖所有 root 的匹配。每条匹配边带一个真实状态和 rainbow r 子树，全部 root 的所有末资源互不相同。μ(r−1)<d 还保证每 state 至少有一个 rainbow r 候选，亦可直接由第 2 节局部结论看出。空 I 的严格条件自动满足。

本次外部定理实际亲核来源沿用已审 v1/v2：Annamalai, *Finding Perfect Matchings in Bipartite Hypergraphs*, arXiv:1509.07007v2，PDF 第2页／印第1页 Theorem1.1 及定义。该文 r-uniform 的 r 是**总边大小**，资源 hitting set 限于 B 侧；本次所有边恰 k+1，完全符合。原 PDF SHA256 `f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce`。未取得／冒称重证 Haxell1995 原全文。

## 4. CONFIG(T) 的 a-tree 支配桥不要求单射

给 1≤T<2 的完整 CONFIG，写 s=⌊d(T−1)⌋、a=d−s。取一份有理可行边际点；v2 小型系统是有理系数，故可无损这样选择。

每内部机器有唯一 incoming unit job，边际 q_v；每 outgoing job 的 unit 下端边际为 t_e。含 incoming 的配置至多 s 枚父置 small，所以边际行满足

\[
 \sum_e(q_v-t_e)_+\le s q_v
 \quad\Longleftrightarrow\quad
 \sum_e\min(q_v,t_e)\ge a q_v.
\tag{4}
\]

外机至多放一枚 unit，故 Σ_leaf e:f(e)=z t_e≤1。这两个条件不需要 f 单射；同一 state 的不同 leaf jobs 若同外机，也逐 job 计入和。

每 root 按各状态根 selector 边际 y_us（和为1）选真实 state。按 v2 递归令根活跃质量 b=y_us。对已定义的 0<b≤q_v，逐项有 `min(b,t_e)≥(b/q_v)min(q_v,t_e)`，故总容量≥ab。可取有理 b_e≤min(b,t_e)、Σb_e=ab，分解 b_e/b 这一 uniform-matroid base vector 成恰 a 个孩子的随机子集；b=0 时后继全零。递归后，每 root 形成一个真实状态内满 a 叉高 h 子树的有限分布，每原叶活跃概率≤t_leaf。

各生成 a-tree 的叶资源映射可能重复，但仍每色≤μ，因为只是原完整 state 的叶子集。将每个正权生成树作为辅助 state，保留其原真实 state witness，取其每 root 分布权重为共同 λ_aux。每外机的期望请求按 multiplicity 为

\[
 \sum_{u,\mathrm{aux}}\lambda_{u,\mathrm{aux}}
  |f_{u,\mathrm{aux}}^{-1}(z)|
 \le\sum_{\mathrm{all\ original\ leaf\ }e:f(e)=z}t_e\le1.
\tag{5}
\]

辅助 state 的支持可为指数大小，但有限。不同 root 尚未互斥；这里只建立 (5)，没有把 LP 自身当整数调度联合分布。

将第 3 节纯组合选择论证应用于分叉数 a 的这些辅助树：候选只取其中的 rainbow r 子树，blocker 为 `[a−μ(r−1)]^h`。若满足 Exact B 的数值条件，Haxell 给出全 root 不交选择。该选择返回原真实 state 内的一棵 r 子树。辅助 a-tree 不是新物理输入，最终负载仍按原 d 个 outgoing jobs 及原时间 1/d 计算。

## 5. 完整原 P 的实际调度

selector 放在匹配选出的原状态根；选中 r 子树内的原 jobs 全下送到 unit 端，所有其它原 jobs 全父置，包括所有未选／零权 states 和同一原 d 树中未选分枝。

活跃内部机器恰一枚 incoming unit（根为 selector，非根为父 job）及 d−r 枚 small，负载 2−r/d。非活跃内部机器没有 incoming unit，其 d 枚 outgoing jobs 父置，总负载1。匹配边为 rainbow，且跨 root 不交，故每外机至多一枚选中 unit leaf。每原 job 恰排一次，所有端是原 P 合法端，完整 Cmax≤2−r/d。

这一步既不要求未选 state 注入，也不对辅助树之外的原 jobs 作删除；私有内部机器是承重条件。

## 6. 默认 r 与全配置整数间隙

令 `r=ceil[a/(μ+2)]`，则 `a≥(μ+2)(r−1)+1`，所以

\[
 a-\mu(r-1)\ge2r-1\ge1.
\]

对 h≥1、r≥1，凸性给 `(2r−1)^h+1≥2r^h`，于是 B≥2r^h−1，且 μ(r−1)<a。默认参数始终合法。

记 β=1/(μ+2)、α_μ=2−β、x=a/d∈(0,1]，T0=1+s/d=2−x。因为 r≥βa，

\[
 C\le2-\beta x\le(2-\beta)(2-x)=\alpha_\mu T_0
 \le\alpha_\mu T.
\]

中间差为 `2(1−β)(1−x)≥0`。T≥2 时原 P 的全部 port 父置且每 selector 任选状态根给实际 C≤2，亦符合 α_μT。非空 selector 排除 T<1。因而对配置阈值取下确界可得 OPT/T_conf≤α_μ；不要求无限阈值或概率极限操作。

μ1 恢复状态注入和 v2 的同一数值条件，α1=5/3；μ2 给 α2=7/4。这里不声称这两个界锐利。

## 7. 退化、复杂度与准确否定范围

- a1、r1 时超图总大小2，条件退化为 Hall；在A共同λ或B的CONFIG(T<2)可行前提下，d1得到实际C1；否则全父置仍给C2，允许任意给定 μ 上界只使 stated α_μ 松一些。
- h1 的 q 是叶数、blocker 为 a−μ(r−1)，全部推导成立。h0 不在模型。
- μ≥1 可以 binary 输入且远大于实际重数；无需按 μ 构造生产算法。资源实际重数从显式 leaf list 可数清；选择较松的 μ 只弱化数值保证。
- 空 U 是单独空任务情况，最优0；主链用非空 selector 下界1。
- Haxell 候选边族及辅助 a-tree 分布可能指数多，本 proof 只给有限实际见证的存在。没有把外部 fixed-rank、fixed-slack 算法套为变参位多项式 σ 构造。
- 均匀 private 结构的 CONFIG 小型系统与可行性算法不受本次 multiplicity 改动影响，但它们只计算分数阈值／作承诺判定，不替代实际 σ 输出。
- 固定 μ 得到常数 α_μ<2；一般 UM 的任意输入、共享内部机器、非均匀时间或 μ 随输入无界不被统一常数结论覆盖。
- 全部已用的 q 子可加、raw blocker、Haxell 与分数求和都明确扣除已有技术。本次新范围是 rainbow 候选与 bounded multiplicity 之间的桥及其全 CONFIG(T) 应用；全球新颖性和独立成文价值未认证。



## UM-PRIVATE-TREE-MULTIPLICITY-GAP-ASYMPTOTIC-v1：重数参数的一阶锐配置间隙

仅给配置gap的参数渐近，平星族本身可直接精确解；不作算法困难性或UM反面。

### Objects / Domain / Definitions

对整数 μ≥2，令 C_μ 为下列所有有限显式调度输入 P 的类：

- 整数 d,h≥1，非空有限 root 集 U，每 u 有非空有限显式 state 菜单 S_u。
- 每 state 为完全私有的满 d 叉高 h 树，内部机器深 0,…,h−1；不同 states 内部机器也互异。共享有限外机集合 Z。
- 每 u 一枚 unit selector，合法端恰为该 u 的全部 state 根；每内部 edge job 父端时间1/d、子端时间1；每 leaf job 父端时间1/d、唯一外机端时间1，外机由显式 f_us:[d]^h→Z 指定；其它端∞。没有其它 jobs、预载或时间。
- 每个**完整 state** 的每个资源实际重数不超过 μ：`|f_us^{-1}(z)|≤μ`。不同 states／roots 间可任意共享外资源。
- 全部状态、机器、jobs 和叶资格显式给出，不能用 binary d,h 代替巨大树展开。

CONFIG(T) 为完整原 P 的普通配置 LP（每机器权重和1，每 job 恰覆盖1，配置负载≤T），T_conf(P) 为其最小可行阈值／可行阈值下确界。非空 selector 使 T_conf(P)≥1，故下面比值良定义。

定义参数类的最坏配置整数间隙上确界

\[
 G(\mu)=\sup_{P\in C_\mu}
 \frac{\operatorname{OPT}(P)}{T_{\mathrm{conf}}(P)}.
\]

上确界同时遍历 d,h、root 数、菜单、外机集合、全部映射及所有有限显式输入长度；μ 仅约束每个完整 state 内的重数，不要求其它参数固定。不声称上确界对每个 μ 都达到。

## Exact Statement / Quantifiers / Conclusion

对每个整数 μ≥2，

\[
 2-\frac1\mu\ \le\ G(\mu)\ \le\ 2-\frac1{\mu+2}.
\]

因而，沿整数 μ→∞，

\[
 \lim_{\mu\to\infty}\mu\,[2-G(\mu)]=1.
\]

等价的误差界为

\[
 0\le G(\mu)-\left(2-\frac1\mu\right)
 \le\frac{2}{\mu(\mu+2)}.
\]

这是叶资源重数参数的一阶锐渐近，不给每个固定 μ 的精确 G(μ)，也不声称各固定 μ 上界 `2−1/(μ+2)` 锐利。

## 显式下界族的对象参数

对每个 μ≥2，取 d=μ、h=1、U={u}，该 root 恰有 μ 个 states s=1,…,μ。外机为 μ 个不同资源 z_1,…,z_μ。state s 的全部 μ 个 leaf jobs 都映到 z_s。内部机器仅为 μ 个 state 根，selector 一枚；每枚叶在其 state 根时间1/μ、在 z_s 时间1。没有其它 jobs 或端。

该族在 C_μ 中，具有精确比值 `OPT/T_conf=2−1/μ`，给上面的下界。这里只陈述该族和准确结论，不附分数证书或实际最优调度证明。


### 证明：平星族与上确界夹逼

1. 下界族的精确配置阈值

取 Exact 的 d=μ、h=1、单 root、μ states，state s 的 μ 个叶 jobs 全映到其私有 z_s。记 state 根为 v_s。所有内部机器仅 v_s；每叶 job 在 v_s 用时 1/μ，在 z_s 用时1；selector 在全部 v_s 用时1。

selector 保证 T_conf≥1。给 T=1 的具体配置点：

- 每根 v_s：selector singleton 权重 1/μ；全部 μ 个本 state small 叶 jobs 的配置权重 1−1/μ。后一配置总负载 μ·(1/μ)=1。
- 每外机 z_s：给其 μ 枚叶 jobs 各自 singleton 配置权重 1/μ，权重和为1。

每根权重和1；每 selector 覆盖 μ·(1/μ)=1；每叶 job 覆盖为 `(1−1/μ)+(1/μ)=1`。所有配置负载均≤1，故 T_conf=1。其共同 λ_s=1/μ，外容量按 μ 次 multiplicity 计，恰为1；此处没有把 μ 片同色叶偷合并成一枚 job。

## 2. 下界族的精确实际最优值

任何实际调度都把 selector 放在某个 v_s。若其 makespan C≥2，则当然 C≥2−1/μ。若 C<2，每个外机 z_s 只能接至多一枚 unit 叶 job；于是 selector 所在 v_s 的 μ 枚叶 jobs 中至少 μ−1 枚必须在 v_s 以 small 端执行。该根负载至少

\[
 1+\frac{\mu-1}{\mu}=2-\frac1\mu.
\]

反向取任一 s，selector 放 v_s，该 state 任取一枚叶外送 z_s，其余 μ−1 枚父置；全部其它 states 的原叶 jobs 全父置。选中根负载2−1/μ，其余根负载1，唯一使用外机负载1。全部原 jobs 恰安排一次，故

\[
 \operatorname{OPT}=2-\frac1\mu,
 \qquad \operatorname{OPT}/T_{\mathrm{conf}}=2-\frac1\mu.
\]

状态内实际重数恰为 μ，该族属于 C_μ。它有 μ 个根机、μ 个外机、μ² 枚叶 jobs 和一枚 selector，所有端、处理时间与∞可显式列出。这是一个参数化显式实例族，不声称仅按 log μ 生成全部 μ² jobs。

## 3. 上确界夹逼与整数参数极限

v3 的一般全 CONFIG(T) 结论对每 P∈C_μ 给出

\[
 \frac{\operatorname{OPT}(P)}{T_{\mathrm{conf}}(P)}
 \le 2-\frac1{\mu+2}.
\]

所以对所有输入取上确界，结合第2节显式族，

\[
 2-\frac1\mu\le G(\mu)\le2-\frac1{\mu+2}.
\]

这些界本身已保证 G 有限，无需主张上确界达到。两边的差为

\[
 \frac1\mu-\frac1{\mu+2}=\frac2{\mu(\mu+2)},
\]

即 Exact 所述精确误差界。等价地，

\[
 \frac\mu{\mu+2}\le\mu[2-G(\mu)]\le1.
\]

沿整数 μ→∞ 两端同趋1，得到 limit=1。因此正确的锐性表述为参数 μ 的一阶渐近，而非每个固定 μ 的 exact G 或 α_μ 锐利。

## 4. 准确身份

本项下界是能显式求解的一层平星实例的配置整数间隙，不能作为 NP-hardness、TFNP 搜索困难性或一般 UM 反面。它仅说明 bounded-multiplicity 上界中距2的 Θ(1/μ) 阶、乃至第一阶系数1不可改善；未消除 O(μ^−2) 范围。

一般上界依赖 v3 的 rainbow blocker/Haxell/全阈值证明；其真假和审查状态应共同登记。下界族和极限不引入额外外部定理。没有新软件实现、有限运行证书、全球新颖性或一般 σ 多项式算法认证。


固定μ的精确G仍未知；本文只证G(μ)=2−1/μ+O(μ^−2)，不能称每个固定μ的上界sharp。要用本类构造YES≤T、NO≥(2−δ)T且全部NO也有CONFIG(T)，允许的最大完整state重数上界μ必须至少1/δ−2：若δ<1/(μ+2)，上界直接排除该NO。μ可随所选固定δ增大，故这条设计限制不排除全部一般近二困难性归约。所有新匹配仅作存在性，没有一般参数polyσ。

## UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1：单强制根、整树重数的配置gap精确上确界

Exact Statement / Objects / Domain / Quantifiers：∀显式完整d叉树U（d≥2,h≥1，同深叶），整树每色≤binary µ≥1；原P为每internal一机/每色一外机（不交namespace）、单端root pin1、每树边job parent1/d与唯一child或色resource1，其余∞。q为最大满r叉同深rainbow。则OPT=2−q/d，q≥ceil(d/µ)，可det bitpoly输出全部原σ C≤2−ceil(d/µ)/d≤2−1/µ；不按巨大µ循环。对每固定µ，sup全部同类OPT/Tconf恰2−1/µ（µ1逐实例为1）。µ≥2、µ|d、µ((d−1)/d)^h≤1时，有每色恰µ的显式族，q=d/µ、OPT=2−1/µ、Tconf=1+1/d；可取h=d ceil(log2µ)，d沿µ倍数增大逼sup。

Assumptions / Dependencies：无复杂度假设；普通CONFIG、raw q子可加/显式DP，自足全P回算与配置分布。Scope / Conclusion：只单root/global whole-tree µ；不改旧privateforest/menu固定µ未知G。此易解族非hardness，µ无界时无统一epsilon。Evidence / Status：完整限定证明/陈述先行独立重构/作者证明读后攻击/root全核；无新代码、外审或新颖性认证。Counterevidence/Objections：无standing fatal；原作者泛d1备注不扩正式域；全部U反向已补。Related Files：本页、既有q正文、对应review及四份冻结源（crosswalk逐项）。

### S0. 任意U的OPT恒等式与全任务提取

记q为最大uniform虹彩分叉。给定q见证，选中边全下送、其余原边全父置；active机unit+(d−q)/d，inactive机1，颜色资源≤1，所以OPT≤2−q/d。反之任意完整实际σ若C≥2下界自动；若C<2，pin迫C≥1，每active机至少r=ceil[d(2−C)]枚原边job真实下送。由root递归每次保留r条，得到满r叉同深树；每resource在C<2至多一unit，故全部选中叶色互异，q≥r≥d(2−C)。因此OPT恰2−q/d，含q1/qd及h1边界。给σ抽树、给树回填均位poly；不免费计算最优q。此段由root与pcsp独立稿补齐作者稿全U反向的整理缺口。

### S1. 完整对象、配置阈值与量词

给整数 d≥2、h≥1，一棵完整 d 叉、根到叶距离 h 的树。每个非叶节点是独立的内部机器。根有一枚只能在根处理、时间 1 的 pin job。每条连接两个内部节点的树边有一枚 job：父机器时间 1/d，子机器时间 1。每条连接最后一层内部节点与概念叶的边有一枚 leaf job：父机器时间 1/d，在该叶的颜色机器时间 1。每种颜色恰对应一台外部机器，此外没有资格、机器、jobs 或预载。同一颜色的全部叶共享同一台外部机器。所有 jobs 不可拆分。

写 L=d^h 为叶数，I=1+d+⋯+d^(h−1) 为内部节点数。基础 job 数恰 I+L：I−1 枚内部边 jobs、L 枚 leaf jobs、一枚 pin。颜色机器数是实际出现的颜色数。本Claim正式域固定d≥2；不以作者稿额外d1备注静默扩域。

给整数 μ≥1，类 S_μ 包含所有这样的有限显式输入，要求每一种颜色在**整棵树**中最多出现 μ 次。μ 是上界，不要求达到。这里没有多根间或多状态间的单独重数约束；仅一棵完整树。

CONFIG(T) 是通常的机器配置 LP：每台机器在其总处理时间不超过 T 的合法 job 子集上取分布，每个 job 的机器边际覆盖恰为 1。允许空配置。用覆盖至少 1、每台总质量至多 1 的写法也等价：利用配置向下封闭、删去冗余 job，再用空配置补齐。记 T_conf 为最小可行阈值。该值存在并且正：pin 强制 T_conf≥1，而所有边 job 都放父机器给出真实 C_max=2，故 CONFIG(2) 可行。有限输入只有有限多个配置负载，最小阈值确实取到。

主结论为

    sup_{P∈S_μ} OPT(P)/T_conf(P) = 2−1/μ       (μ≥1).

μ=1 时右端 1，每个成员恰 OPT=T_conf=1。μ≥2时此处声明的是上确界。另有确定性显式输入位多项式算法，对 S_μ 输出全部原始 jobs 的实际调度，C_max≤2−1/μ；它也给同系数近似，因为 OPT≥1。

### S2. 原始分叉函数的次可加性

对同一完整 d 叉 h 树的叶子集 A，定义 q(A) 为 A 支持的、从原根开始、仍深 h 的完整 uniform r 叉子树的最大整数 r∈{1,…,d}；若没有，q(A)=0。子树的叶必须在 A 中。这里是完整深度、每一层相同分叉 r；不把叶密度当分叉。

引理：对任意有限叶集 A_1,…,A_m，

    q(⋃_i A_i) ≤ Σ_i q(A_i).

证明按 h 归纳。h=1 时 q(A)=|A|，是并集基数不等式。h≥2 时令 Q=q(⋃A_i)、b_i=q(A_i)。若 Q=0 或 Σb_i≥Q，结论成立。反设 Σb_i<Q。并集的 Q 叉见证在根下选择 Q 个孩子，每个选定孩子内的并集分叉至少 Q。对固定 i，至多 b_i 个根孩子的 A_i 局部分叉大于 b_i；否则 b_i+1 个孩子各有分叉至少 b_i+1，便在原根合成 b_i+1 叉树，矛盾。所有 i 的这种例外孩子的并集大小至多 Σb_i<Q，故 Q 个选定孩子中存在一个，对所有 i 均有局部分叉≤b_i。在该孩子的深 h−1 树内应用归纳，并集局部分叉≤Σb_i<Q，矛盾。证毕。

此证明同时允许空 A_i、重复 A_i。它是 q 的次可加性，不声称 q 次模。

### S3. 全树 μ 分桶给出的实际上界

按叶的显式次序，将每种颜色的第 j 次出现放入第 j 桶。若实际最大重数为 m≤μ，只创建 m 个非空桶；不按二进制 μ 创建空桶。每桶叶的颜色互异。所有叶的 q 值是 d，由引理有

    d ≤ Σ_{j=1}^m q(B_j),

故存在桶满足 q(B_j)≥ceil(d/m)≥ceil(d/μ)。取其实际 r 叉见证，r≥ceil(d/μ)。它的所有叶颜色互异。

把见证子树上的所有边 jobs 都向下安排：内部边去子机器，leaf job 去其颜色机器。其余全部边 jobs 留在父机器，pin 在根。于是：

* 每个见证内部节点有且仅有一枚时间 1 的 incoming job（根对应 pin），并保留 d−r 枚时间 1/d 的 outgoing jobs，总负载 1+(d−r)/d=2−r/d。
* 非见证内部节点没有 incoming unit job；其全部 d 枚 outgoing jobs 留在本机，总负载 1。即使某节点与见证相邻，上述 incoming 身份仍由它的入边是否入见证决定。
* 每台外部颜色机器至多收到一枚 unit leaf job，负载≤1。

每枚原始 job 被安排恰一次，资格全部合法，故

    OPT ≤ 2−ceil(d/μ)/d ≤ 2−1/μ.

pin 又给 T_conf≥1，故 OPT/T_conf≤2−1/μ。

构造复杂度：每桶的 q 可用自底向上的整数 DP 计算。在正剩余高度的内部节点，q 是其 d 个孩子值的 H-index，即最大的 r，使至少 r 个孩子值≥r。仅为统一实现，对概念叶设置“在桶内则值 d，否则值 0”的 sentinel；这不是重新定义深度 0 的数学 q。存储 H-index 的见证并回溯即可得到完整 r 树。所有桶数 m≤L，每桶处理显式树及颜色标识的工作量为多项式；例如逐节点排序给 O(m(I+L)log(d+1)) 次整数比较。r、d 和负载均有显式输入多项式位长，实际全部 σ 可直接输出。没有组合优化 oracle、Haxell 算法或分数配置求解器依赖。

μ=1 时每个叶颜色不同，取 r=d，所有 jobs 下传即 C=1，与 pin 下界合并得 OPT=T_conf=1。

### S4. 逼近上界的单树显式族

固定 μ≥2，取任意 μ 的正整数倍 d，令 b=d/μ。取满足

    μ ((d−1)/d)^h ≤ 1

的整数高度 h≥1。在每个最后一层内部节点，将其 d 片叶分成 b 组，每组 μ 片。每组一个颜色；不同组以及不同最后一层父节点的颜色全部不同。于是整棵树的每色重数恰 μ，共有 L/μ 台颜色机器。

### 4.1 最大 rainbow 分叉精确为 b

每个最后一层父节点仅有 b 种颜色。因此任何完整 r 叉 rainbow 子树都有 r≤b。反向在所有上层节点任取 b 个孩子，在每个最后一层活动节点从每个颜色组取一片叶；不同最后一层节点的颜色不相交，故得到完整 b 叉 rainbow 子树。因此 q_rainbow=b。

### 4.2 全部原 jobs 的 OPT 精确为 2−1/μ

上一节的 b 叉树调度给 C=2−b/d=2−1/μ。

反设某完整实际调度的 C<2−b/d。根有 pin unit；任何有 incoming unit 的内部节点都不能保留 d−b 枚 outgoing small jobs，否则该机负载至少 1+(d−b)/d=2−b/d。因此该节点至少有 b+1 枚 outgoing jobs 向下。沿这些边递归，直到最后一层，得到一个有 incoming unit 的最后一层节点，至少 b+1 枚 leaf jobs 必须外送。然而该节点只有 b 种外部颜色，至少一台颜色机器收到两枚 unit jobs，负载 2>C，矛盾。故

    OPT = 2−b/d = 2−1/μ.

这个下界针对任意原始 σ，不预设 σ 来自子树算法。它利用的是 C<2 时同一颜色不可能容纳两枚 unit jobs。

### 4.3 CONFIG(1+1/d) 的完整有理证书

令 β=(d−1)/d，q_l=β^l，其中内部深度 l=0,…,h−1。每个深 l 内部机器有一枚 incoming unit job（l=0 是 pin）。取以下配置分布：

* 对每一枚 outgoing small job，配置“incoming unit 加这一枚 small job”，质量 q_l/d，共 d 份；各份负载 1+1/d。
* 配置“全部 d 枚 outgoing small jobs”，质量 1−q_l；负载 1。

总质量是 q_l+(1−q_l)=1，incoming unit 的边际为 q_l。任一 outgoing job 的父端边际为

    (1−q_l)+q_l/d = 1−βq_l = 1−q_(l+1).

若该 job 连向另一个内部机器，它在子端的 unit 边际正是 q_(l+1)，故总覆盖 1；pin 的根端边际为 q_0=1。若该 job 是 leaf job，它的外部 unit 边际设为 q_h。每种颜色恰有 μ 枚 leaf jobs；在该颜色机器，对每枚 leaf job 取其 unit singleton 配置质量 q_h，并取空配置质量 1−μq_h≥0。所有外部配置负载≤1，每个 leaf job 的总覆盖仍为 1。

这是真正完整机器配置 LP 的证书；不只是边负载 LP，也不把重复颜色当作不同机器。

### 4.4 配置阈值的匹配下界

T<1 时 pin 无可用配置。若 1≤T<1+1/d，内部 incoming unit 与任何一枚 small job 都不能同属配置。根 pin 覆盖 1，且根配置总质量 1，故根的所有 outgoing jobs 在根端边际为 0，必须在子端覆盖 1。递归同理，所有内部 incoming unit 都有边际 1，全部 leaf jobs 的外部 unit 边际也都为 1。

但 μ≥2 且 d≥2，T<1+1/d≤3/2<2；每台外部机器的配置至多含一枚 unit job，而其 μ 枚 leaf jobs 各要求边际 1，不可能。因此所有 T<1+1/d 的 CONFIG 都不可行。结合证书，

    T_conf = 1+1/d,
    OPT/T_conf = (2−1/μ)/(1+1/d).

### S5. 高度选择、上确界与是否取到

可显式取 h=d ceil(log_2 μ)。写 c=ceil(log_2 μ)≥1。由

    (d/(d−1))^d = (1+1/(d−1))^d ≥ 1+d/(d−1) > 2

得 β^d<1/2，故 μβ^h<μ2^(−c)≤1。这一步只给足够高度，不是最小高度公式。取任何更大 h 也成立。

对固定 μ≥2，令 d 沿 μ 的倍数趋向无穷，且每次采用上述 h。每一个输入都有限且满足整棵树重数≤μ，其比值趋向 2−1/μ。与本附节S3的全类上界合并，得到

    sup_{P∈S_μ} OPT(P)/T_conf(P) = 2−1/μ.

μ=1 的同一公式已经逐实例成立。



### S6. 显式位复杂度与否定范围

本族的 I、L 和颜色机器数是显式输出大小的一部分。全部 jobs 的有限处理时间仅 1 与 1/d，二进制位长 O(log d)。上文 CONFIG 证书在每个内部机器列 d+1 个配置，在每台颜色机器列 μ 个 singleton 加空配置；总 incidence 数多项式于显式树大小。q_l=((d−1)/d)^l 的位长 O(h log d)，对 d≥2 有 h log d=log L，所以有理证书位长也为显式输入多项式。未承诺按 log d、log h 或 log μ 生成整棵树；树本身有 d^h 片叶。不按binary d,h参数长度承诺展开整棵树。

固定 d 为 μ 的倍数后，高度可任意增加而仍保持相同 OPT 和 T_conf。这不是 Cartesian tensor 的参数变换。对 d≥2，完整树的 h≤log_2 L，因此自然处于 height O(log 显式输入) 的范围。

这给出以下限定障碍：仅以 CONFIG(1+1/d) 作为 YES 信息，不能对任意完整单树保证某个统一常数 c>0 的 rainbow cd 分叉；取 μ>1/c、d 为足够大的 μ 倍数，上述分叉仅 d/μ<cd。它也展示即使只有一个强制根，随允许重数增长仍有趋近 2 的配置间隙。

它不证明 strong (d−1)-ary rainbow 与 weak δd-ary rainbow 的 promise NP-hard，不证明一般 UM 的近 2 困难性，不排除使用源问题全局一致性或额外表示的算法。此族本身的整数最优值和一个最优 σ 都已显式给出。旧 private forest/menu 类对固定 μ 的 G(μ) 仍与本单树 S_μ 的精确上确界区分，不能将本公式直接写给旧 G。
