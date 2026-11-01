---
id: customer-attraction/twenty-nine-client-root-price-parent-Fraction-reconstruction-contract
kind: resource
type_tag: 资源
title: 二十九客户根价格的父方Fraction重构合同
status: two-whole-primary-sources-read;independent-definition-code-understood;zero-new-29-client-run
summary: 保存3896B标准库自写HI/真BI/G与四价格全部57路径、576B十五字段；原始4322是价格LP可行路径而非代码已验完整SPE，29最优由总客户与全盖证明，旧充分成功按同输入复用不重跑。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/parent/audit_interval_price_independent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/parent/interval_price_independent_audit.json
---

# 二十九客户根价格的父方Fraction重构合同

3896B程序和576B报告共4472B全文实读、核原size/SHA256/Git blob。它只用Fraction、lru_cache、Path、json，从固定客户类型重建HI/真BI/累计floor及价格原始—对偶，不读作者输出、规范solver或LP；确实是定义级另写实现，不是把旧JSON标志当计算。

旧29客户已有充分成功/自足证明，本轮同输入及九项相关数学/原件SHA全部核同，复用其已完成数学，不为新“原CLI”标签重跑。当前本3896原main/import/HI-BI/LP/IC均0。程序所称independent只支持这种代码重构范围；没有“读作者前”时间先验、盲审、外审或乘子独立发现认证。

## 六类型单位客户与原收益约定

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，5个共同标签0…4、4名单位玩家，六类重数都是不同单位客户：

| mask | 喜欢的全部标签 | 客户数 |
|---:|---|---:|
|7|0,1,2|6|
|8|3|4|
|16|4|2|
|21|0,2,4|6|
|22|1,2,4|5|
|26|1,3,4|6|

共29。对终局计数q，d_N=Σ_(a∈N)q_a，已用标签收益U_a(q)=Σ_(N∋a)d_N⁻¹w_N；未用辅助坐标取0。代码用六个Fraction(w_N,d_N)相加，是单位客户份额的精确分组求和，不是给玩家加权，也未逐个物化29个客户set。d_N=0类型先跳过，无0/0。

W(q)=Σ_(N:d_N>0)w_N，始终是全部实际覆盖。所有重复选择、空/同覆盖标签在一般模型合法；本固定六类型没有另遍历其它目录或零客户输入。

## 实际三种递归与历史完整性

原代码自己实现：
\[
H_I(b)=\bigcup_{a\in E_I(b)}H_I(b+e_a),\quad
L_I(b)=\max_a\min_{q\in H_I(b+e_a)}U_a(q),
\]
\[
E_I(b)=\{a:\max_{q\in H_I(b+e_a)}U_a(q)\ge L_I(b)\},\quad
G_I(b)=L_I(b)+\min_{a\in E_I(b)}G_I(b+e_a).
\]
终局H_I={b}、G0。真正exact递归则在孩子R中用l=max_a min_child U_a，再逐个终局只保U_a(q)≥l，而不是把eligible孩子整个留下。exact_floors另存于字典但主程序不拿它们验指定有序path。

缓存对象是各计数状态的全部可实现终局集合，不是一份固定Markov政策。各有序孩子的完整后继策略可独立选，真BI逐终局筛必要充分；HI则放松而保超集。代码从root对全部a递归，计数层0…4合126状态（70终局/56非终局）；它没有物化所有1+5+25+125=156个决策历史的策略。

随后enumerate_paths不缓存有序action序列，从HI allowed边枚举全部57条长度4路径与其共同endpoint，共7个HI终局；不是57份完整策略或57个计数状态。真BI根集合只一个q*=(0,0,2,1,1)，也不等于唯一完整policy或唯一有序SPE路径。

## 四非零价格的原始—对偶证书

沿[共同终局祖先价格定义](../定理/祖先门槛的共同终局根价格与标记流等价--定理.md)，对允许完整路径p及其endpoint q(p)，非负价格给
\[
F_\lambda(p)=W(q(p))+\sum_{e=(b,a)\in p}\lambda_e[L_I(b)-U_a(q(p))].\tag{1}
\]
一个路径始终用同一endpoint算所有先前行动利润，不可逐边挑不同终局。原四价格为：

| prefix b | action a | λ | 本code核的L_I(b) |
|---|---:|---:|---:|
|(0,0,0,0,0)|0|12/5|20/3|
|(0,0,0,0,1)|0|12/5|20/3|
|(1,0,0,0,0)|3|24/5|20/3|
|(1,0,0,0,1)|3|24/5|20/3|

其余λ0。enumerate_paths对每条57路径精确assert Fλ≥29，并另assert min Fλ=29；没有调用优化器寻找这些价格。

