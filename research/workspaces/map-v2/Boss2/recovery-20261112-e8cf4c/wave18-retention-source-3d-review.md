# Wave18：RET 与真实私有块账本的独立 source-only 3D 审读

本报告只核当前两个源对象及其精确静态关系，供 Boss2 当前 integration 的来源审读使用。它不是主 coverage 交付，不替代 Boss1 的正式 repair，不修改 repo、Git、队列、源正文、registry、native 或其它 Boss 资产。所有任务状态结论仅来自本地已提供的 task definition / supersedes / receipts；未查询远端实时归属，也不以 claimed 或静默作接管依据。

## 结论

1. 当前 RET/SWAP 和私有块 SHARE/LEDGER/TOTAL 都保持已证；没有发现这两个当前对象的可检验数学错误。RET 的全前缀累计付款加强已经被真实完整 SPE 族反驳，不能再称开放命题；这不影响两个恒等式，也不反驳仅终点 half 或私有块共同付款 B?。
2. 历史 `retained-comparison-pool-controls-static-private-block-loss` 的**局部 contribution** 仍成立，方向不用反转：固定根池给静态机会损失上界；在每个位置重新建立自己的最优余槽池后，单槽净损失给非负静态交换信用 ε。它没有支付实际收益，也没有证明完整目标 LEDGER。旧边本身已有 contribution/remaining，不能误读成整条定理由 RET 单独推出。
3. 必须把根固定池的 `L_t` 与局部重启的 `L_1^{loc}` 区分，局部套 RET 时先删掉固定过去覆盖 P。准确式为 `G_t ≤ L_t`、`L_1^{loc}=δ_i+平均_j ε_ij`。这里的“上界”方向不能反写，不能推出 `L_t≤P_t`、`δ_i≤u_i` 或跨强制分支付款。
4. 旧边已经不在当前 `data['edge_files']`，仅是明确历史资产。**在 Root 本轮同步后的新快照中，Boss1 的 `boss1-wave12-ret-source-repair-1559410bdf704b13` 与 `...-8324c735e389d989` 均已 done，分别有 19 / 23 资产的 receipt；1559410 已正式 replaced 本条旧边。** 先前本地 claimed/无 receipt 的观测已过时，不作为当前结论。最新读取 registry 时新替代边尚未进入 canonical，故是“原 owner 正式 repair 已交付、待 Root assemble”，不再是“待原 owner 交付”。本报告保持独立 source-only 审读，不接管、不代交回执，也不据此单独改图。

## 当前身份、字节与实际读取范围

使用 `tools.research_runtime.load(root, verify=False)` 获取 `(data, objects_dict)`，只按 `data['edge_files']` 判断当前 canonical。随后对本报告涉及的每项当前正文/证据引用逐一核实际文件 SHA，而非把 SHA 一致当作数学通过。未运行成熟科研程序、solver、旧 audit、树枚举、LP 或扫描。

| 对象 | 当前版本 / 状态 | registration pin | 主正文 SHA-256 |
|---|---|---|---|
| `customer-attraction/optimal-completion-private-block-ledger` | v4 / proved | `b8ef6b0b5064d9918e270459f616577f4908c5284dd91336563c7b40b07d133c` | `5bdc6de1c6e8aa7163903d8339badd8b757e8c1836c21ae6d320c4fe99cc2d8e` |
| `optimal-comparison-pool-net-exchange-and-random-retention-identity` | v3 / proved | `bc70276219fc89dec47233d96d34d864924263952d33c2deeaf870b5d3a10a39` | `400665b8ed3932fb36b7562ced86c182c79852c58d2d2e254ccc87b77c0e0cbe` |

完整读取了 AGENTS、IMPLEMENTATION 的当前阶段/输入/边/替代协议及 `prompts/03-map-worker.md`；完整读取了两对象当前 registry contracts、两篇主正文，以及以下必要数学输入：

