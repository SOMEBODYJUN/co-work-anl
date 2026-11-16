# Boss7：静态补集缺口与联合迁移的收尾复核

日期：2026-11-16。复核输入为 `ea61d399208bc4d91f7acc80d317b3a669df576f` 的当前登记、正文和已交付收据。此记录承担本次实际数学审读，不替代原证明、对象状态或任务收据。

## 范围与结论

本次接入尚未整合的已完成任务 `wc-boss4-deficit-repair-repair-3be320ec40a8e3a3`。已实读该任务、收据、替代后的边 `wc-static-complement-transports-same-action-deficit`，以及其承接的两源 ALL 边 `ca-wc-shapley-and-complement-transfer-global-minimum`。核心仍为两个 v1 对象：

- `weighted-congestion/static-customer-coverage-complement-harmonic-transfer`；
- `weighted-congestion/harmonic-complement-monochromatic-pne-global-minimum`。

替代后的单源边准确只交付静态偏离和共同缺口的恒等变换，保留 `conditional` 与 `contribution`。完整全局势结论由原 Shapley 同色定理与补集桥共同推出；现有 3C ALL 边已明确列齐两个源。没有发现需要再次修改对象或逻辑边的数学错误。本轮需要完成的是已交付替代收据的整合。

## 亲自重推偏离、势与缺口

设活动玩家数为 $m\ge1$，每客户 $x$ 的质量为 $v_x>0$，外生背景 $b_x\ge0$。源玩家的覆盖为 $S_i$，目标动作取 $X\setminus S_i$。固定其他玩家的源覆盖数 $c_x^{-i}$。玩家在目标上使用资源 $x$ 时，目标负载恰为 $m-c_x^{-i}$，所以

\[
p_x(m-c_x^{-i})=\frac{v_x}{b_x+1+c_x^{-i}}.
\]

由此 $C_i=K_i(s_{-i})-u_i$，其中 $K_i=\sum_xv_x/(b_x+1+c_x^{-i})$ 在本次固定对手的偏离中不变。因此对全部合法单方动作，包括弱平局和空动作，$\Delta_iC=-\Delta_i u$，静态 PNE 双向保持。重复标签可保留；取商后把同动作起点统一提升到同一个源标签，其收益与势不变。

若全部源活动覆盖数为 $c_x$，目标负载为 $m-c_x$，令 $H_b(c)=\sum_{\ell=1}^c1/(b+\ell)$，则

\[
\Psi=\sum_x v_x\sum_{j=1}^{m-c_x}\frac1{b_x+m+1-j}
=\sum_xv_xH_{b_x}(m)-\Phi.
\]

同一完整比较剖面 $t$ 因而满足

\[
\Delta\Psi-\sum_i\Delta_iC
=\sum_i\Delta_i u-\Delta\Phi.
\]

这条恒等式本身没有给右端的符号。源同色静态 Shapley 定理另给 $\Delta\Phi\le\sum_i\Delta_i u$；PNE 给每个 $\Delta_i u\le0$。两者与桥联合才得

\[
\Psi(t)-\Psi(s)\ge\sum_i[C_i(t_i,s_{-i})-C_i(s)]\ge0
\]

对所有完整目标剖面成立。故目标同动作精确 PNE 是全局 Rosenthal 势最小点。这解释了单源步骤和两源完整关系各自的实际作用。

## 实背景与独立目标证明

实背景没有被误作整数个固定玩家。原 Shapley 证明的逐参数次模函数可取
$C_p(U)=\sum_{x\in\cup U}v_x(1-p)^{b_x}$。对 $j\ge1$ 位活动覆盖者，每人的积分边际为
$v_x\int_0^1(1-p)^{b_x+j-1}\,dp=v_x/(b_x+j)$；对应势为 $v_xH_{b_x}(j)$。逐参数归零、单调、次模比较仍然成立，故任意固定实 $b_x\ge0$ 的域确已支付。

目标正文还保有独立证明。若起点所有玩家选 $B$，比较剖面从 $x\in B$ 移走 $r_x$ 人，其势损失绝对值至多 $r_xp_x(m)$；对 $x\notin B$ 加入 $r_x$ 人，势增加至少 $r_xp_x(1)$。相加恰为所有玩家从同一起点单方偏离的成本增量和。非减费用足够支持该证明，不能把“证明存在”误读成任意异权或任意起点都有相同结论。

补集正文给出的正系数插值也已核算：$A=b_x+m+1\ge M=m+1$、$D+1=9mM$ 时，修正截断几何多项式的每个系数扰动小于
$mM36^{m-1}(m/M)^{9mM}<2^{2m+6m-6-9m}<1$。因而所有系数仍正，节点精确。$m=1$ 用常数费用。实参数只主张实系数存在；有理输入的幂次和系数位长为显式输入的多项式。

## 序贯反例的精确重算

按原文 13 名单位客户，兴趣类型 $AB,C,BC,ABC$ 的人数依次为 $4,2,3,4$。对根动作 $A,B,C$，末位选择 $A,B,C$ 的收益行分别为

\[
(4,7,7),\qquad(4,11/2,11/2),\qquad(6,15/2,9/2).
\]

完整末位回复 $(C,B,B)$ 均为最优，首位源收益为 $(6,11/2,11/2)$，严格选择 $A$。对精确节点费用 $p_x(z)=z/2$，相同回复在补集末位仍然最优，但首位目标成本为 $(5/2,2,2)$，所以原根动作 $A$ 不再最优。本轮用有理分数重算全部 27 个固定对手单方比较，均满足差值变号，并核对上述三个根分支。

反例只否定“直接保持同一完整序贯策略”：跨根分支时后继会变，$K_i$ 不再固定。它不否定静态 PNE 迁移、全局 Rosenthal 势结论，也不声称不存在其他目标 SPE。社会总成本及乘法近似率仍有各自的数学合同。

## 精确证据

- `archives/weighted-congestion/state/定理/客户均分到非负多项式拥塞的静态补集转移--定理.md`：全文，特别是“静态偏离与势的精确对应”“正系数插值与有理位长”“序贯边界”；SHA256 `e6b18c3998549abe895e26851e05645168eaee8ac0ddd2b8afecabff53ff80ed`。
- `archives/weighted-congestion/state/定理/调和补集拥塞的同动作精确均衡是全局势最小点--定理.md`：全文；SHA256 `278f3b3307126edc820681ccfefbc917d657893119e0bef28c148dc3c3f50f13`。
- `archives/customer-attraction/state/定理/固定背景下单色静态Shapley均衡的全局势最大性--定理.md`：“从单方收益到全部活动配置”“任意外生负载的覆盖专门化”，并读全文的身份抽样公式；SHA256 `bb44ea464f60d7da0fc13551dafca11f08d9f86b69a77e17d4cac4aaeab01e57`。
- `archives/weighted-congestion/state/资料/加权拥塞成果入口的模型与结论范围--资料.md`：核单位权子类、空动作、固定对手静态稳定式以及势、总成本、全状态和序贯量词的分界。

本轮保留其他存档已有的有效审读，不声称重新证明全部 3,821 个对象。没有新增数学开放义务；原记录中的其他开放命题照常保留。
