---
id: customer-attraction/r2fc-independent-mechanism-crosscheck
type_tag: 审查
kind: review
title: R-2fc independent_mechanism 四源的独立精确复放与量词边界
status: completed-source-level-review
truth_status: finite-exact-crosscheck; no-general-half-conclusion
scope: R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism 的四个脚本/JSON；五客户完整有序历史与 k=1,2,3 端点
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/audit_collision_free_spe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/collision_free_spe_exact_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/root_collision_free_family_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/root_collision_free_family_audit.py
evidence_packet: ../../tools/evidence/R-2fc-independent-mechanism-20261031/
related_objects:
  - ../反例/五客户无拥挤SPE负载桥障碍--反例.md
  - ../反例/三人碰撞自由族福利障碍--反例.md
---

# 实读与复放

四个源分别是五客户独立 `Fraction` 审计及其 JSON、任意 (k) 族的有限摘要及其独立有序树脚本。四次 `clean show` 均成功；脚本先 `py_compile`，再在副本中运行并写入新输出。两个生成 JSON 与冻结 JSON 逐字节相同，验证清单见 evidence `validation.json`。

# 五客户精确障碍

主题为 `{0,1,2}`, `{0,1,3}`, `{0,1}`, `{3,4}`，策略根选 2，回复 `(1,0,3,0)`。全部五个决策历史共有 20 项含自身比较，实际 `(2,3)` 的客户负载是 `(1,1,0,1,1)`，(W=4)；枚举 16 个有序终局得 (OPT_2=5)，最优见证为 `(0,3)`。实际负载只有 0/1，所以它反驳所有 `f(0)=0,f(1)=1` 的可加负载桥；`2W=8>5`，不反驳半覆盖。

# 碰撞自由族的独立端点

独立脚本对 `k=1,2,3` 展开所有有序历史与所有主题动作，并以类型负载公式和单位客户公式交叉核验：路径 `(2,3)`, `(2,5,6)`, `(2,5,8,9)`；`W=4,6,8`，`OPT=5,8,11`，比率 `5/4,4/3,11/8`。这与既有 Q/B 归纳对象一致，但脚本实际只运行三个端点；其标题中的 arbitrary-k 不足以单独证明所有 (k)。

# 可继续使用的关系与缺口

本包确认 global_proof 的有限 family replay 与 independent_mechanism 的独立实现相互一致，增强五客户障碍和 `OPT/W→3/2` 存在族的证据链。它没有产生六人或任意人数的完整 SPE 反例，也没有证明 `2W≥OPT` 的一般命题；Q-CAG-HALF 的全局量词、任意离轨历史和所有纯 SPE 仍需独立处理。空主题、重复、零客户、平局等模型边界没有因本四源而删去。
