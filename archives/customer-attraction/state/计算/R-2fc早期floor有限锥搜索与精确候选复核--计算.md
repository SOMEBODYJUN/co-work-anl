---
id: customer-attraction/r2fc-round3-search-early-floor-cones
kind: computation
type_tag: 计算
title: R-2fc round3_search 早期 floor 有限锥搜索与精确候选复核
status: finite-search-and-exact-candidate-review
truth_status: finite-exact-candidates; no-general-floor-or-half-conclusion
scope: R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search 八个脚本/JSON；m=4,p=6 与 m=5,p=7 的早期 position=0 搜索；完整有序历史候选核验
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/audit_unit_points.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/early_floor_walk.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/m4p6_pos0.best.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/m4p6_pos0.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/m4p6_pos0_multi.best.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/m4p6_pos0_multi.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/m5p7_pos0_multi.best.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf1df8ca831/round3_search/m5p7_pos0_multi.json
evidence_packet: ../../tools/evidence/R-2fc-round3-search-20261031/
related_objects:
  - ../计算/R-2fc可信搜索B十源逐源审计--计算.md
  - ../计算/R-2fc根势独立复放与截断探针--计算.md
  - ../反例/五客户无拥挤SPE负载桥障碍--反例.md
---

# 量词与算法

early_floor_walk.py 生成固定 m,p、早期位置、随机种子和起点的完整策略锥。每个锥行由实际完整策略的单步偏离不等式构成；LP 是浮点 proposal，恢复程序再产生整数单位客户和 canonical all-history certificate。脚本显式写出 absence of counterexample is not proof，并在达到 2m-1 后保留有限结果。audit_unit_points.py 不依赖搜索包，直接展开 JSON 中的单位客户、递归完整策略和所有历史偏离。

# 实际读数

m=4,p=6 的两个独立报告分别完成 35/33 和 65/54（steps/cones），最佳 floor proposal 为 7。两个 exact candidate 内容相同：路径 (2,0,0,0)，7 个单位客户，W=5,OPT=7,u=1，完整历史 259 个、非自身偏离 1295 个，最小 slack 0，(2m-1)u-OPT=0，但 2W-OPT=3。

m=5,p=7 的 multi 报告完成 65/56，最佳 floor proposal 为 9。exact candidate 路径 (2,0,0,0,0)，9 个单位客户，W=6,OPT=9,u=1，完整历史 2801 个、非自身偏离 16806 个，最小 slack 0，(2m-1)u-OPT=0，2W-OPT=3。

三个 exact candidate 的 canonical 复核全部通过，说明这些实例确实是完整历史纯 SPE，并精确达到所攻击的早期个人 floor。它们提供有限候选/工具边界，不是 OPT/u 超过 2m-1 的反例，也不证明 floor 对任意目录成立。由于搜索脚本依赖另一批 R-18e993 engines，入口运行范围保留为源码全文读取、依赖边界登记、best JSON 独立复核。

# 接续用途

可把这些候选作为后续搜索的已验证起点，或者研究支持约束下为何 floor 在早期位置取等；要升级成一般结论，必须覆盖任意共同目录、所有完整有序历史、任意平局和六人主目标量词。当前包不改变 Q-CAG-HALF 的开放状态。
