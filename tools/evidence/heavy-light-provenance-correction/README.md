# 重轻冻结审查增量：最小来源指针 errata 候选

本包**未修改共享目标**，不改任何旧 done、claim 或数学结论。目标是 `archives/unrelated-machines/state/审查/重轻森林整数性与价格凸化冻结审查增量--审查.md`。原快照 [target-before.md](target-before.md)，可审候选 [target-proposed.md](target-proposed.md)，精确六行替换 [proposed.patch](proposed.patch)，完整指纹与应用前置 [manifest.json](manifest.json)。数学正文在 frontmatter 后逐字节相同，SHA见manifest；只改 source_ids、source_refs、evidence 三字段。

| 原错误 | 核实后的候选 |
|---|---|
| source_ids 第一项 b7724da00b7bc1ee746e | 943319840138764f0f61；b772实际是 frozen_macro_tiny_review，不是森林整数性review |
| 两个冻结commit下的两份review路径均缺 `_review` | 实际路径 heavy_light_forest_integrality_boundary_review.md 与 heavy_light_price_convexification_review.md，共四行 |
| 第一 evidence 指向 frozen_macro_tiny_audit.json | 新 BE 真实一次原 CLI 的 forest-integrality.stdout；这是新增运行证据，不能倒填成旧审查当时的运行 |

第二source ID ad117632752525a91aa0 与第二 price release evidence 均保留；数学正文全部保留。准确 source/path/SHA/两个冻结提交、错 b772 的真实身份、新 evidence 的原 CLI/argv/退出码与SHA都在manifest。两份实际review原件保存在 [forest review](sources/heavy_light_forest_integrality_boundary_review.md) 与 [price review](sources/heavy_light_price_convexification_review.md)，已完整实读。新的 [forest stdout](new-evidence/forest-integrality.stdout) 和 [execution](new-evidence/forest-integrality.execution.json) 只是从已冻结 BE59 包按字节复制，本errata没有额外数学运行。

Root应先按BE59 manifest保存其证据，再实读此目标与两真实源，核当前目标 SHA 与 manifest 的 beforeSHA 一致后采用候选或patch。若目标已变，须按字段重新核差异，不能覆盖后来的合法修改。本包是独立 proposal，不加入BE59旧copy清单，不把两旧review重新认领/done，不将指针错误说成数学反例。全部操作仍由Root串行保存。
