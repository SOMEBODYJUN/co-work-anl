> **实质纠错（2026-10-18）：旧§F与本记录旧“未覆盖gamma<=delta_q”解读已撤回。高端上限gamma_hi对应低端下限1−gamma_hi，不能混为同一比例。下文旧记录按历史保留，新的准确范围和实际定向审查在末尾；旧PASS未抓出这处错误。**

# 显式XOS分数NSW与同组修复边界：实际审查、来源和版本

2026-10-18，boss11。正式首次ID为 UM-FRACTIONAL-BENCHMARK-REMATCHING-v1、UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1、UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1。当前正文SHA256 2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81。

## 真实审查顺序

旧v1/v2/v3 Exact与rank的Exact-only记录逐版保存；其一般SA数值链的反驳没有被撤销或改写为PASS。v4/v5 coauthor记录只是熟悉工具者验证与提案来源，明确不是完整NSW作者Proof或新盲审。不存在可由本轮追认的旧v4完整NSW作者Proof。

新6.1-sol独立审者只收到冻结Exact v5（3160d7…），先独立重构并冻结a90086…；root实际全文读完该记录，才释放已冻结完整作者Proof v5（298935…）。审者实际完整读后冻结d70dcc…；root又实际全文读完整作者Proof及该read-after。作者Proof编写者事前读过已冻Exact-first及工具，属于informed author，非独立票。

最终中文正文首次版本a12af1…经审者四块全文读取；指出唯一非fatal省略后，root在行394显式补充所有i不属于A''时Ti为空。旧字节保留。审者不是只看hash，而把当前2365f5…版651行再以1–220、221–440、441–651完整实际读取，重构旧hash核唯一102bytes差分，冻结ba2e84…最终记录。root实际全文读完189行该记录后才登记。最终审查不是新的盲审，也不代签未打开的linked source/history。root作为co-developer实际全文读canonical基础版本及全部精确差分，不记blind。

嵌入的逆矩与局部网格DP各有真实Exact-first→作者Proof→actual read-after原件，root实际全文读取；它们只验证其独立合同，完整NSW常数由完整v5另审，不能从standalone PASS跳认。所有冻结原字节及旧反驳均列在下表，gzip只无损包裹，不改内容。

## 承重检查与范围

A：对所有分数残余族的上界、inactive零、真实H代表运输、Jensen、正匹配和总位复杂度。A不提供验证其全局假设的oracle。
B：全U真product singleton matching；固定0/±1 lift与objective无关的vertex位长；纯有理progress；support内CDF welfare；候选先固定再mask；原item唯一label；relative floor只在auxiliary候选权上；shifted inverse、误差总一DP；任意比较匹配的完整paths；sum-to-max的3及c+1的3均支付。最终1125000相对任意正分数benchmark，零正匹配分支真实OPT NSW=0。
C–F：原total-one states的positive-support FSLP benchmark一，rho=2^24；固定eta使少于eta*n组低于q_eta，非全组下界。同一n组、D共享singleton REPAIR只损失D坏组；NP结论要求另有指定promise-gap reduction。所有原selectors、incidences、未选states、zero jobs与unused machines留在完整普通UM矩阵中，makespan只到二和selected-root例外计数。

根本范围：C–D禁区 delta_q<=c_eta<eta<gamma，而条件需求树源解码在直接阈值delta_q处通常需要gamma<=delta_q；本页不覆盖后者。gamma可依赖固定target参数，不可推出gamma随输入n趋零。UM-TARGET-v1仍OPEN，无standing fatal针对当前精确合同；未实现软件、未外审、全球新颖性未认证。

## Primary事实与作者增量分开

原始PDF为arXiv:2309.04656v1，23页/326593bytes；arXiv页眉2023-09-09与PDF内2023-09-12分开，不冒2024 STOC排版。root实际针对性读§2.1–§2.5/Appendix B及相关solver/Thm17、19、20，渲染并看PDF12/13；不是整篇root全文认证。新英文作者全文读所供v1提取文本，未读PDF。独立审者实际读取的primary相关文本范围是229–768及1212–1346 splitlines，文本1391换行加23formfeeds计1414 splitlines；不是整篇全文。最终canonical审查未另打开PDF或链接。

原作的matching/splitting/iteration/rematching为继承模板；本页不把actual-integral-OPT结论直接换成fractional，A/B的全分数界、显式XOS确定性替换、数值合同在正文另证。root实际读最近结果比较报告，但未亲读其中每篇正式PDF；不以报告或下载宣称穷尽新颖性。标准LP/匹配与直接推论不认领原创，论文独立价值尚需外部比较。

## 冻结原件与hash

下列source可审计旧错误/新证明/真实读取次序；原始hash与container hash分列，gzip无损。source范围按以上各段，不把旧full author或旧review整本升级。

