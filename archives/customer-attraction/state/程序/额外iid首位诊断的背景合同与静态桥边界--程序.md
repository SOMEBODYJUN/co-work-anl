---
id: customer-attraction/extra-iid-root-diagnostics-background-contract-and-static-bridge-boundaries
kind: program
type_tag: 程序
title: 额外iid首位诊断的背景合同与静态桥边界
status: exact-identity-entry-replayed; two-finite-LP-diagnostics-retained; global-EI-refuted-elsewhere
summary: 保等f逐客户1080次有理回归、九合法背景完整43节点锥及四个零背景最大f切片；展开正确回复周期归约并以原循环族和后续hub分清已否静态充分桥与真正两人EI。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/check_equal_standalone.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/diagnose_fixed_cone.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/diagnose_maximum_standalone.py
---

# 原候选、已保全数学与历史状态

固定[有限单位客户共同目录模型](../定义/共同目录完整历史模型--定义.md)的任意合法有序前缀，客户背景负载为b，之后余r名单位提供者。EI要求该背景下**每份完整有序历史纯SPE**的当前真实最终利润u≥λ_(r+1)(b)；右侧是另一个静态r+1人对称iid Nash的共同利润。空主题、重复题、零客户、全部离轨历史和平局均保留。静态平均不把实际SPE随机化，也不冻结真实偏离后的后继。

本批四源全文实读；[等单独收益普遍引理](../引理/等单独收益目录的两人首位与任意iid人数比较--引理.md)已经完整保全r1边界、全目录f_b(A)=K的两人u=K−min h_b及对任意q、任意n≥2的iid比较，不另授同一定理。[支持外枢轴族](../反例/支持外枢轴修复与静态查询平均的两人分离族--反例.md)已保262单位客户例与整数无限族：λ₃=997/24、支持平均真实偏离83/2，却可选支持外H保证105/2。这个输入不满足全目录等f，只反支持内查询直接平均的辅助桥。

旧34客户三人例根29/3，而任意四人静态iid总收益≤34，故λ₄≤17/2；旧36客户例根10，λ₄≤9。这两个简单上界无需计算Nash，确实不能反EI。可是原README“一般仍未证/未反驳”只是原2026-10-23时态：[七客户三人银行根](../反例/额外一人iid收益桥的七客户银行根反例--反例.md)已有u=3/2<λ₄=665/432。它否定全r EI，不否定等f子类、r1边界或六人half；本四源也未给一般不等f两人EI的证明/反例。

# 三个程序的实际输入与证明责任

## 等f程序只核逐客户身份和同q删除方向

`check_equal_standalone.py`仅用标准库Fraction、product、comb，无外部输入、无LP或SPE求解器，顶层导入即运行。对b=0,…,9及两个0/1命中a,c，核

\[
 \frac{a}{b+a+c}=\frac{a}{b+1}
 -\frac{ac}{(b+1)(b+2)}
\]

左侧a0时直接取0，未产生0/0。另对t=i/12、i0…12及n2…9，用二项式分布精确计算

\[
 t\sum_{k=0}^{n-1}\binom{n-1}{k}
 \frac{t^k(1-t)^{n-1-k}}{b+1+k}
 \le t\left(\frac{1-t}{b+1}+\frac{t}{b+2}\right).
\]

共10×(4+13×8)=1080次有理断言。这里t是客户被一个q动作命中的概率，不是新玩家权重。代码没有制造等f目录、求h最小值、核完整两人策略或求iid Nash；全b/全q/全n结论依靠已有解析删除耦合，不能从这个有限网格外推。

本批在clone外以原字节、Python3.12.14、assert开启运行一次，exit0、stderr空，stdout为`{'exact_checks': 1080, 'status': 'passed'}`。没有把child的两个hub脚本旧成功日志借给本程序。

## 固定六标签、三真实玩家及九种合法背景

`diagnose_fixed_cone.py`的M6是主题数，真实尾玩家始终3，iid比较始终4。63个变量w_t≥0对应六标签全部非空兴趣类型，Σw=1仅作齐次数值归一化。背景用合法旧行动重数a_j≥0表示，每个类型的真实旧负载是b_t=Σ_(j∈t)a_j，不能改成所有客户同一标量背景。

固定完整规则：根0；首历史a<3后选3，否则选0；深2时由第二动作所属的三标签组中选首个未在历史出现的标签。组含3题而历史长2，规则总定义。它保全部1+6+36=43个**有序**决策节点。每节点对6个当前动作重取同一规则的真实completion，共258行含自身IC，其中215个真正改动作。每行收益按类型精确构造1/(b_t+终局命中数)，最后转float交SciPy/HiGHS。

辅助4人iid分布在六题均匀；类型命中概率|t|/6，查询a的系数是1_(a∈t) E[1/(b_t+1+Bin(3,|t|/6))]。五条等式让六个纯查询同收益，因此在此满支持固定q下恰给对称Nash KKT。目标最大化λ₄−根沿规则真实收益。即使系数来自Fraction，浮点LP也不能自动给精确锥上界。

