# 单home级联原程序、历史审查与冻结证书

数学正文：[完整查询族定理](../../../state/定理/单home级联的完整查询族与可加费用--定理.md)。程序/审查说明：[分层证据](../../../state/计算/单home级联原程序与分层审查证据--计算.md)。

`source/` 保留认领的规范构造器和root review原字节；`inputs/` 保留14机14任务fixture；`frozen/` 保留旧成功8模式输出；`history/` 保留v1两份与v2四份冻结声明/证明/审查；`comparisons/` 保留对应canonical。逐文件冻结源ID、commit、SHA和大小见 [provenance.json](provenance.json)。这些比较依赖未在本批额外认领或done。

旧成功run的程序/input SHA与原字节精确匹配，故本轮没有重复运行原构造器。新增 `verify_frozen_record.py` 只读取旧证书，不导入或执行构造器；从原矩阵用Fraction独立核两输入和8输出的140个原任务归属及140个全机负载，并核路径原端、支持、费用和余量。实际exit0结果见 [frozen-record-verification.json](frozen-record-verification.json)，它不代替一般定理的证明，也不计算OPT。

若需要重新检查旧证书，可执行 `python3 verify_frozen_record.py` 输出到stdout；给一个不存在的新路径作唯一位置参数时，使用独占创建，拒绝覆盖。原构造器将来用于新实例时可执行 `python3 source/single_home_cascade_query_separation.py --input <new-input.json> --output <new-nonexistent-output.json>`。`--subset`只处理显式JSON列表；不提供时读输入的 `audit_patterns`，缺省仅全query。请不要把一次旧成功记录复制成多次实验。

历史最终组合的“软件pending”和后续root真实成功run是两个时点。原Exact-first独立身份依原记录保留，本轮只是读过程序/证明之后的语义核对和独立旧证书回算，未新做blind审查。外审、全球优先权及一般UM近二目标均没有因本证据包升级。
