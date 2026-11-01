---
id: unrelated-machines-historical-workspace-c166-identity
kind: resource
type_tag: 资料
title: 资源畸变研究工作区的四字段身份与版本边界
status: integration-draft-complete-read
summary: 完整解释旧工作区 c166 的 schema/save/actor/instance，核对两冻结根程序及当前路由；旧 boss21 身份和 README 数学指向均只作来源资料。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-0bbb78b7ca994fa99daee018cb914ebe/workspace.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-0bbb78b7ca994fa99daee018cb914ebe/workspace.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-0bbb78b7ca994fa99daee018cb914ebe/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:work.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:work.py
---

# 来源与归属

本稿供父 Boss5 并入 `archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md`。它仅是独立整合稿；本次没有修改共享正文、运行旧工作程序、发消息、改 Git 配置或执行 clean。内部执行身份是 Boss5，旧标题中的 boss21 和旧 actor 只按历史数据保留。

源 `c1661b95bed75f84f298` 是 149 B、6 行的完整 JSON，冻结 blob 为 `574292540b743639ecaa9bdf60d18c379c3b3379`，SHA-256 为 `8248c8f803a731c21891741665a610347dbcb649163181cd9ac008306eb330bc`。`cleanup/inventory.jsonl` 将相同 blob 登记到 legacy-cleanup `68fad804ec5946cb296f77dc5b336308a66abf12` 和 main `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 两快照；这是同一原件的两条出处，不是两个独立证明或两次执行。原字节在本目录 `original/workspace.json`，配套 README 全文在 `original/companion-README.md`。

JSON 全部内容是以下四个键；没有省略数学正文、程序结果或附加字段。

| 字段 | 原值 | 真实语义及不能推出的内容 |
| --- | --- | --- |
| `schema` | 整数 `1` | 工作区 profile 的四字段格式号。冻结程序要求精确 `int` 1，不接受布尔值替代；它不是 active_research schema、目标版本或数学认证等级。 |
| `save` | `unrelated-machines` | 当时个人工作区的主题分区。冻结 `workspace_path` 将它与 actor 拼成 `research/workspaces/<save>/<actor>/`；它不是文件分支、公屏分支、模型证明或当前默认任务。 |
| `actor` | `R-0bbb78b7ca994fa99daee018cb914ebe` | 当时用于个人路径及署名路由的安全发布标签，与目录和 README 固定 actor 一致。它不是实际用户认证、权限凭证或数学作者独立性的证明；也不能直接把其含义改写为本次 Boss5。 |
| `instance` | `5b647a702cb14136b2c1642d5a15e30c` | 同号工作区的 32 位小写十六进制实例标记，供恢复时发现冲突并要求显式 `resume`。值形状合规不证明该字符串确由某次 UUID 生成、何时产生或谁拥有它；它不是论文版本、源码 hash、运行种子或凭据。 |

此 JSON 不含 branch、board、role、时间戳、Claim ID、truth、审查状态、完整性状态、推送回执、工具版本、依赖列表或数学公式。配套 README 自述 `main / unrelated-machines`，可作为历史文字事实保留；不能把 `main` 读成 JSON 第五个字段，亦不能仅凭这些字节认证运行时本地绑定或当前分支。

# 已实读的版本合同

两冻结根 `work.py` 均已实际完整读取。main 版 `d9b5b49ab665613450d6` 为 26,199 B/522 行，SHA `6946299455b653526a548d7108a29480ab328acf7cc4392bfa6959e870229f1d`；legacy 版 `3c0404b7974eca538863` 为 31,695 B/618 行，SHA `bc2cfda7fc2b12b7fa21d75b1266a14bc6993a40e6a31cc90e0f8eb88b301c4e`。二者原件已在 `tools/evidence/frontier-collaboration-and-root-lifecycle/original/`，无需重新导出或执行。现行根程序只作为当前路由的合同比较，实读覆盖第 1–660 行，其中本源承重段为 actor、save_id、workspace_path、workspace_init、visit 和 start；未把它当作冻结源，也未声称全 727 行程序已运行。

两旧程序的 `workspace_init` 都要求 profile 为恰含四键的字典，schema 是整数 1，save/actor 与调用参数一致，instance 是小写 32hex。若文件已存在且格式或绑定不相容，就拒绝覆盖。若旧 profile 的 instance 与本地实例不同，非 `resume` 拒绝；显式 `resume` 采用旧 instance，再写入本地 `wcg.instance`。只在不存在时排他创建 profile/README，已有草稿不被模板覆盖。源码生成新 instance 时使用 `uuid.uuid4().hex`，但不能由这个机制反推本源的历史执行已发生。

`save_id` 与 `actor` 主要从显式参数/环境/本地配置取标签并拒绝不相容改绑；这些是程序路由保护，非服务端身份验证。旧 `actor` 允许缺省随机 `R-UUID`；现行 `actor` 已去掉随机回退，且当前 start/协调策略要求明确 Boss 编号，同一旧对话迁移有显式 `--adopt-legacy` 分支。此次清洗不调用该迁移、不把旧 R 标签绑定到 Boss5，也不试用源 instance 恢复别人的工作区。

| 控制 | main 冻结版 | legacy-cleanup 冻结版 | 当前已读合同 |
| --- | --- | --- | --- |
| 工作区路径 | `research/workspaces/<save>/<actor>` | 同左 | 常规 `archives/<save>/workspaces/<actor>`，清洗为 `cleanup/workspaces/<actor>`；可有明确子存档 |
| 准备工作区的文件分支 | 固定 `main` | 本地绑定目标 branch | 绑定结果分支，当前默认 `rebuild/research-v2` |
| 新会话默认任务 | `customer-attraction` | 长期清洗分支取 `repository-cleanup`，main 兼容仍取旧默认 | 新长期分支默认 `repository-cleanup`；旧绑定不由本源改写 |
| 身份缺省 | 可随机 `R-UUID` | 可随机 `R-UUID` | 不再自动生成发布身份；当前明确 Boss5 |
| `visit` | 读取 origin/main 已推送普通文件 | 默认绑定 branch，可显式另 branch | 当前路径及绑定 branch，不以本地草稿替代远端发表 |

`remote_directory_exists` 只是 tracking tree 中存在目录，`synced` 是同步关系，均不能代替某批新增内容的 `checkpoint status=pushed`。同样，profile 恰好合规也不能认证这次本地材料已发表、clean done 已完成或任何数学命题为真。上述恢复程序只读源码，没有在业务 clone 上重演；本批无新软件运行证据。

# 配套 README 的数学资料边界

配套源 `722087a0e8ad7b2a0316` 也已全文读，997 B、7 行、SHA `ac2f5d9c3332734842d6a5292763353c43e0316af11e429e3653f3c01aaa0a2f`。其标题是“boss21：真实近二反面与实际调度解码”，自述固定 actor、main/unrelated-machines、六个内部求解者和当时攻击源 gap/物理一致性/放大/复杂度。这些是历史研究编排，不是本轮人数、模型、角色或授权。

README 指向逐资源正权畸变完整 flat 菜单和实际审查，并准确保留：固定 κ 完整 flat 源不能承载任意趋二真实 gap；这是 restricted Santa 工具的结构推论，不是一般 hardness。已全文比较的正式定理 `逐资源正权畸变与κ边界--定理.md` 将这句话展开为完整显式菜单域：有限非空 groups、非空 indexed states、每 state private 总权 `W≤1`、独立 unit resource 机器、每组一个 unit selector，以及全部原 incidences 均存在。κ 只比较同一资源的正 private 权，零项不进入比值。

正式对象对每个固定 α>4 导入完整 restricted-Santa 后端合同，解码全部原 jobs，给出

\[
C_{\max}(\sigma)\le 2-\frac{2-\operatorname{OPT}}{\alpha\kappa}
\le \left(2-\frac1{\alpha\kappa}\right)\operatorname{OPT}.
\]

固定 κ≤κ₀ 的源像类若 YES 有 OPT≤1、NO 有 OPT≥2−ε，且严格 ε<1/(ακ₀)，才有固定有理 separator；这筛掉相应 promise，不能推出任意 UM 易解或一般近二困难性。κ 随精度增长也不自动给 NO。已比较的证明页具体保留 baseline `b=1−W`、OPT=2−V、dummy-free 实际 allocation 与完整原任务回填；审查页保留 α>4 与旧独立重构 α>6 的版本区别及固定有理 separator 修补。JSON 自身没有这些论证，不能取代数学来源。

已比较的双路有限穷举资源把 945 个 bonus 输入和 1301 个独立 baseline 输入、1,328,275 个原调度、20,798 个辅助 allocation 分清。它们是历史有限核验，不是 restricted-Santa 后端的仓库实现，也不证明一般硬度。本次没有重新跑两程序、重新读外部论文或声称新盲审。README 所说“不复制桌面数学资产”只解释旧个人目录的组织选择；数学证据仍以现有 canonical、审查、冻结程序和运行证据各自承担。

README 的 typed-dummy 源筛选只说明“进行中，拟接 mixed-small，保有用范围”；没有提供此处的新构造、证明、完成回执或 typed-dummy 输入域，故仅作为未完成接续方向保留。它明确拒绝把语义 coherence 切片当真实输入限制，真实近二 NO 与任意低载完整原 jobs 的 source decoder 仍是缺口。一般 UM 的 OPEN、当前六人 SPE 的独立目标、外审和新颖性状态均不由本 profile 或 README 升级。

# 全仓比较、独有增量与处置

精确 actor/instance 全仓相关检索未发现本源已进入正式对象；冻结 inventory 有 68 份 unrelated-machines 工作区 profiles，这个计数只用于定位，不冒称逐读其余 67 件。现有 `个人工作区恢复规则与旧题路由边界--资料.md` 已完整覆盖旧 workspace README 的备份/恢复纪律，但没有 c166 的具体四值、同 blob 双出处和 boss21/资源畸变配套归属。`根生命周期程序的绑定同步与版本合同--资料.md` 已保两旧 root 的完整机制，但没有这份 profile 的实际实例。`signed-harmonic工作区身份与版本--资料.md` 是另一主题/actor 的短元数据对象，可比较类型，不可复用其身份或数学去向。

因此本源的独有保留内容是：特定 actor/save/instance 的来源身份，四字段的完整意义，两个快照同字节与两个程序不同版本的区分，当前 Boss5/目录/分支路由的非继承边界，以及由配套 README 接到 flat κ 条件结果和未交 decoder 的导航。应作为统一历史工作区资料中的一个具体条目 `integrated`；不新建数学定理，不复制已存在的资源畸变证明，不因体积小丢弃实例身份，也不把它仅标为重复或未读。

第三阶段可建立两类有解释联系：本 profile 与配套 README 是同 actor/save 的 provenance 联系；统一历史工作区资料与恢复规则/生命周期合同是路由解释联系。README 到既有 κ 定理/审查是来源导航关系，绝非 profile 推导该定理。没有已知 profile 到六人 SPE 命题的数学关系，不造此边。
