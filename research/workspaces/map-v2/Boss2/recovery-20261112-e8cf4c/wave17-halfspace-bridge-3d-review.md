# Wave17：七极大固定路由大小半空间到原六人 half 的独立 3D 桥审查

身份：Boss2；本次是只读桥审查，不认领 3A，不创建任务、边或收据。只读 clone `/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`，唯一写入是本报告。已读 AGENTS、构图 Boss/worker 词及 IMPLEMENTATION 第三阶段规则。未使用 Git、work.py、native、队列、原证书入口、LP、SPE 求解或 1631 列重播。

## 结论与精确端点

两源共同给出的准确结论，比“私有块最小时 half”稍宽：在下述真实路由和大小域内，令 `p_j=|X_j|`、`p_*=min_j p_j`，则

\[
\boxed{W-\frac{\mathrm{OPT}_6}{2}
\ge \delta N_+-\frac{p_1-p_*}{2}.}
\tag{A}
\]

因此 **若 `p_1-p_*≤2δN_+`，便有 `2W≥OPT_6`**。`p_1=p_*` 是最清晰的特例，此时还得严格余量 `W≥OPT_6/2+δN_+`。这里没有证明私有块缺口条件对该路由/大小域的所有实例成立。

当前原题精确 ID 是 `customer-attraction/six-providers/exact-six-full-history-half-cover`，v1，`truth_status: open`。本次当前 registry 中没有 `Q-CAG-HALF-6` 这个字面键；不可猜造或把它写成新端点。原题的 legacy ID 为 `customer-attraction/six-providers/problem`。

| 作用 | 当前精确 object_id | version / truth_status | 当前 registration pin（`research_runtime.pin(object)`） |
| --- | --- | --- | --- |
| 证书源 A | `customer-attraction/seven-maxima-fixed-route-size-halfspace-rational-cover-certificate` | 1 / proved | `c44c8904f129a2e683da716943182a40587f59d83142a5854349402f60095d0a` |
| 静态目标桥源 B | `customer-attraction/seven-maxima-private-block-objective-and-current-fractional-cover-scope` | 1 / proved | `a3aabc5153fae5241aff5fd2adf4612ce9de5a908a63eb92e494afd94051a4ec` |
| 原六人目标 Q | `customer-attraction/six-providers/exact-six-full-history-half-cover` | 1 / open | `2d5b191271cb052c435121a41935eb3958540d5a53cb05013f13dd45a70f6e31` |

完整当前合同通过 `tools/research_runtime.py` 的 `load(Path.cwd(),verify=False)` 读取为 `data,objects`，逐项读了这三个对象的完整记录，包括模型、statement、quantifiers、assumptions、scope、objections、body、evidence 和 sources。当前 registry SHA 是 `b3b8ca556430e8938ed3918253a0fd559ca8c47aa5be8362c9f1932d1ffa18ec`；下文 canonical 排重只对这一快照负责。

## 三个合同怎样对齐

共同模型是有限单位客户、有限**非空标签目录**及任意覆盖映射，六名单位提供者依固定顺序各选一次，观察完整有序标签历史，终局客户价值均分。完整纯 SPE 保留全部合法离轨历史、空覆盖、同覆盖异标签、重复选择、零客户和任意历史依赖弱平局；偏离后沿同一张原策略真实续行。`W=Σ_i u_i` 是根福利，不把合法背景的剩余利润误当覆盖。

原题 Q 的完整量词为：对每个有限 `(N,S,cov)` 及每份在全部有序历史定义的六人完整纯 SPE `σ`，是否均有 `2W(σ)≥OPT_6`，其中

\[
\mathrm{OPT}_6=\max_{(T_1,\ldots,T_6)\in S^6}
\left|\bigcup_i\operatorname{cov}(T_i)\right|.
\]

源 A 已证的是严格受限合同：全目录恰有七个**不同包含极大覆盖集合**，固定一个合法极大容器归属，实际六位置容器路由为 `ρ=(0,0,0,0,1,0)`，末位动作恰覆盖 `B_0`；比较索引 `K={0,2,3,4,5,6}`（位掩码 125），`O_K=∪_{j≠1}B_j`；若 `|B_6|≥|B_1|`，则

\[
W\ge\frac{|O_K|}{2}+\delta N_+,
\quad
\delta=\frac{18498863000606739639886045305171986828695633123297448847848950678586594650307}
{6762571796424872885022917111161933156201229619283339655506473064817216175091704}>0.
\tag{B}
\]

