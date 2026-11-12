# Boss1：第二源第三帽减量的完整连续族

RUN `six-boss1-20261111`；实际 agentID `/root/source2_cap3_tradeoff`。

本包只处理指定 δ∈{0,1/144}、s∈{0,61273/6912,9}、q₀∈{1/6,1/5} 和完整闭区间 h∈[0,β3原值]。从真实 COST 独立求全部16尾最小值，未读取候选点、最优面或登记缓存，优化调用为0。

## 完成结果

- [proof.md](source2_cap3_tradeoff/proof.md)：真实付款、完整解析包络、一般T和ordered整段身份、C-only完整冗余证明。
- [exact_family.json](source2_cap3_tradeoff/exact_family.json)：186条完整513列端点行；八合法T144条、C-only18条、ordered24条。
- [affine_family.json](source2_cap3_tradeoff/affine_family.json)：126条完整513列截距/斜率段行及端点凸组合身份。
- [exact_envelopes.json](source2_cap3_tradeoff/exact_envelopes.json)：192个真实物理条件、3072条尾仿射式、全弱态和72个零长最优区间。
- [literal_checker_output.json](source2_cap3_tradeoff/literal_checker_output.json)：独立标准库 Fraction 检查全部 PASS。
- [freeze_manifest.json](source2_cap3_tradeoff/freeze_manifest.json) 与 [SHA256SUMS](source2_cap3_tradeoff/SHA256SUMS)：完整冻结记录与校验和。

## 有用数学

减帽唯一改变 Ψ_h=Ψ_0−h r3。对 t=1，任何 r3=0 尾补入 r3 都使首项下降至少1/2，而帽增加至多59881/414720<1/2，查询项亦不增，故所有真最优尾都有 r3=1，m1(h)=m1(0)−h。对 t=0 必须支付新的真实条件损失。

令 τ4=x，τ5=y，H6=(1/6)(1/3+x/30+y/12)。任意合法 T 的完整整段身份为

\[
R_T(h)=R_T(0)-h(K-|T|)
+h|O\cap T^c\cap A1^c|
+[h-H_6]_+|O\cap T^c\cap A1|.
\]

对 C-only，用减帽后自由乘子 μ=S(h)−s/5 加 `E_C=|C|−K`，准确得到

\[
R_C^{only}(h)=R_C^{only}(0)
+h|O\cap C^c\cap A1^c|
+[h-H_6]_+|O\cap C^c\cap A1|.
\]

因此 C-only 整个新连续子支是旧同参数行加非负客户质量，可以凭该身份关闭；一般 T 的负帽差仍保留，不能跟着删除。

Ordered 全部物理 m 求出后再计算全部六个 f_d。整段准确有 `f_d−f_1≥(d−1)146807/414720>0`，d=1 唯一最弱；所有540个分段重数对无交点。令 H5=(1/5)(1/3+x/30+y/12)，则

\[
G_h(0)=G_0(0)-h,\qquad
G_h(1)=G_0(1)-h/6-(5/6)[h-H_5]_+.
\]

## 全部公共断点

三个 s 共用同一 mode、δ 下的断点，所有闭端点弱态保留。

| 族 | δ | 全部 h 断点 |
|---|---:|---|
| 纯 | 0 | 0，90577/1244160，59833/497664 |
| 纯 | 1/144 | 0，90649/1244160，59881/497664 |
| ordered | 0 | 0，63143/2073600，90577/1036800，59833/414720 |
| ordered | 1/144 | 0，63191/2073600，90649/1036800，59881/414720 |

Ordered 的较小内断点只改变真实的 d=2 条件，其端点行仍保存，并另核为0与H5行的准确凸组合。

## 与旧包的关系

逐513列比较指定旧180条端点行及3条 ordered ε 检查行：本包恰60条 h=0 行相同，126条正 h 行没有字面重复，186个新输出端点向量互异。其中12条正 h C-only 行有上述真正冗余身份；其余96条一般T和18条ordered正 h 端点，K 系数均严格低于对应旧δ连续族的最小 K 系数，只称相对于该族的字面新。没有宣称对全部已有约束的锥非冗余，也没有判断能否切任何新候选点。

独立检查覆盖95,418个端点列、129,276个仿射系数、16,896个全段尾态端点差、全部真实预算元数据与 free EC、全部物理重数和全部64索引菜单。失败记录为空。所有新增文本以且仅以一个换行结尾，无行末空格或 tab；冻结后停止写入，等待 Main 接回。
