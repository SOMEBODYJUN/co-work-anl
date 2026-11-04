---
id: "customer-attraction/r2fc-global-proof-eight-source-audit"
kind: computation
type_tag: "计算"
title: "R-2fc global_proof 八源的精确核查、碰撞自由障碍与有限工具边界"
status: "source-level-recovered-with-exact-replays"
truth_status: "finite-evidence-retained; no-general-half-conclusion"
review_level: "all-eight-original-sources-read-and-replayed; fixed-candidate-source-read; related-mathematical-texts-compared"
scope: "R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof 中八个已认领脚本/JSON；共同目录、单位客户、完整有序历史纯SPE；只保留固定输入、有限枚举和有限浮点探针的量词"
summary: "八个原始 global_proof 源已全文读取并归档；family、五客户障碍和恢复的 78 客户固定候选均经独立 Fraction/逐历史复放。ratio JSON/探针仍按浮点有限发现记录保留；所有精确例都满足 2W>OPT，未形成一般 half 结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_collision_free_family.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_collision_free_obstruction.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_truncated_potential.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/background_regret_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_family_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_obstruction_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_ratio_best.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_ratio_probe.py"
evidence_packet: "../../tools/evidence/R-2fc-global-proof-a-20261031/"
related_objects:
  - "../反例/三人碰撞自由族福利障碍--反例.md"
  - "../计算/背景首步反例发现与精确重放--计算.md"
  - "../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md"
  - "../资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md"
---

# 碰撞自由、调和势障碍与有限探针

八个来源脚本及结果的固定输入证据分属[初始包](../../tools/evidence/R-2fc-global-proof-a-20261031/)和[恢复包](../../tools/evidence/R-2fc-global-proof-a-recovery-20261031/)。后者的 `source-manifest.json` 与 `run-manifest.json` 绑定恢复原件、实际输入和输出；旧包的缺件字段是历史快照。以下只保留数学对象及证据合同。

## 碰撞自由完整SPE族

[完整解析构造](../反例/三人碰撞自由族福利障碍--反例.md)对每个整数 $k\ge1$ 给 $k+1$ 名提供者。互不相交客户块 $|X_i|=2$、$\{a_i\}$、$\{b\}$、$\{d\}$，共同目录为
\[
A_i=X_i\cup\{a_i\},\qquad B_i=X_i\cup\{b\},\qquad C_i=X_i,\qquad D=\{b,d\}.
\]
完整纯SPE的实际路径为 $C_1,\ldots,C_k,D$，因此
\[
W=2k+2,\qquad \operatorname{OPT}_{k+1}=3k+2,\qquad \operatorname{OPT}/W\longrightarrow3/2.
\]
构造的Q状态容许多个旧 $A_i$，B状态处理新 $B_i$ 偏离；不能把它缩成只记录一个旧A的政策。原 `audit_collision_free_family.py` 与独立实现分别对 $k=1,2,3$ 展开全部有序历史，历史/含自身比较数为 $5/20,57/399,1111/11110$，实际路径 `(2,3)`, `(2,5,6)`, `(2,5,8,9)`，$(W,\operatorname{OPT})=(4,5),(6,8),(8,11)$。有限核验是解析构造的端点证据，任意 $k$ 的量词由正式证明承担。

$k=1$ 的五客户四主题实例根选2，末位完整回复为 `(1,0,3,0)`；四个根分支均给首人收益2。全部5历史20项含自身比较（15非自身、9严格）精确成立，最小余量0。实际两个主题不交，四客户负载1、一客户未覆盖，故 $W=\Phi=\Psi=4<\operatorname{OPT}_2=5$。

因此仅依实际终局客户负载构造且满足 $f(0)=0,f(1)=1$ 的加和证书不能普遍支配OPT。整族进一步迫使任何这种普适支配证书满足 $f(1)\ge3/2$；这只是必要条件，不证明其充分性。将原参数 $t=2$ 直接升至 $t>2$ 的指定无碰撞路径，末位改 $A_i$ 得 $2t-1>t$，故该直接推广不可信。它不排除其它构造。

## 两个不同的三人调和势输入

| 固定输入 | 实际路径 | $W$ | $\operatorname{OPT}_3$ | 普通/截断调和势 |
|---|---|---:|---:|---:|
| 恢复的 `truncated_potential_candidate.json`，78客户，q6/r3，trial86/seed29395 | `(1,5,5)` | 54 | 75 | $141/2$ |
| [十一客户压缩证书](../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md) | `(1,5,5)` | 8 | 11 | $21/2$ |

78客户候选由原 `audit_truncated_potential.py` 整数化客户后，以Fraction核全部43有序决策历史、258项含自身比较，最小余量0；势与OPT之差为 $-9/2$。十一客户点的实际负载为三个1、五个2，关联证书另报告258比较、188严格。二者是不同输入，不能共享客户表或把恢复78客户输出称为十一客户重放。两者均精确否定调和/截断势支配OPT，且分别有 $2W>\operatorname{OPT}$。

## 浮点探针究竟搜索什么

`background_regret_probe.py` 以非空兴趣掩码为客户类型，固定随机前缀与完整Markov策略，对全部真实单步激励差施加LP约束，再比较终局“利润+fresh新增覆盖”和比较主题的fresh覆盖。这里固定计数政策是完整历史策略的子类；浮点可行候选仍须精确核验，并检查背景合法过去可达性。冻结合同是q6/r3、seed29393、100棵随机树、每树至多12比较主题；保存输出 `best 0.0` 只表示这些有限搜索未见负点。它不能证明全局 $P+\Delta\ge O_r$，也不反驳[背景首步失败](背景首步反例发现与精确重放--计算.md)的其它输入。

`collision_free_ratio_probe.py` 对q6/m3的500棵随机完整Markov策略施加实际终局负载至多1。保存的best JSON是trial138、浮点目标 $1.116279069767442$，未改善五客户的 $5/4$。三次入口smoke输出只证明该有限调用合同可执行，不能给全部无拥挤SPE的最坏比率上界。

以上原模型固定例都满足half。浮点未命中、恢复/读取成功、有限端点和程序运行均不产生一般人数或六人的福利结论。
