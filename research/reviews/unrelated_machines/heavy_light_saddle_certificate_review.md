# 重轻自洽对偶证书的独立核对

审查对象：`UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1`，正文 `research/current/unrelated_machines/heavy_light_saddle_certificate_and_cycle.md`。

## 先陈述再重构

固定阈值 `T` 和重边分界 `βT`。一个 admissible heavy placement `H` 固定被覆盖任务，剩余任务只走 light 边。残余 LP 的对偶值为 `R(H)=max_lambda g(H,lambda)`，其中被 `H` 覆盖的可选重任务必须从轻任务基线 `mu_j(lambda)` 中扣除；不能把 `g` 简化为只收费 `sum lambda_i a_i(H)`。

若 `lambda*` 是 `H` 的残余最优对偶且 `H` 最小化 `g(.,lambda*)`，则对任意 `H'` 有
`R(H')≥g(H',lambda*)≥g(H,lambda*)=R(H)`，所以 `H` 是全局最优角色。给定 `R(H)≤T` 后，ST 对 light 残余的加性损失至多 `βT`，实际负载至多 `(1+β)T`。

## 反例核对

对任意 `β∈[1/2,1)` 取 `δ=(1-β)/4`、`a=1-δ`、`b1=β+δ`、`b2=β+2δ`、`c=δ`，任务为 `A=(a,a)`、`B=(b1,b2)`、`ell=(c,∞)`，目标 `T=1`。两种 admissible placements 的残余负载分别 `(1,b2)` 与 `(b2,a)`，所以全局最优是后者且 `OPT=a<1`。前者的最优归一化对偶是 `(1,0)`，却严格偏好后者；后者的最优对偶是 `(0,1)`，却严格偏好前者。Fraction 脚本对 `β=1/2,3/4,9/10,99/100` 核对重轻分界、负载和严格二循环。

## 限制

这是纯 saddle 的充分条件与最佳响应边界，不是一般存在性或算法。可选重任务改变残余任务集时必须保留轻基线差项；若角色集合冻结为强制重任务，得到更窄但同样正确的特殊情形。反例在 `OPT≤T` 的 YES 承诺内，只否定“迭代必停/纯 saddle 必存在”，不构成主目标困难性。
