# Boss3 execution line journal

- Identity: Boss3 execution line, studio slot `informed-b`; session `boss3-20261118-live1`.
- RUN: `n6-boss3-20261118`; target: `customer-attraction/six-providers/exact-six-full-history-half-cover`.
- Start state: branch `rebuild/research-v2`, requested starting HEAD `e0b8e7d28c5164fbd5fd0ef689886c1279e380b7`. Repository state will be verified read-only.
- Assignment: audit Boss2's `partial-fractional-cover-to-six-half` and `four-extras-to-six-half` against this RUN's original model and section-scoped target; identify exactly uncovered catalog structures; prepare a reproducible original-model versus relaxation boundary experiment. Read this RUN spec and packet-full first, then context/show evidence. Do not rerun certified computations and do not promote conditional subclasses to general half-cover.
- Write scope: this `informed-b/` workspace only. No commits, pushes, studio save/line, registry edits, or credential access.
- Status: started; awaiting applicable repository instructions and primary RUN context.

## 研究断点 1：边适用性与 q=5 三类剩余

已按 context/show 实读两边源正文、必要上游真实行与partial证书原件，未重跑已认证计算。准确适用性及未覆盖目录结构见 `boundary-audit.md`。本 RUN 题面/模型SHA与Boss2完全一致，section限定不改数学；两条边均只支付条件子类。

Main 指定q=5后，解析分类完成：倒二全部历史由精确P折扣、重复层和真实末位IC可给K/2；前四位的条件归纳只剩A=(第3位前两不同锚)、B=(第4位前两不同锚+一额外)、C=(第4位前一锚+同额外两次)。详见 `q5-prefix-reduction.md`。这是本线待非作者复核的局部推导，不是q5整体已证。

对idea给出的K5循环区间原目录，已独立编写精确全部SPE子局/根可达集合实现 `exact_tail.py`，原输入 `q5-cyclic-K5-input.json`，实际输出 `q5-cyclic-K5-output.json`，完整真实子局策略DAG `q5-cyclic-K5-policy.json`；子局DAG再由不调用集合递推的直接偏离核验器核完。下一动作：读实际输出并把静态暴露失败与真实SPE结论精确并列；再攻B/C真实tail约束。

## 审查反馈与v2修复

review_q5确认旧K5输入B0=T0，实际q4，“q恰5”是错误范围声明。已真实告Main/idea/reviewer并接受；全部v1冻结字节不改。新 `q5-stress-trial-corrigendum-v2.md` 解释准确影响与修复。真正q5改用K6、循环起点1/5/10/15/20，先由 `verify_q5_stress_input.py` 检查实际集合互异/非锚，再计算：互异额外后手静态损失(10/3,10/3,19/6,19/6)>K/2=3；但全部真实子局及根SPE均唯一终局计数六锚各一次，W=36，子局当前最低收益6。固定输入/输出/1405节点策略DAG全为 `q5-cyclic-K6-v2-*`，未覆盖旧文件。

B/C新参数化探针均另文件保存：`probe_bc_tail_lp.py` 的独立尾必要松弛给B=21/44、C≈0.454386，不能实现原策略；接着 `probe_shared_bc_tail.py` 在同一客户空间上固定四个unused额外覆盖，显式加入末位跨枝共享合法菜单查询，第一轮100模式正在核。它仍排除了后继为锚的情形，且只是一组必要约束，不作反例。

## v2通过与B共享模型的完整否决断点

clean `q5-prefix-reduction-v2.md` 与manifest已稳定送Main；review_q5对v2定向复核approve，报告records/review-q5-v2.md（含独立全有序树重算与证书校验）。这只是准确局部解析/有限试验，原题仍开放。v1的q误标已显式勘误，不改旧冻结。

已实读正式末两位7K/12定理及计数引理、idea `tail-menu-reduction-r1.md`，核通B全部四强制枝必双unused-extra、C至少四枝的真实BR缩减。廉价7/12回灌不改变独立尾坏值；旧共享探针漏旧锚+1的范围已在 `bc-tail-progress.md` 明确降为受限目录。

修正6锚+outside精确共同前缀的共享B必要LP，全1365模式已跑，出现精确可行坏点67/136，pair模式[(F0,F1),(F1,F0),(F2,F3),(F3,F2)]。全部模式索引、有理逐行证书和K68原模型补全均落盘，见 `bc-tail-progress.md` 的完整链接；不称浮点最优精确已证。

最短原模型阻断：h=(T4,T5,E)，强制T0候选(F0,F1)倒二收益51；改F2后非重复候选中唯一可能压低它的末位T2自赚44，而查询F3得63，故排除；真实末位唯一BR为F3，倒二获63，严格+12。原候选W334>204；完整SPE原根W408=OPT，指定B子局W371、当前最低105/2。已回送Main与idea，下一动作等待idea选择跨extra真实切行或同叶福利预算；不重跑同一未闭合模型。

## TQ切行固定配对模式的精确局部进展

实读idea `cross-query-cap-row-r1.md`，独立复核同一未知真回复L的容量消元TQ：u5≥f_b(T)+U_b(Q,T)−K，所有背景/标签/弱平局有效。只加四F的16行，固定原最坏pair模式的浮点下界变0.525。已导出有理对偶并另写纯标准库223型Fraction核验器，精确得四条强制收益平均≥21K/40>K/2；完整证明/系数/输入语义见 `TQ-cut-validation.md`，证书及重放 `shared-B-pair-TQ-rational-dual.json`、`shared-B-pair-TQ-exact-replay.json`，复现 `verify_B_pair_TQ_certificate.py`。这支付原3个坏模式的同一置换轨道；其它1362模式仅浮点观测，未精确认证，故不声称一般B或原题闭合。下一步由Main/idea判断是否逐其余68轨道提取精确证书，或优先总福利/C/A。

