# 仿射线两两独立的结构边界：单 primary 精确可解与 simplex 趋二族

本页合并两个互补范围，保留两个独立 ID。§1–2 的 one-primary unit escape 由 general_query_response_review 先独立 Exact-first 重构、再实际读作者 Proof；§3–8 的 simplex 精确族由 bicriteria_set_packing_bridge 按同样次序审查。两项作者均为 rainbow_gap_source，root 均参与先行讨论，不记作 blind reviewer。typed_edge_gap 在实际全文读两组 Exact、作者 Proof 和相应审查后编写本合并稿，不冒充新的独立数学审查。

本稿尚待 root 实际全文通读；复制为 canonical 后，将分别按上述范围路由 final scope actual-read，当前不预称最终页面已获认证。标准有限域、条件化和整数匹配不声称原创。两项都是指定显式对象的结构结论；没有导入 source hardness、未知 NO 解码或新 UM 近似算法，`UM-TARGET-v1` 仍 OPEN。

## 1. 单 primary：完整接口与独立合同

- **ID / version**：`UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1`。
- **Objects / domain**：素数 R≥2；下面明确的 tagged affine-line 菜单、一个 main、每 helper 恰一个 primary、任意共享辅助变量、所有 helper states onehot、main states 任意非负 norm-one 权。完整 indexed states、完整 lines 和零权 incidences 均显式保留。
- **Quantifiers / input**：对每个满足本节条件的输入、main 任意预先指定的原 indexed state，给定满足所述边际等式的有理局部分布；也允许只以实数可行性作为数学前提。不提供全局 source 标签赋值或实际调度见证。
- **Exact / conclusion**：可确定性总位多项式选出原 helper states，各给一个不同正资源，main 获得其指定 state 的全部正资源；全部 groups 质量恰 1，故 V=1。相应完整 ordinary P 的全部原任务可实际调度于 C_max=1，且 OPT(P)=1。
- **Assumptions / dependencies**：无复杂度假设；只用有限分布条件化、仿射线几何和有限二部匹配。可选的接口证书检查使用显式 rational feasibility LP，不是实际 UM 或配置求解 oracle。
- **Definitions / scope**：V 和完整 P 定义于 §1.3。结论不要求所选完整几何 supports 不交，不输出全局 source-CSP 解；不覆盖多 primary helper、diffuse helper、main 参加辅助变量、额外 groups、预载或缺少指定条件边际的模型。
- **Evidence / counterevidence / status**：原 Exact SHA256 `59e71e7d7c496b9dda2a993af5d0253072601190b5e78a8599dd06093fb47bbd`；作者 Proof `2b4d738099afcc78a4d14c42a7142a08a6224f5b9e8fc6ae3a6f463c9e837c6b`。general 的独立重构 `f535ef37960e5a8b30127127514db9035b69482c66c47f157eb26163c539a3a0`、作者读后 `30a76a6681627d137384cb4961b3d61fe46ede5af9fc7a0055e2a018cdcbc628`；精确域内未留 standing objection。本合并稿的最终 scope 审尚待实际读取；无新测试、生产实现、外审或全球新颖性认证。
- **Related files / distinction**：与本页 simplex ID 共用 tagged-line 和完整 P 语言，合同分别保留；§3–8 的多 primary 反例不属于本 ID 的域。

### 1.1 变量、截距和完整菜单

在 F_R 上运算。primary 变量集记为 𝒫，辅助变量集记为 𝒜，两集不交；𝒫 非空，𝒜 可空，也可含 unused variables。普通处理矩阵仍记 P。每个变量 x 拥有互不混同的完整资源 plane

\[
U_x=\{(x,z,y):z,y\in\mathbb F_R\}.
\]

groups 恰为 main M 与有限 helper 集 H，H 可空。M 参加全部 𝒫，不参加 𝒜。每个 helper h 指定唯一 primary u(h)∈𝒫，其变量恰为 X_h={u(h)}∪A_h，A_h⊆𝒜；无重复变量，无其它 primary 或额外 groups。辅助变量可以由来自不同 primary blocks 的 helpers 任意共享。

每个实际 incidence (g,x) 给固定截距 j_x(g)∈F_R；同一变量上不同 groups 的截距互异。因此 primary 至多有 R−1 个 helpers 加 main，辅助变量至多有 R 个 helpers。main 截距不必为 0，算法不改输入编号。

