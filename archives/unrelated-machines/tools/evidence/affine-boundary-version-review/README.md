# 仿射线结构边界：合并版本与分域review证据

说明对象是[版本与分域复核](../../../state/审查/仿射线结构边界合并稿的版本与分域复核--审查.md)。本三源不新增主定理：合并draft保两个既有Claim的完整早期正文，两个review分别保双Claim的分域汇总及单边际独立链。原件共33078字节均已全文实读，按冻结原字节保存，源ID/提交/blob/SHA见[manifest](manifest.json)。

| 源ID | 原件 | 字节 |
| --- | --- | --- |
| 81a6dfe595fab217d13a | structural_boundary_canonical_draft_v1 | 26707 |
| 39a4d75750002384dde4 | pairwise_independence_boundary_review | 4148 |
| 1480d9b9b2b045a290a1 | uniform_marginal_gap_review | 2223 |

`comparisons/`保当前canonical0b941、单边际canonicalb81d和三份实际最终scope的字节副本。它们是已整理内容的比较依赖，不重复done。

[draft-to-current-diff.json](draft-to-current-diff.json)及[unified diff](draft-to-current.diff)确认两版本都是289行，只有三处各一行替换，净增150字节：总前言待root/final→已读及review入口；两Claim各自Evidence中的待final→以冻结scope为准。按这三替换可重建全部当前字节，所有数学正文/定义/条件/量词/公式/counts/scope未改。旧draft保其当时pending状态，不倒改为后来认证。

[reference-hash-checks.json](reference-hash-checks.json)逐项核39a原表11项与1480原表5项引用SHA，全部与库存及保存原件一致。指纹核对不冒称新盲审或重新全文读所有上游raw：本轮五份比较依赖中三个scope均全文读过，前批已充分整理的数学主证明继续使用其正式正文。

Whole-file hash、实际读取范围、数学认证范围必须分开：general的one-primary scope只实读header/§1–2，未读simplex§3–8；bicriteria全文读合并页，却仅认证simplexheader/§3–8和§1.3定义依赖；rank在独立b81d单边际页审header/全部§1–4。Root事先知策略不是blind，typed合稿不成为第三次独立证明；相同wholeSHA不转移各自scope。

无新软件或数学运行；所有diff、SHA和链接检查是静态版本/交付核验。未改任何已有正式页、图或冻结源，不把单边际root旧数字辅助自述补造成运行日志。
