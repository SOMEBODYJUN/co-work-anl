# 三组资源加权菜单嵌入零权三维立方体：Exact-first 独立审查

审查者：general_query_response_review。2026-10-18。

冻结前只读取 `degree_three_weighted_menu_cube_embedding_exact.md`，SHA-256 `b7cd715acf14005fdda54865a23d6d31a956b6f20a7cb19f211189cc154e76ef`。未寻找或读取作者Proof、其它agent论证或外部新证明；未修改repo/Work/Git。

**明确结论：新embedding Claim有效，未发现fatal。下述双向映射对全部实际原jobs成立，不只对最优解或所选states成立。**

## 1. 构造的几何合法性

对每个原resource u建tagged变量 x_u，完整列出27个资源格。其incident groups恰是所有 `u∈U_g` 的groups，包括仅零权原incidences导致的membership。源degree≤3，故可按输入顺序赋互异 `j_u(g)∈{1,2,3}`。

在每个g的全部indexed states中，对每个u∈U_g统一取coordinate label `ell=j_u(g)`。由target slice定义，此组在x_u的slice为

\[
F_{g,u}=\{z\in[3]^3:z_{j_u(g)}=j_u(g)\}.
\]

其恰有9格，且固定 `z*=(1,2,3)` 满足每个条件。因此原u的全部incident groups的slices都包含同一active格 `(x_u,z*)`。

同一组每state对每var只有一个slice，无重复cells；不同变量tag不交，所以每state incidence job总数为9q_g。源union为空时新增仅该组拥有的dummy，label/index均1，9个slice jobs全零，使组变量集非空，且不与任何其它组产生共资源。

构造特意不以label vector表示旧state：同组所有旧states拥有相同label vector，原indexed state、独立private机、selector选项及该state的cost table全部保留。Target定义明确允许此事，故重复vector但cost不同不是漏洞；若另要求vector唯一决定state/cost，则本嵌入不能用于那个更窄模型。

## 2. 每个原对象的单射与有限端逐项保持

保持每个原group、indexed state及private机 M_gs；保持每组原selector及其所有private选项，时间都为1。将原R_u识别为 `(x_u,z*)`，包括unused原resources。

对每个实际存在的原incidence `I_gsu`，将其识别为target state `(g,s)` 中variable x_u的active-cell job。因为u∈S_gs必有u∈U_g，active格必在此state的slice中。其target的两个有限端恰为：

- 原private机 M_gs，时间 p_gsu；
- 原resource像 `(x_u,z*)`，时间1。

全部其它端仍为无穷，没有获得其它8个aux格的资格。不同原incidences的 `(g,s,u)` 不同，像job也不同，因此没有合并任何原jobs。原p=0 job也属于这一单射：不能因为其cost与aux零job相同就删除或替换。

若源state缺u，active格的job才是新增aux job；该slice其余8格jobs也新增，private时间0、各自格resource时间1。对dummy的全部jobs同理。因而原实例是target中带显式identity tags的原子实例，附加的只有这些零private jobs和aux资源机；原private机没有新增正work。

投影必须依照显式原job标识/构造映射辨别原零job与aux零job，不能只看p=0。该映射可随构造保留，标签长度多项式。

## 3. 任意完整源schedule的精确扩展

给任意合法完整原调度σ，不要求最优、不要求C<2、不要求全export。每个原job按上面的机器映射保留原执行端，有限processing time完全相同。

每个aux incidence job都放它自己的indexed private机，那里处理时间恰0。这也适用于selector所在state的aux jobs，以及全部未选states的aux jobs。没有任何原job被删，也无需改动任何原分配。

于是各原机器像的load完全等于原load，全部aux resource机load0。源G非空所以至少一个unit selector、makespan≥1，故加idle资源不会改变最大值；事实上即使只看非负load，零负载机器也不增加峰。得到

\[
C_{\max}(\widehat\sigma)=C_{\max}(\sigma).
\]

若schedule含具体非抢占时间，新增零job可在自己private机时间0瞬时执行，不占正长度区间；仍不改变原执行和makespan。没有虚拟拆分执行。

## 4. 任意完整target schedule的投影

给任意合法target scheduleτ，aux零private jobs可以被τ任意安排，甚至export到unit resource端；无需假设它们已经留private。

