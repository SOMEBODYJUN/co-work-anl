# 纯末位门槛、完整槽门槛与 SUMmin 的最终范围审读

Boss7，2026-11-16。本轮只写本报告；未执行 Git、sync、queue、board、checkpoint，未改 canonical、边、收据、registry 或研究入口。实读范围为下列指定对象记录、正文承重章节、现役关系、coverage 及 integration 的有关条目；不声称全文审读整份 registry/integration。没有运行优化器、策略枚举或 θ 最优值搜索。已知开放数学正常保留为开放数学，不把它记成构图工作未完成。

## 1. 结论与应改的最小范围

`CA-AGGREGATE-LAST-FLOOR-NO`（以下 A）精确否定 **m−1 个纯竞争槽**的全称加强 `W≥mθ_m`。`M-8f66f1abb0374762883f01d13235901c`（以下 E）问的是同一 m 人原游戏中 **m 个纯竞争槽**的 `W≥mθ_(m+1)`，现状仍为 open。两者不是同一命题。

这不只是一项下标辨别：用实际完整叶作为 E 所允许的一个纯背景，可解析证明 A 的两种明确见证都严格满足 E 的不等式。一般 K=6M+4 正编译输入甚至对其**每份完整原 SPE**都有 `W>mθ_(m+1)`；独立36客户例在源指定完整 σ 上有 `3θ_4≤57/2<34`。因此本轮对 A/E 的比较已闭合为“反例不触及该完整槽候选”，没有尚待搜索的 θ 最优值或工作流义务。

现役 609ace 边与 coverage 已准确区分这些量，**无须改边或 coverage**。`map/integration.json` 的 customer-attraction `open_math` 仍有不带槽数的旧短语“动态W≥mθ”，容易让读者误读为 A 已否的命题；只须补足 `θ_(m+1)` 与 m 个纯竞争槽。研究入口初读版本已准确写出 A、混合安全值及 SUMmin，所缺的 E 显式对照和同列相容性已由父Boss在本轮补入并复核；当前入口在这方面**无须再改**。第5节保留 integration 的精确最小替换及入口已付范围。

## 2. 固定相同输入后，四种不同金额及现行身份

共同模型为有限不同单位客户、有限非空共同标签目录及任意覆盖映射、单位顺序提供者；空覆盖、同覆盖异标签、重复、所有弱平局和全部有序离轨历史保留。完整 SPE 的偏离沿同一 σ 在改变后的历史真实续行。下列 W 都是零根背景的实际覆盖及总利润，不用于非零背景的剩余利润。

令 `q_B(T)=Σ_(x∈T)1/(1+c_x(B))`，B 为含重数的合法主题元组。

| 金额/候选 | 比较槽与优化次序 | 实际数学状态 |
| --- | --- | --- |
| `θ_m=min_(B∈S^(m−1)) max_T q_B(T)`；`W≥mθ_m` | m−1 个纯竞争槽，背景先定，再选最佳纯查询 | 全称聚合已被 A 否定；A v2 为 proved 反例对象，不是仍待证明的引理 |
| `θ_(m+1)=min_(B∈S^m) max_T q_B(T)`；E：`W≥mθ_(m+1)` | 恰 m 个可重复纯竞争槽，额外 query 不是真实新增玩家 | E v1，open；已有静态 `OPT_m≤2mθ_(m+1)`，动态聚合未付 |
| `v_k=max_p min_(B∈S^(k−1)) E_p q_B(T)=min_Q max_T E_Q q_B(T)` | 查询分布 p 公开，对手看 p、未看本次抽样；Q 可为相关背景分布 | 同槽 `v_k≤θ_k`；`v_m≥OPT_m/(2m−1)` 已证。完整 m 槽版本 `OPT_m≤2m v_(m+1)` 另已证，不凭此支付实际 W |
| SUMmin-full：`Σ_iR_i(p)≤W` 对同一任意 p；`R_i(p)=min_A E_p q_(Z_i(A))(T)` | `Z_i(A)` 保实际前缀、强制者及同 σ 的全部真实后继，恰 m 槽；每行列可随 i,p，不随已抽到 T | `customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests` v2，open；纯 p 与一般末行已付，一般混合 p 的跨行共同预算未付 |

当前记录定位与 pin：

