---
id: "customer-attraction/terminal-query-tax-reserve"
kind: "lemma"
type_tag: "引理"
title: "实际末两人相对单阻挡安全值的明确查询税余量"
status: "proved-lemma-with-open-aggregate-extension"
summary: "每个安全最优查询分布都给末两位总余量至少h+H_b(p,B)，倒二还可加非负δ；早期亏损由该税池支付仍是更强未证候选。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/terminal_query_reserve.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security_continue/terminal_query_reserve.md"
---

# 实际末两人相对单阻挡安全值的明确查询税余量

## 对象与结论

沿用[完整历史共同目录模型](../定义/共同目录完整历史模型--定义.md)，m≥2。固定一份完整纯SPE的实际倒二主题B、末主题C、前m−2人客户负载d，令b=d+1_B为实际末前背景。对目录查询分布p，令p_x=Pr_{T∼p}(x∈T)，并定义

\[
 \phi_p(e)=\sum_x\frac{p_x}{e_x+1},\quad
 F_b(p)=\sum_x\frac{p_x}{b_x+1},\quad
 H_b(p,A)=\sum_{x\in A}\frac{p_x}{(b_x+1)(b_x+2)}.
\]

令[LAST的准确单阻挡值](../候选/实际末前背景的聚合安全值--候选.md)为

\[
 M_b=\min_q\max_T\mathbb E_{A\sim q}
           \sum_{x\in T}\frac1{b_x+1+\mathbf1_{x\in A}}
     =\max_p\min_A\phi_p(b+\mathbf1_A).
\]

取任意一个右侧最优查询分布p，写h=max_AH_b(p,A)。核分解给

\[
 \boxed{M_b=F_b(p)-h.}                                  \tag{1}
\]

同一完整SPE的实际末两人利润满足

\[
 u_m-M_b\ge h,\qquad u_{m-1}-M_b\ge H_b(p,B).            \tag{2}
\]

所以实际末两位总余量至少为h+H_b(p,B)≥0。这对**每个**安全最优p成立，允许p不唯一；它不是对任意非最优p仍把F_b(p)−h称M_b的断言。

## 完整推导

固定p时，逐客户核分解为φ_p(b+1_A)=F_b(p)−H_b(p,A)。取A的最小并用p最优即得式(1)。实际末位在背景b最优，故

\[
 u_m=\max_TF_b(T)\ge F_b(p),\qquad
 u_m-M_b=[u_m-F_b(p)]+h,
\]

方括号非负，得到式(2)第一项。

对每个合法A，背景d与b=d+1_B的精确差为

\[
 \phi_p(d+\mathbf1_A)-\phi_p(b+\mathbf1_A)
 =\sum_{x\in B}\frac{p_x}
 {(d_x+1+\mathbf1_{x\in A})(d_x+2+\mathbf1_{x\in A})}
 \ge\sum_{x\in B}\frac{p_x}{(d_x+2)(d_x+3)}=H_b(p,B).
 \tag{3}
\]

分母正，最小差在A覆盖该客户时取得。p在背景b安全最优意味着所有A都有φ_p(b+1_A)≥M_b。因此

\[
 \min_A\phi_p(d+\mathbf1_A)\ge M_b+H_b(p,B).
\]

既有[真实末两人保底](../定理/末两人逐人保底与全人数弱福利界--定理.md)给

\[
 u_{m-1}\ge\theta_2(d)\ge v_2(d)
 \ge\min_A\phi_p(d+\mathbf1_A),
\]

其中v_2(d)是固定背景d的真正单阻挡minimax；最后一步只是选择了一个合法查询分布p。由此得到式(2)第二项。没有假设倒二收益和末位收益的大小次序，也没有替换任何实际离轨回复或历史平局。

## 可保留的更细非负余量

置s_A=φ_p(b+1_A)−M_b≥0。B上b_x=d_x+1≥1，所以定义

\[
 \delta_B(p)=\min_A\left[s_A+
       2\sum_{x\in B\setminus A}
        \frac{p_x}{b_x(b_x+1)(b_x+2)}\right]\ge0.
\]

在式(3)中，A覆盖B内客户时差恰为p_x/((b_x+1)(b_x+2))；不覆盖时差为p_x/(b_x(b_x+1))，比前者多2p_x/(b_x(b_x+1)(b_x+2))。因此逐A精确有

\[
 \phi_p(d+\mathbf1_A)=M_b+H_b(p,B)+s_A+
       2\sum_{x\in B\setminus A}\frac{p_x}{b_x(b_x+1)(b_x+2)}.
\]

取最小并用同一倒二保底，得

\[
 u_{m-1}-M_b\ge H_b(p,B)+\delta_B(p).                    \tag{4}
\]

这是同一背景平移的额外非负量，没有给早期真实分支新容量。原来源仅对基本式记录原主代理的独立解析重构，δ式记为原作者自审；本轮重新按两种membership情况逐式核对式(4)，不将历史自审改写成已经发生过另一轮盲审。

若在全部最优p上选择最大基本税池，h=F_b(p)−M_b，所以h+H_b(p,B)是最优面上的线性目标。这里仅给准确优化对象，没有声称已实现通用求解器或已经支付早期亏损。

## 充分候选与仍缺的方向

准确LAST等价于

\[
 \sum_{i\le m-2}(M_b-u_i)
 \le(u_{m-1}-M_b)+(u_m-M_b).
\]

因此更强的充分候选为

\[
 \sum_{i\le m-2}(M_b-u_i)\le h+H_b(p,B).                 \tag{TAX-LAST?}
\]

原来源没有证明它，也没有给完整SPE反例。式(2)只给实际尾余量**不小于**右侧税池，不能反向推出早期亏损**不大于**这个税池；实际尾部最优性松弛或δ也可能参与支付。加入δ的相应条件仍只是充分候选，未被一般证明。

m=2时早期和为空，税池非负，LAST直接成立。零客户、全空目录、重复B或C均按非严格和式处理；δ仅在B内除b_x，那里b_x≥1，没有遗漏零分母。六人时缺口仍是前四名实际玩家的总亏损，不能由两名后继的局部式替代。

原稿记载曾在旧34、36、89客户例的新背景上作定位计算，三例每个实际玩家均超过对应M_b；这是原探索的阴性记录，本轮未复跑这些数值探针，不把它们升级为一般证据。原稿也明确未扩大扫描固定策略锥。此处成熟内容是式(1)–(4)的完整推导，未成熟内容是TAX-LAST?及跨真实分支的共同支付，二者分别保存。

本对象依赖有限minimax、核差分及末两人保底，不依赖二次势自响应等于minimax的错误等式。后续若改变查询p，需保留其安全最优性或重新追踪s_A的符号；若改变真实前缀，需重新计算b，不能将冻结背景差分跨互斥子树抵消。
