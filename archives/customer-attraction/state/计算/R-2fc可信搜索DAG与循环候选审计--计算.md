---
id: customer-attraction/r2fc-credible-search-dag-cyclic-audit
kind: computation
type_tag: 计算
title: R-2fc 可信搜索 DAG 与循环候选审计
status: ten-source-read; finite-runs-reconciled; no-universal-half-result
truth_status: exact-finite-full-history-audits-plus-timeout-diagnostics; old-incumbent-root-omission-confirmed
summary: 十个 credible_search 源已逐源实读并与共同目录完整历史模型、既有 DAG/循环引理和旧 R-18 根审查比较；保留 12 个完整有限证书、两个超时探针和一个根遗漏障碍。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/audit_dag_candidate.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/audit_old_largest_incumbent.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/cyclic_candidate_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/cyclic_construct.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/cyclic_m3p7_individual.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/cyclic_m5p7_half.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/dag_individual_probe.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/dag_restricted_half.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/extra_candidate_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/individual_candidate_audit.json
evidence_packet: ../../tools/evidence/R-2fc-credible-search-a-20261031/
related_objects:
- ../资源/可信全历史搜索与双支持校正的原稿证据--资源.md
- ../引理/循环对称目录的任意后缀均衡根扩张--引理.md
- ../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md
- ../计算/终局见证DAG的原审计与固定锥预算复核--计算.md
---

# 读取和模型边界

十源都属于 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search`。冻结 `clean show` 的十次真实调用均因 partial clone 的 promisor remote 无法连接 `browser-proxy:8889` 而退出1；随后逐一打开冻结提交的 raw 页面读取全文，并将 inventory blob、大小和 SHA-256 写入证据包 `source-manifest.json`。这一区分很重要：源文件确实读过，但本地没有可供原 DAG 入口导入的旧 `customer_attraction` 依赖，因此本轮不把缺依赖误报为新的 MILP 结果。

模型仍是有限单位客户、有限共同非空主题目录、单位权玩家依次观察全部有序历史、客户在最终覆盖者之间均分。`audit_dag_candidate.py` 明确枚举每个 `h∈[p]^{<m}` 以及每个非自身动作；它不是只检查实际路径、计数 Markov 子树或根后子树。`dag_individual_probe.py` 和 `dag_restricted_half.py` 都把浮点 DAG/MIP 当候选生成层，报告中的 `universal_claim_proved=false` 与 timeout 字段必须保留。

# 独立验证入口

标准库 `Fraction` 的 `audit_dag_candidate.py` 恢复 `integer_clones` 后计算每个类型的均分收益、终局福利和静态 OPT，并断言策略键集合恰等全部有序历史。`cyclic_candidate_audit.json`、`extra_candidate_audit.json`、`individual_candidate_audit.json` 是这一验证器的输出读数；本轮在证据包中用 `run/independent_summary_validator.py` 对 12 条记录重新计算历史数、偏离比较数、`2W-OPT` 和个体弱桥余量，exit=0、stderr 为空。

独立重核得到：全部 12 条记录 `full_history_SPE=true`、`violations=[]`、最小 slack 为 0；最大 `OPT-2W=-1`，所以这些已保存点都严格满足 half 不等式。这个结论是对 12 个已给策略和客户目录的定义级检查，不能改写成所有输入的 `OPT/W≤2` 证明。

# DAG individual 探针

`dag_individual_probe.py` 目标为固定根计数 q、目标动作 a 和比较支持 J 的 `coverage(J)-(2m-1)u_a(q)`，允许一般有序策略，不限制计数 Markov。冻结有限运行的三个候选均在 12 秒预算超时但有 incumbent，整数恢复后进入完整审计：

| m,p；根 q | a；J | 精确 `OPT/u_a` | 历史/非自身比较 | 处置 |
|---|---|---:|---:|---|
| 4,5；11110 | 0；1234 | 19/4 < 7 | 156 / 624 | 完整有限证书，低于弱桥阈值 |
| 4,5；21100 | 1；1234 | 6 < 7 | 156 / 624 | 完整有限证书，低于弱桥阈值 |
| 5,5；31100 | 1；01234 | 5 < 9 | 781 / 3124 | 完整有限证书，低于弱桥阈值 |

`individual_candidate_audit.json` 同时给出三个实际福利点：19/19、5/6 和 1/1；它们是固定输入的完整 pure SPE，不是 DAG 搜索的全局最优。

# restricted half 探针

`dag_restricted_half.py` 在真实必要行 `|T|≤m·u_a(q)`（每个根已占主题 a、每个主题 T）之外，发现阶段再施加“每个客户至多关联一个未使用根主题”的 `outside-order=1` 支持限制。m=5,p=7、J=23456、floor=1.8 的 q=3200000 和 q=2210000 两次各 25 秒均无 incumbent，模型规模均为 42345 variables/41888 binary variables。该限制改变了搜索域，timeout 既不证明受限域不可行，也不证明一般域不可行；不产生 half 障碍。

# 循环构造与两份策略

`cyclic_construct.py` 对 p=7 的 19 个循环客户轨道做 LP 投影。旧浮点 oracle 只提议一个前缀 0 的 suffix；`equivariant_policy` 再把 suffix 旋转到所有首动作分支，整数恢复后才写入完整策略。它依赖[循环对称目录的任意后缀均衡根扩张](../引理/循环对称目录的任意后缀均衡根扩张--引理.md)，但有限种子不穷尽循环类。

* m=3,p=7、seed=78123、19 steps 的 `cyclic_m3p7_individual.json` 有 14 个单位客户、57 历史、342 非自身比较、路径 `(0,5,2)`、收益 `(3,4,4)`、W=11、OPT=13，`OPT/u_0=13/3<5`。这是一个完整有限个体候选，不能反驳弱逐人桥，更不能反驳 half。
* m=5,p=7、seed=78124、19 steps 的 `cyclic_m5p7_half.json` 有 7 个单位客户、2801 历史、16806 非自身比较、路径 `(0,4,1,3,6)`、五人收益各 `7/5`、W=OPT=7。它是合法完整策略点，`OPT/W=1`，不是 half 反例。

# 旧 incumbent 的失败机制

`audit_old_largest_incumbent.py` 对 R-18 三人六主题 963 单位客户展开 43 历史/215 非自身比较。独立重核见证根规定 0 的五个正偏离：替代 1、2、3、4、5 的收益分别 303、303、357、190、303，均高于 375/2。其余 42 个后继节点可通过，但这不救根；原生成器重建约束时跳过空历史，`verified:true` 是写入字段而不是完整 SPE 调用。

因此该旧 JSON 处置为“根遗漏障碍/撤回旧完整SPE标签”，不是个体桥或 half 反例。现有《最大incumbent候选的根激励遗漏与错误认证》审查对象继续承载这一真值，本页只增加十源身份、源审计关系和新的独立重核路径。

# 结论和后续边界

本页的 exact 内容是 12 个已给定客户目录/完整策略的有限证书，以及旧候选的五根偏离。搜索层的三个 individual timeout incumbent、两个 restricted-half timeout 和 19 个循环种子都只描述有限实验。没有任何一项提供六人 `for every complete pure SPE` 的 half 上界/反例，也没有把 five-player certificate 拼接成 six-player 结论。