| Source | Container SHA256 | Original SHA256 | Role |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v1.md | 33e8a8ec34d17ed605bf4b752ff4210d1bc9a68a46c8f673dd05f384754d7948 | 33e8a8ec34d17ed605bf4b752ff4210d1bc9a68a46c8f673dd05f384754d7948 | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v1.md | b7f8fe124eed85643dda4e48251da3a794b2869b7b22128c55f899198774d5fa | b7f8fe124eed85643dda4e48251da3a794b2869b7b22128c55f899198774d5fa | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v2.md | 6acd2c44963d9312ade20efed5128048b81f35b8391b5bc09875ec60ed0205de | 6acd2c44963d9312ade20efed5128048b81f35b8391b5bc09875ec60ed0205de | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_review_v2.md | 63c9e78d49c4a0eee967c24a8cc535e5cbcaa3fa149cf4f8e6bde2f8be3235fc | 63c9e78d49c4a0eee967c24a8cc535e5cbcaa3fa149cf4f8e6bde2f8be3235fc | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v3.md | ee80af544eaa5f133efb426a38e8007f21c0ee85594c48e7feaacd5caacc5697 | ee80af544eaa5f133efb426a38e8007f21c0ee85594c48e7feaacd5caacc5697 | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v3.md | a605f5d0aeb5c82de251bf5d37867717da511635bfb5e093c9f6846514534d75 | a605f5d0aeb5c82de251bf5d37867717da511635bfb5e093c9f6846514534d75 | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v4.md.gz | 4b197101a7a2e1b5ea4ecb127a817c1e9ec0b9c37adea30d39dcd4eba6ea2d3e | de055b02aca6d3876628671638bd509c16a1716d052b489d265e2303d37c400a | lossless gzip |
| history/source/notes/unrelated_machines/fractional_rematching_extension_v4_coauthor_validation_and_provenance.md | c1c54165d2875ceb31b47b9406bfcc793488b4bef1bb45efc63c299f53840c3f | c1c54165d2875ceb31b47b9406bfcc793488b4bef1bb45efc63c299f53840c3f | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v5.md.gz | eaa34ed503e7e5c78e755ad8d11efb0a1de82edb622892a3faba188a3f614006 | 3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e | lossless gzip |
| history/source/notes/unrelated_machines/fractional_rematching_extension_v5_coauthor_validation_and_provenance.md | 8bd29ecf095d0f23541893381ee977321348901433a01de899ff2cee9bdc09e4 | 8bd29ecf095d0f23541893381ee977321348901433a01de899ff2cee9bdc09e4 | original bytes |
| history/source/notes/unrelated_machines/fractional_rematching_extension_author_proof_v5.md | 2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af | 2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af | original bytes |
| history/source/notes/unrelated_machines/sol_nsw_v5_exact_first_attack.md | a900867a462b030db5cb2556f68f992b89efce28936a5c2658b13aeb03d7d306 | a900867a462b030db5cb2556f68f992b89efce28936a5c2658b13aeb03d7d306 | original bytes |
| history/source/notes/unrelated_machines/sol_nsw_v5_author_read_after.md | d70dcc172cdaafaf32ba7cdc842d967d0e8289666fcf77d977a3a94506a0d1cb | d70dcc172cdaafaf32ba7cdc842d967d0e8289666fcf77d977a3a94506a0d1cb | original bytes |
| history/source/notes/unrelated_machines/sol_nsw_v5_canonical_full_review.md | ba2e84477f5ab1857b2dce5d61f3fc2c7651d6f0ac17ced051c06ec97ee662cf | ba2e84477f5ab1857b2dce5d61f3fc2c7651d6f0ac17ced051c06ec97ee662cf | original bytes |
| history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md | 148cfe5ba2f6da74d9ce178281310373a31a057db2cfb0811216a4f7332c5801 | 148cfe5ba2f6da74d9ce178281310373a31a057db2cfb0811216a4f7332c5801 | original bytes |
| history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md | 1c2649e6e1c85412c41ab30979d3f8dca6d2c2b205ac8e6419b7da14eb77b284 | 1c2649e6e1c85412c41ab30979d3f8dca6d2c2b205ac8e6419b7da14eb77b284 | original bytes |
| history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md | 891c56ecb28481957e93adb3e70e80ae946e152d440e901aebcdcb17421584c7 | 891c56ecb28481957e93adb3e70e80ae946e152d440e901aebcdcb17421584c7 | original bytes |
| history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_read_after_review_v1.md | 7130d51bf65187a75a80daad756bd04c55b8c26da6de4e8240e40ff1791db044 | 7130d51bf65187a75a80daad756bd04c55b8c26da6de4e8240e40ff1791db044 | original bytes |
| history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md | b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165 | b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165 | original bytes |
| history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_v1_independent_review.md | 25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633 | 25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633 | original bytes |
| history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md | 8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad | 8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad | original bytes |
| history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_v1_author_proof_read_after.md | 8e863fc1772ac2d7c32ea0fab83e2373b7d69f79f93b1646c6513f5bf8c87a59 | 8e863fc1772ac2d7c32ea0fab83e2373b7d69f79f93b1646c6513f5bf8c87a59 | original bytes |
| history/source/notes/unrelated_machines/explicit_xos_deterministic_nsw_primary_scope_audit_rainbow_v1.md | 892b17fd8dbb8051cc8c317c81cb76824722eea26f48c3a210a1e8f9427895f9 | 892b17fd8dbb8051cc8c317c81cb76824722eea26f48c3a210a1e8f9427895f9 | original bytes |
| history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1.pdf | 3ae5ff599f9c5cc367adc1923fdd571d342d967dc2d64e6ad5ff948f3905fc6d | 3ae5ff599f9c5cc367adc1923fdd571d342d967dc2d64e6ad5ff948f3905fc6d | original bytes |
| history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1_text.txt.gz | 38f1ef5071d4a3440556c8caacbe1282690c5f30b0b0aeed5fed5b33809b13eb | 10fb320d3a7aaccb3baf579b657b3bcfecd931c45133df3f14337ce1e94829fb | lossless gzip |