- A：`CA-AGGREGATE-LAST-FLOOR-NO` v2 / proved，pin `699ba4cd7ebf119cdeb83f960aa4519f05068694f6f8507893ff071f155045ed`；主正文 S1，独立36例 S2。
- E：`M-8f66f1abb0374762883f01d13235901c` v1 / open，pin `6353907f3d019879fb7aef30beb5cac53ff1716baf87f8d6faedb45bcddce26a`；正文 S3《纯额外槽静态计数成立》。
- 完整槽静态桥：`M-73d3a9bedfd449d292f04323e540d4ca` v3 / proved，pin `da3d0bbed112a0897b1514eb63acac5dc6da174460f1264a731aa6b46a82e638`；S4《静态充分关系与完整槽数》，S5《完整槽的静态比较常数恰按2m计》。
- SUMmin：上述 e7 对象 v2 / open，pin `e37e6d0b6d0236152b44c5bd1d840157a5f2673bfcf99f9170af932a33e87332`；S4《真完整列、逐行最小与开放付款》。

## 3. 最强已付关系，以及不能由它们补出的金额

对同一目录，向任何 m−1 槽纯背景再添一个合法主题，各查询价均不增，故

\[
\theta_{m+1}\le\theta_m,\qquad v_{m+1}\le v_m,\qquad v_k\le\theta_k.
\]

所以 `W≥mθ_m` 若真会推出 E；一个违反较强式的见证不会自动违反 E。特别，`W=mθ_m−1` **单独**没有说明 `θ_m−θ_(m+1)` 是否至少 `1/m`。必须读具体客户输入、合法背景和完整策略，不能把 n 改名 m+1 后改变真实游戏人数。

完整槽静态桥对任意 m 槽背景分布 Q 取 `L_x=E_Qc_x`、平均主题边际 a，逐客户分解及 Jensen 给

\[
\mathrm{OPT}_m\le2m v_{m+1}\le2m\theta_{m+1},
\qquad
v_{m+1}\le M_{\rm path}.
\]

这里两个 m 分别来自最优比较的 m 个主题和背景的 m 个主题；不能换成 m−1 槽定理的 `2m−1`。现役 `cag-609ace-mixed-extra-slot-pays-pure-static-comparison` 的 `contribution` 正好止于前一项静态比较，明确留着 E 的动态部分。

SUMmin 若成立，则对一个真正的完整槽安全最优查询 `p*`，每行都是合法静态 m 槽列子集，故 `R_i(p*)≥v_(m+1)`，直接得 `W≥m v_(m+1)`；也可经 `M_path≤W/m` 推出 half。E 若成立，也由 `v_(m+1)≤θ_(m+1)` 给 `W≥m v_(m+1)` 并推出 half。这两个充分路线拥有一个共同的较弱后果，不产生它们之间的反向推导：尤其 `v≤θ` 不能把 SUMmin 或 `W≥mv` 升级为 `W≥mθ`。本轮没有证明两条开放候选全局不可比，只是准确指出当前已付不等式没有给出这种蕴含。

对于 SUMmin，纯查询可取 `A=T` 用真实 IC 逐行支付；混合时同一行不能看见已抽到的 T 再选 A。末行 `R_m=G_b−max_A D_b^p(A)≤u_m` 已有显式公式。这些都不支付一般早位、同一 p 的共同总金额，亦不把 v、θ 或真实受限菜单值互换。

## 4. 直接核验 A 的两个分支均不反 E

### 4.1 每 n≥3 的正编译输入：全部完整 SPE 的严格相容性

使用 S1 的具体两组势 F、其整数调和反演 x、`M=Σ|x_B|`、`K=6M+4`、`r_B=x_B+K`，保持原输入不变。另用 `CA-MOBIUS-FULL-HISTORY-EMBED`（S6）的全历史结论：K 大于充分门槛 `4M+1`，所以**每份**原完整 SPE 的 actual 根终局 z 都由 n 个不同标签组成。这里补全全部重复离轨历史的义务已经由 M2 承担，并非只检查指定路径。

对任意这样的 distinct 终局，写 Z 为其标签集合，`C=2^(2n)−2^n`。均匀偏置覆盖恒为 KC。S1 的 F 在纯 n 集上为1、在混合 n−1集上为−1、其余为0，故 signed 覆盖可直接求和：纯组 n 集为 n；一组仅有一个标签的混合 n 集为 n−1；两组各至少两个标签的混合 n 集为 n。因此不必固定 S1 指定辅助策略就有

\[
W(z)\ge KC+n-1.
\tag{1}
\]

额外查询面对这个**完整 n 槽背景**。对未用标签 a，其单位全类型偏置价为

\[
\beta_n=2^{n-1}\sum_{j=0}^{n}\binom nj\frac1{j+1}
=\frac{2^{2n}-2^{n-1}}{n+1}.
\]

