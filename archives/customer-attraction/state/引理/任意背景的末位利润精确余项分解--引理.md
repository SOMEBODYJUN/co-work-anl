---
id: "customer-attraction/terminal-profit-remainder-general-background"
kind: "lemma"
type_tag: "引理"
title: "任意背景的末位利润精确余项分解"
status: "proved-exact-algebra; early-credit-extension-open"
truth_status: "exact identity and nonnegative remainder; no general q-cag-half"
review_level: "full-source-read-symbolic-reconstruction-with-finite-output-boundary"
scope: "finite common catalogue, nonnegative integer background b, r remaining players, actual terminal best response"
summary: "固定任意非负整数背景 b 与实际主题 A_1,…,A_r，只假设末位 A_r 是实际前缀后的最佳回应。对任意比较组合 T_1,…,T_r，精确有 P+(r−1)v−R_b(T)=L(T)+K+J(T)，其中 L/K/J 均非负；因此 F_r(b)−P≤(r−1)v。若末位收益是全体最小值，才可进一步替换为 (r−1)min_i u_i。一般把 v 换成 min_i u_i、或支付早期亏损的跨分支桥，仍未证。"
source_refs:
  - "clean:6bacca03ff57d72f3a8d:dynamic_credit_background_readme.md"
  - "clean:a329e42732730bc0f9d6:terminal_profit_remainder.md"
  - "clean:af18a968e70a74bbba3c:terminal_profit_remainder_exact.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/two_remaining_tax.md#6-空背景根税的末位收益诊断"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/two_remaining_tax.md"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original/terminal_profit_remainder.md"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original/terminal_profit_remainder_exact.json"
related_objects:
  - "archives/customer-attraction/state/引理/末位收益税诊断--引理.md"
  - "archives/customer-attraction/state/引理/固定背景两人税界--引理.md"
  - "archives/customer-attraction/state/引理/任意背景的末位利润精确余项分解--引理.md"
  - "archives/customer-attraction/state/计算/任意背景末位利润余项精确审计--计算.md"
  - "archives/customer-attraction/tools/evidence/dynamic-query-credit-primary/original/research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_optimal_queries/dynamic_query_credit.md"
  - "archives/customer-attraction/tools/evidence/customer-attraction-direct-cover-readme-20261031/original/README.md"
---

# 1. 对象、量词与来源范围

固定有限共同目录、单位客户和 (rge1) 名剩余玩家。客户 (x) 的固定背景负载 (b_xinmathbb Z_{ge0}) 可以来自合法前缀；代数推导本身甚至不需要验证其可实现性。实际主题依次为 (A_1,ldots,A_r)，令

[
 e_x=sum_{i<r}{f1}_{xin A_i},qquad
 l_x={f1}_{xin A_r},qquad
 P=sum_xrac{e_x+l_x}{b_x+e_x+l_x},qquad
 v=sum_{xin A_r}rac1{b_x+e_x+1}.
]

只假设末位 (A_r) 是实际前缀后的最佳回应；前 (r-1) 人的最优性不用于下述分解。对任意比较主题 (T_1,ldots,T_r)，记 (d_x=sum_j{f1}_{xin T_j})，其固定背景剩余收益为

[
 R_b(T)=sum_xrac{d_x}{b_x+d_x},qquad F_r(b)=max_T R_b(T).
]

所有零分子项取零；空主题、重复主题、零客户和 (r=1) 都在该约定下保留。

# 2. 精确 (L+K+J) 分解

定义

[
 L(T)=sum_{j=1}^rleft[v-sum_{xin T_j}rac1{b_x+e_x+1}
ight],
]

[
 K=sum_xleft[rac{e_x}{b_x+e_x+l_x}-rac{e_x}{b_x+e_x+1}
ight],qquad
 J(T)=sum_xleft[rac{d_x+e_x}{b_x+e_x+1}-rac{d_x}{b_x+d_x}
ight].
]

末位最佳回应使每个括号在 (L) 中非负，因此 (L(T)ge0)。逐客户有

[
 K_x=egin{cases}
 0,&l_x=1	ext{ 或 }e_x=0,\\[2pt]
 dfrac{e_x}{(b_x+e_x)(b_x+e_x+1)},&l_x=0, e_x>0,
 end{cases}
]

所以 (Kge0)。对 (J)，若 (b_x+d_x>0)，通分得到

