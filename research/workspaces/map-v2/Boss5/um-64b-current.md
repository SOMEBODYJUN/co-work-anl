# 64b 当前成熟交付

任务：unrelated-machines-3a-3a-64bdf7ec5167df6a。核心 M-665cd08feee04456b5cb538e29d62305 v2；对端 M-8dec531708464aaa87be325982ae38fc v1。

已交一条 accepted / unconditional / contribution 逻辑边：CONFIG(T) 可行足以使 Figure 5 机器计划满整数流，故 REJECT 也否定 CONFIG(T)；确定性配置点支付核心 OPT≤T⇒满流。完整三比例负载与阈值搜索仍由目标原证明承担，未冒称 whole_result。ell2 可提升为满流、CONFIG 与整数 T 调度等价。ell3/4 的逆向由 T10、机1(a6,b5,c1)、机2仅c1 的完整整数例排除：满流存在而 CONFIG10 不可行，OPT11。

完整证明在 map/edges/unrelated-machines-3a-3a-64bdf7ec5167df6a/config-to-machine-plan.md；边在同目录 config-projection-completeness.json；收据在 map/receipts/unrelated-machines-3a-3a-64bdf7ec5167df6a.json。仅写这三项和本独立笔记，未修改源、registry、队列或 Git。

已实读两端正文，pdftotext 读取冻结 PDF，重点复核第6节9–11页并渲染Figure5。复用07fa3既有成熟机器计划辨识。本比较无新增只读端点、无来源勘误、无未闭合follow-up。

验证：edge-bind --write 绑定当前端点/证据，edge-check 通过且 proof_scope=step。另作非证明性的有限分案检查：T=1..20、q=0..4，53,129 个降序加工时间行、757,504 个子集，全部通过合法配置包含、输出行负载包络与 ell2 精确性。该检查不替代正文解析证明。

待父Boss：核对并串行 checkpoint/push/done；没有待付数学义务。
