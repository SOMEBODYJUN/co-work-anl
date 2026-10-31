# 三叉末层两色下的张量与收缩限制：冻结证明

研究身份：boss11 内部研究者 shared_label_attack；无独立 Work / Git 写入。

本证明源于本研究者先核旧三叉构造、独立提出末层调色板不变量及其张量/纯收缩限制，随后 root 整理 Exact。不是对同一自己提出机制的盲审，未读取其它研究者审查稿；在本人先指出 v1 的常量与 U 高度问题后，root 告知另审也发现常量问题，这一简短转述未参与本证明。它只合并为现有三叉资产的路线限制，不声称新的通用困难性或一般调度算法。

精确对象：`UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2`。绑定最终 v2 Exact `/workspace/scratch/038d9dcc4cac/ternary_palette_tensor_obstruction_v2_exact_statement.md`，实际逐字读取并计算 SHA256 `11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df`。

版本审查：此前实际读取 root v1 Exact SHA256 `f6166e0961307f0b69d6c67541d38cf3863be64b05c1b915caae19c108278f22` 后，指出两处域规范：一般 U 必须高度 H>=1；旧 canonical 没有规定常量实例的具体叶色，故应明确固定 h1 `(A,B,A)` 为常量 YES、`(A,A,A)` 为常量 NO，不能说任意合法常量分支都已满足前提。root 另冻 v2 修正这两处，本证明与 v2 对齐，不倒称 v1 第4项原先已充分成立。

实际核对既有 canonical：`research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md`，当时 SHA256 `9314ea1777df138b047587a391bba7ddf487ab5a3ecc94ef928425ed23e654c0`。核阅其中 v1/v2 的 Rigid/palette、Dead、Atom、AND、OR、Pad 全部递归定义，不借旧总结猜测构造。

## 1. 对象及全机矩阵

设 U 是完整 d 叉有根树，高 H>=1，d>=2，全部叶恰深 H。叶着色可重复。定义 q(U) 为最大整数 r in {1,...,d}，使存在包含原 root、每个活跃 internal 恰选 r 个原 children、所有叶仍深 H 的虹彩子树。

P(U) 的 internal machines 与颜色 resources 使用不交 namespace。每个 internal node 一台私有机器，每个实际颜色一台 resource。root pin 一件 job，唯一 finite 端是 root，时间1。每条树边对应一件不同 job：其父端在父机器时间1/d，另一端在 internal child（或 leaf 的颜色 resource）时间1。其余资格全部无限。

这是完整普通不相关调度矩阵；每件 job 都有 finite 端，pin 单端，其它双端。共有 1+树边数 件 jobs，internal 数加实际颜色数台 machines。下端不是可以随意改目的地的抽象 token。时间1/d、1具有明确有限有理位编码。

## 2. 一般恒等式 OPT(P(U))=2-q(U)/d

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

## 3. 实际 v1/v2 编译族的末层不变量

性质 B：每个深 h-1 的原父节点，其三个直接叶 children 至多两种颜色。

v1 Rigid(H,S) 在 H=1 时的三叶正是 `(a,b,a)`；所有更高 Rigid 的末层属于递归 Rigid(1) 星。v1 Dead(H,c) 全叶同色，故末层一色。Atom 明确使用 Rigid(1)，不把裸 height0 atom 当公式构件。

v2 的 R_1(S) 也正是 `(a,b,a)`，protected 色只是选择 b 位，不改变“两色”；D_H 在每个末层星中三叶同色，星与星的颜色不同不影响 B。更高 R_H 的末层来自 R_1 或 D_1，故 B 保持。

两套编译器的 AND、OR、Pad 均只拼接高度至少1的已有 logical/palette/dead 子树，并在上方加 internal root；不会新建一个由来自不同构件的 height0 叶直接混合而成的末层星。按构造归纳，所有非退化公式输出均满足 B。

旧 canonical 只说空/常量输入可映到固定 YES/NO，没有给该固定实例的着色。因此这里明确选择 h=1 的 `(A,B,A)` 常量 YES（q=2）和 `(A,A,A)` 常量 NO（q=1），使这两个合法固定输出同样满足 B。此规范不影响 any nontrivial 3SAT 归约、size 或语义。不能倒称任意合法常量 YES 都满足 B，例如 `(A,B,C)` 明显不是。

## 4. 对齐 Cartesian 张量的精确上界与 YES 等式

设 T 满足 B，完整三叉高 h>=1。T^[k] 在每个深 ell 的节点是 T 深 ell 节点的有序 k 元组；孩子逐坐标选择原 children，故共同度 d=3^k，深度仍 h。叶色为有序原颜色 tuple，用可自定界编码，颜色相等当且仅当所有坐标均相等，不使用有碰撞 hash。

取任一张量末层父节点 `(u_1,...,u_k)`，每个原 u_i 的直接叶色集合 C_i 至多2。该张量父节点全部 children 的颜色集合恰为 C_1×...×C_k，大小至多2^k。任意 full r 虹彩子树至少含一个活跃末层父节点；该节点选中的 r 个叶颜色也必须互异。因此

    q(T^[k]) <= 2^k.

