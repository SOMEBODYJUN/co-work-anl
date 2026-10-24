# round6 relay：全 fresh 归一化与全局费用

2026-10-24。只攻一般 Q-CAG-HALF：任意m、任意有限共同目录、全部有序历史纯SPE。仍OPEN。不git、不覆盖round4/5，由root统一checkpoint。

已恢复round5全fresh sub-Markov、密度对角账、自然重分配与TOTAL-TRIM。dynamic/WORKING.md仅§1–5，parent确认原指令§6–7应指rank密度稿。

- `fresh_profit_normalization.md`：分母改为off-history fresh利润，不重采C。全部fresh正广播仍在严格角色DAG闭合；signed账不再有正X(C)跨叶迁移，仅余actual整行、同query的C返还、fresh负项与完整actual IC slack。credible收到精确陈述后独立重构通过。β可更大，没有总费用改善或half结论。
- `audit_fresh_profit_normalization.py` / `fresh_profit_normalization_audit.json`：定义级Fraction核1364个局部恒等式、18724个子集界、8184个SAFE返还，另有一条正fresh边的两级计数DAG。不是新游戏或SPE证书，不核一般cap。
- `global_role_coupon_hitting.md`：把PRICE提升为全context终端actual角色cut。k-role集合K外source最终落K的净券质量<=k/(k+1)，允许跨客户重采及past终点；合法R/all-O INIT也纳入同一证明。root、credible分别收到陈述后独立重构通过。多源A(K)<=M(K)+k/(k+1)M(Kc)，没有把M替成实际钱包u。
- `audit_global_role_coupon_hitting.py` / `global_role_coupon_hitting_audit.json`：同一九context混合DAG，含past券、future分支/合并和同角色不同context；精确核144个全图集合界、2187个角色价格界及64个多源cut。只核定义，不扫描SPE、不认证half。
- `review_role_price_envelope.md`：独立核root的局部uniform-subset凸包与HIT价格层积分。完整价格稿以 `../parent/role_price_envelope.md` 为准，不另算重复价格关系；lambda恒1只得M<=M。

credible `../credible/safe_coupon_netting.md` §5已独立核fresh分母，§3–4剪枝可作用nu_F，本分支不复制其稿。仅fresh核无past实际券，SAFE后仅剩同角色多个context净整行券可能重复。

继续承重：新HIT/价格包络控制比较源向actual角色分散，未把来源库存M约束为actual钱包u；ell>=0尚未实质接入该共同预算。必须取得同actual角色的多来源净券cap、actual客户券界或更弱真正全局覆盖界。不会把换分母/全图反集中本身当作总费用已付。
