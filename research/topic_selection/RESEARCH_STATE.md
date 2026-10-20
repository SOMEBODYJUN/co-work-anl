# 重新选题：当前实际前沿

更新时间：2026-10-20；boss37。研究分支 `research/or-topic-battle-20261020`，公屏 `topics/or-optimization-board`，save `or-optimization-selection`。从已有分支恢复，没有创建新远端分支。旧UM-TARGET-v1及其否定均仍OPEN，退出默认主攻。

## 已经可以恢复的实物

[45张统一候选卡](candidate_pool.json)包含原子14、公平16、GAP15，A/B/C已统一；第一轮稿内部优先级字母不能当来源。[实际交叉比较](BATTLE.md)记录类型缩放击穿37/33、固定权重curl被旧文覆盖、平分多重边反例、配置次模通用覆盖等判断变化。原文机制链见[原子](lanes/atomic.md)、[公平](lanes/fair.md)、[GAP](lanes/gap.md)，各含论文定性、工具、玩具模型、精确位置和致死异议。[配置归约边界](notes/configuration_reduction_boundary.md)是已知工具重构，不是新算法。

## 当前实际数学证据

原子：有限人口37/33边际证书经过Fraction核验，但第二轮已推得全人数64/59证明草案，原常数不再有新最好界叙事。需核新颖性、类型缩放范围和算法步数。HKM2011 Prop.3.4直接覆盖固定{1,3}的curl充分性，单q递推通解降级。

公平：FA01多重图EF定向重边FPT仍为作者明确原题；普通内部平行边全平分已有反例。第二轮给树支撑残差阈值DP、简单图minimum-charity的3^k算法草案，待boss独立核查与查新。FA03仙人掌极大均衡部分着色和FA11两大小预算chores仍未闭合。三值chores的142个非空真删除子实例皆有EFX，只说明固定例删除极小，复用[原正文](notes/chores_trivalued_exact_boundary.md)。

GAP：等openingcost配置覆盖被CCPV2011直接包含，GS-Poisson2026已有快plainSAP。向量容量三列精确反例是方法边界；整数正类需先排拟阵秩直接覆盖。两大小相关间隙与非均匀预算支持舍入正在独立攻击，不能把未搜到当仍公开的证明。

## 真实团队和接续

环境总并发4（含boss），本轮两批共六名gpt-6.1-sol ultra，均完整注入用户指导。第一轮reselect_atomic/reselect_fair/reselect_gap已经结束并交稿；第二轮battle_atomic_nash/battle_fair_parameter/battle_gap_tools正在交付推导、查重及补充题卡。历史其他six-running文字不表示本轮状态。

接续先读候选池和BATTLE，检查会改变判断的具体异议；不要重扫旧UM全部档案。探索稿可直接保存，成熟一般定理再做独立攻击和长期Claim登记。

## 保留的旧资产

[等长theta图相关间隙](notes/combinatorial_equal_theta_correlation.md)仍是证明候选，新颖性未确认；[公平—fPO边界](notes/fair_fpo_compatibility_boundary.md)仍是已知反例复现；[随机鲁棒卡](lanes/robust.md)保留但不占当前四方向前排。它们不因重新选题被删除或升级。

## 保存合同

用本分支work.py checkpoint；只有status=pushed才报远端保存。结构检查验证路由、文件和字段，不认证新颖性或定理。远端commit以checkpoint回执和Git历史为准，不预填尚未发生的提交。