- `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`，SHA `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`：完整模型，尤其标签、重复、真实有序后继、根福利与背景剩余利润之别。
- `archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md`，SHA `b42e57e311686c2d737d6ade6642efaa05caa28dded02c9cf035ef0ed9c70072`：完整单位客户构造、末位全部分类、全部非末位真实续局证明及最优支持/补全公式。
- `archives/customer-attraction/state/计算/四人首步余额完整策略证书--计算.md`，SHA `60616835c921d4c336019b9f5e107980ac35db330d9c78c3244057327a0e7a9c`：完整证据职责与结果正文；未声称本轮重新读取 259 条底层 JSON 或重放 1554 比较。本轮对普遍反例的认证依上述已完整读取的解析证明，不依有限报告。
- `archives/customer-attraction/state/程序/比较池私有块与平方旧负载信用的原诊断--程序.md`，SHA `6a56e68dca66a3bf88797412577097bb0a399567b1d3f3afb6284db7c97a5a94`：FLOOR/POWER2 精确负点及其模型、停止边界；没有重跑成熟程序或据历史扫描数量宣布新认证。
- `archives/customer-attraction/state/资源/最优首动作菜单原稿的两级信用与真实孩子总账--资源.md` 的完整 `私有块版真实孩子递推` 节，SHA `3c14ddc66e721ffeb750f7e155b1c15e7009f0c14d9b83a6f162c3886cc2cf2d`。
- `archives/customer-attraction/state/资源/一般安全付款检查点与中继分支导航--资源.md` 的完整 `接私有补全总账为何仍缺actual容量` 节，SHA `4f7c985a12523e5098baf1db1036eb6197e60ee19c728cad37869079cb29fd8d`。

还定向读取了当前 `CA-PREFIX-BALANCE-NO`、`M-dfcc6e32210c40c3b80ff0808d132d0b`、`M-8f6719ad729d4806b16e6288dff1806f` 的完整 contracts，以及旧边、三代相关 receipts 的本对 coverage、asset 与 supersession。

## 完整承重：固定池、真实静态补全与局部交换

以下用 \(\mathcal L_t\) 表示 RET 的随机池期望净损失，用 \(\Lambda_{ij}\) 表示私有块 LEDGER 的真实强制尾份额，避免把两个源都记作 L 的不同量混在一起。

### 1. SWAP 是净差，必须扣 actual 独有退款

固定实际旧并集 C、比较槽索引池 M、删除索引 j、当前行动 A。令

\[
U=C\cup\bigcup_{k\in M}T_k,\qquad
V=C\cup A\cup\bigcup_{k\in M\setminus\{j\}}T_k.
\]

则集合差 \(U\setminus V=T_j\setminus(C\cup A\cup\bigcup_{k\ne j}T_k)\)，而 \(V\setminus U=A\setminus(C\cup\bigcup_{k\in M}T_k)\)。因此

\[
|U|-|V|=lost-new.
\]

这是逐集合恒等式，不需最优性、顺序或 SPE。重复主题仍按槽索引保留，不能先把多重集变成不同标签支持再采用均匀概率。gross lost 不等于净缺口，删除 new 会改变结论。

### 2. RET 及相邻退款是已付的组合恒等式

根比较元组固定为 \((T_1,\ldots,T_m)\)，\(O=\bigcup_jT_j\)。均匀随机排列其索引，删去前 t 个；保留索引为 \(R_t\)，实际前缀为 \(C_t\)，设

\[
U_t=C_t\cup\bigcup_{j\in R_t}T_j.
\]

对 \(x\in O\)，它在比较槽的重数为 \(d_x\ge1\)，全部覆盖索引已删概率

\[
p_t(d_x)=\frac{\binom{t}{d_x}}{\binom m{d_x}}
\]

（t<d 时为零）。逐客户比较 \(|O|-|U_t|\) 后取期望，得到

\[
\mathcal L_t=|O|-\mathbb E|U_t|
=\sum_{x\in O\setminus C_t}p_t(d_x)-|C_t\setminus O|.
\]

