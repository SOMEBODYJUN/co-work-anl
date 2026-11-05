# 按实际研究任务使用云计算

入口仍是 `work.py`。普通批计算优先用 GitHub Actions 或已有算力；只有长期交互、持续会话或特殊依赖确实需要时才使用 Codespaces。创建环境只安装 Python 环境，不自动跑数学实验、演示或回归检查。

## 新计算 → 明确请求 → 取回结果

先为当前数学问题写实际计算脚本和一个 manifest。不必限于旧的三个 experiment ID；manifest 可以放在当前研究工作区。命令使用参数数组，不通过 shell 字符串执行。例子只展示接口，请替换为当次真实问题：

```json
{
  "schema": 1,
  "experiments": {
    "current-research-question": {
      "command": ["{python}", "workspaces/current-question/solve.py"],
      "inputs": ["workspaces/current-question/input.json"],
      "checkout_paths": ["workspaces/current-question"],
      "outputs": ["workspaces/current-question/results"],
      "timeout_seconds": 7000,
      "scope": "写清本次计算要区分的数学命题、定义域、输出解释和不能推出的结论"
    }
  }
}
```

`inputs` 与 `checkout_paths` 写全所需文件/目录；命令中的脚本本身会自动绑定，辅助模块与数据必须显式列入，声明的输出目录从输入绑定中排除。Python 包放在 `python_packages`（用明确版本）或 `requirements_file`；不需要安装依赖就省略。不要把凭据或已有无关输出放进计算输入目录。

```sh
python work.py compute request current-research-question --manifest workspaces/current-question/computations.json --request-id C-current-question-01 --timeout-minutes 130
```

这一步只在本地新增 `research/compute-requests/C-current-question-01.json`，不启动云计算。请求保存 experiment 条目的内容摘要、每份实际代码/输入的 SHA-256、runner、预算和恢复输入。随后按当前协作流程，把请求、manifest、脚本和输入一并 checkpoint 到 `rebuild/research-v2`；checkpoint 必须确认 pushed，并记下推送 commit SHA。

该分支**新增请求文件**的 push 才创建计算 job。普通正文、代码或提示词提交不触发计算。改旧请求不会重新计算；有意重跑时用新 ID，保留先前结果与原因。`github submit-compute` 是 `compute request` 的同入口别名。

```sh
python work.py github runs --ref rebuild/research-v2 --head PUSHED_COMMIT_SHA --request-id C-current-question-01
python work.py github run RUN_ID
python work.py github artifacts RUN_ID
python work.py github download ARTIFACT_ID --out validation/downloads/C-current-question-01.zip
```

`runs` 用推送 SHA 找到排队、准备中或准备失败的实际 run；job 名为 `compute/C-current-question-01`。API 接受、找到 run、run 成功、产物已下载是不同状态。下载后读取 `result.json`、stdout/stderr、算法输出和检查点，再判断是否得到有用数学证据。stdout/stderr 写独立文件，避免大输出塞进 JSON。声明的 `outputs` 与结果目录一同上传 artifact；当前保留期 7 天，长期成果应及时取回并 checkpoint。

## 预算、失败和接续

请求明确选择 runner 与分钟预算；默认 runner 为 `ubuntu-latest`。GitHub 托管 runner 单 job 实际上限为 6 小时；本入口接受 3–360 分钟，计算自身的 `timeout_seconds` 至少留出两分钟上传输出。依赖安装也占 job 预算，应按真实任务预留。超过单 job 上限的任务按数学或算法检查点拆分，或转已有合适算力；不能把请求当作获得无限算力。

算法可把可恢复状态写到环境变量 `RESEARCH_CHECKPOINT_DIR` 指定的位置。取回检查点、确认它确实被脚本支持后，再提交新的明确恢复请求：

```sh
python work.py compute request current-research-question --manifest workspaces/current-question/computations.json --request-id C-current-question-02 --timeout-minutes 130 --resume-from workspaces/current-question/resume.json
```

恢复文件也绑定 SHA-256，并通过 `RESEARCH_RESUME_FROM` 以及命令参数里的 `{resume_from}` 提供给算法。程序须实际读取该状态；入口不会替算法发明恢复能力。正常计算超时会保存 timeout receipt 与已有输出；整台 runner 被强制结束前来不及上传的文件无法保证保留，因此长计算必须主动写检查点并合理拆分。

已有本地/远程算力可用同一 manifest 执行，不必开 Codespaces：

```sh
python work.py compute run current-research-question --manifest workspaces/current-question/computations.json --out validation/current-question-01/result.json
```

本地计算可按任务设置更长超时，或显式 `timeout_seconds: null`；云请求仍遵守真实 runner 预算。每次用新结果目录，避免覆盖旧输出。

## 当前云入口状态

2026-11-05 只读核验：仓库默认分支为 `main`，`main` 没有 `research-compute.yml` 或 `research-checks.yml`；`rebuild/research-v2` 有这两个文件。因此不能宣称默认分支 `workflow_dispatch` 已就绪。本次提供的分支 push 请求入口不依赖往 `main` 安装 workflow。启用它需要把本次 workflow/工具修改推送到 `rebuild/research-v2`；本次审查没有提交真实计算请求、dispatch run 或创建云机。

```sh
python work.py github workflow-status --ref rebuild/research-v2
python work.py github status
```

`workflow-status` 读取两分支的实际文件状态；它不做付费资源探测或计算。若今后确需手工 dispatch，先让默认分支也有对应 workflow，再使用 `github dispatch`，随后仍需查实际 run 与 artifact。工程回归 workflow 改为仅显式手工启动，不再随日常 push 自动重跑。

Codespaces 仍保留 `github machines --ref ...`、`create-codespace --ref ... --machine ...` 和 `stop-codespace NAME`，供确实需要的交互工作；普通计算失败不自动新建云机。

依据：[GitHub workflow 语法](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)、[实际执行上限](https://docs.github.com/en/actions/reference/limits)、[run API](https://docs.github.com/en/rest/actions/workflow-runs)、[artifact API](https://docs.github.com/en/rest/actions/artifacts)。账号当前可用额度、费用和实际 runner 状态以账号与任务现场为准，不从仓库写权限推断。
