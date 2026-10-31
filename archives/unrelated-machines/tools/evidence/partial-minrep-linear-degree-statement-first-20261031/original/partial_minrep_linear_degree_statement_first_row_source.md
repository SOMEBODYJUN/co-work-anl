# 部分 Min-Rep 线性 degree v2：陈述先行独立重构

审查对象：`partial_minrep_linear_degree_source_v2_exact_statement.md`，实际 SHA256 `067ebfea168a2047d4b9a533c17430afdfefff78a14c0cb473f61a401b83c906`。

读取顺序与先验披露：收到本次任务前，pcsp_occurrence 曾主动预告旧 O(g log g) 参数及“更小 γ=ρ³/(10⁹g⁸) 可能用 Chernoff 降成 O(g)”；未提供构造、推导或 proof。此后本次仅实际读取指定 Exact Statement，未读 v2 proof、其它 agent source review 或 child review。本稿是据 Exact 独立重构，不称完全未见参数的全盲审。以下推导在读任何冻结证明前完成并冻结。

结论：给定显式 regular projection game 的删边算法四项、线性 degree 必要性以及条件 fee 推论均成立，常数有大量余量。PCP/parallel-repetition 的外部来源未在此审查中读取，故固定参数 SAT-source 句保留为导入这些外部定理后的条件结论；正规化本身在第7节独立重构。没有证明或构造 UM 编译器。

## 1. 用原 soundness 控制所有 cheap lists

记原边数 m=ND/2，τ=ρ/(100g²)，γ=ρ³/(10⁹g⁸)。任取 cost≤gN 的 multilabeling ψ，取实数阈值

    H=4g/τ=400g³/ρ。

称 list 大小>H 的顶点为重顶点。它们至多 gN/H 个。regular 性保证其关联边的比例至多

    D(gN/H)/m=2g/H=τ/2。

对于两端 list 均≤H 的已覆盖边，从每个非空 list 独立均匀选一个 label；空 list 任取一个固定 label。该边被满足的概率至少 1/H²。故所有这种低 list 已覆盖边的比例至多 γH²。精确代数为

    γH²=(2/125)τ。

因此每个 cheap multilabeling 在原图的覆盖率至多

    [1/2+2/125]τ=(129/250)τ<τ。              (1.1)

不需要列出所有 cheap lists；这是统一数学上界。空列表、平行 constraint 边以及非整数 H 均无问题。

## 2. NO 对象域上的 list 数量，不丢入 log N

任何总投影 game 都有 val≥1/Q：固定全部左 label，再对每个右点均匀取一个 label，逐边满足概率为1/Q。因此 val≤γ 时 Q≥1/γ≥2g。

全部 multilabeling 是 NQ 个顶点-label 对的子集，cheap 条件给子集大小≤t=gN；此处 t≤NQ/2。标准二项式和估计给

    number of cheap multilabelings
    ≤Σ_{j=0}^{t} binom(NQ,j)
    ≤(eQ/g)^{gN}
    ≤exp(gNλ)，λ=1+ceil(log₂Q)。             (2.1)

可自足验证中间估计：令 L=NQ、x=t/(L−t)≤1，则 x^tΣ_{j≤t}binom(L,j)≤(1+x)^L；整理并用 (1+t/(L−t))^{L−t}≤e^t。最后 1+ln Q≤λ，所以没有隐藏 log N 或 alphabet 的数值循环。

## 3. D<2μ 的确定性分支

此时原图 maxdegree D<2μ≤1000μ=Δ，且 D≥1、n≥1 保证非空。perfect YES 的 singleton labeling 原样保留。NO 时(1.1)给覆盖率<τ<ρ，所以该分支的 NO 性质确定成立。

## 4. 抽样分支的三个好事件

以下 D≥2μ。令 s 为最小满足 2^s μ≥D 的整数，p=2^(−s)，d=pD，z=pm=N d/2。由最小性

    μ/2<d≤μ，qquad Nμ/4<z≤Nμ/2。           (4.1)

令 X 为中间图总边数，Z 为 degree 清理实际删掉的边数。对每个 cheap ψ，令 Y_ψ 为中间图被 ψ 覆盖的边数。将共同控制以下事件：

    X≥z/2； Z≤z/4； 所有 cheap ψ 均有 Y_ψ<ρz/4。