新客户 \(N_t=C_t\setminus C_{t-1}\) 给相邻式

\[
\mathcal L_t-\mathcal L_{t-1}
=\sum_{x\in O\setminus C_t}(p_t-p_{t-1})(d_x)
-\sum_{x\in N_t\cap O}p_{t-1}(d_x)-|N_t\setminus O|.
\]

末两项是真 actual 新覆盖退款。\(\mathcal L_0=0\)，\(\mathcal L_m=|O|-W\)，中间可为负；随机只发生在辅助比较索引上，未定义玩家混合策略或可信随机承诺。

### 3. 固定最优根池确实控制实际静态补全机会损失，方向是 G≤L

现在仅增加 \(|O|=\operatorname{OPT}_m\)。每次保留恰 m−t 个合法比较槽，故对每个随机排列

\[
F_{m-t}(C_t)\ge|U_t|.
\]

取期望、移项得

\[
\boxed{G_t:=\operatorname{OPT}_m-F_{m-t}(C_t)\le\mathcal L_t.}
\]

精确差为

\[
\mathcal L_t-G_t
=F_{m-t}(C_t)-\mathbb E|U_t|\ge0.
\]

因为任意 t 实际槽加 m−t 补全槽是合法 m 槽组合，又有 \(G_t\ge0\)。在 t=m 时 \(F_0(C_m)=W\)，所以 \(G_m=\mathcal L_m=\operatorname{OPT}_m-W\)。这不提供任何实际收益上界。特别 \(G_t\le\mathcal L_t\) 不能倒过来证明随机账已由实际收益付清。

沿实际路径，\(G_t-G_{t-1}=\delta_t\)。对固定根池定义松弛 \(a_t=\mathcal L_t-G_t\ge0\)，则

\[
\mathcal L_t-\mathcal L_{t-1}=\delta_t+a_t-a_{t-1}.
\]

松弛差没有固定符号。这明确排除从全前缀静态上界直接读成每步 \(\delta_t\le\mathcal L_t-\mathcal L_{t-1}\) 的做法。

### 4. 局部重启必须去掉 P，得到每槽 ε 及均值

在实际位置 i，固定过去并集 P、余 r、规定 S。取**当前**达到 \(F_r(P)\) 的最优 r 槽元组，令

\[
O_i=P\cup\bigcup_{j=1}^rT_j,\quad
D_j=T_j\setminus(P\cup\bigcup_{k\ne j}T_k),\quad
e_i=|S\setminus O_i|.
\]

为严谨使用无背景 RET，应将单位客户空间限制到 N∖P，令 \(T'_j=T_j\setminus P\)、\(S'=S\setminus P\)。固定 P 在交换前后都在，不参与随机删除；否则把 P 内且未在任何槽出现的客户塞进 \(d_x\ge1\) 是非法的。

删除 j 并加入 S 后的合法 r−1 槽补全覆盖数是

\[
V_j=|P\cup S\cup\bigcup_{k\ne j}T_k|
=F_r(P)+e_i-|D_j\setminus S|.
\]

最优补全只保证 \(F_{r-1}(P\cup S)\ge V_j\)，于是

\[
\varepsilon_{ij}:=F_{r-1}(P\cup S)-V_j\ge0,
\]
\[
\boxed{|D_j\setminus S|-e_i=\delta_i+\varepsilon_{ij}},\qquad
\delta_i=F_r(P)-F_{r-1}(P\cup S).
\]

对局部 r 索引均匀选删槽，RET 首步只可能删除重数一的未救客户；这些客户恰是各 \(D_j\setminus S\)。因此

\[
\boxed{\mathcal L^{loc}_1=\frac1r\sum_j|D_j\setminus S|-e_i
=\delta_i+\frac1r\sum_j\varepsilon_{ij}.}
\]

