# 旧客户信用三族独立审查的主源与本次原程序复放

数学与证据责任见[审查正文](../../../state/审查/旧客户信用三族的独立重构与产品强化审查--审查.md)。四原件共17953B，全部由`clean show`导出并完整读取，两个冻结提交的commit/path、字节数、SHA256和Git blob见[source-manifest.json](source-manifest.json)。原件不改语义：

| 源ID | 原件 | 字节 | 内容 |
| --- | --- | ---: | --- |
| 7b788a34f774f8480303 | [audit_independent_credit.py](original/audit_independent_credit.py) | 5457 | 新AB完整计数策略、所有合法计数状态、三族精确利润及两种信用矛盾算术；仅标准库 |
| 90198b79d5aec8bce280 | [independent_credit_audit.json](original/independent_credit_audit.json) | 1252 | AB/all-big/overlap及两种矛盾的全部字段 |
| 429b5fcf06c0d9e6d4c3 | [independent_credit_product_review.md](original/independent_credit_product_review.md) | 4591 | 先精确陈述的产品审查；全历史SPE、F严格可加、相同旧H矛盾272，完全不要求G可加 |
| 53e2ae50b2d829f220f0 | [independent_credit_review.md](original/independent_credit_review.md) | 6653 | 新AB全历史证明、三族独立利润计算、可加模板矛盾17/252；明确交叠SPE复用已有定理 |

本次2026-11-02只在clone外的新临时目录复制原程序运行一次，真实argv/cwd/时间/解释器/exit与源及输出SHA保于[current-replay-20261102/execution.json](current-replay-20261102/execution.json)。Python3.12.14，`-I -B`、无`-O`，assert实际执行；exit0、stderr0B。原程序生成报告和[实际stdout](current-replay-20261102/stdout.json)均与冻结1252B报告逐字节相同，故不另存一份相同的生成报告。该事件属于当前复放，不补造原日期运行日志，不覆盖任何先前证据事件。

如需再次复放，应把原`audit_independent_credit.py`复制到新的可写临时目录，再在那里运行`python3 -I -B audit_independent_credit.py`；它会写脚本相邻JSON。保留这里的冻结原件及此次事件。

程序真正覆盖45760个AB计数状态（各A/B真实偏离及全部单例统一上界）、64个all-big槽计数、45760个交叠规范整数profile，以及产品计数/矛盾算术。2928640是主题选择被这些界覆盖的数，不是逐条执行全部单例或全历史比较。它不导入发现程序、LP、SPE求解器或canonical verifier；不枚举64人交叠策略树或巨大产品目录。完整SPE与产品可加性由正式证明承担，有限算术不替代全称证明。

历史两份审查各有明确先验：基础稿先陈述重建后读旧信用/利润稿、未读当轮新AB/root后续证明；交叠SPE仍复用已发表定理；产品稿先新精确陈述重建，基础数值复用基础审查。当前清洗已知情阅读，不新增盲审、外审或首次发现身份。
