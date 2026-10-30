---
id: "unrelated-machines/processing-gcd-arithmetic-endpoints-and-zero-branch"
kind: "computation"
type_tag: "计算"
title: "加工值GCD审计的算术端点与零分支"
status: "full-canonical-source-read-with-new-targeted-interface-failure"
summary: "完整保存十矩阵精确生成、合法负载格点和单调端点算术；首次定点观察确认有未用正端的OPT0触发原helper断言，包装器正常退出不代表原调用成功。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/finite_palette_gcd_barrier.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/finite_processing_palette_gcd_barrier.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/finite_palette_gcd_barrier_audit.json"
---

# 加工值GCD审计的算术端点与零分支

本批完整实读[主稿](../../tools/evidence/processing-palette/original/research/current/unrelated_machines/finite_processing_palette_gcd_barrier.md)和[规范程序](../../tools/evidence/processing-palette/original/tests/audits/unrelated_machines/finite_palette_gcd_barrier.py)，比较[Boss2已done的十矩阵报告](../../tools/evidence/processing-palette/original/evidence/runs/unrelated_machines/finite_palette_gcd_barrier_audit.json)。代码hash`aea8a50663aa63803b9f5377e992cc7abb6fc3b97ad53bf4c3a2f3c68b4170e1`，报告本体hash`9aac773b2ce4375699870c0e9cd00cc9c45464c76b1ecdb48beea15f9f311010`，新[逐源清单](../../tools/evidence/processing-palette/source-manifest.json)保全部commit/path/size/hash和claimed/comparison角色。报告不重复认领。

[一般格点余量定理](../定理/加工值格点的可计算统一余量--定理.md)承担完整域、严格槽证明、整数目标网格与量词；本程序完全不求LST、不接舍入器，也不输出一般算法的调度。它只独立核GCD/LCM、所有小实例实际负载的g格点和最后的算术不等式。

## 所有函数和真正被枚举的对象

输入P在内部以Fraction/None构造，m≥1、n≥1、每件至少一有限端；不是全格式验证的外部API。`grid`只对至少含一正有限值的矩阵调用：LCM所有有限分母，正整数化时间求GCD，返回(g,B,D)。零参与LCM但不进正GCD，None不参与二者。

`loads`按assignment逐件求和，用到None就返回None。`exact_opt`遍历mⁿ个机器标签元组，删None分配，保最小峰及**合法完整分配数**。`check_one`又枚举一次所有合法分配，逐机核load/g为整数。因此报告的`feasible_assignments`与`assignments_with_all_edges_finite`是相同合法有限端集合的两次计数；它们不是峰≤某阈值的可行分配数，更不是LP可行性证书。

对正OPT，程序只检查T集合`{g,min(B,OPT),OPT}`去重后的2或3端点，b只取0和min(B,T)。代码没有逐点遍历一个可能巨大的有理格，也没有枚举所有实际支撑最大件。其完整算术理由是：

\[
f(T,b)=T+b-g
\]

随b单调，最大值在min(B,T)；最大帽`T+min(B,T)−g`随T单调且只在B换一次线性式。因此这些端点与b两端的检查，结合这个一般单调性，覆盖给定有限实例的全部0≤b≤min(B,T)、g≤T≤OPT格点帽。它**不证明**某个T的LP可行、某个b确来自正支撑，亦不承担严格槽界的证明。

## 完整十例输入与冻结范围

四固定矩阵如下，记D₀=10^100+267，∞在程序中为None：

```text
zero_edges_and_infinity:
  (0,3/2,∞,5/2,1/2)
  (4,0,1,∞,3/2)
  (∞,2,3/2,1,0)
fixed_palette:
  (1/2,3/2,∞,5/2,1/2,3/2)
  (5/2,1/2,3/2,1/2,∞,5/2)
  (3/2,∞,5/2,3/2,1/2,1/2)
coprime_rationals:
  (7/11,5/13,∞,19/17,2/7,11/23)
  (3/5,17/19,1/29,∞,13/31,7/37)
large_denominator:
  (1/D₀,3/D₀,∞,2/D₀,7/D₀)
  (2/D₀,1/D₀,5/D₀,∞,3/D₀)
```

另六个随机例均m3/n7，使用独立`random.Random(20261019)`。每端先用`rng.random()<0.16`选择None，否则加工值为`randint(0,17)/randint(1,9)`；若一列全None，随机一机补`randint(1,9)/randint(1,7)`。这里随机生成资格用float概率选择，所有被核加工值、负载、格点和不等式仍为精确Fraction/整数，未用浮点LP。

