# 五独立原入口的数学与有限运行证据

本包对应唯一实际BO capture：pushed/Boss4/synced，tip `b01e708c20459c0dbd24243bc8bc92500b7c4e7b`。五实际IDs、操作和同步信息见[claim-receipt.json](claim-receipt.json)。主源都是tests/audits/unrelated_machines程序，全部认领后全文实读，不把早前comparison当primary done。本包是外部stage交付，Root串行拷入/保存/done；不称本包已推送。

## 自足数学资源

四页按实际算法和合同归档，不以独立脚本文件名代替数学内容。每页保存完整模型、为什么检查成立、输入/输出、有限域、历史先验及接续。
- [单共享任务条件耦合与长度二细分独立原入口--资源.md](../../../state/资源/单共享任务条件耦合与长度二细分独立原入口--资源.md)
- [最优凸包逐行枚举与两两负相关分布双原入口--资源.md](../../../state/资源/最优凸包逐行枚举与两两负相关分布双原入口--资源.md)
- [极小超载星独立原入口的嵌套替换与逆提升--资源.md](../../../state/资源/极小超载星独立原入口的嵌套替换与逆提升--资源.md)
- [稀释终端独立重算的导入边界与真实探针--资源.md](../../../state/资源/稀释终端独立重算的导入边界与真实探针--资源.md)

## 五份主源原件

| ID | 原路径 | 字节/行 | SHA-256 |
|---|---|---:|---|
| 04e2e91b0c5e1f5ece19 | [tests/audits/unrelated_machines/independent_dilution_audit.py](original/tests/audits/unrelated_machines/independent_dilution_audit.py) | 7883/178 | `f37cfc0a8aba8a33ece4768d0f6224bc6431dd6cd8d7eff368ee8e10721ca6e8` |
| 0468bc8a92fdec6f1dca | [tests/audits/unrelated_machines/independent_marginal_pairwise_oracle.py](original/tests/audits/unrelated_machines/independent_marginal_pairwise_oracle.py) | 3245/66 | `378962201d5446e095aa0ab94b4770b275e077a7cde647ccbc69d110d78a2bb4` |
| 7246ae704ee347f06d87 | [tests/audits/unrelated_machines/independent_marginal_row_oracle.py](original/tests/audits/unrelated_machines/independent_marginal_row_oracle.py) | 4655/95 | `1933bb8d44156fb5a1ad9c7c630e4042db8e5259d0cf04ad51c2d5ab9e77dec1` |
| 9d162c1540169a3297c1 | [tests/audits/unrelated_machines/independent_minimal_star.py](original/tests/audits/unrelated_machines/independent_minimal_star.py) | 5471/133 | `42809e43b35548d5302f4825fcfee7c491e9e81cab90433c8bdfc0ac949134a4` |
| 94a0986533814bdf05a5 | [tests/audits/unrelated_machines/independent_pair_coupling.py](original/tests/audits/unrelated_machines/independent_pair_coupling.py) | 5819/148 | `801e016e773f5abfd4d33f511a2f0d6e1d97d3889edcf177033fafab39ed3945` |

## 14份依赖和原始比较资料

