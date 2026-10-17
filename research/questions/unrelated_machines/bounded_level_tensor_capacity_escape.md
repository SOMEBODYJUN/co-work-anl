# 固定层数共同上容量仍不能修复资源束张量

**读取目的与状态。** 这是 boss11 反面路线的候选工作草稿：检查 tensor 加跨层资源 guards 能否避免 fractional-perfect 整数化。一般存在性证明完成、root 已另行重构主机制；尚无独立外审、新颖性认证或实际 UM 困难性。它不是通用确定性位多项式构造，不申请 Canonical Claim 升级。

候选身份 `UM-TENSOR-JOINT-GUARD-ESCAPE-q1`。Objects/Domain/Quantifiers 为下文 q=2 parity 三维匹配源和固定 L、存在偶 t 的资源束乘积；无复杂度假设。Conclusion 为同一真实整数乘积 matching 通过所有至多 L 层共同上容量；不含 actual UM 矩阵或一般算法否定。Dependencies 是 F₂ 线性代数、共轭对称和 union bound。Evidence 仅给定 L2,t4 原整数 matching/322类guards及资源clone分配；一般 L 由数学推导承担。Counterevidence/Objections：该具体 B 不过展示的三层guard；一般 B 未给统一位poly构造；source-to-UM、所有输入依赖高阶guards和真正prefix functional coherence均未解决。Status 为候选源接口障碍：构造者与 root 各自重构，尚未完成先陈述盲审，不进入 canonical Claim/graph，不认证外审或新颖性。

## 精确接口与结论

令 A⊆X×Y×Z，三轴各 q 元，ν(A) 为整数匹配数。A^{⊗t} 的边为 (x,y,z)∈X^t×Y^t×Z^t，每层 i 的 (x_i,y_i,z_i)∈A。F 是普通整数 tensor matching，即三个全长坐标投影各不重复。

固定 L≥1。一个**至多 L 层上容量 guard**：选非空层集 S、s=|S|≤L；每层 i∈S 选任意非空轴集 T_i⊆{X,Y,Z}；指定这些坐标的值；要求 F 中满足这个 joint pattern 的边数≤q^(t−s)。全部 guards 要由同一个 F 同时满足。没有加入“使用数必须为0或满块”或 joint-prefix functional coherence。

**这些 guards 真正保 YES。** 若 M 是 A 的任意完美匹配，则 M^{⊗t} 为 q^t 条整数 matching。每个被测层至少固定一轴，因 M 的各轴双射，该层最多允许一条 M 边；同层多轴若不兼容则计数0，否则 pattern 恰出现 q^(t−s) 次。因此所有 guards 同时有效，不是只保某个挑选的 YES。

**候选精确陈述。** 对每个固定整数 L≥1，存在有限偶数 t≥L，使固定源

    A⊕={(000),(011),(101),(110)}, q=2,

尽管 ν(A⊕)=1，却有 A⊕^{⊗t} 的完整 2^t 条整数 matching，满足上述全部至多 L 层共同 guards。还同时满足所有单轴 prefix 容量 q^(t−ℓ)。无复杂度假设。

Base 核验：A⊕ 的任意两边共享一轴，故整数最优恰1；每边权1/2时，每元素恰被两边关联，总权恰1，是显式 fractional perfect matching。结论是强化乘积**本身**的整数 YES，不是某个尚未构造 cover 的存在性。它只反驳此明确乘积接口，不排除特定受限 PCP 源族或高阶、输入依赖的其他 guards。

## 一般固定 L 的自足证明

选足够大偶数 t，使

    K=Σ_(s=1..L) binom(t,s)3^s < 2^t−2.              (1)

令 B₀ 为 t/2 个块 [[0,1],[1,1]] 的直和，则 B₀²+B₀+I=0。均匀取 C∈GL(t,2)，令 B=C B₀ C^(−1)，仍有 B²+B+I=0；B、I+B 可逆且没有非零固定点。

对固定非零 b，Bb 均匀分布于 F₂^t\{0,b}：共轭分布在固定 b 的 GL 稳定子下不变，该稳定子在其余非零向量上传递。Bᵀ 同样是均匀共轭。所以对非零 a≠b，Pr[Bᵀb=a]=1/(2^t−2)；a0、b0、a=b 的非零坏关系则被可逆性排除。

