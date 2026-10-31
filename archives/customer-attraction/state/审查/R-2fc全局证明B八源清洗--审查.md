---
id: customer-attraction/r2fc-global-proof-b-eight-source-cleanup
kind: review
status: 已完成语义处置；八个冻结源均保留，精确有限证书与有限数值探索分列
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/harmonic_minimized_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/harmonic_obstruction_minimized.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/joint_collision_free_m3p6.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/joint_collision_free_m3p6_k1.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/joint_collision_free_probe.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/minimize_harmonic_obstruction.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/probe_promoted_family_failure.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/promoted_family_oracle_observed.json
---

# R-2fc 全局证明八源清洗：调和障碍、无拥挤有限探索与围堵族末位失败

本页处置 Boss2 已认领的八个冻结源。源路径、blob、SHA-256、字节数、clean-show 原始错误和每条证据入口均在 `archives/customer-attraction/tools/evidence/R-2fc-global-proof-b-20261031/manifest.json`。每个 `clean-show/<source-id>.stdout.txt`、`.stderr.txt`、`.status.json` 都是本轮真实命令记录。

本次在共享工作树运行了

```text
GIT_NO_LAZY_FETCH=1 python3 co-work-anl/work.py clean show <source-id>
```

八次均返回非零，错误为 `fatal: bad object 68fad804...:<path>`；正常懒取回又因 `browser-proxy:8889` 不可达而失败。因而没有把猜测内容伪装成源字节。语义阅读采用仓库中已经完整归档的相关原文和状态对象（尤其 `R-2fc-global-proof-a-20261031/related/`、`state/资源/` 和 `state/障碍/`），并将这条读取边界写入 `context-scope.md`。新复现只使用明确写出的客户表、策略和末位公式，所有结果带精确/浮点/时限范围。

## 逐源结论

| 源 ID与对象名 | 内容类型 | 可靠结论 | 不能推出的结论 | 处置 |
|---|---|---|---|---|
| `c06e10c8bc47d9ff656c` `harmonic_minimized_audit.json` | 固定策略的完整有限审计输出 | 十一客户、六主题、三人固定策略的 43 个有序决策历史、258 个含自身动作比较（215 个真正偏离）可用 `Fraction` 精确核验；实际路径 `(1,5,5)`，收益 `(3,5/2,5/2)`，`W=8`，`OPT=11`，`Phi=Psi=21/2`，188 个严格偏离，最小松弛 0 | 不是全模型最小性，不是一般半覆盖反例，不是全局调和势定理 | retained；由 `replay/harmonic_11/` 独立复现 |
| `d17fd27b86c077066c01` `harmonic_obstruction_minimized.json` | 固定策略的整数输入/压缩候选 | 记录同一十一客户策略的计数输入；可由上行 `Fraction` 审计验证其有限实例 | MILP 的最小客户数不等于全模型最小性；输入文件自身不是激励证书 | retained；有效性指向独立审计 |
| `d889a8a86821640e75b5` `joint_collision_free_m3p6.json` | 有序历史联合 MILP 有限探索 | m=3、q=6，按交集主题 k=0,1,2 的子问题和 15 秒限制，历史结果只观察到比 1 的候选 | 超时、浮点 incumbent、有限主题切片都不能证明不存在更差 SPE；没有 m=4 结论 | retained；仅有限实验 |
| `00d4e04095615c2ae506` `joint_collision_free_m3p6_k1.json` | 上述联合 MILP 的 k=1 切片输出 | 只承担该切片的观察记录和求解边界 | 不能升格为无拥挤比例下界/上界或全参数证明 | retained；仅有限实验 |
| `c69ae6a40ba4270c0cc2` `joint_collision_free_probe.py` | 联合 MILP/浮点探针代码 | 代码入口与 README 的实验合同相容，实验范围是 m3/q6、k 切片、15 秒 | 浮点探针不是精确证书；时限停止不是 infeasible；不外推到 m4 或所有策略 | retained；代码身份保留 |
| `ff2ee8e20a0b853b3e25` `minimize_harmonic_obstruction.py` | 固定策略上的 MILP 最小化/发现程序 | 可解释为什么从 78 客户浮点发现压到十一客户固定策略点 | 求解器目标值不能证明全模型最小；反例真值由逐历史 Fraction 审计而非 MILP 报告承担 | retained；候选/发现程序 |
| `4e0abf587b1b57da4145` `probe_promoted_family_failure.py` | ExactSPESolver 有限失败探针 | 历史只检查 `(t,k)=(3,1),(3,2),(4,1)` 三点；一般受限族失败由末位解析偏离证明承担 | 三点 oracle 不是一般证明；不否定其它无拥挤趋 2 构造 | retained；有限实验与障碍分开 |
| `f7fcdd25e0b844982443` `promoted_family_oracle_observed.json` | 观察输出转录 | 可作为三点有限 oracle 的历史旁证 | 原 stdout 没有冻结哈希，不能称可重放完整证书或独立运行记录 | retained；转录身份保留 |

## 精确复现一：十一客户调和势障碍

`replay/harmonic_11/audit_harmonic_11.py` 逐客户展开状态。客户类型为

