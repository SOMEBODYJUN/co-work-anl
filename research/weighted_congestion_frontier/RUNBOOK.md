# 启动、读取和保存

新对话直接从 main 恢复本仓库，读取根四入口和[当前数学入口](../current/weighted_congestion/README.md)。仓库内唯一统一程序是 `tools/work.py`。不需要额外上传旧版程序；已有外部程序恢复后改用仓库最新版。

```sh
python3 research/weighted_congestion_frontier/tools/work.py start --token-file /本会话/githubtoken.txt
```

一个对话用独立 clone。省略 --actor 自动产生并记住发布标识；也可显式指定唯一标识。凭据只记仓库外路径，不入 Git。已有工作区安全同步 main；旧 wcg/work 分支保留成果后本地迁移为 main，冲突停住并保留备份。start 不创建远端工作分支。

```sh
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/weighted_congestion_frontier/tools/work.py read
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '具体数学增量和范围'
```

默认 checkpoint 覆盖加权拥塞的正文、候选、审查、审计代码、证据和共同账本。其他主题文件显式列入参数。普通推送自动合入不冲突的 main 更新；真实冲突停住保留双方。本地回执给出已推送 commit、文件 hash 与 descriptor；仅返回 pushed 才说明远端确认。

有重要且具体的研究内容才发公屏：

```sh
python3 research/weighted_congestion_frontier/tools/work.py send --text '精确发现、范围、未解义务和已保存入口'
```

较长内容用 --text-file；成果用 --asset-json 附冻结 descriptor。pending/retry 保持稳定消息 ID。常规排错、自行可完成的核验和碎片过程不发群聊。公屏是研讨，不是每次提交的审批。

核验代码：`python3 tests/audits/weighted_congestion/replay.py --list`，再把所选路径作为参数传入。程序在临时镜像内运行，冻结证据不被覆盖。正式交付按 GROWTH 跑地图、来源与资产检查。
