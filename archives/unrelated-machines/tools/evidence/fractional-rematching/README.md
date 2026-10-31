# Fractional-rematching source evidence

本目录对应数学对象 `unrelated-machines/fractional-rematching-normalized-xos-robust-gap`。冻结来源均来自 `68fad804ec5946cb296f77dc5b336308a66abf12`（`main` 的同路径副本为 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`），实际用 `clean show` 逐份导出并全文读取。未把临时导出文本冒充正式证据副本；下表保留源 ID、路径、SHA 和处置范围。

|source ID|path|SHA-256|实读与去向|
|---|---|---|---|
|`0becaa69222f60a39778`|`history/source/notes/unrelated_machines/fractional_rematching_extension_author_proof_v5.md`|`2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af`|1052 行全文；Residual lift、rounding、split、mask DP、rematching、unit-FSLP、REPAIR、flat-UM 全部写入正式对象；作者稿仅候选、待独立复核。|
|`54a943262a45ccdbab4b`|`history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v1.md`|`b7f8fe124eed85643dda4e48251da3a794b2869b7b22128c55f899198774d5fa`|162 行全文；独立闭合 A、有限位匹配、unit-FSLP 和计数推论，确认 B/C 仅条件。|
|`233b30b9965c44b6279e`|`history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v3.md`|`a605f5d0aeb5c82de251bf5d37867717da511635bfb5e093c9f6846514534d75`|206 行全文；指出旧一般次可加 tail 链的 μ 因子三、任意 Bernoulli/shifted f 适用缺口，给出保守替代范围；未读取作者稿。|
|`9b3c07cbaa852f8b6cd2`|`history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_review_v2.md`|`63c9e78d49c4a0eee967c24a8cc535e5cbcaa3fa149cf4f8e6bde2f8be3235fc`|97 行全文；核对 v2 的 60000、1125000、2250000、3/4 floor 与 rho=2^24 算术，但未审完整 backend。|
|`6850f5bed243e9c279fc`|`history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v1.md`|`33e8a8ec34d17ed605bf4b752ff4210d1bc9a68a46c8f673dd05f384754d7948`|134 行全文；只含定义/条件结论，无证明，保留版本身份。|
|`89d84471bbf353ae5c50`|`history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v2.md`|`6acd2c44963d9312ade20efed5128048b81f35b8391b5bc09875ec60ed0205de`|150 行全文；只含定义/条件结论，加入内部 floor 与保守常数。|
|`4d837b23153a2df96c46`|`history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v3.md`|`ee80af544eaa5f133efb426a38e8007f21c0ee85594c48e7feaacd5caacc5697`|207 行全文；统一 A、B、C、REPAIR、flat-UM 和量词边界；无证明。|

## 读取边界

所有来源均实际导出并逐段读取；不存在 PDF/代码执行声称。作者 Proof v5 引用了其任务中另行冻结的 v5 statement、DLRV 文献和两个工具证明，但这些并不改变本批七个源的身份；本对象只把作者稿中可复述的候选路线作为条件内容。后续必须进行独立 read-after、有限位/采样实现审计和 `map` 关系判断，才能升级 B/C 状态。
