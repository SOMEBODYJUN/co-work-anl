# 最优主题的冻结偏离指派：已否定的加强与保留的静态公式


**第八轮状态纠正：FOMA-EXISTS 与 FOMA-ALL 均已被更早的完整 SPE 反例否定。** 上轮漏读旧资产而标 OPEN 有误。同行 seq252/256 指出来源后，root 实际读取并独立逐单位重放 [旧52客户反例](../../../R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)：W47、唯一最优支持0145、OPT52、全部24匹配最小K48。重放259有序历史/1554含自身IC与全部1296终局通过，见 [root独立证据](../../round8/parent/old_assignment_counterexample_replay.json)。原有限检查没有包含此例，冻结输出不改。下文保留历史候选及正确静态恒等式，不再把强FOMA列为承重义务。弱K≤(1+1/m)W仍未证，来源旧正文已给OPT≤K+(1−1/m)W。

2026-10-24，transport7。任意有限共同目录、任意人数、每份全部有序历史纯 SPE。**本稿没有证明新的 SPE 福利下界或共同 C 容量；Q-CAG-HALF 仍 OPEN。** 这里保存一条可绕开既有 coupon 图的准确候选，以及它的静态运输形式。计数恒等式不依赖 SPE，不能称作已使用真实后继激励。

## 1. 候选必须只量化最优组合

固定原完整 SPE，实际终局为 Z=(S_1,...,S_m)、福利 W，实际客户负载 c_x。对一个达到 OPT_m 的目录 m 元组 T=(T_1,...,T_m)，定义

    d_ij = u_i(T_j,Z_{-i}),
    K(T;Z) = min_{pi in Sym(m)} sum_i d_i,pi(i).

这里 d 冻结其余实际行动，只是静态数值，**不是原 σ 的真实偏离收益**。候选为

    存在最优 m 元组 T，使 K(T;Z) <= W。          (FOMA-EXISTS?)

更强版本要求每个最优元组 T 都满足该式，记 FOMA-ALL?。两者现已由上述旧完整反例否定；本稿初版有限审计未覆盖该输入。重复主题、空主题与任意平局不删去。

不能把“最优元组”改为“任意比较元组”：已有八客户 CCE 反例中 Z=(0,1,1)、W=6，三次重复主题 2 的冻结偏离总额固定为 7>6。这个比较组合只覆盖三客户，不是 OPT_3=8 的最优组合，故它不否定 FOMA-EXISTS 或 FOMA-ALL。

## 2. 若候选成立，怎样接到原目标

给定任意指派 pi，逐客户令 d_x 为该客户属于多少个比较槽 T_j，t_x 为同时满足 x in S_i intersect T_pi(i) 的位置数。静态定义直接给

    sum_i u_i(T_pi(i),Z_-i)
      = sum_(c_x=0) d_x
        +sum_(c_x>0) [d_x/(c_x+1)+t_x/(c_x(c_x+1))].  (COST)

设 O=union T_j。对 x in O outside C，COST 贡献 d_x>=1；对 x in O intersect C，原福利贡献已为1；其余客户非负。因此

    |O| <= W + K(T;Z).                           (SMOOTH)

所以 FOMA-EXISTS? 推出 OPT_m<=2W。它比半覆盖本身更强，不能反向默认成立。确切的额外静态余量是

    K(T;Z) - (|O|-W)
      = |C outside O| + sum_(x in O outside C)(d_x-1)
        +min_pi sum_(x in O intersect C)
             [d_x/(c_x+1)+t_x/(c_x(c_x+1))] >=0.

这条式子也说明：不能把冻结指派的额外税免费退掉之后，仍宣称证明了本候选。

## 3. 唯一可优化部分是实际交集 bonus

定义

    b(T_j) = sum_(x in T_j) 1/(c_x+1),
    H_ij = sum_(x in S_i intersect T_j) 1/[c_x(c_x+1)].

H 内 c_x>=1，所以没有零分母。逐客户展开给

    d_ij = b(T_j)+H_ij,
    K(T;Z) = sum_j b(T_j) + min_pi sum_i H_i,pi(i).  (BONUS)

因此自由排列不改变 fresh 项或 base 项；它只在实际 C 内重新匹配非负交集 bonus。最小 bonus 是标准二分完美指派的原始/对偶共同值：

    min_(p_ij>=0, sum_j p_ij=1, sum_i p_ij=1) sum_ij H_ij p_ij
      = max_(a_i+b_j<=H_ij) [sum_i a_i+sum_j b_j].   (DUAL)

双随机矩阵的置换凸包定理使分数耦合与最佳纯排列等价；a、b 为自由符号，不要求非负。该式没有购买过去角色的 IC，也没有把冻结收益冒充 prescribed completion。

均匀排列只给

    E_pi sum_i d_i,pi(i)
      = sum_(c_x=0)d_x + (m+1)/m sum_(c_x>0)d_x/(c_x+1).

它严格强于“存在好排列”，不能混用。八客户例的唯一最优主题多重集为 (1,2,3)，成本矩阵为

    (4/3, 3, 3), (2, 2, 2), (2, 2, 2).

