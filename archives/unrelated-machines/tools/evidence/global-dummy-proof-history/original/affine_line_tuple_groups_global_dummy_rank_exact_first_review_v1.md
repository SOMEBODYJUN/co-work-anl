# 仿射线 tuple-as-group + global dummy：rank 独立 Exact-first 重构 v1

审查者：rank_deficiency_fee，2026-10-18。仅据 root 给出的新精确陈述，以及已公开 current 的明示 source 定义独立重构。本记录先冻结，再交 root；未读取其它新 Proof 或其它 agent 对本候选的推导，未向其它 agent 发策略。只写 clone 外 scratch。

## 1. 读取边界与精确候选

实际只读取公开 current

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md`

的第1–27行：primary定位、§2的 Objects/Domain、资源/直线公式及旧完整矩阵定义；未读取该页其后的Hall证明作为本候选依据。新的 tuple-group/global-dummy 候选由 root 本轮消息给定，不存在本次声称已读的新作者 Exact/Proof 文件。

本次认证其明示 compiler 的实际≤3/2逃逸及unit可行性等价，不认证外部论文困难性证明、全局新颖性或所有source桥。

## 2. 自足 source 与新完整P

取prime R≥2、k≥1，有限变量X及indexed relations G；每g涉及k个不同变量X_g。每变量x的relation-degree≤R，并给注入j_x:G(x)→F_R。每relation给显式allowed tuple表A_g⊆F_R^{X_g}，本次允许A_g为空；空表不生成tuple groups。

令G₀={g:A_g非空}，m₀=|G₀|。每allowed indexed tuple e=(g,s)、s∈A_g生成一组，组总数n=N_sets=Σ_g|A_g|。给显式整数q，1≤q≤m₀，因此n≥m₀≥1。令d=n−q≥0、D=kR。

真实资源为带tag的U=⊔_(x∈X){x}×F_R²。对tuple e=(g,s)，其原full set是

    E_(x,g,a)={(x,z,az+j_x(g)):z∈F_R}，
    S_e=⊔_(x∈X_g)E_(x,g,s(x))。

每S_e恰D个distinct资源。另添d枚互异global dummy资源δ₁,…,δ_d，与U不交。

新ordinary flat P：每tuple-group e有1+d个indexed states：一个原stateS_e、每个dummy各一个singleton state{δ_l}。原state资源private时间均1/D，dummy state唯一incidence的private时间1；所有资源端时间1。每indexed state独立private机器；每group一枚selector，在自己全部private机器time1。每state-resource incidence一件不同原job，只有其private与对应真实resource两个finite端；未述∞。**全部states全部jobs均存在**，global dummy未按group私有化。

所以每state总private质量严格1。所有group非空，所有原jobs有finite端，n≥1保证完整P机器数正。

## 3. 独立重构的确定性≤3/2算法

从G₀按输入顺序任选q个不同relations，每个选表内第一tuple；得到q个tuple groups F₀。这不读取源赋值、full-set matching、最优值或其它未知witness。其余n−q=d个groups保留待选dummy。

只考虑F₀已选的q个原sets，证明可给每组恰b=⌈D/2⌉枚共同不交真实资源。对任意F⊆F₀及变量x，设r_x为F中包含x的relations数。因每relation至多选一个tuple，degree假设给r_x≤R，且这些relation的intercepts j_x(g)两两不同。

对应r_x条仿射线均长R，任两条交至多一枚资源：若slopes相同，因intercepts不同而平行不交；若slopes不同，方程唯一解。不会出现重合线。由两阶Bonferroni下界，

    |所选x-lines的并|
      ≥r_x R−C(r_x,2)
      ≥r_x(R+1)/2。

带变量tag的资源块互不交，且Σ_xr_x=k|F|。故选中groups的资格邻集满足

    |N(F)|≥k(R+1)|F|/2≥⌈kR/2⌉|F|=b|F|。

最后不等式包括D奇数：⌈D/2⌉≤D/2+1/2≤D/2+k/2。F空自动满足。

因此把每group连b个同邻接slots，任意slot子集涉及F时其数量≤b|F|≤|N(F)|，Hall整数matching给每组选中原set恰b枚互不相交资源B_e。可直接用整数容量flow，或普通slot matching；不用枚举全部F。证明只对选出的q个不同relation原sets使用degree/不重合线性质，未把n个tuple groups全部错误地当作relation-degree仍≤R。

其余d个tuple groups与d枚global dummy作任意确定性bijection，每组选对应singleton state。现构造全部原jobs的实际调度：

* e∈F₀的selector在其原state private，只有B_e对应的b件原incidence外送真实U；其余原state incidence留private。
* 其余group的selector在指派的dummy state private，该singleton incidence外送对应global dummy资源。
* **所有未选states的全部incidence jobs一律留各自private**，包括原groups的未选dummy states，以及选dummy groups的原state与其它dummy states。

每件原job恰一次、仅用原finite端。选中原state private负载

    1+(D−b)/D=2−b/D；

选中dummy private负载1；任一未选state private总负载1。U资源因B_e共同matching至多一枚unit；global dummy因bijection至多一枚unit。故实际全机峰≤2−⌈kR/2⌉/(kR)≤3/2。因q≥1且D≥2，该构造确有selected原private达到所写峰，但认证只需上界。

## 4. 完整unit可行 iff 原full-set matching≥q

**从原full-set packing到unit实际。** 若原indexed tuple sets有q个两两不交，选它们的原states；其余n−q=d个groups分别选择不同dummy singleton。所有selectors在选态private，selected state的**全部**incidences外送；其余所有states的incidences留private。原full sets不交、dummy各只用一次且与U分离，因此全资源≤1；selected private仅selector1，unselected private质量1。全部原jobs完整峰1。

**从任意unit实际到原packing。** 任意完整峰≤1的actual中，每selector占自己的一个state private、耗时1。该selected state的每件incidence private时间都严格正（原state1/D或dummy1），故必须全部导出到其真实resource。每resource时间unit，峰≤1时至多一件。选中dummy的groups至多d个，因为它们各须用不同global dummy资源；n个groups故至少n−d=q个选中原state。这些原full sets全部真实导出、两两不交，得到≥q的原packing。未选states若也有外送，只会占用更多resource，不破坏提取。

这覆盖任意完整unit调度，不假定事先正规化到只有selected states外送。总体OPT≥1由selector给出。命题是unit可行性与full-set cardinality的精确等价，不把≤3/2算法当unit判定器。

## 5. q=n、空relations与source promise

若q=n，则d=0。因q≤m₀≤n，必m₀=n=q，即每个非空relation表恰一tuple。算法选全部q个relations，无groups需要dummy，无dummy state/resource/job，前面Hall与actual输出仍有效。unit提取则要求全部n个原full sets不交，与等价相符。没有除以d或强行添加dummy。

空relations不生成groups，不改变其余原j_x的注入或degree界；原source约束数量若包含空relations仍应按其原定义计算。这里m₀仅用于本候选阈值域1≤q≤m₀及算法选择，不把primary的value分母从|G|免费改为m₀，也不把near-perfect YES换成perfect YES。

若m₀=0或外部给定q>m₀，就不在本候选域；不以删空relations后换阈值冒充原source promise。一个完整source归约若需覆盖这些情形，须另作合法case-handling。本记录不为之补未声明合同。

## 6. 精确规模、位复杂度与否定范围

写v=|X|。完整P有n groups，n(d+1) private机，vR²+d resource机；jobs为

    n+nD+nd = n(D+d+1)。

finite条目为selector资格n(d+1)加两端incidence资格2n(D+d)，合

    n(2D+3d+1)。

dense条目为

    [n(d+1)+vR²+d]·n(D+d+1)。

原时间1/D位长O(logD)，其它有限时间1；tuple/field/tag身份显式。选q不同非空relations、生成qD条selected支持边、b槽/组的整数matching、dummy bijection及全部原job回填，均对完整显式输入/输出总位长多项式。Slots qb≤qD≤nD，不按分母再造数值巨大对象；不枚举2^q Hall子集或source assignments。

此与current源合同相同：不是对succinct binary R参数承诺poly(logR)展开vR²资源及nD原jobs；primary使用固定k,R时才直接是其原source输入的位多项式编译。若显式UM已给出，则找上述≤3/2调度本身是总位多项式，无optimum witness前提。

独立结论：本候选的两项主Claim均成立，未发现standing fatal。Tuple-as-group虽然失去全体n组上的line degree界，但d=n−q个globaldummy足以只让q个不同relations采用原states，恢复用于partial allocation的真实不重合线条件；此仅解释本具体compiler的逃逸，不声称所有grouping/globaldummy桥失败。

技术是标准仿射线交点计数、Hall整数性与完整flat回填；不作新颖性或外部困难性认证。算法没有忽略任何未选state jobs，unit等价也没有提供缺失partial-set soundness。它关闭的是给定的自然tuple-group+globaldummy近二编译，仍不排其它source桥、改变资源/任务/归一化的归约或一般UM反面。
