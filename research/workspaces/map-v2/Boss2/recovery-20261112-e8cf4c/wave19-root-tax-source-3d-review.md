# Boss2 · wave19 root-tax 四对象 source-only 3D 数学复核

结论：本报告负责的四个当前对象均有清楚、有效的数学正文与当前证据绑定，可以清除这四项 **source-only object pending**。这不等于把历史三条 edge 的正式替代集成视为完成。旧三边不能仅重绑旧 SHA 后复活；Boss1 已交付带实质范围修正的三条替代边，应该复用其 done 收据并由 Boss 的后续 assemble 纳入 canonical。在本报告最后观测的 registry 快照中，旧三边和这三条新路径均不在 `registry['edge_files']`，因此此时不能宣称“新 canonical 已集成”。

本报告只读共享 clone `/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`；唯一写入为本报告。没有 Git、claim、接管 primary、队列写、registry/coverage/integration 写，也没有运行成熟 SPE/BI/LP/MILP/IC/旧发现器。保持父身份 Boss2。四对象以外的另两个 pending 对象和第四条 pending edge 由 sibling 范围处理，本报告不清它们，也不据此清整个 archive scope。

## 1. 快照及精确对象身份

最后统一观测时间：`2026-11-12T22:35:32.339588+00:00`。以下均为该次实际文件字节；工作过程中重复检查 registry 未变。没有访问远端实时队列，不以本地 claimed 推断远端存活或归属。下文 `done/Boss1` 是有明确 done request 和内嵌收据的本地已同步任务快照陈述。

| 快照文件 | SHA-256 |
| --- | --- |
| `research/registry.json` | `57f40e76c4bc4ce63f09ea2293a612da61a4f7453a67bff0fec8b23b34ca2271` |
| `map/integration.json` | `f8851173bd017363b18d7a286f0ed8ada3f9e888757556f2c44dccc0e0ec7e3b` |
| `map/coverage.json` | `5b4a2f128f77c7fa46095f20216f8abc9757a6c2766357bc4bd310f6c9af6f05` |

四个 `research show` 的 `binding_status` 均为 `current`，其全部 body/evidence 引用逐文件计算的当前 SHA 均等于 registry 登记值。

| object_id | version / truth_status | 精确 registration_pin |
| --- | --- | --- |
| `CA-ROOT-TAX-NO` | `3 / proved` | `9ccf2e6812603affa30850cacbcb50b716f4ddfbebd1f38ab7243559c859c29a` |
| `M-140da849797c486ba0ad22e4dfbe2631` | `4 / proved` | `f1c7c345dea6c3283c675ba3796aa9f8bcb05650209f85de18ab9faf03b0c143` |
| `M-8a98d8d3ca9a42089dbad81715d6f020` | `3 / proved` | `d9d408ea5b16543fdf7086faae0376ecc5993e30372ba3b2f504f6da3c9f2334` |
| `M-dfcc6e32210c40c3b80ff0808d132d0b` | `2 / refuted` | `af8480b0ae57536ac2f2179ed864741437da4318648d353daa0d6b6979ef4f96` |

当前 integration 原始 pending 实际有六对象、四边。本报告的四对象是其中前四项；另外两个为 `customer-attraction/optimal-completion-private-block-ledger`、`optimal-comparison-pool-net-exchange-and-random-retention-identity`。第四边为 `retained-comparison-pool-controls-static-private-block-loss`。不能把父任务简称“四对象”误报成 integration 当时只含四对象。

## 2. 本次实际读取与证据边界

先全文读 `AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`；从当前 registry 完整读取四对象的全部合同字段、body/evidence/source 引用，再以 `research show` 核 registration_pin 和当前绑定。

以下正文是本次全文新读，包含所有标题、数学式、表和来源/执行边界段落；共用文件只读一次并按各对象作用复用：

