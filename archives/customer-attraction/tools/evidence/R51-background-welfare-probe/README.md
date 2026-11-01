# R51背景福利非单调探针的原件与复现

主源`79799b9b0d7d75fdfef4`（2083B）全文由`work.py clean show`读出，SHA-256为
`6afa7d95db9ed1954cbcc1bba110f1c475104d877d7e77922cc7cd7a15185c06`。
冻结结果`786e0b678d81d2d39f1e`（1040B），SHA-256为
`cec159161952bcaab3fb306cc5b72622356fb3d59e5e70fcdf72c20f2707f68f`。
两文件各在冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`中相同。[manifest](reading-manifest.json)列实际完整路径、双来源、SHA、原样导出映射及实读范围。

`original/`保主[原程序](original/probe_monotone_welfare.py)、[原结果](original/background_welfare_nonmonotone.json)和实际导入闭包四个规范模块：`customer_attraction/__init__.py`、`model.py`、`exact.py`、`certificate.py`。全部由`work.py clean show --out`导出并核原SHA，未修改源码。依赖仅标准库；已先逐行核读，没有网络、消息、子进程、外部写入或动态执行；默认循环有界，简化器每次接受都减少一个客户。执行前关闭字节码写入，未安装额外包。

## 两个实际运行入口

在`original/`为工作目录、其路径加入`PYTHONPATH`后，分别执行原文件及显式导入调用：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 probe_monotone_welfare.py
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import json; import probe_monotone_welfare as p; print(json.dumps(p.minimize(), indent=2))'
```

本次真实stdout、stderr和exit/time/Python记录分别保存在：

- [默认main stdout](replay/default-main.stdout.json)：seed102、trial0，22客户22到20，非冻结13到12输入。
- [minimize stdout](replay/minimize.stdout.json)：13客户13到12，与原1040B JSON逐字段及逐字节相同。
- 两份`*.stderr.txt`均为空；[execution-state](replay/execution-state.json)保两次exit0及真实字节比较。

当前可精确生成不等于知道原研究当时的历史调用命令。原JSON字段与`minimize()`返回结构相符，但未提供原调用日志；本目录不倒造该日志。

## 独立的完整局部策略核验

运行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/R51-background-welfare-probe/audit_two_player_background.py
```

[审计程序](audit_two_player_background.py)展开全部13名单位客户，独立计算每个终局客户分母与去重覆盖，枚举四个首行动下所有末位最佳回复映射，再求首人所有最佳行动。其Fraction计算不导入原探针或规范包；全部结果得到后，才另调冻结规范求解器比较全集。两背景的完整子SPE终局分别恰为：

- `(1,0,0,0)`，剩两人：`{(1,1,1,0)}`，最小覆盖13。
- `(2,0,0,0)`，剩两人：`{(2,1,0,1),(2,1,1,0)}`，覆盖集合`{12,13}`。

[独立结果](replay/independent-unit-tail-audit.json)保存全部末位收益矩阵、BR集合、完整策略数量1及2、两个最差局部策略、首人收益向量及各5节点20项比较。验证的是给定合法过去后的完整两层子博弈，不含过去玩家最优性，不把它写作完整根SPE证书。根总人数为3到4而未来人数始终2；`welfare`含全部背景已覆盖客户，不是尾部利润或新增覆盖。主题1与2覆盖全部13客户，两个相关根最优值均13，探针不反驳half。

## 实际相关阅读及后续状态

下列冻结相关材料完整由`clean show`读取；比较源没有由本子任务claim/done，也没有冒称全部运行：

- `b3eb616280309993a83f`：R51工作区README，区分局部约束非SPE障碍、仍在探索的各分支与根目标。
- `e561d368bd778d8bc822`：同`independent/`的Hamming尾部盲重构原稿，其独立身份针对另一明确Claim，不移授本规范求解器探针；本任务不复跑其40万行审计。
- `db0a56f6801a92b9cff9`与`e721cbff6868a74c7d64`：相邻剩余利润探针/另一18客户9到11结果。对象、方向、add主题和客户输入与本13客户福利下降不同；未在本任务运行。
- 四规范模块的源ID：`e34d11916a2c223f010d`、`999293c4e866618a72f6`、`14e0922138e43b337600`、`52369ae591b07d52c7df`。

当前正式正文全文比较：共同目录模型、完整纯SPE终局全集算法、规范实现复现、R44人口悖论审查、真实路径安全值链。福利非减、minimax利润列嵌入、空根增人数、固定剩余加过去和half分别说明；未将现有静态安全值嵌入当作福利单调。

当前工作树全仓按原文件名、原JSON名、背景福利单调/非单调等检索；冻结inventory按完整R51路径及规范包定位。没有以命中摘要代原件阅读，也没有宣称读取整个R51目录的所有其它搜索程序。

正式[审查正文](../../../state/审查/R51背景福利非单调探针--审查.md)保程序合同、原始两次输出、完整13客户表、全部末位收益和局部策略、全集量词、候选否定及half边界。原程序的随机探测属有限发现；对两个固定背景的全部策略穷举则给这个有限反例的精确证明，不推广为任意目录的新福利界。未证明最少客户、新颖性或外审身份。

本任务没有commit、push、checkpoint、clean done或新claim；待父Boss真实保存后按回执登记。关系判断已写正文，三级超图留第三阶段。