| ID/角色 | 原路径 | 字节 | SHA-256 |
|---|---|---:|---|
| 02411e208331973f0c82 / runtime-dependency | [tests/audits/unrelated_machines/diluted_sink_probe_gap.py](original/tests/audits/unrelated_machines/diluted_sink_probe_gap.py) | 11101 | `9aa9c7c3390b658da10b925618ff0fed2762c61e768cf6e2c232fc3936fd9092` |
| f9cbe459c9a8df5b68f5 / comparison | [evidence/runs/unrelated_machines/independent_dilution_audit.json](comparison/evidence/runs/unrelated_machines/independent_dilution_audit.json) | 2076 | `1cc2df1a6371bae20d9e294a72e1f726d31e89afcc105cd2101573b035516ad7` |
| 12bb18f5791e321dbd5e / comparison | [evidence/runs/unrelated_machines/marginal_pairwise_independent.json](comparison/evidence/runs/unrelated_machines/marginal_pairwise_independent.json) | 2626 | `3f8c20d5ddf159b3abe2d155feca0bb332ea8beff2e6343f098bd34e6440dc9b` |
| 616620a03272d34ac4db / comparison | [evidence/runs/unrelated_machines/marginal_row_independent.json](comparison/evidence/runs/unrelated_machines/marginal_row_independent.json) | 5469 | `14ad94837033996ff1ca91e21ddbbac3629334cce2811ac745aabf65776afe75` |
| e024705ef6909102d311 / comparison | [evidence/runs/unrelated_machines/minimal_star_capacity_audit.json](comparison/evidence/runs/unrelated_machines/minimal_star_capacity_audit.json) | 14593 | `17c4dc79114969228e6eb1c7f02714b22e5145776792f3612ac057589a8558cc` |
| 528f36466ffc7a22d79e / comparison | [evidence/runs/unrelated_machines/bundle_subdivision_audit.json](comparison/evidence/runs/unrelated_machines/bundle_subdivision_audit.json) | 18097 | `c6ae7018142bbef5e2dfd4716aeea0c1f449e4b9e4e12266126167e155abed24` |
| 07f075f376fc5aa958fe / comparison | [research/current/unrelated_machines/diluted_sink_probe_gap.md](comparison/research/current/unrelated_machines/diluted_sink_probe_gap.md) | 23305 | `08c7d787759fd48b65cada97c052bdab80556bedde1e14f4601b8e4447b52ffd` |
| 8c90fcce237d7988a7a5 / comparison | [research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md](comparison/research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md) | 26982 | `bbbf4c4112d14bf656789e174c6b589c8055b466dddea58aff19199c81a21801` |
| 681999ce023678a10c97 / comparison | [research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md](comparison/research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md) | 37556 | `7713a6b8303e83fbfc46bc8c8a390f7886d4e030545376f56e7c4676ed255035` |
| 662f60ef16911ee431c3 / comparison | [research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md](comparison/research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md) | 15254 | `bbbfb292f4ce3cd02eb87864524add850075f20b938f3b9aaef0a2e54b765222` |
| a0db0c802d97be54e692 / comparison | [research/reviews/unrelated_machines/minimal_star_capacity_review.md](comparison/research/reviews/unrelated_machines/minimal_star_capacity_review.md) | 10785 | `1668ceadb7a74b85638a47d8dfc8a3003e72aca580c85c1f61ecb05ef1068620` |
| d7ea60675d8f563250cd / comparison | [research/reviews/unrelated_machines/optimal_hull_marginal_review.md](comparison/research/reviews/unrelated_machines/optimal_hull_marginal_review.md) | 25309 | `7789909f4c9ac7f3e3c718a747d19d321ecfc8a92920c4d565a53806804c744c` |
| d5e1b5b40e6c407f5b41 / comparison | [research/reviews/unrelated_machines/bundle_subdivision_review.md](comparison/research/reviews/unrelated_machines/bundle_subdivision_review.md) | 6076 | `922e1b50597affc9a617a26e1c68c4eaf17ef6e9a831cdbee36159fac65139a1` |
| 0523719ad5957d736c5f / comparison | [history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md](comparison/history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md) | 14900 | `f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894` |

[primary-inventory.json](primary-inventory.json)与[comparison-inventory.json](comparison-inventory.json)另保blob、完整冻结commit、实际源SHA和每项阅读范围。历史source052371…与现行bundle数学全文相同，已逐字节核前缀/末段关系；并非新主源done。六个既有正式对象全文比较的路径和读取SHA见[existing-formal-comparison.json](existing-formal-comparison.json)。

## 原程序没有新增运行

**本批五份原main均新run0。** 同SHA历史证据足以覆盖全部原入口，不为重复计数重跑：

| 主源 | 真实旧运行绑定及范围 |
|---|---|
| independent_dilution_audit | f9cbe…直接绑定独立代码f37…和生成器9aa…；k2/3/4向量14/74/58、全星14/74/4562、3375矩阵/8192可行σ出现；不带共享z |
| independent_marginal_pairwise_oracle | 12bb…全部六law35971支持出现；JSON本身无代码SHA，review d7ea…§7表同时绑定代码378…与该输出3f8…，§7.2真实复跑exit0且解析JSON相等 |
| independent_marginal_row_oracle | 616620…五组281090带标号σ，八大参数仅公式；review d7ea…§7表绑定代码193…与输出14ad…，§7.2同一实际复跑链exit0 |
| independent_minimal_star | e024…sha256表和reports.independent_star_reproduced.json绑定428…；seed918273、1095合法原fixture、92收缩/369拒绝/7486lift、7nested fixture/8nestedσ |
| independent_pair_coupling | 528f…sha256表绑定801…；reports.independent_final.json保存260小输入/113H区间等值/五p/九k局部断点；本main实际H1 |

