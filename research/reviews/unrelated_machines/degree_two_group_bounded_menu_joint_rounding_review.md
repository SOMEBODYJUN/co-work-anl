# 两组资源加权菜单联合舍入：实际数学与来源审查

Claim：`UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`，2026-10-18，boss11。

rainbow提出group平均接degree2 additive MaxMin；root独立核后提出相对真实OPT加强与所有state bonus导出的保OPT归一化，作者再独立核后另冻v2。general仅先读新Exact和primary PDF §5.1，独立完整构证，先冻结后才读作者Proof，再实际通读root自足canonical。root亲读Exact、作者Proof、两实际审查和canonical组合，并独立核OPT2分支、所有原job恢复及bonus两向保OPT。

唯一外部近似算法为已存VW2010v1 Theorem12，PDF10–11/印9–10。root实际提取并读定义、preassignment、Lemma11、定理和证明；general/fee亦核原PDF图像。原字节SHA2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a。辅助玩家是group，不是state：每item正值玩家≤2、异值允许、degree1 bonus允许、zero edges可删；条件全部真实满足。不是新SC近似算法，扣除原定理后是group平均+实际UM/XOS+精确保OPT的直接结构推论。

Exact-first、作者读后和最终组合均无standing fatal。特别OPT2不能用资源独占而须单独证V0；empty states/W0/zero jobs仍保留；phase oracle成功只给T/2不判T可行，二分不假定接受谓词单调；2SAT只禁跨组正support冲突。canonical数学最终hash为 `41ceb9e9bdbe2fe81705d2c4f8b64c23983beba2f9767ec97ad36db4eba97e18`。当前数学审查不认证后来软件实现；代码/有限用例将单列实际核验，不回写冻结数学记录。外审、新颖性未认证；旧DGR比较不是新算法前提，本次不重认证；主目标未解。

| 数学原字节来源 | SHA256 |
|---|---|
| `history/source/notes/unrelated_machines/low_group_degree_bounded_menu_joint_rounding_exact.md` | `413a04f85b8e6886d205f1cf9b9e774b8022b6b02970ae0ad144512d68398998` |
| `history/source/notes/unrelated_machines/low_group_degree_bounded_menu_joint_rounding_v2_exact.md` | `7435885c698e741f0dc762cd1fc79be270ad7de164859477645b37affbd9a298` |
| `history/source/notes/unrelated_machines/low_group_degree_bounded_menu_joint_rounding_v2_proof.md` | `d90349f902c63d9d7814661c5a118e17811c951a669422bfdda8ab07d26437ec` |
| `history/source/notes/unrelated_machines/low_group_degree_bounded_menu_joint_rounding_v2_independent_review.md` | `c02dbb9c9735ab6d816b3de4ea210b60824095ad9d941f5649fd5dc9917a173e` |
| `history/source/notes/unrelated_machines/low_group_degree_bounded_menu_joint_rounding_v2_author_read_after_review.md` | `504cbaf20bfae19b0d3385fefff9dd0ab9e896bcac69c604eae4131e67640039` |
| `history/source/notes/unrelated_machines/degree_two_group_bounded_menu_joint_rounding_canonical_read_after_v2.md` | `e9f6d03b9eb555827fb842b41d91e46457f4567a601d0267d02492d8e4cf89be` |
| `history/source/notes/unrelated_machines/vw2010_theorem12_backend_precheck.md` | `557ab3d25b7eadb9fc63bf64005586001b5a0523a7db9eca7b00464ffdf09d88` |


## 实际结构后端与root有限核验

后端位于`tests/audits/unrelated_machines/degree_two_weighted_menu_backend.py`，独立audit同目录`audit_degree_two_weighted_menu_backend.py`，输入`examples/unrelated_machines/weighted_menu_joint_fixtures.json`。核心独立实现published VW的forced-largest/迭代BFS与单向失败证书二分，再完整group平均/归一化/原jobs时刻输出；不输入OPT，不调brute。metadata分类audit_only，指该结构全链审计后端，不是general UM求解器。数学原审查不冒称看过后来的代码。

root亲读原core/audit，发现初始Python默认4300位decimal转换上限在合法5002位分母p处实际抛ValueError；current core显式解除该数值转换默认上限，实际大有理读写已通过，不按数值复制。原audit默认覆盖__file__旁输出，现改为必给--fixtures/--output-dir，创建目录exist_ok=False、结果文件open x，实际拒绝再次覆盖冻结。初始源码均无损gzip保留原字节，不为通过检查改原来源。

root实际执行当前audit，冻结`evidence/runs/unrelated_machines/degree_two_menu_joint_v2/`的两份运行；五例原OPT分别1、33/17、1、1、2，输出同值，归一化OPT均相等。原assignments总832、归一化24820，只在audit穷举；额外VW T2成功但真OPT1明确检查非精确oracle，1200-agent迭代环无递归。非法空G/degree3/浮点等按此Exact域拒绝。

root另完全不导入core/audit的矩阵构造或brute，从原JSON自行列全部原jobs/资格，穷举832份分配，逐项核输出29枚jobs的合法端、真实p、开始/结束、不重叠与完整峰，两条定量界均过。独立记录`root_independent_original_matrix_verification.json`保代码/输入/正文/冻结输出SHA、有限范围和覆盖拒绝。该有限回算不代一般证明。大数probe只测试5002位显式有理读写，不冒称运行同规模全二分或全输入穷举。

执行：`python3 tests/audits/unrelated_machines/audit_degree_two_weighted_menu_backend.py --fixtures examples/unrelated_machines/weighted_menu_joint_fixtures.json --output-dir <尚不存在的新目录>`。单个原结构输入可用核心CLI输出完整actual jobs；五fixture集合需先选择其中一例，不是把集合当单实例。


## 独立实际代码读后

general在冻结数学三份review后另行实际读当前core 416行、audit 220行和全部输入/原freeze，对SHA3ac389c7ab6bf1037c51d744d18e6191b5be8df1ba559e731fbbcaf4ebcc3c99与2a6b5b009ecedc417343fe42b44113aaf513b7e661756005fdd6738e71979a3d批准，无standing fatal。原字节审查`history/source/notes/unrelated_machines/degree_two_weighted_menu_actual_code_review.md`记录force两端扣除/后向queue、BFS/weak二分、bonus/全部原jobs及真实IO。它在新scratch目录重跑的两份JSON数学内容与root freeze相同，并核输出不可覆盖；扩展4681后端输入、140结构例、长链/环、5002位分母完整solve与CLI也实际通过。扩展数据属该审查者，不冒称root枚举；root亲读其实际报告，未复跑这些扩展，有限scope与一般证明分开。原数学记录/canonical哈希均未改。