| 例 | m/n | 合法分配 | g/B | OPT | ρ=2−g/B |
|---|---:|---:|---:|---:|---:|
| zero_edges_and_infinity | 3/5 | 72 | 1/8 | 1 | 15/8 |
| fixed_palette | 3/6 | 216 | 1/5 | 2 | 9/5 |
| coprime_rationals | 2/6 | 16 | 1/1382294358445 | 332/221 | 2764588716889/1382294358445 |
| large_denominator | 2/5 | 8 | 1/7 | 8/D₀ | 13/7 |
| random0 | 3/7 | 972 | 1/15120 | 14/5 | 30239/15120 |
| random1 | 3/7 | 648 | 1/5040 | 61/18 | 10079/5040 |
| random2 | 3/7 | 432 | 1/5760 | 37/8 | 11519/5760 |
| random3 | 3/7 | 1458 | 1/8400 | 59/21 | 16799/8400 |
| random4 | 3/7 | 486 | 1/11760 | 4 | 23519/11760 |
| random5 | 3/7 | 216 | 1/14280 | 113/42 | 28559/14280 |

完整报告还保每例B、g、有限端数、LCM位长、端点数和算术检查数：总4524合法分配、22目标端点/44帽不等式。互素例D=1236789689135、g=1/D；大共同分母例LCM333bit但g/B仍1/7，说明分母位数与近二余量不是同一个条件。

十例全部OPT>0、`zero_only=false`。即使第一例含多个零端，也没有覆盖OPT0分支，更未覆盖n0。代码的第一条早退只检测**所有有限端均为零**，不是数学模型的“每任务有零端”充要条件。

## 新定点运行保留原调用失败

源码实读发现上述接口范围差异后，本批首次执行了[独立观察包装器](../../tools/evidence/processing-palette/characterize_zero_branch.py)，未重跑十矩阵主程序。它给每个小矩阵另以直接穷举求真实OPT/见证，再调用原`check_one`并记录返回值或AssertionError；原代码、函数与冻结报告完全未改。

| 输入 | 真实OPT/每件零端 | 原helper真实结果 |
|---|---|---|
| `[[0]]` | 0，是 | 返回`zero_only=true`，无正加工端 |
| `[[0],[1]]` | 0，是，未用正端仍在矩阵 | **抛AssertionError**：通过“有正端”分支后，原`assert opt>0`失败 |
| `[[1]]` | 1，否 | 返回g=B=1、ρ1的正分支记录 |

完整[首次stdout](../../tools/evidence/processing-palette/stdout.json)、[stderr](../../tools/evidence/processing-palette/stderr.txt)及[真实命令/返回码](../../tools/evidence/processing-palette/run.json)保留。包装器退出0、stderr空表示观察流程完成且捕获了预期异常，**不表示**中间那次原helper调用成功或通过。此运行是已读源码后的知情接口核验，既不是盲审，也不是一般定理的数值证明。

这限制的是内部算术helper的可复用域。完整数学算法先按“每任务有零端”返回实际零调度，故一般定理不受此断言影响；若要把helper用于宽全域，调用方须先处理该模型零分支。n0也由数学算法处理，而原helper明确断言n≥1。没有借此修写冻结原程序或把算术helper扩称完整LP算法。

## 输出格式、复用证据与接续

规范主程序仅stdout，保Python/platform/seed和十记录；它没有在payload写`code_sha256`、`command`或`scope_note`，冻结报告这三个字段为另附复现/范围元数据。本批静态核payload keys与冻结差集，代码hash与报告附记相同，原字节与Boss2副本相同；不虚构原规范stdout和加元数据报告全字节相同。原程序的数学检查依赖普通启用assert的Python。

本批只新增上述一次三输入定点观察，无十例例行重跑、LP求解或大数网格遍历。[核验记录](../../tools/evidence/processing-palette/verification.json)区分历史报告、首次观察及各自真实scope。原稿归于VW的整数版本保Paper Fact标签，未把未读PDF或已有JSON升级为外审/新颖性证明。

可接续使用的是：正OPT内部算术测试、确切十例输入、一般g格定理及零分支的已观测软件边界。对连续T_LST的gap、随n/N变化字母表、每个固定ε的实际源gap/低负载decoder，须分别使用[一般正文](../定理/加工值格点的可计算统一余量--定理.md)的范围判断；计数与ρ字段本身不提供这些结论。