不为其余旧报告没有记录的数值退出码/耗时补造字段；边际两源原review有明确exit0，注明来自该历史陈述而非本次新执行。旧聚合其他分支的4000/5000采样、k4大图、容量一pair、计数闭包和经典baseline均完整保留作比较，不能混成本主源实际新增覆盖。

稀释脚本在导入时执行自己的顶层程序，因此本批仅读原文件，不导入它以提取函数；动态依赖完整读齐并保原字节。其他四程序没有仓库导入；全部使用标准库精确Fraction/整数，无浮点或外部solver。

## 完整实际输入和新增有界数据核对

原main的所有输入均来自原源码固定字面参数、生成规则或已写明seed；没有遗漏需要另下载的外部输入。新增文档化输入和证书如下：

- [五个row完整矩阵、最优分解和x](inputs/row-five-full-matrices-and-optimal-hull-points.json)：明确job-major，保所有有标号job与原σ；不是旧report曾输出这些数组。
- [六law精确模式规格](inputs/pair-six-exact-mode-specifications.json)与[(4,2,2)全部52原子](inputs/pair-k2-r4-documentary-52-atoms.json)：完整σ、权和机器负载；逐52原子468job及所有边际/pair核验，未重跑其他五law的完整原子生成。
- [强制nested完整矩阵](inputs/minimal-star-forced-nested-full-matrix.json)：两个新文档化argmin记录、残余及逆恢复σ、原负载；新独立枚举仅此18合法σ核OPT1，不重跑1095随机fixture。
- [细分全部260字面输入](inputs/subdivision-all-260-literal-inputs.json)：原四值256+四边界、H1及OPT0→1反例；本次只文档化，260旧/新OPT的实际穷举来自旧run，不冒新跑。

[verify_saved_data.py](verify_saved_data.py)不导入或执行任何原算法。最终实际执行一次通过，Python3.12.14、exit0、耗时0.06658643099945039秒；当前代码SHA1156661ae71dc3b8d293640ba2f0da2fceab18eabd674c62394881a93e378a40。真实命令/cwd/源码与输出SHA见[执行事件](runs/saved-data-check/execution.json)、[stdout](runs/saved-data-check/stdout)、[stderr](runs/saved-data-check/stderr)与[data-selfcheck.json](data-selfcheck.json)。该核对只做上述少量新证书与保存数据闭式；原main新run仍为0。

## 版本和独立先验

[version-relations.json](version-relations.json)保存实际精确恢复：

- 当前minimal-star全文bbbf…在§7之前保一换行恢复旧be27…，旧独立收缩run和最初review只覆盖§1–6；当前§7后拟阵/配置转移/指数外包不倒填。
- 当前optimal-hull全文7713…在§10前保一换行恢复旧f666…，两边际程序及原review§7只覆盖原§1–9；后来§10冻结宏任务、§11高阶NC不是旧run检查。
- 当前bundle bbbfb…与已恢复历史f923…数学全文相同，只追加长链更强边界来源段；旧报告哈希不冒当前整稿SHA。

原review逐项区分声明先独立重构、再读作者证明、给定pair公式后独立核算、后续版本重读。程序名称independent不自动证明零信息发现；未进行新的外部评审、优先权检索或新颖性认证。原文提及外部文献的读取状态属于历史记录，本批不冒称重新取得或读完这些论文。

[comparison-findings.json](comparison-findings.json)保存所有不同输出合同/运行边界及处置，[relationship-review.json](relationship-review.json)解释四新资源与已有正式对象和彼此的证明/实现关系。只作第二阶段关系判断，未覆盖共享旧页或第三阶段超图。五source准确整理完成不等UM主目标解决；一般统一优于2、全局耦合与通用oracle仍未由本批给出。
