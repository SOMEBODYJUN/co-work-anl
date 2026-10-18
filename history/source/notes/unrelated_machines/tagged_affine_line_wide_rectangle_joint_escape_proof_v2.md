# Tagged affine LINE wide-rectangle joint escape：作者 Proof v2

对应 statement-only Exact：`tagged_affine_line_wide_rectangle_joint_escape_exact_v2.md`，SHA256 `6be53020ad2e0f8f810fa1cbc862fa0ba931378c04b60c2e7d81d34a564d9063`。作者 rainbow_gap_source，2026-10-18。仅交 root hold；未向 rank、general、bicriteria 或其它独立 reviewer 发送本 Proof 或作者策略。Root 已读消息推导，不具本合同的 blind 身份。

## 1. 逐组选态与固定编号

按输入给定顺序处理 groups，绝不修改固定 intercepts。对每个变量 x，维护前面已选 states 在 x 上的全部 marked 点列表 Z_x。当前处理 g、x∈X_g 时，前面至多已有 d_x−1 个 groups 使用 x，故

|Z_x|≤b(d_x−1)≤b(D−1)。

这里实际只保存、扫描这些点，不创建 b 个虚拟点。

对一个旧 marked 点 (x,z,y)，求有哪些新 slope a 会使它位于当前 group 的 line y=az+j_x(g)。若 z≠0，恰有一个禁值 a=(y−j_x(g))/z。若 z=0，这个旧点在它所属旧 group h 的 line 上，所以 y=j_x(h)；注入性给 j_x(h)≠j_x(g)，因此它不在当前 group 的任意 slope line 上，禁值为空。

因此 A_{g,x} 内最多排除 b(D−1)<L≤|A_{g,x}| 个 labels，至少可选一个 a_x。为每个 x 独立选一个剩余 label，所得 vector 位于 ∏_xA_{g,x}。Rectangle containment 保证完整 indexed-state menu 有同 vector 的某个 state；查表取一个即可。相同 vector 的其它 indexed states 及其权表仍保留，未被删除或视为与所选 state 相同。

选定完整 state 后才读取它实际的 marked 集并加入对应 Z_x，因而 marked 和权可任意依赖整个 state、intercept 和其它输入。新选的整条 line 已经避开所有旧 marked 点，无需在选 slope 前预知该新 state 的 marked/probe 位置。

归纳得到：任意不同 selected states 的 marked 点不重合。更精确地，较后 state 的完整几何支持避开全部较早 marked 点；它自己的 marked 点仍可与较早的 unmarked 点重合。这一后者损失必须计入，不能声称全部 selected supports 不交。

## 2. 一个共同实际 allocation，兼顾 marked 与 unmarked

记所选完整支持为 T_g，marked 并为 E_g。令

C_g={u∈T_g:u∉T_h 对所有 h≠g}，
B_g=E_g∪C_g。

全部 E_g 互异；任何 C_g 都不在其它组的完整支持内，故 B_g 两两不交。所有 marked 点被保留，所有几何无冲突点被保留；若 marked 点与另一组 unmarked 点重合，后一组不会在 C_h 中取得该点，因而只由 marked owner 保留。没有分别选择两套 allocation 再免费叠加。

固定 g。任何未保留的点都不在 E_g 中，因此其 p 权≤β；它同时属于至少一个其它 selected 完整支持。对一个共享变量 x，g 与其它 h 的 intercept 不同。若所选 slopes 相同，两条 line 平行且不交；若不同，有限域中相交恰一点。不同变量块带标签分离。所以 g 与所有其它 selected supports 的 distinct 交点数量至多

Σ_{x∈X_g}(d_x−1)=M_g≤M。

同一点遇多个对手会在该和中被多计，仍是合法上界。故 g 丢掉的全部质量≤M_gβ，从 row 总质量1得

Σ_{u∈B_g}p_{g,s(g),u}≥1−M_gβ。

质量本身非负，因此每组至少 max{0,1−Mβ}=v。特别，新 marked 点抢走旧 unmarked 点、或旧 marked 点占住新 unmarked 点时，被损失方每点均≤β，而且这些点全部包含在刚才的 M_g 交点计数中。

## 3. 变成包含所有原 jobs 的实际 schedule

把每组 selector 放在其所选 state 的 private root。对所选 state，把 B_g 内全部 incidence jobs 导出到其 resource machines；把它的其它 jobs 留在该 private root。每个未选 indexed state 的全部 incidence jobs 都留它自己的 private root。

