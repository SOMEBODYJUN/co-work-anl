# 静态 (1,1)-smoothness 的精确证明与 SPE 接口障碍

状态：**可复用引理 + 已证接口障碍**；不改变 Q-CAG-HALF 的 OPEN 状态。

## 1. 静态 profile 上确实有 (1,1)-smoothness

固定任意终局行动 profile \(a=(A_1,\ldots,A_m)\)，以及任意比较 profile
\(o=(O_1,\ldots,O_m)\)（稍后取最优 profile）。写

\[
 k_x=|\{i:x\in A_i\}|,
 \qquad t_x=|\{i:x\in O_i\}|.
\]

把每个玩家 \(i\) 单独改为 \(O_i\)，冻结其他玩家的行动。若 \(x\in O_i\)，在该偏离终局中它的分母是
\(k_x-1_{x\in A_i}+1\le k_x+1\)，所以该偏离对 \(i\) 的贡献至少
\(1/(k_x+1)\)。因此对每个 \(x\) 有
\[
 \sum_i u_i(O_i,a_{-i})
 \ \ge\ \sum_{x:t_x>0} \frac{t_x}{k_x+1}.
\]
若 \(k_x=0\)，右侧项 \(t_x\ge1\)。若 \(k_x\ge1\)，现有福利 \(W(a)\) 已对该客户贡献一个单位。逐客户相加得到
\[
 \boxed{\quad W(a)+\sum_i u_i(O_i,a_{-i})\ge
 |\cup_i O_i|.\quad}
\tag{SM(1,1)}
\]
取 \(o\) 为最优 \(m\)-主题 profile 即
\[
 W(a)+\sum_i u_i(O_i,a_{-i})\ge \operatorname{OPT}_m.
\]
所以，若 \(a\) 是**同时行动**纯 Nash 均衡，则
\(u_i(a)\ge u_i(O_i,a_{-i})\) 对每个 \(i\)，再用
\(W(a)=\sum_i u_i(a)\)，即得 \(2W(a)\ge\operatorname{OPT}_m\)。

这说明常见的静态 smoothness/valid-utility-game 证明本身没有问题；它的唯一接口是把每个玩家的终局收益与冻结其他玩家的静态偏离收益逐项比较。

## 2. 该接口不能由全历史 SPE 提供

全历史 SPE 的偏离比较保留**真实后继策略**：在节点 \(h\)，玩家 \(i\) 的原行动与替代行动比较的是两棵完整续局，而不是终局 \(a_{-i}\) 冻结不动。故不能将
\[
 u_i(a)\ge u_i(O_i,a_{-i})
\]
当作 SPE 的结论。

精确三人证书可取目录
\[
 A=\{a\},\qquad B=\{a,b\},\qquad C=\{b,c\}.
\]
存在完整纯 SPE，其实际路径为 \((C,A,C)\)，三人终局收益均为 \(1\)。若把中间玩家的行动从 \(A\) 静态改成 \(B\)，冻结另外两人的行动为 \(C,C\)，其静态收益为
\[
 u_2(B;C,C)=1+\frac13=\frac43>1=u_2(A;C,C).
\]
但在真实顺序偏离中，前缀 \(CB\) 后末位玩家选择 \(B\)（该动作是其最佳反应），于是中间玩家的真实收益变成
\[
 u_2(B;C,B)=\frac12+\frac13=\frac56<1.
\]
因此该 SPE 终局不是静态 PNE，SM(1,1) 不能直接支付 SPE 福利。这是“静态 smoothness 有效、SPE→PNE 桥失败”的精确障碍；它不构成 Q-CAG-HALF 反例（本例 \(\operatorname{OPT}_3=W=3\)）。

## 3. 可继续尝试的严格接口

要从 SM(1,1) 得到一般顺序结论，必须另外控制真实后继与冻结终局之间的差额，例如证明对某个跨分支支付 \(D_i\)
\[
 \sum_i u_i(O_i,a_{-i})
 \le \sum_i u_i(a)+D,
 \qquad D\le W(a),
\]
且 \(D\) 必须来自完整 SPE 的离轨分支一致性。已有静态 PNE/CCE 替换、逐人残余和固定静态安全值桥均有独立反例；本页仅保留 SM(1,1) 引理及其精确失效接口。

## 4. 证据入口

上面的三人完整策略和全部离轨最佳反应逐项见
[`research/current/customer_attraction/continuation_lemmas.md`](../../../../current/customer_attraction/continuation_lemmas.md)，其中 `CA-SPE-NON-PNE` 给出同一数据及审计入口。该引用不声称新主目标结论，也不把有限反例升级为一般否定。