这个局部池通常不同于根池随机删到位置 i 后的保留池。每个位置重新选最优池可以用于各自 EX1，但不是同一随机过程，不能把各局部 \(\mathcal L^{loc}_1\) 拼成根 RET 的相邻差或望远镜。

EX2/EX3 另用当前补全最优性：将一槽/若干槽换为同样数量合法主题，覆盖不能超过 \(F_r(P)\)，故比较并集外新增不超过删除私有部分。它们也不含真实收益支付。某 \(D_j=\varnothing\) 时 EX2 强制所有合法 A⊆O_i，e=0，且该槽可删而不降原最优值，故 δ_i=0；重复/空槽退化没有漏掉。

## 完整承重：怎样从静态净损失到真实 LEDGER，哪里仍未付款

固定**同一精确有序历史**，强制当前改选 \(T_j\)，其余沿原完整 σ 真实续行。当前收益记 d，当前在 D_j 外的份额为 d_out，同枝后继在 D_j 的总份额为 \(\Lambda_{ij}\)。因为 D_j 无过去覆盖，当前覆盖整个 D_j，所以每名该块客户的一单位价值恰分给当前及本枝后继：

\[
|D_j|=d-d_{out}+\Lambda_{ij}.
\]

这是 SHARE；将其误套到有旧覆盖的客户会漏过去玩家份额。SPE 仅在下一步提供原真实 IC：\(\Gamma_{ij}=u_i-d\ge0\)。将静态净差与 SHARE 合并：

\[
\begin{aligned}
\delta_i-u_i
&=|D_j\setminus S|-e_i-\varepsilon_{ij}-u_i\\
&=\Lambda_{ij}-d_{out}-|D_j\cap S|-e_i
-\varepsilon_{ij}-\Gamma_{ij}.
\end{aligned}
\]

只消费一次完整 d≤u_i；不能把块内当前份额与 d_out 各再领一份 u_i。沿 actual 路径 \(\sum_i\delta_i=OPT-W\)，且根全收益守恒 \(\sum_i u_i=W\)，故

\[
OPT-2W=\sum_i[\Lambda_{ij}-d_{out}-|D_j\cap S_i|-e_i
-\varepsilon_{ij}-\Gamma_{ij}].
\]

这完整证明当前 LEDGER/TOTAL，并未把它降格成 open。开放的是额外共同付款：能否为每份原完整 σ 联合选择各 i 的最优补全/索引，使

\[
\sum_i\Lambda_{ij}\le\sum_i[d_{out}+|D_j\cap S_i|+e_i].
\]

该 B? 删除了非负 ε、Γ，是 half 的充分条件，未证必要性或等价。\(\Lambda_{ij}\) 属于各自互斥强制子树；不能用 actual 继任人的 u 或 surplus 未经共同容量构造逐项替换。某离轨继任人 IC 只给 \(u^{off}\ge u^{copy}\)，不提供所需的 \(u^{off}\le u^{actual}+退款\)，复制动作还会改后继。

当前资源中的双孩子递推同样只给

\[
R_h-u=R_{hS}+\frac{r-1}{r}R_{hT_j}
-\frac{\varepsilon+e+\eta^{priv}}r
-\frac{r-1}{r}(f+\xi)-\Gamma.
\]

两个 R 属于原 σ 的两个真实孩子；尾 Y_j 静态放到 S 后用于 ξ≥0，并不声称仍为 S 后 SPE。该递推没有额外支付跨孩子利润。

## 当前新增反驳为何精确，以及不能迁移哪些全称量词

当前完整证明给每个 n≥4 的单位客户族，令 x=n−2，目录 A、B、L_1,…,L_n。普通叶各有 x 个仅 L_j 客户、1 个 A/L_j 客户、x 个 B/L_j 客户；特殊叶各有 x 个仅 L_n、x 个 B/L_n、n−1 个 A/B/L_n 客户。叶两两不交，每叶有只能自己覆盖的客户。

