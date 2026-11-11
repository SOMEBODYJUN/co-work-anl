# InfDegreeOne、InfDegreeTwo 与降度交域：当前合同及松弛边界复核

任务：`boss6-mlp-g-scope-repair-72191b93dbe23cdd`；作者：Boss6 的 fresh 数学 worker。本文定向替代旧任务 `unrelated-machines-3a-3a-9a8dd2493600ac1c` 对当前输入的审读说明。旧 review 原字节另存于本目录 `prior-review-preserved.md`，旧路径不改写。完整构造与证明在下文重新自足展开，不以历史快照替代当前审读。

本轮实际得到的数学句子是：三个明示族分别有原始配置 LP 最高阈值 T、整数最优值 q=floor(√T)，但人数依次为 T³+T²+1、T²+T、T³+T；前两族又各有独立的阈值规范化 M-LP(T) 可行证书。由此分别得到 InfDegreeOne 的 Ω(n^(1/6))、InfDegreeTwo 的 Ω(n^(1/4)) 和 DegreeThree∩InfDegreeTwo 的 Θ(N^(1/6)) 明示家族。它们共享 H_T 的内部瓶颈，却没有由此支付三个存在性合同间的完整蕴含。交付保留一条 `motivates/context` 边，核心覆盖为 `isolated-after-review`。

## 1. 当前端点、模型与规范化

当前核心是 `M-90610eea6c6447188c03208eaa549254` v3；共享比较端点为 `M-b126c4b3ff29400589f7f38abdca4d85` v4（下文 G）及 `M-7bc9eab74ecd475db7df33c3f4b75e61` v1。三个完整登记记录已读。G v4 的新增证据明确区分原 PDF 的 InfDegreeTwo 脚注声明、透明 I_T 重构和阈值规范化 M-LP 的独立证书。旧 edge 使用 G v3 的 pin，须以当前输入重绑。

所有实例均为有限非空玩家集、有限不可分物品集、非负加性效用，每件物品至多一位受领者，允许留空。未列估值为零；符号 ∞ 表示单件可达到任意有限正阈值。非负性允许把留空物品任意补分而不损害已达最低值。InfDegree 是每物品的 ∞ 玩家端数，Degree 是每物品的正值玩家端数；它们不自动限制玩家侧的度。

在原估值 p 上，CONFIG(s) 使用每位玩家全部价值至少 s 的子集 C，变量 y_iC≥0，要求每行配置质量之和为一，每件物品在全部配置中的总边际至多一。不同玩家的配置分布无须有共同整数实现。定义 ConfigOPT 为最高可行阈值；本文各族直接证明其值恰为 T。

为免把人数或物品数 M 与目标混淆，M-LP 的目标写为 L>0。固定有限 λ≥1，逐玩家–物品端作

\[
\widehat p_{ij}=R_{L,\lambda}(p_{ij})=
\begin{cases}L,&p_{ij}\ge L/\lambda,\\p_{ij},&p_{ij}<L/\lambda.\end{cases}
\]

重估后值 L 的端为 big，其余为 small；分类依赖玩家。原 PDF Definition 2.2 的全部约束为

\[
\sum_i x_{ij}\le1,\qquad
\sum_{j:\widehat p_{ij}=L}x_{ij}+z_i\ge1,
\]
\[
\sum_{j:\widehat p_{ij}<L}\widehat p_{ij}x_{ij}\ge Lz_i,\qquad
x_{ij}\le z_i\ (\widehat p_{ij}<L),\qquad x,z\ge0.
\]

没有额外要求每位玩家的全部 x 和为一。零端的 x 可统一设零。本文给 gap 证书时固定 **λ=2、L=T、整数 T≥4**。单位端满足 1<T/2，仍是 small；原 ∞ 端重估为 T，恰是原大端，没有新增大端破坏 InfDegree 条件。原值上的整数 OPT 与原始 ConfigOPT 始终按原 p 计算。

这里所需的安全接口仅是原始 CONFIG(T)→规范化 M-LP(T)。先把每个含 big 的正质量配置缩为其中一个 big singleton，无 big 的配置保留为小端集合；有效性保持，物品边际只下降。令 z_i 为小配置总质量，令 x 为缩整后的物品边际：big 质量+z_i=1，小值和≥Tz_i，每个 small x≤z_i，容量及非负性继承。因此正向接口完整成立。没有用一般同阈值等价，更没有用无条件的 cap-M-LP(L)→原值 CONFIG(L/2) 逆向说法。现有独立审查中关于 Theorem 2.3 的早期概括，只在当前 MLP 正文修订后的规范化和小端条件下使用；本轮 gap 推导不依赖该逆接口。

