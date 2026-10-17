# 完整三叉树的二叉彩虹子树困难性与实际调度阈值

读取目的：给“重复叶色且height随输入增长”的私有树路线一个真实NP-hard锚点，并保留全部原任务的阈值解码。它只给4/3与5/3的实际gap，比例5/4，弱于一般UM已有困难性；不回答近二主目标，也不凭NP完全名义保证新颖性或论文价值。

本页保留原无重数限制身份 `UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1`，下文另立全局重数2/3的v2精确门槛。作者先冻Exact与proof，cover仅陈述独立给另一份完整归约，再读作者proof攻击；root亲核两者、最终原P与总规模。无standing fatal，暂无实现/有限运行、外审或新颖性认证。

## Objects / Domain / Quantifiers

输入一棵显式完整 rooted ternary tree T，height h≥1，所有叶深度均h，每个internal node恰有3个children。只给叶着色：χ:L(T)→C，C为有限非空显式颜色集合；允许重复颜色，包括同一颜色多次出现在同一child subtree。内部节点无颜色约束。颜色ID用有限二进制字符串给定，总输入长度包括完整树和所有叶颜色。h可随输入增长，不是固定常数；完整树的叶数3^h，因此h=Θ(log |T|)。

full binary subtree F要求root为T的root，每个active internal node恰选T的2个children，全部F叶仍在原深度h。F rainbow当且仅当χ在其恰2^h个叶上单射。不是任意大小connected subtree、不是仅root到叶路径色异、不是所有颜色至少出现一次。

## Exact Claim

1. 判定是否存在这样的full binary rainbow subtree是NP-complete。
2. NP-hardness可由显式3SAT公式Φ作确定性多项式many-one归约。若Φ总编码长度为s≥1，输出完整三叉树满足h≤C log₂(s+2)，完整显式规模≤(s+2)^C，其中C为与Φ无关的绝对常数；Φ可满足当且仅当输出树存在full binary rainbow subtree。颜色可用多项式位长的整数ID，不使用隐式指数树、oracle或随机化。
3. 任何YES见证可按完整T大小多项式时间核验；构造不声称对YES未知输入多项式寻找见证。

等价地，q(T,χ)=max{r∈{1,2,3}: 存在rooted full r-ary rainbow subtree至深度h}满足q≥1；区分q≥2与q=1是NP-hard。这个合同只到k=3、strong k−1=2、weak r=2的可行性，不是任意δ的near2 soundness，不由(2/3)^h叶比例下降推导uniform branching gap。

## 明确的原UM矩阵推论（非主目标突破）

由该树按以下明确规则给出全部P。机器为每个internal node一台私有机器，以及每个实际颜色c一台resource machine R_c；所有这些机器互异。任务如下：

- root pin一枚，只能在root internal machine执行，time1。
- 每条parent到internal-child的树边一枚job，在parent端time1/3，在child端time1，其余∞。
- 每条parent到leaf ℓ的树边一枚job，在parent端time1/3，在R_{χ(ℓ)}端time1，其余∞。

每job至少一条finite边，无其它任务/预载，有限时间均为1/3或1；重复颜色的leaf jobs仍为不同任务，只是它们共享同一resource machine。

此P在树有binary rainbow subtree时存在具体Cmax≤4/3调度；若树无binary rainbow subtree，则真实OPT=5/3。对所有树均有具体Cmax≤5/3调度。给定实际Cmax<5/3完整调度，可确定性多项式提取binary rainbow subtree。因此该特定私有noninjective、输入增长height类上的(4/3,5/3) promise具有NP-hardness，所给间隙比仅5/4，弱于一般UM既有常数困难性；不宣称原创或一般near2困难性。

## Dependencies / Evidence / Scope / Status

依赖标准3SAT的NP-completeness。完整归约、颜色重复的局部逻辑、equal-height补齐及总规模已由陈述先行独立重构及全文读后攻击；本陈述不引用Maximum Colorful Subtree或Group Steiner的不同目标困难性作替代。

暂未做实现、有限枚举或运行声明。新颖性未认证。若后续改k、strong/weak branching、叶颜色量词或P的处理时间，则另立精确版本，不能以此已核k3可行性替代。UM-TARGET-v1保持OPEN。


## 完整归约与原矩阵证明

### 1. 一种中间的彩色 AND/OR 表达式

给标准3CNF Φ，m≥1个clauses，n≥1个variables，每个clause恰3个literal occurrences。每个occurrence (j,l)给一个独有颜色c_{j,l}，即使同一literal重复也用不同ID。

