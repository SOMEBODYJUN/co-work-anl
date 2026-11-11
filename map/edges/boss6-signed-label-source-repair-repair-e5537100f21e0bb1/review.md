# signed 来源修复后的原 3A 数学包完整复核

本次任务为 `boss6-signed-label-source-repair-repair-e5537100f21e0bb1`，沿用 Boss6，定向替代原已交付的 `customer-attraction-3a-3a-7b5d2e180fc235e1`。原任务的 25 个核心、16 个共享记录、25 项覆盖和 27 份独立边资产全部保留逐项处置。本次不把来源修复缩成只剩一条 signed 边的交付。

本轮完整实读了 41 份当前 registry 记录、原 receipt 和 27 份旧边 JSON；对发生变化的 signed 正文及新标签审查全文重读，对两个三人网格算术句和中继纤维角色句读其必要正文与记录。其他成熟证明及原运行证据按原资产、当前 SHA 与精确范围继承。`reading-ledger.json` 逐文件区分本轮全文读取和只核字节后继承，不能把该账簿当成 109 份材料本轮全部全文重读的声明。

## 标签元组与永久退出保住的编译

当前 signed v3 pin 为 `133e3bed60171a4bfcd5a49eec4330324a99998b2a92c60dc0b6dce1bc877309`。其正文 SHA 为 `e131b381683729532c961d175a879ae0ed73d4e1d392681d14fc5f323c2dad74`，新审查 SHA 为 `2a1c8458efb4e48917c6a7af77df37076aee259dd7f5f2f7ee5eb7a07e02e66f`。旧正文关于从覆盖并集唯一读回标签的句子不适用于非单射覆盖映射，本轮不能继承该句。

修正后的行动集是各组件原标签集的完整 Cartesian 积。产品覆盖是不同客户块上覆盖的并集，实际行动和有序历史保留元组本身；坐标标签历史直接从元组投影，完全不使用覆盖映射的逆。因而同覆盖异标签、零质量产生的别名、空标签、重复行动及离轨平局都保留。

每个正常前缀位置 i 都必须给每一合法坐标行动 T 的真完整孩子 SPE，包含 own 行动。定义全局策略时，在唯一首次异常元组所在层 i 固定所有坐标的退出点；未改变的坐标也选择 own 对应孩子。退出后永久使用该完整孩子，输入该坐标真实有序标签历史，后续异常不重选退出点。退出节点的全局偏离收益差是各份真子 SPE 收益差之和。未退出节点的联合异常收益不超过各坐标 U_i 之和，分层 donor 保证 Σ(U_i−u_i)≤0；末位逐坐标 BR。全部有序节点的 IC 因此成立。

固定正常叶的 W 按客户不交相加。任意产品 m 槽投影给每分量合法 m 槽，故 OPT 不超过分量 OPT 和；逐槽配对各分量最优标签得到反向不等式。因此 W、OPT 和 B=2W−OPT 均精确相加。清全分母的正整数 Q 保单位客户及同人数，输出差额仍恰为 Q[B+C(d)]。

正层 marked 成本是 2P+p，负层 LOW 成本是 n−N，故 C(d)=2P−N+p+n 不变。它可以负，是辅助组件 half 差额，不是负客户数或权重。有限真 U 表不要求 U 紧，但要求每个合法标签含 own 的完整真实退出，不能以末位 BR 叶或若干名义终局代替。K_pm 支持函数及有限 H/LOW 字典的 sum-g LP 最小性没有被标签编码改变；该最小性仍不涵盖利用 product exact-M 严格次可加的实际自由修复最优。

以上保住了原编译和 HALF 等价的数学合同，没有给出六人严格负种子，也没有证明一般 B+C≥0。五人预算仍只是由另证 HALF5 推回。两尾 FILTER 的门槛可加和固定前缀首位最低值不加，与本次指定坐标退出的收益相加相容；不能要求任意联合 SPE 都逐坐标分解。

## 稀疏两邻环的预算特化

原图 q=m−1≥3，X_j={A,B_j}、Y_j={R_j,B_j}、Z_j={R_(j+1),B_j}，目标全 X 再 Y_0。客户数 2q+1、W=q+2、OPT=2q+1、B=3，末位得 3/2 且为真实 BR。早期目标尚未认证 SPE。

