# 5180与5189联合回复图精确输入点

正式对象：[联合回复图的扩展切面与局部查询精确点](../../../state/计算/联合回复图的扩展切面与局部查询精确点--计算.md)。

source-manifest.json保存两个primary原点的完整双冻结版本、原路径、源ID、大小和SHA；original保823005B latest及822687B local完整原字节，包含全部1905列及零质量。两点都是K1/hist16/joint582/overlap1306，不能将辅助质量当新增客户。

关键模式：latest是5180=5108+72；local文件实际header是5189=5108+72+5nested+4requery，正确对应 --latest --new-local。单独--new-local只有5117行却用同一local文件名，不能冒完整原图核验。一次构造5189超集的前5180恰latest，追加次序及原行名前缀已验证。

实际唯一构图事件：

- verify_both_points.py导入未改冻结combined_branch_master，build仅调用一次；没有原CLI或优化器调用。全部数学代码/依赖/输入/输出均在clone外新树。
- 对latest向量精确核前5180行，对local核全部5189行；均O1、保存W匹配、全部已列行非负/min0，零行分别2278/2282，1905个嵌套描述符/长度和全部weight完整核对。
- latest在末9条局部行全负，新local全非负（5个零、4个正）；前5个nested原负值与冻结发现字段完全一致。
- 两点描述符相同，但218质量变化：K1/hist11/joint102/overlap104；W/K/hist均不同。完整差异和具名余量见replay。
- run_once.py是本事件组织脚本，execution-record/stdout/stderr保存真实37.59秒、exit0、stderr空。不是两次CLI、两套独立全矩阵或精确最优证明。

后续有限检查只复用已审三切面包的27条稀疏向量：apply_certified_cuts_to_local.py先校原长度与row哈希，再核共同1905描述符。22条原5180负记录移到5189：8容量全正，14再查询为7负/4零/3正，其中两条对角重复，故仍6不同必要再查询负。5个pending原长2033且尾128全0，核后才移入1905；portfolio负/正/正、requery两负同向量。该程序没有重构系数、调用原row helper或LP，也不将原5277的负分数贴成新5189值。

replay文件：

- two-point-full-verification.json：原build身份/追加顺序、两输入全部标量和当前表、218逐列差异。
- latest-all-superset-row-slacks.json / local-all-superset-row-slacks.json：每点全部5189个具名精确余量，明确本点原矩阵纳入范围，旧点末9负条不冒已列行。
- certified-cuts-at-local5189.json：全部27参数、原绑定点/原已审值、新5189精确值、原1905/2033长度、hash与重复身份。
- execution-record.json / stdout.txt / stderr.txt：一次真实事件。

复现时从仓库根材料化到一个新独立绝对路径：

    python3 archives/customer-attraction/tools/evidence/combined-latest-local-points-boss3/materialize_runtime.py /absolute/new-runtime
    python3 -B archives/customer-attraction/tools/evidence/combined-latest-local-points-boss3/verify_both_points.py /absolute/new-runtime
    python3 -B archives/customer-attraction/tools/evidence/combined-latest-local-points-boss3/apply_certified_cuts_to_local.py /absolute/repository-root

材料化复用已持久保存的47源树并覆盖两输入；根work.py只是找根用的注释标记。第一条不构图或优化。第二条需要NumPy/SciPy且assert开启，后两条只更新本包replay当前报告，不改original。run_once.py拒绝覆盖已存事件记录；重现可直接调用上述回代脚本，不能把它当现有事件第二次运行声明。

全输入行合法性由既有模型/真实IC证明承担；当前同实现构图精确可行、缺行负值和完整SPE是不同等级。一般/六人half仍开放，没有完整策略反例、精确最优或全支持不可行证书。