`N_+=|V|`，`V=∪_{j=0}^6B_j`。这是至少属于一个目录覆盖的客户数；objective 正文以 `U=|V|` 表示同一个量。完全无兴趣客户可在 `N` 中保留，不能把它们加进 `δN_+`。源 A statement 中的 `δU` 应按这个可覆盖总并集理解。

该正证书用 18 条合法基础总行及一个大小行，共十九个正有理乘子；所有 ASR 权均为零。正文完整说明了真实末位 BR、真实偏离两人税、真实前缀最坏后继行、混合路由和子目录席位汇总的合法性。1631 是 route-compatible 的完整客户列域，不是 1631 个游戏/策略样本。已保存摘要、原有理权和压缩残差 SHA 一致；本次读取并核 SHA，没有重算该证书。

源 B 的可复用部分是精确静态公式 `OPT_6=U−min_j p_j`。该对象同时保留旧单私有块目标/原乘子失败的纠错，明确旧负列不构成完整 SPE 反例；并另有当前 `k≤2` 分数覆盖推论。此桥只用正确静态公式，不用那些失败模板，也不把后来的分数覆盖结果倒填旧证书。

## 静态最优公式的完整证明与边界

设去重后的覆盖集合族为 `C={cov(s):s∈S}`。因为 `S` 有限非空，每个 `C∈C` 均包含于 `C` 的某个包含极大元素：若当前不是极大，严格扩张；有限性保证过程终止。题设恰有七个不同极大元素 `B_0,…,B_6`，各有至少一个合法代表标签。

对任意六标签比较元组 `(T_1,…,T_6)`，逐项选一个包含其覆盖的极大容器。其六个容器可能重复，去重后有 `r≤6` 个。将它们补成恰好六个不同极大覆盖：七者中总有足够未选者，补入只会扩大并集。因此任意六标签比较覆盖都不大于某个六极大覆盖的并集。反过来，任意六个不同极大覆盖各取一个合法代表，确是 `S^6` 中的比较元组。由两向比较，

\[
\mathrm{OPT}_6=\max_{0\le j\le6}\left|\bigcup_{k\ne j}B_k\right|.
\tag{C}
\]

定义全局私有块

\[
X_j=B_j\setminus\bigcup_{k\ne j}B_k,
\qquad p_j=|X_j|,
\qquad U=|V|=N_+.
\]

这里“私有”按七个不同极大覆盖定义，不是“只属于一个目录标签”：一个私有客户可同时属于 `B_j` 的多个子主题和别名。对于遗漏 `j` 的六极大并集，恰丢失 `X_j`：客户在 `V` 中却不在其余六集合，当且仅当它属于 `B_j` 而不属其余任何 `B_k`。于是

\[
\left|\bigcup_{k\ne j}B_k\right|=U-p_j,
\qquad
\boxed{\mathrm{OPT}_6=U-\min_jp_j.}
\tag{D}
\]

所有边界均保留：

* 任意子主题只在**静态比较元组**中扩张到容器；没有删去任何游戏动作，没有声称原策略在缩目录后仍是 SPE。
* 别名不增加不同极大集合数；每个极大集合仍有合法标签代表，故反向可实现比较成立。历史中的别名不合并。
* 重复标签或重复容器去重后补足即可；不要求六个原比较标签不同。
* 空覆盖标签仍有容器，因为空集包含于每个极大集合。它对并集和收益为零，不阻断比较证明。
* **空标签目录不在当前模型内**。不能把有限非空 `S` 改成允许 `S=∅`，否则 `S^6` 上最大值无默认定义。
* `N=∅` 或全目录零覆盖时，非空 `S` 的去重覆盖族只有 `{∅}`，不可能恰有七个不同极大覆盖；七极大分支在这些边界为空。一般原题仍直接有 `W=OPT_6=0`，不用 `0/0`。
* 完全无兴趣客户在 `V` 外，既不进入 `OPT_6`、`p_j` 也不进入 `N_+`。因此不能把公式写成 `|N|−min p_j`，除非另有 `N=V`。

## 路由身份与未用标签重标的证明

实际最后一位行动覆盖必须是一个极大覆盖：若其覆盖 `A` 严格包含于合法 `B`，在最后一位真实前缀负载 `b_x` 下，换到 `B` 保留 `A` 上全部原收益，并严格增加 `Σ_{x∈B\A}1/(b_x+1)>0`，违背最后一位 BR。因此可将实际末位覆盖标为 `B_0`；这不推出 `|B_0|` 全局最大。

