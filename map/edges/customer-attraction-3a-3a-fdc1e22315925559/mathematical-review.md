# M-bb7d149596394020804ac192335b8678：保交叠必要行与真实路径补全边界

## 实读与对象范围

本任务按声明的 7 个 staged passes 读取同一反例正文的三个精确章节，以及 `new-product-completion-and-2016.json` 的六个连续区间。正文的对象是固定合法有序两人前缀后的末两人子局；证据 JSON 同时保存有限 product 构造检查、13 客户两人 completion 例和选定 60 原子的 2016 条必要行。未将 deferred 的 `M-e960d7f4ebca40a38760eb3ae044cc19` 提升为前提。

## 精确数学结果

固定前缀后，令
\[
f(T)=\sum_x(b_x+1)^{-1},\quad g(T,Q)=\sum_{x\in T\cap Q}[(b_x+1)(b_x+2)]^{-1},\quad U(T,Q)=f(T)-g(T,Q).
\]
末位最佳回复为 `BR(T)=argmax_Q U(Q,T)`，进入者在给定首主题 `T` 下的最坏可信收益为 `L(T)=min_{Q∈BR(T)}U(T,Q)`，`G=max_T L(T)`。一条广告路径 `(A,B)` 能在该固定前缀后补成两人完整纯 SPE，当且仅当 `B∈BR(A)` 且 `U(A,B)≥G`。必要性来自根 IC 与每个孩子的末位最佳回复；充分性只是在有限两人子局逐个有序孩子指定实现 `L(T)` 的回复。该准则不支付到达前缀之前的祖先 IC，也不允许任意改写另一个完整策略的孩子。

13 个单位客户分成 `A-only=2`、`A∩T=2`、`T-only=4`、`B-only=5`，目录为 `A,B,T`。广告 `(A,B)` 的覆盖为 9，正文给出的九条保交叠查询 slack 全部非负，且 `B∈BR(A)`；但 `T` 在 A 后的进入者收益为 6，相对 A 的 4 有严格 `+2`，所以 `(A,B)` 不是 SPE。三主题的 `L` 值为 `L(A)=3,L(B)=5,L(T)=6`，门槛 `G=6` 只接受 `(T,B)`。完整形式策略枚举得到 2 个 SPE，它们的实际有序路径都为 `(T,B)`，覆盖 `W=11`，同时是两主题静态最优 `OPT=11`。这个例子准确说明“所有保交叠必要行非负”仍不能推出给定广告路径可补全；它不是六人 half 反例。

同一证据还报告 `K=1..5,r=0..5` 的 30 个有限 product 情形，共 461 个 balanced count vectors、24 个构造 product 和 44 个有序结果。解析证明给出一般 iff，但有限扫描不证明 product optimum；其中 `(K,r)=(3,2),(3,5),(4,3),(5,2),(5,3),(5,4)` 的 `product_attainment_by_proved_condition=false`。在 `(K,r)=(3,2)` 中，构造查询值为 `(1,-1/2)`，孤立区间为 `[63/100,16/25]`，最小多项式为 `2t^2+5t-4`。

选定 60 atoms 与 21 菜单列表的 `new60_2016` 有 2016 条有限必要行：Cartesian 1386、own-index diagonal/off-diagonal 420、direct 210；120960 个原子系数。2016 个总 slack 全部非负，最小为 0，恰 10 条为零。JSON 明确没有重算 old557/GO220，因此该检查不能扩张成完整策略搜索、普适福利保证或 product optimum。

## 还欠什么

当前结果支付的是固定两人 completion criterion、13 客户精确路径障碍、有限 product 枚举边界和选定 60 原子的 2016 行非负核验。它没有给出祖先节点 IC、全目录/全历史 pure SPE、六人 `2W≥OPT_6`、普遍 half 或 product optimum。正文列出的旧 70-policy、61-atom negative cuts、GX53/100 full trees 与 GO557/cross220 记录仍未新核验；这些缺口不能被本包的有限非负 slack 填平。