原始价格LP是路径概率π≥0、Σπ1，且每条允许边e满足
\[
\sum_{p\ni e}\pi_p[U_a(q(p))-L_I(b)]\ge0.\tag{2}
\]
HI孩子包含真BI孩子，所以同一行动的HI最小收益不高于真最小收益，取max后仍有L_I不高于真阈值。真SPE在轨收益达到真阈值，故其实际路径的点质量满足(2)；一般LP可行混合/路径则不必是真SPE。对可行π，将(1)求期望有
\[
E_\pi W=E_\pi F_\lambda+
\sum_e\lambda_e\sum_{p\ni e}\pi_p[U_a(q(p))-L_I(b)]\ge29.
\]
这给固定λ对全部真实SPE福利的下界29；共同endpoint/有序路径是付款不能丢的量。

代码另指定p*=(4,3,2,2)，逐边assert HI允许，最终q*= (0,0,2,1,1)且W29，再对四条沿途边assert U_a(q*)≥L_I(b)。故δ_p*是(2)的原始可行点，目标29，与固定价格下界匹配，准确根价格LP值29。它沿途不使用上表四个非零价格边，但仍核所有原始边条件。

这里`primal_path`是**价格LP原始路径**：本main没有逐边比较exact_floors、没有构造其全部离轨policy。终局恰等真BI唯一q*，不授权把“此有序路径已被代码验为完整SPE”写进记录；当前也不另重演来补这个标签。

λ0给min_HI W25，常数λ1因Σ玩家终局份额=W给min路径floor和G_I=80/3；四价29严格大于两者。真BI/所有客户总数29说明本例全部真SPE覆盖29；价格是在这个有限输入上弥补HI放松，而非宣称普遍最优价格总达OPT或half。

报告optimum=29虽是literal字段，数学上总客户上界29、p*覆盖29已经证明OPT₄=29，无须另外穷举625个终局。源未运行OPT枚举器的事实与该精确有限结论不矛盾。

## 576B原报告全部15字段

| 字段 | 原值/类型 |
|---|---|
|unit_customer_count|29|
|player_count|4|
|topic_count|5|
|HI_paths|57|
|HI_terminals|7|
|G_I|字符串80/3|
|minimum_HI_welfare|25|
|certified_price_value|29|
|optimum|29|
|true_SPE_terminal|[0,0,2,1,1]|
|primal_path|[4,3,2,2]|
|all_primal_edge_constraints_pass|Boolean true|
|all_57_dual_path_inequalities_pass|Boolean true|
|status|independent Fraction reconstruction passed|
|scope|Strict finite improvement of a universally valid root price interface; no general half proof.|

两个pass Boolean仅在原代码全部assert之后写出；历史报告不含每条path的value、各状态完整H/R、策略图、argv/时长/退出码或源码SHA。当前不补这些旧日志、不把status冒本次原main执行，也不把True当无需读源的前提。原字节与完整代码可审阅，原程序的定义域/断言强度已逐条核清。

## 与旧成功、其它程序及先验的关系

已有4169B verify_interval_prices会读1881B candidate，检查共同q/流/57路径等；本3896另写递归、字面客户/价格/原始路径，无该运行输入、没有canonical或作者helper。它还自己算G_I并断言80/3，而旧verifier本身不算GI。二者数学实例相同，不因此构成同一个原main的运行或两个独立新发现。

父审与原7539价格稿/7333证据边界及[全路径与列生成程序资源](根价格全路径与列生成的原程序合同--资源.md)、[共同终局最短路算法](../算法/共同终局根价格的最短路与列生成证书--算法.md)和[325客户层级构造](../构造/三百二十五客户层级目录的唯一续局与根价格--构造.md)已全文读，当前九项SHA与原读取相同，诚实复用。325是另一个输入，列生成的float/限制列上界不是这个29固定Fraction证书；别组母审PASS不移作本原程序当次成功。

程序有main guard、无命令参数/本地input，只标准库。全部assert通过后覆盖写邻interval_price_independent_audit.json，再打印完整pretty JSON；原code/报告相邻原路径保全，当前只AST不import或main。报告未给盲读先验/新颖性，当前知情核对不倒填为旧独立发现或外审。

完整7源claim390da51f…pushed/synced、本2 Boss4 owner/sourceSHA/normal-show及旧比较SHA核见[证据](../../tools/evidence/parent-interval-price-audit-primary/README.md)。本批原main/import/HI-BI/G/57路径重演/LP/规范或独立IC均0；数学通用性来自完整共同终局论证，有限值复用已有充分证据，第三阶段不建图。
