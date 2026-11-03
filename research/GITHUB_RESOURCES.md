# GitHub资源与实际部署边界

核对日期：2026-11-03。以下是公开官方权益，不代表本账号已认证、领取或启用；当前附件的Git写端点认证失败，未读取账号账单。

| 功能 | 用途 | 本次配置 |
|---|---|---|
| Git与历史 | 保存正文、证据、失败路线、断点 | 沿用work.py sync/checkpoint、共同分支和Boss工作区 |
| Codespaces | 可重建的Linux/Python计算环境 | `.devcontainer/devcontainer.json`与`tools/bootstrap_research.py`；未创建实例 |
| Actions | 工具兼容测试、手动复现数学计算 | 两份workflow；contents:read；不自动改数学状态 |
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
python tools/compute.py runtime-smoke --out validation/runtime-smoke.json
python tools/compute.py cag-five-local --out validation/cag-five-local.json
python tools/compute.py positive-kernels-rank --out validation/positive-kernels-rank.json
```

后两项均为仓库已有的标准库精确有理数计算。cag-five-local只检查五人局部组件，不是完整五人证明或六人结论；positive-kernels-rank只检查既有有限代数输入，不外推任意权重、次数或闭包定理。

配置成功推送后，Code→Codespaces可按统一配置创建环境。Actions手动workflow_dispatch通常还要求workflow文件存在于默认分支；长期工作分支与main分开，不擅自合并。保持main不动时，可用工作分支push检查或Codespaces直接运行命令。配置已写不代表云端运行通过。

当前远端部署需要被GitHub接受且具备目标Contents/Workflows权限的凭据；附件返回Invalid username or token，已停止重试。学生状态、配额和Copilot权益须在本人Education/Billing确认。未创建Codespace、未触发远端Actions、未代办学生认证。

官方依据：

- [学生权益](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [学生认证](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student)
- [Student Developer Pack](https://education.github.com/pack)
- [当前计划配额](https://docs.github.com/en/billing/reference/product-usage-included)
- [Codespaces计量](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
- [Python devcontainer](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces)
- [Actions语法](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [手动工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
