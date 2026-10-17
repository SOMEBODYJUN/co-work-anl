# 近单位蕴含 promise：真实一般困难性与物理复制缺口

读取目的：保存已经闭合的 unrestricted PCSP 困难性，准确隔开尚未闭合的调度编译。它给一个可供主反面归约使用的源，但没有证明 UM-TARGET-v1 不成立。普通 non-delta-matroid / edge-CSP 定理不能自动补上 promise、任务出现次数和端口类型。

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

一般UM也允许任务有三个以上有限端，两端Boolean表示不是目标的限制。一个native任务可在A端耗时1、在k个不同M_i端耗时1/k。若b表示它是否分给A，x_i表示它是否离开small端M_i，则其精确可选状态为(1,1^k)，或某个(0,1^k−e_i)。b0时并非全部x0；这提供真实one-cold多端关系，但仍只有一件任务/一次占用。全部unit端任务则给incoming one-hot。不同表示可以独立攻击，不把Boolean两次发生copy路线当方法白名单。

足够反面的一条精确义务是：对任意大固定k，把一个已NP-hard的上述source（例如r2）编译成显式普通UM，YES所有原任务C≤T₀，且任意C≤C_r实际σ均可构造源weak解，并保持全部机器同时负载、任务合法性、总位多项式规模。该义务仍未完成。不能仅验证某个label pattern或局部Boolean关系。

数量上，若此编译只用{1,1/k}，所有实际负载在1/k网格上，NO无C≤C_r会给

    OPT_NO≥2−(r−1)/k，
    OPT_NO/T₀≥(2k−r+1)/(k+1)=2−(r+1)/(k+1)。

因此如果能对任意大固定k保持r2的**物理**hardness，就足以在P≠NP下排除每个固定(2−ε)算法。该句是明确条件推论，不是已构成的归约；一般PCSP已hard不能删掉“物理”。单个固定k或固定ρ<2也不排除所有ε改善。

现有private-tree、半密度与逐行均匀资产只封闭其准确合同；没有一项证明上述三型全局编译不可能。新的承重机制仍须在实际P上闭合copy/decoder，不把可求源oracle、non-delta或LPgap冒作解码。
