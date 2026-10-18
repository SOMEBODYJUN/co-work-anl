# Flat 菜单资源度三的重匹配路径归约：冻结 Exact v1

ID: UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1。
作者：boss11 内部 typed_edge_gap，2026-10-18。本文件只给完整物理构造与待独立攻击结论，暂不附作者证明。不是hardness源，不登记Work/Git。

## 1. Source与全部原P

源为非空有限group集G，各group非空显式indexed菜单A_g。每state s有distinct资源集合S_gs，每incidence给非负二进制有理p_gsu，总private质量W_gs=Σp_gsu≤1。资源与private机器namespace不交，零权、空state、重复indexed states和unused资源允许。不限制资源跨group度、不限制group interaction、state数或support大小。

源ordinary UM P：每state一私有机器M_gs，每resource一机器R_u；每group一件selector J_g，只能在本group state机器上执行，time1；每(g,s,u)一件独立job，只能在M_gs耗时p_gsu或R_u耗时1。其余∞，无其它jobs/预载。若要求归一化，再加W_gs=1；本构造不改变任何旧private权。

记Γ(u)={g:u∈∪_sS_gs}，d_u=|Γ(u)|，全部membership包括零权incidence。每个d_u≥1的resource，把Γ(u)按任意显式次序列为g_1,…,g_{d_u}。

## 2. Target的完整flat-menu构造

每个旧resource u改为d_u枚互异port资源 z_{u,1},…,z_{u,d_u}。旧group g_j的所有states中u均统一改名为z_{u,j}，private权p_gsu保持不变；同一group不同states不会得到不同port。其余旧state和indexed结构均保留。

对每u、每j=1,…,d_u−1新增一个heavy-only helper group H_{u,j}，恰有两个indexed states：

    state L：singleton {z_{u,j}}，权1；
    state R：singleton {z_{u,j+1}}，权1。

每个helper按source同一flat菜单规则实际生成自己的两台private state机器、一枚unit selector与两枚incidence jobs（各private1/resource1）。没有抽象matroid约束或免费边。d_u=1时无helper。d_u=0的旧resource可保留为unused机器，也可删除；若保留它不参与任何资格。

Target P'恰为这些旧改端jobs与全部helper原jobs的完整flat普通UM矩阵。旧private机器/selector不动；旧incidence job的唯一resource端改到该group的port。未列端全部∞。

## 3. Exact Statements

(A) Target每个resource跨全部indexed菜单的group度至多3：一个旧group，加至多两个相邻helper groups。旧group菜单数不变，helper恰2states，故若源每group至多Kstates，目标至多max{K,2}states。源若全部W=1，目标仍全部W=1；非归一化源的旧W也原样保留。helper菜单是实际heavy-only singleton选择，不能把它们误作one-heavy/two-diffuse mixed group。

(B) 对每份源实际完整σ，若Cmax(σ)=C<2，可det bitpoly构造目标完整actualσ'，每件旧job身份保留且private端选择不变，满足Cmax(σ')≤C。对每份目标完整actualτ'，若Cmax(τ')=C<2，可det bitpoly投影成源完整actualτ，所有旧job原private端或原resource端均合法，满足Cmax(τ)≤C。投影必须覆盖目标任意实际partial exports，不能只处理full states或预先选好的helper matching。

(C) 真实普通makespan精确保留：

    OPT(P') = OPT(P)。

本域总有1≤OPT≤2。结论涵盖OPT=2边界，不仅给strict<2的promise。归约不需要输入OPT、YES witness或source assignment。

(D) 在归一化W=1域，定义V为：给每group选一个indexed state，再给它一个该state资源子集，所有groups的资源子集两两不交，最大化最小导出private质量。则V(P')=V(P)，包含V=0边界。更强地，对每正有理阈值v∈(0,1]，source有value≥v的whole-state partial allocation iff target有，且两向actual见证可det bitpoly转换。每helper在正阈值下必须拿到其所选singleton整资源，不能给它fractional份额。

所以任意已闭合的normalized flat tiny-gap源可按本构造降到resource degree3，同时保持原K≥2；但本构造自身不给这样的源、不改进NP/ETH/UGC假设，也不把singletons matching的可解性冒作hardness。

## 4. 显式规模与位合同

令L为旧incidence数、B为旧P总位编码长；Σd_u≤L。新增helper数Σ(d_u−1)_+≤L、port数≤L；每helper精确增加2台private机器、3件jobs、6条finite资格（selector两条、两incidence各两条）。旧private数/旧jobs不复制。完整dense P'仍为B的多项式规模，只复制旧有理权并加入time1。处理路径与分配映射均按显式路径长度运行，不按处理时间分母/参数倒数展开。

Zero/private0 jobs仍是真实原jobs、resource端仍unit；所有group degree均按完整菜单并集计算。没有声称能把任意一般UM先分解成此flat结构，也没有声称将所有group强制成one-heavy/two-diffuse型。
