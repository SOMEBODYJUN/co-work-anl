# Tagged affine LINE：一个 primary 与 pairwise 标签的 onehot helpers 必有 actual unit escape

ID：UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1。

作者 rainbow_gap_source，2026-10-18。仅 scratch。本文件是首次冻结的 statement-only Exact，不含作者 Proof；先交 root，再由 root 路由独立审查。root 已读此前消息策略，不具 blind 身份。作者未向 general、rank 或其它独立 reviewer 发送本合同策略/Proof。

## 1. 完整变量、groups 与 line 资源

给定素数 R≥2，在 F_R 上运算。变量 namespace 为不交的 primary 集 P 与 auxiliary 集 A。P 非空，A 可空或含 unused variables。资源为各变量带标签的完整 plane U_x={x}×F_R²，不同变量块互异。

groups 恰为一个 main M 与有限 helper 集 H（允许为空）。M 恰参加全部 P，不参加 A。每个 helper h 指定唯一 primary u(h)∈P；它的全部变量恰为 {u(h)}∪A_h，其中 A_h⊆A 可空且无重复。helper 不参加其它 primary，也没有额外非helper groups。Auxiliary variables 可在不同 primary blocks 的任意 helpers 间共享。

对每个 incidence (g,x) 给固定 intercept j_x(g)∈F_R，同一变量的不同 groups 的 intercept 互异。因此所有变量度至多R；每个 primary 至多有R−1个 helpers加main，auxiliary 至多有R个 helpers。intercepts 不要求main为0，不允许算法改编号。

每group有非空显式 indexed-state 菜单 S_g。每state s给其各变量一个 slope label a_{g,s}(x)∈F_R，完整资源集为各 tagged lines 的不交并

T_{g,s}=⊔_{x∈X_g}{(x,z,a_{g,s}(x)z+j_x(g)):z∈F_R}。

每个完整 state-resource incidence 显式给非负有理 private 权 p_{g,s,u}，每state总和恰1。Main各state权完全任意，可有任意多个正cells、任意0权cells。每个 helper 的每个 indexed state 必须恰有一个正cell，该cell权为1，其余完整 line incidences权0；此 onehot cell 可依赖完整state、变量、intercept及全部输入，未预先绑定到任何主线或parking点。所有 states 与零权 incidences 均保留。

## 2. 精确局部分布接口

每helper h 给显式非负有理分布 λ_{h,s}（s∈S_h），总和1；允许部分state概率0。要求：

对每 t∈F_R，Σ_{s:a_{h,s}(u(h))=t}λ_{h,s}=1/R；

对每 x∈A_h 及 t,a∈F_R，

Σ_{s:a_{h,s}(u(h))=t, a_{h,s}(x)=a}λ_{h,s}=1/R²。

即每个 helper 的 primary label uniform，且 primary label 与每个 auxiliary label pairwise uniform。不同 auxiliary labels 之间不要求独立或uniform joint；main不要求有任何局部分布或pairwise性质。λ 是显式输入证书，不是从实际YES调度推导出的分布。

也可仅把“存在满足这些等式的非负实数 λ”作为数学前提；此时本结论的实际存在性仍成立。若没有提供 λ，算法可先对每个helper的显式 state table 解上述有限 rational feasibility LP，取得有理证书后继续；若不可行可返回该接口失败，不能据此宣称UM不可行。该LP的变量、约束和编码长度均按完整显式输入多项式，不枚举指数配置。给定的有理证书也可在总位多项式内直接核查。

## 3. 全量实际结论

对每个上述输入，以及 main 任意预先指定的 indexed state s_M∈S_M，存在确定性总位多项式算法：

- 为每个helper选择一个原 indexed state，并为其分配该state的唯一正cell；
- 给main其指定state的全部正cells；
- 所有这些正资源跨groups互异，每组质量恰1。

算法输出不要求全部 selected 完整几何 supports 互不相交；helper在auxiliary上的0权cells可与其它selected supports相交。它不需要给定全局source标签赋值，也不声称找到source CSP全满足。

记normalized flat partial allocation最优值为V，则V=1。输出的helper states仍是输入原菜单中的合法 indexed states，不能仅输出互相独立、却拼不成某个原state的labels。算法保留 main 给定state，不改其权或label vector。

## 4. 完整 ordinary P 与全部原jobs

每indexed state各一台不同private root，每tagged resource各一台resource machine。每group一枚unit selector，在该组全部state roots可用。每state-resource incidence是一枚不同job，在自己private root用时p_{g,s,u}、在对应resource machine用时1，其余选项∞。没有额外machines、jobs、预载、虚拟容量或外部锁定模式。

上述算法可输出包含每个selector、每个indexed state及每枚incidence job（包括全部0权jobs）的完整实际schedule，C_max=1。因此OPT(P)=1。所有未选states也实际调度；不存在删除未选states、忽略baseline原任务或免费外送。0权private jobs可与所选selector共处，仍属于原job列表。

## 5. 显式编码与总位复杂度

所有资源planes、state label tables、完整line权表均已显式给出或实际展开。若n=1+|H|、S=Σ_g|S_g|、I=RΣ_g|S_g||X_g|，则完整P有S+(|P|+|A|)R²台机器和n+I枚jobs。有限资格表每incidence两端，private权0亦照列；dense矩阵乘积仍是此显式输入规模的多项式。

λ只在显式state列表上运算，所有有理运算、field arithmetic、整数matching、state查表与完整schedule输出均按总位长多项式。没有按R!、1/λ或有理分母的数值展开。若λ仅以实数可行性存在，前述有理LP可找到多项式位长证书；该说明不依赖未知实际allocation。

不声称仅给二进制R、compact predicates或权oracle时可在poly(logR)内展开R²planes和全部jobs。

## 6. 范围与不适用条件

这是具体 tagged-line/onehot-helper interface 的实际unit escape。它允许任意共享auxiliary，允许main任意state-dependent norm1权，且不需要uniform-within-line、wide rectangles或LLL。

它不覆盖helper同时参加多个primary、helper有多个正cells的diffuse states、main参加auxiliary、额外非onehot groups、外部预载，或缺少所述primary–auxiliary条件pairwise marginals的模型。不能据此宣称所有pairwise-independent line菜单都actual常数，亦不能把它转成一般identity复制不可能性。

未声称它是Chan/LST原hard image或任何新hardness；本合同只指出以一个conditioned primary加onehot matching core来PI化旧parking族时的真实escape。
