# 混合强PAIR程序证据

[正式程序对象](../../../state/程序/新回复与旧主题的混合强配对行程序--程序.md)保存全部量词、三真实IC、72键、12查询、列公式、原CLI合同和有限结果。原主源1527B完整保在[original/mixed_pair_reply_rows.py](original/mixed_pair_reply_rows.py)，只读比较的较早7749B同名混合投影保在[related/older_mixed_pair.py](related/older_mixed_pair.py)；两者不是同一个程序或行系统。

[audit_mixed_rows.py](audit_mixed_rows.py)是新增标准库精确核：从原数学函数AST加载被比较实现，独立一侧按单客户收益和六个具体索引边重建。它核160个有符号三IC恒等式、两点各72×1905系数、每点8条旧query映射的8×1905系数；全部通过，8条旧cut仅3个distinct向量。脚本运行一次，完整72条余量见[exact-audit.json](exact-audit.json)。它不调用整个图或优化器，不重算其它图行、O/W或SPE。

从仓库根可用以下命令重现局部核验；输出路径选隔离位置，避免覆盖本包证据：

```bash
python3 -B archives/customer-attraction/tools/evidence/mixed-pair-reply-rows-program/audit_mixed_rows.py \
  --source archives/customer-attraction/tools/evidence/mixed-pair-reply-rows-program/original/mixed_pair_reply_rows.py \
  --old-query archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/old_query_reply_cuts.py \
  --priced archives/customer-attraction/tools/evidence/combined-branch-master-program/dependencies/customer_attraction/priced_hidden_reply.py \
  --cuts archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/old_query_cuts.json \
  --point archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/all_reply_floors_exact.json \
  --point archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json \
  --out /tmp/mixed-pair-local-check.json
```

原CLI本轮只执行一次，输入是上述旧floor点。它报告7负行及负最小值，仍退出0；这是程序预期的报告功能，不能把退出0解释成可行性PASS。事件、完整stdout和空stderr在[rerun/](rerun/execution.json)，主源、两个直接依赖及原点四文件前后SHA不变。输出是Python字典repr，不是JSON。clone外原执行只跑72行，不跑LP。先前5108行联合入口的原复放另见[共享事件](../combined-branch-master-program/rerun/execution.json)，本轮没有重复该整图。

如要重跑原CLI，应在隔离目录按 `research_3/mixed_pair_reply_rows.py`、同目录 `old_query_reply_cuts.py`、根部 `customer_attraction/priced_hidden_reply.py` 的布局放原字节，并以根部 `work.py` 文件作为旧代码找根标记（标记不被导入执行），然后运行 `python3 -B research_3/mixed_pair_reply_rows.py <原点JSON路径>`。原程序没有`--verify`开关，也不写文件；日志由外层保存。所有来源SHA、实际运行与读过的比较源见[manifest](manifest.json)，本地格式/链接/targets/原件核见[self-check](self-check.json)。
