# 双见证查询分离作者证明与审查历史

[自足审查对象](../../../state/审查/双见证查询分离的染色证明与冻结审查边界--审查.md)合入两份来源。`original/`保留两源完整原字节；`source-manifest.json`给冻结定位、大小与SHA。`comparisons/`保留实读的七份相邻冻结历史和当前全文，详见`comparison-manifest.json`；它们仅供比较，本批不新增其done。

新整理明确旧端为a、新端为b，染色流入使用b；对照的general五机例blocker两端均1/2，typed五机和作者六机例则旧1、新1/2。三者合同相同，矩阵不同。最终组合审查的canonical指纹只对应当时v2，并明确软件pending；源审查另记后来的root运行，不能把两个时间点合并。

本目录没有数学程序运行输出。本批只实际运行`verify_delivery.py`核字节、SHA、JSON和新增页的本地链接，不重跑旧查询审计、不产生新的32状态证书、不声称Exact-first独立身份。原程序/既有实际证据见[查询原程序证据](../query-witness-originals/README.md)。

自查入口由结果仓根执行：

```sh
python3 archives/unrelated-machines/tools/evidence/two-witness-proof-review-history/verify_delivery.py --repo-root . --report /absolute/path/to/new-report.json
```

输出路径必须尚不存在；校验结果不证明一般数学命题。正式入库前另检查正文的完整条件和推导；逐源语义receipt保存在`cleanup/workspaces/Boss4/two-witness-proof-review-history-next/`。
