# 最优索引交换的 Bernoulli 生成表示与积分税核

2026-10-24，general_exchange。范围是 CAG-MODEL 的任意有限单位客户、有限非空共同目录、任意人数。**这是既有 E1/E2 对全部子列表的生成表示，不是新的动态付款机制，不新增 half 已证范围。** 原 Q-CAG-HALF 仍 OPEN；外审与新颖性未认证。

既有来源为 `R-acd97406d8c4409d962eab2adcdc520c/round3_structure/optimal_portfolio_exchange.md` 的最优索引交换 E1/E2。本轮 root 与 aggregate_security 分别从定义独立重构了下列公式；后者先只读精确陈述，并以随机注入最优索引给出另一证明，审查见同轮 `security/bernoulli_exchange_blind_review.md`。这里只把原交换约束转换成能直接识别 `c/(c+1)` 的形式，不能以两人审查代替尚缺的动态接入。

## 1. 全范围精确陈述

固定一个最优带索引元组 `(T_1,...,T_m)`，其中 m>=1，允许重复。记

- `O = union_j T_j`，`|O|=OPT_m`；
- `d_x = #{j : x in T_j}`，故对 x in O 有 1<=d_x<=m。

任取 0<=s<=m 个合法目录主题 `(A_1,...,A_s)`，允许重复，记其客户负载 `c_x=#{i:x in A_i}`。它们可以是同一真实离轨枝的尾行动，也可以是任何合法主题列表；只有前一种情况才可把相关收益称为某条真实枝的收益。对每个实数 `t in [0,1]`，有

\[
\boxed{
\sum_{x\notin O}\bigl[1-(1-t)^{c_x}\bigr]
\le
\sum_{x\in O}
\frac{\binom{s-c_x}{d_x}}{\binom m{d_x}}
 t^{d_x}(1-t)^{c_x}.}
\tag{B}
\]

上标不足下标时二项式为零。端点处零次幂按一处理。左边 c=0 客户贡献零；右边 d>=1，因此 t=0 时也是零。s=0、空主题、重复主题、零客户均合法。

所有 `t` 上积分，得到精确的倒数核：

\[
\boxed{
\sum_{x\notin O}\frac{c_x}{c_x+1}
\le
\sum_{x\in O}
\frac{\binom{s-c_x}{d_x}}{\binom m{d_x}}
\frac{c_x!d_x!}{(c_x+d_x+1)!}.}
\tag{I}
\]

更一般，任意 `a>0` 取同一个非负积分权 `a(1-t)^(a-1)`，可得

\[
\sum_{x\notin O}\frac{c_x}{a+c_x}
\le
\sum_{x\in O}
\frac{\binom{s-c_x}{d_x}}{\binom m{d_x}}
 a\,\mathrm B(d_x+1,a+c_x).
\tag{Ia}
\]

`B` 是通常的 Beta 积分。a=1 为(I)。这只是不同的合法非负组合；不引入分数玩家或混合 SPE。

## 2. 从 E1/E2 生成的完整证明

对于任意子索引 `I subseteq [s]`，令 `k=|I|`、`B_I=union_(i in I) A_i`。从最优 m 个位置均匀删除 k 个索引 J，再加入这 k 个主题，仍是恰 m 个合法行动。若 `M_J={x in O:all optimal cover indices of x lie in J}`，最优性给既有 E1：

\[
|B_I\setminus O|\le |M_J\setminus B_I|.
\]

先对 J 均匀平均，即既有 E2：

\[
|B_I\setminus O|
\le\sum_{x\in O\setminus B_I}
\frac{\binom{k}{d_x}}{\binom m{d_x}}.
\tag{E2-I}
\]

现在各 A 槽独立以概率 t 进入 I。对 x outside O，它被 B_I 覆盖的概率是 `1-(1-t)^c`。对 x in O，未被 B_I 覆盖要求其 c 个覆盖槽全未选。条件于此，k 是 `Bin(s-c,t)`；因此

\[
\begin{aligned}
\mathbb E\left[
 \mathbf1_{x\notin B_I}\binom{|I|}{d_x}\right]
&=(1-t)^{c_x}
 \mathbb E\binom{\mathrm{Bin}(s-c_x,t)}{d_x}\\
&=(1-t)^{c_x}\binom{s-c_x}{d_x}t^{d_x}.
\end{aligned}
\]

最后的二项矩恒等式是把 `binom(K,d)` 写成 d 元子集全被选中的指示和。对(E2-I)取期望即得(B)。这也精确说明(B)不增加全部 E2-I 已有的可行性限制。

积分左边为 `int_0^1 [1-(1-t)^c]dt=c/(c+1)`；右边为整数 Beta 积分 `int_0^1 t^d(1-t)^c dt=d!c!/(c+d+1)!`，得到(I)。一般权的同一计算得(Ia)。

## 3. 保留任意比较前缀锚点

固定最优索引子集 J，q=|J|<m，令 `H=union_(j in J) T_j`、n=m-q。任取 s<=n 个合法主题 A 槽及负载 c。保留 J 的位置，只在其余 n 个最优位置作上述交换，即得更适合真实强制比较前缀的版本：