于是剩余边 m'=X−Z≥z/4>0。删除不能增加已覆盖边绝对数，所以每个 ψ 在输出图覆盖严格少于 ρz/4≤ρm'。这同时给非空和严格<ρ，而不是非严格 soundness。

### 4.1 总边数下尾

X 是独立边抽样的 binomial，均值 z。Chernoff 给

    Pr[X<z/2]≤exp(−z/8)。

有 ℓ=floor(log₂g)≤g，λ≥2，ρ≤1，因此 μ≥2000，N≥2，(4.1)给 z>1000。于是该失败概率<exp(−125)<1/1000。

### 4.2 同时控制全部 cheap lists

固定 ψ 时，原图已覆盖边数≤τm，所以 Y_ψ 的均值≤τz。取实阈值 t=ρz/4。上尾 Chernoff（均值为0时结论直接成立）给

    Pr[Y_ψ≥ρz/4]
    ≤[4eτ/ρ]^{ρz/4}
    =[e/(25g²)]^{ρz/4}。

因为 g≥2^ℓ、ln2≥1/2 且 25>e，

    ln(25g²/e)≥2ln g≥ℓ。

再用(4.1)和 μ≥1000gλ/(ρℓ)，得到单个 ψ 的坏概率至多

    exp[−(125/2)gNλ]。

用(2.1) union bound，存在任何 cheap list 坏的概率至多

    exp[−(123/2)gNλ]≤exp(−492)<1/1000。     (4.2)

阈值可以非整数；指数 Markov/Chernoff 对实阈值也成立。坏事件用 ≥ρz/4，所以好事件确实给严格小于。

### 4.3 一次 degree deletion 的损失

某顶点中间 degree V 服从 Bin(D,p)，均值≤μ。Δ=1000μ 为整数。由 size-bias 恒等式

    E[V·1_{V>Δ}]
    =Dp·Pr[Bin(D−1,p)≥Δ]
    ≤μ(eμ/Δ)^Δ
    ≤μ·2^(−1000μ)。

若 Δ>D−1，相关尾概率为0，仍可用此上界。每条被清理边至少在一个 high-degree 端被上述和计入，因此

    E[Z]≤Nμ·2^(−1000μ)。

由 z>Nμ/4 和 Markov，

    Pr[Z>z/4]≤16·2^(−1000μ)<1/1000。       (4.3)

这里只使用中间 degree 一次；不要求迭代清理。输出 high-degree 顶点已无边，其余点输出 degree≤其中间 degree≤Δ，所以 maxdegree 对每个随机种子都成立。

三个失败概率之和<3/1000，得到至少0.997、因而至少0.9的所需 NO 事件。此处更高成功常数只是本审查的余量，不建议据此改原 Claim 版本。

## 5. perfect YES 与统一总位复杂度

原 perfect singleton labeling 对任意边子集仍满足全部投影，所以每个种子都保留 cost≤N 的全覆盖；输出无边时真空成立。

ℓ、λ由显式整数位长取得；τ、γ、μ、Δ均用二进制整数/有理运算计算，其编码长为输入编码长的多项式。μ、Δ 即便数值远大于输入规模也不要求循环其数值。

若进入抽样分支，μ≥1 保证 s≤ceil(log₂D)。逐条显式边生成 s 个独立公平位，全部为0才保留，概率恰 p。总随机位≤m ceil(log₂D)，对显式输入为多项式。之后计中间 degree、标记 degree>Δ 的点、扫描原样本边输出符合条件者，均为多项式。平行边各自独立采样并分别计数，没有借用简单图假设。

输出只是原顶点、alphabet 和 constraint 表的删边子对象，长度不超过显式输入加多项式元数据。源外部 PCP 链不属于此统一 bit-poly 断言。

本审查用 Fraction 作了独立精确常数反算：γH²/τ=2/125；1/2+2/125=129/250；1000/16−1=123/2；(123/2)·8=492。概率界使用 e≥2、ln2≥1/2 等粗界，未依赖浮点尾概率。

## 6. 线性 degree 必要性：ceil 和严格性

