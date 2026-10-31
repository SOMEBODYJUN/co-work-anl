# 7d9f8d124c39b973dec0 语义清洗草稿

## 来源身份

- source id: `7d9f8d124c39b973dec0`
- 路径：`history/research_operations/customer_attraction_transition/original/research/active_research.json`
- 冻结提交：`68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）
- 两个版本逐字节相同；blob `4a14ff7d31bb78e06045395c064eb2481cacb6ab`，大小 3212 bytes，SHA-256 `dd8c1b0bf632803a9abaa2c5e75d793c7d9d6e455da627ddb16f3968dd417404`。

## 实际全文读取

通过 `python3 work.py clean show 7d9f8d124c39b973dec0` 读取全部 JSON（不是只读清单标签），并核对两冻结提交的 SHA。顶层字段为 `schema_version=1`、`title=当前主攻与新会话路由合同`、`purpose`、`target_id`、`default_save`、`goal`、三个入口、程序/提交脚本、旧共享入口、兼容提示、`active_entrypoints`、`role_prompts` 和 `research_direction`。

文件的承重内容如下：

1. 历史目标身份是 `UM-TARGET-v1`，`default_save=unrelated-machines`；目标是一般 (R\|C_{\max}) 上寻找统一 \(\varepsilon\in(0,1)\) 和确定性、总位多项式时间算法，使所有合法输入都有完整分配且 (C_{\max}\le(2-\varepsilon)\operatorname{OPT})，包含可增长的机器/任务数及 `OPT=0`。
2. 当时的规范入口分别指向 `research/current/unrelated_machines/README.md`、`research/unrelated_machines/README.md`、`research/unrelated_machines/BOSS_START.md` 和 `research/unrelated_machines/RUNBOOK.md`；程序/提交脚本仍沿 `research/weighted_congestion_frontier/tools/work.py` 与 `checkpoint.py`。旧共享入口为 `research/weighted_congestion_frontier/README.md`，并明确旧绑定/显式 shared 的模型和范围保持不变，旧题 clone 不自动改绑。
3. `active_entrypoints` 完整列出根 README、RESEARCH_STATE、CLAIMS、FAILED_ROUTES、AGENTS、ASSETS、USAGE、research/current/questions/reviews/ROADMAP/REPOSITORY_GUIDE/workspaces，以及 unrelated-machines 的路线卡、BOSS brief、模板、README、当前 README、weighted-congestion 的 README/AGENTS/RUNBOOK/PROTOCOL。
4. `role_prompts` 指向 weighted-congestion-frontier 兼容的 TEAM、OPERATIONS、CLEANER、EXTRACTOR、PAPER_WRITER、PEER、PRO_ATTACK；这解释历史协作兼容层，不是数学证明或角色授权的当前版本。
5. `research_direction` 为 `choice=negation-first`，来源是明确的历史 owner 决策（board message 501）；目标陈述本身不改写，状态为 `OPEN; research priority is not evidence`。方向是直接攻击一般目标：对每个固定 \(\varepsilon>0\) 证明不存在统一确定性总位多项式 \((2-\varepsilon)\) 近似；需要真实近二整数 OPT gap、可靠绝对阈值 decoder 和完整复杂度假设。`P != NP` 仅作为 primary hypothesis，必须显式写出，不能读作已证困难性。`positive_assets=preserve as tools and attacks on reductions`，不因否定路线而退休既有正面资产。

## 与当前材料的比较

- 当前冻结的 `research/active_research.json`（source `aba0feb89c0a654eab75`，schema 2）已切换到 `Q-CAG-HALF`、`default_save=customer-attraction`，目标是六人/任意人数单位权提供者与共同目录的纯 SPE 半覆盖命题；当前方向是 `general-half-coverage-proof`，状态仍 OPEN。它还把 unrelated-machines 作为 `legacy_entries`，并以 `retired_operations_manifest` 指向本次迁移目录。
- 因而本源是迁移前的历史路由合同：它准确记录了当时 `UM-TARGET-v1` 的入口、角色兼容和“negation-first”研究方向，但不代表当前用户指令、当前存档默认或当前数学真值。当前 `archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md` 已承接 UM-TARGET-v1 的精确定义、四项承重义务和 OPEN 边界；当前 `archives/customer-attraction/state/资料/客户吸引迁移历史归档清单--资料.md` 只在 28 项 manifest 中列出此文件为“superseded navigation or operating prompt; not a mathematical claim retirement”，尚未把本 JSON 的字段细节写入正文。
- 本源没有调度定理、算法证明、反例证书、有限实验或外部文献结论；其唯一独有内容是迁移时点的版本化路由字段、旧兼容入口和历史研究方向元数据。`UM-TARGET-v1` 的数学范围应回到 unrelated-machines 的 canonical 正文、审查和 evidence；当前六人 SPE 结论不能由本 JSON 推出。

## 处置建议

建议 `integrated` 到现有资源对象，不新建数学定理/反例/算法：

1. 在 `archives/customer-attraction/state/资料/客户吸引迁移历史归档清单--资料.md` 增补本源的 source id、SHA、历史 `UM-TARGET-v1`/`negation-first` 字段、旧默认入口和与 schema-2 当前路由的差异；说明它是“迁移前路由合同”，不是数学 claim retirement。
2. 在 `archives/customer-attraction/tools/evidence/history-transition-20261031/transition-manifest.json` 的既有条目旁保留同一 SHA/归档路径（该 manifest 已登记此条目），必要时新增原件字节副本或 manifest 交叉引用；不要把原 JSON 改写为当前入口。
3. 在 `archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md` 只建立历史来源链接（或在关系段落注明本源），不重复创建一个旧导航对象；其当前目标/OPEN 状态仍由该资料页和 canonical 正文承重。

如果维护者认为现有迁移清单已充分吸收这些字段，也可以将本源标为 `duplicate`，targets 仍指向上述迁移资源和 evidence manifest；不能标 `retired`，因为它承载了可复核的版本/路由 provenance，且“superseded navigation”不等于数学命题被否定。

## 不能外推的范围

- 不能从 `research_direction.choice=negation-first` 得出一般 (R\|C_{\max}) 近二困难性、`P\ne NP` 结论或任何固定 \(\varepsilon\) 的 gap；该字段只记录研究优先级。
- 不能把 `goal` 的存在式/全称式文本当作已证明的算法目标，也不能把入口和角色列表当作数学假设。
- 不能把旧 weighted-congestion 共享入口、旧程序路径或旧 role prompts 导回当前 customer-attraction；迁移后两模型保持独立身份。
- 不能把旧 `UM-TARGET-v1` 的 OPEN/反面方向覆盖当前 `Q-CAG-HALF` 状态，也不能将 unrelated-machines 的局部结果转写为六人 SPE 半覆盖结论。

## 回执字段建议（供 Boss 串行提交）

```json
{
  "id": "7d9f8d124c39b973dec0",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取3212字节历史active_research.json并核对两个冻结提交逐字节相同；解析全部schema/入口/角色/研究方向字段。",
  "comparison_note": "与当前schema-2 research/active_research.json、customer-attraction迁移manifest、unrelated-machines入口资料和现有UM canonical对象比较；确认本源是迁移前UM-TARGET-v1/negation-first路由合同，非数学证明。",
  "decision_note": "独有内容是可复核版本/路由 provenance 与旧兼容边界；建议整合到客户吸引迁移资料对象并保留evidence manifest，不新建数学对象，不把旧方向升级为困难性结论。",
  "disposition": "integrated",
  "targets": [
    "archives/customer-attraction/state/资料/客户吸引迁移历史归档清单--资料.md",
    "archives/customer-attraction/tools/evidence/history-transition-20261031/transition-manifest.json",
    "archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md"
  ]
}
```
