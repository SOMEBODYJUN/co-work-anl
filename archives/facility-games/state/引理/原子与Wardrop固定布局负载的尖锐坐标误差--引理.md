---
id: "facility-games/atomic-wardrop-fixed-layout-sharp-coordinate-error"
kind: "lemma"
type_tag: "引理"
title: "原子与Wardrop固定布局负载的尖锐坐标误差"
status: "proved-arbitrary-facility-count; exact-sharp-family"
legacy_ids: ["LOCAL-ATOM-WARDROP-k"]
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/local_and_exact/atomic_wardrop_gap.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/local_and_exact/atomic_wardrop_gap.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/local_and_exact/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/local_and_exact/README.md"]
---

# 原子与Wardrop固定布局负载的尖锐坐标误差

## 任意布局、任意原子NE与任意Wardrop对照

固定K≥2个标签设施，有限正权客户，每人按该布局的可达设施集强制服役，无覆盖者不服务；客户独立混合、最小化所选设施包含自身的实际总负载。x_f取**任意**精确原子NE期望负载，ℓ_f取把每名客户权重可分后的**任意**同布局Wardrop负载。θ是该布局可达至少两家设施客户的最大单体重，不存在取0。则
\[
\max_f|x_f-\ell_f|\le (K-1)\theta/2.
\]
目录可异构、布局可同址、允许空负载；这是每个固定布局的加性误差，未给选址SPE倍数。正实权也成立。

## 运输耦合证明

原子概率p_if、对照质量比例q_if（不可达皆0），令T_fg=Σ_i w_i p_if q_ig≥0。行和x、列和ℓ，d_f=x_f−ℓ_f为净流出，Σd=0。若f≠g且T_fg>0，有i同时p_if>0,q_ig>0，原子条件NE和Wardrop支持分别给
\[
x_f+w_i(1-p_{if})\le x_g+w_i(1-p_{ig}),
\qquad\ell_g\le\ell_f.
\]
故d_f−d_g≤w_i(p_if−p_ig)≤θ。

把d降序为d_1≥…≥d_K。若邻隙d_j−d_(j+1)>θ，前j点不能向后缀输正流，故前缀净流出Σ_(f≤j)d_f≤0、后缀和≥0；这与前缀每个d都严格高于后缀矛盾。于是每邻隙≤θ，由d_j≥d_1−(j−1)θ与零和得d_1≤(K−1)θ/2，反向同得d_K≥−(K−1)θ/2。没有把原子拆成Wardrop流来求原子最佳反应，两组只用于比较。

## 每个K的等号链

M=K(K−1)/2。每条相邻设施边{i,i+1}上放M名单位客户，仅可达这两家。边i令a_i=M−i(i−1)/2名选左、其余右（i1..K−1，整数0<a_i≤M）。纯负载x_i=M−i+1，相邻差1；高侧移低侧恰平局，低侧移高侧更差，故精确纯NE。

可拆分边i给左质量M(1−i/K)，各设施得到共同L=(K−1)²/2，为Wardrop均衡。两端偏差恰(K−1)/2且θ1，常数尖锐。K3另只需三名单位客户：两人可达12且都选1，一人可达23选2，x=(2,1,0)，对照(1,1,1)。但此例也存在原子纯NE(1,1,1)，所以不反驳“选择好续局”的设施存在性。

## 与两设施粒度界的真实差别

K2给任意NE误差≤θ/2，不能不改常数搬到一般K。另一个[共同目录粒度原稿](../../tools/evidence/local-exact/related/research/current/shared/atomic_granularity.md)把θ只计**不同物理站点**共有的最大原子，并在所有同址布局主动选独立半分。这是选择规则的θ，不是本文同址任意NE的θ；一站单重w客户的纯NE偏差w/2而不同站交叠可为0，不能混用。

该两设施比较稿另自足重建Wardrop选址字典序势，并给R=max reach、θ<R时(R+θ)/(R−θ)保证；这不来自把本文K线性误差除以零负载。其原子NO实例宏粒度约束也不是一般复杂度下界。本批仅旁读不额外done该依赖。

原稿引用Cominetti等arXiv2001.02797作为大原子/Wardrop背景；本批open未取得内容，未逐定理核新意。这里保自足运输证明与尖锐构造，未声称首次发表、外审或新运行验证。
