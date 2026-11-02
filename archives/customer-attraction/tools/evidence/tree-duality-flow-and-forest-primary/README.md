# 收益图闭集、森林与原定义级回归

本证据包复用已存在的8942B `payoff_form_graph.md`原件并补齐同目录六原件；原稿及两程序/两JSON/入口/分数覆盖审查共七源28034B。每份实际大小、SHA-256、源ID、两个冻结commit与完整原路径见[source-manifest.json](source-manifest.json)。所有original保持冻结字节；没有修补原脚本。

数学与精确范围见[闭集散度与森林定理](../../../state/定理/真实收益图的闭集散度判别与森林证书--定理.md)和[原程序合同](../../../state/程序/收益图闭集与森林压缩的定义级原审计合同--程序.md)。前者的五客户完整SPE段由本批补齐，SCC非最大后继和一般half缺口保留。

仓内此前没有这两个原入口SHA绑定的成功执行材料；本次在clone外复制相邻文件后，以新Python3.12.14进程按顺序各执行一次 `graph_probe.py`、`graph_flow_audit.py`。均exit0、stderr空，生成3396B与782B JSON逐字节同冻结原件；无需存第二份同字节JSON。[replay-metadata.json](replay-metadata.json)保版本、时长和输出哈希；两`.stdout`和`.stderr`保实际过程输出。source manifest是来源身份，重放事件是本次有限过程，二者分开。

`graph_probe.py`无main guard且覆盖写相邻输出；`graph_flow_audit.py`有guard、固定全局随机种子并读取相邻动作JSON。要重放应先复制到隔离目录、保原名、正常assert，不在original直接执行。无规范solver、NumPy、SciPy或外部数据依赖。

有限运行覆盖136个二主题二/三人完整形式策略、每图四个指定整数散度（合544项）、35可行流、137流形式/森林槽；五客户策略另核40完整节点120项含自身IC、30收益顶点33合并非自边、末端维数0/SCC像1。没有全客户域、全整数散度、一般half或完整lineality认证，也没有新增盲审/外审。