[
{0}^{(2)}, {1,2}, {2,3}, {0,1,4}, {1,2,4}, {5}^{(2)}, {3,4,5}^{(3)}.
]

固定完整策略的根动作为 1；首动作不是 5 时第二位选 5，首动作为 5 时第二位选 1；末位默认选 5，唯五个无序前缀例外为 `{0,5}->4`、`{2,5}->4`、`{3,5}->1`、`{4,5}->2`、`(5,5)->1`。在全部 43 个有序决策历史上，指定动作均达到真实最大收益。实际路径是 `(1,5,5)`，负载谱为 3 个负载 1、5 个负载 2、3 个未覆盖客户，故

[
W=8,qquad mathrm{OPT}_3=11,qquad
Phi=Psi=3H_1+5H_2=rac{21}{2}<11.
]

这确实否定“完整 SPE 的调和势/截断调和势普遍支配 OPT”的加强桥；它保留一般 half 的余量 `2W=16>11`，因此不是 Q-CAG-HALF 的反例。任意纯负载函数 `F=sum_x f(c_x)` 若强加 `f(0)=0,f(1)=1` 且要求 `F>=OPT`，本例只给必要条件 `f(2)>=8/5`。

## 精确复现二：无拥挤族的有限端点

`replay/family_related/audit_collision_free_family_independent.py` 是与求解器无关的有序树审计，直接按客户负载公式和 `Fraction` 展开 k=1,2,3：

| k | 玩家 m | 主题 p | 客户 N | 实际路径 | W | OPT | OPT/W | 历史/比较数 |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 2 | 4 | 5 | (2,3) | 4 | 5 | 5/4 | 5 / 20 |
| 2 | 3 | 7 | 8 | (2,5,6) | 6 | 8 | 4/3 | 57 / 399 |
| 3 | 4 | 10 | 11 | (2,5,8,9) | 8 | 11 | 11/8 | 1111 / 11110 |

这里的有限审计支持现行任意 k 归纳构造的端点，但代码本身只逐项检查 k<=3；一般结论来自 `state/反例/三人碰撞自由族福利障碍--反例.md` 的 Q/B 状态归纳，不由有限样本外推。该族所有实际主题互不相交，收益全为 2，`W=2k+2`、`OPT=3k+2`，比例趋 `3/2`。这是一条完整有限证书/解析族，仍不是一般 half 定理。

## 精确复现三：多围堵族的末位障碍

`replay/promoted_family/verify_promoted_family_failure.py` 用有理数直接验证目标终局的末位偏离。每组有 `t` 个共享客户 `X_i`、`t-1` 个私有 `a_i`；围堵块为 `B_{i,r}=X_i∪b_r` 和 `D_r=b_r∪{d_r}`，目标实际行动为全部 `C_i=X_i` 与 `D_r`。若末位是 `C_i`，实际收益为 `t`，改选 `A_i=X_i∪a_i` 得 `2t-1`，增益 `t-1>0`。若末位是 `D_r`，改选任意 `A_i` 得 `t/2+t-1=3t/2-1`，增益 `t/2-1`；当 `t>2` 严格为正，当 `t=2` 恰为 0。于是 `t>2,k>=1` 时目标的任意排列都不是完整 SPE 终局；`t=2` 仍要求末位是 D，正好与已证无拥挤 `3/2` 族相容。

这条末位计算是完整的局部障碍，因为偏离发生在最后节点，不依赖离轨续局、平局规则或求解器。它只排除这一指定多围堵族，不能排除其它趋 2 构造。

## 全仓相关关系与当前缺口

相关全文与正文已查：

- `state/资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md` 把完整 Q/B 归纳、五客户负载障碍、十一客户调和势和三类有限扫描分开；明确无拥挤趋 `3/2` 族不等于一般上界。
- `state/资源/边际势预算与全局正矩原稿的精确证据层次--资源.md` 将十一客户有限证书与扩展模型 DR/正矩预算分离；正矩假输入不是合法 CAG 反例。
- `state/障碍/多个围堵块的目标终局末位障碍--障碍.md` 给出 `t>2` 的解析末位偏离，并保留 `t=2` 边界。
- `R-2fc-global-proof-a-20261031/related/global_proof_README.md` 明确原先有限无反例扫描的精确范围、背景候选仍需单独处理、未继续 m=4；本页没有把其历史扫描改称新运行。

当前数学结论是：十一客户例给固定调和势桥的完整有限反例；无拥挤族给比例趋 `3/2` 的完整解析族和 k<=3 的 Fraction 端点；多围堵 `t>2` 目标族因末位偏离普遍失败。一般 Q-CAG-HALF 仍未被证明或否证，无拥挤最坏比例是否超过 `3/2` 仍是开放问题；任何把 MILP timeout、浮点候选、三点 oracle 或转录 JSON 升格为全参数不存在性证据的说法均被本页拒绝。

证据目录、八源指纹、clean-show 错误、回放 stdout/stderr 和逐次 manifest 在 `archives/customer-attraction/tools/evidence/R-2fc-global-proof-b-20261031/`；八条完整处置字段列表在 `cleanup/workspaces/Boss2/receipts-R-2fc-global-proof-b-20261031.json`。
