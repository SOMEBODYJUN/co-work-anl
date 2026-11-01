# 完整DAG热启动的原代码、小证书与元资料

正式说明：[程序合同](../../../state/程序/完整终局见证的热启动向量与受限搜索合同--程序.md)、[两人原始对偶证书](../../../state/计算/两人两主题热启动原始对偶证书与版本边界--计算.md)。

三主源12485B位于original原目录布局：9844B warm_dag_search.py、2491B warm_m2p2_final.json、150B workspace.json。source-manifest.json给11个本批实际全文读取并保留的源原件（3主源、8related/依赖）、全部大小/SHA/blob/双冻结来源。original根下model/exact/certificate/init、tests/audits策略锥helper、R3d6旧DAG满足warm脚本的路径查找布局；NumPy/SciPy私有接口依赖仍须单独满足，当前未import或执行。

小报告自报warm源码20a37…与当前6e419…不匹配；旧DAGc7d550…匹配。版本与零运行边界保于version-and-execution-scope.json，不把历史小报告绑成当前程序执行；小点数学已完整解析重构。

本related审计audit_warm_start.py还引用外部Markov报告，本包未替它补齐该审计运行数据；6193BREADME的42回归/大规模报告仅按历史所述，未借此称本次读完或复跑它们。不得对这些related源额外done。

## 原件入口

| 源文件 | 身份 | 源ID |
|---|---|---|
| [certificate.py](original/customer_attraction/certificate.py) | related/依赖 | 52369ae591b07d52c7df |
| [__init__.py](original/customer_attraction/__init__.py) | related/依赖 | e34d11916a2c223f010d |
| [exact.py](original/customer_attraction/exact.py) | related/依赖 | 14e0922138e43b337600 |
| [model.py](original/customer_attraction/model.py) | related/依赖 | 999293c4e866618a72f6 |
| [customer_attraction_strategy_lp.py](original/tests/audits/customer_attraction_strategy_lp.py) | related/依赖 | 51b578ac60c377c6f060 |
| [workspace.json](original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/workspace.json) | 主源 | 29d0b0997f32f56dd8cf |
| [outcome_dag_milp.py](original/research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py) | related/依赖 | ba24829ca8aa642f892c |
| [README.md](original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/README.md) | related/依赖 | a607df1fe2b98e17868c |
| [audit_warm_start.py](original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/audit_warm_start.py) | related/依赖 | c18e27c5f56908a85700 |
| [warm_m2p2_final.json](original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/warm_m2p2_final.json) | 主源 | 23a9decde7450d02d501 |
| [warm_dag_search.py](original/research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/warm_dag_search.py) | 主源 | 0cce6d9347944260698c |