假想每个中间位置有完整 U_i=1 表，正常中间利润 1+1/q，故 k=q−1 个缺陷都等于 −1/q。根缺陷 t=U_1−1/2−1/q，U_1≥0。代入当前完整 signed C 得

\[
C(t,-1/q,\ldots,-1/q)=
\begin{cases}
-k/q,&t\le-1/q,\\
t-(k-1)/q,&-1/q\le t\le0,\\
3t-(k-1)/q,&t\ge0.
\end{cases}
\]

第一段由最大负高度 −t 抵销根负供给，第二段最大负高度是 1/q，第三段根正部贡献 3t。三段连续，根可行域包含 0≤U_1≤1/2 的第一段，所以 min C=−k/q，B+C≥2+1/q>2。由此只排除此固定目标、该假想中间上界表经同一编译产生严格负 half 余额。它没有证明这份全动作表存在，没有给真实 M_i 下界，也不排更低退出或不同修复器。`ideal-signed-budget.json` 保原 stable edge ID，以当前正文、完整退出段和新审查重证重绑。

closed-source 的作用仍是控制器动作域障碍：源 fresh 而两个邻银行已旧时，预定另一 fresh 银行的下一步不存在。裸值 3/2 不能当作所有真实孩子的最低利润；因此其 coverage 仍为 isolated-after-review，语境 motivates 边照留。达裸界 2 的规定者加末位真实 BR 的匹配工具仍只是充分条件，不能扩成全主题 U 表。

## 两份三人网格的最小算术更正

两份旧边 `grid-r3-units-1.json`、`grid-r3-units-2.json` 都把每尾收益写成 3Q，同时写根 Q 和总覆盖 4Q；这个句子漏了分母 2。当前源正文和 Q=1 的原脚本/报告都正确。

四类行或列兴趣各 Q 名客户。一个根和它的同行、同列邻居组成的三标签叶中，根的两个块各与一尾分享，根收益 Q/2+Q/2=Q。任一尾在共享块得 Q/2，在自己的另一独用块得 Q，故每尾 3Q/2，总福利 Q+3Q/2+3Q/2=4Q。Q=1 的根叶为 (1,3/2,3/2)，Q=2 为 (2,3,3)，与两份独立完整动作表对应。

两表的第二行动和末位离轨动作不同，不把 Q=1 报告当 Q=2 的执行证据。均匀驻留的 D=Q、P=4Q、P/D=4、根/尾比例 2/3 不受影响。两份 replacement 保原 stable edge ID 和 contribution 作用范围，仅改错句并加显示份额说明。本轮未运行原脚本、全树核验、BI、LP 或随机程序，也不把阅读原执行事件计作新运行。

## 中继投影的同一纤维

原 `relay-fiber.json` 的 explanation、条件和 contribution 均说同一实例、同 actual、同实际查询末回复、同 z，净金额相同而真实根偏离不同；但 target 角色句写“两个纤维中的不同 SPE 点”。准确的句子应为“同一投影纤维中的两个不同 SPE 点”。该角色句本次最小更正，保 stable edge ID。

全文重读净中继正文后，两表 actual MRR、收益 (3,2,2)、W7、全部实际前缀 query 的末回复相同。根改 T 后两表的真实中继分别为 M 和 R，当前者收益分别为 2 和 3，离轨福利分别为 8 和 7。δ_1、s_1 各相差 1/3，但 τ(δ_1−s_1)=−5/3，Debt=−133/12，NET 两边都是 −187/12。PROJ 只消去净额内的真实偏离项，不能据末回复投影反演完整中继。强付款仍需额外不等式，K 非负不等于已支付。

具体令 Π 保留同一实例、actual 有序路径与收益、每个 actual 前缀对每个合法 query 的末回复，并固定同一 z。两份策略的这些保留坐标逐项相等，所以在 Π 的同一纤维内；根真实偏离利润却分别为 2 与 3，故它不是 Π 坐标的函数。直接来源是 `archives/customer-attraction/state/引理/净中继债务的包络余项与真实信息消元--引理.md`，唯一标题“八客户：真实SPE到该投影确实非单射”，当前完整文件 SHA `a5a2815369825a109430268811774c5465df43f7e07e541576c6199738312ac8`。不是以两个独立输入的同汇总量冒充同一实例的非单射。