一个彩色表达式由叶atom（带一个颜色）、binary AND、binary OR组成。其“彩虹 realization”递归定义：atom选择其颜色；AND必须选两子式各一个realization且所选颜色集不交；OR恰选一个子式realization。最后要求所有选中的atom颜色互异。这是辅助语义，不是待引用的外部困难性定理。

对每变量 x_i，建立两个branch V_{i,0}、V_{i,1}。V_{i,t}为所有在 x_i=t 时取false的literal occurrence颜色的AND。该集合若空，用一个完全私有的fresh颜色atom代替（这些neutral atoms不会与任何其他颜色碰撞）。变量子式为 OR(V_{i,0},V_{i,1})。每个clause C_j的子式为 OR(c_{j,1}, OR(c_{j,2},c_{j,3}))。最后将全部n+m个变量/子句子式作AND；所有多输入AND用balanced binary tree实现。

若Φ满足，按assignment选变量branch，每clause选一个true literal。该clause颜色没有出现在所选false-occurrence variable bundle中，其他occurrence IDs又各不相同，故得到彩虹realization。

反之，彩虹realization给每变量恰一个truth branch、每clause恰一个occurrence。若所选clause occurrence为false，其颜色同时出现在对应变量的false bundle，形成重复；故每clause所选literal为true，Φ满足。

表达式大小O(n+m)，高度O(log(n+m+2))：各false bundle长度≤3m，用balanced AND；变量OR增加1层；clauseOR最多2层；顶层balanced AND再增加O(log(n+m))层。公式输入编码长度s≥n+m（可先删除未出现variables，且通常编码更长），这些都是s的多项式和log上界。

### 2. 三种完整三叉叶着色构件

记height0为单叶；实现中的所有公式输入构件height至少1。

### Rigid(H,S)

给H≥0及恰2^H个互异颜色组成的集合S，构造完整三叉heightH树，使其所有full binary rainbow subtrees的叶颜色集合**恰为S**，且这种subtree存在。

H0时S只有一色，直接单叶。H≥1时把S任意等分A、B，三个children分别为Rigid(H−1,A)、Rigid(H−1,B)、另一份Rigid(H−1,A)。两份A-tree的实体叶与internal nodes不同，仅颜色相同。

归纳可知每个子式rainbow binary选择的颜色集恰为A或B。选两个A-child会发生重复色，不能rainbow；选择B与任一A产生恰S。因此性质成立。Ambient树虽有3^H叶，但每个rainbow binary witness恰取2^H不同颜色。Rigid不是把同一资源复制为多个容量。

### Dead(H,c)

H≥1，完整三叉heightH，所有叶同一fresh色c。任一full binary subtree有2^H≥2叶，因此都不是rainbow。Dead只在height≥1时调用，绝不把单叶错当dead。

### Atom与内部颜色管理

颜色c的atom编成Rigid(1,{c,p})，p为fresh private颜色。每个rainbow binary witness必含原c，此外只含本atom私有padding色p。所有辅助颜色新分配且跨构件私有，只有下面OR两条guard刻意共用g。原atom c在公式不同位置的重复ID保留，不能改fresh。

### 3. AND、padding与OR的等高编译

以“抹去所有辅助颜色后恰得到原表达式realization”为归纳不变量；辅助颜色除某一个OR的两条guard共用外都不跨构件相等。每棵构件的ambient树都是完整三叉、叶在统一深度。

### AND(T,U)

先把T,U补到同一heightH≥1。新root三个children为T、U、Dead(H,c)。任何rainbow binary subtree不可选dead，故必须选T与U，要求双方实际color sets不交。辅助色私有，所以这个全局不交正好施加原realization颜色互异及已经存在的内部要求。反向若两个子realizations颜色不冲突，可取其对应rainbow witnesses，选T+U得到输出。新heightH+1。

### Pad(T,H*)

T现heightH≥1，若H<H*，用AND(T, Rigid(H,S_private))升高1，其中S_private为2^H个从未用过的私有颜色，第三child如AND为Dead。反复至H*。输出只增加私有必含padding颜色，不改变原语义，也不删除约束。每次生成的是完整三叉新height树。

### OR(T,U)

先Pad到共同heightH≥1。取fresh guard色g。分别建立G_T=Rigid(H,S_T)、G_U=Rigid(H,S_U)，其中S_T、S_U各有2^H个不同颜色，交集**恰为{g}**，其余全fresh，且g及其余guard色在T,U内均未使用。