源 A 还要求真实动作在一个固定容器归属下满足路由 `000010`：前四位置实际动作覆盖包含于 `B_0`，第五包含于 `B_1`，最后恰为 `B_0`。此固定容器标号在客户之间一致；同容器不表示动作标签相同。只有最后一位的极大性是自动的，`000010` 本身仍是严格输入子域条件。

若

\[
\max_{j\in\{2,3,4,5,6\}}|B_j|\ge |B_1|,
\tag{E}
\]

取一个达标 `j_*`，用一个固定排列 `π` 交换未用极大索引 `j_*` 与 `6`，同时保持 `π(0)=0`、`π(1)=1`。将整个极大索引、容器映射和全部客户会员索引统一重标，不改任何原目录动作或原策略。则：

1. `ρ` 只取 0 和 1，因而仍为 `000010`。
2. `K={0,2,3,4,5,6}` 是“除 1 外全部索引”，排列使 `π(K)=K`，故 `O_K` 完全不变。
3. `B_1` 及其私有块身份不变；其余 `p_j` 被置换，`min_j p_j` 不变。
4. 新 `B_6` 是原达标集合，故满足源 A 的 `|B_6|≥|B_1|`。该源对任何固定合法标号都可用；虽然原具体乘子特别对待 6，把对应排列后的证书应用到新标号就够，不必要求原十九权在旧标号逐项不变。

故可把证书的大小条件准确扩写为 (E)，无需新扫描。不能交换 0 或 1 来强迫大小/私有块条件，否则可能同时改掉实际末位、第五路由或被遗漏的比较集合。

## 两源 ALL 合成的完整推导

在同一实际实例、同一完整 `σ`、同一合法极大标号及容器路由下，源 B 给

\[
|O_K|=U-p_1,
\quad \mathrm{OPT}_6=U-p_*,
\quad |O_K|=\mathrm{OPT}_6-(p_1-p_*).
\]

若大小条件 (E) 成立，先只置换未用索引将其实现为 `|B_6|≥|B_1|`，再由源 A：

\[
\begin{aligned}
W-\frac{\mathrm{OPT}_6}{2}
&=\left(W-\frac{|O_K|}{2}\right)
 -\frac{\mathrm{OPT}_6-|O_K|}{2}\\
&\ge\delta N_+-\frac{p_1-p_*}{2}.
\end{aligned}
\]

这证明 (A)，没有缺步。追加**已给输入条件** `p_1-p_*≤2δN_+` 时，右边非负，故得到原题在这个严格子域上的 half。若 `p_1=p_*`，同一式给严格余量。若只知道 `p_1` 是最小私有块而不知道大小条件，当前证书仍不能应用。若只知道大小条件而不知道缺口界，也只能保留有符号下界 (A)。

两源作用不可拆：证书源 A 支付固定比较并集的下界；目标桥源 B 支付 `OPT_6` 与固定比较之间的**确切差额**。不能把源 A 单独称作原题全域 half，也不能把静态等式单独称作福利保证。

## 大小条件不推出最小私有块：纯集合反例

取九个单位客户 `N={a_0,…,a_6,p,q}`，目录恰给下列七个覆盖：

\[
B_0=\{a_0,q\},\quad
B_1=\{a_1,p\},\quad
B_j=\{a_j\}\ (2\le j\le5),\quad
B_6=\{a_6,q\}.
\]

每个 `a_j` 只在 `B_j`，所以任意两个不同 `B_j,B_k` 均有 `a_j∈B_j\B_k` 与 `a_k∈B_k\B_j`；七者两两不包含，恰为七个不同极大覆盖。此时

\[
|B_6|=|B_1|=2,
\qquad p_1=2,
\qquad p_j=1\ (j\ne1).
\]

故大小条件成立而 `p_1>min p_j`。并且 `U=9`、`|O_K|=7`、`OPT_6=8`，直接展示把 `O_K` 认作最优的错误。此例只反驳**集合论蕴含** `|B_6|≥|B_1|⇒p_1=min p_j`。没有指定或审计任何完整 `σ`，没有证明它同时具有实际 SPE 路由 `000010`，没有声称它是 half 或证书反例。

## 推荐的 3D 关系口径与仍欠域

