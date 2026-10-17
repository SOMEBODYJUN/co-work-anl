# 近单位 promise：一般源困难性、多小端边界与任务正规形

读取目的：保存已经闭合的 unrestricted PCSP 困难性，准确隔开尚未闭合的调度编译。它给一个可供主反面归约使用的源，但没有证明 UM-TARGET-v1 不成立。普通 non-delta-matroid / edge-CSP 定理不能自动补上 promise、任务出现次数和端口类型。第6–8节进一步给native多小端的流边界和保实际调度的三端单位选择器正规形；后者是主目标的等价研究语言，没有提供其求解器或近二hardness。

## 1. 精确模板与全部量词

固定整数 k≥2、1≤r≤k−1。底集均为{0,1}，三个关系名的 strict / weak 解释为

\[
 A_k(b,x_1,\ldots,x_k)\iff b=0\ \lor\ \sum_i x_i\ge k-1,
\]
\[
 B_{k,r}(b,x_1,\ldots,x_k)\iff b=0\ \lor\ \sum_i x_i\ge r,
\]

以及两端相同的 AMO₂={(0,0),(0,1),(1,0)}、ONE={1}。identity给strict模板到weak模板的同态。PCSP任务是区别全部strict约束可满足与全部weak约束不可满足的实例。

本页一般源允许任意约束图、同一变量任意多次出现、同一约束内变量重复。它没有父out/子in、DAG或每物理任务只出现两次的承诺。每个k,r分别固定，模板规模属于归约常数；未把随输入增长的truth table隐藏为常数。

f:{0,1}ⁿ→{0,1}（n≥1）是polymorphism，指对每个关系，将n个strict合法输入逐坐标应用f，结果满足对应weak关系。写F_f={S⊆[n]:f(1_S)=1}，称其为winning supports。

## 2. 精确 minion

**ID/version：UM-NEAR-UNIT-PCSP-EXACT-MINION-v1。**

**Exact Statement / Conclusion。** 对每个上述固定k,r、每个n≥1，f为该模板对的polymorphism，当且仅当：

1. f单调；F_f非空；
2. 任意两个winning supports相交（包括同一个集合与自身）；
3. 每个inclusion-minimal winning support的大小≤C=k−r。

任意一个这样的minimal winning S都是同一个双侧C-fixing set：S坐标全1强制f1，S坐标全0强制f0。r=k−1时只有projections；C≥2时可以有任意大essential arity，不能把本结论写成bounded-essential-arity。

Objects / Domain / Quantifiers / Assumptions：第1节的全部显式Boolean模板，固定k,r，所有正有限arity与全部Boolean函数；不对物理约束出现方式加假设。Definitions：单调按集合包含；minimal取全部winning supports下的inclusion-minimal。Scope：一般PCSP的精确algebra，不是调度gap。Dependencies：仅模板定义及下述自足有限证明。Evidence / Counterevidence：独立陈述重构和后读冻结证明；无新生产实现；未认证新颖性。Status与Related Files：限定证明完整，实际内审见[审查](../../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)，外审未记录。

### 必要性：三个可逐项核对的矩阵

ONE给f(1,…,1)=1。AMO₂给任意两个winning supports不能不交：否则把它们指示向量并列为二列，每行均在AMO₂，输出却为(1,1)。同理空集不能winning。

先直接核单调性。若X⊆Y、f(1_X)=1而f(1_Y)=0，把A_k的incoming列设为1_X，全部k个outgoing列都设1_Y。每个active row在所有outgoing位上都是1，所以每行strict合法；输出却为incoming1、全部outgoing0，违反r≥1的weak关系。故f单调。

若某minimal winning S大小≥k−r+1，从其中取k−r+1个不同坐标i_j。incoming列为S；前k−r+1个outgoing列分别是S\{i_j}，其余r−1列是S。每个active row最多缺一枚outgoing1，故strict合法。所有proper-subset列losing，仅余r−1枚winning输出，违反B_{k,r}。所以|S|≤k−r。

S坐标全1时，support包含S，单调性强制f1；全0时，若输出f1，其winning support将与S不交，违反AMO₂保持。因此同一S双侧fixing。

### 充分性：真正处理inactive rows