令T'=AND(T,G_T)、U'=AND(U,G_U)，两者heightH+1，每个rainbow witness必含g。新OR root三个children为T'、U'及Rigid(H+1,S_F)，S_F全部fresh且与此前任何色不交。

选择T'和U'必重复g，故不是rainbow。任何合法binary subtree必须选fresh filler加两option之一；被选option存在当且仅当相应原T或U有rainbow realization。反向按所选option加filler即可。新heightH+2。对一个OR，g只在两option中共用，父级不会再无意使用它，因此不会给本来合法的跨表达式选择添加冲突。

### 4. 完整性、可靠性和规模

递归编译表达式，先完成所有logical子式，辅助色从全局新ID分配器生成。每个atom、AND、OR、Pad均保持第3节不变量；其中OR选项之间的共guard只用来禁同时选择，父级只接收其中一条，故全局语义精确。最终存在rainbow binary subtree当且仅当中间表达式有彩虹realization，当且仅当Φ满足。

Height满足atom=1、AND=max(H_T,H_U)+1、OR=max(H_T,H_U)+2。补高不额外超过所需max。表达式高度O(log s)，所以最终H=O(log s)，可例如取统一绝对常数C覆盖全部小s，并给H≤C log₂(s+2)。完整三叉树顶点数(3^(H+1)−1)/2=s^{O(1)}。

每个Rigid/Dead/Pad构件均实际展开成完整树；所有中间子树最终为输出某子树，复制的Rigid pattern只复制有限color IDs。即使某auxiliary集合含2^H个颜色，其规模不超过3^H树规模，仍为多项式。颜色总数≤输出叶数，均可用O(log |T|)位整数ID表示。整个构造按显式节点递归创建，时间多项式，没有implicit exponential tree或隐藏oracle。对Φ空/常数规模，可直接输出固定YES/NO实例；3SAT困难族本已可取m,n≥1。

在输入完整T中，full binary subtree的见证按active节点的两个child编号编码，大小≤|T|。核验root、深度、每active internal两children、2^h叶色互异都多项式。因此问题在NP，结合归约得NP-complete。

若YES也可能含full ternary rainbow subtree，并不妨碍q≥2 vsq=1的promise；NO始终有任意一条root-to-leaf path形成rainbow1 subtree，所以q恰1。

### 5. 所有原UM任务和完整σ的回算

P定义严格按Exact。每个internal node一台private machine，root pin time1；每树edge job在parent time1/3，若child internal则child time1，若child为leaf则对应唯一color resource time1。其他∞。Repeated叶仅共享同一resource，不合并不同jobs。

给full binary rainbow F，F选中的所有edge jobs送down；其他全部edge jobs送其parent。Root和F中的其他internal nodes各有一枚unit incoming/root pin，恰一个未选outgoing job留parent，负载4/3；F外internal node无unit incoming，其三个outgoing jobs全home，负载1；每resource最多一枚down leaf unit job，负载≤1。所有任务恰选一合法端，得到实际C≤4/3。

反之，给完整实际σ，C<5/3。每resource上有至多一枚unit job，因为两枚将负载2。Root含unit pin而active。每active internal node已含incoming unit或pin；若保留两枚small outgoing jobs，将负载≥1+2/3=5/3，所以至少两枚outgoing jobs实际down。递归按固定顺序取两枚，深度统一h，得到full binary subtree。其全部leaf unitjobs为实际σ的一个子集、resource各至多一，故叶色互异。这里私有原tree每node最多一个parent incoming，未引入ambient cycles或共享internal DAG。

任意T均可任选一条root-to-leaf path，沿path edge jobs down，其余parent。每active machine负载1+2/3=5/3，inactive internal machines负载1，只有一枚leaf job占其resource，负载1。故所有T的OPT≤5/3。NO树不能有C<5/3，结合上界得OPT=5/3。

因此承诺YES≤4/3、NO=5/3为NP-hard；只能排除比5/4更小的该类近似比，不排除任意统一2−ε。输入处理时间仅1/3或1，分母固定、每job至多两资格（root pin只有一个finite端，其余各两个），所有机器与任务数显式poly|T|。

### 6. 范围、可能最近结果与仍缺的放大

本证明不使用Maximum Colorful Subtree或Group Steiner的其它目标定理作转移。它与标准彩色选择/forbidden-pair SAT编码相近，NP-completeness和该受限完整分叉形式是否已知未认证；不以新题名推定新颖。固定height及固定k可枚举见证，不与此h随输入增长的NP-hardness矛盾。

