# 二十三客户两策略原独审与本次重放

四个original文件为逐源clean show导出的冻结原字节；两份相关作者输入保于replay-root的credible_counterexample目录，本批仅作相关材料读取，不代它们done。source-manifest.json含全部定位和指纹。

冻结脚本逐一展开23单位客户，125终局、31有序节点、155含自身比较，非自身124。普通与计数策略分别91/33和95/29严格/平局。两次原入口恰各一次，exit0，stdout和空stderr保留。没有调用MILP或重跑发现过程。

在本目录运行：

```sh
python replay-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/independent_mechanism/payoff_cap_independent_audit.py replay-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/credible_counterexample/payoff_cap_failure.json
python replay-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/independent_mechanism/payoff_cap_independent_audit.py replay-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/credible_counterexample/payoff_cap_failure_markov.json
```

脚本按自身目录定位输出，会覆盖replay-root中对应生成报告；original只作历史原件保存。普通旧报告缺新增same_count_histories_same_action=false，旧全部字段及31节点表相同但字节不同；Markov输出字节完全相同。完整比较见replay-comparison.json。不倒填普通旧报告生成源码版本。

正文见[单位展开审查](../../../state/审查/二十三客户两份完整策略的单位展开独审与输出版本--审查.md)。本次为知情复核，不新增blind/外审或全局最优性认证。
