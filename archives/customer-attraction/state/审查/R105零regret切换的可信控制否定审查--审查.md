---
id: customer-attraction/R105-zero-regret-switch-credible-controller-review-20261031
kind: review
type_tag: 审查
title: R105 零 regret 切换的可信控制否定审查
status: complete-source-read-integrated-negative-construction-boundary
truth_status: excludes the stated switch family only; Q-CAG-HALF remains open
review_level: full-clean-show-read-cross-comparison
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/switch_reachability_negative.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_counterexample_attack/switch_reachability_negative.md
source_ids:
  - eee731d3c914f91a6ef7
  - 98148ca8241baf2b121f
related_objects:
  - R105交叉分支与regret修复障碍接续审查--审查.md
  - R105全历史反族定义审计接续审查--审查.md
  - ../问题--问题.md
---

# 来源身份与结论

本轮完整读取 R-105 `new_counterexample_attack` 的 README 与 `switch_reachability_negative.md`。这是对一个“删除后零实际节点 regret、再寻找可信控制器”的构造尝试的精确否定；它不是 Q-CAG-HALF 的一般反例，也没有否定所有删除修复路线。源 README 明确停止了该攻击，没有数值搜索或新普遍范围。

| source ID | 路径 | 处置 |
|---|---|---|
| `eee731d3c914f91a6ef7` | `.../new_counterexample_attack/README.md` | integrated：停止理由与范围边界 |
| `98148ca8241baf2b121f` | `.../new_counterexample_attack/switch_reachability_negative.md` | integrated：完整代数否定 |

# 交换族和虚拟零 regret 路径

取互不相交客户块 \(F,P,H,Q\)，大小 \(f,p,h,q\)，满足 \(f,p>0\)、\(q=f+2p\)。三个主题为
\[
A=F,\qquad B=F\cup P\cup H,\qquad T=H\cup Q.
\]
候选尾部真实行动为 \((A,B,T)\)，删除第一位 A 后保留虚拟路径 \((B,T)\)。文档逐项核对原两人子博弈：在 `(A,B)`、`(A,T)`、`(A,A)` 后，末位选择 T 的收益分别严格优于或并列其他主题；原第二位选择 B 的收益为
\[
 f/2+p+h/2=(f+2p+h)/2=t/2,
\]
选择 T 也给 \(t/2\)，选择 A 仅给 \(f/2\)，所以该原两人子博弈确为完整纯 SPE。

删除 A 的负载但沿用虚拟策略时，令 \(b=f+p+h/2\)。幸存 B 玩家的实际节点偏离到 T 或 A 的收益分别为 \(t/2=b-f/2\) 和 \(f\)，均不超过 \(b\)；末位在 B 后选择 T 也是严格最佳回应。因此虚拟保留策略确有零**实际路径** regret。

# 可信控制器为何必失败

问题在于 `(B,T)` 不是删除后两人游戏的任何完整纯 SPE 路径。若根节点改选 T，末位的唯一最佳回应是 B，因为
\[
u_{last}(B\mid T)=f+p+h/2=b>t/2=u_{last}(T\mid T),
\]
且 A 只给 \(f/2\)。因此每个完整 SPE 都拒绝根节点的 B 后继，零 regret 仅是虚拟续局的局部属性。

更强地，原始控制器在 `(A,B,T)` 收益只有 \(f/2\)。若它偏离到 T，在任何可信的完整纯 SPE 续局中，后两名玩家不可能都选 T：若都选 T，末位得到 \(t/3\)，改到 B 得 \(f+p+h/3\)，严格差为 \((2f+p)/3\)。所以至多一位后继选择 T；Q 客户最终负载至多 2、H 客户至多 3，偏离控制器收益至少
\[
q/2+h/3=f/2+p+h/3>f/2.
\]
这排除了所有 off-path tie 选择，说明该控制器从来不是原始完整纯 SPE 的理性行动者。添加更早的、在不相交客户宇宙上的 bank 前缀不会改变这一严格偏离。

例如 \((f,p,h,q)=(2,1,2,4)\) 时，虚拟节点收益为 4、5，但原控制器偏离后至少得到 5；这是公式核对例，不是完整 Q-CAG 反例。

# 范围和接续

文档还指出 \(B\cup T\) 已覆盖全部目录客户，因此即使虚拟路径可实现也没有 half 缺口：\(OPT-2W<0\)。保险编译器需要的 `OPT-2W>(2j+1)\Delta` 严格不等式无法由该 primitive 提供。

本批应登记为“对一个具体 switch family 的反驳/可信性边界”。它连接已有 R105 删除盲性、零 regret 重选和全历史 regret 审查，但不升级为一般不可能性定理；第三阶段关系语义是 `反驳候选构造 -> 说明必须检查完整 off-path 可信性`。Q-CAG-HALF、一般删除修复和其他客户块切换仍保持开放。
