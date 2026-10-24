# 末个非 B 行动的刚性：盲独立重构与同额信用审查

2026-10-24。本轮 menu 子研究员仅先收到 credible_construction 的精确陈述，未读发现证明，独立完成以下推导；随后收到其同额信用陈述并对照。结论为一般模型中的**有条件全范围引理**，无外审或新颖性认证。它没有证明 Q-CAG-HALF，没有免费保持更早祖先 IC。

## 精确对象

任意有限单位客户、有限非空共同集合目录 S、非负整数固定负载 b、n≥1 名单位尾玩家及完整有序历史纯 suffix-SPE。给定 B∈S，假设在 b 后前 n−1 名尾玩家均选 B 时，末位选 B 是全目录最佳回复。主题是真实客户集合；重复标签若代表同一集合，应视为同一个主题，或将“恰为 B”改为“覆盖集合恰为 B”。

若该 SPE 实际尾路径不全为 B，取最后一个非 B 行动 T，之前 k 个行动 P_1,…,P_k，之后 r 个 B，k+1+r=n。令 p_x=Σ_{j≤k}1_(x∈P_j)，并记

\[
\alpha_T=\sum_{x\in T\setminus B}\frac1{b_x+1},\qquad
\beta_T=\sum_{x\in B\setminus T}\frac1{b_x+n}.
\]

## 独立证明

末位条件中 T 与 B 的交集贡献相同，故 α_T≤β_T。T 节点真实当前收益为

\[
u_T=\sum_{x\in T\setminus B}\frac1{b_x+p_x+1}
+\sum_{x\in T\cap B}\frac1{b_x+p_x+r+1}.
\]

当前改 B 后，保留**同一原策略的真实后继**，其收益 d_B 至少为

\[
G_B=\sum_{x\in B}\frac1{b_x+p_x+r+1}.
\]

这是每名未来玩家对 B 客户最多贡献一次的逐客户下界，不冻结后继。于是

\[
u_T\ge d_B\ge G_B,
\]

而

\[
\begin{aligned}
u_T-G_B
&=\sum_{x\in T\setminus B}\frac1{b_x+p_x+1}
-\sum_{x\in B\setminus T}\frac1{b_x+p_x+r+1}\\
&\le\alpha_T-\beta_T\le0,
\end{aligned}
\]

因为 0≤p_x≤k 且 k+r+1=n。全链只能取等，得到

\[
\alpha_T=\beta_T,
\quad p_x=0\ (x\in T\setminus B),
\quad p_x=k\ (x\in B\setminus T).
\]

逐点刚性使用每个客户正单位价值及有限正分母；不存在正负逐客户误差相消。空差集的条件自然为空。

另外 d_B=G_B 迫使改 B 后每名真实未来玩家覆盖 B 的每个客户，否则该客户分母严格小于下界所用分母，产生严格收益增量。末位条件排除目录中 B 的任何严格超集：若 D⊋B，D 对 n−1 个 B 的收益严格高于 B。因此每名真实后继的主题恰为 B。

当前改 B 与原 T 精确平局，其孩子原本已是完整 SPE；仅把 T 节点的规定行动切换为 B、其他各孩子保留原策略，便保留此节点以下的完整 SPE。不能据此断言该节点之前的祖先仍最优。

B=∅ 时末位条件迫使目录仅含空集合，不存在所假设的非全 B 实际路径；n=1 时证明仍成立，改 B 后无未来玩家。

## 同额信用的独立核验

设 n≥2。比较原实际尾终局和上述 T 节点改 B 后的真实终局。除当前外的每名尾玩家，在 T\B 上均不覆盖任何客户，在 B\T 上覆盖全部客户。因此每名这样的玩家都恰损失

\[
\varepsilon_T=\sum_{x\in B\setminus T}
\left(\frac1{b_x+n-1}-\frac1{b_x+n}\right)
=\sum_{x\in B\setminus T}\frac1{(b_x+n-1)(b_x+n)}.
\]

当前玩家收益不变，且

\[
\varepsilon_T\le\frac{\beta_T}{n-1}
=\frac{\alpha_T}{n-1}.
\]

当 b=0 时取等。固定旧背景玩家不必覆盖整个 B\T，也可能覆盖 T\B；他们的返还应另算，不能当作同额 ε。这份同额信用不会自动支付祖先节点对其他互斥孩子的比较。

还有一个定义级后果：n≥2 时，每份满足前提的 suffix-SPE 实际尾联合都覆盖 B。若非全 B，T 覆盖 B∩T，其余 n−1 名玩家每一位都覆盖 B\T。n=1 时不能宣称集合包含（两个同大不交主题即可并列最佳）。这个后果仍保留原末位条件，不是任意目录/任意 B 的无条件覆盖定理。

## 接续边界

本次盲重构未发现致命异议。末位条件是承重假设；不能从任意实际末位最佳回复直接推出该条件，因为它指定的是 n−1 个相同 B 的背景。局部切换降低此前尾玩家收益 ε，因此更早规定路径的 IC 恰是尚需支付的真实缺口。全树付款和一般半覆盖仍 OPEN。

## 补注：量化等号来源及旧背景守恒

这里的精确域是任意有限共同目录、任意非负整数背景 b、任意 n≥1、任意完整历史 suffix-SPE，以及任意 B∈S。**不假设全 B 末位最佳**。若实际尾路径不全为 B，才定义 T 为实际最后非 B，并有精确分解

\[
\alpha_T-\beta_T=A_T+E_T+\gamma_T+\zeta_T\ge0,
\]

其中

\[
\begin{aligned}
A_T&=\sum_{x\in T\setminus B}
\left(\frac1{b_x+1}-\frac1{b_x+p_x+1}\right),\\
E_T&=\sum_{x\in B\setminus T}
\left(\frac1{b_x+p_x+r+1}-\frac1{b_x+n}\right),\\
\gamma_T&=u_T-d_B,\qquad \zeta_T=d_B-G_B.
\end{aligned}
\]

四项分别非负。因此存在该实际最后非 B 节点本身就迫使 α_T−β_T≥0；不能忽略这个结论而让左边为负。当 B 取实际末位主题时，T 正是实际路径最后一个异题节点，其后至少一个 B；若实际全为 B，则没有这样的 T，分解不作定义。若另外加入原末位条件，它提供相反方向 α_T−β_T≤0，因而一次压零四项。这只是本证明夹逼的定量写法，尚无跨不同 B 或不同真实节点的共同总预算，不另记作 half 推进。

在刚性成立且 n≥2 时，还可精确保留原固定背景的返还。T→B 后，背景总份额的变化为

\[
\Delta P_{\rm old}
=\sum_{\substack{x\in T\setminus B\\b_x>0}}\frac1{b_x+1}
-\sum_{x\in B\setminus T}\frac{b_x}{(b_x+n-1)(b_x+n)}.
\]

加上当前不变和其余 n−1 位尾玩家共损失 (n−1)ε_T 得

\[
\Delta W=\Delta P_{\rm old}-(n-1)\varepsilon_T
=-|\{x\in T\setminus B:b_x=0\}|.
\]

因此没有漏掉旧背景利润：原来仅由 T 新覆盖且旧背景为零的客户恰是切换后的覆盖损失，其余 T\B 的背景返还也有明确位置。此守恒仍是两条互斥真实叶之间的账，不自动为祖先其他动作提供付款。
