---
id: customer-attraction/effective-insurer-margin-seven-fixed-input-outcome-diagnostic
kind: program
type_tag: 程序
title: 有效保险幅度的七输入完整续局诊断
status: 原2014B程序与七条报告全读；绑定七原整数输入并精确重构全部根后终局集合
truth_status: finite-input-maxima-only-no-universal-overlap-insurer-bound
review_level: full-primary-and-canonical-recurrence-reading-plus-seven-definition-level-input-checks
scope: 七固定实例；全部真实suffix纯SPE终局；M为完整根可信floor，e=h−M≥0；非客户重数锥或随机扫描
summary: 七个max[3e−(2W_H−OPT)]分别−9、−2、−30、−11、−55/2、−6、−36；有效幅度不可换同根span，未给一般交叠保险D≥3e。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/overlap_insurer_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/overlap_insurer_probe.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/overlap_insurer_probe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/overlap_insurer_probe.json
---

# 有效保险幅度的七输入完整续局诊断

原2014B程序和3256B报告均完整保全于[证据包](../../tools/evidence/d398-parent-diagnostics-primary/README.md)。这里固定七份单位客户实例，保全部真正可信后继，而不是固定一张原策略再改客户质量；与[230个根遗憾锥](../计算/正深度根遗憾锥的二百三十份有理证书--计算.md)是不同有限域。

## 判别量与精确集合值求法

定义和普遍证明见[保险有效幅度引理](../引理/保险根菜单的有效幅度与调和后继保底--引理.md)。固定m人、共同有限目录。根a后的完整suffix-SPE终局集合R(a)保留原根负载；令

\[
 M=\max_a\min_{q\in R(a)}U_a(q).
\]

M恰是所有完整根SPE的最低首人收益。任一根a、真实后继q的首人h若h≥M，可在其他根贴最低可信后继而补为完整根SPE；有效修复幅度是e=h−M。仅同一根的高低差h−min_R(a)U_a会忽略其他根的可信floor，不可替换e。

令 \(D=2W(q)-\operatorname{OPT}_m\)。程序在所有a及q∈R(a)、h≥M上最大化

\[
 3e-D. \tag{1}
\]

正值才是优于三倍成本的有限候选；e=0而D<0本身已有half坏分支。源码过滤h<M，不声称检测没有有效修复幅度的任意非可信根计划。它不改变原单位客户/单位玩家模型，空覆盖、重复和所有离轨弱平局由规范集合值BI保留。

ExactSPESolver在计数s上保存**整个可实现终局集合**：各行动a的孩子先取最小U_a，再取这些最小值的最大门槛；逐终局筛选达到门槛者。不同有序历史可独立选续局，这不是计数统一策略。M是空根的精确threshold；OPT逐支持精确枚举。

## 七个原输入和全部字段

| 输入 | m / p / 客户总数 | M | 原赢家h / e | W_H / OPT | 最大(1) |
|---|---:|---:|---:|---:|---:|
| root_tax_failure | 4 / 6 / 61 | 9 | 11 / 2 | 38 / 61 | −9 |
| eight_cce_welfare_gap | 3 / 4 / 8 | 2 | 4 / 2 | 8 / 8 | −2 |
| aggregate_theta_failure | 3 / 6 / 36 | 10 | 12 / 2 | 36 / 36 | −30 |
| fractional_actual_load_failure | 4 / 4 / 17 | 7/2 | 7/2 / 0 | 14 / 17 | −11 |
| individual_security_failure | 3 / 6 / 34 | 29/3 | 67/6 / 3/2 | 33 / 34 | −55/2 |
| prefix_balance_failure | 4 / 6 / 22 | 15/4 | 15/4 / 0 | 14 / 22 | −6 |
| portfolio_matching_failure | 2 / 5 / 86 | 22 | 23 / 1 | 42 / 45 | −36 |

报告的criterion及七条各11字段全部读取，原root/terminal向量保持。客户总数和OPT不可混同，最后一例86客户、两主题最优仅45。每条仅存一个达到最大值的根/终局，不宣称最大者唯一。原winner选择取决于frozenset遍历，独立实现可选另一并列winner，正确核验是提交winner可实现且达到同一最大值。

原程序无main guard，导入即运行七次规范solver并覆写相邻JSON。需要七examples和规范包；本轮全部七原输入全文读取、各字段合法性/版本指纹绑定于manifest，复用已存原件。原报告没有输入SHA、argv、环境或完整R(a)，不能凭名字匹配另一同名实例，更不能把当前绑定当原进程日志。

若score>0，源码才附一份完整high_certificate；其h≥M保证根a可以保该终局，故能找到该首动作的可信有序实现。实际七条均未走该分支，报告没有完整策略表。不能把缺表的终局计数当作已提交完整σ。

## 本轮有限补验及停止界

为了核原报告未保存的完整R(a)/M/最大性，并防同名版本错配，本轮一次[标准库检查](../../tools/evidence/d398-parent-diagnostics-primary/check_saved.py)从上述七份实际整数客户重构定义级集合值BI，不导入规范solver或作者函数。它精确算每个根后全部终局、M和OPT，确认原winner存在、h/e/D及score逐字段一致且确达全部符合h≥M的根/终局最大值。完整根后集合已存[verification.json](../../tools/evidence/d398-parent-diagnostics-primary/verification.json)。

七输入总714个计数状态；符合h≥M的根/终局对分别33、9、24、14、24、3、6。只是七个原输入，未增加参数、抽新客户或LP。该新小检查补的是原报告仅存赢家、没有完整后继集合的证据缺口；原入口及规范solver调用0，不重复成熟有效幅度解析定理。

全部非正排除这七实例中更优保险候选，不排其所有客户重赋权、更大目录、交叠结构或根后耦合。特别[不交保险三倍锐界](../定理/不交花瓣同根保险的三倍损耗锐界--定理.md)对独立坐标架构的普遍证明不能由本七条代替，也不能反过来把该停界推广为所有交叠保险。一般D≥3(h−M)及原根修复等价问题仍各按其精确量词接续。
