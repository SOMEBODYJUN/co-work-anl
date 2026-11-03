# 2.5 第一步／第二步协作设计

只设计材料定性、非数学清理、对象群蒸馏所需协作。2.5第三步正式登记、第三阶段超边结构和未来数学研究Agent由用户与另一AI设计。当前没有创建新公屏、登记身份、认领任务、发布消息或删除旧工作区。

## 实读接口：能复用什么，尚缺什么

| 现有接口 | 实际可用能力 | 边界／缺口 |
| --- | --- | --- |
| `work.py start --board-branch` | 在独立clone显式绑定新公屏；已绑定clone拒绝改公屏 | 默认仍是旧cleanup公屏，不会因curator自动变更 |
| `start --role curator` | 使用2.5入口，显式Boss，结果分支同步及写端点验证 | 没有step1/step2路由，也没有2.5任务认领 |
| `workspace_path()`、`workspace_init()` | 当前repository-cleanup使用 `cleanup/workspaces/<Boss>`；profile/instance，明确resume | 新curation工作区布局尚未实现 |
| `coordination.register()` | 固定Boss/instance，receive-pack dry-run，checkpoint确认 | 硬编码cleanup/people和cleanup/workspaces，须与新工作区同步修改 |
| `read/send/inbox/pending/retry`、board.py | 新分支独立存储；稳定event ID；丢失响应后实际确认；asset指纹 | 公屏说“负责这批”不产生互斥claim；result消息必须带pushed asset |
| `clean claim/done/handoff` | 仅原始冻结来源版本的事务式认领和完成 | 不能用于认领4千多份当前正文或新对象群，不应重开来源done |
| `curate scan/freeze/plan/check/export` | 当前候选枚举、原字节保全、既有准入manifest检查 | 不是快速材料定性表，也不是新任务队列；不能当作步骤1 |
| `checkpoint`、`--local-only`、`sync` | 明确范围保存、正常推送、远端确认；保留本地草稿 | checkpoint不等于任务完成；新curation路径需显式选择或补默认范围 |

另有一个部署陷阱：当前 `start --save curation-25 --role curator` 会拒绝，因为该save不在RESEARCH_ENTRIES，也没有对应archive入口。根程序read/send自动使用绑定save。`curation-25`可作为新公屏的逻辑save提案，但须程序显式支持，不能冒充当前可用命令。

## 独立运行域（提案，尚未创建）

- 结果仍为 `rebuild/research-v2`，不另造研究成果远端分支。
- 新2.5公屏：`wcg/board-curation-25`；逻辑save：`curation-25`。
- 顶层 `curation/` 只存本轮步骤1/2机器状态与临时协作；与旧 `research/curation/` 准入原型分开，不暗示第三步schema已定。
- `curation/runs/<run>/run.json`：交接提交、运行ID、范围、公屏与步骤状态。
- `curation/runs/<run>/snapshot.jsonl`：材料ID、路径和源SHA。材料ID不是最终数学对象ID。
- `curation/runs/<run>/records/<material-id>.json`：步骤1定性与短理由。
- `curation/runs/<run>/tasks/<task-id>.json`：步骤2对象群任务及互斥可写范围。
- `curation/workspaces/<run>/<Boss>/step1/`、`step2/<task-id>/`：批次输出、未完成推导和交接。

不要在正式state树中另造“材料清单资源页”或工作区身份数学对象。必要机器身份属于后台，不加载到数学研究上下文。

## 第一步：单Boss与六名gpt-6-sol/high

未来由本对话Boss串行登记，六内部代理分别实读互斥批次。内部handle不登记六个公开Boss号。建议初始每批20份常规页；首批测吞吐，长页另列，不许仅按文件数追速度。每人只占当前批次，完成立即补位，不预占几百份。

读当前材料全文即可定性，不核查全套历史、不重新跑程序、不审完整证明。长页分块读完，不以标题、前几行或数字出现次数定性。每条只需内容性质、路由、短理由和具体定位；不强迫填完整数学准入字段。

步骤1输出数学材料清单和清理路由，不宣告真值、不预定超边节点粒度。定性为纯无数学包装者由Boss小批删除并修入口；混合页先保全数学，未知/解析失败/疑有完整证明的计算页不能按类别删。

单Boss阶段无需给每份材料发远端claim：Boss维护当前六批本地分工，串行收回记录并正常checkpoint。分批保存后实际确认pushed，才显示本批已登记；分类完成与删除是否落实分字段，不能把计划当完成。公屏按批次发可用成果和争议，避免4千条打卡消息。

## 第二步：按对象群派发

