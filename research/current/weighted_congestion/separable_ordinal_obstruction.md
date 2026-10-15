# 资源可分序势的线性障碍：任意乘子与同一有限游戏

本页将任意玩家乘子障碍与同一游戏内的资源束比较接成完整证明。命题身份沿用
`WC-R1-MULTIPLIER-BARRIER v1` 与
`WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER v1`，没有扩大结论。
原独立推导仍在[乘子稿](../../questions/weighted_congestion/marginal_potentials/arbitrary_multipliers.md)
和[序势稿](../../questions/weighted_congestion/ordinal_potentials/game_specific_separable_ordinal_barrier.md)；
本页提供可直接调用的现行重构，[独立攻击](../../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)
核对其承重推理。全类匹配上界仍开放。

## 精确身份

固定整数 d≥2，定义

\[R_d(t)=\frac{(d+1)(1+t)^d+t^{d+1}}{d+(1+t)^{d+1}},\qquad
\rho_d=\sup_{t>0}R_d(t).\]

**任意乘子障碍。** 对每个实数 1≤a<ρ_d，存在有限正实权向量
w=(w_1,…,w_n)，使不存在集合函数 F:2^N→R 和正数 h_i，同时对
所有 i 与所有 S⊆N\{i} 满足

\[h_i(w(S)+w_i)^d\le\Delta_iF(S)\le a h_i(w(S)+w_i)^d.\tag{1}\]

F 与 h 可以依赖完整有限权向量，没有匿名性、连续性或统一生成规则假设。

**依游戏选择的可分序势障碍。** 对每个 1≤α<ρ_d，存在一个
MODEL 中的有限游戏，所有资源费用均为 x^d、每人策略族均为 2^E，
使对任意实集合函数 F_e:2^N→R，势 Φ(s)=Σ_e F_e(S_e(s)) 都不能在
每条严格 α 改善边上严格下降。F_e 在完整游戏确定后才任意选取。

Objects、Domain、Quantifiers、Assumptions、Definitions 与 Scope 如上；
成本与严格改善采用 [MODEL](../../weighted_congestion_frontier/MODEL.md)。
Conclusion 只是否定这两种证书，不是均衡非存在。Dependencies 是下述有限
对称化、同端点路径、黎曼和与有限取整，证明不导入外部均衡定理。
Evidence 为一般证明及所链独立攻击；有限有理核验只检查实现。
Counterevidence/Objections：该游戏有全空精确均衡；非可分势、选定改善步、
只保证极小点的依游戏目标均不在否定范围。Status 为内部完整重构与独立攻击，
外审和全球新颖性未认证；相关文件见本页末。

## 一、同端点路径强制相邻尺度乘子增长

假定 (1) 可行。将每个等权类的玩家置换，对 F 及 h 同时平均。
边际不等式保持，故可设每类乘子相同。权为 b_j 的类记 β_j=h_j/b_j。

取一个权 b 的重玩家和 K 个权 εb 的轻玩家，轻重密度比为 s>0。
分别按重末与重先顺序插入这个子集。从空集到同一端点的势增量相同，
而其成本路径和（除以 h_heavy b^d）为

\[A=(1+K\varepsilon)^d+s\varepsilon\sum_{k=1}^K(k\varepsilon)^d,
\quad B=1+s\varepsilon\sum_{k=1}^K(1+k\varepsilon)^d.\]

因此 1/a≤r_{ε,K}(s)=A/B≤a。它对 s 严格递减：写 A=u+sv、B=1+sz，
则 u>1、0<v<z，导数分子 v−uz<0。固定 t>0、K=⌊t/ε⌋，ε→0 时

\[r_{\varepsilon,K}(s)\longrightarrow
R_s(t)=\frac{(d+1)(1+t)^d+s t^{d+1}}{d+1+s((1+t)^{d+1}-1)}.\tag{2}\]

