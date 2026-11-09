# common-many 八包的数学集成比较

内部词：`474257b8-commonmany-integration`。身份 Boss5；本次 fresh 数学比较工作，不是常驻审核。只写本笔记，不操作 Git、队列或 canonical 文件。

## 阅读范围与当前快照

已读 AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md。逐包提取并读了下列八个 task 的核心/共享端点、coverage、closed_overlaps 和全部交付边的语义字段：`commonmany-3a-3a-47c906ea6eb2b3a6`、`6551dba0c3ad3ad4`、`93b668d2f3f4c0bb`、`9455223ce90f49b6`、`c6a55eaaaa6f95dd`、`e41a1f33282daba3`、`f5031745c59be4fa`、`f5c42e38d2d95b66`（后七均同前缀）。比对当前 registry 中相关对象的 statement、assumptions、scope、objections 与 body。最初宽打印发生过截断，随后按任务/字段/必要对象重读；不以那次截断输出声称完整阅读所有 task 的 reading_refs。

全文实读以下正式数学正文：共同目录模型；结构参数推论；规范贪心完整盒与因子二续局；有向深度二整池证明；受限同链双端 Nashification 导入；固定贪心坏选择反例；客户类型支持 ILP/有限目录选择；冻结静止超载补全；原池双装箱/盒外纯 NE；晚开中心星最大键算法。另实读一般构造工作坊的“路线 A：一般盒内均衡的位多项式选择”和“路线 C：偏离者专属安全超载证书”。未重读全部历史证据程序、保存的报告、外部论文 PDF、截断归位引理全部证明或全局字典序存在原正文全篇；后两项已有结果在此按当前登记及现行 canonical 联合边使用，不声称重新证明。

八份收据的 17 个 asset 引用逐个比 SHA，均与当前文件字节一致。读取时八 task 均为 done，尚未列入当时 map/integration.json 的 task_receipt_pins；17 个 asset 只有 655 包复用的全局字典序 ALL 边已在 registry.edge_files，其余 16 条尚未 canonical。根后续 assemble 已推进，因此这段仅记录本次读取时的快照，不覆盖根的新状态。没有遇到需立即报错的数学源错误。部分 receipt.review_note 保留“本地候选/尚未 done”等旧阶段描述，与 task 当前 done 不同；这是历史审读文字，不据此否定已交付，也不把它当数学状态。

## 可以直接接入的承重链

1. **全局字典序存在路线。** 655 包正确复用 `commonmany-global-lex-budgets-and-finite-repair-imply-factor-two`，路径 `map/edges/commonmany-3a-3a-7fbed9462b1600ef/global-lex-budgets-and-finite-repair-to-factor-two.json`。全部共同前提为 `SC-K-LEX-BUDGET`、`MF-PACK-2`、`MF-PURE-CAP`、`MF-CONT-COMPLETE`，共同推出 `SC-K-2-E`。在轨全布局全局 lexmax、源存续/消失四预算、纯帽修复、实际标签拼接各有工作，不能拆成任一项单独足够。源消失还须保原源客户交集项。此边只付完整存在，不付全局 lexmax 的一般高效搜索或默认查询的位时间。

2. **旧浅层结构构造。** e41 的 `commonmany-incidence-dp-depth-two-to-complete-two` 保留 ALL：`SC-K-INCIDENCE-BOX-DP` + `SC-K-HEIGHT-TWO-BOX-EXISTS` + `SC-K-GREEDY-BOX-TO-2` + `facility-games/common-many/restricted-identical-link-range-preserving-nashification-import` ⇒ `SC-K-HEIGHT-TWO-INCIDENCE-2`。深度二支付同一指定冻结域的存在，A-DP 支付选择时间，BOX-TO-2 支付原池/当前池与标签兼容，MAX 支付离轨及默认查询时间。没有把有限势下降的次数写成多项式。47 的新结构推论→旧浅层推论只是同域限制，不删旧 ID 的“两选项、开站深度≤2、关联树宽与双侧度固定”条件。

