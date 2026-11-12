# Boss2：十三人共同查询障碍与 ENT1 的独立 3D 预审

本报告是只读预审，不是主覆盖领取、队列交付或任何任务的 done。仅新写本 scratch 报告；未改仓库正文、登记、超边、coverage、Git 或队列。工作根为 `/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`。以下状态是该 clone 当前文件快照，不替代 Root 随后领取前的轻量远端核对。

核心结论：**M-7e…v2 所携同一份完整具体 witness，加上短的终局分数计算，足以完整推出 M-05…v2；这不等于“抽象 delta 粗预算失败蕴含 ENT1 失败”。** 反向仅从 ENT1 失败及终局统计，本次只能交共同完整 witness/静态端点的局部贡献，不能标作整条 M-7e 的反向 whole_result。真实中继 delta、2002 查询的有限统计及重叠信用仍须其自己的真实后继证据。

## 1. 当前身份、版本及读取控制

使用 `research_runtime.load(root, verify=False)` 的 `(data, objects_dict)`，用 `runtime.pin(record)` 取 pin。没有把 registry 文本 hash 当 object pin。仅 `data['edge_files']` 的 2287 个路径被当作 canonical 清单。

| 记录 | 当前值 |
|---|---|
| registry SHA256 | `020a2927997479967535eeeaa5e22ec3ad3f136534a302809de218ba920a5a50` |
| M-7e204ccd7c6e4b7c8cbd5ddec64f5716 | v2；proved counterexample；“十三人完整SPE否定同一查询的统一有符号delta粗预算” |
| M-7e object pin | `44af07af51f1f14492a6e65ed69729763a72dc5cdcfd75aec7be0135937d194d` |
| M-05b51399a0114768921338b101578273 | v2；proved counterexample；“十三人完整SPE否定未缩放单查询插入端点ENT1” |
| M-05 object pin | `168d3c72291a54640e4bb0d3779b0fb0efba031884ad88923c1d1957f8f7a1ae` |

已先完整阅读 `AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`，其当前 SHA256 分别为：

- `20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`
- `fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`
- `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2`

两对象的完整记录均已读，包括 model、statement、quantifiers、assumptions、scope、objections、全部 body/evidence refs 与 sources。共同域是有限不同单位客户、共同带标签目录、单位提供者、完整有序历史纯 SPE；偏离沿同一原策略在改变后的历史真实完成。允许重复行动和弱平局，不把计数自动机误称为 count-only 策略，也不把 27243 个压缩节点误称全展开历史数。

## 2. 实读正文与必要证据清单

下表路径均相对工作根；所有列出的引用 SHA 已逐字节核对。标“全文”是本轮实际读全文；gzip 只按明确范围读取，没有冒称逐节点重读或新 IC 审计。

