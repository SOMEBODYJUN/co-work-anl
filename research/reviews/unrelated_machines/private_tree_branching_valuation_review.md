# 私有分叉树估值、包络与支持LP的实际独立攻击

审查对象：UM-PRIVATE-TREE-Q-VALUATION-v1、UM-TREE-Q-XOS-ENVELOPE-v1、UM-TREE-Q-MINORANT-LP-v1。完整精确陈述和自足证明见[现行正文](../../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)。本记录是内部审查，不是外审或新颖性认证。

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