每组给非空显式 indexed-state 菜单 S_g。state s 给每个 x∈X_g 一个 slope label a_(g,s)(x)∈F_R；完整资源集为

\[
T_{g,s}=\bigsqcup_{x\in X_g}
\{(x,z,a_{g,s}(x)z+j_x(g)):z\in\mathbb F_R\}.
\]

每个 state-resource incidence 给非负 binary 有理私权 p_(g,s,r)，每 state 的私权和恰 1。main 私权可任意依赖完整 state，可有多个正 cells。每个 helper 的每个原 indexed state 恰有一个私权为 1 的正 cell，其余完整 line incidences 私权为 0；该 onehot cell 可依赖整个 state 和全部输入，不预先绑定某个 parking 点。即使 label vectors 重复，仍保留 indexed-state 身份与相应全部任务。

### 1.2 局部边际前提

每个 helper h 的原 state table 上给非负分布 λ_(h,s)，总和 1，满足对全部 t∈F_R

\[
\sum_{s:a_{h,s}(u(h))=t}\lambda_{h,s}=\frac1R,
\]

并对每个 x∈A_h、全部 t,a∈F_R 满足

\[
\sum_{\substack{s:a_{h,s}(u(h))=t\\a_{h,s}(x)=a}}
\lambda_{h,s}=\frac1{R^2}.
\tag{1.1}
\]

这里只要求 primary uniform 及其与每个 auxiliary 的 pairwise uniform；不同 auxiliaries 不要求联合独立。main 不需要局部分布前提，允许某些 helper states 的 λ 为零。也可以只承诺这些有限等式有非负实解；§2 的直接状态图算法无需先取出 λ。

### 1.3 分配量与完整普通 UM 编码

对本页任一 norm-one 菜单，定义

\[
V=\max_{\substack{s_g\in S_g,\ A_g\subseteq T_{g,s_g}\\
A_g\text{ 跨 groups 两两资源不交}}}
\min_g\sum_{r\in A_g}p_{g,s_g,r}.
\tag{1.2}
\]

允许任意 partial subsets，不要求分配完整 support。完整 ordinary P 始终按以下规则定义，后文 simplex 也使用同一规则：每个 indexed state 一台不同 private root，每个 tagged resource 一台资源机；**每 group 一枚** unit selector，可在该组全部 state roots 执行。每个 state-resource incidence 各是一枚不同原任务，在自身 private root 的真实时间为 p_(g,s,r)，在对应资源机的真实时间为 1，其余时间 ∞。无其它任务、预载、机器或免费外送资格。

所有零私权 incidences、λ 为零的 states、未选 states 及其任务都在 P 中。设 n=1+|H|、S=Σ_g|S_g|、I=RΣ_g|S_g||X_g|，则 P 恰有 S+(|𝒫|+|𝒜|)R² 台机器、n+I 枚任务、S+2I 个有限资格；私权 0 的端仍计入有限表。

## 2. 条件化 Hall、直接状态图与全部原任务的 unit 调度

固定任意输入指定的 main state s_M，写 t_u=a_(M,s_M)(u)。对每个 h 只条件化其唯一 primary label 为 t_(u(h))：

\[
\mu_{h,s}=
\begin{cases}
R\lambda_{h,s},&a_{h,s}(u(h))=t_{u(h)},\\
0,&\text{否则}.
\end{cases}
\]

primary marginal 保证 μ_h 是分布。由 (1.1)，其每个辅助 label 仍各自 uniform：对 x∈A_h，Pr_(μ_h)[a_(h,s)(x)=a]=1/R。此处只条件化一个 primary；没有从 pairwise independence 推出多坐标条件化后的均匀性。

令 e_h(s) 是 h 的唯一正 cell，定义证明用质量 f_(h,r)=Σ_(s:e_h(s)=r)μ_(h,s)。每个 helper 的行和为 1。以下核每个资源列和≤1，并避开 main 的全部正 cells。

在 primary u 上，所有相关 helpers 与 main 的斜率均为 t_u，但真实固定截距互异，所以其完整平行线两两不交。某 primary cell 最多被一个 helper 的条件状态正质量使用，总量≤1；helper 的 primary 正 cell 也避开整个 main 线。main 不参加辅助变量，所以 helper 的辅助正 cell 同样避开 main。

