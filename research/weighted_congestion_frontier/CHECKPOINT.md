# 有价值阶段的保存

按 [GROWTH](../GROWTH.md) 与[全仓施工规则](../REPOSITORY_GUIDE.md)完成可复用正文、精确身份和对应核验后，直接执行：

```sh
python3 research/weighted_congestion_frontier/tools/work.py checkpoint -m '实际增量与准确范围'
```

默认保存当前加权拥塞主题的正式稿、候选、审查、程序、证据和共同账本；其他文件显式列入。研究者使用各自独立 clone 的 main。程序 commit、普通 push、拉取远端确认，只有可达后返回 pushed；同时给出 commit/hash/descriptor。重复运行不制造空提交，真实冲突保留双方并停住。

候选按候选保存，失败按准确失败保存。提交不是数学升级，阶段成果不是主目标解决。程序不会自动产生随机工作分支，也不把研究资产只留在公屏。

有重要结果需研讨时，再用 descriptor 分享冻结入口。没有必要让所有人审查日常中途工作；独立攻击用于承重数学结论的状态提升。
