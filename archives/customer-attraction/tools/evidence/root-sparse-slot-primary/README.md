# CK 五主源：父方额外槽报告与稀疏槽作者证明

原25来源claim回执[原样保留](original-25-claim-receipt.json)，pushed/Boss4/synced `9bff88d715e258bf152edf97073591b1652307e2`；本包只声明planned root_ck的5交集，详[authority](claim-intersection-authority.json)。不接管另20主源，不触碰Boss3 BY5或已done两生产者。

五原件本地齐且核inventory SHA/字节；3份用Root已有source，2份用已提交额外槽贡献中的比较原件；其余数学比较从本地Git blob只读取得，`GIT_NO_LAZY_FETCH=1`、`protocol.allow=never`。本批从未clean show或发网络。

主原件（完整逐字段/逐节阅读）：

- [3564da928d1da0e50943 — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/extra_slot_independent_report.json](original/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/extra_slot_independent_report.json)，1460B，SHA `89f666def96e5408ef43d099f4468878779110ffd83cb21a0262925ca0b06ad8`。
- [b4e64f98e7453d4d228a — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/nonempty_padding_report.json](original/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/nonempty_padding_report.json)，722B，SHA `700fb6b173611ab8d56afa62644ef85a3b329e5bfd4f76cfff9b2202bcf09c58`。
- [1fcf4d32e4c24b455d9f — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/chronological_sparse_rent_audit.json](original/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/chronological_sparse_rent_audit.json)，535B，SHA `19e80bc2890ad906ac50467a966d552b753248394d77bfcbe67209c74e067683`。
- [a8f608020c5f7b69f334 — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/sparse_slot_complete_spe_audit.json](original/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/sparse_slot_complete_spe_audit.json)，500B，SHA `754eb43745fc8eed9d55dd8795823554a2b336107150ebc9d0d7f9bd26d9ab62`。
- [a736ca58ff82a1a2192b — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/sparse_slot_complete_spe_obstruction.md](original/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/sparse_slot_complete_spe_obstruction.md)，5464B，SHA `4594a404e513e2e27881ca8f190deec227e107788f8b842e24b34ca8bc3110f1`。

比较原件（完整读，comparison-only，不抵primary done）：

- [251ddedf0a4a923e6fc4 — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/audit_sparse_slot_complete_spe.py](comparison/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/audit_sparse_slot_complete_spe.py)，SHA `4e50d31d0e2bd298a7708cc0dcce00edb73a2c17e488079874466cd4f457498c`。
- [2a3ae62cdcb1da780b81 — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/audit_chronological_sparse_rent.py](comparison/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/audit_chronological_sparse_rent.py)，SHA `fc059b95363385506568e7bfd1f2164c43d2f6bfe1d482b1f74181bd5611adbb`。
- [512a98c3ca26894b432e — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/nonempty_padding_transfer.md](comparison/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/nonempty_padding_transfer.md)，SHA `89d2ea9f8ce8c0b529027814a2633597112f65b612eee82b6ebf60eac2305e20`。
- [708e078a449b904a88de — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_nonempty_padding.py](comparison/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_nonempty_padding.py)，SHA `da69294d9c2150ef68cb29e95d833f5b7b13a98dc7c684740180674e289365fc`。
- [747065dc4abd4929807d — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/path_interval_rent_budget.md](comparison/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/path_interval_rent_budget.md)，SHA `7e5aef9e2ecf35d9ae24ad8012d8dfcf39b36a79fd36d695ce9d2d9176482b23`。
- [94bf0c2e1187fd8ae253 — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/chronological_sparse_rent_and_skip_premium.md](comparison/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/coupling/chronological_sparse_rent_and_skip_premium.md)，SHA `622e3e7f58d5b51f6c617bebd9dfd6a77b652dca6e9b6b5afdc17c0b6daf11f3`。
- [b853d289bf1362f8cdef — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/extra_slot_independent_review.md](comparison/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/extra_slot_independent_review.md)，SHA `efa424bd20475f4d2351872969b40990ac6a4296f1e3c731590a8401f42c3f0f`。
- [c814b3d572d72f7d9eaa — research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/sparse_spe_rent_review.md](comparison/research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/sparse_spe_rent_review.md)，SHA `08198ded26246d38d8fd5feaa30e266223ac8b43e08d8e5ef48cf05846a1bce1`。
- [f3b5851cc7fb29ce4d0f — research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_extra_slot_independent.py](comparison/research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_extra_slot_independent.py)，SHA `db1fb3c980ae6985c43177a95bb9d15830b7079b411ff9186eb8a3d5ddeb8d0a`。
- [f218c3c894b4635ecca2 — research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json](comparison/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json)，SHA `14f8b29548715323a8ee6eac0fabc3efb7e8ea0537fb34cd866c66ed131c855d`。

| 证据 | 实际范围 |
|---|---|
[两旧报告成功运行](execution-boundaries.json) | extra两生产者事件/完整stdout均已提交且与本primary字节相等；复用，本批不执行 |
[parent-aggregate执行记录](historical-runs/parent-aggregate/execution.json) | 原exit0/命令/cwd/源码及stdout SHA |
[parent-padding执行记录](historical-runs/parent-padding/execution.json) | 原exit0/完整旧输出，不改时间/次数 |
[新有界helper源码](verify_report_data.py) | 无原程序导入/执行，不重做全树或259080循环 |
[新有界检查结果](new-data-check/result.json) | 旧byte绑定、四计数公式、q2/3/10租金、超载离轨收益 |
[新检查事件](new-data-check/event.json) | 一次exit0、stdout/stderr/SHA；缺开始时间不虚填 |
[未应用旧页修订](unapplied-correction/whitelist.json) | 精确旧SHA/before/proposed/patch三处，未写共享页 |
[相关查核](comparison-findings.json) | 完整数学关系与实际执行证据边界 |

稀疏两生产者虽有Boss3已done原源码，但本地没有找到其成功stdout/event，因此只保存原535/500B有限声明与完整源码/证明。读过源码不算原run，父方初始成功线索未被当作事实。原main新run总0。

一般proof/有限报告/新小检查分开：SPE任意χ与全部离轨分支、ρ任意正、q增长导致reset调和发散，而clock有共同预算；真实全树运输与当前六人half仍开放。q3正好六人但W=OPT=2，不反驳目标。

复现新数据checker应在另一个新空目录运行其绝对路径，避免覆写已保存result/log。生产者若以后需要真实重跑，应另设空目录/原输入结构记录真实事件；本包不自动重跑已足够的额外槽原入口，也不为凑稀疏run数量执行。

