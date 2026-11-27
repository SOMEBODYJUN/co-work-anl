# 180核小时怎样用于实际研究

本账户在本仓库实测可选2核/8GB和4核/16GB。学生认证有效时，官方额度为每月180核小时及Pro等量存储额度；本项目未把这个标准额度当作账户当前剩余余额。

计费按机型核心数乘开机时间，机器等LLM、下载或闲置也消耗计算额度。180核小时约为2核90小时或4核45小时；以30天举例，分别约3小时/天或1.5小时/天。一个Codespace单次最长运行12小时，停止后进程结束、保存的文件保留，后续从检查点恢复。停止仍会计存储；自定义基础镜像会计入存储用量，默认基础镜像有不同的存储计量规则。

官方依据：[额度计量](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-included-usage)、[学生权益](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)、[生命周期](https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle)。

## 可完成的任务与首期预算

以下为可挪用的调度上限，既不是模型权重，也不是必须消耗的工时。每批先有问题、输入和验收对象，计算留下能改变判断的结果。同样输入和代码的已完成任务复用结果。

| 工作 | 初始核小时上限 | 实际交付 |
|---|---:|---|
| 数据面板与活动模型 | 20 | 整理新发布、修订和口径，更新中国活动基线及信息归因 |
| 历史预警实验 | 50 | 简单/非线性候选、时间滚动、国家和制度留出，记录误报、漏报及可靠性 |
| 部门联合压力 | 50 | 地产、财政、平台、银行及家庭参数组合，找现金/资本缺口、承接资源与触发条件 |
| 稳定性与参数研究 | 40 | 换时期、事件定义、变量组、样本及有依据的参数范围；必要时按合适事件/国家/时间块重采样 |
| 独立复算和月度更新 | 20 | 从保存输入重跑承重计算，处理新数据和结构变化，修订正文与行动参数 |
| 合计 | 180 | 随实际瓶颈重新分配 |

已执行的2核容量夹具是30000行、24特征，logit拟合和单独校准约0.02秒，HGB约0.30秒；完整混频例约1.3秒。它说明常规表格模型适合本机，不能把这些局部计时直接乘成“一个月能做几百万个有效模型”。真实历史面板更小，但独立事件少、制度转用和因果判断更难；无限调参不会增加独立信息。对这类宏观研究，目前瓶颈首先是数据、标签、机制和验证设计，常规CPU容量充足。完整真实训练与恢复演练另见 `tests/live/scientific-compute-codespaces.json`。

新增流程也在重新创建的2核/8GB、Python3.12.11容器实跑：真实JST历史训练/校准/验证、银行会计用例及混频接口三个任务，整体约25.37秒；相同输入再执行约0.13秒，三个任务均复用已有结果。各子进程壁钟约19.46、0.11、4.76秒，含导入和本次环境开销；历史模型内部拟合/校准/评估logit约0.29秒、HGB约0.12秒。子进程峰值RSS约167MiB。实际模型成绩与保存的研究结果一致。计时存在冷启动、调度和系统波动，不外推所有负载的速度，也不包含建环境和远端连接耗时。

原文阅读、作者思考方式蒸馏及主裁决使用LLM推理；Codespaces负责采集处理、估计、回测、压力与复算。LLM的上下文或调用能力不随Codespaces CPU增加。现阶段不需要GPU平台来建立这些模型；大型文本模型训练或明显超出内存/时间的任务再按负载另配算力。

## 已接入的执行与恢复

```sh
python bootstrap.py --research
.venv-methods/bin/python work.py --workspace work/cycle-01 compute plan \
  --file examples/compute-first-cycle.json
.venv-methods/bin/python work.py --workspace work/cycle-01 compute run \
  --file examples/compute-first-cycle.json --session-seconds 10800
```

示例计划包含真实历史预警、银行会计用例和混频接口用例。后两项标为合成验算，不能进正式宏观结论。Pro把实际中国输入、已登记实验和参数范围接入新的任务。Codespaces中runner读取实际可见CPU数；其他环境按allocated_cores显式声明估算。计划预算须按实际可用额度设置。

runner串行运行仓库已登记的研究方法。结果、输入/数据/代码指纹和耗时保存；同一有效结果直接复用，输入或代码变更才重算。每约5秒保存检查点，单任务超时及单次会话/计划预算均受限；失败保留并可重跑，不把未完成任务当成功。锁防止同工作区并行写入；中断后从同一计划和工作区接续。单次上限11小时，给12小时生命周期限制留出保存空间。

## Pro如何真正使用远端

Pro执行环境须有终端、GitHub CLI和已授权的远端访问；提示词本身不建立远端连接。已有Codespace先核对分支和未保存工作再复用。无实例时，可用仓库外的既有GitHub认证创建：

```sh
gh codespace create --repo SOMEBODYJUN/co-work-anl --branch work/cn-crisis \
  --machine basicLinux32gb --devcontainer-path .devcontainer/devcontainer.json \
  --idle-timeout 240m --display-name cn-crisis-research
gh codespace ssh --codespace <实际实例名>
# 在远端仓库目录运行上面的compute命令，批次完成后保存并同步实际产物。
# 从发起端停止该实例：
gh codespace stop --codespace <实际实例名>
```

认证来自执行环境的既有凭据，不把令牌写入仓库、文章笔记或公开结果。连接超时与模型报错分别诊断；未运行的远端任务不能登记为已成功。

[官方空闲定义](https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces)以用户或终端活动为依据；后台计算及检查点文件写入本身不保证重置空闲计时。默认30分钟，允许5—240分钟。上例240分钟配合三小时批次，避免依赖后台活动维持机器；已有实例的超时更短时，相应缩短session-seconds，并给本次开机已用时及保存留余量。真实进度可以输出，不伪造活动。每批结束主动停止；远端中断时根据账本恢复，不能把12小时寿命上限误当无条件可用的单次计算时间。

账本记录的是runner内按声明核心数估计的核时，不是GitHub账单。建环境、runner外的开机时间、其他实例及停止后的存储均不在其中。长计算分批运行、及时保存和提交；阅读讨论期间停止不用的计算实例，恢复后继续。新预算周期使用独立工作区，保留旧周期的结果与变更原因。不会在本模板中自动创建整月云资源或定时消耗账户额度。