3. **轻分量支持 IP。** 93 的 `commonmany-type-support-and-greedy-existence-imply-frozen-light-fpt` 正确保留 ALL(`SC-K-BOX-NE-FPT-TYPES`,`SC-K-GREEDY-BOX-EXISTS`) ⇒ `SC-K-FROZEN-LIGHT-FPT`。一般盒存在保留的恰是这里冻结的重客户/单选客户，所以各分量 IP 必可行；冻结重客户即使有跨分量备选，也由 `(W_s-w_i)/q_s≤γ≤W_t/q_t` 稳定。完整原动作未丢。任意预设占用 NP 完全对象 `M-57da53da3efa46998555bccf77c69d35` 不保真实规范贪心承诺，不能反驳这条必成功路线。全目录/全权种的 `SC-K-CATALOG-WEIGHT-XP-2` 是另一条全局 lexmax 搜索实现；`(k+1)^(p-1)p!p f(p,d)poly(L)` 只给 XP(p,d)，不由轻分量 FPT 得到 FPT(p,d)。

4. **原池删除箱与双 LPT。** 945 的两条 ALL 边各自完整。固定 γ 接口接受任意显式有理独立 mixed 在轨精确 NE、逐家 `a_f≥γ` 与全部多设施源的原池 `q_u-1` 删除箱；不是只给上盒或只给某一项偏离。双 LPT 首轮用 RANGE 保最小设施收益，第二轮提供原池删席证书；MAX 单独不能代替首轮 RANGE。三角例选定 NE 的 M 总重 430>400，故不能直接作为 BOX-TO-2 输入；这不反驳另一个盒 NE 存在。两接口在当前池/原池、站均匀/任意 mixed、完整上盒/删席证书上各有不同，不能互推。现行 canonical 的 AR/AD 条件边保留更宽自适应阈值路线；本包是固定 γ 充分域。

5. **给定种子的冻结完成。** f503 的三个联合关系准确区分：`MF-PURE-CAP`+MAX ⇒ `MF-PURE-CAP-POLY`；`SC-K-FORCED-FLOOR`+MAX ⇒ `MF-FROZEN-OVERLOAD-POLY`；`MF-FROZEN-OVERLOAD-POLY`+MAX ⇒ `SC-K-FROZEN-OVERLOAD-2`。残余按真实普通重数重算 η，冻结客户逐人逐目的地比较，普通/普通、普通/冻结、冻结/普通、冻结/冻结四类全部恢复。基本 η 版只需 MAX；可选分量初始最小值 μ 强化另需 RANGE。所有实际偏离的证书必须已经给定，默认布局也须精确 NE。零收益直接用帽 0，不除以收益。此链不生成种子，也不使任意在轨 NE 变得可救。

## 局部权种 DP 只支付适用域包含

e41 的 `commonmany-local-weight-dp-covers-incidence-domain` 正确使用 contribution。将 A 的关联图袋中每名客户替换为其所有站邻居，袋至多 `d(τ+1)` 站，连通性由原站袋子树与相交的邻客袋子树并合得到；站点原图宽至多 `d(τ+1)-1`。每站客户数≤d，所以局部精确权种也≤d。因而 B-DP 覆盖 A 的全部固定参数输入。

这不推出 A 的细运行界。A 直接子集表示每袋至多 `2^{d²(τ+1)}` 状态；B 使用最终/部分计数，自己的每袋界为 `(N+1)^{2d(τ+1)}`，保守总时间为 `poly(L,分解长度)(N+1)^{4d(τ+1)+τ+1}`。把 A 的参数转换代入 B，最多得到另一个固定参数多项式界，不能得到 A 的常状态界。因此不能把 contribution 改为不带边界的“B 推出 A 整条精确陈述”。B 允许许多同权客户而站度无界，反向域包含不成立。两类参数均固定才有相应多项式，单独树宽固定不足。

