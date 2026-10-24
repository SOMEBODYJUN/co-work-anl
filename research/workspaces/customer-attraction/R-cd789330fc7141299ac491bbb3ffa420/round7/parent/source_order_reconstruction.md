# fresh 初始化的源时间界：root 独立重构

2026-10-24。收到 coupling7 的精确陈述后、读取其证明正文前完成下述重构。不是完全盲题发现，且已有 round5 causal interval / round6 HIT 是共同来源。只审下列结构命题，不审 actual cap。

## 域及不变量

固定原全历史 SPE 和实际终局 Z。每个源客户在实际覆盖集 C 外，源标签为 owner k，在实际前缀 Z_<k 强制一个包含该客户的主题。它在该真实叶的 current/future coverers 间均分，没有 past coverer；future 份额送真实 prescribed context。采用完整客户利润分母及 SAFE 或合法 CLIP 子边删减；不混用修改分母而未经再证 PRICE 的变体。

对每一份保留源标签 k 的输入，当前 context (g,i) 的历史 g 在 k 以前与 Z 相同。初始化时成立。重置在 i 强制当前规定主题，得到 A=finish(Z_<i,a)，新 future context j>i 的历史在 i 以前与 Z 相同，故仍在 k 以前相同。源可在 merge 后保留分析标签并线性拆分，客户重采不破坏历史不变量。

正 past recipient j<i 必须满足 A_j 覆盖当前某客户而旧 B_j 不覆盖。若 j<k，A_j=B_j=Z_j，矛盾；所以 past 出口 j≥k。当前出口 i≥k，future 后续同样保持。初始 current 亦为 k。因此源 k 的一切最终实际角色 j≥k。若某 context 恰为实际前缀，B=A=Z、正边为零，只终止在其当前角色，不制造逆时间出口。零利润 context 不能承载正输入；u_i=0 也无合法正当前金额。空主题/零客户按零量处理。

## 后缀角色集合界

固定源 k，将同一 PRICE / HIT 归纳限制到 [k,m] 中的可达角色。任意 K 令 h_k=|K∩[k,m]|/(1+|K∩[k,m]|)。源 k 若不在 K：对未来 context 当前不在 K，其 future recipient 在 K 时后续值≤1，其他≤h_k；past 出口在 K 时1、否则0。PRICE 的 uniform-subset 行对至多 |K∩[k,m]| 个目标角色给值≤h_k。按 future 角色逆序闭合；初始 fresh 均分行同理。源 k 若在 K，只用终值≤1。线性求和得到

    A(K) ≤ Σ_(k∈K) M_k + Σ_(k∉K) M_k |K∩[k,m]|/(1+|K∩[k,m]|)。

K=[1,l] 时 k>l 没有可达目标，故 A([1,l])≤Σ_(k≤l)M_k。对非增非负价格 p，逐源 p_final≤p_k，因此 Σ_j p_j A_j≤Σ_k p_k M_k。一般价格的 layer-cake 可用上述 suffix-HIT 逐源积分。这里 M 是来源质量，绝不能改写成 u。

## 范围反检查

全 O 初始化不具此时间界：m2、N={x}、唯一主题{x}的唯一完整 SPE，给 x 选 owner2，则初始化的一半立即支付 past 角色1。没有客户重采或策略平局问题。故不能将 fresh 结论套到全 O 的 cap2 图。

此证明不使用 off-history slack ell≥0，不能补全一般半覆盖，也不能证明全部 R≤W。它是因果区间与全图 HIT 的综合推论。待与作者正文逐项对照后另记结果。

## 对稿结论

独立重构落盘后读取作者 [source-order 正文](../coupling/fresh_source_order_and_suffix_hits.md)。SOURCE-ORDER、ORDERED-HIT 和 PRICE 的域、方向均一致；价格显示式由层积分展开为 lambda_k/(l+1)+Σ lambda_(s)/(s(s+1))，含 l=0。无致命异议。作者明确其为已有因果区间与 HIT 的综合推论，不认领新颖性；root同意此定位。审查不包含新实际钱包不等式，因为正文也没有这样的结论。
