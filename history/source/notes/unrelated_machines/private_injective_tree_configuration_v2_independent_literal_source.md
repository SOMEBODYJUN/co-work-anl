# 私有树配置五三界与非注入菜单承诺判定：独立陈述先行审查

## 读取对象与来源隔离

审查对象为 `UM-Q-PRIVATE-INJECTIVE-TREE-CONFIGURATION-FLOOR-v2`。实读 Exact：

`/workspace/scratch/038d9dcc4cac/private_tree_configuration_floor_v2_exact_statement.md`

SHA256：`ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900`。

本稿冻结前未读作者 v1/v2 proof、未问作者构造。已自行完成的 v1 Exact-first 稿为：

`/workspace/scratch/038d9dcc4cac/private_injective_tree_fractional_floor_statement_first_review_literal.md`

SHA256：`9f60a21914a49efab98beacfedd93494dd98ddbd2478afee7ff8453f20432a4b`。

v1 的单树 blocker 归纳及 Haxell 适用条件已独立重构，可作为本次已披露前提；v2 新增 A/B/C 不被视作自动审过。本稿再次独立推导其配置边际、随机 a 叉树、完整实际负载与严格承诺判定。

## 结论与认证层级

未发现 fatal objection。A 的严格配置等价、B 对所有配置阈值的五三存在性，以及 C 对任意非注入原菜单的严格 (1,5/3) 承诺判定均成立。关键新增桥是：CONFIG(T<2) 可导出真实状态上的 a 叉树分布，全部叶活跃边际不超过对应原 LP 外置边际；无需错误地把 CONFIG(T) 当作 full-leaf bundle λ。

本稿未认证一般变参下输出 σ 的位多项式算法、非注入原 P 的配置间隙界、新颖性或 UM-TARGET-v1 的任何解答。

## 1. 模型和全配置阈值的局部精确系统

每个内部机器 v 恰有一个合法 unit incoming job：状态根处是对应 u 的 selector，其他位置是其父边 job；另有 d 枚各时间 1/d 的 outgoing jobs。不同状态内部机器私有。外机只处理 unit leaf jobs。

固定 1≤T<2，写

\[
 s=\lfloor d(T-1)\rfloor,\qquad a=d-s\in[1,d].
\]

在含 incoming unit 的机器配置中，父置 outgoing jobs 至多 s 枚，故至少 a 个 outgoing jobs 不在父配置中；不含 incoming 的配置中，任意 outgoing 子集都合法，因为全部父置的总负载为 1≤T。

下面还给出一个独立重构的多项式规模扩展系统，核查 Exact 中关于 CONFIG(T) 可行性规模的附加句。设 q_v 为 incoming unit 的本机边际；对每个从 v 出发的 port e，令 x_e 为该 job 向下/外置的边际，令 y_e 表示“v 的 incoming unit 出现且 e 没有父置”的联合概率。可用以下有理线性系统：

\[
\begin{gathered}
 0\le q_v,x_e\le1,\\
 \max(0,x_e+q_v-1)\le y_e\le\min(q_v,x_e),\\
 \sum_{e\text{ outgoing from }v}y_e\ge a q_v,\\
 x_e=q_w\quad\text{若 e 的下端是内部机器 w},\\
 \sum_{s\in S_u}q_{\operatorname{root}(u,s)}=1,\\
 \sum_{e:\,f(e)=z}x_e\le1\quad(z\in Z).
\end{gathered}
\]

max/min 各自展开成常数条线性不等式。给定 CONFIG(T)，这些变量来自本机配置分布，均满足系统。反过来，若 0<q_v<1，则 incoming=1 时 outgoing 向下指示的边际为 y_e/q_v，处于立方体且总和≥a；多面体 `{b∈[0,1]^d:Σb≥a}` 是所有大小至少 a 的 0/1 子集凸包。incoming=0 时边际为 `(x_e−y_e)/(1−q_v)`，由上述 Fréchet 不等式处于 [0,1]^d，无额外限制。q_v=0 或 1 时分别直接用相应单个分支。于是得到全部本机合法配置分布。父边际为 1−x_e，与对应向下边际精确合为 1；外机用 singleton 加 empty 配置即可。

该系统规模为显式原 P 的多项式，系数由整数 a、d 与显式关联构成，总位长多项式。s 通过有理精确取整可算。T<1 因非空 selector 而不可行；T≥2 时全部 port 父置、selector 任选根已给合法实际 C≤2。因此本模型全 T 的配置可行性确可归结为多项式规模的精确有理 LP。

## 2. A：CONFIG(1) 与共同 λ

### 必要性

