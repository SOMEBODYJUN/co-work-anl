# 上一版准入与超图程序原型：不是当前2.5.1/2执行协议

用户已将2.5分为材料定性、数学整理、重新登记三步。本文件保留上一轮程序契约用于后续设计比较；其中一页一ID、最终manifest、accepted边等不约束前两步。新入口见[CURATION.md](CURATION.md)。现在不据此冻结生产manifest或启动第三阶段。

# 2.5 数学内容准入与保全

2.5 处理阶段二留下的冗余、混层、局部错误和承重内容损伤。它可以删除、归附件、修复、合并和重写；原本好的数学应保留。`tools/curation.py` 管固定快照、处置绑定与准入名单，不判断数学真值，也不批量删除文件。

## 两种记录

`cleanup` 的来源处置说明原材料曾如何处理；本层说明**当前哪份数学正文可以供后续研究使用**。完成回执不能替代本层准入。身份、提交和运行履历只在必要机器状态中保留，不因需要记录而另建数学对象页。

数学正文仍是人和 Agent 阅读的权威内容；准入 JSON 是路由和覆盖记录。研究图允许定义、已证/条件结论、精确反例、算法、有限结论、猜想和明确缺口，不能把未知内容当成立前提。计算证书可以承担证明，常规执行统计通常只是附件。

## 操作

设计/审查阶段，阶段二仍有人持续写正式正文，只运行 `scan` 与隔离测试；不在共享分支提前建立全量 baseline/manifest，也不批量删除数学。实际2.5须等阶段二交接且快照稳定后，由 Boss 固定原始快照。在该时机，仓库根目录执行：

```sh
python3 tools/curation.py scan
python3 tools/curation.py freeze --manifest-out research/curation/manifest.json
python3 tools/curation.py plan
python3 tools/curation.py check
python3 tools/curation.py export --out research/curation/admitted.json
```

全仓最终验收使用：

```sh
python3 tools/curation.py check --final
python3 tools/curation.py export --final --out research/curation/admitted.json
```

默认文件为 `research/curation/baseline.json` 与 `research/curation/manifest.json`。`scan`、`freeze`、`plan`、`check`、`export` 支持 `--out FILE`，`plan`、`check`、`export` 支持 `--manifest FILE`；文件参数须是仓库内相对路径，全局 `--repo PATH` 置于子命令前。`freeze` 不覆盖既有基线，要求正式文件与固定 Git HEAD 字节一致；不得先删改原文再造基线。`--manifest-out` 生成全 `pending` 骨架，绝不自动放行。先由 Boss 固定基线，各 worker 只交约定对象群的正文和记录，由 Boss 合并 manifest。程序没有自动批准或批量 unlink 操作。

`check` 的局部通过只表示所填绑定与结构可用，报告仍待处理的范围。`--final` 要求基线全量已处置、无 `pending`、无 `bundle-pending-split`、当前正式文件没有漏覆盖且所有当前 SHA 匹配。后续新增正式数学须明确纳入本轮目标或由 Boss 协调独立增量批次；不能静默改原 baseline、忽略新增文件或用局部检查宣称全仓完成。任何绑定的正文、证据或关系内容变化后，旧声明不再覆盖新版本；必须重审受影响数学，禁止只刷新 SHA 继承批准。

## 最小文件契约

baseline 保存版本、固定提交和当前正式对象文件的 `path`、`sha256`，并可记录解析得到的 `object_id`、`kind` 或 `parse_error`。只收 `archives/<档>/(subarchives/<子>/)*state/` 的正文及相应直接问题入口，不收证据目录里的比较/历史副本。

manifest 结构如下；路径和哈希必须来自实际文件，示例不是可直接提交的数学声明：

