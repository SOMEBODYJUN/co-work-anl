# 阈值叶 Hall、共同边际投影与趋二间隙的实际审查

2026-10-18，boss11。新 Claim：`UM-THRESHOLD-LEAF-HALL-CONSISTENT-MARGINALS-PATH-PROJECTION-GAP-v1`。当前全文 SHA256 `1dd80c98ea677ed136e7dcea24463304f1e68e2b69aef658337b41866b6c9469`，338行；原前101行/13813bytes SHA256 `be1a7aa42674347045ebef10f78875bf68b0af2011ec6c51c03a2f568af85833` 逐字节不变。旧 v3 Claim、旧审查和旧来源不改写、不升级；本次新身份只覆盖新增§8–11。

## 真实读取顺序

6.1-sol 审者先仅收到弱合同 Exact v2（828c6a…），独立重构冻结 f5e2bb…；root实际完整读记录后才释放作者 Proof（357c76…）。实际全文读后另冻 ca41d9…；root实际完整读作者证明及该记录。弱合同的每状态单整数 matching witness 没有被转为强化合同的 witness。

root随后提出新(MC)对象，冻结 Exact v3（34244f…）和运输作者 Proof（730c5e…）。审者此前熟悉弱证明，明确不是新盲票；只看新 Exact 条款先独立重构，冻结783e27…；root实际完整读后才释放新Proof。审者实际完整读后另冻4cd8ac…；root亦实际完整读新Proof与该记录。两种有效运输完成（作者greedy、审者proportional）均核零lambda、beta=1和非邻居。

最终中文338行正文1dd80c…由审者实际一次完整读原header与§1–11，冻结5a526f…；root实际全文读该2452-token记录，实际读旧101行及新增正文/精确差分并比对旧前缀后才登记。最终审查不是新盲票，也不代签未打开的历史链接或作者代码。root是共同推导者，不记独立票。

## 数学范围

阈值 unit-demand 的严格 b<epsilon 判别；指定partition的逐点投影；新D_+只列positive邻居、旧D还列zero-only邻居；完整originaljobs和零值端均明确。运输只共享同一套叶边边际，不共享所有core状态与完整matching的共同law。弱条件可用单matching，MC条件一般必须混合。自动消去全部叶的版本须所有原组均非阈值unit-demand；不能换partition沿用等式。q_t含unit core系数，但parking tail真为一，不是趋零伪尾巴。

精确V=1/t与完整ordinary OPT=2-1/t、180机201job的t2例和总位复杂度已检查。有限审计只核其明确fixtures，不能作一般证明。标准有理LP可生成/拒绝这些有限显式系统；没有exact SDP oracle或一般调度finder。

## 软件实际重放

root实际完整读取两套独立stdlib/Fraction脚本，在两个新空目录调用、逐个断言执行，并程序比对冻结JSON。弱版语义相同；MC版输出字节完全相同。程序的输出文件名固定、相对于cwd；请在新空目录执行下列绝对脚本路径，避免覆盖任何冻结输出。原作者checker及其735等计数没有被root实读/运行，本资产不据此认证，亦不复制无关作者大统计。

- `tests/audits/unrelated_machines/conditional_leaf_hall_path_projection_independent.py`；代码SHA a27da8f52dc4fbe2bf719214c1d38ea2fbc75d3ef0a310fcb75b54bb0457fc38；输出在cwd为 `sol_conditional_leaf_hall_independent_audit.json`，与 `evidence/runs/unrelated_machines/conditional_leaf_hall_path_projection_independent.json` 比较。
- `tests/audits/unrelated_machines/conditional_leaf_consistent_marginals_independent.py`；代码SHA d4b8a93458e584057108414aa0d883a0ea16423f255beab627aa45abed8c5e71；输出在cwd为 `sol_conditional_leaf_consistent_marginals_independent_audit.json`，与 `evidence/runs/unrelated_machines/conditional_leaf_consistent_marginals_independent.json` 比较。

弱版核完整t2矩阵和partial-z/零lambda/zero jobs；MC版核t2的1360条边际等式、全部条件行列与176个完整matching混合片段，并另核beta=1等退化。详见root replay scope。无一般LP后端实现，不能把finite verification变成全称定理。

## 状态与反面目标的关系

限定证明完整，独立重构、作者读后、最终全文审查及精确重放已完成；无standing fatal针对当前精确合同。外审与全球新颖性未认证。路径思想来自既有BCG2009，扣除既有配置gap后，新增是精确阈值消元、全部perspective条件、共同叶边际仍逐点退回basic的运输机制及其准确失效范围。不是近二计算困难性，不是实际YES反例，不排更强共享selector条件/共同law/高阶PSD。UM-TARGET-v1及其反面均未因此关闭。

## 冻结原件

| 来源 | Container SHA256 | Original SHA256 | 包装 |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_exact_v2.md | 828c6a178729bf4ce03855ef8e1f53d9efaf85fb9aaa680a6cd4c5a0e012bb4f | 828c6a178729bf4ce03855ef8e1f53d9efaf85fb9aaa680a6cd4c5a0e012bb4f | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_proof.md | 357c762c9481183dd3f0f5fdf9631beddad931bb80977e753287d6bf662d73e6 | 357c762c9481183dd3f0f5fdf9631beddad931bb80977e753287d6bf662d73e6 | original bytes |
| history/source/notes/unrelated_machines/sol_conditional_leaf_hall_exact_first_review.md | f5e2bbfc15066eff1969a8a91106d92c22103c1c245b80f65eda365e85518812 | f5e2bbfc15066eff1969a8a91106d92c22103c1c245b80f65eda365e85518812 | original bytes |
| history/source/notes/unrelated_machines/sol_conditional_leaf_hall_author_read_after.md | ca41d9f2bde78ceee5a2905ad00ac3ee871467ecfcdc909aa16c2c85d47264f5 | ca41d9f2bde78ceee5a2905ad00ac3ee871467ecfcdc909aa16c2c85d47264f5 | original bytes |
| history/source/notes/unrelated_machines/conditional_leaf_hall_consistent_marginals_exact_v3.md | 34244f9737bbbe7baa858482d31f8154f0e4146be0f1464c9e0598a402bfb38b | 34244f9737bbbe7baa858482d31f8154f0e4146be0f1464c9e0598a402bfb38b | original bytes |
| history/source/notes/unrelated_machines/conditional_leaf_hall_consistent_marginals_author_proof_v3.md | 730c5ef3af3861f123466d7e561111b363f5effb51c839efc0d6d284591d14c9 | 730c5ef3af3861f123466d7e561111b363f5effb51c839efc0d6d284591d14c9 | original bytes |
| history/source/notes/unrelated_machines/sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md | 783e27cbc45db0421164d2953d48c47ee66a8c0969210e399a9adb91fbf7e0cf | 783e27cbc45db0421164d2953d48c47ee66a8c0969210e399a9adb91fbf7e0cf | original bytes |
| history/source/notes/unrelated_machines/sol_conditional_leaf_hall_consistent_marginals_author_read_after.md | 4cd8ac153a7532edd5e97a4009e741c2c7142827b7b5f93b96a984da323dff41 | 4cd8ac153a7532edd5e97a4009e741c2c7142827b7b5f93b96a984da323dff41 | original bytes |
| history/source/notes/unrelated_machines/sol_conditional_leaf_hall_final_canonical_review.md | 5a526fd69b8174218796e674e3f378cd1c6bd7f52ced120dad1121ffd168731b | 5a526fd69b8174218796e674e3f378cd1c6bd7f52ced120dad1121ffd168731b | original bytes |