均匀排列成本58/9>W=6，但最佳指派成本16/3<6。independent7独立给出同一量词区分。此处没有新实例；只是对同一已认证 SPE 的另一种明确一般候选作检查。

## 4. 有界、准确标级的检查

`audit_frozen_optimal_assignment.py` 仅读取既有完整证书，不生成新游戏。它逐客户重新核验全部有序历史的真实偏离 IC、枚举原实例全部 m 槽比较多重集以确定 OPT，随后对每个最优多重集求精确最小冻结指派，并重算 BONUS/COST。输入清单及完整有理输出见 `frozen_assignment_existing_audit.json`。

root另指定的旧耦合失败输入给：

| 既有输入 | W | OPT | 最优元组中的最小 K | 最优元组中的最大 K |
| --- | ---: | ---: | ---: | ---: |
| high_insertion_2cycle_348_exact | 230 | 270 | 189 | 226 |
| terminal_pushforward_34_D_lt_C_exact | 32 | 34 | 59/2 | 32 |
| aggregate_theta_failure | 34 | 36 | 86/3 | 91/3 |
| individual_security_failure | 32 | 34 | 59/2 | 32 |

因此这些已知强推送/逐人安全值失败不自动否定本候选。表中有限阴性不构成一般证据。

另一次有界浮点分离诊断保留在 `diagnose_frozen_assignment_cones.py` 和 `frozen_assignment_cone_diagnostic.json`：只在八客户CCE、十三客户CCE、prefix-balance及worst-PNE四个既有完整策略脚手架中，开放全部非空客户类型，保持全部真实 IC，并同时要求所指定最优多重集严格优于其它多重集、其所有冻结排列成本都严格大于 W。归一 W=1 后最大共同严格 margin 均报告为0；未产生正候选，未提取有理对偶，不对这些锥宣称精确上界，不继续扩策略或人数。worst-PNE的三个重复target尤其有多重集严格唯一性自身不可能的风险，故这些零margin不给它们任何反例搜索强度。这些检查只是一条一般候选的失败定向攻击。

## 5. 真正待证位置及与旧图的关系

若走本桥，承重步骤是在全部真实 SPE 约束下控制同一矩阵 H 的最优指派值：

    min_(T optimal) [sum_j b(T_j)+min_pi sum_i H_i,pi(i)] <= W。

这不是已完成的共同容量不等式。其价值仅在把需要证明的静态运输对象缩到实际交集 bonus，并明确最好排列与均匀排列、最优比较与任意比较之间的量词差别。

本稿没有将 full/fresh/CLIP 的 beta、HIT 角色概率、SOURCE 钱包或 rank 的 M-H 同这份静态指派相加。那些图的源量守恒仍不限制这里的 K；这里的静态公式也不能付它们的 actual C 券。全历史 off-IC 怎样迫使上述运输界，目前仍未获得推导。

下一步若接续，应转到不同的一般支付或明确的弱化；不得继续证明已被否定的强 FOMA。不把更多固定人数锥阴性、运输重写或角色重新命名当作一般 half 进展。

## 6. root提出的交替环接合：准确未付式

将一个最小冻结指派重标为 T_i 对应角色 i。记

    Y^i=finish_sigma(Z_<i,T_i),
    D_i=u_i(Y^i), e_i=u_i-D_i>=0,
    f_i(x)=c_Z(x)+1-1_(x in S_i), y_i(x)=c_(Y^i)(x)
        （仅对x in T_i使用，所以两分母正）。

actual-prefix 原 IC 给出同一份全部 source slack e_i。逐客户精确有

    K(T;Z)-W = sum_i [E_i-e_i],
    E_i = sum_(x in T_i) [1/f_i(x)-1/y_i(x)]
        = sum_(j>i,x in T_i)
             [1_(x in Y^i_j)-1_(x in S_j)]/[f_i(x)y_i(x)].  (GAP)

past 前缀完全相同，故差异仅在未来。GAP保留真实查询后的全部后继；它没有冻结σ的偏离收益。

另一方面，最优冻结指派只保证每个角色循环 i_1,...,i_l 有

    sum_r H_(i_r,T_(i_r)) <= sum_r H_(i_r,T_(i_(r+1))),
    i_(l+1)=i_1。                                 (CYCLE)

GAP若能由同一组CYCLE和真实off-history IC控制到 sum E_i<=sum e_i，就闭合FOMA。但本稿未证明这种控制。

需特别注意：actual-fresh客户的 H_ij 全为0，所以其比较槽对每个角色只增加同一个 base 列常数。它可以造成 GAP 中正的真实捕获税，却不直接造成任何严格冻结指派改进。因而从coupon行过载直接宣称存在负交替环，会漏掉这一层真实off-history激励。这个观察只说明上述短推理缺一条关系，不是否定交替环方法或一般目标。

root转来的global_budget7唯一首次偏离压缩同样没有被本稿当作容量：同一(k,a) reset可汇集多份 off-history整行重采密度。尚未证明它的bracket共同<=1，也未找到将bracket过载合法映成(CYCLE)违例的关系。
