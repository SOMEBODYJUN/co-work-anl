# 数学研究仓库

这是研究运行树：保存可复用的数学正文、证据、超边、研究 RUN 和未完成义务。旧的 2.5.3／第三阶段队列、公屏、清点台账、重复登记表和派生图已经退出当前树，不再作为研究启动前置条件。

新对话从 [研究分支的 work.py](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/rebuild/research-v2/work.py) 起步，使用仓库外凭据。启动成功后，后续命令使用检出目录内的程序。

```sh
python work.py --repo <clone> start --actor BossN --save customer-attraction --token-file <仓库外凭据>
```

新 Boss 用自己的空目录。start 绑定个人工作区。进入 clone 后，先在 `research/workspaces/<RUN>/spec.json` 填写[原题 spec 模板](research/agent-design/spec-template.json)，再创建该 Boss 的研究工作室。

```sh
python work.py research studio init <RUN> --spec research/workspaces/<RUN>/spec.json --expect-branch rebuild/research-v2
```

如果接续旧研究，使用原来的 Boss 和存档，在 `start` 加 `--resume`，然后读取自己的原 RUN。新 Boss 可以沿同一原题研究，使用自己的 RUN。

```sh
python work.py --repo <clone> research studio status <RUN> --session-tag <本次会话标签>
```

RUN ID 和原始题目可从仓库的 [research/runs/](research/runs/) 查到。首次下载中断时，重跑同一条 `start` 即可。

Main 用 Work 派工，查看超边和短回执，负责选路线和发布。idea 子代理提出可检验路线，执行子代理用 `research search/show/context/frontier` 按需读依赖、正文和证据。工作者从研究笔记和精确引用恢复，接近上下文上限时换 fresh 子代理。推导、失败、反馈和断点先保存，成熟数学再更新对象、证据和超边。

数学核心保留在 `archives/`、`tools/evidence/`、`research/registry.json` 和 `map/edges/`。迁移后仍有数学作用的阶段证据统一放在 `tools/evidence/canonical/`，并由绑定清单和 SHA-256 固定；它们是现行证据，不是历史下载包。

常用入口：

- `work.py`：同步、启动、工作区、研究、计算、GitHub 资源和 checkpoint。
- `prompts/research-runtime.md`：Main、独立障碍线、idea 和执行线的运行词。
- `research/registry.json`：唯一当前对象、材料和正式超边登记。
- `map/edges/`：可复用的完整联合前提、替代证明、条件和未付义务。

新问题必须由用户明确指定；仓库不会从已删除的阶段任务或公屏推断研究目标。