## 2. InfDegreeOne 的完整输入和 CONFIG(T) 见证

取整数 T≥4，K=T²。每份 H_T 编号 r∈{0,…,K−1}，有 root a_r、辅助玩家 b_r1,…,b_rT，物品 u_r1,…,u_rT 及 w_r1,…,w_rT。a_r 对本 block 全部 u 值一；b_rk 对自己的 u_rk 值 ∞，对本 block 全部 w 值一。另加 K 件 B_r，每件仅对对应 root a_r 值 ∞，并加中心玩家 c，对全部 K 件 B 值一。

人数和物品数是

\[
n_1=K(T+1)+1=T^3+T^2+1,\qquad
m_1=2TK+K=2T^3+T^2.
\]

u 只有对应 b 的一个 ∞ 端，B 只有对应 root 的一个 ∞ 端，w 无 ∞ 端。因此属于物品侧 InfDegreeOne。w 的总正度为 T，并非 DegreeTwo 或一般的 DegreeThree。

在 CONFIG(T) 中给每位玩家如下分布：

| 玩家 | 有效配置 | 质量 |
| --- | --- | --- |
| a_r | 本 block 全部 T 件 u | 1/T |
| a_r | singleton {B_r} | 1−1/T |
| b_rk | singleton {u_rk} | 1−1/T |
| b_rk | 本 block 全部 T 件 w | 1/T |
| c | C_ℓ={B_ℓ,B_(ℓ+1),…,B_(ℓ+T−1)}，指标模 K，ℓ=0,…,K−1 | 每个 1/K |

全 u、全 w 和每个中心 C_ℓ 的原值均为 T，∞ singleton 也有效。每个玩家质量和一；中心的每个配置是 T 件互异 B。每件 B 恰出现在 T 个中心配置中，所以中心边际为 T/K=1/T。加对应 root 的 1−1/T，总边际恰一。每件 u 的 root 和 b 边际为 1/T+(1−1/T)=1；每件 w 在 T 位 b 中各出现质量 1/T，总边际一。这支付完整有效配置及全部单物品容量，强于只写中心的分数期望效用为 T。

## 3. InfDegreeOne 的精确整数值与原始配置值

任何最低效用 V>0 的整数分配中，中心必须取得至少一件 B。假设它取得 B_r，则 a_r 没有自己的唯一外部 ∞ 物品。若它取得 s 件本 block 的 u，必有 s≥V；对应 s 位 b 失去各自唯一 ∞ 物品，只能共享本 block 的 T 件单位 w。要使这些 b 也至少达到 V，必须 sV≤T，故 V²≤T。中心的效用有限且为整数，所以整份分配的最低值有限且为整数；因此 OPT≤q=floor(√T)。

反向在每个 block 给 root 任意 q 件 u；失去这些 u 的 q 位 b 各给 q 件彼此不重叠的 w，共用 q²≤T 件 w；其余 b 各取自己的 ∞ u。给中心任意 q 件 B，q≤K，其余物品可留空或任补。所有玩家至少得 q，故

\[
\operatorname{OPT}(I_T^{(1)})=q.
\]

若配置阈值 s>T，每位 root 的全部有限正值物品总和仅 T，其每个有效配置必含自己的 B。K 位 root 的归一配置质量因此占满全部 K 件 B 的容量，而中心的任何正阈值有效配置也须含 B，矛盾。亦可先看每位 b 在 s>T 必含自己的 u，继而全部 u 容量耗尽、root 必用 B；这是旧 review 的同一容量论证。于是

\[
\operatorname{ConfigOPT}(I_T^{(1)})=T.
\]

本族的原始配置 gap 恰为 T/q，q∈[√T/2,√T]，故为 Θ(√T)。因为 T³≤n_1≤2T³，特别 T/q≥2^(−1/6)n_1^(1/6)。这不声称 InfDegreeOne 全类的 tight 上界，也不声称 hardness。

## 4. InfDegreeOne 的独立规范化 M-LP(T) 证书

