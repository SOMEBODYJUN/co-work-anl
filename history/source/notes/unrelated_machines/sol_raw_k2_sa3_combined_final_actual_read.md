# 最终组合新增 §13–14：知情 actual-full-read 与角色分工

记录者：`/root/sol_nsw_independent_attack`。本记录只审 parent 本次释放的最终新增两节，不重签旧 374 行。**§13 我是 Exact-first 独立重构者，随后读过作者 Proof；§14 我本人是作者，本次只能作作者一致性/准确性复核，不能独立认证自己的结果。** §14 的独立审查由 parent 另安排 identity 承担；我未读取他的审查记录，不代其签字。

## 1. 精确原件、实际完整阅读与字节范围

最终组合原件：

`/workspace/scratch/038d9dcc4cac/single_outer_flat_with_raw_k2_boundary_and_sa3_repair_final_v1.md`

- 实核 SHA-256：`404cf16df23cffe7b7c61c498907b744047473cf2d2db4e403630e5b6279edd2`。
- 实核 **48,840 bytes、702 行、0444**。
- 真正显示并逐行读完新增 **375–484、485–594、595–702**，含两空行、全部 §13/13.1–13.6、全部 §14/14.1–14.6 和最后新 review 链接；各次输出无截断。
- 初次 exec 因 transport disconnect 没有返回任何读取结果；随后重试成功，只有实际成功输出的三块计入上述范围。
- 对旧 1–374 行只做 byte/hash 统计，没有语义阅读或重签。当前 prefix 为 **25,741 bytes**，SHA `8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221`，与 parent 给出的旧 prefix 标识一致。我没有另开旧算法原件作历史版本逐字比较。

§14 最终正文 **559–700** 的 10,804 bytes，与我冻结的 standalone 文件逐 byte 相同，实核 SHA `8318d6558c31a6b4a85d48a31d86571af5016c3a8f4cabec155bab792e172f68`。701 为空行；702 是 parent 增加的新 review routing。此 byte 比较不代替本次已经完成的全文实际读取。

## 2. 真实审查链与不变的旧记录

§13 新18m族的真实次序是：已知旧14m背景 → 仅读新 Exact 76 行 → 独立重构并冻151行记录 → parent 实际读完才释放新122行 Author Proof → 我全文读后另冻70行记录 → 本次才读最终 canonical 新增两节。

| 已冻文件 | 实核仍为 SHA-256 | bytes / lines |
|---|---|---|
| `sol_general_repair_k2_local_law_independent_exact_first.md` | `8e3dbbf6ba04069eec67723c1d39458de0bb2e1d39f7776367aad76a58fb4412` | 10,311 / 151 |
| `sol_general_repair_k2_local_law_author_read_after.md` | `1ca2515b431457cb7301c26a325339e8a878ae51bd51ed99260f6fecb55903b1` | 7,271 / 70 |
| `sol_raw_sa3_to_canonical_sa1_exact_v1.md` | `9c2a180330eed2a9b5f5b35b07eb76e2b33ed7ff853bba7376cc06e060595b71` | 5,572 / 50 |
| `sol_raw_sa3_to_canonical_sa1_author_proof_v1.md` | `de3736cf6fd4d601c96f87f2c2af28e5b15bf62b25855b85134b761c6d0d0778` | 9,648 / 138 |

后两文件是我写的 S3 作者材料，不是我对别人的独立 PASS。没有修改任何旧冻结记录，也没有把新全局 literal lifts 追认进旧 raw K2 合同。

## 3. §13 知情 canonical 实审

正式 ID `UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1` 的表格 fields 与前置 Exact/Proof 同对象：每个有理 `0<c<1`，T=1+c、epsilon=1−c，完整18m17j34端，原全部 ordinary jobs 必执行；共同 degree4、全部 one-hot/Boolean、global M2、所有物理 raw-affine localizers、每机完整 local row law 相容，均同时要求。

396–423 行的菜单和全部 endpoint substitutions 与已审 Exact 一致。所有 listed coefficients 正；constant-0 assignment endpoints 仍保留，未删 job、未加 export≤activation guard。

425–458 行 global M2 两种证明均正确：七维正 pivots 与独立块分解一致；signed cube 的权为四个35、三个7和一个−1除160，三阶差分及 weighted Cauchy 常数608/7给16/35正下界。原596个 reduced quadratics 由 affine pullback 全部覆盖，不是只核局部 principal submatrix。

460–479 行的两个 raw slacks 是 `(1−b1)+c b2` 和 `b1+c(1−b3)`；全局 affine q 下 literal×q² 等于 quadratic square 的 L 值。其余 c 或 c 加 literal 的 slack 同样正。因此对全部参数的证明闭合，不需假定某份实际全局位分布。