调和反演在 Boolean 集合上的恒等式给其 signed 价
`F(Z∪{a})−F(Z)=−F(Z)`，因为 `|Z∪{a}|=n+1`。所以所有未用 a 的完整槽查询价都恰为 `Kβ_n−F(Z)`。

对已用标签，其单位偏置价记 γ_n；直接积分或二项式和给

\[
\beta_n-\gamma_n=\delta_n/n,\qquad
\delta_n=C-n\beta_n
=\frac{2^{n-1}(2^{n+1}-n-2)}{n+1}>n.
\]

最后严格不等式由 `2^(n−1)≥n+1` 及 `2^(n+1)>2n+2` 得到。已用查询的 signed 价绝对值至多 M，故
`Kγ_n+M<Kβ_n−1≤Kβ_n−F(Z)`，其中用到 K=6M+4、`β−γ>1` 及 `F(Z)∈{0,1}`。由此

\[
\max_a q_z(a)=K\beta_n-F(Z)\le K\beta_n.
\tag{2}
\]

E 对全部合法纯 n 槽背景取 min，actual z 本来就是其中一个，故 (1)—(2) 立即给

\[
\boxed{
n\theta_{n+1}\le n\max_aq_z(a)\le nK\beta_n
<KC+n-1\le W(z).
}
\tag{3}
\]

这是源**同一正编译输入族的每份完整原 SPE**上的结论；不只 S1 指定 σ 的扩展。它没有给 `θ_(n+1)` 的最优值，也不需要该值。不能外推成“每个违反 W≥nθ_n 的任意输入/σ 都满足 E”，更不能由这一输入族解决一般 E 或 SUMmin。

### 4.2 独立36客户输入：保留源指定 σ

S2 的 actual `z=(0,3,4)`、`W=34`。现役 d86 的 `comparison-review.json/three_player_36_proof` 逐兴趣类型给六个合法查询价

\[
(20/3,\ 35/4,\ 35/4,\ 22/3,\ 22/3,\ 19/2).
\]

仍取 actual z 作为 E 中一个合法的纯三槽背景，即得

\[
\boxed{\theta_4\le19/2,\qquad3\theta_4\le57/2<34=W.}
\]

这不求 `θ_4` 最优值，不把源指定完整 σ 扩成此输入的全部 σ；源登记仍为 finite，现役 d86 预算贡献仍保 conditional。已付的 `θ_3=12`、`v_3=10` 与这里的 `θ_4` 各按自己的槽数使用。

## 5. 现役图、入口与必要最小文字修正

本地读取快照：registry SHA `ee1148cd8c8053496e64e259902fb4890ea9a5add5a9c5a090b0d14739fc64ac`，coverage SHA `081e990b1fd3cca3e0394825875ce97f2073fbf0c172d4640037f817e1fdfa07`，integration SHA `c08cbe61cb3f074a4c82fada92835ff4868964d79123cca250c69c7092d8c0c9`。研究入口初读版本 SHA `35c0f946f133b4b7f7f0b37a54f38519a08cc18e7b5de39a0d0a94d30e18acd5`；补入阈值段后的复核版本 SHA `3132b6e1c0687bc34dd1d959f46b27e279a6cf05199d6df2635524e561d5421e`。其 d86 历史快照/其后已正式整合说明已更新，不再建议重复修此处。

末次补读时，正式新资产 `map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/all-spe-summin-budget.json` 已落盘，全文所载 ALL/unconditional/contribution 给出了第4.1节使用的全部σ、actual价精确式及更强共同预算；其 SHA 为 `2fcab5e1df6980e81a0880fe84554f1a1d9b0f83b14704a80481f56264476e86`。对应正式收据 `map/receipts/boss5-summin-all-spe-3b-7383c8bf44f753cc.json` SHA 为 `5814e7d63f26bf076b6eea897d5866687b898a696bf875e3f4a27c9fde5677d6`。父Boss确认该包当前done；本报告独立实读正式边的全部数学，不代称自己调用了任务状态接口。在上述registry快照中该新边尚未进入edge_files，故这里称其正式交付资产，不冒称已canonical。