## 全部核心的实际比较与剩余义务

下表的“保留”表示本轮逐条比较了完整当前 registry、旧边和旧 coverage，并核必要引用当前 SHA；没有声称所有原始脚本/大证书本轮重新展开。changed-source 及上述错句按前文另作全文重核。

|核心对象|比较结果|剩余范围|
|---|---|---|
|M-bdc70d9420664c1396118db568c5675f|同一投影纤维两份完整 SPE 的 NET 净额相同，真实中继不同；更正角色句，保局部 contribution。|一般强付款仍未证；9 客对照不是两表存在性的独立证明。|
|customer-attraction/net-relay-debt-envelope-residual-and-true-information-elimination|同一个 z 和全部 E/F/K 的消元恒等式保留。|重新引入真实节点的跨位置漂移及一般预算未付。|
|M-6f70a2911d6f4ca98691a971b07f73e2|裸界 2、末位 BR 及 fresh 匹配构成真实 BI 拼接的充分条件。|不能替代任意前缀、全合法动作的退出表。|
|M-a10a08e480b24d959811b551f145a26d|仅证明 one-herder 所需 fresh 邻银行不存在，保 isolated。|没有真实 M≥1 或 M≥3/2 的结论。|
|customer-attraction/sparse-two-neighbor-cycle-ideal-exit-table-signed-budget-exclusion|当前 signed C 的三段特化仍给 B+C≥2+1/q。|完整中间 U=1 只是理想假设；其它退出和修复未排。|
|M-eb1e9781aec04857b104eea981a86059|r≥5 所有规定尾序都有严格末位换行/列偏离，保整条结果。|不排其它菜单，也不以 r=4 的零增益自动给策略。|
|M-46712a7278244313a7802a857065b4e3|一般合法网格代数锐性、两份 r3 真实实现及原 r4 成熟有限构造均保留；修 r3 尾收益。|r≥5 这套网格末位失败，不能宣称一般真 SPE 域最优系数。|
|M-3e048fe6c4e34f639497dd78ec993637|Q1 的独立 21 节点完整表给 (1,3/2,3/2)。|只是三人零背景特例，不代替 Q2 离轨表。|
|M-e55ccf2f12664e9594eaf13382f7a3aa|Q2 作者完整表给 (2,3,3)；原运行职责独立。|只保原 84 比较的固定输入，不外推人数。|
|M-2639704a112a411cb26b33ca7444df18|两尾 FILTER 使单件 L=3/2、双件 L=5/2<3，并有解析完整根补全。|不反指定坐标策略收益相加，不给一般长尾加性。|
|customer-attraction/arbitrary-background-two-tail-product-threshold-and-credible-filter|联合末 BR 积、λ 和 θ 加性及总阈值 FILTER 全部保留。|固定首位最低 L 或任意长后缀不能据此可加。|
|M-56ec9cd2fcce45aa9967d48ed1da0a7b|真实 fresh 初始化的 reset 前缀不变量保 source-order 及后缀 HIT。|full-O 初始化可直接付过去，不能继承 source-order。|
|customer-attraction/net-coupon-global-role-hitting-and-fresh-source-suffix-bounds|同一 SAFE 核及局部凸包共同给全 context 终点 HIT 和价格。|来源 M 不是 actual u；角色 cap、客户 cap、共同费用未证。|
|M-0b53618e76614597a1b1991efa5cc496|固定 m2、单题种子闭包 p 标签/p−1 轮；双题最优种子 p−2 轮。|不是低福利反例，不排重选另一小目录策略。|
|M-5a729675672041dd87da781da105b537|完整有序回复闭包保原 SPE、actual 和指定证书，最优支持种子保 OPT。|同时删查询行/列的整体 minmax 没有一般单调方向。|
|customer-attraction/legal-prefix-independent-background-anchored-counting-and-same-leaf-ancestor-reserve|ANCHOR 和同叶祖先 reserve 为同 Q 提供准确静态接口。|自由 Q 仍需同份分布联付查询与祖先；actual 删除支持失败不否自由 Q。|
|customer-attraction/reply-closed-catalog-exact-policy-restriction-and-certificate-lift|保留 Γ 等价、类型投影和已存在 λ 的证书提升均保。|不能保证 λ 存在；压缩静态 N 见证须仍合法或重新验证。|
|customer-attraction/pb-counterexample-extension-to-fractional-extra-slot-floor|PB 完整子 SPE 加连续容量/Jensen 独立证明得到前三位各 u<s≤f_r。|不从 t≤v 的方向偷传反例；合法大背景未必原根在轨。|
|customer-attraction/static-slot-deletion-and-security-aggregate-boundary-resource|带索引槽均匀删一的静态人数不等式及零背景精确式保 isolated。|未找到把 Q′ 当原 σ 真实回复或动态共预算的桥。|
|customer-attraction/sixty-four-atom-shared-punisher-exclusion-and-failed-alignment/integer-catalogue-rejection|原 114 类型/15 标签精确递推在 ABC 剔名义目标，ABCD 尚允许。|只拒冻结整数目录和指定路径，不全否浮点对齐路线或 half。|
|M-e81e94795a014e59a87f8ab9e2b654d5|同一 34 客 σ 的自由 13/48、强差 −1/48 和实际列 cap17/2 并存。|共同实际列的精确支配只及此输入，不可删所有空强制端点。|
|M-060a9717320f4f57bfa76d087c8909fb|固定 GF(2) 秩束的 Möbius 三交量 −1 阻非负客户覆盖，保 isolated。|扩大模型的等号不能直接迁到单位客户覆盖；一般表示桥未付。|
|cag-strict-policy-discovery-and-frozen-static-deviation-compression|闭包完整保持严格 S 行，旧 q* 支撑保留时 P 行仍非负。|其它计数的 N 盈利方向及 W 需重核，不宣称全局客户数最小。|
|customer-attraction/three-theme-fixed-root-suffix-cones-and-old-two-theme-replay-contract|固定 m=p3、81² 对同根完整两尾锥及花瓣达到点身份保留。|历史只保存摘要和证书流 SHA，不虚称全 6561 流重审或一般人数结论。|
|M-064ab2773d0c4071b4532a7a0102685b|9 客终局占用/势 7<OPT8 精确否直接支付，保 isolated。|相同汇总与 8 客不同占用是语境对照，不是其独立全历史证明，更非 half 反例。|

