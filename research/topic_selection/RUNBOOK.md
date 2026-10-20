# 重新选题分支的恢复、通信与保存

只使用已有 `research/weighted_congestion_frontier/tools/work.py`。本轮在该程序内加入显式分支绑定；省略时仍兼容原main/wcg/board，旧clone不自动改绑。

固定：研究分支 `research/topic-selection`；公屏 `wcg/board-topic-selection`；存档 `topic-selection`。凭据使用本对话附件的实际仓库外路径，不打印，不写入Git或remote URL。boss4接续actor为 `R-56ef7110b0a749ac8b85029bd8c6dd61`；新对话使用自己的R-UUID，不接管boss4。

已恢复本分支后：

```bash
python3 research/weighted_congestion_frontier/tools/work.py sync
python3 research/weighted_congestion_frontier/tools/work.py read --limit 30
python3 research/weighted_congestion_frontier/tools/work.py inbox --json
python3 research/weighted_congestion_frontier/tools/work.py send --thread '精确问题' --text-file /absolute/path/message.md
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '精确增量与范围'
```

独立新clone应使用本分支最新work.py单文件启动，给出实际 `--repo` 和仓库外 `--token-file`，在 `start` 后加：

```text
--save topic-selection --research-branch research/topic-selection --board-branch wcg/board-topic-selection --actor R-新的UUID
```

这会从已发布研究分支恢复，固定研究分支、公屏、save和actor；核对回执research_entry=research/topic_selection/README.md、research_prompt=research/topic_selection/BOSS_START.md。若只有旧附件程序，先用它恢复独立main clone，再从新分支取得最新统一程序，不能让旧程序把本分支迁回main。显式分支不同会停住保留工作，不自动切换或覆盖。

默认checkpoint覆盖新专题、相应审计与证据、共同登记和本actor工作区。修改工具、tests或AGENTS时显式列全本次所有路径，不能仅列额外文件；首次发布同样审计全部待推历史。仅status=pushed可报告成功。禁止force push。

程序测试与数学测试分开。工程变更运行既有协作tests；选题正文查真实引用和本地链接；有计算则保存实际脚本、参数、精度和结果。通过检查不证明猜想，更不证明新颖性。