在 §1 固定的 λ=2、L=T 下，直接取

\[
z_{a_r}=z_{b_{rk}}=1/T,\qquad z_c=1,
\]

\[
x_{a_r,u_{rk}}=1/T,\quad x_{a_r,B_r}=1-1/T,
\]
\[
x_{b_{rk},u_{rk}}=1-1/T,\quad x_{b_{rk},w_{r\ell}}=1/T,
\quad x_{c,B_r}=1/T.
\]

所有未列坐标为零。各 root 与 b 的 big 质量均为 1−1/T，加其 z 恰为一；各自 small 总值为 T·(1/T)=1=Tz，每个 small 坐标恰为 z。中心没有 big 端，z_c=1；其 small 总值是 K/T=T=Tz_c，每个 small 坐标 1/T≤z_c。各 u、w、B 容量按 §2 的同一边际恰饱和；非负性成立。因此所有 M-LP 约束逐项满足，确有 M-LP(T) 可行。

这是核心 M-LP gap 的足够下界：其最高可行参数至少 T，除以原值整数 q 得 Ω(n_1^(1/6))。没有从 ConfigOPT=T 自动断言 M-LP 最优值也为 T，也没有把中心错误地设为 z_c=1/T。若另改 λ 而把单位端升为 big，必须重新核大端度及原值解释，当前证明固定 λ=2 避开该变更。

## 5. InfDegreeTwo 的完整外层路径重构

现在取 **T** 份相同 H_T，编号 r=1,…,T；去掉中心，改放 T−1 件外部 B_r，每件仅对相邻 a_r、a_(r+1) 均值 ∞。人数和物品数为

\[
n_2=T(T+1)=T^2+T,\qquad m_2=2T^2+T-1.
\]

u 的 ∞ 度一，w 为零，B 为二，故在 InfDegreeTwo。这里的完整透明构造来自当前 helper/交域正文 §8，原 PDF 印刷页 13 脚注 2 只声明类似论证给 Ω(n^(1/4))，并未列出这条路径或全部证书。

CONFIG(T) 的 block 内部配置仍为 §2 的 root 全 u 质量 1/T、b 自己 u singleton 质量 1−1/T 和全 w 质量 1/T。外部 B_r 的 singleton 给左 root a_r 质量 (T−r)/T，给右 root a_(r+1) 质量 r/T。内部 root a_r 的外部质量为

\[
(r-1)/T+(T-r)/T=(T-1)/T;
\]

两端 root 也各有 (T−1)/T。每个 root 总质量一，每件 B 的左右边际和一；u、w 容量与前族相同。每个正质量配置原值至少 T，所以 CONFIG(T) 可行。

整数分配中只有 T−1 件 B，却有 T 位 root，故至少一位 root 没有任何外部正值物品。该 block 同样满足 s≥V、sV≤T，推出 V²≤T。该 root 的有限效用为整数，整个最低值也为有限整数，给 OPT≤q。在所有 block 分别给 root q 件 u，受影响 q 位 b 各 q 件不重复 w，其他 b 取自己的 ∞ u，外部 B 留空，即给所有玩家至少 q。故 OPT=q。若配置阈值 s>T，每个 root 的合法配置都必须含 B，T 行归一质量至少占 T 份 B 边际，但只有 T−1 件容量，矛盾。因此

\[
\operatorname{ConfigOPT}(I_T^{(2)})=T,\qquad
\operatorname{OPT}(I_T^{(2)})=q.
\]

同样按 λ=2、L=T，取所有 root 与 b 的 z=1/T；root 的各 u 边际1/T，b 的自己 u 边际1−1/T、各 w 边际1/T；外 B 坐标就是上述左右质量。每行 big 质量+z=1、small 值和=1=Tz、每个 small x=z，全部容量≤1。于是直接支付 M-LP(T) 可行，亦可用 §1 的正向配置接口得到它。由 n_2≤2T²，两个松弛的 gap 各至少

\[
T/q\ge\sqrt T\ge2^{-1/4}n_2^{1/4}.
\]

这支付 G v4 的完整存在性目标，分别证明两种松弛的下界，没有宣称它们在一般实例或所有阈值上同值等价。

## 6. 降度交域 J_T：完整结构、阈值证明与人数账

