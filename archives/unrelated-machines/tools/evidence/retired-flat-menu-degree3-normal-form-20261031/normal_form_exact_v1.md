# Normalized flat 菜单的三态/资源度三实际正规形：冻结 Exact v1

ID: UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1。
作者：boss11内部typed_edge_gap，2026-10-18。本页为前述资源路径归约的同一路线扩展，先给完整构造与待独立攻击的量词，不附作者证明；不另立资产树、不称新原创。

## 1. Source

非空显式groups G，每group有K_g≥1个indexed states s。每state是distinct资源集合S_gs与非负二进制有理权p_gsu，严格归一化Σ_up_gsu=1。不同states可重复、权可0，资源跨group度、K_g、support与group interaction均不受限。源普通P完全采用flat规则：每state一私有机器，每group unit selector只到该group的state机器；每state-resource incidence一原job（private p，唯一resource unit），其余∞。没有其它jobs/预载。

V是给每group选一个原indexed state，并分给它该state内一个资源子集、跨groups不交，所能达到的最大最小private质量。归一化保证OPT(P)=2−V，1≤OPT≤2；本Claim亦要求通过全部原jobs实际映射核对，不能仅引用分数值。

## 2. 显式三态预处理

对每原group g，取叶恰为它全部indexed states的满二叉树B_g；K_g=1时为单叶。树中每个顶点v变成一个新flat group Q_v。对每个非root顶点v添加一枚全局fresh resource a_v，称own-resource。所有B_g、a_v及旧资源互不混淆。

每个Q_v的完整菜单如下：

- root若是internal，有两个singleton states，分别为两个child的own-resource {a_child}，权1；没有own state。
- 非rootinternal，有三个singleton states：{a_v}、{a_left}、{a_right}，每个权1。
- 非rootleaf，对应原indexed state s，有两个states：own singleton {a_v}权1；及原state S_gs、原权p_gsu。
- root若本身是leaf，只有原state s、无own-resource。

每个indexed state按同一flat规则实际生成private machine、unit selector与独立incidence jobs。原state/private/incidence可在leaf中沿用其身份；每原selector的目标资格改为对应root的新state机器。所有新增singleton/job/resource都显式生成，不使用抽象OR、免费激活、未知最优见证或任务复制执行。每target group至多3states，全部仍归一化。

此步可能把一个旧group内多state的同资源membership拆成很多leaf-groups，不声称资源度保持。

## 3. 再执行资源路径降度

对第2节所得全部资源按实际incident groups分ports，并加相邻port的heavy-only二态singleton helpers，完全采用 `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1` 的显式矩阵规则。顺序必须是先三态预处理、后资源降度。最终每group至多3states、每resource跨全部菜单至多3groups，仍是normalized flat ordinary P*。

## 4. Exact Statements / Partial Decoder

(A) 对每个正阈值v∈(0,1]，source有whole-state partial allocation value≥v iff第2节中间实例有 iff最终P*有。存在det总位poly的双向actual见证映射，所有被选择的原state及原资源子集都保留/可解码；不只full-state情况。

特别逆向要求：给任何target value≥v分配，从每原group的B_g root实际被选择的singleton出发，可沿资源阻塞逐层解码到一个实际采用原diffuse state的leaf。不得预设target只激活一条路径；未选分支可自行改态，但解码不能因此失败。所提取的各原group leaf资源子集仍全局不交。

(B) V(P*)=V(P)，包括V=0边界。

(C) 给任意完整source actual σ，若Cmax=C<2，可det bitpoly构造target全部原jobs actual σ*≤C；给任意完整target actual τ*，若Cmax=C<2，可det bitpoly解码source全部原jobs actual τ≤C。映射不能只给资源子集后省略unselected states的原incidence jobs，也不要求目标schedule事先对应某个正规路径matching。

(D) 精确保actual ordinary OPT：OPT(P*)=OPT(P)，包括OPT=2端点。最终P*至多3states/group、resource degree≤3；输出大小为源显式输入总位长的多项式，无按分母/参数倒数展开。

所以任意normalized flat菜单源的tiny-gap困难性若能独立闭合，可不失gap移到(K≤3,Δ≤3)域；本正规形不创造这样的源，不覆盖未归一化Σp>1的任意Santa Claus行，不解决UM-TARGET。它没有把所有group变成one-heavy/two-diffuse型：内部groups可有三枚heavy singleton states，leaf有one-heavy/one-original-state，资源路径helpers是two-heavy。

## 5. 证据/范围

只用于给定flat结构，不将一般UM输入免费分解到此结构；M不声称保持。own-resources只属owner与其parent，fresh命名是实际新资源而非原资源的别名。完全显式binary tree有2K_g−1个vertices，新增own资源2K_g−2；中间states和新增singleton incidences均O(ΣK_g)。资源路径处理再按其中真实memberships生成，dense完整矩阵仍poly。

本页未依赖外部degree3 Santa Claus论文的新颖性声明，视为selector/matching路径的直接重构。尚无hardness claim、软件大枚举或外部认证。