完整策略：根选 A；非末位非空历史若此前全 B 则选 A，否则选 B；末位按真实份额最佳回复，以 B、A、L_1,…,L_n 打破平局。源解析分五类证明所有末位最优，再分四类证明全部非末位真实偏离 IC，故不是只冻结 actual 后继或给出可行边际。

叶支持满覆盖且唯一：每叶 x>0 个目录私有客户迫使任何满覆盖 n 槽元组包含每叶一次；因此所有最优元组仅差排列，每个客户 d_x=1。实际第一步 A⊂O，

\[
OPT_n=2n^2-2n-2,\quad |A|=2(n-1),\quad
u_1=n-1/n,\quad W=n^2-2.
\]

在 A 外各叶有 2x 客户。余 n−1 槽不用 B 最多补 n−1 叶，用 B 则至多再补 n−2 叶的私有 x 客户，两类最大新增均为 2(n−1)x。因此

\[
F_{n-1}(A)=2(n-1)^2,\quad
\delta_1=OPT-F_{n-1}(A)=2(n-2).
\]

RET 同时给

\[
\mathcal L_1=\frac{|O\setminus A|}{n}=2(n-2)=\delta_1,
\]
\[
\mathcal L_1-P_1=\delta_1-u_1=n-4+1/n>0.
\]

本族所有叶的 \(|D_j\setminus A|=2(n-2)\)，e=0，所以每个 ε_1j=0：这里并非一个随机池松弛过大的伪失败，而是真实静态首步机会损失本身超过实际收益，且对所有最优池都失败。

n=4 的直接可检验值为：22 客户、OPT=22、W=14、F_3(A)=18、δ_1=\(\mathcal L_1\)=4、u_1=15/4，差 1/4；终点 `2W−OPT=6>0`。普遍族终点余量为 2(n−1)>0。故当前 `M-dfcc...` 的全前缀全称确实 refuted，甚至把比较元组量词放宽成“存在某个最优元组可付清全部前缀”也无法避开该族。

不能迁移为：RET 为假、终点 half 为假、B? 为假、任何非局部跨期付款都不可能、旧逐人 D 已反驳，或任意余人数带背景利润 F_r(b) 的结论。总覆盖 F_r(P) 与背景剩余总利润 \(\max\sum_x c_x/(b_x+c_x)\) 是不同量；旧61客户 FLOOR 和 POWER2 只反各自精确局部模板。

## 历史边与当前可复用关系的逐项差别

旧文件：`map/edges/customer-attraction-3a-3a-00c291811e5de4b9/retained-comparison-pool-controls-static-private-block-loss.json`，本地资产 SHA `f787c849c072e77caad5bb0698969680518693e4495616c720fe8bd29c5ba4ed`。它写 accepted 是**历史文件内字段**，不等于当前 canonical accepted。

| 项 | 历史资产内容 | 当前审读结论 / 正式 repair 所需 |
|---|---|---|
| source pin | `38e6d2a40b21871b26c4c206333f740613ae4b7cc07e2e5dcb73d202f08c0c84` | 改为当前 RET v3 pin `bc7027…a39`，并按当前全文重核语义 |
| RET evidence SHA | `aeb776e8877dadb113c2039c34007a2a5509a77dfea8231a3ce485216eeeb218` | 当前为 `400665…cbe`；旧值不可继续绑定 |
| target pin / 账本正文 | ledger pin `b8ef6…133c` / SHA `5bdc6…2d8e` | 两者与当前相同；数学不因 source 改版消失 |
| 方向 | RET → ledger 的静态 contribution | 保该方向，不能改写为 ledger 整条定理由 RET 单独推出 |
| 根固定池式 | `OPT−F_(m−t)(C_t)≤L_t`，末期等号 | 完整成立；保持固定同一池、实际退款和重复槽 |
| 局部式 | `lost−new=δ_i+ε_ij`，均匀 j 得“本节点 L1” | 完整成立；须显式写 `L1^loc`、删除固定 P、用当前真正最优 r 槽池 |
| contribution remaining | 还需 SHARE、IC、actual 望远镜，随机池不给跨步付款 | 继续保留，并明确这些步骤已由目标正文证明；缺的是**从 RET 单独推目标**而非目标定理未证 |
| 前缀付款状态 | 旧边无正面付款断言；旧收据已记负前缀族 | 当前 `M-dfcc` 从候选变成 refuted 的来源状态必须接回；不能恢复成待证全前缀机制 |
| 本次地位 | 旧关系文件已退出 canonical | 只作历史资产；Boss1 新1559410收据已 replaced 到新路径，最新读取时待 assemble 入 canonical；本审读未发布边 |

