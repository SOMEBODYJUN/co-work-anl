# 私有分叉树估值、包络与支持LP的实际独立攻击

审查对象：下列分版本记录的私有 q 估值、支持 LP 各项，以及追加的坐标切片编译反例。原各项完整陈述和证明见[私有树正文](../../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)，新增完整实际 P 反例见[坐标编译正文](../../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。本记录是内部审查，不是外审或新颖性认证。

## 冻结顺序与实际读取

1. 精确陈述先行，SHA256 `c8a686e99d9ba1e086fb0996573765de9b129d759366fd74026c4ef4d4d38ff4`。审查者仅据陈述重构三项合同，冻结独立稿SHA256 `db2d5dae205831a18cab1323d00d38fbeff630fa5d9ed0f75f20eeda65ac216c`；没有先读拟议证明、代码或有限输出。
2. 随后实际读冻结证明说明SHA256 `223e2c4e6c3945f1bd4dfe93b439144f50cb52cd9f45627d6f163b0dec60d477`，第二阶段记录SHA256 `a22a538bbebdbd3031b6852fe796ba27aba2d9d7ed88902e28ba87d18b89ec43`。三个Claim分别无standing fatal。该审查者没有运行文中的旧scratch测试，未把其旧数字当作复跑结果；canonical只列下面实际冻结的新审计。
3. 实现者依据合同写生产value/demand/分离函数与独立枚举审计。boss完整读生产代码，亲自重跑新审计；除elapsed_seconds外全部字段相同。标准generic LP优化没有实现或运行，未虚构实现状态。

以上scratch哈希固定实际顺序；并非本文证明依赖。承重推导已完整保存在现行正文。

## 实质攻击

- 深度固定：分叉子树必须一直到原深h；0高度仅用来归纳，不代入XOS分母。k=1是显式深链，分母1；输入必须支付链/完整叶地址的真实长度。
- 子加性：二色分叉对偶可直接重构；原证明的h-index整数递推也正确。有限状态最大值保留子加性，未偷加次模/XOS。
- Demand：逐state单射是叶成本可加的承重条件。跨state共享资源允许，但一次只选择一个state；全U负价资源先收入并只计一次credit，包括所选state之外资源。上界/达到性两向均已核，输出实际最优集合与子树。
- XOS全叶包络：最大q≤t集合大小M_t=N−(k−t)^h来自旧命中引理。uniform权重的全域有效性需M_t≤tM_1；反向需叶传递自同构平均，不能先把任意w假设均匀。平均只作证明，不枚举指数群。实域紧致与有理uniform达到性均有效。
- 渐近量词：Γ(B)按叶数上限取max；k1无限h但值恒1。若t=min(k,h)，tlogt≤logB，选k=h≈logB/loglogB分别给上下界。没有声称每个B是k^h或由此得到NP-hardness。
- LP投影：任意辅助c只须不超过真实最便宜s树；不能假定它自动等于DP值。sum-s-smallest的hypograph与归纳提供反向；正向取真实DP、顺序统计z及正差t，全部在[0,k]。s0由W≤k处理。
- 多状态：single-state LP没有自然交集延伸；精确demand交换两个max也不解决共同blocking的并集成本。本文未升级多状态minorant优化。

## 实现和认证边界

代码SHA256 `e483a5f148c42c498b45fb160e73666f43cc90672758b9f68eb2cad4d46c3090`；冻结新审计SHA256 `8f893e295438e739efcc20fb718412cfbe03b0d3519118c032e5131ab4ccb9cc`。800子集、901实际树、52分离、24 signed价格的枚举只核所列输入；LP证据是约束数据与给定权重的扩展证书，不是generic最优解。

三项限定证明完整、先陈述独立重构及后读冻结证明已发生。value/demand/分离已实现；generic LP优化未实现。外审、新颖性、独立成文价值未认证；一般UM正反目标不变。

## GLOBAL-XOS、图计算障碍与单阈值简化的追加审查

- GLOBAL-XOS的精确陈述先行：独立者重构具体r树uniform权重及全域有效性，冻结稿SHA256 `5581aebabee27bf093f8303b3f2aaa3901dcb85f13b68c90e84f5dc26bd5f5a6`；之后实际读root冻结证明SHA256 `e34538110de25700cef1a61886bdde90d6085ed4632907acc7cdee186b387462`，读后稿SHA256 `49777713333633f97c78da96dc27ded8fe5618f1a8a06c04c22d07c438d35920`。核partial S、几何和G单调、全域B的minorant、真实同深子树和共享state均无fatal；未声称新增w输出接口已实现。
- 多状态图Claim仅含精确陈述的输入SHA256 `eb76748843a3be7431be1bb8b7accd14eadcfa6e76b43e6661ee61ae20712642`。独立者先冻结重构稿SHA256 `6bd8b44a0fe0300b052a6ea16db8b018d3bea0b9e793e369c5364017f76c4880`；之后实际读拟议证明SHA256 `681e920a056b54af9859787d365e9d78e323f218a71cd926989c7d6be5a4a233`，读后稿SHA256 `bb0ab4441034781320bc18c3572caa5a95ae1adefc2ca96298339e32d2e71471`。逐项核Δ精确式、uniform W<2归约、K1解码、NP/coNP区别、signed demand及E_f(S)=f(S)易解反例、有效生成LP后果。root实际渲染已注册Karp2010再版PDF14/原印94核MainTheorem/CLIQUE；未复制另一份扫描、未声称重构Karp全归约。
- 原三项与图Claim的canonical全文又实际核至SHA256 `3a56512de619eeefa58bbc89f897eaeeda914ba9365c4b83c14503d55699f916`，回执SHA256 `1da7cc525596a3f2f496450ced2f9e6fe5cbcc516eb86a61d32123e580be0dc6`。该审查者仅把GLOBAL-XOS作为上下文读，不冒新盲审；指出开头“三项”及“不是计算困难性”两处导航措辞与追加后内容不合，已改为“本页各项”及“包含限定minorant计算障碍，不是UM makespan困难性”。原已审证明未改。
- 单阈值Claim另冻结只有陈述的SHA256 `319feb4a879a6b6384c24fa15fd62b56d2410db8c2ef99411555a8998d78ecb7`；另一独立者先重构并冻结SHA256 `d0e3a2e57ae981d7ee830a334438d1e2b99a8cd12b7999299813b70ff4ae509f`，之后读完整证明SHA256 `bbeaa68822fcd311b902662c698a165e6ac0b4e5cad27149b1e7cc95a1297e72`，读后稿SHA256 `4e03c512c95163bc4bb4e196280bf3ba0b04ed2ea46b47fe23d8a76dd0090145`。实际色类划分、高孩子数量、h1/k1、F叶0、消Z后的正系数归纳、人工W/F/Z界及全矩阵非零计数均无fatal。root亲自逐式核对。未改旧代码，未声称新增O(V)LP已由generic solver运行。

六项身份在各自范围内成立；不是六个一般UM结果。最深层的源gap/弱调度解码仍为未完成义务。真值、实现、外审、新颖性继续分轴记录。

最终整合正文SHA256 `e26b2b805d635380bd05e1b7a45a0bea9e6e9ed681cb91b3b4680f68154cf467` 由GLOBAL-XOS/单阈值原审查者实际读取相关新增段并核旧代码及冻结证据hash不变；没有冒审其未负责的图hardness。原三项与图Claim另由前述审查者核至3a56512版本；之后仅修两处导航并追加已另审的单阈值合同，不改变其证明。

## 坐标切片的精确阈值、padding及双射反例：v4追加审查

本节只覆盖 `UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v4`，不改变上面各项旧证明。一个候选随新增结论依次冻结v1–v4，最终仅登记v4，不将中间版本复制成独立结果树。

### 实际先陈述与读后次序

- v1 Exact SHA256 `2d889e2109657bffda860acbad4ce64accd06fd207d47c96fa803647fc15b6a8`，原字节见 [初始陈述](../../../history/source/notes/unrelated_machines/coordinate_slice_initial_exact_source.md)。作者先有证明并向root披露，因此root不记作零信息盲审。另一研究者只读Exact，自足重构A–D后冻结 `31b04eafa400809d69db35fa2dcad0dfde7f590895855e351bbf44e4c1733714`，见 [初始独立稿](../../../history/source/notes/unrelated_machines/coordinate_slice_initial_independent_source.md)。随后才读作者完整证明 `24dc6c82f4203b02afd02be8c8c4ffe22d23ccd9ac21ca1e0a8dd00045fbfc5a`，读后稿 `d1590ac6f0a3204cabb7cadca5a4bed55f312efbb04b6d177b5f51da5e7f7bf1`，无fatal。root亲自逐边重构、逐机核全部任务。
- v2 Exact增补 `6f547983c9bdb112db07d17e0a246ea2ef57c3f72919f440c6f4141995623abf`，见 [原字节](../../../history/source/notes/unrelated_machines/coordinate_slice_exact_threshold_addendum_source.md)。root独立新增strict iff及网格精确OPT，未先给证明。两位研究者分别冻结重构 `b2deacd4830bdf64b7671de2ba4280936c1104ffada4f12e95ae050de32644fc`、`9b46c05a7153ed902237e96f9f5083c34a20543487d144c42259e44609c99fb5`，才读root证明 `50672b829eb28d7f0c301c9dbe1d42fc541fb1e1a7905a17e0ddc1eaed2d3fb8`。v1“固定D从而固定rho”的措辞不严已修为固定满足条件的g、rho、D，不改变数学。
- v3 Exact增补 `8abe3bf7eb704ad41acfffae69ed0f0fd1eb1a824fb9b0216698815c455331d7`，见 [padding陈述](../../../history/source/notes/unrelated_machines/coordinate_slice_private_output_padding_exact_source.md)。root和一位已读思路的研究者不称盲审。另两位只据Exact分别冻结 `c8cda1833f77407c110dca959795e9080d6e24e2791aeb1a8a8d8ba49be896c4`（[完整独立稿](../../../history/source/notes/unrelated_machines/coordinate_slice_padding_independent_source.md)）和 `6b9bdaecfdd5e86385bcbc9bd5d7667b6c6ca16fda7f77bb597b57631ae78217`；之后才读root proof `c41120d402cf022abff01beb838f81ce974a68ea622ec29ad1a84a1873fae5e8`。读后回执 `6995df185e55ac74848b2e343c73e90ade5467cccb09dc653ac1c3c5c7d2bd72`、`b48a5ea2b56843976b77a247cc83a2824d5f995c14d5ffbb2aeaba1daaacea0e` 均无fatal。v3 canonical `835e6a15c0be10ffcf14847b071c31076aaa5a2efbb8e8e8e3723d64958943fd` 另实际全文读后确认。
- v4独立作者先冻Exact `dfe2def5608363c3615f1d2eb7085e6b30598196f746b112e9fc28f5e52ef7f5`，见 [双射陈述](../../../history/source/notes/unrelated_machines/coordinate_slice_bijection_exact_source.md)。两位未看作者/root新证明的研究者只据Exact分别冻重构 `53aab5e16266c8b8d8b335906bb1272493025728ef4c03b2f1b4b44aa5823346`（[第一独立稿](../../../history/source/notes/unrelated_machines/coordinate_slice_bijection_independent_source.md)）和 `77d6670e58f2689b0644160e968eddc02e2cf982072ed80e87b8d346e1f0a8f5`（[第二独立稿](../../../history/source/notes/unrelated_machines/coordinate_slice_bijection_second_independent_source.md)）。后者仅读v4就自足重构共同P及strict iff，未读v1 proof。
- v4作者proof `fe099722b7e9fe110ce471925ab9ca3a35b1d9b4d57aff5164436157dbf9fc44` 与root另冻的GF/配置proof `49eb8841c737e69ed09d804f3964a8e072553333ca2bee9cfbdcf9630fffe976` 使用不同计数常数。root见过作者思路，独立推导冻结在实际读作者全文前，不冒称Exact盲审。第一位随后实际读两稿，读后回执 `177345f2de7e679f1c3a068ac5a19023abff159d1f35a6e20110d3cebe910ec7`，无fatal。
- 最终canonical SHA256 `c0fc1e637c6cac96c4809bfa7e27113f8383556a8301037501ddcfe8891cfacc`，由v1/v3独立审查者和v4第一位Exact-first审查者分别实际核hash并全文读后；均确认无承重誊写遗漏。第二位v4审查者随后实际读作者proof及finalcanonical的H–K/共同P/strict iff，读后回执SHA256 `0b71b6a4a23ce23756b323fde15c1bfddfcc36a0d00f9ce14ddf29d26c705a10`，无fatal；明确不冒审未负责的v3 padding或代码。root随后也全文读作者proof，复核不同列表计数/尾界和全部配置覆盖，无尚成立异议。

### 承重攻击与否定范围

simple、Dregular、公共字母表、完整坐标顺序和逐state单射均按定义核对。port下传当且仅当子边在所选根子树；未选节点不存在单位入边，其全部D个小任务留父恰1，不能只算active树。strict≤1的归纳不假设其他states为空；不同投影坐标的两完整切片必交，故反向确给fullLC。网格只把已经证明的OPT>1升为≥1+1/D，未用有限最优求解。

padding颜色是坐标**名**，right邻居index才是坐标**值**；所有新左符号都走新投影行。proper coloring使每个新右token至多收费一边；parallel会破坏这步，未免费使用cover重接来消parallel。padding统一位poly不使后续D^Q树展开变uniformpoly。

双射H的NO同时量化全部cheap lists，ordinary覆盖跨edge独立；planted0覆盖单独充右token。root生成函数与两位独立者的不同列表计数/尾界均闭合。每seed的实际C上界与CONFIG1，goodNO的精确OPT，以及H仅概率存在性三层不混。每个资源恰Q枚eligible叶port靠双射计数，并非默认每neighbor只有一枚；这正是J证书的关键。

### 实际代码与有限核验

独立小审计 [代码](../../../tests/audits/unrelated_machines/coordinate_slice_physical_configuration_audit.py) SHA256 `4b68ff34425627028be293ee597774d76aa30aeee3529648633f49643ece89fd`；root全文读后原字节复制、亲自复跑，stdout解析后与作者冻结输出完全一致。[新冻结输出](../../../evidence/runs/unrelated_machines/coordinate_slice_physical_configuration_audit.json) SHA256 `3d5203005914cf8f1432f48b3d9d4ba7f985d435d8b155dc33a464150d297619`。

核了全部16个D2Q3 conditioned permutation arrays（各58机86任务132配置）与1个D3Q4（723机1443任务1932配置）。逐任务有限边、实际sigma全部机器、每个真实配置负载、每job覆盖恰1、每机配置权恰1均用Fraction检查。它们不满足H的NO常数；没有检验cheap-list NO、没有运行原OPT oracle，不把3/2或4/3的显式sigma值称为这些小例精确OPT。

本节限定证明与实际内审完成，implementation=audit_only；没有新增随机源NO判别器或一般UM算法。外审/新颖性未认证；该编译失败不否定一般q-hardness或UM-TARGET-v1。