对 §5 的 I_T^(2)，仅把 T² 件总正度 T 的 w 作 ∞ helper 链。对某个 w（原正端为本 block 的 b_1,…,b_T），删除旧 w，建立 T 个副本 c_1,…,c_T；c_k 只对原 b_k 保单位值。新增 T−1 名 helper h_k，h_k 仅对 c_k、c_(k+1) 取值 ∞。其他 u、B 不动。

对任意有限 s>0，整数正向：若旧 w 给 b_r，给其 c_r；给 k<r 的 h_k 以 c_k，给 k≥r 的 h_k 以 c_(k+1)。这些 helper 得 ∞ 且避开 c_r；若旧物品未用，任选一处留空。原玩家值不变。整数反向：T−1 名 helper 在正阈值下必须取得 T−1 份互异副本，至多留一份正值服务原玩家，合回旧 w 不冲突。逐链同时处理，所以整数正阈值可行性双向保持，OPT仍为q。

配置正向也不要求联合整数实现。对一般 d 副本链，令 q_r 是旧 owner i_r 在旧 item 上的边际，Σq_r≤1。选 w_r≥q_r、Σw_r=1，令 W_k=Σ_(r≤k)w_r。旧玩家在各配置中只把旧 item 换为其专属副本；给 helper h_k 两个 singleton 配置，左质量1−W_k、右质量W_k。副本 c_r 的 helper 边际恰为1−w_r，连同旧 owner 为 q_r+1−w_r≤1。每名 helper 质量一，值∞，所以同一输出对所有有限 s>0 都合法。反向每名 helper 的每个有效配置至少含一份相邻副本，d−1 名 helper 共占至少d−1；d个副本总容量d使旧玩家总边际≤1。删零值物品后，每个旧玩家在该链每份配置至多含其唯一专属副本，合回旧 item 不制造重复，配置值和行质量保持。故 CONFIG 在全部正阈值双向保持，ConfigOPT仍为T。

对当前具体 CONFIG(T) 证书，每个 w 的各旧 owner 边际都是1/T，可取均匀 hole w_k=1/T。第k名helper的左/右singleton质量分别为(T−k)/T、k/T；每个副本原玩家边际1/T加helper边际1−1/T恰为一。这给出完全显式的 J_T 证书。若只需要规范化 M-LP(T) 下界，也可给旧玩家保同样专属副本 x,z，给每个 helper z_h=0、两个 big 坐标为(T−k)/T、k/T，直接满足全部五类约束；不以 CONFIG 桥冒作一般 M-LP 桥。

新增人数为 S=T²(T−1)，故

\[
N=n_2+S=T^3+T,\qquad
M=m_2+S=T^3+T^2+T-1.
\]

| 物品类型 | 原玩家正端 | helper 正端 | 总正度 | ∞ 度 |
| --- | --- | --- | --- | --- |
| u_rk | root值1、对应b值∞ | 无 | 2 | 1 |
| B_r | 相邻两个root均∞ | 无 | 2 | 2 |
| w端点副本 | 专属b值1 | 一名helper值∞ | 2 | 1 |
| w内部副本 | 专属b值1 | 两名helper均∞ | 3 | 2 |

因此 J_T 属于 DegreeThree∩InfDegreeTwo，值域仍为{0,1,∞}。本族玩家侧∞度也≤2：root至多两件B、b只有自己的u、helper恰两件副本；玩家侧总正度却可为T+2或T+1。全部 helper 都计入最低效用目标与N。见证的权重分母为T，显式输入和见证编码poly(T)，没有声称poly(log T)压缩构造。

由于 T³≤N≤2T³，精确原始配置比值 T/q=Θ(√T)=Θ(N^(1/6))，且至少2^(−1/6)N^(1/6)。不能沿用原 n_2=Θ(T²) 的1/4指数；当前交域合同也没有该指数。

## 7. 逐合同比较与关系范围

