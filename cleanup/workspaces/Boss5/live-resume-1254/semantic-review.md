# 个人空白工作区 README 与身份元数据：完整语义清洗

本稿为 Boss5 内部整合草稿。已完整读取两个恢复文件；没有改共享正文、执行 Git、联网、claim 或 done。按父 Boss 最新整合安排，两源写入统一资料对象《不相关机历史工作区的身份与接续边界》，不新建定理、算法、候选或实验对象。

## 来源身份与字节核验

|源 ID|冻结路径尾部|字节／行数|冻结 blob|SHA-256|
|---|---|---|---|---|
|`1254c0254ceb82d8b6b7`|`R-0aebcce9ae5842fdb1be78207a977265/README.md`|653 B／15 行|`ec6854ff73577984ac024d1c7a2195374a568933`|`45179122a6fd97736092ff7b4013dac141079326ea738fd08a244048e05b6032`|
|`49da93c86a94d8f7adf8`|`R-0aebcce9ae5842fdb1be78207a977265/workspace.json`|149 B／6 行|`75c6d9805c824386cfc2e8357c45ca80e3d1d513`|`029203bfd28d64bc87b6ac1106ffff25cb2ec12a30e19f725198c13a431e2941`|

完整路径前缀均为 `research/workspaces/unrelated-machines/`。`cleanup/inventory.jsonl` 中两个源均由冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 共同定位；它们不是两份不同内容的数学版本。本次恢复文件的实际字节数和 SHA-256 与冻结清点一致，故不是截断前缀或摘要替身。恢复路径分别为 `/workspace/scratch/9cf2a96299f5/boss5-source-1254.md`、`/workspace/scratch/9cf2a96299f5/boss5-source-49da.json`。

## README 逐段实际内容

1. 第 1、3 行把该个人区标为 `R-0aebcce9ae5842fdb1be78207a977265` 的研究工作区，研究存档是 `unrelated-machines`。这是历史身份和存档绑定，未描述任何机器、任务、客户、博弈、证明或算法。
2. 第 5—7 行的“当前研究”只有占位指令：“在这里写准确问题、采用的定义/命题版本、当前表示与卡点。”源作者没有填写具体问题、定义版本、表示或卡点。不能根据标题推断其已经研究过某个不相关机器构造。
3. 第 9—11 行的“可访问材料”只是允许在 `notes/`、`experiments/`、`candidates/` 保存有接续价值的材料，并要求成熟资产进入既有正式位置、工作区链接正文而不重复复制。这里出现的三个目录名是模板建议，不是这些目录已存在、含有实验、或其中候选已成立的证据；本文件也没有一个实际材料链接。
4. 第 13—15 行的“交流与状态”声明可经同一 `work.py` 私聊该发布身份；他人可读已推送材料；本地草稿须完成 checkpoint 并确认 pushed 才对其他 clone 可见。它记载旧工作流的可见性条件，没有私聊实录、推送回执或已保存数学成果。可见性不等于数学正确性。

源文件没有附录、尾部数学、数据表、代码或隐藏在正文中的参考链接。十五行已全部读取，不能把占位句当作尚未抽取的研究摘要。

## workspace.json 的四个字段

JSON 的完整内容只有 `schema: 1`、`save: "unrelated-machines"`、`actor: "R-0aebcce9ae5842fdb1be78207a977265"` 和 `instance: "6c503610b032439788ef0dbda024ab52"`。`save` 和 `actor` 与 README 及冻结目录路径一致；`schema`、`instance` 仅补充该工作区格式版本和实例标识。

这些字段既不是数学假设，也不是认证凭据、论文作者身份验证、工作区完成标记或推送证明。这里保留它们作为来源定位信息，不用旧 actor 代替当前 Boss5 身份，不据此启动旧任务。

## 实际全仓相关比较

已全文读取并比较的文件如下。

