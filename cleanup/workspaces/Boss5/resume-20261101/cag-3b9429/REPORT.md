# R-3b9429 四根稿独立清洗复核

本批只处理 Boss5 已认领的四项；四份冻结全文已分别以 `python3 work.py clean show ID` 阅读。发现现有正式数学对象已完整吸收其独有内容，依 Boss 指示不新增重复正文，逐项作 duplicate；这不表示问题退休，也不新增旧程序成功运行记录。收据待 Boss 串行 checkpoint/done。

## 源与去向

|源ID|文件|字节|处置与承载|
|---|---|---:|---|
|755dab71e7e850faffbe|CLAIMS.md|1138|duplicate；根稿合同的状态表和完整槽引理保全六个准确对象|
|a5e1d1aada0668079ab0|FAILED_ROUTES.md|905|duplicate；根稿合同及完整槽引理保全失败机制、未排除状态和停止范围|
|4deb530d341310e63c6b|GENERAL_WORKING.md|5715|duplicate；两篇正文分别保全NET/SLACK/ENV/HYBRID与完整m槽末位/静态充分链|
|093d6b4381a4039cc8c0|RESEARCH_STATE.md|815|duplicate；根稿合同末节保全恢复状态和下一共同付款义务|

所有源路径共同前缀为 `research/workspaces/customer-attraction/R-3b9429e7635a48208e072c8f1597126a/`。每件均有两个同字节冻结定位：`68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。原件各文件SHA、blob及完整路由已逐项读取现有 source-manifest.json，并重新核对实际原件大小/SHA，合计8573B。不是两份独立证明。

正式承载路径：

- `archives/customer-attraction/state/资料/净覆盖缺口与真实补全余额的根稿合同--资料.md`
- `archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`
- `archives/customer-attraction/tools/evidence/complete-slot-price-and-net-slack-primary/README.md` 及其 `source-manifest.json`、`original/` 原件。

## 实际完整阅读和比较

已读协议：根 AGENTS.md、cleanup/README.md、cleanup/OBJECTS.md、tools/README.md、cleanup/receipt-example.json。检查写入路径全部祖先，相关路径没有额外嵌套 AGENTS；档内两份 evidence/source-root/AGENTS 不适用于本批。

除四份 clean show 冻结源外，下列现有正文均全文阅读；不是只读检索命中：

1. `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`：有限单位客户、共同非空目录、所有有序历史纯SPE、根覆盖和非空背景利润的区别。
2. `archives/customer-attraction/state/资料/净覆盖缺口与真实补全余额的根稿合同--资料.md`：四源对应8573B已齐，全部六节推导及恢复边界。
3. `archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`：末位精确折扣、纯p边界、2m比较和SUMmin条件蕴含。
4. `archives/customer-attraction/state/障碍/R-3b942一般查询行共同付款缺口--障碍.md`：固定σ真实query、child-min消元、对角修正及BAL债务。
5. `archives/customer-attraction/state/障碍/R-3b942混合账本与根菜单候选停界--障碍.md`：slack/hybrid及仅根W/m候选；其元数据错误见后。
6. `archives/customer-attraction/state/反例/实际前缀的剩余利润与新增覆盖--反例.md`：52客户表、259位完整策略编码、根真实偏离、平局版本差异及17<18。
7. `archives/customer-attraction/state/计算/实际前缀背景反例的完整策略核验--计算.md`：原八源、独立核验职责、旧259节点/1554比较、后续p2/p3有限根补证及版本边界。
8. `archives/customer-attraction/state/反例/唯一最优组合的全遗漏支付--反例.md`：12类客户、全参数两人SPE、21个无序主题对、k3的W35/OPT38/L36/E33。
9. `archives/customer-attraction/state/资料/背景总份额归纳的两种覆盖量与失效接口--资料.md`：BG与UNION-BG有不同净补偿；GLOBAL只反整体UNION-BG，不反裸BG。
10. `archives/customer-attraction/state/资源/完整终局推送的自身折扣与末两位储备--资源.md`：P/C/D区别、L/V/Q和actual末列储备不可双花，早期债仍未付。
11. `archives/customer-attraction/state/反例/银行完整根列的两查询最小分离--反例.md`：Mfull是逐人u封顶，精确值2−1/m−1/[3(m−1)]；m6实际W12故W/m=2，53/30没有反根W/m候选。
12. `archives/customer-attraction/state/定理/五人半覆盖--定理.md`：完整53乘子、6144条件的全域机制及余项表；当前五人定理已证而四源仅说本轮未新证。

另全文读取现有四源证据README与source-manifest.json。四份冻结源本身的读取是本次新的实际工作；旧README记载的先前0-run或原审计运行不冒称本次运行。

全仓相关检索：R-3b9429、SUMmin-full、M_root、RAVG、52客户、唯一最优全遗漏及真实slack等；检索用于找比较对象，不把其余所有命中列为已读。原 source subtree 中的其他代码、JSON、README没有因链接而算本批完整阅读或done。

## 数学判断与关系证据

- 域始终是有限单位客户、有限非空共同目录、任意m≥1的完整历史纯SPE；当前目标仅取m6。保留空主题、重复、零客户及所有离轨平局，其他模型不迁移。
- NET: |C|−W=L−E；71客户例全遗漏36>35，只反丢E的强桥，净缺口3、half余量32。目录六标签不是六提供者。
- SLACK: s(h)=W_h+V_h−F_r(P)=D_h+V_h−R_r(P)，沿同一实际孩子s(h)=s(h,S)+u−δ；根值2W−OPT。52客户实际AB前缀s=−1，同一例否每个固定实λ的R≤V+λD，却根half余量16。合法背景、实际可达均不能挽救这强式。
- ENV与HYBRID分别是有限孩子消元和同一完整σ真实叶的守恒；对角修正必须保留，旧收益只能在对应hybrid叶间望远镜。不能把互斥孩子覆盖搬成一个实际W的钱包。
- 完整m槽末位R_m≤u_m和纯p的全部位置界是真结论；SUMmin-full全混合p、Mpath≤W/m、仅根Mroot≤W/m分别是未证辅助预算。仅根逐人封顶反例不反根平均W/m；删根m−1槽反例不反完整m槽。
- 现有五人定理独立闭合，不倒推上述更强接口；六人half仍未因本批整理解决。有限阴性、原程序精确反例审计、全参数解析证明和当前实际执行分开。
- 已知关系是模型前提、恒等式重述、条件充分、明确加强的反驳及来源复用。正式对象和必要关系说明已存在，本批没有新数学对象或新超边；第三阶段不在本批重做。

## Boss明确授权的单一元数据修复

已修改 `archives/customer-attraction/state/障碍/R-3b942混合账本与根菜单候选停界--障碍.md` 的两行source_refs，其他正文与frontmatter字段不变。旧证据README已经提过这个同一错误，本次按Boss授权实际修正：

|旧值|准确冻结路由|
|---|---|
|`source:68fad804ec5946cb296f77dc5b336308a66f7ef8f/global_certificate/README.md`|`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b9429e7635a48208e072c8f1597126a/global_certificate/README.md`|
|`source:68fad804ec5946cb296f77dc5b336308a66f7ef8f/proof_core/README.md`|`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b9429e7635a48208e072c8f1597126a/proof_core/README.md`|

两准确路由由clean list --prefix该工作区/ --full逐项元数据确认，分别源ID a68027f980b90d991700 与6802e96a922d9ff79dff。没有改数学内容或承诺其普遍付款已证。

## 交付与校验

本工作区新增：`receipts.json`、`REPORT.md`、`validation.json`。四条receipt全部为duplicate、字段完整，targets是上述已存在正式对象/证据README。

验证：四源原件SHA/大小匹配；收据JSON及必填字段有效；全部targets存在；两篇主承载正文的本地链接逐一存在；元数据修补仅两条source_refs且frontmatter后的正文逐字不变。校验值及修补前后SHA见validation.json。

本次数学原程序运行0、SPE/LP扫描0、Git写0、sync/claim/done/checkpoint/send0。没有读取或输出凭据。未额外认领，不扩大范围，后续由Boss串行提交和下一批分配。
