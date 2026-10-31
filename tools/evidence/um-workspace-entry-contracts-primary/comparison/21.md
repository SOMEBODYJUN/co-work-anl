---
id: "unrelated-machines/grouped-hypercube-slice-hall-retention"
kind: "theorem"
type_tag: "定理"
title: "分组超立方切片菜单的Hall保留与锐三半界"
status: "proved-with-stated-scope"
summary: "任意显式菜单选择均满足共同Hall保留界，可构造全部任务C≤3/2且界取得；d5Q2三变量组固定选择可通用保留11资源。"
legacy_ids:
  - "UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/grouped_hypercube_slice_scheduling_review.md"
---

# 分组超立方切片菜单的Hall保留与锐三半界

每状态每变量只取一个乘积坐标切片，变量资源命名互不合并，每变量参加至多d组且组编号注入。对任意菜单选择和全部组子族，精确并集计数给共同Hall界，从而可输出完整实际调度C≤3/2，无需源YES假设。三半是归一化负载界且有真实锐例；19/25和每组三变量保留11只是在d=5、Q=2下对任意固定状态选择的改进。它们不表示一般UM的三半算法或近似困难性。

## 超立方分组菜单的 Hall 保留与锐3/2实际界

本节是不同于前述需求树编译的新对象，另立 `UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2`；不改变 v4 的源反例合同。读取目的：检验 Davies–Guruswami–Ren 的新双标准 Set Packing 困难性是否能直接提供近二调度源。答案限于以下具体菜单桥：不能，整类输入都有实际3/2界，且该归一化界可达。

### 精确对象、算法与量词

取整数 d,Q≥1；变量集 X 与非空组集 G。每组 g 有非空的 distinct-variable 集 X_g、非空显式状态菜单 A_g。每变量 x 参加至多 d 个组，给单射 j_x:{g:x∈X_g}→[d]。状态 s∈A_g 为各 x∈X_g 选一个标签 ℓ_{g,s}(x)∈[Q]。

变量资源是带 x 标签的互不相交立方 U_x={x}×[d]^Q。其状态资源集为

\[
 S_{g,s}=\biguplus_{x\in X_g}
 \{(x,z):z_{\ell_{g,s}(x)}=j_x(g)\},
 \quad L_g=|X_g|d^{Q-1},\quad c_d=1-(1-1/d)^d.               \tag{H1}
\]

每状态每变量恰取一个切片；不同变量不能合并资源名，组的 incidence 索引必须注入；L_g 可随组变化，同组各状态大小相等。没有 CSP 可满足性或源 YES 假设。

**Exact Statement / Quantifiers。** 对每个这样的显式输入、每种任选一状态 s(g)∈A_g、每个组子族 F⊆G，同时有

\[
 \left|\bigcup_{g\in F}S_{g,s(g)}\right|
 \ge c_d\sum_{g\in F}L_g.                                 \tag{H2}
\]

故可在显式输入总位长的确定性多项式时间，分配两两不交 B_g⊆S_{g,s(g)}，|B_g|=⌊c_dL_g⌋。若 d=1 或 Q=1，则可全部分配，|B_g|=L_g；其余情形可以保证 |B_g|≥⌈L_g/2⌉。

**实际 UM 桥。** 每状态一个不同根机器 M_{g,s}；每资源 u 一个不同资源机器 R_u；每组一个 unit selector，只在自己组的各状态根可用。每个 state-resource incidence (g,s,u) 是一枚不同任务，在 M_{g,s} 时间1/L_g，在 R_u 时间1，其他端∞。所有机器、任务标签分离，全部任务必须分配。若完整选定状态集互不相交，OPT=1。对任意上述输入，不依赖 YES/NO，可确定性位多项式输出完整调度，且

\[
 C_{\max}\le3/2;                                         \tag{H3}
\]

d=1 或 Q=1 时 OPT=1。该类所有输入的 OPT/1 的上确界恰为3/2且取得；这不是声称3/2的近似比 NP-hard。

当 d=5,Q=2 时(H2)中的 c_d 可加强为19/25。每组恰三个变量、L_g=15时可每组分配11个资源，实际负载≤19/15。11是对任意固定状态选择的最佳通用整数保留量；不声称优化所有菜单选择之后仍必需要该界。

### 自足证明

固定状态选择及 F。在单个变量 x 上，令 r≤d 为 F 中的 incidence 数，t_ℓ为使用标签 ℓ 的个数，Σt_ℓ=r。注入索引保证同标签所取坐标值不同，因此资源并集恰为

