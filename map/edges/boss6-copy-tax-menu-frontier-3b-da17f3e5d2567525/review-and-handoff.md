# Boss6 round44：全集、复制税与两种Pareto菜单的具体3B比较

本轮数学完整成熟，无新原文错误、无read-add需求。只读clone `/workspace/scratch/bbb425bb840f/co-work-anl-boss6`；产物按实际task write_paths镜像放在仓库外staging。task owner Boss6，request `306b364b91a2443cb06dc4e881f38f03`，definition pin `d471b84d7aa4bf139fecbeb696c3e2b69b98b2729f960203de106ab0603dc15f`。父已核pushed remote `0e2f56e4c9b67b4e5a755aa149394f16a3998eec`；worker没有再作远端或Git操作。

新逻辑边 `ca-round44-exact-outcomes-give-minimum-copy-tax-dp` 为 accepted/unconditional/whole，完整推出M949当前注册陈述，包括终端0、keys E=全部可实现R、阈值L、每终局最小实际路径标量复制税、最小值达到及固定输入最大PC6缺口。不是仅证明终局可达部分。

关键独立推导：固定终局f时，当前玩家及每个已行动祖先的最终收益全部不变；Q(c,a)仅依当前计数和行动并只沿规定路径相加。因此实际孩子可在同一f纤维中取税最小完整子SPE；其它有序孩子可分别取令各偏离者收益最小的子SPE。子树不相交，完整拼接仍满足全部真实IC。必要方向从任意完整σ的真实孩子逐项给下界，充分方向给达到下界的完整策略，故递推精确。再按f对全部σ分组即付清max-gap最后一句。

新语境边 `ca-round44-pareto-obstructions-motivate-terminal-fibre-boundary` 为 motivates/context：两Pareto规则跨不同终局删点，会改变祖先终局收益与偏离地板；M949始终保留每个f，只优化其纤维内部一个成本。max三例A/B/D各一次删除，最坏W10→11、11→12、18→21；min独立例C五次删除，根T4地板31/6→37/6，W15→17。A/B/C/D人数4/3/3/4，不能声称六人Pareto反例，不给M949造refutes。

| 核心 | coverage | 本轮实际结果 |
| --- | --- | --- |
| CA-EXACT-PURE-SPE-ALL v2 | linked | 为新增完整六人标量成本定理提供精确全集与有序拼接全部前提 |
| M-94942bfb644042ea8039e44db39d1504 v1 | linked | 整条理想算法定理及最大PC6缺口均已付清 |
| M-66132ab86a054b33b1c753158dd4f3ad v1 | isolated-after-review | 完整核其独立极小方向反例及与固定f成本优化的区别；只有准确语境边 |
| M-e3fc9489148a4369adfc1e663579be9c v1 | isolated-after-review | 完整核其三份极大方向反例及与固定f成本优化的区别；只有准确语境边 |

普遍PC6和六人half仍未由算法正确性解决。每个f各有最小σ，绝不意味着同一σ共同最小化多个f、客户税向量、多个查询或离轨枝预算。计数只缓存可实现集合和数值，不将完整策略限制为Markov。势/税全用未缩放有理量；源实现60倍记号、七标签生成域、int64/10^30哨兵及有限阴性报告各守原范围。

当前canonical的1553边元数据已逐条筛查，17条与四核心入射，本轮两个精确source/target/kind组合均不存在。48a已canonical的 M949→PC6 是固定输入contribution，与本轮 CA-EXACT→M949 whole 不同，不复制其边。48a独立DP推导按原SHA复用，作为evidence及成熟合同。460保存包已读相关review/ledger，但不是本轮canonical边来源，不继承其未完source修订状态或无关pins。

完整阅读三核心正文、共同模型、势候选定义全文、四核心记录、48a独立推导及已有contribution边；Pareto大JSON只读四例完整菜单/地板/所有删除事件和合同字段，有序树303节点1430比较按精确SHA成熟合同复用。33条declared refs对应32 distinct文件，全部SHA匹配；其它附件仅hash，不冒称全文实读。阅读账本逐文件区分。0原main/LP/RNG/全树/旧报告重跑，无规范clone写入。

task未声明overlap_comparisons，closed_overlaps=[]、follow_up_tasks=[]；无须为已解决比较造承接任务。

两边已用只读 `research_runtime.edge_bindings`、`verify_endpoints`、`require_edge_result`核当前端点/证据/标题和结果范围；返回的bindings仅写入staging边JSON。原生CLI不接收仓库外绝对staging路径，未改clone。Root安装后须按真实仓库相对路径运行edge-bind --write/edge-check；若bindings和数学文字未改，SHA应保持当前值，否则先更新manifest及receipt。最后复核远端owner/request/definition/four-core pins，checkpoint pushed后done并assemble。manifest只列其前置新资产，不hash自身/receipt；receipt列manifest等assets，不列自身，避免hash环。最终完整file SHA还会在worker交付消息给出。
