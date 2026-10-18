# 固定轮 assignment Sherali--Adams 趋二间隙的独立攻击

## 审查对象

`UM-FIXED-SA-ASSIGNMENT-GAP-v1`，正文为 `research/current/unrelated_machines/fixed_sa_assignment_gap.md`。

## 先行重构

对 `m` 台机器、`m+1` 个 unit 任务和任意涉及至多 `r` 个任务的 literal 事件 `Lambda`，审查者定义 `A_Lambda` 为满足该事件的局部注入集合，并取 `y_Lambda=|A_Lambda|/(m)_{|Q|}`。若事件无注入，权重为 0；这一步避免把原调度允许的同机多任务误称为逻辑矛盾。

## 容量乘式攻击

固定一个正概率事件并条件于其中一个满足注入 `phi`。若机器 `i` 已被查询任务占据，条件负载至多 1；若空闲，则每个未查询任务以 `1/(m-q)` 概率扩展到 `i`，总负载为 `(m+1-q)/(m-q)=1+1/(m-q)`。因容量乘子只涉及 `q≤r-1` 个任务，该值不超过 `T=1+1/(m-r+1)`。负 literal 只限制满足注入的混合，不改变这个逐 `phi` 的计算。

## 结果与范围

鸽巢原理给真实 `OPT=2`，比值 `2-2/(m-r+2)` 在固定 `r`、`m→∞` 时趋 2。审查没有发现 signed-literal、`r≤m`、`r=m` 边界或位长表述的致命漏洞。命题只限制固定 literal-SA assignment/load 舍入；不适用于 configuration-LP 合取、增长层 SOS/Lasserre、跨机器联合 cuts 或直接算法。证书对固定 `r` 可用局部注入计数显式生成，但 `r` 随输入增长时不声称显式证书大小多项式。
