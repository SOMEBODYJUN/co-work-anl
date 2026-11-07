# 0113 新增18条审查证据：正式冻结验收候选

本交付只处理 `register-ab98f323ad-0113` 已有18个数学身份，从0118的精确请求逐项实际接收审查片段。18条已按原数学对象、模型、量词、条件、完整正文及成熟必要证据比较；无新ID、无关系边、无原数学扫描。原DONE、batch、receipt、registry、母候选和保护ready17均未改。

## 身份和合法顺序

原0113是57对象/46材料。原完整身份、原alias/历史10项分配及模型拆分均保存在 `original-identity-audit.json`；本轮不重新分配历史ID。当前canonical的目标18全部是与原batch逐字段相等的record v1。

实际DONE10（Boss5接办）是另外18身份/27材料。它与本轮18的对象交集是0；原母候选 `Boss3/0113-evidence-closure/schema2-supplement-candidate.json` SHA ff275f93787cd589304880c3ae9ff93d3cc5162edecacaed53281f76e13c1863 的交集也为0。不能把DONE10强套成这些对象的v2前置。原46材料与DONE10共有13页，审计保留其完整已发表row/owner，但本轮11材料与DONE10共有0页，未替换它们。

真正重叠的是0079候选 SHA 9343d61ebb29fd9d610eb202b1778725b4e7cfa56fc9fd036f9f32cfef89bbac 的8个v2。逐字段检查：它们相对canonical v1仅version加1和各自精确历史资产section补证，其余所有旧字段/evidence完全保留。父已指定先由Boss6的 `register-boss3-source-closure-0079-30` 实际发布唯一v2，再由本轮8条出v3，另10条v1→v2。

现已实际读到task30为DONE/Boss6、request cd129ea69d2e4695b1ff150de79967c5。实际batch SHA与母候选同为9343d61e…，8完整v2记录已分组全文实读并逐字段比对无差异。receipt中旧mature-local自述不改变task.state=done。`required-0079-v2-preimage.json` 改绑实际已发表batch/task/receipt，保存完整8记录与pin。当前registry SHA22b476a35c3221bbc17f36d29f165e9933f8f0e7c4a92b00c358122b302b4bfe（2891对象/3377材料）仍含这些8的v1，故前置是已DONE待集成；必须先30的v2再本包v3，不能声称canonical已有v2。若随后有其他实际增量，全数并入再升级，不能用旧候选覆盖新发表内容。

## 数学接收的实际内容

`mathematical-comparison-18.json` 对18个身份逐一写明对象、精确结论、承重推导和不应扩大的范围。两混页及9个主正文已全文实读；完整两列归约和source32符号证明额外全文读取，只用于分离定理依赖，不吞0112对象。

- 阶跃DAG的6身份分别保根整列/轻对称动作的字面真实费用、任意非负幅度的q端点、有理r参数、路径图极值/入度、祖先闭包树以及浅DAG反例。W<1、outsum<w严格，路径按顶点数，非连续阶跃不等于有限多项式。
- 端点系统2身份保存在权与固定权的不同量词、弱预算等号、全部slack权和饱和正纯d次刚性。该iff只对指定端点(E)，不把它当全状态模拟。
- 全入多项式4身份保共同极值幅度(N)，作者ending-path矩和独立有限双和矩，两套一般推导并存；真实light/root偏离的负载、正分母和strict Jensen尾步完整。d≥1的游戏定理与d≥16全实q统一常数分开。
- 十四资源6身份保固定degree32全16态/64翻位证书与弱B端点、固定权升幂在40及最终尾部失败、重调m3有限证书及m≥20统一方向误差、固定8witness三次根严格锥、完整正Boolean极限表及有限min/max连续性、全拓扑归约加source32证书得到的固定拓扑分离。m3不补m4..19，模板根不是全部拓扑最优，Bernstein源式上界不是全类G32保证。

ReviewB第6节末尾与旧资产JSON的OPEN属于旧背景，不接收为当前全类状态；成熟正文已明确后续线性全状态族更新。审查接证不删原成熟证明，也不重跑其审计来制造新成果。

## 候选、材料与验证

`schema2-supplement-candidate.json` 是完整schema2：18 objects、11 materials、edge_files空。8记录v3保完整0079 v2及其精确历史ref，10记录v2保真实canonical v1。每条只追加一个精确新review ref并升record.version；所有其他字段、aliases、sources、旧evidence和数学状态保持。

9正文材料行保canonical所有owner，包括本轮不升级的4个已登记owner。两新review材料行仍为needs-decision：本轮实际接受12/6对象的唯一ATX片段，三载荷和source32 Bernstein的0112范围仍未收。0118当前未发表草案在曲率页已有线性全态owner，完整原row单列材料ledger供串行集成，不向官方验证伪装已发表peer。

0079的历史可选页材料由前置30保其完整owner并集；本轮不提交替换row，所以不会删除其他已接受owner，也不把该页其余对象借进无peer验证。所有旧evidence ref照常保留且精确字节/ATX检查。

`validation.json` 是实际调用官方 `registration.validate_batch`、原baseline约束、peer_objects=None 的结果：18/11通过，仅只读复用canonical四个共正文owner。结构验证不等于已发布或再次数学独审。`reference-check.json` 对所有候选body/evidence用官方ref_bytes/heading_sections核精确SHA及唯一ATX。

## 阅读与预算

计划遵照Sol500K：正文/元数据300K，其他200K。这是用户规划，绝非系统实报剩余。`reading-scope.json` 逐文件/JSON值组/selected section记录实际阅读，去重复内容单元，给字符/UTF8字节及区间；没有provider真实token计数，故不冒称精确输入tokens。未读原旧46份材料全部正文、整个registry、0079全部41证明或原程序证书字节全文，不作此类声明。原JSON值分组读取的截断均已回补，成熟证据不重新扫描。

## 正式前必须完成

实际DONE30前置与最新9正文owner已核，正式目录授权后已完成材料化、精确SHA/manifest及一次官方无peer验证。父执行全部Git/队列/集成/push。已获父明确授权，仅materialize本正式目录，两个私有helper未携入。正式官方无peer验证一次通过，完整资产已冻结，父串行compose/保存/发布，本一次性worker结束。

最终顺序及实际DONE30完整41对象/36材料batch、receipt、task精确绑定见 `integration-contract.json`。当前canonical仍18个v1；8个实际v2已发表待集成。交付17个文件（16资产+manifest），无helper、无compose。

父验证按两次合法增量顺序：先将实际DONE30的41/36 compose到临时base，再绑定其精确SHA compose本18/11；同ID v2/v3不放同一组。该验证不写canonical，临时大表由父验证后删除，worker不需等待lead实际register。
