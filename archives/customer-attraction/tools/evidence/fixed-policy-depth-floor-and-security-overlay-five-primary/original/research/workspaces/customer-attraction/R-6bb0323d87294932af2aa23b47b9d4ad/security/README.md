# 真正聚合安全值：本轮准确边界

2026-10-24；Q-CAG-HALF 一般人数、一般有限共同目录、全部有序历史纯 SPE。
允许空主题、重复、零客户及任意离轨平局。没有找到一般证明、原命题反例，
或真正强/弱安全桥反例。没有新完成的承重继任者关系；父研究员提出的
53客户 reservation 检验现已严格否定下文正深度逐人加强。无外审或新颖性声明。
未提交、未同步；只保存本目录。

## 目标与没有采用的循环步骤

真正静态值为

\[
v_m=\max_p\min_{B\in\mathcal S^{m-1}}
 \sum_Ap_A\sum_{x\in A}\frac1{1+c_x(B)}.
\]

静态 B 不能观察 A 的抽样。希望证明
`W >= (m-1/2)v_m`，或更强 `W >= m v_m`。
逐人 `u_i>=v_m`、局部链债 `D_i>=0`、iid Z 强弱桥和 all-p 去相关均不再使用。
安全最优 p 的存在本身不允许把顺序偏离后的适应性尾部变成静态对手。

本轮重新导出的两件东西已有准确旧资产，故不算新增：

- 安全最优查询能否保留终局聚合静态无悔 SSR，见
  `../../R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/safety_preserving_static_regret.md`。
- Cartesian 真安全值可加、常数三保险 v_m=s，以及强桥 root-only
  等价式 `W+Delta>=m v_m`，见
  `../../R-4ffa8b85fa8847e09e45dcafc8e1326f/counterexample/root_insurance_security_threshold.md`。

这两项都没有闭合一般桥；本轮没有重复包装或继续以保险障碍作为主攻。

## 一项精确在研加强：按位置全历史地板

对固定完整 SPE sigma 定义

\[
L_i(\sigma)=\min_{|h|=i-1}u_i(\alpha(h,\sigma)).
\]

恒有 `W>=sum_i L_i(sigma)`。因此候选

\[
\sum_i L_i(\sigma)\ge m v_m                                      \tag{PF?}
\]

若普遍成立将给强聚合桥。但 PF? 未证明。它比单条真实路径的聚合桥更强，
其失败也不能称安全桥或 half 反例。

direct 研究员另定义 `ell_i`：同时在全部该深度历史及全部 SPE 续局上取最小。
因此 `ell_i<=L_i(sigma)`。其候选 `2 sum ell_i>=OPT_m` 与 PF? 不同；
`sum ell_i>=m v_m` 又是 PF? 的加强。两种地板没有混用。

`position_floor_check.py` 不导入均衡求解器，从保存的完整策略直接核验全部有序
历史、全部行动比较，并在有匹配保存证书时用 Fraction 核验静态安全原始/对偶。
四个精确结果如下；只是精确有限诊断，绝非一般正面证据的升级。

| 已有单位客户输入 | `sum L_i(sigma)` | 真正 `v_m` | `sum L_i-m v_m` |
| --- | ---: | ---: | ---: |
| individual_security_failure，m=3 | 63/2 | 2411/246 | 86/41 |
| root_tax_failure，m=4 | 36 | 9 | 0 |
| global_decorrelation_failure，m=4 | 85 | 508643/26546 | 110919/13273 |
| five_individual_security，m=5 | 1677/20 | 2262/139 | 6903/2780 |

完整地板向量、见证历史和比较数在 `position_floor_check.json`。
另两份输入仅有浮点安全 LP 输出，已明确标 `discovery`。

`depth_floor_security_overlay.py` 复用 direct 的19份精确 `ell_i` 数据，
只追加真正静态安全 LP；输出 `depth_floor_security_discovery.json`。
所有无负差、约0差结果都只是浮点有限筛查，既不证明 PF?，也不证明其加强。
没有继续扩大扫描。

## 被53客户完整证书否定的弱桥分解

曾考虑两个充分组成：

1. 原总人数 m 的每个正深度历史上，规定当前者收益至少 `v_m(0)`；
2. 根当前者收益至少 `v_m(0)/2`。

若两项均对全部一般输入和全部完整 SPE 成立，就有
`W>=u_1+(m-1)v_m>=(m-1/2)v_m`。
**第一项现已严格被否定。** `positive_depth_floor_counterexample.md` 给原34客户
实例加不交19客户主题 B、总人数m=4的完整 SPE。实际 `(B,0,3,4)` 的第二位
收益29/3，真正 `v_4=28481/2924`，差 `647/8772>0`。
独立标准库 Fraction 审计400个有序历史、2800行动比较和343静态有序背景。
menu研究员另从53名单独客户、原始输入和完整策略盲重构通过，
见 `../menu/reservation_blind_review.py` 与 `.json`。
该例 `W=51,OPT=53`，强聚合余量 `8800/731>0`，不反驳强/弱聚合桥或half。
第一项只在末两人时由既有同背景 theta 保底和静态背景嵌入直接得到，
更早正深度不能借此支付。第二项根半值仍未证明，单独不足以闭合。
额外一槽 ES 并不自动证明第一项：其竞争槽数相加是 m 而非 m-1，
所以只自动嵌入 `v_(m+1)(0)`，不能少算一槽。
第二项弱于已在研的 `u_1>=OPT_m/(2m)`，但本轮没有新证明。

下一项真实数学义务仍是：使用同一原策略全部真实继任者 IC，
支付安全最优查询的适应性损失；或者对 PF? / 上述分解给严格完整反例，
再准确限定被否定的加强。恒等式、静态 minimax、同叶代数及无反例扫描都没有支付这笔损失。