[
 J_x=rac{b_xe_x+d_x(d_x-1)}{(b_x+e_x+1)(b_x+d_x)}ge0,
]

因为 (d_x) 是非负整数；若 (b_x=d_x=0)，则按零分子约定得到 (J_x=e_x/(e_x+1)ge0)。因此

[
 oxed{P+(r-1)v-R_b(T)=L(T)+K+J(T).}	ag{1}
]

证明只需展开 (L)，用 (sum_j{f1}_{xin T_j}=d_x) 消去比较主题和，再由 (K) 把 (sum_x e_x/(b_x+e_x+1)) 换成实际早期总收益，末位实际收益由 (v) 给出。没有把不同比较分支当成同一实际历史。

空背景 (b=0) 时，(J) 具体记录比较组合的重复覆盖和实际早期覆盖落在比较组合之外：

[
 J_x=rac{d_x-1}{e_x+1} (d_xge1),qquad J_x=rac{e_x}{e_x+1} (d_x=0).	ag{2}
]

# 3. 末位界和条件性最小收益替换

取达到 (F_r(b)) 的比较组合 (T^*)，由 (1) 的非负性得到

[
 oxed{F_r(b)-Ple(r-1)v.}	ag{3}
]

如果额外知道实际末位是全体实际收益中的最小者，即 (v=min_i u_i)，则

[
 F_r(b)-Ple(r-1)min_i u_ilerac{r-1}{r}P,
]

从而 (F_r(b)le(2-1/r)P)。完整 SPE 本身并不保证末位收益普遍最小；因此不能删除该条件，也不能将 (3) 改写成一般 ((r-1)min_i u_i) 界。

现有恰两人背景税引理还给出合法特例：由 (F_2(b)-Ple g_b(A_1,A_1))，以及实际两位收益各至少 (sum_{xin A_1}1/(b_x+2)ge g_b(A_1,A_1))，有

[
 F_2(b)-Plemin(u_1,u_2).	ag{4}
]

这是现有两人税界的推论，不是由本分解建立的一般人数归纳。

# 4. 真实末位过高时的未解决信用义务

令 (R^*=L(T^*)+K+J(T^*))。将 (1) 改写后，若要把 (v) 替换为全体最小收益，需要分别支付

[
 R^*ge(r-1)v-rmin_i u_i,	ag{5}
]

或更强版本

[
 R^*ge(r-1)(v-min_i u_i).	ag{6}
]

这些是不等式候选和充分支付条件，不是本页已证结果。它们要求早期真实偏离菜单提供非循环信用，不能由重新排列 (1) 自动得到。现有 dynamic-query-credit 分解中的自适应罚项 (Q_i) 和 direct-cover 的弱匹配/弱平均接口正说明了这项困难：多条强制分支互斥，尾部余项不能直接相加成同一钱包。

# 5. 69 客户标量分解和非 SPE 压力测试

来源以四人六主题既有完整 SPE 为标量例：实际路径 ((0,0,0,5))，收益 ((10,10,10,18))，(P=48)，(F_4(0)=69)。取比较组合 ((0,1,2,3))，覆盖全部 69 名客户且 (d_x=1)，则

[
 v=18,quad L=rac{51}{2},quad K=rac{15}{2},quad J=0,quad R^*=33,
]

并满足 (P+3v-F_4(0)=48+54-69=33)。JSON 只保存这个标量重算，`full_SPE_reaudit=false`；完整 SPE 合法性沿用既有独立审查，不能写成本次 JSON 已重审。

来源还给出一个非 SPE 模板：(r) 个两两不交大主题，前 (r-1) 位选私有主题，末位选大主题。比较全部大主题时 (P=KH_r)、(F_r(0)=rK)、(v=K)、(L=0)、(K=J=K(H_r-1)/2)，故 (R^*=K(H_r-1))，大 (r) 时违反 (5)。这说明仅有末位最优性和粗分母保底不能支付早期真实激励；它不是新的完整 SPE 反例。

# 6. 状态与关系

该引理是一般背景的精确末位余项/条件界。它不证明 Q-CAG-HALF，不提供一般人数动态信用桥，不产生新的完整 SPE 族，也不迁移到 unrelated-machines。后续若闭合 (5)/(6)，仍须另证所有早期真实偏离、历史平局和跨分支支付；若找不到支付，则该接口保持 OPEN。