删除全部aux jobs及aux资源机；对每个保留的原job按逆identity映回原机。每个原selector只可能在其原private菜单；每个原incidence只可能在其原private机或其active-resource像，所以逆映一定是原合法端。每个原job仍恰一次，原zero jobs也保留。原unused R_u的active像属于保留机器，不应误作为aux删除。

删除任务只减少load，保留任务的time不变，所以

\[
C_{\max}(\pi\tau)\le C_{\max}(\tau).
\]

不需要resource独占或threshold<2；即使target某active机接多枚unit jobs，投影也是完整原调度。aux导出占用额外资源只会影响该target schedule是否可行，不会破坏删除后的合法性。

因此扩展给 `OPT(C(P))≤OPT(P)`，投影给反向不等式，实际OPT精确相等。所有以实际makespan阈值定义的YES/NO promises随之转移；不自动转移aux job计数、其它费用或未声明的allocation/source promises。

## 5. Private mass、正support与严格unit

每target state只有原incidences在active格保留原p，其余全部0，故总private mass恰为原W_gs≤1。

记原state正support `P^+_gs={u∈S_gs:p_gsu>0}`。Target对应正support恰为

\[
\{(x_u,z*):u\in P^+_{gs}\}.
\]

active原p0与缺失incidence新增p0都不进正support，dummy贡献空support。此处正support与完整union必须区别使用。

在makespan≤1时，selector已占满所选private机；其每个p>0 incidence都必须export到unit资源，p0可与selector同机。因此每组选一个state且跨组正supports不交是必要条件。反向给定这样的选态：选中state正jobs export、zero jobs留private，所有未选state jobs全部留private，row sum≤1；完整调度峰≤1。该论证对源与target均成立，且正support在active格的映射精确保持。

几何slice可以在其它零权cells相交，这些零jobs可留private，不产生标签一致性约束。若把aux零cells扰动为正，其选中state jobs将必须export，重叠slice会造成新增unit冲突，可能破坏严格unit completeness。Exact没有作该错误扩张。

## 6. Interaction exact保持

对不同源groups g,h：

- 若共享原u，则两组均incident于x_u，其slices都含active `(x_u,z*)`，所以target完整state-resource unions相交。不同j还给其几何pair交3格，但至少active已经足够。
- 若无共享原u，则两组使用的x_u tags不交，dummy也各组独有，因此target完整unions不交。

这包括共享原resource但所有相应p都为零的情况：源interaction仍存在，target几何interaction也仍存在。故源和target是同一group顶点集上的完全相同interaction graph，最大度M精确保持，不只是上界。

任何target resource格只来自一个variable cube，拥有它的groups是该variable的至多3个incident groups的子集；dummy至多1，unused原cube为0。故target resource group-degree≤3。Q=d=3不限制一个group可同时incident多少variables，也就不限制保留的M。

## 7. 空集、unused与显式计数/位复杂度

令e为q_g=0组数、`q'_g=max(1,q_g)`、S为总state数。资源机恰 `27(|U|+e)`，其中每原R_u对应一个active格；private机S、selectors|G|不变；incidence jobs恰

\[
9\sum_gK_gq'_g.
\]

全部原incidences都在其中，aux incidence数为上式减原incidence数。Aux资源机数为`26|U|+27e`。

q_g可以0，U甚至可以空；此时给每组独占dummy，原selector/state完整保留，所有新增jobs零private，interaction仍空。Unused原resource也保留其active原机像及26个aux格，不擅自删原machine inventory。

因源groups及menus非空，e≤|G|≤S，且 `q'_g≤max(1,|U|)`，所以

\[
\sum_gK_gq'_g\le S\max(1,|U|).
\]

即使某原state缺其group union中大量resources，补齐仍是显式输入规模的多项式。27、9为固定常数，不生成3^{q_g}个全局状态；每state只显式写其q'_g个labels及9q'_g个jobs。Dense矩阵的jobs×machines条目计数如Exact所列，仍poly。有限非零times只是复制原二进制有理数，其余0/1，标签与identity map编码长度poly；没有按时间数值、分母或倒数循环。

## 8. 组成范围

固定M的positive theorem `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2` 本轮未另读或重新证明。此embedding实际满足其在Exact中所引用的flat weighted-menu结构、resource degree上界3及同一M，因此给定该已成立positive theorem后，参数代入的composition没有额外结构障碍。这里认证的是exact embedding及其保参性质，不为未知hardness promise背书。

**最终冻结：新Exact的实际instance/schedule embedding有效，无fatal；尚未读取作者Proof。**
