# INF-CHAIN-3D：有限 unit path、固定正阈值与同一 ∞ 输出的有界数学复核

身份 Boss1。本报告只复核下列两条现役精确边，不认领任务、不形成 formal coverage，不更改 clone、registry、队列或 pending。结论来自本次直接推导，不以历史 PASS、哈希或旧审查结论代替证明。当前 clone 的两条 accepted/unconditional/whole 关系均成立，无数学修复或降为 contribution 的必要。这里的 DegreeThree 严格指物品侧正度，不能读成一般不相关机的机器总度三。

本次没有重跑科学程序、LP、旧证书、枚举或原审计；只读本地已提供文件，并对必要原 PDF 页做文本提取、对 Figure 2 所在第9页做视觉核对。所有新文件仅在父任务指定外部目录。

## 1. 精确当前资产与已交付 owner

两边均从当前 `research/registry.json.edge_files` 逐文件精确匹配 edge_id 得到，未采用旧同名路径。当前 registry 原始 SHA 为 `ee69e1d69997195bca745ef6b475bed6bd1e68122a0da4b0a112868d3d375d0e`。本报告 native pin 采用实读 `tools/research_runtime.py` 的规范 JSON 规则：UTF-8、ensure_ascii=False、sort_keys=True、separators=(',',':') 后 SHA-256；不是声称本次运行了 native edge-check。

| edge_id | 当前现役路径 | 原始字节 SHA-256 | native pin |
| --- | --- | --- | --- |
| boss6-finite-unit-path-to-all-positive-infinity-chain | map/edges/boss2-wave10-repair-46ecca640d16d383/finite-unit-path-to-all-positive-infinity-chain.json | cd8023fd11bd80ea891f6cc4392266d82ec6ca792616b1d1c6df82e8d0c93dab | a662b342b97437774566f9afb1f210161547eb7209475d1609de8ecfcd4c5d2e |
| um-826e-unit-helper-path-to-fixed-threshold-degree-three | map/edges/boss2-wave10-repair-46ecca640d16d383/unit-helper-path-to-fixed-threshold-degree-three.json | acdb4fa386dd1c42520ebf011a67d07188db025435fc86a5325094a7a6e05243 | aea920f15340eb218f5c5023275052e761a12143f7cd133f2e6afaad8432446d |

两者当前精确资产的 done 持有者都是 **boss2-wave12-shared-infinity-3b-862d68637cc402ea，Boss2，stage 3B**。该 task 的 embedded receipt 与现存 receipt JSON 逐值一致；receipt.assets 同时列出上述精确路径和 SHA。原46e目录名不能据此解释为46e任务已经done。

| 定位 | 原始字节 SHA-256 | native pin / definition pin |
| --- | --- | --- |
| research/operations/map-v2/tasks/boss2-wave12-shared-infinity-3b-862d68637cc402ea.json | 7b2cd88fbfda063660dbd795727e34e81ba3947940cdd8414fdc3608f8b85d48 | 整记录 fcef4869fcd27e2951c71a7e397325c9962e14417667fa3a8fa89e778d79b30d；definition c6057b474f6f781498b8f33c02eb9d57951975d8ec8b4f5840d9ca0a15c5dbd2 |
| map/receipts/boss2-wave12-shared-infinity-3b-862d68637cc402ea.json | 70b0f90acb14ee5b7f44e6228bbbbb40dcc6e9ff45f66e1aeaad9618645bb516 | 6e53322b16ba7364baf2947d919d5762b972404dbe4df7220c79b7413b23ca63 |

当前 integration 的两 edge_pins 及上述 task_receipt_pin 与独立重算一致。原 `boss2-wave10-repair-46ecca640d16d383`、`boss2-wave11-inf-chain-transfer-repair-repair-f72bef2e3569ee84` 已 withdrawn；现有 done 联合3B明确 supersede b222 和 ea6be 两个旧 holder。只读筛查本 clone 的未完 tasks，没有发现仍在途且同时涵盖本精确问题的 repair。因此本次不采纳未交付草稿，也不新建、抢占或重做该3B。这里的状态是提供 clone 的现存同步快照，没有访问凭据或另查远端。

## 2. 三端点当前合同与所用证明

