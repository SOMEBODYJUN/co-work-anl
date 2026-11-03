---
id: "customer-attraction/d1-finite-insurance-and-background-aggregate-probes-actual-contract"
kind: "program"
type_tag: "程序"
title: "R-d1有限保险与背景聚合探针的真实目标"
status: "original-code-and-all-saved-fields-read;no-new-search-or-LP"
summary: "完整区分单客户阴性、两固定策略有理提案、150次背景LP记录及成熟11/36客户原审计；原浮点值、未保存策略、入口副作用和真实0运行保全。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/insurer_candidate_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/insurer_candidate_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/insurer_candidate_probe.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/insurer_candidate_probe.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/overlap_policy_cone.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/overlap_policy_cone.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/overlap_policy_cone.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/overlap_policy_cone.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/attack_background_aggregate.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/attack_background_aggregate.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/attack_background_aggregate.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/attack_background_aggregate.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_extra_failure.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_extra_failure.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_extra_failure.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_extra_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_tax_alpha1.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_tax_alpha1.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_tax_alpha1.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_actual_tax_alpha1.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/README.md"
---

# 五个程序不能合并为一种验证

本页全部程序/JSON 均全文实读；原 150 行背景记录、31 类型权重、全部额外查询矩阵以及 13 人审计字段均保原字节。[原件与输入身份](../../tools/evidence/d1-stable-reset-and-shared-rent-primary/README.md)记录双冻结 commit、精确路径、SHA、大小与复用依赖。**本轮原 import/main/函数、随机/BI/LP、完整 IC 新调用均 0**。保存的历史统计不是这轮新产生的日志。

## insurer_candidate_probe：计数全集的浮点有限诊断

2480B NumPy 程序默认 k=4、m=5、1000 trials、seed=13721，生成整数 1…14 的稀疏类型重数并用容差 10⁻⁹ 的计数递归求 SPE 可实现终局集合。对根各行动 child 集取最小当前利润，再取最大得到浮点 M；随后扫描各 child 的 h 与叶福利 W，最大化
\[
J=OPT_m-2W+3(h-M).
\]
它**没有先过滤 h≥M**，因而一般被扫描的 child 未必可作为根实际选中分支；若今后提案满足 h≥M，才有可信根补齐方向。此区别不影响以下全平局保存点。改进阈值 10⁻⁸、正候选阈值 10⁻⁷，仅为数值筛选，不是精确证书。

414B 报告保存 trial124、seed13721、15 个非空类型权重、a=0、q=(5,0,0,0)、h=M=0.2、W=OPT=1、J=−1、completed_trials=1000、历史 seconds=1.9216210842132568。唯一非零权重在 mask13（喜欢标签 0、2、3），另一个标签 1 为空。该**另定义单位客户点**可直接解析：有覆盖标签时，任一玩家若选空收益 0，可改覆盖标签得至少 1/5；所以任何 SPE 每位都覆盖，利润 1/5，W=OPT=1，准确 J=−1。原 float0.2 不被改写成有理证书，解析值 1/5 另标来源。

1000 次随机输入未全部保存，报告只留下一个 best 与计数/时间，不据此重建丢失轨迹或作一般上界；本轮未重启该扫描。

## overlap_policy_cone：两份固定全策略的全部类型重权

2332B 源码先用私有质量 (2,m−1,1,…,1) 的 Fraction BI 补齐特定 offpath，构造两份全有序动作图 H/L；其实际叶 H=(0,1,…,1)、L=(0,0,1,…,1)。之后对每个非空兴趣 mask 构造的是 **NumPy float IC 行**，包含根、全部历史、全部行动和自身零行。LP 变量为 w≥0、Σw=1，强制这两图都 SPE，目标
\[
J=1-2W_H+3(h_H-h_L).
\]
m 标签、m 玩家时全部标签可被 m 槽覆盖，所以总质量 1 就是真 OPT_m。若未来精确可行点 J>0，它足以反更强的有效幅度界（真 M≤h_L）；源码不求新 M。

SciPy HiGHS 成功后每个权重独立限分母 10⁶，既不再核有理和/非负，也不精确回代 IC 或目标。513B 保存 m5、types31、rows7810、float score=−0.0、31 个权重字符串、H=01111、L=00111 和 numerical-only status。非零权重为单例 mask1,2,4,8,16 的 2/9,4/9,1/9,1/9,1/9，其他全零。原数组自身恰非负且和 1；清分母是 9 名新单位客户，不是报告的 LP 最优证书。

按该字面点和两叶直接算 h_H=2/9、h_L=1/9、W_H=2/3、OPT=1，所以 J=0。这里仅是明确原始点的静态代数，未重跑两图 7810 个 IC；两完整保险形状与[既有不交构造](../定理/多主题独立保险的三倍根修复与半覆盖等价--定理.md)一致，不能从这个零点推全部交叠策略锥的精确最优或一般常数三上界。原 CLI 需 m/out，成功覆盖指定输出。