| 实际文件/关系定位 | 核对结果 |
| --- | --- |
| `map/edges/customer-attraction-3a-3a-609ace1518772a58/mixed-extra-slot-pays-pure-static-comparison.json`；ID `cag-609ace-mixed-extra-slot-pays-pure-static-comparison` | accepted/unconditional 的局部静态贡献；source M73，target E；明示 m 槽与 `v≤θ`，remaining 为动态 `W≥mθ_(m+1)`。内容准确，无须改 |
| 同目录 `one-reentry-to-complete-path-menu.json`；ID `cag-609ace-one-reentry-to-complete-path-menu` | 单次重入列逐一等于 `Z_i(A)`，给 `M_path=M_1≥M_m=v_(m+1)`；不提供实际 W 付款。内容准确，无须改 |
| `map/edges/Boss7-summin-six-half-3b-3b-17d90d43aa54c665/summin-conditionally-pays-six-half.json` | accepted/conditional/whole；唯一开放 SUMmin 前提到六人原题，完整2m静态链无缺步；不把θ当v。无须改 |
| `map/edges/boss3-summin-budget-repair-d86bee169e3617da/{all-n-counterexample-summin-contribution,three-player-36-summin-contribution}.json` | 分别明确指定一般族策略扩展、指定36例σ；全 p 预算为局部贡献。没有宣称 E 被反或一般 SUMmin 已证。无须静改其量词 |
| `map/edges/Boss7-aggregate-floor-pivot-3b-3b-677e813b56475fca/aggregate-attacks-unconditional-not-pivot-relay.json` | checks/context；无条件 `W≥mθ_m` 的攻击与带(P)中继条件分开，没有反驳 E。无须改 |
| `map/coverage.json` 的 A、E、M73、SUMmin 四键 | A明确 m−1槽θ反族；E 的 comparison_scope 写 `θ_(m+1)` 且 reason 用银行族 `W=2m>mθ` 保留动态open；M73及SUMmin也各留共同付款。无须改 |
| `map/integration.json` → `archive_reviews["archives/customer-attraction"].open_math` 中含“动态W≥mθ”的条目 | 这是唯一需要本轮消歧的现行短句。其余多项数学仍各自open，不合并为一个θ命题 |

integration 最小替换：只把该条中的 `动态W≥mθ` 改成：

> 完整m槽纯门槛 W≥mθ_(m+1)（M-8f66f1abb0374762883f01d13235901c；区别于已否的m−1槽 W≥mθ_m）

同文件 `previous_note` 内的旧句是历史快照字段；可原样留存并由当前文字消歧，不必改写历史引用的内容或 SHA。本报告没有实施这些修改。

研究入口当前“聚合末位保底已否，但没有否定 SUMmin”节已补入 E 的稳定ID、恰m个竞争槽、`OPT_m≤2mθ_(m+1)`、`v_(m+1)≤θ_(m+1)`、一般正编译族的全部σ同列不等式和36例指定σ界，并链接本报告。逐项核与第4节一致，m−1纯 max/min、m槽纯θ、混合v与SUMmin均分开准确，**无须再作阈值文字修改**。入口末尾7383交付状态由父Boss随当前正式交付更新；不把该状态文字当作本数学比较的未付证明。

## 6. 接续判断与准确未付义务

当前 canonical 里 E 只由609ace的静态贡献接入，未直接记录第4节的正编译族相容性。该相容性是新正式7383边所证 actual 同列上界的直接推论，不是新开放研究问题；Boss 已决定本轮作为**已闭比较**记录，不另起任务或重复边。

若以后因实际检索需求确要显式保存局部逻辑贡献，准确 ALL 端点应为 `{CA-AGGREGATE-LAST-FLOOR-NO, CA-MOBIUS-FULL-HISTORY-EMBED}` → E，结论仅为 S1 的 K=6M+4 固定输入族每份完整原 SPE 严格满足 `W>nθ_(n+1)`；第4.1节给完整推导，不能标目标 whole。36例另由其独立源到 E，在 finite 身份下保存指定σ的 conditional contribution 即可，不能与一般族合并假称同一输入。这是可选保存方案，不是建议再起比较包。

真正未付且仍各自 open 的是：

- E：任意有限合法输入、每个 m≥1、每份完整原 SPE 的 `W≥mθ_(m+1)`。已证静态计数、自由进入势全局最大、真实偏离枝的覆盖上界、逐人银行反例都没有支付它。
- SUMmin：任意有限输入、全部 m 与完整 σ、同一个任意混合 p 的 `Σ_iR_i(p)≤W`。一般早位改变整份真实后继的共同金额仍缺；纯查询、末位精确折扣及指定反族的全 p 预算已付。
- 真正混合安全值聚合与原 half：本轮只使用它们的静态/条件接口，不声称原一般目标或六人目标已关闭。

已经付清的 A 的反例存在性及本报告 A/E 范围比较，不在上列未付义务中。

## 7. 实读 source/edge SHA 定位

以下 SHA 为完整文件原始字节；章节名称是数学定位。本轮源正文 S1—S7及共同模型全文读取，registry 只实读本题精确对象记录；d86比较文件实读 `shared_row_argument`、`three_player_36_proof`、`all_n_positive_compilation_proof` 及边的量词/解释，不把大证书或其作者旧运行当成本轮新运行。

