# 数学研究仓库

这是研究运行树：保存可复用的数学正文、证据、超边、研究 RUN 和未完成义务。旧的 2.5.3／第三阶段队列、公屏、清点台账、重复登记表和派生图已经退出当前树，不再作为研究启动前置条件。

新工作区只需要仓库外凭据和当前版本的 `work.py`：

```sh
python work.py --repo <clone> start --actor BossN --save customer-attraction --token-file <仓库外凭据>
python work.py --repo <clone> research studio init <RUN> --spec <原题spec> --expect-branch rebuild/research-v2
```

研究过程写入 `archives/<问题>/workspaces/` 与 `research/runs/`。Main 和三条研究线用 Work 实际派工；中间推导、失败、反馈和断点先保存，成熟数学再更新对象、证据和超边。研究读取使用 `research search/show/context/frontier`，结构检查使用 `research check/build`，不依赖旧阶段账本或公屏。

数学核心保留在 `archives/`、`tools/evidence/`、`research/registry.json` 和 `map/edges/`。迁移后仍有数学作用的阶段证据统一放在 `tools/evidence/canonical/`，并由绑定清单和 SHA-256 固定；它们是现行证据，不是历史下载包。

常用入口：

- `work.py`：同步、启动、工作区、研究、计算、GitHub 资源和 checkpoint。
- `prompts/research-runtime.md`：Main、独立障碍线和两条成果线的运行词。
- `research/registry.json`：唯一当前对象、材料和正式超边登记。
- `map/edges/`：可复用的完整联合前提、替代证明、条件和未付义务。

新问题必须由用户明确指定；仓库不会从已删除的阶段任务或公屏推断研究目标。
