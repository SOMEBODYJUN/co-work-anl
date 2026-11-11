# G v4 的窄范围修复：有限阈值 D 与全正阈值 A/B helper 族

G v4 已以明确源族 I_T 和固定 λ=2 的 M-LP 证书支付原人数 n=T²+T 下的 Ω(n^(1/4)) 存在性目标。该证据补全不改变既有 F→D、F→A、A→B 三条 accepted whole 关系的端点、推导或证据字节。本次三个核心均保持 linked；三条旧 canonical 边按原 path/SHA retained，四份旧 review/ledger 按原 SHA 逐字节复制到本任务保留写入范围，并在 supersession 中以 replaced 指向副本。另新增本窄范围审查和 reading-ledger，不另造逻辑边。

本报告对应 `boss6-mlp-g-scope-repair-b2229510e88b478a`。本地任务快照为 claimed/Boss6，request_id 为 `6eec589cecb548fdb99bb3d7c64e3f2f`；Root 已通知该认领确认 pushed。本 worker 只读 clone，所有新文件仅写指定 staging。没有 Git、队列、registry、旧 review/ledger/edge、native binding 或科学程序写入。

## 1. 精确身份、变化范围与来源层次

| 简写 | 当前对象 | 版本 | 本次角色 |
| --- | --- | --- | --- |
| D | M-a9534c70ffa74fca9a91cd270468de3f | 3 | 固定正阈值整数 DegreeThree 降度，核心 |
| A | M-16209762a32e42e48ec20b76381b5e9d | 1 | 同一 ∞ 输出的全正阈值整数/原始 CONFIG 桥，核心 |
| B | M-7bc9eab74ecd475db7df33c3f4b75e61 | 1 | 明确交域族 J_T 的精确 CONFIG/整数值与人数账，核心 |
| F | M-080d9b22ae87408f9a673a898c7a6dc3 | 4 | 已登记有限 unit-helper actual/CONFIG 证明，只读依赖 |
| G | M-b126c4b3ff29400589f7f38abdca4d85 | 4 | 原 InfDegreeTwo 存在性 gap，本次唯一改变 pin 的输入 |

另外两项原只读依赖 M-e52574ff126d4b128f222053c97bf596 v3 和 UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1 v1 未改版，其 DegreeTwo 域和后端 success 仅给阈值一半的边界沿用旧比较；本次不重开两个算法的完整证明。

用 `research_runtime.pin` 的规范 JSON 规则独立计算七项当前对象 pin，全部与本任务 input_pins 相等。与两份旧 done 收据记录的输入 pin 比较，唯一变化为 G：旧 v3 pin `290a361d6679820d0f4564c518bb120fd486835a7bf8cd08e6660438cf690029`，现 v4 pin `41317fd2c135289be3f3d2a44b38cdfc149eb6b2987b104845a176ef1abc017e`。F/D/A/B 的三个旧边端点 pin 全部仍为当前值，各条 evidence_pins 所指文件字节也全部未变。

本次直接从原 `maxmin.pdf` 导出并读印刷/PDF 页 6–8、12–13，另渲染并实看页13的脚注位置。页13正文展开的是 InfDegreeOne 的 Lemma 4.1；脚注2只声明 InfDegreeTwo 有相似论证可得 Ω(n^(1/4))，没有展开下面的完整 I_T。因此证据层次保持为：原 PDF 给存在性来源；A/B 主正文唯一节“8. 透明重构的 InfDegreeTwo 原 gap 家族”给明确 I_T 和全部原始 CONFIG/整数证明；G 新 evidence 所指 H 正文唯一节“5.3 原人数下的旧 InfDegreeTwo 存在性目标”给固定 λ=2 的 M-LP 证书和人数指数。本次没有把历史 review 中所记的扫描、外部 scratch、旧程序或整篇 PDF 阅读重新说成本 worker 的新阅读。

