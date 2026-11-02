# 六十四列四阶段重优化的原件与静态核对

主正文：[六十四列必要系统的四阶段重优化与三人扩充边界](../../../state/计算/六十四列必要系统的四阶段重优化与三人扩充边界--计算.md)。八原件共176415B，保留原完整字节；[source-manifest.json](source-manifest.json)逐份给来源ID、双冻结40位commit/path、blob、SHA-256及当前相对文件位置。它们是本批正式处置的全部来源，不以旁读依赖凑额外done。

| 原件 | 字节 | 本批独有处置 |
| --- | ---: | --- |
| reopt_support.py | 1372 | 固定原64列、437+27行、float LP/覆写合同 |
| reopt_support.json | 12003 | 464全行名、64质量、41正支撑，五字段全核 |
| reopt_cross.py | 1446 | 另加70跨菜单，仍原64列，不采新列 |
| reopt_cross.json | 14453 | 534全行名、64质量与support逐值差分 |
| reopt_tax.py | 1516 | 另加1386全积税成1920行，未加对齐税 |
| reopt_tax.json | 52452 | 1920全行名、44正质量，与精确恢复对象分域 |
| reopt_triple.py | 1827 | tax后依次加276同/异税及200三人行，2396行 |
| reopt_triple.json | 91346 | 2396行/乘子、64质量；与既有aligned同点同旧λ，新200λ全零 |

[review_saved_reports.py](review_saved_reports.py)是本批新写的静态绑定及最小新增行诊断。实际执行一次，Python3.12.14、assert启用、约1.736秒，退出0。结果是[saved-report-review.json](saved-report-review.json)。原程序顶层或import运行、linprog调用、旧规范主审计、旧2196×64矩阵重查、有理对偶恢复、全型定价均0次；不是重演四份历史LP进程，也不是独立重新推导全部2396行。

核对范围：四报告全部字段、256个point、5314条逐序名字、triple全部2396乘子；定义级行名合同只在一个原子调用既有行函数，名字循环不依赖会员数。只对**新200行**在全部64列调用原triple函数并求保存二进制浮点质量下的slack，200×64系数，全部严格正，最小约2.21622232594。新200值虽以Fraction精确记录，但四份浮点质量的W均不精确等于1，不能称新精确原始可行证书。

复用并核SHA的既有依赖，**不复制其大文件**：

- `../aligned-dual-five-boss3/related/evidence/certificates/customer_attraction/five_player_indexed_bound.json`：原64有序atom定义；旧mass_numerator不用于新质量。
- 同包 `related/tests/audits/customer_attraction_five_indexed.py`：437行函数定义前缀；其后完整审计不执行。
- `../global-indexed-reviews-boss3/related/` 的五份rows函数：offdiagonal/crossmenu/menutax/alignedtax/tripleprofit；用AST只加载q/rows函数，不执行原main或文件I/O。
- `../aligned-dual-five-boss3/original/reopt_aligned.json`：2196行版本的逐值对照输入，SHA `0bce38e76961db95c79fbd1c86ce79c1364a48cbcc7bc9bce42727d1b2fe2e69`。
- 同包 `aligned_support_exact_dual.json`、`aligned_dual_exact_negative.json` 及 `parameter-and-one-column-comparison.json`：已精确审计的64列对偶和单个域外负余项；本批只核保存值/来源一致性，再由新增200个零乘子作代数继承，不重算原矩阵或负列。

五份既有helper的SHA还与根本批冻结导出逐件一致，见[borrowed-helper-binding.json](borrowed-helper-binding.json)。所有实际读取路径、字节数、SHA在新记录inputs中，实际静态核对范围在execution中。当前运行是在仓库外暂存交付树进行，所以部分原件绝对路径指向当次暂存位置；永久相对位置由source-manifest给定。提交后可从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/reopt-four-stage-boss3/review_saved_reports.py --repo .
```

保全关系依据见[relationship-review.json](relationship-review.json)。这是阶段二正文接续资料，没有自动写第三阶段超边。本批没有新完整SPE、原模型反例、全型最优证书、六人结论或外审/新颖性认证。
