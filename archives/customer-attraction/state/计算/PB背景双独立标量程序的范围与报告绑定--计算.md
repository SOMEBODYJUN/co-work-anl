---
id: customer-attraction/pb-background-two-independent-scalar-programs-scope-and-report-binding
kind: calculation
type_tag: 计算
title: PB背景双独立标量程序的范围与报告绑定
status: four-first-primary-originals-retained-and-fully-accounted; no-new-run
truth_status: fixed-parameter-rational-margins-only; full-history-PB-proof-separate
review_level: 全1595/1515B程序及1826/1096B完整JSON、既有作者程序/报告及PB全证明审查全文比较
summary: 两独立标准库程序固定同8参数，核G/P/F/s−u/singleton与计数；dynamic另核g1比较，parent另作ℓ1..3两类界。无外部输入/策略树/搜索；两个顶层入口及写盘差别、不同计数强度和报告SHA不借作者旧run。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/pair_scalar_independent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/pair_scalar_independent.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/parent/audit_pair_parameters.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/parent/pair_parameters_independent.json
---

# 四原件、模型及已经存在的全历史证明

1595B dynamic程序/1826B报告和1515B parent程序/1096B报告，共6032B，均完整读取、核冻结size/SHA/blob。两代码只用标准库、全部数值字面固定，无外部输入、作者代码导入、参数/策略扫描、客户展开或全树枚举。报告中的“independent”指原实现不调用作者程序，不是本次新盲审、外审或新运行。

被核的是[任意合法背景PB-extra反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)的同一参数：k3、d20、q12、t10、r2475、Q2063、H100000、M10^9。48,495,120客户仍为不同单位客户；巨大整数背景由合法singleton历史实现，已覆盖所有客户。余r玩家的静态安全值v_(r+1)(b)用r个竞争槽、不观察查询。前两人实际各u而一个合法查询分布保证s>u，反驳任意合法背景的pair桥；不是零根pair、实际前缀或half反例。

完整regular策略、Greedy水位及最近偏离者平局、Punish真实切换、Fill/Copy、首次singleton后纯SPE补齐、逐层Jensen都在上述正式反例及[四审查读序](../审查/PB背景反例的全历史审查与版本--审查.md)全文重读。本四资源只核给定函数的标量条件，不能替代那些全历史理由；“scalar true”不证明巨大SPE或背景在轨可达。

# 函数、七项标量和完整精确值

两程序同定义

\[
 f(c)=\frac{q-1}{M+c}+\frac1{M+c+1},\quad
 g(c)=\frac{Hq}{HM+c},\quad
 u=dkf(k),\quad s=d[f(1+rk/Q)+(k-1)g(r+1)].
\]

dynamic先造Fraction(q−1)/(M+c)，parent用Fraction(q−1,M+c)；在固定整数/有理输入上同值。这里u是完整实际一位利润，F是**每段**差，P已经是**整位**比较，不能忘乘d或再重复乘d。

| 本页名 | 精确差 | 两份报告字段 |
|---|---|---|
| G | g(r)−2f(1)+f(2) | G / G |
| P | f(t)+(d−1)f(1)+d(k−1)g(r)−d[f(2)+(k−1)g(1)] | P / P |
| F | kf(k)−f(t)−(k−1)g(1) | F / Fill |
| S | s−u | S_minus_U / safety_gap |
| singleton | dq/(M+r+1)−1/(M+1) | singleton / singleton |
| e₁ | g(1)−f(1) | g1_minus_f1 / 未单列 |
| e₂ | g(1)−f(2) | g1_minus_f2 / 未单列 |

原报告完整有理数为

\[
u=\frac{180000000705}{250000001750000003},\quad
s=\frac{1741078242325546490301775210615}{2418164229266383467676453180700905788}.
\]

G=85212124514272735691/121212121942393940745272728033000000018；P=660643478483407311335386299631939824524678161070147/5499642671862510299007430845381554422866313730295231941054450090745；F=17241792075873809327687186758861/1724137979310362532759105210349467793121068965540；S=655518746053822970420433555247437051305/604541061548383275389777051408169916255944671102717364；singleton=5431818131/22727329022727329；e₁=118180727490907/9090909118181909109091181818182；e₂=2499988007199965/100000000500001000600005000000006。

