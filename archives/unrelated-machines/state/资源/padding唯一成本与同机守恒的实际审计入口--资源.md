---
id: padded-fork-and-identical-work-audit-entrypoints
kind: resource
type_tag: 资源
title: padding唯一成本与同机守恒的实际审计入口
status: 两个原入口完整保留，历史运行与文档版本差异明确
summary: 保独立padding的显式分数点/真槽注入/16核心分配检查，以及同机凸包初始化调用真实舍入与循环代码的完整依赖范围。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/padded_fork_unique_cost_independent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/identical_work_invariant_audit.py
---

这两源不建立同一种初始化障碍。padding给任意可行assignment-LP点上的单目的地峰非增停滞，点不满足CONFIG投影；同机族点有完整真实最优凸分解，却只排逐坐标非增。一般证明和真实先验已在[分流版本审查](../审查/分流循环修复的冻结版本与审查先验--审查.md)，固定槽主族已有[双源正文](../审查/固定工作局部极小与真实凸包固定槽双源审查--审查.md)，本页补全部原入口及它们确实执行的检查。

## 独立padding原矩阵和分数点

[6728B程序](../../tools/evidence/cyclic-independent-audit-suite/original/padded_fork_unique_cost_independent.py)，SHA256 `25be7b639d34faa0eb9292c08e910d55027fed9cb4e4bd0a7624257ae5c4a538`，无仓库导入/外部文件。`case(theta)` 内构造T1、C2−θ、a1−θ/2、N=⌈8/θ⌉，实际main只取θ=1/k、k2–64，所以N8k。任务行字典P保存有限机器端，未列即无穷。核心X:Aa/Bθ/4，Y:Aa/Eθ/2，b:Ba/A1，c:Ea/Bθ/4，另两私有f_B/f_E各a；四件可动任务各添到每H时间1，每H另有仅该机的私有h_s:a。

初态X,Y在A，b/f_B在B，c/f_E在E，h_s在H；最优把X,c送B，Y送E，b送A，其它不动，核心全1、H载a。b若留B必与f_B合载C>1，去任其它有限端需1，所以OPT下界1，不错误使用b的最短端。

取t=(a+1)/(4a)、β=θ/(4a)、F=4−2t−2β：X,Y当前端质量t，其余均分H；b/c当前端质量β，其余均分H；私有任务全留原机。程序逐行核质量和1、全部正支撑合法且处理时间≤1、初态边正支撑，分数负载三核心1−θ/4、H为a+F/N≤1，初始总工作量≤m且≤分数总成本。所有新H接任何可动任务后1+a=C+θ/2>C，因此峰≤C的全矩阵分配必完全避开新增端点。

程序只需枚举核心四任务的2^4=16个实际端点选择，后续私有任务固定，核不同于初态且峰≤C者恰为所列OPT分配；这迫A向B/E分流。输出one_destination修复0来自这一完整核心排除加H容量论证，并非穷举(N+2)^4个padding目的地或调用一般重配置求解器。

## 真正槽图、成本证明与有限输出

对每机器按(-P[j][i],job_index)排序正分数区间，精确切单位槽，保存每任务的所有正交长(machine,slot)；没有浮点、匹配求解器或成本优化器。显式注入为X→(A,0)、Y→(A,1)、b/f_B→(B,0/1)、c/f_E→(E,0/1)、各h_s→(H_s,1)，程序逐项核槽边合法、注入数n及无重复槽。

X/Y质量t满足1/2<t<1，故X/Y可以占A两槽；b/c与私有任务按job标签平局序有正交长；H先放时间1小分数前缀F/N∈(0,1)，再放质量1的私有任务跨槽0/1，因此槽1合法。正支撑中四件可动任务当前a<1，是各自唯一最便宜机器；私有任务只有原机。显式注入达到逐任务成本下界，故全部最小成本槽匹配都诱导同一坏机器分配，槽级匹配本身不必唯一。代码不是通过“跑一个min-cost matching得到坏例”来证此全称结论。

main无CLI/seed，k2–64共63实例，m8k+3、n8k+6；[完整1,104,957B冻结JSON](../../tools/evidence/cyclic-independent-audit-suite/historical-frozen-runs/padded_fork_unique_cost_audit.json)保全部63条记录和17010个[job,machine,slot]注入三元组。k2还输出完整P/x/初态/OPT/全部负载，与[拆分矩阵](../../tools/evidence/cyclic-independent-audit-suite/comparisons/padded_fork_k2.json)及[证书](../../tools/evidence/cyclic-independent-audit-suite/comparisons/padded_fork_k2_certificate.json)对应：19机器22任务，a3/4、t7/12、β=1/6、F5/2，核心分数载7/8、H29/32。其余k记录只有统计和注入，不伪称每条都有完整矩阵序列化。