在 T=1 的配置中，incoming unit 与任何正的 outgoing small job 不能共存。令 λ_us 为 selector 在状态根 (u,s) 出现的边际，显然 λ≥0 且每 u 的 Σ_sλ_us=1。若某内部机器的 incoming unit 边际为 q，则任一 outgoing job 的父置边际≤1−q，故下置边际≥q。逐层归纳，每个该状态叶的外置边际至少 λ_us。外机至多容纳一枚 unit job，得到每 z 的共同容量

\[
 \sum_{u,s}\lambda_{us}|f_{us}^{-1}(z)|\le1.
\]

这里从同一份全局 selector 边际取得所有资源行，不能逐外机重选 λ。

### 充分性

给定共同 λ，每个状态内的每个内部机器取 incoming-unit singleton 配置权重 λ_us，另取全 d 枚 outgoing small jobs 的配置权重 1−λ_us。这两类配置负载均为 1。外机给每个映到该机的原 leaf job 的 singleton 配置权重 λ_us，剩余权重放 empty；共同容量保证剩余非负。

每内部或叶 job 的父置边际为 1−λ_us，向下/外置边际为 λ_us，总覆盖恰 1。每 selector 的覆盖恰为 Σ_sλ_us=1。所有未选状态与 λ=0 状态的原 jobs 均在此配置系统中。由此 A 成立，且共同 λ 系统的显式矩阵规模及位长多项式。

本等价论证本身甚至不需要状态内注入，但本稿不扩改 Exact 的量词；注入性在 B 的资源 blocker 和实际匹配中不可省略。

## 3. B：从 CONFIG(T) 独立构造受容量支配的 a 叉树分布

给定一份可行 CONFIG(T)。对每个内部机器 v，保留其真实本机配置分布，并记 incoming unit 概率 q_v；每个 port 向下边际记 x_e=1−Pr(e 父置)。对应内部子机器 w 有 x_e=q_w，叶 job 的 x_e 是其 unit 外置边际。

对每 u，先按其根 selector 边际 λ_us=q_root(us) 选一个真实状态。根必活跃。在一个已活跃内部机器 v：按该机配置分布条件于其 incoming unit 出现抽样，再从这份配置中未父置的 outgoing ports 中取恰 a 个（例如按固定顺序取前 a 个），使这些孩子/叶活跃。每份条件配置至少有 a 个未父置端，故抽样良定义。若某节点 q_v=0，它活跃概率也为 0，无需取条件分布。

设某机器无条件活跃概率为 α_v。根有 α_v=q_v。若 α_v≤q_v，则对其任一 outgoing port e，

\[
 \Pr(e\text{ 被活跃子树选中})
 \le \alpha_v\Pr(e\text{ 未父置}\mid\text{incoming})
 \le q_v\Pr(e\text{ 未父置}\mid\text{incoming})
 \le x_e.
\]

逐层归纳，该过程产生真实状态中的满 a 叉高 h 子树，并使每个原 leaf 的活跃边际不超过其 LP 外置边际。每个 root 恰选一个真实状态；不存在按不同路径分别取不一致 state 的问题。全外机满足

\[
 \sum_{u,s,w:\,f_{us}(w)=z}
 \Pr((u,s,w)\text{ 活跃})\le1.
\]

上述分布可以很大；这里只用于有限存在证明，不以列举分布称为总位多项式。

## 4. B：blocker、Haxell 与全部实际 jobs

固定 1≤r≤a，记 k=r^h，b=(a−r+1)^h。超图 A=U，B=Z，对所有原状态及其所有满 r 叉高 h 子树加入其 k 个实际叶资源及 root tag。状态内完整 leafmap 单射保证超边总大小为 R=k+1。

给任意 D⊆U 和命中其全部 incident 超边的 X⊆Z。每次抽出的满 a 叉子树，其每个满 r 叉子树也是原 d 叉树中的候选，因此 X 必须命中它们全部。v1 已独立证明的叶 blocker 归纳应用于这棵 a 叉树，给出每次至少 b 个叶被 X 命中。取抽样期望、再使用外机共同容量，即得

\[
 b|D|\le\sum_{z\in X}\sum_{u\in D,s,w:f_{us}(w)=z}
 \Pr((u,s,w)\text{ 活跃})\le|X|.
\]

若 b≥2k−1，则 τ(E_D)≥(2k−1)|D|>(2k−1)(|D|−1)。空 D 也满足严格条件。总超边大小 R=k+1，因此 Haxell 常数 2R−3=2k−1，得到每 root 选一真实状态和满 r 子树的完美匹配。

本次外部依赖沿用已冻结 v1 亲核：Annamalai, *Finding Perfect Matchings in Bipartite Hypergraphs*, arXiv:1509.07007v2，PDF 第 2 页／印刷第 1 页 Theorem 1.1 及定义；本地原 PDF SHA `f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce`。Haxell 1995 原全文本次未取得，不冒称亲读。总均匀度、B-only hitting set、严格不等式、有限性及 k=1 的 Hall 退化均与定理相符。