H 的正式正文为 `archives/unrelated-machines/state/定理/无限helper链对阈值规范化MLP的全正阈值双向保持--定理.md`，SHA256 `f07cd5f7128a9e8ac0f4667b8e69f5d89905b8d4e4d999edd090612cb95a9dfb`。本次按 G 的正式 evidence 读取该文件，使用其规范化、固定 λ 证书及 cap 边界作范围核对；不把 H 或 cap 反族 C 新添为本包三条旧边的逻辑前提，也不需要为保留这些旧边增加 read endpoint。直接 M-LP 桥与 cap 反族已有独立完整证明，不能再记作数学 open。

## 2. 原 I_T 的明确输入、精确值和 n^(1/4)

对整数 T≥4，取 T 个 block。block r 有 root a_r 和 T 名 b_(r,k)，以及 T 件 u_(r,k)、T 件 w_(r,ℓ)。a_r 对本 block 全部 u 值一；b_(r,k) 对自己的 u_(r,k) 值 ∞、对本 block 全部 w 值一；另外 T−1 件 B_r 只对相邻 root a_r、a_(r+1) 值 ∞。其余估值为零。原人数 n=T²+T，物品数 m=2T²+T−1。每物品 ∞ 度至多二，原玩家 ∞ 度也至多二；w 的总正度是 T，不能改称 DegreeTwo。

原始 CONFIG(T) 的完整证书是：root 的 full-u 配置质量 1/T；B_r singleton 给左 root 质量 (T−r)/T、右 root 质量 r/T；每个 b 的自己 u singleton 质量 1−1/T、full-w 配置质量 1/T。内部 root 的两侧 B 质量为 (r−1)/T+(T−r)/T=(T−1)/T，端 root 同样；故每行质量一。u 总边际为 1/T+1−1/T=1，w 为 T/T=1，B 的两端之和为一。全部配置在原值上达到 T。

若 s>T，每个 root 的有效配置都必须含 B，因为全部有限正端总值只有 T；T 个 root 所需 B 边际至少 T，而 B 总容量仅 T−1，故 ConfigOPT(I_T)=T。

任一最低效用 V>0 的整数分配有一 root 没拿 B。设它拿 s 件 u，则 s≥V；相应 s 位失去唯一 ∞ 物品的 b 只能分享 T 件 w，故 sV≤T，从而 V²≤T。最低值有限且为整数，所以 OPT≤q=⌊√T⌋。反向在每个 block 让 root 取 q 件 u，失 u 的 q 位 b 各取 q 件互异 w（q²≤T），其余 b 取自己的 ∞ u，即得 OPT≥q。故 OPT(I_T)=q。

因此原始 CONFIG/整数比恰为 T/q。由 q≤√T、n=T²+T≤2T²，

\[
T/q\ge\sqrt T\ge2^{-1/4}n^{1/4}.
\]

这是原人数 n 下的存在性族，且 q≥2；既不是每个 InfDegreeTwo 实例都具有此 gap，也不是 hardness 或该类 tight 上界。

## 3. 固定 λ=2 的 M-LP 见证怎样补齐 G

依原 PDF Definition 2.2，给目标 M>0、λ≥1，先令原端 p≥M/λ 的规范化值为 M，其他端不变；M-LP 要求物品容量 Σ_i x_ij≤1、大端质量加 z_i≥1、小端值和≥Mz_i、小端 x_ij≤z_i，以及非负性。大小分类是玩家–物品端的分类。

取同一原 I_T、目标 M=T 和固定 λ=2。因为 T≥4 时 1<T/2，全部单位正端仍是 small，原 ∞ 端是 big。故规范化没有把额外有限旧端变成 big，InfDegreeTwo 的相关端点条件保持。置

\[
z_{a_r}=z_{b_{r,k}}=1/T,\qquad
x_{a_r,u_{r,k}}=1/T,
\]
\[
x_{b_{r,k},u_{r,k}}=1-1/T,\qquad
x_{b_{r,k},w_{r,\ell}}=1/T,
\]

并把 B_r 的两端 x 置为 (T−r)/T、r/T，其余 x=0。各 root 与 b 的 big 质量都是 1−1/T，加 z 后为一；每行 small 值和是 T·(1/T)=1=Tz；每个 small x=z；各物品容量正如 §2，恰为一。于是全部 M-LP 约束逐项满足。也可从 §2 的 CONFIG 证书，把含 big 的配置剪为一个 big singleton、保留全 small 配置，取 small 配置质量为 z 得到同一证书。

