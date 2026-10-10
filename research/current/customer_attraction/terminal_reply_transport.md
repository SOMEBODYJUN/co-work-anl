# CA-TERMINAL-REPLY-DUAL-LIFT：末回复规范化的显式 dual 提升

**版本与状态，2026-10-10。** 本页给任意人数的条件性证书提升定理、转移图的
DAG 不变量及不对称收益预算。直接代数证明与独立内部 Fraction 审查完成；没有
外部同行评审或新颖性认证。没有构造普遍半覆盖证书，也没有证明聚合安全值桥。

输入为 [CAG-MODEL](model.md)：有限共同非空主题目录、单位玩家、单位客户，策略
定义于全部有序历史；空主题、重复主题和任意历史依赖平局均允许。客户类型质量
\(w_T\ge0\) 表示喜欢非空主题标签集 \(T\) 的客户数，有理质量可清分母展开为
不同单位客户。全类型恒等式先于质量代入，不把有符号辅助质量当作合法输入。

## 1. 末节点的真实行与 incumbent 转移

固定人数 \(n\ge2\) 和完整形式策略 \(\sigma\)，暂不要求它在某个质量上是 SPE。
记 \(\Gamma_{h,a}\) 为在有序节点 \(h\) 的原当前收益，减改选 \(a\) 后后继沿
同一原策略真实执行的收益行。故 \(\Gamma w\ge0\) 恰为全部节点的 SPE 条件。

末位前缀 \(\ell\in\mathcal L^{n-1}\) 的类型负载、原回复及查询行记为

\[
p_{\ell,T}=\sum_{j<n}\mathbf1_{\ell_j\in T},\qquad
a_\ell=\sigma_n(\ell),\qquad
L_\ell(b)_T=\frac{\mathbf1_{b\in T}}{p_{\ell,T}+1}.
\]

若 \(\ell,g\) 有相同主题计数，则它们对**全部类型**有相同负载，且

\[
\Gamma_{\ell,a_g}=L_\ell(a_\ell)-L_\ell(a_g)
                  =-\Gamma_{g,a_\ell}.\tag{1}
\]

因此这个 reciprocal 向量的任意符号倍数，均可用两条原真实行的非负乘子表示。
在原策略锥内两行总 slack 都为零。如果仅在一个给定实例的正质量客户上同负载，
只能得到该实例的总收益等式，不能声称全类型的式 (1)。

把 \(\ell\) 的末回复从 \(a\) 改成 \(b\)。对前缀中一份主题 \(S\)，该 incumbent
的新最终收益减旧最终收益为

\[
\delta_{\ell,S}(a\to b)_T
=\frac{\mathbf1_{S\in T}(\mathbf1_{a\in T}-\mathbf1_{b\in T})}
       {p_{\ell,T}(p_{\ell,T}+1)}.\tag{2}
\]

分子为零取零；分子非零时 \(S\) 在前缀中，故 \(p_{\ell,T}\ge1\)。令
\(q_\ell(S)\) 是主题在前缀中的次数。所有 incumbent 的收益变化和为

\[
\Delta P_\ell=\sum_Sq_\ell(S)\delta_{\ell,S}
=\mathbf1_{p_\ell>0}\frac{\mathbf1_a-\mathbf1_b}{p_\ell+1}.
\]

若末位自身收益变化为 \(\Delta L=L_\ell(b)-L_\ell(a)\)，完整覆盖变化满足

\[
\boxed{\Delta c_\ell=\Delta L+\Delta P_\ell.}\tag{3}
\]

逐类型核对即可证明：\(p=0\) 时只有末位决定覆盖；\(p>0\) 时覆盖不变，两种
收益变化恰相反。末位最佳收益相等不能抹去 incumbent 的变化。

## 2. 保留根覆盖的规范化与全部行的变换

对每个长度 \(n-1\) 的主题计数 \(q\)，选一个代表有序历史 \(g(q)\)，令
\(b_q=\sigma_n(g(q))\)。根实际末位前缀记为 \(\ell_0\)，特别选择
\(g(q(\ell_0))=\ell_0\)。定义形式策略 \(\bar\sigma\)：前 \(n-1\) 位全部行动仍为
原 \(\sigma\)，末节点 \(\ell\) 的行动改成 \(b_{q(\ell)}\)。