输入为步骤1的记录、同命题/同机制候选关联、现成成熟正文、具体缺口、可写路径和预算。按数学内容组成任务，不能按“所有含数字的页”机械分组。不同模型/量词可同组比较，输出含义仍须分开。

每个对象群一个当前写入者，所有代理可跨范围读和交流；Boss负责跨文件衔接与同clone的Git。不得让多个内部代理同时改同一权威正文。成熟一组立即整合，不等一轮。无需占主要并发的常驻汇报角色。

给每组探索预算，例如“先一次结构比较，最多两条具体化简/推广尝试；到界交准确保留版本及具体缺口”。不以产生一般定理作为完成条件。成果说明数字的作用、结构、化简/推广、限制；不交执行日记。现成成熟证明不为统一措辞重做。

步骤2不承担全仓correctness audit。改写承重数学须局部核清；可疑处交明确反例/条件/缺口及影响范围。不能把“不全仓审查”理解为可不验证推广，SPE不能省离轨或任意平局。

多Boss分发前增加最小单任务文件事务：固定run和任务ID、源SHA、父Boss、可写路径、request_id、状态。正常push竞争；失败读最新状态，仅当任务仍可领且路径不冲突才重放。先推送并实际读回确认者获claim；禁止force push、聊天代锁或一次预领大量任务。

状态建议：`available -> claimed -> submitted -> completed`，另有blocked/handoff。submitted必须指向已pushed、他人可读取的产物；仅本地草稿只在工作区和交接记录标local-only，不能记submitted。completed表示本步骤工作已落实，不代表证明了新定理。源变更先标stale并核差异，不按旧SHA覆盖。claim、产物pushed、complete三个事实分别确认。

## 新公屏消息边界

thread按 `步骤1/批次` 或 `步骤2/task-id`。复用现有message/progress/help/objection/result，不给board传不存在的新kind。启动只放运行入口、任务表、范围和当前阶段，不复制旧清洗历史。

普通消息只报批次可取用、对象群交付、争议和阻塞。result消息需现有 `{branch,commit,path,sha256}` asset，并指实际正文。身份、阅读量、PASS统计不是数学成果，也不回流正式state。

## 启动与部署顺序

目前只确认旧根程序支持 `start --board-branch`、`--role curator`、`board-init`、`doctor`、`checkpoint` 等单项接口。**暂不发布可复制的完整2.5启动命令**：当前启动仍登记cleanup域，新save也不支持；原样启动会把新旧工作混起来。

正式启动顺序：阶段二交接 → 实现并隔离测试新运行域 → 发布更新后的根work.py及真实启动模板 → 用用户给定Boss编号在独立clone绑定结果分支与新公屏 → 登记身份并验证结果、公屏及新任务状态的写端点 → 固定本轮材料快照 → 小批校准 → 全量定性。公屏由协调Boss初始化一次并读回确认，不从旧分支复制消息历史。现在不执行这些远端动作。

`--resume` 只在确属本对话原绑定且已授权接续时使用；不抢其它对话同号绑定。新路径应显式进入checkpoint范围。不存在的新任务CLI不能写成已经可用；接口规格见 [PHASE25_PROGRAM.md](PHASE25_PROGRAM.md)。

## 暂停、恢复、退役

认证失败停止同凭据重试和新认领；token只作认证，不入日志、remote、消息或文件。保存本地用checkpoint --local-only，明确未共享。

步骤1单Boss暂停：保存已收批次和未收代理文件，释放内部未完成分工，交接下批位置。步骤2多Boss暂停：释放本人未完新任务，记录真实原因、草稿位置、是否pushed及下一步；须补新任务handoff。现有clean handoff只释放旧来源，不能谎称释放2.5任务。

阶段二旧认领按旧流程交接，不搬成2.5任务。旧公屏/旧工作区目前不删除。最终退役先保全仍被数学或必要证据引用的内容，再清掉无用当前树，Git历史留回滚。新的2.5公屏与工作区也是临时设施，完成交接后退役，不进入数学清单。未来研究Agent的协作设施由另行设计确定。

## 正式运行前的最小缺口

1. 新curation运行配置、步骤路由、工作区、登记路径与checkpoint默认范围一致。
2. 步骤1材料导出/收回/覆盖/重复与SHA变化检查；不改旧来源库存、不要求每条远端claim。
3. 步骤2多Boss单任务文件CAS正常push及路径冲突检查；claim/submit/complete/handoff最低闭环。
4. 新公屏逻辑save和实际读写绑定；初始化后读回确认，独立写权限错误明确停止。
5. 材料清单与对象群产物导出保留可迁移字段，第三步和超边schema不在本轮冻结。
