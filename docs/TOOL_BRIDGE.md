# 统一入口与模型协作

`python work.py --workspace work/<RUN> ...` 管理工作区，`methods` 调用经过适配的计算方法，`collect` 采集公开来源。Pro在自己的运行环境里使用内置搜索、阅读和分析能力；检索结果和裁决经JSON接口进入同一研究账本。CLI不需要另一个模型的API密钥来调用当前Pro。

## 内置搜索如何接入

1. `search-plan` 检查相同争议、统计期、已有结果及新鲜度。
2. 主模型使用运行环境提供的网络搜索/网页/PDF读取，按计划补具体缺口。
3. 保存如下JSON，执行 `collect bridge --file <JSON>`，再 `search-log --file <JSON>` 登记检索回执。内置工具的引用保留在原记录中。
4. 核读原文后，将事实、作者观点、政策和方法分别 `ingest`；一条检索摘要不自动成为承重证据。

```json
{
  "provider": "host-built-in-search",
  "query": "原样保留实际查询",
  "topic": "银行关注类与逾期贷款",
  "period": "2026Q3",
  "searched_at": "2026-11-27T00:00:00+00:00",
  "results": [
    {"url": "https://example.org/publication", "title": "原文标题", "host_reference": "工具实际返回的引用标识"}
  ],
  "decision": "对哪一条旧判断产生了什么影响，或为何保持",
  "next_gap": "下一项有价值的缺口"
}
```

正文可在本地缓存全文；公开提交只保留必要数据、短摘要、定位和许可允许的复现输入。原文URL、访问时点与哈希用于追溯。`cache/` 不进入Git。

## 额外公开发现接口

```sh
python work.py --workspace work/<RUN> collect discover --provider github --query 'repo:statsmodels/statsmodels' --topic methods --period current
python work.py --workspace work/<RUN> collect discover --provider crossref --query 'household debt business cycle China Korea' --topic household-debt --period historical-reference
python work.py --workspace work/<RUN> collect fetch --url <公开原文URL> --family <原始作者或机构> --kind viewpoint --period historical-reference
```

GitHub发现用于代码与方法选型，Crossref发现用于论文线索；经济观点可以来自论文、研究机构原文、作者研究笔记和公开仓库。每份观点学习其解释框架、关键机制、适用条件和错判经历，逐一检验迁移到本题的结果。

## 分析与程序的接口

模型提交：明确判断、依据、因果机制、适用条件、时滞、反证、对旧版本的具体改动，以及对情景/正文/家庭行动的影响。程序负责版本、依赖、去重、复算和保存。图中的箭头由研究者分析、检验和复核，程序不会根据关键词自动判定经济因果成立。

所有运行状态逐项记录：实际调用成功、只借入方法、需要外部数据或需要运行时内置工具。`methods list` 和 `docs/METHODS.md` 对应具体文件、接口和实跑结果。