若 q(T)>=2，取 T 中一棵实际 full binary rainbow F。每坐标都限制在 F，逐节点取这 k 个 binary child 选择的 Cartesian product，获得 T^[k] 中 full 2^k 叉子树。任意两个不同的叶元组至少在某坐标的原 F 叶不同；F 的该坐标叶色互异，故 tuple 颜色不同。此乘积见证真虹彩。

于是 q(T^[k])>=2^k，结合局部调色板上界恰等2^k。应用第2节：

    OPT(P(T^[k])) = 2 - 2^k/3^k = 2-(2/3)^k.

这不是仅承诺一份较弱 YES 调度，而是本输入族的实际精确 OPT。k>=2 时 2^k<3^k-1，所以这些 YES 输入本身没有 full(d-1) 虹彩子树。这个原因已先于任何 NO 解码失败。

## 5. 实际 gap 上界 G_k 严格递减

对任意上述 YES base tree，其张量普通 P 的 OPT 同为 A_k=2-(2/3)^k。NO 一侧甚至不需要保留原二叉谓词；对任意同域 base tree 张量，由第2节路径构造，实际 OPT<=B_k=2-3^(-k)。所以任何意图赋予本操作 YES/NO 值 gap 的实际比率至多

    G_k = B_k/A_k = (2*3^k-1)/(2*3^k-2^k).

没有使用未证明的 NO soundness，也没有把叶数比例当逐层分叉。令 A=3^k，B=2^k。两个分母均正，直接通分：

    G_k-G_(k+1)
      = [2*A*(B-2)+B] / [(2*A-B)*(6*A-2*B)] > 0,

因为 k>=1 时 B>=2 且 B>0。故 G_k 对所有整数 k>=1 严格递减。G_1=(5/3)/(4/3)=5/4，因此 G_k<=5/4；又 `(2/3)^k` 与 `3^(-k)` 均趋0，G_k趋1。

数值 sanity：G_1=5/4，G_2=17/14，G_3=53/46；这是“任意 NO 最强”的上包络，不与特定小例 NO 的实际 gap 混淆。已用 Fraction 对 k=1,...,30 反算上述精确通分恒等式及严格性，有限回算只查代数排印，非一般证明来源。

## 6. 纯 k 层收缩的独立完备性障碍

现在 k>=2 且 k 整除 h。把原深0,k,2k,...,h 的节点保留为 macro 节点，原 k 步后代连为 macro children；不改任何原叶颜色。新共同度 d=3^k，高 h/k>=1。这里随后按 P 定义重编 macro-tree 的普通调度；不是声称原 physical P 的内部 jobs/资格原封保存。

每个末层 macro-parent 对应一个原完整 height-k 子树。它含3^(k-1)个原末层三叶星，每星颜色数<=2。因此该 macro-parent 的全部原叶（即新直接 children）合计至多

    2*3^(k-1) = (2/3)d

种颜色。任意虹彩 full r macro 子树在活跃的某个末层 macro-parent 必选 r 种不同色，所以

    q(contract_k(T)) <= 2*3^(k-1) < 3^k-1 = d-1.

严格不等式来自 3^(k-1)>1。它对 SAT/YES 输出同样成立，因此该纯收缩连所需 strong(d-1) 完备性都达不到。k=1 只给2=d-1，不声称该边界也被排除。若 h 不整除 k、最后层不等长、再补节点或改色，就不是本条定义的纯收缩，必须重新检查实际对象。

## 7. 显式规模、复杂性条件和不外推

T^[k] 的第 ell 层有3^(k*ell)个节点；总数为 `(3^(k(h+1))-1)/(3^k-1)`。完整输入必须实际展开，颜色 tuple 也是实际记录；没有按 binary k 的原编码长度承诺多项式输出。若原 SAT 编译树大小 n^{O(1)}，取 k=O(log n)，张量大小至多 n^{O(log n)}，所以允许准多项式归约是合理的规模范围。

但是数学上对每个有限 k 的 YES 精确 OPT 与 G_k 上界均已成立；允许这种更大展开不会把 G_k 从<=5/4变到近2，反而 k 增大时趋1。不存在可在此处援引 NP 不包含 QP 来弥补的 gap：只有已经证明的准多项式 gap 归约，加上假定多项式近似算法，才可导出 NP 包含 QP；这个复杂度假设不能替代缺失的 gap。

纯收缩保留全部原叶，macro 树规模不超过原树，h>=k 且 d=3^k 已显式受原叶数约束；颜色位编码未变。

结论严格限于末层两色前提下，tuple-equality 的对齐 Cartesian 张量及保叶色的等长纯收缩。它不排除重新设计跨副本颜色约束、非对齐变换、改变时间/任务接口、加入其它状态或 padding 的新机制；也没有证明所有 rainbow-tree gap amplification 不可能。一般 UM-TARGET-v1 仍 OPEN。本条只应并入旧三叉路线的精确限制，无一般算法或主困难性升级，新颖性/独立论文价值未认证。
