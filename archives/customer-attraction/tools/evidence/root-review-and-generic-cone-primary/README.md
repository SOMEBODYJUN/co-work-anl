# 根独立审计与通用完整锥交替探测证据

本5actualclaim明确pushed/synced4062d709a9b0b600597ed94cf4dbd33dfc647b41。正式正文是[根独立单位客户复核](../../../state/计算/根平稳弱核的独立单位客户复核--计算.md)和[通用锥交替数值探测](../../../state/计算/完整策略静态安全锥的交替数值探测--计算.md)。本stage只external写入，没有Git分支写、claim/done、checkpoint、认证重试或新代理。

[primary-manifest](primary-manifest.json)和[source-manifest](source-manifest.json)逐份记5主源25179B、1真实输入372216B及5比较源21873B的大小/SHA/双冻结定位。所有原件保repo相对路径，原报告不覆盖。

| 主源ID | 大小 | 去向 |
|---|---:|---|
| 8fb492268f7ad2fd3e37 | 5782B | 根独立原码：严格结构检查、逐单位客户/真实IC、唯一平稳系统及静态修复，首次本批原main复现 |
| cc31f0e547a5bce7512e | 1558B | 原独立报告全部字段与源hash，新旧输出全字节核对 |
| deb74d312cf9a35b4985 | 1925B | 内部先验/原模型/准确反驳域已由现有同source_ref反例和资源充分吸收；本批duplicate并保原件，不重复造反例 |
| 847a210188334e25b4bd | 4990B | 通用锥原码：全部节点Γ、三种背景域、两个块LP、16起点/停止/输出全控制流 |
| d0790545c28af71b92b1 | 10924B | 32行完整数值轨迹、best、scope及微小cone_margin残差，按实际默认原main复现 |

唯一真实运行输入为旧十三人gzip，SHA bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce。两程序直接读取它；不导入对方代码或规范模型。根审计只用标准库，generic用numpy/scipy。比较原件为发现者主稿/a5代码/a5报告/security README以及后续OQ代码；仅比较，不额外done或重跑这些程序。

## 两个原入口各一次

新replay-tree按原层级放原码和输入，两个输出起初均不存在。prepare_and_run有执行记录保护；check_package只核记录和已有字节，不执行数学原码或LP。

- [根独立执行](replay-review/execution.json)：0.48367810249328613秒，exit0/stderr空，新1558B报告与冻结全字节相同，SHA 8ad65b11e4e51dbcdfdd85327b02774caaf6f219a631a8bab65060dc1d48d310。[stdout](replay-review/stdout.txt)也同一SHA，[结果](replay-review/root_stationary_audit.json)分存。原x模式在新空输出路径成功，未改程序去覆盖旧文件。
- [默认锥执行](replay-cone/execution.json)：25.006980895996094秒，exit0/stderr空，Python3.12.14/numpy2.3.5/scipy1.17.0。新10924B与冻结全字节同SHA 961b23f89517f9220ba5af5edbfb7fa27ae8a045366f35aa43834295aafaa1af。[stdout](replay-cone/stdout.txt)、[新报告](replay-cone/cone_security_probe_all_13.json)和原文件分别保留。

generic本批明确用无可选参数的默认all/强factor13。输出新名为cone_security_probe_all_13.json，冻结源名为cone_security_probe.json，内容完全相同。冻结JSON未记旧命令/mode/factor，不补造其历史命令。新默认运行32迭代行/16起点，按完成控制流65次LP；没有运行root/onpath/weak或扩大起点。两原码与各自输入前后不变。

## 精确与数值结论分别承担

根代码从27243节点完整观察图重建原36客户完整SPE；报告只计93375项非自比较，代码也检查自比较。秩6/π/cap427/156/弱阈值66/25/379/3900差与自由静态背景5/2均精确。原root审查明示先合同+packet、未读发现代码的历史独立身份，本批是读后复现，不自称盲审。此前仅比较未运行的记录不回填。

generic固定原形式策略、变63客户类型、生成31454 Γ行、all含6188背景；目标是factor·静态安全值−W。它不是OQ的ΣC−W目标，也不是指定根stationary分布。16起点各两轮都返回打印的全兴趣质量1、W1、v约1/13、true_gap0；正负1e−15级cone_margin原样保留，不当作反例。解析全兴趣点确为精确零边界，但没有精确全锥上证书或全局双线性最优证明。

完整读并比较当前原模型、静态锐界、完整策略锥对偶、跨分支预算、已发表根反例/a5资源与固定原鞍点OQ对象。不同菜单/真正v、固定输入/整个锥、内部独立先验/新执行、浮点点/精确优化分别保持。六人half与普遍安全付款未因这些有限结果升级；无外审或新颖性主张。

[verification](verification.json)、current-comparison-manifest及工作室5receipt/数学自查/关系/HANDOFF/下一候选一并交付。正文/证据保存与done由Boss串行完成。