给任何非空双部总投影 game，左右顶点各 N/2，允许 isolates、非regular、平行边。先给每个左顶点任取一个 label，费用 N/2。再任取 t=ceil(ρM) 条 constraint，在每条的右端 list 加其左 label 的实际投影；总费用≤N/2+t，至少 t 条边被覆盖。去重只会少花费用。

令 T=(g−1/2)N 为整数，因为 N 偶数、g 整数。若 M≤T/ρ，则 ρM≤T，所以 ceil(ρM)≤T。于是该 labeling 费用≤gN，覆盖率≥ρ，违反所述严格<ρ禁令。

故必须

    M>(g−1/2)N/ρ。

由总 degree=2M≤NΔ_max，进一步

    Δ_max>(2g−1)/ρ。

ρ=1 时仍正确；因为 t≤M，所选边总存在。必要性完全不使用 PCP、regularity 或抽样算法，确实排除固定ρ时的 o(g) degree 阶。

## 7. 外部 source 条件及精确正规化的独立部分

本次未读取 primary PCP/parallel-repetition 原文，因此不认证外部定理适用条件已由本审查逐项核过。以下是条件推导：若有 perfect-complete、常数 soundness<1、固定有限字母表的 biregular projection PCP，且其 parallel repetition 有指数 soundness 衰减，则对固定ρ，取 O_ρ(log g) 次重复即可达到 γ=ρ³/(10⁹g⁸)，alphabet 为 poly_ρ(g)。对先固定的 g、ρ，重复次数为常数，所以 SAT-size 的多项式指数可依赖它们；这不提供 uniform 随 g 增长的 PCP 归约。

两项正规化本身可自足保 value：

1. biregular 左右度 d_A,d_B 时，把每个左点复制 d_A 份、每个右点复制 d_B 份，每条旧 constraint 替成其 clone 间完全双部 constraint。新两侧各 m 个顶点，degree=d_A d_B。旧标签复制给新点证明 value不降；给任意新赋值，从每个旧顶点的 clones 独立均匀取一个 label，期望满足率恰新赋值满足率，故 value不升。允许平行边。显式规模至多旧边数的三次量级，故位多项式。
2. 两侧 alphabet 不同时取共同 alphabet 大小 max(2,Q_A,Q_B)。把左方无效标签固定折回某个有效旧左 label，然后按旧投影输出有效右 label；右方 padding labels 从不成为任何投影像。任意赋值可把无效左 labels 折回、无效右 labels 改有效而不减满足边，因此精确保value和perfect completeness。总映射显式大小只多项式增长。

Q≤poly_ρ(g) 给 λ/ℓ=O_ρ(1)，所以 μ=O_ρ(g)、Δ=O_ρ(g)，ceil 的常数项不改变 g≥2 下的阶。

随机 source composition 的 YES 每种子保留、NO成功≥0.9；若存在其确定性 promise 判定器，SAT 得一个 YES总接受、NO高概率拒绝的随机算法，特别在 BPP 中。因此 NP⊄BPP 是充分明确的排除假设；仅 P≠NP 不足据此推出不存在该判定器。

## 8. 物理 fee 条件仅作条件推论

需 F>0、c≥0（除法/预算语义所需）。若真实 compiler 已证实际弱 σ 可解码 coverage≥ρM，且

    cost≤N+B(σ)/F，qquad B(σ)≤cM，

则由 maxdegree≤Δ 和保留 N 顶点，M≤ΔN/2。取 F≥cΔ/[2(g−1)] 得 cost≤gN，立即与 NO cheap-list 条件冲突。

Δ=O_ρ(g)、g≥2 给所需 fee 为 O_ρ,c(1)，前提是 c 与 Q、g 独立；该常数可能非常大，不能把“常数存在”替换成F=1。没有新增实际 P、query-trigger、π 接口或 fee 实现。这些仍是主物理义务。

## 冻结审查回执

给定显式输入的随机删边四项：独立重构通过。degree 必要性、ceil 严格性、fee 条件代数：通过。正规化：本稿给出独立自足证明。外部 PCP/parallel-repetition 导入：本次未读 primary，保持条件身份。没有 standing fatal objection；F>0、c≥0 可作物理段定义澄清，不改变其正常数学语义。新颖性、实现、UM 主反面均未认证。