本次完整解析63条记录及每个注入条目，核参数、个数和注入结构；这是旧证据的结构核对，不是执行原case/main生成新结果。旧记录代码SHA与本次原件一致，原审查明确主研究者实际重跑该规范入口。复用历史run，本批新增运行0，旧status passed/Python3.12.14但进程exit_code未记，不补造。没有宣称点basic；A大任务总质量2t>1，故不在T1配置投影；也不说所有LST实现或所有LP点都选同一坏输出。

## 同机守恒入口的真实调用链

[4630B程序](../../tools/evidence/cyclic-independent-audit-suite/original/identical_work_invariant_audit.py)SHA256 `a3c47247037f4b494b1db98b881792d220c485ab1cbea149e71b486e0ebd4c46`。ROOT取原脚本 `parents[3]`，动态导入且登记sys.modules：

|文件|执行作用|本次实际SHA256|
|---|---|---|
|rounding_and_gap.py|`round_slots` 标准排序单位槽+BFS增广匹配，接给定可行x；不运行其audit/main|`5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a`|
|cyclic_batch_repair.py|`optimize`，T1、η=1/4；导入不执行其audit/main，不读取padding夹具|`47dbed9b77a7ec7e3c12f30a7110adb398ec6d96197ab0b642457584dba8a057`|
|optimal_convex_fixed_slot_gap.md|仅在最终输出时read_bytes求证明来源文档SHA，**不解析或执行**|当前冻结 `37f9ae7920ff063c3cd6dcf331d974194bde2f3e5913c7ebc0a7e7e2db333e29`|

两执行依赖[原件](../../tools/evidence/cyclic-independent-audit-suite/dependencies/rounding_and_gap.py)及[循环原件](../../tools/evidence/cyclic-independent-audit-suite/dependencies/cyclic_batch_repair.py)已完整实读，验证/真槽区间/匹配与循环合同对应；related `optimal_convex_slot_gap.py` 虽也旁读保留，却**不被本入口导入**。将来隔离重跑需镜像共同仓库根路径，不能只复制脚本到任意目录。

## 同机族、实际穷举与允许的逃逸

对m2–8，n=m²，任务时间为[1]+[1/(m+1)]*(n−1)，每机器相同，x每项1/m。入口独立建立m份循环平移调度，每份每机负载1，逐i,j核均匀平均恰x；大任务时间1给真实OPT1。调用真实round_slots，独立重算其报告负载，核总工作量m、峰2m/(m+1)，再调用真实循环optimize并核分配未变、成功0轮。

为何不是仅有限巧合：相同机器总工作量对所有合法分配恒为m；若所有坐标不增而总和不变，各坐标只能全相等。每循环批次撤出等于到达，正余量不可能。标准固定槽每机恰m槽，总槽数n，任意覆盖匹配每机恰m任务，所以大任务机负载2m/(m+1)，余机m/(m+1)；真实最优凸分解并不能给逐坐标非增修复留下下降处。这是复用boss7族的直接守恒推论，不是新族。

入口另独立枚举m2的16、m3的19683个**完整实际分配**，每份验证总量不变，并检查逐坐标不增者载荷全等，计数分别3和560。这些不是只有原分配一个：任务身份变化可以保持全载荷。m4–8没有全分配枚举，JSON相应0是未执行计数，不能说不存在满足者。

每m还真的迁一件大任务机上的小任务到任一light机。接收机从m/(m+1)升至1；原高机降到(2m−1)/(m+1)，因此新峰为该值，严格低于原峰。这是接收机增载的单任务逃逸，不受逐坐标单调合同约束。冻结表：

|m|初峰|单件后峰|优化器成功轮|
|---|---|---|---|
|2|4/3|1|0|
|3|3/2|5/4|0|
|4|8/5|7/5|0|
|5|5/3|3/2|0|
|6|12/7|11/7|0|
|7|7/4|13/8|0|
|8|16/9|5/3|0|

## 历史文档版本不能伪装成整体同字节重放

旧[守恒JSON](../../tools/evidence/cyclic-independent-audit-suite/historical-frozen-runs/identical_work_invariant_audit.json)与原审查追加记载实际规范运行，代码及两执行依赖SHA均与本次字节相同。但旧第三项证明文档SHA为 `8bbc487e1d4d4f69a0755e92e7f1f803217d63dd52b774a3a6f4eb42a7847f9c`，当前[冻结全稿](../../tools/evidence/cyclic-independent-audit-suite/comparisons/optimal_convex_fixed_slot_gap.md)37f9...已有后续§6最小工作量面。因而本次复用的是带8bbc历史文档元数据的旧run，不能称当前整套依赖逐字节重放过。代码只输出此文档hash，数值输入/调用不取其内容；当前全读确认原族与守恒推论保持，后续支撑面不是本入口新增测试内容。

本次不执行新main，不生成冒充当前stdout的新JSON，不倒填旧第三依赖或退出码。历史身份、两实际执行代码相同和文档版本差异同时保留，详见本批run-binding。一般UM、配置派生单目的地修复、外审与全球新颖性均没有因此被否定或认证。
