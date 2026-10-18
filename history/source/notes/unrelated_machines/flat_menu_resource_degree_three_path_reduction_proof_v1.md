# Flat 菜单资源度三路径归约：作者 Proof v1

对应 `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1`，完整对象与构造见 `flat_menu_resource_degree_three_path_reduction_exact_v1.md`。Exact先发root与rainbow；两者均仅读Exact消息/陈述独立重构后，root要求冻结本Proof。本文只发root，不主动发送rainbow，待其Exact-only记录冻结。

这是标准单位matching路径的直接物理重构，未认证全球新颖性或独立成文价值。只覆盖给定flat菜单域，不冒称一般UM机器降度；不声称保持group interaction M。

## 1. 路径的任意指定hole

固定资源u，d=d_u≥1，port编号1,…,d，helper H_j相邻ports j,j+1，j=1,…,d−1。给定任一希望空出的port a，把H_j选左singleton j（j<a），选右singleton j+1（j≥a）。这恰覆盖全部port除a，各port恰一helper。

每helper在所选private机器执行selector，所选state incidence job完整外送选中的unit port；未选state incidence job留其private，时间1。helper两个private机器负载各1。无辅助的分数执行，无需把一helper的两incidence视作同job。

## 2. 任意源actual C<2的完整前向映射

源非空group的unit selector给C≥1。任何原resource R_u至多执行一枚原incidence unit job，因为两枚将负载2>C。若它执行属于旧group g_a的某原job，指定port a为空；若无原external job，任取a，例如1。

保留每件旧job的private/外送决定；旧private执行机器和处理时间均不变，外送原R_u改为该旧group的唯一port z_{u,a}，仍time1。同group的全部states统一用同port，所以未选state的实际外送也保留，不按某个预定选态删改。

按第1节完成全部helper原jobs。每port要么一枚旧unit，要么一枚helper unit，要么空；新private机器各负载1。旧private负载仍≤C；1≤C，所以全target峰≤C。d=1没有helper，同样成立。unused旧resource没有job，可删或保idle。

## 3. 任意target actual C<2的完整逆映射

考虑任意helper H_j，其selector实际选了自己的某一state private机。该state的incidence job若仍留private，将与unit selector形成负载2，违反C<2。因此该枚真正原incidence job必须完整外送所选singleton port。这对每个d−1枚helper分别成立。

所有port接收的旧/新incidence job时间都精确1。在C<2下每port至多接一件unit，故上述d−1枚所选helper jobs占用d−1个不同port。未选helper state也可能在给定actual调度中外送；它只会再占port，不能减少已强制的d−1个占用。因此一个原resource的整条port路径上至多还剩一个旧incidence job外送。

删除全部helper jobs与helper private机器，并把每枚旧port外送job改送原R_u。上段给每R_u至多一本旧unit job；所有旧private执行不动，负载不增。其余原任务各恰一次、所有旧资格合法，源Cmax≤C。这覆盖所有旧/新未选state的外送和任意partial exports，不借用full-state witness。

## 4. 实际OPT=2端点

源与target均有unit selectors，故OPT≥1。把每selector放任意本group state、全部incidence留自身private时，state总private权W≤1，目标新增helper W=1，故两边均有完整actual峰≤2。

若源OPT<2，第2节给target OPT≤源OPT<2；第3节施于最优target实际分配，反得源OPT≤targetOPT。若源OPT=2而targetOPT<2，第3节会给源实际峰<2，矛盾。于是targetOPT=2。两边候选完整assignments有限，最优值实际达到，不用极限或近似见证。

所以所有源输入均OPT(P')=OPT(P)，而不仅strict promise。

## 5. Normalized whole-state部分导出值

现在每state W=1。给定源value≥v>0的state/subset allocation，若资源u被旧group g_a领取，就按a留下hole；未被领取则任留hole。旧state与全部领取资源统一改名为本group port，保留原权。按路径matching为每helper选singleton并完整领取其port，helper value为1≥v。资源互不相交，故target value≥v。

反向，给任意target value≥v>0的allocation。每helper所选state是权1的singleton；为得到正value，它必须完整领取该singleton resource。因此d−1helpers占d−1个不同ports，旧groups至多还领取其中一个port。删除helpers并把旧port改名回u，得到源disjoint allocation；每个旧group仍是原同一个indexed state、原权与整个领取子集，value不减。这一步不要求导出整个state，也不假定target helper使用某个预先挑好的path matching。

V由有限state/subset allocations取最大，且0≤V≤1。所有正阈值的双向映射给正最优值相等；若源V=0、targetV>0，则逆映射矛盾，故V0也精确保留。此value证明独立于第2–4节actual映射，没有把allocation与完整job执行混淆。

## 6. 度数、K、M与规模

每port z_{u,a}在旧菜单中只属于一个旧group g_a，即使该group在多个states重复出现u，也只记一个group membership；另外只属于至多两个相邻helpers。因此完整跨group资源度≤3，零权membership照样计数。旧states数量不动，helper恰2states，故K'≤max(K,2)。旧private总量原样不变，helpers W=1，所以normalized域保持。

没有M保持声明：旧的共享resource clique被分成旧groups与路径helpers的不同交互，任意输入上可能变化。也不声称helpers符合one-heavy/two-diffuse型；它们是heavy-only两singleton states，目标必须明确允许该matching core。

Σd_u≤旧incidence数L，因为每个不同(group,resource)membership至少对应一枚旧incidence。helper数≤L、ports≤L，每helper两台private机、三件原jobs、六条有限端。只复制旧二进制有理数与加入time1。两向映射逐原job/port/helper线性扫描，必要的hole编号来自实际外送或实际正值allocation；不搜索未知OPT、不按分母/参数倒数造对象。Dense完整矩阵按总行列显式填∞仍为源总位多项式。

既无hardness源也无外部论文新颖性认证。它只把一份已证明的flat菜单tiny-gap源传到resource度三，不能替代normalized源与partial decoder本身。