## 2026-10-18：高低比例互补的实质纠错与新身份

新ID `UM-NORMALIZED-ROBUST-HIGH-LOW-COMPLEMENT-v1`；该次冻结纠错正文648行 SHA256 `bfd9a2c452aff3d5ab1b5813b7afe9a2fb388196384efe686d4aa73356b29ae5`。旧完整651行2365f5…保真来源另列，旧Exact、作者Proof和raw最终审查均未改写。原A/B与C–D精确低端结论保留，撤回的是§F高/低gamma混用及“不覆盖典型gamma_hi<=delta_q”的解释；本次不把历史PASS追认为早已发现错误。

root独立核对集合互补后，审者实际读git还原旧header/完整F、全部diff及新header/C–F，未重新审A/B。冻结fc0f04…定向记录；root实际全文读完该1160-token记录才登记。新页只header和§F变化，删除了未完成审查的未来gated链接；不认证未知来源draft或未采用新构造。

原norm1显式菜单unit-FSLP可行；固定eta，q_eta=(2^24)^(-ceil(1/eta))，0<delta_q<=q_eta及0<=gamma_hi<=1−eta时，C的同一实际allocation有计数 #{g:quality_g>=delta_q}>gamma_hi*n。因此all-allocation高端robust NO不可能；其互补低端比例是1−gamma_hi。

双等号delta_q=q_eta、gamma_hi=1−eta也矛盾，原输出低端计数严格<eta*n。高端若用>delta_q，互补须用<=delta_q；仅依C.4第一项时需delta_q<q_eta，等号处若另证须明确引用C.2严格NSW，不作无依据符号交换。固定eta=1/2给q_eta=2^-48，所以0<gamma_hi<=delta_q<=2^-48属于被排除常数域；不能再报告未覆盖。

新解释不提供原flat全部selectors的统一负载改善，不给源hardness，不扩到不保FSLP/非归一化/隐式/多层内部对象。所有源假设、实际解码与一般UM正反目标继续开放。

| 新保真来源 | SHA256 |
| --- | --- |
| history/source/notes/unrelated_machines/explicit_xos_fractional_nsw_original_canonical_before_gamma_correction.md | 2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81 |
| history/source/notes/unrelated_machines/nsw_gamma_complement_correction_actual_read_after_review.md | fc0f0432c6a676f73696ac1aa845c323592bbda34068fa32452e0bc5da892644 |


## 2026-10-18 高低比例互补的定向纠错

原651行正文SHA2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81已按原字节另存history/source/notes/unrelated_machines/explicit_xos_fractional_nsw_original_canonical_before_gamma_correction.md。本次合并前实际审读版本SHA 214eb466e53629952d70b6c78a857af628dd5a523a01b64a372f06b686b9b6e0；只改header/§F解释，A/B及C–D原精确结论保留。本次未重新审A/B长证明。

source审者在独立高低参数重构后实际读现行header/C–F及差分、旧本review全文，明确要求撤回旧scope；root实际读其完整记录并在此落实。C.4的低组计数对应源高组上限的补数，因此delta<=q_eta、gamma_hi<=1−eta双等号也矛盾；不能再沿用“不覆盖典型gamma_hi<=delta”结论。新的短福利源判别及独立审查另见[门控福利审查](normalized_gated_menu_welfare_review.md)；该新页不重认领旧NSW算法。冻结旧Exact/Proof/raw reviews未倒改，历史PASS不追认为早已发现此错。


### 两份纠错的语义合并

同步双方都撤回同一个高低gamma混用，定量内容相同。本页保留双方真实审查顺序；当前旧NSW正文保留已单独登记UM-NORMALIZED-ROBUST-HIGH-LOW-COMPLEMENT-v1的那份纠错字节（bfd9a2c…），新gated算法及near-perfect源结论在独立自足正文，不借旧NSW审查认证。两份具体header/F措辞差异保真保存于nsw_parallel_gamma_correction_exact_comparison.diff.gz（gzip无损保留标准diff上下文空白）；没有删除任何数学结果或倒改冻结review。