给任意n行strict合法矩阵。若其incoming列被f判0，weak蕴含自动成立。否则在incoming support中取minimal winning S，|S|≤k−r。每个S中row是active，最多缺一枚outgoing1。因此不包含整个S的outgoing列至多|S|个；至少k−|S|≥r列包含S，由单调性全winning，输出weak合法。未对S之外的inactive rows误加约束。

相交性恰给AMO₂保持；非空winning族与单调性给ONE保持。三个关系全部覆盖，iff得证。

C1时每minimal winner是singleton，相交性使其唯一，故f是一个projection。C≥2时取任意n≥2，f=x₁∧(x₂∨…∨xₙ)的minimal winners为{1,j}，rank2且相交，所有坐标均可essential；它说明strong fixing不蕴含bounded essential arity。

## 3. 一般源困难性确已闭合

**ID/version：UM-NEAR-UNIT-PCSP-UNRESTRICTED-HARDNESS-v1。**

**Exact Statement。** 对每个固定k≥2、1≤r≤k−1，第1节的PCSP为NP-hard，采用通常确定性多项式归约。该结论包括r=1。没有声明保持变量次数、物理端口或DAG。

Objects / Domain / Quantifiers：上述固定有限模板和所有一般实例。Assumptions：导入BBKO的既有NP-hardness theorem；P≠NP只在推论“无确定性多项式求解器”时需要，不是结构恒等假设。Definitions / Scope / Conclusion：promise decision hardness，不是actual makespan近似困难性或某个ρ的UM下界。Dependencies：UM-NEAR-UNIT-PCSP-EXACT-MINION-v1和下面的Paper Fact，共同前提缺一不可。

**Paper Fact。** Barto–Bulín–Krokhin–Opršal, arXiv:1811.00970v3，Definition5.16、Proposition5.17（PDF33/印33）：若Pol(A,B)有minion homomorphism进入Boolean strongly C-fixing minion、C为常数，则PCSP(A,B) NP-hard。这里strong fixing正是同一坐标集全0迫0、全1迫1。[原始PDF](../../../history/source/literature/unrelated_machines/barto_bulin_krokhin_oprsal_2019_algebraic_pcsp_v3.pdf)保留v3原字节，source定理statement及适用条件已实际核读；未声称重构其PCP全证明。不要误用v3 Proposition5.15的bounded essential arity，或旧稿不同编号。

**证明。** 第2节给C=k−r≥1，对整个Pol minion中全部arity统一。取同一minion为目标、identity为minion homomorphism，准确满足Paper Fact。有限模板、A→B以及非空fixing set条件均已核。故NP-hard。

