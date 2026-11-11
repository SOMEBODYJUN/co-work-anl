# 全可见真最大裸标签 C 联合层：来源与构建前审查

Boss1；RUN `six-boss1-20261111`。本包仅准备精确符号输入与独立 Fraction 预检，状态固定为 **PREPARED_NO_OPTIMIZER**。本阶段优化器调用为零，不做任何具体旧点补全、不构造 phase-I、不声称某个必要系统点可由完整 SPE 实现。原六人 half 仍为 OPEN。

## 1. 原模型、同一 actual 历史与两个不同的最大标签

亲读 `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`。客户有限、价值均为一；共同目录是有限非空的标签集，覆盖映射可以有别名和空覆盖。恰六名提供者各行动一次；完整纯策略在每个合法有序历史上给动作，SPE 对每个历史、每个合法偏离以弱不等式比较。同负载的不同有序历史可以有不同后继。所有来源均保留同一完整策略在各自强制动作后的真实续局，不把 actual 后继固定来做偏离。

actual 动作是 A1,…,A6。令 P 为这同一条 actual 路径的前四动作负载，取合法 X 达到全目录最大

\[
F_X=\max_{L\in\mathcal S} f_P(L),\qquad
f_P(L)=\sum_{y\in L}\frac1{P_y+1}.
\]

另取合法 C 达到全目录最大裸大小 K。C 和 X 可以相同、同覆盖不同标签，也可以完全不同；没有把 C 设成 X 或任何 Ai，更没有使 C 获得别的前缀下潜力最大性。有限非空目录保证两个最大者存在，任意弱平局取一个即可。

取达到 OPT6 的六个合法标签 Q1,…,Q6，允许重复，O 是其覆盖并。O 从不作为合法目录行动。令客户在六比较索引中的会员为 q1,…,q6，d=Σqj、o=1[d>0]。归一化仅在 OPT6>0 时进行；OPT6=0 的原模型直接有 W=K=0，不需要此归一化 LP。

## 2. 全客户型、忠实拉回和两条等式

新型位序为 `(a1,a2,a3,a4,a5,a6,x,o,c)`，保留全部 2^9=512 型，包括全零型、o=0 型和仅 C 覆盖的型。新列 v'=2v+c，旧 v 的系数在 c=0/1 两列原样复制；旧 K 列256移至新 K 列512。所有513列非负。

旧 v6 输入 SHA 为 `49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936`，证书 SHA 为 `98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d`。全部867 raw 行、行序、名称、族、原 rhs、显式零系数及其他行元数据忠实拉回；旧全零行与重复行继续占原 raw 位置。此操作完全不读取旧证书的原始点支撑，也不把旧全最优面当作待补全的点。

目标为 W=Σz·1[Σai>0]，由旧目标忠实拉回。两条独立等式为

\[
\sum_v o_vz_v=1,\qquad \sum_v c_vz_v-K=0.
\]

第二式表达 C 真达到 K；不新造另一个 K，也不额外追加 `K_ge_size_C` 重复行。旧 `K<=1`、六纯并的 rhs=-1 等归一化常数保持原数值。

## 3. 两条冻结根行，只准备准确通式

第一条是 Main 的 `main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json`，SHA `8459c0a86264e02efae76f16a060f1af0d0941c190863c7344b25481bc42fdc8`。亲读其完整 proof；原行按 u1 系数为1的尺度保存：

\[
u_1-\frac{117135582158121}{1145925867755340}K
-\frac{23074097917720}{1145925867755340}O\ge0.
\]

第二条来自 `maximal_root_tail_wallet_v3/exact_certificate.json`，证书 SHA `b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925`，输入 SHA `01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0`，proof SHA `f5d47adde14fd247eeb55a4d1afa282400030ff361966e47c62deeabd1810851`。亲读完整 proof，只抽取其齐次普遍根线：

\[
u_1-\frac{1767904008200582}{16877573861922720}K
-\frac{337340181272013}{16877573861922720}O\ge0.
\]

两条根线都把 u1 取为 actual 第一人收益。根强制最大 C 的后继不出现在本可见层，且没有把被强制者当成新最优根。两份来源的正预算不使用分支 OPT 帽，所以根线本身适用于任意六合法查询并；本输入取 O=OPT6。两根均按 u1 系数1、数值正除数1保存。

