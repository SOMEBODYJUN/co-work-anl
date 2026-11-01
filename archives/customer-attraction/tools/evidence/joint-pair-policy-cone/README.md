# 固定路径计数策略与客户质量的两步联合搜索证据

主程序及两原数据的自足语义在[程序对象](../../../state/程序/固定路径计数策略与客户质量的两步安全联合搜索--程序.md)和[计算对象](../../../state/计算/两步安全联合搜索的全兴趣停点与去除超时记录--计算.md)。本包保原件、唯一新增标准库诊断及真实缺口，不运行原 MILP，也没有修复原质量。

## 主源和相关原件

| 身份 | clean ID | 原件 | 字节数 | SHA-256 |
|---|---|---|---:|---|
| 主程序 | aa6e631f947632ad3b97 | [pair_joint.py](original/pair_joint.py) | 4772 | e8c041a0d823007af60810d39fbba8745b98d743936b2c62d3ea7585cc607f22 |
| 主普通表 | 94848de4b8bc81673e78 | [joint_0012_345.json](original/joint_0012_345.json) | 35014 | 5a6c30321d1662ae9a3f3cb28f948bee968260d67f629b73574a396e3dbcf1e3 |
| 主去除表 | 0aeca94c92b65295e750 | [joint_0012_345_strip.json](original/joint_0012_345_strip.json) | 791 | 7065eb68ace0d0f21116d10e100f7cae35d97a03da8de5c8e8c4795fe76b112e |
| related，不登记本批完成 | 9a9073c94bd99b05119e | [joint_0123_all.json](related/joint_0123_all.json) | 34920 | e4678d8d37f3c5a65462c97742d50c7ef897e86b63c3c0005bae693a292bcce4 |
| related，不登记本批完成 | 243d456afe321b1c9d05 | [joint_0123_all_strip.json](related/joint_0123_all_strip.json) | 843 | 4a97efdb5e1e553c8181cbf707210affedb32c1cc0113042f08bff519a7a709e |

五件均由 clean show 正常导出并全文读取，保两个冻结提交 68fad804ec5946cb296f77dc5b336308a66abf12 与 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 的相同字节身份。路径均在 `research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_security/`。blob 身份及全部共享绑定在 [source-manifest.json](source-manifest.json)。raw 正负零和原文字不改。

主普通报告有 19 根字段，63 质量、84 计数动作、259 ordered 动作；strip 有 14 根字段，无保存候选。两 related 表同样所有字段/动作已读，但本包对它们新增收益、策略、静态背景、LP 或 MILP 核验为零。

## 实际导入闭包与比较

三件依赖均全文读，复用唯一现有原件，不复制成不同版本：

| 实际源码 | 作用 | 稳定原件 |
|---|---|---|
| pair_attack.py，5887 B | 动态载入 old；本 joint 仅调用 tail_tensor | [同目录依赖原件](../background-pair-attack-source/original/pair_attack.py) |
| common_q_generator.py，22102 B | Space 的计数/历史/整数收益及 full_policy；其他求解和精确恢复未调用 | [原件](../transport-tail-common-q-20261031/common_q_generator.py) |
| policy_patterns.py，6608 B | common_q 顶层导入的规则模块；本入口不调用其候选生成 | [原件](../transport-round-obstacle-20261031/policy_patterns.py) |

本程序新目录的原件是归档副本，其相对 parents[5] 布局不构成自动可运行环境；本次没有借修改导入路径重跑发现。源所需 NumPy/SciPy 版本及历史完整 argv 缺失，不填造环境指纹。

数学比较实际涉及[完整历史模型](../../../state/定义/共同目录完整历史模型--定义.md)、[PAIR 条件望远镜及全兴趣零系数](../../../state/候选/两步安全链的条件归并与有限探索边界--候选.md)、[旧固定完整策略锥](../../../state/程序/两步安全链的固定策略锥搜索与两份浮点纪录--程序.md)、[单步与固定锥边界](../../../state/审查/两步安全归纳与策略锥精确边界--审查.md)、[plain 首对合法背景探针](../../../state/程序/合法背景首两人安全比的有限探针与三个取等点--程序.md)及[PB-extra 大背景反例](../../../state/反例/任意合法背景的前两人额外槽安全值--反例.md)。它们分别支撑模型、上界方向、版本比较或命题区别，不把别人的成熟运行计入本事件，也不新建第三阶段图边。

## 唯一新事件和结果身份

[audit_reports.py](audit_reports.py) 只用标准库，从原 JSON 建立真实有序后继并按兴趣集合份额计算。一次事件见 [execution.json](execution.json)、[stdout.txt](stdout.txt)、[stderr.txt](stderr.txt)。0.2624448249989655 秒，退出码 0、stderr 0 B、三主源前后指纹相同；没有原 main、candidate、Space、full_policy、LP/MILP 或随机扫描。不是历史作者重放。

字面十进制与 JSON 解码 binary64 各是一份明确有理输入；对同一原 normal 点各核全部 1554 行（259 自身、1295 非自身），合计 3108 行，并各列全部 56 根背景和 6 尾查询的完整收益。不是两次原数值发现。两种输入均 3 负质量、662 负 IC、259 零 IC、633 正 IC；84↔259 动作和实际0012路径一致。原 p/Q 的精确和不是 1。当前源码 w_all 上界 0，但普通表 w_all≈1，存在不能用浮点误差抹平的源/表版本不一致。

[exact/exact-audit.json](exact/exact-audit.json) 保完整分数、所有字段名、维数合同1073/504/8715及 strip 全14字段；[exact/full-history-ledger.json.gz](exact/full-history-ledger.json.gz) 保两解释的每条真实叶子、两份收益、余量及全背景表。gzip 84476 B SHA 2e5bc7c980382ebe907218fc3249a2e6d1ab1ca9039337957f3bffe045d9c73a；解压 1795593 B SHA 9efff677765aec3e25b1611c485292e7e1c9f4be91e8d9e02b526f94ede12835。诊断重建的 tight formal surrogate 约 +3.756e−13，不是原缺 t/h 的 −4.286e−14 数值 fun，也不是合法游戏的精确安全界。

没有对质量作 rounding、清除负坐标或 limit_denominator；正文提到的纯全兴趣单位点仅复用普遍解析零系数，没有新运行，也不当作当前 strip 可行点。超时无 incumbent 不等于不可行；普通近零候选不是精确 SPE，两个有限停点都不证明一般 PAIR/half。

## 静态自查与复用

[self_check.py](self_check.py) 只核原件 SHA/blob、共享依赖、交付文件、JSON/AST 语法、完整账结构及实际链接，不重新运行数学。实际输出在 [self-check.json](self-check.json)。三份逐源回执只覆盖主源，正文与证据均列于 targets。

如未来确需再次运行独立核，应在新输出目录执行 `python audit_reports.py --normal original/joint_0012_345.json --strip original/joint_0012_345_strip.json --source original/pair_joint.py --out NEW_OUTPUT_DIRECTORY`，单独记录新事件；当前事件的原命令与脚本 SHA 已冻结在 execution.json。本说明不要求重复成熟核验，也不补造历史 MILP 命令。