这里只取有限区间上的幂函数黎曼和；不对未知 F、h 取极限。

选 t_0 使 R_1(t_0)>a，再选 λ>1 使 R_λ(t_0)>a。
因为 t^{d+1}/((1+t)^{d+1}−1)→0，能先选小 t_1，再选 B_0>λ
使 R_{B_0}(t_1)<1/a。严格间隙与 (2) 给 δ>0，使 ε<δ 时两不等式
同时成立。递减性说明这些测试分别强制 s>λ 与 s<B_0。

选有限整数 ℓ≥1 使 λ^ℓ>B_0，选 0<q<min{δ,t_0,t_1,1}。
建立权 b_j=q^j、j=0,…,ℓ 的类，每类有
N_j=⌈max{t_0,t_1}/b_j⌉+1 名玩家。每个相邻类测试都能选够
⌊t_0/q⌋ 名轻玩家，强制 β_{j+1}/β_j>λ。
第 0 类与第 ℓ 类也能选够 ⌊t_1/q^ℓ⌋ 名轻玩家，强制 β_ℓ/β_0<B_0，
与前面连乘矛盾。玩家数虽可很大但有限，所有权严格正。这证明第一项。

## 二、先固定有限资源数，再量化任意势

给定 α<ρ_d，先选 α<R<ρ_d，并用第一项在因子 R 取一个坏权向量。
记 W=Σw_i，η=(min_i w_i/W)^d>0。任意同一玩家的两个背景费用
A=(w(S)+w_i)^d 与 B=(w(T)+w_i)^d 满足 η≤B/A≤1/η。

先固定整数 L>1/((R−α)η) 和

\[M=L+\lfloor\alpha L/\eta\rfloor+1.\tag{3}\]

游戏取这 M 个相同 x^d 资源，每人可用任意资源子集。
此时游戏已完全确定；资源数不能在看到势后增大。对任意背景取
m=⌊αLB/A⌋+1，则

\[m+L\le M,\qquad\alpha B/A<m/L<RB/A.\tag{4}\]

这也覆盖 αLB/A 为整数的情形。

若存在所述可分严格序势，平均同一游戏的全部资源置换。
置换是实际自同构，故有限平均仍严格下降，而且等于 Σ_e H(S_e)，
其中 H(U)=M^{-1}Σ_e F_e(U)。无须原 F_e 匿名。

玩家从单个资源删到空策略总是严格 α 改善，所以每个 Δ_iH(S)>0。
记 q_i(S)=Δ_iH(S)/(w(S)+w_i)^d。对任意 S,T，用互不相交的 m、L
个资源分别实现这两个背景，让玩家由前一束切到后一束。其他玩家的
策略由其是否属于 S、T 决定，交集中玩家用两束，均属于已固定的 2^E。
成本是 mA 与 LB，故 (4) 和严格序势下降给出

\[q_i(T)<(m/L)(A/B)q_i(S)<R q_i(S).\]

有限背景集的正最小值 h_i=min_S q_i(S)>0 存在，因而
h_i(w(S)+w_i)^d≤Δ_iH(S)<R h_i(w(S)+w_i)^d，
与坏权向量在因子 R 的选择矛盾。这证明第二项。

## 三、线性量级与准确否定范围

取 y=d^{2/(d+1)}、t=y−1，有
R_d(t)>(d+1)y^d/(d+d²)=d^{(d−1)/(d+1)}。
另一方面，集合函数

\[H_d(S)=\frac{w(S)^{d+1}+d\sum_{i\in S}w_i^{d+1}}{d+1}\]

的增量满足 w_i(w(S)+w_i)^d/d≤Δ_iH_d(S)≤w_i(w(S)+w_i)^d：
令 x=w(S)/w_i，将归一化增量展开为
1+Σ_{k=1}^d binom(d,k)x^k/(d+1−k)，逐系数比较即可。
于是 dH_d 提供因子 d 的夹逼；第一项对每个 a<ρ_d 的障碍迫使 ρ_d≤d。
因此 ρ_d/d→1。

