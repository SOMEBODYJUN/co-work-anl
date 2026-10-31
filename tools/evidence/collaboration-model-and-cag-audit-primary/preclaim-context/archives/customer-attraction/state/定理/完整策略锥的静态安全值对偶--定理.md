---
id: "customer-attraction/full-strategy-cone-security-duality"
kind: "theorem"
type_tag: "定理"
title: "完整策略客户锥与不受限静态安全值的精确对偶接口"
status: "complete"
truth_status: "equivalence-proved-universal-certificate-existence-open"
review_level: "self-contained-minimax-and-cone-reconstruction"
scope: "固定完整有序历史形式策略与有理查询分布；全部非负客户质量；共同标签目录允许同覆盖标签"
legacy_ids:
  - "CA-SECURITY-CONE-DUAL"
summary: "固定σ与p后，全客户锥上的W≥n min_B β_B(p)w等价于一个跨全树、静态背景不限菜单的非负线性证书。普遍证书尚未构造；严格失败的有理LP见证则真正给合法完整SPE反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/security_cone_duality.md#1-固定策略混合分布及客户锥"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/security_cone_duality.md#2-精确等价定理"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/uploaded_pro_2026-10-10/global_security_source.md#三完整树不受限静态对偶的精确证书定理"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/security_cone_duality.md"
---

# 完整策略客户锥与不受限静态安全值的精确对偶接口

## 固定策略，把客户质量作为变量

固定 $m\ge1$ 个共同主题标签、$n\ge1$ 名单位玩家及定义于全部有序决策历史的形式纯策略 $\sigma$；尚不假定其在某个客户实例上满足SPE。采用[原完整历史模型](../定义/共同目录完整历史模型--定义.md)，允许同覆盖标签。非空兴趣类型 $T\subseteq[m]$ 的质量为 $w_T\ge0$；整数点即不同单位客户，有理点可清分母展开。

对决策历史 $h$，令 $z_h$ 为沿 $\sigma$ 完成的终局，$z_{ha}$ 为先选 $a$ 再沿同一 $\sigma$ 完成的终局。对当前人的已选主题定义单类型份额

