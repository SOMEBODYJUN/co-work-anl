# 重轻自洽 saddle 森林整数边界的独立审查

审查对象：`UM-HEAVY-LIGHT-FOREST-INTEGRALITY-BARRIER-v1`，正文
`research/current/unrelated_machines/heavy_light_forest_integrality_boundary.md`。

## 先陈述再重构

参数族取 `T=1`、中心任务成本 `beta`、每台机器唯一私有任务成本
`a=1−beta/m`。中心边为 light；私有边若超过 `beta` 则被唯一 heavy placement
强制，否则为唯一空 heavy placement。均匀分割中心任务给出每机负载
`a+beta/m=1`，总工作量下界和对偶值给出 `R(H)=1`。均匀价格下 `H` 因唯一而为
纯 saddle。整数中心任务必须选一台机器，故 `OPT=a+beta=1+beta−beta/m`，可趋二。

## 最小例攻击

`m=2,beta=2/3` 缩放为 `T=3` 的两机三任务树：四条有限边均为 `2`，分数负载
为 `(3,3)`，整数负载为 `4`。对任意 `lambda=(u,1−u)`，对偶目标
`g(u)=2+2min(u,1−u)≤3`，等号唯一在 `u=1/2`，所以分数值与最优对偶均已核对。
关联图五个顶点四条边，反馈秩为零；森林叶消元可可靠拒绝阈值 `3`。

## 边界与状态

该结果只否定“残余森林 + `R(H)≤T` 自动给整数补全”，不否定反馈边算法、完整
配置证书或其他共同整数信息；也不是一般 hardness。参数族和最小例的 Fraction 审计
均通过，未发现声明范围内 fatal；外部优先权和新颖性未核查。
