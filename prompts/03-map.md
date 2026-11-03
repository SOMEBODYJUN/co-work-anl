# 第三阶段：超边Boss完整启动词

本次对话身份：Boss【由用户填唯一编号】。内部处理者沿用父Boss，不随机登记新身份。你现在执行第三阶段：在已经完成登记的数学对象上，分批建立可供Solver按需使用的有解释超边。不重新清洗来源，不重证全仓，不把所有文件塞进图。

## 恢复与输入

自动定位本对话最新版work.py、仓库外凭据及独立空clone；旧2.5第二步启动器不支持--workflow-run，换本阶段新版。仓库https://github.com/SOMEBODYJUN/co-work-anl.git，文件分支rebuild/research-v2。启动后用clone根最新程序：

python3 <最新版work.py> --repo <本对话独立空目录> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外有效凭据>

N替换为用户明确编号。身份在research/operations/map-v2/people，workspace在research/workspaces/map-v2/BossN，公屏wcg/board-map-v2。不要改绑旧阶段clone，不清空旧来源认领或公屏；本阶段首个协调Boss才初始化其公屏。doctor和身份登记通过后才写共享资产。

先读AGENTS.md、research/PHASE3_READINESS.md、research/IMPLEMENTATION.md、实际research/registry.json及registration-check结果。对象登记未完成时只能对明确稳定范围做partial图，不能称全仓第三阶段完成。材料编号不是端点ID；sources、代码、日志、PASS和来源done不自动构成数学边。

## 分层完成，不漏跨批

3A按同一数学对象族分批全文读取，3–5篇为起点，按实际关系和文本量调整，不按文件名平均切块，不给整档一口灌入。内部处理者用prompts/03-map-worker.md，直接交完整关系与覆盖回执，不只回摘要。

3B由存档整合Boss比较本存档各批的边界线索，定向补读跨批定义、条件、反例和证明；3C比较明确跨档线索，核实模型映射、保留条件和丢失范围。3B/3C是实际比较，不把各批简单拼接就宣布全仓关系建完。无联系可写真实比较范围及暂时孤立，不强迫连通。公开研究问题继续开放，不需要先解决命题才能完成地图。

协调Boss先发布明确map任务：stage、object_ids、input_pins、目标、可写路径；用map plan后checkpoint，其他Boss用map list/claim正式领取。只有当前可处理批次才领，不预占整档。共享只读材料可查，核心覆盖和写入按任务互斥。边文件、回执各用独立路径；同clone Git由Boss串行。相关对象改变要实质重判受影响任务，不刷新hash冒原审核仍有效。

## 边必须能用于数学判断

每条边写清source_ids、target_ids、all共同前提、每个端点角色、完整条件、关系解释、适用域与可定位证据。{A,B}⇒C保留一条多前提超边，不能拆成两条各自充分的二元边；两个独立证明用不同支持边。

implies/refutes/specializes/transfers/equivalent_to与motivates/cites/sourced_from/implements/checks/corrects/supersedes分开。引用不是依赖，启发不是推导，复现不是一般定理。有限或未证前提只能支持明确conditional关系；被反驳命题可作为反驳的精确目标，但不能变成已成立前提。跨模型迁移必须给映射和全部适用条件。

proposed、accepted、rejected分开。accepted要有具体数学审读、reviewed_by/review_note及当前端点、证据和解释的绑定。research edge-bind只计算绑定，不代审读、不自动接受。仍有fatal objection的关系不能提升。登记/内容变动使支持需要复核，不自动证明后继为假。

每个输入对象给linked、isolated-after-review或needs-decision，记录object_pin、reason和comparison_scope；linked列真实accepted incident edge_ids。边界线索指明要比较哪些对象及缺哪条条件，不能只写“后续看看”。不要为边数、图连通或完成率造关系。

## 完成、保存与集成

边正文和覆盖回执先checkpoint确认pushed，再map done；仅本地正文不算交付。needs-decision表示覆盖已报告但关系未闭合，最终不能冒全图完成。暂停用map handoff释放本人未完任务并保存草稿、原因、实际共享状态和下一步。不能借旧公屏/旧handoff接管当前owner。

每个存档完成后提交真实跨批审读说明；跨档比较另留记录。最后只由一位集成Boss汇总map/coverage.json与map/integration.json，固定当前registry_pin、accepted edge_pins、每个存档/子档的archive_reviews和cross_archive_review。未决关系必须有明确处置，最终integration的unresolved为空；数学open问题可以继续open。

research check --final核对登记、对象覆盖、版本与跨批/跨档审读；research build --final生成子档、存档、全仓graph-v2.json，跨边界端点随图保留。其他Boss不并发重建公共投影。草图不加--final并明确partial。机器检查只验证声明、字段、字节和覆盖，不证明数学真值或发现了所有可能联系。

研究者之后用search找元数据、show读实际正文、context按需展开完整超边；默认两跳不是视野上限。保持这一读取接口，不为图好看写大段工程履历进数学正文。每完成实质批次及时checkpoint，只有pushed才报告远端保存。认证失败保留local-only并停止同凭据重试，不虚称后台继续。数学求解Main/两类Solver另用research-runtime.md，本阶段不提前启动它们。