|比较文件|实际共性与差异|
|---|---|
|`AGENTS.md`、`cleanup/OBJECTS.md`、`cleanup/receipt-example.json`、`cleanup/README.md`|当前任务要求完整实读、保留真实状态、共享正式对象按数学身份组织、完成记录在正文保存以后。旧模板的“成熟资产入库并链接正文”与此相容；旧发布身份不替代当前 Boss 编号及 clean 协议。|
|`tools/README.md`（63 行全文）|当前工具仍区分本地材料、checkpoint/pushed、共享可见性及正式源处置。README 的“可以私聊”是历史功能描述，本轮没有发送消息或验证该旧 actor 当前可达。模板本身没有 clean done 所需的语义清洗回执。|
|`archives/unrelated-machines/state/资料/个人工作区恢复规则与旧题路由边界--资料.md`|既有资料对象已保存独立 clone/actor、README 记录问题与卡点、未完成备份、checkpoint/pushed、visit 可见性、成熟资产链接正式正文等一般规则。本源增加的是一个具体的空白工作区及其精确身份／元数据，没有新增一般恢复方法。|
|`archives/unrelated-machines/tools/evidence/workspaces-readme-20261031/original/README.md`、同目录 `comparisons/comparison-notes.md`，以及 `cleanup/workspaces/Boss3/receipt-workspaces-readme.json`|中央旧 README 规定新 clone 默认 `customer-attraction`，旧 `shared/unrelated-machines` 保留原绑定，并曾宣布一般人数 Q-CAG-HALF 为当时方向。本源的 `unrelated-machines` 绑定与“旧绑定保留”相容；它没有写停止特殊人数，也没有把工作区迁移到 customer-attraction。原中央 README 的旧方向不能转为本源中的数学研究承诺，亦不能覆盖当前六人 SPE 清洗。|
|`archives/unrelated-machines/README.md`、`问题--问题.md`、`state/定义/不相关机器与两个调度松弛--定义.md`|这些已清洗页面定义不相关机器主目标、统一 ε 与所有输入量词、配置 LP／LST 的分域和原目标未闭合状态。空白个人 README 不含这些数学内容，不能成为突破因子二、配置间隙、困难性或反例的新增证据。这里比较的是已清洗页面，没有冒充已经另读其全部冻结数学来源。|

对精确 actor、精确 instance 和两个源 ID 做了全仓检索，并核对冻结 inventory 相关行。结果中的正命中是 `cleanup/checklists/0051.md`、`cleanup/inventory.jsonl`，以及几个工具保留的冻结清点／路径索引副本；这些命中只是同一来源的目录记录。未在 `archives/`、`map/`、`research/`、`prompts/`、`tests/` 或现存 `cleanup/workspaces/` 的研究正文中发现该 actor／instance 的实质引用。当前冻结清点中该工作区路径前缀只有 README 和 workspace.json 两个文件，没有可据此继续导出的 notes、experiments 或 candidates 文件。

这是对当前材料集合的检索结论，不能推成“该研究者在任何时间、任何位置都没有研究”。也没有因检索无命中而声称完成全仓 10,921 源的数学审查。

## 独有内容、状态和历史纠错边界

本源可保存的独有内容是：具体 actor 与 `unrelated-machines` 的旧绑定；README 三个空白栏目和其实际占位状态；对应四字段实例元数据；该实例未在本文件链接实际数学材料。一般工作区纪律已在既有资料对象保存，因此无需复制成另一篇同义资源对象。

没有数学候选、定理、条件结果、有限实验、实际反例或源作者的数学宣称需要重新推导。唯一源作者宣称是工作流可见性和交流方式，已明确区分为历史流程说明而非本次独立功能核验。

本次没有发现源内数学错误，也没有找到一个需要改写的数学结论。需要防止的历史误读是：把占位“当前研究”当作成果；把 `unrelated-machines` 目录绑定当作当前主攻命令；把 checkpoint/pushed 当作数学通过；把中央旧 README 的一般人数 Q-CAG-HALF 方向倒灌进当前六人目标。上述均是解释边界，不声称这些误读曾由本源作者实际作出。

## 建议归类与接续

建议将两源以 `retained` 处置，整合到父 Boss 统一的 `archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md`。现有 `personal-workspace-recovery-routing-boundary` 资料对象承担中央 README 的一般规则，本源提供具体空白实例的来源增量；统一资料可链接该既有资源解释一般恢复纪律。整合时保留两份原文件的准确指纹和路径，明确“空白模板、非数学成果”；不新增数学对象、不改不相关机器主目标状态，也不建立数学推导或反驳边。

关系判断限于来源／恢复元数据：README 说明工作区意图和可见性规则，workspace.json 核对 save/actor/instance，既有资料对象解释其旧路由边界。若后续图登记，应把它们作为该资源对象的来源证据，而不是与调度定理建立因果关系。具体可插入正文见 [integration-note.md](integration-note.md)，逐源草案见 [receipts-draft.json](receipts-draft.json)；正式整合、checkpoint 和 done 由父 Boss 串行执行。