$$
\rho_T(a,z)=\frac{\mathbf1_{a\in T}}{\#\{i:z_i\in T\}},
$$

零分子项为零；非零分子时终局确含该玩家行动，分母为正。为每个 $h,a$ 建立真实偏离行

$$
\Gamma_{h,a;T}=\rho_T(\sigma(h),z_h)-\rho_T(a,z_{ha}).
$$

于是

$$
\mathcal K_\sigma=\{w\ge0:\Gamma_\sigma w\ge0\}
\tag{1}
$$

恰是该完整策略成为纯SPE的全部客户质量，没有删掉重复历史、独立平局或真实后继。根覆盖行为 $c_T=\mathbf1_{T\cap z_\varnothing\ne\varnothing}$，故 $W=c\cdot w$。

再固定有理查询分布 $p\in\Delta([m])$。每个合法竞争元组 $B\in[m]^{n-1}$ 定义

$$
\beta_B(p)_T=\frac{\sum_{a\in T}p_a}{1+\#\{j:B_j\in T\}}.
$$

$\beta_B(p)\cdot w$ 是不观察查询的静态竞争背景下的期望收益。竞争主题允许重复、可以任意相关；$B$ 不要求来自指定策略的任何回复菜单。

## 固定 $\sigma,p$ 的精确等价

以下两项等价：

$$
\forall w\in\mathcal K_\sigma:\quad
c\cdot w\ge n\min_B\beta_B(p)\cdot w;
\tag{A}
$$

存在 $Q\in\Delta([m]^{n-1})$、$\lambda_{h,a}\ge0$ 和客户余项 $r_T\ge0$，使逐类型恒等式

$$
\boxed{c-n\sum_BQ_B\beta_B(p)=\Gamma_\sigma^T\lambda+r.}
\tag{T}
$$

$Q,\lambda,r$ 可依赖固定的策略和查询分布，却须同时支付整个客户锥，不能在(A)中的每个 $w$ 变化后再任意换证书。$\lambda$ 可分别使用每个历史和每个偏离，不要求同节点或深度内先平均。该等价不声称所有 $\sigma,p$ 都有证书。

**(T)推出(A)。** 与任意 $w\in\mathcal K_\sigma$ 内积，右边为 $\lambda^T\Gamma w+r\cdot w\ge0$。所以
$c\cdot w\ge n\sum_BQ_B\beta_B(p)\cdot w\ge n\min_B\beta_B(p)\cdot w$。

**(A)推出(T)。** 零向量无需处理。对非零质量归一化，令

$$
K=\{w\ge0:\Gamma w\ge0,\ \sum_Tw_T=1\}.
$$

它是非空紧凸多面体：只给全兴趣类型 $[m]$ 质量一，则每个终局各玩家均分同一客户，任意形式策略的全部激励行都是零。由(A)，

$$
\max_{w\in K}\min_Q\left(n\sum_BQ_B\beta_B(p)-c\right)\cdot w\le0.
$$

两域均紧凸、表达式双线性，有限维minimax交换最大与最小，得到存在同一个 $Q$，使括号向量对全部 $w\in K$ 的内积至多零。齐次性恢复整个锥，故
$c-n\sum_BQ_B\beta_B(p)\in\mathcal K_\sigma^*$。有限多面体锥的Farkas对偶为

$$
\mathcal K_\sigma^*=\{\Gamma^T\lambda+r:\lambda,r\ge0\},
$$

即得(T)。所有系数有理；当该有限线性系统可行时可取有理 $Q,\lambda,r$。这是标准minimax与锥对偶的组合，作用是明确安全值支付接口，不是新SPE递推或规模突破。

## 与普遍聚合安全桥的关系

真正安全值为 $v_n(w)=\max_p\min_B\beta_B(p)\cdot w$。在允许同覆盖标签的当前合同下，普遍 $W\ge nv_n$ 等价于：对每个 $m,n$、每份完整形式策略 $\sigma$、每个有理 $p$，(T)存在。

正向先把整数客户实例上的桥延拓至非负有理点（清分母），再利用有理多面体中的有理点稠密性及有限最小值连续性延拓到整个 $\mathcal K_\sigma$，应用(A)与(T)等价。反向对实际整数实例和其完整SPE，有限安全值线性规划有有理最优查询 $p^*$；代入对应(T)内积即得 $W\ge nv_n$。

这个等价没有构造任意 $\sigma,p$ 的 $Q$ 和乘子，故聚合桥及普遍证书存在性均仍开放。固定策略样本成功不覆盖所有策略，固定目录大小和人数也不覆盖一般模型。

若另研究一个**额外要求所有主题覆盖两两不同**的合同，则正向只对至少有一个该类实现 $w^0\in\mathcal K_\sigma$ 的形式策略作同样普遍等价。对任何锥点 $w$，$w+\varepsilon w^0$ 仍在锥中，且 $w^0$ 的分离客户使所有标签覆盖重新不同；有理逼近、清分母、再令 $\varepsilon\downarrow0$ 即恢复(A)。若没有该 $w^0$，不能凭空假设存在。这个附加步骤保留上传原稿的不同覆盖版本，不把它加到当前允许同覆盖标签的模型中。

## 证书严格失败时提取真正反例

固定 $\sigma,p$，考虑有理线性规划

$$
\begin{array}{ll}
\text{最大化}&nt-c\cdot w,\\
\text{满足}&w\ge0,\ \Gamma w\ge0,\ \sum_Tw_T=1,\\
&t\le\beta_B(p)\cdot w\quad\forall B\in[m]^{n-1}.
\end{array}
\tag{LP}
$$

若最优值严格正，取有理可行见证，即有

$$
W=c\cdot w<n\min_B\beta_B(p)\cdot w\le nv_n(w).
$$

清共同分母后得到有限不同单位客户；所有收益和严格差距同比例缩放，而 $\Gamma w\ge0$ 已逐历史认证完整原策略为SPE。因此这是聚合桥的真正反例，不是缺少后继理性的松弛点。若采用额外不同覆盖合同且已知 $w^0$，可先加充分小的有理 $\varepsilon w^0$，由连续性保持严格差距。

反过来，若(T)不存在，则由精确等价(A)失败，存在这样的严格违反点，且有理数据可取有理见证。仅由浮点求解器报告不可行不等于已经交付反例；应提供完整有理点与全部 $\Gamma$ 行。只保留部分历史、冻结后继或任意填写不可信处罚的LP，即便产生正目标也没有此原模型保证。聚合安全桥反例还不自动是half反例，后者必须另算真实 $\operatorname{OPT}_n>2W$。

## 与已失败预算的区别和可接续用途

[全分布补偿预算](../定义/跨分支去相关与激励补偿总预算--定义.md)固定了按实际节点、查询 $p$ 推送真实竞争元组的一种 $Q$。36客户反例否定那一规则；(T)允许任意合法静态组合和全树激励，不受其失败排除。89客户负总去相关也只否定一种删去激励松弛的简化，不否定(T)。

本定理与[完整树iid平均障碍](../障碍/完整策略树平均与独立同分布福利桥--障碍.md)共用完整 $\Gamma$ 结构，但目标不同：这里是固定 $p$ 的最小静态查询收益，那里是静态Nash分布的iid覆盖及受限平均证书。不得把其非SPE分离向量移来作为本LP的可行反例。

来源 `security_cone_duality.md` 全文，源ID `108862fe1631cfd367b1`；上传原稿 `92058a98876e6ae2cb8d` §§三–四。已完整比较两者的量词和不同覆盖附加版本，并自足重构双向证明及严格失败提取。数值[独立审计资源](../计算/总安全预算的精确证书与独立审计--计算.md)只认证具体89/36策略与预算，未声称用有限证书检验这一普遍Farkas定理。原稿内部审阅记录保留，无外部同行评审或全球新颖性认证。
