# 旧任意锚 AP 的独立只读源审原始反馈

实际工具返回的完整 agent ID（canonical task name）：`/root/early_x_anchor_queries/ap_source_audit`。

派工范围：只读完整原主稿、CLAIMS、README 与现行 AP 对象，核 actual 玩家 1–3 对同一合法 X 的代入、真实收益与后继、M 条件、付款及边界；不写文件、不改 Git/RUN/registry、不优化、不读 cb45 权重。本文件由父代理在子审完成后原样保存其完整最终反馈；不把该只读数学审查称作 51 行程序的独立代码审计。

以下为该代理的完整最终反馈。

---

**独立核验通过：常数和代入均正确。** 对 actual 玩家 \(i=1,2,3\)，令 \(r=7-i\)、\(h=(A_1,\ldots,A_{i-1})\)、\(b_j=\sum_{\ell<i}1_{j\in A_\ell}\)。同一个在 actual 前四历史选定的合法标签 \(X\) 可以直接作为旧 AP 的任意锚；不需要它最大化 \(\sum_X1/(b+r)\)。结论是对每个合法 \(Q\) 同时成立

\[
C_i u_i-(C_i-1)\kappa_X-L_{b,r}(X,Q)\ge0,
\]

\[
\kappa_X=\sum_{j\in X}\frac1{b_j+r},\qquad
L_{b,r}(X,Q)=
\sum_{j\in Q}\frac1{b_j+1}
-\sum_{j\in X\cap Q}\frac{r-1}{(b_j+1)(b_j+r)},
\]

且

| actual 玩家 \(i\) | 剩余人数 \(r\) | \(C_i=5(r-1)+r^2/2\) |
|---:|---:|---:|
| 1 | 6 | \(43\) |
| 2 | 5 | \(65/2\) |
| 3 | 4 | \(23\) |

### 精确来源定位

已完整实读以下三份原件及当前对象正文：

- 原主稿  
  `archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md`。  
  第 8–26 行明确任意完整纯 SPE、任意有序历史、当前人真实收益、\(M\le m\) 及真实后继不冻结；第 33–112 行给 BNS 承重证明；**第 132–155 行明确任意合法 \(C,D\) 的 AP，并在 149–151 行明言可用原总人数 \(m\) 作统一常数、无需猜加权最大者。**
- 同目录 `CLAIMS.md`：第 8 行为 `B10-AP-v1`，第 10 行为 `B10-AP-v2`；第 14–17 行解释 \(M_C\) 的两处用途及空锚边界。
- 同目录 `README.md`：区分原解析证明、内部独立重构和有限程序审计，不构成外审或新颖性认证。
- 当前对象  
  `customer-attraction/background-weighted-near-saturation-exchange-and-common-anchor-cap`，正文  
  `archives/customer-attraction/state/引理/任意背景加权近饱和交换与统一锚主题上界--引理.md`。  
  第 17–35 行为量词及 AP1/AP2；第 93–107 行完整重构任意锚误差；第 109–119 行为固定支持共同上界合同。

本次代入使用旧 **AP1 的 \(M\le6\) 统一放宽**，不依赖 v2 或旧固定支持点。因为 \(b_j\le i-1\)，有

\[
M=r+\max_jb_j\le r+i-1=6,
\]

而 \(u_i-\kappa_X\ge0\)，所以把原常数中的 \(M\) 提高到 6 方向正确。

### 完整付款链，以及可直接使用的非负恒等式

固定 \(i\)，以下将 \(u_i\) 写为 \(u\)，\(\kappa_X\) 写为 \(s\)。

仅强制当前人在真实前缀 \(h\) 选择 \(X\)，其后按同一 \(\sigma\) 的真实有序后继得到

\[
B_2,\ldots,B_r=L.
\]

令 \(v\) 是此分支中强制选 \(X\) 的当前人收益，\(t\) 是此分支真实末位 \(L\) 的收益；\(q_j\) 是本分支剩余 \(r\) 人对客户 \(j\) 的覆盖次数。定义

\[
w_j=\frac1{b_j+r},\qquad e=u-s,
\]

\[
d=\sum_{j\in X}(r-q_j)w_j,\qquad
d_L=\sum_{j\in X\setminus L}w_j,
\]

\[
I=\sum_{\ell=2}^{r-1}\sum_{j\in B_\ell\setminus X}w_j,
\qquad c_L=\sum_{j\in L\setminus X}w_j.
\]

当前真实激励给 \(u-v\ge0\)。对每个合法 \(B_\ell\)，在**原当前节点 \(h\)** 改选 \(B_\ell\) 并沿其自己的真实后继后，最坏分母保底给

\[
g_\ell:=u-\sum_{j\in B_\ell}w_j\ge0.
\]

这里没有把在 \(X\) 分支看见的 \(B_\ell\) 的后续冻结下来。所用的是它作为合法标签在 \(h\) 的独立真实偏离。

由定义有精确式

\[
c_L=d_L+e-g_r,
\]

\[
I=d-d_L+(r-2)e-\sum_{\ell=2}^{r-1}g_\ell.
\]

