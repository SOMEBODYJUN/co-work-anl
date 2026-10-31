---
id: "customer-attraction/static-insertion-true-continuation-signed-debt-ledger"
kind: "lemma"
type_tag: "引理"
title: "静态插入与真实后继的带符号债务及完整松弛账"
status: "complete"
review_level: "full-source-read-and-self-contained-mathematical-reconstruction"
summary: "保q=f+δ、R=q−真实收益及coverage/IC两松弛的精确恒等式；R预算只是half充分条件，非无条件定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/direct/static_debt_reduction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/direct/static_debt_reduction.md"
---

# 静态插入与真实后继的带符号债务及完整松弛账

## 模型和固定对象

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、m≥1名单位提供者，按全部有序历史各选一次主题；均分客户收益；空主题、重复、离轨和平局均保留。固定完整纯SPEσ的实际终局a=(A_1,…,A_m)，客户计数c_x，收益u_i，福利W=Σu_i=|∪A_i|。比较元组(T_1,…,T_m)取任意固定最优m元组，其覆盖O=OPT_m；索引可重复，不把不同元组在不同枝中重选。

定义
\[
 f_c(T)=\sum_{x\in T}{1\over c_x+1},\quad
 \delta_i(T)=\sum_{x\in T\cap A_i}{1\over c_x(c_x+1)},\quad
 V=\sum_{x:c_x>0}{1\over c_x+1}.
\]
δ只对A_i内客户求和，c_x≥1，故无0/0；不在实际覆盖中的客户在f中c_x=0，贡献1。

## 静态行是真实定义中的比较量，不是顺序激励

只在一个**辅助静态求值**中，将i改成T、其他全部实际行动保持不变，收益q_i(T)。若x∈T\A_i，其他覆盖者数为c_x，贡献1/(c_x+1)；若x∈T∩A_i，移去再加回i，贡献1/c_x。故精确
\[
 q_i(T)=f_c(T)+\delta_i(T).
\]
另令d_i(T)是在i的实际有序前缀处强制T后，沿**同一σ改变后的历史**真实完成所得当前收益。SPE只给s_i(T)=u_i−d_i(T)≥0，没有给u_i≥q_i(T)。定义有符号反制债
\[
 R_i(T)=q_i(T)-d_i(T).
\]
R可正可负，不能改成max(R,0)而仍声称保原恒等式。于是精确
\[
 f_c(T)=u_i+R_i(T)-\delta_i(T)-s_i(T)
 \le u_i+R_i(T)-\delta_i(T).
\]
同一完整策略的真回复允许反应；这里没有把冻结q冒充真实偏离d。

## 覆盖松弛、动态不等式与准确的充分条件

令e_x为客户在比较元组中的出现次数。覆盖账
\[
 E_{cov}=W-V+\sum_i f_c(T_i)-O\ge0
\]
逐客户可证：实际覆盖且比较也覆盖时系数为1−1/(c+1)+e/(c+1)≥1；只比较覆盖时贡献e≥1；只实际覆盖时贡献c/(c+1)≥0。未被任一并集覆盖者贡献0。它一般有严格松弛，不是无条件等号O=W−V+Σf。

置S_IC=Σ_i s_i(T_i)≥0。代入静态精确行得到**完整等号**
\[
 \boxed{2W-O=V+\sum_i\delta_i(T_i)-\sum_iR_i(T_i)+E_{cov}+S_{IC}.}
\]
丢掉两非负松弛才得主源所列
\[
 O\le2W-V-\sum_i\delta_i(T_i)+\sum_iR_i(T_i).
\]
因此 $\sum_iR_i(T_i)\le V+\sum_i\delta_i(T_i)$ 是half的**充分加强**，本源未证明它。对这份固定比较元组，half准确等价于 $\sum_iR_i\le V+\sum_i\delta_i+E_{cov}+S_{IC}$，不能删除两松弛后仍称等价。源标题的“exact general reduction”保的是q/d/R精确定义及正确不等式，不使未付债预算变成定理。

## 带符号的原模型小例与自查范围

两名玩家，四单位客户a,b,c,d，主题A={a,b}、B={a,b,c}、C={c,d}；根A，末位在首A/B/C后依次C/B/B。末位每行指定动作最优，根三个真实值(2,3/2,3/2)，是完整纯SPE。实际(A,C)。根改B时静态q=5/2、真d=3/2，R=1；根改C时静态q=1、真d=3/2，R=−1/2，说明同一合法策略即可两种符号。它不是half反例，也不是本源声称首次的构造；本批用它校验定义。

另复用已完整核验的DN四主题七客户作者策略表作新债务计算输入；没有重新跑DN全树认证。对其64个比较三元组逐个核q=f+δ、覆盖松弛、真实IC松弛和完整等号（其中最优元组满足本页O=OPT，非最优元组也同样满足代数式）。新检查的第一尝试误预设该单一复用策略应含全部三种R符号，在此前64个债账均通过后触发断言；保原脚本/日志，修为该样本实际符号并另加上述显式正负例，必要第二次运行PASS。不是源公式错误；不虚称一次无失败运行。

## 与当前方法边界的关系

主源指出Cartesian root-reset例含跨枝membership/tail-share协方差，局部slack/tax或逐对非负cap不足以自动付R总和；这是对特定付款路线的障碍，不是本R预算已被反驳的直接证明，更不是half失败。R、V和δ已经在同一账中各用一次，不能再独立当另一份W。源日期2026-10-24、OPEN与个人研究身份是历史载体；本页只认定所证等号/不等式及尚未在所读材料闭合的总债义务，不认证外审或新颖性。