## 整体B类付款完成（作者精确核，待非作者冻结复核）

Main授权后完整构造1365→69的S4轨道映射：同时置换四新锚/分枝坐标和F会员坐标，保所有原前缀、客户、容量、查询/TQ行；映射给出逐模式F置换及锚排序。`certify_B_all_orbits.py` 提取69个代表的全部有理对偶；`verify_B_all_orbits.py` 完全用标准库Fraction重建223型/165行/224列与1365×24覆盖，69/69通过，失败空，最小证书界325/632>1/2。

合成自足稿 `B-all-orbits-proof.md` 与全依赖SHA `B-all-orbits-review-manifest.json` 已稳定，后续不改这些受审字节。精确结果证明四枝全双extra模型max强制收益≥325K/632；一般B节点必须和锚后手解析分支合成，只主张K/2。q≤4由正式四额外定理支付；q=5才恰有四合法unused-extra，未新增占位行动。K0、前缀任意次序、同覆盖异标签/离轨弱平局均明列。

这是q≤5总体路线的B类局部付款；C和A仍欠，一般原目标未闭合。下一动作：Main冻结整体稿并派非作者审读；本线仅准备另文件正式局部回流草案，不漂移受审文件。

## Main扩展写权限后的正式新草稿

Main明确授权新建canonical正文/证据、records batch和map edge，未授权改registry或旧正文。已按最终受审字节复制新child-state正文与六个同目录证据文件到 `tools/evidence/six-five-extra-B-prefix/`；canonical solver-free重放再次通过，SHA与工作区源完全相同。新batch `records/B-registration-batch.json`；新条件结构域局部贡献边 `map/edges/n6-boss3-20261118/B-prefix-half-contribution.json`，只result=B当前K/2，remaining=A/C及一般无锚/更多extra。边引用已审q5-prefix-reduction-v2.md §3，保同叶条件账。

已执行batch叠加edge-bind --write和edge-check，返回proof_scope=step、canonical_registry_modified=false；未运行register、studio保存、commit或push。最终publication_refs、canonical全SHA与artifact数据见 `B-publication-final-manifest.json`；可直接给Main使用的artifact记录为 `records/B-artifact-publication.json`。Main将新freeze派非作者窄核迁移/注册/边字节后串行回流。

## C接续开始

B全部数学/canonical/batch/edge受审字节保持不变。Main新义务为C：唯一旧锚5载荷+1，E覆盖载荷+2；新锚0..4，选四轻锚0..3、第五新锚4保持fresh且参加全部菜单/倒二deficit比较。已实读idea `probe_C_four_light_TQ.py`、单pair输出及 `C-migration-map-r2.md`，复读B冻结整体稿以核迁移差异。

另文件 `verify_C_all_orbits.py` 已重新构建C自己的223型、189行、224列纯Fraction模型与完整1365→69映射；`certify_C_all_orbits.py` 先完整69轨道浮点排查，全部过半才接受C新有理对偶并调用独立于发现模块的标准库精确重放。不复用B乘子；不把第五新锚当旧锚；q≤4走正式四额外，不添加占位。C发现/映射/证书/重放全部另存C前缀新文件。

## C整体作者核完成

C全部69轨道浮点无失败、最小约.5279535865；随后为C独立重取有理对偶，69/69精确通过、失败空。标准库 `verify_C_all_orbits.py` 重新构建2E+唯一旧锚5+强制轻锚j的C背景、189行/224列和全部1365→69映射，最小有理界1001/1896>1/2。

自足稿 `C-all-orbits-proof.md` 已完整写轻锚存在性（至少4/5个Ej≤K/2）、任选四轻锚重命名而固定第五新锚4、同一完整σ/任意前缀次序/异标签重复E、q≤4走正式旧定理而不添占位、所有189行真实来源及69轨道合成。一般C只主张K/2；1001/1896不越出四轻枝双extra模型。C没有调用B乘子/证明结论，B全部受审字节未改。

全15项依赖准确SHA在 `C-all-orbits-review-manifest.json`，当前C数学文件稳定待Main冻结非作者。仅本线新C文件，无新canonical/registry变更。已付B/C后仍欠A，一般原题也仍开放。

## C新canonical与共同最终冻结输入

Main再次明确授权C新canonical/records/map草稿。已复制准确受审C数学正文与七份同目录证据到指定child-state及 `tools/evidence/six-five-extra-C-prefix/`，不改任何B字节。正文materials.objects、七个必要附件materials.attachment，吸收B publication-v1的元数据反馈。

canonical标准库69轨道重放再次通过、所有目的SHA与来源一致。`records/C-registration-batch.json`、`map/edges/n6-boss3-20261118/C-prefix-half-contribution.json` 已batch overlay bind/check，proof_scope=step、canonical_registry_modified=false。边只付C且显式结构域/真实σ/原标签历史；A与一般原题剩余保留，B为另项真实已审准备发布结果，未在C单源边隐藏共同采用。

可直接artifact记录 `records/C-artifact-publication.json`，artifact_id=SIX-FIVE-EXTRAS-C-PREFIX。全publication_refs/canonical准确SHA、数学manifest和检查回执见 `C-publication-final-manifest.json`。供Main做C数学+publication一次最终freeze并派非作者全核；本线未register、studio保存或Git操作。
