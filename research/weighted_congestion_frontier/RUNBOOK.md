# 本地程序与 Work 对话

每个研究对话复制 [TEAM.md](prompts/TEAM.md)，填好自己的角色号。论文者和提取者使用各自的完整提示词。所有入口都使用同一份本地程序、同一份当前会话凭据和异步公屏。

## 首次准备

上传 `work.py` 和 `githubtoken.txt`，在提示词中写好角色号、程序路径、项目目录和凭据路径。凭据 txt 包含一个 GitHub PAT：`github_pat_…` 或 `ghp_…`。本轮附件里的 `githubtoken.txt` 可直接用于用户授权的仓库操作。

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl start --actor R1 --token-file /本会话/githubtoken.txt
```

`start` 自动恢复缺失仓库，检查已有目录、Git 状态、origin 和远端，安全同步 main，固定角色号、凭据路径和本地专属工作分支。外部 `work.py` 是完整启动入口，空目录也可运行。仓库恢复后提供相同命令的 `tools/work.sh`。

同一 clone 的后续操作直接复用配置。新对话使用自己的角色号和目录；接续同一对话的本地目录时使用原配置，先 `sync`，再 `read`，然后继续研究。项目状态从实际 Git 与研究文件读取。

## 日常操作

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl read
python3 /本地程序/work.py --repo /本地目录/co-work-anl send --text '具体发现或问题'
python3 /本地程序/work.py --repo /本地目录/co-work-anl sync
python3 /本地程序/work.py --repo /本地目录/co-work-anl checkpoint
```

从仓库根也可使用：

```sh
bash research/weighted_congestion_frontier/tools/work.sh read
bash research/weighted_congestion_frontier/tools/work.sh send --text '具体发现或问题'
bash research/weighted_congestion_frontier/tools/work.sh sync
bash research/weighted_congestion_frontier/tools/work.sh checkpoint
```

`read --json` 读取结构化消息；`send --text-file 文件` 发布较长内容；`--reply-to MESSAGE_ID` 回应具体消息，`--thread 话题` 连接同一讨论。成果消息可附 `--asset-json` checkpoint 返回的 descriptor。`sync` 拉取 main 并安全接入本地工作分支，保留本地修改。发送未确认时，`pending` 查看待发消息，`retry MESSAGE_ID` 以原 ID 恢复。

## 实际研究循环

先读根 README、RESEARCH_STATE、CLAIMS、FAILED_ROUTES、AGENTS，再读本分支 README、MODEL、CLAIMS、RESEARCH_STATE、LITERATURE、PRIOR_ASSETS、FAILED_ROUTES、PROTOCOL、ACCEPTANCE、SOURCES 和相关提示词。读公屏后自主选择高信息价值的义务，立即开展数学工作。

按当前任务启动 subagent，让不同成员独立提出表示、证明或攻击。并行数量按实际有价值的工作和工具能力安排，完成一个义务后接续新的义务。主对话汇集结果并以自己的角色号分享。

公屏按群聊使用：消息可稍后回复，研究在等待回复期间继续。多个对话可以独立研究同题，重要区别与结果及时公开。文献核对、精确计算、一般证明、反例与独立审查围绕实际瓶颈展开。

本项目按研究需要持续工作。局部结果完成后继续追关键义务；路线失败时提取准确边界并换机制。用户停止、实际工具限制或确无可判别下一动作时，保存已知结果和精确交接。

## 阶段保存

研究资产使用 `assets/<actor>/<idea>/`，独立工具使用 `toolbox/<actor>/<tool-id>/`，论文材料使用 `papers/<actor>/<paper-id>/`。建立有价值文件且完成对应核验后执行 checkpoint，并将已推送 descriptor 分享到公屏。

```sh
python3 /本地程序/work.py --repo /本地目录/co-work-anl checkpoint research/weighted_congestion_frontier README.md RESEARCH_STATE.md -m '准确的阶段结果'
```

默认范围为本研究目录；范围外文件显式列出。数学候选与失败回收按真实层级及时保存。正文、账本和图关系在真正形成新数学资产时同步维护。其他对话可以直接阅读工作分支的冻结文件并继续研究。

## 交付层级

| 交付 | 判据 |
| --- | --- |
| 本轮交接 | 已知、关键未解义务、下一动作与已推送资产可恢复 |
| 可复用阶段成果 | 精确 lemma、反例、工具、obstruction 或实验有真实增量 |
| 主目标阶段突破 | 完整一般证明的全类 o(d) 上界，或严格改善核实过基线的无限非存在下界 |
| 主目标解决 | 对目标给出准确结论；宣称增长阶已确定时具有同一全类的匹配上下界 |

完整数学门槛见 [ACCEPTANCE.md](ACCEPTANCE.md)。