因此最小数学修订不是撤销静态定理，也不是反转不等式，而是保 contribution、消除根/局部 L1 歧义、更新来源 pins 与精确退款/背景映射、明确全前缀付款已假。relation_mode 在全部已列静态最优性条件内可继续 unconditional；不应凭空给尚未付款的 whole_result。

若要作“旧 v2 全文究竟每句改了什么”的严格版本差分，本地本次已提供的旧边/收据只有旧 pin 与旧正文 SHA，没有旧正文完整字节或旧 v2 contract 快照。本报告不伪称已读它们，也不自行扩大访问。精确需求为：RET v2、registration pin `38e6d2a40b21871b26c4c206333f740613ae4b7cc07e2e5dcb73d202f08c0c84` 的完整 registry 记录，以及该主正文旧 SHA `aeb776e8877dadb113c2039c34007a2a5509a77dfea8231a3ce485216eeeb218` 的完整文件。当前关系的独立证明及旧边语义对照不依赖取回这两个历史输入。

## 定向 canonical / 任务 / receipts 查验：同步后当前状态

- 最新本地读取时，`data['edge_files']` **不包含**上述旧 retained 文件，也暂未包含新1559410替代文件或新8324净swap文件；Root 正在另行 assemble。该快照中，本对直接端点相关的 canonical 资产只有 `private-block-common-payment-condition-to-half.json`，它以 `{B?, ledger}` ALL 条件推出 Q-CAG-HALF；本次已读并核其条件方向，没有把 open B? 当 proved。
- 同一快照中没有 source 或 target 是 RET 的 canonical 直接边，也没有以 `M-dfcc...` 为端点的 canonical 替代反驳边。与 CA-PREFIX-BALANCE-NO 有关的四条既有 canonical 边分别讨论首步固定系数、释放独占信用阈值、末对 quantile、背景利润实例化。以下新 done 收据须按其真实替代交付进入 assemble；旧快照“未见替代”不能据以忽略它们。
- 本地 supersession 链为原任务 `customer-attraction-3a-3a-00c291811e5de4b9` → `ca-eta-exact-current-repair-repair-14fd2eadba3fde65` → `boss5-eta-status-round55-repair-6cda1bce3d48b546`。后三代相关收据都按同一旧资产 SHA retained，并保 RET 旧 pin；它们的数学说明已经写出随机池不付款及负前缀边界。不能把这些旧 done 再算作当前 v3 repair 完成。
- `boss1-wave12-ret-source-repair-1559410bdf704b13` supersedes 上述 Boss5 任务，核心同时包含 ledger 与 RET，输入 pins 正是当前版本；同步后本地 state=`done`、owner=`Boss1`，19 资产 receipt 已出现。它 retained 18 旧有效资产，明确将旧 retained 边 `replaced` 到 `map/edges/boss1-wave12-ret-source-repair-1559410bdf704b13/retained-comparison-pool-controls-static-private-block-loss.json`，新边 SHA `a2e109495d6cece05136852d11f4e36403d35c3611ff6e9a5915b0e4d744f3b2`。该 receipt SHA 为 `cdbd1109933de6d5b43f8336f162cc50665b5b82e061406b61e81d8bb1584b30`。本次全文读取新边、本对 coverage 与 supersession，确认它保 contribution、更新当前 pins/证据、明确根池/局部池及全前缀 refuted 范围。19 项资产当前实际字节均与 receipt SHA 匹配。
- `boss1-wave12-ret-source-repair-8324c735e389d989` 同样已 done、owner=`Boss1`，23 资产 receipt SHA 为 `bb6b76b922aabf1e36abbccd3c7ef2c806e9b7fa59342f978f23258479ef8a21`。它 supersedes `boss6-bank-status-repair-repair-5f402448a1964e8e`，本对不在其核心；RET 是共享 read 依赖。它对三个旧局部关系各作新路径替代，不能把该包冒称为 ledger 主覆盖。23 项资产当前实际字节均与 receipt SHA 匹配；本报告只审其与本对有关的局部关系，不重领或重审整个19核心包。

