# Boss2：平均偏离与末位标量七源

七份主源28557B全部由 clean show 导出并核大小/SHA；双冻结提交、blob、稳定ID及原保存路径见 [source-manifest.json](source-manifest.json)。原字节在 original，未覆盖原输出。所有四个py及三个JSON均完整阅读，19511B报告的156项动作和31坐标亦全读。

正文：

- [不重复前缀平均的四人原点与精确恢复](../../../state/障碍/不重复比较前缀平均的四人原点与精确恢复--障碍.md)：第9策略的有理33/16有限分离点，J实际最优，但非完整SPE且不满足全部历史平均。
- [平均续局集合的递推与28客户原点](../../../state/程序/固定比较组平均续局集合的递推与二十八客户原点--程序.md)：(2)集合递推、原OPT字段误名、新完整平均策略及真正SPE结果区分。
- [四人末位标量桥接](../../../state/反例/四人完整策略的末位标量桥接反例--反例.md)末尾附记：新恢复 last_payoff_probe.py 的准确诊断和生成合同，原随机入口0运行。

## 新核验与成熟复用

[check_average_sources.py](check_average_sources.py) 只用标准库，针对两个固定保存输入成功运行一次。它不调用原浮点程序、LP、原随机入口、规范SPE求解器或70棵策略的成熟证明重放。

原平均点的四个浮点质量明确换成新选择的19/96、1、19/48、15/32，逐坐标保存十进制差额，再按完整策略精确核验。这里的“恢复”不是假称浮点数本身与有理数完全相等。结果包含780真IC、41筛选平均、156全历史平均及全部负者。

原28客户输入是整数，不需质量恢复。新精确递推保每状态全部平均结果，另算真正SPE结果；保存新构造的156节点平均策略和其780逐行动比较。该策略是本次生成的有限见证，原609B只有终局人数、没有保存完整动作。

完整结果为 [new-average-exact-check.json](new-average-exact-check.json)，执行数量与代码/输出哈希为 [execution-record.json](execution-record.json)。复用的StrategyCone、原70输入第9策略和原有序路径求解器的实际读取范围见 [reused-source-contracts.json](reused-source-contracts.json)；未重跑成熟350原始/348对偶。

可在仓库根复现到一个新临时输出：

    python archives/customer-attraction/tools/evidence/average-and-last-payoff-resumed-boss2/check_average_sources.py \
      --original-dir archives/customer-attraction/tools/evidence/average-and-last-payoff-resumed-boss2/original \
      --out workspaces/average-fixed-recheck/result.json

## 仍保留的原始边界

原best4没有保存相应达到点，随机best约5/3且null没有保存完整完成次数，不能据此补造精确上界或阴性穷尽。原mean字段OPT19仅为固定J覆盖，真实OPT28；松弛W12不属于真正SPE终局。原last-payoff脚本没有同名输出与生产日志，不将其他桥接反例文件冒作该脚本的产物。没有任何六人half结论或新颖性认证。