来源：结构参数正文的“A：个体客户关联图的固定树宽与双侧度”“B：站点原图的固定树宽与局部权值多样性”“树分解输入、比较与准确边界”，SHA `9d02870fb31e12e603886b503b39ca7fc396fa15e888d6f2643bb678a25e8863`。

## 深度二、三站链与坏选择器各自的精确量词

c6 的 `commonmany-depth-two-specializes-to-three-site-chain` 是真的选择器特化：H→M→L 的最长有向路径≤2，权种和每边人数可无界。一般深度二证明按来源整池首越 δ；三站独立证明可一次退回 HM 全池，保逐人平方项。`S≤γ`、`T≤S²` 与 `Q≥q` 使势差严格负。因此这里得到的是“每个完整盒 P 全局极小者均为原 NE”，并非仅存在某个 NE。后来的普遍盒存在不证明任意图的这个 P 选择器正确，深度三障碍仍有效。多项式可生成的邻域加严格降势也不控制重复返回或总阶段数。三站任意异权的统一位多项式选择仍未由 c6 解掉。

f5 的唯一逻辑边 `commonmany-bad-order-witness-certifies-fixed-layout-lexmax` 只在精确原十客户 k8 输入证明：同一固定贪心占位、不加完整盒过滤、对全部合法站纯赋值取升序收益 lexmax，唯一选择坏 NE。要最小收益>82，96 必须 E、32 和 52 都必须 B、40 必须 A，故唯一候选为 `(120,178,165,120,268,0)`。B 每家 `165/2`，B→G 后 96 在 G 恒付 176、B/E 至少 177/178，所以**每个独立 mixed 离轨 NE**的移动者收益均 176，倍率 `32/15>2`。同占位另有安全 NE，故它不否定规范贪心占位、不否定跨布局全局 lexmax 的存在证明，也不否定一般盒存在。

其余三条为 context 检查且应保持：39/35 最重规则变体与 32/40 原见证原子不同；势反例 86200<86264 与收益 214→430 是另一个输入；九客户当前静止池 44>41 只否定逐站旧装箱，增加 G 后才否定任意全局旧帽种子。即使旧全局帽种子不存在，指定移动者仍可为 20，冻结定理准确覆盖此情况。没有精确错误普遍目标对象时不造 refutes；这些反例不证明强 NP/PLS 困难。

## MAX/RANGE 当前已证与 conditional 边的逐条判定

当前 registry 把 `facility-games/common-many/restricted-identical-link-range-preserving-nashification-import` 记 proved，statement 同时包含 MAX 与 RANGE；正文给出了 UBF 子实例两端保持、阶段/递归/重组归纳、有理缩放和分量版。本文实读这份本地完整证明，但没有重读它所依赖的外部论文 PDF。不能因旧审查页曾打不开 PDF、或冻结/双 LPT 正文 frontmatter 仍写“conditional-on-MAX”，就把当前导入重新当开放前提。现有数学完成结论已可按当前 import 调用；canonical `commonmany-greedy-box-packing-reset-max-to-complete-continuation` 也是 unconditional ALL。软件未实现该算法是独立实现边界，不是数学定理的缺口。

本次四条 conditional 逻辑边并没有发现“还差某个未证明数学前提”的实质缺步：