| 文件 | 实际阅读范围 | SHA256 |
|---|---|---|
| `archives/customer-attraction/state/障碍/R-171有符号delta选择与重叠信用边界--障碍.md` | 全文（M-7e body） | `7a85659ade80875c9e9889074d5ecec1b8565eb2088ba5cef3aa2d24e2d7b3a9` |
| `archives/customer-attraction/state/障碍/R-171有符号delta选择性预算独立复核--障碍.md` | 全文 | `7f2ff187a395c6a7380672aacd8aaa3fa0602d916be555b16de2757dbb4531e5` |
| `archives/customer-attraction/state/障碍/R-171固定包络价格13节点有符号delta有限审计--障碍.md` | 全文，包含登记指定三个 section | `431f661e12248a5c5b8b2f7e003b8c3cc9cc907d47745c7e5c9f13b7effea445` |
| `archives/customer-attraction/state/审查/实际终局插入预算与未缩放税桥的同一性--审查.md` | 全文（M-05 body） | `a57391ef0955e4fac8a7b49ebde98deadbc7c7a668f804ca2b0090562d30fd9f` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 全文 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/state/定义/固定背景剩余收益与税--定义.md` | 全文 | `c752babf29ecf272b564fe9ff9883c77dcbf6d7fc5e3e501321fab8c5237b4ee` |
| `archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md` | 全文，包含完整 13 人证书资格说明及 alpha1 算术 | `32a7f769383211709c67373e85118ceb541b5e4d58d2bb3d826272ac3e332b1f` |
| `archives/customer-attraction/state/审查/十三人静态宽限与最优组合平均的原独立审计--审查.md` | 全文 | `4567cc3cb8a8179f8fe1b2283bf9ef2d78e5aa20422926ef992d171a4cf8c22b` |
| `archives/customer-attraction/state/资料/最优排列调和债与归属端点薄化的边界--资料.md` | 全文；重点登记 section“逐行加强和旧十三人例的有限含义” | `867e798a53abb4755270a3c71ec3dc67993158a2e2349b2e60592e41369dc6c4` |
| `archives/customer-attraction/state/程序/实际末菜单的十三人精确点与两种固定锥原探针--程序.md` | 登记 section“十三人旧税见证的静态鞍点与完整报告”完整读取；不声称其余程序正文全部实读 | `65a9369f3c2931c9765869edf04d89169922c3b93779618602aea72356dc8d4b` |
| `archives/customer-attraction/state/审查/R-f6插入信用与纯遗漏底薪候选的准确状态--审查.md` | 全文 | `6b7dbbbdf5ea25764b33c47e67f2469cb66d96058b05b2e0b80174f9a695d2d7` |
| `archives/customer-attraction/state/想法/最优覆盖查询的自留份额预算--想法.md` | 全文 | `136032aeef1bd264a76783f6c3c98152095d4efad8536d43eb1a4a6f33a1e228` |
| `archives/customer-attraction/state/资源/真实child价差的旧反例与最优查询量词--资源.md` | 全文 | `049a65d265733346acccf580bd9e49ed115767d2fc7ebc770e33553add2ef3c2` |
| `archives/customer-attraction/tools/evidence/R-171-price13-20261031/original/probe_signed_delta.py` | 全文；没有 import 或执行入口 | `53c14148d65c4e7f35c44b77bdf6b9f6204f49507bf96c842a07f9a50e336252` |
| `archives/customer-attraction/tools/evidence/R-171-price13-20261031/replay/signed_delta_report.json` | 全文；全部 12 行菜单、6×6 总矩阵和汇总字段 | `46e73447954de7f97a7f72a61fb24f12388dee54a0cffddb2d7f8b8716b47756` |
| `archives/customer-attraction/tools/evidence/R-171-price13-20261031/replay/packet13_all_nodes_audit.json.gz` | 结构、source/SHA、节点/比较总数与一条示例记录；未重读 18675 条比较记录 | `413b08a0ff864c409ce08932a4172bc259ff3ba9d0d1e3d27653ae194aeb87b5` |
| `archives/customer-attraction/tools/evidence/R-171-price13-20261031/original/refined_tax_k10_packet.json.gz` | 顶层结构、完整 instance、root/样例节点；实际链 14 个节点逐步读取 | `bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce` |
| `archives/customer-attraction/tools/evidence/static-allowance-original-notes-and-independent-review-primary/source-root/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz` | 相同 372216B packet 的当前字节/SHA核对；不重复读取另一份全图 | `bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce` |
| `archives/customer-attraction/tools/evidence/static-allowance-original-notes-and-independent-review-primary/source-root/research/workspaces/customer-attraction/R-a40925880381414dbaba3a8314be5f93/restore_attack/static_allowance_audit.json` | 1706B 冻结报告全部字段 | `74cab9d8340c121a56392a47303abd77c7aeff15504a0030d812a36d9cd5e55f` |

成熟完整资格复用为：每个决策节点六条观察行动边封闭，沿边计数严格加一、深度递增；全图可达、叶深度 13；沿指定行动逆序求真实终局，全部 18675×6=112050 项含自身收益比较通过。边封闭使每个有序历史唯一映射到图节点，等计数可落不同节点，所以完整有序历史量词已支付。此处是复用成熟证据的逻辑解释，不是新跑 112050 次。

本次新增的执行只有读取、hash、实际 14 节点绑定和短 Fraction 运算。未跑原脚本、成熟全 IC、2002 枚举、优化器或大证书。

## 3. 同一 witness 的短证明：M-7e 完整推出 M-05

把 M-7e 的完整具体 witness 记作 `(I, sigma)`。其客户类型及在 actual 上的负载如下。人数均表示不同单位客户，非加权玩家。

| 兴趣类型 | 客户数 | actual 客户负载 |
|---|---:|---:|
| A | 2 | 2 |
| B | 2 | 1 |
| T | 1 | 0 |
| TD | 1 | 0 |
| TE | 1 | 0 |
| ADE | 3 | 2 |
| BDE | 1 | 1 |
| P | 25 | 10 |

本轮从 root 沿真实指定边读到节点链 `0,27228,…,27239,11013`，动作恰 `P^10,A,A,B`，叶计数为 `(2,1,0,0,0,10)`，未以 `expected_path` 当证明。由各类型直接算：5 客户负载 2、3 客户负载 1、25 客户负载 10、3 客户未覆盖；W=33。P 玩家每人得25/10=5/2，A 玩家每人得5/2，末位 B 得3。A、B、T、P 的并集盖满36客户，所以 OPT13=36。所给完整 sigma 的资格由上一节成熟证据承担。

定义本次目标的**未缩放**终局价格

\[
g(S)=\sum_{x\in S}\frac1{1+c_x},\qquad
R_0=\sum_{c_x>0}\frac1{1+c_x},\qquad M_1=\max_Sg(S).
\]

逐类型直接得到

\[
g(A)=\frac{2+3}{3}=\frac53,
\quad g(B)=\frac{2+1}{2}=\frac32,
\quad g(T)=1+1+1=3,
\]
\[
g(D)=g(E)=1+\frac33+\frac12=\frac52,
\quad g(P)=\frac{25}{11}.
\]

所以 M1=3，且

\[
R_0=\frac53+\frac32+\frac{25}{11}=\frac{359}{66},
\qquad 13M_1-W-R_0=39-33-\frac{359}{66}=\frac{37}{66}>0.
\]

这已经是一份完整合法 SPE 对全称 ENT1 的完整反例，不需要任何 delta 结论、2002 查询枚举或新的 IC 审计。M-7e 在此方向的数学作用是**给一份已认证完整具体 witness 及其实际叶**。不能把这条边的解释压成“delta>预算，所以 ENT1 假”；该抽象推理没有给出两个预算之间的普遍蕴含。

目标中的 SAIC 别名也全部支付：记

\[
B=\sum_x\frac{c_x}{1+c_x}
=W-R_0=\frac{1819}{66}.
\]

逐式有

\[
m\max_TJ_T+B\le2W
\iff m\max_TJ_T\le W+R_0,
\qquad J_T=g(T).
\]

所以 SAIC 和 ENT1 在此定义下是同一陈述，失败量也是同一个37/66；它们不是两份独立付款证据。任意比较负载d仍满足 `1_(d>0) <= (d+c)/(1+c)`，故 `OPT <= mM1+B` 的静态充分逻辑成立；反例只否充分桥，不否静态代数。

若正式主包采用本比较，可用单 source 的 `implies`、`relation_mode: unconditional`，whole_result 准确写为：“从 M-7e 所给同一完整13人/36客户/六标签 SPE 及其实际叶，未缩放插入向量与R0如目标，M1=3、13M1−W−R0=37/66>0，且B=W−R0使SAIC与ENT1逐式同一，因此完整得到M-05整条反例陈述。”无需 ALL 加入另一个新数学前提；模型、证书、实际叶与算术定义要在 conditions/roles/evidence 中明确。此是成熟 witness 的新比较连接，不声称新反例发现。

## 4. 两类失败的精确否定对象和量词

M-7e 使用同一 sigma 在 actual 第i前缀强制查询后得到的真实中继和末回复。原脚本中 `diagonal[a]` 是该强制分支的当前玩家真实收益；`matrix[a][q]` 是在 actual 删除当前与末位背景上、以 q 分支的真实末回复作额外挡位的查询值减 `diagonal[a]`。同一个分布 mu 在两指标独立抽样：delta_i(mu)=mu^T M_i mu。此 delta 不是终局 fresh 价格 g，也不是 H4 的 `Delta_i(T)=g(T)-d_i(T)`。

冻结报告的前十行 TT 元素1/2、后两行0，故同一个 mu=delta_T 下总 delta=5，粗预算 `(W+w)/(2m)=18/13`，差47/13。总矩阵全部条目<=5且 BB/TT=5，故 `mu^T M mu<=5` 对任意概率向量成立，点质量达到5。本轮仅从36格总矩阵算了 uniform、T及两个已报告极值查询，分别得7/132、5、1373/507、−38375/5577，核其短算术；未重跑2002查询。

最优13槽计数必须且只须含 A/B/T/P 各一次，余九槽在六标签分配；因此计数总数解析为 C(14,5)=2002。冻结报告给其中368坏、最大点(1,1,1,9,0,1)、最小点(10,1,1,0,0,1)。这否定：

1. 对**每份**完整 SPE、**每个**共同查询 mu 都有该粗总delta付款；
2. 对**每份**完整 SPE、**每个**覆盖最优13槽计数所诱导的共同查询 mu=n/13 都有该粗付款。

它没有否定“对每份完整 SPE，**存在**一个好共同最优查询”，因为同一个例子已经存在好查询；更没有否定保留全部真实 slack/重叠余项后的选择性接口。

M-05 则否定 `∀I ∀完整sigma: m max_T g(T)<=W+R0`，等价于每个单query都支付的全称加强。其精确否定是 `∃I ∃完整sigma ∃T`，本例T足够。**不是说本例六个query每个都违反**；也不是每个最优元组失败。T重复13次只盖3客户，根本不达到OPT36。

同一个例子对存在最优查询的静态版本明确通过：强制 A/B/T/P 四主题价和

\[
P^*=\frac53+\frac32+3+\frac{25}{11}=\frac{557}{66}.
\]

补齐九槽以全目录最便宜的 B、价3/2重复，得到固定13槽最小费用

\[
K_0=\frac{557}{66}+\frac{27}{2}=\frac{724}{33},
\quad W+R_0=\frac{2537}{66},
\quad W+R_0-K_0=\frac{33}{2}>0.
\]

所以 `P*`、固定m槽 min-fresh K0、真实 H4存在元组/排列，与两种全称失败各保自己的量词。两对象均有half余量2W−OPT=30；m13也不判定m6限制域。

反向审查：M-05提供同一个完整witness、客户表、actual、W/OPT/利润与未缩放端点失败，是M-7e的一部分基础。但仅此静态端点或“ENT1为假”的抽象结论没有计算真实中继后继，不给TT十行1/2、两行0，更不给2002族的368/极值。因此本次不建议写M-05⇒M-7e的whole_result或equivalent_to。若保反向逻辑贡献，其 result 应仅列共同witness资格与actual数据，remaining 明列12个真实菜单/总矩阵、有限最优查询统计、全部slack和重叠账；可复用M-7e已存在冻结报告支付这些义务，不应把复用目标自己的报告包装成ENT1失败的独立推导。若这种基础贡献没有新的研究用途，保在comparison说明而不另添反向边更简洁。这是本次作用范围判断，不是宣称不存在任何把完整指定自动机重新计算成全部delta数据的算法。

## 5. 原程序归一、两处源勘误与最小替换文本

原 `probe_signed_delta.py` 最后明确是：

```python
adjusted_total_delta = worst[0] - credits/m
adjusted_excess = worst[0] - credits/m - budget
overlap_adjusted_excess = worst[0] - (credits+overlap_credit)/m - budget
```

`credit_current=5/11`、`credit_last_menu=40/13`、`credit_last_player=68/33` 合计 `credits=2399/429`；该累计值整体除m=13。`overlap_credit=441/2` 也为累计、未除13的字段。于是

\[
\frac{1373}{507}-\frac{2399/429}{13}=\frac{12704}{5577},
\quad \frac{12704}{5577}-\frac{18}{13}=\frac{4982}{5577},
\]
\[
\frac{441/2}{13}=\frac{441}{26},
\qquad \frac{4982}{5577}-\frac{441}{26}=-\frac{179225}{11154}.
\]

所以 **12704/5577 应保为原字段的 adjusted_total_delta，不应改称“粗包络值”**。需要补齐的是整组信用统一除13的量纲。原脚本/JSON本身字段相容，不需改科学证据字节。

第一处当前源：`R-171有符号delta选择与重叠信用边界--障碍.md`，当前 SHA `7a85659ade80875c9e9889074d5ecec1b8565eb2088ba5cef3aa2d24e2d7b3a9`。第7行 summary 已正确写441/26及负excess。第26行仍说“再扣…E_i,E_m…441/2的大信用”，没有标明累计/未归一化；它未声称保全部信用后仍为正，但和summary量纲不清。建议只替换第26行整段为：

> 对 2,002 个达到 `OPT` 的重复主题组合逐一取 `mu=n/13`，最大总 delta `1373/507`，超预算 `671/507`；最小值 `-38375/5577`，所以“任意最优组合支付”失败，而“存在有利最优组合”仍开放。该最大查询的原探针累计真实 `S/Z` 相关 `G` 信用为 `2399/429`，在同一总 delta 账本中须除以人数 `m=13`，实际扣项为 `2399/5577`；因此仅扣这些信用后的调整总 delta 为 `12704/5577`，预算超额为 `4982/5577`。原探针新增标量余项 `E_i,E_m` 的累计重叠信用 `441/2` 也尚未除以人数，同一账本实际再扣 `441/26`，得到调整超额 `-179225/11154`。因此该固定重复查询并未否定保全部信用的预算，也不能把删信用后的失败外推到少重复、选择性最优组合。

第二处当前源：`R-171固定包络价格13节点有符号delta有限审计--障碍.md`，当前 SHA `431f661e12248a5c5b8b2f7e003b8c3cc9cc907d47745c7e5c9f13b7effea445`。第31行写“overlap credit441/2也加入后…−179225/11154”，未解释除13；它仍是负excess结论，不是当前正失败，但显式减法量纲不全。建议只替换第31行整段为：

> 脚本按最大经验查询 `(1,1,1,9,0,1)` 计算累计真终局 `G` 信用：当前菜单 `5/11`、末菜单 `40/13`、末位玩家 `68/33`，合计 `2399/429`。原程序将该合计除以人数 `m=13` 后才从总 delta `1373/507` 扣除，实际扣项为 `2399/5577`，所以调整总 delta 为 `12704/5577`、预算超额为 `4982/5577`。字段 `overlap_credit=441/2` 同样是未除人数的累计重叠信用；在同一账本实际再扣 `(441/2)/13=441/26`，该固定查询的调整超额因此变为 `-179225/11154`。这说明重叠信用可能修复这一固定选择，但不能推出所有选择都能统一获救；“从最优计数选择一条共同查询并控制所有独立行余项”的选择性量词仍开放。

这些建议没有改变M-7e v2已更正的 statement/objections、反例结论或量词，只使正文和v2/summary/原程序字段一致。但当前 `tools/research_runtime.py` 的 register 流程要求任何对象 record 改变（包括 body/evidence SHA 更新）都必须增加 version，因此两正文更新并刷新引用时，M-7e 记录必须由 v2 升为 v3，statement/quantifiers 保持不变。这是引用身份记录的版本更新，不是新增数学命题；全文SHA、各引用、pin和未领取任务输入仍必须一致刷新。报告其余 v2 标识保留为本次实际读取的原快照事实。

## 6. 两待勘误路径的全部 registry owner 与任务影响

实际遍历当前 registry 所有 object 的 `body` 及 `evidence`：**只有 M-7e204ccd7c6e4b7c8cbd5ddec64f5716 v2** 命中两路径，命中如下；没有其它对象直接引用这两路径。

| 路径 | 实际 owner/version 与引用 |
|---|---|
| R-171有符号delta选择与重叠信用边界--障碍.md | M-7e…v2 的 body，绑定全文SHA `7a85659…` |
| R-171固定包络价格13节点有符号delta有限审计--障碍.md | M-7e…v2 的 evidence 三条，section分别“输入与 SPE 验证”“有符号 delta 的实测范围”“信用尝试与开放缺口”，三条均绑定全文SHA `431f661e…` |

哪怕只改第二页的信用section，三条section引用都须更新其全文SHA。M-05 v2没有直接引用这两页，不因本次正文勘误自动改pin。材料行/baseline的相应文件绑定亦须随源字节按现行定向规则一致处理；本预审没有执行这些写入。

本地完整筛查 `research/operations/map-v2/tasks/*.json` 的 definition（非误读顶层），并核 owner、核心/只读ID、reading_refs和supersedes：

| 主包 | 当前本地状态 | 与待勘误页关系 |
|---|---|---|
| `customer-attraction-3a-3a-c986a138e6639b6f` | available，owner=null；核心仅M-7e…v2 | 当前pin `44af07…`；reading_refs命中两页共4条；未见done/claimed，未见替代者 |
| `customer-attraction-3a-3a-a5d4516886ba4323` | available，owner=null；核心仅M-05…v2 | 不引用待勘误两页；未见done/claimed，未见替代者 |

因此就两页当前实际owner，没有有效已done/claimed主覆盖包需要本预审替代。Root应先修正文及相应引用/未领取输入，再按最新远端状态领取；本报告不是领取或done证据。c986当前任务文件SHA为 `315719735150192290cfcdc0654156a3cda5e54218dfa6a2d0602c391e40cc51`，可供刷新前对照。

## 7. canonical 已有关系、去重及建议读依赖

仅遍历 `data['edge_files']`：两ID均无当前canonical端点命中；两待勘误路径也无canonical evidence引用命中。不能据此说与十三人例有关的边全部为空：按数学文本检索后，实际完整读到并核对下列有效旧边。

`map/edges/customer-attraction-3a-3a-c0d8496dbc098925/root-stationary-witness-to-unscaled-insertion.json`

- edge_id：`ca-r36-root-stationary-witness-to-unscaled-insertion`
- SHA：`6d86d996fd580245bda754ecafa9223b175d0ae5fbe6ed3ffc6fa516c6dfd690`
- accepted、transfers、unconditional；source为 `cag-unique-root-stationary-weak-cap-counterexample` v2（pin `ced29a172e6109b3da37f8a018b8d4c9f5adb086d571c138bf48c609a92a70b5`），target为 `M-3505416cc1714c84baef9767bd1ca902` v4（pin `889ec3cbe103bc41ca4c477a928062efcbfca9130c32863dfde59ab941ddf80c`）。两当前记录均已完整读；未声称其全部其它正文也于本轮重读。
- 完整结论为同一13人例对全部alpha>=12/13反实际缩放精确税桥，含alpha1的37/66；其解释已经是“完整具体witness→终局静态价格”的相同类型迁移。
- 原c0d8496…包（Boss1 done）已由 `boss6-fr-status-repair-repair-4de57d1ac5095cea`（Boss6 done）替代；后者receipt.supersession将此资产明确 `retained`，资产SHA与当前canonical相同。因此此边仍有效，不能当旧失效边重新写一份。
- 此边没有引用两待勘误页，不能因本次勘误机械刷新它。

这条已有效边不等于M-7e→M-05这对端点已完成，但显示37/66静态反证不是新发现。新主包应复用既有算术和证书，不重复发布根平稳核→M350这条旧关系。若扩展真实比较，M350在alpha=1特化也可完整支持M05，其新端点关系是否值得增加由主包取实际研究用途，勿机械铺满同一witness所有对象对。

本次另外实读 `B5-EARLY-MENU-LOAD-DEFECT-v1` 当前v3完整记录（pin `04ca37efea3ef4943bb3d848795bae169cc1deedfec694460ee3ee68f77ea050`），用于确认原带delta引理保留真实中继及开放付款，不把其已证价格转移当作已反。其正文未于本轮全文重读。建议正式主包的必要只读依赖为共同完整历史模型；若主包要正式比较粗delta与原价格引理，再完整读B5正文/独审，避免只凭脚本名义给错误refutes边。M350及上述canonical边是已存在的替代证明/去重导航。M05的K0/P*/H4边界所需完整证据本轮已按第2节实读。

可交Root的本次成熟数学是第3节的单向whole推导、反向作用范围和第5节两段源勘误。未付的一般数学义务仍为：从任意完整SPE共同选择有利最优查询并同时控制真实slack、重叠、总质量和各行余项；不能由本例好查询、half正余量或SAIC改名代付。