这已给 M-LP(T) 可行，连同原整数 OPT=q 和原人数 n，支付 G 所需的另一条 Ω(n^(1/4)) 存在性。若要求这个固定 λ=2 模型的精确最高阈值，M>T 时单位端仍 small；root 的 small 约束给 Mz≤Σ_kx_u≤Tz，逼 z=0，再由 T 个 root 需要至少 T 的 big B 质量而容量仅 T−1 排除。因此该族在 λ=2 时 M-LP 最高阈值也恰为 T。

这里 CONFIG 与 M-LP 各自对同一明确族得出了相应结果，不推出它们在一般输入或所有阈值上同值。该论证只用 CONFIG→规范化 M-LP 的正向证书或直接约束核验；没有用任何无条件 cap-M-LP(M)→原值 CONFIG(M/2) 逆桥。

## 4. 新人数 N、CONFIG 迁移及有限 helper 边界

将 A 作用于上述明确 I_T，只对 T² 件正度 T 的 w 建 ∞ helper 链。每件增 T−1 名 helper 和 T−1 件净新增物品，故 S=T²(T−1)、N=n+S=T³+T、物品数 M_items=m+S=T³+T²+T−1。A 的同一输出对全部有限正阈值保持 INTEGER 与原始 CONFIG，所以 J_T 的 OPT=q、ConfigOPT=T。物品总正度≤3，物品与玩家的 ∞ 度均≤2；玩家总正度没有三上界。全部新 helper 计入人数和最低效用目标。

由 T³≤N≤2T³ 与 √T/2≤q≤√T，

\[
2^{-1/6}N^{1/6}\le T/q\le2N^{1/6}.
\]

因此 B 的精确显式 CONFIG 族为 Θ(N^(1/6))。不能把原 n=T²+T 换成新 N=T³+T 后保留 1/4 指数；本包保留的 A→B whole 关系只承诺它原来确证的 INTEGER/CONFIG 整句，不把新 H 的 M-LP 结论混进旧边。

F 经缩放的有限 helper H>0 版本，仅在 0<s≤H 正向保持 INTEGER/CONFIG。至少有一条 d>3 链时，s>H 的每个 helper 有效配置必须耗两份副本（s>2H 时根本没有有效配置）；故 helpers 总边际至少 2(d−1)>d，INTEGER 与 CONFIG 都不可行。若完全没有降度物品，输出是原输入，不能套有限 H 截断句子。D 只要给定 t 的整数合同，因此 helper=t 已足够；A 要求先造同一输出再对所有 s>0 保持，必须用符号 ∞ 的相应证明。逐 s 另造 J_s 不等于同一 J_∞ 的量词。

这一“s>H 不可行”不是 cap M-LP 的结论。H 正文 §4 的 d=4、H=1、目标 M=4/3、λ=1 例中，三位 helper 都取 z=1，相邻两端 x 依次为 (1,1/3)、(2/3,2/3)、(1/3,1)。每个副本占用一，每行小端和为 4/3，x≤z。四位旧 owner 各取自己的私有值100 big 物品即可补齐完整 M-LP 证书，而同一输出 INTEGER/CONFIG 最高阈值仍为一。对一般 λ，有限 helper 在 M≤λH 时被规范化为 big；这是 M-LP 的相应正向区间，不能改写为原值 CONFIG 的阈值区间。

另按 H 正文 §3.3 的 n=4 cap 反例，三件共享值3/4、每玩家一件私有值7/16，在 M=1 取共享 x=1/4、私有 x=1、z=1，每行值9/16+7/16=1。原 CONFIG 的最高阈值为7/16，因为超过该值时四行各需共享物品而只有三件容量；故原 CONFIG(1/2) 不可行。此精确边界否定无条件 cap 二倍逆桥，并不否定 §3 的固定 λ=2 证书或 G 的存在性目标。

## 5. 三条旧 whole 关系为何全部 retained