在原策略锥内，规范化后的末节点都仍最佳回应；早期节点不保证最佳回应。
根实际前缀和末回复保持不变，故 \(\bar c=c\) **逐类型**成立。以下固定

\[
\delta_{\ell,S}:=\delta_{\ell,S}(a_\ell\to b_{q(\ell)}).
\]

代表历史的这些向量全为零。对于早期节点 \(h\)，当前主题为
\(S_h=\sigma(h)\)。令 \(\ell_h\) 是从 \(h\) 沿原策略执行到末位前的完整前缀；
\(\ell_{ha}\) 是在 \(h\) 改选 \(a\)，再沿原策略执行到末位前的完整前缀。两条
路径所有中间动作都是真实续局，没有固定或搬用另一分支的后继。由式 (2)，

\[
\boxed{\bar\Gamma_{h,a}=\Gamma_{h,a}
       +\delta_{\ell_h,S_h}-\delta_{\ell_{ha},a}\quad(|h|<n-1).}\tag{4}
\]

末位行另有更简单的非负表达。写 \(g=g(q(\ell))\)，则

\[
\boxed{\bar\Gamma_{\ell,t}=\Gamma_{\ell,t}+\Gamma_{g,a_\ell}.}\tag{5}
\]

式 (5) 第二项是 \(L_\ell(b_q)-L_\ell(a_\ell)\)，与第一项相加就是
\(L_\ell(b_q)-L_\ell(t)\)。两行均属于原完整策略，系数均为 \(+1\)。

## 3. CA-TERMINAL-REPLY-DUAL-LIFT 的精确陈述和构造

固定任意目标类型向量 \(d\)。例如 \(d=2c-o\)，其中 \(o\) 是任意 \(n\) 个合法
比较主题的并集向量。假定给出规范化形式策略的逐类型恒等式

\[
d=\bar\Gamma^\mathsf T\lambda+r,\qquad \lambda\ge0,\quad r\ge0.
\]

不假定 \(\bar\sigma\) 是原实例的 SPE。定义

\[
E(\lambda)=\sum_{|h|<n-1,a}\lambda_{h,a}
  (\delta_{\ell_h,S_h}-\delta_{\ell_{ha},a}).\tag{6}
\]

