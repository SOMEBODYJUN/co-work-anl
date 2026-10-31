---
id: "customer-attraction/r105-zero-regret-switch-reachability-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "R-105 零 regret 切换的原模型不可达障碍"
status: "proved-for-stated-switch-family"
truth_status: "exact analytic exclusion of the proposed controller; not a general Q-CAG-HALF counterexample"
review_level: "full-source-read-and-existing-object-comparison"
summary: "所提删除切换在保留虚拟策略上可做到实际节点零一步 regret，却无法在原单位客户共同目录完整有序历史模型中由可信控制者实现；控制者存在对任意完整后继的严格偏离。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/switch_reachability_negative.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/switch_reachability_negative.md"
evidence_manifest: "../../tools/evidence/r105-counterexample-switch-20261031/source-manifest.json"
---

## 模型与拟议切换

在有限单位客户、有限非空共同目录、完整有序历史的纯 SPE 模型中，取两两不交客户块 (F,P,H,Q)，大小分别为 (f,p,h,q)，满足 (f>0,p>0,q=f+2p)。三个主题为
(A=F)、(B=F\cup P\cup H)、(T=H\cup Q)，令 (t=h+q)。拟议末三步为 ((A,B,T))，删除第一步后保留虚拟路径 ((B,T))。

在原前缀 (A) 后，指定 (B) 为倒数第二人、(T) 为末位；在倒数第二人的替代 (A,T) 后也指定 (T) 为末位。逐项比较可验证这些末位动作是真实最佳回应，原两人子博弈可形成完整纯 SPE。删除 (A) 后，记 (b=f+p+h/2=t/2+f/2)。保留的虚拟策略上，(B) 的偏离到 (T) 或 (A) 均不提高收益，末位在 (B) 后仍严格选择 (T)，所以存活节点的单步 regret 为零。

## 原模型可达性失败

虚拟路径 ((B,T)) 不是任一完整纯 SPE 的真实有序路径。若根偏离到 (T)，末位的唯一最佳回应为 (B)，其收益 (u_{last}(B\mid T)=b)，严格超过其选择 (T) 的 (t/2) 与 (A) 的 (f/2)。因此任何完整 SPE 都必须拒绝根选 (B) 的该路径，不能把零 regret 的保留子策略当作少一人真实 SPE。

更强地，拟议原控制者在 ((A,B,T)) 中只得 (f/2)。若改选 (T)，任一可信完整后继都不能让两名追随者同时选 (T)：若两者都选 (T)，末位得 (t/3)，改选 (B) 得 (f+p+h/3>t/3)。故至多一名追随者选 (T)，每个 (Q) 客户最终负载至多二、每个 (H) 客户至多三，控制者得至少
[
q/2+h/3=f/2+p+h/3>f/2.
]
这是对任意可信后继的严格盈利偏离，排除了控制者成为原模型 SPE 行动的可能。额外加入不触及四块客户的 disjoint bank 前缀不会改变该偏离；改变块或目录交集则已离开此排除族。

例 ((f,p,h,q)=(2,1,2,4)) 给出虚拟存活收益 ((4,5)) 和零实际节点 regret，但它不是完整原模型 SPE 反例。

## 精确处置与边界

两源均为停下来的解析构造尝试，没有数值搜索或优化器。第一源说明攻击接口、严格不等式 `OPT-2W>(2j+1)Delta` 未被满足；第二源给出上述全量词严格偏离。且 (B\cup T) 已覆盖整个目录并集，故该路径没有福利半覆盖缺口，不能由保险编译器导出 Q-CAG-HALF 反例。

本障碍与[因果吸引亏空的单客户锐包络](../引理/因果吸引亏空的单客户锐包络--引理.md)、[固定插入共同池与删除后的原策略激励界](../引理/固定插入共同池与删除后的原策略激励界--引理.md)和[R105 直接覆盖前缀可达性与中继比例障碍](R105直接覆盖前缀可达性与中继比例障碍--审查.md)衔接：它们共同区分虚拟删除后的零 regret、原模型可信可达性和福利支付。此源族不否定更一般的 switch gadget，也不证明通用删除修复定理，更不解决六人 Q-CAG-HALF。
