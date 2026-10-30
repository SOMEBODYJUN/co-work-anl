---
id: "customer-attraction/pb-background-scalar-audit-and-prefix-arithmetic"
kind: "computation"
type_tag: "计算"
title: "PB背景反例的标量证据与实际前缀算术"
status: "fixed-exact-scalar-audit-replayed"
summary: "保全原Fraction标量程序和冻结JSON，原字节副本一次重放输出逐字节相同；另精确核最后D-singleton的R负载上界与正交叉乘积。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/direct_PB_prefix_obstruction.md"
---

# PB背景反例的标量证据与实际前缀算术

本对象提供[PB子SPE反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)的固定精确数值资源，并记录[原背景实际前缀障碍](../障碍/PB大背景的最后单例偏离--障碍.md)的整数重算。没有求解器、参数搜索、完整实例展开或SPE树枚举；普遍历史结论分别由两个数学对象的证明承担。

## 原件和本轮输出

原程序（源7b0d54b5a98f01ca6cc8，1926字节）及原报告（源d503fa5e58d8c295c70b，1564字节）位于证据目录`original/`下的完整冻结原路径：

- [pair_background_scalar_audit.py](../../tools/evidence/pb-background/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.py)
- [pair_background_scalar_audit.json](../../tools/evidence/pb-background/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.json)

本轮从源码原字节复制到一个新的工作目录，以普通Python 3.12.14运行一次，保留断言。原代码在顶层执行并把JSON写到自身同名后缀路径，不拒绝覆盖；因此没有直接在冻结原件旁运行。副本源码与冻结源码完全相同，仅执行位置不同，详见[比较记录](../../tools/evidence/pb-background/replay/scalar_comparison.json)及[复现步骤](../../tools/evidence/pb-background/README.md)。

生成的[完整JSON](../../tools/evidence/pb-background/replay/pair_background_scalar_audit.json)与冻结JSON逐字节一致，SHA256均为`d332f7fe7584e3ea435637cc286f5562056ea087a7d76edafecd7deacad66f65`；完整[stdout](../../tools/evidence/pb-background/replay/scalar_stdout.txt)也单独保存。没有仅比摘要字段，也没有改写旧报告中的待审状态文字。

## 代码实际计算的五项有理差

程序只依赖Fraction、Path和json，参数固定为k=3、d=20、q=12、t=10、r=2475、Q=2063、H=100000、M=10^9。没有外部输入、随机数、第三方包或仓库模块导入。

以数学正文的f、g定义计算u=dkf(k)和s=d[f(1+rk/Q)+(k−1)g(r+1)]，断言以下五项严格正：

| 报告字段 | 实际公式及作用 |
|---|---|
| G_greedy_padding | g(r)−2f(1)+f(2)，用于所有Greedy多块偏离 |
| F_fill_per_segment | kf(k)−f(t)−(k−1)g(1)，是每段Fill/Copy差；全玩家差需乘d |
| P_punisher | f(t)+(d−1)f(1)+d(k−1)g(r)−d[f(2)+(k−1)g(1)]，是整位处罚者的上下界差 |
| singleton_strict_inferiority | dq/(M+r+1)−1/(M+1)，对所有未来都成立的regular/singleton比较 |
| S_security_lower_minus_actual_one_player | s−u，查询下界与一位实际玩家收益的差 |

G/P/F在程序中全为精确有理数，不以小数容差作判断。由G及f、g单调性推得g(1)>f(1)>f(2)属于解析推导，不是这里另报一次独立实验。

完整报告中

\[
 u=\frac{180000000705}{250000001750000003},\qquad
 s=\frac{1741078242325546490301775210615}
 {2418164229266383467676453180700905788},
\]

并保存

\[
 2u-2s=-\frac{655518746053822970420433555247437051305}
 {302270530774191637694888525704084958127972335551358682}<0.
\]

所有五项正差的完整分子分母也均在原JSON中，没有由近似小数反推。

## 四个整数不等式及报告计数

代码计算并输出max_punish=180、min_free=1877、max_greedy_after_punish=2474、min_future_after_punisher_deviation=2292，并实际断言

\[
 2474<2\cdot1877,\quad2292>2063+3,\quad
 2472>2060,\quad2472<2\cdot2060.
\]

它还按块数公式输出48,495,120名客户，但没有建立这48,495,120个客户对象、列举全部主题或生成其有序策略树。输入规模、完整策略定义、贪心水位和模式切换均需从数学正文理解，不能由这些标量断言代替。

## 原JSON的全部身份字段

原报告保存被攻击候选的完整r槽量词、固定参数、客户总数、u、s、两人负差、五项正差、四个计数，以及范围说明“只攻击任意背景PB；前缀已覆盖全部客户；不是根half反例”。

status字段的“analytical full-history proof awaiting independent review”保留了程序写出时点。后续四份审查已在[版本与审查对象](../审查/PB背景反例的全历史审查与版本--审查.md)按真实读序整合；本轮不修改旧状态，也不把一个冻结字符串视为新的数学反驳。程序只检查单个明确参数组，未寻找别的可行参数或证明该组最小。

## 本轮新增的实际前缀整数重算

针对源5b753273b2fb8219b7bc，本轮用同一参数直接计算

\[
 L_0=dQ(qM+1)=495120000041260,\qquad
 L=L_0+r\,dkq=495120001823260,
\]

\[
 \frac{L_0}{dq}=\frac{24756000002063}{12}<HM,
 \qquad dq\,HM-(M+L+2)=23504878998176738>0.
\]

[完整算术记录](../../tools/evidence/pb-background/replay/prefix_obstruction_arithmetic.json)保存全部参数、R总负载、regular前缀次数上界、最后D-singleton利润上界及其regular偏离下界。它是本轮新计算记录，不冒称旧冻结报告；复现说明给出同一Fraction公式。根路径排除仍依赖“最后D-singleton之后每个实际行动触及R、偏离不改变后继人数”的解析步骤，不由一个正整数输出独立承担。

这些资源可以复核当前固定参数的代数接口。若改动目录、模式、背景或参数，必须重新证明全历史IC及合法背景关系，再检查相应标量；仅得到同号差值不足以继承PB反例。