若 Boss 后续选择立边，推荐 `{A,B}⇒Q` 一条 ALL 的 `accepted / unconditional / contribution` 关系；本报告不写 edge。数学推导在所述输入子域上已完整成立，route、大小与 private 缺口是受限实例的域条件，不是声称普遍成立而尚欠证明的前提。`conditions` 应完整保模型、恰七不同极大、固定实际路由、未用五标签大小条件；`contribution.result` 宜先写无需额外 private 假设的定量式 (A)，再写 `p_1-p_*≤2δN_+` 的 half 推论和最小 private 的严格特例。

不能填 `whole_result` 为原题全称结论。`contribution.remaining` 至少明确：

* 这个桥没有覆盖其他实际容器路由；仅实际末位极大不能自动推出 `000010`。
* 在此路由中，`|B_1|>max_{2≤j≤6}|B_j|` 的互补大小域未由当前非负大小行处理。
* 在 route/size 域内，`p_1-p_*>2δN_+` 时 (A) 可能只给负右端；此桥没有付 half。不能把缺口充分条件宣称普遍成立，也不能把剩余域称作反例域。
* 原题允许任意数量的不同极大覆盖；恰七个不是已证的一般目录归约。子主题和别名保留不等于任意目录可压成七极大。
* 本次不解决完整原题的任意目录、任意六人完整 SPE 的全部量词；Q 继续 open。上述未付仅是**此桥的覆盖缺口**，不声称其他现有路线均不能处理其中实例。

`p_1=min p_j` 不必设为唯一推荐域；更宽缺口条件确由两前提和既有 δ 直接支付。缺口条件等号边界只保证 half；严格不等号或 `p_1=p_*`（非空七极大实例 `N_+>0`）才由该式得到严格 half 余量。

## 当前 canonical 排重：仅 registry.edge_files

只遍历当前 `registry.edge_files` 的 2285 个条目，解析其 JSON 后按三个精确端点的 `source_ids/target_ids` 定向筛选；没有扫描旧历史边目录，也没有把未入当前清单的文件视为 canonical。命中共 9 条：证书源 A 命中 **0**；目标桥源 B 命中 **1**；Q 命中 **8**。不存在以这两个源共同指向 Q 的现行 canonical ALL，故在此快照下该精确组合不是重复交付。

| 当前命中 edge_id | 命中端点 / 实际作用 | 文件与 SHA256 |
| --- | --- | --- |
| `boss6-six-half-fixed-policy-cut-and-rank-sparse-forest-certificate` | Q；固定策略对偶/森林稀疏证书规格的局部贡献 | `map/edges/boss6-cone-metadata-repair-7f00141aa48c078d/boss6-six-half-fixed-policy-cut-and-rank-sparse-forest-certificate.json`；`ffd9c856df6905de129f3e79347580cde5ac4a43f82cf645ada18ea311755566` |
| `boss6-six-half-fixed-policy-lossless-scc-certificate-criterion` | Q；固定策略 SCC 商证书无损转换的局部贡献 | `map/edges/boss6-cone-metadata-repair-7f00141aa48c078d/boss6-six-half-fixed-policy-lossless-scc-certificate-criterion.json`；`6b71d4de22eec85bd5b9483cf85727bacc660369af1649c6836cac12be7f61c2` |
| `boss6-six-universal-fixed-query-cone-security-and-static-price11-imply-half` | Q；开放 C6 安全证书充分路线 | `map/edges/boss6-six-security-bridge-3b-37e2f44d17517898/universal-fixed-query-security-to-six-half.json`；`3d26fb6b6167a692827a5b5a881ccc3c079474fc73d6db5000dc90074799d4d4` |
| `boss6-six-weak-total-security-debt-and-static-price11-imply-half` | Q；开放弱总安全债务充分路线 | `map/edges/boss6-six-security-bridge-3b-37e2f44d17517898/weak-total-debt-to-six-half.json`；`176c456b30458166480360b6e1483b9652411efdbacf4846ec9f224d7054a996` |
| `ca-net-credit-minimum-row-to-six-half` | Q；MIN-ROW 条件路线 | `map/edges/customer-attraction-3a-3a-94b7d37e9ed5bb28/minimum-row-to-six-half.json`；`0cc81b3658cba0212a067e56131f59387c7d81d4db7194782423f774a7193452` |
| `ca-net-credit-real-matching-to-six-half` | Q；真实净差匹配条件路线 | `map/edges/customer-attraction-3a-3a-94b7d37e9ed5bb28/real-matching-to-six-half.json`；`12a0254551eb2c36f5f1ed866f5a2aa2ff7e2d8910989974640c15e2270113ff` |
| `ca-net-credit-shared-payment-to-six-half` | Q；共同 saddle 的 PAY-HALF 条件路线 | `map/edges/customer-attraction-3a-3a-94b7d37e9ed5bb28/shared-payment-to-six-half.json`；`f1802770d96aa549ce3c3a879400478df9ef6aa5bfd5556397c81a7e8c9c2982` |
| `cag-a371-fractional-cover-and-correct-opt-pay-two-private-half` | B；另与 `CA-SIX-FRACTIONAL-COVER-ENDPOINT-9-2-v1` 共同支付七极大 `k≤2` 推论到 `M-991f4d4aa574487fa67ab5abf474a739`，不是本次 route/size 桥 | `map/edges/customer-attraction-3a-3a-a371a98e4075b2e6/cover-two-private-half.json`；`37c7aacd8492654f2fa9c04e396f9e0daf9861d63493a137db4c3118da05a2d9` |
| `m397-conditional-six-half` | Q；共享终局多惩罚模板的六人严格子域 | `map/edges/maintenance-scope-cf45f539d61398/m397-conditional-six-half.json`；`03cb034cb9ee2ce0e2fc9e89bb2b2160434b51b35fbe39dfcca67acbb8c58a15` |

