# CA-SECURITY-CONE-DUAL：完整策略锥与静态安全值的精确对偶接口

本页由第二份[用户上传稿](../../../history/source/notes/customer_attraction/uploaded_pro_2026-10-10/global_security_source.md)
独立重构。它是已有 [CA-STRATEGY-CONE](strategy_cone.md) 与有限minimax/Farkas的标准组合，
相对仓库新增的是安全值目标的明确接口，不是新的SPE递推、普遍支付证明或复杂度突破。
外审及全球新颖性未认证。

## 1. 固定策略、混合分布及客户锥

固定m个共同主题标签、n名单位玩家，以及全部有序决策历史上的形式纯策略sigma。
允许同覆盖不同标签；若另要求两两不同覆盖，将在§4单独处理。
非空兴趣类型T⊆[m]的客户质量为w_T≥0。整数点是不同单位客户；实数仅用于证明中的有理锥。

记z_h为从历史h沿sigma得到的完整终局，z_ha为在h先选a后沿同一sigma得到的终局。
设

\[
\rho_T(a,z)=1_{a\in T}/\#\{i:z_i\in T\},
\quad\Gamma_{h,a;T}=\rho_T(\sigma(h),z_h)-\rho_T(a,z_{ha}).
\]

零分子项为零；非零分子时z中确有该玩家行动，分母至少一。
每行都是真实节点的一次偏离，故

\[
\mathcal K_\sigma=\{w\ge0:\Gamma_\sigma w\ge0\}
\]

恰描述固定策略成为完整SPE的所有客户类型质量，完全保留历史依赖。
实际根覆盖系数为c_T=1_{T与根终局标签相交}，W=c·w。

固定有理p∈Δ([m])。对每个合法n-1竞争元组B，定义

\[
\beta_B(p)_T=\frac{\sum_{a\in T}p_a}{1+\#\{j:B_j\in T\}}.
\]

于是beta_B(p)·w是静态查询期望；竞争组合不观察所抽主题。

## 2. 精确等价定理

以下等价：

\[
\forall w\in\mathcal K_\sigma:\quad
c\cdot w\ge n\min_B\beta_B(p)\cdot w;
\tag{A}
\]

存在Q∈Δ([m]^(n-1))、lambda≥0和r≥0，使逐客户类型恒等式

\[
\boxed{c-n\sum_BQ_B\beta_B(p)=\Gamma_\sigma^T\lambda+r.}
\tag{T}
\]

Q可以使用任意合法静态竞争组合，不局限根回复菜单；lambda可以使用所有真实历史的激励。
此处“固定p”先于整个客户锥的量词，证书可以依赖sigma和p。

**T⇒A。** 对任意可行w内积，右侧非负。因此W≥n平均beta_B(p)·w≥n最小值。

**A⇒T。** 把非零锥点按sum_T w_T=1归一化，得到紧凸多面体K。
它非空：只给全兴趣类型正质量，则每个终局每人收益相同，任意形式策略都可行。
由A，`max_(w in K) min_Q (n sum Q beta-c)·w<=0`。
K与概率单纯形均紧凸，目标双线性，有限维minimax可交换max/min，
故存在同一Q使 `(c-n sum Q beta)·w>=0` 对全部K成立，再由齐次性对整个锥成立。
锥的对偶为 `{Gamma^T lambda+r:lambda>=0,r>=0}`，由Farkas得到T。
所有矩阵为有理数，因此当证书存在时可取有理Q、lambda、r。

## 3. 与普遍安全值桥的准确关系

真正安全值为 `v_n(w)=max_p min_B beta_B(p)·w`。
在允许重复覆盖标签的合同下，普遍 `W>=n v_n` 等价于：对每个m,n、每个完整sigma、
每个有理p，T都有证书。正向由普遍桥覆盖整个锥并使用§2；反向对任意实际w选择安全值
最优p后内积T。有理w的有限安全值LP具有有理最优p。

§2不构造这样的普遍证书。它把开放桥精确化为一个有限规模接口，策略数和类型数仍随m,n
急剧增加。固定策略样本的成功没有覆盖所有策略，固定m,n也没有覆盖任意目录和人数。

## 4. 两两不同覆盖标签的额外条件

若合同要求m个覆盖两两不同，则只对有一个这种合法实现w0的sigma声称普遍等价。
任意w∈K_sigma可以加epsilon w0，锥仍可行；w0中区分各主题的客户使新覆盖两两不同。
先用有理多面体中的有理点逼近，取有理epsilon>0，再清除分母展开单位客户，
最后用有限最小值的连续性令epsilon下降，恢复整个锥上的A。
不可实现的sigma不能凭空假设有w0。允许同覆盖标签时则无需该额外条件。

## 5. 证书失败怎样给真正反例

固定sigma,p，求

\[
\max (nt-c\cdot w),\quad
w\ge0,\ \Gamma w\ge0,\ \sum_Tw_T=1,
\quad t\le\beta_B(p)\cdot w\ \forall B.
\]

如果最优值正，可取有理见证，并有
`W<n min_B beta_B(p)·w<=n v_n(w)`。
清除分母得到单位客户，同时Gamma约束已逐节点认证完整原策略的SPE。
若要求不同覆盖且sigma已有w0，可加入足够小的有理epsilon w0；连续性保留严格正差距。
缺少完整Gamma行的松弛点，或者没有w0却强制要求不同覆盖，不能据此声称真正反例。

## 6. 结论状态

本等价定理成立。上传89客户实例的总去相关为负，也成立。
但上传稿的全p补偿预算GB已经由既有36客户证书否定，见
[准确边界](global_security_budget_boundaries.md)。这些证书均仍满足真正BR。
任意人数、任意目录半覆盖与普遍安全值桥继续开放。