每个原 selector 和每个原 incidence job 因此恰被分配一次。此规则包括0权 jobs：即使某些被领取的0权点对应 job 被导出，它仍以真实 unit 时间占资源；B_g 互异保证没有容量重复。亦可把这些0权 jobs 留 private，不影响负载。没有删除任何实际任务。

每个 resource machine 至多一枚 unit job，负载≤1。每个未选 state private root 的全部 row 权和为1，负载1。g 的 selected root 负载是

1+Σ_{u∈T_g\B_g}p_{g,s(g),u}=2−Σ_{u∈B_g}p_{g,s(g),u}≤2−v。

v∈[0,1]，所以2−v≥1，涵盖资源与未选 roots 的负载。由此得到完整实际 C_max≤2−v。即使 v=0，论证仍给合法 C_max≤2，不需要正值逆向投影。

## 4. Sparse-positive 与 arbitrary-weight 两个应用

Sparse 情形取 marked 恰为全部正权点、β=0。每 incidence 的实际 marked 列表≤b，主不等式给 v=1；所有正质量均保留。Unit selector 本身给任何完整实际 schedule 的 C_max≥1，故 OPT(P)=1。

Arbitrary-weight 情形设 D>1，K=2q(D−1)>0，β=1/K。取每个 incidence 中权严格大于 β 的实际 cells 为 marked。每条 line 的总权≤1，故这类 cells 的数量严格小于K，特别≤b:=K=floor(1/β)。这只是一个计数上界，不是需要创建的列表大小。

若 L>2q(D−1)²=K(D−1)=b(D−1)，主合同适用。由 M≤q(D−1) 得 Mβ≤1/2，所以 v≥1/2、完整实际 C_max≤3/2。所有 marks 从现有显式 line 点中用精确有理阈值比较得到；即使 K 大于实际 line 长度 R，也不迭代到K。

## 5. D=1、M=0 与零端点

若 D=1，每个变量最多属一个 group，tagged blocks 使任意两组完整 supports 不交。任意选 states 并领取全部资源即质量1，按§3给实际 unit schedule；不需要定义1/(D−1)、1/M或1/β。非空 groups 与各 X_g 非空保证 D≥1；M=0在本域也等价于没有共享变量，因此同一处理成立。

β=0时从不计算1/β；主合同本身仅用给定 b 和实际 marks。b=0时所有 marked 列表为空，选态及无冲突 allocation 仍合法，全部损失用β和M计。归一化使 b=β=0 同时出现的非空实例前件不可满足，但不影响一般端点逻辑。Unused variable 的资源机器可空置；其 d_x=0 不会出现在任何 X_g 的 M_g 和中。

## 6. 查表、输入规模与确定性位复杂度

给定显式 rectangle sets，令 N_g=∏_x|A_{g,x}|。其二进制位长≤Σ_xlog₂R+1，为输入的多项式。用确定性排序/去重统计显式菜单中落在 rectangle 的 distinct vectors 数 K_g。它们本来就是该 Cartesian product 的子集，故 containment 当且仅当 K_g=N_g。即使 N_g 巨大，也只作二进制乘法和比较，不枚举该 product。对算法选出的 vector，线性扫描或排序字典均可取一个匹配 indexed state。

求 forbidden slopes 只扫描旧的实际 marked 列表；field 非零除法用有限域逆，prime R 时扩展欧几里得算法位多项式。每一步从显式 A_{g,x} 列表中找未禁值，不扫描1/β、b或有理分母个对象。构造 B_g 可枚举所有已选完整 line cells、按 tagged resource 排序计 multiplicity，再加 marks，工作量为显式输入的多项式。

完整 P 有 Σ_g|S_g|+|X|R² 台机器和 |G|+RΣ_g|S_g||X_g| 枚 jobs；这些数量本就在展开的资源/权表的多项式内。输出稀疏两端资格或 dense matrix 都是多项式。Private rational 权的精确和、比较与Mβ有总位多项式长度；没有数值展开。Compact source 若未实际展开，不能由本结论偷得原 compact 位长下的统一编译保证。

整个证明只用输入 wide rectangles、固定 intercept 注入性、每对 tagged lines 至多一交点与显式权表。它不依赖任何未审的 PCP/perfect-PI source typing，不将可自行选择大 R 误称排除 compiler 的其它参数或原 Chan RS code-coset tables。