```json
{
  "version": 1,
  "baseline": "research/curation/baseline.json",
  "baseline_sha256": "基线文件实际SHA256",
  "objects": [
    {
      "path": "archives/demo/state/引理/对象--引理.md",
      "sha256": "当前正文实际SHA256",
      "role": "mathematics",
      "object_id": "demo/object",
      "statement": "精确数学陈述",
      "conditions": "模型、定义域、量词及承重条件",
      "support": "论证/构造的正文定位，或未付的具体义务",
      "use": "可以复用在哪里、排除哪条推理或界定何种缺口",
      "status": "conditional",
      "dependency_scope": "single-object"
    }
  ],
  "decisions": [
    {
      "path": "基线中的原正文路径",
      "sha256": "基线原SHA256",
      "action": "rewrite",
      "targets": ["archives/demo/state/引理/对象--引理.md"],
      "reason": "确切问题及此行动理由",
      "preservation": "原有条件、证明、构造和独有边界的准确去向"
    }
  ]
}
```

数学对象准入状态为 `definition`、`proved`、`refuted`、`conditional`、`finite`、`conjecture`、`gap`、`algorithm`。未评估内容用处置 `pending`；`unknown` 不能填成已准入状态。对 `refuted` 要清楚区分被否命题和合法反例；被撤回的旧证书不能作真事实。

当前工具按一份正式正文的 frontmatter ID 读取对象，不提供段落子对象登记。对象须声明 `dependency_scope: "single-object"`；复合文稿可先以 `"bundle-pending-split"` 保全文，局部输出会把它改标 `status: "unresolved-bundle"`，原声明另放 `declared_status`。它是待拆阅读容器，不能当整页已证单结论，也不能作已接受逻辑边端点；最终准入拒绝待拆容器。同页若含有独立依赖或不同状态的实质命题，应拆为独立正文/ID。单个证明中的常规运算不因此各立节点。历史审查说 pending 而后继已有证明时，现行入口要接回准确结论，不能保留历史状态作为当前未知。

附件对象用 `role: "evidence"`，给实际 `path`、`sha256`、非空 `owner_ids` 及具体 `use`；owner 是本轮明确准入的数学对象 ID。附件放在正式 `state` 外，不能独立冒充数学前提。

每个基线文件只作一个当前处置：

| action | 数学处理与目标 |
| --- | --- |
| `keep` | 原有数学已经清楚，保留原 SHA 内容并绑定当前正文。 |
| `rewrite` | 修复或重构，写明旧内容全部必要部分的去向。 |
| `merge` | 同机制或同一对象并入权威正文，保留独有条件、证明与边界。 |
| `attach` | 移到正式 `state` 外，作为明确数学 owner 的代码、输入、证书或必要输出。 |
| `delete` | 纯非数学内容，或有确切替代的冗余正式页。 |
| `pending` | 尚未理解/裁定，写出具体疑问，不默认入图。 |

`delete` 另给 `delete_kind: "non-mathematical"` 或 `"redundant"`；后者必须指向实际数学替代目标。除头部正常且明确为 `metadata` 的原件外，直接非数学删除或 `attach` 都须给独立内容分类说明 `classification_correction`，严格包含 `original_kind`、`why_nonmathematical`、`why_no_mathematics_lost`、`reviewed_by`。这同样保护未知 kind、解析失败、计算、程序、resource 和 review；它们可能含完整证明，不能靠类型名绕过保全。原 kind 缺失时填 `original_kind: "unparsed"`。有独立数学内容时应以 `merge` 保留数学目标，并把代码/原输入留附件，不得整份降成另一对象的无关附件。不能以未证明、旧、暂无引用或不在主线为删除理由。数学有损的合并不因文件数减少而合格。

`keep` 要求原 SHA 不变。仅补元数据或格式也应填 `rewrite`，在 `preservation` 说明数学正文未改；不要把保住数学误解为必须逐字保留不兼容格式。

最终验收要求废弃旧正式路径已删除；局部计划阶段可保留旧页供审阅，但不能把未执行计划当完成。处置后须同步当前链接与目标路由，避免旧回执绑住无用空壳。`legacy_target_routes`／`resolve_legacy_target` 供现有工具解析已删除目标的准确去向，绑定本轮基线提交；不能用其返回值证明替代页数学正确。

## 准入与超边

