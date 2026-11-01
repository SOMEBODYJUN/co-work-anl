# 完整156主题收益矩的独立客户认证

正式对象：[完整156主题固定前缀的收益矩数据](../../../state/计算/完整156主题固定前缀的收益矩数据--计算.md)。主源ID `4fb7add9aa294a3da316` 的3395493B原件共用 [full156-tail-parent-report原件](../full156-tail-parent-report/original/research_5/full156_tail2_kernel_10344.json)，没有持久复制或修改。输入和相关完整阅读见 [source-manifest.json](source-manifest.json)。

`verify_kernel_atoms.py` 是本轮新增标准库精确实现，不导入原生成器，不解LP，不枚举策略。它遍历point全部1905列及pair全部364项，解释并检查当前hist归属、194组隐含00、29个R阈值段与Z质量界；枚举六个有名索引全部不同模式排列，按共同阈值分成1590个类型。每类型的正整数重数表示等量不同单位客户。直接按客户均分定义核全部156个F、24336个G及24336个U，另核旧六A收益总和、覆盖和六T分割。

从仓库根运行：

```sh
python3 -I archives/customer-attraction/tools/evidence/full156-payoff-kernel-data/verify_kernel_atoms.py
```

脚本需要assert开启，拒绝 `-O`；会重写本目录两个派生JSON，不会修改三个共享原件。`--pair PATH` 可显式选择同SHA的pair文件，默认使用 `../full156-pair-master-point/original/pair_master_exact.json`。作者原入口的实际复跑由 [生成器证据](../full156-kernel-generator/rerun/comparison.json)承担，本包没有重复原run。

产物：

- [independent-report.json](independent-report.json)：全19字段、输入哈希、1590类型、逐hist排列/阈值数量、全部48828整数一致和具体限制。
- [unit-customer-types.json](unit-customer-types.json)：156标签及1590对 `[十六进制会员掩码, 十进制整数重数]`，按掩码整数升序。掩码第i位对应标签i。类型总重数为S。
- [independent-execution.json](independent-execution.json) 与 [independent-stdout.json](independent-stdout.json)：本轮独立实现的实际最终运行，不是原CLI记录。

类型规范摘要的编码为 Python `json.dumps([[hex(mask), str(count)] for mask,count in sorted(atoms.items())], separators=(',', ':')).encode()`；SHA-256为 `87d207363bf7e9401b47c7a8be10cb8e7b23227fcd0a8cfbd2198893c21abccd`。这与整个带标签及缩进JSON文件的字节哈希不同。

S是单位客户总数；原收益整数除以60是单位客户实例收益，除以60S是归一化收益。F是一维向量；G与U是156乘156矩。246是原轨道缓存键数，1590是客户类型数，24336是行动对数，均不是完整游戏枚举量。

本包新增的是客户空间共同实现及固定前缀收益认证。point的5108、pair的10344行未在本包重新核完；尾终局与前四层SPE激励亦不在本包运行范围。原低福利A1至A6路径没有因此成为SPE；一般sixhalf仍未解决。
