# 一般归纳与真实分支：本轮可接续工作

2026-10-24。研究者 `/root/general_induction`。仅研究 Q-CAG-HALF 的一般人数、一般共同目录；主目标仍 OPEN。本目录是探索备份，不作内部可靠结论提升，不修改共享文件。

## 已确认的归纳状态与断点

固定合法前缀客户整数负载 b、r 位仍活动的单位玩家，活跃利润总和为

`F_active(b;s)=sum_x c_x(s)/(b_x+c_x(s))`。

删除当前玩家并把其主题加入 b 后，后继博弈保持同类且完整 SPE 继承于该真实孩子。这个数学事实并不支付跨孩子预算：一个孩子的活跃总利润归纳界不能直接搬到另一个孩子，当前玩家的 IC 只比较自己的利润。故仅扩张到任意 b 尚未给一般 half 证明。

## 来自父方公屏的门槛候选

对任意前缀 h、尚余 r 人，令 R(h,A) 是强制当前行动 A 后全部完整纯 SPE 可实现终局。定义

`L(h,A)=min_{y in R(h,A)}u_current(y)`，`Theta(h)=max_A L(h,A)`。

完整 SPE 的实际当前利润至少 Theta。来源是已有完整续局拼合，不固定匿名平局。

本轮提出更强的 **TB-ANY** 候选：即使 z=(A_1,...,A_m) 是任意合法有序路径而不要求其为 SPE，也有

`OPT_m <= W(z) + sum_i Theta(A_1,...,A_(i-1))`。

若成立，它与真实 SPE 的逐节点 `u_i>=Theta(h_i)` 立即给原 half。**TB-ANY 未证明，也未被本轮有限搜索否定。** 它不是已建立的一般桥。

令 k 是任意主题计数前缀。完整续局集合可按 k 缓存，但不固定每个有序历史选择同一续局。TB-ANY 的准确有限 DP 为

`J(k)=Theta(k)+min_A J(k+e_A)`，`J(k)=W(k)`（终局）。

于是 TB-ANY 等价于每个输入 `J(0)>=OPT_m`。该表示保留任意路径，但没有证明该不等式，不以等价重述冒充推进。

## 一个已被现成证据否定的局部加强

曾尝试如下 Bellman 充分条件。令 `F_j(b)` 为 j 个主题在尚未被 b 覆盖客户上的最大新增覆盖。若普遍有

`Theta_r(b)>=F_r(b)-F_(r-1)(b)`，

则对任意下一动作 A，因

`F_(r-1)(b+A)>=F_(r-1)(b)-new_b(A)`，

可得 `Theta_r(b)+new_b(A)+F_(r-1)(b+A)>=F_r(b)`，随后望远镜证明 TB-ANY。

**该局部加强为假，已停止。** 父方指出的现成 `examples/customer_attraction/root_tax_failure.json` 有 `OPT_4=61`、`OPT_3=51`，规范完整续局求解器精确给 `Theta_4(0)=9`，所以 `9<61-51=10`。原文 `research/current/customer_attraction/coverage_opportunity_counterexample.md` 末尾还有更小的既有十五客户同机制失败。该失败不否定 TB-ANY，不能把局部失败当原目标反例。

## 代码、证据及复现

- `attack_arbitrary_path_threshold.py`：直接用规范 ExactSPESolver 和 Fraction 门槛，DP 最小化任意路径的 `W+sum Theta`。随机种子 20261024；本次 3250 个明确有限样本无失败。另核对 root_tax、local_security_increment、aggregate_theta_failure、individual_security_failure 四个现成实例均无失败。**没有证明含义。**
- `attack_marginal_optimum_floor.py`：只攻击已否定的裸边际 floor，含任意合法计数前缀与稀疏类型。收到现成反例后主动停止；没有把其未完成输出作正面证据。
- `attack_threshold_policy_cone.py`：下一阶段只攻击 TB-ANY 的固定策略锥充分反例。对任意完整 SPE sigma，`Theta(h)<=u_current(Z_h^sigma)`，故若客户权重 LP 找到 `coverage(T)>W(z)+sum_i u_current(Z_h_i^sigma)`，便可构成 TB-ANY 反例。固定 sigma 时所有全历史 IC 和这个上界都线性，未把非线性 Theta 塞入固定 Gamma。LP 浮点发现必须有理化并全树精确核验后方可称反例。

直接运行（仓库根）：

```sh
python3 research/workspaces/customer-attraction/R-f81c243529cf49a0a454fba6708cf80f/general_induction/attack_arbitrary_path_threshold.py
python3 research/workspaces/customer-attraction/R-f81c243529cf49a0a454fba6708cf80f/general_induction/attack_threshold_policy_cone.py
```

## 剩余义务

需要一个真实跨多步的门槛支付、适用全部 b 的显式势，或 TB-ANY 的完整精确反例。当前没有新正确的全范围福利不等式。不得从有限阴性、局部 floor 失败、DP 可计算性或同类递归推出 Q-CAG-HALF。
