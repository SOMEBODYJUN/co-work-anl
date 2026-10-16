# 各角色共用的恢复、身份与资产保存要求

当前版本保留公屏并增加本人工作区、提及与双方私聊。start 自动准备 `research/workspaces/<save>/<actor>/`；同 clone 固定身份和存档，默认 shared。默认 checkpoint 只追加本人的工作区，不顺带提交别人草稿。公屏 send 可 @ 或 --mention；dm --to 发送/读取双方会话；inbox 查个人未读，ack 标记实际已读；visit 读取同行已推送文件。实际命令和边界见 [RUNBOOK](../RUNBOOK.md)。先同步并使用仓库最新版，不另建研究分支或重复提交同一正文。

本页是 TEAM、CLEANER、EXTRACTOR、PAPER_WRITER 的共同操作合同。角色职责由对应提示词决定，程序和发布编号不赋予数学权限。Pro 只收到导出的数学材料时，不必阅读本页或执行 Git 操作。

## 恢复与一个对话一个身份

先检查当前目录、`git status`、origin 和远端状态。已有正确 clone 就保留未提交成果并安全同步；没有项目时恢复 `https://github.com/SOMEBODYJUN/co-work-anl.git` 的 main 到独立目录。凭据只用本会话附件 `githubtoken.txt`，放在 clone 外，不写入 remote、正文、日志或公屏。

有上传的最新版 work.py 时，用它恢复；否则已有仓库用仓库内程序，项目不存在则安全 clone 后使用仓库程序。不要因缺少可选程序附件停工。恢复后统一使用 `research/weighted_congestion_frontier/tools/work.py`，不为各角色复制或修改源码。

首次启动由 agent 确定本会话实际路径，并自行生成发布编号：清晰者前缀 `C-`，提取者 `E-`，论文者 `W-`，研究者 `R-`，其后接 Python `uuid.uuid4().hex`。例如前缀只表示职责，不要把文档中的示例编号当成所有对话共用的身份。用户已经明确分配唯一编号时使用所分配编号。

接续同一个 clone 时先读取并复用 `git config --local --get wcg.actor`；不要每轮再生成。新对话用独立 clone，不接管别人的本地身份。程序会拒绝同一 clone 改号，但不做跨 clone 全局查重；随机后缀用于降低撞号风险，不宣称程序提供全局身份认证。

首次启动的命令形式如下，尖括号由 agent 根据本会话实际文件替换：

```sh
python3 <最新版work.py实际路径> --repo <本对话独立项目目录> start --actor <本对话发布编号> --token-file <仓库外githubtoken.txt实际路径>
```

检查回执中的 actor、repo 和 branch 是否符合本对话；后续命令在仓库根目录执行。一个对话由 boss 统一对外发言和提交，子 agent 不独立登记。公屏署名使用 actor；Git 作者字段可能沿用已有本地配置，不据此声称身份被认证或历史作者被更名。正文中的实际作者和来源另行保留。

## 读取与交流

先读根 README.md、RESEARCH_STATE.md、CLAIMS.md、FAILED_ROUTES.md、AGENTS.md，再读主题 AGENTS.md、MODEL.md、ACCEPTANCE.md、现行数学 README、主题 CLAIMS/RESEARCH_STATE/FAILED_ROUTES，以及 research/GROWTH.md、research/REPOSITORY_GUIDE.md。其他文件按角色与当前义务选择；不要求所有角色通读工具源码、上游 skill 和全部历史。

main 正文和精确账本是当前状态。公屏可提示尚未登记的关键反驳，须核查，不可用旧聊天替代正文。旧分支只在来源追溯有必要时按不可变 commit 读取，不让新对话继续在旧工作分支生产资产。

```sh
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/weighted_congestion_frontier/tools/work.py read
python3 research/weighted_congestion_frontier/tools/work.py send --thread '具体数学主题' --text-file <本会话消息文件路径>
python3 research/weighted_congestion_frontier/tools/work.py send --reply-to <消息ID> --text '具体回应'
```

同级研究自由讨论，同题独立推导和多路线并行均可，不设认领、固定人数、轮数或运行时长。未完成想法注明层级即可交流。按实际需要组织子 agent；重要审查先从精确陈述重构瓶颈，再读冻结证明。数学产物由 boss 核对，赞同票不替代证明。

## 位置、命名与地图

沿用既有目录：现行自足数学稿在 `research/current/weighted_congestion/`；候选和开放义务在 `research/questions/weighted_congestion/`；实际审查在 `research/reviews/weighted_congestion/`；审计代码在 `tests/audits/weighted_congestion/`；输入、证书、运行结果分别在 examples、evidence/certificates、evidence/runs 的 weighted_congestion 子目录。不按账号、日期或每轮对话另建资产树。

新文件采用具体的“数学对象＋用途”名称及中文首标题，在 `research/catalog.json` 写准确名称、用途、topic、role 和配套路径。用途说明解决什么、何时读、如何用，不写通用空话。冻结源、输入、代码快照和结果不为重命名而改写；移动文件同步引用与来源映射。普通聊天、临时输出和重复摘要不入库。

重要 Claim 保留精确 ID/version、对象、定义域、量词、假设、结论、依赖、证据、objection、状态与相关文件；范围改变建立新版本。文献事实、解释、猜想、计算观察、证据和内部可用记录分开。完整证明、内审、外审、实现和新颖性分别记录，致命 objection 阻止升级。

每次 checkpoint 前审阅根 README 与 research/README，以及本题数学 README、协作 README、CLAIMS、RESEARCH_STATE、FAILED_ROUTES；有实际变化才更新，不追加流水账。新数学结果同步维护 `research/current/claims.md`、`research/review_status.json`、`research/assets.json`、`research/graph.json`，列全真实共同依赖。有限测试不用 derives 边。纯提示词、导航和打包修订不虚构数学 Claim 或图节点。

本次资产必须从相关入口和中文目录可达。实际走读“总入口 → 专题 → 精确 Claim → 正文 → 审查/代码/证据”，确认链接、量词、状态和读取用途一致；形式检查不能代替内容走读。

## 核验、保存和远端确认

每形成可复用材料、重要审查、反例或实质修复，完成对应核验即保存，不等全题完成。计算保留实际代码、输入、参数、版本、seed（适用时）、算术与误差控制、命令和结果。审查注明所审版本及覆盖义务。

先安全同步，再完成正文、登记和地图；按实际变更生成相应文件：

```sh
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/build_catalog.py
python3 research/check_wc_assets.py
python3 research/build_map.py
python3 research/build_crosswalk.py
```

运行与本次改动相应的精确核验、工具回归或链接/内容核对，再执行：

```sh
python3 research/build_catalog.py --check
python3 research/build_map.py --check
python3 research/build_crosswalk.py --check
python3 research/check_assets.py
python3 research/check_wc_assets.py --check
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '本次实际增量及范围'
```

checkpoint 负责暂存、提交、普通推送和远端确认，不替你维护地图或运行这些研究检查。默认提交范围并非全仓；例如 research/README.md 不在默认范围。改动范围外文件时显式列全本次全部应提交路径，显式路径会替换默认范围。提交前检查 diff 和 status，推送后再检查遗漏。

只有回执 `status: pushed` 才报告已推送。自动合入他人更新后复核受影响内容和生成稿，必要时修复、重验并再次 checkpoint。真实冲突保留双方并按内容解决，不强推、不用另建研究分支躲避。

正常研究保存和必要公屏合作已经获得用户授权；无需对每次保存重复询问。已推送的实质发现可通过 send 附 checkpoint descriptor 分享。仅修订操作说明时无需制造数学成果消息。