在辅助变量 x 的 cell (x,z,y) 上，若 z≠0，h 的线经过该 cell 必须满足唯一斜率 a=(y−j_x(h))/z。其条件概率为 1/R，而事件 e_h(s)=(x,z,y) 是线经过事件的子集，故 f_(h,(x,z,y))≤1/R。同一 x 至多 R 个 helpers，列和≤1。若 z=0，线经过该 cell 当且仅当 j_x(h)=y；截距互异保证至多一个 h，其列贡献≤1。零横坐标不能靠 uniform slope 的 1/R 界替代，必须使用这个截距论证。

现在直接从原 state table 建二部图：左边是 helpers，右边是原资源；只要 h 的某个原 state s 满足 a_(h,s)(u(h))=t_(u(h)) 且 e_h(s)=r，就连边 hr，并储存一个这样的完整原 state。图可包含 λ=0 的 states；构图无需计算任何 λ 或 μ。上述分数 f 支持于该图，且行和 1、列和≤1。因此对任意 helper 子集 Q，

\[
|Q|=\sum_{h\in Q,r}f_{h,r}\le|N(Q)|.
\]

这就是 Hall 条件。确定性增广路匹配覆盖全部 helpers：若最大匹配仍漏一左点，沿未匹配边/匹配边交替可达的左集合会比其右邻域更大，矛盾。每条匹配边输出所储存的**完整原 indexed state**，不拼接互不兼容的坐标 labels。匹配正 cells 两两不同并避开 main 正 cells；各 helper 取得其 unit 正 cell，main 取得指定 state 的全部正 cells。所有 groups 质量恰 1，而 norm-one 使 V≤1，故 V=1。

直接状态图算法在仅承诺 λ 有实解时仍成立：λ 仅用于证明 Hall，算法本身由显式 table 与匹配完成。若需要检查局部分布接口，可对每 helper 解原 table 上的有限有理 LP：非负变量 λ、归一化、R 个 primary 等式及 |A_h|R² 个 pair 等式。实可行时有多项式位长有理解，标准 rational LP 可找到；接口不可行只说明这项额外前提失败，不能据此判普通 P 无 unit 调度。

完整 actual 调度如下。各 group selector 放在选中原 state root；选中 state 的全部正 incidence jobs 导出到上述分配的不同资源机，全部零私时 jobs 留 root；**每个未选 state 的全部 jobs** 留自身 root。选中 roots 为 unit selector 加零负载，未选 roots 的私权和恰 1；资源机最多一枚时间 1 的原 incidence job。所有原 jobs 各执行一次，全部机器负载≤1。至少 main selector 存在且只在 unit 端可执行，所以 OPT(P)≥1，等号由该完整调度达到。

H、𝒜 为空或 𝒜 含 unused variables 均可；unused planes 保留为空机。R=2、非零 main 截距、零概率 states、任意 state-dependent onehot 点均已覆盖。状态图边数至多 Σ_h|S_h|，每边储存原 state 身份；匹配、查表、field arithmetic、有理核验以及扫描全部 I 个 incidence jobs 输出完整调度均按显式总位长多项式。无概率分母复制、R! 或隐藏配置枚举；不声称仅给 binary R 与 compact oracle 就可在 poly(log R) 内展开所有 planes 和任务。

## 3. Simplex 多 primary：独立合同与一个公共域代码

