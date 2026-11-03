# 新坐标初始化之后的直接覆盖攻击：旧桥纠正与剩余义务

2026-10-24。只研究 CAG-MODEL 任意人数、任意有限共同目录、全部有序历史纯SPE。**没有证明新的half付款不等式；Q-CAG-HALF仍OPEN。** 本页不是固定人数项目，没有新开小人数策略锥或阴性扫描。

## 1. 必须先纠正：FOMA-EXISTS不是OPEN

本轮按父指令读了同行
`R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md`
和 `round7/transport/frozen_optimal_assignment_working.md`。
其中 FOMA-EXISTS 的精确量词是：每个完整SPE实际叶Z，存在最优m元组T与排列，使冻结偏离和K(T;Z)<=W。

这已经被旧资产
[`R-a0.../static_matching/optimal_static_matching_counterexample.md`](../../../R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)
以**完全相同量词**否定，并非仅否定固定最优组合或均匀排列。52单位客户、6主题、4人完整SPE实际(3,3,2,2)，每人47/4、W47，唯一最优支持{0,1,4,5}、OPT52，全部24排列的最小冻结支付为48>47。

本分支重新写了独立定义级脚本 `audit_old_foma_counterexample.py`，不导入规范model、solver、旧审计或发现实现。它把52单位客户展开，检查全部259有序节点的1554项含自身比较，枚举全部1296有序终局和全部24最优排列，确得minK48、maxK293/6。结果在 `old_foma_counterexample_independent.json`。它只重放已知反例，不产生新游戏或新反例身份。

更早的
[`R-d22.../exchange/unique_optimum_omission_obstruction.md`](../../../R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md)
也直接否定此桥：actual(A,B)无拥挤W35，唯一最优(T,Q)各19客户且不交，二者各仅一客户与actual相交、都交于B。冻结矩阵的两列均为(37/2,19)，故K=75/2>35；该例OPT38，仍满足half。甚至对每个最优客户只收费一次的partitioned-R也至少为遗漏36>35，不能仅通过去掉最优重复库存恢复强桥。

因此不能闭合普遍FOMA-EXISTS，不能将其记为待证明的新路线。旧更弱的`K<=(1+1/m)W`不被上述反例否定，其准确旧入口是
[`R-275.../weak_matching/README.md`](../../../R-27557809587746c59216a46867c9eb07/weak_matching/README.md)。本页没有证明这个弱化。

## 2. 对新初始化的独立理解

同行INIT-2对任意比较元组保留每个比较客户一单位，得到

    |O|=sum_l(d_l+H_l)+sum_i b_i,
    0<=d_l<=u_l, 0<=H_l<=u_l.

该关系没有用“比较元组最优”，因此可以先将两份已付预算视为确定的真实付款；直接证明half仍需将真实未来注入的终端总额放进同一角色剩余R_l=2u_l-d_l-H_l。第一接收动作不含该源的actual会员，并不使整个future重采永久保留客户支撑。

我尝试绕过SAFE图，直接由最优元组交换控制这批future来源；这一步尚未成功。没有将INIT-2的守恒式或非负余额R_l误称为容量证明，也未把源库存标签当作actual同客户钱包。

## 3. 最优组合交换的直接尝试与精确停止处

固定真正最优元组T及非空索引集J，令

    D_J=O \ union_(j notin J)T_j.

任取至多|J|个合法主题的并集U，最优性给

    |U\O| <= |D_J\U|.                         (EXCHANGE)

这是旧全槽交换工具，不认领为本轮新引理；来源为
`R-ab183d14fb74403091d09db766b05f73/global2/optimal_exchange_and_multisource_error.md`。
它可以限制一批真实未来主题在O外获得的新覆盖。但初始化正future税也可以完全位于O内：某个源客户x属于T_i和真实未来动作、actual接收主题不含x，而其他比较主题仍覆盖x。此时把真实未来动作换进比较元组可以不增加覆盖，EXCHANGE不直接给这份稀释税任何正资金。

所以短推理“future捕获过载 => 某次最优覆盖交换可改善”没有证明。它需要一条额外跨真实历史IC，控制O内部重复覆盖带来的原偏离稀释，而不仅是O外新增客户。这里没有声称所有交换机制不可能；只指出本次直接接合缺失的确切量。

## 4. 保留净差，不能只付遗漏

设C为实际联合，D=|O\C|、G=|C\O|、I=|O intersect C|，则

    OPT-W=D-G.

真正half要付的是D-G<=W，而非D<=W。旧71客户例已使D36>W35但D-G=3，说明保留G是承重的。将初始化的O库存全看成遗漏需求、丢掉actual O外利润，然后要求它只用一份W支付，会再次加强为已失败义务。

当前没有证明一套可与真实future injections同时兼容的G退款分配。静态最优交换确能给总量G<=D，但这种总量比较不自动给同一context/同一whole-IC下的定向容量，不能先任意取消G个源客户再假定SAFE/CLIP与原付款不受影响。

## 5. 当前可继续的一般义务

可选择直接证明`OPT-W<=W`，或为INIT-2提供同一批future来源的共同实际容量，或证明已明确更弱的冻结指派预算。三者现在均未在本分支闭合。新增的实际结论仅是去重确认FOMA-EXISTS已FALSE并独立复核旧完整证书；这不是一般half正向突破。