准备过程中 Main 明确完成 ROOT270 完整 proof 及270/129、自由K/O131列复核，并提供标准257列源行 `main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json`，SHA `d4ee988b28e897bcb836811c45e1c27a9728c64e352d2e30c79c93fded71a834`。本包逐字段忠实拉回该标准行，名称保持 `ROOT270_TRUE_BRANCH_P25`，再独立核其与上式一致。Main 后续另行决定数值释放，本包不运行根锥或全局锥求解。

## 4. C 的132条新增合法查询

记 L=Σai，ui=ai/L（L=0 时为0）、bi=Σ(j<i)aj、D=P+1。所有系数都从这些 actual 客户份额重新构建。

### 4.1 六条 SAFE、一条 FMAX 与一条 MX

actual 源 i 真改合法 C 后，同一真实续局最多使 C 客户承受 bi+7−i 个覆盖。因此

\[
\mathrm{SAFE}_i(C)=u_i-\sum_v\frac{c_vz_v}{b_i+7-i}\ge0
\quad(i=1,\ldots,6).
\]

X 是同一 actual 前四 P 下的全目录最大者，故

\[
\mathrm{FMAX}(C)=F_X-f_P(C)\ge0.
\]

actual 第五人强制 C 后取真实末回复 R_C。第五源 IC、R_C 末节点对 X 的最佳回复，以及 FX≥fP(RC) 得

\[
u_5\ge f_P(C)-g_P(C,R_C)
\ge f_P(C)+F_X-g_P(C,X)-f_P(R_C)
\ge\sum_v\frac{c_vz_v}{D+x_v}.
\]

所以 MX(C) 是 u5 减最后的和。这里使用 X 的全目录最大性；C 仅须合法。

### 4.2 同一 actual 末两人钱包：RC 九条、PAIR 九条

亲读正式 RC owner `customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints`，实际路径是 `archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md`；亲读正式 PAIR `archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md`（Main 给定 owner `M-e960d7f4ebca40a38760eb3ae044cc19`）。同时核对旧 `universal_union_wallet_lp/source_derivations.md`、`build_and_solve.py` 和 `check_certificate.py` 的字面方向；只读取，从未执行旧 builder。

对任意合法 T,Q，取同一个真实末回复 R_T。RC 以第五源对 T 的 IC、R_T 对 Q 的末位 BR、FX−fP(RT) 三项支付；PAIR 以同一前两项、actual 第六人对 RT 的 BR、逐客户 g(A5,A5)−g(A5,RT)≥0 支付。因此同一 P 下

\[
\mathrm{RC}(T,Q)=u_5+F_X-f_P(T)-f_P(Q)+g_P(T,Q)\ge0,
\]

\[
\mathrm{PAIR}(T,Q)=u_5+u_6+g_P(A_5,A_5)
-f_P(T)-f_P(Q)+g_P(T,Q)\ge0,
\quad g_P(T,Q)=\sum_v\frac{t_vq_vz_v}{D(D+1)}.
\]

固定一边 C，另一边依次为 A1,…,A6,X,Omean,C，共9条每钱包。纯角色保留真实交叠 cr；自对保 c²=c，不能把自对当独立两份 C。混合 C/Omean 从六个合法 Qj 分别求和再除6：其 RHS 为

\[
\frac cD+\frac d{6D}-\frac{cd}{6D(D+1)}
\ge\frac cD+\frac o{6D}-\frac{co}{6D(D+1)}.
\]

差为 `(d−o)(D+1−c)/[6D(D+1)]>=0`。这不是把 O 合法化，也不假设六标签分割。旧双均值钱包完整36有序对的行只做忠实拉回，不用新增 C 自对替换其精确平均。

### 4.3 五个 actual 源 P25，共85条

亲读 Main `main_all_source25_family/proof.md`，SHA `abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0`，完整族 SHA `8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0`。每个源 i≤5，n=6−i、p=bi、c0=(n+1)/2，正式原行是

\[
25u_i+c_0K-\sum_vz_v\left[
c_0t+\frac{24t}{p+n+1}+\frac q{p+1+nt}\right]\ge0.
\]

付款为源 IC 权25、每个真实中间尾大小帽权1/2、真实末尾大小帽权1、同一真实末节点对 Q 的 BR 权1。逐客户真实成本为

\[
\Phi_{25}=\frac{25t-z}{p+t+s+z}+\frac s2+z+\frac q{p+t+s+1},
\]

其中零负载、零分子的份额取0。完整最小成本为上式方括号；其证明保留弱平局，不推断真实尾必须全覆盖 T。构建和独立检查分别对全部456隐藏态及60最小值作 Fraction 字面验证。

