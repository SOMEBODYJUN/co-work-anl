# 私有完整三叉树二叉彩虹子树：作者证明冻结

绑定 Exact SHA256 `3264ae3c3a2100fe0ef50aff1a729f9282346dba45059e20f9dcdc28d739563d`，Candidate ID `UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1`。作者 pcsp_occurrence 在发 Exact 前已有本构造，不称作者盲审；本证明在收到审查者任何本次证明前冻结。未改clone、不登记Work，不声称near2、实现或新颖性。

## 1. 一种中间的彩色 AND/OR 表达式

给标准3CNF Φ，m≥1个clauses，n≥1个variables，每个clause恰3个literal occurrences。每个occurrence (j,l)给一个独有颜色c_{j,l}，即使同一literal重复也用不同ID。

一个彩色表达式由叶atom（带一个颜色）、binary AND、binary OR组成。其“彩虹 realization”递归定义：atom选择其颜色；AND必须选两子式各一个realization且所选颜色集不交；OR恰选一个子式realization。最后要求所有选中的atom颜色互异。这是辅助语义，不是待引用的外部困难性定理。

对每变量 x_i，建立两个branch V_{i,0}、V_{i,1}。V_{i,t}为所有在 x_i=t 时取false的literal occurrence颜色的AND。该集合若空，用一个完全私有的fresh颜色atom代替（这些neutral atoms不会与任何其他颜色碰撞）。变量子式为 OR(V_{i,0},V_{i,1})。每个clause C_j的子式为 OR(c_{j,1}, OR(c_{j,2},c_{j,3}))。最后将全部n+m个变量/子句子式作AND；所有多输入AND用balanced binary tree实现。

若Φ满足，按assignment选变量branch，每clause选一个true literal。该clause颜色没有出现在所选false-occurrence variable bundle中，其他occurrence IDs又各不相同，故得到彩虹realization。

反之，彩虹realization给每变量恰一个truth branch、每clause恰一个occurrence。若所选clause occurrence为false，其颜色同时出现在对应变量的false bundle，形成重复；故每clause所选literal为true，Φ满足。

表达式大小O(n+m)，高度O(log(n+m+2))：各false bundle长度≤3m，用balanced AND；变量OR增加1层；clauseOR最多2层；顶层balanced AND再增加O(log(n+m))层。公式输入编码长度s≥n+m（可先删除未出现variables，且通常编码更长），这些都是s的多项式和log上界。

## 2. 三种完整三叉叶着色构件

记height0为单叶；实现中的所有公式输入构件height至少1。

### Rigid(H,S)

给H≥0及恰2^H个互异颜色组成的集合S，构造完整三叉heightH树，使其所有full binary rainbow subtrees的叶颜色集合**恰为S**，且这种subtree存在。

H0时S只有一色，直接单叶。H≥1时把S任意等分A、B，三个children分别为Rigid(H−1,A)、Rigid(H−1,B)、另一份Rigid(H−1,A)。两份A-tree的实体叶与internal nodes不同，仅颜色相同。

归纳可知每个子式rainbow binary选择的颜色集恰为A或B。选两个A-child会发生重复色，不能rainbow；选择B与任一A产生恰S。因此性质成立。Ambient树虽有3^H叶，但每个rainbow binary witness恰取2^H不同颜色。Rigid不是把同一资源复制为多个容量。

### Dead(H,c)

H≥1，完整三叉heightH，所有叶同一fresh色c。任一full binary subtree有2^H≥2叶，因此都不是rainbow。Dead只在height≥1时调用，绝不把单叶错当dead。

### Atom与内部颜色管理

颜色c的atom编成Rigid(1,{c,p})，p为fresh private颜色。每个rainbow binary witness必含原c，此外只含本atom私有padding色p。所有辅助颜色新分配且跨构件私有，只有下面OR两条guard刻意共用g。原atom c在公式不同位置的重复ID保留，不能改fresh。

## 3. AND、padding与OR的等高编译

以“抹去所有辅助颜色后恰得到原表达式realization”为归纳不变量；辅助颜色除某一个OR的两条guard共用外都不跨构件相等。每棵构件的ambient树都是完整三叉、叶在统一深度。

### AND(T,U)

先把T,U补到同一heightH≥1。新root三个children为T、U、Dead(H,c)。任何rainbow binary subtree不可选dead，故必须选T与U，要求双方实际color sets不交。辅助色私有，所以这个全局不交正好施加原realization颜色互异及已经存在的内部要求。反向若两个子realizations颜色不冲突，可取其对应rainbow witnesses，选T+U得到输出。新heightH+1。

### Pad(T,H*)

T现heightH≥1，若H<H*，用AND(T, Rigid(H,S_private))升高1，其中S_private为2^H个从未用过的私有颜色，第三child如AND为Dead。反复至H*。输出只增加私有必含padding颜色，不改变原语义，也不删除约束。每次生成的是完整三叉新height树。

### OR(T,U)

