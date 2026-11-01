# R51独立汉明尾部报告的原件与字段核验

主源`bb9fcb09621318faf643`由`work.py clean show`完整读取并`--out`导出[原JSON](original/hamming_tail_audit.json)：9758B，SHA-256 `b7fc7c50c846c63983dfc8747bf0e3acc33fb0a9bd16f0d18eebc11fafcf7199`，blob `3c7686da3c671b11e8bf93d4fb4692bf2c8ffabc`。路径为`research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/independent/hamming_tail_audit.json`，两个冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`及`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`同字节。

必要旁读生成器`0a373b467b7bf2d0be8b`亦完整`clean show`读取并导出[原代码](related/audit_hamming_tail.py)：3072B，SHA-256 `d7f3b3fc99f4d58cad64d267459423b5ed366d70a050429a9fdeaa068a67cd02`。只有Python标准库，无外部输入或项目依赖；本回执不代它done。

全文相关阅读包含4951B `independent/hamming_tail_blind_review.md`及正式对象：标签汉明邻域与完整末尾的删行障碍、标签汉明保护与真尾计数的有限审计、汉明删行障碍的双独立审查与范围增量、共同目录完整历史模型、区间终局剪枝的上界比较与全效率目录类，以及同批R51汉明尾部审计器审查。旧MD原20组、父560组和发现8组各保真实范围，不把它们混成同一次运行。

新增[字段核验](verify_report_fields.py)不导入或执行原生成器，用组合计数、多项式排除future A、根调和福利和显式远轨有理公式重建全部键值，再与原JSON全相等比较。实际命令：

```sh
python3 archives/customer-attraction/tools/evidence/R51-hamming-tail-report/verify_report_fields.py > archives/customer-attraction/tools/evidence/R51-hamming-tail-report/field-check-result.json
```

本次退出码0，[输出](field-check-result.json)为PASS，核20组/12205near/406555tail/640future-A历史、十组负行及十组d1全历史覆盖。字段核验不重新枚举全部IC，生成器的完整局部assert与解析证明另承担这部分。未把它称原程序复跑、盲审或外审。

同批程序子任务已经正常重放原生成器一次，本报告任务不重复原入口。其[run/event.json](../R51-hamming-tail-auditor/run/event.json)、[stdout](../R51-hamming-tail-auditor/run/stdout.json)、[stderr](../R51-hamming-tail-auditor/run/stderr.txt)已读取核对：Python3.12.14、优化0、exit0、stderr空、stdout与本9758B原报告逐字节相同。该原入口事件和本页组合公式核验是不同事件，不相加为两次独立IC枚举，也不回填原历史运行元数据。

正式对象为[R51汉明尾部有限审计报告](../../../state/计算/R51汉明尾部有限审计报告--计算.md)。其新增准确范围：d1的r=n−1使全部early历史都被保留，加全ordered-tail便覆盖完整树；十组每节点所有动作均检查，构成这些具体策略的完整SPE有限证书，W=OPT=m。另十组明确非SPE；全部20组实际根均满足half。没有一般六人结论。

本子任务无提交、push、done或claim；由父Boss协调发布。
