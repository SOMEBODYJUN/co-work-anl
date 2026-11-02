# 最坏可信终局与静态CCE差值发现器的原程序合同

正式对象为[程序正文](../../../state/程序/最坏可信终局与静态CCE差值交替发现器--程序.md)。主源ID `60bd06f1f9dcdc4e5347`，原件为4806B；`source-manifest.json`给两个冻结提交、完整路径、blob、SHA-256和本次逐提交字节核对。`original/search_cce.py`保持原字节，没有认证信息或本地身份文件。

原程序只需Python、NumPy和SciPy/HiGHS，无仓库内文件依赖。默认k4/m3/trials1000/seed1，`--out`必填；运行原main会随机发现、打印进度并多次覆写out，原程序不自动创建父目录。本批未调用原main、随机搜索或客户交替LP。`solve_spe`先用计数可实现集合重构一棵全部有序历史策略，随后main固定该树，只交替修改客户和重求同人数静态CCE；target是计数的排序代表。

`check_small_contract.py`是本批独立小型接口检查。它只调用原模块data/solve_spe/cce，自行从整数客户实现Fraction收益、全部有序历史可信递推、全部真实偏离及Γ系数，再以全部有序终局的逐玩家CCE LP比较原计数LP。五例为三单例、零客户、单人、空及重复覆盖标签、单主题。它不导入规范模型、求解器、旧审计或候选JSON。

从仓库根复核当前小检查：

```sh
python3 archives/customer-attraction/tools/evidence/security-cce-search-program-primary/check_small_contract.py
```

这会覆写本包`small-contract-check.json`；其原始本次执行的argv、耗时、源码指纹和stdio在`small-check-execution.json`及两个txt中。五次原CCE LP与五次独立个体LP一致，三单例数值21/10；数值库版本是Python3.12.14、NumPy2.3.5、SciPy1.17.0。这是小规模接口检查，未认证所有参数、全局交替最优或新反例。

`comparison-reading-manifest.json`记录实际全文比较的正式数学/资源正文；`repository-related-search.json`保存本轮全仓相关检索的命令及匹配位置；`prior-mature-evidence-reuse.json`接受已存八/四十二客户精确重放及其公开资源合同，未再运行原审计。`relation-review.json`给实施、发现、有限检查关系和未付全称边界，没有生成第三阶段图。

`self-check.json`是原字节、JSON、Python AST、文内链接和交付文件自查，不代表数学证明。逐源receipt在`cleanup/workspaces/Boss7/resume-current/cce-program/receipts.json`，只有父方checkpoint确认推送后才可将主源done。本包没有执行claim、done、checkpoint或公屏消息操作。