T、Q 各从 A1,…,A6,X,C,Omean 九描述中取有序对，只新增至少一个 C 的 `9²−8²=17` 对，每源17，共85。两边顺序真实保留，不作对称化。

写 `A=c0+24/(p+n+1)`、`B=1/(p+1)`、`E=n/[(p+1)(p+n+1)]`，纯成本是 At+Bq−Etq。两个混合方向必须从六个合法索引分别平均：

\[
T=C,\ Q=\mathrm{mean}:\quad Ac+\frac o6(B-Ec),
\]

\[
T=\mathrm{mean},\ Q=C:\quad Bc+\frac o6(A-Ec).
\]

其从 d 到 o 的差分别是 `(d−o)(B−Ec)/6` 和 `(d−o)(A−Ec)/6`，系数均非负。绝不把 t=o/6 代入非线性分母 `p+1+n*t`。新增行没有双均值；旧 P25 双均值30有序异索引版本原样拉回，不改36平均、不改标签去重。独立检查会枚举全部64个六索引会员向量验证混合方向，并单独复核旧30/36索引语义。

### 4.4 含 C 的六纯角色并帽，共21条

从旧七个纯合法角色 A1,…,A6,X 选择五个，连同 C 得六个合法查询角色。每个并的覆盖均不大于 OPT6，故归一化原行

\[
-\sum_v z_v\,\mathbf1[c_v\lor\bigvee_{r\in J}r_v]\ge-1,
\qquad J\subset\{A1,\ldots,A6,X\},\quad |J|=5.
\]

共有 binom(7,5)=21。角色重复为同一标签或同一覆盖不妨碍“六合法查询”上帽。旧七个不含 C 的六纯并帽全在867内，不再重造。

## 5. 原尺度、完整 raw 合同与未加入的假设

原准备合同为 `867+2+6+1+1+9+9+85+21=1001 raw`。冻结前 Main 明确追加一条此前遗漏的真实六查询菜单大小预算

\[
\mathrm{MENU\_MAX\_SIZE\_LOWER\_BOUND}=K-O/6\ge0.
\]

理由是每个合法 Qj 均有 |Qj|≤K，而 O≤Σj|Qj|。其完整非负支付为

\[
K-O/6=\frac16\sum_{j=1}^{6}(K-|Q_j|)
+\sum_vz_v(d_v-o_v)/6\ge0.
\]

这对任意六合法查询并成立，包括重复标签、同覆盖别名、空覆盖、零客户；不把它称为 C 的实测均值，也不把 O 当行动。新增行每原子系数−o/6，K列1，rhs0，数值正除数1。该增量在最后原始位置1001（零基）加入，先前1001行顺序不变。Main 已说明此预算可以支付 ROOT270 替换旧正根付款后的斜率差，本包只准备这一真实原行，不复述或认领额外全局下界。

因此最终合同为 **`867+2+132+1=1002 raw / 513 cols / 2 equalities`**。旧867的未缩放系数和 rhs 忠实复制，新P25原收益系数25，其他新增原行按上述尺度。数值正除数单独记录：旧行若原字段指定则继承，否则按旧 ingest 的 `max(1,abs(rhs),max_j abs(a_j))`；旧 `numerical_scaling.json` 的全部798已存唯一行尺度逐项核对。新增85 P25除25，其他新增50行除1。原输入不进行数值缩放；任何将来缩放付款必须回到原行。

不增加 `ROOT_RIG(C,*)`、`UP(C)`、`QX(C)` 或 `P31(C,*)`。不新增未授权查询或删减原族，不把 Omean 当行动，不限制可见 C 的客户支撑，不固定 K，不制造另一条 actual 路径，不把额外 C 比特当作 SPE 充分性证书。

## 6. 可复核产物与冻结前边界

`build_input.py` 只用标准库与 Fraction，生成完整输入、全行目录、全列路由、正尺度和字面查询检查。`independent_precheck.py` 由独立 worker 阅读正式来源后单独撰写，不导入 builder，也不运行任何优化器。它逐项核512型、513列、1002原行、两等式、旧867原行拉回、新132行真实系数、两根通式、新菜单K下限、全部相关正除数及六真实索引平均。

输入准备和预检完成后，先向 Main 报告实际范围、尺寸、精确 SHA 与潜在问题，再写准备冻结 manifest。Main 的后续明确释放不在本包自动推断；此包不含求解器入口、一次求解标记或重试路径。