Hierarchical composition只会使weak subtree的叶比例(2/3)^h下降；每active node仍需2 children，不能把它说成r/k趋0的分叉promise。要达到任意δ的strong(k−1)/weak≈δk，需另一份完整归约；此稿没有给出。UM-TARGET-v1保持OPEN。


## 外部源、已有结果与放大义务

只导入标准3SAT的NP-completeness。root实际打开已登记Karp1972的2010reprint，渲染并目读PDF14/MainTheorem和PDF15/item11（原印94–95）：源为每clause至多3 literals的SAT；非空短clause可重复literal补成3个positions，空clause与空合取分别映固定NO/YES，按实际出现的binary变量ID重新编号。没有声称重构Karp全文归约，没有新复制原PDF。

本文的中间彩色AND/OR表达式、Rigid固定palette、Dead、共guard选择和Pad/完整高度证明均在上文自足给出。它与标准false-occurrence SAT颜色编码相近；没有从Minimum Rainbow Subgraph、凸重着色或Steiner的其它目标困难性直接转移。没有找到/认证精确本形式的全球新颖性，不能以搜索未命中称原创。

这不与[私有注入结构界](private_injective_tree_configuration_floor.md)冲突：原状态允许重复色，YES是≤4/3而非≤1，NO恰5/3而非>5/3。注入类CONFIGgap与非注入严格(1,5/3)判定均没有被此反驳。

还缺的主义务是对每个固定δ>0给largek强(k−1)彩虹分叉与无δk弱分叉的真实源，或另一份完整near2调度归约。递归提高height只降低叶比例，不自动降低每active节点必须保留的children比例；给OR堆大量fresh fillers会让弱树只走fillers，不能据此放大。局部门的strong-witness交集/二色分叉障碍也不能被color同名技巧免费消去。UM-TARGET-v1正反面保持OPEN。


## UM-PRIVATE-TERNARY-RAINBOW-MULTIPLICITY-THRESHOLD-v2：全局叶色重数的精确复杂性门槛

仅陈述先行独立重构及全文读后攻击已完成，无standingfatal。此为新域/量词，不倒改旧v1字节；全部辅助色纳入全局≤3计数。

对象仍为显式完整三叉rooted树T，高h≥1，全部叶深h，每internal恰3children；显式叶颜色χ，binary颜色ID可重复。满binary子树含原root，每active internal恰2children，叶仍深h；rainbow指所选全部叶颜色单射。现在以整个输入T为单位限制每个颜色的实际全局出现次数，不是只在选中见证或某局部子树计数。

精确结论：

1. 若每个颜色在整个T出现至多2次，则对任意h，必存在满binary rainbow子树。该项为存在性，不先声称已实现一般多项式寻找程序。
2. 即使每个颜色在整个T出现至多3次，判定是否存在满binary rainbow子树仍NP-complete。存在从所有显式3SAT公式Φ的确定性many-one位多项式归约，SAT iff输出tree有该子树；对输入长s，输出h≤Clog₂(s+2)、完整树与颜色编码长≤(s+2)^C，C为与Φ无关的绝对常数。每个原色或辅助色都须满足≤3，不能把高重数控制色视为不计数的别名。空/常量输入合法映射，短clause与binary变量ID正确处理。
3. 两项共同给这一叶重数上界的精确复杂性边界：上界2时所有输入YES，上界3时NP完全。若要说无poly判定器另用P≠NP；NP-completeness本身是归约/成员结论。
4. 按v1相同完整普通P（internal私有；单端time1 root pin；每tree-edge job父端1/3、唯一child或叶颜色外机time1；其余∞）转换，YES actualOPT≤4/3，NO actualOPT=5/3，任意<5/3实际σ可poly提取binary rainbow。第2项中每个外颜色resource的eligible leaf jobs总数至多3，每个非pin job恰两端，pin单端。仍只是5/4比值，不是near2困难性。

依赖可用标准3SAT NP-completeness及既有raw叶q子可加性；新的全局重数3归约必须重证，不能引用旧Rigid/Dead的无限重数模板。无实现/有限运行、外审、新颖性或独立论文价值认证。结构性sharp门槛不等于UM-TARGET-v1一般正反解答。


### 完整证明

1. 重数2全部YES

把同色至多两个occurrences分别放入叶类A、B；每类本身rainbow，允许空类。已证raw q对子集并子可加，q(L)=3，所以3≤q(A)+q(B)。整数性保证至少一个类q≥2，其满二叉子树自然rainbow。任意height均有效，不借固定height枚举。q子可加性可独立按height归纳：若Q=q(A∪B)>q(A)+q(B)=a+b，在支持Q的Q个孩子中，至多a个孩子的A值>a，至多b个孩子的B值>b，故有孩子两值各≤a,b，与孩子归纳Q≤a+b矛盾。h1为叶计数。

