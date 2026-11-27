# 复制给 Pro 的启动消息

使用我在启动消息中给出的完整身份号，之后始终保持原样。编号11不能变成1，数字身份也不能截断；不按日期重分角色。先读`docs/PRO_RUNTIME.md`。在仓库根目录运行`python work.py session start --actor <我给出的身份号>`，默认工作区是`work/<完整身份号>`；已有指定路径就用全局`--workspace`恢复它。下面所有研究、模型、阶段和提交都针对这一工作区。此命令只恢复状态，你必须继续实际执行研究。

必须形成明确主判断，并说明机制、时间窗口和家庭行动含义；不得以防御性话术回避裁决。允许按科学建模规范建立评分或概率模型，禁止任意赋权、未经检验把分数映射为概率和虚报精度。

检查已有clone和工作区；存在时运行状态命令恢复原断点，不覆盖或重复创建。新环境直接克隆本项目的公开分支：

```bash
git clone --depth 1 --single-branch --branch work/cn-crisis https://github.com/SOMEBODYJUN/co-work-anl.git cn-crisis
cd cn-crisis
python bootstrap.py --research
.venv-methods/bin/python work.py methods doctor
```

若使用附带的 `CN_crisis_workbench.zip`，先解压并读取其中完整源码；也可通过包内 `repository.bundle` 建立真正的Git clone：

```bash
git clone --branch work/cn-crisis /解压目录/cn-crisis/repository.bundle cn-crisis-run
cd cn-crisis-run
git remote set-url origin https://github.com/SOMEBODYJUN/co-work-anl.git
python bootstrap.py --research
.venv-methods/bin/python work.py methods doctor
```

若直接使用解压的源码目录，先 `git init -b work/cn-crisis` 建立本地提交历史；不要覆盖已有Git工作区。本地提交使用当前Git身份；若新clone没有身份配置，则设置本仓库研究身份 `git config user.name 'Research Workbench'` 与 `git config user.email 'research@users.noreply.github.com'`。公开读取本分支不需要令牌。后续推送使用已给的仓库外凭据，不把凭据写入项目或结果。已有工作区先用 `.venv-methods/bin/python work.py --workspace work/<实际run> status` 读取状态，再接续。

完整读取 `prompts/00_PRO_FIRST.md`、`docs/WORKFLOW.md`、`docs/RESEARCH_DESIGN.md`、`docs/AGENT_PLAYBOOK.md`、`docs/SCIENTIFIC_MODELS.md`、`docs/VIEWPOINT_PROGRAM.md`、`docs/METHODS.md` 与 `prompts/05_CALCULATOR_SPEC.md`，专题派工使用 `prompts/06_SPECIALIST_TASK.md`，再读 `inputs/01`—`05`。用仓库自己的 `work.py` / `crisis.py` 统一入口恢复或创建首轮工作区，按真实20阶段完成资料、观点方法学习、专题分析、可修改因果超边、测算、对抗裁决、报告写作、离线计算器、独立复核与发布。每个实质批次保存，阶段结束提交；必要时用真实子代理独立研究与复核。

同时读 `docs/THINKING_FRAMEWORKS.md`、`docs/ANALYST_LEARNING.md`、`docs/MODEL_PROGRAM.md` 和 `docs/COMPUTE_BUDGET.md`。从稳定分析动作与制度约束学习，更新当期结论；先跑已接好的历史训练和银行核算，读取真实成绩及未通过项，再部署中国研究实验。使用 `compute plan/run` 保存实际输入、模型输出、代码版本和预算检查点，断点后恢复。必须作出主判断，不能只列无排序情景；不用扩大模型数量代替调查、数据和机制研究。

使用Codespaces时，按计算预算文档的实际CLI连接步骤核对终端、仓库外认证、实例分支、空闲超时和本批预算；不能仅凭提示词宣称已连接。计算批次结束同步产物并主动停止对应实例。若当前执行环境具备本地CPU运行条件，也可原样执行仓库方法，明确登记实际运行位置。

本次授权先完整贯通首轮。按`docs/RESEARCH_EXECUTION.md`分别使用数值模型、作者思考框架和机制超边；长期学习问题意识、约束和分析动作，当期观点随新事实修订。模型差就明确拒绝该用途并继续经济裁决；情绪词、目录盘点、接口测试和合成用例不能当完整分析。每批实际研究或运行，保存文件，读取`session next`的缺项并继续修复、补采和复算。

实际完成检查后，按`examples/acceptance-template.json`结构写工作区的`research/acceptance.json`，不得预填通过。将验收记录和所有引用的检查证据纳入当前独立review，用完整身份号作`--author`，实际独立执行者作`--reviewer`，然后发布同一版本。持续执行`session check --actor <完整身份号>`；只有`complete: true`才按完成交付停止。未通过就处理具体缺项，不停在计划，不请求重复授权。遇到实际环境、输入或权限阻塞，保存可恢复断点并报告未完成，不能自造通过或承诺脱离执行环境无限运行。

选定上游工具、适配器和使用说明已在本仓库；先运行自己的工具并读取已有检索与事件记录，复用适用资料。新材料通过 `targets` 挂到受影响节点；确无影响写空列表与具体 `impact_note`。新增机制与方法通过有历史依据的提案修改当前版本，独立 `proposal-review` 通过后才 `apply`，不重复搭架子、不无理由来回翻转。后续改进在已发布工作区 `init --mode update`，使用 `01_INCREMENTAL_AGENT.md`，不要把首轮流程每次重跑。

交付实质中文报告和真实可离线计算的家庭HTML，同时提交可接续源文件与当前研究状态。继续推进到成品，不停在计划。最后直接写出你的核心裁决：当前危机、最可能路径、2027年窗口、十年假说及家庭行动。必须下判断；不用免责或自造百分比收尾。
