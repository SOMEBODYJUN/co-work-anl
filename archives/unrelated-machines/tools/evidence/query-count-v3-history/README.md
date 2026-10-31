# 查询计数v3的端点、最终scope与精确快照

正式对象：[近单位查询必要条件的端点与最终组合合同](../../../state/审查/近单位查询必要条件的端点与最终组合合同--审查.md)。完整计数/heavy主证明沿用[版本审查](../../../state/审查/单件查询计数与近单位必要条件的版本审查--审查.md)，原零端修复和实际/owner两筛选见[零边界与保守证书](../../../state/审查/查询计数的零边界修复与保守筛选证书--审查.md)。本批不重复主定理，而保全五个正式源的独有版本、先验、端点与final范围。

[source-manifest.json](source-manifest.json)列5个主源：v3 Exact、作者Proof、general read-after、typed final、general final。它们此前作为比较依赖保存；本批正式认领后重新全文读取并核字节，各源独有内容与receipt单独保全。完整原件继续复用 `query-final-scope-history/comparisons/` 的原字节，不改Exact中“本v2单列”历史文字，不改旧v1异议/原v2文件。

[comparison-manifest.json](comparison-manifest.json)列8个全文比较源：v1/v2五份历史、root计数review、当前完整canonical及一般分离作者Proof。源版本分母/完成身份不因本批比较重复增加。

本批新增可复核资源：[两final所核的同SHA canonical快照](two_witness_query_separation_count_v3_canonical.md)，13950字节，SHA256 `fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c`。这份字节由当前19988字节、SHA `bf942037e600967fa86b76c2b1f0db41673a2bae71411e1afb6527d6f332c709` 的保真canonical提取：截在首个ASCII `## 6.` 之前，去尾空白后补恰一个LF。输出SHA与两个final及root review声明完全一致。实际提取规则/标记偏移/输入输出大小与SHA见[canonical-snapshot-recovery.json](canonical-snapshot-recovery.json)。原完整源未改，恢复快照全文再次实读；这不是一份新增审查、数学run或独立源分母。

快照确实只含分离v2第1–4节和计数v3/heavy第5节；两final不自动认证当前后加的多见证第6节。原快照内部链接保留源目录语境，未为迁移改字节；结果仓的可用入口采用上面的正式对象链接。

[review-scope-ledger.json](review-scope-ledger.json)逐源保存general读后8项端点、typed final 9项及general final 10项承重核对、真实先验和未认证软件/外审范围。[relation-review.json](relation-review.json)记录同族计数/条件收费联合推导、版本来源、快照身份及scope关系；本阶段未提前写形式超图。

[delivery-self-check.json](delivery-self-check.json)仅是实际交付完整性检查：13份复用原件大小/SHA、恢复快照的逐字节提取/13950B与fa93 SHA、5条receipt和正式正文/本README链接。检查器不执行原染色/构造器或枚举程序。本批数学run、新blind、原程序重跑均0；历史独立性只按原读取顺序保留，不升级外审/新颖性、生产后端或一般UM主目标。