| 原边 | 本次直接核对的承重数学 | 当前处置 |
| --- | --- | --- |
| F→D：um-826e-unit-helper-path-to-fixed-threshold-degree-three | 固定 t 归一到一、必要时原 ∞ 端封顶 t、逐物品 owner-copy matching；d−1 helpers 至少占 d−1 份，反投影至多一份服务原玩家；只改 d>3、精确 counts 与有理输入/t 位复杂度 | accepted whole 原字节保留。G 不在端点或必要证据中；固定整数阈值不需要新 M-LP 桥。 |
| F→A：boss6-finite-unit-path-to-all-positive-infinity-chain | 固定输入先造同一 J_∞；逐 s 以 H≥s 辅助复用有限证明；hole/prefix helper 边际为 1−w_r、旧边际 q_r≤w_r；反向总容量；∞ 端置链端点、counts、见证支持与位长 | accepted whole 原字节保留。新 cap 边界反而确认不能把 F 的有限 H 直接当全阈值结果；旧边已明确此区别。 |
| A→B：boss6-infinity-chain-to-exact-intersection-config-gap | 明确 I_T 的全部性质由直接 evidence 已付，再用 A 保精确 INTEGER/CONFIG 目标；只降度 w，新增人数 S 全计，得到 N 的 1/6 指数 | accepted whole 原字节保留。G 从来没有承担这条精确族迁移的必要前提；G v4 补证不改变 B 的人数或模型。 |

这三条边的 endpoint_pins 和 evidence_pins 均已逐项与当前字节核对；本包不改任何语义、绑定字段或 review_digest。没有需要通过重绑才能纳入的新端点或证据。两份旧 review/ledger 保留其当时的 G v3、历史读取范围、F publication refresh 和原路由叙述，作为历史证据原样保留；本报告给出当前 G v4 的补充范围，不能倒写旧文冒称当时已读新证明。

原 D 收据中的实际后续任务 `boss6-inf-chain-transfer-3b-ea6be0c00b1186cf` 继续保留为既有关系交付路由。H/C 数学正文已有完整证明；此路由不表示数学尚未证明，也不影响本包三条旧 whole 关系。Root 已确认原 3B worker 的最终资产成熟并独立接受其 ALL{A,B}→G whole 结果；本包不以暂时 claimed/done 状态猜测其发布回执，不另建未知后续任务。

## 6. 字节处置、实际阅读与发布界限

两个 superseded 任务的全部七项 prior_assets 均逐项处置：三条旧 canonical 边以原 path、原 SHA 列入本收据 assets，disposition=retained；四份旧 review/ledger 原样复制到本任务保留写入目录，复制品 SHA 与原文件完全相等，并以 disposition=replaced、replacement_paths 指向该副本。此处 replaced 只调整新收据资产路径以满足写入范围，不表示数学内容或历史阅读记录发生替换。四个副本名为 retained-a-b-review.md、retained-a-b-reading-ledger.json、retained-d-review.md、retained-d-reading-ledger.json。已发布的原文件完全未改动，三条 retained 边仍引用历史原路径；没有 retired 或遗漏项。新收据在保留三条旧边外，列入四个字节相同副本及本 review/reading-ledger，共九项资产；收据不列自身为 asset。

本次实读包括：任务定义与当前七对象合同；两份旧 done 收据；三条完整边 JSON；两份旧 review；两份旧 ledger 的已声明阅读范围、版本/pin、历史限制与 publication-refresh 元数据；F 主正文、A/B 主正文、对应独立复核、H 正文、文献汇编全文；PDF 指定五页及页13图像。五篇旧 F evidence 的原先逐段实读范围以原 ledger 保留，本次只核其 SHA，没有把这些旧扫描重新宣称为新实读。未重跑科学程序、证书、枚举或 LP solver，亦未重审 DegreeTwo/VW 原始算法证据闭包。

所有输入/资产精确 SHA、当前 pin、各文件实际读取范围及限制另见本 reading-ledger。数学判断来自上述约束、配置质量、容量、matching、阈值量词和人数账的直接核验。此次路径修复只复制既有字节并更新资产处置与引用，没有新增数学阅读或程序重放。Git、native edge-bind/check、checkpoint、done 与集成均由 Root 按实际需要执行；本 worker 不冒称已经发布。
