# 接续研究：原资源核与聚合共同支付

2026-10-25；复用本clone及actor R-c8ca54e5f2854c2c93bf83abc2f24f5c，main/customer-attraction/boss。先安全同步并保留其他actor未跟踪文件，未改其绑定或内容。原Q-CAG-HALF仍OPEN，任意人数/目录、单位客户、全部历史、任意平局、空与重复主题及零客户均不变。

本轮六名指定模型研究员实际启动，完成者按有效任务补入；父方持续一般推导。下列组件或边界都不是一般half已证。

- [工作稿](MAIN_PROOF_WORKING.md)、[精确账本](CLAIMS.md)、[状态](RESEARCH_STATE.md)、[失败/来源](FAILED_ROUTES.md)。
- [有限匿名势凹化定理](independent/concavification_theorem.md)：任意有限层匿名势可改成非负单调DR，而所有m槽终局和m−1竞争槽查询共同平移，AFC及安全聚合缺口保持。不是CAG反例，不能把它用于m槽竞争/第m+1槽查询。
- [合同盲审](curvature/blind_cardinality_dr_review.md)、[父方另写核验器](parent/audit_concavification.py) / [精确输出](parent/audit_concavification.json)：重复动作、全层DR/单调及m=1空二阶集均核对。
- [原零根逐人地板勘误重放](parent/audit_root_floor_correction.py) / [输出](parent/audit_root_floor_correction.json)：父方未导入peer控制器而重建BASE/EXIT/PUNISH。有限重放不替代其全m解析证明；来源在工作稿。
- [全optional的未来负载截面界](jointflow/same_query_history_aggregation.md)：全部query、全部histories的未来负载密度和仍受一份源库存控制，并推出同query current一次IC付款；[独立合同盲审](curvature/blind_optional_jointflow_section_review.md)、[父方另写核验](parent/audit_layer_current_parent.py) / [输出](parent/audit_layer_current_parent.json)。这是已内部核对的原模型流组件，尚未支付不同query的整行总量。

当前正向目标仍是实际利润与混合查询之间的新共同金额，或净覆盖差额的直接证明。仅匿名势、一般DR、KKT重排、条件cut及有限阴性均不自动提供它。