**提升定理。** 若 \(r+E(\lambda)\ge0\) 逐类型成立，则可显式构造
\(\lambda'\ge0\)，使

\[
\boxed{d=\Gamma^\mathsf T\lambda'+r',\qquad r'=r+E(\lambda)\ge0.}\tag{7}
\]

构造：每个早期行的乘子原样加到原 \(\Gamma_{h,a}\)；每个末行 \((\ell,t)\) 的
乘子同时加到原 \(\Gamma_{\ell,t}\) 和原 \(\Gamma_{g(q(\ell)),a_\ell}\)。收到多次的
原行合并相加。全部乘子非负；式 (4)–(5) 求和即得式 (7)。这是具体提升机制，
没有调用 Farkas 或以目标已真来保证乘子存在。各历史各偏离保持独立权重。

一种可组织的充分条件是转移净流消去。以 \((\ell,S)\) 为顶点，每个早期行给边

\[
(\ell_{ha},a)\longrightarrow(\ell_h,S_h),
\quad\text{边权 }\lambda_{h,a}.
\]

记入流减出流为 \(\kappa_{\ell,S}\)，则

\[
E(\lambda)=\sum_{\ell,S}\kappa_{\ell,S}\delta_{\ell,S}.\tag{8}
\]

若所有非代表顶点有 \(\kappa=0\)，代表顶点因 \(\delta=0\) 可提供或吸收净流，
因此 \(E=0\)，提升余项仍为原 \(r\)。**这只是一种充分机制，不是 \(E=0\) 的必要
条件**：非代表顶点也可有 \(\delta=0\)，不同张量也可能线性消去。一般只需
式 (6) 与 \(r\) 合并非负。

定理亦可用于安全值目标 \(d=c-\alpha\sum_BQ_B\beta_B(p)\)：\(p\) 是查询主题
分布，\(Q\) 是不观察查询的合法 \(n-1\) 个竞争主题元组分布，
\(\beta_B(p)_T=p(T)/(1+\operatorname{load}_B(T))\)。提升保持同一 \(Q,p\)，特别
包括 \(\alpha=n-1/2\)。它没有构造这种目标的普遍输入证书。

## 4. 转移图的 DAG 不变量

定义一个有序前缀相对于原策略的偏离次数

\[
D(\ell)=|\{j<n:\ell_j\ne\sigma_j(\ell_1,\ldots,\ell_{j-1})\}|.
\]

因为在 \(h\) 或 \((h,a)\) 之后都沿原策略执行，

\[
D(\ell_h)=D(h),\qquad
D(\ell_{ha})=D(h)+\mathbf1_{a\ne S_h}.\tag{9}
\]

所以图源 \((\ell_{ha},a)\) 到图目标 \((\ell_h,S_h)\) 的每条真实非自偏离边，使
\(D\) 严格下降一。自行动给零行和自环。图无非平凡有向循环，非平凡路径长至多
\(n-1\)。采用“非代表顶点 \(\kappa=0\)”这个充分机制时，净源净汇位于代表顶点；
不能把这一机制误写成所有零张量 \(E\) 的必要端点条件。

末两人的 stationary reply-map 循环是在主题图 \(a\mapsto\sigma_n(P,a)\) 上，
不是本 incumbent 图的循环；不能据其局部消去，自动断言式 (8) 的全局净债消去。

## 5. 锐而不对称的收益预算

设末回复从 \(a\) 改成 \(b\)，某 incumbent 原最终收益系数为 \(u_{S,old,T}\)。
式 (2) 逐类型给

\[
(-\delta_{\ell,S,T})_+\le\tfrac12u_{S,old,T},\qquad
(\delta_{\ell,S,T})_+\le u_{S,old,T}.\tag{10}
\]

损失对应分母 \(p\to p+1\)，损失与原收益之比 \(1/(p+1)\le1/2\)；增加对应
\(p+1\to p\)，增加与原收益之比 \(1/p\le1\)。若两个末回复并列，末位共同收益
为 \(v\)，全部 incumbent 原收益为 \(P_{old}\)，按客户取正、负的转移总量
\(G,L\) 满足

\[
G\le\min\{v,P_{old}\},\qquad L\le\min\{v,P_{old}/2\}.\tag{11}
\]

其中 \(G\) 不超过旧末位在旧覆盖客户上的利润，\(L\) 不超过新末位在这些客户上的
利润；式 (10) 给另一侧界。完整覆盖变化另满足

\[
|\Delta W_\ell|\le\sum_{T:p_{\ell,T}>0}\frac{w_T}{p_{\ell,T}+1}
\le|C_\ell|/2.\tag{12}
\]

不能把式 (11) 压成对称的 \(v/2\)。两人目录 \(A,B\) 不交，大小为 \(2m,m\)，
\(m\ge1\)。根选 \(A\)，在 \(B\) 后选 \(A\)；在 \(A\) 后选 \(A\) 或 \(B\) 都构成
完整 SPE。末节点比较为 \((m,m)\) 或 \((2m,m/2)\)，两种根选择收益分别为
\((m,m)\) 或 \((2m,m)\)。终局 \(AA,AB\) 覆盖 \(2m,3m\)，末位收益均为 \(m\)，
覆盖转移等于 \(m\)，达到式 (12)。静态安全值恰 \(v_2=m\)：纯查询 \(A\) 保证
\(m\)，固定竞争者 \(A\) 又使每个查询收益最多 \(m\)。故单叶转移可为 \(v_2\)。

在提升误差中，实际分支 \(\ell_h\) 的 incumbent 损失可按半原收益定价；偏离分支
\(\ell_{ha}\) 的**增加**在式 (6) 中带负号，只有全原收益预算。这是尚未支付的
方向差异。对应图的术语，实际分支是图目标，偏离分支是图源。

## 6. 根覆盖不变也不能直接规范化 SPE

三位单位玩家、三个单位客户，目录为 \(A=\{a\},B=\{a,b\},C=\{b,c\}\)。
原策略根选 \(C\)；第二位在 \(A,B,C\) 后分别选 \(C,B,A\)；末回复见下表。
每行列出当前玩家改选 \(A,B,C\) 后，沿原策略真实续局的最终收益；指定动作均为
该行最大者，故表完整证明原策略是 SPE。

| 历史 | 指定动作 | 选 A 收益 | 选 B 收益 | 选 C 收益 |
| --- | --- | ---: | ---: | ---: |
| 空 | C | 1/2 | 5/6 | 1 |
| A | C | 1/2 | 1 | 3/2 |
| B | B | 1/2 | 5/6 | 5/6 |
| C | A | 1 | 5/6 | 5/6 |
| AA | C | 1/3 | 4/3 | 2 |
| AB | C | 1/3 | 5/6 | 3/2 |
| AC | B | 1/2 | 1 | 1 |
| BA | C | 1/3 | 5/6 | 3/2 |
| BB | C | 1/3 | 2/3 | 4/3 |
| BC | C | 1/2 | 5/6 | 5/6 |
| CA | C | 1/2 | 1 | 1 |
| CB | B | 1/2 | 5/6 | 5/6 |
| CC | B | 1 | 4/3 | 2/3 |

实际 \(CAC\)，各收益为 1，覆盖为 3。将 \(CA\) 选为其计数代表，其他计数选
词典最小历史，规范化把 \(AC,CB\) 的末回复改成 \(C\)，实际 \(CAC\) 保持不变。
但在前缀 \(C\)，第二位偏离 \(B\) 的真实规范化续局 \(CBC\) 给收益 \(4/3\)，
大于指定 \(A\) 的 1。其 slack 精确为

\[
\bar\Gamma_{(C),B}\cdot w=-1/3=1/6-1/2.
\]

其中原 slack 为 \(1/6\)，转移误差为 \(-1/2\)。客户 \(a\) 类型为 \(\{A,B\}\)，
在 \(CB\) 的回复 \(B\to C\) 下，第二位 \(B\) 收益增加 \(1/2\)，甚至大于其原
分支收益的一半 \((5/6)/2=5/12\)。因此不能将式 (10) 的半收益界用于偏离分支的增加。

零 \(E\) 也不要求非代表守恒：上述原策略在节点 \(B\) 偏离 \(A\)，对应图边
\((BA,A)\to(BB,B)\)。\(BA\) 非代表，但其末回复未变，\(\delta_{BA,A}=0\)；
\(BB\) 是代表，故该非自偏离行的 \(E\) 逐类型为零。

## 7. 边界、核验与剩余义务

\(n=1\) 可直接给半覆盖证书：对比较主题 \(t\)，
\(\Gamma_{\varnothing,t}=c-o\)，所以 \(2c-o=\Gamma_{\varnothing,t}+c\)。
任意 \(n\) 的 \(W=0\) 情形，根偏离任何主题至少得其大小除以 \(n\)；SPE 因而使
全部主题大小为零，最优覆盖亦为零，不定义 \(0/0\)。

主 [精确审计](../../../tests/audits/customer_attraction_terminal_transport.py) 从真实
终局直接重构原/规范化行，检查全部 39 比较、273 行类型恒等式、incumbent 和
reciprocal 向量、12 rank 边及任意非负逐行乘子的提升式；另复验三项锐两人实例。
[独立审计](../../../tests/audits/customer_attraction_terminal_transport_independent.py)
不导入主实现或规范模型，重构 273 恒等式、63 不同 gauge 列和 12 rank 边，并精确
检查零 \(E\) 的非代表 source 例。[冻结主记录](../../../evidence/runs/2026-10-10/terminal_transport_audit.json)、
[独立记录](../../../evidence/runs/2026-10-10/terminal_transport_independent.json)和
[数学审查](../../../evidence/runs/2026-10-10/terminal_transport_mathematical_review.json)
分别记录计算与措辞审查。默认只打印，\(\texttt{--output}\) 排他创建新报告：

```sh
python3 tests/audits/customer_attraction_terminal_transport.py
python3 tests/audits/customer_attraction_terminal_transport_independent.py
```

来源为本轮 [最终推导稿](../../../history/source/notes/customer_attraction/transport_round/terminal_transport_source.md)。
独立审查纠正了图源/目标称呼反置，以及把代表端点充分机制误写成零 \(E\) 必要条件
的两处措辞；最终来源和本页均已修正。

尚缺对任意策略和比较 portfolio 构造输入 \(\lambda,r\)，并支付
\(r+\sum\kappa\delta\)。条件性提升定理和有限审计没有解决这项一般义务，也不把
规范化策略自动认作 SPE。一般半覆盖与较弱安全值桥继续开放。
