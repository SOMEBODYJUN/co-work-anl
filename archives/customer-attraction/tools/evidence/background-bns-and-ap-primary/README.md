# DQ3 加权背景BNS/AP完整证据

实际三源[claim回执](claim-receipt.json)原样保留，pushed/Boss4/synced `bf8532e7fe048fa031da634baebbd85db15446a7`，owner再次核Boss4/in-progress。实际ID与本3原件一致。[安全local导出](local-export-manifest.json)核Git blob SHA1/size/SHA256；本代理无网络/懒加载/clean show/shared Git写/claim/done/checkpoint。

三主原件9918B全部完整逐节/逐字段阅读：

- [577c036ceeac0040c7e9 — research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/CLAIMS.md](original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/CLAIMS.md)，2461B，SHA `6be7a7a0ad16cf3b243e29fad6e840a5b318d8ec0d452746d09060ed87252ccb`。
- [0fc618b232c3486fbbc3 — research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/README.md](original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/README.md)，1851B，SHA `98cff368ab51cf24dd09208070b10409fb28cf027d3eac6a23ce5f49cdc3fd87`。
- [1a1bf1f73c14d766e93a — research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md](original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md)，5606B，SHA `f7f5d496681a3952159aa1a1c4299234aa2f59e14d6858ea12f2df2a5314665b`。

完整比较输入（不抵primary done）：

- [46b1b3c7907ee8c886ce — examples/customer_attraction/individual_security_failure.json](comparison/examples/customer_attraction/individual_security_failure.json)，SHA `bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a`。
- [4617d18c9d098ce255c9 — evidence/certificates/customer_attraction/individual_security_failure.json](comparison/evidence/certificates/customer_attraction/individual_security_failure.json)，SHA `d5c8fc3abe3acf7b4b61b776a957a13e49dfe276df517ee9ba4a47093a2792ab`。
- [b312212275551b29955a — evidence/certificates/customer_attraction/aggregate_theta_failure.json](comparison/evidence/certificates/customer_attraction/aggregate_theta_failure.json)，SHA `cf08edab0813de8eccee8d5466d15b40bd42c980da9b0b68c925f4ae80991010`。
- [c838c11dfaa7a54dcca8 — examples/customer_attraction/aggregate_theta_failure.json](comparison/examples/customer_attraction/aggregate_theta_failure.json)，SHA `be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf`。

| 证据 | 实际范围 |
|---|---|
[相关audits local export](related-audit-local-export-manifest.json) | 只得主MD，四原程序/JSON缺blob，不fallback |
[新checker源码](verify_background_rows.py) | 标准库，weighted行与整数核，无原程序/solver/LP |
[新检查result](new-data-check/result.json) | 每版516 AP/186 BNS、90空C、175核；新3客户14 IC |
[新检查event](new-data-check/event.json) | 一次exit0、日志/SHA，缺开始时间不虚补 |
[旧DG有效性复用](reused-DG-check/manifest.json) | 同四输入字节/43策略完整IC，旧成功记录保留；本批DG helper新run0 |
[执行边界](execution-boundaries.json) | 1867与八证书均未本批认证 |
[数学比较](comparison-findings.json) | v1/v2空锚/共同支持上界/根特例去重 |
[正式比较snapshot](formal-context/inventory.json) | 整体相关对象精确SHA；相邻换位M_C仅符号排歧，不造依赖 |

正文完整重构BNS/AP v1/v2，保任意有序真实后继、k2特殊符号方向、C空直接证明、加权最大主题刚性、统一MC支持上界及不能逐列替换。CLAIMS/README全部身份、数字、有限程序域及旧点非SPE限制另有自足资源，没有只写路由。

本批原入口0、LP0。新数据checker一次exit0；两旧34/36完整SPE有效性按DG成功同字节复用，只算新的weighted行，不重做其258IC。新三客户控制全7节点14含自身IC为本批新检查，展示MC3→2收紧；空C直接公式不当旧游戏新加空标签后的SPE证明。

四相关audit源码/JSON本地导出失败，原八证书数10025/55360/1603/65345只保原声明、不猜self口径、不冒v1/v2两次新覆盖。固定支持原点/行包未取得，后两长分数>2的算术不认证1867行可行、精确最优或完整SPE。所有缺口明确写在receipt/正文而非强签。

复现新checker须另建新空目录，以绝对路径调用，不覆写现有证据。旧DG代码以原字节另名保全，本批未调用；新检查依赖其保存结果/同输入策略。当前五人half另证、六人开放，不由本必要行给全局slack支付。