- **ID / version**：`UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`。
- **Objects / domain**：每个 odd prime R≥3，以下显式二次域、公共四维 simplex code C、等 arity 的 padded tagged-line menus、一个 diffuse main 和 B(R−1) 个 onehot helpers。helpers 各含 R+1 个 primary；全部完整 lines、全部原 states 和零私权任务都保留。R=2 不在本 ID 的域。
- **Quantifiers / definitions**：给定任意这样的 R 和非平方 ν，构造下面唯一指定族。V 与普通 P 均按 §1.3；V 上界量化所有 state choices 与所有 partial allocations，actual 下界量化 P 的每一份完整合法调度；CSP 是 §7 明确定义的全局赋值问题。
- **Exact / conclusion**：所有 groups 的 uniform state distributions 均为 uniform pairwise-independent；所有 local relations 是同一 C 的 cosets。精确 V=2/(R+1)，完整实际 OPT_UM=2−2/(R+1)，ordinary additive-CSP 的精确值为 B/[1+B(R−1)]，其中 B=R²+1。达到各值的对象可确定性总位多项式生成。
- **Assumptions / dependencies**：无复杂度假设；只用下列有限域/trace 线性代数、资源计数和完整原任务负载。未调用 source hardness、外部全局见证或未知配置求解器。
- **Scope / nonclaim**：排除仅从 local PI、common coset code、common arity/partiteness 得到统一正 actual-export 常数的保证。它是易于明确计算的结构族，不是 NP-hard promise gap、原 Chan/LST hard image、任意 NO 源的 decoder，或删除预算稳健性结果。
- **Evidence / counterevidence / status**：原 Exact SHA256 `670bd2deb41f4b5fc9df6ca3f0ed460ca2daaa3a9cca38604561bfff3d7b10d2`；作者 Proof `4278590caacc424c5df2574ecd8d70a9d53f08fb42f0703aee9bee088913d474`。bicriteria 的独立 Exact-first `db3db1a1f09f1392ba880a749959171ea131d044acdb7772e0c315dcadf2112f`，作者读后 `1addfcb4e4c0e771eb7b30e03cfa699b51b4deae55abe173c824d896a618008c`；该 reviewer 不认证 one-primary ID。精确域内未留 standing objection，本合并稿尚待 final scope actual-read。无新软件运行、外审或全球新颖性认证。
- **Related files / distinction**：与 §1–2 共用规范编码，但主结论相反的结构原因是 helper 同时含多个 primary。§8 保留唯一 main 瓶颈和原 LST 参数域的准确边界，不扩展两个 ID。

取 quadratic nonresidue ν∈F_R，显式表示

\[
K=\mathbb F_R[\omega]/(\omega^2-\nu),\qquad
\operatorname{Tr}(a+b\omega)=2a.
\]

有序代表集为

\[
\mathcal T=\{1+c\omega:c=0,1,\ldots,R-1\}\cup\{\omega\},
\quad \mathcal B=K\cup\{\infty\},
\quad B=R^2+1,
\quad\Pi=\mathcal B\times\mathcal T,
\quad q=B(R+1).
\]

每个 (a,t)∈Π 是一个公共 part。对 ζ=(u,v)∈K² 定义

\[
w_a(\zeta)=
\begin{cases}u+av,&a\in K,\\v,&a=\infty,\end{cases}
\qquad E_{a,t}(\zeta)=\operatorname{Tr}(t w_a(\zeta)),
\]

并固定**一个公共代码**

\[
C=\{(E_{a,t}(\zeta))_{(a,t)\in\Pi}:\zeta\in K^2\}
\subseteq\mathbb F_R^q.
\tag{3.1}
\]

其维数、PI 和 full projective simplex 身份在 §5 直接证明，未把代码作为不透明 source oracle。

## 4. 全部变量、公共 cosets、完整 lines 与每个 state 的私权

每个 part (a,t) 有一 primary 变量 x_(a,t)。main M 包含全部 q 个 primary，各 part 恰一个变量。对每个 $a\in\mathcal B$、j∈F_R\{0} 建 helper H_(a,j)。它在自身 block a 的 R+1 个 parts 使用 primary x_(a,t)；每个其他 part (b,t)，b≠a，使用新变量 d_(a,j;b,t)，只属于该 helper。全部 fresh variables 互异并与 primary 不交。

因此 helpers 数 H=B(R−1)，groups 数 G=1+H；**每个 group 均为 q-ary，且每个公共 part 恰一不同变量**。fresh padding 是实际对象，不是免费 common-arity 承诺。

每个 group 的完整 indexed-state 集都是 K²，共 R⁴ 个 states，一个也不删除。main state ζ 在 x_(b,t) 上的 label 是 E_(b,t)(ζ)。helper H_(a,j) 的 state ζ 在自身 primary x_(a,t) 上的 label 为 E_(a,t)(ζ)−j，在 fresh d_(a,j;b,t) 上为 E_(b,t)(ζ)。等价地，其完整 local relation 为 b_g+C：b_M=0，b_(H_(a,j)) 在 block a 的各坐标为 −j，在其他坐标为 0。

每个 primary x_(a,t) 的 main 截距为 0，其 H_(a,j) 截距为 j；每个 fresh variable 唯一 helper 的截距为 0。因此 primary group-degree 恰 R、fresh degree 1，同一变量截距全部互异。对每个 group 的每个 state，按 §1.1 的公式列出其全部 qR 个 tagged-line incidences。

定义 R+1 个点的 block

\[
\mathcal D_a=\{(x_{a,t},1,0):t\in\mathcal T\}.
\]

main 的每个 state (u,v) 都指定

