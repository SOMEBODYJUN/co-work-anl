# independent_attack 分支交接

2026-10-25。主目标 Q-CAG-HALF 仍 OPEN；本分支没有一般 half 证明或主反例。仅维护本目录，未改 canonical、未运行 git 或网络、未再派代理。

## 已完成

- [完整额外槽逐位置菜单身份核查](mfull_insurance_scope_review.md)：独立重构零根保险族完整 SPE 及 minimax/Jensen 方向，确认一般工作稿 §8 (26?) 已被反驳。准确方向为 Mfull_i≥v_(m+1)≥δ_(m+1)，故 m5 原实际根 u1=5/4<25/18 足以分离。另直接解析得到原族 v_(m+1)=3/2−1/[3(m−1)]、Mfull_1=2−1/m−1/[3(m−1)]；m5 分别是17/12及103/60。本族根Mfull_1<2=W/m，因此不否定 Mpath 聚合候选。

## 探索与明确停止点

- 自然背景尾福利 `Σ c/(b+c)` 保持预算平衡，但没有给出不同真实孩子之间的付款；没有把这个表示升级成新定理。
- 静态最差 PNE 桥和纯遗漏总额桥分别已有规范反例，本分支在读到后停止。
- 另曾考虑通用终位时机 `v_2(b_m)≤W/m`。其确等于末位完整菜单值，但这已由最新来源 `R-d3981c0168644971803a9c3380ed687c/round5_general/construction/padded_core_last_budget_counterexample.md` 的全 k 真正根 SPE 反驳：m=k+3、W=5k+23、v2(b)=6，所以 m v2−W=k−5>0 对k≥6。更弱预算 `m v2≤W+u_m/2` 也在k≥12失败。原族覆盖所有客户，绝非half反例。此已知来源优先于下面有限检查，终位时机不列开放候选。

## 一次已过时的有限检查

[terminal_extra_security_probe.json](terminal_extra_security_probe.json) 是在收到上述新 LAST 来源前已启动并已结束的16份旧规范证书检查；用已有共同时间脚本的 loader/oracle，查询向量由数值LP提出、每个psi用Fraction重算。没有正分离只说明这16个旧证书没撞到反族，不是一般结果，也不改变全 k 解析反例。未扩样、未继续计算、未将此检查作为证明。

## 下一步

(26?) 的共享身份修正由 root 汇总执行。保留 (27?) Mpath 聚合及其通用时间等价式原 OPEN 状态。本分支可等待新的成熟全输入候选并独立攻击其量词、返还、同池重计和真实后继可信性。

## 后续盲独审：任意删位保险上漂

[root_deletion_insurance_drift_review.md](root_deletion_insurance_drift_review.md) 已完成内部解析审查，通过 `../induction/root_deletion_insurance_drift.md` 的准确合同。先盲推全历史fresh坐标归纳，再读稿核对：m≥3、删整位提供者行动、同目录新零根n=m−1人游戏每份SPE福利3m−3；旧独占数(0,2,…,2,1)，任意修复上漂d_i=m−3+e_i，无法由绝对常数乘删除者利润或主题大小支付。审查另核n=1边界、未来不碰旧坐标的非循环归纳、slack恒等式及既有Cartesian/别名/人口删除/真实上漂来源范围。没有数值扫描，没有新half结论。
