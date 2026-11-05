# 2.5第三步与第三阶段：固定执行接口

本轮2.5第二步160群已完成。以下对象登记与建图接口已准备，尚未初始化后续公屏、登记Boss、冻结真实全仓baseline或启动批量建图。原第二阶段56条来源记录仍需核清处置；不能把本轮对象群完成当作全部原始来源已逐源验收。后续按用户指定阶段启动。

## 已固定的原则

| 身份 | 表示什么 | 不替代什么 |
|---|---|---|
| 原来源ID/第一步材料号 | 精确来源版本或一份分类材料 | 不是图节点；来源done不等于数学准入 |
| object_id | 可独立陈述、引用的数学对象 | 不是一文件一编号；不同模型、量词或结论不偷合并 |
| version与SHA/pin | 对象版本、正文/证据字节、审读绑定 | 不是数学真值或新颖性评分 |
| edge_id | 一份解释充分的数学关系/证明支持 | 不是引用、同时出现或文件夹关系自动变成推导 |
| 任务/Boss/run ID | 协作、互斥写入和恢复 | 不进入数学推理投影 |

对象保留已有稳定ID；新增用`research new-id`生成一次M-UUID并随批次保存。路径、类型、状态与研究路线不编码进ID；同一对象改名不换ID，修改记录明确增version。改变精确Claim身份须明确新旧版本/新对象及差异。借鉴的是Pharos/Danus的独立数学事实及按需取证明机制；本库把稳定ID与版本指纹分开，没有谎称照搬其内容hash编号。原始代码依据见[UPSTREAM_ADAPTATION](UPSTREAM_ADAPTATION.md)。

完整定义、一般/条件结论、有效具体反例、可复用方法、具有数学保证的算法、猜想、具体障碍与开放义务都可登记。未证不自动排除；类型、真值、审读与新颖性分开。普通算术、纯身份、日志、PASS、代码与输出不自动作命题；必要附件有数学owner。excluded只是登记去向，不执行删除。正文不因编号被切碎、合并或改写。

## 两套可直接使用的入口

| 阶段 | 完整Boss启动词 | 内部处理者 | 独立运行/公屏 |
|---|---|---|---|
| 2.5第三步 | [02.5-3-register.md](../prompts/02.5-3-register.md) | [02.5-3-worker.md](../prompts/02.5-3-worker.md) | p25-register-v2 / wcg/board-registration-v2 |
| 第三阶段 | [03-map.md](../prompts/03-map.md) | [03-map-worker.md](../prompts/03-map-worker.md) | map-v2 / wcg/board-map-v2 |

新启动参数`--workflow-run`进入`research/operations/<run>/people`与`research/workspaces/<run>/<Boss>`。不改绑旧cleaner/curation-run clone，不复用旧阶段占用；不同阶段可使用同一明确Boss号，阶段内不同对话仍不能借号。配置已发布但公屏/身份只在用户实际启动时创建。旧第二步zip中的work.py不认识新参数，后续交付必须附此分支最新根work.py；现有第二步继续使用其自己的入口。

## 2.5第三步独立闭合

1. 从第二步实际已发布出口形成明确inputs文件：`{scope:"repository"或"partial",coverage_note:"具体覆盖依据",materials:[{path,sha256,catalogue_id?}]}`。不能依据旧数量、分类标签或尚在改写的工作区猜全仓范围。
2. `research freeze --inputs-file ...`固定版本；原件字节不变。全仓scope会核对当前正式材料是否遗漏；第一步材料目录中正式树之外的数学须由第二步明确去向，并列入本轮显式输入。冻结后新增/变更材料定向重判，不覆盖旧baseline。
3. 处理者仅写自己的`research/registration/batches/<id>.json`；一个总集成人负责canonical registry。批次使用schema:2，含objects/materials，edge_files为空。跨批同一对象先保住精确身份，重复/冲突经集成人处理；不能让多个Boss各自重写总表。
4. 总集成人的manifest为`{baseline:{path,sha256},batches:[{batch_id,record:{path,sha256}}]}`。批次先checkpoint，compose核字节并拒绝冲突，随后register候选总表并checkpoint。
5. `research registration-check --final`专门验收登记，不读取或要求任何超边/图。要求明确全仓冻结范围、所有输入去向、当前版本与无未决身份。明确open/conjecture可以登记；needs-decision是尚不能辨认/路由材料的状态，两者不混。