记 F=M-080d9b22ae87408f9a673a898c7a6dc3 v5、A=M-16209762a32e42e48ec20b76381b5e9d v1、D=M-a9534c70ffa74fca9a91cd270468de3f v3。三者完整 object record（含 model、statement、quantifiers、assumptions、scope、objections、body/evidence）均已直接读取。

| 端点 | 当前 registration pin | 本次实际使用的正文和完整文件 SHA |
| --- | --- | --- |
| F | d0b2a08064ea4ddb1eb3d096b576113c85d2effdc50f43593b10cf756e4c217a | `archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md`，8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66；全文实读，承重节“4. SC unit-helper 路径” |
| A | 7eccabec57217ad462462ba0ca4da21e7e3928e2cf3d1859fedf609e00dc907e | `archives/unrelated-machines/state/定理/无限helper全阈值降度与三度二无限度配置间隙--定理.md`，9d56eff7715d695c85f6e45707b899633faef71dd1388c86bea1ac4fc721dbca；全文实读，本次承重§1–7；§8–10虽读到，不据此申报额外覆盖 |
| D | 608415f3a648158ae4b612cc7a9f2e21699ee3b73ef786908e0f40654b33fb44 | `archives/unrelated-machines/state/文献/PCSP最大最小分配与投影博弈平行重复三篇文献整理--文献.md`，a0d8bb0b5261e46ef6843a1e2c9bb812393f22953129ffba03313e0c16b5fb36；只将§2 MaxMin完整连续部分作为本次正文审读范围 |

F 的正向合同是被保阈值在 (0,1]，不是要求每个旧端值≤1。oldOPT≤1或旧最高CONFIG阈值≤1仅用于源的精确最优值推论，不是转换一次给定阈值见证的前提。反向对任何正阈值有效，helper可能同时占两份copy，不能强剪singleton。

A 要求量词 `∀I ∃J∞=G(I) ∀有限实s>0`，并同时支付 INTEGER、原始CONFIG、扩展最优值、物品度、条件∞度、值域、counts及给定证书编码。D 只要求 `∀I ∀给定有限实t>0 ∃J_t=G_t(I)` 的整数阈值/见证、组合规模和显式有理编码合同。以下证明逐项区分。

原始CONFIG使用所有效用≥s的配置，每玩家配置质量恰为1、每物品总边际≤1。非负加性估值、物品单归属、有限非空玩家都是承重条件；允许可空物品，∞按常长符号解释。本次原 PDF（SHA 7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f）直接读印刷/文件第4页的物品侧定义、第6页 Definition 2.1、第8–9页 Theorem 2.4/Figure 2，并视觉核第9页。没有宣称重读49页全部论文或重新审计其算法。

## 3. 共同局部构造与整数双向见证

对旧物品j，按不同玩家身份列出全部正owner i_1,…,i_d。仅当d>3时删j，加d份copy c_1,…,c_d：旧玩家i_r只在c_r保留v_(i_r,j)，其他旧玩家对此链copy为零。增加d−1位helper h_k，h_k仅在c_k、c_(k+1)各取值H。未列端为零；d≤3的旧物品保持。令H=t有限正数得到固定阈值输出；H=∞得到同一全阈值输出。helper属于新增玩家，全部加入maxmin目标。

正向，先删旧分配中的零值使用。旧j给i_r时，旧玩家取c_r；k<r的helper取c_k，k≥r的helper取c_(k+1)。副本两两不同且恰好避开c_r。旧j未用时任选一个hole，照样满足helper。每个旧玩家逐物品效用精确保留，每个helper得到H。因此H≥s时任意旧s见证都转成新s见证；不需要知道或求出旧OPT。

反向，新正阈值分配中的每位helper必须取至少一份相邻正值copy；不同helper受物品单归属约束，d−1位helper占至少d−1份不同copy。最多剩一份可正值服务旧玩家。删掉零值使用后，把原玩家所用的这份copy合回j，逐链无冲突、旧玩家效用不变。helper拿两份时可能一份也不剩；正确结论是“至多一份”，不是任意目标见证都“恰好一份”。

上述matching按每件物品独立，没有跨链共享helper或copy，所以仅对d>3物品局部应用是实质上合法的；没有从全变换中无证明地删除需求。整数正向在H=t处给D的固定t等价，在H=∞处对每个有限s>0给A的整数等价。

## 4. F→D：固定t、封顶、实数与编码分开

