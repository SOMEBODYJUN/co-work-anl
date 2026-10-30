---
id: "customer-attraction/optimal-exchange-kernel-exact-audit"
kind: "computation"
type_tag: "计算"
title: "最优交换二项矩与Beta核的有限精确核验"
status: "finite-exact-audit-replayed"
summary: "原字节标准库脚本实际运行一次，核m≤12的24570次有理二项矩与4095次Beta系数；固定组合身份，不枚举客户输入或SPE。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/audit_bernoulli_exchange.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/audit_bernoulli_exchange.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/bernoulli_optimal_exchange.md"
---

# 最优交换二项矩与Beta核的有限精确核验

本对象保留[最优交换生成表示](../引理/最优索引交换的生成表示与查询税--引理.md)的原组合核验程序，并提供本轮一次实际运行输出。它核对E2子列表平均中用到的有限算术身份，不扫描客户实例、策略树或半覆盖。

## 可用文件与运行接口

- [原程序](../../tools/evidence/optimal-exchange/audit_bernoulli_exchange.py)：1492字节，原字节不改。
- [本轮原始stdout](../../tools/evidence/optimal-exchange/replay_report.txt)：Python字典的repr格式，原样保存。
- [解析后的JSON副本](../../tools/evidence/optimal-exchange/replay_report.json)：由原stdout作字面量解析，仅改变存储格式。
- [来源与执行记录](../../tools/evidence/optimal-exchange/PROVENANCE.json)：源ID588621da61aa3af9d88c、两冻结版本、代码hash、实际Python版本、命令和输出hash。

从仓库根运行：

~~~bash
python3 -B archives/customer-attraction/tools/evidence/optimal-exchange/audit_bernoulli_exchange.py
~~~

程序只使用标准库Fraction、comb和factorial，无仓库导入、外部文件、随机种子、LP或优化器。它向stdout打印结果，不写输出文件。主入口固定调用run(limit=12)，没有解析CLI参数；内部函数的limit不是已经建立一般输入拒绝合同的外部接口。

核验由assert承担，须保持普通Python执行，不能使用-O或-OO。-B只禁止产生pycache，不移除断言。本轮保留源码SHA256 `ad995bdab91f6500f20b39af7af5791125d72f2bf42d62e51b05e988a59af64d`，实际执行退出码0，所得pass只表示下述有限断言通过。

## 全部参数循环及两类身份

程序遍历m=1,…,12、s=0,…,m、c=0,…,s、d=1,…,m。定义不足下标的组合数为零；分母binom(m,d)在全部循环中均正。

每个(m,s,c,d)先检查展开多项式积分：

\[
 \sum_{j=0}^{c}\frac{(-1)^j\binom cj}{d+j+1}
 =\frac{c!d!}{(c+d+1)!}.
\]

左端来自将(1−t)^c展开后逐项积分t^d，右端是整数Beta系数。随后在六点

\[
 t\in\{0,1/7,1/3,1/2,6/7,1\}
\]

逐个检查

\[
 \sum_{k=0}^{s}
 \frac{\binom{s-c}{k}\binom kd}{\binom md}
 t^k(1-t)^{s-k}
 =\frac{\binom{s-c}{d}}{\binom md}t^d(1-t)^c.
\]

两边全部用Fraction计算；即使d>s−c或端点t=0,1也直接处理，零次幂按Python有理幂的通常约定为一。没有浮点容差或随机选择。

## 本轮结果与计数含义

完整原输出为status=pass、m_limit=12、exact_moment_cases=24570、exact_beta_cases=4095，以及“有限身份实现核验，不是SPE或half证明”的范围说明。

4095是(m,s,c,d)循环项数：Σ_{m=1}^{12}m(m+1)(m+2)/2=4095。不同m、s可能重复同一(c,d)的Beta身份，所以它不是4095个互不相同的多项式，也不是4095个客户输入。每项有六个t检查，因此二项矩检查次数为24570。

原来源没有在这个脚本旁指定一份独立冻结运行输出，本轮保存的是新执行stdout，不声称与不存在的旧JSON逐字节比对。原代码自身是冻结原字节；原始stdout和派生JSON的格式区别均在执行记录中说明。

## 证据边界与接续

它只检查均匀选槽二项矩和a=1的整数Beta核在所列有限范围的实现。没有验证任意m、所有实t或一般a，没有单独检查非均匀NU、辅助质量FL或实际SPE激励；那些普遍式子由[解析证明](../引理/最优索引交换的生成表示与查询税--引理.md)承担。

锚点版本的正确性依赖保留最优位置的组合论证，真实外部利润还需保留R_out返还池，不因有限核验通过就已获得跨枝预算。后续实现这些核时可复用此固定算术回归，但必须另外说明新输入、计算范围及与证明的对应。
