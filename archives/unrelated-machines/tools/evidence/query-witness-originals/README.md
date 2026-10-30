# 双见证查询染色与两个固定矩阵的原程序证据

数学合同、证明、三case及两固定矩阵的完整解释见[计算对象](../../../state/计算/双见证查询染色与固定矩阵证书的原程序核验--计算.md)。三个本批来源原字节如下；两冻结分支同字节只计一次。

| 源ID | 原路径 | 字节 | SHA256 |
| --- | --- | --- | --- |
| 414eccc0da49f496cb03 | tests/audits/unrelated_machines/two_witness_query_separation.py | 20317 | cc50d2e612de59b225d8bdf009d38cfa7e22c8ae67b10900086e6b7786238759 |
| 45f1ffd14fb1ebfb8770 | examples/unrelated_machines/two_witness_query_separation_cases.json | 5105 | cee13089d6cc2e8d78aaae6fe80b60da442ff3fabced16bb7ff70f44406e147c |
| 4294a3a29634d52e6dde | tests/audits/unrelated_machines/audit_query_return_source_fixed_certificates.py | 7050 | 5a338e62d31512260d6ab41c479cda482f6fd0d4cb3b28e31e8a956ccd339a74 |

`original/` 保原代码和三case输入；`comparisons/` 保全文实读的当前数学正文、查询审查及三个固定证书作为精确依赖，不新增这些来源的done。原矩阵的全部资格、原任务分配和全机负载都可直接读取。旧来源字节不随整理纠偏而改写。

`replay.py` 是本批原入口首次复现包装器：复制输入到全新目录，两个入口各用子进程运行一次，不import原程序；随后自己重算查询保存输出的全部实际负载、目标时间流入/触发和32状态阈值。`runs/original-replay-001/` 从已存在的首次成功运行目录原样恢复，内有两个实际命令、stdout/stderr、原程序副本、四输入副本、两个原输出、input manifest和 `verification.json`。Python3.12.14，两个命令exit0、stderr空。保留命令中的原绝对路径作为历史证据，不冒称归档后运行目录路径。

查询程序核三个显式输入，6份给定见证、6单查询和32混合，共44保存记录、224任务归属、264机器负载和7次触发；只有6机5任务例的32状态覆盖该例所有合法端。固定审计核26机30任务57资格的take/continue达界证书，未优化；另在8机10任务24资格的单个UNSAT矩阵上枚举全部5184合法分配，OPT3/2。两个矩阵互异，不是同一P的两个strict actual。

针对现有摘要把流入权误写为旧端时间，本轮另写并实际运行 `inspect_saved_witnesses.py`，不import原程序或replay，也不重新运行原入口、生成32状态或枚举5184。它核原字节一致性，从输入重算查询44份完整调度和目标时间流入，重建全部take矩阵并核证书，再核sharp的三个保存分配。一次exit0、stderr空，48保存分配记录、284任务归属、314机器负载；10个a/b不同的流入格见[runs/saved-witness-inspection.json](runs/saved-witness-inspection.json)。其精确命令、标准输出、标准错误保存在同一 `runs/` 下的同名前缀文件中。这是读后独立算术检查，不是新盲审或第二次原程序复现。

两个原入口均禁止覆盖已有输出；固定矩阵程序及独立检查依靠 Python `assert`，复现须使用未加 `-O` 的通常运行方式。需要独立复现时，从仓库根选择一个尚不存在的目录：

```sh
python3 archives/unrelated-machines/tools/evidence/query-witness-originals/replay.py --run-dir /absolute/path/to/new-run
```

保存见证检查也要求尚不存在的新输出路径：

```sh
python3 archives/unrelated-machines/tools/evidence/query-witness-originals/inspect_saved_witnesses.py /absolute/path/to/new-report.json
```

首次运行和新保存检查均未记录失败。检查成功不提供未知YES搜索、v3计数/全部pattern生产实现、通用优化器、源解码或全输入UM算法；原一般证明及固定矩阵下界应从计算对象读取，不能以assertions替代。
