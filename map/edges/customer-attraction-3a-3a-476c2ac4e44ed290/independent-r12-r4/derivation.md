# R12 → R4：同一实际孩子账本与全部最优槽必要结构

任务：`customer-attraction-3a-3a-476c2ac4e44ed290`；Boss6；request `613c3e3a01c94a76bec55743d2704d92`；Boss给定remote `b4388516dbfdded9a6b91d12d1832fa9dbb8dd13`。本窄任务未独立查询远端，未操作Git/队列。

## 当前端点与实读范围

- R12：`M-b83c6050d75e4252bbe71ed2e71569e6` v2，当前登记为proved；正文《R12动态信用查询分支容量与覆盖付款义务--审查.md》全文实读，承重点为§5。只使用精确递推，不使用2394次有限检查或标量容量分式。
- R4结构目标：`customer-attraction/r4-background-candidate-transport-obstruction` v1，proved；正文《R4背景候选运输攻击--障碍.md》全文实读，承重点为“只调用实际孩子：精确坏差额”与“每个最优元组、每个槽的必要私有残块”。
- R4 IND：`M-482bb579abd84fb39d3ea98cb587b33f` v1，proved的条件引理；同页“由所有偏离孩子归纳实际得到的式子”已实读，用于严格区分另一路量词。
- 共同目录完整历史模型、固定背景剩余收益与税两定义全文实读。
- 为核对PRIVATE-LOSS静态桥，另全文实读《最优补全私有块交换与分支账本--引理.md》，只使用“不需要均衡假设的交换关系”中的EX1。其现有登记owner为`M-229d7c0b44324c27b2755e659b46d235` v2，registry明确EX1为多槽交换k=1、Y空投影。本窄任务没有实读该owner的其它主正文，不能声称完成其整体审查。
- R12所绑《背景覆盖信用的旧租金攻击与等号压力--资源.md》全文实读，只核对候选身份、递推与同一实际续局约束。
- registry另仅查看`M-21108b01d92540379cb7c7227ec6ade3` v3记录，确认其objections已记载R4 DEFECT同一映射；未实读其正文。是否已有精确canonical关系由主worker按当前registry清单去重。本地`map/edges`对三主端点ID的定向文本检索无命中，不把它解释为不存在canonical边。
- 所读文件当前SHA详见`source-freshness.json`。未读其余20 core；未运行LP、旧探针、策略树或证书重放。

## 1. 同一输入及严格映射

固定同一有限单位客户总体N、有限非空标签目录𝒮及覆盖映射、合法有序前缀h、剩余r≥1，以及同一完整纯策略σ在h后的实际路径。h可离轨，标签可重复或同覆盖，允许空覆盖、零客户。令U为h已覆盖客户，A为σ在h实际首动作，u≥0为该人的最终实际收益，Vtail为同一实际尾以后玩家最终收益，W为该路径的完整总覆盖数。令

\[
C=\max_{T\in\mathcal S^r}|U\cup\bigcup T|,\qquad
C'=\max_{Y\in\mathcal S^{r-1}}|U\cup A\cup\bigcup Y|,
\quad S=W+V^{tail}-C'.
\]

最大值在**完整共同目录**全部有序槽元组上取，不是在指定最优候选、出现过的动作或某枝的受限菜单上取。r=1时子元组为空，C′=|U∪A|。实际孩子的BG恰为S≥0；父BG恰为C≤W+u+Vtail。

R12变量逐项为

| R12 | R4同输入表达 |
|---|---|
| B | U |
| G | W−|U| |
| P | u+Vtail，仍包含旧客户上的剩余玩家利润 |
| M_r(B) | C−|U| |
| a | |A∖U|=|U∪A|−|U| |
| G′ | W−|U∪A| |
| P′ | Vtail |
| M_(r−1)(B∪A) | C′−|U∪A| |
| E_h | W+u+Vtail−C |
| E_hA | W+Vtail−C′=S |
| δ_R12=M_r(B)−a−M_(r−1)(B∪A) | C−C′=δ_R4 |

δ≥0：任一孩子的r−1槽补全与A共同构成父节点合法r槽补全，因此C′≤C。R12递推于是精确成为

\[
E_h=S+u-\delta,\qquad
C-W-u-V^{tail}=\delta-u-S.\tag{D}
\]

这一步无需SPE，也无需任何孩子BG。不能从它将E_h≥0当作已证；它只是给出待付款δ−u。即使S≥0，仍须另外支付δ−u−S。

## 2. 逐tuple、逐槽集合交换，及严格必要界

现在任取**任意**达到C的T=(T₁,…,Tᵣ)∈𝒮ʳ，并任取j∈{1,…,r}。定义

\[
O_T=\bigcup_{k=1}^rT_k,\quad
P_{T,j}=T_j\setminus\left(U\cup\bigcup_{k\ne j}T_k\right),\quad
E_{A,T}=A\setminus(U\cup O_T).
\]

P是本比较tuple的私有块，并非全目录私有客户。删除槽j，再加入A时，原覆盖恰失去P_(T,j)∖A，恰增加E_(A,T)，故有准确集合计数

\[
\left|U\cup A\cup\bigcup_{k\ne j}T_k\right|
=C+|E_{A,T}|-|P_{T,j}\setminus A|.
\]

其余r−1槽在**同一个**孩子(h,A)中可行，因而

\[
C'\ge C+|E_{A,T}|-|P_{T,j}\setminus A|,
\quad
\delta\le|P_{T,j}\setminus A|-|E_{A,T}|.\tag{X}
\]

