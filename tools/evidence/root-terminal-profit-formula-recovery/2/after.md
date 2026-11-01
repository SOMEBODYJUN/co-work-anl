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

固定有限非空共同目录、单位客户和 \(r\ge1\) 名剩余单位玩家。客户 \(x\) 的固定背景负载 \(b_x\in\mathbb Z_{\ge0}\) 可以来自合法前缀；代数推导本身甚至不需要验证其可实现性。实际主题依次为 \(A_1,\ldots,A_r\)，令
\[
e_x=\sum_{i<r}\mathbf1_{\{x\in A_i\}},\qquad
l_x=\mathbf1_{\{x\in A_r\}},\qquad
P=\sum_x\frac{e_x+l_x}{b_x+e_x+l_x},\qquad
v=\sum_{x\in A_r}\frac1{b_x+e_x+1}.
\]
只假设末位 \(A_r\) 是实际前缀后的最佳回应；前 \(r-1\) 人的最优性不用于下述分解。对任意比较主题 \(T_1,\ldots,T_r\)，记 \(d_x=\sum_j\mathbf1_{\{x\in T_j\}}\)，其固定背景剩余收益为
\[
R_b(T)=\sum_x\frac{d_x}{b_x+d_x},\qquad F_r(b)=\max_T R_b(T).
\]
所有零分子项取零；空主题、重复主题、零客户和 \(r=1\) 都在该约定下保留。此为原空背景末位证书的全背景推广与精确余项重写，不声明新颖性或一般 half 已证。

# 2. 精确 \(L+K+J\) 分解

定义
\[
L(T)=\sum_{j=1}^r\left[v-\sum_{x\in T_j}\frac1{b_x+e_x+1}\right],
\]
\[
K=\sum_x\left[\frac{e_x}{b_x+e_x+l_x}-\frac{e_x}{b_x+e_x+1}\right],\qquad
J(T)=\sum_x\left[\frac{d_x+e_x}{b_x+e_x+1}-\frac{d_x}{b_x+d_x}\right].
\]
这里也沿用零分子取零。末位最佳回应使 \(L\) 中每个括号非负，因此 \(L(T)\ge0\)。逐客户有
\[
K_x=\begin{cases}
0,&l_x=1\text{ 或 }e_x=0,\\[2pt]
\displaystyle\frac{e_x}{(b_x+e_x)(b_x+e_x+1)},&l_x=0,\ e_x>0,
\end{cases}
\]
所以 \(K\ge0\)。对 \(J\)，若 \(b_x+d_x>0\)，通分得到
\[
J_x=\frac{b_xe_x+d_x(d_x-1)}{(b_x+e_x+1)(b_x+d_x)}\ge0,
\]
因为 \(d_x\) 是非负整数；若 \(b_x=d_x=0\)，则按零分子约定得到 \(J_x=e_x/(e_x+1)\ge0\)，不能代入含零分母的上一式。因此
\[
\boxed{P+(r-1)v-R_b(T)=L(T)+K+J(T).}\tag{1}
\]
证明只需展开 \(L\)，用 \(\sum_j\mathbf1_{\{x\in T_j\}}=d_x\) 消去比较主题和，再由 \(K\) 把 \(\sum_x e_x/(b_x+e_x+1)\) 换成实际早期总收益，末位实际收益由 \(v\) 给出。没有把不同比较分支当成同一实际历史。

空背景 \(b=0\) 时，\(J\) 具体记录比较组合的重复覆盖和实际早期覆盖落在比较组合之外：
\[
J_x=\frac{d_x-1}{e_x+1}\quad(d_x\ge1),\qquad
J_x=\frac{e_x}{e_x+1}\quad(d_x=0).\tag{2}
\]

# 3. 末位界和条件性最小收益替换

取达到 \(F_r(b)\) 的比较组合 \(T^*\)，由 (1) 的非负性得到
\[
\boxed{F_r(b)-P\le(r-1)v.}\tag{3}
\]
如果额外知道实际末位是全体实际收益中的最小者，即 \(v=\min_i u_i\)，则
\[
F_r(b)-P\le(r-1)\min_i u_i\le\frac{r-1}{r}P,
\]
从而 \(F_r(b)\le(2-1/r)P\)。完整 SPE 本身并不保证末位收益普遍最小；因此不能删除该条件，也不能将 (3) 改写成一般 \((r-1)\min_i u_i\) 界。

