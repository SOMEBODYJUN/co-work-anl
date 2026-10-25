# 实际第三位13真行投影：全类型定价合同

新必要行的来源、13个非负整数乘子和严格精确分离均属于本轮certificate的
`actual13_projection.py/json`。它来自实际第三位的同一原策略真实H,Q,R分支，
不是旧七行(P)漏用主题，也不主张多个历史之间的新兼容缺口。
本稿只证明将该行接入现有三直方图oracle时没有错分多family的max。

令G(a;h,q,r)为13行的加权逐客户和。新row系数是

    φ(a)=max_(h,q,r∈{0,1}) G(a;h,q,r).

对原真实HQR membership可以逐客户代入，φ逐客户不小于真实加权系数，
而13条原行均非负。因此Σφ≥0。max不能直接拆成三个family各自的max。

## 精确二状态分解

固定十个old主题membership、最优重数d及五个最大根membership。
把AB的mY、AE的mY、Sbranch的U/V/W计数同时置零，保留原d。
这只是系数多项式的常数项，不要求这些零计数能实现为该d的真实histogram。
定义C_h=max_(q,r) G(counts=0;h,q,r)。

对固定h，三个family的计数依赖差值Δ_AB、Δ_AE、Δ_S均不含q,r。
例如Δ_AB=2·mY[-5/(p+h+1)+2d(1/(p+h+1)−1/(p+h+2))]；
Δ_AE=−925·mY/(p+3)。Sbranch含U,V,W的二次项，但乘积均在同一family内部。
因此完整恒等式是

    φ(a)=max_(h∈{0,1}) [C_h+Δ_AB(h)+Δ_AE(h)+Δ_S(h)].

`actual13_payment_pricing.audit_decomposition()`在完整p,h,x,d、各family全部允许计数
及四个q,r状态上检验65664个差值，全部Fraction相等。
certificate另有独立Θ(p,h,d)表及144个core余项核验；父方和tree也独立重构税常数983。
所以四个q,r状态已在固定系数块里完整max化，二状态优化没有丢掉八状态中的任何一种。

## 两个h状态给出完整oracle

新row的对偶乘子μ必须非负。对每个固定old/max/d状态，严格有

    max_hist [old_score+μ·max_h(C_h+ΣΔ_family)]
      = max_h max_hist [old_score+μ(C_h+ΣΔ_family)].

固定h以后所有hist依赖仍逐family相加，三个完整histogram可各自独立最大化。
最外层保留h=0,1，原最大根保留全部32状态；所以64个旧oracle条件覆盖完整允许系数域。
这不是目录或SPE样本搜索。

## LP和定价的求值严格分开

LP添加每个类型列时始终使用φ=full max8，`Universe.proj_h=None`保证这一点。
只有oracle内部固定h的条件计算期间，`atom_rows`临时返回fixed-h max4，
使旧oracle的direct residual等式检查对应当前条件表达式。
generic driver结束两个h状态后恢复None，才把候选列加入LP。
fixed-h row本身不被当作原游戏必要行。

若某条件h产生负余项，full max8只会使实际余项更小，故仍给真负类型。
两个h的完整最大化保证没有遗漏全域最坏类型。任何浮点无负候选仍须有理恢复和真正整数/分数审计。

## 本轮结果

6751行在旧849列上重求后仍O/W≈2.00063351925>2，故没有启动β2全域oracle。
该63正支持点已交certificate恢复并做单HQR诊断。新投影严格分离6750旧点，
但新点仍actual单747行不可lift、max单可lift；因此仍无新的跨history兼容归因。
继续的强接口是显式保留同一个actual HQR三位及其全部747原行，而非把每个投影面当新机制。
