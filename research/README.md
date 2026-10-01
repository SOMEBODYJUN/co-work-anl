# 数学关系图、资产索引与增长接口

[现行研究](current/README.md)说明已有结果；[下一阶段路线](ROADMAP.md)排序真正的新问题，[开放问题](questions/README.md)记录其待解量词；[增长规则](GROWTH.md)及[命题模板](templates/claim.md)说明下一项成果怎么放入仓库。现行共享证明的 G1–G3、L1–L2 已在独立 Markdown 页重写，不混入开放问题。

本目录有两份彼此不同的机器可读关系：

| 文件 | 表示什么 | 不表示什么 |
| --- | --- | --- |
| [graph.json](graph.json) 与[交互 HTML](index.html) | 定义、引理、反例、命题之间的**数学合取超边**。derives 需要全部前提；attacks 为反例；checks 为有限观测；implements 为程序关系；limits 为未解决处。 | 不是旧稿文件夹或普通链接图；测试边不证明普遍定理。 |
| [assets.json](assets.json) | 每条命题的精确适用条件、现行新稿、规范实现、测试、冻结结果、历史来源。 | 历史来源不自动具有现行证明地位。 |
| [review_status.json](review_status.json) | 所有现行命题的来源证明、当前重写、内部审读、外部审查、实现五个独立状态；构图时强制与命题节点一致。 | 内部审读不代替外部同行评审。 |
| [path_migration.json](path_migration.json) | 原始文件搬迁和旧命令退出位置。 | 不要求继续在根目录保留旧模型命名。 |
| [source_crosswalk.md](source_crosswalk.md) | 68 个原始文件/旧代码入口各自如何被新稿解释、保留或取代。 | 原稿文件本身不等于现行命题。 |

超图每个节点有稳定 ID、数学细节、状态和来源，每条超边有联合前提、结论、类型、语句和证据位置。改动成本、目录、客户均衡、编码或量词时须新建或修订命题，并同步改动依赖边。当前结论编号见[命题登记](current/claims.md)。HTML 内嵌数据，不需要服务器；GitHub 直接预览会显示源码，下载后可在浏览器查看节点和边。

从仓库根目录运行：

    python3 research/build_map.py
    python3 research/build_map.py --check
    python3 research/build_crosswalk.py --check
    python3 research/check_assets.py

第一个命令重建 HTML，后两个检查图结构、所有路径、现行稿/实现/历史来源的角色和旧入口确已退出。证明状态仍需人对数学推导负责；路径校验不会变成证明。