\[
 d^Q-\prod_{\ell=1}^Q(d-t_\ell).
\]

r=0无需证明。d=1时每变量至多一组，所选集合互不相交。d>1，令 z=1−1/d。整数 t∈[0,d] 满足1−t/d≤z^t，故并集≥d^Q(1−z^r)。几何序列的前 r 项平均随 r 下降，r≤d 给

\[
 d(1-z^r)/r\ge1-z^d=c_d.
\]

故该变量并集≥c_d r d^{Q−1}。对带标签分离的变量求和即得(H2)。每个组需求⌊c_d L_g⌋满足全部带需求 Hall 不等式；组到资源二部网络的整数最大流输出实际不交分配。

进一步，d>1时二项式给

\[
 (1+1/(d-1))^{d-1}\ge2,
 \quad (1-1/d)^d\le(d-1)/(2d),
 \quad c_d\ge(d+1)/(2d).
\]

Q≥2时L_g/d为正整数，因此

\[
 c_d L_g\ge L_g/2+L_g/(2d)\ge L_g/2+1/2
 \ge\lceil L_g/2\rceil.
\]

Q=1时同一变量的索引互异，全部所选集合已不交。由此均可得到至少一半的整数分配。

在实际 P 中，把 selector 放在任选根 M_{g,s(g)}，将 B_g 对应的 incidence jobs 移到各自 R_u，其余 incidence jobs 留自己的状态根。资源机各至多一个 unit；未选根的全部小任务负载1；选中根负载

\[
 1+(L_g-|B_g|)/L_g\le3/2.
\]

全部原任务均被恰好分配，证明(H3)。若完整所选集不交，把所选 states 的全部 incidence jobs 外放，未选 states 的全部 incidence jobs 留在各自根，即可达1；至少一个 selector 时间1给 OPT≥1。

**3/2锐例。** d=2,Q=2、一个变量 x、两个组 j_x(g₁)=1,j_x(g₂)=2，各仅一状态，分别取标签1、2。两个大小2切片是 {z₁=1} 与 {z₂=2}，并集大小3。两根均被 selector 占1。若 C<3/2，四枚 incidence jobs（根端1/2）均须外放；但资源机 unit 容量为1，三个可用资源不能接四任务。各组分配一个不同资源则达到3/2，故 OPT=3/2。原 universe 第四格机器仍在，只是没有相应 incidence 可利用。

**19/25与11。** d=5,Q=2，变量上的 a 条行、b 条列满足a+b=r≤5，并集5r−ab≥5r−⌊r²/4⌋≥19r/5，故比率≥19/25。在r=5、(a,b)=(2,3)时等号成立。三变量组的 Hall 需求可取11，因为任意 F 并集≥57|F|/5≥11|F|。五组都使用同三个变量、各变量索引j=g，前两组选标签1、后三组选标签2，总并集57，不能每组分12（需60）。这只证明固定选择下的通用整数界。

### 原论文身份、位复杂度与范围

**Paper Fact。** Davies–Guruswami–Ren, *Scheduling Problems with Constrained Rejections*, arXiv:2511.00184v1，§5用 degree-five 3SAT、二元 alphabet、七个满足局部状态、每 set 大小15。Theorem4 是存在固定常数的**无分组 set selection**双标准困难性，参数 α=1/7、β=(1−ε₀)/7、ε<1/30；并非任意小保留比例困难性。15元素且保留比例1−ε、ε<1/30时，整数上已强制保留全部15。

本文另定义 clause groups，各有七状态，再接(H1)的实际 UM 桥；该桥不是原论文声称的 UM 近二归约。19/15和一般3/2是这里从乘积计数、Hall及全任务负载回算得到的结构推论，不归于原文定理。原PDF字节、SHA、实际读取范围见 literature manifest；冻结来源记载，原研究者核过§5的18页作者版原PDF（印13–14）及HTML对应段。没有把下载或摘要当新数学。

**Bit complexity。** 资源/状态/incidence显式给出或先实际展开，网络与 P 的规模均为其多项式；时间1/L_g用O(log L_g)位。c_d为O(d log d)位有理数，显式非空cube大小至少d，故精确需求计算也按显式位长多项式。若仅给二进制d,Q及简洁菜单描述，d^Q可指数大，不宣称该隐式编码的位多项式。各参数可增长，不能把固定参数结论冒充一般UM。