将匹配选中子树的端口 jobs 全向下/外置，selector 放选中根，其余所有原 jobs 全父置。每活跃内部机器负载 `1+(d−r)/d=2−r/d`；每非活跃内部机器（包括全部未选状态）恰有 d 个 small outgoing jobs，负载 1；每外机至多一个选中 unit 叶，负载≤1。因此对完整原 P 有实际 C≤2−r/d，而非仅配置或叶资源分配结论。

取 r=⌊(a+2)/3⌋=⌈a/3⌉，则 a−r+1≥2r−1，凸性给 `(2r−1)^h+1≥2r^h`，所以 blocker 前提成立。又

\[
 2-r/d\le 5/3+s/(3d)
 \le (5/3)(1+s/d)\le(5/3)T.
\]

T≥2 的父置调度已给 C≤2。非空 selector 保证配置阈值≥1；取所有可行阈值的下确界即可得到配置整数间隙≤5/3，不需要把某有限阈值测试升级为一般证明。

## 5. C：非注入原状态的严格承诺判定

### 严格 YES 不会在过滤中丢失

若原 OPT≤1，一枚 selector 实际放在某状态根后，该根所有 positive small outgoing jobs 都必须向下。沿整树归纳，选中状态的每个原 port 都向下，每个原 leaf 都到其唯一 unit 外端。负载≤1 强迫该状态完整 f_us 单射，并且不同选中状态的叶资源全局不同。因此这些实际选中状态全部保留，取其 λ=1（其余 λ=0）即满足过滤后共同 λ LP。

所以空菜单或 LP 不可行都排除原 OPT≤1，确实保证原 OPT>1；这里未把这种返回一律误写成原 OPT>5/3。

### 过滤后 LP 可行保证原完整实例的五三存在性

把过滤后仍可作为 selector 候选的状态及其私有树看作缩小结构，应用 A 和 v1／B 在 T=1 的结论，存在这部分所有 jobs 的 C≤5/3 调度。随后把每个被排除状态的全部原 port jobs 父置；它们机器完全私有，负载恰 1，且没有 selector 放在这些根上。原 selector 的真实允许端包含保留下来的候选，所以得到原全部 jobs 的合法调度，C≤5/3。

被过滤的机器和 jobs 并未删除；仅从求解 LP 的 selector 菜单及相应受选结构中忽略它们，再用明确的父置规则覆盖。此举不占用任何外机，不干扰剩余调度。

注入性可按每份显式 leaf list 的资源 ID 确定性检查，保留 LP 有一个变量／状态及一行／root、外机，系数为 0/1，规模和编码长均多项式。使用确定性精确有理 LP 可行性算法得到总位多项式判定器。该判定器不要求实现上一步 Haxell σ 构造。

所以承诺域 YES OPT≤1 必返回 YES，NO OPT>5/3 必返回 NO；中间带允许任意回答。LP 可行性只证明真实调度存在，不能把该判定器描述成输出 σ 的 approximation algorithm。

## 6. 退化、位复杂度与适用范围

- d=1：所有状态只有一条链、一片叶，注入性自动；T∈[1,2) 有 s=0,a=r=1，超图是 Hall 情形，实际 C=1。
- h=1：抽样是一层 a-subset，blocker 为 a−r+1；所有证明和 C 的过滤不变。
- a=1 或 r=1：k=1，总超边大小 2，Haxell 退化为普通 Hall，未使用不存在的高均匀度条件。
- T 恰在 1+s/d 的阈值上时，floor 和“至多 s 个 small”的不等式仍正确；T 接近 2 时仍有 a≥1。
- q_v=0 和 1、λ=0 均在局部系统与条件抽样中单列，不对零概率作除法。
- 空 U 是 Exact 另列域：没有 selector/port jobs，返回空 σ／OPT=0；不能套非空配置下界 1。
- 所有状态、内部机器及 leaf 资格显式输入；没有以 binary d,h 代替指数展开。抽样分布、超图和 Haxell 存在性本身仍可能指数规模，不冒称构造复杂度。
- B 需原完整状态注入；C 只给承诺判定和完整实例五三存在性蕴含，不推出任意非注入原 P 的 CONFIG gap 界。
- 没有共享内部机器、非均匀处理时间、额外任务、预载或多单位叶端；这些机制仍在本结论范围外。

Status：v2 Exact-first independent reconstruction completed；A/B/C 无 fatal；作者证明尚未读；无新增代码或有限实验；新颖性和一般构造算法未认证。
