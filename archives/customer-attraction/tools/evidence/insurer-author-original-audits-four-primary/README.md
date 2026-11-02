# 作者不交与padded保险原审计及冻结证书

原程序/报告四份冻结源共91,488B，来源身份见[manifest.json](manifest.json)，原件位于original/。作者原件与独立blind/sharp原件分包，本包只给作者两入口的事件。

- [程序正文](../../../state/程序/不交花瓣与多主题保险的作者原审计--程序.md)解释完整模型、集合值BI、精确输入、所有断言及边界。
- [340行输入目录](disjoint-input-catalogue.jsonl)逐行展开源生成规则，不调用任何求解器；[报告汇总](report-summary.json)读取全部340+4条冻结记录。
- runs/disjoint与runs/padded保存本轮各一次原入口的event/stdout/stderr；重生两报告均逐字同冻结，故不另存重复报告。
- [四份完整padded证书清单](certificate-manifest.json)对应certificates/中的gzip文件，解压内容是未改代码实际生成的JSON，每份含全部客户与全部有序历史行动。压缩mtime固定0，清单同时保解压指纹。
- [自查程序](check_saved.py)不导入源程序、不算BI或LP；核四原件SHA/size/blob、冻结报告统计、显式输入与断言结构、完整行动表的合法历史覆盖、运行事件及各资源指纹。[自查结果](verification.json)保本轮结果。
- [比较阅读与关系判断](comparison-and-relationships.json)明确有限验证、实现、来源和域区别；阶段二没有借旧图造超边。

成熟解析结论分别是同根跨度/总客户成本、不交结构类三倍half稀释、多主题完整修复与R4等价。空主题、重复选择、离轨平局保在正文；零客户或只有核的退化类未被本main实际输入测试。一般六人half未解；本包不作新blind、外审或新颖性认证。

另有四份正式冻结完整证书主源，共1,178,612B，与现有四gzip解压字节逐一完全相同。[冻结证书来源清单](frozen-certificate-source-manifest.json)保各源ID、双commit、SHA/size/blob及复用路由；[完整无损阅读视图](frozen-certificate-full-reading-view.md)保全部非actions字段及3/6/10/13类完整有序子树；[阅读数据](frozen-certificate-reading-data.json)可恢复全部原字段及源JSON字节。[结构阅读器](read_frozen_certificates.py)不求BI、不回放收益、不调用原源码；当前四源复用此前唯一gzip与成功事件，新增入口0，原四条收据不改。