原main只列以下9个背景重数：0向量、全1、全2、全10、全100、(1,0,0,0,0,0)、(10,0,0,0,0,0)、(1,1,1,0,0,0)、(1,0,0,1,0,0)。这些是同一目录旧动作可实现的合法背景。返回字段为background、success、lambda4_minus_root和positive_types，正重数阈值1e−8。没有自动有理化、完整策略精确复核或负目标的有理对偶；源码未导出通用全背景证明。原README自报九点未命中，本批保其历史自报，不冒新进程；本源没有冻结该程序的stdout/JSON报告。

## 最大单独收益行动的四个零背景切片

`diagnose_maximum_standalone.py`仍用六标签63个非空类型、w≥0/Σw1，但**没有非零背景参数**，真实游戏只有两名玩家。默认first0、reply1，约束f(0)≥f(a)对全a、U(1,0)≥U(a,0)对全a。它只让1是0后的一个真实末BR，不给其余首动作后的回复映射或当前根最优性，故绝不是完整两人EI反例搜索。

对给定有理q，查询系数用g₃(t)=1−t+t²/3；正支持查询等值，支持外查询≤参考支持值，恰为所给静态三人q的KKT。目标最大化λ₃−U(0,1)。四个原q依次为全1/6、(0,1/5,1/5,1/5,1/5,1/5)、(1/2,1/2,0,0,0,0)、(0,1/2,1/2,0,0,0)。它们不是遍历q单纯形。

返回的weights把浮点正坐标用limit_denominator(100000)转成字符串，但**没有随后逐行有理验证**；不能因打印为分数就标为精确可行点或精确反例。原README自报四点未命中，无独立冻结输出；本批不重跑这4个LP，也不扩大扫描。

# 正确的回复周期归约，及已经失败的静态充分前提

原README的静态归约仍有正确数学内容。任取固定背景二人末位选择器R(A)∈BR_b(A)，令

\[
 P(A,B)=f_b(A)+f_b(B)-h_b(A,B),
 \quad h_b(A,B)=\sum_{x\in A\cap B}\frac1{(b_x+1)(b_x+2)}.
\]

这是同一固定背景两人势。因R(B)对B最优，P(B,R(B))≥P(B,A)=P(A,B)。有限目录的R有有向周期，沿周期非减的P必须处处相等。于是周期中A→B边的反向A也是B的最佳回复，每条边是静态PNE；同时U_b(B,R(B))=U_b(B,A)。如果所有真实强制首收益U_b(A,R(A))都小于λ₃，则周期每条静态PNE的双方也都小于λ₃。因此“每个两人静态PNE至少一侧≥λ₃”**若成立**，足够推出两人EI。这是条件归约，不是已经取得该静态前提。

该前提及更强“任意单向BR对都至少一侧≥λ₃”随后已被related原稿`two_pne_extra_iid_obstruction.md`明确反驳。本批全文核过3120B原件，保related身份，不替其owner登记完成。为看清精确范围：对整数k≥26，A/B各有2k名不交核心客户；每个核心客户另喜欢三个连续模k的周边标签，每周边另2k−9私有客户。A与B互为两人末BR，双方收益2k；每周边裸收益2k+3。周边均匀q是三人静态对称Nash，

\[
 \alpha_A=\alpha_B=2k-6+6/k,\quad
 \lambda_3=2k+1-79/(3k)+33/k^2,
\]

\[
 \lambda_3-2k=\frac{3k^2-79k+99}{3k^2}>0.
\]

令k26+h，分子为3h²+77h+73>0；λ−α_A=7−97/(3k)+33/k²>0保证支持外查询也满足KKT。k26时1222客户/28题、λ=105529/2028、双方52、差73/2028。它仅反上述两个静态辅助桥：A/B都不是最大f，周边仍可救真实根，原稿未给低于λ₃的完整两人SPE。

原README另保正确局部式：静态PNE(A,B)的经验p=(δ_A+δ_B)/2，在三个静态玩家都用p时每纯查询C满足α_C(p)≤[U_b(C,A)+U_b(C,B)]/2≤(u_A+u_B)/2。第一步由同q删一个竞争者逐客户成立，第二步用PNE两项IC。上面循环例正显示，不能把**特定p**下的cap改成另一Nash分布的共同λ₃的cap。

“先取最大f主题，再任取末BR支付λ₃”这一更窄选根规则，也已有[唯一最大主题hub旁支](../审查/圆环可信性父审的旁支合同与证据身份--审查.md#hub反的是唯一最大单独收益的选根规则)完整反驳：k12时强制唯一最大H得693<λ₃=299441/432，实际外围根818>λ₃。它不是循环PNE同一个输入，也不把旧四个固定q阴性变成阳性报告。

# 复用、证据与关系

等f引理使用固定背景两人f/h身份；本程序只给其逐客户有限实现回归。回复周期归约是正确条件工具，但两个静态充分前提已否；最大f后续hub只反选根规则；七客户银行否全r EI。四种关系都不能合成真正两人EI或六人half的反驳。

十主源及这个related原件的双冻结定位、原字节和本次三次精确原入口事件见[证据目录](../../tools/evidence/r75-extra-iid-and-signed-audits-primary/README.md)。本页只执行check_equal一次；两LP诊断原程序0新main/0新LP，未知原输出不补造。全部结论保内部知情清洗/解析核对身份，未认证外审或新颖性。