### 新1559410替代边的数学核验

该新边给的根静态 \(\mathcal S_t\le\mathcal L_t\)、末期等号、局部 `lost−new=δ+ε` 及均值，与本报告前面的独立推导一致。它在 conditions/explanation 中已明确固定根池与局部重新最优池不是同一过程，并保留全部 actual 独有退款与重复索引；不会从辅助随机化推出真实收益付款。

它另写“此族恰使 \(\mathcal S_t=\mathcal L_t\)”而不只 t=1。本次独立确认这一全 t 扩展也正确：t=0 两边为0，t=1 如上为 2(n−2)；t≥2 时 actual 并集恒为 A∪B，未覆盖者恰是 n(n−2) 个各叶目录私有客户，根最优叶池中每个 d=1，故 \(\mathcal L_t=t(n−2)\)。任一剩余叶槽恰可补 n−2 个遗漏客，剩 n−t 槽可达到且不可能超过 \((n-t)(n-2)\)，所以 \(\mathcal S_t=t(n−2)\)。因此这一句不构成新边错误。

新边的 remaining 明确保留“完整 LEDGER 还另需 SHARE、当前 IC、actual 望远镜”，同时没有把已证目标改称 open；开放的仍是跨分支共同付款。其范围和当前两源吻合，允许 Root 作为正式已交付替代关系继续整合。

### 新8324三局部替代关系与本对的关系

本次全文读取三条新 JSON，定向核各自条件与作用，不把其它19核心的全部证明算作本次新读：

| 新路径文件（共同目录 `map/edges/boss1-wave12-ret-source-repair-8324c735e389d989/`） | SHA-256 | 与本对的实际作用 |
|---|---|---|
| `private-block-witness-violates-net-swap-step.json` | `09f2f76f6a5419959ffb43e8d548185ffc99387e85316044373d695e01badb5d` | 从 M-140 的局部 FLOOR 见证到 RET 的局部 contribution；h=A、池BCD、new=0、损失10/11/10，均匀一步条件期望31/3>u9；明确不是根无条件RET全前缀反例 |
| `root-tax-controller-restricts-to-private-floor.json` | `0df997a3c418daa370914fb6be121e40d57633b9eb24e497bf751a525963fd1c` | 原真实AAAF控制器特化到同一 h=A 的FLOOR完整见证，不直接推出随机池恒等式或全前缀反驳 |
| `root-tax-controller-restricts-to-square-credit-failure.json` | `c21ddde4b76948754f60f21d9699056a03ed994862cf8efb4c212772ce772b02` | 同一实际u9/真尾AF与静态F3=36、F2=21、平方ΔH=25/6给−11/6；保背景利润与总覆盖的区分 |

上述局部式与已读当前诊断证明一致。未发现它们对 RET 或 LEDGER 的范围冒用；其中净swap边已明确将当前全前缀已反驳状态归给独立CA-PREFIX完整SPE族，没有继续将“可更换最优池”当作修复该全称不变量的办法。本报告没有新跑61客户全部历史或77静态值；这些成熟证据按现行原证明继承，Root 的更广原包核验不由本source-only报告冒充。

