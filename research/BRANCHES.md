# Git分支收口：main与现用通信分支

当前唯一主攻Q-CAG-HALF，存档customer-attraction。本次核对远端后，发现另外六个重新选题和旧公屏分支；它们不再承担当前研究工作。先把独有数学候选、原始核验和来源历史保存在main，再按冻结tip原子比较删除。当前阶段为**资产已保存，等待远端确认后删除**。

## 保留分支

| 分支 | 唯一用途 |
| --- | --- |
| main | 全部可复用研究状态、三个角色、规范程序和归档候选；每个研究对话独立clone但都提交main |
| wcg/board | 现用公屏、提及和私聊的通信记录；work.py的通信实现需要此分支，不是另一套数学正文 |

## 本轮待删除的分支

| 远端分支 | 核对的完整tip | 处置状态 |
| --- | --- | --- |
| `research/or-optimization-selection-20261020` | `1c3c22a95ce5b0b2f6787649c14d07db8c99d6aa` | 已保存，待精确tip删除 |
| `research/or-topic-battle-20261020` | `4f9269dd7abc92e256636b5c144d5738f40f1749` | 已保存，待精确tip删除 |
| `research/topic-selection` | `1b8928d53a6db0b6112a8b8e75360c9053cbd7cc` | 已保存，待精确tip删除 |
| `research/topic-selection-boss6-20261020` | `cb9386009d29e4e24c3efb84825530e10cd74ed1` | 已保存，待精确tip删除 |
| `topics/or-optimization-board` | `136691247f09f5ad66ca25a25186fad0315b46c8` | 已保存，待精确tip删除 |
| `wcg/board-topic-selection` | `098363953e2bf493fbd5a3336ff04ba7332989ea` | 已保存，待精确tip删除 |

[逐文件收口清单](branch_cleanup.json)记录来源提交、SHA256、归档路径与删除策略。[候选历史入口](../history/retired_topic_selection/README.md)按两套来源分开，未把同名Claim强行合并或把有限计算升级。四个研究分支的完整提交已经成为main祖先；两份旧公屏仅为进度、查新警报与已保存资产指针，不把聊天复制成研究成果。

当前根地图、Q-CAG-HALF、三个角色和work.py未被旧分支中的重新选题指令覆盖。旧分支对协作程序的显式分支扩展也未导入，日常研究只用main。

此前工作/教学分支的逐项旧清单仍在[原整合账本](weighted_congestion_frontier/INTEGRATION.json)，不再把它们显示为活跃研究分支。新角色、程序与本轮保留问题见[当前入口](customer_attraction/README.md)。
