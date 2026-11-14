# M-b233 同源折扣闭包审读

审读对象：`M-b233ef00a9c34e189817cdfb7a495107`（`archives/customer-attraction/state/引理/同源真实末回复的折扣闭包与二状态精确投影--引理.md`，registration pin `308401b736d5e278edb8a86a3dbfd2d3466aa1455f9c627b8b72069a9197c411`）。本包按任务声明逐一核对 17 个 reading refs 的 SHA 和全文字节；两个 1.45MB 级必要 LP 通过有理 JSON 全量解析，公式/脚本/独立核验器逐段读取。

## 模型、量词与完整结论

共同模型是有限单位客户、有限非空带标签共同目录 `S`，覆盖映射可重复且可为空；提供者按固定顺序观察全部有序历史各行动一次，完整纯 SPE 在每个合法有序历史对全部合法偏离沿同一完整策略的真实后继满足弱 IC。保留重复主题、同覆盖异标签、空标签、零客户和弱平局。`OPT_m` 是恰 `m` 个标签的最大并集，福利为各客户在覆盖者间均分之和；合法背景剩余利润和根福利不混用。

固定同一真实源 `h`、余 `k>=2`、强制当前合法标签 `T`、同一策略真末回复 `C(T)`，中间 `k-2` 位按同价 `alpha_mid,beta_mid` 计数 `s`，末位按 `alpha_last,beta_last` 计数 `c`。固定查询菜单后再对当前 `T` 取辅助最大值；查询权、源权、价格和容量权均非负，源权 `a0` 可为零，且 `0<=theta<1`。正文逐项把源 IC、真实后继实际末价、共同 `K=max|S|` 容量以及同一真末回复的全部查询 IC 合为

`B = a0*r + ((k-2)*alpha_mid+alpha_last)*u_m + ((k-2)*beta_mid+beta_last)*K`

和客户局部代价 `H_x(t,c,s)`。因此每个合法 `T` 有 `B >= sum_x H_x(1_T(x),1_C(T)(x),s_T(x))`。若局部势满足 `V_x(t)-theta*V_x(c) <= H_x(t,c,s)` 对四种 `t,c` 和全部 `s`，有限共同目录中取 `sum_x V_x(1_T(x))` 最大的合法 `T*`，因为 `C(T*)` 仍在同目录，得到完整结论

`B >= (1-theta) * sum_x V_x(1_T0(x))`

对每个合法种子 `T0`。这一步是有限最大值闭包，未把辅助势当真实玩家效用，也未假设最优主题在循环上。逐客户 Bellman 收缩 `e_tc=min_s H_x(t,c,s)` 只有三个不同有理候选；所有输入有理时结果有理。`k=2` 且源权 `a0=M` 时四边平衡，二循环候选夹在另两者之间，固定有限质量输入的整段 `theta` 最小值可精确检查有理折点。

## 已复用的逻辑边

本包没有新造同义边。直接复用已发布并已绑定的 canonical edge：

- `boss2-six-cross-portfolio-to-discounted-closure`（`map/edges/customer-attraction-boss2-six-cross-20261111/boss2-six-cross-portfolio-to-discounted-closure.json`）。共享组合查询引理先把同一真末回复的源/实际末价/`K` 预算合账，当前对象再以有限目录最大值闭包和二状态 Bellman 精确消元；方向是共享组合投影 `=>` 同源折扣闭包。条件是同一源、同一完整策略、固定菜单/种子、所有回复仍为共同目录合法标签、非负权及 `theta<1`；不允许不同离轨源免费合账。此边的 `contribution` 已明确：一般折扣闭包、三候选消元和平衡权连续有限化由本对象给出；5716/5727 数值证书另由有限证据承担。

该 edge 的文件 SHA 为 `1fa592e9dbaf65520f5a235adf6731c77ef3707006718199d09b741454b800bd`。本包将其作为 unchanged canonical asset 复用，未复制或修改数学文本。共同定义 `CAG-MODEL` 仅提供模型背景，不能作为 hub 边；没有因共享定义另造关系。

## 5716 精确证书

`master_cuts/merged_5716_exact.json`（SHA `c86ea061c22ce1ece9df4955a9861a80935cabe1f293ecb8d62e4c0b17e0caf0`）是 4849 列、5716 条必要行的精确有理可行点，`W=0.4900905644294647...<1/2`；不是完整 SPE。`new5716_joint_discounted.json`（SHA `2f8cbc1f34b3746e46d549fd348c547792873a459632626da0c156cd10c98b6a`）在 120 个（5 个源、两个种子位、三轨道、四个采样 `theta`）全非负乘子 LP 中保存 6 条精确负行：