481–514 行使用同一 positive one/two-bit marginal 构造各机 full law。两个 outer roots 的四配置、权、load=T 的边界配置均与独立重构一致。每 row 最多依赖两位、最多三个原 endpoints；所有本地 Boolean membership 条目都共享，而跨三位 global law 不存在。没有靠漏掉同机 triple 支撑这个新例。

516–546 行的全部17-job C1 witness 正确，unit selector 给实际 OPT≥1，故 actualOPT=1。两个 canonical 负式为−1/160、−c/160；其三个原因子位于三台不同机器。Activation localizer 只对明确 raw-affine q=b3 给出 physical degree≤4 的负值，没有把包含 canonical claims 的任意 affine test 免费降为 raw affine 或扩到未知六阶。

548–556 行的范围准确：有限 fixed-c audit 与全参数代数证明分开，旧14m缺少同机 triple 的局限保留；不升级旧证据，不声称实际 gap、反对改点/另求R或否定旧 typed 算法。文中关于 global triple 正性的排除，数学上是要求包含 `b1b2b3≥0` 的全局 triple-positive family；不是说添加任意一条与该负式无关的正 triple row 都会切点。

**§13 最终知情实读未发现 fatal。** 这延续先前 Exact-first 独立数学重构与 author-read-after 的限定结论，不是新的全盲审，也不是软件独立认证。

## 4. §14 作者最终一致性复核（非独立 PASS）

正式 ID `UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1` 在559–568行给出完整正式 fields。Source 适用一般 normalized-flat 输入，阈值 `1≤T<2`、epsilon∈(0,1]；它只保证每给定共同 rational 点的 product pullback 为完整 plain-SA1，PSD 部分只对同一点给定 rawM2 保 canonicalM1。

570–615 行定义完整 all-finite-endpoint S3 和目标 R。所有原 boxes/raw machine slacks/**unit resource cap1** 都乘≤3原 literals；原 Boolean 和 job one-hot 乘至 degree4。Zero/inactive/indexed objects 全保；cap1 与 T-cap 分列。Canonical F 的所用 raw entries 不改，但没有声称 canonical claim first 与原 export first 相同。

617–679 行的每个 positive-row 义务均在本文付清：真实 Dirac 点必要性/soundFAIL；长度≤4 cylinder 正性；`1−aE=(1−a)+a(1−E)` 的正展开；claim Boolean defect 的 degree2/1 multipliers；group one-hot；全部 gate/boxes；resource slack 的 cap1+inactive-claim 分解；quality `a_s h_s≡Σp a_sE−epsilon a_s` 的 exact normalized 身份。Quality private-end identity 的 multiplier≤3，Boolean multiplier≤2，source row 的 literal multiplier≤3，全部总次数≤4。W 可来自任意 group/state，使用同一个 L。

681–698 行的 rawM2→canonicalM1 由 affine canonical test pullback 为 raw quadratic，未带入 PSD finder。S3 是固定次数 rational LP；moments 的[0,1]界给 reduced bounded polytope，vertex/Cramer/Hadamard 控 witness bitlength，普通 rational LP 求解和已给点的条目提取均 total-bit polynomial。无概率/最小正系数/epsilon 倒数枚举，未声称可找到 optional exact PSD rational point。

700 行明确 S3 可独立作 source，或在已给 raw K2 上额外核验这些 lifts；不把两系统作包含关系，不称层数最小/锐或每 row 必要，也不给全 groups rounding/general UM result。Software none 与作者稿一致。

这些是**作者对自己最终文本的实际一致性和正确性核对**。我不把它包装为“本 agent 独立认证 §14”；parent/identity 的独立记录须另列。我未读取 identity 的新 Exact-first/读后 records，也没有据其 hash 代签。

## 5. Links、软件与最终签署范围

702行新链接字面目标为 `../../reviews/unrelated_machines/raw_k2_canonical_pullback_and_sa3_repair_review.md`，在 article 的常规 current/unrelated_machines 路由下指向对应 review 目录。未打开该链接、未读待注册 repo 新 canonical/metadata，所以不认证目标文件当前实体或审查账内容。

§13 的作者程序、249行代码和四次 CLI 工作由 parent 报告并实做。我没有读取或运行 code/run；此记录不替 parent 的实际代码阅读、default stdout 比较或附加参数 summary-projection 比较签字。特别没有声称所有参数原 stdout 相同。§14 的 implementation/checker/run 为 none；其一般证明不由§13有限程序补签。

**最终结论：对精确404cf…原件，我已实际全文读完新增375–702。§13在已独立重构后的知情最终复核无fatal；§14完成作者最终一致性复核，独立审查职责在其他 reviewer。旧374行算法范围不重签、不升级，所有旧冻结记录不改。** 本记录不能被登记成“同一 agent 独立审通过两节”。全球新颖性未认证；一般 UM 主目标仍 OPEN。