| edge_id | 现行 conditional 的文字条件 | 当前精确判断 |
| --- | --- | --- |
| commonmany-structured-box-specializes-to-height-two-incidence | 固定参数、给定合法分解、MAX 合同 | 参数和分解是目标输入域，MAX 已有 proved 导入；specialization 的 whole_result 无开放证明义务。 |
| commonmany-type-support-and-greedy-existence-imply-frozen-light-fpt | 固定维 ILP 标准合同、真实贪心冻结域；离轨另接 BOX/MAX | ILP 是源对象显式导入，源亦 proved；冻结域和跨分量重客户稳定性已在边中证明。其 whole_result 只付目标所需在轨 FPT，离轨不是隐藏缺步。未重读 Lenstra 原论文，保留这项外部导入来源边界。 |
| commonmany-packing-cap-reset-to-fixed-gamma-interface | 在轨 NE 与全部原池删除箱证书已给定、MAX | 成功证书是目标接口的输入条件；边已证明对每份合格输入都成功，MAX 已证。没有证明所有输入存在该证书，但整条目标本就不要求。 |
| commonmany-double-lpt-supplies-fixed-gamma-reset-interface | 两轮测试全成功、首轮 RANGE、完成 MAX | 测试成功是目标输入域，RANGE/MAX 都是当前 proved 导入；失败 unknown 保留，不能因此说关系证明未完。 |

因此若 relation_mode 的 conditional 专用于尚未付清的研究前提，这四条可作**定向元数据修订候选**：在不扩大输入域、不删除 ILP/分解/MAX/RANGE 来源合同的前提下改 unconditional。这里没有擅改文件，也不把这种保守标记当错误数学边。若项目选择用 conditional 继续显式标识“对成功证书/外部算法合同的接口”，须让投影说明它不是“MAX 未证”。四条的 accepted 状态本身没有问题。根可按当前语义决定是否起定向替代；本次集成不应把仅改字段说成新证明。

## 三项可发布的定向 3B 承接

以下均核了当前 canonical 索引和相关近边。所需新边还没有 canonical 资产；不是新数学原创声称，而是把已读证明之间的真实对应正式接入。每项列明作用范围，不能在本次 3D 中冒称已经交付。

### A. 固定权种三站链的参数算法切片

- 精确 source：`SC-K-FROZEN-LIGHT-FPT`。精确 target：`M-5f6a6e775ed04aebb768fb5444607893`。若需要展开来源，可再共享读 `SC-K-BOX-NE-FPT-TYPES`、`SC-K-GREEDY-BOX-EXISTS`；不可把这三者当互为替代的单项证明。
- 新比较：真实 H→M→L 任意人数链自动只有一个至多 3 站的轻分量。若不同轻权总数为参数 d，则 93 的算法取 c=3，给 `f(3,d)poly(L)` 的完整盒原 NE 选择，保全部原客户/动作和指定冻结。这比“每边各自等权”的已接子类更广，但不解 d 无界时统一固定多项式目标。
- 可交 `contribution.result`：在真实任意人数三站链上，以轻权种 d 为参数，位时间 `f(3,d)poly(L)` 必成功输出同规范贪心完整盒、冻结客户不动、全部原客户站纯/站内独立均匀精确 NE；无需最小化旧势。
- 可交 `contribution.remaining`：目标允许 d 随输入无界，仍需一个输入无关固定多项式时间选择器；不能把 f(d) 消掉或把局部交换次数直接当多项式。完整离轨如需展示另加 BOX-TO-2/MAX，目标本项只问在轨。
- 必要正文 refs：`archives/facility-games/subarchives/common-many/state/算法/客户类型支持整数规划与有限目录选择--算法.md` §“冻重客户后的局部FPT与后续存在性更新”；`archives/facility-games/subarchives/common-many/state/问题/一般构造工作坊与安全冻结证书的完整任务合同--问题.md` §“路线 A：一般盒内均衡的位多项式选择”；`archives/facility-games/subarchives/common-many/state/定理/开站有向深度二的整池交换盒均衡--定理.md` §“域与所选择的对象”“三站链的独立单池证明”。
- 查到的近边：canonical `commonmany-directed-path-solves-edge-uniform-three-site-slice`，文件 `map/edges/commonmany-3a-3a-6e262425576aef93/directed-path-solves-edge-uniform-three-site-slice.json`，只接逐边等权的路径子域；本次 93 的 FPT ALL 边给支持算法来源，尚未接到这个开放三站目标。上述近边此次只查端点/作用范围索引，未重审其全部证明。

