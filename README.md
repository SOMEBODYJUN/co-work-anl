# 中国经济危机研究工作台

从明确判断出发，把材料、分析、计算、写作和持续修订接成一个能恢复的研究过程。

首轮Pro执行 **20阶段**，交付经济报告、离线家庭计算器和可接续源文件。后续研究agent执行 **8阶段**，从旧结论、检索记录、因果传导链和修改历史出发，补充、加强、替换或撤回具体内容。所有核心问题都要给主判断；允许科学建模和评分，禁止任意赋权、未经检验映射概率和伪精确数值。评分与概率模型遵守 [科学建模规范](docs/SCIENTIFIC_MODELS.md)。

## 直接启动

完整工作台已发布到独立分支 `work/cn-crisis`。新环境直接克隆本分支：

```sh
git clone --depth 1 --single-branch --branch work/cn-crisis https://github.com/SOMEBODYJUN/co-work-anl.git cn-crisis
cd cn-crisis
python work.py --help
python bootstrap.py
.venv-methods/bin/python work.py methods doctor
```

已有下载包时，也可通过其中的 `repository.bundle` 建立本地clone并持续提交：

```sh
git clone --branch work/cn-crisis /实际路径/cn-crisis/repository.bundle cn-crisis-run
cd cn-crisis-run
git remote set-url origin https://github.com/SOMEBODYJUN/co-work-anl.git
python bootstrap.py
.venv-methods/bin/python work.py --help
```

读取 [Pro首轮完整执行词](prompts/00_PRO_FIRST.md)，发送 [启动词](prompts/04_LAUNCH.md)。`bootstrap.py`从精确版本的PyPI包安装计算依赖；选定上游代码、许可、方法材料和本题适配器都在本仓，无须再clone其他GitHub仓库。

核心账本、来源采集、检索复用、超边和版本管理使用Python标准库。可先不安装计算环境，直接 `python work.py --workspace work/cn-v0 init`。完整模型计算再用 `.venv-methods/bin/python` 运行。Windows对应 `.venv-methods/Scripts/python.exe`。

## 真实输入入库

```sh
python work.py --workspace work/cn-v0 init
python tools/import_seed.py --output work/cn-v0/intake/seed.json
python work.py --workspace work/cn-v0 ingest --file work/cn-v0/intake/seed.json
python work.py --workspace work/cn-v0 status
```

原始精简包在 `inputs/`，47条指标来自18个来源项。当前执行规范为 `prompts/`，`inputs/00_MASTER_PROMPT.md`保留原始版本供追溯。

## 研究中怎样使用

| 需求 | 统一命令 |
|---|---|
| 搜索前查已有查询/统计期/新鲜度 | `search-plan` |
| 保存检索、零结果和决定 | `search-log` |
| 内置搜索结果桥接、公开发现与原文采集 | `collect bridge/discover/fetch` |
| 保存分类型证据和版本 | `ingest` |
| 初建联合前提传导链、查看受影响结论 | `graph-put`、`graph-status` |
| 基于新学习提交修改、独立审核、主代理合并 | `proposal`、`proposal-review`、`apply` |
| 贷款、桥接回归、混频、部门会计 | `methods run` |
| 阶段产物与正式审核 | `stage`、`review`、`release` |
| 串行保存到Git及远端 | `checkpoint --paths ... --message ... [--push]` |
| 已发布首版后开始增量周期 | `init --mode update` |

各命令 `--help` 给出实参。文件哈希绑定阶段和审核；原文、参数或传导链变化后，相关结论和阶段会进入重审。模型负责实质分析和裁决，CLI负责持久化、依赖和复算。详见 [接口](docs/TOOL_BRIDGE.md)、[完整阶段](docs/WORKFLOW.md)、[研究设计](docs/RESEARCH_DESIGN.md)、[实际工具](docs/METHODS.md)。

具体职责、滚动派工和超边由谁裁决见 [专题协作手册](docs/AGENT_PLAYBOOK.md)；每组观点学什么、如何比较见 [观点研究程序](docs/VIEWPOINT_PROGRAM.md)；作者与独立复核者使用 [专题任务合同](prompts/06_SPECIALIST_TASK.md)。

[分析者历史学习](docs/ANALYST_LEARNING.md)接入公开文章目录、逐篇观点与预测核验，再据此修订专题；[首批原文笔记](research/analysts/INITIAL_READING.md)包含实际竞争观点与失误检查，目录盘点不冒充全文蒸馏。`analysts inventory-wordpress`可持续更新公开博客目录。评分仅指建模后的输出。

[Codespaces远端实测](docs/CODESPACES_VALIDATION.md)记录本账户实际可选的2核/8GB与4核/16GB，以及两档机器上的安装、适配器和真实训练执行。新增 `.devcontainer/devcontainer.json` 固定Python 3.12；可选 `python bootstrap.py --benchmark` 安装容量基准依赖。合成训练测试不充当中国危机模型结果。

[实际整合状态](docs/INTEGRATION_STATUS.md)列出执行过的工具和输入、选段借入的方法、真实搜索查询、现有观点阅读范围，以及首轮将产出的实质专题。

每阶段完成实质产物后由主代理保存：

```sh
python work.py --workspace work/cn-v0 checkpoint --paths work/cn-v0 --message 'cn-v0: 保存本阶段研究'
```

远端凭据由运行环境配置，放在仓库外；不随研究包分发。研究者私密家庭输入保留本地，使用合成样例测试公开引擎。

## 演练与复现

```sh
.venv-methods/bin/python -m unittest discover -s tests -v
```

[实际验收记录](docs/ACCEPTANCE.md)说明首轮、增量、方法实算、新clone恢复和故障拦截的结果。演练数据与正式研究分开；Pro首轮从当前输入执行经济裁决与完整家庭计算器。
