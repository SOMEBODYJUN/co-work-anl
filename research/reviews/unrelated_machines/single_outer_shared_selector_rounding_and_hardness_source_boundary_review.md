# 单外层完整 flat 的两种输入合同与实际审查

2026-10-18，boss11。当前374行正文SHA256 `8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221`；只有两个正式结果：给定 primitive-SA1 点的 epsilon²/4 舍入，以及只输入 typed Q 的11次普通LP查询13/8算法。软件实现均为 none，标准有理LP只作已付费的数学算法规格。

## 实际顺序与独立性

旧 Exact 736405…先给6.1-sol审者，其独立重构419df2…先冻结；root实际完整读该记录后才释放作者166行Proof da4897…。审者实际全文读后另冻5c1f16…；root实际完整读Proof与该记录。旧uniform-winner/count-DP、审者独立CDF后端分开；其32小例代码不等于作者count-DP实现。本资产不复制该未由root阅读/重放的代码，不登记软件通过。

新 typed-Q-alone Exact 81b1c6…另先释放；审者已有旧阈值结果背景，不能算方向全盲。它先重构128-grid的独立13/8算法，冻结399c6b…；root实际全文读完后才释放root作者11-bisection Proof 2a6af6…。审者实际完整读后另冻206405…，具体核root的11查询算法，而不混称与自己128-grid实现相同。root也实际完整读新Proof与该记录，并用Fraction复核有理系数、511/65536及51/16384余量。

知情作者据此写916de8…中文自足正文，root实际全文读374行后只调整三处最终审查状态/链接用语，形成当前8c5fcf…；旧原稿保留于scratch，冻结数学来源不改。审者随后实际完整读当前header、身份表及§1–12，另冻81491b…；root实际完整读这份最终post-read和旧5c1f16…记录后才登记。最终复核不是新盲票，root作为共同作者也不算独立票；正文末尾review链接不是审者已打开目标review的证据。

## 数学覆盖

域只有一个outer，每个正home跨全部state索引互异且恰有一位own-singleton helper，fallback任意共享但与全部homes分离，无额外无home组。每个helper可以没有fallback。输入显式给结构，不声称任意P的识别器；空任务/OPT0不属于这个含unit selectors的特殊域，不缩小主目标原域。

完整ordinary OPT=2−V、每台private与资源load、全部未选state及显式零jobs的恢复均已核。singleton closure来自同一完整primitive/补lift，不用triple；所有packing行在同一个outer条件下。正marginal只除一次，零分支不除。第一合同给epsilon²/4真实全组值；第二合同独立用CDF-max的严格5/8福利、固定有理线q=(13/8)epsilon−10/8+1/256及11次查询。

FAIL仅为普通有理LP的精确不可行，故V<epsilon；feasible下端l可能大于V，搜索只保V<=h。q<=0分支用完整load2基线，q>0分支回填所有原jobs。所有11次阈值位长为常数，不用分母格点、未知OPT或exact SDP oracle。NP-source推论只排该明确typed结构的真实YES OPT1 / NO>=2−delta（固定0<delta<3/8）在相应P!=NP假设下的归约。

## 已有工具、同步后的比较与未解范围

福利的独立state选择、逐资源最大系数及有限CDF条件期望属于标准工具；同期已入库的[门控菜单正文](../../current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md)明确将该工具归于DNS。root同步后实际全文读该191行正文；其矩阵多了pin/connectors/gates，目标是组数与质量的平衡值beta，并非本页每组都必须选state的原flat。两个13/8不能互相套用，也不把新门控class的算法算作本页旧review已读过的背景。本文扣除已有福利工具后只保存具体singleton同点闭包、一次条件packing与完整typed all-jobs算法合同；不认证新颖性或独立成文价值。

多个outer之间的共同fallback容量尚未由这些逐次条件点支付；没有home的辅助组也不能自动回填。本结果不是一般UM改善或困难性。当前精确域无standing fatal；外审、全局新颖性、端到端有理LP软件均未记录。UM-TARGET-v1及其反面仍OPEN。

## 冻结来源

| 来源 | Container SHA256 | Original SHA256 | 包装 |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/one_outer_full_primitive_sa1_rounding_exact_v1.md | 7364055e2c13a8962b5a022f959721014fb6219465dbe0340676521ac9437eac | 7364055e2c13a8962b5a022f959721014fb6219465dbe0340676521ac9437eac | original bytes |
| history/source/notes/unrelated_machines/sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md | da4897a966e8b5e10299622c5f93d67b115f859d1ae8fc77bd29f8f7ce0aa571 | da4897a966e8b5e10299622c5f93d67b115f859d1ae8fc77bd29f8f7ce0aa571 | original bytes |
| history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_exact_first_reconstruction.md | 419df2115facfc2b8cbd976d7f3a3a94fed2dc707ab915f34be10f5d19c8ca94 | 419df2115facfc2b8cbd976d7f3a3a94fed2dc707ab915f34be10f5d19c8ca94 | original bytes |
| history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_author_read_after.md | 5c1f16cee1d7a1825e7a65552ca5fdab2fca0e8f193fed6c990fe5a92ae986ff | 5c1f16cee1d7a1825e7a65552ca5fdab2fca0e8f193fed6c990fe5a92ae986ff | original bytes |
| history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_approximation_exact_v2.md | 81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69 | 81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69 | original bytes |
| history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_author_proof_v2.md | 2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf | 2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf | original bytes |
| history/source/notes/unrelated_machines/sol_one_outer_13_8_exact_first_reconstruction.md | 399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f | 399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f | original bytes |
| history/source/notes/unrelated_machines/sol_one_outer_13_8_author_read_after.md | 2064056e2cbd657f45238b0249516558472a3567568074b4aedba3e5c3bf88d9 | 2064056e2cbd657f45238b0249516558472a3567568074b4aedba3e5c3bf88d9 | original bytes |
| history/source/notes/unrelated_machines/sol_single_outer_canonical_final_post_read_v2.md | 81491b420b5054782a48e085109ddc510b03780d473cbbc84aa6e783acdb6eb9 | 81491b420b5054782a48e085109ddc510b03780d473cbbc84aa6e783acdb6eb9 | original bytes |