\[
\alpha(u,v)=\begin{cases}-u/v,&v\ne0,\\\infty,&v=0.\end{cases}
\]

该 state 在 D_(α(u,v)) 的全部 R+1 点各给私权 1/(R+1)，其余完整 incidences 均为 0。对任意 w∈K，令 t₀(w) 为有序 T 中第一个满足 Tr(tw)=0 的元素；w=0 也用此 first 规则。helper H_(a,j) 的每个 state ζ 只在

\[
(x_{a,t_0(w_a(\zeta))},1,0)
\tag{4.1}
\]

给私权 1，其余 qR−1 个 incidences 均为 0。§5 核这些正点确在原 state 的 line 中。每个 state 总私权恰 1；fresh lines 私权全 0，但其 labels 依旧完整变化，仍有对应全部原任务。只有私权为 0，不是删除 lines、states 或 jobs。

普通 P 完全按 §1.3 构造：每 group 一 selector、每 state 一 private root、每个完整 incidence 一独立两端 job，资源端耗时 1。均匀局部分布在每组的每个原 state 赋概率 1/R⁴；这不是未知全局赋值。

## 5. Trace、公共 simplex、全部 pairs 和正资源可达性

非平方 ν 使 K 为 R² 元域。对 t=a+bω、w=c+dω，

\[
\operatorname{Tr}(tw)=2(ac+\nu bd).
\]

其配对矩阵为 diag(2,2ν)，在 odd prime 域非退化。T 恰代表 K 的每个一维 F_R 子空间：常数项非零者唯一缩放到 1+cω，常数项为零者对应 ω。对非零 w，t↦Tr(tw) 的核恰一维，故 T 中恰一元素令其为零；w=0 时所有元素都可。反过来每个指定 t∈T 的正交核有非零 w，且其唯一零方向就是 t。这证明 t₀ 定义合法，并可遍历全部指定方向。

E 在 block ∞ 的 trace coordinates 确定 v，在 block 0 确定 u，因为 T 含 1、ω 这组基的方向。因此 E 对四维 F_R 向量 ζ 单射，C 的维数为 4，恰有 R⁴ 个不同 codewords。系数向量

\[
(t,ta)\quad(a\in K,t\in\mathcal T),\qquad
(0,t)\quad(t\in\mathcal T)
\]

经非退化 trace 配对代表 K² 的全部一维 F_R 方向：第一坐标非零者先唯一归一到 T，再由第二/第一坐标确定 a；第一坐标为零者由 (0,t) 表示。因此 q=(R⁴−1)/(R−1)，本代码确为所写四维 full projective simplex code。

uniform ζ∈K² 时，每个 w_a uniform 于 K。一个 block 内不同 t、t′ 不是 F_R 倍数，对应两个独立 trace forms，故 (E_(a,t),E_(a,t′)) uniform 于 F_R²。不同 finite blocks a≠b 时，(u,v)↦(u+av,u+bv) 是可逆 K-linear map；finite block 和 ∞ 时，(u,v)↦(u+av,v) 同样可逆。输出为独立 uniform K 元素，再应用指定的非零 trace forms，仍给 uniform pair。由此 main 的全部不同坐标 pairs 均 uniform，单坐标亦 uniform。helper 只是公共 codeword 的固定 coset 平移，故它的**所有 primary/fresh pairs** 也精确 uniform。未把只检查 primary 的边际冒充完整 PI。

main 的指定 block 满足 w_(α(u,v))=0，所以该 block 全部 labels 为 0；截距 0 的线在 z=1 经过 y=0，全部 D_α 正点合法。helper 在 t₀ 处 E=0，其实际 slope 为 −j、截距 j，所以 z=1 也确为 y=0，(4.1) 是合法原资源。

每个 helper 的所有 states 的正资源邻域恰为整个 D_a。包含性来自定义；反向对任意目标 t，选非零 w 满足 Tr(tw)=0。finite a 取原 state ζ=(w,0)，∞ 取 ζ=(0,w)，即可使 w_a=w、t₀(w_a)=t。对给定 w_a，实际上有 R² 个原 ζ，padding 的其它坐标区分它们；它们全部保留，不因一个 block 的重复值而合并 indexed states。每 state 内不同变量的 tags 不同，每条线的 R 个横坐标不同，故 qR 个 incidences 也确实全为不同资源。

## 6. 精确 V、任意实际调度的下界与完整达到调度