现有恰两人背景税引理还给出合法特例：由 \(F_2(b)-P\le g_b(A_1,A_1)\)，以及
\[
u_1\ge\sum_{x\in A_1}\frac1{b_x+2}\ge g_b(A_1,A_1),\qquad
u_2\ge U_b(A_1,A_1)=\sum_{x\in A_1}\frac1{b_x+2}\ge g_b(A_1,A_1),
\]
有
\[
F_2(b)-P\le\min(u_1,u_2).\tag{4}
\]
第一条是当前与另一位最多分摊的保底；第二条是实际末位可改 \(A_1\) 的真实最佳回应。这里是现有两人税界的推论，不是由本分解建立的一般人数归纳。

# 4. 真实末位过高时的未解决信用义务

令 \(R^*=L(T^*)+K+J(T^*)\)。将 (1) 改写后，一般背景 half 恰需的余项条件为
\[
R^*\ge(r-1)v-P.\tag{HALF}
\]
这一式在冻结原稿的“真实末位过高时还缺什么”式 (5) 明写；旧派生页曾遗漏该方向，此处随逐式可读性恢复一并准确补回。若要把 \(v\) 换为全体最小收益，分别需
\[
R^*\ge(r-1)v-r\min_i u_i,\tag{5}
\]
或更强版本
\[
R^*\ge(r-1)(v-\min_i u_i).\tag{6}
\]
(HALF)/(5)/(6) 是不同的候选或充分支付条件，不是本页已证结果。它们要求早期真实偏离菜单提供非循环信用，不能由重新排列 (1) 自动得到。现有 dynamic-query-credit 分解中的自适应罚项 \(Q_i\) 和 direct-cover 的弱匹配/弱平均接口正说明了这项困难：多条强制分支互斥，尾部余项不能直接相加成同一钱包。

# 5. 69 客户标量分解和非 SPE 压力测试

来源以四人六主题既有完整 SPE 为标量例：实际路径 \((0,0,0,5)\)，收益 \((10,10,10,18)\)，\(P=48\)，\(F_4(0)=69\)。取比较组合 \((0,1,2,3)\)，覆盖全部 69 名客户且 \(d_x=1\)，则
\[
v=18,\qquad L=\frac{51}{2},\qquad K=\frac{15}{2},\qquad J=0,\qquad R^*=33,
\]
并满足 \(P+3v-F_4(0)=48+54-69=33\)。原稿还说明：主题0的30名早期客户不被末位5覆盖，故 \(K=30/4=15/2\)；比较四主题在末位前缀的收益为 \(15/2,13,13,13\)，故 \(L=72-93/2=51/2\)。强候选 (6) 在该例需 \(3(18-10)=24\)，余项33足够，仅是这个实例的标量核算。JSON 只保存此标量重算，`full_SPE_reaudit=false`；完整 SPE 合法性沿用既有独立审查，不能写成此 JSON 已重审。

来源还给出一个非 SPE 模板。为避免与上文余项 \(K\) 同名，这里将原稿的大主题大小记为 \(\kappa=\operatorname{lcm}(1,\ldots,r)\)：有 \(r\) 个不交大主题；前 \(r-1\) 位按位置选互不交私有主题，第 \(j\) 位私有客户数 \(\kappa/(r-j+1)\)，末位选大主题。其早期真实偏离严格获利，因此不是完整 SPE。对比较组合取全部大主题，有
\[
P=\kappa H_r,\qquad F_r(0)=r\kappa,\qquad v=\kappa,\qquad
L=0,\qquad K=J=\frac{\kappa(H_r-1)}2,\qquad R^*=\kappa(H_r-1).
\]
大 \(r\) 时它违反 (HALF)，说明仅有末位最优性和粗分母保底不能支付早期真实激励。它不是新的完整 SPE 反例，也不反驳 half。

# 6. 状态与关系

该引理是一般背景的精确末位余项/条件界。它不证明 Q-CAG-HALF，不提供一般人数动态信用桥，不产生新的完整 SPE 族，也不迁移到 unrelated-machines。后续若闭合 (HALF)/(5)/(6)，仍须另证所有早期真实偏离、历史平局和跨分支支付；若找不到支付，则这些接口保持未证状态。