## 2. 全局重数3的dead与固定palette

修改原v1的Dead：D_H，H≥1，为完整三叉高H树；对每个深H−1的父节点，给其三个叶同一全局新色c_v，且不同父节点及不同dead构件的c_v全部不同。每色恰3次。任何满二叉高H子树在末层必选同一父节点的两个同色叶，因此没有binary rainbow。不能在H0调用dead。

固定palette构件R_H(S)，|S|=2^H，所有S内颜色不同。H0为单叶。H1设S={a,b}，三个叶(a,b,a)，必选b与一个a，任何binaryrainbow叶色恰S。若S含一个指定的protected颜色p，则在H1将它放b位，使其实际出现恰1次。H≥2时，把S等分A、B，三个children为R_(H−1)(A)、R_(H−1)(B)、全局新色的D_(H−1)。若p指定，递归传给其所在的唯一A/B子树。两个palette孩子各出现一次，dead无binaryrainbow，故任何binaryrainbow必选A与B且色集恰S；这种选择存在。每个palette颜色实际出现1或2次，protected p恰1次；所有dead辅助色恰3次。R内的dead色与S及全部其它逻辑构件颜色全局不交。

以上不是用旧(A,B,A-copy)的palette递归，该旧递归会让颜色重数随height增长。新构件上层只各用A、B一次，以dead代替重复A；最底H1仍合法，protected位置可以保证某个共享色不重复。

## 3. 不复制逻辑子式的AND/OR编译

沿用已完整证明的v1中间彩色表达式：每literal occurrence e的原色c_e出现在变量的false branch atom和其clause literal atom恰两处；空false bundle用fresh neutral atom。变量恰选truth branch、clause恰选literal，所有逻辑模块由balanced AND组合。该中间realization rainbow iff SAT。逻辑表达式是树，任何子式只被使用一次；不要把它编成共享DAG或复制子式。

Atom(c)现在编R_1({c,p})，p全局fresh，且protected c取单出现b位；于是本atom中c实际一次，p实际两次。非空短clause可重复literal补三positions，但这些positions仍给不同occurrence色；每色c_e仍在上面两atom位置各一次。所有原色在整个输出中最多2次。

AND(T,U)：先用下面Pad补到共同H≥1，新root children(T,U,D_H)。选中binaryrainbow不能走dead，必须T与U，保持原语义且不复制任何子式。Pad(T,H*)每次以AND(T,R_H(S_private))升高1，新的palette全部fresh；该次AND两输入同高，故不会互递归。Pad只增加fresh色，T本身出现一次。

OR(T,U)：先Pad到共同H≥1，取fresh guard g，分别取palette S_T,S_U，各2^H色且交集恰{g}；其它色全局fresh。用新R_H(S_T),R_H(S_U)，两份都将g指定protected，所以g分别只出现一次，总重数2。T'=AND(T,R_H(S_T))和U'=AND(U,R_H(S_U))高H+1。OR新root的第三child是R_(H+1)(S_F)，S_F全fresh。每option的每个binaryrainbow必含g，不能同时选择两option；必须fresh filler加一option，精确OR语义。全root没有复制T/U。

全局辅助色命名规则：先占住原occurrence/neutral颜色ID，再从不交namespace逐构件新分配；只有一个OR的两guard共用同一个g。每palette构件的dead部分用独占新色，不重用别的构件aux。于是逐类统计整个最终T：原occurrence c_e恰2（或≤2），neutral原atom色1，atom私有p2，每OR guard g2，每其它palette色1或2，每个dead底层色3。没有颜色超过3，所有控制色也已计入，不是别名免费复制资源。

## 4. 完整性、NP、size与原P

所有构件完整三叉、全叶同深；Atom高1，AND=max+1，OR=max+2，Pad只达max。中间表达式各false bundle及顶层AND balanced，clauseOR深≤2，故logicalheightO(log(s+2))，输出hO(log(s+2))，完整节点数(3^(h+1)−1)/2为固定多项式。R和D均显式展开，颜色数≤叶数，整数ID位长O(log|T|)。实际出现的binary变量ID可排序重编号，输入空/常量SAT直接给height1(a,b,a)YES或(a,a,a)NO；均全局重数≤3。构造时间按显式输出多项式，没有hidden exponential tree。