对显式有限有理原值和有理t>0，把原值除t，在目标1复用F逐物品构造，再乘回；单位helper值成为t、旧copy值成为原值。即使归一化后的oldOPT>1，只要给定旧分配达1，正向matching仍保每个旧玩家原效用且helper值1，所以本边没有误用F精确OPT推论的oldOPT≤1条件。

若允许旧端∞，在固定t先取vhat=min(v,t)。对任意非负bundle，原和≥t当且仅当封顶后和≥t：含一个被封顶端时该端封顶即为t；无被封顶端则和不变。归一化后是有限有理输入；最终把旧owner-copy恢复原v。新实例的任一达t见证也可先封顶，回源后再恢复，阈值双向仍成立。helper本来∞可以在此固定t截成t，因其单件已足达标。

任意有限实t>0的数学结论由§3同一matching直接验证，无需有限字符串编码任意实数。位多项式的算法结论单独限定原估值及t采用显式二进制有理编码；分母除乘的位长受输入与t的总编码控制。不按t数值枚举，不解决未知OPT或隐式配置搜索。

D的目标是完整整数阈值合同，其全部整数、见证、规模及编码结论均由本边付清；F已有CONFIG性质是额外背景，不拿它替代D的整数目标。固定有限helper不能再推任意OPT全值保持。

## 5. F→A：同一J∞的CONFIG双向与全阈值量词

先按I构造J∞，构造公式不含s。固定任意有限s>0，给旧CONFIG(s)可行解；先从配置中删除所属玩家的零值物品，不改变效用、质量并只降低物品负载。

对一件被拆旧物品j，定义其owner边际q_r=Σ_(C含j)x_(i_r,C)。旧容量给q_r≥0和Σq_r≤1。确定性选w_r≥q_r、Σw_r=1，例如把全部余量加到最后一个r；令W_k=Σ_(r≤k)w_r。旧配置把j换成该owner专属copy。为helper h_k添加两份singleton，{c_k}质量1−W_k，{c_(k+1)}质量W_k。质量非负且和1，singleton值∞，所以对当前任意有限s均合法。

副本c_r的helper总边际为：r=1时1−W_1=1−w_1；1<r<d时W_(r−1)+1−W_r=1−w_r；r=d时W_(d−1)=1−w_d。因此每copy总占用q_r+1−w_r≤1。旧玩家配置的效用及质量保持；未拆物品容量保持。这得到正向raw CONFIG(s)见证。这里仅用玩家各自配置分布及单物品边际，不假设其存在共同的整数随机分配。

反向，给新CONFIG(s)解并逐玩家删零。每helper的每份正质量合法配置都含至少一份其相邻copy；该helper行质量1，所以它在该链的期望copy消耗至少1。d−1位helper合计消耗至少d−1，而d份copy总容量d，故原玩家全部copy边际总和≤1。每个旧玩家在这组copy只有自己的一份有正值，因此同一配置投影不会产生重复j，效用、配置质量均保持；所得旧j总边际≤1，逐链同时投影合法。这不是把fractional见证改称integer分配。

同一J∞的公式、INTEGER matching及CONFIG见证公式均不含s。故确为 `G(I)=J∞，对每个有限实s>0同时两类Feas等价`，而不是先∀s另造输出。若要形式上复用F有限输入证明，对某个s选有理H≥s，封顶旧端至H、再除H，在阈值s/H≤1使用F；恢复copy旧值与helper∞后各bundle达s的判定不变。H只是这个逐阈值证明的辅助量，绝非J∞输出参数；任意实s也不进入证书编码。

两个非负优化值均由正阈值可达集确定。全正阈值等价遂给整数OPT及最高raw CONFIG阈值的扩展值相等，包含零和∞。s=0本身不用helper耗一份推理；零最优值由不存在正阈值的双向等价处理，配置在零可用空配置。

## 6. 度、值域、精确大小与位复杂度

每个内部copy只有一个旧正端及两个相邻helper正端，总正度3；链端点只有一个旧正端和一个helper端，总正度2。低度旧物品本来≤3。若输入每物品∞度≤2，将至多两个旧∞owner排在链两端。内部旧端有限，于是只有两helper∞端；端点有一helper∞端加至多一个旧∞端，∞度仍≤2。原值域{0,1,∞}保留。一般旧玩家的正度/∞度逐边保留，不因此有三/二上界；每个新helper自身正度和∞度都为2（∞版本）。

