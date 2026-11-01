## R-1c6e：未填写研究内容的工作区容器

源 `7269fd34dc65405db134` 的README全文653B、15行，研究存档为 `unrelated-machines`，发布身份为 `R-1c6e4b8ee8e244459a04f106c812a2c2`。其“当前研究”仍是要求作者填写准确问题、定义/命题版本、表示与卡点的占位说明；没有实际问题、命题、推导、卡点或下一步。“可访问材料”只建议按需在 `notes/`、`experiments/`、`candidates/` 保存并链接材料，没有具体材料链接，不能由目录建议推断存在实验或候选结果。

“成熟资产沿既有规范入库，此处链接正文，不重复复制”记录备份和共享数学正文之间的职责。“交流与状态”允许经同一work.py私聊旧发布身份、同行访问已推送材料，并以checkpoint实际确认pushed为跨clone可见性条件；它没有给一次实际推送回执，也不认证数学正确性。与已保留的R-0aeb空模板逐字比较，替换actor后文字完全相同；这是模板内容重复，精确actor及其配套instance仍需保留，不能用另一作者文件替代本原件。

配套 `8df35936cf8c7e2d597a` 是149B、6行的完整四键JSON：`schema` 为整数1，`save` 为 `unrelated-machines`，`actor` 为上述完整发布身份，`instance` 为 `d66ed5b0549449448e5e7007d270cc2d`。README与JSON的actor/save一致。四键仅记录历史容器及相容性标记，没有题目版本、模型型号、日期、分支、数学状态或角色字段；instance不代表调度实例、凭据或当前进程授权。当前根 `workspace_init` 仍检查四键、整数schema、save/actor及32位小写十六进制instance，相异instance要显式resume，已有README不覆盖；这是恢复合同的相关比较，不是本次恢复旧身份的操作。

冻结inventory在这个精确actor前缀下只列这两源；本次精确actor/instance检索未发现正式数学对象引用。该结论只涉及可见冻结材料，不断言作者在其他位置没有研究。两源以 `retained` 保留为身份资料和未填模板状态，不创建数学算法、实验或未完成idea对象。[README原件](../../tools/evidence/historical-workspace-identities/original/7269fd34dc65405db134/README.md)与[四键原件](../../tools/evidence/historical-workspace-identities/original/8df35936cf8c7e2d597a/workspace.json)分别保存，两个冻结提交中的同一源不算两次独立证据。

## R-2101：机器固定倍率公共尺寸的未知容量接续

源 `97aa1010113a81a7b0be` 的README全文736B、11行，历史研究身份为 `R-2101fd5fab2d47a8883de5ee245616f0`，存档为 `unrelated-machines`。与空模板不同，它明确记载本轮已将机器固定倍率公共尺寸的未知容量精确接口整理入库，并准确指向正文 `unknown_target_common_multiplier_exact_repair.md`、独立审查 `unknown_target_common_multiplier_review.md` 和Fraction脚本 `unknown_target_common_multiplier_exact_repair.py`。本工作区不重复保存已入库正文和脚本，主目标 `UM-TARGET-v1` 仍OPEN。[README原件](../../tools/evidence/historical-workspace-identities/original/97aa1010113a81a7b0be/README.md)保留这三条旧相对路径。

其数学接续落在[机器固定倍率残余任务的精确阈值](../算法/机器固定倍率残余任务的精确阈值--算法.md)，稳定身份 `UM-COMMON-MULTIPLIER-UNKNOWN-B-EXACT-v1`。输入是冻结核心的非负有理负载 `f_i` 与完整残余资格图；有限零端任务先放零端并移出，剩余每任务有正有限端。每资格连通分量C满足 `p_ij=a_i q_C`，其中 `a_i,q_C>0`；等价地，同一机器在所有残余资格边上的实际时间恒为 `s_i`。给定这项可检查结构，候选峰为 `f_i+s_i t`（`0≤t≤|U_C|`）。候选B先检查冻结峰guard，再取各机器容量 `min{|U_C|,floor((B−f_i)/s_i)}`；资格二分图整数满流与完整残余分配等价。排序候选求首个满流阈值，各分量取最大并保留孤立机器冻结负载，空残余直接返回完整冻结峰。这关闭了受限结构中的未知B精确生成，未从一般矩阵生成核心或该结构。

源主稿的“同组件两种公共尺寸就拒绝”须按现有算法正文的精确解释接续：q与机器倍率有共同缩放自由，可以任取 `q_C=1`；不能因外加两个尺寸标签就拒绝真实行常数矩阵。失效点是实际同机时间随残余任务变化，此时一般多尺寸不可拆分任务不能按件数槽免费流化。结构检测失败只表示接口不适用，不推出一般原实例 `OPT>T`。冻结峰guard、空残余、孤立高核心和零端分支也不能省略。

[共同容量修复审查](../审查/共同容量修复的判定与实现边界--审查.md)和[有限精确核验](../计算/共同容量与未知阈值的有限精确核验--计算.md)分别承载证明审查与实际运行范围。已实读冻结正文、审查和脚本：脚本seed=2101，生成400个 `m=1..4,n=0..6` 的小实例，用真实完整分配枚举oracle比较各候选的递归容量匹配，另核guard及不同q的不交组件；其 `candidate_opt` 顺序扫描而非二分，不含通用结构识别器或完整大规模调度后端，实现轴为 `audit_only`。原审查的运行/编译记录和既有清洗的复跑记录保留原执行归属，本次新增程序运行数为0。有限核验、受限数学算法、内部审查、外审和新颖性分开；本README没有新增认证，也没有一般统一次二保证。

本次冻结inventory与可见manifest只定位到该actor的README，没有可据以声明配套四键值的来源；因此不补写其instance或配对metadata，也不对未认领metadata登记完成。本源保留为具体数学资产的历史导航与版本边界，不另立同义算法定理，不更改当前Boss身份或六人SPE任务。