先核所有 partial allocations。若某 helper 质量 0，则 minimum quality≤2/(R+1) 已成立。否则每个 helper 的 onehot 正点都必须实际分给它。因此每个 block a 的 R−1 个 helpers 占 D_a 中 R−1 个不同点。任意被选 main state 的正质量只在某个 D_α 的 R+1 个等权点上，至多还剩 2 点，故 V≤2/(R+1)。这个论证不要求分配完整 supports，也不要求分配零权 cells；任意省略不能增加私权质量。

达到时 main 选 ζ=(0,0)，其 α=∞；在 D_∞ 预留任意两点给 main，其余 R−1 点分给该 block 的 R−1 个 helpers。其他 blocks 各给 R−1 个 helpers 选不同的 R−1 点。§5 为每个 helper 目标点找回一个合法原 state。不同 blocks 的资源互异，故 helpers 各质量 1、main 质量 2/(R+1)，证明

\[
V=\frac{2}{R+1}.
\tag{6.1}
\]

同一选择给完整 actual 上界。每 group selector 放其选中 private root；main 仅导出其预留两点的正 incidence jobs，其他全部选中 main jobs 留 root；每个选中 helper 导出唯一正 job，其余零私时 jobs 留 root；**所有未选 states 的全部 incidence jobs** 留各自原 private roots。资源机至多一枚 unit job，未选 roots 的私权和为 1，选中 helper roots 为 1，选中 main root 为

\[
1+\left(1-\frac{2}{R+1}\right)=2-\frac{2}{R+1}.
\]

这列全 selectors、全部 zero/fresh incidences、未选 states 和原 baseline jobs，各恰执行一次，没有免费删除或外送。

下界直接量化任意完整合法实际 σ。记 C=C_max(σ)。若 C≥2，所求下界已成立；若 C<2，每个 group 的真实 selector 选择了它自己某个原 state root。被选 helper state 的唯一正 job 若留 private，会与 unit selector 合成负载 2，故必须真的导出。每个资源端耗时 1，所以 C<2 时同一资源不能接两枚原 incidence jobs。于是每 block 的被选 helpers 必占 R−1 个不同 D_a 点，不论未选 states 的任务另作何安排。

被选 main state 的正资源都位于其 D_α，至多能实际导出余下两枚正 jobs；其 private root 至少留 R−1 枚时间 1/(R+1) 的正 jobs，再加 selector，负载≥2−2/(R+1)。未选 states 的其它 exports 只会占掉资源，额外私下执行的任务只会增加 root 负载，均不能削弱下界。因此

\[
\operatorname{OPT}_{\rm UM}=2-\frac{2}{R+1}.
\tag{6.2}
\]

这是完整 P 的直接上下界，不以任何未陈述的配置结论代替实际任务核验；C=2 与达到值的等号均已覆盖。

此族只有 main 是 diffuse 瓶颈。若删去 main group 及其 selector、全部 main-state incidence jobs 和对应 private roots，保留资源 planes 与全部 helpers，则每 block 的 R−1 个 helpers 可注入 D_a 的 R+1 点。按 §2 相同的完整原任务留私下/正点导出规则，剩余实例有 V=1 与完整 unit 调度；剩余 helpers 的 unit selectors 也给 OPT=1。该单次删除事实正是此族的范围边界，不支持任何删除预算稳健困难性推论。

## 7. 对应 ordinary additive-CSP 的全局精确值

CSP 变量是全部 primary 和 fresh variables；每 group 一个 q-ary 约束，按公共 part 顺序使用实际变量，接受 relation b_g+C，没有额外约束。全局赋值给每个实际变量一个 F_R label，value 是 G 个约束中满足的比例。

单 block 的 trace code 为

\[
C_{\rm block}=\{(\operatorname{Tr}(tw))_{t\in\mathcal T}:w\in K\}.
\]

其中每个向量都有一个零坐标，故不含非零常量向量。由线性性，不同 j∈F_R 的 cosets −j·1+C_block 两两不交：若相交，差会给非零常量向量属于 C_block。

helper H_(a,j) 要求其共享 primary block 属于该非零 j coset。若全局赋值满足 main，则每个 primary block 都在 j=0 的 C_block 内，因而没有任何 helper 可满足；最多满足 main 一项。若不满足 main，则每 block 至多满足一个 helper，故至多 B 项。因为 B≥1，所有全局赋值最多满足 B 个约束。