置 (X,Y,Z)=(x,Bx,(I+B)x)。从 s≤L 个不同层各选一个输出 bit 的形式；任何非空线性依赖可写为 a+Bᵀb=0，其中每个使用层 (a_i,b_i) 为 (1,0)、(0,1)、(1,1) 之一，且联合 support 大小≤L。这样的非零对至多 K 个。由 (1) 与 union bound，存在一个 B 使所有坏关系同时不存在。

因此任意≤L 个不同层、各层任选一轴的线性形式都独立。取

    F={(x,Bx,(I+B)x):x∈F₂^t}.

B、I+B 可逆给三个全长投影双射，x_i+y_i+z_i=0 给逐层合法，故 F 是真实完美整数 matching。对涉及 s 层的任意 guard，**先从每层被测轴中任选一轴**：这 s 个形式独立，每个 pattern 恰有 2^(t−s) 个 x；再固定同层额外轴只能删去 x，故完整 joint pattern 计数仍≤2^(t−s)。同一个 F 通过全部 guards。单轴 prefix 容量由全长坐标不重复自动成立。

**构造性边界。** 此为有限存在性证明；未证明按输入 t,L 确定性多项式找共轭 B。对固定 L 可将成功 B 当反例常数。下面 L2,t4 是直接给定并完整核验的例子；其 t 无须满足粗充分条件 (1)。

## 显式 L2,t4：16 条整数边

按通常行乘列，取

    B=[[1,1,0,1],[0,0,1,1],[1,1,0,0],[1,0,1,1]],
    I+B=[[0,1,0,1],[0,1,1,1],[1,1,1,0],[1,0,1,0]].

直接有 B²=I+B、B(I+B)=I；12 个形式 {e_i,row_i B,row_i(I+B)} 全非零且互异，故任意两形式独立。

| X | Y | Z |
|---|---|---|
|0000|0000|0000|
|0001|1101|1100|
|0010|0101|0111|
|0011|1000|1011|
|0100|1010|1110|
|0101|0111|0010|
|0110|1111|1001|
|0111|0010|0101|
|1000|1011|0011|
|1001|0110|1111|
|1010|1110|0100|
|1011|0011|1000|
|1100|0001|1101|
|1101|1100|0001|
|1110|0100|1010|
|1111|1001|0110|

精确程序逐项核同一 F 的全部 28 个一层、294 个两层非空轴集 test families，以及全部轴 prefix。对跨层单轴 pair guards，另给实际资源 clone 分配：每条边用3个 word resources与54个 pair-pattern resources；后者每 pattern 容量4，16边共用912个不同 clones，确为整数束分配。没有新增随机样本、LP或matching oracle。该固定 B 不通过所有三层 guards：X₁+X₂+Y₃=0，其四个可行 patterns 各4次，大于三层自然容量2。

## 与旧结果的区别和剩余义务

裸 parity tensor NO→YES 已在 `private_graft_and_resource_repetition.md` 保存；单轴 prefix 容量完全冗余，也已被旧反例直接覆盖。新增对象是**强化后的同一个产品**与任意固定 L 的所有跨层共同上容量，本页给同一整数 matching，而非引用某个有限 cover。它仍不实现 joint-prefix 的整数 functional association。

若把后者直接当额外 primitive——每个已出现的共同 prefix triple 内，下一坐标边必须构成 base 整数 matching——最大叶数确为 ν(A)^t（逐层归纳；重复最大 matching 达到）。但该 primitive 尚未在实际加性调度中实现；且 private 分层 min-degree 分数仍只取逐层最小 ν/q，不自动成为叶密度 (ν/q)^t。真正 O 是同时保 prefix 单次激活、全局一致性和 root 的乘法计数，并从任意低负载完整 σ 解码源。本文未闭合此 O。

随附[精确代码](../../../tests/audits/unrelated_machines/bounded_level_tensor_escape.py)与[冻结候选输出](../../../evidence/runs/unrelated_machines/bounded_level_tensor_escape_candidate.json)；程序只审 L2,t4，一般固定 L 由上文证明承担。保存/推送不升级候选身份。
