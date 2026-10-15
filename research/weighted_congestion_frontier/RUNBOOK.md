# 启动、读取和保存

新对话附上本仓库当前 `tools/work.py` 和仓库外的 `githubtoken.txt`，按 [TEAM](prompts/TEAM.md) 的具体题目、完成标准和入库要求开始研究。外部程序用于缺失工作区恢复 main：`python3 <最新版程序实际路径> --repo <项目目录> start --token-file <凭据实际路径>`。已有仓库直接使用仓库内统一程序，读取根四入口和[当前数学入口](../current/weighted_congestion/README.md)。恢复后不继续使用旧附件副本。

```sh
python3 research/weighted_congestion_frontier/tools/work.py start --token-file /本会话/githubtoken.txt
```

一个对话用独立 clone，在 main 研究和提交，不创建研究分支。省略 --actor 自动产生并记住发布标识；也可显式指定唯一标识。凭据只记仓库外路径，不入 Git。已有工作区安全同步 main；旧 wcg/work 分支保留成果后本地迁移为 main，冲突停住并保留已有工作。

```sh
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/weighted_congestion_frontier/tools/work.py read
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '具体数学增量和范围'
```

不指定路径时，checkpoint 覆盖加权拥塞的正文、候选、审查、审计代码、证据和共同账本。显式路径会替换整个默认范围：若涉及默认范围外文件，必须列全本次应提交的正文、登记和额外文件，不能只列额外文件。普通推送自动合入不冲突的 main 更新；真实冲突停住保留双方。本地回执给出已推送 commit、文件 hash 与 descriptor；仅返回 pushed 才说明远端确认。

公屏可自由讨论有启发的 idea、卡点、反例与合作问题，注明已证和未证，不要求先成稿：

```sh
python3 research/weighted_congestion_frontier/tools/work.py send --text '精确发现、范围、未解义务和已保存入口'
```

较长内容用 --text-file；回复用 --reply-to，话题用 --thread；成果用 --asset-json 附冻结 descriptor。pending/retry 保持稳定消息 ID。无需强制汇报常规排错和逐轮日志；聊天、候选入库和重要 claim 升级分别按其要求处理。

形成第一份可复用候选、重要审查、精确反例或实质修复，claim 范围和状态实质改变，以及分享成果或交接前，及时完成相应核验并 checkpoint。只有返回 `status: pushed` 才报告远端保存成功。他人先更新 main 时，同步后复核实际受影响的 claim、objection 和登记并重跑相关检查；程序若在 checkpoint 期间自动合入他人更新，须随后核验最终内容，必要时立即提交修正。真实冲突按内容处理，不强推，也不另建分支躲开冲突。

核验代码：`python3 tests/audits/weighted_congestion/replay.py --list`，再把所选路径作为参数传入。程序在临时镜像内运行，冻结证据不被覆盖。正式交付按 GROWTH 跑地图、来源与资产检查。