达到时把所有 primary labels 设为 −1。每个 block 的 H_(a,1) 使用原 state ζ=(0,0)，其 primary labels 正为 −1，fresh labels 都为 0；把这些 helpers 各自的 fresh variables 设为 0，其余 fresh labels 任意。不同 helper 的 fresh variables 不共享，故这 B 项同时满足。main 不能接受：任一主 codeword 在它指定 block 全为零，而当前 primary 全为非零 −1。同 block 其余 helpers 也不能满足。因此

\[
\operatorname{val}_{\rm CSP}
=\frac{B}{1+B(R-1)},\qquad B=R^2+1.
\tag{7.1}
\]

这是普通全局赋值的精确计算，没有把各 constraint 的 local PI distributions 当作同一 global assignment，也没有由小 CSP value 推导 hardness。

## 8. 完整 counts、位长、共同域与不适用范围

保留全部 fresh padding、完整原 states 和零权 incidences 后，精确 counts 为

\[
\begin{aligned}
H&=B(R-1),&G&=1+H,&q&=B(R+1),\\
N_{\rm var}&=q+H(q-(R+1)),&&&N_{\rm state}&=GR^4,\\
I_{\rm line}&=GR^4qR=GqR^5,&&&N_{\rm resource}&=N_{\rm var}R^2,\\
N_{\rm machine}&=GR^4+N_{\rm var}R^2,&&&N_{\rm job}&=G+I_{\rm line}.
\end{aligned}
\]

有限资格共有 2I_line+GR⁴ 个：每 incidence 两端（包括私权 0 端），每 selector 的 R⁴ 个原 roots。唯一有限数值时间为 0、1/(R+1)、1；没有隐藏的资格或额外物理容量。

q、G 为 O(R³)，变量数 O(R⁶)，states 数 O(R⁷)，资源/机器数 O(R⁸)，incidences/任务数 O(R¹¹)。因此完整 state/label/line 资料、局部分布证书和**有限资格表**的展开位长为 O(R¹¹ polylog R)。这不是稠密 job×machine 矩阵大小；若完整主模型要求列出全部 ∞ 项，稠密矩阵有 O(R¹⁹) 项，位长再乘 polylog R，仍是展开规模多项式，不能称为 R¹¹ 稠密输入。

给 R 和非平方 ν 可直接生成所有对象，也可扫描 F_R 找一个 nonresidue；这是按实际输出规模 polynomial，不是 poly(log R) 的免费展开。trace、field arithmetic、固定概率 1/R⁴、1/(R+1) 及各 tags 的位长为 poly(log R)。确定性查表或解 trace 线性方程可恢复每个目标点对应的原 state，生成达到 allocation、CSP 赋值与全部原任务调度。所有步骤按上述显式总位长多项式；没有 compact predicate/state oracle，也没有按一个隐藏 reciprocal weight 复制任务。

one-primary 的 R 可为任意素数≥2；本 simplex 明确限 odd prime R≥3，其 Tr=2a 和非退化配对不向 R=2 免费延伸。simplex 每个 helper **联合包含 R+1 个 primary**，这是超出 §1–2 的真正结构区别：只对单 primary 条件化得到的辅助均匀性，不能套到同时条件化这些 primary。本例使用 R+1 个 primary，不声称恰两个 primary 已有相同构造或精确界。common padding 的辅助 fresh variables 全部私权 0，但它们的 labels 仍提供完整公共 C、q-arity、partiteness 和全部 pairs，不能删去后继续称同一 padded 对象。

在每个 simplex 实例内所有 groups 共用一个 C，但 C 与 arity q 都随 R 变化，且 q=(R²+1)(R+1)≈R³。它不属于已核原 LST 编译中固定 arity、R 相对 arity 充分大的参数域，也未断言是任何 Chan/LST hard reduction 的 image。本页不新增配置或稳健困难性结论；唯一 main 删去后的 unit escape 已在 §6 明列。实际 OPT 趋于 2 是这个显式易算族的值，不是 ordinary UM 的近二近似 hardness。

两项合起来准确区分结构：单 primary 加指定 PI-onehot core 不能阻止 unit actual escape；允许 helper 联合约束多个 primary 后，即使全部 local pairs uniform、公共代码、common arity 和真实全任务编码都保留，也可使 V 趋于 0、实际 OPT 趋于 2。尚缺的 source NO 解码与复杂性归约没有由这些结构值自动补齐。