先Pad到共同heightH≥1。取fresh guard色g。分别建立G_T=Rigid(H,S_T)、G_U=Rigid(H,S_U)，其中S_T、S_U各有2^H个不同颜色，交集**恰为{g}**，其余全fresh，且g及其余guard色在T,U内均未使用。

令T'=AND(T,G_T)、U'=AND(U,G_U)，两者heightH+1，每个rainbow witness必含g。新OR root三个children为T'、U'及Rigid(H+1,S_F)，S_F全部fresh且与此前任何色不交。

选择T'和U'必重复g，故不是rainbow。任何合法binary subtree必须选fresh filler加两option之一；被选option存在当且仅当相应原T或U有rainbow realization。反向按所选option加filler即可。新heightH+2。对一个OR，g只在两option中共用，父级不会再无意使用它，因此不会给本来合法的跨表达式选择添加冲突。

## 4. 完整性、可靠性和规模

递归编译表达式，先完成所有logical子式，辅助色从全局新ID分配器生成。每个atom、AND、OR、Pad均保持第3节不变量；其中OR选项之间的共guard只用来禁同时选择，父级只接收其中一条，故全局语义精确。最终存在rainbow binary subtree当且仅当中间表达式有彩虹realization，当且仅当Φ满足。

Height满足atom=1、AND=max(H_T,H_U)+1、OR=max(H_T,H_U)+2。补高不额外超过所需max。表达式高度O(log s)，所以最终H=O(log s)，可例如取统一绝对常数C覆盖全部小s，并给H≤C log₂(s+2)。完整三叉树顶点数(3^(H+1)−1)/2=s^{O(1)}。

每个Rigid/Dead/Pad构件均实际展开成完整树；所有中间子树最终为输出某子树，复制的Rigid pattern只复制有限color IDs。即使某auxiliary集合含2^H个颜色，其规模不超过3^H树规模，仍为多项式。颜色总数≤输出叶数，均可用O(log |T|)位整数ID表示。整个构造按显式节点递归创建，时间多项式，没有implicit exponential tree或隐藏oracle。对Φ空/常数规模，可直接输出固定YES/NO实例；3SAT困难族本已可取m,n≥1。

在输入完整T中，full binary subtree的见证按active节点的两个child编号编码，大小≤|T|。核验root、深度、每active internal两children、2^h叶色互异都多项式。因此问题在NP，结合归约得NP-complete。

若YES也可能含full ternary rainbow subtree，并不妨碍q≥2 vsq=1的promise；NO始终有任意一条root-to-leaf path形成rainbow1 subtree，所以q恰1。

## 5. 所有原UM任务和完整σ的回算

P定义严格按Exact。每个internal node一台private machine，root pin time1；每树edge job在parent time1/3，若child internal则child time1，若child为leaf则对应唯一color resource time1。其他∞。Repeated叶仅共享同一resource，不合并不同jobs。

给full binary rainbow F，F选中的所有edge jobs送down；其他全部edge jobs送其parent。Root和F中的其他internal nodes各有一枚unit incoming/root pin，恰一个未选outgoing job留parent，负载4/3；F外internal node无unit incoming，其三个outgoing jobs全home，负载1；每resource最多一枚down leaf unit job，负载≤1。所有任务恰选一合法端，得到实际C≤4/3。

反之，给完整实际σ，C<5/3。每resource上有至多一枚unit job，因为两枚将负载2。Root含unit pin而active。每active internal node已含incoming unit或pin；若保留两枚small outgoing jobs，将负载≥1+2/3=5/3，所以至少两枚outgoing jobs实际down。递归按固定顺序取两枚，深度统一h，得到full binary subtree。其全部leaf unitjobs为实际σ的一个子集、resource各至多一，故叶色互异。这里私有原tree每node最多一个parent incoming，未引入ambient cycles或共享internal DAG。

任意T均可任选一条root-to-leaf path，沿path edge jobs down，其余parent。每active machine负载1+2/3=5/3，inactive internal machines负载1，只有一枚leaf job占其resource，负载1。故所有T的OPT≤5/3。NO树不能有C<5/3，结合上界得OPT=5/3。

因此承诺YES≤4/3、NO=5/3为NP-hard；只能排除比5/4更小的该类近似比，不排除任意统一2−ε。输入处理时间仅1/3或1，分母固定、各job两资格，所有机器与任务数显式poly|T|。

## 6. 范围、可能最近结果与仍缺的放大

本证明不使用Maximum Colorful Subtree或Group Steiner的其它目标定理作转移。它与标准彩色选择/forbidden-pair SAT编码相近，NP-completeness和该受限完整分叉形式是否已知未认证；不以新题名推定新颖。固定height及固定k可枚举见证，不与此h随输入增长的NP-hardness矛盾。

Hierarchical composition只会使weak subtree的叶比例(2/3)^h下降；每active node仍需2 children，不能把它说成r/k趋0的分叉promise。要达到任意δ的strong(k−1)/weak≈δk，需另一份完整归约；此稿没有给出。UM-TARGET-v1保持OPEN。
