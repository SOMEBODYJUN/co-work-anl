# Boss 整合说明

本组完整完成5源实读和比较，未修改共享仓库。请由Boss串行：

1. 将 `section.md` 追加到 `archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md`，frontmatter加入 `source-refs-to-add.txt` 的10条定位（如已存在则去重）。
2. 将 `original/<ID>/<basename>` 合并到 `archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/`，保持五份原字节。
3. 将 `manifest-entries.json` 复制为该证据目录的 `batch-e-resume-group4-manifest.json`，并按需要将 sources 合并主manifest；将 `byte-comparison.json` 复制为 `batch-e-resume-group4-byte-comparison.json`。section.md里这两个链接按这些最终名字写成。
4. `semantic-receipts.json` 恰5条，全部指向上述已存在资料对象；正文/原件/manifest先经Boss checkpoint并确认pushed，再提交done。

关系：新段是历史来源/导航/接续边界；数学由链接对象承担。JSON只支撑身份表，不连为推导。未发现要建立到六人SPE的数学边。此处是阶段二资料整理，不复制旧图。

注意比较中发现旧《固定阶压缩乘法向量贪心真实最优源--反例.md》写B件单位anchor，而较新完整canonical审查的同源模型是q件普通任务+一件时间B的anchor，n=q+1。本组新段明确采用canonical身份，既未静默传播旧压缩，也未越权修改共享旧页/receipt。若Boss另外整理该旧页，应保留其审查源身份，按原canonical source核对后再做单独纠错；本组5源处置本身不依赖修改它。

已实际验证：5个原件大小/SHA-256/Git-blob-SHA1均同inventory，3个JSON归一化完整字节同参考，2份README不是空模板，receipt schema齐全。数学原程序新运行0。
