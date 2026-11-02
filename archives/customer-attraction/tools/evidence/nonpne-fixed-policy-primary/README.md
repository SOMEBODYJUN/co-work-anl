# 非PNE完整策略搜索三原件与固定点精确证据

正式对象：[搜索程序合同](../../../state/程序/保留静态盈利偏离的完整策略锥搜索--程序.md)、[五人七主题整数见证](../../../state/计算/五人七主题非静态均衡完整策略的整数见证--计算.md)。三直接源分别332574、5950、87196B，共425720B，全部实际读取并与本次正常clean show的冻结size/SHA/blob核对。

## 原字节及真实依赖

- `original/nonpne_best.json`：保存最佳五人七标签点的全部18客户类型、2801有序动作、实际终局计数、ratio、静态偏离标签、参数和step；原canonical标志单独保留，不代本轮数学审计。
- `original/nonpne_cone_probe.py`：原5950B搜索入口，不作修改；不要在证据目录执行，它覆写自身目录下两个JSON。
- `original/nonpne_run.json`：原1500条记录及所有外层字段，绝不以新结果替换原报告。
- `related-original/R84-workspace-README.md`：同工作区根入口，完整比较，不额外primary done；原一般half、旧身份/团队/路线是历史内容，非当前执行指令。
- `source-manifest.json`：三直接源、一个相关README、五项本地代码依赖的完整commit/path/id/blob/size/SHA及原件地址。

实际动态加载的是原R18 `counterexample_search/cone_walk.py` 11291B，SHA为766ae31b…，已全文读且同冻结字节复用；不是另一2784B同名脚本。其完整原件在既有`R-18-harmonic-counterexample-20261031/original/cone_walk.py`。规范四模块__init__/model/exact/certificate复用`root-static-security-and-paired-lift-program-contracts/source-root/customer_attraction/`的同SHA已发表原件。NumPy/SciPy/HiGHS是原发现器外部运行依赖，历史版本未记录。

以上依赖路径按结果仓库根解释，见manifest的preserved_repo_path。若未来确需运行原发现器，应按每项source path在隔离树恢复原布局；不能把本证据包简单import当成原目录。新固定点审计不需要这些依赖。

related-original内根README保持原字节，其相对链接仍以原R84工作区解释；没有为修复历史导航而改写原件或顺带导入本批未处理的其它选题。新写正文和本证据入口的链接按当前结果目录核对。

## 全文阅读的可逆排版

- `policy-depth-lex.json`保留best全部非动作字段，并以每深度完整0…6动作串无损表示2801动作；原数组恰按depth/lex排序，已逐值重建相等。
- `policy-depth-lex.md`把同一完整动作表按深度及前缀排版，正式计算正文也含该全表。不是只列actual或计数商。
- `run-lossless.json`保全部外层字段、17个完整payload及有序连续step区间，解码逐项等于原1500条records；浮点不猜有理数。16个非零事件亦已全列入程序正文。
- `record-analysis.json`列16条所有原字段、1484条零事件、21个原候选计数和保存点身份；其余15份完整见证不在三原件中，不能独立重验。

## 本轮唯一一次新数学执行

`audit_fixed_witness.py`只用Python标准库，只读保存最佳JSON。它不导入作者代码或规范solver/verifier，不运行LP、BI或随机。L=60整数系数精确代表不同单位客户的均分；全部2801历史、19607含自身比较/16806非自身比较通过。输出保在`fixed-witness-audit.json`，所有节点的完整七收益值保在`exact-ic-data.json`。

精确IC数据用276个完整payload和每深度词典序索引无损表示；payoff均为60倍整数，包含规定动作。audit输出的exact_ic_data_sha256指该数据按紧凑JSON编码后的哈希，不是缩进文件字节哈希。

实际结果：actual00466，W1250000，OPT1992009，ratio1992009/1250000，half余量507991。第三位静态4→0冻结尾66多得1250=W/1000，真后继改为65则无收益增加。这一固定输入真实通过，不赋其它15日志点新核验身份。原程序/模块import/Engine/LP/BI/随机重跑均0，固定输入新数学审计恰1次，没有新外审或blind身份。

可复现这一固定审计的逻辑命令（在本包目录）为：

```sh
python3 audit_fixed_witness.py --input original/nonpne_best.json --output fixed-witness-audit.json --ic-output exact-ic-data.json
```

该命令会写两个指定输出；若复核应选择新的输出文件。原发现器不在本轮执行范围。

`relation-evidence.json`供父方阶段三逐边判断来源、实现、有限核验及Ra0曾缺输入的依赖链，不直接生成正式图。`selfcheck-results.json`另记录原字节、可逆排版、JSON/语法/链接/回执目标检查；这些字段检查不替代数学判断。Ra0原部分运行/未运行记录保持历史真实，当前得到输入不等于其BNS/AP已经被本轮运行验证。
