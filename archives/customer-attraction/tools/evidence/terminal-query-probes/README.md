# 实际终局查询、LAST探针与顺序遗漏勘误

数学入口：

- [终局遗漏客户的顺序偏离份额](../../../state/引理/终局遗漏客户的顺序偏离份额--引理.md)
- [半因子勘误与净需求](../../../state/障碍/遗漏份额支付的半因子勘误--障碍.md)
- [实际终局额外查询反例](../../../state/反例/实际终局额外查询的三人反例--反例.md)
- [程序、输出和复现范围](../../../state/计算/实际终局查询与LAST探针的核验范围--计算.md)

`original/`逐字节保留本批九份源文件以及七份已处理过的运行依赖/输入；[PROVENANCE.json](PROVENANCE.json)记录源ID、完整冻结提交、路径和SHA256。依赖不是本批重复done的来源。三份独立纠错与最终修正版分别保存，未用改写旧稿消除原错误身份。

## 重建一个明确输入的可运行目录

从仓库根执行，目标目录必须尚不存在：

~~~bash
python3 -B archives/customer-attraction/tools/evidence/terminal-query-probes/stage_probes.py \
  cleanup/workspaces/Boss3/customer-structure/query-probes-fresh
~~~

该步骤只复制并逐文件验证10个运行文件：三个原探针、四个规范customer_attraction模块、一个策略锥模块、十一客户输入和同名旧规范证书。目录保持原`research/workspaces/...`、`tests/audits/...`、`examples/...`层级，使两个security程序的`parents[5]`与本地导入都有效。

它不是历史整个examples目录的重建。冻结失败报告、数学稿和纠错原件保存在本证据目录，不复制为新执行输出。需要新增输入时应另明确其出处和范围。

## 重放明确正例的原精确程序

在新的目标目录上加`--run-extra`：

~~~bash
python3 -B archives/customer-attraction/tools/evidence/terminal-query-probes/stage_probes.py \
  cleanup/workspaces/Boss3/customer-structure/query-probes-extra-fresh --run-extra
~~~

辅助程序设置新目录为cwd和PYTHONPATH，保留原脚本全部字节，清除子进程的PYTHONOPTIMIZE环境选项，且不给-O/-OO。原程序自身会在其目录写`actual_extra_candidate_failure.json`，因此不能直接在`original/`运行以免覆盖冻结报告。

本轮只实际执行一次，Python3.12.14，退出0、stderr为空。它对这个单输入找到8个可实现终局计数、2个正差，生成的AAB报告和冻结4134字节原报告逐字节一致，SHA256均为`1acd1404ec8d7f3d594b1bc0525dbb98ea64cd9734ea74d539b624a5fc47a568`。报告完整保存31动作与31历史/124非自身偏离认证；8不是完整策略数。

[运行清单](replay/stage_manifest.json)、[完整stdout](replay/extra_stdout.txt)、[stderr](replay/extra_stderr.txt)和[新报告](replay/actual_extra_candidate_failure.json)分别保存。程序输出的FAIL表示被检验辅助不等式失败，不是运行失败，也不是half反例。

## 新增精确查询对照

~~~bash
python3 -B archives/customer-attraction/tools/evidence/terminal-query-probes/audit_fixed_query_values.py
~~~

这份本轮新标准库程序读取冻结客户和完整策略记录，计算终局额外查询向量、末前LAST核、显式有理p/q上下界，并对账旧规范证书的四处末位平局差异。它不重新搜索或验证全体SPE。完整结果在[fixed-query-comparison.json](replay/fixed-query-comparison.json)。

本例额外查询最大值为3；真正LAST值为7/3，且3M_b=7≤8。新有理证书与旧报告分开保存，没有把新计算写回旧历史输出。

## 两份浮点LAST探针的继续使用

重建目录已包含其所有仓库内导入及一个明确种子；运行还需要NumPy和SciPy。原路径为：

~~~text
research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security/probe_last.py
research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security/last_cone_attack.py
~~~

probe_last的主程序可接一个根目录参数，跟随同名证书的实际路径后打印数值minimax。last_cone使用自身相对根和seed942137，尝试固定完整策略锥内的交替重数/查询优化。可在重建目录作为cwd用普通Python运行相应路径；这些是供后续显式探索的入口，**本轮未执行这两个主扫描函数**。

数值value/row_opt未充分检查求解器成功状态，主probe不验证所有离轨激励；cone程序虽然精确恢复实例和策略激励，最终安全值仍用浮点比较。因此输出只能按正文范围解释，正候选需另给精确查询下界，阴性输出不证明LAST。last_cone成功时会覆盖自身目录的`last_candidate.json`，应始终在新的明确工作目录使用。

零客户和零福利仍属于原模型；原搜索的W=1归一化没有处理这类全部边界。目录没有冻结时，glob顺序和随机流也不确定。本资源不以一个可运行种子代替历史全部输入或一般数学量词。
