# 因子二历史抽样与交付记录

对应正式对象为[因子二冻结审计记录与版本归属](../../../state/计算/因子二冻结审计记录与版本归属--计算.md)。本目录和相邻逆向目录保留四份原始冻结资源，全部字节哈希与清点一致；[provenance.json](provenance.json)给源 ID、原路径、完整 SHA-256 和现位置。

| 文件 | 内容与本轮实际状态 |
| --- | --- |
| [kfac_independent.py](kfac_independent.py) | 仅用标准库的独立随机小输入/纯 NE 极值检查器；已全文读代码，本轮未执行 |
| [kfac_independent.json](kfac_independent.json) | 原历史输出汇总；1319 是抽查在轨见证数，不是不同实例数 |
| [kfac_delivery_validation_v2.json](kfac_delivery_validation_v2.json) | 原交付回执、当时八个程序哈希及未运行范围；本轮未执行其交付套件 |
| [frozen_reverse.json](../factor-two-reverse-review/frozen_reverse.json) | 原 kfac_two_reverse.json 完整冻结字节；已有本轮真实逆向复跑与其逐内容相等 |

[delivery_version_comparison.json](delivery_version_comparison.json)把 v2 的全部八个历史程序哈希与当前冻结清点逐一对比：三项相同、五项不同。这是版本归属检查，不是当前程序测试通过证明。

相邻目录的[完整数据结构核对](../factor-two-reverse-review/frozen_data_inventory.json)读取了逆向原 JSON 的全部612个小输入记录和7个对称族，复核可由记录重建的计数，并确认与已生成复跑数据除 Python 版本外全内容相等；本批未重复执行求解枚举。

独立抽样器可单独复现，输出应使用新文件：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-historical-audits/kfac_independent.py > /tmp/kfac_independent_new.json
~~~

程序无第三方依赖，在模块顶层运行并打印 JSON，须保持断言开启。它枚举全部最优在轨见证后，每输入只检查至多前三个；基础输入四组各175次且跳过全空菜单，不能把输出 cases 当成不同输入数。原摘要不保存逐输入或逐偏离证书。

v2 回执本身不是可执行脚本，也没有包含其所指全部历史程序字节；重放原整套结论前，应先恢复所列哈希对应版本及依赖。回执观察的公开上游 main.patch 不能当成当时成功 Git fetch、写端点认证或推送。更晚真实合入检查在正式审查对象中另述，不覆盖这里保留的历史限制。