若实际孩子BG成立S≥0，而父BG失败C>W+u+Vtail，则(D)给δ>u+S；与(X)联用得

\[
\boxed{\forall T\in\operatorname{argmax}_{\mathcal S^r}C\ \forall j:\quad
|P_{T,j}\setminus A|>u+S+|E_{A,T}|.}
\]

量词顺序是固定同一输入(h,σ,A,u,Vtail,W,C,C′,S)，然后∀最优T、∀槽j。S和δ不随T改变；E_(A,T)可以随最优并集改变。不得从不同输入或不同续局取更有利的S后与本C组合，也不能删去|E_(A,T)|后继续声称同一精确必要界。

实际上“父失败⇒严格残块界”本身不需要S≥0；该假设用于把它解释为孩子成功而父失败，并用于下述继承结论。

## 3. 空私有槽与低支持继承，包括边界

若存在一个达到C的T及一个槽j使P_(T,j)=∅，则(X)给δ≤−|E_(A,T)|≤0。与δ≥0合并，得到δ=0且E_(A,T)=∅。于是(D)给E_h=S+u≥0，父BG成立。这里只用u≥0，不需要当前人的IC，不需要其它偏离孩子BG，也不需要r≥2。

若C由k≤r−1个主题达到：k≥1时，将这些槽重复补至r槽，可选择两个同标签槽，其中至少一槽私有块为空。k=0时C=|U|；若任何合法主题有U外客户，用它并合法补槽会使C>|U|，矛盾。因此全部合法主题都包含于U，任取主题补齐r槽均有空私有块。这覆盖r=1、零支持、零客户及最优覆盖不增加的边界。

## 4. ALL最小前提及IND边界

上述完整结构定理的实质ALL依赖为：

1. R12递推/同一实际父子账本(D)，所有量严格按第1节共同输入解释；
2. 同一完整目录上父/实际孩子覆盖最大值与逐最优槽交换(X)；若列为显式数学端点，其既有owner为M-229d7c0b44324c27b2755e659b46d235的EX1投影；
3. 实际孩子BG S≥0作为目标中的条件，父失败作为必要结构部分的条件；u≥0用于空私有槽继承；有限、非空目录保证最大值和补槽。

完整SPE是目标登记的环境，但对这条集合/账本推导是较强环境：任意固定完整策略的同一实际路径已足够，收益只需非负。证明没有消费当前IC d_j≤u，因而不需要额外付任何离轨孩子BG。若把第2步直接在边explanation中完整证明，它是显示的集合桥；若想以源端点注明现有静态结果，必须由Boss按任务权限补入上述owner。不能把IND加作假前提来掩盖它与实际孩子证明的差别。

相比之下，M-482…的IND依赖**所有真实偏离孩子**(至少所有被比较最优槽动作的孩子)BG，以及当前真实IC。强制T_j后的实际尾一般不同于A枝。该孩子最优值恰为C：其它最优槽达到C，任意孩子补全又是父r槽补全。故孩子BG给

\[
C-|U|\le A_j+V_j^{tail}
=d_j+2V_j^{tail}-B_j\le u+2V_j^{tail}-B_j.
\]

只有另有某j满足2V_j^tail−B_j≤A_h+Vtail，才完成该充分SWITCH路线；标量凸混合存在则必有一个单独j成立。**实际孩子S≥0不提供所有强制孩子BG，也不能把V_j^tail或B_j换成actual值。**因此仅凭本次候选实际映射，不能声称whole_result覆盖IND整句；最多得到同一BG对象的actual-child DEFECT贡献。若另保留IND的全部孩子BG与IC条件，可另作完整条件推导，但这是不同证明分支。

## 5. 可交付范围判定

- 对目标`customer-attraction/r4-background-candidate-transport-obstruction`的**整条登记陈述**：第1–3节已完整证明“每个最优tuple每槽严格必要残块界＋存在空私有槽则继承＋≤r−1主题实现的推论”。可以写`whole_result`，必须明确第4节ALL与同一输入。条件关系可accepted；这不证明普遍BG、普遍E≥0、δ≤u或half。
- 如边只展示第1节R12↔DEFECT而未展示/调用第2节集合交换，则必须写`contribution.result = 同一实际孩子坏差额δ−u−S=−E_h`，`remaining = 全catalog逐tuple逐槽交换及空槽/低支持继承`；此时whole_result夸大。
- 对M-482…IND：当前actual-child推导只够上文所述contribution，不能给它whole_result。新增所有偏离孩子BG和IC是新的ALL条件，不能无声明混入。
- 本推导不含新的数学阻断：私有残块目标完整成立；真正未付的是由一般完整SPE保证S≥0或保证δ≤u+S。已知BG反例说明不能补成普遍背景余额非负。严格必要块也不构成父失败的充分机制或根玩家同大小收益保底。
- 当前R4正文/登记所给结构、R12递推没有在本窄范围发现需修订的数学错误。R12的标量查询容量分式并未参与此推导；不要给它虚构的付款作用。

建议边实写的完整结果句：在同一有限共同目录完整策略的合法前缀h和同一实际孩子hA中，若S≥0而C>W+u+Vtail，则∀全目录最优r槽tuple T及∀j有|P_(T,j)∖A|>u+S+|E_(A,T)|；若∃一个最优tuple含空私有槽，则S≥0蕴含父BG，特别C可由≤r−1主题达到时如此。
