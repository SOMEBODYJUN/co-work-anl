# Support note: finite eight-theme witness and credible-continuation interface

任务 `customer-attraction-3a-3a-a37d9a24b357c2d8` 的核心 `M-69317c7da9a34834b0e93efeaa77f0ef` 是一个**有限完整 SPE 见证**：五名提供者、八标签、16 个正客户类型、总重数 1795；指定策略保留全部 4681 个有序历史，实际路径 `(5,1,1,0,0)`，终局计数 `(2,2,0,0,0,1,0,0)`，每人收益 200，`W=1000`。五标签组合 `(2,3,4,5,6)` 覆盖 1791，且全 56 个组合的最大覆盖为 1791，所以该点的 `OPT/W=1791/1000`。

精确节点账 `all-node-comparisons.json` 对该数组给出 4681 节点、37448 含自身比较、32767 非自身比较、31208 严格非自身比较、最小 slack 0、无负 slack。私有重数 `(1,1,3,198,198,3,198,1)` 满足 `1000*n_singleton >= W`，因此八个物理覆盖集两两不同、互不包含并均极大。

唯一交付边是 `M-69317c7da9a34834b0e93efeaa77f0ef` → `CA-CREDIBLE-CONTINUATIONS` 的 `implements` 上下文边：`Engine.solve` 的精确计数递推、`cone` 的有序历史展开和离轨孩子门槛与可信续局菜单接口一致，本对象的保存策略是该接口在固定 m=5,p=8 输入上的一个具体全历史实例。该边只记录实现/语境对应；不承诺 `CA-CREDIBLE-CONTINUATIONS` 的全称定理由有限样本推出，也不承诺本实例的全局最优或所有 SPE 福利。

与同页七主题对象 `M-44d519528ba04dd3b348a9bdb1c31d16` 的 overlap 已消解：共享程序、审计和同一 `1791` 比值来源，但输入、标签数、客户表、策略图和量词不同；无迁移或重复边。普通/pilot 九客户同覆盖别名也不属于本八主题对象。完整 half、`min_SPE_W`、全局搜索和更大 m 的 int16 实现风险均保留为边界。