以下余项均非负：

\[
R_d:=5(v-s)-d\ge0.
\]

理由：对 \(X\) 内存在缺失席位的客户，\(b_j+q_j\le5\)，故
\(v-s=\sum_X(r-q_j)/[(b_j+q_j)(b_j+r)]\ge d/5\)。

\[
R_t:=r c_L-\frac65d_L-(t-v)\ge0.
\]

理由：\(L\setminus X\) 上 \(1/(b+q)\le1/(b+1)\le r/(b+r)\)；\(X\setminus L\) 上

\[
\frac1{b+q}\ge\frac1{b+r-1}\ge\frac6{5(b+r)}
\]

使用 \(b+r\le6\)。

令 \(p_Q\) 为在该真实末节点改选 \(Q\) 的实际收益。真实末位 IC 给

\[
BR_Q:=t-p_Q\ge0.
\]

整数核

\[
\frac1{b+z+1}\ge
\frac1{b+1}-\frac{r}{2}\frac z{b+r},
\qquad z\in\{0,\ldots,r-2\},
\]

与 \(Q\cap X\) 上的最坏分母下界给

\[
R_Q:=p_Q-L_{b,r}(X,Q)+\frac r2 I\ge0.
\]

因此，写 \(C=5(r-1)+r^2/2\)，有以下**完整精确付款恒等式**：

\[
\boxed{
\begin{aligned}
s+Ce-L_{b,r}(X,Q)
={}&5(r-1)(u-v)
+r\,g_r+\frac r2\sum_{\ell=2}^{r-1}g_\ell\\
&+BR_Q+R_t+R_Q\\
&+\left(r-\frac65\right)R_d
+\left(\frac r2-\frac65\right)(d-d_L).
\end{aligned}}
\]

所有乘子在 \(r=4,5,6\) 非负；\(d-d_L\ge0\)。展开右端，\(u\) 的总系数恰为

\[
5(r-1)+r+\frac r2(r-2)=5(r-1)+\frac{r^2}{2}=C.
\]

这不是额外新引理，是原 AP 付款链在统一 \(M=6\) 下的显式非负分解。

### 量词及边界

1. **同一 \(X\) 合法。** AP 是对所有合法锚 \(C\) 同时成立的命题。先从 actual 前四的 \(f_P\) 最大者中固定一个标签 \(X\)，再代入较早的三个 actual 前缀，无任何因果或量词冲突。不能逐客户、逐 hist 或逐 \(Q\) 更换 \(X\)。
2. **收益左端正确。** \(u_i\) 是原 actual 完整终局中玩家 \(i\) 的收益；\(v\) 才是其在 \(h\) 强制改 \(X\) 后的收益。二者不混同。
3. **真实后继完整。** 每次偏离都沿同一完整 \(\sigma\) 在改变后有序历史上的真实后继继续；同负载不同历史允许不同动作和平局。
4. **空锚与零客户保留。** 上述直接 \(M=6\) 分解没有除以 \(s,e,u\)，也没有对空 \(X\) 求不存在的最大客户；空锚时 \(d=d_L=R_d=0\)，仍成立。零客户时全式零。
5. **固定支持不要逐列改常数。** 如果另用 v2，更小 \(M_X\) 必须是整个允许支持上共同的上界，不能在每个 hist 或客户列分别取 \(r+b_h\)。当前统一 6 不存在这个问题；全部零质量 hist 应完整保留。
6. **有限轨道平均合法。** 固定非负平均是合法纯标签查询不等式的平均，不是另造可行动的分数标签。
7. **交叠放宽方向正确。** 展开后 \(XQ\) 系数为
   \((r-1)/[(b+1)(b+r)]>0\)，故可用现有共同上包络替代真实交叠；没有由此证明这些上包络共同可实现。

### 与 SAFE/H3 的准确有限比较

- 完整“所有合法 \(Q\)”AP 族包含 \(Q=X\)，该行退成 \(C(u_i-\kappa_X)\ge0\)，与对应 SAFE 等价。**你只生成的 17 个旧查询轨道不必包含新标签 \(X\)，因此不要声称单凭这 17 行就逻辑推出 SAFE；既有 SAFE 继续保留。**
- 对其他 \(Q\)，AP 付款为
  \(C(u_i-\kappa_X)\ge L_{b,r}(X,Q)-\kappa_X\)。这明确记录目录查询费用；不能只由单条 SAFE 得到这份预算。
- actual 玩家 4 若用旧任意锚 AP，统一常数是 \(29/2\)。已审 H3-X 在额外 \(f_P\) 最大性下使用 10，因此对**同一玩家 4、同一 \(b\)、同一 \(X,Q\)**，H3-X 加 SAFE 推出该 \(29/2\) AP 行。
- 本次玩家 1–3 使用不同 \(u_i,b,r\)。没有证据宣称它们被 H3-X 推出、支配 H3-X，或必然提高冻结 LP 的最优值。
- 未对任何点估价，未调用优化器，未读取 cb45 权重，未写任何文件。只读核验完成，释放本席。