## attack_background_aggregate：150 条有限数值非分离

3345B 原码**没有 main 保护**，import 即开始随机/LP 并写同目录报告。seed482019，依次 (k,r)=(4,3),(5,3),(4,4),(5,4),(5,5)，每组最多30轮；合法背景主题计数 b 随机取0…4，每第三轮改为单一大背景。每轮先以随机浮点质量和 10⁻¹¹ jitter 做全有序 BI 选一图，再固定这张图的全部真 IC，对新非空类型质量 x≥0、Σx=1 做 LP。

查询 p 由正整数1…4归一，偶数轮均匀；p 是输入当轮先选的分布，不是优化后的安全最优查询。对兴趣类型 M，令 b(M) 为背景主题计数在 M 上的和，c(B,M) 为静态 **r 槽**多重集 B 在 M 上的份数。对每个这样的 B 加约束
\[
t\le\sum_M x_M\frac{\sum_{a\in M}p_a}{1+b(M)+c(B,M)}.
\]
目标最小化 V−r t，其中 V 是该固定真实尾 σ 的**剩余玩家总利润**，非含背景旧人的全体福利。若存在精确可行正 gap=r t−V，因同一 p 对所有静态 B 保证 t，足以否
\[
\mathrm{BG\!\!-AGG}:\quad P_r(b)\ge r\,v_{r+1}(b).
\]
静态对手不观察 query 实现，r 槽与 r−1 槽的其他安全值不同。

44297B JSON 包含 150 条完整 records（5组各30），各有 k,r,b,trial,p,gap,success，全部 success=true、gap<0；总 status 是 finite numerical nonseparation。最好为 k4/r3/trial18、b=(24,0,0,0)、p=(.25,.25,.25,.25)、gap=−0.003968253968253968。不能把近似数自动授精确 −1/252 上界。

每条没有保存 LP 新 x、完整 σ、IC 松弛、t、对偶或逐轮时间，不能从这些行直接重验 SPE 或安全值。数值 p 也未有理恢复；例如五项 literal0.2 的 binary 和不等于精确 1，须保其原数值身份，不静默归一为原运行输入。正 gap>10⁻⁸ 时才另外写完整点并 sys.exit；95秒预算只在每轮 LP 后检查，阴性记录的源码不保证严格95秒硬限时。本报告确有150行，但没有完整当次 stdout/版本/时间事件，既不捏造也不重跑以补旧历史。

任意背景前两人 PB 反例不直接反本 **全部 r 人总利润** 的 BG-AGG；原背景可能全覆盖客户，P_r亦非W。相邻根/实际前缀强聚合、Mpath/FTA和原half都保各自量词。本有限阴性不恢复已被别族否掉的逐人或首对桥，也不证明尚未支付的总预算。

## 两份已成熟正例的独立原实现

3809B review_actual_extra_failure.py 无 guard，读取规范十一客户输入及证书顶层 actions，核31个有序决策键及155个全行动 IC；实际 AAB，u=(5/2,5/2,3)、W8。按5个查询给 (5/3,3/2,3,5/2,5/2)，m max−W=1。4248B 输出另存三位置各5列真强制终局的查询矩阵（75项）、actual终局查询、末位 LAST 矩阵及有理 p=q=(0,1/3,1/3,1/6,1/6)。该有理匹配上下界给 M_LAST=7/3，3M=7≤8。

本原实现读的规范策略与另一旧 actual-extra 生成证书四处末位平局不同，不能因同 AAB 当同图；[成熟三人正文](../反例/实际终局额外查询的三人反例--反例.md)已明确这四键。这里只保本来源真实证书读取合同和全矩阵，不借旧另一证书重放声称本入口已跑。两个实现算术相同也不能使全图身份相同。

3982B review_actual_tax_alpha1.py 同样无 guard，读取原36单位客户、m13/6标签的 gzip 完整自动机。每个有序历史按观察行动运行该自动机；独立遍历27243可达状态（含终局），检查行动边计数增一/13深终止，再反向求真终局、用 lcm(1,…,13) 整数放大核18675决策×6=112050全行动 IC，最小0。915B JSON 保存 actual P^10,A,A,B，12人利润5/2、末位3、W33、G=359/66、查询向量 (5/3,3/2,3,5/2,5/2,25/11)；m max−W−G 及 mF(last)−W−G 都为37/66。

它否的是未缩放实际终局税桥/插入预算 SAIC=ENT1，**不是**本例 LAST、安全聚合或原half。成熟[同一性审查](../审查/实际终局插入预算与未缩放税桥的同一性--审查.md)已绑定完整原输入和验证范围，本轮不重复112050 IC，不把旧 JSON 的 all_exact 当新调用。原 meta 中 α=(m−1)/m 版本另有29481/123025超额，是另一缩放目标，不能替换本 α=1 的37/66。

五程序输出都保覆盖写副作用；本轮只读原字节。原运行次数和本轮0运行分别记录，成熟成功范围及新增解析算术没有相互代记。