### B. 坏在轨选择导致成功冻结证书不存在

- 精确共同 sources：`SC-K-GREEDY-REPAIR-ORDER-NO`、`MF-FROZEN-OVERLOAD-POLY`；也可共享 `SC-K-FROZEN-OVERLOAD-2` 的完整拼接合同。精确 target：`M-306e4a2a13234a759f50236322dd308d`。
- 实际推导：在原十客户坏 NE 上 a=165/2，B→G 的正确帽为 165。若存在任一覆盖全部实际服务客户、指定偏离者普通且全部(C)成功的纯种子，冻结完成会给移动者≤165的原完整客户 NE；但 f5 证明所有独立 mixed NE（含全部纯 NE）移动者都等于176。矛盾。因此这项偏离在这份在轨 NE 下不存在任何成功冻结证书。这里是数学上的不存在，不是一次搜索失败；不必做新枚举。
- 可交边界结果：`contribution.result` 可写“给出精确合法在轨 NE 与实际偏离，使帽2a_f下任意成功冻结证书均不存在；因此生成器必须联合选择可救在轨 NE，不能先任取 NE 再承诺成功”。`contribution.remaining` 是“开放目标允许联合选择其他在轨 NE；同一占位已有安全 NE，本例不否定该目标，也不给所有输入的安全选择/证书算法”。若把这项仅作为路线 C 的适用域核查，采用 `checks/context` 更直接，仍应在 explanation 中完整写出反证；不要写成 refutes(M-306...)。
- 必要 refs：`archives/facility-games/subarchives/common-many/state/反例/固定贪心均衡的坏选择与静止超帽边界--反例.md` §“任意严格修复顺序可到无法因子二支撑的NE”；`archives/facility-games/subarchives/common-many/state/定理/冻结静止超载的偏离者受帽补全--定理.md` §“固定布局的完整证书”“残余完成与重新接纳全部原动作”；工作坊正文 §“路线 C：偏离者专属安全超载证书”。路线 C 原文已明确提到强制176边界，所以这项是跨包显式闭合，不冒称首次发现。
- 查到的近边：c6 `commonmany-frozen-consumer-checks-certificate-generation-obligation` 从 `MF-FROZEN-OVERLOAD-POLY` 到同一 open target，只分消费/生成量词；f503 `commonmany-all-frozen-certificates-glue-complete-factor-two` 要全部成功证书已给定；f5 `commonmany-bad-order-witness-certifies-fixed-layout-lexmax` 指向 fixed-layout 选择器。当前没有把坏在轨不可救与路线 C 证书不可能直接相接的 canonical 边。

### C. 晚开中心星的完整位多项式续局

- 精确 ALL sources：`SC-K-INWARD-STAR-2`、`SC-K-GREEDY-BOX-TO-2`、`facility-games/common-many/restricted-identical-link-range-preserving-nashification-import`。精确 target：`SC-K-GREEDY-BOX-FINITE-2`。目标全域更广，因此必须写 contribution；不能以星形结果当作全域高效算法。
- 可交 `contribution.result`：对所有非平凡轻分量均为晚开中心两选项星的真实规范贪心正覆盖输入，最大键算法在有理位多项式时间逐人一次输出完整盒和全部原 NE，并额外保 H；交 BOX-TO-2，以 MAX 完成全部实际标签偏离纯 NE及位多项式默认查询，保同在轨策略与因子二。一份完整续局采用多项式多的实际偏离条目加默认规则。
- 可交 `contribution.remaining`：其余一般正覆盖输入的在轨选择时间仍未闭合；零覆盖另走直接分支。已证数学 MAX 不等于当前仓内有限最佳反应程序已实现该时间界。
- 必要 refs：`archives/facility-games/subarchives/common-many/state/算法/晚开中心星形的最大键盒均衡--算法.md` §“精确域与算法”“已移客户的正确不变量”“输出的归位保护H”“复杂度、证据和不同方向”；`archives/facility-games/subarchives/common-many/state/定理/规范贪心占位的完整盒均衡与因子二续局--定理.md` §“存续源：按当前在轨池装箱”“单设施源：重置全部原客户池”“完整续局和时间层级”；双端导入正文 §“输入与准确结论”“有理位长与分量版”。
- 查到的近边：canonical `commonmany-early-center-star-box-to-factor-two`（`map/edges/commonmany-3a-3a-6e262425576aef93/early-center-star-box-to-factor-two.json`）处理 `SC-K-STAR-LIGHT-GREEDY-2` 的早开中心外向星，不能复用为晚开内向星；`commonmany-greedy-box-packing-reset-max-to-complete-continuation` 已接通通用 BOX/MAX 离轨部分；47 的 closed_overlaps 已文字确认晚开星→BOX接口，但没有本项 ALL 逻辑资产。

