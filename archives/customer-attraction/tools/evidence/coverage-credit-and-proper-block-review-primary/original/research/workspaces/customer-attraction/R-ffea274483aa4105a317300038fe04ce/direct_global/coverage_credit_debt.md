# 真实偏离的缺口支付与精确覆盖信用（探索，未证明）

日期：2026-10-21。模型及全部量词固定为 `research/current/customer_attraction/model.md`。
Q-CAG-HALF 仍 OPEN。本页没有一般正面定理或目标反例，也不把已有有限扫描当作证明。

## 1. 恢复的旧 Boss8 材料

旧工作区 `R-d51d7a410c12456aa5c44e84b78708d0` 的根 README、`global_proof/README.md`、
`global_proof/static_allowance_notes.md`、`round2/README.md` 均存在并已读取。
`round2/direct_global/` 存在，但没有 README；其中有额外映射环流的独立审查和审计。
旧 round2 README 列出的 `round2/static_allowance/`、`round2/security_global/`、
`round2/independent_attack/` 在当前 clone 不存在，不能按索引假定具体正文已经恢复。

旧候选 SA 是：对实际终局 s 的每个合法 T，

`D_T(s):=sum_i u_i(T,s_{-i}) <= (1+1/m) W`。

其充分性推导保留，但 SA 没有一般证明。母代理本轮在独立攻击 SA，本分支不重复同类 LP。

## 2. 区别于已失败残余匹配的更弱接口

固定一份完整历史纯 SPE sigma，其实际终局为 s，覆盖 C，W=|C|。
固定任意 m 个比较主题 T_1,...,T_m，允许重复；令 O 为比较并集，d_x 是比较重数。
对每个实际位置 i，令 V_{ij} 为玩家 i 在自己的实际有序历史改选 T_j 后、
所有后继沿原 sigma 行动所得的真实收益。由 SPE，逐项 V_{ij}<=u_i。

一个未证明的充分候选是：至少存在一个最优比较组合及其排列 pi，使

`sum_i V_{i,pi(i)} >= OPT_m-W`。                                      (RM-gap)

更强、但可能更便于代数的均匀版本为

`P := (1/m) sum_{i,j} V_{ij} >= OPT_m-W`。                           (UR-gap)

两者均足以推出半覆盖，因为任意排列的真实偏离收益和、以及 P，都不超过 W。
UR-gap 蕴涵 RM-gap：均匀排列的期望匹配值恰为 P。

已有 `portfolio_matching_counterexample.md` 否定的是右侧更大的 |O\C|。
其 W=44、OPT=45、两种匹配真实收益都为41，所以没有否定本页的右侧 OPT-W=1。
本页没有宣称 RM-gap 或 UR-gap 新颖，也没有得到它们的证明。

## 3. 精确信用恒等式

令 c_x 是实际终局负载，并定义均匀静态比较值

`Q := (1/m) sum_j D_{T_j}(s)`。

对固定 T，逐客户精确计算给

`D_T = sum_{x in T cap C} (m+1)/(c_x+1) + m |T\C|`。

故定义有符号真实分支债务 Delta=Q-P 后，有恒等式

`P - (|O|-W) = E - Delta`，

其中

`E = |C\O| + sum_{x in O\C}(d_x-1)
     + sum_{x in O cap C} d_x(m+1)/(m(c_x+1)) >= 0`。                 (E)

因此 UR-gap 精确等价于 `Delta<=E`（当比较组合最优时）。
这不是一条已知支付不等式；它准确展示已失败的纯残余匹配遗漏了什么信用：
实际覆盖但不在比较并集中的客户，给每人完整一单位；比较重复和真实交叠另给信用。

由于 d_x>=1 且 c_x<=m，交叠每客户至少贡献 1/m；实际并集外客户每人贡献1。
所以 `E>=W/m`。这个粗下界不能自行支付 Delta，也不能用来证明 SA。

## 4. 债务是精确的分母变化

对实际位置 i 与比较主题 T_j，记 b_i(x) 为实际前缀 i-1 人对 x 的负载，
r_i(x) 为实际后缀 i+1,...,m 的负载，f_ij(x) 为偏离到 T_j 后原策略真实后缀的负载。
则

`u_i(T_j,s_{-i}) - V_ij
 = sum_{x in T_j} (f_ij(x)-r_i(x)) /
   ((b_i(x)+1+r_i(x)) (b_i(x)+1+f_ij(x)))`。

对 i,j 取 (1/m) 总和就是 Delta。分母恒正，债务可以为负；
不能把 f_ij 独立更换为全部克隆，也不能冻结为实际后缀。
本分支的直接缺口是：用完整离轨节点的最优性，将这些有符号分母变化共同支付给 E。
只用实际节点 V_ij<=u_i 无法得到该上界。

## 5. CAG 的可复用强核，尚未合并成全树预算

对任意合法整数背景 b 和主题 A,B，有逐客户精确交换式

`u(A;b+B)-u(A;b+A)
 = sum_{x in A\B} 1/((b_x+1)(b_x+2)) >=0`。

更一般，把 Delta_R f(b)=f(b+1_R)-f(b)，则

`(-1)^k Delta_{R_1} ... Delta_{R_k} u(A;b)
 = k! sum_{x in A cap R_1 cap ... cap R_k}
       1/prod_{ell=1}^{k+1}(b_x+ell) >=0`。

这是非负 CAG 客户核的完全交替有限差分性质。它严格强于只假定匿名对称精确势；
已有抽象势菜单反例违反全克隆最坏性，所以不能用于否定本页候选。
目前没有把这些局部正核组织成任意深度、任意完整策略的非负覆盖证书。

## 6. 接续建议与边界

下一步真正承重的工作是证明或反驳 `Delta<=E`，或允许最优组合/排列共同选择后证明 RM-gap。
若找到辅助桥失败，须给完整客户输入和全部有序历史 SPE，再准确保留其未否定半覆盖的边界。
不再重试纯残余覆盖 `OPT_m(N\C)<=W`、静态最低 PNE/CCE 比较、固定缩放实际背景弱桥或逐期非负预算。

本轮没有导入任何外部定理。网页检索未提供可直接导入的一般顺序定理；
已有文献页已经说明 shared misery 与 symmetric singleton 的条件不适用一般主题目录。