## 原资产处置及阅读边界

27 份旧资产中，4 份 replaced：`ideal-signed-budget.json` 刷当前源并显式保标签/own/永久退出条件；两份 `grid-r3-units-*.json` 补漏写的 /2；`relay-fiber.json` 改同一纤维角色句。其余 23 份 retained，原路径和原 SHA 精确写入新 receipt，不复制、不改绑，不退休任何一份数学资产。逐项理由同时见 receipt 的 supersession 与 reading ledger。

25 核心的旧 linked/isolated 划分保持；新 receipt 给出本次具体比较、结果及 remaining，不以语境边充当逻辑覆盖。没有明示 follow-up 对象对，因此 `closed_overlaps` 和 `follow_up_tasks` 都为空。普通比较留在 coverage/comparison_scope 和本审读，不制造假 follow-up。

本轮核了全部 41 input pins；146 个 task reading refs 和全部当前 registry refs 去重后 109 个文件的完整 SHA 均吻合，71 个带 section 的 task refs 标题均存在且唯一。逐项旧资产 SHA 亦相符，旧边中只有 signed 特化的端点/证据过时。字节核对不等于重新读取全部数学证明，全部文件实际读取范围逐项见 ledger。没有并发版本变化被悄然接受；交付前再次核任务 SHA 和 inputs，变化须交 Root 处理。

本轮科学程序执行数为 0。元数据 JSON 解析、SHA、标题定位、写 staging 不是新科学证据。成熟 r4 有限构造及其它历史运行证据按旧已付合同继承，不为缺少新 journal 而重跑。所有新文件只在独立 staging，Root 负责 native bind、check、Git 与队列交付。