```sh
python work.py research freeze --inputs-file research/registration/inputs.json
python work.py research new-id --count 需要的新对象数量
python work.py research compose --manifest research/registration/batches.json
python work.py research register --record-file research/registration/proposed.json
python work.py research registration-check --final
```

程序不会替人判断数学，也不会自动把对象摘要当完整正文。body/evidence可定位独立段落；证明、条件或定义在别处时引用完整必要位置。程序通过后仍保留准确objections和认识层级。

## 第三阶段质量与多人接口

3A局部对象族 → 3B存档内跨批整合 → 3C明确跨档比较 → 3D单Boss生成投影。按数学关系密度分批，3–5篇只是起点。每个对象都有linked、isolated-after-review或needs-decision及真实比较范围；没有边可以保持孤立，不按边数验收。

任务通过map plan/claim/done/handoff/status。核心对象覆盖与输出路径互斥，共享只读材料可查。正文、边和回执先pushed再done；旧消息、旧handoff或本地草稿不能代替当前远端所有权/交付。这也落实了清洗公屏seq66、68、71反复提醒的边界：来源完成、可领取集合为空、当前有效owner及数学准入各自独立。

多前提保留一条all超边；独立证明是替代支持。逻辑推导、反驳、迁移与启发/引用/实现/有限检查分开。accepted绑定端点身份、证据及关系解释；改动后重判，不把复核过期解释成全部后继为假。有限实验不冒充一般定理，辅助模型反例不冒原模型反例。

总集成人必须同时交两份收尾记录：

- `map/coverage.json`：每个对象的当前object_pin、比较范围、理由及真实incident边。
- `map/integration.json`：`reviewed_by,review_note,registry_pin,edge_pins,archive_reviews,cross_archive_review`。archive_reviews覆盖每个当前存档和子档；每条审读含comparison_scope、outcome、unresolved，最终unresolved为空。单档也可明确说明不涉及跨档，不伪造迁移。

`research check --final/build --final`要求登记独立闭合、对象覆盖和跨批/跨档审读均当前有效，不会因每批各有几条边就自动当整合完毕。开放数学问题可保持开放；这里清零的是尚无处置的关系疑点，不是要求证明所有命题。最终不声称发现所有可能数学联系，只精确声明实际比较范围。

## Work与GitHub资源

Work里的Main可通过现有执行工具调用根work.py；凭据放clone外，用`--token-file`或本clone既存配置。没有另一个必须连接账号的服务或MCP数据库。

| 命令 | 行为 | 当前验证 |
|---|---|---|
| research search/show/context | 元数据定位、实际正文、完整超边按需读取 | 本地真实端到端与专项测试 |
| research init/save/resume | 两类输入、不可变笔记、agent_id、具体反馈和原任务接续 | 已测试；模型创建由Work真实spawn/followup承担，GitHub token不能替代模型能力 |
| github status | 本仓库权限、workflow和本人的本仓库Codespaces，只读 | 本轮真实API成功；无云机器创建 |
| github machines --ref ... | 查看实际机器类型 | 接口已实现，不据猜测选昂贵机器 |
| github dispatch --workflow research-compute.yml --ref ... --inputs-file ... | 明确提交登记实验 | 接口/参数已测试；本轮不调用。接受请求不等于运行通过 |
| github create-codespace / stop-codespace | 明确创建或停止本仓库环境 | 接口与仓库边界已测试；本轮不创建、不停止任何实例 |

本轮实际API读取到仓库admin/push等权限可用、Research tools workflow可读、Codespaces列表可读且为空。没有据此推断学生认证、余额或所有写权限。workflow_dispatch要求workflow在默认分支可用；不擅自把研究分支合入main，未满足时在当前环境或Codespaces运行已登记命令。GitHub额度、限制及官方接口依据见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。

后续Main仍只有两类主要Solver：障碍组与成果组，均空历史启动；Main负责送资料、具体反馈、持续checkpoint。用户让运行哪个阶段时才启动对应阶段，不因为配置已发布而自动开始数学研究。
