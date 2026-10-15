# 历史与可追溯来源

这里存放**可查的旧材料**，不充当现行定理的唯一入口。新的数学论证从[现行研究](../research/current/README.md)进入，旧路径的完整对照在[迁移表](../research/path_migration.json)。

| 位置 | 内容 | 使用方式 |
| --- | --- | --- |
| [source/manuscripts](source/manuscripts) | 两份原始完整 TeX 手稿、PDF 与构建脚本 | 按节号核对每条新证明的来源；旧稿声称“证明完成”不等于已外部复核 |
| [source/notes](source/notes) | 原始局部、精确算法、扩展和异构证明笔记 | 重建计算与查找未进入主稿的推导；保留当时的时点措辞 |
| [source/audits](source/audits) | 内部反驳、量词审计和优先权意见 | 查审查实际覆盖了哪里；“内部独立”不冒充外部认证 |
| [proofs](proofs)、[searches](searches) | 被替代的证明路线、交接及搜索 | 理解失败路线和反例来源，不能绕过现行条件直接引用 |
| [退出当前树的副本](source/notes/retired_snapshots.md) | 旧整理、交接与过时导出 | 原提交可恢复，不作为新会话读取入口 |

具体差异：旧共同目录存在性笔记依赖真实局部极小值，不能成为位数多项式菜单算法；旧强弦存在性取全局平方最大值，当前实现需要局部端点交换；旧稀疏异构稿末节的未闭合上界已被后来因子 2 整数族更新。每个冲突在相应[共享](../research/current/shared/README.md)、[异构](../research/current/heterogeneous/README.md)、[局部](../research/current/local_and_exact/README.md)新稿中标注。

原始两个 ZIP 的逐文件导入核对在第一轮[来源记录](https://github.com/SOMEBODYJUN/co-work-anl/blob/bd7798d5bbcc8086217ff54d7f91b445d0374b4f/history/curation-2026-10-01/PROVENANCE.md)：共同目录 19 项、异构目录 24 项，当时映射到 Git 导入记录。ZIP 容器没有再复制入当前树；早期提交仍可从 Git 历史恢复。今后新的原始材料按[增长流程](../research/GROWTH.md)进入 source/，先写新稿才可提升为现行内容。