新R仍强制同一palette，新D仍无binaryrainbow，其余AND/OR/Pad语义与v1一一相同，因此SAT iff存在binaryrainbow。全局≤3限制在所有YES/NO输出都成立。给定binary subtree可多项式核验颜色单射，故受限问题在NP。标准3SAT源给NP-hardness，合起来是NP-complete。

转换原P完全沿v1明确矩阵，未更改times/端点；所有叶色全局≤3使每resource machine至多有3个eligible leaf jobs（仍不同原job）。Root pin单资格，其余各父1/3与唯一下端1。给binaryrainbow时activeunit+一个small=4/3、inactive原jobs父置1、外机≤1；给actualC<5/3时每active节点至少2down、每外机至多1unit，递归提取binaryrainbow；任意path给完整C5/3。因此NO恰5/3，YES≤4/3，仍只有5/4比值，非near2。

无软件实现、有限运行、新颖性、外审或独立成文价值认证。全局重数2/3的sharp复杂性边界是限定树源结果，未升级UM-TARGET-v1。


本页重数门槛针对单棵tree的整个叶色重数；配置界v3针对每完整state内重数，跨states/roots可任意共享。两种μ域不能混为同一个全局容量假设。新版仍只有5/4调度比值，未放大到near2。

## UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2：现有三叉编译族的张量与纯收缩放大失败

Exact Statement / Objects / Domain / Quantifiers：∀显式完整三叉同深h≥1树T，每末父三叶≤2色。T^[k]的同深节点为原节点有序k元组、child逐坐标、叶色有序tuple相等，d=3^k。∀k≥1，q(T^[k])≤2^k；若原T有binary rainbow则恰2^k，按原P(U)重编后YES精确OPT=2−(2/3)^k。∀完整d叉H≥1 U，OPT(P(U))=2−q(U)/d，路径全σ≤2−1/d。故任意同域NO相对YES的gap≤Gk=(2−3^(−k))/(2−(2/3)^k)，G1=5/4，严格递减趋1，不假设NO谓词经张量保持。另k≥2、k|h时，保原叶色的纯k层收缩q≤2·3^(k−1)<d−1，连YES strong(d−1)也失效。两套既存非退化SAT构件族满足末层两色；常量规范为(A,B,A) YES/(A,A,A) NO，A≠B。

Assumptions / Dependencies：无复杂度假设；明确张量/收缩及普通P定义、旧v1/v2的实际构件，不导入其它rainbow目标困难性。Scope / Conclusion：只上述操作，非所有改色/跨副本/padding/张量不可能。允许显式QP展开不改变数学gap；不按binary k承诺poly输出。Evidence / Counterevidence / Status：先v1陈述独立重构找到常量/高度域缺口，另冻v2关闭，再实际读后攻击；root核全部P与代数。作者讨论段NP包含方向已改为NP⊆QP，raw冻结保留。无standing fatal，无新软件/外审/新颖性认证。Related Files：本页、对应review、六份冻结源与source_crosswalk。主目标正反面OPEN。

### T1. 对象及全机矩阵

设 U 是完整 d 叉有根树，高 H>=1，d>=2，全部叶恰深 H。叶着色可重复。定义 q(U) 为最大整数 r in {1,...,d}，使存在包含原 root、每个活跃 internal 恰选 r 个原 children、所有叶仍深 H 的虹彩子树。

P(U) 的 internal machines 与颜色 resources 使用不交 namespace。每个 internal node 一台私有机器，每个实际颜色一台 resource。root pin 一件 job，唯一 finite 端是 root，时间1。每条树边对应一件不同 job：其父端在父机器时间1/d，另一端在 internal child（或 leaf 的颜色 resource）时间1。其余资格全部无限。

这是完整普通不相关调度矩阵；每件 job 都有 finite 端，pin 单端，其它双端。共有 1+树边数 件 jobs，internal 数加实际颜色数台 machines。下端不是可以随意改目的地的抽象 token。时间1/d、1具有明确有限有理位编码。

### T2. 一般恒等式 OPT(P(U))=2-q(U)/d

### 给定虹彩子树的完整调度

取任意 full r 虹彩子树 F。F 中选中的边 jobs 全送其真实下端，其它边 jobs 全放其真实 parent；root pin 放 root。

- F 的每个活跃 internal（root 含 pin；其它活跃节点含来自其父的下送 job）恰接一枚 unit，并保留 d-r 枚 outgoing small，负载 1+(d-r)/d=2-r/d。
- F 外的 internal 无 unit incoming，全部 d 枚原 outgoing jobs 父置，总负载1。
- 每颜色 resource 只接 F 的 leaf-edge unit jobs；虹彩性保证至多一枚，负载<=1。