第二项的全空状态是精确均衡。甚至 Σ_e|S_e(s)| 也有全空唯一极小点。
这明确区分了“所有改善边下降”和“全局选态能得到均衡”。
对一般非可分势，不能直接用聚合资源转移守恒替代真实改善环：
调度移动时，其余共享资源的共同成本会贡献 (α−1) 倍损失，
上述证明没有控制它。全类 O(d/ln d) 命题未获肯定或否定证明。

## 四、依游戏最小点选择的精确量词边界

### WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1

**Exact Statement / Conclusion。** 对每个 MODEL 有限游戏 G 及每个实 α≥1，G 存在 α-PNE，当且仅当存在依整个游戏任意选择的实集函数 F_e:2^N→R，使 Σ_eF_e(S_e(s)) 的每个全局最小点都是 α-PNE。更强地，任意指定合法状态 s* 都可成为非负资源可分目标的唯一全局最小点。

**Objects / Domain / Quantifiers / Definitions / Assumptions。** 完全采用 MODEL；令 S_e(s) 为资源 e 的用户集，△ 为对称差。F_e 可以依已选定的 s*，不要求跨游戏或限制策略后保持同一规则。有限非空状态空间是逆向的实质前提。

**证明。** 给定 s*，取 F_e(U)=|U△S_e(s*)|。双重计数给出

    Σ_eF_e(S_e(s))=Σ_i|s_i△s_i*|≥0。

零值恰好在每名玩家策略子集均等于目标时取得，故唯一最小点为 s*。若 s* 是 α-PNE 就得正向。反向由有限非空状态集上最小值存在立得。空策略、零费用、全零游戏、异质策略族及任意正实权全部覆盖；权重与费用实际未用于双重计数。

**Dependencies / Scope / Objections。** 仅有限性与策略入射表示。若企图用这个构造证明新的倍率存在界，就把所需均衡作为输入而循环论证。要求资源函数单调、由费用局部决定、可有效求出、跨游戏固定或对全部改善严格下降，都是本等价之外的额外条件。本引理只澄清旧障碍的准确否定范围。

**Evidence / Status / Related Files。** 完整直接证明，由子研究者独立提出、主研究者逐式复核；[范围审查](../../reviews/weighted_congestion/ordinal_potentials/minimizer_scope_review.md)说明 informed 旧稿核对与新引理审查的区别。[有限审计](../../../tests/audits/weighted_congestion/template_certificates/verify_template_certificates.py)穷举其输入中每个目标和状态，冻结记录见[运行结果](../../../evidence/runs/weighted_congestion/template_certificates/exact_audit.json)。Truth：所述等价已证；Value：量词边界；Novelty：未评估；Mechanism：入射 Hamming 距离；Ambition：不提供近似上界。未外审。

## 核验与继续使用

[独立审查](../../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)
记录先自行重构再阅读冻结正文的过程、所审 commit/hash、全部承重步骤和边界。
[精确核验代码](../../../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py)
检查有限路径和、取整整点与非匿名资源平均；[冻结结果](../../../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json)
不枚举巨大游戏，也不替代上述一般证明。

后续若主张次线性存在界，须说明如何超出固定玩家乘子边际夹逼或
全改善边可分序势，而不能从本障碍推导无均衡。

## 后续桥梁：真实改善环已经另行闭合

[循环窗口复制定理](cyclic_clone_improvement_cycles.md)现已用等权类循环窗口、连接guard与严格锥替代，把上述近d路径障碍实现为逐人真实改善闭环，因而对任意非可分全局全边下降势也有障碍。本页两个旧Claim身份与证明不变；新定理独立登记、审查和核验。所构游戏仍有全空精确PNE，选择改善步或全局选态的存在路线没有由此被否定。
