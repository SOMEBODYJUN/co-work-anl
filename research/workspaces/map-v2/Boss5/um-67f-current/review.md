# 67f 固定 g 的 MinRep 源审读

本包核心 M-8b63c8bed3d44f34a50cc846cc98d80a v1，pin 0a7443fbb503448d27919bd02589188e155ea9faec436fea6b9f9d1eee17f203。父 Boss 已追加并确认发布只读依赖 M-8c360a7779154480879e38c65d1f827e v1，pin 3dd4454f24e6ace08f116048d88ada39f73596fb57ae251b1d7b61568079281d。未操作 Git、认领、共享 registry 或源正文。

## 完成的数学关系

新增 `um-67f-fixed-chan-interface-and-sparsification-imply-minrep-gap`，accepted / conditional / whole。明确外部 Chan/Laekhanukit 正规 PCP 接口与已登记稀疏化共同支持核心，不把稀疏化算法保证独自当成 NP-hardness。

先固定 g，再取 q/ln q>10⁵Cg²，s=C ln q/q、γ=2s、Q=q²、Δ=10⁶·2ln(2Q)/sqrtγ、ε=1/Δ、δ=min{ε,s/2}。上游 YES≥1−δ≥1−ε，NO<s+δ≤3s/2<γ<10⁻⁴/g²。于是 YES 以至少0.9概率 OPT≤2N；NO 以至少0.9概率对所有输出后列表同时给 OPT>0.06N/sqrtγ>6gN>2gN。q=Θ(g²ln g)给 Q=O(g⁴ln²g)、Δ=O(g ln g)。N为已正规化源规模，YES与NO分别在各自承诺输入计概率；近完美YES没有升级为每个seed singleton。

精确编码复核：按现有正文§3取固定整数预算 Δ̂≥Δ 且 Δ̂≤Δ+2，设置 ε=1/Δ̂ 和 p=10⁻⁴Δ̂/D。原4.1、4.3–4.4的成功率至少0.98，YES为至少0.9999。每边用 b=ceil(log₂(100M)) 位将 p 向下舍入到二进制网格，采样分布总变差至多 M·2⁻ᵇ≤0.01，保住本对象所需0.9；随机位总数 O(M log M)。这说明固定参数显示式不依赖精确采样无理概率。低度直出支不含采样。

## 实际阅读与旧成果

实读任务、两端当前登记、共同正文全文§1–8，SHA 187fcaeed9bc5f98d04f60b9a137c7c117707674a670bed95d876a2529971217。重新pdftotext并全文读取冻结Manurangsi PDF全部9页；文本31,835字符/32,875 UTF-8字节，PDF 134,108字节，SHA 259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8。印4、5、7页实际视图复核。未重新阅读Chan或Laekhanukit外部全证明。

按核心ID检索现有边与收据，仅有现有 `minrep-gap-transfers-to-rooted-vertex-connectivity` 出边；不重造它。现有MZ参数修复、正规化桥及其后联合源边的目标是 M-fb633…，不是本核心的无条件替代证明；本轮只辨别其范围，不冒称新实读MZ PDF。未发现67f本人旧稿。

## 已核边界与接续

原PDF印4的δ、印5–6的pΔn、印7尾界及γ字面域等错误都已经在当前正文修复；本轮无新增源勘误。若要取消本边的conditional限定，需要实际重核并完整接入Chan/Laekhanukit正规化源接口；这不是稀疏化本身的结论。

本任务没有指定follow-up对象对，此次内部关系已闭合。partial-MinRep线性度、高围长、typed质量复制、Minzer–Zheng较小字母表及ordinary UM都不由本源自动推出，未将这些背景强行接成逻辑边。

交付文件：`map/edges/unrelated-machines-3a-3a-67f21b35ba26bbc2/sparsification-with-fixed-chan-interface-to-minrep-gap.json` 与 `map/receipts/unrelated-machines-3a-3a-67f21b35ba26bbc2.json`。edge-bind/edge-check通过，proof_scope=whole；本地coverage、follow-up空义务、资产哈希和端点范围检查通过。