`export` 只输出已声明的 `mathematics` 对象，其中局部待拆容器强制标为 `unresolved-bundle`；没有 manifest 时拒绝默认放行，附件不导出为数学节点。第三阶段默认读取同一 manifest 和按需证据，不再把目录里所有 Markdown 视为节点。草图也要 manifest；最终图另须通过阶段二来源完成门槛。

```sh
python3 tools/maps.py check --structural
python3 tools/maps.py check
python3 tools/maps.py build --draft
python3 tools/maps.py fingerprints archives/demo/map/edges/实际关系--关系.md
python3 tools/maps.py impact demo/object
python3 tools/maps.py freshness
```

第一条仅诊断当前正式候选的结构，不作数学准入，也不生成可用研究图。第二条检查当前准入图；第三条仅生成有明确准入范围的草图。`fingerprints`／`impact` 中的 ID／路径应替换为实际对象和关系，`fingerprints` 不会代写关系或将其批准。`freshness` 只判断当前派生图是否匹配全部当前输入，不判断数学正确；构建前后输入指纹若改变，程序拒绝写出，须在一致快照上重建。

逻辑超边保留联合前提、共同模型、变量对应、条件、准确结论和数学理由。条件依赖尚未解决时标清条件，不能仅因关系审读通过就提升结论真值。来源、实现、有限检查和启发不作已证蕴含。跨模型运输、反驳范围与多版本命题都要明确；语义改变用独立对象身份，不自动改接旧关系。

关系只有 `proposed`、`accepted`、`rejected` 三种审读状态。新 `kind` 在程序与关系协议中登记方向、参与对象作用和适用语义前，只能 `proposed`，不能靠任意字符串生成 accepted 边。已接受关系还必须绑定：

| 字段 | 绑定内容 |
| --- | --- |
| `endpoint_hashes` | 本关系全部端点的 `对象ID:SHA256`，不得夹入无关端点。 |
| `evidence_hashes` | 本关系使用的全部本地证据文件的 `仓库相对路径:SHA256`。 |
| `reviewed_content_sha256` | 本关系数学正文与元数据的规范化内容摘要。 |
| `relation_mode` | `unconditional` 或 `conditional`；逻辑边含未证或已否前提时，只能显式作条件关系。 |

本地证据须已登记为数学正文，或是 `owner_ids` 至少包含本关系一个端点的附件；随意存在的日志不能充当 accepted 边证据。冻结原来源可以用精确 `source:<commit>:<path>#段落` 引用，其版本须属于冻结来源清单。

先完成真实数学审读和将要提交的关系内容/状态，再用 `fingerprints` 机械计算绑定，并对同一版本执行检查。随后改动条件、关系正文、状态、端点或证据都可能使旧绑定失效；重新判断数学，不仅是重算 hash。程序对 accepted 关系导出 `asserts_endpoint_truth: false`，因此条件关系不会自动改变目标真值，也不会撤回目标另有的独立证明。有限前提支持一般结论时仍需实际数学归约，类型检查不替代它。

`impact` 针对实际关系给出待复核范围，返回 `needs-review-not-refuted`；纠错不自动宣布所有后继无效，替代证明仍可能成立。保留精确猜想、失败机制和暂时孤立的实质对象；不为连通而造边。

## 上游要求的适配

- [Danus verify-proof](https://github.com/frenzymath/Danus/blob/codex/agents/skills/worker/verify-proof/SKILL.md)：有实质意义的自足数学事实；常规计算留在证明中；显式定义、量词和依赖。
- [MATEK graph-only state](https://github.com/PhillipKerger/matek-theorem-agent/blob/main/GRAPH_ONLY_RESEARCH_STATE.md)：数学研究上下文和调度身份分离；部分成果、具体失败路线仍可保留。
- [Noemesis index curation](https://github.com/kbr-/math-research/blob/main/research/notes/INDEX_MIGRATION.md)：引用不自动成为依赖；修正、替代和有限证明范围分别表达。

不同项目的认知图范围不同，有的含任务、审查或计算节点。本项目在第三阶段建立的是供数学研究读取的投影：工作流不进入该投影，必要证据按需展开。这里不安装任何上游运行时，也不把 LLM 审读或结构检查说成形式证明或百分之百正确。
