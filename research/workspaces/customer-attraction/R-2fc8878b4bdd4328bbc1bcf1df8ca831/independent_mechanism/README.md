# 独立机制探索与代数候选审查

状态：2026-10-21；本子研究员不自行 git 或外发，由根研究者统一 checkpoint。

- `coverage_representation_independent_review.md`：独立从定义重构末层真实比较行空间、完整真实行空间、加根福利补空间，以及非负覆盖矩锥的暴露极射线。给出普遍证明和 `m=1`、`p=1`、有限类型限制、行锥/lineality、真矩锥与严格不同覆盖标签边界。不是一般半覆盖证明。
- `collision_free_spe_independent_review.md`：未读发现稿，独立重构五客户、二人、四主题完整 SPE；实际无拥挤 `W=4`、`OPT=5`，统一否定 `f(0)=0,f(1)=1` 的纯终局可加负载函数直接上界 OPT。含完整收益表与20比较合同，不是半覆盖反例。
- `audit_collision_free_spe.py`、`collision_free_spe_exact_audit.json`：显式五单位客户、标准库 `Fraction` 独立核验五历史20比较，并枚举16有序终局得到精确最优值；已实际运行全过。
- `collision_free_family_independent_review.md`：对全部 `k>=1`、`m=k+1` 无拥挤比率趋 `3/2` 族独立闭合 Q/B 加强状态归纳；详查多旧 A、fresh B 危险偏离、最终收益、完整有序历史粘合与精确 OPT。不用有限搜索证明一般族。
- 早先尝试“全部红色未覆盖客户的至多 m 覆盖都由实际蓝预算 W 支付”，已由另一会话 `R-d51d7a410c12456aa5c44e84b78708d0/independent_attack/residual_cover_family.md` 的两人族否定，立即放弃；没有把此强化当作主目标的等价形式。

候选作者 CR-1–CR-5 草稿已经读完并逐项独审，作者修订后边界异议均关闭；没有未解决致命异议。一般问题仍缺非负跨分支福利证书。