## 对当前 pending 的精确处置建议

Root 可以据本报告在其授权的 archive/source 审读范围记录：当前两源 contracts 与必要证明已实读；RET/SWAP、ledger 整体保持 proved；全前缀付款加强 refuted；静态 contribution 在新源下有效，且原 owner 的1559410新替代已经 done。本报告可完成**这两个来源的理解义务**，不会自动生成主 coverage 或 canonical 边。实际关系交付现在应按新 done 收据与 Root assemble 处理，不再保持一个已过时的“待 owner 交付”判断。

本source-only审读支持清的 object source-review 范围仅为 `customer-attraction/optimal-completion-private-block-ledger` 与 `optimal-comparison-pool-net-exchange-and-random-retention-identity`。正式关系 pending 要由已到的1559410/8324替代收据及 assemble 的实际结果结算，不能仅凭本报告手删，也不能复活旧路径。其余 pending 的 CA-ROOT-TAX-NO、M-140、M-8a、M-dfcc 来源审读由 Root/各负责线按实际读取另行处理，本报告不把邻接三新边的定向核验冒充全包 coverage。

正式 owner 已把当前字节/端点与数学范围落到实际替代资产，并在 supersession 将旧 retained 边标为 replaced。剩余流程是 Root 按当前有效交付完成 assemble 与所需的整合审读，确认新 canonical 清单及 pending；这不是要求重证已证 RET/LEDGER，也不是本次接管该任务。

## 可检验问题与没有发生的结论

**已确认的问题**：历史 retained 边使用过时 RET pin/SHA，故不可直接当当前 canonical；局部背景/根池同名 L1 若不作上述区分会造成错误使用；任何“随机保留余额逐前缀已经由实际收益付清”均被 n=4 的 `4>15/4` 精确反例直接否定。

**未发现的问题**：当前 RET 和 ledger 的陈述、精确恒等式、退款符号、单槽最优性、IC 方向与路径望远镜没有可检验错误。当前源已明确标记前缀加强 refuted，没有继续把它冒充定理。当前完整解析反例不是有限观测，也不能被改称 open。没有把 B?、仅终点付款、旧逐人 D 或 half 从未证升级为 proved 或从 open 改成 refuted。

### 本地读取快照指纹

以下仅用于复查报告读取的是哪一份本地快照，不替代数学判断，也不代表远端实时状态：

| 路径 | SHA-256 |
|---|---|
| `research/registry.json`（同步后最后读取） | `57f40e76c4bc4ce63f09ea2293a612da61a4f7453a67bff0fec8b23b34ca2271` |
| `map/integration.json` | `f8851173bd017363b18d7a286f0ed8ada3f9e888757556f2c44dccc0e0ec7e3b` |
| `map/coverage.json` | `5b4a2f128f77c7fa46095f20216f8abc9757a6c2766357bc4bd310f6c9af6f05` |
| `research/operations/map-v2/tasks/boss1-wave12-ret-source-repair-1559410bdf704b13.json`（done） | `a05af6af00a547d71513a3226e8316f073aacb7d9783540af518f47c26eb77ec` |
| `research/operations/map-v2/tasks/boss1-wave12-ret-source-repair-8324c735e389d989.json`（done） | `d8f0627fda4310b49368fc667daa425aba2d153c11df214e9dc7a4f80403590f` |

初读时1559410/8324的本地任务曾为claimed且无新收据；Root同步后已按以上done状态、真实新边和收据完整改写当前处置。所有canonical暂未入清单的陈述仅定位上述最后读取快照；Root随后assemble产生的新清单以其实际输出为准。

最终修订时间（UTC）：2026-11-12 22:36:24 UTC。本次修订增加的实际读取范围为1559410新静态贡献边全文、本对coverage与supersession，8324三条局部替代JSON全文及相关coverage/supersession，并核两份收据全部19/23资产SHA；没有将其它21/19核心的成熟证明归作本轮新读或新证明。