\[
\boxed{
\sum_{x\notin O}[1-(1-t)^{c_x}]
\le\sum_{x\in O\setminus H}
\frac{\binom{s-c_x}{d_x}}{\binom n{d_x}}
 t^{d_x}(1-t)^{c_x}.}
\tag{BH}
\]

对 x in O outside H，全部最优覆盖索引都不在 J，因此其剩余最优重数仍是 d_x，且 1<=d_x<=n。H 内客户永久由锚点保留，不会支付替换损失，所以完全从右侧消失。它也等价于在删除 H 客户的辅助覆盖实例上调用(B)；该辅助操作只证明组合最优性，不声称删除客户后原 SPE 仍可信。

特别是根强制某个比较主题 T_j 后，取 H=T_j、n=s=m-1，A 槽为原策略的真实尾行动。积分(BH)将该枝在 O 外的额外查询税 `sum_(x outside O)c/(c+1)` 全部放到 `O outside T_j` 的(d,c)谱上，T_j 的客户没有参与支付这份税。

## 4. 与真实枝利润的精确差额

上述税不是尾部在 O 外的实际利润。根是 T_j subseteq O 且没有其他旧玩家时，O 外客户若被尾行动覆盖，尾部实际总利润是 1。写

\[
E=|\{x\notin O:c_x>0\}|,\quad
L_{\rm out}=\sum_{x\notin O}\frac{c_x}{1+c_x},\quad
R_{\rm out}=\sum_{x\notin O:c_x>0}\frac1{1+c_x}.
\]

则精确地 `E=L_out+R_out`。BH/IH 只支付 `L_out`，**没有支付返还池 R_out**。分支根和尾部的实际利润之间的部分继承为

\[
u_k(z)-u_{\rm root}(z)
\le\sum_{x\in A_k\setminus T_j}\frac1{c_x(z)}.
\tag{PI}
\]

其中分母是在同一个真实叶 z 内的完整负载。若将右边的实际份额换成额外查询分母 `1+c_x(z)`，每条尾行动的差额都必须保留；对 O 外尾行动求和时，差额正好汇成 R_out。因此不能把(IH)直接代入(PI)而漏掉 R_out，也不能跨各强制 T_j 枝重复使用同一份原路径利润。

当前没有从全部真实后继 IC 得到 R_out 的共同预算，也没有控制各互斥比较枝右侧的总使用量。这是该表示接入一般付款时真正停下的位置。最优交换公式正确，不等于半覆盖目标已推进到闭合。


## 4.1 非均匀选择与辅助分数负载

同一 E2-I 可以让各 A 槽以各自概率 p_i in [0,1] 独立进入 I。记 C_x={i:x in A_i}，e_d 是 d 次初等对称多项式，则

\[
\sum_{x\notin O}\left[1-\prod_{i\in C_x}(1-p_i)\right]
\le\sum_{x\in O}
\frac{\prod_{i\in C_x}(1-p_i)}{\binom m{d_x}}
 e_{d_x}\bigl((p_i)_{i\notin C_x}\bigr).
\tag{NU}
\]

原因仍是条件于所有覆盖槽未选后，`E binom(|I|,d)=e_d(p_noncover)`。锚点版本同时把右侧 O 换成 O outside H、m 换成 n。它与全部 E2-I 约束相比也没有新增限制。

这表示可以接受任意辅助质量 w_i>=0（不是新玩家）。令 c_x(w)=sum_(i in C_x)w_i；对 v>=0 取 p_i(v)=1-exp(-w_i v)，再对 v 以 a exp(-av) 积分，a>0，得到

\[
\begin{aligned}
\sum_{x\notin O}\frac{c_x(w)}{a+c_x(w)}
\le\sum_{x\in O}\frac1{\binom m{d_x}}
\int_0^\infty a e^{-(a+c_x(w))v}
 e_{d_x}\bigl((1-e^{-w_i v})_{i\notin C_x}\bigr)\,dv.
\end{aligned}
\tag{FL}
\]

积分绝对收敛：各 e_d 有有限项，每项介于0和1，a exp(-av)可积。w=0、质量为零的槽、支撑退化均包含；有限非负求和和积分可直接交换。所有 w_i=1 时换元 t=1-exp(-v) 恰还原(Ia)。

FL 可描述某条原真实枝做软水位后的额外查询外税，而不假定水位后的对象是 SPE。它尚不能把原枝利润、规范水位信用 H 或变分 F* 免费放到右侧；两个合法上界也不能直接相减得到水位前后差界。真实外部利润的返还差额和跨枝信用池仍是§4同一断点。

## 5. 可复现精确组合核验与状态

`audit_bernoulli_exchange.py` 不调用均衡求解器或 LP，独立核验有限参数下二项矩生成式和 Beta 系数；一般结论由§2和§3的解析证明承担。它不扫描实例、不构造一般 SPE 证据。运行：

```sh
python3 research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/audit_bernoulli_exchange.py
```

本轮其他候选已停止：单实际列的 `m max_T sum_(x in T)1/(1+c_actual)<=W` 已被旧十一客户机会损失例否定，见 `actual_extra_candidate_failure.json`。这只定位新候选的失败，未发现新 half 反例。旧 route5a 的遗漏半因子纠错单独留在 `omission_factor_correction.md`，原共享稿现由 root 合并远端并发的更精确版本。
