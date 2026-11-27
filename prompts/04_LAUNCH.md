# 复制给 Pro 的启动消息

必须形成明确主判断，并说明机制、时间窗口和家庭行动含义；不得以防御性话术回避裁决，不得自创危机评分公式、风险总分和任意概率。

检查已有clone和工作区；存在时运行状态命令恢复原断点，不覆盖或重复创建。新环境直接克隆本项目的公开分支：

```bash
git clone --depth 1 --single-branch --branch work/cn-crisis https://github.com/SOMEBODYJUN/co-work-anl.git cn-crisis
cd cn-crisis
python bootstrap.py
.venv-methods/bin/python work.py methods doctor
```

若使用附带的 `CN_crisis_workbench.zip`，先解压并读取其中完整源码；也可通过包内 `repository.bundle` 建立真正的Git clone：

```bash
git clone --branch work/cn-crisis /解压目录/cn-crisis/repository.bundle cn-crisis-run
cd cn-crisis-run
git remote set-url origin https://github.com/SOMEBODYJUN/co-work-anl.git
python bootstrap.py
.venv-methods/bin/python work.py methods doctor
```

若直接使用解压的源码目录，先 `git init -b work/cn-crisis` 建立本地提交历史；不要覆盖已有Git工作区。本地提交使用当前Git身份；若新clone没有身份配置，则设置本仓库研究身份 `git config user.name 'Research Workbench'` 与 `git config user.email 'research@users.noreply.github.com'`。公开读取本分支不需要令牌。后续推送使用已给的仓库外凭据，不把凭据写入项目或结果。已有工作区先用 `.venv-methods/bin/python work.py --workspace work/<实际run> status` 读取状态，再接续。

完整读取 `prompts/00_PRO_FIRST.md`、`docs/WORKFLOW.md`、`docs/RESEARCH_DESIGN.md`、`docs/METHODS.md` 与 `prompts/05_CALCULATOR_SPEC.md`，再读 `inputs/01`—`05`。用仓库自己的 `work.py` / `crisis.py` 统一入口恢复或创建首轮工作区，按真实20阶段完成资料、观点方法学习、专题分析、可修改因果超边、测算、对抗裁决、报告写作、离线计算器、独立复核与发布。每个实质批次保存，阶段结束提交；必要时用真实子代理独立研究与复核。

选定上游工具、适配器和使用说明已在本仓库；先运行自己的工具并读取已有检索与事件记录，复用适用资料。新材料通过 `targets` 挂到受影响节点；确无影响写空列表与具体 `impact_note`。新增机制与方法通过有历史依据的提案修改当前版本，独立 `proposal-review` 通过后才 `apply`，不重复搭架子、不无理由来回翻转。后续改进在已发布工作区 `init --mode update`，使用 `01_INCREMENTAL_AGENT.md`，不要把首轮流程每次重跑。

交付实质中文报告和真实可离线计算的家庭HTML，同时提交可接续源文件与当前研究状态。继续推进到成品，不停在计划。最后直接写出你的核心裁决：当前危机、最可能路径、2027年窗口、十年假说及家庭行动。必须下判断；不用免责或自造百分比收尾。
