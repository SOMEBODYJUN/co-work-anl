# 三人笛卡尔数值筛选与六标签全覆盖基点

完整清洗两个主源：4114 B cartesian_limit.py（0668a7eadde334207c8a），2497 B cartesian_limit_k6.json（b25ffb3be50288f87850）。两个冻结提交均同字节。对应[程序正文](../../../state/程序/三人笛卡尔根门槛凸化的数值筛选程序--程序.md)与[计算正文](../../../state/计算/六标签全覆盖基点的笛卡尔极限筛选记录--计算.md)。

## 资产与真实执行

- original/ 保存两个未改主原件；源路径、提交、blob、字节与 SHA 见 source-manifest.json。
- observe_original.py 是实际执行的旁观包装器原字节。它仅导入原代码、调用一次 analyze(6,w)，用 sys.setprofile 保存原 linprog 参数/结果与局部变量；原 main 0、helper 替换 0。replay/ 的 execution.json 是函数区间及来源记录，process-capture.json 是外层进程记录；两种计时不能混用。
- replay/linprog-calls.json 保存全部 9 次原 LP。前六根 LP 成功，严格 guard LP status=2，不可行，弱回退成功，静态 LP 成功。original-analyze-locals.json 保存原全部 216 终局中间列、36 菜单行及 21×6 静态矩阵；不是另一实现的矩阵。
- replay/new-analysis.json 有 18 字段；旧 best 仅 16 字段。共享字段逐 JSON 值相同，新字段为 pure_root_floor_by_action、pure_root_floor。未篡改旧 JSON 或冒称逐字重放。
- audit_k6_exact.py 是一次实际执行的独立标准库脚本原字节。exact/exact-k6-audit.json 保存 23 名单位客户、216 终局收益、36 末位节点、6 第二人节点、21 静态背景与 258 项完整策略比较；43 节点常 0 策略非自身 215 项均严格，最小余量 5/3。原源码导入、原 analyze、LP、规范 SPE solver 均 0。
- exact/execution.json 是这次独立核验外层进程记录。精确证明使任意正根裕量不可行、弱可行支持唯一为 (0,0,0)，v3=23/3，W=OPT=23。648 项原已占用收益比对为精确；843 项浮点数值对照包括九套参数及静态矩阵/解/历史字段，不能称 843 个独立约束或全部矩阵系数。
- source-to-object.json 逐语义单元说明去向，comparison.json 保关系和证据边界；artifact-manifest.json 绑定本包及两正文。self_check.py 仅做静态 SHA/JSON/AST/链接/回执/已存证据结构检查，不计算收益、IC、LP 或 SPE。

实际执行脚本保留当时 scratch 的绝对路径，事件中 argv 与输入路径也原样保留。这使其确为所执行版本。若将来在另一路径复现，应另存调整路径的副本并记录新事件，不覆盖本次脚本或记录。包内只存一份主原件；运行目录当时的同字节副本不重复入库。

## 数学及历史界限

三人始终是三人，k 是基标签数，K 才是客户不交副本数。原程序为产品根菜单的数值松弛；需要有理概率、末位 BR、第二人总盈余、严格根裕量和统一取整误差，才有通用有限完整 SPE 编译。强聚合 W≥3v3 与半最优覆盖不同。

冻结报告记 completed=requested=300、seed=7301201；本次没有运行其随机 main 或默认 500 次主循环，没有重算已成熟四标签四个小 LP、双副本 273 节点独立核，也没有运行相邻 108 行客户锥。历史 300 个实例未认证。六标签单点是全覆盖等号，不是负种子；其完整常 0 策略和全 K 特殊等式来自新增精确证明，不是原数值 status 的含义。

所有 LP 状态、时间、输入输出字节、版本差与不可行分支原样保留。静态封包不会增加任何原函数或数学运行。