**Dependencies / Objections / Status。** 全部(H1)共同前提、精确乘积补集、整数 Hall/max flow、selector/incidence实际任务桥。重复 incidence 索引、合并变量资源、非乘积切片、多尺度负载或第二种接口可离开本定理，但没有由此自动得到 hard source；既有一般私有注入树5/3界仍须另核。完整证明如上；冻结来源的陈述先行独立重构及读后记录见[切片新对象审查](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/reviews/unrelated_machines/grouped_hypercube_slice_scheduling_review.md)。无新生产 LP/flow 实现；证明的可构造性与软件实现状态分开。外审/新颖性未认证，属于经典计数与Hall的结构推论，非主目标完成。

## 冻结审查范围与本轮比较

本轮全文读取独立审查源aa2d41822ff3e0ca8de1，核其明确指出并已修复的唯一措辞问题：存在完整不交状态选择时，仅把所选state的全部incidence jobs外放，未选state全部留根。原稿曾可能将“全部incidence外放”误读为含未选state；本正文保留完整全任务回填，未采用该含混表述。旧审查还核过d=1、Q=1、floor/ceil、L_g的整除性与显式位长。作者的额外有限算术检查不是本轮新运行，没有生产flow程序交付。

**原论文范围核对。** 本轮打开[Davies–Guruswami–Ren原论文v1 §5](https://arxiv.org/html/2511.00184v1#S5)及Theorem4，核其无分组set selection、高保留比例、degree5/二元字母表/七满足状态/15元素及ε<1/30参数。每组必须选择一个状态与这里的普通UM任务桥属于本对象另加的合同；19/15及三半是本文计数与Hall推导的结论，不归给原论文。这里只核这组具体依赖和差异，不声称重证该论文的全部困难性。

**关联。** 与[深树坐标切片源反例](../反例/坐标切片投影源编译--反例.md)的共同来源是乘积坐标切片，区别是这里资源保留不需形成深度Q的完整分叉子树；因此Hall匹配可直接输出本平星模型的调度。若改变变量资源命名、incidence索引注入、非乘积共享或小端归一化，就离开本定理域，但仍需另给源NO与每个低负载调度的解码。一般UM目标未被本对象解决。

## 分组切片专门审查的来源与独立性

本段整理source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/grouped_hypercube_slice_scheduling_review.md（对应源ID aa2d41822ff3e0ca8de1）的独有审查信息。它只覆盖分组超立方v2，不扩到坐标源v4或一般UM。

原构造者先读DGR原论文§3/5再提出乘积计数与Hall。原独立审者先只收Exact并重构Hall与19/15；原研究者后来提出全类三半与四格锐例，该审者也推出这一结论并提供c_d≥(d+1)/(2d)的短证。作者核对后冻结新的v2 Exact/Proof，审者再按Exact、Proof、最终组合的顺序核读。因此这份记录既含独立重构，也含审查者对最终证明的实质贡献，不能把整个过程一概称为对最终作者证明完全无先验的盲审。

最终读后提出的“全部incidence jobs外放”歧义及其修复已在上文保留。原记录没有生产flow实现，构造者额外有限算术检查也没有登记成原主研究者的新运行。

| 冻结来源路径（均相对于同一完整commit） | 原记录的SHA256 |
|---|---|
| history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v1_exact_and_proof.md | e380618458138f3c43f9692673f19b208c604112dd41a31c89b92e3b297987bf |
| history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v2_exact.md | edc9658d7f33ece188b4542178f7b82cf7d657099da1c6fd90dcf5979cf6ee55 |
| history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v2_author_proof.md.gz | 74715bf688a7819b389f036608ecb7a79c370c8d253694f3ce51362c019dad04 |
| history/source/notes/unrelated_machines/grouped_hypercube_slice_scheduling_v2_independent_review.md | f0b20bdd293b123d62f098d391427c2516fca27c7dd4fdf940c6830ad3a6304d |

gzip行是压缩文件的指纹；冻结记录另给解压原文SHA256 f773a57f681556f331f7d9804cf0c30d2fedbd00ac9ac595804cfda2330e7db0，说明保留了包括末尾空行的完整原字节。这两个指纹属于不同字节对象，不能直接比较为“文件变了”。本轮读取并整理该记录，没有重新解压该历史附件或重新执行其算术检查；其真实性范围仍按明确来源和读取顺序登记。
