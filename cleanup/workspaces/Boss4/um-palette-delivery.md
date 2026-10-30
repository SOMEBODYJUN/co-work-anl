# 固定加工值格点两源交付

正式claim pushed：`692c11e49f21eb65f875113fc440555853d6f663`。`NEW21_READY`后完整实读主稿7547字节、代码5805字节，并逐字段比较Boss2已done报告8e850e2f9cc0ce939add。三原件全部hash/size匹配inventory及集中缓存；报告只比较、不重复登记。未执行Git、claim、done或sync。

## 精确checkpoint路径

- `archives/unrelated-machines/state/定理/加工值格点的可计算统一余量--定理.md`
- `archives/unrelated-machines/state/计算/加工值GCD审计的算术端点与零分支--计算.md`
- `archives/unrelated-machines/tools/evidence/processing-palette/`（整个新目录，9文件）
- `cleanup/workspaces/Boss4/um-palette-receipts.json`
- `cleanup/workspaces/Boss4/um-palette-delivery.md`

Boss先checkpoint并确认pushed，再以两条独立语义回执登记。旧7、旧2、共享README/图及Boss2原件/manifest均未改。

## 完整一般数学

主稿§1–7的全部模型/量词/算法/位长/两情形/文献及未完成义务独立落定理正文。n0、每任务零端的精确OPT0分支先行，允许未用正端；g从全部正有限值取最大有理公因子，∞不参与。补LCM/GCD和Bezout最大性、U/g二分/精确有理LP的总位复杂度，不按分母值或格点数循环。

原稿略引的严格槽界已完整证明：按加工值排序后，最后含正分数费用的槽不会被任何正任务的前槽收费使用，留出严格正费用；配合T*>0及g格点得实际负载≤T*+b_i−g。再按真实OPT≥B或<B两情形证明2−g/B；全局慢边可能不在支撑中，后一分支必须用b_i≤T*。

明确T*是整数g目标网格最小可行值，不是连续T_LST。新给单位加工时间q机/q+1件例：T_LST=1+1/q、T*=OPT2、连续LP gap趋2，g/B却1且算法相对OPT精确。这保护本定理的原比较基准，不误排连续LP间隙。

固定实际数值集S、字母表大小固定、依固定ε选Sε、随n/N变动的三正规形分别保量词；只有全类g/B有输入无关正下界才统一改善。对单ε须看其与β的大小，不能把g/B→0无条件套给每个固定精度家族。与{1/k,1,∞}双树gap、dense/log²/padded log正规形完整比较，未给未知backend、一般近二否定、NP/UGC下界或decoder。原稿VW整数版本仍保Paper Fact，未把未读原PDF或登记manifest升级为内化/优先权认证。

## 程序独有内容与真实新观察

完整实读grid/loads/exact_opt/check_one/fixtures/main。新资源保存四固定矩阵全部有理数据、六seed20261019随机生成、全部十行结果、4524合法分配、22算术端点/44帽不等式。报告“feasible”只是合法有限端分配，不是某目标下可行或LP证书；T/b端点靠单调/分段线性覆盖算术帽，不是逐格枚举或LP求解。

十冻结例均OPT>0、zero_only=false，不能说已测全模型零边界。新发现原helper只在无正有限边时早退，而模型OPT0还允许未用正端。本批因此**首次只做三输入定点观察**，没有例行重跑十fixture：

- `[[0]]`：独立OPT0，原helper正常返回zero_only。
- `[[0],[1]]`：独立OPT0、每件有零端，原helper真实抛`AssertionError`（进入其正端分支后assert opt>0失败）。
- `[[1]]`：独立OPT1，原helper正常返回g=B=1/ρ1。

包装器退出0、stderr空表示捕获并记录上述观察，**不是原check_one对中间零输入成功**。完整首次脚本、输入、原stdout、空stderr、真实命令/路径/返回值与所有hash均在新证据；标知情接口核验，不冒充新盲审或一般证明。冻结代码没有改，也没有把算术helper当完整算法。一般数学先零分支不受此内部范围缺口影响。

## 自查和接续

三原件大小/hash、Boss2副本相同字节、代码与报告code_sha256、首次wrapper/source/stdout hash/返回值与真实AssertionError均核对。AST静态比较确认规范payload之外的冻结字段恰`code_sha256`、`command`、`scope_note`，没有虚构原stdout与加元数据报告全字节相同。

两正文frontmatter/全局稳定ID、4条完整commit来源、19个本地链接及两回执全部正式targets均通过。未重复其他owner done或已有十例运行。可接续的是g格输入类算法、连续/整数目标区别、完整输入与软件零分支边界；g/B小、有限计数或ρ字段本身不提供近二整数gap/解码。
