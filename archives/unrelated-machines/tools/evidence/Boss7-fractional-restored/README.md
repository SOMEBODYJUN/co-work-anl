# 分数重匹配 v4/v5 四源恢复证据

本目录保全四个已认领源的原字节及 gzip 的无损解压正文，服务于[完整中文审查对象](../../../state/审查/分数重匹配显式XOS-v4-v5增量--审查.md)。恢复使用只读 `python tools/cleanup.py --repo . show ID --out PATH`；没有读取认证文件或执行 Git 写入、认领及 done。

| clean ID | 原件 | 原件 SHA-256 | 解压正文 SHA-256 |
|---|---|---|---|
| `93808197dd001b8ac118` | [v4 gzip](original/fractional_rematching_extension_statement_only_v4.md.gz) | `4b197101a7a2e1b5ea4ecb127a817c1e9ec0b9c37adea30d39dcd4eba6ea2d3e` | `de055b02aca6d3876628671638bd509c16a1716d052b489d265e2303d37c400a` |
| `b50f2d64238493b723a0` | [v5 gzip](original/fractional_rematching_extension_statement_only_v5.md.gz) | `eaa34ed503e7e5c78e755ad8d11efb0a1de82edb622892a3faba188a3f614006` | `3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e` |
| `dc1a1b0e22af277523e9` | [v4 coauthor 原文](original/fractional_rematching_extension_v4_coauthor_validation_and_provenance.md) | `c1c54165d2875ceb31b47b9406bfcc793488b4bef1bb45efc63c299f53840c3f` | 同原件 |
| `8e013b1a8d17a54eba9a` | [v5 coauthor 原文](original/fractional_rematching_extension_v5_coauthor_validation_and_provenance.md) | `8bd29ecf095d0f23541893381ee977321348901433a01de899ff2cee9bdc09e4` | 同原件 |

[解压 v4](decoded/fractional_rematching_extension_statement_only_v4.md)和[解压 v5](decoded/fractional_rematching_extension_statement_only_v5.md)与已恢复 root 正文逐字相同。[完整 315 行 diff](v4-v5-full.diff)由全文生成并实际阅读，A 段不变，B1/B2/B5 的强化及 C 取消全局 floor 是主要数学增量。两份 coauthor 均为知情协作验证，不是 independent Exact-first 或完整 NSW 作者证明。

[manifest.json](manifest.json)保留冻结提交、路径、blob、原件/解压 SHA、字节数和行数。五版 A 的机械比较为 3,565 bytes，SHA-256 `1c1250fb4e62c641d2bdc1d688d967cc5334e999ad61862a2641c1e3bd0f4828`；v1–v3 的比较副本和实读记录在本轮 fractional 工作区，原件仍按 inventory 冻结路径可恢复。字节相同不替代数学证明。

运行 `python archives/unrelated-machines/tools/evidence/Boss7-fractional-restored/verify_sources.py --repo .` 可复核四源身份、解压、v4/v5 的 A、完整 diff 哈希及精确常数算术。实际输出保存在 [validation.json](validation.json)。该脚本只核源字节及常数，**没有实现或执行 NSW、LP 迭代、福利 CDF 或 label DP 后端**，也不声称以有限实验证明普遍算法结论。

相关后续证据沿用现有目录而不重复包装：`retired-nsw-v5-20261031/` 是 Exact-first、作者 proof 读后和旧 canonical 读后；`retired-nsw-flat-followup-20261031/` 保存高端/低端 γ 互补勘误。旧 canonical §F 的“不覆盖”外推已被后者撤回，详见审查对象第 8 节。

本批仅在本地交回父 Boss；推送及四条 receipt 的正式提交尚未执行，不称 done。
