# GitHub资源与实际部署边界

核对日期：2026-11-03。以下是公开官方权益，不代表本账号已认证、领取或启用；学生身份与账号余额未核验。

本轮更新：此前已成功推送的初版为历史事实；本次新增运行协议和回执已形成本地提交`c7708eaf`，同步远端后尝试推送时当前外部凭据返回GitHub `401 Invalid username or token`，所以本次改动尚未共享。直接PAT接口`work.py github`仍实现status、machines、dispatch、create-codespace、stop-codespace，但当前凭据下不能把API写入或实时资源状态说成已验证；本轮未创建/停止实例或dispatch任务。学生状态与余额仍未读取或推断。

## 现在能用什么

| 能力 | 研究用途 | 当前状态 |
|---|---|---|
| Actions push检查 | 只在明确登记的数学计算或阶段交付需要时运行 | 不再自动跑181项工程回归测试 |
| Actions workflow_dispatch | 明确选择一个已登记实验，在GitHub runner上执行并上传artifact | 工作流已配置，手动运行需实际调用 |
| Actions artifacts/logs | 保存stdout、stderr、版本、输入指纹和结果 | 已配置7天artifact；长期数学结果仍需整理回仓库 |
| Actions concurrency/timeout | 同一分支只留一个检查，防止重复消耗和长时间空转 | 已配置 |
| Actions environments/secrets | 给特定云任务提供受控凭据 | 可用，但本项目当前不把Secret读进代码 |
| Codespaces | 统一Python、Git和项目依赖；可以直接运行登记实验 | devcontainer已配置；未创建实例 |
| Codespaces machines | 按实际可用机器选择CPU/内存 | `work.py github machines`读取，不猜机器名 |
| Codespaces prebuilds | 预装依赖、减少启动时间 | 当前未配置，依赖较重时再加 |
| Branches/commits | 保留数学推导、实验和恢复点 | 已使用 |
| Issues/Discussions/Projects | 管理开放义务和工作分配 | 可启用；正式数学不放在任务卡片里 |
| Releases/Packages/Pages | 发布工具模板、依赖包和只读导航 | 当前未作为研究状态源 |

| 功能 | 用途 | 本次配置 |
|---|---|---|
| Git与历史 | 保存正文、证据、失败路线、断点 | 沿用work.py sync/checkpoint、共同分支和Boss工作区 |
| Codespaces | 可重建的Linux/Python计算环境 | `.devcontainer/devcontainer.json`与`tools/bootstrap_research.py`；未创建实例 |
| Actions | 手动复现登记数学计算并保存artifact | 一个`research-compute.yml`；contents:read；不自动改数学状态 |
| Artifacts | 下载实验版本、输出、错误和范围 | compute.py回执；云端保留7天，有价值结果另做checkpoint |
| Copilot Student | 编辑器代码辅助 | 不等同Work额度或外部模型API额度；未声称已领取 |
| Issues/Projects/Discussions | 可选任务协作 | 已有认领账本和公屏，不建立重复系统 |
| Releases/模板 | 稳定版本分发、迁移其他命题 | 已提供本地导出器；未创建新远端仓库或Release |
| Pages | 可选只读展示 | 当前不另开站点 |
| Pack合作权益 | 云计算、IDE、域名等 | 按真实需求领取；第三方账号与学生核验由用户完成 |

认证学生的Codespaces个人权益为**180核时/月、20 GB-month存储**：2核约90机器小时，4核约45机器小时，多个实例共享。停止计算后存储仍计量。此配置建议2核、不启用预构建，不开空闲机器消耗配额；剩余量以本人账单为准。

Education页面仍展示“3K Actions minutes”，当前Billing参考页把Pro的included compute写为**$18/月**并列1 GB Actions存储。官方存在新旧口径，不承诺本账号固定3000分钟；以当前账号Billing、runner类型、预算和实际用量为准。

Pack目前还列出Azure学生$100额度、JetBrains学生订阅等。Copilot Student包含代码补全和有额度限制的聊天/Agent使用，并非无限模型算力。这些优惠不能仅靠仓库PAT自动领取；普通Git认证也不等于学生认证。

## 实际入口

```sh
python tools/bootstrap_research.py
.venv/bin/python work.py research --help
python tools/compute.py cag-five-local --out validation/cag-five-local.json
python tools/compute.py positive-kernels-rank --out validation/positive-kernels-rank.json
```

在Codespace里给数学研究直接使用的入口是：

```sh
python work.py research compute cag-five-local --out research/checks/codespace/cag-five-local.json
```

这条命令先运行`research/experiments.json`中登记的精确计算，保存命令、版本、seed、精度、stdout/stderr和适用范围；随后立即做一次本地Git提交，再尝试把同一提交推送并确认远端。共享回执应放进未被`.gitignore`排除的`research/checks/`或存档证据目录。凭据或网络失败时输出`local-only`，计算回执和本地提交仍保留，不能把它说成已共享。每个有价值的引理、构造、反例或实验都重复这条保存动作；一个长任务不能只在最后提交一次。

具体数学用途是：在统一的Linux/Python环境中运行Solver写的有限枚举、`fractions.Fraction`精确不等式审计、符号/优化程序或可复现实验；把输入、参数、随机种子、精度控制、输出和解释放在`validation/`或对应存档的`tools/evidence/`，再由Main判断哪些只是Observation/Evidence、哪些值得写入数学正文。Codespace本身不增加Work模型或Solver数量，也不自动把计算结果升级为证明。

后两项均为仓库已有的标准库精确有理数计算。cag-five-local只检查五人局部组件，不是完整五人证明或六人结论；positive-kernels-rank只检查既有有限代数输入，不外推任意权重、次数或闭包定理。

配置成功推送后，Code→Codespaces可按统一配置创建环境。Actions手动workflow_dispatch通常还要求workflow文件存在于默认分支；长期工作分支与main分开，不擅自合并。保持main不动时，可用工作分支push检查或Codespaces直接运行命令。配置已写不代表云端运行通过。

一条完整云端实验链是：`research/experiments.json`登记命令 → `workflow_dispatch`选择实验 → runner或Codespace执行 → `validation/*.json`保存命令、版本、精度、seed、输出和错误 → Main检查结果 → 有数学价值的内容写入对应archive/evidence并checkpoint。云端输出只是Evidence或Observation，不能自动成为Claim。

新凭据已经通过Git发布与本仓库资源只读API检查。学生状态、配额和Copilot权益仍须在本人Education/Billing确认。本轮未创建Codespace、未手动dispatch计算、未代办学生认证；代码推送触发的检查与实际数学计算分别报告。

GitHub资源调用使用仓库外PAT，无需账号连接器；仓库写权限与Actions/Codespaces权限分开报告。`status`只读；只有明确运行dispatch或create-codespace才产生对应请求，创建环境会使用配额。stop先核对实例属于当前origin仓库。401立即停止，403不会伪装该功能可写，认证信息不跟随重定向。API定义见[Actions workflows](https://docs.github.com/en/rest/actions/workflows)和[Codespaces](https://docs.github.com/en/rest/codespaces/codespaces)。

官方依据：

- [学生权益](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [学生认证](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student)
- [Student Developer Pack](https://education.github.com/pack)
- [当前计划配额](https://docs.github.com/en/billing/reference/product-usage-included)
- [Codespaces计量](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
- [Python devcontainer](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces)
- [Actions语法](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [手动工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