| 文件（均在 clone 内） | 实际读取范围 | SHA-256 |
| --- | --- | --- |
| `archives/customer-attraction/state/反例/四人实际根总税--反例.md` | 全文 1–174 行，含 21 背景对×6 行动表、完整 SPE 手证、实际叶、正确末位税式、静态安全证书及边界 | `2efa02ba1a7186cf23fcc29e0f70f6cbeb36ce5db6614960091b3233e5b5aab4` |
| `archives/customer-attraction/state/程序/比较池私有块与平方旧负载信用的原诊断--程序.md` | 全文 1–181 行，含完整模型、固定证书身份、FLOOR/POWER2 定义、原报告每字段及程序责任边界 | `6a56e68dca66a3bf88797412577097bb0a399567b1d3f3afb6284db7c97a5a94` |
| `archives/customer-attraction/state/引理/最优比较池的净交换与随机保留恒等式--引理.md` | 全文 1–84 行；M-dfcc 的精确 body section 为“累计付款是目标而非已证不变量” | `400665b8ed3932fb36b7562ced86c182c79852c58d2d2e254ccc87b77c0e0cbe` |
| `archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md` | 全文 1–262 行，特别是末位五类、非末位四类的全部真实续局证明、唯一最优支持和终点/根税边界 | `b42e57e311686c2d737d6ade6642efaa05caa28dded02c9cf035ef0ed9c70072` |
| `archives/customer-attraction/state/计算/四人首步余额完整策略证书--计算.md` | 全文 1–116 行，含两独立实现的责任、全前缀 F/B/δ、字面策略与一般族的分工 | `60616835c921d4c336019b9f5e107980ac35db330d9c78c3244057327a0e7a9c` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 全文；有限标签目录、可能同覆盖异标签、全部有序历史、同一 σ 的真实后继、非零背景剩余利润 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/state/定义/固定背景剩余收益与税--定义.md` | 全文；R/F、税 Telescope、三个不同已否桥、正确预算与全终局税的区别 | `c752babf29ecf272b564fe9ff9883c77dcbf6d7fc5e3e501321fab8c5237b4ee` |

最后一项定义的 SHA 按当前字节计算；它不是四对象登记 evidence 中的新附件要求。必要资源只新读 `archives/customer-attraction/state/资源/重复奖励尾目录扩展与前缀收费的原始合同--资源.md` 的唯一 section “61客户原路径的收费可逐式核对”（54–66 行），全文文件 SHA `1647d9285cd6fdc9d1dab6e12b318b38d2318e406b284d9b48be68e2d9153ca2`。该 section 给 ABCD 唯一支持与三个前缀收费值；没有把它的其它旧报告全部重新认证。

实际新读原已付证据如下：

- root-tax 单位客户输入 JSON 全文 97 行，SHA `864eca4cc1d5df2d039704eb444863405298e6fc6746efb18c49035a801a7ce6`。
- `RootTax-summary.raw` 全文 194 行，SHA `c4e005ef63dbfaad8395ff39ae782217aae02800355c113d0b3dd5a1665e9de0`：明确 259 节点、1295 非自身比较、0 盈利偏离、65 非自身弱平局、实际 AAAF、税缺口，以及负控制确被拒绝。
- `local-point-check.json` 全文 691 行、全部 56+21 个保存的静态尾值及全部最大者，SHA `405fada8ac56e35f26b6b8939114aea25550690df1b80ff67e14de36af7f2ab0`。其中 `full_SPE_IC_checks=0`；本次也没有把局部点检查冒充全树 IC 审计。
- `archives/customer-attraction/tools/evidence/four-player-prefix-balance/replay/second.json` 全文，SHA `70842e685bc8509ce044a1b89e2ee1d0187107a87a496c56a50f0782649015cf`：原保存独立重放给 22 客户、259 节点、1554 含自身比较、路径 ABBB、唯一最优叶支持、全部前缀余额；本次没有重新执行验证器。
- `RootTax-all_nodes.raw` 只新读表头与前九条记录；`RootTax-all_deviations.raw` 只新读表头与前九条记录。它们明确根/实际 h=A 的偏离沿同一真实策略后继，不能冻结末位。其余长表按完整正文手证与已保存 summary 继承，未声称逐行新读完全部长证书。

以下是 CA-ROOT-TAX-NO 其余登记 evidence 的当前字节核验；没有为本次 source-only 审查重新完整读或执行这些成熟代码/长表：

| evidence path | SHA-256 | 本次处理 |
| --- | --- | --- |
| `archives/customer-attraction/tools/tax-interfaces/root_tax_original.py` | `6006ae53cf053ef771cf7b2b71fc783fd694058ab2ad775466fe6224a957106d` | SHA/文件长度核对；成熟代码不重跑 |
| `archives/customer-attraction/tools/tax-interfaces/audits/customer_attraction_root_tax_upload_independent.py` | `0696d1f668e5889564905400d8eb150333bb1941371b23e691d941ab1b362aa0` | SHA/文件长度核对；其全树结果按全文 summary 与自足正文证明复用 |
| `archives/customer-attraction/tools/evidence/root-tax-upload-20261030/RootTax-all_nodes.raw` | `d15c42541a45b71d3bd880b79051b6b2ad54c52168b88f0b652c7e9c8572de09` | 新读 1–10 行；其余按成熟证明继承 |
| `archives/customer-attraction/tools/evidence/root-tax-upload-20261030/RootTax-all_deviations.raw` | `c0dfee9ec5d3fe03b51e33ed9b47f6addd015e8246ed9f6b1c47645627d3b7b0` | 新读 1–10 行；其余按成熟证明继承 |
| `archives/customer-attraction/tools/evidence/root-tax-upload-20261030/RootTax-static_safety_56_multisets.raw` | `9c1f49dcbf4857d01ae7fa9146e734002cc4376e69514e3bb3533b77c3f81b59` | SHA 核对；静态安全不是本次三个负点的承重前提 |

本次还全文读取三条新替代 edge、Boss1 的 `8324.../review.md`，以及 c385 的两条付款相关 edge 和 `review.md`；实读其当前 coverage、assets、supersession 各项和任务记录的 owner/state/requests。对旧三 edge 专门读取了条件、解释、contribution/whole_result 和旧 pin，与新文件逐项比较。对其余 13 条 retained 逻辑边只核本次收据的逐字节保留与成熟贡献继承，不冒称逐源全文新证。

## 3. 同一完整 61 客户 SPE 付清什么

共同模型是有限单位客户、共同有限非空**标签**目录、单位提供者依次观察全部有序历史，每人选一次，终局每客在全部覆盖者间均分。一个完整纯 SPE 必须给所有合法有序历史动作，并比较“改当前动作后，沿同一完整 σ 在新历史续走”的真实收益。两个反例目录都在此模型内部；六标签覆盖恰好互异不削弱其作为允许同覆盖异标签大模型反例的合法性。

61 客户的 12 个精确兴趣型和重数是 A12、B8、C4、D8、AE6、AF6、CE3、CF3、AEF6、BEF2、CEF1、DEF2。主题大小 `(30,10,11,10,20,20)`；每型恰含 A/B/C/D 之一。因此 ABCD 两两不交并分割全部 61 客户。只喜欢 A/B/C/D 的客户各有 12/8/4/8，满覆盖四槽必须各选 A/B/C/D 一次；最优支持唯一，最优有序元组可排列。

完整 σ 的前三位在每个历史恒 A，末位按真实最佳回复及固定 `F>E>D>C>B>A` 平局序选。这不是只列 actual AAAF。正文完整的 21 无序背景对×6 行动值给第三位所有有序历史的 A 最优；本固定末位函数只依赖负载与固定优先序，所以这次才可交换背景对次序。第二位的每个偏离之后第三位仍 A，可用 `(P,A)` 对应行；第一位可用 `(A,A)` 行。末位最优由定义保证。这样同一张完整 σ 同时支付早期全部历史的可信性，而不是用“末位 BR”单独替早期 IC。

实际 AAA 后末位收益向量是 `(15/2,10,11,10,11,11)`，按序取 F。A∩F 有 12 人，A\F 有 18 人，F\A 有 8 人，故 actual AAAF 的收益为 `(9,9,9,11)`、W=38。第一位偏离 F 后是 FAAE，收益 9；它不是把 actual F 末位冻结后的同题复制。根六行动弱平局合法，所以这是严格违反量的反例，**不是严格 SPE**。

### 3.1 CA-ROOT-TAX-NO v3：根税加强仍假

税只计前 m−1 个实际槽。前三个 A 给 A 的 30 客户各负载 3，其他人负载 0，故

`τ=30·3/4=45/2`，`OPT−W−τ=61−38−45/2=1/2>0`。

被否的精确全称式是 `OPT_m≤W+τ_0(c_<m)`。它不是非零背景总税式，也不是把末位一并计入的另一税定义。正确末位式仍是 `OPT_m≤m u_m+τ`：每个比较主题的末位查询可行且不超过同一实际末位的 BR 收益；逐客 `1_{d>0}≤d/(b+1)+b/(b+1)`。此例给 `4u4+τ=133/2`，不存在与反例矛盾。

最优 ABCD 的末位查询总和 77/2，BR 松弛 11/2，`4u4−W=6`，差仍 1/2。故失败定位在以 W 无条件替换 `m u_m`。`2W−OPT=15>0`，不反 half。静态安全值 v4=9 的原匹配证书及 `W−4v4=2` 只保本例兼容性。

### 3.2 M-140 v4：同 σ 实际 h=A 的局部私块 floor 仍假

固定真实第二位节点 h=(A)，剩 r=3，当前按同 σ 再 A，真实 tail=(A,F)，u=9。固定不同合法比较主题池 BCD。它们在 A 外且两两不交，删除独有、未被旧前缀或当前 A 救回的 lost 恰 `(10,11,10)`，全部 >9。背景 A 加 BCD 满覆盖 61，故它是给定背景的**并集最优补全池**；不宣称 BCD 是裸 OPT3。

SWAP 还必须扣 current A 在旧前缀/池外的新覆盖退款。本节点 A 早已在前缀，`new=0`，所以三个净损失仍为 10/11/10；固定此池均匀删一个索引的条件一步期望为 `31/3>9`。这是准确的局部 obstruction。此 r=3 比较池不是从根无条件 RET 抽样后所有随机余池的替代；局部条件一步不能独自反驳根全前缀付款。

其存在性量词、同一完整 SPE、合法非零旧负载、所有可删 j 的严格违反均已付清。无需依赖原 1971 项扫描的全局最大性或唯一最大点。

### 3.3 M-8a v3：平方旧负载信用 Bellman 单步仍假

`F_r(b)=max_{合法静态r槽尾Z} Σ_{c_x(Z)>0}c_x(Z)/(b_x+c_x(Z))` 是背景下**未来总利润**。它不等非零背景的裸覆盖，不是完整可信菜单门槛，最大尾无需为 SPE。平方信用 `H_b(Z)=Σ_{c(Z)>0}(b+1)^−2` 则在该 σ 的真实当前动作与真实 tail 上求差。

已保存且本次全部审读的 56 个三槽尾给 `F3(A)=36`，最大者 ABC/ACD；21 个二槽尾给 `F2(2A)=21`，最大者 AC/BC/CD。这里静态最优尾和真实 tail=AF 的身份没有混同。A 外信用抵消，30 名 A 客旧负载 1 且被真尾 A 覆盖，故 `ΔH=30(1/4−1/9)=25/6`。于是

`u+ΔH−F3(A)+F2(2A)=9+25/6−36+21=−11/6<0`。

这完整否定指数精确为 2 的指定局部 Bellman 付款模板。没有指数搜索、没有其它信用的普遍不可能结论，也没有 half 反例。本次只用短 Fraction 复核上述已有标量，不重新生成 77 值，更不重跑原历史扫描。

## 4. M-dfcc v2/refuted：全前缀付款的反例是另一族

RET 对固定最优带槽元组 T1,…,Tm 的**比较索引**随机排列，不是玩家的混合承诺。若每客户在该元组出现 d_x 次，则删除前 i 索引使其全部覆盖被删概率 `p_i(d)=binom(i,d)/binom(m,d)`。含 O 外 actual 新覆盖退款的精确式是

`L_i=Σ_{x∈O\C_i}p_i(d_x)−|C_i\O|`。

该组合恒等式无需 SPE，终点 `L_m=OPT_m−W` 仍已证。被否的原 M-dfcc 是对每个原输入、每份完整 SPE、任意固定最优元组、每个实际 i 的 `L_i≤P_i=Σ_{j≤i}u_j`。不能再把它列 open。

CA-PREFIX-BALANCE-NO 的既有构造对每个整数 n≥4 取 x=n−2，目录 A、B、n 个叶；普通叶有 x 个只由本叶覆盖、1 个 A/叶、x 个 B/叶客户，特殊叶有 x 个私有、x 个 B/叶、n−1 个 A/B/叶客户。全部是不同单位客户。实际路径 `AB^(n−1)`，`u1=n−1/n`、W=n²−2、OPT=2n²−2n−2。

该族完整 σ：根 A；非空非末位全 B 历史选 A，其余选 B；末位真实最佳回复按 B、A、叶序破平局。全文证明把末位穷尽为五类、非末位穷尽为四类；只有在逐枝证明真实后继相同后才归约同背景 BR。Jensen 正分母与 n=4 弱等号均保留；末位 B/特殊叶平局由固定序处理。因此一般 n 的完整 SPE 不依靠有限扫描代替证明。

每叶有 x>0 个只能由本叶覆盖的客户，n 槽最优元组必须含全部 n 叶、各一次。故所有最优元组仅差排列，所有客户 d=1；A⊂O，|A|=2(n−1)，|O\A|=2n(n−2)，退款零。RET 因而给

`L1=|O\A|/n=2(n−2)>n−1/n=P1`，差 `n−4+1/n>0`。

因此连“存在一个最优元组能付清所有前缀”的弱化也被该族排除，不能靠换一个最优初始池修复这条原不变量。n4 的已有 22 客户字面策略证书是 ABBB，u=(15/4,41/12,41/12,41/12)，L1=4>P1=15/4；完整原证据含 259 字面历史、1554 含自身比较。此处只继承原成熟重放，本次未执行验证器。

这与 61 客 AAAF 是两个不同输入、两个不同完整策略，不能把同一个源反例说成同时否根税与全前缀付款：本 n≥4 族的根税余量为 `(n−3)/2+1/(n−1)+1/n>0`。反过来，61 客局部 lost>u 本身并不支付 M-dfcc 的全称否定。

本族 `2W−OPT=2(n−1)>0`；n4 half 余量 6。`L_m≤P_m` 仍恰等 half 的净缺口付款目标，允许早期欠账后期支付的不同非局部机制保持独立开放。原 ALL{RET,M-dfcc}→一般 half 可保一个完整反事实 **accepted/conditional** 充分归约：取 i=m，用 `L_m=OPT−W` 和同一 actual 钱包 `P_m=W` 即得 `2W≥OPT`。其 M-dfcc 普遍前提现已 refuted，所以该条件边不能当一般 half 的可行无条件路线。

## 5. 历史三边与 Boss1 已交付 repair 的确切归属

历史 holder 沿革为：原 `customer-attraction-3a-3a-227c1bd1c11fc2c4`（Boss1/done）→`round18-ca-representation-repair-repair-29b87721a16fc7a3`（Boss1/done）→`boss6-bank-status-repair-repair-5f402448a1964e8e`（Boss6/done）→本次 Boss1 `boss1-wave12-ret-source-repair-8324c735e389d989`（本地任务快照 done）。前两轮 retained 记录只说明当时版本的沿革；当前不能据其旧 pin 复活旧三边。

当前 repair 的精确证据：

- 任务 `research/operations/map-v2/tasks/boss1-wave12-ret-source-repair-8324c735e389d989.json`，SHA `d8f0627fda4310b49368fc667daa425aba2d153c11df214e9dc7a4f80403590f`；`state=done`、`owner=Boss1`；requests 包含 plan `cd72ace8bcca48968e82a71daaac2038`、claim `179522759edf4463b24383b99de50f7a`、done `13d51c4a6e0d4350b95adfef647c6db8`。这是具体 receipt 完成证据，不是以 claimed 猜实时归属。
- 正式收据 `map/receipts/boss1-wave12-ret-source-repair-8324c735e389d989.json`，SHA `bb6b76b922aabf1e36abbccd3c7ef2c806e9b7fa59342f978f23258479ef8a21`。23 项 assets 当前字节全部与收据 SHA 一致。
- 唯一直接 supersedes 是 `boss6-bank-status-repair-repair-5f402448a1964e8e`；旧 20 资产逐项 `17 retained / 3 replaced`。13 条未受影响逻辑边逐字保留，四份 Boss6 辅助资产仅作历史沿革，三条受影响边明确 replacement_paths。原 227/round18 的 supersession 只作 provenance，不列新接管目标。
- 本报告无新 claim 或写入；应直接复用 Boss1 已有交付，不新建竞争 primary。

三条替代 edge 保原稳定 edge_id，换到任务新路径，当前已带 endpoint/evidence/review_digest：

| edge_id | 新路径（前缀均 `map/edges/boss1-wave12-ret-source-repair-8324c735e389d989/`） | 最终 edge SHA-256 | 当前作用 |
| --- | --- | --- | --- |
| `cag-227-private-block-witness-violates-net-swap-step` | `private-block-witness-violates-net-swap-step.json` | `09f2f76f6a5419959ffb43e8d548185ffc99387e85316044373d695e01badb5d` | accepted/unconditional/contribution；M-140→RET，固定 BCD 条件一步净付款障碍 |
| `cag-227-root-tax-controller-restricts-to-private-floor` | `root-tax-controller-restricts-to-private-floor.json` | `0df997a3c418daa370914fb6be121e40d57633b9eb24e497bf751a525963fd1c` | accepted/unconditional/whole_result；CA-ROOT→M-140，同 σ 实际 h=A 的完整私块见证 |
| `cag-227-root-tax-controller-restricts-to-square-credit-failure` | `root-tax-controller-restricts-to-square-credit-failure.json` | `c21ddde4b76948754f60f21d9699056a03ed994862cf8efb4c212772ce772b02` | accepted/unconditional/whole_result；CA-ROOT→M-8a，同 σ 真实 tail 与静态 F 明确分工 |

三新边 endpoint_pins 分别准确使用本报告 §1 的当前四相关 pin；RET 的 pin 为 `bc70276219fc89dec47233d96d34d864924263952d33c2deeaf870b5d3a10a39`。所有 evidence SHA 与当前正文一致。第一边的实质修正尤其必要：旧 remaining 写“累计付款 L_i≤P_i 仍须另证，也可能利用不同初始池”，新 remaining 明确独立 CA-PREFIX 已反驳全前缀、该族最优支持唯一、不能靠换最优池普遍修复，同时保终点/其它跨期信用/旧逐人 D 的独立未付范围。因此绝非只换 hash。

旧三路径和旧 SHA 仅作历史识别：

| 旧文件（前缀 `map/edges/customer-attraction-3a-3a-227c1bd1c11fc2c4/`） | 旧 SHA-256 |
| --- | --- |
| `private-block-witness-violates-net-swap-step.json` | `62b274f5f6d2b61cb535aeb73275be7ec1d44f79b9d1334df0679eb8a03dc647` |
| `root-tax-controller-restricts-to-private-floor.json` | `92ba029bd792ce24a3335af3d3d16158f9f05de577a9ef41384fb39e12a763da` |
| `root-tax-controller-restricts-to-square-credit-failure.json` | `f8450afdcdead5523726266f570162d31c35b456466afe007c3a0e66dc34f9ec` |

M-dfcc 也已有 Boss1 已交付成果可复用：任务 `customer-attraction-3a-3a-c385b158f346250d` 的本地记录 `state=done/owner=Boss1`，任务文件 SHA `f21675c0fc4c3e2557031f750e81900a6b807447069c49c9161d4cf0e6c50509`，done request `13d51c4a6e0d4350b95adfef647c6db8`。其正式收据 SHA `cf1001ef6be2d08b119c14a882dd64db098d00c76d9c6e3ddefa2ccd43f473d1`，7 项资产当前字节全部匹配。

| c385 付款相关 edge | edge SHA-256 | 本次判断 |
| --- | --- | --- |
| `boss1-security2-prefix-family-and-ret-refute-all-prefix-payment`，文件 `prefix-family-and-ret-refute-all-prefix-payment.json` | `e5a13ba3e9f04d297df638dbea84853e8398ef333a9dc81a092ea9b95dc8505a` | ALL{CA-PREFIX,RET} 无条件反驳原 M-dfcc，完整量词和唯一最优支持均正确 |
| `boss1-security2-ret-and-cumulative-payment-conditionally-imply-general-half`，文件 `ret-cumulative-payment-conditionally-implies-half.json` | `0babc8c9b9437bdb25c06682b98412dd091b622ba473709715049df318921c07` | 完整但已被假前提截断的反事实条件归约，准确保留 Q open |

这两文件完整前缀为 `map/edges/customer-attraction-3a-3a-c385b158f346250d/`。当前 endpoints 使用 M-dfcc pin `af8480...`、RET `bc7027...`、CA-PREFIX `4d500022638bb5dcc117edeace66f673af98737256c72c9ebf3217ac49949bb1`；half 条件边使用 Q-CAG-HALF `dccd5277f7b0c1bb4dcac17287010f1d012bb40c6244c51f24808c1519a4b5ea`。本报告不承接其独立 selected-security 主任务。

## 6. 真正 canonical 与 pending 的处置

严格检索的是当前 registry 的 `edge_files`，没有把整个 map 目录或旧任务 edge_paths 当 canonical：

- CA-ROOT 当前 canonical incident 六条为 `cag-052c1a-last-reply-tax-slack-accounts-for-real-root-failure`、`cag-052c1a-root-tax-witness-satisfies-free-column-budget-at-equality`、`cag-227-root-weak-tie-switch-derives-actual-prefix-relay-witness`、`cag-boss4-2fcb-root-tax-transforms-into-fixed-safe-cap-obstruction`、`cag-6306-root-tax-instance-gives-private-root-obstruction`、`ca-r34-root-tax-policy-and-true-menus-give-two-bank-debts`。它们不是本次旧三边的替代路径；其中有 contribution 的继续仅为原局部贡献。
- M-140、M-8a、M-dfcc 在该 registry 快照中均无 canonical incident edge。
- 历史三旧路径已不在 `edge_files`。8324 的三条新路径、c385 的两条付款新路径在该快照也都尚未列入。因此“已 done 且文件存在”“数学已实质修好”“已 canonical 集成”是三件不同事实。

| pending 项目 | 本报告支付的义务 | 可执行处置 |
| --- | --- | --- |
| CA-ROOT v3 | 完整合同、合法同 σ、root-tax 精确 1/2 反例及停止范围已审，全部登记引用 current | 可清 source-only object pending |
| M-140 v4 | 当前 h=A、BCD 背景补全最优、lost/new、全 j 失败与局部量词已审 | 可清 source-only object pending |
| M-8a v3 | 同 σ 真实 tail、静态 F 优化、指数2及 −11/6 已审 | 可清 source-only object pending |
| M-dfcc v2/refuted | RET 原命题和另一完整 SPE 族、唯一最优元组、首步严格反驳、half 独立已审 | 可清 source-only object pending |
| 历史三 edge_id | Boss1 正式新替代成果已实读，当前 pins/SHA/收据/17留3替处置齐全 | 在本报告快照仍保留 edge pending；下一次 assemble 纳入上述精确新路径并验证后，才可清其正式 repair/integration pending；不复活旧路径 |
| 另两对象、第四 edge、archive scope | 不在本包 primary；RET 全文只作必要证据，不冒 sibling 的完整对象/边义务 | 留给已分配 sibling/父 Boss 整合，本报告不清 |

父 Boss 在消息中说明 assemble 暂被另一个本地源勘误发布顺序挡住，正先 checkpoint 源与相关资产，再 done/sync/assemble。该消息解释后续操作顺序；本报告不把未来操作当已发生结果。只要后续 canonical 选择上述 done 成果，现有数学不需重跑成熟完整审计，不需再造反例，不需改变一般或六人 half 的开放状态。

## 7. 本次短标量核对

唯一新增数值核对是一段标准库 Fraction 标量代入：`18/3+12/4=9`、`8+12/4=11`、`30·3/4=45/2`、root 缺口 `1/2`、固定 BCD 删槽均值 `31/3`、`30(1/4−1/9)=25/6`、Bellman slack `−11/6`、n4 RET `L1=4`、`P1=15/4`、差 `1/4`，两个现成实例 half 余量分别 15 和 6。没有枚举新输入、策略或历史；没有重新生成原 77 静态值、1971 floor 检查或原全策略审计。
