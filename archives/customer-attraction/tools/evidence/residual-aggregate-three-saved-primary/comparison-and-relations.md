# R642 security_aggregate 五源只读比较

本辅助检查只读共享clone与父方clean show原件，未运行原main、LP、DP，未操作Git/work.py，未读凭据。三张静态纯背景查询行用一次标准库Fraction计算；不是新随机实验。

## 已有内容与真正差异

- `65bccd3aa2af649ab6c1`、4708 B `probe.py` 的同SHA `ddca945bcdea1da2610e2da7520902fb875531d619be99e5b8da7998f33c8ae0` 已原样保存在 `archives/customer-attraction/tools/evidence/residual-aggregate-group-cone-two-primary/related/probe.py` 和 `residual-pair-probe-resume-primary/related/probe.py`；两manifest明确属于related-only，不是该源已完成的证据。
- `f43fdecee794648b584b`、3952 B R642 `pair_cone_probe.py` 与正式 `pair-aggregate-security-search-five-primary/original/d2b7efc9400032fbf105/research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/security_aggregate/pair_cone_probe.py`（4040 B）逐字diff只有一行：后者在ROOT后增加 `sys.path.insert(0,str(ROOT/'history/source/notes/customer_attraction/transport_round'))`。数学LP、19个5人7标签策略过滤、seed615039及更新停止逻辑完全相同。`common_q_generator.py` 顶层第366行 `from policy_patterns import candidates`，故旧R642裸运行能否加载依赖还取决于环境；不能借后继修正版1900记录替本源制造成功运行。
- 本R642 3952 B不要和R731 5331 B `pair_cone_probe.py` 混为同一程序。后者是带(counts,target)控制器的plain首两人安全值锥，前者是带尾项的PAIR上界交替锥。正式已有页 `两步安全链的固定策略锥搜索与两份浮点纪录--程序.md` 处理R-d51修正版与all-subpath版本，可去重数学正文而补版本差异。
- 三JSON的SHA未在已查Boss8/正式证据manifest中出现。它们全部没有 `ordered_path`、`path_payoffs`，而当前4708 B helper会返回两字段；不能把新恢复策略冒原保存动作表，也不宜声称当前原脚本逐字段生成了较早格式。
- 旧Boss8 `resume-aggregate-pair` 是2316 B `pair_probe.py` /2254 B `pair_probe_r5b0.json`（七标签五人空根111客户），不是本三点。其保留完整集合值递推及一条最差终局路径的逻辑可复用；原1500请求不是完成数。

## 三保存点纯鞍点与标签

各行D_j是对手全选终局唯一标签a共r−1次时所有纯查询收益；c为a项。纯a对任意合法r−1槽对手保证c，以下每行其余项均严格小于c。

|源|客户数|b|r|a|c=v_r|P_r|D_0,...,D_(k−1)|
|---|---:|---|---:|---:|---:|---:|---|
|cdc51dbd8435fa588def|33|(5,0,5)|3|1|63/10|189/10|(29/6,63/10,51/10,51/10,74/15,47/15)|
|816d08f10bd9433415e7|61|(3,4)|4|2|32/3|128/3|(89/10,133/15,32/3,103/15,112/15,6,11/2)|
|ec4a78b7b0f1e4b3d871|48|(1)|5|6|53/6|265/6|(16/5,23/6,43/6,32/15,32/15,67/15,53/6)|

三点P_r/(r v_r)=1精确成立，r5原0.9999999999999999只是数值打印，不能作严格负点。r3客户支持上标签2、3同覆盖；仍保两个动作及所有由其区分的有序历史。另两点标签覆盖互异。三个b均为合法有序旧动作，不自动是在某根SPE上发生的实际前缀；P_r也不等全局覆盖。

## 一般重复终局校准已存在的承重证明

固定合法背景b、r≥1、任一合法标签a。记

`c = sum_(S contains a) w_S/(b_S+r)`，

`D_j = sum_(S contains j) w_S/[1+b_S+(r−1)1_(a in S)]`。

若一份完整子SPE实际终局为a^r，则末位真实BR给全部D_j≤c。纯查询a的逐客户竞争负载≤r−1给v_r≥c，纯对手(r−1)a给v_r≤max_jD_j≤c，故v_r=c且P_r=rc。这只需所选路径末节点的BR；不以静态鞍点逆推一份任意给定策略全部离轨可信。

同定义及一般条件证书已明确写在 `state/程序/合法背景首两人安全比的有限探针与三个取等点--程序.md` 式(6)(7)。其式(8)还证明：D_j≤c时，全部有序历史恒选a是一份完整子SPE；D_j<c对全部j≠a时，由末位再向前逆推得该完整纯SPE唯一。三本点恰均满足严格条件，因此可用既有解析论证证明唯一恒a策略，再以新DP/全历史账本作独立有限核验。重复标签、空题、零客户和任意弱平局均不破坏非严格版；三点的严格性只属本输入，不改一般模型量词。

`state/计算/五人七主题静态安全值探针的精确取等点--计算.md` 是同纯鞍点/严格优势原理的空根34客户特例，不能混其数据/运行和本三个合法背景点。`单色真实后缀的饱和查询与剩余税--引理.md` 是A B^r及M=0的更一般不同接口，不能把其正税开放问题塞入本简单a^r特例。

## 接续关系

1. 共同目录完整历史模型定义承担单位客户、真实偏离、任意有序历史/平局；标签别名按软件扩展保留。
2. 完整历史终局全集算法和既有pair恢复页承担集合缓存不限制为计数策略、最差终局可由完整有序树实现的逻辑。
3. PAIR候选及R-d51后继程序承担固定策略全IC客户锥和上界方向；非负有限筛查不给PAIR或六人half。
4. 本三点纯鞍点是P_r=rv_r有限等号基准，不是一般残余聚合桥证明。任意合法背景plain前两人桥已有PB-extra否定，PAIR因尾项不同不能借此标假。
5. 原samples_requested1000/1000/300并无实际完成数，不合并成2300已执行，更不重复随机重跑以补造旧历史。