每件原 job 恰一次，所有原 machines 的总负载都已核。因 r<=d，2-r/d>=1；所以实际 C<=2-r/d。取 r=q(U) 得上界。

### 任意低负载实际调度提取子树

任意实际调度 C>=2 已自动满足 C>=2-q(U)/d，故只看 C<2。root pin 强制 C>=1。每颜色 resource 不可能接两枚 unit。

令 r=ceil(d(2-C))，则 1<=r<=d。任何接了一枚 unit 的活跃 internal，其 outgoing small 若有 t 枚留 parent，则 1+t/d<=C，故 t<=floor(d(C-1))，至少有

    d-floor(d(C-1)) = ceil(d(2-C)) = r

枚原 outgoing jobs 真正下送。root 因 pin 活跃；任取其中 r 枚下送边，遇 internal child 它就因这一真实 unit 活跃，继续任取 r 枚下送边。深度 H 后获得 rooted full r 子树。选中 leaf jobs 都按原实际调度去其颜色 resource，每资源最多一枚，所以该子树虹彩。

于是 q(U)>=ceil(d(2-C))>=d(2-C)，即 C>=2-q(U)/d。结合上界得到恒等式，含等号边界，不偷用严格小于代替小于等于。给定实际低负载 sigma 的提取、给定具体 F 的全任务回填均按显式树遍历与原负载核算，多项式位时间；本恒等式不把求最优 q 当作免费算法。

任意 root-to-leaf path 本身是 full 1 子树且只有一片叶，必虹彩。因此对所有 U 都有完整实际调度 C<=2-1/d，且其全部未选 jobs 仍按上述规则回填。此路径上界不需要任何源 YES/NO 或分数可行性假设。

### T3. 实际 v1/v2 编译族的末层不变量

性质 B：每个深 h-1 的原父节点，其三个直接叶 children 至多两种颜色。

v1 Rigid(H,S) 在 H=1 时的三叶正是 `(a,b,a)`；所有更高 Rigid 的末层属于递归 Rigid(1) 星。v1 Dead(H,c) 全叶同色，故末层一色。Atom 明确使用 Rigid(1)，不把裸 height0 atom 当公式构件。

v2 的 R_1(S) 也正是 `(a,b,a)`，protected 色只是选择 b 位，不改变“两色”；D_H 在每个末层星中三叶同色，星与星的颜色不同不影响 B。更高 R_H 的末层来自 R_1 或 D_1，故 B 保持。

两套编译器的 AND、OR、Pad 均只拼接高度至少1的已有 logical/palette/dead 子树，并在上方加 internal root；不会新建一个由来自不同构件的 height0 叶直接混合而成的末层星。按构造归纳，所有非退化公式输出均满足 B。

旧v1未指定固定常量的着色；旧v2已明确相应height1实例。为统一两套规范输出，因此这里明确选择 h=1 的 `(A,B,A)` 常量 YES（q=2）和 `(A,A,A)` 常量 NO（q=1），使这两个合法固定输出同样满足 B。此规范不影响 any nontrivial 3SAT 归约、size 或语义。不能倒称任意合法常量 YES 都满足 B，例如 `(A,B,C)` 明显不是。

### T4. 对齐 Cartesian 张量的精确上界与 YES 等式

设 T 满足 B，完整三叉高 h>=1。T^[k] 在每个深 ell 的节点是 T 深 ell 节点的有序 k 元组；孩子逐坐标选择原 children，故共同度 d=3^k，深度仍 h。叶色为有序原颜色 tuple，用可自定界编码，颜色相等当且仅当所有坐标均相等，不使用有碰撞 hash。

取任一张量末层父节点 `(u_1,...,u_k)`，每个原 u_i 的直接叶色集合 C_i 至多2。该张量父节点全部 children 的颜色集合恰为 C_1×...×C_k，大小至多2^k。任意 full r 虹彩子树至少含一个活跃末层父节点；该节点选中的 r 个叶颜色也必须互异。因此

    q(T^[k]) <= 2^k.

若 q(T)>=2，取 T 中一棵实际 full binary rainbow F。每坐标都限制在 F，逐节点取这 k 个 binary child 选择的 Cartesian product，获得 T^[k] 中 full 2^k 叉子树。任意两个不同的叶元组至少在某坐标的原 F 叶不同；F 的该坐标叶色互异，故 tuple 颜色不同。此乘积见证真虹彩。

于是 q(T^[k])>=2^k，结合局部调色板上界恰等2^k。应用本附节T2：

    OPT(P(T^[k])) = 2 - 2^k/3^k = 2-(2/3)^k.