| 标记 | 完整路径与主要数学定位 | SHA256 |
| --- | --- | --- |
| S1 | `archives/customer-attraction/state/反例/三人及以上聚合末位保底--反例.md`；《两组子集势及全部distinct历史的辅助策略》《从带符号势到合法单位客户的精确接口》《最坏末位背景：为什么重复历史不会降低θ_n》《福利、覆盖及明确未否定的命题》 | `d316702ecc98a5976769d1d2e0094341474e0c4655deaac825bc208ae81d36e7` |
| S2 | `archives/customer-attraction/state/反例/三人聚合末位保底--反例.md`；《终局算术与全部历史策略》《θ_3、真正安全值及失败范围》 | `f2ff6b486d46f5e05d9acb2497ec1114ac8ab4698460fb46656d320e640fe4c0` |
| S3 | `archives/customer-attraction/state/资源/额外槽饱和势与真实偏离分支覆盖上界--资源.md`；《纯额外槽静态计数成立》《自由进入势有全局最大，但不生成指定SPE尾》 | `8ac4dd871ab891e20bf9f80bc03fe8640efa0887dd4d590a1f6ee58f4e1ffaaa` |
| S4 | `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`；《真完整列、逐行最小与开放付款》《静态充分关系与完整槽数》 | `e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a` |
| S5 | `archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`；《末位的精确式与一份已付款松弛》《完整槽的静态比较常数恰按2m计》《从未证全路径预算到half的条件推导》 | `a2c504c39c6b1ab1d4a2a8d9f48b5a977ad2aa648aab0ac066771d22ff5ccf2a` |
| S6 | `archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md`；《两个游戏和精确的策略投影》《所有重复历史上的严格支配证明》《无重复子树的等价及重复子树的扩展》 | `e6e06a43973f7c37673b498074475fdf8aa37338d448aff53b2bf9b2e7fa0dd4` |
| S7 | `archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md`；《任意相关背景的完整证明》《与末位值、真实菜单和顺序收益的区别》 | `034c940129b4ef2e1b5a2902f9256f9dbfed5fbc8bf6750c4403217db3a6b15f` |
| 定义 | `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| 609静态 | `map/edges/customer-attraction-3a-3a-609ace1518772a58/mixed-extra-slot-pays-pure-static-comparison.json` | `2fd49eab666413b5034a5f8eb1e9d9a1612013ead42894952d2d9dfe4e591902` |
| 609菜单 | `map/edges/customer-attraction-3a-3a-609ace1518772a58/one-reentry-to-complete-path-menu.json` | `fee4b30fd401034299dce627dcd41c6d069dc4b4c3f6e9b61f34fd7db20a5e7f` |
| 六人条件whole | `map/edges/Boss7-summin-six-half-3b-3b-17d90d43aa54c665/summin-conditionally-pays-six-half.json` | `699209dd36c7bc2c5f7b5e040bb2adffe481cea5a35bd52188447b03b7974a5f` |
| d86解析 | `map/edges/boss3-summin-budget-repair-d86bee169e3617da/comparison-review.json` | `367e6ffe393a1b80fa04c433da84b50ec491a5e157244c2b2770950b5aca1671` |
| d86全n边 | `map/edges/boss3-summin-budget-repair-d86bee169e3617da/all-n-counterexample-summin-contribution.json` | `4eb5151221da99f7b46822bc4615dff81e6bca8febdb44d4ef1b21410bdd6a71` |
| d86三人边 | `map/edges/boss3-summin-budget-repair-d86bee169e3617da/three-player-36-summin-contribution.json` | `b0802cd74bc7d229396e1ebb65718b787b5aeee7022faee6010de0526aae5131` |
| 7383全部σ边（正式交付，尚待本快照整合） | `map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/all-spe-summin-budget.json` | `2fcab5e1df6980e81a0880fe84554f1a1d9b0f83b14704a80481f56264476e86` |
| 枢轴边界 | `map/edges/Boss7-aggregate-floor-pivot-3b-3b-677e813b56475fca/aggregate-attacks-unconditional-not-pivot-relay.json` | `7ef5fbfcd18263885753a16220bdbc0500146b8f8f0e704723e2fc16cce0631a` |

入口合同亦已实读：`AGENTS.md` SHA `20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`；`research/IMPLEMENTATION.md` SHA `fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`；`prompts/03-map-worker.md` SHA `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2`。这些工作合同不充当数学证明。
