---
id: "weighted-congestion/history-team-compatibility-prompt-and-um-quantifiers"
kind: resource
type_tag: 资料
title: "历史共同研究提示词 TEAM 兼容入口与 UM 量词边界"
status: integrated-historical-compatibility-resource
truth_status: historical-routing-and-model-contract-only; no-mathematical-claim
review_level: full-source-read-and-cross-archive-comparison
summary: "完整保留迁移期 weighted_congestion_frontier/prompts/TEAM.md 的 boss 研究提示、UM-TARGET-v1 精确量词、反面研究纪律和证据/保存边界；该文件是旧 unrelated-machines 兼容入口，不是加权拥塞定理、当前工作指令或复杂度结果。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/prompts/TEAM.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/prompts/TEAM.md"
source_id: "91c1bb29b3f2c25e9b7f"
source_blob: "d6b65fb35bf2d133f2b0a7cb730871c3d5f9f2a6"
source_sha256: "ae30c5493d6481195b2871e6de2dc1f41578a08b8569093522e563ede5524cff"
source_size: 26374
source_commits:
  - "68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup)"
  - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)"
evidence_manifest: "../../tools/evidence/history-transition-prompts-20261031/source-manifest.json"
---

# 实读范围与文件身份

经 `clean show 91c1bb29b3f2c25e9b7f --out` 完整读取 26,374 字节，并核对两个冻结提交、blob、大小与 SHA-256。两个提交的正文相同。源文件标题是“不相关并行机共同研究提示词：兼容入口”，开头说明它是旧 `weighted_congestion_frontier/prompts/TEAM.md` 路径下的完整 `UM-TARGET-v1` 主研究提示词，规范版本已迁移到 `unrelated_machines/BOSS_START.md`。

它与已归档的 `CLEANER.md`、`EXTRACTOR.md`、`MODELS.md` 三份角色/模型提示不同：TEAM 是一份完整 boss 研究提示，另外三份只承担清洗职责、提取职责和模型配置。原字节保存在[提示词证据包](../../tools/evidence/history-transition-prompts-20261031/TEAM.md)，来源清单和 SHA 在同目录 manifest 中。

# TEAM 提示词实际承载的内容

## 模型与反面研究方向

TEAM 完整写出一般 unrelated parallel machines 的 (R\|C_{\max}) 模型：机器与任务数量可增长，处理矩阵为二进制非负有理数并允许不可用的 \(\infty\)，任务不可拆分且必须实际分配到一台可用机器。它固定
\[
  C_{\max}(\sigma)\le(2-\varepsilon)\operatorname{OPT}(P)
\]
的精确量词为“存在统一 \(\varepsilon\) 和确定性总位多项式算法，对所有合法输入输出实际分配”，并保留零任务、零处理时间、单可用机器、极大分母和 \(\operatorname{OPT}=0\) 的边界。

迁移时点的用户方向是反面总攻：在明确写出的 (P\ne NP) 或其他复杂度假设下，逐固定 \(\varepsilon\) 寻找真实近二整数 gap、完整 YES/NO、低负载调度 decoder 和总位复杂度；固定比例 hardness、配置 LP gap、有限搜索、未证的自定义假设或“没有找到算法”都不等于全量词反面。提示词同时要求保留正面算法、障碍和局部结果，明确它们不能替代一般目标，也不能把 `UM-TARGET-v1` 的 OPEN 状态升级为已解。

## 研究与协作合同

TEAM 要求 boss 带领自己的 subagents，直接进入证明、构造、反例和来源核查，不先等待 Route Card、审批或固定角色配额；成熟候选再做独立攻击。它规定独立 clone、旧 save 保持绑定、程序统一使用 `work.py`，外部凭据不进入 URL/正文/日志；并要求把正文、算法、代码、输入、证据、Claim、地图和来源对照一起保存。

提示词明确区分 Truth、Value、Novelty、Mechanism、Ambition，区分 Paper Fact、Interpretation、Hypothesis、Observation、Evidence 和 Canonical Record。有限实验、配置 gap、特殊机器数、随机/准多项式结果、局部反例和路线障碍可以保留，但不能冒充一般 (2-\varepsilon) 算法或全量词困难性。改变模型、量词、假设或结论必须建立新 Claim/version 并说明关系。

## 保存与核验边界

TEAM 要求沿“总入口 → 本题地图 → 精确 Claim → 正文 → 独立审查/代码/证据”读取；更新受影响的 README、Claim、review status、assets、graph、catalog 和 source crosswalk。计算需保留精确输入、参数、seed、软件版本、精度、误差和未检查范围；审查要记录冻结 commit/hash 与仍存 objections；只有 checkpoint 回执为 `pushed` 才能报告远端保存。真实冲突保留双方，不强推、不用 ours/theirs 代替数学判断。

这些是历史生产和证据纪律，不是加权拥塞或不相关机算法的证明。TEAM 的 `Cd/\ln d`、near-two、配置 gap 等词只说明当时的研究分流和障碍；任何数学真值必须回到当前 `archives/unrelated-machines` 的定义、定理、审查和 evidence。

# 与现行结果树的比较

- 旧 TEAM 的主目标和入口已经由当前 `archives/unrelated-machines` 的模型资料、研究入口和新版 `BOSS_START`/`RUNBOOK` 分担；当前清洗工作使用结果分支 `rebuild/research-v2`、显式 Boss 编号和 `clean claim/done`，不执行 TEAM 的旧 `main`/旧角色路由。
- `archives/weighted-congestion/state/资料/历史角色提示词三件套--资料.md` 已保存 CLEANER、EXTRACTOR、MODELS 三份较短历史提示；本对象补足 TEAM 的完整 boss 研究合同，不把四份文本合并成一个数学对象。
- `archives/weighted-congestion/state/审查/历史拥塞运行手册与新题路由处置--审查.md` 保存旧 RUNBOOK 的运行路由；TEAM 与 RUNBOOK 互补，前者是研究目标/证据纪律，后者是保存和兼容程序细节。
- 现行 `archives/unrelated-machines/README.md` 和其 canonical state/evidence 承载当前目标与 OPEN 状态；旧 TEAM 的 `P\ne NP` 假设、反面优先级、角色列表和旧路径不构成今日数学结论或用户指令。

# 处置与第三阶段边界

处置为 `integrated` 历史兼容资源：它有独有的完整 boss 提示和精确 UM 量词/证据纪律，不能只标 `duplicate`；但它也不是当前运行指令或数学证明，不能标为当前 theorem/algorithm/obstruction。第三阶段如建立关系，只能记录“历史 TEAM 入口 → 当前 unrelated-machines 模型/审查入口”的资料关系；不能由提示词文字建立 `derives`、`attacks` 或 `checks` 数学边。后续若要复现其中的复杂度方向，必须在当前 canonical 目标下独立写出归约、decoder、假设和位复杂度证据。