补充接口边界：晚开星可有中心不同轻权种随 n 增长的真实 n³ 族，因此它不只是固定局部权种 B-DP 的重复实例；关联图中心度也可无界。其正确不变量是旧客户返回阈值≥当前最近处理键并严格高于当前中心负载，不是≥其入场旧键。完整续局构造只需盒和 NE；H 是该算法的额外输出，不能反向作为一般 BOX-TO-2 的必要前提。

## 关键正文版本定位

以下相对路径均从本 clone 根起；标题均为本次读取原文中的精确 ATX section。

| 正文 | SHA256 |
| --- | --- |
| archives/facility-games/subarchives/common-many/state/推论/结构参数下完整盒均衡的多项式选择--推论.md | 9d02870fb31e12e603886b503b39ca7fc396fa15e888d6f2643bb678a25e8863 |
| archives/facility-games/subarchives/common-many/state/定理/规范贪心占位的完整盒均衡与因子二续局--定理.md | f396976f98369f049e84504ca584011691a991340804f0331a582e0fbf216a1b |
| archives/facility-games/subarchives/common-many/state/定理/开站有向深度二的整池交换盒均衡--定理.md | f8444a6566044c5749edda255101fd9e901f6edc43e363c8ca3857a85d691a7b |
| archives/facility-games/subarchives/common-many/state/引理/受限同链Nash化的双端负载保持导入--引理.md | 2e772ca84c157f59cfda395b974d3ad2f85d63ba1206105e85fa320f5a995f0a |
| archives/facility-games/subarchives/common-many/state/反例/固定贪心均衡的坏选择与静止超帽边界--反例.md | f17a382546c11c8ee4157c911e7262023c4d35426bd29a6f66c4ef47fae8988c |
| archives/facility-games/subarchives/common-many/state/算法/客户类型支持整数规划与有限目录选择--算法.md | 91f596960bff1f8fec521a1f6ed468aed409c2a34cdb07f2d880ca9fff663fdd |
| archives/facility-games/subarchives/common-many/state/定理/冻结静止超载的偏离者受帽补全--定理.md | 6be181b8a474095c33d8168852a1093eeae1937e91cfe52ebff3953be18b5cff |
| archives/facility-games/subarchives/common-many/state/算法/晚开中心星形的最大键盒均衡--算法.md | 2eca6591d675afaa727d8fda3b944945f09bcfa501bb64f21a42ef5aa9300443 |
| archives/facility-games/subarchives/common-many/state/算法/原池双装箱证书与盒外纯均衡续局--算法.md | 9cc6ab5dabf876015419f5c5483ac27c30bd0aa46bc619991e6060c0d1b9f0d0 |
| archives/facility-games/subarchives/common-many/state/问题/一般构造工作坊与安全冻结证书的完整任务合同--问题.md | 53663903a43cd211b4b7f5a9feba62942a72d326c8a9dbd2a69a659fe464b059 |