这不是仅承诺一份较弱 YES 调度，而是本输入族的实际精确 OPT。k>=2 时 2^k<3^k-1，所以这些 YES 输入本身没有 full(d-1) 虹彩子树。这个原因已先于任何 NO 解码失败。

### T5. 实际 gap 上界 G_k 严格递减

对任意上述 YES base tree，其张量普通 P 的 OPT 同为 A_k=2-(2/3)^k。NO 一侧甚至不需要保留原二叉谓词；对任意同域 base tree 张量，由本附节T2路径构造，实际 OPT<=B_k=2-3^(-k)。所以任何意图赋予本操作 YES/NO 值 gap 的实际比率至多

    G_k = B_k/A_k = (2*3^k-1)/(2*3^k-2^k).

没有使用未证明的 NO soundness，也没有把叶数比例当逐层分叉。令 A=3^k，B=2^k。两个分母均正，直接通分：

    G_k-G_(k+1)
      = [2*A*(B-2)+B] / [(2*A-B)*(6*A-2*B)] > 0,

因为 k>=1 时 B>=2 且 B>0。故 G_k 对所有整数 k>=1 严格递减。G_1=(5/3)/(4/3)=5/4，因此 G_k<=5/4；又 `(2/3)^k` 与 `3^(-k)` 均趋0，G_k趋1。

数值 sanity：G_1=5/4，G_2=17/14，G_3=53/46；这是“任意 NO 最强”的上包络，不与特定小例 NO 的实际 gap 混淆。已用 Fraction 对 k=1,...,30 反算上述精确通分恒等式及严格性，有限回算只查代数排印，非一般证明来源。

### T6. 纯 k 层收缩的独立完备性障碍

现在 k>=2 且 k 整除 h。把原深0,k,2k,...,h 的节点保留为 macro 节点，原 k 步后代连为 macro children；不改任何原叶颜色。新共同度 d=3^k，高 h/k>=1。这里随后按 P 定义重编 macro-tree 的普通调度；不是声称原 physical P 的内部 jobs/资格原封保存。

每个末层 macro-parent 对应一个原完整 height-k 子树。它含3^(k-1)个原末层三叶星，每星颜色数<=2。因此该 macro-parent 的全部原叶（即新直接 children）合计至多

    2*3^(k-1) = (2/3)d

种颜色。任意虹彩 full r macro 子树在活跃的某个末层 macro-parent 必选 r 种不同色，所以

    q(contract_k(T)) <= 2*3^(k-1) < 3^k-1 = d-1.

严格不等式来自 3^(k-1)>1。它对 SAT/YES 输出同样成立，因此该纯收缩连所需 strong(d-1) 完备性都达不到。k=1 只给2=d-1，不声称该边界也被排除。若 h 不整除 k、最后层不等长、再补节点或改色，就不是本条定义的纯收缩，必须重新检查实际对象。

### T7. 显式规模、复杂性条件和不外推

T^[k] 的第 ell 层有3^(k*ell)个节点；总数为 `(3^(k(h+1))-1)/(3^k-1)`。完整输入必须实际展开，颜色 tuple 也是实际记录；没有按 binary k 的原编码长度承诺多项式输出。若原 SAT 编译树大小 n^{O(1)}，取 k=O(log n)，张量大小至多 n^{O(log n)}，所以允许准多项式归约是合理的规模范围。

但是数学上对每个有限 k 的 YES 精确 OPT 与 G_k 上界均已成立；允许这种更大展开不会把 G_k 从<=5/4变到近2，反而 k 增大时趋1。不存在可在此处援引 NP不包含于QP 来弥补的 gap：只有已经证明的准多项式 gap 归约，加上假定多项式近似算法，只能导出 NP⊆QP（相应排除假设为NP⊄QP）；这个复杂度假设不能替代缺失的 gap。

纯收缩保留全部原叶，macro 树规模不超过原树，h>=k 且 d=3^k 已显式受原叶数约束；颜色位编码未变。

结论严格限于末层两色前提下，tuple-equality 的对齐 Cartesian 张量及保叶色的等长纯收缩。它不排除重新设计跨副本颜色约束、非对齐变换、改变时间/任务接口、加入其它状态或 padding 的新机制；也没有证明所有 rainbow-tree gap amplification 不可能。一般 UM-TARGET-v1 仍 OPEN。本条只应并入旧三叉路线的精确限制，无一般算法或主困难性升级，新颖性/独立论文价值未认证。
