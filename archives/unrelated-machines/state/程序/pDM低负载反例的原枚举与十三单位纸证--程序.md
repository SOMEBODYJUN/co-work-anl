---
id: unrelated-machines/program-pdm-escape-original-and-thirteen-load-proof
kind: program
type_tag: 程序
title: pDM低负载反例的原枚举与十三单位纸证
status: retained-finite-witness-program-with-direct-instance-proof
summary: 完整2997B生产源码和1362B原报告绑定，三超边NO实例648分配、OPT13/T12；给同一实例负载13显式解与负载12不可能的整数纸证，补齐原资料链接而不改旧报告或done。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/pdm_escape_counterexample.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/pdm_escape_counterexample.py
  - clean:3c0b982bc439ef7ad28d
---

# 完整源与旧有限结果

[原2997B程序](../../tools/evidence/restored-pair-subdivision-and-pdm-audits-two-primary/source-root/tests/audits/unrelated_machines/pdm_escape_counterexample.py)
完整读，SHA `d8ecca86cfd98551ed046fd5f2d3466c00c8832b8bbd0b2767bb8499c94a64f6`。
[旧1362B结果](../../tools/evidence/restored-pair-subdivision-and-pdm-audits-two-primary/source-root/evidence/runs/unrelated_machines/pdm_escape_counterexample_audit.json)
的audit_code_sha与它一致。
[已有有限反例页](../计算/pDM阈值桥低负载NO逃逸的有限反例--计算.md)
当时没有拿到程序；本次补全生产源码、实例解释和指纹，并把相同原报告复制到该页原来缺失的链接路径。
不改其它Boss已完成正文、原报告或旧done。

本源此前handoff，本次从本地Git blob且禁网正常show恢复。当前main/import/分配枚举均0运行。
下面的13单位推导是同一已知有限实例的纸面证明，不是新的困难性结果或新反例族。

# 一、三超边与十个实际任务

三个部分各两顶点，三条超边

\[
 e_0=(a_1,b_1,c_1),\quad e_1=(a_1,b_2,c_2),\quad
 e_2=(a_2,b_1,c_2).
\]

两两相交，故不能选两条互不相交超边覆盖六顶点，没有三维完美匹配。
机器就是这三超边，d3、n2、m3、b4、阈值T=bd=12。
六个vertex任务各处理时间4，只可去含该顶点的机器；
另 `b(m−n)=4` 个dummy任务各时间3，可去任意机器。总任务10，总工作量24+12=36。

`build_instance`先有一条zip展平vertices的临时赋值，但紧接着用
`(a1,a2,b1,b2,c1,c2)`完全覆盖；实际迭代顺序以后者为准，不产生重复顶点任务。
三个vertex(a1,b1,c2)各有两个可用端，另三个各一个，四dummy各三端，
完整合法assignment总数为 `2^3*3^4=648`。
这不是无资格任务、零客户或其它博弈的输入。

# 二、不用重跑即可核实的最优值13

给一个实际调度：

| 机器 | vertex任务 | dummy数 | 负载 |
|---|---|---:|---:|
|e0|a1,b1,c1|0|12|
|e1|b2,c2|1|11|
|e2|a2|3|13|

每vertex确在所属超边，每dummy均有资格，所以OPT≤13。
这张表是纸面显式见证，与原报告best_loads相同；原报告没有保存best_assignment，不将本表伪称原stdout逐字段重放。

若峰≤12，总工作36分三机迫每机恰12。
设某机接v个vertex和d个dummy，整数式 `4v+3d=12`，且0≤v≤3，因为每超边仅含三个顶点。
唯一解为(v,d)=(0,4)或(3,0)。
四dummy因而全放一机，其余两机各接自己的全部三vertex；
这要求两条互不相交超边覆盖六顶点，与两两相交矛盾。
因此没有峰≤12的调度；负载均整数，OPT≥13。合上界得

\[
 OPT=13,\qquad OPT/T=13/12.
\]

这保住了pDM精确阈值桥“NO则至少T+1”的方向，
同时否定仅从无完美匹配就推近二NO负载的朴素加强。
一个13/12例不证明所有NO有此上界，不排除别的gap放大或一般UM算法。

# 三、原枚举的准确控制流与输出

`exhaustive_optimum`逐完整options笛卡尔积枚举，按原jobs顺序用Fraction累加每台机器真实负载；
首次遇更小峰值才替换best，不在平局时替换，所以返回一个固定字面顺序的最优见证。
它不调用LP、配置、匹配判定器或外部依赖，时间随本显式有限分配数增长。
`main`断言超边两两相交、一个附加坐标重复条件、总工作36，
随后枚举并断言最优13、输出负载峰等最优、最优>T且比为13/12。
附加 `not any(某坐标三值互异)`并非一般无完美匹配验证器；
这里的NO已由上述三条边两两相交独立证明。

有main guard，import仅定义函数；无参数解析，`--help`仍执行main。
只用fractions/itertools标准库，不读输入文件、不写文件、不访问网络。
原stdout是Python字典的 `print({...})`，**不是json.dumps**：
含tuple、字符串及status，不保存源码SHA、Python版本或perfect_matching判定字段。
原1362B JSON是对结果的结构化记账，额外有code hash及解释；
不能把它当作本源码未经处理的逐字节stdout。
`NO_schedule_at_T:false`是原报告的原字段名和布尔值，原样保留；
本页直接用纸证说明不存在T调度，不以这个名称歧义扩大判定器合同。

`exhaustive_optimum`自身不验证任意调用者提供的jobs/options一致性，
它遍历的就是给定options；main只用build_instance产生的固定合法10任务。
这不是一般(pDM,参数)构造器、一般perfect-matching识别器或多项式调度算法。

# 四、来源关系与接续

[主/相关清单](../../tools/evidence/restored-pair-subdivision-and-pdm-audits-two-primary/primary-and-related-manifest.json)
保原source、旧handoff状态、禁网恢复、新actual13源claim raw needs-attention及独立无损proof。
认领pushed与本地恢复是两事实；独立proof的3untracked/2tracked均same、无unmerged，stash保留，未把raw改成synced。

本次把原JSON补存至已有计算页的原缺失路径，是精确字节复制，非重新生成报告。
其余新关系是“原程序实现既有有限记录”及“同一具体实例的纸面最优证明”；
没有建立阶段三超图，也没有改变一般UM目标的开放状态。
正式正文与必要依赖checkpoint确认pushed之后，才给2997B程序单独done，
旧报告来源不额外计数。