Evidence：实际statement-first独立重构、primary theorem读取及后读冻结证明；无新软件。Counterevidence / Objections：r1一般源hard而purearc rootedDAG的r1可解，正说明有不能省去的出现方式义务，不构成矛盾。Status：限定一般源证明完整、内部攻击无standing fatal；外审、新颖性及UM编译未认证。Related Files：本页、原始PDF、[实际审查](../../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。

## 4. 普通 Feder 扇出定理不能原样保 promise

这节是精确路线失效，不另冒主目标反证。Kazda–Kolmogorov–Rolínek arXiv:1602.03124v6 Theorem7（PDF5/印0:5）转述Feder：含0/1 unary常量、普通CSP NP-hard、某relation非delta-matroid时，普通edge-CSP NP-hard。它只有一个关系族，没有strict/weak pair，也没有本题物理端口合同；Theorem8的even-delta可解也只是普通CSP。

root实际读Feder作者原始[PostScript](../../../history/source/literature/unrelated_machines/feder_fanout_limitations_author_original.ps)的Theorems3–4（印8–11）：先在ordinary setting构造clauses，再从最小可行support取三坐标；若干分支用循环不等式实现相等。循环本身并不违反一般UM的模型；若候选自加DAG限制，才另有DAG保持义务。真正首先失效的是promise。

可直接算：在A_k/B_{k,r}中pin x_k=0，保留b,y=x₁,z=x₂，存在量化其余k−3个outputs（k≥3），所得关系恰为

    strict: b=0 或 y=z=1，
    weak:   b=0 或 y+z≥max(0,r−k+3)。

active strict必须打开全部k−1枚未pin出口；weak可用被量化的k−3枚出口支付配额，公式两向都达到。r≤k−3时weak是完整Boolean cube，而strict仍non-delta：000到111的incoming flip不能由再翻一个坐标修复。故普通最小support/三坐标提取的严格non-delta见证在弱端完全失去soundness。r=k−2时weak只剩b⇒(y∨z)，r=k−1时两端相同。

这只否定把上述步骤原样移用，不否定更大promise gadget、多任务/多尺度编码或全局decoder。源文原字节/hash及实际读取页码见manifest；转换PDF仅作本地读取，不替换原PS。source定理不作为第3节困难性的额外证明前提。

## 5. 真正未解的物理编译与数量关系

对只含1与1/k的任务，在机器上把unit到达位记作in、small job离开本机记作out。若机器有k个small端，C<2时unit incoming至多1，且active机器在

    T₀=1+1/k 时至少k−1个out为1；
    C_r=2−r/k 时至少r个out为1。

inactive机器把全部small留本机也只负载1。多个incoming应在同一个machine relation中同时守AMO；不能免费再造一个可任意复用的activation变量。

三类**实际合法两端任务**必须按位语义区分：

| 原job两端时间 | 两incidences的物理关系 |
| --- | --- |
| 1/k 与 1 | out–in EQ |
| 1 与 1 | in–in NEQ（普通unit selector） |
| 1/k 与 1/k | out–out NEQ |

out–out EQ不是这里免费提供的连线。一般UM不要求ambient DAG；用DAG只是候选的一种额外结构。一个变量在unrestricted source中任意复制，仍不能据此成为一枚有两个有限端的job。

一般UM也允许任务有三个以上有限端，两端Boolean表示不是目标的限制。一个native任务可在A端耗时1、在与A互异的k个不同M_i端耗时1/k。若b表示它是否分给A，x_i表示它是否离开small端M_i，则其精确可选状态为(1,1^k)，或某个(0,1^k−e_i)。b0时并非全部x0；这提供真实one-cold多端关系，但仍只有一件任务/一次占用。全部unit端任务则给incoming one-hot。不同表示可以独立攻击，不把Boolean两次发生copy路线当方法白名单。

足够反面的一条精确义务是：对任意大固定k，把一个已NP-hard的上述source（例如r2）编译成显式普通UM，YES所有原任务C≤T₀，且任意C≤C_r实际σ均可构造源weak解，并保持全部机器同时负载、任务合法性、总位多项式规模。该义务仍未完成。不能仅验证某个label pattern或局部Boolean关系。

数量上，若此编译只用{1,1/k}，所有实际负载在1/k网格上，NO无C≤C_r会给

    OPT_NO≥2−(r−1)/k，
    OPT_NO/T₀≥(2k−r+1)/(k+1)=2−(r+1)/(k+1)。

因此如果能对任意大固定k保持r2的**物理**hardness，就足以在P≠NP下排除每个固定(2−ε)算法。该句是明确条件推论，不是已构成的归约；一般PCSP已hard不能删掉“物理”。单个固定k或固定ρ<2也不排除所有ε改善。

现有private-tree、半密度与逐行均匀资产只封闭其准确合同；没有一项证明上述三型全局编译不可能。新的承重机制仍须在实际P上闭合copy/decoder，不把可求源oracle、non-delta或LPgap冒作解码。

## 6. 多小端任务的全局流边界与真正需要的单小端瓶颈

**ID/version：UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1。** 本节不是新的近二困难性，而是对上一节native方向的完整算法核查。它比逐端one-cold语义多用真实small关联图及所有任务的共同整数流，不能从一个局部配置下界直接读出。

**Objects / Domain / Definitions。** 显式合法UM，整数k≥2，所有有限时间属于{1,1/k}。Q为没有small端的任务（故其全部有限端时间1）；R为其余任务。每j∈R的small可选机器集合为S_j、d_j=|S_j|≥1。定义

\[
 \rho_i=\sum_{j\in R:i\in S_j}1/d_j,\qquad c_i=\lceil\rho_i\rceil.
\]

B为仅安排Q时最优的每机unit任务最大数；F为仅在small端安排R时最优的每机任务最大数；对应任务集空时各值为0。两种容量均是任务数，尚未除以k。

**Exact Statement / Quantifiers / Conclusion。** 对每个上述P与二进制k，确定性总位多项式算法可输出全部原任务的实际σ，使

\[
 C_{\max}(\sigma)\le B+F/k\le B+\max_i c_i/k. \tag{6.1}
\]

若每台机器small资格关联数≤k、每j∈R有d_j≥D≥2，则

\[
 C_{\max}(\sigma)\le\left(1+\frac{\lceil k/D\rceil}{k}\right)\mathrm{OPT}
 \le\frac53\mathrm{OPT}. \tag{6.2}
\]

该算法不需要OPT或一份strict见证。若d_j≥k且每机small关联数≤k，strict阈值T₀=1+1/k可行**恰当且仅当**Q有每机至多一件的unit匹配；匹配失败则OPT≥2，成功则能直接输出T₀完整σ。

**Assumptions / Dependencies / Scope。** 只调用标准整数二部容量流。任务可以有任意多unit和small端，不把一任务拆开执行；但(6.2)需要每个非unit-only任务都有至少两个不同small端及真实行关联预算。没有涵盖only-one-small arcs、非统一small时间或超过该行预算的矩阵；不声称一般UM的新近似因子。5/3是此算法的保证，不声明该类最优因子。

### 实际构造及全部机器负载

对Q建立任务到原unit机器的二部流。机器容量为整数b时，整数满流恰为每机至多b件的合法Q分配。对b∈[0,|Q|]做整数二分可求B并回溯实际目的机器。

对R同样建立任务到原small机器的二部流。先核一个不依赖Q的共同可行证书：对每j，把一单位分数均分到其d_j个small端。任务列总量恰1，机器行总量恰ρ_i≤c_i。容量为c_i的整数流故可覆盖R；不以该分数执行任何任务，而是取整数流的一个small端。因此仅small端的最优整数瓶颈F≤max_i c_i。再对[0,|R|]的整数机器容量做二分，可求最小F及其实际分配。

Q与R互不相交，叠加两个整数分配。逐机unit任务数≤B、small任务数≤F，实际总负载≤B+F/k；所有机器、包括无unit与未用机器同时满足。R原来可能有unit选项，这个构造全部忽略；不存在一任务既按unit又按small重复计入。

### 不知道OPT时的全部分支

若Q非空，则B≥1，任何原调度中的Q仍只能走unit端，所以OPT≥B。因而(6.1)给

\[
 \frac{C_{\max}(\sigma)}{\mathrm{OPT}}
 \le1+\frac{F}{kB}\le1+\frac{F}{k}.
\]

若每机small关联数≤k且d_j≥D，则ρ_i≤k/D，故F≤ceil(k/D)。k≥2、D≥2给ceil(k/D)<k，以及

\[
 \frac{\lceil k/D\rceil}{k}\le\frac23.
\]

最后不等式中k2为1/2，k3为2/3，偶k≥4至多1/2，奇k≥5为1/2+1/(2k)≤3/5。因此得到(6.2)。

若Q为空且F/k<1，构造本身给OPT≤F/k<1。任何使用unit端的实际调度负载≥1，故最优调度全部走small端；由F的定义，这时输出恰是最优。若所有任务都空，则B=F=0、返回空调度，OPT=0。R为空时只有Q流，算法也精确。因所有有限时间正，本限定域不存在非空任务OPT0；一般UM的零时间输入不在本节改写范围内。

### balanced native 的 strict iff 与近二NO的必要局部形状

当d_j≥k且small行关联数≤k时ρ_i≤1，所以F≤1。若Q有unit匹配，即B≤1，则(6.1)给≤1+1/k的完整调度。反之任一C≤1+1/k<2的实际调度在每机至多一件Q，故Q匹配必要；匹配失败时每个实际调度必有某机至少两件Q，OPT≥2。这是在完整原P上的可判定iff，不依赖隐藏源赋值。

再给一般{1,1/k}、small行关联数≤k的一个直接推论，不额外假设d_j≥2。设Q的unit匹配存在，r为整数1≤r≤k−1。若某实际NO满足OPT>2−r/k，则必有一台机器i使ρ_i>k−r，否则容量c_i≤k−r的small流与unit匹配会直接产生≤2−r/k调度。于是该机器满足

\[
 \sum_{j:i\in S_j}(1-1/d_j)
   = |\{j:i\in S_j\}|-\rho_i <r.
\]

每个d_j≥2的small incidence贡献至少1/2，故该机器的这类incidences**少于2r个**，并且总small关联数至少k−r+1。若a为one-small数、b为multi-small数，则ρ_i≤a+b/2且b≤2r−1，推出a≥k−2r+1。r2时，这一瓶颈机器至多有三枚multi-small incidence、至少k−3枚one-small incidence（下界为负时当然只取无信息）。结论只要求至少存在这一台机器，不声称每台机器都有此形状；若Q匹配失败，则首先已有多项式可检测的unit障碍。

因此全native one-unit+k-small的对称编译已经落入易解合同；要继续该nearunit反面方向，真实承重必须保留足够one-small传播，或突破小时间/行关联预算等假设。这仍未排除一般多端、混合多尺度或全局decoder。

### 总位复杂度、证据与认证

所有二部网络仅含原输入的显式有限边；机器容量可截到任务数。B、F的二分次数O(log(n+1))，不是按k或处理时间数值循环。每个d_j≤m为显式计数，ρ_i的分母可取相关d_j之积，其总位长≤Σ_j log d_j，按原输入长度多项式；也可完全不计算ρ而仅用B、F流求实际输出，ρ只用于保证分析。实际σ只写一个原机器编号/任务，负载有理回算位长多项式。

Evidence / Counterevidence / Status / Related Files：标准Hall/整数流的直接推论，非新匹配定理；未认证全球新颖性或独立论文价值。没有新的通用流软件实现，也没有用有限测试代替本证明。精确陈述、独立重构及后读本节的实际范围见[审查](../../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。本新增算法不依赖第2–3节一般PCSP困难性；主目标正反面仍OPEN。

## 7. 三端单位选择器：保实际调度的全输入阈值正规形

**ID/version：UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1。** 本节不再把native多端当作免费copy。相反，任意任务的多选项可用单位容量的一个OR选择器精确表示；它只负责选一个原端，不制造多份原任务。

**Objects / Domain / Quantifiers。** 任意显式合法UM矩阵P，m≥1、n≥0，给正二进制有理b；本节输入的每条有限p_ij≤b，允许零。令E为全部有限资格。正规类随输入给出b：每个任务要么恰两有限端，一端q∈[0,b)、另一端b；要么有1至3有限端且时间全部为b。两端机器互异，原模型一行一列只有一个时间。

**Exact Statement / Conclusion。** 确定性总位多项式可构造属于此类的N_b(P)，保留原机器副本，新增O(|E|)机器、任务和有限资格，并有两个构造映射：

- 任意原实际完整σ可映为新实际完整τ，C_max(τ)≤max{b,C_max(σ)}。
- 任意新实际完整τ且C_max(τ)<2b，可映为原实际完整σ；逐台原机器的负载不超过τ在该原机器副本的负载，故C_max(σ)≤C_max(τ)。

若原有限时间仅{b/k,b}、整数k≥2，则新时间仍仅这两值；每台原机器small资格数逐条保持，所有新增机器small资格数为0。每个新small任务恰为small–unit两端；unit-only任务至多三端。k可二进制很大，构造不循环k。

**Assumptions / Definitions / Dependencies / Scope。** 仅标准有限树/单位容量计数，无源困难性定理或配置LP。b是给定阈值，不是隐藏OPT；一般P按b测试时须先删p>b的资格，若某任务无剩余边则可靠判OPT>b，而不是对无资格输入调用本构造。没有声称C≥2b时仍可解码；新OPT在两端截断，而非始终等于原OPT。路径容量选择器/单位匹配是标准机制，本页重构实际双向负载合同，全球新颖性未认证。

### 每个原任务的一棵私有二叉单位树

固定原任务j，把它的d≥1个不同有限机器选项按编号列成i₁,…,i_d。建立一棵叶子恰d个、每内部点有两个孩子的满二叉树，每个点是一台新私有机器。可用固定的comb或平衡树，所有点显式生成。叶t对应原选项i_t。该构件新增：

1. 一枚只在根执行、时间b的unit pin；
2. 每内部点v一枚unit job，在v及其两个孩子均耗时b；
3. 每叶t一枚port job，在该叶耗时b，在原机i_t耗时p_{i_tj}。

不同原任务的全部新机器、任务互异，只在原机器上共同负载。内部unit job正是三端one-hot，不能当两次发生的Boolean NEQ连线。

一棵d叶满二叉树有2d−1点、d−1内部点，因此构件有2d−1新机器、2d新任务、5d−2有限端。d1也按同一定义：根即叶，有一个pin及一枚port，没有内部unit job。p=b时port为两端unit-only，p<b时port为small–unit；零p允许。故所有新任务都属于正规类。

### 前向映射：沿原所选叶运输一枚单位占位

给原σ，j选择原选项s。pin放根；沿根到叶s的路径，每个内部unit job送到路径中的下一孩子。路径外的内部unit job留自身；port s送原机i_s，其它ports留各自叶。

每台新私有机器恰接一件unit任务：根接pin，路径其余点接父unit，路径外内部点接自己的unit，路径外叶接自己的port；选中叶接父unit而其port已送原机。d1同样由pin占根、port送原端。因此全部新私有负载为b。原机器上的各任务只换成同处理时间的一枚所选port，逐机原负载完全保持。全部新任务恰一合法目的地，得到所述max{b,C_max(σ)}界。空任务时没有新构件，原m≥1保留。

### 反向映射：任意低负载实际τ都必须外送一枚port

给τ且C_max(τ)<2b。每台私有机器上的任务处理时间都是b，故最多接一件构件任务。一个j构件有2d件任务，仅有2d−1台私有机器；pin与内部jobs都不能去原机器，所以至少一枚port实际上在其原选项机器执行。可沿root占位逐点查找，也可直接扫描实际port目的地，任选编号最小的外送port，将原任务j放到对应原机。

对每个原j恰选一枚在τ中已经执行的原端port；不同j的port是不同任务。逐台原机器，恢复负载是τ该机port负载的非负子和，因而不增。它允许τ曾外送多枚同构件ports，未假设τ只有一条规范路径；也未要求τ来自某个预选label。所有原任务均恢复且全机同时受控。

### 非空输入的精确截断最优值

同一构造另满足一个直接恒等式：原n≥1时

\[
 \mathrm{OPT}(N_b(P))
 =\min\{2b,\max\{b,\mathrm{OPT}(P)\}\}. \tag{7.1}
\]

所有新pin迫最优值≥b。除前向映射外，还有一个完全不使用原机器的≤2b分配：pin放根、每内部job留自身、每port留自身叶，只有根可能收到两枚unit。若新最优值小于右侧，则它严格小于2b，可以反向恢复原调度；结合新值≥b会与右侧定义矛盾。因此上下界相等。原n0时无构件，两边新旧OPT均0，必须单列，不套(7.1)。特别原OPT∈[b,2b]时精确保持，阈值1≤C/b<2的YES/NO gap没有损失。

### 规模、位长与使用边界

总新机器数2|E|−n，总新任务数2|E|，有限端数5|E|−2n，另保留m个原机器。只复制原p与给定b，没有新大数或按分母展开；完整含∞矩阵仍为多项式大小。生成树、映射路径、扫描外送ports及有理负载回算均总位多项式。所有p≤b的前置条件可按二进制有理比较检查。

C<2b是精确承重条件：若允许每台私有机接两件unit，容量计数不再迫port外送。新构件的unit基线还会把原OPT0提高到b（原任务非空时），所以不能忽略原零值或直接把N的近似比当原P的比。下一节单独证明未知OPT时的正确使用。

Evidence / Status / Related Files：独立研究者仅据精确陈述重构出上述二叉树版本；另一研究者独立构出路径容量版本。实际记录见[审查](../../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。规范[正规形构造与实际映射](../../../tests/audits/unrelated_machines/ternary_unit_selector_normal_form.py)实现本节，不含假设的次二求解器；[冻结有限审计](../../../evidence/runs/unrelated_machines/ternary_unit_selector_normal_form_sparse_audit.json)只核关键实际分配及位编码边界，不承担一般证明。这是自足阈值表示与解码，不是主目标存在或反面的证明。

## 8. 三端正规类与 UM-TARGET 的统一次二算法等价

**ID/version：UM-TARGET-TERNARY-SELECTOR-EQUIVALENCE-v1。**

**Exact Statement / Objects / Domain / Quantifiers。** UM-TARGET-v1成立，当且仅当存在某个固定ε>0、对第7节全部正规类输入（b随实例显式给出）输出实际(2−ε)调度的确定性总位多项式算法。两方向均包含空任务、OPT0、零端及单可用机器。这里证明的是算法存在的等价性，不声称已构造任一边的算法；也不把某个固定ρ<2困难性升级成所有ε的否定。

**Definitions / Assumptions / Dependencies / Scope / Conclusion。** 正规类严格是第7节明确结构，所有有限原端时间≤给定b；只导入UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1和下一段有理尺度搜索。一般源PCSP困难性不是前提。任意一般UM算法当然可用于该子类，下面是承重反向。

### 零值先处理，正值尺度只跨一个n因子

若没有任务，返回空分配。若每个任务都有一个零端，逐任务选零端得到OPT0的完整调度。反之令

\[
 \ell_j=\min_{i:p_{ij}<\infty}p_{ij},\qquad
 L=\max_j\ell_j>0,\qquad U=\sum_j\ell_j.
\]

每个任务在任何分配上耗时至少其最小时间，所以OPT≥L；逐任务选最小端给完整调度且最大负载≤U。因此L≤OPT≤U≤nL。个别零端任务可保留，不能把所有ℓ_j都当正；只需它们的最大值L正。

设正规类有实际(2−ε)算法。固定有理η∈(0,min{ε,1})，取g=1+η/4。枚举b_t=L g^t，从t0开始直到首个b_t≥U，包含该末项；总项数O_η(log(n+1))。对每个b，先删原p>b资格。因为b≥L≥ℓ_j，每个任务至少保留一条有限边，然后构造N_b并调用所假设的正规类算法。

只在返回实际τ确实满足C_max(τ)<2b时运行第7节解码；其余候选丢弃。每次可解码都得到一个合法原σ，选择实际makespan最小者。

### 存在一个保证合格的guess，并给统一余量

有枚举尺度b满足OPT≤b≤gOPT：取首个不小于OPT者。原最优调度不使用p>b，故剪枝后的P仍有≤b调度；正规形前向映射给OPT(N_b)≤b。所假设算法于是返回

\[
 C_{\max}(\tau)\le(2-\epsilon)b
 <(2-\eta)b<2b,
\]

该候选必保留且可解码。输出原σ满足

\[
 C_{\max}(\sigma)
 \le (2-\eta)g\,\mathrm{OPT}
 =\left(2-\frac\eta2-\frac{\eta^2}4\right)\mathrm{OPT}
 \le(2-\eta/2)\mathrm{OPT}.
\]

η/2是独立于m,n,P的正固定常数，实际分配由解码给出。未把未知OPT当输入，未要求任意小guess成功，也不对≥2b的τ强行作容量投影。

### 位复杂度及主反面的准确含义

L、U可精确计算，位长受原有理输入长度多项式控制。η、g是算法固定常数；尺度数O_η(log(n+1))，b_t的分子分母位长多项式。每次剪枝、正规形、假设算法、严格阈值比较和解码均位多项式，所以整个反向算法满足目标的确定性总位复杂度。它没有按处理时间或分母数值循环。

正规类因此保留了主目标的重要全部内容：可以把一般研究聚焦到**一任意小端加一unit端的两端任务、及最多三端的unit-only one-hot任务**。这不是证明该类hard，也不是把它任意退化为只有两端unit任务的旧arc模型。任何足以否定所有统一次二算法的困难性仍需真实YES/NO归约与全局源解码；第2–3节一般PCSP NP-hard没有自动完成这一步。

Evidence / Counterevidence / Status / Related Files：statement-first独立重构已分别核正规形和未知OPT算法等价；后读正文的实际记录见[审查](../../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。数学条件推论完整，无已提供的正规类近似求解器，外审/全球新颖性未认证。UM-TARGET-v1及其一般反面仍OPEN。