| 比较 | 实际所得 | 不能据此支付的整条合同 |
| --- | --- | --- |
| InfDegreeOne v3 与 G v4 | 共同H_T、配置质量1/T、失去大物品后V²≤T；外层由T²个私有B加中心改为T个root的缺一B路径 | 核心存在性合同本身不提供双∞外B、路径概率或新人数；类包含至多保留较弱Ω(n^(1/6))，未支付G的1/4目标。反向较宽类存在性也不指定∞度1实例。 |
| InfDegreeOne v3 与交域v1 | 两族比值均为Θ(人数^(1/6))，来源block与整数瓶颈可比较 | 同指数不等于同结构。核心w正度T不满足DegreeThree；J_T的外B和内部副本有两个∞端，不满足InfDegreeOne。任何方向都未给保持所有目标条件的迁移。 |
| G v4 与交域v1 | 本文对明确I_T^(2)与J_T给完整正阈值容量证明及N=T³+T | 此处调用的是明确源族及链构造的完整证明，不把宽泛G存在性一句单独充当指定I_T的全部证据；不重复另发已有交域迁移边。 |

本轮保留的语境边说的是：InfDegreeOne 的 H_T 内部构造与自足块瓶颈，提供 InfDegreeTwo 外层路径重设计的可复用模板。它不声称两个存在性定理逻辑互推，不是同一输入的不变映射；因此不设 whole_result 或 contribution，也不将它列入核心逻辑 edge_ids。

本次三份合同和三个指定明示族的比较已闭合。没有证明一般不可能存在其它 InfDegreeOne↔交域构造。若未来明确研究把J_T改成∞度1，则必须另支付新结构、完整配置证书、整数上界和全部新增人数；这只是精确剩余数学要求，不是本轮已确认需要新任务承接的对象对。

## 8. 旧资产的逐项处置

旧 edge `map/edges/unrelated-machines-3a-3a-9a8dd2493600ac1c/one-gadget-to-two-context.json` 替换为本目录当前 edge。旧边的数学用途仍有效，旧endpoint pin不再绑定G v4；新边保留H_T、循环配置、路径质量、两族指数及不蕴含边界，补明λ=2和两种松弛分别支付的证书。旧文件保持原字节。

旧 review `map/edges/unrelated-machines-3a-3a-9a8dd2493600ac1c/review.md` 在当前交付中由本完整review及 `prior-review-preserved.md` 替换。后者与旧review逐字节同SHA，保全旧审读的全部数学、来源定位和历史版本说明；当前review另完整重写构造、阈值与交域证明，并修正为G v4。旧路径保持原字节，不覆写历史结论。收据对两个旧asset各给replaced与本批内replacement_paths。

## 9. 直接实读证据及使用边界

本次完整读取项目AGENTS、worker提示词、IMPLEMENTATION（分段补读第三阶段与替代规则）、当前task、旧task和旧receipt、旧edge和旧review，以及三个当前完整登记合同。正文实读为共同文献全文106行、∞helper/交域定理全文155行、独立复核全文274行、阈值规范化MLP定理全文281行；任务单列的§8与§5.3均实际读到，去重为各自全文读取。独立复核的历史source段落不是本次新读取其所列全部文件的声明。

对冻结 maxmin.pdf 直接逐页 pdftotext -layout 实读印刷页4、6、7、8、12、13；另外渲染并目视印刷页4、7、13。印4核物品侧定义，印6核Definition2.1及τ=L/λ重估，印7核Definition2.2式(4)–(8)和Theorem2.3印刷措辞，印8核其证明的M−p_max目标及转换语境，印12–13核{0,1,∞}与重估后仍需类条件、Lemma4.1和脚注2。49页是PDF总页数，本轮没有审读49页全部算法。页码由渲染页眉核实，不把PDF序号和印刷页默认为不同。

所有输入、读取范围、实际SHA及PDF提取文本/图片的临时路径列于reading-ledger.json。只运行来源提取、渲染和字节摘要，没有重跑旧数学程序、枚举或科学计算。另一个fresh窄审独立复核了两族的完整证书、中心z_c及人数账，未发现缺口；本文仍给出可直接检查的完整数学。

## 10. 覆盖和接续处置

核心M-906…在本轮比较范围内为isolated-after-review：有已接受语境关系，未发现支付另一端完整合同或其指定组成步骤的逻辑边。InfOne/G对象对以外层结构、人数指数及当前G来源修订的上述结果关闭；InfOne/交域对象对以总度/∞度分离和完整新增人数账的上述结果关闭。当前任务没有显式follow-up overlap列表；这两个已解决的实际比较逐对记录于收据additional_comparisons，closed_overlaps仅用于任务指定的deferred对故置空，follow_up_tasks为空。数学身份、版本和证据均已辨清，不使用needs-decision掩盖一般未给出的桥。