所有分子/分母正，显示值即给该组固定差的精确正性；dynamic附decimal只是float展示，不参与判定，不能以10^−19附近小数决定符号。两个原JSON全部字段/分子分母都保留，parent缺e₁/e₂不是缺一般证明：f严格降、g(1)≥g(r)，G>0已蕴含g(1)>f(1)>f(2)。没有由这些一个参数值宣称全参数族正性或规模最小性。

# 整数断言和parent额外六次比较

两程序都取L=d(t−1)=180，最晚惩罚索引k+L=183，处罚后的最小空块Z=Q−(k+k+L)=1877，偏离后最少future r−(k+L)=2292；实际Greedy步r−k=2472、初始空块Q−k=2060。

dynamic实际断言2292≥2063、2475<2·1877、2472<2·2060、t10>2；另输出2Z−r=1279。parent实际断言2474<2·1877、2292>2063+3、2472<2·2060。前者的2475界比旧2474界更强，而2292≥Q比后者2292>Q+k更弱；不能把所有代码都说成断同一组式子。完整PB证明选择相应真实遵循/偏离人数方向，不能仅借较弱标量冒同一义务已核。

parent还对ℓ=1,2,3各断

\[
 \ell f(2)+(k-\ell)g(1)\le f(2)+(k-1)g(1),
\]
\[
 f(t)+(\ell-1)f(1)+(k-\ell)g(1)\le f(t)+(k-1)g(1).
\]

第一右减左=(ℓ−1)[g(1)−f(2)]，第二为(ℓ−1)[g(1)−f(1)]，由上述严格比较非负，ℓ1等号。这六次标量比较解释为什么偏离上界在只选一个R块时最大，不是六个策略历史或新扫描。dynamic显式核两正差，parent显式循环六式，两者实现不同、数学兼容。

# 与已发表作者标量原件及两份独立报告的绑定

[既有作者标量资源](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/8a23b701a162a1dd678c.md>)的1926B原代码和1564B报告本次亦全文比较。作者程序同五主要差，断2474<3754、2292>2066、2472>2060和2472<4120，并用`write_text`覆盖同名JSON。其旧一次原字节成功只属于SHA绑定的作者程序，不是本两份不同SHA入口的执行。作者旧JSON“awaiting independent review”是冻结时点，后来四审查不改该字节，本资源也不倒造旧运行。

dynamic报告全顶层含scope/constants、customer/count字段、七组exact/decimal、u/s、strict-positive true、proves_all_histories=false、proves_half=false；parent报告含status、python3.12.14、arithmetic、script_sha256、parameters、五gaps、u/s、free1877、punish180与unit_customers。parent记录源码SHA严格为32ce45d11250eecc08d69b5441f17a5132ac0d5a27f15d88f05a4a73994fdeac，与实际1515B原件一致；版本字符串仅为原报告，不冒称本次解释器事件。

dynamic与parent数值功能已逐项归于上表，二者输出格式和检查域不同，不当字节duplicate。本包将四资源first-primary **retained**：原bytes及功能完整保全，数学去向是本计算及已有PB反例，不另造同一个PB游戏或全历史定理。数值正确性的显示有理证明与程序实际执行状态分开。

# 无guard的真实入口和不执行处置

两代码都在顶层算全部式子、断言、输出，无main guard、无argparse；导入或加`--help`不会只看帮助。dynamic以源码同目录固定`pair_scalar_independent.json`独占创建（x），随后stdout也打印完整JSON，目标已存在会在算完后失败。parent不写JSON，只stdout完整结果，调用者才可能捕获文件；它另读自身源码求SHA，参数不依任何外部JSON。

本次0源码导入、0原CLI、0标量checker、0优化器、0新数学程序；只对原文件/JSON/hash/链接做结构自查。不因为小脚本便补重复执行，也不把历史independent/true字段当新PASS。若将来改变参数/背景/目录，必须重证全历史与静态槽量词，光重获同号标量不足以继承PB反例。完整六源绑定、两正文及逐源receipt见[证据](../../tools/evidence/dynamic-order-summary-and-pb-independent-scalars-primary/README.md)。
