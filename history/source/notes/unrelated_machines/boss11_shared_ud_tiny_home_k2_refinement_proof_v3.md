# k² home 上界的证明修订：共享UD叶profile势

2026-10-18，boss11。对应Exact v3 SHA cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39；本文件在fresh审者只获Exact期间另冻，不作为其先行输入。原80fd Exact、409ce作者Proof、055331追加v2字节不改。

## 新域与旧证明接口

主张：k=1允许ν=maxw≤1/4096；k≥2允许ν≤1/(16384k²)。完整域的其他量词见Exact。用原作者primal smooth-deficit/profile-exchange/FW算法，不改c=5/16、θ=1/32、ξ=1/(2²⁰H²)、τ=1/(2048H)、停止阈值25/128或质量q1/10。该原算法有两条分支：得到完整实际allocation，或可靠actualV<15/16后用全jobsC2基线。一般UM未解。

旧作者Proof §1–4的实际OPT=2−V、UD匹配、vacancy matroid、共同实际benchmark、势、任意最优fractional点的stable weightedL∞/L1交换均不使用ν的具体k指数。tiny只在累计曲率及最后prefix损失出现。以下替换累计曲率的代数，其余逐处核保。

## 曲率的直接统一式

令D=Σ_i d_i、d_i=(c−W_i*)_+，λ_i=θ/k+2d_i。每outerΣw²≤ν，稳定交换给

    Σ_j B_j ≤ (2ν/λ_min²)Σ_i λ_i²,
    λ_min≥θ/k,
    Σ_i λ_i²≤θ²/k+4θD/k+4cD。

所以对任意ν均有

    Σ_j B_j ≤ 2νk+(8νk/θ+8cνk²/θ²)D。             (1)

k≥2且ν≤1/(16384k²)时，将θ1/32,c5/16代入：

    Σ_j B_j ≤ 1/(8192k)+(1/(64k)+5/32)D
            ≤1/16384+(21/128)D。                 (2)

这是旧k⁴证明在k2最坏情况下使用的同一个最终常数，不需把新的ν代进旧已粗化的1/k³式。若actualV≥ε，旧次模比较仍给ΣΔ_j≥(65/128)D−287/8192。因此D≥9/80时

    Σ_j[P(A_j)−P(A)] ≥(11/32)D−575/16384
                       ≥293/81920>0。            (3)

k=1独立用λ_min=λ_1与Σ_jw_j²≤ν，得ΣB≤2ν≤1/2048；同D阈值的剩余177/8192>293/81920。没有将k≥2 floor估计错误套k1。

## 算法、bit与全jobs的其余依赖

精确P的deficit稳定性、近似FW误差ξ、观察到的τ进展及soundFAIL证明只用(3)，所以原算法及O(kH)次替换上界原样成立。每profile固定N=ceil(4k/ξ)匹配调用；payoff原分母D1及权重2(r+1)/(t(t+1))给相同位长。新域未添加oracle、随机化或指数枚举。

新ν对全部k均≤1/4096，因此最后同一prefix/叶circulation仍仅损≤ν，实际W≥25/128−ν≥799/4096>19/100。Good helper/home mass严格大于1/10，恢复所有原selectors/incidences、inactive/zero/duplicate indexed payload仍C≤19/10。基线失败branch仍actualOPT>17/16，ratio<32/17。无叶全匹配、空叶、rank0、无fallback同原证明处理。

原k⁴域包含于新域：k1界相同；k≥2时1/(4096k⁴)≤1/(16384k²)，k2等号，k>2严格。原175行v1及其CDF算法/软件不改；k⁴+UD的未发布v2草稿仅作为本v3证明前身，不自动升级为更广已审结果。

本文件是root的新数学推导；general作者收到后另行知情重算，不计fresh审票。fresh Exact-first、实际读后与最终规范新节审核仍须分别记。Python Fraction精确核了(2)在k2取界与(3)常数；这不是端到端软件或一般证明替代。新颖性未认证。