这 9 边用于定向排重，仅实读其当前字段及命中关系；没有重审它们各自全部承重证明，亦没有据此做全仓边正确性断言。

## 实读与 SHA 账本

下列路径相对上述 clone 根；SHA 均对本次实际原字节计算。`verify=False` 只免去无关全仓证据校验；本桥承重三正文、模型、证书摘要和原有理权均另全文读，并核对实际 SHA 与当前合同。压缩残差只核绑定字节，未解压遍历或重建计算。

| 路径 | 读取范围 | SHA256 |
| --- | --- | --- |
| `AGENTS.md` | 全文 | `20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9` |
| `prompts/03-map.md` | 全文 | `5e4d0e44f5831506e989b78f81b967a9ed91385e067604c79eb0b8a98bdc24dd` |
| `prompts/03-map-worker.md` | 全文 | `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2` |
| `research/IMPLEMENTATION.md` | 第三阶段、定向替代完整规则；其余接口背景读 | `fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b` |
| `tools/research_runtime.py` | `load` 完整实现、pin/reference/section 及模块入口有关段；调用只读 load | `414713215bc28a062a2ef0330b150f81298987e893278fe90b44b38c7f4d4023` |
| `research/registry.json` | load 完整解码；三个对象完整合同；精确 ID 定位；edge_files 仅定向筛选 | `b3b8ca556430e8938ed3918253a0fd559ca8c47aa5be8362c9f1932d1ffa18ec` |
| `archives/customer-attraction/state/证明/七极大固定路由的大小半空间有理覆盖证书--证明.md` | 全文 16118 B | `a06141db4845abc6f6fb0599ebfa2847d00a5798894da6f2212dc6fe5fc8e351` |
| `archives/customer-attraction/state/审查/七极大单私有块证书目标与当前覆盖范围--审查.md` | 全文 8014 B，静态公式精读；未把正文引用的旧源冒作本次已读 | `b800495e653a5ade48b3c04d9836a78b19d60da47cb8ad7a4826bab0a25f73b2` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | 全文 4995 B | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 全文 7598 B | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/exact-review/summary.json` | 全文；18 base / 0 ASR / 1 order、δ、输入和残差 SHA | `4d7ae70b3f3758d965f8664e352159b97ff483379ae6c9020337cae39845e736` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/original/b6e38a6404bc19b47b14/exact_branch_audit.json` | 全文 3070 B；route/K/十九权/δ，与摘要一致 | `db1cac116f4161c7f4cebf34fde261613fdca4a699539d6ac4923289cf5db715` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/exact-review/all-1631-residuals.json.gz` | 52003 B 原字节 SHA；未解压和重播 | `e3103e64a25e109556082313f3ac7ac1638b6cf38f6ba12019238c779b1667ad` |

精确摘要的 `input_sha256` 与原 3070 B JSON 实际 SHA 相等；`compressed_residual_sha256` 与压缩残差实际 SHA 相等；摘要与原 JSON 的 `exact_min` 字符串相等。源正文三份及模型的实际 SHA 都与当前对象引用相等。没有运行原两个顶层有副作用的入口，没有调用它们的 `--help` 或 import。