- 源 2、member 0、轨道 `(1,1)`、`theta=0`，slack `-1.2091146756783306e-5`；这是普通单步 portfolio 更新，不是折扣循环。
- 源 5、member 1、轨道 `(0,0)`、`theta=3/4`，slack `-3.2542921103115166e-4`。
- 源 5、member 1、轨道 `(0,0)`、`theta=9/10`，slack `-6.538855700339799e-5`。
- 源 5、member 1、轨道 `(1,0)`、`theta=3/4`，slack `-3.3866612587990074e-4`；这是固定最强参数的最负行，完整有理 slack 及 4849 列 row SHA 保存在 `certificate-summary.json`。
- 源 5、member 1、轨道 `(1,0)`、`theta=9/10`，slack `-1.0265807809888603e-4`。
- 源 5、member 1、轨道 `(1,1)`、`theta=3/4`，slack `-1.0274379924671345e-4`。

`main_verify_discounted.json` 是独立字面索引/中间位/四策略 Fraction 重建，`status=PASS`；`discounted_audit_and_finite_depth.json` 以另一套 Cramer/轨道枚举重建 6 行，`all_passed=true`。在固定最强参数、非对角 `(1,0)`、`theta=3/4` 的有限截断族中，深度 1--17 均非负，首次负值为深度 18；这只对固定参数与截断族成立，不能说所有较浅策略或所有权重都失败。

## 5727 精确证书及失败边界

`master_cuts/dynamic_5727_exact.json`（SHA `6ce39057d1ac4e81c2794ba7214e67349b2c004c1ec479a28fb39c5b3cec0ba`）是 5727 行必要系统，`W=0.4901508813179543...<1/2`。`new5727_single_portfolio_cut.json`（SHA `875e9f3192f5c0f7202ba1e40d63b8d3dde42534e30de62f3bb850178650d98a`）只保留一条负行：源 2、member 0、轨道 `(1,1)`、`theta=0`，slack约 `-4.6888704511e-6`；`main_verify_portfolio_5727.json` 独立重建 `status=PASS`。因此 5727 的新增分离是普通单步组合权重更新，不是正折扣带来的新行。

`continuous_discount_5727.json`（SHA `9af6b1cd7054e7caf112466c11f087b9c85415ea49e7cdd15c5e2e1c8ee790b1`）精确检查固定平衡族（`k=2, a=M=1`、A6 权 `1/4`、六个旧 `C` 各 `1/8`、末价 `3/8`、容量 `1/64`）的整段 `theta in [0,1]`。六个 R/Z 轨道-种子位的最小值都在 `theta=3/4` 取得；R 的 member 0 最小余量依次约 `0.00278118,0.00326707,0.00526834`，member 1 三项为 0，Z 同样非负。因此“加密固定折扣网格”不能再切 5727 点；该结果不覆盖重新优化权、非平衡源权、额外查询、第二枝共享身份或其他输入点。

## whole / contribution / remaining 的边界

`boss2-six-cross-portfolio-to-discounted-closure` 的 whole result 是一般同源折扣闭包、三候选 Bellman 消元及平衡权连续折点有限化；这是在其明确共同模型、同源、固定菜单和非负权条件下的完整关系。5716 六条负行和 5727 一条 `theta=0` 行属于绑定 SHA 的有限必要行贡献，不是该一般定理的反例，也不能把 `W<1/2` 的必要 LP 点说成完整 SPE 反例。`certificate-summary.json` 仅保存可审计的精确证书摘要与独立 PASS 标记。

剩余义务是：六人全局 `2W>=OPT_6` 的统一共同付款/完整 SPE 实现仍未完成；任意有限必要 LP 点不自动给全目录完整策略；120 点扫描不证明四状态或全部参数锥冗余；`theta=1` 只是连续极限；不平衡源权、不同中间价、动态改变 seed 查询、互斥源合账和跨枝共同运输仍需各自付款或证明。5727 固定平衡整段非分离也不能排除重新优化后的其他查询族。

## deferred candidates 的处置

任务定义里的 `CAG-MODEL` 与共享组合查询对象列在 `deferred_candidate_ids`，但没有 `overlap_comparisons` 中的 `status=follow-up` 对；共享对象已作为直接 canonical source 读完并复用上面的 edge，`CAG-MODEL` 只作共同定义背景。因此本包准确填写 `closed_overlaps=[]`、`follow_up_tasks=[]`，不虚构后续任务，也不把共享定义升级成逻辑 hub。
