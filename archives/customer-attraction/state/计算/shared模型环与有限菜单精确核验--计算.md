---
id: "shared-model/ring-and-finite-menu-certificates"
kind: "computation"
type_tag: "计算"
title: "shared模型环限制与有限菜单精确核验"
status: "complete-frozen-independent"
truth_status: "exact-restricted-and-exact-menu-reports"
review_level: "full-json-read-model-isolation"
scope: "shared模型的tiny与five_site冻结报告；不迁移CAG"
summary: "tiny_lazy_ring和tiny_optimal给出alpha=1的环限制核验；前者status=exact_ring_restricted、路径(0,4,3)，后者status=exact、978次查询、618个half states。sharp_lower_rational给出有限alpha=499750/309017、kappa=4。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/tiny_lazy_ring.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/tiny_optimal.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/sharp_lower_rational.json"
---
# shared模型环与有限菜单精确核验

## 三种计算对象

tiny_lazy_ring 状态为 exact_ring_restricted，ring=(4,3)，visited_path=(0,4,3)，layout=(4,3)，alpha=1；on_path common为空、loads=(39,33)、gap=6、score=1。它访问3个位置，做6次exact pair call并剪枝12个response。deviation_certificate逐项保存两个偏离者、目标设施、共同客户、概率和gap，其中有负gap；所以该报告只对声明的环限制负责。

tiny_optimal 状态为 exact，layout=(3,4)，ring=(4,3)，alpha=1，on_path score=1；报告统计45次pair oracle、618个half states、978个queries，逐项保存所有deviation certificates。其on_path raw gap为−6但score字段为1，必须保留两个字段而不能把raw gap误写成失败或把score误写成普适定理。

sharp_lower_rational 给出 finite_factor_exists=true，alpha=499750/309017，kappa=4；on_path layout=(0,4)，loads=(2000000,1236068)，并保存10条偏离witness。它是一个有限有理下界/存在性报告，默认continuation是枚举local并取首个下端，不等于全局最优延续或CAG策略。

## 证据阅读和边界

七份原JSON均按原字节保存在 evidence/shared-certificates/original；本轮没有把设施索引或客户概率改写成CAG类型。所有概率、loads、alpha和统计字段是冻结结果；未声称独立重跑外部生成器。它们适合作为shared模型的精确回归资产，或提醒第三阶段保留路径依赖和环限制；不承担Q-CAG-HALF的数学证据。