DegreeThree是物品侧定义。若把玩家与机器、物品与job作纯二部图对应，也只能得到job有至多三台正关联机器，不能称机器本身总度≤3；更不能由这项图对应自动得到UM makespan的目标、处理时间和阈值迁移。两边当前scope均明确不外推一般UM。要迁移另一个已登记结果R到UM目标，必须另给实际模型桥B并以ALL{R,B}为源；仅存在某个性质相同的图像不支付多项式归约。

令S=Σ_(d_j>3)(d_j−1)，每链净增d−1位玩家、d−1件物品、2(d−1)条正边，故n′=n+S、m′=m+S、E′=E+2S。S≤E给组合规模O(n+m+E)。n,m≥1时E≤nm，且n+m≤2nm，故为O(nm)；输出稠密矩阵至多O((nm)^2)项，也仍位多项式。不能将O(nm)改成两种顶点数各自≤nm；n=5,m=1,d=5时n′=9>5。原论文p9的字面mn表述已被当前端点的O(nm)准确合同替代，无需再改现役边。

设给定有理旧CONFIG见证有Q个正质量项，总编码L。原玩家配置只重命名物品，不做配置笛卡尔积；每新helper至多两singleton，所以新支持≤Q+2S。q、w、W只需有限多次有理加减和部分和。取输入见证概率所有分母之积D0，log D0不超过输入分母位长总和；全部输出概率可用D0作分母且落在[0,1]，每个输出概率位长O(L)。输出配置标号增长也只多项式；反向不增加旧玩家项数，可保留重复项或合并。这里支付“给定证书的转换”，不支付求解指数配置LP。

## 7. 真正边界、ALL前提与修复判断

有限H>0若有至少一条被拆d>3链，在s>H时每helper需至少两份copy才能达标（s>2H则无合法配置）。INTEGER单归属或CONFIG边际均需至少2(d−1)>d，故新实例不可能可行。若旧四玩家各有私有值100的物品并另共享一件四端值100物品，旧OPT=100，helper取H=1后新OPT=1。这给出去掉s≤H条件的明确反例。若没有物品被拆，输出恒等，不能套截断句。当前两边已正确保留该范围。

本次两条边不是把某个未知外部结果跨模型搬运：F本身提供已证有限SC构造与见证算法，D/A是通过上述缩放/封顶/局部应用或∞扩展得到的新完整构造合同。两边单source F合法，全部新增推理已经直接付清；没有漏掉一个尚未证明而又必要的独立桥端点。若后续把A作用于某个原定理R，则相应结果边仍须列R与A共同前提。本报告没有为其它边补写或省掉这种ALL条件。

F v5唯一共享来源更正属于flat machine CONFIG(1)：质量λ的selector+零job配置和质量1−λ的全部incidence配置都含零job，其覆盖λ+(1−λ)=1，私有负载仍零。F主正文原已写对，§4 unit path并未改变。当前source-delta-review及done联合3B的新review均明确更正只刷新证据/record pin，不产生本两条边的新数学缺步。历史F v3/v4、future f72等字样应按原时点读取；不能用旧稿的claimed措辞覆盖当前task已done的状态。

**最终处置建议：保留两条现役accepted/unconditional/whole关系的原文件原字节。** A的同一∞输出、整数/raw CONFIG全正阈值、扩展最优值、条件∞排序、值域、counts、支持及编码均已证明；D的固定正阈值整数/见证和规模/编码均已证明。没有需写入clone的最小修复。若3D展示中出现“机器总度3”“有限helper全OPT”“逐阈值输出等于同一∞输出”“配置存在性即整数/多项式求解”等额外表述，应只收回该额外投影，不损害这两条准确边。

## 8. 实读与复核记录

`refs.json`逐项给出当前路径、全文SHA、native pin、endpoint pins、实际使用章节、done task和receipt定位，以及原证据的字节一致性。其read_scope严格区分完整读取、必要章节、PDF指定页与只读状态定位。本次不对未读的原canonical外部scratch稿、全49页论文、其它算法、B/G/H/C对象的完整数学或全仓覆盖作承诺。

本次新增的是本报告的独立matching、copy容量、prefix边际、量词、编码和边界推导；历史review只用于比较来源与已交付owner，不替代这些数学步骤。
